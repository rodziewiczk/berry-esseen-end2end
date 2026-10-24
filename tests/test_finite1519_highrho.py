"""Four-action synthetic infrastructure fixtures; original files are trap bytes."""
from __future__ import annotations
import copy
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch,Mock
import zipfile
from be_replay import finite1519_highrho_sources as s,finite1519_highrho_evidence as e,finite1519_highrho as r


def put(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.dump(x));return s.digest(p)


class Highrho(unittest.TestCase):
    def setUp(self):
        # The production target is Linux. Keep the Windows-only synthetic
        # root short enough for nested stopped-output cache copies.
        self.temp=tempfile.TemporaryDirectory(dir=s.ROOT.parent,prefix='t57h-');self.root=Path(self.temp.name)
        self.assertTrue(self.root.resolve().is_relative_to(s.ROOT.parent.resolve()));self.addCleanup(self.temp.cleanup)
        self.cache=self.root/'inputs';self.native=self.cache/s.NATIVE;self.audit=self.cache/s.AUDIT
        self.native.mkdir(parents=True);self.audit.mkdir(parents=True)
        for p in [self.native/n for n in('run.py','protocol.py','planner.py','integrate.py')]+[self.audit/'readback.py']:
            p.write_bytes(b'raise AssertionError("Never import or execute archived numerical source locally")\n')
        (self.audit/'REVIEW.txt').write_bytes(b'Synthetic unattested fixture only\n')
        files={p.relative_to(self.cache).as_posix():s.digest(p)for p in self.native.iterdir()}
        pin=put(self.native/'MANIFEST.json',dict(scope='SYNTHETIC_ONLY',files_sha256=files))
        allfiles={p.relative_to(self.cache).as_posix():dict(bytes=p.stat().st_size,sha256=s.digest(p))for p in self.cache.rglob('*')if p.is_file()}
        self.plan=dict(source_files=allfiles,original_manifest_sha256=pin)
        self.context=dict(scope='UNTRUSTED_FLOATING_DISCOVERY_ONLY',distribution='numpy',version='synthetic',
                          entry_sha256='0'*64,thread_environment={n:'1'for n in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')},
                          acceptance_arithmetic_depends_on_numpy=False)
        for obj,name,value in((s,'plan',self.plan),(r,'numpy_context',self.context)):
            p=patch.object(obj,name,return_value=value);p.start();self.addCleanup(p.stop)
        p=patch.object(r.sys,'platform','linux');p.start();self.addCleanup(p.stop)
        p=patch.object(r.sys,'stdout',io.StringIO());p.start();self.addCleanup(p.stop)

    def fake(self,argv, *,cwd,output_dir,**kw):
        output_dir=Path(output_dir);action=output_dir.name;task=output_dir.parent.parent;c=task/'capsule'
        request=s.read(task/'SOURCES.json');manifest=s.read(c/s.NATIVE/'MANIFEST.json')
        pplan=c/s.RUNS/'plan01/PLAN.json';native_manifest=c/s.NATIVE/'MANIFEST.json'
        if action=='readback':
            con=s.read(c/s.RUNS/'construct01/RESULT.json');graph=dict(manifest['files_sha256'])
            for n in[s.NATIVE+'/MANIFEST.json',s.RUNS+'/plan01/PLAN.json',s.REQUEST,s.AUDIT+'/readback.py',s.AUDIT+'/REVIEW.txt']+s.output_paths('construct')+s.output_paths('replay'):graph[n]=s.digest(c/n)
            result=dict(status='PASS_INDEPENDENT_GLOBAL_HIGHRHO14_19_READBACK',mathematical_status=e.MATHEMATICAL_STATUS,execution_status=e.EXECUTION_STATUS,
                n=list(range(14,20)),finite_rho=['33/25','19/10'],target='4097/10000',strips=1,exact_rows=6,attempts=1,
                per_n_upper=con['per_n_upper'],uniform_upper=con['uniform_upper'],negative_controls=24,files_sha256=graph,
                )
            put(c/s.RESULT,result);stdout=json.dumps({k:v for k,v in result.items()if k!='files_sha256'})+'\n'
        else:
            directory=c/s.RUNS/s.LABELS[action];directory.mkdir(parents=True)
            if action=='plan':
                result=dict(schema='HIGHRHO14_19_UNCONDITIONAL_PLAN_V1',n=list(range(14,20)),target='4097/10000',rho=['33/25','19/10'],
                            strips=[dict(rho=['33/25','19/10'],c='2',tau='1/4',heuristic_upper=.2)])
                name='PLAN.json';command=[argv[0],'-B','planner.py',str(pplan)]
            else:
                result=dict(status='EXACT_HIGHRHO14_19_UNCONDITIONAL_PASS',theorem=e.THEOREM,n=list(range(14,20)),target='4097/10000',
                    finite_rho=['33/25','19/10'],rows=[dict(strip_index=0,n=n)for n in range(14,20)],attempts=[dict(synthetic=True)],
                    published_tail=dict(synthetic=True),uniform_upper='1/5',uniform_upper_float=.2,
                    per_n_upper={str(n):'1/5'for n in range(14,20)},controls=dict(negative_controls=13,finite_sum_identities=4),
                    plan_sha256=s.digest(pplan),manifest_sha256=s.digest(native_manifest),seconds=.1 if action=='construct'else.2)
                if hasattr(self,'native_mutator'):self.native_mutator(result)
                name='RESULT.json';command=[argv[0],'-B','protocol.py',action,str(pplan),str(directory/name)]
            put(directory/name,result);stdout='SYNTHETIC ORIGINAL '+action+'\n'
            (directory/'stdout.txt').write_bytes(stdout.encode());(directory/'stderr.txt').write_bytes(b'')
            inputs=dict(manifest['files_sha256']);inputs[s.NATIVE+'/MANIFEST.json']=s.digest(native_manifest)
            if action!='plan':inputs[s.RUNS+'/plan01/PLAN.json']=s.digest(pplan)
            meta=dict(command=command,cwd=str(c/s.NATIVE),input_sha256=inputs,python=r.sys.version,platform='synthetic',
                started_utc='2026-10-24T00:00:00+00:00',returncode=0,elapsed_seconds=.1,finished_utc='2026-10-24T00:00:01+00:00',
                changed_inputs=[],stdout_sha256=s.digest(directory/'stdout.txt'),stderr_sha256=s.digest(directory/'stderr.txt'))
            meta[name+'_sha256']=s.digest(directory/name);put(directory/'metadata.json',meta)
        output_dir.mkdir(parents=True);(output_dir/'stdout.txt').write_bytes(stdout.encode());(output_dir/'stderr.txt').write_bytes(b'')
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,**kw)
        launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds'])
        launch['checkpoint_paths']=[str(x)for x in launch['checkpoint_paths']];put(output_dir/'launch.json',launch)
        checkpoints=[]
        for source in kw['checkpoint_paths']:
            source=Path(source);dest=output_dir/'checkpoints'/source.relative_to(c);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
            checkpoints.append(dict(source_path=str(source),exists=True,trusted_certificate=False,path=str(dest),bytes=source.stat().st_size,sha256=s.digest(source)))
        scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(e.WALL_SECONDS),
            per_process_RLIMIT_AS_bytes=e.MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=e.CPU_SECONDS,aggregate_kernel_memory_limit=False,
            aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=e.MEMORY_BYTES,sampled_group_CPU_limit_seconds=e.CPU_SECONDS,
            sampled_file_limit_bytes=512*s.MIB,sampled_log_limit_bytes=16*s.MIB,descendants_changing_session_are_contained=False,
            equivalent_to_Windows_Job_or_cgroup=False)
        observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,
            elapsed_seconds=.1,maximum_sampled_group_RSS_bytes=10*s.MIB,maximum_sampled_group_CPU_seconds=.1,
            guard_scope=scope,checkpoints=checkpoints,**{k+suffix:value for k in('stdout','stderr')for suffix,value in(
                ('_path',str(output_dir/(k+'.txt'))),('_sha256',s.digest(output_dir/(k+'.txt'))))})
        put(output_dir/'supervisor-result.json',observed);return observed

    def complete(self,name='task',effect=None):
        task=self.root/name
        with patch.object(r.linux_supervisor,'run',side_effect=effect or self.fake),patch.object(r,'Follow'):
            checked=r.execute(task,self.cache,root=self.root)
        return task,checked

    def test_four_actual_commands_complete_with_all_full57_flags_false(self):
        task,checked=self.complete();self.assertTrue(checked['conditional_highrho_arithmetic_completed'])
        for flag in e.FLAGS:self.assertIs(checked[flag],False)
        self.assertEqual(checked['summary']['native_controls'],13);self.assertEqual(checked['summary']['independent_controls'],24)
        self.assertEqual([x['action']for x in s.read(task/'STAGE_OBSERVED.json')['actions']],list(s.ACTIONS))
        self.assertEqual((self.native/'MANIFEST.json').read_bytes(),(task/'capsule'/s.NATIVE/'MANIFEST.json').read_bytes())

    def test_unchanged_full_source_capsule_rejects_extra_or_modified_helpers(self):
        task=self.root/'prepare';s.prepare(self.cache,task);p=task/'capsule'/s.NATIVE/'unbound.py';p.write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify_job(task)
        p.unlink();(task/'capsule'/s.NATIVE/'run.py').write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify_job(task)

    def test_relocation_preserves_original_capture_paths_and_all_bytes(self):
        task,checked=self.complete();dest=self.root/'restored';shutil.copytree(task,dest)
        before={p.relative_to(dest).as_posix():p.read_bytes()for p in dest.rglob('*')if p.is_file()}
        self.assertEqual(e.validate_completed(dest),checked)
        self.assertEqual(before,{p.relative_to(dest).as_posix():p.read_bytes()for p in dest.rglob('*')if p.is_file()})

    def test_boolean_rc_bad_guard_or_capture_never_creates_completed_ledger(self):
        for i,change in enumerate((lambda o:o.update(returncode=False),lambda o:o['guard_scope'].update(proof_acceptance=True),
                                   lambda o:o.update(checkpoints=[]),lambda o:o.update(stderr_sha256='0'*64))):
            def fake(*a,**k):
                out=self.fake(*a,**k);change(out);put(Path(k['output_dir'])/'supervisor-result.json',out);return out
            with self.assertRaises(ValueError):self.complete('bad'+str(i),fake)
            self.assertFalse((self.root/('bad'+str(i))/'STAGE_COMPLETED.json').exists())

    def test_false_readback_status_missing_controls_and_false_complete_scope_rejected(self):
        task,_=self.complete();observed=s.read(task/'STAGE_OBSERVED.json')
        for field,value in(('full_notebook57_completed',True),('resource_to_count147_interfaces_verified',True)):
            packet=copy.deepcopy(observed);packet[field]=value
            with self.assertRaises(ValueError):e.validate_run(task,packet)
        p=task/'capsule'/s.RESULT;d=s.read(p);d['negative_controls']=0;put(p,d)
        with self.assertRaises(ValueError):e.validate_completed(task)

    def test_coherently_captured_failed_native_results_never_complete(self):
        self.native_mutator=lambda p:p.update(status='EXACT_HIGHRHO14_19_NOT_CLOSED')
        with self.assertRaises(ValueError):self.complete('native-not-closed')
        self.assertTrue((self.root/'native-not-closed/STAGE_OBSERVED.json').exists())
        self.assertFalse((self.root/'native-not-closed/STAGE_COMPLETED.json').exists())

    def test_rehashed_wrong_discovery_thread_context_is_rejected(self):
        task,_=self.complete();report=s.read(task/'STAGE_OBSERVED.json')
        bad=copy.deepcopy(self.context);bad['thread_environment']['OPENBLAS_NUM_THREADS']='64'
        put(task/'DISCOVERY_CONTEXT.json',bad);report['discovery_context']=bad
        with self.assertRaises(ValueError):e.validate_run(task,report)

    def test_complete_cache_roundtrip_requires_actual_sha_and_skips_all_native_calls(self):
        task,checked=self.complete();cache=self.root/'saved';export=r.save_completed(task,cache)
        with patch.object(r.linux_supervisor,'run',side_effect=AssertionError('No partial cache replay'))as native:
            restored=r.restore_completed(cache,self.root/'restore',root=self.root)
        self.assertEqual(restored[1],checked);native.assert_not_called()
        Path(export['path']).with_suffix('.zip.sha256').write_bytes(b'bad')
        self.assertIsNone(r.restore_completed(cache,self.root/'bad-cache',root=self.root))

    def test_missing_actions_and_unsafe_zip_members_are_rejected_before_extraction(self):
        z=Mock();z.infolist.return_value=[zipfile.ZipInfo('SOURCES.json')]
        with self.assertRaises(ValueError):r.cache_members(z)
        for name in('../escape','/absolute','a//b','a\\b'):
            info=zipfile.ZipInfo();info.filename=info.orig_filename=name;z.infolist.return_value=[info]
            with self.assertRaises(ValueError):r.cache_members(z)

    def test_missing_numpy_or_native_failure_still_exports_false_final_bundle(self):
        with (patch.object(r,'restore_completed',return_value=None),patch.object(r,'numpy_context',side_effect=ValueError('Missing NumPy')),
              patch.object(s,'obtain_assets')as download):
            out=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'work')
        self.assertFalse(out['status']['conditional_highrho_arithmetic_completed']);self.assertTrue(Path(out['bundle']).is_file());download.assert_not_called()

    def test_second_run_reuses_only_full_transaction_without_download(self):
        task,checked=self.complete();cache=self.root/'drive/finite1519-highrho/completed'/s.PLAN_SHA256[:16];r.save_completed(task,cache)
        with patch.object(r.linux_supervisor,'run')as native,patch.object(s,'obtain_assets')as download:
            out=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'work')
        self.assertTrue(out['status']['conditional_highrho_arithmetic_completed']);self.assertTrue(out['status']['reused_complete_transaction'])
        native.assert_not_called();download.assert_not_called()


class SourcePlan(unittest.TestCase):
    def test_actual73_file_plan_keeps_original70_manifest_and_all_programs(self):
        d=s.plan();self.assertEqual(len(d['source_files']),73);self.assertEqual(d['original_manifest_graph_rows'],70)
        self.assertTrue(d['source_programs_unchanged']);self.assertTrue(d['source_manifests_unchanged'])
        self.assertEqual(sum(x['bytes']for x in d['source_files'].values()),500147)
        self.assertEqual({a['name']for a in d['assets']},{'cutoff5_10_15.zip', 'cutoff5_20261020.zip'})

    def test_discovery_resource_context_forces_and_records_one_thread_without_numpy_import(self):
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory()as directory:
            p=Path(directory)/'numpy/__init__.py';p.parent.mkdir();p.write_bytes(b'raise AssertionError("Do not import fake NumPy")\n')
            distribution=SimpleNamespace(version='synthetic',locate_file=lambda name:Path(directory)/name)
            with patch('importlib.metadata.distribution',return_value=distribution),patch.dict(r.os.environ,{'OPENBLAS_NUM_THREADS':'64'}):
                context=r.numpy_context()
                self.assertEqual(context['thread_environment'],{n:'1'for n in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')})
                self.assertEqual(r.os.environ['OPENBLAS_NUM_THREADS'],'1')
                self.assertFalse(context['acceptance_arithmetic_depends_on_numpy'])


if __name__=='__main__':unittest.main()
