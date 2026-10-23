"""Notebook metadata and fake routing only; no original numerical imports."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1014_notebook_builder',ROOT/'tools/make_finite1014_supported_notebook.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
PIN='a'*40
def cell(d,name):return ''.join(next(c['source']for c in d['cells']if c['id']==name))


class Notebook56B(unittest.TestCase):
    def test_exact_pin_separate_scope_and_failure_gate(self):
        d=builder.build(PIN)
        self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(d,'pinned-code'))
        self.assertIn('part 56B',cell(d,'instructions'))
        for text in ('97 original inputs','94-row','1049/2500','52/125','not acquired here','217 count interfaces'):
            self.assertIn(text,cell(d,'instructions'))
        self.assertIn('test_finite1014_supported*.py',cell(d,'finite1014-fixtures'))
        self.assertIn('raise RuntimeError',cell(d,'finite1014-fixtures'))
        for variable in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
            self.assertIn(variable,cell(d,'planner-dependency'))
        ids=[c['id']for c in d['cells']]
        self.assertLess(ids.index('planner-dependency'),ids.index('execute-task'))
        self.assertLess(ids.index('finite1014-fixtures'),ids.index('execute-task'))
        for c in d['cells']:
            if c['cell_type']=='code':compile(''.join(c['source']),'56B','exec')

    def test_only_declared_runner_receives_same_drive(self):
        calls=[];module=types.ModuleType('be_replay.finite1014_supported')
        def fake(**kw):calls.append(kw);return dict(status={'all_index_conclusion_verified':False},bundle='synthetic.zip')
        module.run_colab=fake
        with patch.dict(sys.modules,{module.__name__:module}):
            ns={'DURABLE':Path('/synthetic/drive')};exec(compile(cell(builder.build(PIN),'execute-task'),'fake56B','exec'),ns)
        self.assertEqual(calls,[dict(durable_root=Path('/synthetic/drive'),backup_interval=60)])
        self.assertIs(ns['RESULT']['status']['all_index_conclusion_verified'],False)

    def test_bad_pin_has_no_output_and_writer_creates_only56b_lf(self):
        with tempfile.TemporaryDirectory()as tmp:
            dest=Path(tmp)/'out'
            for pin in(None,True,'main','0'*40,'A'*40,'a'*39):
                with self.assertRaises(ValueError):builder.write(pin,dest)
                self.assertFalse(dest.exists())
            p=builder.write(PIN,dest)
            self.assertEqual([x.name for x in dest.iterdir()],['56B_n10_14_supported_fourier.ipynb'])
            self.assertNotIn(b'\r\n',p.read_bytes())


if __name__=='__main__':unittest.main()
