"""56F fake supervisor/source fixtures only; original mathematical modules are traps."""
from fractions import Fraction as F
from pathlib import Path
import io
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch,Mock
import zipfile
from be_replay import finite1014_coarse_sources as s,finite1014_coarse_evidence as e,finite1014_coarse as r

def put(p,value):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.dump(value));return s.digest(p)


class Coarse(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=s.ROOT.parent,prefix='t56f-');self.root=Path(self.temp.name)
        self.assertTrue(self.root.resolve().is_relative_to(s.ROOT.parent.resolve()));self.addCleanup(self.temp.cleanup)
        self.cache=self.root/'input';self.native=self.cache/s.NATIVE;self.native.mkdir(parents=True)
        for n in('construct.py','replay.py','direct_gaussian_support.py'):
            (self.native/n).write_bytes(b'raise AssertionError("Never import or execute original mathematics locally")\n')
        (self.native/'PROOF.txt').write_bytes(b'SYNTHETIC CONDITIONAL PREMISES\n')
        put(self.native/'COPIES.json',{'synthetic':True})
        self.bands=[dict(name='global',rho_interval=['1','7/5'],predecessor_cap='423/1000',beta_upper='95741889960107/200000000000000'),
                    dict(name='localized',rho_interval=['7/5','71/50'],predecessor_cap='209/500',beta_upper='244365230009117/500000000000000')]
        files={p.relative_to(self.cache).as_posix():dict(bytes=p.stat().st_size,sha256=s.digest(p))for p in self.cache.rglob('*')if p.is_file()}
        self.plan=dict(source_files=files,original_source_graph_rows=len(files),bands=self.bands,conditional_premises=['Synthetic unacquired premises'])
        for target,name,value in((s,'plan',self.plan),(r.sys,'platform','linux')):
            p=patch.object(target,name,return_value=value)if name=='plan'else patch.object(target,name,value)
            p.start();self.addCleanup(p.stop)
        p=patch.object(r.sys,'stdout',io.StringIO());p.start();self.addCleanup(p.stop)

    def fake(self,argv, *,cwd,output_dir,**kw):
        d=Path(output_dir);action=d.name;task=d.parent.parent;c=task/'capsule';request=s.read(task/'SOURCES.json')
        if action=='construct':
            rows=[]
            for n in range(10,15):
                for b in self.bands:
                    q=str(n*(F(b['predecessor_cap'])-F(4097,10000)));beta=F(b['beta_upper'])
                    proof=dict(n=n,K='0',radius='3',support_sign=0,q_contact=q,rho_upper=b['rho_interval'][1],
                               beta_interval=[str(-beta),str(beta)],ray_rows=[dict(sign=-1),dict(sign=1)])
                    rows.append(dict(n=n,band=b['name'],rho_interval=b['rho_interval'],predecessor_cap=b['predecessor_cap'],q=q,beta_upper=b['beta_upper'],proof=proof))
            packet=dict(status=e.NATIVE_STATUS,n=list(range(10,15)),radius='3',rho_interval=['1','71/50'],rows=rows,
                predecessor_caps_verified=False,owncap_proved=False,physical_defect_seed_imported=False,cutoff_proved=False,files_sha256=request['sources'])
            if hasattr(self,'native_mutator'):self.native_mutator(packet)
        else:
            capture=c/s.RUNS/s.LABELS['construct'];meta=s.read(capture/'metadata.json')
            self.assertEqual(meta['command'][1:],['-B','construct.py'])
            self.assertEqual(meta['cwd'],str(cwd));self.assertEqual(meta['input_sha256'],s.native_input_map(request))
            self.assertEqual(meta['capture_bridge']['outer_launch_sha256'],s.digest(task/'executions/construct/launch.json'))
            graph=dict(request['sources']);graph[s.NATIVE+'/RESULT.json']=s.digest(c/s.NATIVE/'RESULT.json')
            for name in s.capture_paths('construct'):graph[name]=s.digest(c/name)
            packet=dict(status=e.REPLAY_STATUS,n=list(range(10,15)),rho_interval=['1','71/50'],radius='3',complete_index_band_rows=10,
                both_support_rays=True,full_threshold_line_and_tails=True,candidate_sha256=s.digest(c/s.NATIVE/'RESULT.json'),
                malformed_controls=20,parser_controls=2,predecessor_caps_verified=False,cutoff_proved=False,files_sha256=graph,
                execution_scope='SYNTHETIC FRESH COMPLETE REPLAY')
            if hasattr(self,'replay_mutator'):self.replay_mutator(packet)
        output=c/s.NATIVE/s.OUTPUT_NAMES[action];put(output,packet)
        stdout=packet['status']+' '+s.digest(output)+'\n'
        if hasattr(self,'stdout_mutator'):stdout=self.stdout_mutator(stdout,action)
        d.mkdir(parents=True);(d/'stdout.txt').write_bytes(stdout.encode());(d/'stderr.txt').write_bytes(b'')
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(d),sample_seconds=.2,**kw)
        launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds'])
        launch['checkpoint_paths']=[str(p)for p in launch['checkpoint_paths']];put(d/'launch.json',launch)
        checkpoints=r.linux_supervisor._capture_checkpoints(launch)
        scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(e.WALL_SECONDS),
            per_process_RLIMIT_AS_bytes=e.MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=e.CPU_SECONDS,aggregate_kernel_memory_limit=False,
            aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=e.MEMORY_BYTES,sampled_group_CPU_limit_seconds=e.CPU_SECONDS,
            sampled_file_limit_bytes=512*s.MIB,sampled_log_limit_bytes=16*s.MIB,descendants_changing_session_are_contained=False,
            equivalent_to_Windows_Job_or_cgroup=False)
        observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,
            elapsed_seconds=.1,maximum_sampled_group_RSS_bytes=10*s.MIB,maximum_sampled_group_CPU_seconds=.1,
            guard_scope=scope,checkpoints=checkpoints,**{k+suffix:v for k in('stdout','stderr')for suffix,v in(
                ('_path',str(d/(k+'.txt'))),('_sha256',s.digest(d/(k+'.txt'))))})
        put(d/'supervisor-result.json',observed);return observed

    def complete(self,name='task',effect=None):
        task=self.root/name
        with patch.object(r.linux_supervisor,'run',side_effect=effect or self.fake),patch.object(r,'Follow'):
            checked=r.execute(task,self.cache,root=self.root)
        return task,checked

    def test_complete_original_commands_two_actions_full_ten_rows_and_false_premises(self):
        task,result=self.complete();self.assertTrue(result['conditional_coarse_support_arithmetic_completed'])
        for flag in e.FLAGS:self.assertIs(result[flag],False)
        self.assertEqual([x['action']for x in s.read(task/'STAGE_OBSERVED.json')['actions']],list(s.ACTIONS))
        self.assertEqual(s.read(task/'executions/construct/launch.json')['argv'][1:],['-B','construct.py'])
        self.assertEqual(s.read(task/'executions/replay/launch.json')['argv'][1:],['-B','replay.py'])
        self.assertEqual(result['summary']['complete_index_band_rows'],10)
        self.assertEqual(result['summary']['malformed_controls'],20);self.assertEqual(result['summary']['parser_controls'],2)

    def test_real_checkpoint_copier_layout_relative_to_original_cwd(self):
        task,_=self.complete()
        for a in s.ACTIONS:
            d=task/'executions'/a;packet=s.read(d/'supervisor-result.json')['checkpoints'][0]
            self.assertEqual(Path(packet['path']),d/'checkpoints'/s.OUTPUT_NAMES[a])
            self.assertTrue(Path(packet['path']).is_file());self.assertFalse((d/'checkpoints/work').exists())

    def test_whole_source_and_capture_graph_bound_without_historical_hash(self):
        task,_=self.complete();c=task/'capsule';candidate=s.read(c/s.NATIVE/'RESULT.json');result=s.read(c/s.RESULT)
        self.assertEqual(candidate['files_sha256'],s.read(task/'SOURCES.json')['sources'])
        self.assertEqual(set(result['files_sha256']),set(candidate['files_sha256'])|{s.NATIVE+'/RESULT.json'}|set(s.capture_paths('construct')))
        self.assertNotEqual(result['candidate_sha256'],'1e62add4add829e95dfa4552aa42f3ef6badb711879d146b983d8ee55b8015ff')

    def test_relocated_completed_cache_preserves_all_recorded_bytes(self):
        task,result=self.complete();moved=self.root/'moved';shutil.copytree(task,moved)
        before={p.relative_to(moved).as_posix():p.read_bytes()for p in moved.rglob('*')if p.is_file()}
        self.assertEqual(e.validate_completed(moved),result)
        self.assertEqual(before,{p.relative_to(moved).as_posix():p.read_bytes()for p in moved.rglob('*')if p.is_file()})

    def test_zero_false_rc_bad_guard_missing_checkpoint_and_changed_actual_stdout(self):
        for i,mutate in enumerate((lambda p:p.update(returncode=False),lambda p:p['guard_scope'].update(aggregate_kernel_memory_limit=True),
                                  lambda p:p.update(checkpoints=[]),lambda p:p.update(stdout_sha256='0'*64))):
            def effect(*a,**k):
                p=self.fake(*a,**k);mutate(p);put(Path(k['output_dir'])/'supervisor-result.json',p);return p
            with self.assertRaises(ValueError):self.complete('bad'+str(i),effect)
            self.assertFalse((self.root/('bad'+str(i))/'STAGE_COMPLETED.json').exists())

    def test_changed_launch_cwd_bridge_or_static_graph_fails_readback(self):
        task,_=self.complete();p=task/'capsule'/s.RUNS/s.LABELS['construct']/'metadata.json';raw=p.read_bytes()
        for change in(lambda x:x.update(cwd=str(task)),lambda x:x['input_sha256'].pop(next(iter(x['input_sha256']))),
                      lambda x:x['capture_bridge'].update(outer_launch_sha256='0'*64),lambda x:x.update(returncode=False)):
            x=json.loads(raw);change(x);put(p,x)
            with self.assertRaises(ValueError):e.validate_completed(task)
        p.write_bytes(raw);launch=task/'executions/replay/launch.json';x=s.read(launch);x['cwd']=str(task);put(launch,x)
        with self.assertRaises(ValueError):e.validate_completed(task)

    def test_literal_bands_indices_n_scaled_allowances_and_signed_rays(self):
        changes=(lambda x:x['rows'][0].update(n=True),lambda x:x['rows'][1].update(q='0'),
                 lambda x:x['rows'][1].update(rho_interval=['7/5','7/5']),lambda x:x['rows'][0]['proof']['ray_rows'].pop(),
                 lambda x:x['rows'][0]['proof'].update(beta_interval=['0','1']),lambda x:x['rows'].pop())
        for i,mutate in enumerate(changes):
            self.native_mutator=mutate
            with self.assertRaises(ValueError):self.complete('scope'+str(i))

    def test_no_zero_rc_terminal_or_historical_native_hash_shortcut(self):
        self.stdout_mutator=lambda line,a:'INCOMPLETE\n'if a=='construct'else line
        with self.assertRaises(ValueError):self.complete('terminal')
        del self.stdout_mutator
        self.replay_mutator=lambda x:x.update(candidate_sha256='1e62add4add829e95dfa4552aa42f3ef6badb711879d146b983d8ee55b8015ff')
        with self.assertRaises(ValueError):self.complete('oldhash')

    def test_replay_full_controls_all_rays_and_no_premise_promotion(self):
        for i,mutate in enumerate((lambda x:x.update(malformed_controls=19),lambda x:x.update(parser_controls=1),
                                   lambda x:x.update(both_support_rays=False),lambda x:x.update(predecessor_caps_verified=True),
                                   lambda x:x.update(status='INCOMPLETE'))):
            self.replay_mutator=mutate
            with self.assertRaises(ValueError):self.complete('replay'+str(i))

    def test_extra_helper_and_changed_static_source_rejected(self):
        task=self.root/'sealed';s.prepare(self.cache,task);p=task/'capsule'/s.NATIVE/'foreign.py';p.write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify_job(task)
        p.unlink();(task/'capsule'/s.NATIVE/'construct.py').write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify_job(task)

    def test_actual_completed_zip_sidecar_reuse_and_bad_partial_zip(self):
        task,result=self.complete();cache=self.root/'saved';saved=r.save_completed(task,cache)
        with patch.object(r.linux_supervisor,'run',side_effect=AssertionError('No original maths'))as native:
            loaded=r.restore_completed(cache,self.root/'restored',root=self.root)
        self.assertEqual(loaded[1],result);native.assert_not_called()
        Path(saved['path']).with_suffix('.zip.sha256').write_bytes(b'bad')
        self.assertIsNone(r.restore_completed(cache,self.root/'badrestore',root=self.root))
        z=Mock()
        for name in('SOURCES.json','../escape','/absolute','a//b','a\\b'):
            info=zipfile.ZipInfo();info.filename=info.orig_filename=name;z.infolist.return_value=[info]
            with self.assertRaises(ValueError):r.cache_members(z)

    def test_failure_exports_false_session(self):
        with patch.object(r,'restore_completed',return_value=None),patch.object(s,'obtain_assets',side_effect=ValueError('Synthetic unavailable')):
            result=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'runs')
        self.assertFalse(result['status']['conditional_coarse_support_arithmetic_completed']);self.assertTrue(Path(result['bundle']).is_file())


class SourcePlan(unittest.TestCase):
    def test_actual81_original_inputs_and_exact_recovered_prose(self):
        d=s.plan();self.assertEqual(len(d['source_files']),81);self.assertEqual(sum(x['bytes']for x in d['source_files'].values()),471452)
        self.assertEqual(d['original_source_graph_rows'],81);self.assertEqual(len(d['assets']),2)
        for a in s.ACTIONS:
            for n in s.generated_paths(a):self.assertNotIn(n,d['source_files'])
        prose={Path(n).name:v['sha256']for n,v in d['source_files'].items()if n.endswith(('foundation.tex','resource_unified.tex'))}
        self.assertEqual(prose,{'foundation.tex':'997b364445ddd31ee1babd24fe809058081eaaef94e8efe6066c82ac60d4baf1'})


if __name__=='__main__':unittest.main()
