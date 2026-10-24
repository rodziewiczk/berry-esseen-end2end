"""58D/E/F fake pipeline and sealed-source fixtures; original math sources are traps."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import io,json,shutil,tempfile,unittest,zipfile
from unittest.mock import patch,Mock
from be_replay import finite2024_fourier_sources as s,finite2024_fourier_evidence as e,finite2024_fourier as r

def put(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.dump(x));return s.digest(p)

class Fourier(unittest.TestCase):
    def setUp(self):
        self.real=s.plan();self.temp=tempfile.TemporaryDirectory(prefix='t58def-',dir=s.ROOT.parent);self.root=Path(self.temp.name);self.addCleanup(self.temp.cleanup)
        self.assertTrue(self.root.resolve().is_relative_to(s.ROOT.parent.resolve()));self.caches={};self.fakeplan=deepcopy(self.real)
        for key in s.FAMILIES:
            cfg=self.fakeplan['families'][key];cache=self.root/'source'/key;self.caches[key]=cache
            for name in [cfg['native']+'/'+v for v in('run.py','planner.py','protocol.py','kernel.py')]+[cfg['audit']+'/readback.py']:
                p=cache/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'raise AssertionError("Never execute or import original math locally")\n')
            (cache/cfg['audit']/'REVIEW.txt').write_bytes(b'SYNTHETIC conditional source premise\n')
            native={p.relative_to(cache).as_posix():s.digest(p)for p in(cache/cfg['native']).glob('*.py')}
            cfg['original_manifest_sha256']=put(cache/cfg['native']/'MANIFEST.json',dict(files_sha256=native,scope='SYNTHETIC'))
            cfg['source_files']={p.relative_to(cache).as_posix():dict(bytes=p.stat().st_size,sha256=s.digest(p))for p in cache.rglob('*')if p.is_file()}
        for p in(patch.object(s,'plan',side_effect=lambda:deepcopy(self.fakeplan)),patch.object(r.sys,'platform','linux'),
                 patch.object(r.sys,'stdout',io.StringIO()),patch.object(r,'numpy_context',return_value=dict(scope='UNTRUSTED_FLOATING_DISCOVERY_ONLY',
                 distribution='numpy',version='synthetic',entry_sha256='a'*64,thread_environment={n:'1'for n in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')},acceptance_arithmetic_depends_on_numpy=False))):
            p.start();self.addCleanup(p.stop)
        self.calls=[]

    def fake(self,argv,*,cwd,output_dir,**kw):
        d=Path(output_dir);action=d.name;task=d.parent.parent;c=task/'capsule';request=s.read(task/'SOURCES.json');key=request['family'];cfg=s.family(key);self.calls.append((key,action))
        planfile=c/cfg['runs']/'plan01/PLAN.json'
        if action=='plan':
            strip=dict(rho=cfg['rho'],c='12/5',tau='1/4',heuristic_upper=.4)
            if key=='universal':strip=dict(rho=cfg['rho'],h_panels=[dict(h=['1/2','1'],c='12/5',tau='1/4',heuristic_upper=.4)])
            value=dict(schema=cfg['plan_schema'],n=cfg['n'],target=cfg['target'],rho=cfg['rho'],strips=[strip])
            if key=='supported':value['support_absolute_upper']='3'
        elif action!='readback':
            upper='41/100'if key=='auxiliary'else'2/5';rows=[]
            for n in cfg['n']:
                row=dict(n=n,target=cfg['target'],strict_target_pass=True,normalized_upper=upper)
                row.update(dict(rho_strip_index=0,h_cell_index=0)if key=='universal'else dict(strip_index=0));rows.append(row)
            attempts=dict(mesh=128,normalized_uppers=[upper]*len(cfg['n']))
            attempts.update(dict(rho_strip_index=0,h_cell_index=0,passed=True)if key=='universal'else dict(strip_index=0,strict_target_pass=True))
            value=dict(status=cfg['native_status'],n=cfg['n'],target=cfg['target'],rows=rows,attempts=[attempts],
                       plan_sha256=s.digest(planfile),manifest_sha256=cfg['original_manifest_sha256'],seconds=.1 if action=='construct'else .2)
            if key=='universal':value.update(scope='SYNTHETIC',rho=cfg['rho'],h_cells=1,rho_strips=1,negative_controls=cfg['native_controls'])
            else:
                value.update(theorem='SYNTHETIC',uniform_upper=upper,uniform_upper_float=float(F(upper)),per_n_upper={str(n):upper for n in cfg['n']},controls=cfg['native_controls'])
                if key=='auxiliary':value.update(finite_rho=cfg['rho'],published_tail=dict(rho_lower='19/10',upper='2/5',source='SYNTHETIC'))
                else:value.update(rho=cfg['rho'],support_absolute_upper='3')
        else:
            native=s.read(c/cfg['runs']/'construct01/RESULT.json');graph=dict(s.read(c/cfg['native']/'MANIFEST.json')['files_sha256'])
            names=[cfg['native']+'/MANIFEST.json',cfg['runs']+'/plan01/PLAN.json',s.request_path(cfg),cfg['audit']+'/readback.py',cfg['audit']+'/REVIEW.txt']
            names+=s.output_paths('construct',cfg)+s.output_paths('replay',cfg)
            for name in names:graph[name]=s.digest(c/name)
            value=dict(status=cfg['readback_status'],mathematical_status='SYNTHETIC',execution_status='SYNTHETIC',n=cfg['n'],target=cfg['target'],
                exact_rows=len(cfg['n']),attempts=1,negative_controls=cfg['readback_negative_controls'],files_sha256=graph)
            if key=='universal':value.update(rho=cfg['rho'],normalized_upper_max='2/5',rho_strips=1,h_cells=1,external_tail_from='19/10',external_tail_upper='2/5')
            else:
                value.update(strips=1,per_n_upper=native['per_n_upper'],uniform_upper=native['uniform_upper'])
                if key=='supported':value.update(rho=cfg['rho'],support_absolute_upper='3')
                else:
                    value.update(finite_rho=cfg['rho'],sharp20_contact_allowance_using_CE_gt_4095_10000=str(20*(F(41,100)-F(819,2000))),
                                 sharp20_contact_allowance_using_CE_gt_40973218_100000000=str(20*(F(41,100)-F(40973218,10**8))))
        if hasattr(self,'mutate'):self.mutate(action,value,key)
        if action=='readback':
            output=c/s.result_path(cfg);put(output,value);stdout=json.dumps({k:v for k,v in value.items()if k!='files_sha256'})+'\n'
        else:
            folder=c/cfg['runs']/s.LABELS[action];folder.mkdir(parents=True,exist_ok=False);name='PLAN.json'if action=='plan'else'RESULT.json';output=folder/name;put(output,value)
            stdout='SYNTHETIC ORIGINAL '+action+'\n';(folder/'stdout.txt').write_bytes(stdout.encode());(folder/'stderr.txt').write_bytes(b'')
            inputs=dict(s.read(c/cfg['native']/'MANIFEST.json')['files_sha256']);inputs[cfg['native']+'/MANIFEST.json']=s.digest(c/cfg['native']/'MANIFEST.json')
            if action=='plan':child=[argv[0],'-B','planner.py',*cfg['plan_extra_arguments'],str(planfile)]
            else:
                child=[argv[0],'-B','protocol.py',action,str(planfile),str(output)];inputs[cfg['runs']+'/plan01/PLAN.json']=s.digest(planfile)
            put(folder/'metadata.json',dict(command=child,cwd=str(c/cfg['native']),input_sha256=inputs,python=r.sys.version,platform='SYNTHETIC',
                started_utc='SYNTHETIC',returncode=0,elapsed_seconds=.1,finished_utc='SYNTHETIC',changed_inputs=[],
                stdout_sha256=s.digest(folder/'stdout.txt'),stderr_sha256=s.digest(folder/'stderr.txt'),**{name+'_sha256':s.digest(output)}))
        d.mkdir(parents=True);(d/'stdout.txt').write_bytes(stdout.encode());(d/'stderr.txt').write_bytes(b'')
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(d),sample_seconds=.2,**kw);launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds']);launch['checkpoint_paths']=[str(p)for p in launch['checkpoint_paths']];put(d/'launch.json',launch)
        copies=r.linux_supervisor._capture_checkpoints(launch)
        scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(e.WALL_SECONDS),
            per_process_RLIMIT_AS_bytes=e.MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=e.CPU_SECONDS,aggregate_kernel_memory_limit=False,
            aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=e.MEMORY_BYTES,sampled_group_CPU_limit_seconds=e.CPU_SECONDS,
            sampled_file_limit_bytes=512*s.MIB,sampled_log_limit_bytes=16*s.MIB,descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
        observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,elapsed_seconds=.1,
            maximum_sampled_group_RSS_bytes=10*s.MIB,maximum_sampled_group_CPU_seconds=.1,guard_scope=scope,checkpoints=copies,
            **{k+suffix:v for k in('stdout','stderr')for suffix,v in(('_path',str(d/(k+'.txt'))),('_sha256',s.digest(d/(k+'.txt'))))})
        put(d/'supervisor-result.json',observed);return observed

    def complete(self,key='auxiliary',name=None,effect=None):
        task=self.root/(name or key)
        with patch.object(r.linux_supervisor,'run',side_effect=effect or self.fake),patch.object(r,'Follow'):
            result=r.execute(task,self.caches[key],key,root=self.root)
        return task,result

    def test_three_whole_original_families_captures_and_false_global_flags(self):
        for key in s.FAMILIES:
            task,result=self.complete(key);self.assertTrue(result['conditional_fourier_arithmetic_completed'])
            for flag in e.FLAGS:self.assertIs(result[flag],False)
            self.assertEqual([a for k,a in self.calls if k==key],list(s.ACTIONS))
            cfg=s.family(key);plan=s.read(task/'executions/plan/launch.json')
            self.assertEqual(plan['argv'][-2:],['6/5','19/10']if key=='universal'else['plan','plan01'])
            if key=='auxiliary':self.assertEqual(result['summary']['n'],[19,20,21,22,23,24]);self.assertTrue(result['summary']['interfaces']['actual20_24_owncap419_numeric_gate'])

    def test_relocation_full_cache_bytes_and_wrong_family_rejected(self):
        task,result=self.complete();moved=self.root/'moved';shutil.copytree(task,moved)
        before={p.relative_to(moved).as_posix():p.read_bytes()for p in moved.rglob('*')if p.is_file()};self.assertEqual(e.validate_completed(moved),result)
        self.assertEqual(before,{p.relative_to(moved).as_posix():p.read_bytes()for p in moved.rglob('*')if p.is_file()})
        cache=self.root/'saved';r.save_completed(task,cache)
        with patch.object(r.linux_supervisor,'run',side_effect=AssertionError('No original maths'))as native:loaded=r.restore_completed(cache,self.root/'restored','auxiliary',root=self.root)
        native.assert_not_called();self.assertEqual(loaded[1],result)
        self.assertIsNone(r.restore_completed(cache,self.root/'wrong','universal',root=self.root))

    def test_closed_domains_h_full_cover_n19_and_support_cannot_shrink(self):
        for key,change in(('auxiliary',lambda p:p['n'].pop(0)),('supported',lambda p:p.update(support_absolute_upper='4')),
                           ('universal',lambda p:p['strips'][0]['h_panels'][0].update(h=['1/2','9/10']))):
            self.mutate=lambda a,p,k:change(p)if a=='plan'else None
            with self.assertRaises(ValueError):self.complete(key,'badplan-'+key)

    def test_changed_whole_replay_payload_or_native_status_is_not_ignored(self):
        for key in s.FAMILIES:
            self.mutate=lambda a,p,k:p.update(status='NOT_CLOSED')if a=='replay'else None
            with self.assertRaises(ValueError):self.complete(key,'badnative-'+key)
        self.mutate=lambda a,p,k:p.update(uniform_upper_float=.123)if a=='replay'else None
        with self.assertRaises(ValueError):self.complete('auxiliary','changedfloat')

    def test_controls_literal_rows_meshes_and_readback_terminal_all_bound(self):
        for i,change in enumerate((lambda p:p.update(controls={'negative_controls':12,'finite_sum_identities':4}),
                                   lambda p:p['rows'].pop(),lambda p:p['attempts'][0].update(mesh=256))):
            self.mutate=lambda a,p,k:change(p)if a in('construct','replay')else None
            with self.assertRaises(ValueError):self.complete('auxiliary','badrows'+str(i))
        self.mutate=lambda a,p,k:p.update(negative_controls=23)if a=='readback'else None
        with self.assertRaises(ValueError):self.complete('auxiliary','badcontrols')

    def test_auxiliary42_does_not_automatically_supply_419_interface(self):
        def mutate(a,p,k):
            if a in('construct','replay'):
                p['per_n_upper']['20']='839/2000';p['uniform_upper']='839/2000';p['uniform_upper_float']=.4195
                p['rows'][1]['normalized_upper']='839/2000';p['attempts'][0]['normalized_uppers'][1]='839/2000'
        self.mutate=mutate
        with self.assertRaisesRegex(ValueError,'Fresh numeric actual20 allowance'):self.complete('auxiliary','wrong419')

    def test_actual_guard_copies_cwd_and_capture_stream_mutations_rejected(self):
        for i,change in enumerate((lambda p:p.update(returncode=False),lambda p:p['guard_scope'].update(proof_acceptance=True),lambda p:p.update(checkpoints=[]))):
            def effect(*a,**k):
                p=self.fake(*a,**k);change(p);put(Path(k['output_dir'])/'supervisor-result.json',p);return p
            with self.assertRaises(ValueError):self.complete('auxiliary','guard'+str(i),effect)
        task,_=self.complete('supported','capture');cfg=s.family('supported');p=task/'capsule'/cfg['runs']/'construct01/metadata.json';v=s.read(p);v['cwd']=str(task);put(p,v)
        with self.assertRaises(ValueError):e.validate_completed(task)

    def test_unbound_import_source_and_partial_cache_rejected(self):
        task=self.root/'sealed';s.prepare(self.caches['auxiliary'],task,'auxiliary');cfg=s.family('auxiliary');(task/'capsule'/cfg['native']/'foreign.py').write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify_job(task)
        z=Mock()
        for name in('SOURCES.json','../escape','/absolute','a//b','a\\b'):
            v=zipfile.ZipInfo();v.filename=v.orig_filename=name;z.infolist.return_value=[v]
            with self.assertRaises(ValueError):r.cache_members(z)

    def test_failure_always_exports_false_session(self):
        with patch.object(r,'restore_completed',return_value=None),patch.object(s,'obtain_assets',side_effect=ValueError('Synthetic unavailable')):
            result=r.run_colab('auxiliary',durable_root=self.root/'drive',work_root=self.root/'runs')
        self.assertFalse(result['status']['conditional_fourier_arithmetic_completed']);self.assertTrue(Path(result['bundle']).is_file())

class SourcePlan(unittest.TestCase):
    def test_actual_all_three_original_manifests_and_complete_sources(self):
        for key,count,rows,size in(('auxiliary',51,48,405220),('universal',46,43,377460),('supported',51,48,463636)):
            c=s.family(key);self.assertEqual(len(c['source_files']),count);self.assertEqual(c['original_manifest_rows'],rows);self.assertEqual(sum(v['bytes']for v in c['source_files'].values()),size)
            self.assertNotIn(s.request_path(c),c['source_files'])
            for a in s.ACTIONS:self.assertFalse(set(s.output_paths(a,c))&set(c['source_files']))

if __name__=='__main__':unittest.main()
