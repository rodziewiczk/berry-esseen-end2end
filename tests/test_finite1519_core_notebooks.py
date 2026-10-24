"""Only notebook structure, defaults and syntax; no cell is executed."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('core_notebooks',ROOT/'tools/make_finite1519_core_notebooks.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)


class Notebooks(unittest.TestCase):
    def test_both_full_bands_immutable_pin_and_code_syntax(self):
        for band in('B0','BN'):
            doc=builder.build('a'*40,band);text='\n'.join(''.join(c['source'])for c in doc['cells'])
            for cell in doc['cells']:
                if cell['cell_type']=='code':compile(''.join(cell['source']),'synthetic-core','exec')
            self.assertIn(f"run_colab({band!r}, durable_root=DURABLE, backup_interval=60)",text)
            self.assertIn('MyDrive/Berry-Esseen-end2end',text);self.assertIn('test_finite1519_core*.py',text)
            self.assertIn('UNACQUIRED_NOT_STAGED',text);self.assertIn('There are20',text)
            self.assertIn('not aggregate',text);self.assertIn('four-call cache transaction',text)
            self.assertIn('82,800-second per-process',text);self.assertIn('23 hours',text)
            self.assertNotIn('43,200-second',text);self.assertNotIn('54,000-second',text)
            self.assertNotIn('pip install',text)
        self.assertIn('compatible57E HIGH cache',''.join(builder.build('a'*40,'BN')['cells'][0]['source']))
        self.assertIn('selected-candidate SHA',''.join(builder.build('a'*40,'B0')['cells'][0]['source']))

    def test_invalid_pins_bands_and_lf_output(self):
        for pin in('main','HEAD','0'*40,True):
            with self.assertRaises(ValueError):builder.build(pin,'B0')
        with self.assertRaises(ValueError):builder.build('a'*40,'B2')
        with tempfile.TemporaryDirectory(dir=ROOT.parent,prefix='t56cn-')as directory:
            paths=builder.write('b'*40,directory);self.assertEqual(len(paths),2)
            for p in paths:
                raw=p.read_bytes();self.assertNotIn(b'\r',raw);self.assertEqual(json.loads(raw)['nbformat'],4)


if __name__=='__main__':unittest.main()
