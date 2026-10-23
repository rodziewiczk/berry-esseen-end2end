"""Queued notebook24 syntax/routing fixtures; no mathematical code is run."""
import importlib.util
from pathlib import Path
from types import ModuleType
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('n25_notebook_builder',ROOT/'tools/make_n25_join_notebook.py')
builder=importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class N25JoinNotebookTests(unittest.TestCase):
    def test_pinned_notebook_compiles_and_describes_partial_proof_scope(self):
        notebook=builder.build('a'*40)
        for cell in notebook['cells']:
            if cell['cell_type']=='code':
                compile(''.join(cell['source']),'notebook24','exec')
        text='\n'.join(''.join(c['source'])for c in notebook['cells'])
        for phrase in ('a'*40,'01–07','09/10','WAITING_FOR_N25_EVIDENCE','four closed','does not complete all n25'):
            self.assertIn(phrase,text)
        self.assertIn('test_n25_*.py',text)

    def test_execute_cell_calls_only_mocked_collector(self):
        notebook=builder.build('b'*40)
        execute=next(c for c in notebook['cells']if c['id']=='execute-task')
        module=ModuleType('be_replay.n25_collect')
        calls=[]
        def run_colab(**kw):
            calls.append(kw)
            return dict(status=dict(state='MOCKED_ONLY'),bundle='fixture.zip',work='fixture')
        module.run_colab=run_colab
        scope=dict(DURABLE=Path('/synthetic/drive'))
        with patch.dict(sys.modules,{'be_replay.n25_collect':module}):
            exec(''.join(execute['source']),scope)
        self.assertEqual(calls,[dict(durable_root=Path('/synthetic/drive'))])
        self.assertEqual(scope['RESULT']['status']['state'],'MOCKED_ONLY')

    def test_nonimmutable_pin_rejected(self):
        for pin in ('main','a'*39,'a'*41,'G'*40,None):
            with self.subTest(pin=pin),self.assertRaises(ValueError):
                builder.build(pin)


if __name__=='__main__':
    unittest.main()
