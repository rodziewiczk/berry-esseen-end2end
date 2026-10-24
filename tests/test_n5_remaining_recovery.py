"""Complete-stage recovery transport fixtures; no original arithmetic runs."""
import copy,hashlib,io,json,stat,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
from be_replay import n5_remaining_recovery as recovery,n5_remaining_sources as src,n5_remaining_evidence as ev

class Recovery(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=src.ROOT.parent,prefix='t35recover-');self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
    def archive(self,extra=()):
        p=self.root/'source.zip'
        with zipfile.ZipFile(p,'w')as z:
            for name in('JOB_SOURCE.json','STAGE_OBSERVED.json','STAGE_COMPLETED.json'):
                z.writestr(recovery.PREFIX+name,'{}\n')
            for name,value in extra:z.writestr(recovery.PREFIX+name,value)
        return p
    def admitted(self,p):
        from contextlib import ExitStack
        stack=ExitStack();stack.enter_context(patch.object(recovery,'ARCHIVE_SHA256',src.digest(p)))
        stack.enter_context(patch.object(recovery,'ARCHIVE_BYTES',p.stat().st_size));return stack
    def test_only_selected_whole_task_is_extracted_without_executing_it(self):
        p=self.archive([('trap.py','raise AssertionError("Never run fake mathematics")\n')])
        with self.admitted(p):dest=recovery.extract_selected(p,self.root/'restored')
        self.assertEqual(set(x.name for x in dest.iterdir()),{'JOB_SOURCE.json','STAGE_OBSERVED.json','STAGE_COMPLETED.json','trap.py'})
    def test_unpinned_bundle_is_rejected_before_extraction(self):
        p=self.archive()
        with self.assertRaises(ValueError):recovery.extract_selected(p,self.root/'rejected')
        self.assertFalse((self.root/'rejected').exists())
    def test_traversal_case_alias_or_link_is_rejected_before_any_write(self):
        for i,name in enumerate(('../outside','stage_completed.JSON')):
            p=self.root/f'bad{i}.zip'
            with zipfile.ZipFile(p,'w')as z:
                for normal in('JOB_SOURCE.json','STAGE_OBSERVED.json','STAGE_COMPLETED.json'):z.writestr(recovery.PREFIX+normal,'{}')
                z.writestr(recovery.PREFIX+name,'bad')
            with self.admitted(p),self.assertRaises(ValueError):recovery.extract_selected(p,self.root/f'reject{i}')
            self.assertFalse((self.root/f'reject{i}').exists())
        p=self.root/'link.zip';info=zipfile.ZipInfo(recovery.PREFIX+'link');info.external_attr=(stat.S_IFLNK|0o777)<<16
        with zipfile.ZipFile(p,'w')as z:z.writestr(info,'target')
        with self.admitted(p),self.assertRaises(ValueError):recovery.extract_selected(p,self.root/'link-reject')
    def test_missing_saved_bundle_keeps_all_proof_flags_false(self):
        with patch.object(recovery.run,'restore_stage',return_value=None),patch.object(recovery.run.linux_supervisor,'run',side_effect=AssertionError('No arithmetic'))as child:
            out=recovery.recover_saved_initial(durable_root=self.root/'drive',work_root=self.root/'work')
        child.assert_not_called();self.assertEqual(out['state'],'saved_bundle_unavailable_normal_initial_replay_required')
        self.assertIs(out['full_n5_verified'],False);self.assertIs(out['mathematical_replay'],False)
    def test_existing_fully_revalidated_cache_needs_no_saved_bundle_or_arithmetic(self):
        with patch.object(recovery.run,'restore_stage',return_value=(self.root,{},dict(sha256='a'*64))),\
             patch.object(recovery.run.linux_supervisor,'run',side_effect=AssertionError('No arithmetic'))as child:
            out=recovery.recover_saved_initial(durable_root=self.root/'drive',work_root=self.root/'work')
        child.assert_not_called();self.assertEqual(out['state'],'existing_complete_initial_revalidated')

class PriorCache(unittest.TestCase):
    def test_complete_old_reader_packet_still_gets_full_current_validation(self):
        from test_n5_remaining import fixture,put
        with tempfile.TemporaryDirectory(dir=src.ROOT.parent)as tmp:
            task,row,request,report=fixture(Path(tmp)/'original')
            old=dict(ev.implementation(),**{'n5_remaining_evidence.py':ev.LEGACY_METADATA_READER_SHA256})
            report['implementation']=old;put(task/'STAGE_OBSERVED.json',report)
            with patch.object(src,'verify_job',return_value=request),patch.object(src,'job',return_value=row):
                summary=ev.validate_run(task,row,report)
                put(task/'STAGE_COMPLETED.json',dict(schema=ev.SCHEMA,scope=ev.SCOPE,job_id=row['job_id'],
                    implementation=old,observed_sha256=src.digest(task/'STAGE_OBSERVED.json'),summary=summary,
                    artifacts=ev.inventory(task),conditional_arithmetic_completed=True,native_arithmetic_accepted=False,
                    fresh_parent_fact_joins_verified=False,full_n5_verified=False,all_index_conclusion_verified=False))
                self.assertTrue(ev.validate_completed(task)['conditional_arithmetic_completed'])
                report['observed']['returncode']=False;put(task/'STAGE_OBSERVED.json',report)
                with self.assertRaises(ValueError):ev.validate_completed(task)

if __name__=='__main__':unittest.main()
