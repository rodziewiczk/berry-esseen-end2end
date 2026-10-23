"""New notebook metadata/fake routing only; no original mathematics imports."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite2630_notebook_builder',ROOT/'tools/make_finite2630_notebook.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
PIN='a'*40
def cell(d,name):return ''.join(next(c['source']for c in d['cells']if c['id']==name))


class Notebook53(unittest.TestCase):
    def test_exact_selection_census_pin_and_failure_gate(self):
        d=builder.build(PIN);selection=json.loads((ROOT/'proof/finite2630_selection.json').read_bytes())
        self.assertEqual(selection['complete_census'],dict(forests=80,roots=2316,nodes=150296,leaves=76306))
        self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(d,'pinned-code'))
        self.assertIn('raise RuntimeError',cell(d,'finite2630-fixtures'))
        self.assertIn('test_finite2630*.py',cell(d,'finite2630-fixtures'))
        ids=[c['id']for c in d['cells']];self.assertLess(ids.index('finite2630-fixtures'),ids.index('execute-task'))
        for c in d['cells']:
            if c['cell_type']=='code':compile(''.join(c['source']),'notebook53','exec')

    def test_execution_routes_same_drive_to_only_new_isolated_runner(self):
        calls=[];module=types.ModuleType('be_replay.finite2630_counts')
        def fake(**kw):calls.append(kw);return dict(status={'all_index_conclusion_verified':False},bundle='synthetic.zip')
        module.run_colab=fake
        with patch.dict(sys.modules,{module.__name__:module}):
            ns={'DURABLE':Path('/synthetic/drive')};exec(compile(cell(builder.build(PIN),'execute-task'),'fake53','exec'),ns)
        self.assertEqual(calls,[dict(durable_root=Path('/synthetic/drive'),backup_interval=60)])
        self.assertIs(ns['RESULT']['status']['all_index_conclusion_verified'],False)

    def test_bad_pin_cannot_create_output_and_writer_creates_only53_lf(self):
        (ROOT/'work').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'work')as tmp:
            dest=Path(tmp)/'out'
            for pin in (None,True,'main','0'*40,'A'*40,'a'*39):
                with self.assertRaises(ValueError):builder.write(pin,dest)
                self.assertFalse(dest.exists())
            p=builder.write(PIN,dest)
            self.assertEqual([x.name for x in dest.iterdir()],['53_n26_30_conditional_counts.ipynb'])
            self.assertNotIn(b'\r\n',p.read_bytes())


if __name__=='__main__':unittest.main()
