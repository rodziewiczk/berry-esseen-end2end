"""Notebook structure/fake routing only; no original numerical imports."""
import importlib.util
from pathlib import Path
import sys,tempfile,types,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('join_notebook_builder',ROOT/'tools/make_finite1014_join_notebook.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
PIN='a'*40
def cell(doc,name):return ''.join(next(c['source']for c in doc['cells']if c['id']==name))


class Notebook56I(unittest.TestCase):
 def test_pin_full_scope_and_fixture_gate(self):
  doc=builder.build(PIN);intro=cell(doc,'instructions')
  for text in('234','217','202','1,000','twenty restrictions','23 hours','same-law supported n9','eventual n15','ten complete original'):
   self.assertIn(text,intro)
  self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(doc,'pinned-code'))
  fixture=cell(doc,'finite1014-join-fixtures');self.assertIn('test_finite1014_join*.py',fixture);self.assertIn('raise RuntimeError',fixture)
  ids=[c['id']for c in doc['cells']];self.assertLess(ids.index('finite1014-join-fixtures'),ids.index('execute-task'))
  self.assertNotIn('numpy',cell(doc,'execute-task'))
  for c in doc['cells']:
   if c['cell_type']=='code':compile(''.join(c['source']),'synthetic56I','exec')

 def test_only_declared_runner_receives_same_drive(self):
  calls=[];module=types.ModuleType('be_replay.finite1014_join')
  module.run_colab=lambda **kw:(calls.append(kw)or dict(status={'all_index_conclusion_verified':False},bundle='synthetic.zip'))
  with patch.dict(sys.modules,{module.__name__:module}):
   ns=dict(DURABLE=Path('/synthetic/drive'));exec(compile(cell(builder.build(PIN),'execute-task'),'fake56I','exec'),ns)
  self.assertEqual(calls,[dict(durable_root=Path('/synthetic/drive'),backup_interval=60)])
  self.assertIs(ns['RESULT']['status']['all_index_conclusion_verified'],False)

 def test_bad_pin_before_output_and_only56i_lf(self):
  with tempfile.TemporaryDirectory()as tmp:
   out=Path(tmp)/'out'
   for pin in(None,True,'main','0'*40,'A'*40,'a'*39):
    with self.assertRaises(ValueError):builder.write(pin,out)
    self.assertFalse(out.exists())
   path=builder.write(PIN,out);self.assertEqual([p.name for p in out.iterdir()],['56I_n10_14_finite_join.ipynb'])
   self.assertNotIn(b'\r\n',path.read_bytes())


if __name__=='__main__':unittest.main()
