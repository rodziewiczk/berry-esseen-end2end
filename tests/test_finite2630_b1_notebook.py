"""59A notebook packaging only; no original mathematical module imports."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('b1_builder',ROOT/'tools/make_finite2630_b1_notebook.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class Notebook(unittest.TestCase):
    def test_only_declared_full_runner_and_same_drive(self):
        d=g.build('a'*40);text='\n'.join(''.join(c['source'])for c in d['cells'])
        self.assertIn('be_replay.finite2630_b1 import run_colab',text)
        self.assertIn('run_colab(durable_root=DURABLE, backup_interval=60)',text)
        self.assertIn('test_finite2630_b1*.py',text)
        for word in('all23','115','all18','all55','Only two JSON','does not repeat completed53/64','All corresponding flags stay false'):
            self.assertIn(word,text)
        for c in d['cells']:
            if c['cell_type']=='code':compile(''.join(c['source']),'59A','exec')
    def test_mutable_or_placeholder_pin_produces_no_output(self):
        for pin in('main','a'*39,'A'*40,'0'*40,None):
            with self.assertRaises(ValueError):g.build(pin)
    def test_writer_is_exact_single_lf_notebook(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent)as tmp:
            p=g.write('a'*40,tmp);self.assertEqual(p.name,'59A_n26_30_b1_sine_fourier.ipynb')
            self.assertEqual(list(Path(tmp).iterdir()),[p]);self.assertNotIn(b'\r',p.read_bytes())
            self.assertEqual(json.loads(p.read_bytes()),g.build('a'*40))
if __name__=='__main__':unittest.main()
