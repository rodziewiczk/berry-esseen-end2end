"""Offline runtime integrity fixtures; never evaluate original mathematics."""
from contextlib import redirect_stdout
import hashlib
import importlib.util
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('offline_runtime_under_test', ROOT/'tools/local_notebook_runtime.py')
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


class OfflineRuntime(unittest.TestCase):
    def setUp(self):
        (ROOT/'work').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT/'work')
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.source = self.root/'source'
        for name, raw in {
            'be_replay/__init__.py': b'',
            'be_replay/environment.py': b'def snapshot(): return {"scope":"SYNTHETIC_ONLY"}\n',
            'tools/make_notebooks.py': b'# synthetic source fixture\n',
            'proof/input.json': b'{"exact":"1/3"}\n',
        }.items():
            path = self.source/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        self.packet = self.root/'source.zip'
        self.content = self.root/'content'
        self.content.mkdir()
        self.report = runtime.build(self.packet, root=self.source)
        self.copied = self.content/self.packet.name
        self.copied.write_bytes(self.packet.read_bytes())

    def execute(self, *, source_sha=None, upload=None):
        google = types.ModuleType('google')
        colab = types.ModuleType('google.colab')
        colab.files = types.SimpleNamespace(upload=upload or mock.Mock(side_effect=AssertionError('Unexpected upload')))
        google.colab = colab
        code = runtime.bootstrap(self.packet.name, source_sha or self.report['sha256'], 'fixture')
        code = code.replace("Path('/content')", 'Path('+repr(str(self.content))+')')
        saved = {key: value for key, value in sys.modules.items()
                 if key == 'be_replay' or key.startswith('be_replay.')}
        path = sys.path[:]
        bytecode = sys.dont_write_bytecode
        try:
            with mock.patch.dict(sys.modules, {'google': google, 'google.colab': colab}), redirect_stdout(StringIO()):
                namespace = {}
                exec(compile(code, 'offline-runtime-fixture', 'exec'), namespace)
            return namespace
        finally:
            for key in tuple(sys.modules):
                if key == 'be_replay' or key.startswith('be_replay.'):
                    del sys.modules[key]
            sys.modules.update(saved)
            sys.path[:] = path
            sys.dont_write_bytecode = bytecode

    def test_actual_manifest_roundtrip_no_upload_and_no_kernel(self):
        namespace = self.execute()
        self.assertEqual(namespace['snapshot'](), {'scope': 'SYNTHETIC_ONLY'})
        self.assertTrue((namespace['CODE']/'work').is_dir())
        self.assertEqual(self.report['source_files'], 4)
        self.assertEqual(hashlib.sha256(self.packet.read_bytes()).hexdigest(), self.report['sha256'])
        self.assertFalse(self.report['original_mathematics_executed'])

    def test_changed_runtime_source_and_extra_helper_are_rejected(self):
        namespace = self.execute()
        path = namespace['CODE']/'proof/input.json'
        original = path.read_bytes()
        path.write_bytes(b'{}')
        with self.assertRaisesRegex(RuntimeError, 'Changed runtime source'):
            self.execute()
        path.write_bytes(original)
        (namespace['CODE']/'be_replay/unbound.py').write_text('pass\n')
        with self.assertRaisesRegex(RuntimeError, 'Unexpected runtime helper'):
            self.execute()

    def test_partial_existing_extraction_cannot_resume_as_complete(self):
        code = self.content/('berry-esseen-local-'+self.report['sha256'][:20])
        code.mkdir()
        (code/'LOCAL_RUNTIME_MANIFEST.json').write_text('{}')
        with self.assertRaisesRegex(RuntimeError, 'Changed local source manifest'):
            self.execute()

    def test_outer_pin_and_inner_source_digest_both_required(self):
        upload = mock.Mock(return_value={self.packet.name: b'wrong'})
        with self.assertRaisesRegex(RuntimeError, 'exact local source ZIP'):
            self.execute(source_sha='1'*64, upload=upload)
        with zipfile.ZipFile(self.packet) as packet:
            records = {name: packet.read(name) for name in packet.namelist()}
        records['proof/input.json'] = b'{"forged":true}'
        with zipfile.ZipFile(self.copied, 'w') as packet:
            for name, raw in records.items():
                packet.writestr(name, raw)
        forged_pin = runtime.digest(self.copied)
        with self.assertRaisesRegex(RuntimeError, 'manifest mismatch'):
            self.execute(source_sha=forged_pin)

    def test_new_source_package_never_overwrites_and_excludes_notebooks(self):
        (self.source/'tools/ignored.ipynb').write_text('{}')
        with self.assertRaises(FileExistsError):
            runtime.build(self.packet, root=self.source)
        other = self.root/'other.zip'
        runtime.build(other, root=self.source)
        with zipfile.ZipFile(other) as packet:
            self.assertNotIn('tools/ignored.ipynb', packet.namelist())
            ledger = json.loads(packet.read(runtime.MANIFEST))
            self.assertFalse(ledger['generated_notebooks_included'])

    def test_canonical_names_and_literal_fixed_configuration(self):
        for name in ('../escape.zip', '/x.zip', 'a\\x.zip', 'C:x.zip', 'x//y.zip', 'a/./x.zip', 'x\0.zip'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                runtime.safe_name(name)
        for name, pin, task in [('a/b.zip', '1'*64, 'ok'), ('ok.zip', 'x'*64, 'ok'), ('ok.zip', '1'*64, 'bad task')]:
            with self.assertRaises(ValueError):
                runtime.bootstrap(name, pin, task)

    def test_finish_accepts_both_real_export_shapes(self):
        spec = importlib.util.spec_from_file_location('finish_fixture_base', ROOT/'tools/make_notebooks.py')
        base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
        for packet in ('/drive/result.zip', {'path':'/drive/result.zip', 'sha256':'a'*64}):
            with self.subTest(packet=packet):
                events = []
                google = types.ModuleType('google')
                colab = types.ModuleType('google.colab')
                colab.files = types.SimpleNamespace(download=lambda path: events.append(('download', path)))
                google.colab = colab
                ipython = types.ModuleType('IPython')
                display = types.ModuleType('IPython.display')
                display.FileLink = lambda path: ('link', path)
                display.display = lambda value: events.append(value)
                with mock.patch.dict(sys.modules, {'google':google, 'google.colab':colab,
                        'IPython':ipython, 'IPython.display':display}), redirect_stdout(StringIO()):
                    exec(compile(''.join(base.finish()['source']), 'finish-fixture', 'exec'),
                         {'RESULT':{'status':{'state':'SYNTHETIC_ONLY'}, 'bundle':packet}})
                self.assertEqual(events, [('link','/drive/result.zip'), ('download','/drive/result.zip')])


if __name__ == '__main__':
    unittest.main()
