"""67 infrastructure and evidence corruption fixtures; no original arithmetic."""
from __future__ import annotations
from copy import deepcopy
import importlib.util,json,tempfile,unittest,zipfile
from pathlib import Path
from unittest import mock
from be_replay import n5_full_join_sources as src,n5_full_join_control_evidence as ev
from be_replay import n5_full_join_semantics as sem,n5_full_join_evidence as evidence,n5_full_join_inputs as upstream
from be_replay.colab_batch import atomic_json

ROOT=Path(__file__).resolve().parents[1]

class Scope(unittest.TestCase):
    def test_all22_original_actions_and47_source_reference_partition(self):
        p=src.plan();self.assertEqual(len(p['actions']),22);self.assertEqual(len(p['groups']),15)
        self.assertEqual(sum(len(g['action_ids'])for g in p['groups']),22)
        self.assertEqual(len(p['groups'][-1]['action_ids']),8)
        self.assertEqual(p['count_forests'],295);self.assertEqual(p['count_leaves'],75178)
        self.assertGreater(len(p['files']),16000)
        partition=src.read(ROOT/'proof/remaining_n5_delivery_partition.json',8*src.MIB)
        self.assertEqual(len(partition['original_resource_and_count_semantic_reference_actions']),24)
        self.assertEqual(len(sem.CASES),12)
        self.assertFalse(p['original_mathematics_executed'])

    def test_original_graph_pins_and_entry_closure(self):
        p=src.plan()
        for action in p['actions']:
            entry=action['cwd']+'/'+action['argv'][1]
            self.assertIn(entry,p['files'])
            for name in action['outputs']:
                self.assertIn(name,p['files']);self.assertIn(name,action['expected_outputs'])
            self.assertTrue(set(action['outputs']).isdisjoint(action['inputs']))
        self.assertIn('work/cutoff5_20261020/root/count_identity_controls_v1/check.py',p['files'])

    def test_strong_G3_is_required_before_ROOT4(self):
        small={'conditional_targets':{'n2':'2*sqrt(2)/7','n3':'59*sqrt(3)/250'}}
        physical={'required_predecessor':'C3<=59*sqrt(3)/250','bound':'4097/10000'}
        d=evidence.foundations(small,physical)
        self.assertEqual([r['id']for r in d['proof_nodes']],['G2','G3','G4','Q5'])
        self.assertFalse(d['all_law_C4_verified']);self.assertFalse(d['full_n5_verified'])
        bad=deepcopy(small);bad['conditional_targets']['n3']='CE'
        with self.assertRaises(ValueError):evidence.foundations(bad,physical)
        self.assertGreater(len(d['universal_analytic_premises']),4)

    def test_precise_paired_timing_positions_and_no_boolean_math(self):
        reference={'answer':'1/2','history':[{'result':{'v':'3'},'seconds':1.2}],'initial_seconds':2.0}
        changed=deepcopy(reference);changed['history'][0]['seconds']=6.0
        self.assertTrue(sem.same_resource_answer(changed,reference))
        for change in (lambda z:z['history'][0]['result'].update(seconds=0),
                       lambda z:z['history'][0].update(seconds=True),
                       lambda z:z.update(answer='0'),lambda z:z.update(extra=1)):
            bad=deepcopy(changed);change(bad);self.assertFalse(sem.same_resource_answer(bad,reference))
        self.assertFalse(ev.same({'n':True},{'n':1}))

    def test_partial35_and_unknown_upstream_never_complete(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'work')as td:
            root=Path(td);atomic_json(root/'SESSION_RESULT.json',{'schema':'CONDITIONAL_N5_REMAINING_BATCH_V1','jobs':[]})
            with self.assertRaises(ValueError):upstream.validate35(root)
        with self.assertRaises(ValueError):evidence.import_validator('99')

    def test_final_selected35_ledgers_ignore_preserved_rejected_cache_attempts(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'work')as td:
            root=Path(td);rows=[];declared=[];values={};called=[]
            for i in range(326):
                job='fixture.'+str(i);task=root/'jobs'/job;task.mkdir(parents=True)
                atomic_json(task/'JOB_SOURCE.json',{'job_id':job});atomic_json(task/'STAGE_COMPLETED.json',{'fixture_job':job})
                pin=src.digest(task/'STAGE_COMPLETED.json');checked=dict(job_id=job,stage_result_sha256=pin)
                declared.append(dict(job_id=job,validated=checked));values[job]=checked
                row=dict(job_id=job,kind='count'if i==0 else'initial',census={'leaves':75178}if i==0 else{})
                rows.append(row)
            rejected=root/'jobs/aaa-rejected-same-ledger';rejected.mkdir()
            (rejected/'STAGE_COMPLETED.json').write_bytes((root/'jobs/fixture.0/STAGE_COMPLETED.json').read_bytes())
            atomic_json(rejected/'JOB_SOURCE.json',{'job_id':'fixture.0'})
            unselected=root/'jobs/zzz-rejected-different-ledger';unselected.mkdir()
            atomic_json(unselected/'STAGE_COMPLETED.json',{'old_rejected_cache':True})
            atomic_json(root/'SESSION_RESULT.json',dict(schema='CONDITIONAL_N5_REMAINING_BATCH_V1',jobs=declared))
            def validate(task):
                called.append(task.name)
                if task.name.startswith('aaa-'):raise ValueError('synthetic source/capture corruption')
                return values[src.read(task/'JOB_SOURCE.json')['job_id']]
            with mock.patch.object(upstream.old.src,'jobs',return_value=rows),\
                 mock.patch.object(upstream.old.src,'job',side_effect=lambda job:next(r for r in rows if r['job_id']==job)),\
                 mock.patch.object(upstream.old,'validate_completed',side_effect=validate):
                checked=upstream.validate35(root)
            self.assertEqual(len(checked),326);self.assertEqual(checked['fixture.0']['task'],root/'jobs/fixture.0')
            self.assertIn('aaa-rejected-same-ledger',called);self.assertNotIn('zzz-rejected-different-ledger',called)

class Capture(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'work');self.task=Path(self.temp.name)
        self.origin='/content/berry-esseen-runs/n5-full-join/example/groups/g'
        (self.task/'capsule/work/control').mkdir(parents=True);self.execution=self.task/'executions/a';self.execution.mkdir(parents=True)
        self.action=dict(id='a',cwd='work/control',argv=['-B','check.py'],outputs=['work/control/CHECKED.json'],
            expected_outputs={'work/control/CHECKED.json':{'status':'PASS_FIXTURE','n':5,'controls':['a','b'],'files_sha256':{}}},capture_label=None)
        atomic_json(self.task/'REQUEST.json',{'original_task_root':self.origin})
        atomic_json(self.task/'capsule/work/control/CHECKED.json',self.action['expected_outputs']['work/control/CHECKED.json'])
        (self.execution/'stdout.txt').write_text('synthetic complete fixture\n',encoding='utf-8');(self.execution/'stderr.txt').write_bytes(b'')
        launch=dict(argv=['/usr/bin/python3','-B','check.py'],mode='untrusted_search',cwd=self.origin+'/capsule/work/control',
            output_dir=self.origin+'/executions/a',cpu_seconds=82800,wall_seconds=82800.0,memory_bytes=2*1024**3,
            disk_bytes=512*src.MIB,log_bytes=16*src.MIB,heartbeat_seconds=20.0,sample_seconds=.2,checkpoint_paths=[])
        atomic_json(self.execution/'launch.json',launch)
        self.observed=dict(status='completed',reason=None,returncode=0,mode='untrusted_search',proof_accepted=False,
            elapsed_seconds=1.25,sample_count=2,checkpoints=[],guard_scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,
            external_wall_seconds=82800.0,per_process_RLIMIT_CPU_seconds=82800,per_process_RLIMIT_AS_bytes=2*1024**3,
            aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=2*1024**3,
            sampled_group_CPU_limit_seconds=82800,sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,
            descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False))
        for stream in('stdout','stderr'):
            self.observed[stream+'_path']=self.origin+'/executions/a/'+stream+'.txt'
            self.observed[stream+'_sha256']=src.digest(self.execution/(stream+'.txt'))
        atomic_json(self.execution/'supervisor-result.json',self.observed)
        progress=dict(event='linux_supervisor_finished',stage='untrusted_search',status='completed',reason=None,elapsed_seconds=1.25,proof_accepted=False)
        atomic_json(self.execution/'progress.json',progress);(self.execution/'progress.jsonl').write_text(json.dumps(progress)+'\n',encoding='utf-8')
        self.record=dict(action_id='a',python='/usr/bin/python3',observed=self.observed)
    def tearDown(self):self.temp.cleanup()
    def test_float_budget_ABI_and_strict_full_output(self):
        self.assertEqual(ev.capture(self.task,self.action,self.record)[0]['status'],'PASS_FIXTURE')
        output=self.task/'capsule/work/control/CHECKED.json';bad=src.read(output);bad['n']=True;atomic_json(output,bad)
        with self.assertRaises(ValueError):ev.capture(self.task,self.action,self.record)
    def test_boolean_exit_wrong_cwd_and_changed_stream_rejected(self):
        bad=deepcopy(self.record);bad['observed']['returncode']=True;atomic_json(self.execution/'supervisor-result.json',bad['observed'])
        with self.assertRaises(ValueError):ev.capture(self.task,self.action,bad)
        atomic_json(self.execution/'supervisor-result.json',self.observed)
        launch=src.read(self.execution/'launch.json');launch['cwd']='/tmp/unrelated';atomic_json(self.execution/'launch.json',launch)
        with self.assertRaises(ValueError):ev.capture(self.task,self.action,self.record)
        launch['cwd']=self.origin+'/capsule/work/control';atomic_json(self.execution/'launch.json',launch)
        (self.execution/'stdout.txt').write_bytes(b'changed')
        with self.assertRaises(ValueError):ev.capture(self.task,self.action,self.record)
    def test_final_progress_tuple_and_checkpoint_namespace_required(self):
        progress=src.read(self.execution/'progress.json');progress['elapsed_seconds']=0;atomic_json(self.execution/'progress.json',progress)
        with self.assertRaises(ValueError):ev.capture(self.task,self.action,self.record)
    def test_missing_original_graph_or_unknown_graph_field_is_rejected(self):
        output=self.task/'capsule/work/control/CHECKED.json';original=src.read(output)
        bad=deepcopy(original);bad.pop('files_sha256');atomic_json(output,bad)
        with self.assertRaises(ValueError):ev.output(self.action,self.task)
        bad=deepcopy(original);bad['unexpected_timing_field']=0;atomic_json(output,bad)
        with self.assertRaises(ValueError):ev.output(self.action,self.task)
    def test_source_plan_and_partial_control_list_fail_closed(self):
        with mock.patch.object(src,'verify',return_value=({},dict(id='g',action_ids=['a','b']))):
            packet=dict(schema=ev.OBSERVED,group_id='g',implementation=ev.implementation(),actions=[self.record],conditional_arithmetic_completed=False,
                **{k:False for k in ev.FLAGS})
            with self.assertRaises(ValueError):ev.validate_observed(self.task,packet)

    def test_completed_cache_roundtrip_relocates_without_native_execution(self):
        from be_replay import n5_full_join as runner
        group=dict(id='g',action_ids=['a']);request={'original_task_root':self.origin}
        with mock.patch.object(src,'verify',return_value=(request,group)),mock.patch.object(src,'actions',return_value=[self.action]):
            observed=dict(schema=ev.OBSERVED,group_id='g',implementation=ev.implementation(),actions=[self.record],
                conditional_arithmetic_completed=False,**{k:False for k in ev.FLAGS})
            atomic_json(self.task/'OBSERVED.json',observed)
            summary=ev.validate_observed(self.task,observed)
            completed=dict(schema=ev.SCHEMA,implementation=ev.implementation(),observed_sha256=src.digest(self.task/'OBSERVED.json'),
                summary=summary,artifacts=ev.inventory(self.task),conditional_arithmetic_completed=True,**{k:False for k in ev.FLAGS})
            atomic_json(self.task/'COMPLETED.json',completed)
            # Keep the source tree separate from its cache and restored destinations.
            with tempfile.TemporaryDirectory(dir=ROOT/'work')as td:
                root=Path(td);cache=root/'cache';archive=runner.save_completed(self.task,cache)
                (root/'PROGRESS.jsonl').write_bytes(b'')
                with mock.patch.object(runner,'execute',side_effect=AssertionError('Original mathematics must not run')):
                    found=runner.restore_completed('g',cache,root/'restored',root=root)
                self.assertIsNotNone(found);self.assertEqual(found[1]['completed_sha256'],src.digest(self.task/'COMPLETED.json'))
                packet=Path(archive['path']);packet.with_suffix('.zip.sha256').write_text('0'*64+'  '+packet.name+'\n',encoding='ascii')
                self.assertIsNone(runner.restore_completed('g',cache,root/'bad',root=root))

class Packaging(unittest.TestCase):
    def test_unsafe_completed_zip_rejected_before_extraction(self):
        from be_replay.n5_full_join import cache_members
        with tempfile.TemporaryDirectory(dir=ROOT/'work')as td:
            path=Path(td)/'bad.zip'
            with zipfile.ZipFile(path,'w')as z:z.writestr('../escape','x')
            with zipfile.ZipFile(path)as z:
                with self.assertRaises(ValueError):cache_members(z)
    def test_local_notebook_entire67_scope_and_exact_final_shutdown(self):
        spec=importlib.util.spec_from_file_location('full67gen',ROOT/'tools/make_n5_full_join_notebook.py')
        generator=importlib.util.module_from_spec(spec);spec.loader.exec_module(generator)
        notebook=generator.build_local('actual-local-runtime.zip','a'*64)
        text='\n'.join(''.join(c['source'])for c in notebook['cells'])
        self.assertIn('from be_replay.n5_full_join import run_colab',text)
        self.assertIn("SOURCE_SHA256 = '"+'a'*64+"'",text)
        self.assertEqual(notebook['cells'][-1]['id'],'shutdown-runtime')
        self.assertIn('23hours',text);self.assertNotIn('git clone',text)
        for c in notebook['cells']:
            if c['cell_type']=='code':self.assertEqual(c['outputs'],[]);compile(''.join(c['source']),'67','exec')
        with self.assertRaises(ValueError):generator.build_local('runtime.zip','bad')

if __name__=='__main__':unittest.main()
