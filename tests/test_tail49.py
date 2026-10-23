"""Full-suite schema, source-binding and negative-control fixtures only."""
from copy import deepcopy
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import tail49


class Tail49Tests(unittest.TestCase):
    def fixture(self, directory):
        root, output = directory/'source', directory/'result'
        root.mkdir()
        output.mkdir()
        components = output/'components'
        components.mkdir()
        new = [{'name': name, 'argv': [name+'.py']} for name in tail49.TOP_NAMES[:10]]
        retained = [{'name': 'component_'+str(i), 'cwd': 'original/relative',
                     'argv': ['unchanged_'+str(i)+'.py'], 'source_run': 'historical/provenance/'+str(i)}
                    for i in range(41)]
        def row(name, directory, command, **extra):
            result = dict(name=name, command=command, returncode=0, **extra)
            for kind, content in (('stdout', 'fresh fixture '+name+'\n'), ('stderr', '')):
                path = directory/(name+'.'+kind+'.txt')
                path.write_text(content, encoding='utf-8')
                result[kind+'_sha256'] = tail49.sha(path)
            return result
        commands = [[sys.executable, '-B', *job['argv']] for job in new]
        commands += [[sys.executable, '-B', script] for script in
                     ('accept_finite_base.py', 'validate_schedule.py', 'check_consolidation.py')]
        commands += [[sys.executable, '-B', str(root/tail49.RUNNER), '--workspace-root',
                      str(root/'baseline/certificates'), '--job-file', str(root/'retained_jobs.json'),
                      '--output', str(components)]]
        top = {'status': 'PASS_BE49_SELECTED_ARITHMETIC', 'quick': False, 'sources_unchanged': True,
               'manifest_sha256': tail49.MANIFEST_SHA, 'manifested_files': 1400,
               'executable': sys.executable,
               'jobs': [row(name, output, cmd) for name, cmd in zip(tail49.TOP_NAMES, commands)]}
        child = {'schema': 'BE_FIXED_CERTIFICATE_SUITE_V2', 'status': 'PASS', 'selected_jobs': 41,
                 'optimized': False, 'sources_unchanged': True,
                 'input_sha256': {'source.py': 'a'*64}, 'input_sha256_after': {'source.py': 'a'*64},
                 'jobs': [row(job['name'], components, [sys.executable, '-B', *job['argv']],
                              **{k: v for k, v in job.items() if k != 'name'}) for job in retained]}
        (output/'result.json').write_text(json.dumps(top), encoding='utf-8')
        (components/'metadata.json').write_text(json.dumps(child), encoding='utf-8')
        return root, output, new, retained, top, child

    @contextmanager
    def mocked_full_suite(self, directory, *, status='completed', returncode=0, reason=None,
                          close_error=None):
        """Only synthetic JSON/captures: no original worker is imported/run."""
        source, _, new, retained, _, _ = self.fixture(directory)
        archive = directory/'fixture.zip'
        archive.write_bytes(b'fixture archive, never a numerical source')
        def execute(argv, **kwargs):
            output = kwargs['output_dir']
            output.mkdir(parents=True)
            stdout, stderr = output/'stdout.txt', output/'stderr.txt'
            stdout.write_text(''.join('START '+job+'\nPASS '+job+'\n' for job in tail49.TOP_NAMES)
                              +'PASS_BE49_SELECTED_ARITHMETIC\n', encoding='utf-8')
            stderr.write_bytes(b'')
            return dict(status=status, returncode=returncode, reason=reason,
                        stdout_path=str(stdout), stderr_path=str(stderr),
                        stdout_sha256=tail49.sha(stdout), stderr_sha256=tail49.sha(stderr))
        with patch.object(tail49.sys, 'platform', 'linux'), \
             patch.object(tail49, 'obtain_archive', return_value=archive), \
             patch.object(tail49, 'prepare', return_value=source), \
             patch.object(tail49, 'source_jobs', return_value=(new, retained)), \
             patch.object(tail49, 'verify_sources'), \
             patch.object(tail49, 'ARCHIVE_SHA', tail49.sha(archive)), \
             patch.object(tail49, 'validate_full_result', return_value=dict(
                 top_level_executions=14, retained_component_executions=41)) as validate, \
             patch('be_replay.linux_supervisor.run', side_effect=execute) as launched, \
             patch.object(tail49.Progress, 'start'), \
             patch.object(tail49.Progress, 'close', side_effect=close_error):
            yield validate, launched

    def test_complete14_and41_captures_required(self):
        with tempfile.TemporaryDirectory() as name:
            root, output, new, retained, _, _ = self.fixture(Path(name))
            result = tail49.validate_full_result(root, output, new, retained)
            self.assertEqual((result['top_level_executions'], result['retained_component_executions']), (14, 41))
            self.assertIs(result['quick_mode_used'], False)

    def test_quick_partial_reordered_or_historical_executable_fails(self):
        changes = [lambda top: top.update(quick=True), lambda top: top['jobs'].pop(),
                   lambda top: top['jobs'].reverse(), lambda top: top.update(executable='historical-python'),
                   lambda top: top.update(sources_unchanged=False),
                   lambda top: top['jobs'][0].update(returncode=False),
                   lambda top: top['jobs'][0]['command'].append('--quick')]
        for mutate in changes:
            with self.subTest(change=mutate), tempfile.TemporaryDirectory() as name:
                root, output, new, retained, top, _ = self.fixture(Path(name))
                mutate(top)
                (output/'result.json').write_text(json.dumps(top))
                with self.assertRaises(ValueError):
                    tail49.validate_full_result(root, output, new, retained)

    def test_missing_changed_or_nonempty_stderr_capture_fails(self):
        for change in ('missing', 'changed', 'stderr'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as name:
                root, output, new, retained, top, _ = self.fixture(Path(name))
                if change == 'missing':
                    (output/(tail49.TOP_NAMES[0]+'.stdout.txt')).unlink()
                elif change == 'changed':
                    (output/(tail49.TOP_NAMES[0]+'.stdout.txt')).write_text('old capture substituted')
                else:
                    path = output/(tail49.TOP_NAMES[0]+'.stderr.txt')
                    path.write_text('warning')
                    top['jobs'][0]['stderr_sha256'] = tail49.sha(path)
                    (output/'result.json').write_text(json.dumps(top))
                with self.assertRaises(ValueError):
                    tail49.validate_full_result(root, output, new, retained)

    def test_outer_captures_require_actual_hashes_and_empty_regular_bounded_stderr(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            stdout, stderr = root/'stdout.txt', root/'stderr.txt'
            raw = 'START composition49\nPASS composition49\n'
            stdout.write_text(raw, encoding='utf-8')
            stderr.write_bytes(b'')
            execution = dict(stdout_path=str(stdout), stderr_path=str(stderr),
                             stdout_sha256=tail49.sha(stdout), stderr_sha256=tail49.sha(stderr))
            self.assertEqual(tail49.wrapper_captures(execution), raw)
            stdout.write_text(raw+'changed capture\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'stdout capture matches supervisor SHA'):
                tail49.wrapper_captures(execution)
            stdout.write_text(raw, encoding='utf-8')
            # A nonempty original capture cannot be erased after supervision.
            stderr.write_bytes(b'actual warning\n')
            execution['stderr_sha256'] = tail49.sha(stderr)
            stderr.write_bytes(b'')
            with self.assertRaisesRegex(ValueError, 'stderr capture matches supervisor SHA'):
                tail49.wrapper_captures(execution)
            # Matching a new hash does not permit nonempty successful stderr.
            stderr.write_bytes(b'actual warning\n')
            execution['stderr_sha256'] = tail49.sha(stderr)
            with self.assertRaisesRegex(ValueError, 'Empty successful wrapper stderr'):
                tail49.wrapper_captures(execution)
            stderr.unlink()
            stderr.mkdir()
            with self.assertRaisesRegex(ValueError, 'bounded wrapper stderr'):
                tail49.wrapper_captures(execution)
            stderr.rmdir()
            with stderr.open('wb') as stream:
                stream.seek(16*tail49.MIB)
                stream.write(b'x')
            with self.assertRaisesRegex(ValueError, 'bounded wrapper stderr'):
                tail49.wrapper_captures(execution)

    def test_retained_all41_exact_invocations_and_unchanged_inputs_required(self):
        changes = [lambda child: child['jobs'].pop(), lambda child: child['jobs'].reverse(),
                   lambda child: child.update(selected_jobs=40), lambda child: child.update(optimized=True),
                   lambda child: child['input_sha256_after'].update({'source.py': 'b'*64}),
                   lambda child: child['jobs'][0].update(source_run='wrong/epoch'),
                   lambda child: child['jobs'][0].update(returncode=1)]
        for mutate in changes:
            with self.subTest(change=mutate), tempfile.TemporaryDirectory() as name:
                root, output, new, retained, _, child = self.fixture(Path(name))
                mutate(child)
                (output/'components/metadata.json').write_text(json.dumps(child))
                with self.assertRaises(ValueError):
                    tail49.validate_full_result(root, output, new, retained)

    def test_json_duplicate_keys_and_unsafe_paths_fail(self):
        with self.assertRaises(ValueError):
            json.loads('{"status": "PASS", "status": "FAIL"}', object_pairs_hook=tail49.unique)
        for path in ('../input', '/absolute', 'a//b', 'a\\b', 'C:input', 'a/./b'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                tail49.safe(path)

    def test_source_manifest_hash_and_literal_driver_pins_are_mandatory(self):
        pins = {'verify.py': tail49.VERIFY_SHA, 'new_jobs.json': tail49.NEW_JOBS_SHA,
                'retained_jobs.json': tail49.RETAINED_JOBS_SHA}
        raw = json.dumps({'schema': 'BE49_ARCHIVE_V1', 'files': pins}).encode()
        with patch.object(tail49, 'FILE_COUNT', 4), patch.object(
                tail49, 'MANIFEST_SHA', hashlib.sha256(raw).hexdigest()):
            self.assertEqual(tail49.manifest(raw), pins)
            with self.assertRaises(ValueError):
                tail49.manifest(raw+b' ')
        changed = deepcopy(pins)
        changed['verify.py'] = 'f'*64
        bad = json.dumps({'schema': 'BE49_ARCHIVE_V1', 'files': changed}).encode()
        with patch.object(tail49, 'FILE_COUNT', 4), patch.object(
                tail49, 'MANIFEST_SHA', hashlib.sha256(bad).hexdigest()):
            with self.assertRaises(ValueError):
                tail49.manifest(bad)

    def test_source_archive_mismatch_fails_before_extraction(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            archive = root/'bad.zip'
            with zipfile.ZipFile(archive, 'w') as capsule:
                capsule.writestr('BE_cutoff49_20260930/verify.py', 'not the frozen source')
            with self.assertRaises(ValueError):
                tail49.prepare(archive, root/'source')
            self.assertFalse((root/'source').exists())

    def test_native_mode_never_falls_back_or_starts_subprocesses(self):
        with tempfile.TemporaryDirectory() as name, patch(
                'be_replay.linux_supervisor.run') as execute:
            with self.assertRaisesRegex(ValueError, 'no native-mode fallback'):
                tail49.run(Path(name)/'epoch', archives=Path(name)/'cache', mode='native')
            execute.assert_not_called()
            self.assertFalse((Path(name)/'epoch').exists())

    def test_colab_error_still_bundles_and_keeps_global_false(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            with patch.object(tail49, 'run', side_effect=ValueError('fixture failure')):
                result = tail49.run_colab(durable_root=root/'durable', work_root=root/'work',
                                         archives=root/'cache', backup_interval=60)
            self.assertEqual(result['status']['state'], 'incomplete_error')
            self.assertFalse(result['status']['native_arithmetic_accepted'])
            self.assertFalse(result['status']['all_index_conclusion_verified'])
            self.assertTrue(Path(result['bundle']).is_file())

    def test_full_suite_explicit_memory_budget_reaches_basic_supervisor(self):
        from be_replay import linux_supervisor
        for memory in (512*tail49.MIB, 2048*tail49.MIB):
            with self.subTest(memory=memory), tempfile.TemporaryDirectory() as name:
                directory=Path(name)
                source, _, new, retained, _, _=self.fixture(directory)
                archive=directory/'fixture.zip'
                archive.write_bytes(b'fixture source archive; never executed')
                def execute(argv, **kwargs):
                    self.assertEqual(kwargs['memory_bytes'], memory)
                    self.assertEqual(kwargs['mode'], 'untrusted_search')
                    self.assertEqual((kwargs['cpu_seconds'],kwargs['wall_seconds']),
                                     (tail49.DEFAULT_CPU_SECONDS,tail49.DEFAULT_WALL_SECONDS))
                    output=kwargs['output_dir'];output.mkdir(parents=True)
                    stdout=output/'stdout.txt';stderr=output/'stderr.txt'
                    stdout.write_text(''.join('START '+job+'\nPASS '+job+'\n'for job in tail49.TOP_NAMES)
                                      +'PASS_BE49_SELECTED_ARITHMETIC\n',encoding='utf-8')
                    stderr.write_bytes(b'')
                    return dict(status='completed', returncode=0, stdout_path=str(stdout),stderr_path=str(stderr),
                                stdout_sha256=tail49.sha(stdout),stderr_sha256=tail49.sha(stderr))
                with patch.object(tail49.sys,'platform','linux'),patch.object(tail49,'obtain_archive',return_value=archive),\
                     patch.object(tail49,'prepare',return_value=source),patch.object(tail49,'source_jobs',return_value=(new,retained)),\
                     patch.object(tail49,'verify_sources'),patch.object(tail49,'ARCHIVE_SHA',tail49.sha(archive)),\
                     patch.object(tail49,'validate_full_result',return_value=dict(top_level_executions=14,retained_component_executions=41))as validate,\
                     patch.object(linux_supervisor,'run',side_effect=execute)as launched,\
                     patch.object(tail49.Progress,'start'),patch.object(tail49.Progress,'close'):
                    result=tail49.run(directory/'epoch',archives=directory/'cache',memory_bytes=memory)
                self.assertTrue(result['all_required_jobs_computed'])
                self.assertFalse(result['native_arithmetic_accepted'])
                self.assertFalse(result['all_index_conclusion_verified'])
                self.assertEqual(result['basic_memory_bytes'],memory)
                validate.assert_called_once();launched.assert_called_once()

    def test_invalid_memory_budget_fails_before_any_source_or_execution(self):
        for memory in (True,0,512*tail49.MIB-1,2048*tail49.MIB+1):
            with self.subTest(memory=memory),tempfile.TemporaryDirectory()as name,patch(
                    'be_replay.linux_supervisor.run')as execute,patch.object(tail49,'obtain_archive')as source:
                output=Path(name)/'epoch'
                with self.assertRaisesRegex(ValueError,'memory budget'):
                    tail49.run(output,archives=Path(name)/'cache',memory_bytes=memory)
                self.assertFalse(output.exists());execute.assert_not_called();source.assert_not_called()

    def test_colab_forwards_corrected_two_gib_budget_without_changing_scope(self):
        with tempfile.TemporaryDirectory()as name:
            root=Path(name)
            with patch.object(tail49,'run',return_value=dict(all_required_jobs_computed=False))as execute:
                result=tail49.run_colab(durable_root=root/'durable',work_root=root/'work',archives=root/'cache')
            self.assertEqual(execute.call_args.kwargs['memory_bytes'],2048*tail49.MIB)
            self.assertEqual(execute.call_args.kwargs['cpu_seconds'],64800)
            self.assertEqual(execute.call_args.kwargs['wall_seconds'],64800)
            self.assertEqual(execute.call_args.kwargs['mode'],'basic')
            self.assertFalse(result['status']['native_arithmetic_accepted'])
            self.assertFalse(result['status']['all_index_conclusion_verified'])
            self.assertTrue(Path(result['bundle']).is_file())

    def test_default_and_custom_budgets_cross_all_layers_and_are_persisted(self):
        for budget in ({}, dict(cpu_seconds=12000, wall_seconds=15000.5)):
            with self.subTest(budget=budget), tempfile.TemporaryDirectory() as name:
                root = Path(name)
                expected_cpu = budget.get('cpu_seconds', 64800)
                expected_wall = budget.get('wall_seconds', 64800)
                with self.mocked_full_suite(root) as (validate, launched):
                    exported = tail49.run_colab(durable_root=root/'durable', work_root=root/'work',
                                                archives=root/'cache', **budget)
                actual = launched.call_args.kwargs
                self.assertEqual((actual['cpu_seconds'], actual['wall_seconds']),
                                 (expected_cpu, expected_wall))
                self.assertEqual(actual['mode'], 'untrusted_search')
                self.assertEqual(actual['memory_bytes'], 2048*tail49.MIB)
                session = json.loads((Path(exported['work'])/'SESSION_RESULT.json').read_text())
                result = json.loads((Path(exported['work'])/'arithmetic'/'TAIL49_RESULT.json').read_text())
                for packet in (session, result):
                    self.assertEqual(packet['basic_cpu_seconds'], expected_cpu)
                    self.assertEqual(packet['basic_wall_seconds'], expected_wall)
                    self.assertEqual(packet['execution_resource_profile'],
                                     'BASIC_FULL_SUITE_EXPLICIT_BUDGETS_V3')
                    self.assertFalse(packet['native_arithmetic_accepted'])
                    self.assertFalse(packet['all_index_conclusion_verified'])
                self.assertTrue(result['all_required_jobs_computed'])
                self.assertEqual((result['top_level_executions'], result['retained_component_executions']),
                                 (14, 41))
                self.assertEqual(result['original_driver_semantic_argv'][1:],
                                 ['--output', str(Path(exported['work'])/'arithmetic'/'native-full')])
                validate.assert_called_once()
                launched.assert_called_once()
                self.assertTrue(Path(exported['bundle']).is_file())

    def test_invalid_cpu_or_wall_rejected_before_platform_files_or_download(self):
        bad = [dict(cpu_seconds=v) for v in (True, False, 0, -1, 1.0, 64801)]
        bad += [dict(wall_seconds=v) for v in
                (True, False, 0, -1, float('nan'), float('inf'), 64801, 10**1000)]
        for budget in bad:
            with self.subTest(budget=budget), tempfile.TemporaryDirectory() as name:
                root = Path(name)
                with patch.object(tail49.sys, 'platform', 'not-linux'), \
                     patch.object(tail49, 'obtain_archive') as obtain, \
                     patch('be_replay.linux_supervisor.run') as execute, \
                     patch('be_replay.environment.snapshot') as environment:
                    with self.assertRaisesRegex(ValueError, 'BASIC (CPU|wall) budget'):
                        tail49.run(root/'epoch', archives=root/'cache', **budget)
                    with self.assertRaisesRegex(ValueError, 'BASIC (CPU|wall) budget'):
                        tail49.run_colab(durable_root=root/'durable', work_root=root/'work',
                                         archives=root/'cache', **budget)
                    self.assertFalse((root/'epoch').exists())
                    self.assertFalse((root/'work').exists())
                    self.assertFalse((root/'durable').exists())
                    obtain.assert_not_called()
                    execute.assert_not_called()
                    environment.assert_not_called()

    def test_cli_defaults_match_run_and_custom_values_are_forwarded(self):
        for arguments, expected in (([], (64800, 64800)),
                                    (['--cpu-seconds', '12000', '--wall-seconds', '15000'], (12000, 15000))):
            with self.subTest(arguments=arguments), patch.object(sys, 'argv',
                    ['tail49', '--output', 'unused', '--archives', 'unused', *arguments]), \
                 patch.object(tail49, 'run', return_value=dict(all_required_jobs_computed=False)) as run:
                self.assertEqual(tail49.main(), 2)
                self.assertEqual((run.call_args.kwargs['cpu_seconds'], run.call_args.kwargs['wall_seconds']), expected)
                self.assertEqual(run.call_args.kwargs['memory_bytes'], 2048*tail49.MIB)

    def test_timeout_and_boolean_exit_never_qualify_even_with_full_markers(self):
        for status, returncode, reason in (('incomplete', -15, 'external_wall_timeout'),
                                           ('completed', False, None)):
            with self.subTest(status=status, returncode=returncode), tempfile.TemporaryDirectory() as name:
                root = Path(name)
                with self.mocked_full_suite(root, status=status, returncode=returncode,
                                           reason=reason) as (validate, _):
                    result = tail49.run(root/'epoch', archives=root/'cache')
                validate.assert_not_called()
                self.assertFalse(result['all_required_jobs_computed'])
                self.assertFalse(result['native_arithmetic_accepted'])
                self.assertFalse(result['all_index_conclusion_verified'])
                self.assertEqual(result['execution_reason'], reason)
                self.assertEqual(result['status'], 'INCOMPLETE_NO_ACCEPTANCE')
                saved = json.loads((root/'epoch'/'TAIL49_RESULT.json').read_text())
                self.assertEqual(saved, result)
                self.assertTrue((root/'epoch'/'ERROR.txt').is_file())

    def test_timeout_and_progress_close_failure_still_export_incomplete_evidence(self):
        cases = (dict(status='incomplete', returncode=-15, reason='external_wall_timeout'),
                 dict(close_error=RuntimeError('fixture progress shutdown failure')))
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as name:
                root = Path(name)
                with self.mocked_full_suite(root, **case):
                    exported = tail49.run_colab(durable_root=root/'durable', work_root=root/'work',
                                                archives=root/'cache')
                self.assertEqual(exported['status']['state'], 'incomplete_full_suite')
                result = exported['status']['arithmetic_result']
                self.assertFalse(result['all_required_jobs_computed'])
                self.assertFalse(result['native_arithmetic_accepted'])
                self.assertFalse(result['all_index_conclusion_verified'])
                work = Path(exported['work'])/'arithmetic'
                self.assertEqual(json.loads((work/'TAIL49_RESULT.json').read_text()), result)
                self.assertTrue((work/'ERROR.txt').is_file())
                if 'close_error' in case:
                    self.assertIn('fixture progress shutdown failure', result['progress_error'])
                else:
                    self.assertEqual(result['execution_reason'], 'external_wall_timeout')
                self.assertTrue(Path(exported['bundle']).is_file())


if __name__ == '__main__':
    unittest.main()
