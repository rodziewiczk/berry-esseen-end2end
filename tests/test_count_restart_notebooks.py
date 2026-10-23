import ast
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('restart_notebook_fixture', ROOT/'tools/make_restart_notebooks.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class RestartNotebookTests(unittest.TestCase):
    def test_seven_unique_numbered_targets_and_scopes(self):
        self.assertEqual([name[:2] for name in builder.TARGETS], ['01','02','03','04','05','06','07'])
        self.assertEqual(len(set(builder.TARGETS.values())), 7)
        for name, target in builder.TARGETS.items():
            document = builder.build('a'*40, name)
            text = '\n'.join(''.join(cell['source']) for cell in document['cells'])
            self.assertIn('SAME Google Drive', text)
            self.assertIn('100000', text)
            self.assertIn('2GiB', text)
            self.assertIn('12 hours', text)
            self.assertIn('untrusted_checkpoint_migrated', text)
            for cell in document['cells']:
                if cell['cell_type'] == 'code':
                    compile(''.join(cell['source']), name, 'exec')
            self.assertIn(repr(target), text)

    def test_each_execution_routes_to_exact_target_without_parameters_to_edit(self):
        from be_replay import count_recovery
        for name, target in builder.TARGETS.items():
            execute = next(cell for cell in builder.build('a'*40, name)['cells'] if cell['id'] == 'execute-task')
            code = ''.join(execute['source'])
            with self.subTest(target=target), patch.object(count_recovery, 'run_colab', return_value={'fixture': True}) as run:
                namespace = {'DURABLE': 'fixture-drive'}
                exec(compile(ast.parse(code), name, 'exec'), namespace)
            run.assert_called_once_with(target, durable_root='fixture-drive')
            self.assertEqual(namespace['RESULT'], {'fixture': True})

    def test_only_full_commit_and_named_notebook_are_accepted(self):
        with self.assertRaises(ValueError):
            builder.build('main', next(iter(builder.TARGETS)))
        with self.assertRaises(ValueError):
            builder.build('a'*40, '08_new_job')


if __name__ == '__main__':
    unittest.main()
