"""Notebook routing/compilation only, without original mathematical imports."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('n27_p41_generator_fixture',ROOT/'tools/make_n27_p41_recovery_notebook.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)


class Notebook(unittest.TestCase):
    def test_all_cells_compile_and_full_source_scope_is_explicit(self):
        d=gen.build('a'*40);text='\n'.join(''.join(c['source'])for c in d['cells'])
        for c in d['cells']:
            if c['cell_type']=='code':compile(''.join(c['source']),'notebook64','exec')
        for phrase in('construct_alpha4.py','count_protocol.py accept','28 original count roots','24 original corruption',
                       '10,000-node','600-second','depth128','Notebook53 remains NOT_READY','7,200-second','7,260-second',
                       'test_n27_p41_recovery*.py'):
            self.assertIn(phrase,text)
        self.assertIn('a'*40,text)

    def test_real_execute_cell_routes_only_the_agreed_api(self):
        from be_replay import n27_p41_recovery
        d=gen.build('a'*40);c=next(c for c in d['cells']if c['id']=='execute-task');sentinel={'fixture':True}
        with patch.object(n27_p41_recovery,'run_colab',return_value=sentinel)as execute:
            scope={'DURABLE':'synthetic-Drive-root'};exec(''.join(c['source']),scope)
        execute.assert_called_once_with(durable_root='synthetic-Drive-root',backup_interval=60)
        self.assertIs(scope['RESULT'],sentinel)

    def test_invalid_pin_rejected_before_output(self):
        with tempfile.TemporaryDirectory()as name:
            path=Path(name)/'absent'
            for pin in(None,'main','0'*40,'g'*40,'a'*39):
                with self.subTest(pin=pin),self.assertRaises(ValueError):gen.write(pin,path)
            self.assertFalse(path.exists())

    def test_output_name_and_bytes_are_english_utf8_lf(self):
        with tempfile.TemporaryDirectory()as name:
            p=gen.write('a'*40,Path(name));b=p.read_bytes();d=json.loads(b)
            self.assertEqual(p.name,'64_n27_p41_new_candidate.ipynb');self.assertNotIn(b'\r',b)
            self.assertEqual(d['nbformat'],4);self.assertIn('new conditional candidate',''.join(d['cells'][0]['source']))


if __name__=='__main__':unittest.main()
