"""New notebook metadata/fake routing only; never import original mathematics."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite69_caps_notebook',ROOT/'tools/make_finite69_caps_notebook.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
PIN='a'*40
def cell(doc,name):return ''.join(next(c['source']for c in doc['cells']if c['id']==name))


class Finite69CapsNotebook(unittest.TestCase):
    def test_pinned_preflight_and_gate_before_routing(self):
        d=builder.build(PIN);ids=[c['id']for c in d['cells']]
        self.assertLess(ids.index('finite69-caps-fixtures'),ids.index('numpy-discovery-preflight'))
        self.assertLess(ids.index('numpy-discovery-preflight'),ids.index('execute-task'))
        self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(d,'pinned-code'))
        self.assertIn('raise RuntimeError',cell(d,'finite69-caps-fixtures'))
        self.assertIn('test_finite69_cap*.py',cell(d,'finite69-caps-fixtures'))
        self.assertIn('numpy.__version__',cell(d,'numpy-discovery-preflight'))
        for c in d['cells']:
            if c['cell_type']=='code':compile(''.join(c['source']),'notebook46','exec')

    def test_only_intended_runner_is_called_with_same_durable_root(self):
        calls=[];module=types.ModuleType('be_replay.finite69_caps')
        def fake(**kw):calls.append(kw);return dict(status={'all_index_conclusion_verified':False},bundle='fake.zip')
        module.run_colab=fake
        with patch.dict(sys.modules,{module.__name__:module}):
            namespace={'DURABLE':Path('/synthetic/drive')}
            exec(compile(cell(builder.build(PIN),'execute-task'),'fake46','exec'),namespace)
        self.assertEqual(calls,[dict(durable_root=Path('/synthetic/drive'),backup_interval=60)])
        self.assertIs(namespace['RESULT']['status']['all_index_conclusion_verified'],False)

    def test_invalid_pin_cannot_create_output_and_valid_write_is_only46(self):
        (ROOT/'work').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'work')as tmp:
            dest=Path(tmp)/'out'
            for pin in [None,True,'main','0'*40,'A'*40,'a'*39]:
                with self.assertRaises(ValueError):builder.write(pin,dest)
                self.assertFalse(dest.exists())
            p=builder.write(PIN,dest)
            self.assertEqual([x.name for x in dest.iterdir()],['46_n7_9_conditional_caps_resources.ipynb'])
            self.assertNotIn(b'\r\n',p.read_bytes())


if __name__=='__main__':unittest.main()
