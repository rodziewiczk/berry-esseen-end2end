"""Notebook syntax/defaults only; no generated cell is executed."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('kappa_notebook_builder',ROOT/'tools/make_finite1014_kappa_notebook.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)


class Notebook(unittest.TestCase):
    def test_immutable_pin_code_syntax_and_exact_one_scalar_task(self):
        doc=builder.build('a'*40);self.assertEqual(doc['metadata']['colab']['name'],'56K_kappa_62_625.ipynb')
        texts=[''.join(c['source'])for c in doc['cells']];alltext='\n'.join(texts)
        for c in doc['cells']:
            if c['cell_type']=='code':compile(''.join(c['source']),'synthetic-kappa-notebook','exec')
        self.assertIn('from be_replay.finite1014_kappa import run_colab',alltext)
        self.assertIn('RESULT = run_colab(durable_root=DURABLE, backup_interval=60)',alltext)
        self.assertIn('/content/drive/MyDrive/Berry-Esseen-end2end',alltext)
        self.assertIn('test_linux_supervisor.py',alltext);self.assertIn('test_finite1014_kappa*.py',alltext)
        self.assertIn('21 malformed',alltext);self.assertIn('324 exact',alltext)
        self.assertNotIn('pip install',alltext);self.assertNotIn('controls.py',texts[-2])
        self.assertIn('not aggregate',alltext);self.assertIn('Native/global proof',alltext)

    def test_invalid_mutable_pins_and_utf8_lf_output(self):
        for bad in('main','HEAD','0'*40,'a'*39,True):
            with self.assertRaises(ValueError):builder.build(bad)
        with tempfile.TemporaryDirectory(dir=ROOT.parent,prefix='t56kn-')as directory:
            p=builder.write('b'*40,directory);raw=p.read_bytes();self.assertNotIn(b'\r',raw)
            self.assertEqual(json.loads(raw)['nbformat'],4)


if __name__=='__main__':unittest.main()
