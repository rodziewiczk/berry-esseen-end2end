"""Shutdown-cell tests use fake Colab modules; they never terminate a real session."""
from __future__ import annotations

import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock
from contextlib import redirect_stdout

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load('shutdown_test_builder', ROOT / 'tools/make_notebooks.py')
retrofit = load('shutdown_test_retrofit', ROOT / 'tools/add_shutdown_cells.py')


class ShutdownCellTests(unittest.TestCase):
    def execute_cell(self, *, hosted=True, mounted=False, flush_error=None, sync_error=None, shutdown_error=None):
        self.events = []
        google = types.ModuleType('google')
        google.__path__ = []
        colab = types.ModuleType('google.colab')
        drive = types.ModuleType('google.colab.drive')
        runtime = types.ModuleType('google.colab.runtime')

        def sync():
            self.events.append('sync')
            if sync_error:
                raise sync_error

        def flush_and_unmount(*, timeout_ms):
            self.events.append(('flush_and_unmount', timeout_ms))
            if flush_error:
                raise flush_error

        def unassign():
            self.events.append('unassign')
            if shutdown_error:
                raise shutdown_error

        drive.flush_and_unmount = flush_and_unmount
        runtime.unassign = unassign
        google.colab = colab
        colab.drive, colab.runtime = drive, runtime
        modules = {'google': google, 'google.colab': colab,
                   'google.colab.drive': drive, 'google.colab.runtime': runtime}
        env = dict(os.environ)
        env.pop('TBE_RUNTIME_ADDR', None)
        if hosted:
            env['TBE_RUNTIME_ADDR'] = 'fake-test-only'
        self.output = io.StringIO()
        with mock.patch.dict(sys.modules, modules), mock.patch.dict(os.environ, env, clear=True), \
                mock.patch('os.sync', sync, create=True), redirect_stdout(self.output):
            exec(compile(''.join(builder.shutdown()['source']), '<shutdown-cell>', 'exec'),
                 {'BERRY_ESSEEN_DRIVE_MOUNTED': mounted})

    def test_success_flushes_before_unassign(self):
        self.execute_cell()
        self.assertEqual(self.events, ['sync', ('flush_and_unmount', 300_000), 'unassign'])

    def test_successful_drive_mount_licenses_shutdown_without_optional_environment_marker(self):
        self.execute_cell(hosted=False, mounted=True)
        self.assertEqual(self.events, ['sync', ('flush_and_unmount', 300_000), 'unassign'])

    def test_drive_failure_never_unassigns(self):
        with self.assertRaisesRegex(RuntimeError, 'flush failed'):
            self.execute_cell(flush_error=RuntimeError('flush failed'))
        self.assertEqual(self.events, ['sync', ('flush_and_unmount', 300_000)])

    def test_local_sync_failure_never_unassigns(self):
        with self.assertRaisesRegex(OSError, 'sync failed'):
            self.execute_cell(sync_error=OSError('sync failed'))
        self.assertEqual(self.events, ['sync'])

    def test_unassign_failure_is_not_hidden(self):
        with self.assertRaisesRegex(RuntimeError, 'backend unavailable'):
            self.execute_cell(shutdown_error=RuntimeError('backend unavailable'))
        self.assertEqual(self.events[-1], 'unassign')

    def test_outside_managed_colab_does_not_flush_or_shutdown(self):
        self.execute_cell(hosted=False)
        self.assertEqual(self.events, [])
        self.assertIn('skipping shutdown', self.output.getvalue())

    def test_generator_appends_after_result_download(self):
        cells = [builder.cell('markdown', '# Test', 'instructions'), builder.finish()]
        before = copy.deepcopy(cells)
        doc = builder.notebook(cells, 'test.ipynb')
        self.assertEqual(cells, before)
        self.assertEqual(doc['cells'][:-1], before)
        self.assertEqual(doc['cells'][-2]['id'], 'download-result')
        self.assertEqual(doc['cells'][-1], builder.shutdown())

    def test_append_is_idempotent_and_moves_shutdown_to_end(self):
        original = [builder.shutdown(), builder.finish(), builder.shutdown()]
        result = builder.with_shutdown(original)
        self.assertEqual([c['id'] for c in result], ['download-result', 'shutdown-runtime'])
        self.assertEqual(builder.with_shutdown(result), result)
        self.assertEqual(len(original), 3)

    def test_shutdown_does_not_import_project_or_change_result(self):
        source = ''.join(builder.shutdown()['source'])
        self.assertNotIn('be_replay', source)
        self.assertNotIn('RESULT =', source)
        self.assertNotIn('kill', source)
        self.assertNotIn('finally:', source)

    def test_all_shipped_notebooks_have_exact_final_cell(self):
        paths = sorted((ROOT / 'colab').rglob('*.ipynb'))
        self.assertGreater(len(paths), 0)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                doc = json.loads(path.read_text())
                self.assertEqual(doc['cells'][-1], builder.shutdown())
                self.assertEqual(sum(c.get('id') == 'shutdown-runtime' for c in doc['cells']), 1)
                self.assertEqual(doc['cells'][-2]['id'], 'download-result')
                for cell in doc['cells']:
                    if cell['cell_type'] == 'code':
                        compile(''.join(cell['source']), str(path), 'exec')

    def test_retrofit_preserves_outputs_and_all_prior_cells(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'test.ipynb'
            original = {'nbformat': 4, 'nbformat_minor': 5, 'metadata': {'sentinel': 'keep'},
                        'cells': [builder.cell('code', 'print(17)\n', 'original')]}
            original['cells'][0].update(execution_count=7, outputs=[
                {'output_type': 'stream', 'name': 'stdout', 'text': ['17\n']}])
            p.write_text(json.dumps(original))
            original_bytes = p.read_bytes()
            self.assertTrue(retrofit.update_notebook(p, check=True))
            self.assertEqual(p.read_bytes(), original_bytes)
            self.assertTrue(retrofit.update_notebook(p))
            result = json.loads(p.read_text())
            self.assertEqual(result['cells'][:-1], original['cells'])
            self.assertEqual(result['metadata'], original['metadata'])
            first_bytes = p.read_bytes()
            self.assertFalse(retrofit.update_notebook(p))
            self.assertEqual(p.read_bytes(), first_bytes)
            self.assertFalse(retrofit.update_notebook(p, check=True))

    def test_invalid_notebook_remains_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'invalid.ipynb'
            p.write_text('{"nbformat":3,"cells":[]}')
            original = p.read_bytes()
            with self.assertRaises(ValueError):
                retrofit.update_notebook(p)
            self.assertEqual(p.read_bytes(), original)

    def test_symbolic_link_is_not_modified(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / 'target.ipynb'
            target.write_text('{"nbformat":4,"cells":[]}')
            original = target.read_bytes()
            link = Path(td) / 'link.ipynb'
            try:
                link.symlink_to(target)
            except OSError as error:
                if sys.platform == 'win32' and getattr(error, 'winerror', None) == 1314:
                    self.skipTest('Windows account cannot create symlinks; run this fixture on Linux')
                raise
            with self.assertRaises(ValueError):
                retrofit.update_notebook(link)
            self.assertEqual(target.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
