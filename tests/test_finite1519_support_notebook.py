"""Synthetic57D notebook routing and failure-gate fixtures."""
import importlib.util,sys,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1519_support_builder',ROOT/'tools/make_finite1519_support_notebook.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
PIN='a'*40
def cell(d,name):return ''.join(next(c['source']for c in d['cells']if c['id']==name))
class Notebook(unittest.TestCase):
 def test_scope_original_two_passes_controls_and_code_compile(self):
  d=b.build(PIN);text=cell(d,'instructions');self.assertTrue(text.isascii())
  for token in('57D','26 exact input','both complete support rays','14 malformed-candidate','2 parser','21/50','147 resource-to-count','All native'):
   self.assertIn(token,text)
  self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(d,'pinned-code'))
  for c in d['cells']:
   if c['cell_type']=='code':compile(''.join(c['source']),b.NAME,'exec')
 def test_fixture_gate_and_fake_routing(self):
  d=b.build(PIN);ids=[c['id']for c in d['cells']];self.assertLess(ids.index('support-fixtures'),ids.index('execute-task'))
  self.assertIn('raise RuntimeError',cell(d,'support-fixtures'));self.assertIn('test_finite1519_support*.py',cell(d,'support-fixtures'))
  m=types.ModuleType('be_replay.finite1519_support');calls=[]
  def fake(**kw):calls.append(kw);return{'status':{'all_index_conclusion_verified':False},'bundle':'SYNTHETIC.zip'}
  m.run_colab=fake
  with patch.dict(sys.modules,{m.__name__:m}):
   ns={'DURABLE':Path('/synthetic')};exec(compile(cell(d,'execute-task'),'synthetic','exec'),ns)
  self.assertEqual(calls,[dict(durable_root=Path('/synthetic'),backup_interval=60)])
  self.assertFalse(ns['RESULT']['status']['all_index_conclusion_verified'])
 def test_invalid_pin_before_output_and_lf_without_ignored_work(self):
  with tempfile.TemporaryDirectory()as tmp:
   dest=Path(tmp)/'out'
   for pin in(None,False,'main','0'*40,'A'*40):
    with self.assertRaises(ValueError):b.write(pin,dest)
    self.assertFalse(dest.exists())
   p=b.write(PIN,dest);self.assertEqual(p.name,'57D_n15_19_full_ray_support.ipynb');self.assertNotIn(b'\r\n',p.read_bytes())
if __name__=='__main__':unittest.main()
