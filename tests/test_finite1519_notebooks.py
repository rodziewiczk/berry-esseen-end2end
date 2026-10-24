"""Notebook source and fake routing fixtures; no original numerical imports."""
import importlib.util,sys,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1519_builder',ROOT/'tools/make_finite1519_fourier_notebooks.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
PIN='a'*40

def cell(doc,name):return ''.join(next(c['source']for c in doc['cells']if c['id']==name))


class Notebooks57(unittest.TestCase):
 def test_all_three_exact_profiles_pin_and_compile(self):
  docs=builder.build_all(PIN);self.assertEqual(set(docs),{'auxiliary','supported','highrho'})
  for kind,d in docs.items():
   p=builder.PROFILES[kind];text=cell(d,'instructions')
   for value in(p['label'],'indices 14--19',str(p['files']),str(p['manifest'])+'-row','complete package 57','147 count-interface'):
    self.assertIn(value,text)
   self.assertTrue(text.isascii())
   self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(d,'pinned-code'))
   for c in d['cells']:
    if c['cell_type']=='code':compile(''.join(c['source']),p['name'],'exec')

 def test_each_fake_runner_gets_same_drive_without_other_parameters(self):
  for kind in builder.PROFILES:
   calls=[];m=types.ModuleType('be_replay.finite1519_'+kind)
   def fake(**kw):calls.append(kw);return dict(status={'all_index_conclusion_verified':False},bundle='synthetic.zip')
   m.run_colab=fake
   with patch.dict(sys.modules,{m.__name__:m}):
    ns={'DURABLE':Path('/synthetic/drive')};exec(compile(cell(builder.build(PIN,kind),'execute-task'),'synthetic','exec'),ns)
   self.assertEqual(calls,[dict(durable_root=Path('/synthetic/drive'),backup_interval=60)])
   self.assertIs(ns['RESULT']['status']['all_index_conclusion_verified'],False)

 def test_dependency_and_fixture_failure_gate_precede_execution(self):
  for kind in builder.PROFILES:
   d=builder.build(PIN,kind);ids=[c['id']for c in d['cells']]
   self.assertLess(ids.index('planner-dependency'),ids.index('execute-task'))
   self.assertLess(ids.index('finite1519-fixtures'),ids.index('execute-task'))
   self.assertIn('test_finite1519*.py',cell(d,'finite1519-fixtures'));self.assertIn('raise RuntimeError',cell(d,'finite1519-fixtures'))
   for name in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):self.assertIn(name,cell(d,'planner-dependency'))

 def test_bad_pin_no_output_and_three_lf_files_without_ignored_work(self):
  with tempfile.TemporaryDirectory()as tmp:
   dest=Path(tmp)/'out'
   for pin in(None,True,'main','0'*40,'A'*40,'a'*39):
    with self.assertRaises(ValueError):builder.write(pin,dest)
    self.assertFalse(dest.exists())
   with self.assertRaises(ValueError):builder.build(PIN,'unselected')
   paths=builder.write(PIN,dest);self.assertEqual(len(paths),3)
   self.assertEqual({p.name for p in paths},{p['name']+'.ipynb'for p in builder.PROFILES.values()})
   for p in paths:self.assertNotIn(b'\r\n',p.read_bytes())


if __name__=='__main__':unittest.main()
