"""Three-action transport fixtures with trap sources; no original numerical imports."""
from pathlib import Path
import copy
import io
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch,Mock
import zipfile
from be_replay import finite1014_high_sources as s,finite1014_high_evidence as e,finite1014_high as r


def put(p,value):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.dump(value));return s.digest(p)


class High(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=s.ROOT.parent,prefix='t56e-');self.root=Path(self.temp.name)
        self.assertTrue(self.root.resolve().is_relative_to(s.ROOT.parent.resolve()));self.addCleanup(self.temp.cleanup)
        self.cache=self.root/'input';self.native=self.cache/s.NATIVE;self.audit=self.cache/s.AUDIT
        self.native.mkdir(parents=True);self.audit.mkdir(parents=True)
        for p in [self.native/n for n in s.ENGINE_NAMES]+[self.audit/'check.py']:
            p.write_bytes(b'raise AssertionError("Never execute or import original mathematics locally")\n')
        (self.audit/'REVIEW.txt').write_bytes(b'Synthetic infrastructure only\n')
        pins={p.relative_to(self.cache).as_posix():s.digest(p)for p in self.native.iterdir()}
        manifest=put(self.native/'MANIFEST.json',dict(files_sha256=pins,scope='SYNTHETIC'))
        files={p.relative_to(self.cache).as_posix():dict(bytes=p.stat().st_size,sha256=s.digest(p))for p in self.cache.rglob('*')if p.is_file()}
        self.bands=[dict(name='B0',rho_upper='11/10',support_radius='23/10',target='69/200'),
                    dict(name='BN',rho_upper='23/20',support_radius='12/5',target='93/250')]
        self.plan=dict(source_files=files,original_manifest_sha256=manifest,bands=self.bands)
        for target,name,value in((s,'plan',self.plan),(r.sys,'platform','linux')):
            p=patch.object(target,name,return_value=value)if name=='plan'else patch.object(target,name,value)
            p.start();self.addCleanup(p.stop)
        p=patch.object(r.sys,'stdout',io.StringIO());p.start();self.addCleanup(p.stop)

    def fake(self,argv, *,cwd,output_dir,**kw):
        d=Path(output_dir);action=d.name;task=d.parent.parent;c=task/'capsule'
        if action!='readback':
            packet=dict(status=e.NATIVE_STATUS,n=list(range(10,15)),pi={'synthetic':True},
                        manifest_sha256=s.digest(c/s.NATIVE/'MANIFEST.json'),scope='SYNTHETIC UNATTESTED')
            packet['attempts']=[dict(name=b['name'],rho_upper=b['rho_upper'],support_radius=b['support_radius'],
                mesh=mesh,all_cells=mesh,rows=[dict(n=n)for n in range(10,15)])for b in self.bands for mesh in(512,1024)]
            if hasattr(self,'native_mutator'):self.native_mutator(packet,action)
            put(c/s.NATIVE/s.OUTPUT_NAMES[action],packet);stdout=e.NATIVE_STATUS+'\n'
        else:
            for n in s.ENGINE_NAMES:
                dest=c/s.AUDIT/'engine'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(c/s.NATIVE/n,dest)
            graph=dict(s.read(c/s.NATIVE/'MANIFEST.json')['files_sha256'])
            names=[s.NATIVE+'/MANIFEST.json',s.NATIVE+'/RESULT.json',s.NATIVE+'/REPLAY_RESULT.json',s.AUDIT+'/check.py',s.AUDIT+'/REVIEW.txt']
            names += [s.AUDIT+'/engine/'+n for n in s.ENGINE_NAMES]+[n for a in('construct','replay')for n in s.capture_paths(a)]
            for n in names:graph[n]=s.digest(c/n)
            packet=dict(status=e.READBACK_STATUS,mathematical_status='SYNTHETIC',execution_status='SYNTHETIC',n=list(range(10,15)),
                rows=[dict(band=b['name'],n=n,rho_upper=b['rho_upper'],support_radius=b['support_radius'],upper='1/5',target=b['target'])for b in self.bands for n in range(10,15)],
                counts=dict(e.COUNTS),independent_closed_cells=64,cell_tests=[['synthetic',i]for i in range(64)],
                complete_native_rows=20,selected_fixed_target_rows=10,full_integrations_in_this_readback=0,
                actual_support_acquired=False,physical_D_seed_used=False,cutoff10_claimed=False,files_sha256=graph)
            if hasattr(self,'readback_mutator'):self.readback_mutator(packet)
            put(c/s.RESULT,packet);stdout=json.dumps({k:v for k,v in packet.items()if k not in('files_sha256','cell_tests','rows')})+'\n'
        d.mkdir(parents=True);(d/'stdout.txt').write_bytes(stdout.encode());(d/'stderr.txt').write_bytes(b'')
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(d),sample_seconds=.2,**kw)
        launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds'])
        launch['checkpoint_paths']=[str(p)for p in launch['checkpoint_paths']];put(d/'launch.json',launch)
        # Use the deployed pure transport copier: its layout is relative to cwd,
        # never relative to the outer capsule. No child or mathematical code runs.
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

    def test_complete_three_commands_truthful_bridge_and_false_full_scope(self):
        task,checked=self.complete();self.assertTrue(checked['conditional_supported_high_arithmetic_completed'])
        for f in e.FLAGS:self.assertIs(checked[f],False)
        report=s.read(task/'STAGE_OBSERVED.json');self.assertEqual([x['action']for x in report['actions']],list(s.ACTIONS))
        meta=s.read(task/'capsule'/s.RUNS/s.LABELS['construct']/'metadata.json')
        self.assertEqual(meta['input_sha256'],s.native_input_map(s.read(task/'SOURCES.json')))
        self.assertEqual(meta['command'][1:],['-B','bound.py','RESULT.json'])
        self.assertEqual(meta['capture_bridge']['schema'],e.BRIDGE)
        self.assertEqual(checked['summary']['complete_native_rows'],20);self.assertEqual(len(checked['summary']['rows']),10)

    def test_relocated_cache_preserves_every_recorded_byte(self):
        task,checked=self.complete();dest=self.root/'moved';shutil.copytree(task,dest)
        before={p.relative_to(dest).as_posix():p.read_bytes()for p in dest.rglob('*')if p.is_file()}
        self.assertEqual(e.validate_completed(dest),checked)
        self.assertEqual(before,{p.relative_to(dest).as_posix():p.read_bytes()for p in dest.rglob('*')if p.is_file()})

    def test_actual_supervisor_checkpoint_layout_is_action_cwd_relative(self):
        task,_=self.complete()
        for action in s.ACTIONS:
            d=task/'executions'/action
            cwd=task/'capsule'/(s.AUDIT if action=='readback'else s.NATIVE)
            observed=s.read(d/'supervisor-result.json')
            expected=[d/'checkpoints'/(task/'capsule'/n).relative_to(cwd)for n in s.output_paths(action)]
            self.assertEqual([Path(p['path'])for p in observed['checkpoints']],expected)
            self.assertTrue(all(p.is_file()for p in expected))
        self.assertTrue((task/'executions/construct/checkpoints/RESULT.json').is_file())
        self.assertTrue((task/'executions/readback/checkpoints/engine/kernel.py').is_file())
        self.assertFalse((task/'executions/construct/checkpoints/work').exists())

    def test_false_rc_guard_checkpoint_and_changed_stdout_are_rejected(self):
        for i,mutate in enumerate((lambda p:p.update(returncode=False),lambda p:p['guard_scope'].update(proof_acceptance=True),
                                   lambda p:p.update(checkpoints=[]),lambda p:p.update(stdout_sha256='0'*64))):
            def effect(*a,**k):
                p=self.fake(*a,**k);mutate(p);put(Path(k['output_dir'])/'supervisor-result.json',p);return p
            with self.assertRaises(ValueError):self.complete('bad'+str(i),effect)
            self.assertFalse((self.root/('bad'+str(i))/'STAGE_COMPLETED.json').exists())

    def test_changed_current_capture_launch_source_graph_or_bridge_never_validates(self):
        task,_=self.complete();path=task/'capsule'/s.RUNS/s.LABELS['construct']/'metadata.json';raw=path.read_bytes()
        for mutate in(lambda p:p.update(cwd=str(task)),lambda p:p['command'].append('foreign'),
                      lambda p:p['input_sha256'].pop(next(iter(p['input_sha256']))),
                      lambda p:p['capture_bridge'].update(outer_supervisor_result_sha256='0'*64)):
            p=json.loads(raw);mutate(p);put(path,p)
            with self.assertRaises(ValueError):e.validate_completed(task)
        path.write_bytes(raw)
        launch=task/'executions/replay/launch.json';p=s.read(launch);p['cwd']=str(task);put(launch,p)
        with self.assertRaises(ValueError):e.validate_completed(task)

    def test_failed_native_status_changed_mesh_or_missing_index_cannot_complete(self):
        for i,mutate in enumerate((lambda p:p.update(status='INCOMPLETE'),lambda p:p['attempts'][1].update(mesh=512),
                                   lambda p:p['attempts'][0]['rows'].pop())):
            self.native_mutator=lambda p,a:mutate(p)
            with self.assertRaises(ValueError):self.complete('native'+str(i))
            self.assertFalse((self.root/('native'+str(i))/'STAGE_COMPLETED.json').exists())

    def test_complete_native_objects_must_match_as_bytes(self):
        self.native_mutator=lambda p,a:p.update(scope='SYNTHETIC '+a)
        with self.assertRaises(ValueError):self.complete('unequal')

    def test_zero_return_code_without_original_success_terminal_is_incomplete(self):
        def effect(*a,**k):
            p=self.fake(*a,**k)
            if Path(k['output_dir']).name=='construct':
                d=Path(k['output_dir']);(d/'stdout.txt').write_bytes(b'INCOMPLETE\n')
                p['stdout_sha256']=s.digest(d/'stdout.txt');put(d/'supervisor-result.json',p)
            return p
        with self.assertRaises(ValueError):self.complete('wrong-terminal',effect)
        self.assertFalse((self.root/'wrong-terminal/STAGE_COMPLETED.json').exists())

    def test_readback_controls_both_radii_all_rows_and_no_promotions(self):
        for i,mutate in enumerate((lambda p:p['counts'].update(result_negative_controls=21),
                                   lambda p:p['rows'][0].update(support_radius='3'),lambda p:p['rows'].pop(),
                                   lambda p:p.update(actual_support_acquired=True))):
            self.readback_mutator=mutate
            with self.assertRaises(ValueError):self.complete('readback'+str(i))
            self.assertFalse((self.root/('readback'+str(i))/'STAGE_COMPLETED.json').exists())

    def test_modified_sources_or_unbound_imports_are_rejected(self):
        task=self.root/'sealed';s.prepare(self.cache,task);p=task/'capsule'/s.NATIVE/'foreign.py';p.write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify_job(task)
        p.unlink();(task/'capsule'/s.NATIVE/'bound.py').write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify_job(task)

    def test_complete_cache_requires_real_sidecar_and_skips_every_native_call(self):
        task,checked=self.complete();cache=self.root/'saved';saved=r.save_completed(task,cache)
        with patch.object(r.linux_supervisor,'run',side_effect=AssertionError('No fresh mathematics'))as native:
            loaded=r.restore_completed(cache,self.root/'restore',root=self.root)
        self.assertEqual(loaded[1],checked);native.assert_not_called()
        Path(saved['path']).with_suffix('.zip.sha256').write_bytes(b'bad')
        self.assertIsNone(r.restore_completed(cache,self.root/'badrestore',root=self.root))

    def test_unsafe_or_partial_zip_is_rejected_before_extraction(self):
        z=Mock()
        for name in('SOURCES.json','../escape','/absolute','a//b','a\\b'):
            info=zipfile.ZipInfo();info.filename=info.orig_filename=name;z.infolist.return_value=[info]
            with self.assertRaises(ValueError):r.cache_members(z)

    def test_failure_still_exports_false_session(self):
        with patch.object(r,'restore_completed',return_value=None),patch.object(s,'obtain_assets',side_effect=ValueError('Synthetic missing asset')):
            result=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'runs')
        self.assertFalse(result['status']['conditional_supported_high_arithmetic_completed']);self.assertTrue(Path(result['bundle']).is_file())


class SourcePlan(unittest.TestCase):
    def test_actual98_input95_manifest_plan_has_no_historical_selected_results(self):
        d=s.plan();self.assertEqual(len(d['source_files']),98);self.assertEqual(sum(v['bytes']for v in d['source_files'].values()),670997)
        self.assertEqual(d['original_manifest_graph_rows'],95)
        self.assertEqual(d['original_manifest_sha256'],'93f6a628a1c78cd6e23c2daaf5197808bda40787f2ee2141e6b94089a2241be0')
        for a in s.ACTIONS:
            for n in s.generated_paths(a):self.assertNotIn(n,d['source_files'])


if __name__=='__main__':unittest.main()
