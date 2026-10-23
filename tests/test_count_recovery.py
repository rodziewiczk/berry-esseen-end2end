"""Synthetic recovery orchestration traps; no numerical module executes."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from be_replay import count_recovery as recovery


def pending():
    return dict(schema='UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1', binding={},
                arithmetic_accepted=False, roots=[dict(k=k, tree={'kind': 'pending'}) for k in range(26)])


class RecoveryTests(unittest.TestCase):
    def test_topology_accounts_for_pending_without_accepting_it(self):
        packet = pending()
        packet['roots'][6]['tree'] = dict(kind='split', axis=0, cut='1/2',
            left=dict(kind='leaf', box=[], decision='untrusted', result={}), right=dict(kind='pending'))
        self.assertEqual(recovery.checkpoint_statistics(packet),
                         dict(nodes=28, leaves=1, pending=26, maximum_depth=1))
        self.assertFalse(packet['arithmetic_accepted'])

    def test_malformed_topology_never_becomes_a_resume_candidate(self):
        bad = []
        packet = pending();packet['roots'][0]['k'] = False;bad.append(packet)
        packet = pending();packet['roots'][0]['tree']['accepted'] = True;bad.append(packet)
        packet = pending();packet['roots'].pop();bad.append(packet)
        packet = pending();packet['roots'][0]['tree'] = {'kind': 'shortcut'};bad.append(packet)
        for packet in bad:
            with self.subTest(packet=packet), self.assertRaises(ValueError):
                recovery.checkpoint_statistics(packet)

    def test_selection_prefers_advanced_candidate_and_retains_source_object(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            first = root/'old';first.mkdir()
            second = root/'more';second.mkdir()
            a = pending()
            b = copy.deepcopy(a)
            b['roots'][0]['tree'] = dict(kind='leaf', box=[], decision='untrusted', result={})
            a['binding']['design_sha256'] = recovery.count.TARGETS['b4-q2'][2]
            b['binding']['design_sha256'] = a['binding']['design_sha256']
            recovery.atomic_json(first/'CHECKPOINT.json', a)
            recovery.atomic_json(second/'CHECKPOINT.backup.json', b)
            with patch.object(recovery.epoch, 'migrate_checkpoint', side_effect=lambda value,*_,**__:copy.deepcopy(value)), \
                 patch.object(recovery, 'check_extended_checkpoint', side_effect=lambda value,*_:recovery.checkpoint_statistics(value)):
                source, before, after, stats = recovery.select_checkpoint([root], root/'original', root/'extended')
            self.assertEqual(source.parent.name, 'more')
            self.assertEqual(before, b);self.assertEqual(after, b)
            self.assertEqual(stats['leaves'], 1)

    def test_missing_checkpoint_refuses_fresh_restart(self):
        with tempfile.TemporaryDirectory() as name, self.assertRaisesRegex(ValueError, 'never restarts'):
            root = Path(name)
            recovery.select_checkpoint([root], root/'original', root/'extended')

    def test_search_uses_actual_new_design_and_same_vendor_guard(self):
        with tempfile.TemporaryDirectory() as name:
            task = Path(name)
            capsule = task/'capsule';capsule.mkdir()
            recovery.atomic_json(capsule/'FROZEN_DESIGN.json', {'fixture': 'not mathematical code'})
            previous = task/'input.json';recovery.atomic_json(previous, pending())
            calls = []
            def supervise(argv, **kwargs):
                calls.append((argv, kwargs))
                return dict(status='incomplete', returncode=1)
            with patch.object(recovery.epoch, 'verify'), patch.object(recovery, 'check_extended_checkpoint'), \
                 patch.object(recovery.count, 'supervise', side_effect=supervise):
                result = recovery.search(task, previous, 60)
            argv, kwargs = calls[0]
            self.assertEqual(argv[argv.index('--design-sha256')+1], recovery.count.digest(capsule/'FROZEN_DESIGN.json'))
            self.assertEqual(argv[argv.index('--alpha-priority')+1], '4')
            self.assertEqual(kwargs['mode'], 'untrusted_search')
            self.assertEqual(kwargs['memory_bytes'], 2048*1024**2)
            self.assertFalse(result['arithmetic_accepted'])
            self.assertIsNone(result['search_result'])

    def _run_fixture(self, base, observed=None, complete=False, accepted=None, target='b4-q2'):
        def prepare(task, roots, selected):
            self.assertEqual(selected, target)
            task.mkdir()
            recovery.atomic_json(task/'INPUT_CHECKPOINT.json', pending())
            return dict(design_sha256='a'*64, original_design_sha256='b'*64,
                        migration=dict(source_checkpoint_sha256='c'*64, statistics=dict(nodes=26, leaves=0, pending=26)))
        def search(task, previous, seconds, selected):
            self.assertEqual(selected, target)
            run = task/'search-fixture';run.mkdir()
            return dict(epoch=str(run), observed=observed or dict(status='completed', returncode=0),
                        search_result=dict(status='CANDIDATE_COMPLETE_NOT_ACCEPTED' if complete else 'SEARCH_CHECKPOINTED_INCOMPLETE',
                                           nodes=26, leaves=26 if complete else 0, pending=0 if complete else 26))
        with patch.object(recovery, 'prepare', side_effect=prepare), patch.object(recovery, 'search', side_effect=search), \
             patch.object(recovery, 'accept', side_effect=accepted or ValueError('fixture native guard unavailable')) as accept:
            result = recovery.run_colab(target, durable_root=base/'drive', work_root=base/'work', total_seconds=1)
        return result, accept

    def test_partial_search_does_not_invoke_acceptor(self):
        with tempfile.TemporaryDirectory() as name:
            result, accept = self._run_fixture(Path(name))
        accept.assert_not_called()
        self.assertEqual(result['status']['state'], 'candidate_incomplete_budget_exhausted')
        self.assertFalse(result['status']['native_arithmetic_accepted'])

    def test_native_failure_is_bundled_and_never_accepted(self):
        with tempfile.TemporaryDirectory() as name:
            result, accept = self._run_fixture(Path(name), complete=True)
            self.assertTrue(Path(result['bundle']).is_file())
        accept.assert_called_once()
        self.assertEqual(result['status']['state'], 'incomplete_error')
        self.assertFalse(result['status']['native_arithmetic_accepted'])
        self.assertFalse(result['status']['all_index_conclusion_verified'])

    def test_guarded_stop_retains_diagnostics_and_does_not_accept(self):
        with tempfile.TemporaryDirectory() as name:
            result, accept = self._run_fixture(Path(name), observed=dict(status='incomplete', returncode=1, reason='fixture limit'))
            progress = (Path(result['work'])/'PROGRESS.jsonl').read_text()
            self.assertIn('fixture limit', progress)
        accept.assert_not_called()
        self.assertEqual(result['status']['state'], 'incomplete_guarded_stop')
        self.assertFalse(result['status']['all_index_conclusion_verified'])

    def test_every_target_routes_to_its_own_cache_and_result_directory(self):
        with tempfile.TemporaryDirectory() as name:
            base = Path(name)
            for target in recovery.count.TARGETS:
                with self.subTest(target=target):
                    result, accept = self._run_fixture(base/target, target=target)
                    self.assertEqual(result['status']['target'], target)
                    self.assertEqual(Path(result['work']).parent.name, target)
                    self.assertTrue(Path(result['bundle']).is_file())
                    self.assertFalse(result['status']['native_arithmetic_accepted'])
                    accept.assert_not_called()

    def test_unknown_target_fails_before_creating_work(self):
        with tempfile.TemporaryDirectory() as name:
            base = Path(name)
            with self.assertRaisesRegex(ValueError, 'seven reviewed'):
                recovery.run_colab('another-region', durable_root=base/'drive', work_root=base/'work')
            self.assertFalse((base/'work').exists())


if __name__ == '__main__':
    unittest.main()
