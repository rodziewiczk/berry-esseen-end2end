"""Synthetic source/guard/cache/join tests; original kernels are trap bytes."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import test_finite1039_counts as fixture
from be_replay import finite2630_sources as src,finite2630_counts as run,finite2630_evidence as ev


put=fixture.put


class Counts(unittest.TestCase):
    def setUp(self):
        fixture.Counts.setUp(self)
        self.rows=self.rows[:2]
        for row in self.rows:row['lane']='n26_30'
        self.cat['jobs']=self.rows
        self.declaration=dict(original_census=dict(forests=len(self.rows),**{
            k:sum(r['census'][k]for r in self.rows)for k in('roots','nodes','leaves')}),
            complete_census=dict(forests=len(self.rows)+1,**{
                k:sum(r['census'][k]for r in self.rows)+28 for k in('roots','nodes','leaves')}))
        self.pair=dict(census=dict(roots=28,nodes=28,leaves=28),same_candidate_and_contract_verified=True)
        for name,value in(('jobs',self.rows),('selection',self.declaration)):
            p=patch.object(src,name,return_value=value);p.start();self.addCleanup(p.stop)

    def fake_supervisor(self,*a,**k):return fixture.Counts.fake_supervisor(self,*a,**k)

    def complete(self,name='task',row=None,effect=None):
        task=self.root/name
        with patch.object(run.linux_supervisor,'run',side_effect=effect or self.fake_supervisor),patch.object(run,'Follow'):
            checked=run.execute(task,row or self.row,self.cache)
        return task,checked

    def test_own_epoch_never_claims_old_adapter_or_copies_old_acceptance(self):
        task=self.root/'prepared';m=src.prepare_job(self.row['job_id'],self.cache,task)
        self.assertEqual(m['schema'],src.SCHEMA)
        self.assertEqual(m['source_adapter_sha256'],src.digest(src.__file__))
        self.assertNotEqual(m['source_adapter_sha256'],src.digest(src.old.__file__))
        self.assertFalse((task/'capsule'/src.output_relative(self.row)).exists())
        with self.assertRaises(ValueError):src.old.verify_job(task,self.row)
        (task/'capsule/unbound.py').write_bytes(b'raise AssertionError("unbound import")')
        with self.assertRaises(ValueError):src.verify_job(task)

    def test_observed_false_precedes_validation_and_complete_is_rechecked(self):
        original=ev.validate_run
        def check(task,row,report):
            self.assertFalse(report['conditional_arithmetic_completed'])
            self.assertFalse((Path(task)/'STAGE_COMPLETED.json').exists())
            return original(task,row,report)
        # validate_completed invokes the same routine after writing COMPLETED;
        # the first call alone must be the unaccepted observed transition.
        calls=[]
        def observe(task,row,report):
            calls.append((Path(task)/'STAGE_COMPLETED.json').exists())
            return original(task,row,report)
        with patch.object(ev,'validate_run',side_effect=observe):task,checked=self.complete()
        self.assertEqual(calls,[False,True])
        self.assertTrue(checked['conditional_arithmetic_completed'])
        for f in ev.FLAGS:self.assertIs(checked[f],False)

    def test_relocated_full_stage_preserves_all_receipt_bytes(self):
        for i,row in enumerate(self.rows):
            task,checked=self.complete('family'+str(i),row);other=self.root/('copy'+str(i));shutil.copytree(task,other)
            before={p.relative_to(other).as_posix():p.read_bytes()for p in other.rglob('*')if p.is_file()}
            self.assertEqual(ev.validate_completed(other),checked)
            self.assertEqual(before,{p.relative_to(other).as_posix():p.read_bytes()for p in other.rglob('*')if p.is_file()})

    def test_bad_guard_rc_capture_or_receipt_cannot_create_completed(self):
        changes=(lambda o:o.update(returncode=False),lambda o:o.update(checkpoints=[]),
                 lambda o:o.update(stderr_sha256='0'*64),lambda o:o['guard_scope'].update(proof_acceptance=True))
        for i,change in enumerate(changes):
            def fake(*a,**k):
                o=self.fake_supervisor(*a,**k);change(o);put(Path(k['output_dir'])/'supervisor-result.json',o);return o
            with self.assertRaises(ValueError):self.complete('bad'+str(i),effect=fake)
            self.assertFalse((self.root/('bad'+str(i))/'STAGE_COMPLETED.json').exists())

    def test_bad_whole_stdout_receipt_and_wrong_native_controls_rejected(self):
        task,_=self.complete();row=self.row;path=task/'capsule'/src.output_relative(row)
        answer=src.read(path);answer['negative_controls']=[];put(path,answer)
        with self.assertRaises(ValueError):ev.validate_completed(task)

    def test_cache_requires_sidecar_and_full_validation(self):
        task,checked=self.complete();cache=self.root/'completed';export=run.save_stage(task,cache)
        restored=run.restore_stage(cache,self.root/'restore',self.row)
        self.assertEqual(restored[1],checked)
        p=Path(export['path']);p.with_suffix('.zip.sha256').write_bytes(b'0'*64)
        self.assertIsNone(run.restore_stage(cache,self.root/'bad-sha',self.row))
        # A coherently rehashed transport cannot invent a native receipt.
        p.unlink();p.with_suffix('.zip.sha256').unlink()
        answer=src.read(task/'capsule'/src.output_relative(self.row));answer['status']='DELIBERATE_FAILURE'
        put(task/'capsule'/src.output_relative(self.row),answer)
        with self.assertRaises(ValueError):run.save_stage(task,cache)

    def test_unsafe_cache_paths_missing_ledgers_and_oversized_members(self):
        for name in('../escape','/absolute','a//b','a\\b'):
            with self.subTest(name=name):
                info=zipfile.ZipInfo();info.filename=info.orig_filename=name
                z=unittest.mock.Mock();z.infolist.return_value=[info]
                with self.assertRaises(ValueError):run.cache_members(z)
        info=zipfile.ZipInfo('SOURCES.json');info.file_size=129*src.MIB
        z=unittest.mock.Mock();z.infolist.return_value=[info]
        with self.assertRaises(ValueError):run.cache_members(z)
        z.infolist.return_value=[zipfile.ZipInfo('SOURCES.json')]
        with self.assertRaises(ValueError):run.cache_members(z)

    def test_two_completed_jobs_resume_with_zero_native_calls(self):
        first=self.root/'batch1';first.mkdir();cache=self.root/'durable';status=dict(jobs=[])
        with patch.object(run.linux_supervisor,'run',side_effect=self.fake_supervisor)as native,patch.object(run,'Follow'):
            run.batch_jobs(first,cache,self.cache,status,self.rows)
            self.assertEqual(native.call_count,2)
        second=self.root/'batch2';second.mkdir();again=dict(jobs=[])
        with patch.object(run.linux_supervisor,'run',side_effect=AssertionError('No partial or completed job rerun'))as native:
            run.batch_jobs(second,cache,self.cache,again,self.rows)
            self.assertEqual(native.call_count,0)
        self.assertTrue(all(e['reused_completed_stage']for e in again['jobs']))
        self.assertTrue(all((second/e['task_relative']).is_dir()for e in again['jobs']))

    def test_failure_keeps_prior_completed_stage(self):
        root=self.root/'batch';root.mkdir();state=dict(jobs=[]);calls=0
        def native(*a,**k):
            nonlocal calls
            calls+=1
            if calls==2:raise RuntimeError('Synthetic interruption')
            return self.fake_supervisor(*a,**k)
        with patch.object(run.linux_supervisor,'run',side_effect=native),patch.object(run,'Follow'):
            with self.assertRaises(RuntimeError):run.batch_jobs(root,self.root/'saved',self.cache,state,self.rows)
        self.assertEqual(len(state['jobs']),1)
        self.assertEqual(len(list((self.root/'saved').rglob('*-complete.zip'))),1)

    def test_full_crossjoin_requires_every_job_and_exact_census(self):
        root=self.root/'join';root.mkdir();state=dict(schema='CONDITIONAL_FINITE2630_COMPLETE_COUNT_BATCH_V1',
            selection_sha256=src.SELECTION_SHA256,implementation=ev.implementation(),
            state='complete_selected_conditional_count_arithmetic_basic',conditional_arithmetic_completed=True,
            all_selected_arithmetic_completed=True,jobs=[],recovered64=self.pair,
            actual_census=self.declaration['complete_census'],**{f:False for f in ev.FLAGS})
        with patch.object(run.linux_supervisor,'run',side_effect=self.fake_supervisor),patch.object(run,'Follow'):
            run.batch_jobs(root,self.root/'saved',self.cache,state,self.rows)
        put(root/'SESSION_RESULT.json',state)
        with patch.object(ev,'validate_recovered',return_value=self.pair):
            checked=ev.validate_batch(root);self.assertEqual(checked['actual_census'],state['actual_census'])
            state['jobs'].pop();put(root/'SESSION_RESULT.json',state)
            with self.assertRaises(ValueError):ev.validate_batch(root)

    def test_missing64_exports_waiting_without_any_download_or_native_call(self):
        with (patch.object(run.recovery,'restore_completed',return_value=None),patch.object(src,'obtain_assets')as download,
              patch.object(run.linux_supervisor,'run')as native):
            answer=run.run_colab(durable_root=self.root/'drive',work_root=self.root/'work',backup_interval=60)
        self.assertEqual(answer['status']['state'],'waiting_for_validated64')
        self.assertFalse(answer['status']['conditional_arithmetic_completed'])
        self.assertTrue(Path(answer['bundle']).is_file());download.assert_not_called();native.assert_not_called()

    def test_failed_final_crossjoin_exports_but_revokes_proposed_completion(self):
        with (patch.object(run,'import_recovered_pair',return_value=self.pair),
              patch.object(src,'obtain_assets',return_value={}),patch.object(src,'prepare_cache',return_value=self.cache),
              patch.object(run.linux_supervisor,'run',side_effect=self.fake_supervisor),patch.object(run,'Follow'),
              patch.object(ev,'validate_batch',side_effect=ValueError('Synthetic final join rejection'))):
            answer=run.run_colab(durable_root=self.root/'drive',work_root=self.root/'work',backup_interval=60)
        self.assertEqual(len(answer['status']['jobs']),2)
        self.assertFalse(answer['status']['conditional_arithmetic_completed'])
        self.assertFalse(answer['status']['all_selected_arithmetic_completed'])
        self.assertTrue(Path(answer['bundle']).is_file())
        self.assertFalse((Path(answer['work'])/'BATCH_VALIDATED.json').exists())

    def test_successful_full_run_exports_stable_revalidated_session(self):
        with (patch.object(run,'import_recovered_pair',return_value=self.pair),
              patch.object(src,'obtain_assets',return_value={}),patch.object(src,'prepare_cache',return_value=self.cache),
              patch.object(run.linux_supervisor,'run',side_effect=self.fake_supervisor),patch.object(run,'Follow'),
              patch.object(ev,'validate_recovered',return_value=self.pair)):
            answer=run.run_colab(durable_root=self.root/'drive',work_root=self.root/'work',backup_interval=60)
            root=Path(answer['work']); checked=ev.validate_batch(root)
        self.assertEqual(answer['status']['state'],'complete_selected_conditional_count_arithmetic_basic')
        self.assertTrue(answer['status']['conditional_arithmetic_completed'])
        self.assertEqual(src.read(root/'BATCH_VALIDATED.json'),checked)
        self.assertEqual(checked['session_result_sha256'],src.digest(root/'SESSION_RESULT.json'))
        with zipfile.ZipFile(answer['bundle'])as archive:
            members=[n for n in archive.namelist()if n.endswith('/SESSION_RESULT.json')or n=='SESSION_RESULT.json']
            self.assertEqual(len(members),1)
            self.assertEqual(archive.read(members[0]),(root/'SESSION_RESULT.json').read_bytes())


class RecoveredPair(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.task=self.root/'recovered64/pair';self.capsule=self.task/'capsule';self.capsule.mkdir(parents=True)
        for name in('SOURCES.json','CONSTRUCT_OBSERVED.json','ACCEPT_OBSERVED.json','COMPLETED.json'):
            put(self.task/name,dict(synthetic_unattested=True))
        candidate=put(self.capsule/'COUNT41_FOREST.json',dict(synthetic_complete_roots=True))
        contract=put(self.capsule/'contract.json',dict(synthetic_contract=True))
        (self.capsule/'count_protocol.py').write_bytes(b'raise AssertionError("Never import or execute")\n')
        checker=src.digest(self.capsule/'count_protocol.py')
        put(self.capsule/'CONSTRUCTION_RUN.json',dict(synthetic_only=True))
        accepted=put(self.capsule/'COUNT41_ACCEPTED.json',dict(synthetic_fresh_acceptance=True))
        self.expected=dict(source_plan_sha256='1'*64,candidate_sha256=candidate,contract_sha256=contract,
            checker_sha256=checker,historical_receipt_sha256='2'*64,census=dict(roots=28,nodes=28,leaves=28,maximum_depth=0),
            n=27,index=41,p=['41/100','21/50'],rho=['1','11/10'],contact_allowance='0')
        summary={k:v for k,v in self.expected.items()if k not in('checker_sha256','historical_receipt_sha256')}
        summary.update(historical_candidate_sha256=candidate,historical_acceptance_sha256='2'*64,
                       acceptance_receipt_sha256=accepted)
        self.checked=dict(summary=summary,completed_sha256=src.digest(self.task/'COMPLETED.json'),
                          **{f:False for f in ev.recovered.FLAGS})
        self.archive=self.root/'recovered64/SOURCE_PAIR.zip'
        with zipfile.ZipFile(self.archive,'w')as z:
            for p in self.task.rglob('*'):
                if p.is_file():z.write(p,p.relative_to(self.task).as_posix())
        self.record=dict(schema='IMPORTED_FULL_N27_P41_PAIR_FOR_FINITE2630_V1',selection_sha256=src.SELECTION_SHA256,
            task_relative=self.task.relative_to(self.root).as_posix(),source_zip_relative=self.archive.relative_to(self.root).as_posix(),
            source_zip_sha256=src.digest(self.archive),validated=self.checked,conditional_arithmetic_completed=False,
            **{f:False for f in ev.FLAGS})
        put(self.root/'RECOVERED64.json',self.record)
        p=patch.object(src,'selection',side_effect=lambda:dict(recovered=self.expected));p.start();self.addCleanup(p.stop)
        self.validate=patch.object(ev.recovered,'validate_completed',return_value=self.checked).start()
        self.addCleanup(patch.stopall)

    def test_full_pair_validator_and_identical_candidate_gate_both_required(self):
        checked=ev.validate_recovered(self.root)
        self.assertTrue(checked['same_candidate_and_contract_verified'])
        self.assertFalse(checked['parent_acquisitions_verified'])
        self.validate.assert_called_once_with(self.task)
        self.assertEqual(checked['fresh_acceptance_sha256'],self.checked['summary']['acceptance_receipt_sha256'])
        self.assertNotEqual(checked['fresh_acceptance_sha256'],checked['historical_acceptance_sha256'])

    def test_public_full_pair_rejection_is_never_bypassed(self):
        self.validate.side_effect=ValueError('Reject incomplete or invalid original64 evidence')
        with self.assertRaises(ValueError):ev.validate_recovered(self.root)

    def test_cross_profile_candidate_contract_or_checker_substitution_rejected(self):
        for key in('candidate_sha256','contract_sha256','checker_sha256'):
            old=self.expected[key];self.expected[key]='0'*64
            with self.assertRaises(ValueError):ev.validate_recovered(self.root)
            self.expected[key]=old

    def test_mutated_exported_receipt_cannot_match_preserved_zip(self):
        put(self.capsule/'COUNT41_ACCEPTED.json',dict(synthetic_forged=True))
        with self.assertRaises(ValueError):ev.validate_recovered(self.root)
        self.validate.assert_not_called()

    def test_missing_constructor_evidence_is_not_an_accepted_pair(self):
        (self.task/'CONSTRUCT_OBSERVED.json').unlink()
        with self.assertRaises(ValueError):ev.validate_recovered(self.root)
        self.validate.assert_not_called()

    def test_wrong_zip_hash_or_source_root_traversal_rejected(self):
        for change in(dict(source_zip_sha256='0'*64),dict(task_relative='../outside')):
            record=self.record|change;put(self.root/'RECOVERED64.json',record)
            with self.assertRaises(ValueError):ev.validate_recovered(self.root)
        self.validate.assert_not_called()


class Selection(unittest.TestCase):
    def test_actual_compact_selection_and_original_readiness_are_distinct(self):
        rows=src.jobs();d=src.selection();self.assertEqual(len(rows),79)
        self.assertFalse(src.old.catalog()['lane_ready']['n26_30'])
        self.assertEqual(d['complete_census'],dict(forests=80,roots=2316,nodes=150296,leaves=76306))
        self.assertEqual({v['archive']for v in src.selected_files().values()},
                         {'cutoff25_20261011.zip','cutoff25_continue_20261015.zip'})
        self.assertTrue(all(r['arguments']==['accept']and r['family']=='count_protocol'for r in rows))


if __name__=='__main__':unittest.main()
