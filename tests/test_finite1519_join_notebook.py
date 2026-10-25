"""57H complete offline wrapper scope and checksum-bound bootstrap."""
import importlib.util,json,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('test57Hgenerator',ROOT/'tools/make_finite1519_join_notebook.py')
maker=importlib.util.module_from_spec(spec);spec.loader.exec_module(maker)


class Notebook(unittest.TestCase):
 def test_real_local_bootstrap_full_controller_fixtures_and_shutdown(self):
  doc=maker.build_local('actual-source.zip','a'*64);cells=doc['cells'];text='\n'.join(''.join(c['source'])for c in cells)
  self.assertIn('SOURCE_SHA256 =',text);self.assertIn('actual-source.zip',text);self.assertIn('a'*64,text)
  self.assertIn('be_replay.finite1519_join import run_colab',text);self.assertIn('RESULT = run_colab(durable_root=DURABLE, backup_interval=60)',text)
  self.assertIn('test_finite1519_join*.py',text);self.assertIn('164',text);self.assertIn('147',text);self.assertIn('1000',text)
  self.assertIn('82800',text);self.assertNotIn('CODE_COMMIT =',text)
  tail=''.join(cells[-1]['source']);self.assertIn('flush_and_unmount',tail);self.assertIn('unassign',tail)
  self.assertLess(tail.index('flush_and_unmount'),tail.index('unassign'))
  for cell in cells:
   if cell['cell_type']=='code':compile(''.join(cell['source']),'57H','exec')

 def test_invalid_source_pin_never_writes_notebook(self):
  scratch=ROOT/'work/finite1519-join-fixtures';scratch.mkdir(parents=True,exist_ok=True)
  with tempfile.TemporaryDirectory(dir=scratch)as tmp:
   for pin in('',True,'a'*63,'A'*64):
    with self.subTest(pin=pin),self.assertRaises(ValueError):maker.write_local('actual-source.zip',pin,tmp)
   self.assertEqual(list(Path(tmp).iterdir()),[])
   path=maker.write_local('actual-source.zip','b'*64,tmp)
   self.assertEqual(path.name,'57H_n15_19_finite_join.ipynb');self.assertNotIn(b'\r\n',path.read_bytes())
   self.assertEqual(len(list(Path(tmp).iterdir())),1)


if __name__=='__main__':unittest.main()
