"""58D/E/F notebook compilation and fake routing only."""
import importlib.util
from pathlib import Path
import sys,tempfile,types,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite2024_fourier_builder',ROOT/'tools/make_finite2024_fourier_notebooks.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
PIN='a'*40
def cell(d,name):return ''.join(next(c['source']for c in d['cells']if c['id']==name))

class Notebooks(unittest.TestCase):
    def test_three_full_scopes_pin_and_gates_before_execution(self):
        docs=builder.build_all(PIN);self.assertEqual(set(docs),{'auxiliary','universal','supported'})
        for key,d in docs.items():
            intro=cell(d,'instructions');self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(d,'pinned-code'))
            for phrase in('all four unchanged original actions','original inputs','completed-cache transaction','not repeated here','No all-index theorem'):
                self.assertIn(phrase,intro)
            self.assertIn('test_finite2024_fourier*.py',cell(d,'finite2024-fixtures'));self.assertIn('raise RuntimeError',cell(d,'finite2024-fixtures'))
            ids=[c['id']for c in d['cells']];self.assertLess(ids.index('planner-dependency'),ids.index('execute-task'));self.assertLess(ids.index('finite2024-fixtures'),ids.index('execute-task'))
            for n in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):self.assertIn(n,cell(d,'planner-dependency'))
            for c in d['cells']:
                if c['cell_type']=='code':compile(''.join(c['source']),'58DEF','exec')
        self.assertIn('Index 19',cell(docs['auxiliary'],'instructions'));self.assertIn('419/1000',cell(docs['auxiliary'],'instructions'))
        self.assertIn('unacquired premise',cell(docs['supported'],'instructions'))

    def test_exact_three_family_routes_and_durable_root(self):
        calls=[];module=types.ModuleType('be_replay.finite2024_fourier')
        def fake(key,**kw):calls.append((key,kw));return dict(status={'all_index_conclusion_verified':False},bundle='synthetic.zip')
        module.run_colab=fake
        with patch.dict(sys.modules,{module.__name__:module}):
            for key in builder.NAMES:
                ns={'DURABLE':Path('/synthetic/drive')};exec(compile(cell(builder.build(PIN,key),'execute-task'),'fake58DEF','exec'),ns)
                self.assertIs(ns['RESULT']['status']['all_index_conclusion_verified'],False)
        self.assertEqual(calls,[(k,dict(durable_root=Path('/synthetic/drive'),backup_interval=60))for k in builder.NAMES])

    def test_invalid_input_and_three_lf_files_only(self):
        for key in(None,True,'all','B0'):
            with self.assertRaises(ValueError):builder.build(PIN,key)
        with tempfile.TemporaryDirectory(prefix='notebook58def-',dir=ROOT.parent)as t:
            self.assertTrue(Path(t).resolve().is_relative_to(ROOT.parent.resolve()));out=Path(t)/'out'
            for pin in(None,True,'main','0'*40,'A'*40,'a'*39):
                with self.assertRaises(ValueError):builder.write(pin,out)
                self.assertFalse(out.exists())
            paths=builder.write(PIN,out);self.assertEqual(sorted(p.name for p in paths),sorted(v+'.ipynb'for v in builder.NAMES.values()))
            self.assertTrue(all(b'\r\n'not in p.read_bytes()for p in paths))

if __name__=='__main__':unittest.main()
