"""56F compilation and fake Run all API routing; no original mathematics."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1014_coarse_notebook_builder',ROOT/'tools/make_finite1014_coarse_notebook.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
PIN='a'*40

def cell(d,name):return ''.join(next(c['source']for c in d['cells']if c['id']==name))


class Notebook56F(unittest.TestCase):
    def test_pin_complete_census_required_premises_and_fixture_gate(self):
        d=builder.build(PIN);intro=cell(d,'instructions')
        self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(d,'pinned-code'))
        for token in('part 56F','81 original static inputs','20 malformed-scope','2 parser','Ten literal','9–13','209/500','unacquired','capture bridge'):
            self.assertIn(token,intro)
        self.assertIn('test_finite1014_coarse_*.py',cell(d,'finite1014-fixtures'))
        self.assertIn('raise RuntimeError',cell(d,'finite1014-fixtures'))
        ids=[c['id']for c in d['cells']]
        self.assertLess(ids.index('finite1014-fixtures'),ids.index('execute-task'))
        self.assertNotIn('planner-dependency',ids)
        for c in d['cells']:
            if c['cell_type']=='code':compile(''.join(c['source']),'56F','exec')

    def test_only_exact_runner_receives_same_drive(self):
        calls=[];module=types.ModuleType('be_replay.finite1014_coarse')
        def fake(**kw):calls.append(kw);return dict(status={'all_index_conclusion_verified':False},bundle='synthetic.zip')
        module.run_colab=fake
        with patch.dict(sys.modules,{module.__name__:module}):
            ns={'DURABLE':Path('/synthetic/drive')};exec(compile(cell(builder.build(PIN),'execute-task'),'fake56F','exec'),ns)
        self.assertEqual(calls,[dict(durable_root=Path('/synthetic/drive'),backup_interval=60)])
        self.assertIs(ns['RESULT']['status']['all_index_conclusion_verified'],False)

    def test_invalid_pin_no_outputs_and_lf_writer_only56f(self):
        with tempfile.TemporaryDirectory()as tmp:
            dest=Path(tmp)/'out'
            for pin in(None,True,'main','0'*40,'A'*40,'a'*39):
                with self.assertRaises(ValueError):builder.write(pin,dest)
                self.assertFalse(dest.exists())
            p=builder.write(PIN,dest)
            self.assertEqual([x.name for x in dest.iterdir()],['56F_n10_14_coarse_support.ipynb'])
            self.assertNotIn(b'\r\n',p.read_bytes())


if __name__=='__main__':unittest.main()
