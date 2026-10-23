"""Six queued notebook routes and syntax only; never a numerical worker."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('extra_notebook_fixture', ROOT/'tools/make_retained_n25_extra_notebooks.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ExtraNotebooks(unittest.TestCase):
    def test_exact_six_routes_pins_empty_outputs_and_scope(self):
        self.assertEqual([name[:2] for name in builder.JOBS], ['29','30','31','32','33','34'])
        self.assertEqual(sum(row[1] for row in builder.JOBS.values()), 115)
        self.assertEqual(sum(row[2] for row in builder.JOBS.values()), 178294)
        for name, (branch, count, leaves) in builder.JOBS.items():
            notebook = builder.build('a'*40, name)
            cells = {c['id']: ''.join(c['source']) for c in notebook['cells']}
            self.assertIn('CODE_COMMIT = "'+'a'*40+'"', cells['pinned-code'])
            self.assertIn('run_colab("'+branch+'", durable_root=DURABLE)', cells['execute-task'])
            self.assertIn('NOT_READY.json', cells['instructions'])
            self.assertIn('stale or missing historical designs', cells['instructions'])
            self.assertIn(f'{leaves:,} leaves', cells['instructions'])
            self.assertIn('test_retained_n25_extra*.py', cells['retained-extra-infrastructure'])
            for c in notebook['cells']:
                if c['cell_type'] == 'code':
                    compile(''.join(c['source']), name, 'exec')
                    self.assertEqual(c['outputs'], [])
                    self.assertIsNone(c['execution_count'])

    def test_unpinned_code_refs_rejected(self):
        for pin in ('main','HEAD','a'*39,'A'*40,'../main'):
            with self.subTest(pin=pin), self.assertRaises(ValueError):
                builder.build(pin, next(iter(builder.JOBS)))


if __name__ == '__main__':
    unittest.main()
