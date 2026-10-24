"""59B/C generator scope/failure-gate/fake routing fixtures."""
import importlib.util,sys,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite2630_cover_builder',ROOT/'tools/make_finite2630_covers_notebooks.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
PIN='a'*40
def cell(d,name):return ''.join(next(c['source']for c in d['cells']if c['id']==name))
class Notebooks(unittest.TestCase):
 def test_both_complete_profiles_scope_and_all_code_compile(self):
  docs=b.build_all(PIN);self.assertEqual(set(docs),{'b2','higher'})
  for name,doc in docs.items():
   p=b.PROFILES[name];text=cell(doc,'instructions');self.assertTrue(text.isascii())
   for value in(p['label'],str(p['rows']),str(p['strips']),str(p['actions']),'48 original','34 active','both fresh passes','full package 59','53/64'):
    self.assertIn(value,text)
   self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(doc,'pinned-code'))
   for c in doc['cells']:
    if c['cell_type']=='code':compile(''.join(c['source']),p['name'],'exec')
 def test_exact_lane_routing_to_same_drive(self):
  for name in b.PROFILES:
   m=types.ModuleType('be_replay.finite2630_covers');calls=[]
   def fake(*a,**kw):calls.append((a,kw));return{'status':{'all_index_conclusion_verified':False},'bundle':'SYNTHETIC.zip'}
   m.run_colab=fake
   with patch.dict(sys.modules,{m.__name__:m}):
    ns={'DURABLE':Path('/synthetic')};exec(compile(cell(b.build(PIN,name),'execute-task'),'synthetic','exec'),ns)
   self.assertEqual(calls,[((name,),dict(durable_root=Path('/synthetic'),backup_interval=60))]);self.assertFalse(ns['RESULT']['status']['all_index_conclusion_verified'])
 def test_selftest_failure_gate_precedes_any_native_work(self):
  for name in b.PROFILES:
   doc=b.build(PIN,name);ids=[c['id']for c in doc['cells']];self.assertLess(ids.index('cover-fixtures'),ids.index('execute-task'))
   self.assertIn('raise RuntimeError',cell(doc,'cover-fixtures'));self.assertIn('test_finite2630_covers*.py',cell(doc,'cover-fixtures'))
 def test_bad_pin_before_output_two_lf_files_no_ignored_work_required(self):
  with tempfile.TemporaryDirectory()as tmp:
   dest=Path(tmp)/'out'
   for pin in(None,True,'main','0'*40,'A'*40):
    with self.assertRaises(ValueError):b.write(pin,dest)
    self.assertFalse(dest.exists())
   with self.assertRaises(ValueError):b.build(PIN,'not-selected')
   paths=b.write(PIN,dest);self.assertEqual(len(paths),2)
   self.assertEqual({p.name for p in paths},{p['name']+'.ipynb'for p in b.PROFILES.values()})
   for p in paths:self.assertNotIn(b'\r\n',p.read_bytes())
if __name__=='__main__':unittest.main()
