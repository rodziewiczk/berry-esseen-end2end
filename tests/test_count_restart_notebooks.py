import ast
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
from types import ModuleType
import unittest
from unittest.mock import Mock, patch

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
            self.assertIn('2 GiB', text)
            self.assertIn('12 hours', text)
            self.assertIn('RESTORED_PREFIX2_V1', text)
            self.assertIn('alpha 16, depth first', text)
            self.assertIn('Incomparable maximal candidates', text)
            self.assertIn('never silently starts empty roots', text)
            self.assertIn('backup_saved', text)
            for cell in document['cells']:
                if cell['cell_type'] == 'code':
                    compile(''.join(cell['source']), name, 'exec')
            self.assertIn(repr(target), text)

    def test_each_execution_routes_to_exact_target_without_parameters_to_edit(self):
        fake = ModuleType('be_replay.count_recovery')
        fake.DISCOVERY_STRATEGY = 'RESTORED_PREFIX2_V1'
        for name, target in builder.TARGETS.items():
            execute = next(cell for cell in builder.build('a'*40, name)['cells'] if cell['id'] == 'execute-task')
            code = ''.join(execute['source'])
            fake.run_colab = Mock(return_value={'fixture': True})
            with self.subTest(target=target), patch.dict(sys.modules, {'be_replay.count_recovery': fake}), redirect_stdout(io.StringIO()):
                namespace = {'DURABLE': 'fixture-drive'}
                exec(compile(ast.parse(code), name, 'exec'), namespace)
            fake.run_colab.assert_called_once_with(target, durable_root='fixture-drive')
            self.assertEqual(namespace['RESULT'], {'fixture': True})

    def test_wrong_discovery_policy_cannot_start_a_worker(self):
        fake = ModuleType('be_replay.count_recovery')
        fake.DISCOVERY_STRATEGY = 'LEGACY_MIDPOINT_V1'
        fake.run_colab = Mock()
        for name in builder.TARGETS:
            execute = next(cell for cell in builder.build('a'*40, name)['cells'] if cell['id'] == 'execute-task')
            with self.subTest(name=name), patch.dict(sys.modules, {'be_replay.count_recovery': fake}):
                with self.assertRaisesRegex(RuntimeError, 'required PREFIX2 resume policy'):
                    exec(''.join(execute['source']), {'DURABLE': 'fixture-drive'})
        fake.run_colab.assert_not_called()

    def test_existing_drive_root_is_preserved_for_every_target(self):
        for name, target in builder.TARGETS.items():
            document = builder.build('b'*40, name)
            drive = next(cell for cell in document['cells'] if cell['id'] == 'durable-drive')
            code = ast.parse(''.join(drive['source']))
            assignments = {node.targets[0].id: node.value for node in code.body
                           if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)}
            self.assertEqual(ast.literal_eval(assignments['DURABLE'].args[0]),
                             '/content/drive/MyDrive/Berry-Esseen-end2end')
            execute = next(cell for cell in document['cells'] if cell['id'] == 'execute-task')
            calls = [node for node in ast.walk(ast.parse(''.join(execute['source'])))
                     if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                     and node.func.id == 'run_colab']
            self.assertEqual(len(calls), 1)
            self.assertEqual(ast.literal_eval(calls[0].args[0]), target)
            self.assertEqual([(kw.arg, kw.value.id) for kw in calls[0].keywords],
                             [('durable_root', 'DURABLE')])

    def test_notebooks_keep_strict_guard_fixtures_and_conditional_scope(self):
        for name in builder.TARGETS:
            document = builder.build('c'*40, name)
            labels = [cell['id'] for cell in document['cells']]
            self.assertLess(labels.index('actual-linux-guard-tests'), labels.index('execute-task'))
            self.assertLess(labels.index('driver-fixtures'), labels.index('execute-task'))
            text = '\n'.join(''.join(cell['source']) for cell in document['cells'])
            self.assertIn('all 24 corruption controls', text)
            self.assertIn('all 26 closed root domains', text)
            self.assertIn('This job cannot establish the global theorem', text)
            self.assertIn('portable V14 jobs 06/07', text)
            self.assertIn('attained positive-closed contact', text)
            self.assertNotIn('starts from all 26 original roots', text)
            self.assertNotIn('latest_checkpoint(', text)

    def test_checked_in_notebooks_are_clean_valid_python_documents(self):
        for name in builder.TARGETS:
            path = ROOT/'colab'/(name+'.ipynb')
            document = json.loads(path.read_text(encoding='utf-8'))
            source = ''.join(next(cell for cell in document['cells'] if cell['id'] == 'pinned-code')['source'])
            pin = re.search(r'CODE_COMMIT = "([0-9a-f]{40})"', source).group(1)
            self.assertRegex(pin, r'^[0-9a-f]{40}$')
            self.assertEqual(len({cell['id'] for cell in document['cells']}), len(document['cells']))
            for cell in document['cells']:
                if cell['cell_type'] == 'code':
                    compile(''.join(cell['source']), name, 'exec')
                    self.assertEqual(cell['outputs'], [])
                    self.assertIsNone(cell['execution_count'])

    def test_only_full_commit_and_named_notebook_are_accepted(self):
        with self.assertRaises(ValueError):
            builder.build('main', next(iter(builder.TARGETS)))
        with self.assertRaises(ValueError):
            builder.build('a'*40, '08_new_job')


if __name__ == '__main__':
    unittest.main()
