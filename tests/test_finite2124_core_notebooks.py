"""58B/C notebook syntax and fake runner routing only."""
import importlib.util
from pathlib import Path
import sys,tempfile,types,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite2124_core_builder',ROOT/'tools/make_finite2124_core_notebooks.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
PIN='a'*40
def cell(doc,name):return ''.join(next(c['source']for c in doc['cells']if c['id']==name))

class Notebooks(unittest.TestCase):
    def test_both_complete_bands_census_pin_and_required_failure_gate(self):
        docs=builder.build_all(PIN);self.assertEqual(set(docs),{'B0','BN'})
        for band,d in docs.items():
            intro=cell(d,'instructions');self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(d,'pinned-code'))
            for text in('16 full original calls','193 original static inputs','190 static graph','eight example','all 32 calls','conditional','2,592','all 100'):
                self.assertIn(text,intro)
            self.assertIn('test_finite2124_core*.py',cell(d,'finite2124-fixtures'));self.assertIn('raise RuntimeError',cell(d,'finite2124-fixtures'))
            self.assertIn('[1,11/10]'if band=='B0'else'[11/10,9/8]',intro)
            ids=[c['id']for c in d['cells']];self.assertLess(ids.index('finite2124-fixtures'),ids.index('execute-task'))
            for c in d['cells']:
                if c['cell_type']=='code':compile(''.join(c['source']),'58BC','exec')

    def test_exact_bands_route_to_same_durable_root(self):
        calls=[];module=types.ModuleType('be_replay.finite2124_core')
        def fake(band,**kw):calls.append((band,kw));return dict(status={'all_index_conclusion_verified':False},bundle='synthetic.zip')
        module.run_colab=fake
        with patch.dict(sys.modules,{module.__name__:module}):
            for band in('B0','BN'):
                ns={'DURABLE':Path('/synthetic/drive')};exec(compile(cell(builder.build(PIN,band),'execute-task'),'fake58','exec'),ns)
                self.assertIs(ns['RESULT']['status']['all_index_conclusion_verified'],False)
        self.assertEqual(calls,[(b,dict(durable_root=Path('/synthetic/drive'),backup_interval=60))for b in('B0','BN')])

    def test_invalid_pin_or_band_and_two_lf_outputs_only(self):
        for band in(None,True,'B1','bn'):
            with self.assertRaises(ValueError):builder.build(PIN,band)
        with tempfile.TemporaryDirectory(prefix='notebook58bc-',dir=ROOT.parent)as t:
            self.assertTrue(Path(t).resolve().is_relative_to(ROOT.parent.resolve()))
            out=Path(t)/'out'
            for pin in(None,True,'main','0'*40,'A'*40,'a'*39):
                with self.assertRaises(ValueError):builder.write(pin,out)
                self.assertFalse(out.exists())
            paths=builder.write(PIN,out);self.assertEqual(sorted(p.name for p in paths),sorted(n+'.ipynb'for n in builder.NAMES.values()))
            self.assertTrue(all(b'\r\n'not in p.read_bytes()for p in paths))

if __name__=='__main__':unittest.main()
