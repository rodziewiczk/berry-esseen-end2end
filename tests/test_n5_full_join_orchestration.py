"""Synthetic complete/partial/cached67 orchestration, with native-call traps."""
from contextlib import ExitStack
from copy import deepcopy
import json,tempfile,unittest
from pathlib import Path
from unittest import mock
from be_replay import n5_full_join as runner,n5_full_join_sources as src,n5_full_join_control_evidence as ev
from be_replay import n5_full_join_evidence as semantic
from be_replay.colab_batch import atomic_json

ROOT=Path(__file__).resolve().parents[1]

class Orchestration(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'work');self.root=Path(self.temp.name)
        self.cache=self.root/'source-cache';(self.cache/'work/control').mkdir(parents=True)
        (self.cache/'work/control/check.py').write_text('raise AssertionError("fixture source must never execute")\n',encoding='utf-8')
        (self.cache/'work/control/input.json').write_text('{"fixture":true}\n',encoding='utf-8')
        self.rootlog=self.root/'logs';self.rootlog.mkdir()
        self.rows=[];outputs=[]
        for i,label in enumerate(('support_tighter_construct01','support_tighter_replay01')):
            name='work/control/RESULT'+str(i)+'.json'
            result=dict(status='SYNTHETIC_FULL_ACTION',n=5,index=i,controls=['one','two'],files_sha256={})
            self.rows.append(dict(id='fixture.'+str(i),argv=['-B','check.py',str(i)],cwd='work/control',outputs=[name],
                expected_outputs={name:result},capture_label=label,scope='SYNTHETIC_FIXTURE_ONLY'))
            (self.cache/name).write_text(json.dumps(result)+'\n',encoding='utf-8')
            outputs.append(name);outputs.extend('runs/cutoff5_20261020/high/'+label+'/'+stream for stream in('metadata.json','stdout.txt','stderr.txt'))
        group=dict(id='fixture.group',action_ids=[r['id']for r in self.rows],inputs=['work/control/check.py','work/control/input.json'],outputs=outputs)
        files={p.relative_to(self.cache).as_posix():dict(bytes=p.stat().st_size,sha256=src.digest(p))for p in self.cache.rglob('*')if p.is_file()}
        self.plan=dict(groups=[group],actions=self.rows,files=files);self.calls=[];self.fail_second=False
    def tearDown(self):self.temp.cleanup()
    def fake_run(self,argv,**kw):
        i=int(argv[-1]);self.calls.append(i)
        if i==1:
            self.assertTrue((Path(kw['cwd'])/'RESULT0.json').is_file())
            if self.fail_second:raise TimeoutError('synthetic interrupted second action')
        action=self.rows[i];directory=Path(kw['cwd']);execution=Path(kw['output_dir']);execution.mkdir(parents=True)
        output=directory/('RESULT'+str(i)+'.json');self.assertFalse(output.exists())
        atomic_json(output,action['expected_outputs'][action['outputs'][0]])
        (execution/'stdout.txt').write_text('synthetic original stdout '+str(i)+'\n',encoding='utf-8');(execution/'stderr.txt').write_bytes(b'')
        launch=dict(argv=argv,cwd=str(directory),output_dir=str(execution),cpu_seconds=kw['cpu_seconds'],wall_seconds=float(kw['wall_seconds']),
            memory_bytes=kw['memory_bytes'],disk_bytes=kw['disk_bytes'],log_bytes=kw['log_bytes'],heartbeat_seconds=float(kw['heartbeat_seconds']),
            mode=kw['mode'],sample_seconds=.2,checkpoint_paths=[])
        atomic_json(execution/'launch.json',launch)
        guard=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(kw['wall_seconds']),
            per_process_RLIMIT_AS_bytes=kw['memory_bytes'],per_process_RLIMIT_CPU_seconds=kw['cpu_seconds'],
            aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=kw['memory_bytes'],
            sampled_group_CPU_limit_seconds=kw['cpu_seconds'],sampled_file_limit_bytes=kw['disk_bytes'],sampled_log_limit_bytes=kw['log_bytes'],
            descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
        observed=dict(status='completed',reason=None,mode=kw['mode'],returncode=0,elapsed_seconds=.5+i,
            stdout_path=str(execution/'stdout.txt'),stderr_path=str(execution/'stderr.txt'),
            stdout_sha256=src.digest(execution/'stdout.txt'),stderr_sha256=src.digest(execution/'stderr.txt'),
            guard_scope=guard,sample_count=3,maximum_sampled_group_RSS_bytes=1,maximum_sampled_group_CPU_seconds=.1,
            checkpoints=[],proof_accepted=False)
        atomic_json(execution/'supervisor-result.json',observed)
        progress=dict(event='linux_supervisor_finished',stage=kw['mode'],status='completed',reason=None,elapsed_seconds=.5+i,proof_accepted=False)
        atomic_json(execution/'progress.json',progress);(execution/'progress.jsonl').write_text(json.dumps(progress)+'\n',encoding='utf-8')
        return observed
    def patches(self):
        stack=ExitStack();stack.enter_context(mock.patch.object(src,'plan',return_value=self.plan))
        stack.enter_context(mock.patch.object(runner.sys,'platform','linux'))
        stack.enter_context(mock.patch.object(runner.linux_supervisor,'run',side_effect=self.fake_run))
        return stack
    def test_full_multi_action_capture_dependency_and_cache_reuse(self):
        with self.patches():
            task=self.root/'complete';checked=runner.execute('fixture.group',self.cache,task,root=self.rootlog)
            self.assertEqual(self.calls,[0,1]);self.assertTrue(checked['conditional_arithmetic_completed'])
            report=src.read(task/'OBSERVED.json');self.assertFalse(report['conditional_arithmetic_completed'])
            self.assertEqual(len(report['actions']),2)
            second=src.read(task/'capsule/runs/cutoff5_20261020/high/support_tighter_replay01/metadata.json')
            self.assertEqual(second['input_sha256']['RESULT0.json'],src.digest(task/'capsule/work/control/RESULT0.json'))
            saved=runner.save_completed(task,self.root/'completed-cache');self.assertTrue(Path(saved['path']).is_file())
            with mock.patch.object(runner.linux_supervisor,'run',side_effect=AssertionError('completed reuse must never execute')):
                restored=runner.restore_completed('fixture.group',self.root/'completed-cache',self.root/'restored',root=self.rootlog)
            self.assertIsNotNone(restored);self.assertEqual(restored[1]['completed_sha256'],checked['completed_sha256'])
            for key in ev.FLAGS:self.assertFalse(restored[1][key])
    def test_incomplete_second_action_never_creates_complete_group(self):
        self.fail_second=True
        with self.patches():
            task=self.root/'partial'
            with self.assertRaises(TimeoutError):runner.execute('fixture.group',self.cache,task,root=self.rootlog)
            self.assertFalse((task/'COMPLETED.json').exists());self.assertTrue((task/'capsule/work/control/RESULT0.json').is_file())
            self.assertEqual(len(src.read(task/'OBSERVED.json')['actions']),1)
            with self.assertRaises((ValueError,FileNotFoundError)):runner.save_completed(task,self.root/'invalid-cache')
    def run_session(self,*,missing=None,semantic_failure=False):
        def import_inputs(root,durable,status):return missing or []
        with self.patches(),mock.patch.object(src,'obtain_archive',return_value=self.root/'unused.zip'),\
             mock.patch.object(src,'prepare_cache',return_value=self.cache),\
             mock.patch.object(semantic,'import_completed_inputs',side_effect=import_inputs),\
             mock.patch.object(semantic,'validate_batch',return_value={'fixture':'complete semantic readback'})as batch,\
             mock.patch.object(semantic,'validate_completed',side_effect=ValueError('synthetic semantic rejection')if semantic_failure else None)as completed:
            result=runner.run_colab(durable_root=self.root/'drive',work_root=self.root/'runs',archives=self.root/'archives')
            return result,batch.call_args_list,completed.call_count
    def test_waiting_for_upstream_keeps_complete_cache_and_final_zip(self):
        result,semantic_calls,completed_calls=self.run_session(missing=[{'notebook':'35','reason':'incomplete'}])
        self.assertEqual(result['status']['state'],'waiting_for_complete_prerequisite_exports')
        self.assertFalse(result['status']['conditional_finite_chain_verified']);self.assertEqual(len(semantic_calls),0)
        self.assertEqual(completed_calls,0);self.assertTrue(Path(result['bundle']).is_file())
        self.assertEqual(len(list((self.root/'drive/n5-full-join/completed').rglob('*-complete.zip'))),1)
    def test_semantic_readback_rejection_cannot_leave_success_flag(self):
        result,calls,completed=self.run_session(semantic_failure=True)
        self.assertEqual(len(calls),1);self.assertTrue(calls[0].kwargs['prepare']);self.assertEqual(completed,1)
        self.assertEqual(result['status']['state'],'incomplete');self.assertFalse(result['status']['conditional_finite_chain_verified'])
        self.assertTrue(Path(result['bundle']).is_file());self.assertIn('semantic rejection',result['status']['error'])
    def test_conditional_completion_requires_readback_and_keeps_universal_flags_false(self):
        result,calls,completed=self.run_session()
        self.assertEqual(len(calls),1);self.assertTrue(calls[0].kwargs['prepare']);self.assertEqual(completed,1)
        self.assertEqual(result['status']['state'],semantic.COMPLETE);self.assertTrue(result['status']['conditional_finite_chain_verified'])
        self.assertGreater(len(result['status']['unacquired_universal_analytic_premises']),4)
        self.assertTrue(Path(result['bundle']).is_file())
        for key in ev.FLAGS:self.assertFalse(result['status'][key])
    def test_handled_original_failure_still_exports_false_final_bundle(self):
        self.fail_second=True;result,calls,completed=self.run_session()
        self.assertEqual(result['status']['state'],'incomplete');self.assertEqual(result['status']['groups'],[])
        self.assertEqual(len(calls),0);self.assertEqual(completed,0);self.assertTrue(Path(result['bundle']).is_file())
        for key in ev.FLAGS:self.assertFalse(result['status'][key])

if __name__=='__main__':unittest.main()
