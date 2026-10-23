"""Metadata-only checks for the explicit high-memory full restart."""
import ast
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('tail49_highmem_builder', ROOT/'tools/make_tail49_highmem_notebook.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class HighmemNotebookTests(unittest.TestCase):
    def test_full_restart_has_explicit_budget_and_existing_full_guard_fixtures(self):
        pin = 'a'*40
        doc = builder.build(pin)
        cells = {c['id']: ''.join(c['source']) for c in doc['cells']}
        self.assertIn('CODE_COMMIT = "'+pin+'"', cells['pinned-code'])
        self.assertIn('tail49-highmem16g-full-restart', cells['pinned-code'])
        self.assertIn('test_linux_supervisor.py', cells['actual-linux-guard-tests'])
        self.assertIn('test_tail49.py', cells['driver-fixtures'])
        call = ast.parse(cells['execute-task']).body[1].value
        args = {k.arg:k.value for k in call.keywords}
        self.assertEqual(set(args), {'durable_root','memory_bytes','cpu_seconds','wall_seconds'})
        self.assertEqual(ast.dump(args['memory_bytes']), ast.dump(ast.parse('16*1024**3',mode='eval').body))
        self.assertEqual(ast.literal_eval(args['cpu_seconds']),64800)
        self.assertEqual(ast.literal_eval(args['wall_seconds']),64800)
        self.assertEqual(doc['metadata']['accelerator'],'GPU')
        self.assertIn('no numerical resume',cells['instructions'])
        self.assertIn('all41retained',cells['instructions'])

    def test_original_two_gib_notebook_route_is_preserved(self):
        original = builder.phase2.build('b'*40,'12_tail49_complete_arithmetic')
        execute = ''.join(next(c for c in original['cells'] if c['id']=='execute-task')['source'])
        self.assertIn('memory_bytes=2048*1024**2', execute)
        with self.assertRaises(ValueError):
            builder.build('main')


if __name__ == '__main__':
    unittest.main()
