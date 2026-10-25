"""Full evidence / cache / dispatcher tests, using non-executable synthetic math."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
import time
import unittest
from unittest.mock import patch

from be_replay import count_task as common, n25_recovered_counts as runner
from be_replay import n25_recovered_counts_evidence as evidence, n25_full_counts as dispatcher
from tests import test_retained_n25_extra_evidence as fixtures


class RecoveredEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.RetainedEvidenceTests('test_complete_stage_and_preledger_validation_do_not_execute_trap_source')
        self.f.setUp(); self.addCleanup(self.f.doCleanups)
        self.target = 'synthetic-original'
        self.census = dict(self.f.census,pending=0,arithmetic_accepted=False)
        spec = dict(index=37,kind='ordinary-v14',files={r['filename']:r for r in self.f.files
                                                    if r['filename']!='COUNT37_FOREST.json'},design_sha256='1'*64)
        for obj,name,value in (
            (evidence.sources,'normalize',lambda t:self.target),
            (evidence.sources,'profile',lambda *a,**k:spec),
            (evidence.sources,'verify',lambda *a,**k:spec),
            (evidence.sources,'verify_preparation',lambda *a,**k:{}),
            (evidence.sources,'geometry',lambda *a,**k:self.census)):
            p=patch.object(obj,name,value);p.start();self.addCleanup(p.stop)
        for name in ('NATIVE_OBSERVED.json','NATIVE_ACCEPTED.json'):(self.f.epoch/name).unlink()
        before=dict(schema=evidence.SCHEMA,target=self.target,scope=evidence.SCOPE,epoch=str(self.f.epoch),
                    observed=self.f.observed,census=self.census,implementation=evidence.implementation(),
                    arithmetic_accepted=False,parent_acquisitions_verified=False,full66_complete=False)
        common.write(self.f.epoch/'NATIVE_OBSERVED.json',before)
        common.write(self.f.epoch/'NATIVE_ACCEPTED.json',dict(before,arithmetic_accepted=True,
                     native_receipt=str(self.f.capsule/'COUNT37_ACCEPTED.json'),
                     native_receipt_sha256=common.digest(self.f.capsule/'COUNT37_ACCEPTED.json'),
                     negative_controls=24,conditional_premises=evidence.premises(self.target)))

    def validate(self):return evidence.validate_stage(self.f.task,self.target,self.f.epoch)

    def change(self,path,fn):
        value=common.read(path);fn(value);path.write_text(json.dumps(value),encoding='utf-8')

    def test_complete_stage_is_conditional_and_not_full66(self):
        value=self.validate()
        self.assertTrue(value['native_arithmetic_accepted'])
        self.assertFalse(value['parent_acquisitions_verified'])
        self.assertFalse(value['full66_complete'])
        self.assertEqual(value['negative_controls'],24)

    def test_receipt_schema_count_controls_and_elapsed_are_strict(self):
        path=self.f.capsule/'COUNT37_ACCEPTED.json';raw=path.read_bytes()
        for change in (lambda x:x.update(fresh_leaf_evaluations=25),lambda x:x['negative_controls'].pop(),
                       lambda x:x.update(seconds=True),lambda x:x.update(extra_success=True),
                       lambda x:x.update(contract_sha256='0'*64)):
            self.change(path,change)
            with self.assertRaises((ValueError,KeyError)):self.validate()
            path.write_bytes(raw)

    def test_full_captures_and_successful_transport_required(self):
        for name in ('stdout.txt','stderr.txt'):
            path=self.f.execution/name;raw=path.read_bytes();path.write_bytes(raw+b'corrupted')
            with self.assertRaises(ValueError):self.validate()
            path.write_bytes(raw)
        p=self.f.execution/'supervisor-result.json'
        self.change(p,lambda x:x.update(returncode=1))
        with self.assertRaises(ValueError):self.validate()

    def test_missing_native_capability_and_changed_source_rejected(self):
        p=self.f.execution/'native-worker-guard.json'
        raw=p.read_bytes();self.change(p,lambda x:x.update(cpu_seconds=2))
        with self.assertRaises(ValueError):self.validate()
        p.write_bytes(raw)
        (self.f.capsule/'count_protocol.py').write_text('raise ValueError("changed")\n')
        with self.assertRaises(ValueError):self.validate()

    def test_false_global_promotion_and_partial_transition_rejected(self):
        p=self.f.epoch/'NATIVE_ACCEPTED.json';raw=p.read_bytes()
        for change in (lambda x:x.update(arithmetic_accepted=False),lambda x:x.update(full66_complete=True),
                       lambda x:x.update(parent_acquisitions_verified=True),lambda x:x.update(negative_controls=True)):
            self.change(p,change)
            with self.assertRaises(ValueError):self.validate()
            p.write_bytes(raw)
        (self.f.epoch/'NATIVE_OBSERVED.json').unlink()
        with self.assertRaises((ValueError,OSError)):self.validate()

    def test_wrong_implementation_and_source_plan_rejected(self):
        for name in ('NATIVE_OBSERVED.json','NATIVE_ACCEPTED.json'):
            self.change(self.f.epoch/name,lambda x:x['implementation'].update(count_source_plan_sha256='0'*64))
        with self.assertRaisesRegex(ValueError,'implementation'):self.validate()

    def test_real_cache_roundtrip_relocation_preserves_receipts(self):
        directory=self.f.root/'cache'
        raw=(self.f.epoch/'NATIVE_ACCEPTED.json').read_bytes()
        saved=runner.save_stage(self.f.task,self.target,self.f.epoch,directory)
        other=self.f.root/'relocated';other.mkdir()
        restored=runner.restore_stage(other,self.target,directory)
        self.assertIsNotNone(restored)
        self.assertEqual((restored[0]/'NATIVE_ACCEPTED.json').read_bytes(),raw)
        self.assertFalse(restored[1]['full66_complete'])
        # A second call validates the existing epoch without overwriting it.
        self.assertIsNotNone(runner.restore_stage(other,self.target,directory))
        self.assertEqual(saved.with_suffix('.zip.sha256').read_text(),common.digest(saved)+'  '+saved.name+'\n')

    def test_corrupted_cache_sidecar_and_truncated_bundle_rejected(self):
        directory=self.f.root/'cache'
        saved=runner.save_stage(self.f.task,self.target,self.f.epoch,directory)
        marker=saved.with_suffix('.zip.sha256');raw=marker.read_bytes();marker.write_text('0'*64+'\n')
        destination=self.f.root/'bad';destination.mkdir()
        self.assertIsNone(runner.restore_stage(destination,self.target,directory))
        marker.write_bytes(raw)
        saved.write_bytes(saved.read_bytes()[:100])
        self.assertIsNone(runner.restore_stage(destination,self.target,directory))

    def test_native_launch_only_accept_and_no_old_receipt(self):
        task=self.f.root/'launch-task';task.mkdir()
        shutil.copytree(self.f.source,task/'capsule')
        def observe(argv,**kwargs):
            capsule=Path(kwargs['cwd'])
            self.assertEqual(argv[1:3],['-B','-S'])
            self.assertEqual(argv[-1],'accept')
            self.assertEqual(kwargs['mode'],'trusted_native')
            self.assertEqual(kwargs['checkpoint_paths'],[])
            self.assertFalse((capsule/'COUNT37_ACCEPTED.json').exists())
            raise RuntimeError('synthetic-stop-before-any-math')
        with patch.object(common,'supervise',side_effect=observe) as launch:
            with self.assertRaisesRegex(RuntimeError,'synthetic-stop'):runner.accept(task,self.target)
            self.assertEqual(launch.call_count,1)

    def test_timeout_budget_does_not_trigger_discovery_or_native(self):
        task=self.f.root/'empty-task';task.mkdir()
        with patch.object(common,'supervise',side_effect=AssertionError('must not start')):
            result=runner.run_target(task,self.target,self.f.root/'durable',deadline=time.monotonic()-1)
        self.assertEqual(result['state'],'incomplete_native_replay_pending')
        self.assertFalse(result['full66_complete'])


class DispatcherTests(unittest.TestCase):
    def test_default_preparation_uses_original_lane(self):
        with patch.object(runner,'prepare',return_value={'fixture':True}) as p:
            result=dispatcher.prepare('task','b5-p26-v14-new',recovery_archive='original.zip')
        self.assertEqual(result,{'fixture':True})
        p.assert_called_once_with('task','b5-p26-v14-new',archive='original.zip')

    def test_preparation_rejects_mixed_source_choices(self):
        with self.assertRaisesRegex(ValueError,'Choose'):
            dispatcher.prepare('task','target','legacy',recovery_archive='original.zip')

    def test_recovered_marker_dispatches_without_legacy_search(self):
        with tempfile.TemporaryDirectory() as tmp:
            task=Path(tmp);(task/'RECOVERY_INPUTS.json').write_text('{}')
            with patch.object(runner,'run_target',return_value={'original':True}) as p,\
                 patch.object(dispatcher,'search',side_effect=AssertionError('no discovery')):
                self.assertEqual(dispatcher.run_target(task,'target','durable',deadline=1),{'original':True})
            self.assertEqual(p.call_count,1)

    def test_invalid_original_does_not_silently_fall_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            task=Path(tmp);(task/'RECOVERY_INPUTS.json').write_text('{}')
            with patch.object(runner,'run_target',side_effect=ValueError('bad original')),\
                 patch.object(dispatcher,'search',side_effect=AssertionError('no fallback')):
                with self.assertRaisesRegex(ValueError,'bad original'):
                    dispatcher.run_target(task,'target','durable',deadline=1)

    def test_ambiguous_original_and_legacy_markers_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            task=Path(tmp)
            for name in ('RECOVERY_INPUTS.json','TASK.json'):(task/name).write_text('{}')
            with self.assertRaisesRegex(ValueError,'mixed original'):
                dispatcher.run_target(task,'target','durable',deadline=1)

if __name__=='__main__':unittest.main()
