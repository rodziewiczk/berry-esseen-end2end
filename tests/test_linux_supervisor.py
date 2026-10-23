"""Small adversarial fixtures only; no mathematical search or native proof."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from be_replay import linux_supervisor as supervisor


class PolicyTests(unittest.TestCase):
    @staticmethod
    def evaluate_filter(machine, number, *, arch=None, new_limit=0):
        rows, architecture, _, _ = supervisor._filter_instructions(machine)
        memory = {0: number, 4: architecture if arch is None else arch,
                  32: new_limit & 0xffffffff, 36: new_limit >> 32}
        accumulator, pointer = 0, 0
        while pointer < len(rows):
            code, yes, no, value = rows[pointer]
            if code == 0x20:
                accumulator = memory[value]
            elif code == 0x15:
                pointer += yes if accumulator == value else no
            elif code == 0x35:
                pointer += yes if accumulator >= value else no
            elif code == 0x06:
                return value
            else:
                raise AssertionError('Unexpected untested BPF instruction')
            pointer += 1
        raise AssertionError('Filter ran off its complete program')

    def test_bpf_every_denial_arch_guard_and_x32_are_terminal(self):
        for machine in ('x86_64', 'aarch64'):
            _, _, denied, _ = supervisor._filter_instructions(machine)
            for name, number in denied.items():
                with self.subTest(machine=machine, syscall=name):
                    self.assertEqual(self.evaluate_filter(machine, number), 0x80000000)
            self.assertEqual(self.evaluate_filter(machine, 0, arch=0), 0x80000000)
            self.assertEqual(self.evaluate_filter(machine, 0x40000000), 0x80000000)

    def test_bpf_prlimit_get_allowed_set_blocked_in_both_pointer_halves(self):
        for machine in ('x86_64', 'aarch64'):
            _, _, _, prlimit = supervisor._filter_instructions(machine)
            self.assertEqual(self.evaluate_filter(machine, prlimit), 0x7fff0000)
            self.assertEqual(self.evaluate_filter(machine, prlimit, new_limit=1), 0x80000000)
            self.assertEqual(self.evaluate_filter(machine, prlimit, new_limit=1 << 40), 0x80000000)

    def test_unsupported_abi_and_native_inline_code_are_rejected(self):
        with self.assertRaisesRegex(supervisor.SupervisorError, 'architecture'):
            supervisor._filter_instructions('unknown')
        with self.assertRaisesRegex(supervisor.SupervisorError, 'literal Python script'):
            supervisor._python_target([sys.executable, '-c', 'print("unreviewed")'], Path.cwd())

    def test_progress_tail_ignores_partial_final_json(self):
        with tempfile.TemporaryDirectory() as name:
            path = Path(name)/'stdout.txt'
            path.write_bytes(b'noise\n{"nodes": 12, "pending": 4}\n{"nodes": ')
            self.assertEqual(supervisor._last_json(path), {'nodes': 12, 'pending': 4})

    def test_durable_progress_appends_without_losing_earlier_stage(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            supervisor._progress(root, {'stage': 'start', 'nodes': 0})
            supervisor._progress(root, {'stage': 'search', 'nodes': 12})
            rows = [json.loads(line) for line in (root/'progress.jsonl').read_text().splitlines()]
            self.assertEqual([row['stage'] for row in rows], ['start', 'search'])
            self.assertEqual(json.loads((root/'progress.json').read_text()), rows[-1])

    def test_bad_parameters_are_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for updates in ({'wall_seconds': 0}, {'cpu_seconds': True}, {'mode': 'trusted'},
                            {'memory_bytes': 1}, {'sample_seconds': 5}):
                with self.subTest(updates=updates):
                    args = dict(argv=['not-executed'], cwd=root, output_dir=root/'out', wall_seconds=1)
                    args.update(updates)
                    with self.assertRaises(supervisor.SupervisorError):
                        supervisor.run(**args)

    def test_checkpoint_outside_owned_work_or_old_output_is_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root/'work').mkdir()
            with self.assertRaisesRegex(supervisor.SupervisorError, 'belongs'):
                supervisor.run(['not-executed'], cwd=root/'work', output_dir=root/'out', wall_seconds=1,
                               checkpoint_paths=[root/'outside.json'])
            (root/'old').mkdir()
            (root/'old/receipt.json').write_text('old')
            with self.assertRaisesRegex(supervisor.SupervisorError, 'empty'):
                supervisor.run(['not-executed'], cwd=root/'work', output_dir=root/'old', wall_seconds=1)

    def test_unsupported_platform_never_spawns_or_claims_acceptance(self):
        with tempfile.TemporaryDirectory() as name:
            with patch.object(supervisor.sys, 'platform', 'unsupported'), patch.object(
                    supervisor.subprocess, 'Popen') as started:
                result = supervisor.run(['not-executed'], cwd=name, output_dir=Path(name)/'out', wall_seconds=1)
            started.assert_not_called()
            self.assertEqual(result['status'], 'unsupported')
            self.assertFalse(result['proof_accepted'])

    def test_checkpoint_capture_includes_main_and_backup_and_hashes(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root/'work').mkdir()
            (root/'out').mkdir()
            for suffix in ('', '.backup'):
                (root/'work'/('checkpoint'+suffix+'.json')).write_text('{"partial": true}')
            config = {'cwd': str(root/'work'), 'output_dir': str(root/'out'), 'disk_bytes': 1000,
                      'checkpoint_paths': [str(root/'work'/('checkpoint'+s+'.json')) for s in ('', '.backup')]}
            rows = supervisor._capture_checkpoints(config)
            self.assertEqual(len(rows), 2)
            self.assertTrue(all(Path(row['path']).is_file() and len(row['sha256']) == 64 for row in rows))
            self.assertTrue(all(row['trusted_certificate'] is False for row in rows))

    def test_sampled_quota_rejects_special_file_and_excess_bytes(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root/'large').write_bytes(b'x'*10)
            with self.assertRaisesRegex(supervisor.SupervisorError, 'quota'):
                supervisor._directory_bytes([root], 9)


@unittest.skipUnless(sys.platform == 'linux', 'Actual Linux process fixtures')
class LinuxExecutionTests(unittest.TestCase):
    def execute(self, script, *, seconds=2, checkpoints=()):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        (root/'work').mkdir()
        return supervisor.run([sys.executable, '-B', '-S', '-c', script], cwd=root/'work',
                              output_dir=root/'out', wall_seconds=seconds, cpu_seconds=5,
                              checkpoint_paths=checkpoints, sample_seconds=.02)

    def test_observes_real_exit_and_untrusted_scope(self):
        result = self.execute('print("fixture")')
        self.assertEqual((result['status'], result['returncode']), ('completed', 0))
        self.assertIn('fixture', Path(result['stdout_path']).read_text())
        self.assertFalse(result['guard_scope']['aggregate_kernel_memory_limit'])
        self.assertFalse(result['proof_accepted'])

    def test_external_timeout_captures_partial_checkpoint(self):
        result = self.execute('from pathlib import Path; import time; '
                              'Path("checkpoint.json").write_text("partial"); time.sleep(20)',
                              seconds=.3, checkpoints=['checkpoint.json', 'checkpoint.backup.json'])
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['reason'], 'external_wall_timeout')
        self.assertLess(result['elapsed_seconds'], 5)
        self.assertEqual(Path(result['checkpoints'][0]['path']).read_text(), 'partial')
        self.assertFalse(result['checkpoints'][1]['exists'])

    def test_timeout_terminates_owned_child_group_not_only_leader(self):
        result = self.execute('import os,time; from pathlib import Path; p=os.fork(); '
                              'Path("child.pid").write_text(str(p)) if p else None; time.sleep(20)',
                              seconds=.3, checkpoints=['child.pid'])
        self.assertEqual(result['status'], 'incomplete')
        child = int(Path(result['checkpoints'][0]['path']).read_text())
        try:
            self.assertIn(supervisor._proc_stat(child)['state'], ('Z', 'X'))
        except FileNotFoundError:
            pass

    def test_native_inline_code_cannot_fallback_to_search(self):
        with tempfile.TemporaryDirectory() as name:
            with self.assertRaises(supervisor.SupervisorError):
                supervisor.run([sys.executable, '-c', 'raise Exception("must not run")'],
                               cwd=name, output_dir=Path(name)/'out', wall_seconds=1,
                               mode='trusted_native')

    def native(self, script):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root/'work').mkdir()
        path = root/'work/fixture.py'
        path.write_text(script)
        return supervisor.run([sys.executable, '-B', '-S', str(path)], cwd=root/'work',
                              output_dir=root/'out', wall_seconds=3, cpu_seconds=10,
                              mode='trusted_native', sample_seconds=.02)

    def test_native_real_seccomp_and_both_hard_caps_before_script(self):
        result = self.native('import json,resource; print(json.dumps({"address": '
                             'resource.getrlimit(resource.RLIMIT_AS)}))')
        self.assertEqual(result['status'], 'completed', result)
        self.assertTrue(result['guard_scope']['capability_established'])
        self.assertEqual(result['guard_scope']['hard_sum_RLIMIT_AS_bytes'], 512*1024**2)
        self.assertEqual(json.loads(Path(result['stdout_path']).read_text())['address'],
                         [448*1024**2, 448*1024**2])
        self.assertFalse(result['proof_accepted'])

    def test_native_kernel_rejects_process_creation_exec_and_group_escape(self):
        for operation in ('os.fork()', 'os.execv(sys.executable,[sys.executable,"-c","pass"])',
                          'os.setsid()'):
            with self.subTest(operation=operation):
                result = self.native('import os,sys; '+operation+'; print("UNREACHABLE")')
                self.assertEqual(result['status'], 'incomplete')
                self.assertNotIn('UNREACHABLE', Path(result['stdout_path']).read_text())

    def test_native_kernel_rejects_changing_hard_limits(self):
        result = self.native('import resource; resource.setrlimit(resource.RLIMIT_AS,'
                             '(128*1024**2,128*1024**2)); print("UNREACHABLE")')
        self.assertEqual(result['status'], 'incomplete')
        self.assertNotIn('UNREACHABLE', Path(result['stdout_path']).read_text())

    def test_native_address_space_limit_rejects_oversized_allocation(self):
        result = self.native('x=bytearray(700*1024**2); print("UNREACHABLE")')
        self.assertEqual(result['status'], 'incomplete')
        self.assertIn('MemoryError', Path(result['stderr_path']).read_text())
        self.assertNotIn('UNREACHABLE', Path(result['stdout_path']).read_text())


if __name__ == '__main__':
    unittest.main()
