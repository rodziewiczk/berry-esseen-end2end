import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('recovery_builder_fixture', ROOT/'tools/make_count_recovery_notebook.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class NotebookTests(unittest.TestCase):
    def test_all_code_cells_compile_and_new_epoch_scope_is_explicit(self):
        notebook = builder.build('a'*40)
        text = '\n'.join(''.join(cell['source']) for cell in notebook['cells'])
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                compile(''.join(cell['source']), 'recovery-notebook-fixture', 'exec')
        self.assertIn('from be_replay.count_recovery import run_colab', text)
        self.assertIn('100000', text)
        self.assertIn('UNTRUSTED', text)
        self.assertIn('same', text.lower())
        self.assertIn('test_count_*.py', text)
        self.assertIn('updated notebook24', text)

    def test_builder_rejects_mutable_code_pin(self):
        for value in ('main', 'a'*39, 'A'*40, None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                builder.build(value)


if __name__ == '__main__':
    unittest.main()
