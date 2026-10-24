"""58B/C infrastructure uses trap original sources and fake arithmetic only."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import io,json,shutil,tempfile,unittest,zipfile
from unittest.mock import patch,Mock
from be_replay import finite2124_core_sources as s,finite2124_core_evidence as e,finite2124_core as r

def put(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.dump(x));return s.digest(p)

class Core(unittest.TestCase):
    def setUp(self):
        real=s.plan();self.temp=tempfile.TemporaryDirectory(prefix='t58bc-',dir=s.ROOT.parent);self.root=Path(self.temp.name);self.addCleanup(self.temp.cleanup)
        self.assertTrue(self.root.resolve().is_relative_to(s.ROOT.parent.resolve()));self.cache=self.root/'sources'
        I=self.cache/s.INITIAL;S=self.cache/s.RESOURCE;I.mkdir(parents=True);S.mkdir(parents=True)
        for p in [I/'initial.py',I/'engine/kernel.py',S/'resources_v2.py']+[S/s.case(n,b)/'engine/resource25_core.py'for n in(21,22,23,24)for b in s.BANDS]:
            p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'raise AssertionError("Never import or execute original mathematical modules locally")\n')
        initial_graph={p.relative_to(self.cache).as_posix():s.digest(p)for p in(I/'initial.py',I/'engine/kernel.py')}
        freeze=put(I/'FROZEN_SOURCES.json',dict(files_sha256=initial_graph,scope='SYNTHETIC'))
        put(self.cache/s.INITIAL_REVIEW,dict(status='PASS_INDEPENDENT_CONDITIONAL_21_24_INITIAL_SOURCE_REVIEW',files_sha256=initial_graph|{s.INITIAL+'/FROZEN_SOURCES.json':freeze}))
        rg={p.relative_to(self.cache).as_posix():s.digest(p)for p in S.rglob('*.py')}|{s.INITIAL+'/FROZEN_SOURCES.json':freeze}
        rfreeze=put(S/'FROZEN_SOURCES_V2.json',dict(files_sha256=rg,initial_source_freeze_sha256=freeze))
        static={p.relative_to(self.cache).as_posix():s.digest(p)for p in self.cache.rglob('*')if p.is_file()}
        removed={s.INITIAL+'/n21_B0/'+v:'f'*64 for v in('CANDIDATE.json','ACCEPTED.json')}
        removed|={p:'f'*64 for a in('initial_construct','initial_accept')for p in s.capture_paths(a,21,'B0')}
        put(self.cache/s.RESOURCE_REVIEW,dict(status='PASS_INDEPENDENT_CONDITIONAL_21_24_RESOURCE_SOURCE_REVIEW',files_sha256=static|removed,
                                            whole_module_ports=128,profile_ports=list(range(8)),scope='SYNTHETIC conditional source review'))
        files={p.relative_to(self.cache).as_posix():dict(bytes=p.stat().st_size,sha256=s.digest(p))for p in self.cache.rglob('*')if p.is_file()}
        self.plan=dict(source_files=files,static_resource_review_graph=static,removed_historical_example_graph=removed,
                       initial_negative_controls=real['initial_negative_controls'],resource_negative_controls=real['resource_negative_controls'])
        for p in(patch.object(s,'plan',side_effect=lambda:deepcopy(self.plan)),patch.object(s,'INITIAL_FREEZE',freeze),
                 patch.object(r.sys,'platform','linux'),patch.object(r.sys,'stdout',io.StringIO())):
            p.start();self.addCleanup(p.stop)
        self.calls=[]

    def fake(self,argv,*,cwd,output_dir,**kw):
        d=Path(output_dir);action=d.name;task=d.parent.parent;c=task/'capsule';request=s.read(task/'SOURCES.json');n,b=request['n'],request['band']
        self.calls.append((n,b,action));name=s.case(n,b);rho,radius=s.BANDS[b]
        if action=='initial_construct':
            req=dict(n=n,nmax=n,K='0',q='0',owncap='419/1000',band=b,rho_interval=rho,radius=radius,grid=[12,12,6,3]);beta='1/5'
            panels=[dict(pl=str(F(i,100)),pu=str(F(i+1,100)),raw='1',D='1',theta='1/100')for i in range(100)]
            cover=dict(total=2592,active=2592,excluded=0,reasons={},R='1',D='1',panels=panels)
            stages=[dict(input_raw=None if j==0 else'1',input_D=None if j==0 else'1',next_raw='1',next_D='1',cover=deepcopy(cover))for j in range(8)]
            support=dict(schema='DIRECT_SAME_LAW_CONTACT_SUPPORT_DISCOVERY_V1',n=n,K='0',q_contact='0',radius=radius,support_sign=0,
                         rho_upper=rho[1],beta_interval=['-1/5','1/5'],ray_rows=[dict(sign=-1),dict(sign=1)],scope='SYNTHETIC original support scope')
            packet=dict(status=e.INITIAL_CANDIDATE,request=req,beta_upper=beta,support=support,
                profile=dict(n=n,nmax=n,radius=radius,radius_minus=radius,radius_plus=radius,cap='419/1000',barrier='0',grid=[12,12,6,3],
                             invariants=dict(rho=rho[1],rho_lo=rho[0],beta_lo='-1/5',beta_hi='1/5')),
                stages=stages,export=cover,final_invariants=dict(raw='1',D='1'),predecessor_verified=False,owncap_source='SYNTHETIC UNACQUIRED',
                sharp20_proved=False,cutoff20_proved=False,source_freeze_sha256=s.INITIAL_FREEZE)
        elif action=='initial_accept':
            initial=c/s.INITIAL/name;z=s.read(initial/'CANDIDATE.json')
            packet=dict(status=e.INITIAL_ACCEPTED,n=n,band=b,request=z['request'],candidate_sha256=s.digest(initial/'CANDIDATE.json'),
                source_freeze_sha256=s.INITIAL_FREEZE,source_review_sha256=s.digest(c/s.INITIAL_REVIEW),negative_controls=deepcopy(self.plan['initial_negative_controls']),
                final_invariants=z['final_invariants'],fresh_support_calls=1,fresh_complete_signed_covers=9,signed_cells_per_cover=2592,
                original_probability_panels=100,predecessor_verified=False,sharp20_proved=False,cutoff20_proved=False,elapsed_seconds=.1)
        elif action=='resource_construct':
            s.verify_review_epoch(task,n,b);z=s.read(c/s.INITIAL/name/'CANDIDATE.json');rows=[];folder=c/s.RESOURCE/name
            for i in range(100):
                source=deepcopy(z['export']['panels'][i]);source['rho_lo']=rho[0];status='EXCLUDED_BY_SAME_LAW_RESOURCE'if i%3 else'RESOURCE_ROW_ACQUIRED_FOR_COUNT'
                row=dict(n=n,band=b,index=i,source=source,plan=[],status=status,result=dict(excluded=i%3!=0))
                if getattr(self,'criterion_failed',False)and i==0:
                    row={k:v for k,v in row.items()if k not in('plan','result')};row.update(status='RESOURCE_CRITERION_FAILED_NO_EXCLUSION',failure_type='ValueError',reason='SYNTHETIC criterion not acquired');status=row['status']
                p=folder/'rows'/('%.3d.json'%i);put(p,row)
                rows.append(dict(n=n,band=b,index=i,p=[str(F(i,100)),str(F(i+1,100))],path='rows/'+p.name,sha256=s.digest(p),status=status))
            support=deepcopy(z['support']);support['schema']='DIRECT_FIXED_INDEX_GAUSSIAN_SUPPORT_V1';support['q']=support.pop('q_contact')
            support['scope']='Attained positive closed maximizer at the stated fixed index, C_n>=CE+K/n and delta_n<=q, with any additionally declared same-law moment caps. Excludes every support point on the specified full ray(s), uniformly in H. This is not a score exclusion.'
            packet=dict(status=e.RESOURCE_CANDIDATE,n=n,K='0',q='0',owncap='419/1000',band=b,rho_interval=rho,rows=rows,
                status_counts=dict(Counter(x['status']for x in rows)),initial_candidate_sha256=s.digest(c/s.INITIAL/name/'CANDIDATE.json'),
                initial_acceptance_sha256=s.digest(c/s.INITIAL/name/'ACCEPTED.json'),support=support,files_sha256=e.resource_graph(task,request),
                predecessor_verified=False,global_bound_proved=False,cutoff20_proved=False)
            put(folder/'CONSTRUCT_TIMINGS.json',[.01]*100)
        else:
            folder=c/s.RESOURCE/name;z=s.read(folder/'CANDIDATE.json')
            packet=dict(status=e.RESOURCE_ACCEPTED,n=n,band=b,candidate_sha256=s.digest(folder/'CANDIDATE.json'),rows=z['rows'],status_counts=z['status_counts'],
                negative_controls=deepcopy(self.plan['resource_negative_controls']),timings_seconds=[.01]*100,files_sha256=z['files_sha256'],
                predecessor_verified=False,global_bound_proved=False,cutoff20_proved=False)
        if hasattr(self,'mutate'):self.mutate(action,packet)
        output=c/s.output_paths(action,n,b)[0];put(output,packet)
        label={'initial_construct':'CANDIDATE_STORED','initial_accept':'ACCEPTED_STORED','resource_construct':'RESOURCE_CANDIDATE','resource_accept':'RESOURCE_ACCEPTED'}[action]
        line=label+' '+str(n)+' '+b+' '+(str(packet['status_counts'])+' 'if action.startswith('resource_')else'')+s.digest(output)+'\n'
        if hasattr(self,'stdout_mutator'):line=self.stdout_mutator(action,line)
        d.mkdir(parents=True);(d/'stdout.txt').write_bytes(line.encode());(d/'stderr.txt').write_bytes(b'')
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

    def complete(self,name='task',n=21,band='B0',effect=None):
        task=self.root/name
        with patch.object(r.linux_supervisor,'run',side_effect=effect or self.fake),patch.object(r,'Follow'):
            result=r.execute(task,self.cache,n,band,root=self.root)
        return task,result

    def test_full_four_calls_actual_cwd_copies_and_false_scope(self):
        task,result=self.complete();self.assertEqual([x[2]for x in self.calls],list(s.ACTIONS));self.assertTrue(result['conditional_core_arithmetic_completed'])
        for flag in e.FLAGS:self.assertIs(result[flag],False)
        self.assertEqual(result['summary']['resource_rows_per_action'],100)
        for action in s.ACTIONS:
            d=task/'executions'/action;launch=s.read(d/'launch.json');observed=s.read(d/'supervisor-result.json')
            self.assertEqual(launch['argv'][1:3],['-B','-u']);self.assertEqual(launch['argv'][4:7],[action.split('_')[1],'21','B0'])
            for p in observed['checkpoints']:self.assertEqual(Path(p['path']),d/'checkpoints'/Path(p['source_path']).relative_to(Path(launch['cwd'])))
        self.assertEqual(len(s.read(task/'executions/resource_construct/supervisor-result.json')['checkpoints']),102)

    def test_other_band_actual_n24_and_closed_seam(self):
        _,result=self.complete('bn',24,'BN');req=result['summary']['request']
        self.assertEqual(req['rho_interval'],['11/10','9/8']);self.assertEqual(req['radius'],'12/5');self.assertEqual(req['n'],24)

    def test_data_only_review_preserves_every_non_graph_field_and_exact_eight_change(self):
        task,_=self.complete();c=task/'capsule';original=s.read(c/s.RESOURCE_REVIEW);fresh=s.read(c/s.review_paths(21,'B0')[0]);bridge=s.verify_review_epoch(task,21,'B0')
        self.assertEqual({k:v for k,v in original.items()if k!='files_sha256'},{k:v for k,v in fresh.items()if k!='files_sha256'})
        self.assertEqual(bridge['fresh_parent_graph'],s.fresh_parent_graph(task,21,'B0'));self.assertEqual(len(bridge['fresh_parent_graph']),8)
        self.assertEqual(original['files_sha256'],self.plan['static_resource_review_graph']|self.plan['removed_historical_example_graph'])
        self.assertNotEqual(original['files_sha256'],fresh['files_sha256'])
        self.assertEqual(fresh['files_sha256'],self.plan['static_resource_review_graph']|bridge['fresh_parent_graph'])

    def test_relocation_and_complete_zip_skip_all_four_calls_without_rewriting(self):
        task,result=self.complete();dest=self.root/'moved';shutil.copytree(task,dest)
        before={p.relative_to(dest).as_posix():p.read_bytes()for p in dest.rglob('*')if p.is_file()};self.assertEqual(e.validate_completed(dest),result)
        self.assertEqual(before,{p.relative_to(dest).as_posix():p.read_bytes()for p in dest.rglob('*')if p.is_file()})
        cache=self.root/'saved';saved=r.save_completed(task,cache)
        with patch.object(r.linux_supervisor,'run',side_effect=AssertionError('No original math'))as native:
            restored=r.restore_completed(cache,self.root/'restore',21,'B0',root=self.root)
        native.assert_not_called();self.assertEqual(restored[1],result)
        self.assertIsNone(r.restore_completed(cache,self.root/'wrong-case',22,'B0',root=self.root))
        Path(saved['path']).with_suffix('.zip.sha256').write_bytes(b'bad');self.assertIsNone(r.restore_completed(cache,self.root/'bad',21,'B0',root=self.root))

    def test_changed_fresh_review_graph_or_non_graph_metadata_fails(self):
        task,_=self.complete();p=task/'capsule'/s.review_paths(21,'B0')[0];raw=p.read_bytes()
        for mutate in(lambda x:x.update(whole_module_ports=0),lambda x:x.update(files_sha256=self.plan['static_resource_review_graph']|self.plan['removed_historical_example_graph'])):
            d=json.loads(raw);mutate(d);put(p,d)
            with self.assertRaises(ValueError):e.validate_completed(task)
        p.write_bytes(raw);p=task/'capsule'/s.review_paths(21,'B0')[1];d=s.read(p);d['metadata_only']=False;put(p,d)
        with self.assertRaises(ValueError):e.validate_completed(task)

    def test_changed_current_initial_capture_cwd_command_result_or_bridge(self):
        task,_=self.complete();p=task/'capsule'/s.capture_paths('initial_accept',21,'B0')[0];raw=p.read_bytes()
        for mutate in(lambda x:x.update(cwd=str(task)),lambda x:x['command'].append('foreign'),lambda x:x.update(result_sha256='0'*64),
                      lambda x:x['capture_bridge'].update(supervisor_result_sha256='0'*64),lambda x:x.update(returncode=False)):
            d=json.loads(raw);mutate(d);put(p,d)
            with self.assertRaises(ValueError):e.validate_completed(task)

    def test_initial_covers_panels_controls_and_zero_allowance_cannot_shrink(self):
        self.mutate=lambda action,x:x.update(fresh_complete_signed_covers=8)if action=='initial_accept'else None
        with self.assertRaises(ValueError):self.complete('badinitial-census')
        self.assertFalse((self.root/'badinitial-census/STAGE_COMPLETED.json').exists())
        self.assertFalse(any(a=='resource_construct'for _,_,a in self.calls))
        del self.mutate
        task,_=self.complete('initial-payload-controls');p=task/'capsule'/s.INITIAL/'n21_B0/ACCEPTED.json';raw=p.read_bytes()
        for mutate in(lambda x:x.update(original_probability_panels=99),lambda x:x['request'].update(q='1'),
                      lambda x:x['negative_controls'].pop(),lambda x:x.update(n=True)):
            packet=json.loads(raw);mutate(packet);put(p,packet)
            with self.assertRaises(ValueError):e.validate_completed(task)
        p.write_bytes(raw)

    def test_resource_all_rows_controls_parent_and_no_false_global_claim(self):
        task,_=self.complete();p=task/'capsule'/s.RESOURCE/'n21_B0/ACCEPTED.json';raw=p.read_bytes()
        for mutate in(lambda x:x['rows'].pop(),lambda x:x['negative_controls'].pop(),lambda x:x.update(candidate_sha256='f'*64),
                      lambda x:x.update(global_bound_proved=True),lambda x:x.update(n=True)):
            packet=json.loads(raw);mutate(packet);put(p,packet)
            with self.assertRaisesRegex(ValueError,'Whole fresh full resource acceptance'):e.validate_completed(task)
        p.write_bytes(raw)

    def test_failed_criterion_is_explicit_no_exclusion_not_a_theorem(self):
        self.criterion_failed=True;_,result=self.complete();self.assertEqual(result['summary']['status_counts']['RESOURCE_CRITERION_FAILED_NO_EXCLUSION'],1)
        self.assertFalse(result['all_index_conclusion_verified']);self.assertFalse(result['resource_count_join_verified'])

    def test_false_rc_bad_guard_or_missing_copies_stop_before_acceptance(self):
        for i,mutate in enumerate((lambda x:x.update(returncode=False),lambda x:x['guard_scope'].update(proof_acceptance=True),
                                   lambda x:x.update(checkpoints=[]),lambda x:x.update(stdout_sha256='0'*64))):
            def effect(*a,**k):
                p=self.fake(*a,**k);mutate(p);put(Path(k['output_dir'])/'supervisor-result.json',p);return p
            with self.assertRaises(ValueError):self.complete('guard'+str(i),effect=effect)

    def test_zero_rc_without_exact_initial_terminal_never_starts_resource(self):
        self.stdout_mutator=lambda a,line:'INCOMPLETE\n'if a=='initial_construct'else line
        with self.assertRaises(ValueError):self.complete('terminal')
        self.assertEqual([a for _,_,a in self.calls],['initial_construct','initial_accept'])

    def test_extra_source_or_changed_hardcoded_freeze_cannot_validate(self):
        task=self.root/'sealed';s.prepare(self.cache,task,21,'B0');p=task/'capsule'/s.INITIAL/'foreign.py';p.write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify_job(task)
        p.unlink();(task/'capsule'/s.INITIAL/'FROZEN_SOURCES.json').write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify_job(task)

    def test_complete_case_routing_all_four_and_failure_export(self):
        def loaded(cache,destination,n,b,*,root):
            p=Path(destination)/s.case(n,b);p.mkdir(parents=True);return p,{'conditional_core_arithmetic_completed':True},{'sha256':'a'*64}
        with patch.object(r,'restore_completed',side_effect=loaded),patch.object(s,'obtain_assets',side_effect=AssertionError('Complete cache must skip download')):
            result=r.run_colab('BN',durable_root=self.root/'drive',work_root=self.root/'runs')
        self.assertTrue(result['status']['conditional_band_core_arithmetic_completed']);self.assertEqual([x['n']for x in result['status']['cases']],[21,22,23,24])
        for flag in e.FLAGS:self.assertIs(result['status'][flag],False)
        with patch.object(r,'restore_completed',return_value=None),patch.object(s,'obtain_assets',side_effect=ValueError('Synthetic unavailable')):
            failed=r.run_colab('B0',durable_root=self.root/'drive',work_root=self.root/'runs')
        self.assertFalse(failed['status']['conditional_band_core_arithmetic_completed']);self.assertTrue(Path(failed['bundle']).is_file())

    def test_bad_cache_members_rejected_before_extraction(self):
        z=Mock()
        for name in('SOURCES.json','../escape','/absolute','a//b','a\\b'):
            info=zipfile.ZipInfo();info.filename=info.orig_filename=name;z.infolist.return_value=[info]
            with self.assertRaises(ValueError):r.cache_members(z)


class SourcePlan(unittest.TestCase):
    def test_actual193_inputs_initial_freeze_controls_and_no_old_parent_outputs(self):
        d=s.plan();self.assertEqual(len(d['source_files']),193);self.assertEqual(sum(x['bytes']for x in d['source_files'].values()),1159340)
        self.assertEqual(d['initial_freeze_sha256'],s.INITIAL_FREEZE);self.assertEqual(len(d['static_resource_review_graph']),190)
        self.assertEqual(len(d['initial_negative_controls']),12);self.assertEqual(len(d['resource_negative_controls']),12)
        self.assertFalse(set(d['source_files'])&set(d['removed_historical_example_graph']))
        for n in(21,22,23,24):
            for b in s.BANDS:
                self.assertFalse(set(s.generated_paths(n,b))&set(d['source_files']))


if __name__=='__main__':unittest.main()
