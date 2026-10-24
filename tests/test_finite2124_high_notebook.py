"""Generated notebook syntax/default fixtures only; no generated cell executes."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('actual2124_high_builder',ROOT/'tools/make_finite2124_high_notebook.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class Notebook(unittest.TestCase):
    def test_exact_runner_drive_scope_and_syntax(self):
        doc=builder.build('a'*40);text='\n'.join(''.join(c['source'])for c in doc['cells'])
        self.assertEqual(doc['metadata']['colab']['name'],'58A_n21_24_highrho_support.ipynb')
        self.assertIn('/content/drive/MyDrive/Berry-Esseen-end2end',text)
        self.assertIn('from be_replay.finite2124_high import run_colab',text)
        self.assertIn('RESULT = run_colab(durable_root=DURABLE, backup_interval=60)',text)
        self.assertIn('test_linux_supervisor.py',text);self.assertIn('test_finite2124_high*.py',text)
        self.assertIn('does NOT rerun',text);self.assertIn('not aggregate',text)
        for cell in doc['cells']:
            if cell['cell_type']=='code':
                self.assertEqual(cell['outputs'],[]);self.assertIsNone(cell['execution_count'])
                compile(''.join(cell['source']),'generated58A','exec')

    def test_bad_pin_and_lf_writer(self):
        for bad in('main','HEAD','0'*40,'a'*39,True):
            with self.assertRaises(ValueError):builder.build(bad)
        with tempfile.TemporaryDirectory(dir=ROOT.parent,prefix='t58an-')as directory:
            path=builder.write('b'*40,directory);raw=path.read_bytes()
            self.assertNotIn(b'\r',raw);self.assertEqual(json.loads(raw)['nbformat'],4)

if __name__=='__main__':unittest.main()
