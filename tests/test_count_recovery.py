"""Synthetic recovery orchestration traps; no numerical module executes."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
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
        def prepare(task, roots, selected, *, strategy):
            self.assertEqual(selected, target)
            self.assertEqual(strategy, recovery.DISCOVERY_STRATEGY)
            task.mkdir()
            recovery.atomic_json(task/'INPUT_CHECKPOINT.json', pending())
            return dict(design_sha256='a'*64, original_design_sha256='b'*64,
                        migration=dict(source_checkpoint_sha256='c'*64, statistics=dict(nodes=26, leaves=0, pending=26)))
        def search(task, previous, seconds, selected, *, strategy):
            self.assertEqual(selected, target)
            self.assertEqual(strategy, recovery.DISCOVERY_STRATEGY)
            run = task/'search-fixture';run.mkdir()
            packet = pending()
            if complete:
                for root in packet['roots']:
                    root['tree'] = dict(kind='leaf', box=[], decision='TRAP', result={})
            recovery.atomic_json(run/'candidate/CHECKPOINT.json', packet)
            return dict(epoch=str(run), observed=observed or dict(status='completed', returncode=0),
                        search_result=dict(status='CANDIDATE_COMPLETE_NOT_ACCEPTED' if complete else 'SEARCH_CHECKPOINTED_INCOMPLETE',
                                           nodes=26, leaves=26 if complete else 0, pending=0 if complete else 26))
        def select(roots, original, capsule, selected, **kwargs):
            path = roots[0]/'CHECKPOINT.json'
            packet = recovery.count.read(path)
            return path, packet, packet, recovery.checkpoint_statistics(packet)
        with patch.object(recovery, 'prepare', side_effect=prepare), patch.object(recovery, 'search', side_effect=search), \
             patch.object(recovery, 'restore_saved_archives', return_value=[]), \
             patch.object(recovery, 'completed_cache', return_value=None), \
             patch.object(recovery, 'select_checkpoint', side_effect=select), \
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

    def test_boolean_returncode_never_dispatches_even_complete_candidate_to_native(self):
        with tempfile.TemporaryDirectory() as name:
            result, accept = self._run_fixture(Path(name), complete=True,
                observed=dict(status='completed', returncode=False))
        accept.assert_not_called()
        self.assertEqual(result['status']['state'], 'incomplete_guarded_stop')

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


class RestoredMigrationTests(unittest.TestCase):
    """Source/geometry fixtures: there is no imported oracle or mathematical code."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.capsule = self.root/'capsule'
        self.capsule.mkdir()
        recovery.atomic_json(self.capsule/'FROZEN_DESIGN.json', {'trap': 'source only'})
        recovery.atomic_json(self.capsule/'contract.json', {'rows': [dict(n=25, index=29,
            p=['29/100', '3/10'], Lambda='1', d0='1/10')]})
        self.header = dict(schema='TRAP_NATIVE_HEADER_V1', n=25, index=29,
            checker_sha256='c'*64, contract_sha256='d'*64, kernel_sha256={'trap.py': 'e'*64})
        self.strategy = dict(discovery_strategy=recovery.DISCOVERY_STRATEGY, search_sha256='f'*64,
            discovery_sources_sha256={'prefix2_strategy.py': 'a'*64}, alpha_priority='16', traversal='depth')
        self.patches = [patch.object(recovery.epoch, 'verify', return_value={}),
                        patch.object(recovery.count, 'native_header', return_value=self.header),
                        patch.object(recovery, 'discovery_binding', return_value=self.strategy)]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.temp.cleanup()

    def packet(self):
        packet = pending()
        packet['binding'] = dict(design_sha256=recovery.count.digest(self.capsule/'FROZEN_DESIGN.json'),
            native_header=dict(copy.deepcopy(self.header), target=recovery.NATIVE_TARGET),
            search_sha256=recovery.LEGACY_SEARCH_SHA256, alpha_priority='4', traversal='root-first')
        return packet

    def leaf(self, *, alpha=('0', '1')):
        return dict(kind='leaf', box=[['29/100', '3/10'], ['0', '1'], list(alpha),
                                     ['-1/2', '1/2'], ['0', '1/10']],
                    decision='TRAP_SAVED_NOT_ACCEPTED', result={'not_evaluated': True})

    def test_explicit_transition_preserves_every_root_leaf_payload_and_input(self):
        before = self.packet()
        before['roots'][7]['tree'] = dict(kind='split', axis=2, cut='1/2',
            left=self.leaf(alpha=('0', '1/2')), right=dict(kind='pending'))
        saved = copy.deepcopy(before)
        after = recovery.migrate_discovery_checkpoint(before, self.capsule)
        self.assertEqual(before, saved)
        self.assertEqual(recovery.epoch.canonical(after['roots']), recovery.epoch.canonical(before['roots']))
        self.assertEqual(after['binding']['native_header'], before['binding']['native_header'])
        self.assertEqual(after['binding']['design_sha256'], before['binding']['design_sha256'])
        self.assertEqual({k: after['binding'][k] for k in recovery.DISCOVERY_FIELDS}, self.strategy)
        self.assertEqual(recovery.check_extended_checkpoint(after, self.capsule, require_restored=True),
                         dict(nodes=28, leaves=1, pending=26, maximum_depth=1))
        self.assertFalse(after['arithmetic_accepted'])
        self.assertEqual(recovery.migrate_discovery_checkpoint(after, self.capsule), after)

    def test_target_kernel_search_and_strategy_mismatches_fail_closed(self):
        mutations = [lambda p: p['binding']['native_header'].update(index=31),
                     lambda p: p['binding']['native_header'].update(target='1'),
                     lambda p: p['binding']['native_header']['kernel_sha256'].update(extra='0'*64),
                     lambda p: p['binding'].update(search_sha256='0'*64),
                     lambda p: p['binding'].update(alpha_priority='16'),
                     lambda p: p.update(arithmetic_accepted=True)]
        for mutation in mutations:
            packet = self.packet()
            mutation(packet)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                recovery.migrate_discovery_checkpoint(packet, self.capsule)

    def test_bad_cut_leaf_box_boolean_axis_and_truncated_tree_are_rejected(self):
        for variant in ('cut', 'box', 'axis', 'child'):
            packet = self.packet()
            tree = dict(kind='split', axis=2, cut='1/2',
                        left=self.leaf(alpha=('0', '1/2')), right=dict(kind='pending'))
            packet['roots'][0]['tree'] = tree
            if variant == 'cut': tree['cut'] = '1'
            elif variant == 'box': tree['left']['box'][2] = ['0', '1']
            elif variant == 'axis': tree['axis'] = True
            else: tree.pop('right')
            with self.subTest(variant=variant), self.assertRaises(ValueError):
                recovery.migrate_discovery_checkpoint(packet, self.capsule)

    def test_new_binding_cannot_carry_unbound_helper_or_extra_strategy_claim(self):
        for mutation in (lambda b: b['discovery_sources_sha256'].update(unbound='0'*64),
                         lambda b: b.update(accepted_strategy=True)):
            packet = recovery.migrate_discovery_checkpoint(self.packet(), self.capsule)
            mutation(packet['binding'])
            with self.assertRaises(ValueError):
                recovery.migrate_discovery_checkpoint(packet, self.capsule)

    def test_selection_uses_descendance_and_reports_truncated_newer_copy(self):
        old, new = self.packet(), self.packet()
        new['roots'][0]['tree'] = self.leaf()
        a, b, c = [self.root/s for s in ('ancestor', 'descendant', 'truncated')]
        recovery.atomic_json(a/'CHECKPOINT.json', old)
        recovery.atomic_json(b/'CHECKPOINT.backup.json', new)
        c.mkdir();(c/'CHECKPOINT.json').write_text('{"roots":')
        rejected = []
        path, before, after, census = recovery.select_checkpoint([a, b, c], self.root/'old', self.capsule,
            strategy=recovery.DISCOVERY_STRATEGY, diagnostics=rejected)
        self.assertEqual(path, b/'CHECKPOINT.backup.json')
        self.assertEqual(before, new)
        self.assertEqual(after['roots'], new['roots'])
        self.assertEqual(census['leaves'], 1)
        self.assertEqual(rejected[0]['path'], str(c/'CHECKPOINT.json'))

    def test_incomparable_lineages_never_choose_largest_leaf_count(self):
        a, b = self.packet(), self.packet()
        a['roots'][0]['tree'] = dict(kind='split', axis=2, cut='1/2',
            left=self.leaf(alpha=('0', '1/2')), right=dict(kind='pending'))
        b['roots'][0]['tree'] = dict(kind='split', axis=2, cut='1/4',
            left=dict(kind='pending'), right=dict(kind='pending'))
        recovery.atomic_json(self.root/'a/CHECKPOINT.json', a)
        recovery.atomic_json(self.root/'b/CHECKPOINT.json', b)
        with self.assertRaisesRegex(ValueError, 'Ambiguous incompatible checkpoint lineages'):
            recovery.select_checkpoint([self.root], self.root/'old', self.capsule,
                                       strategy=recovery.DISCOVERY_STRATEGY)

    def test_prepare_preserves_original_source_bytes_and_records_full_transition(self):
        raw = json.dumps(self.packet(), indent=3).encode()+b'\n\n'
        source = self.root/'saved/CHECKPOINT.json'
        source.parent.mkdir();source.write_bytes(raw)
        task = self.root/'new-task'
        def old_sources(roots, destination, target):
            recovery.shutil.copytree(self.capsule, destination)
            return dict(source_design_sha256='0'*64, copied_source_files=0, historical_receipts_copied=False)
        def build(original, destination, target):
            recovery.shutil.copytree(self.capsule, destination)
            return {'fixture': 'source-only trap'}
        with patch.object(recovery, '_old_sources', side_effect=old_sources), \
             patch.object(recovery.epoch, 'build', side_effect=build), \
             patch.object(recovery, 'implementation', return_value={'fixture': 'no mathematical imports'}):
            report = recovery.prepare(task, [source.parent], strategy=recovery.DISCOVERY_STRATEGY)
        self.assertEqual((task/'SOURCE_CHECKPOINT.json').read_bytes(), raw)
        migration = report['migration']
        self.assertEqual(migration['migration_type'], recovery.MIGRATION_TYPE)
        self.assertEqual(migration['before_statistics'], migration['after_statistics'])
        self.assertEqual(migration['input_checkpoint_sha256'], recovery.count.digest(task/'INPUT_CHECKPOINT.json'))
        self.assertEqual(migration['target_strategy'], self.strategy)
        self.assertTrue(migration['roots_preserved'])
        self.assertFalse(migration['arithmetic_accepted'])
        self.assertFalse(report['all_index_conclusion_verified'])

    def test_search_dispatches_explicit_new_strategy_without_evaluating_math(self):
        packet = recovery.migrate_discovery_checkpoint(self.packet(), self.capsule)
        task = self.root
        previous = task/'input.json';recovery.atomic_json(previous, packet)
        with patch.object(recovery.count, 'supervise', return_value=dict(status='incomplete', returncode=1)) as guard:
            report = recovery.search(task, previous, 1, strategy=recovery.DISCOVERY_STRATEGY)
        argv = guard.call_args.args[0]
        self.assertEqual(argv[argv.index('--strategy')+1], recovery.DISCOVERY_STRATEGY)
        self.assertEqual(argv[argv.index('--alpha-priority')+1], '16')
        self.assertEqual(argv[argv.index('--order')+1], 'depth')
        self.assertEqual(recovery.count.read(Path(report['epoch'])/'resume.json'), packet)
        self.assertFalse(report['arithmetic_accepted'])


class SavedCacheTests(unittest.TestCase):
    def archive(self, root, entries):
        path = root/'saved-results.zip'
        with zipfile.ZipFile(path, 'w') as zipped:
            for name, raw in entries:
                info = zipfile.ZipInfo('placeholder')
                info.filename = info.orig_filename = name
                zipped.writestr(info, raw)
        path.with_suffix('.zip.sha256').write_text(recovery.count.digest(path)+'  '+path.name+'\n')
        return path

    def test_restore_preserves_exact_checkpoint_source_bytes_and_rechecks_cached_copy(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            raw = b'{"fixture": "untrusted checkpoint bytes"}\n\n'
            path = self.archive(root, [('run/task/search-a/candidate/CHECKPOINT.json', raw),
                                       ('run/UNRELATED.txt', b'not imported')])
            restored = recovery.restore_cache_archive(path, root/'imports')
            self.assertEqual((restored/'run/task/search-a/candidate/CHECKPOINT.json').read_bytes(), raw)
            self.assertFalse((restored/'run/UNRELATED.txt').exists())
            self.assertEqual(recovery.restore_cache_archive(path, root/'imports'), restored)
            (restored/'run/task/search-a/candidate/CHECKPOINT.json').write_bytes(raw+b' ')
            marker = recovery.count.read(restored/'CACHE_RESTORE.json')
            marker['files_sha256']['run/task/search-a/candidate/CHECKPOINT.json'] = recovery.hashlib.sha256(raw+b' ').hexdigest()
            recovery.atomic_json(restored/'CACHE_RESTORE.json', marker)
            with self.assertRaisesRegex(ValueError, 'byte-identical'):
                recovery.restore_cache_archive(path, root/'imports')

    def test_zip_traversal_duplicate_case_backslash_and_hash_mismatch_fail_before_extraction(self):
        cases = [[('../task/CHECKPOINT.json', b'{}')],
                 [('run/task/CHECKPOINT.json', b'{}'), ('run/task/checkpoint.json', b'{}')],
                 [('run\\task\\CHECKPOINT.json', b'{}')]]
        for entries in cases:
            with self.subTest(entries=entries), tempfile.TemporaryDirectory() as name:
                root = Path(name);path = self.archive(root, entries)
                with self.assertRaises(ValueError):
                    recovery.restore_cache_archive(path, root/'imports')
                self.assertFalse((root/'imports').exists())
        with tempfile.TemporaryDirectory() as name:
            root = Path(name);path = self.archive(root, [('run/task/CHECKPOINT.json', b'{}')])
            path.with_suffix('.zip.sha256').write_text('0'*64)
            with self.assertRaisesRegex(ValueError, 'matches its SHA256'):
                recovery.restore_cache_archive(path, root/'imports')

    def test_zip_requires_sidecar_and_bounded_expansion(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name);path = self.archive(root, [('run/task/CHECKPOINT.json', b'{}')])
            with patch.object(recovery, 'MAX_CACHE_EXPANDED_BYTES', 1), self.assertRaisesRegex(ValueError, 'expansion'):
                recovery.restore_cache_archive(path, root/'imports')
            path.with_suffix('.zip.sha256').unlink()
            with self.assertRaisesRegex(ValueError, 'requires its actual'):
                recovery.restore_cache_archive(path, root/'imports')

    def test_completed_cache_reuse_runs_no_search_preparation_or_native_acceptor(self):
        with tempfile.TemporaryDirectory() as name:
            base = Path(name)
            accepted = dict(native_arithmetic_accepted=True, parent_acquisitions_verified=False,
                            all_index_conclusion_verified=False, receipt_sha256='a'*64)
            with patch.object(recovery, 'restore_saved_archives', return_value=[]), \
                 patch.object(recovery, 'completed_cache', return_value=(base/'old/task', accepted)), \
                 patch.object(recovery, 'copy_completed_cache', return_value=accepted), \
                 patch.object(recovery, 'prepare') as prepare, patch.object(recovery, 'search') as search, \
                 patch.object(recovery, 'accept') as native:
                result = recovery.run_colab(durable_root=base/'drive', work_root=base/'work', total_seconds=1)
            prepare.assert_not_called();search.assert_not_called();native.assert_not_called()
            self.assertTrue(result['status']['completed_cache_reused'])
            self.assertTrue(result['status']['native_arithmetic_accepted'])
            self.assertFalse(result['status']['all_index_conclusion_verified'])
            self.assertTrue(Path(result['bundle']).is_file())

    def test_completed_cache_needs_full_validator_not_accepted_label(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            recovery.atomic_json(root/'run/task/TASK.json', {'target': 'b4-q2', 'schema': recovery.TASK_SCHEMA})
            recovery.atomic_json(root/'run/task/accept-aaaaaaaaaaaa/NATIVE_ACCEPTED.json', {'arithmetic_accepted': True})
            with patch.object(recovery, '_validate_completed_task', side_effect=ValueError('forged receipt')) as validate:
                self.assertIsNone(recovery.completed_cache([root], 'b4-q2'))
            validate.assert_called_once()


if __name__ == '__main__':
    unittest.main()
