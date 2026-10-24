"""Synthetic support pipeline fixtures. Original mathematical files are traps."""
from __future__ import annotations
import copy,io,json,shutil,stat,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import Mock,patch
from be_replay import finite2124_high_sources as s,finite2124_high_evidence as e,finite2124_high as r

def put(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(s.dump(value));return s.digest(path)

class Pipeline(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=s.ROOT.parent,prefix='t58a-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.cache=self.root/'inputs';self.spec=copy.deepcopy(s.plan())
        for name,row in self.spec['source_files'].items():
            p=self.cache/name;p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(b'raise AssertionError("Original math must never run in local fixtures")\n'if name.endswith('.py')else b'{}\n')
            row['bytes']=p.stat().st_size;row['sha256']=s.digest(p)
        for target,name,value in((s,'plan',lambda:self.spec),(r.sys,'platform','linux'),(r.sys,'stdout',io.StringIO())):
            q=patch.object(target,name,value);q.start();self.addCleanup(q.stop)

    def fake(self,argv,*,cwd,output_dir,**kwargs):
        c=Path(cwd);task=c.parents[3];directory=Path(output_dir);action=argv[-2]
        # The following fabricated row payloads deliberately do not prove support.
        common=dict(actual_n=[21,22,23,24],excluded_rho=['9/8','infinity'],remaining_rho=['1','9/8'],
            remaining_upper_endpoint_open=True,source_freeze_sha256=s.digest(c/'FROZEN_SOURCES.json'),
            global_predecessors_verified=False,historical_fourier_replayed=False,sharp20_proved=False,cutoff20_proved=False)
        if action=='construct':
            result=common|dict(status=e.CONSTRUCT,strict_fourier_target='4097/10000',
                rows=[dict(request=dict(n=n,K='0',q='0',rho_upper='6/5',radius='3',sign=0,mesh=10),
                    proof=dict(n=n,K='0',q_contact='0',rho_upper='6/5',radius='3',support_sign=0,
                               ray_rows=[dict(sign=-1),dict(sign=1)]))for n in(21,22,23,24)],
                universal_readback_sha256=s.digest(task/'capsule/cutoff20_20261016/analytic/fourier_cover_review_v1/READBACK.json'),
                supported_readback_sha256=s.digest(task/'capsule/cutoff20_20261016/analytic/supported1125_review_v1/READBACK.json'))
        else:
            result=common|dict(status=e.ACCEPT,candidate_sha256=s.digest(c/'CANDIDATE.json'),
                source_review_sha256=s.digest(task/'capsule'/s.REVIEW),fresh_support_calls=4,
                negative_controls=e.CONTROL_NAMES,elapsed_seconds=.1)
        if hasattr(self,'result_mutator'):self.result_mutator(action,result)
        output=c/s.OUTPUTS[action];put(output,result);directory.mkdir(parents=True)
        (directory/'stdout.txt').write_bytes((result['status']+' '+s.digest(output)+'\n').encode())
        (directory/'stderr.txt').write_bytes(b'')
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,**kwargs)
        launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds'])
        launch['checkpoint_paths']=[str(p)for p in kwargs['checkpoint_paths']]
        if hasattr(self,'launch_mutator'):self.launch_mutator(launch)
        put(directory/'launch.json',launch);stopped=directory/'checkpoints'/output.name
        stopped.parent.mkdir();shutil.copyfile(output,stopped)
        observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,
            sample_count=1,elapsed_seconds=.1,maximum_sampled_group_CPU_seconds=.1,maximum_sampled_group_RSS_bytes=1024,
            guard_scope=e.guard(),checkpoints=[dict(source_path=str(output),exists=True,trusted_certificate=False,
                path=str(stopped),bytes=output.stat().st_size,sha256=s.digest(output))],
            **{kind+suffix:value for kind in('stdout','stderr')for suffix,value in
               (('_path',str(directory/(kind+'.txt'))),('_sha256',s.digest(directory/(kind+'.txt'))))})
        if hasattr(self,'observed_mutator'):self.observed_mutator(observed)
        put(directory/'supervisor-result.json',observed)
        final=dict(event='linux_supervisor_finished',stage='untrusted_search',status=observed['status'],
            reason=observed['reason'],elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
        put(directory/'progress.json',final);(directory/'progress.jsonl').write_bytes(json.dumps(final).encode()+b'\n')
        return observed

    def complete(self,name='task'):
        task=self.root/name
        with patch.object(r.linux_supervisor,'run',side_effect=self.fake)as child,patch.object(r,'Follow'):
            result=r.execute(task,self.cache,root=self.root)
        self.assertEqual(child.call_count,2);return task,result

    def test_two_full_original_commands_and_false_global_flags(self):
        task,result=self.complete();self.assertTrue(result['conditional_support_arithmetic_completed'])
        self.assertEqual(result['summary']['actual_n'],[21,22,23,24])
        self.assertEqual(result['summary']['negative_controls'],10)
        for flag in e.FLAGS:self.assertIs(result[flag],False)
        request=s.read(task/'SOURCES.json');observed=s.read(task/'STAGE_OBSERVED.json')
        for action in s.ACTIONS:
            self.assertEqual(s.read(task/'executions'/action/'launch.json')['argv'],
                             e.command(request,action,observed['python_executable']))

    def test_complete_cache_relocation_and_no_native_repeat(self):
        task,checked=self.complete();export=r.save_completed(task,self.root/'completed')
        with patch.object(r.linux_supervisor,'run',side_effect=AssertionError('No replay'))as child:
            loaded=r.restore_completed(self.root/'completed',self.root/'restore',root=self.root)
        self.assertEqual(loaded[1],checked);child.assert_not_called()
        self.assertEqual({p.relative_to(task).as_posix():p.read_bytes()for p in task.rglob('*')if p.is_file()},
                         {p.relative_to(loaded[0]).as_posix():p.read_bytes()for p in loaded[0].rglob('*')if p.is_file()})
        Path(export['path']).with_suffix('.zip.sha256').write_bytes(b'bad')
        self.assertIsNone(r.restore_completed(self.root/'completed',self.root/'bad-restore',root=self.root))

    def test_coherent_bad_index_missing_ray_controls_or_promoted_claim_rejected(self):
        changes=[lambda a,p:p.update(global_predecessors_verified=True),
                 lambda a,p:p.update(actual_n=[20,21,22,23]),
                 lambda a,p:p['rows'][0]['proof']['ray_rows'].pop()if a=='construct'else None,
                 lambda a,p:p['rows'][0]['proof']['ray_rows'][1].update(sign=True)if a=='construct'else None,
                 lambda a,p:p.update(negative_controls=[])if a=='accept'else None,
                 lambda a,p:p.update(fresh_support_calls=True)if a=='accept'else None]
        for i,change in enumerate(changes):
            self.result_mutator=change
            with self.assertRaises((ValueError,KeyError)):self.complete('bad'+str(i))
            self.assertFalse((self.root/('bad'+str(i))/'STAGE_COMPLETED.json').exists())

    def test_failed_bool_exit_or_wrong_guard_rejected(self):
        for i,change in enumerate((lambda p:p.update(returncode=False),lambda p:p.update(status='incomplete'),
                                  lambda p:p.update(checkpoints=[]),lambda p:p.update(proof_accepted=True))):
            self.observed_mutator=change
            with self.assertRaises(ValueError):self.complete('guard'+str(i))

    def test_wrong_command_cwd_or_limits_rejected(self):
        for i,change in enumerate((lambda p:p['argv'].append('--quick'),lambda p:p.update(cwd=str(self.root)),
                                  lambda p:p.update(cpu_seconds=True),lambda p:p.update(memory_bytes=1024))):
            self.launch_mutator=change
            with self.assertRaises(ValueError):self.complete('launch'+str(i))

    def test_stopped_copy_stream_source_or_complete_inventory_mutation_rejected(self):
        for i,path in enumerate(('executions/accept/checkpoints/ACCEPTED.json','executions/construct/stdout.txt',
                                 'capsule/'+s.NATIVE+'/check.py','unexpected.txt')):
            task,_=self.complete('changed'+str(i));p=task/path;p.write_bytes(b'changed')
            with self.assertRaises(ValueError):e.validate_completed(task)

    def test_unsafe_incomplete_or_alias_archive_rejected(self):
        z=Mock()
        for name in('../outside','/absolute','a//b','C:/outside','SOURCES.json'):
            info=zipfile.ZipInfo();info.filename=info.orig_filename=name;z.infolist.return_value=[info]
            with self.assertRaises(ValueError):r.cache_members(z)
        info=zipfile.ZipInfo('link');info.external_attr=(stat.S_IFLNK|0o777)<<16;z.infolist.return_value=[info]
        with self.assertRaises(ValueError):r.cache_members(z)

    def test_failed_sources_export_false_session(self):
        with patch.object(s,'obtain_assets',side_effect=ValueError('Synthetic unavailable source')):
            out=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'work')
        self.assertFalse(out['status']['conditional_support_arithmetic_completed'])
        self.assertTrue(Path(out['bundle']).is_file())

class SourcePlan(unittest.TestCase):
    def test_exact_original_domain_and_sources(self):
        plan=s.plan();self.assertEqual(len(plan['source_files']),40)
        self.assertEqual(plan['actual_n'],[21,22,23,24]);self.assertEqual(plan['excluded_rho'],['9/8','infinity'])
        self.assertFalse(plan['historical_fourier_replayed']);self.assertFalse(plan['all_index_conclusion_verified'])

if __name__=='__main__':unittest.main()
