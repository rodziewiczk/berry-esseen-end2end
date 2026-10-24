"""Synthetic59A transport/metadata/cache fixtures; original programs are traps."""
from __future__ import annotations
import copy,io,json,shutil,stat,tempfile,unittest,zipfile
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import Mock,patch
from be_replay import finite2630_b1_sources as s,finite2630_b1_evidence as e,finite2630_b1 as r

def put(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(s.dump(value));return s.digest(path)

class Pipeline(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=s.ROOT.parent,prefix='t59a-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.cache=self.root/'cache';self.spec=copy.deepcopy(s.plan())
        for name,row in self.spec['source_files'].items():
            p=self.cache/name;p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(b'raise AssertionError("Original mathematics must not run in local fixtures")\n'if name.endswith('.py')else b'{}\n')
            row.update(bytes=p.stat().st_size,sha256=s.digest(p))
        rows=[dict(id=f'B1_sine_strip{j:02d}',n_values=[26,27,28,29,30],
                   rho=[str(F(11,10)+F(j,230)),str(F(11,10)+F(j+1,230))],D_upper='1',zeta_lower='1',c='1',tau='1/10')for j in range(23)]
        record=dict(status='SYNTHETIC_NOT_A_MATHEMATICAL_CERTIFICATE',intended_integration_target='4097/10000',rows=rows,
                    acquired_scopes=[dict(n=26+i//11,index=32+i%11)for i in range(55)],
                    support_constants=dict(A='17/10',B='1037/100',M='13/5'),kappa='62/625',controls={'synthetic':True},
                    input_sha256={old:self.spec['source_files'][name]['sha256']for old,name in self.spec['original_absolute_input_map'].items()})
        put(self.cache/s.RECORD,record)
        self.spec['source_files'][s.RECORD].update(bytes=(self.cache/s.RECORD).stat().st_size,sha256=s.digest(self.cache/s.RECORD))
        manifest=dict(status='SYNTHETIC_SOURCE_ONLY',files_sha256={n:v['sha256']for n,v in self.spec['source_files'].items()if n!=s.MANIFEST})
        put(self.cache/s.MANIFEST,manifest)
        self.spec['source_files'][s.MANIFEST].update(bytes=(self.cache/s.MANIFEST).stat().st_size,sha256=s.digest(self.cache/s.MANIFEST))
        self.spec['original_manifest_sha256']=s.digest(self.cache/s.MANIFEST)
        for target,name,value in((s,'plan',lambda:self.spec),(r.sys,'platform','linux'),(r.sys,'stdout',io.StringIO())):
            p=patch.object(target,name,value);p.start();self.addCleanup(p.stop)

    def fake(self,argv,*,cwd,output_dir,**kwargs):
        c=Path(cwd);task=Path(output_dir).parents[1];directory=Path(output_dir);action=argv[-1]
        record=s.read(task/'capsule'/s.RECORD);expected={k:v for k,v in record.items()if k not in('controls','input_sha256')}
        source=dict(manifest_sha256=s.digest(task/'capsule'/s.MANIFEST),files_sha256=s.read(task/'capsule'/s.MANIFEST)['files_sha256'])
        if action=='construct':
            result=dict(schema='ACTUAL26_30_ALL_B1_SCALAR_SINE_PHASE_FOURIER_V1',target='4097/10000',inputs=expected,
                pieces=[dict(id=row['id'],cells_per_piece=256,result=dict(rows=[dict(n=n,normalized_upper='2/5',terms={'tail':'1/100'})for n in range(26,31)]))for row in expected['rows']],
                source=source,mathematical_status='SYNTHETIC NO MATHEMATICS',cutoff25_proved=False,global_predecessors_proved=False)
        else:
            result=dict(status=e.ACCEPT,proof_sha256=s.digest(c/'COVER.json'),source=source,target='4097/10000',
                        maximum_upper='2/5',maximum_upper_float=.4,exact_rows=115,rho_strips=23,
                        acquired_scopes=expected['acquired_scopes'],negative_controls=e.CONTROL_NAMES.copy(),seconds=.1,
                        cutoff25_proved=False,global_predecessors_proved=False)
        if hasattr(self,'result_mutator'):self.result_mutator(action,result)
        output=c/s.OUTPUTS[action];put(output,result);directory.mkdir(parents=True)
        last=('CONSTRUCTED_NOT_ACCEPTED '+s.digest(output)+' 0.1')if action=='construct'else e.ACCEPT+' 115 0.4 18 0.1'
        stdout=''.join('EXACT_SCALAR_B1_STRIP '+str(i+1)+' 23 SYNTHETIC\n'for i in range(23))+last+'\n'
        (directory/'stdout.txt').write_bytes(stdout.encode());(directory/'stderr.txt').write_bytes(b'')
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,**kwargs)
        launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds'])
        launch['checkpoint_paths']=[str(p)for p in kwargs['checkpoint_paths']]
        if hasattr(self,'launch_mutator'):self.launch_mutator(launch)
        put(directory/'launch.json',launch)
        copies=r.linux_supervisor._capture_checkpoints(launch)
        observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,
            sample_count=1,elapsed_seconds=.1,maximum_sampled_group_CPU_seconds=.1,maximum_sampled_group_RSS_bytes=1024,
            guard_scope=e.guard(),checkpoints=copies,
            **{kind+suffix:value for kind in('stdout','stderr')for suffix,value in
               (('_path',str(directory/(kind+'.txt'))),('_sha256',s.digest(directory/(kind+'.txt'))))})
        if hasattr(self,'observed_mutator'):self.observed_mutator(observed)
        put(directory/'supervisor-result.json',observed)
        final=dict(event='linux_supervisor_finished',stage='untrusted_search',status=observed['status'],reason=observed['reason'],elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
        put(directory/'progress.json',final);(directory/'progress.jsonl').write_bytes(json.dumps(final).encode()+b'\n')
        return observed

    def complete(self,name='task'):
        task=self.root/name
        with patch.object(r.linux_supervisor,'run',side_effect=self.fake)as child,patch.object(r,'Follow'):
            result=r.execute(task,self.cache,root=self.root)
        self.assertEqual(child.call_count,2);return task,result

    def test_full_two_passes_false_global_scope_and_real_stopped_copy_layout(self):
        task,result=self.complete();self.assertTrue(result['conditional_fourier_arithmetic_completed'])
        self.assertEqual(result['summary']['exact_rows'],115)
        for flag in e.FLAGS:self.assertIs(result[flag],False)
        request=s.verify_job(task)
        for action in s.ACTIONS:
            launch=s.read(task/'executions'/action/'launch.json')
            self.assertEqual(launch['argv'],e.command(request,action,s.read(task/'STAGE_OBSERVED.json')['python_executable']))
            self.assertEqual((task/'executions'/action/'checkpoints'/s.OUTPUTS[action]).read_bytes(),(task/'capsule'/s.NATIVE/s.OUTPUTS[action]).read_bytes())

    def test_only12_locations_and_one_manifest_hash_change(self):
        task=self.root/'prepared';s.prepare(self.cache,task);request=s.verify_job(task)
        old=s.read(task/'provenance'/s.RECORD);new=s.read(task/'capsule'/s.RECORD)
        self.assertEqual({k:v for k,v in old.items()if k!='input_sha256'},{k:v for k,v in new.items()if k!='input_sha256'})
        self.assertEqual(len(new['input_sha256']),12)
        new['kappa']='1';put(task/'capsule'/s.RECORD,new)
        with self.assertRaises(ValueError):s.verify_job(task)

    def test_whole_cache_relocation_preserves_original_metadata_and_skips_all_math(self):
        task,checked=self.complete();export=r.save_completed(task,self.root/'completed')
        with patch.object(r.linux_supervisor,'run',side_effect=AssertionError('No replay'))as child:
            loaded=r.restore_completed(self.root/'completed',self.root/'restored',root=self.root)
        child.assert_not_called();self.assertEqual(loaded[1],checked)
        self.assertEqual({p.relative_to(task).as_posix():p.read_bytes()for p in task.rglob('*')if p.is_file()},
                         {p.relative_to(loaded[0]).as_posix():p.read_bytes()for p in loaded[0].rglob('*')if p.is_file()})
        Path(export['path']).with_suffix('.zip.sha256').write_bytes(b'bad')
        self.assertIsNone(r.restore_completed(self.root/'completed',self.root/'bad-restore',root=self.root))

    def test_coherently_captured_wrong_indices_domains_rows_controls_or_claims_fail(self):
        changes=[lambda a,p:p.update(cutoff25_proved=True),
                 lambda a,p:p['pieces'][0]['result']['rows'][0].update(n=True)if a=='construct'else None,
                 lambda a,p:p['pieces'].pop()if a=='construct'else None,
                 lambda a,p:p['inputs']['rows'][0]['rho'].__setitem__(0,'1')if a=='construct'else None,
                 lambda a,p:p.update(negative_controls=[])if a=='accept'else None,
                 lambda a,p:p.update(exact_rows=True)if a=='accept'else None]
        for i,change in enumerate(changes):
            self.result_mutator=change
            with self.assertRaises((ValueError,KeyError)):self.complete('bad'+str(i))
            self.assertFalse((self.root/('bad'+str(i))/'STAGE_COMPLETED.json').exists())

    def test_bool_exit_incomplete_guard_or_missing_copy_fail(self):
        for i,change in enumerate((lambda p:p.update(returncode=False),lambda p:p.update(status='incomplete'),
                                  lambda p:p.update(checkpoints=[]),lambda p:p['guard_scope'].update(proof_acceptance=True))):
            self.observed_mutator=change
            with self.assertRaises(ValueError):self.complete('guard'+str(i))

    def test_wrong_command_cwd_or_limits_fail(self):
        for i,change in enumerate((lambda p:p['argv'].append('--quick'),lambda p:p.update(cwd=str(self.root)),
                                  lambda p:p.update(cpu_seconds=True),lambda p:p.update(memory_bytes=1024))):
            self.launch_mutator=change
            with self.assertRaises(ValueError):self.complete('launch'+str(i))

    def test_capture_source_epoch_or_complete_inventory_change_fails(self):
        for i,name in enumerate(('executions/accept/checkpoints/ACCEPTED.json','executions/construct/stdout.txt',
                                 'capsule/'+s.NATIVE+'/protocol.py','provenance/'+s.RECORD,'LOCATION_EPOCH.json','unexpected.txt')):
            task,_=self.complete('changed'+str(i));(task/name).write_bytes(b'changed')
            with self.assertRaises((ValueError,KeyError)):e.validate_completed(task)

    def test_incomplete_unsafe_linked_or_case_alias_cache_fails(self):
        z=Mock()
        for name in('../outside','/absolute','a//b','C:/outside','SOURCES.json'):
            info=zipfile.ZipInfo();info.filename=info.orig_filename=name;z.infolist.return_value=[info]
            with self.assertRaises(ValueError):r.cache_members(z)
        info=zipfile.ZipInfo('link');info.external_attr=(stat.S_IFLNK|0o777)<<16;z.infolist.return_value=[info]
        with self.assertRaises(ValueError):r.cache_members(z)

    def test_source_failure_still_exports_false_session(self):
        with patch.object(s,'obtain_assets',side_effect=ValueError('Synthetic source failure')):
            out=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'work',archives=self.root/'archives')
        self.assertFalse(out['status']['conditional_fourier_arithmetic_completed']);self.assertTrue(Path(out['bundle']).is_file())

class SourcePlan(unittest.TestCase):
    def test_exact83_original_sources_and_12_location_bindings(self):
        d=s.plan();self.assertEqual(len(d['source_files']),83);self.assertEqual(len(d['original_absolute_input_map']),12)
        self.assertEqual(d['actual_n'],[26,27,28,29,30]);self.assertEqual(d['exact_rows'],115)
        self.assertFalse(d['arithmetic_computed']);self.assertFalse(d['all_index_conclusion_verified'])

if __name__=='__main__':unittest.main()
