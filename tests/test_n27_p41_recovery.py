"""Synthetic source/geometry/process/cache fixtures; never execute original math."""
from __future__ import annotations
import copy
import io
import json
from pathlib import Path
import shutil
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from be_replay import n27_p41_recovery as run,n27_p41_recovery_sources as src,n27_p41_recovery_evidence as ev


def raw(p):return (json.dumps(p,indent=2)+'\n').encode()
def put(p,d):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw(d));return src.digest(p)


class Recovery(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        folder=self.root/'fixture';folder.mkdir();pins={}
        for i in range(39):
            name=f'kernel{i}.py';(folder/name).write_bytes(b'raise AssertionError("NEVER IMPORT ORIGINAL NUMERICAL CODE")\n');pins[name]=src.digest(folder/name)
        put(folder/'KERNEL_COPY_MANIFEST.json',dict(files=pins))
        self.cfg=dict(n=27,index=41,K='0',p=['41/100','21/50'],rho_lower='1',rho_upper='11/10',Lambda='1/4',d0='1/16')
        put(folder/'contract.json',dict(rows=[self.cfg]))
        for name in('count_protocol.py','construct_alpha4.py'):(folder/name).write_bytes(b'raise AssertionError("NUMERICAL TRAP MUST NEVER RUN")\n')
        self.archive=self.root/'source.zip'
        with zipfile.ZipFile(self.archive,'w')as z:
            for p in folder.iterdir():z.write(p,'original/'+p.name)
            z.writestr('original/COUNT41_ACCEPTED.json',b'oldPASSisNEVERaninput')
        self.plan=dict(archive=dict(name=self.archive.name,bytes=self.archive.stat().st_size,sha256=src.digest(self.archive)),
            source_files={p.name:dict(member='original/'+p.name,bytes=p.stat().st_size,sha256=src.digest(p))for p in folder.iterdir()},
            historical_selected_forest=dict(sha256='6'*64),historical_selected_acceptance=dict(sha256='a'*64))
        for obj,name,value in((src,'plan',self.plan),(run.sys,'platform','linux'),(run.sys,'stdout',io.StringIO())):
            p=patch.object(obj,name,return_value=value)if name=='plan'else patch.object(obj,name,value)
            p.start();self.addCleanup(p.stop)

    def fake_supervisor(self,argv, *,cwd,output_dir,**kwargs):
        capsule=Path(cwd);action='construct'if Path(argv[3]).name=='construct_alpha4.py'else'accept'
        if action=='construct':
            b=[self.cfg['p'],['0','1/4'],['0','1'],['-1/2','1/2'],['0','1/16']]
            def leaf(box):return dict(kind='leaf',box=copy.deepcopy(box),decision='PASS_TARGET',result=dict(status='PASS',score_upper='1/4'))
            roots=[dict(k=k,tree=leaf(b))for k in range(28)]
            left=copy.deepcopy(b);right=copy.deepcopy(b);left[2][1]='1/2';right[2][0]='1/2'
            roots[0]['tree']=dict(kind='split',axis=2,cut='1/2',left=leaf(left),right=leaf(right))
            forest=dict(schema='ACTUAL27_FLOOR25_B0_P41_CLOSED_COUNT_FOREST_V1',n=27,index=41,target=ev.TARGET,
                contract_sha256=src.digest(capsule/'contract.json'),kernel_sha256=src.read(capsule/'KERNEL_COPY_MANIFEST.json')['files'],
                checker_sha256=src.digest(capsule/'count_protocol.py'),roots=roots)
            put(capsule/'COUNT41_FOREST.json',forest)
            answer=dict(scope=ev.CONSTRUCTION_SCOPE,status='STORED_CONDITIONAL_FOREST_CONSTRUCTED_NOT_ACCEPTED',
                contract_sha256=src.digest(capsule/'contract.json'),fixed_acceptor_sha256=src.digest(capsule/'count_protocol.py'),
                constructor_sha256=src.digest(capsule/'construct_alpha4.py'),forest_sha256=src.digest(capsule/'COUNT41_FOREST.json'),
                visited=30,seconds=.25)
            put(capsule/'CONSTRUCTION_RUN.json',answer)
        else:
            c=ev.forest_census(capsule)
            answer=dict(status='PASS_FRESH_CONDITIONAL_ACTUAL27_EXACT_COUNT41',n=27,index=41,
                forest_sha256=src.digest(capsule/'COUNT41_FOREST.json'),contract_sha256=src.digest(capsule/'contract.json'),
                checker_sha256=src.digest(capsule/'count_protocol.py'),kernel_sha256=src.read(capsule/'KERNEL_COPY_MANIFEST.json')['files'],
                statistics={k:c[k]for k in('nodes','leaves','closed_statuses','maximum_score','maximum_depth')},
                negative_controls=ev.CONTROLS,fresh_leaf_evaluations=c['leaves'],seconds=.5,scope=ev.ACCEPT_SCOPE)
            put(capsule/'COUNT41_ACCEPTED.json',answer)
        output_dir=Path(output_dir);output_dir.mkdir(parents=True);(output_dir/'stdout.txt').write_bytes(raw(answer));(output_dir/'stderr.txt').write_bytes(b'')
        kwargs['checkpoint_paths']=[str(Path(p).resolve())for p in kwargs['checkpoint_paths']]
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,**kwargs)
        launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds'])
        put(output_dir/'launch.json',launch);caps=[]
        for name in ev.ACTIONS[action][2]:
            native=capsule/name;copied=output_dir/'checkpoints'/name;copied.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(native,copied)
            caps.append(dict(source_path=str(native),exists=True,trusted_certificate=False,path=str(copied),bytes=native.stat().st_size,sha256=src.digest(native)))
        scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(ev.WALL_SECONDS),
            per_process_RLIMIT_AS_bytes=ev.MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=ev.CPU_SECONDS,
            aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=ev.MEMORY_BYTES,
            sampled_group_CPU_limit_seconds=ev.CPU_SECONDS,sampled_file_limit_bytes=256*src.MIB,sampled_log_limit_bytes=16*src.MIB,
            descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
        o=dict(status='completed',reason=None,returncode=0,mode='untrusted_search',proof_accepted=False,sample_count=1,
            elapsed_seconds=.75,maximum_sampled_group_CPU_seconds=.5,maximum_sampled_group_RSS_bytes=src.MIB,
            guard_scope=scope,checkpoints=caps,**{k+suffix:value for k in('stdout','stderr')for suffix,value in
             (('_path',str(output_dir/(k+'.txt'))),('_sha256',src.digest(output_dir/(k+'.txt'))))})
        put(output_dir/'supervisor-result.json',o);return o

    def complete(self,name='task',effect=None):
        task=self.root/name
        with patch.object(run.linux_supervisor,'run',side_effect=effect or self.fake_supervisor)as execute:
            result=run.execute(task,self.archive)
        self.assertEqual(execute.call_count,2);return task,result

    def recapture(self,output_dir,o, *,packet=None):
        output_dir=Path(output_dir);capsule=output_dir.parent.parent/'capsule'
        if packet is not None:(output_dir/'stdout.txt').write_bytes(raw(packet));o['stdout_sha256']=src.digest(output_dir/'stdout.txt')
        for c in o['checkpoints']:
            native=capsule/Path(c['source_path']).name;shutil.copyfile(native,c['path']);c.update(bytes=native.stat().st_size,sha256=src.digest(native))
        put(output_dir/'supervisor-result.json',o);return o

    def test_complete_original_pair_has_new_evidence_and_all_false_global_flags(self):
        task,result=self.complete();self.assertEqual(result['summary']['census']['roots'],28)
        self.assertEqual(result['summary']['census']['nodes'],30)
        self.assertNotEqual(result['summary']['candidate_sha256'],self.plan['historical_selected_forest']['sha256'])
        self.assertEqual(src.read(task/'capsule/COUNT41_ACCEPTED.json')['negative_controls'],ev.CONTROLS)
        for f in ev.FLAGS:self.assertIs(result[f],False)

    def test_exact_original64_pair_restores_byte_preserving_without_native_calls(self):
        task,_=self.complete()
        for name in('CONSTRUCT_OBSERVED.json','ACCEPT_OBSERVED.json'):
            packet=src.read(task/name);packet['implementation']=copy.deepcopy(ev.ORIGINAL64_IMPLEMENTATION);put(task/name,packet)
        packet=src.read(task/'COMPLETED.json');packet['implementation']=copy.deepcopy(ev.ORIGINAL64_IMPLEMENTATION)
        packet['artifacts']=ev.inventory(task);put(task/'COMPLETED.json',packet)
        checked=ev.validate_completed(task);before={n:(task/n).read_bytes()for n in('CONSTRUCT_OBSERVED.json','ACCEPT_OBSERVED.json','COMPLETED.json')}
        cache=self.root/'old64cache';run.save_completed(task,cache)
        with patch.object(run.linux_supervisor,'run',side_effect=AssertionError('No original numerical rerun')):
            restored=run.restore_completed(cache,self.root/'old64restored')
        self.assertIsNotNone(restored);self.assertEqual(restored[1],checked)
        for name,content in before.items():self.assertEqual((restored[0]/name).read_bytes(),content)

    def test_original64_whitelist_rejects_hash_mixing_and_pair_epoch_mismatch(self):
        old=copy.deepcopy(ev.ORIGINAL64_IMPLEMENTATION)
        self.assertTrue(ev.known_implementation(old))
        for key in old:
            missing=copy.deepcopy(old);missing.pop(key);self.assertFalse(ev.known_implementation(missing))
        mixed=copy.deepcopy(old);mixed['n27_p41_recovery_evidence.py']=ev.implementation()['n27_p41_recovery_evidence.py']
        self.assertFalse(ev.known_implementation(mixed))
        extra=copy.deepcopy(old);extra['extra']='0'*64;self.assertFalse(ev.known_implementation(extra))
        task,_=self.complete();record=src.read(task/'ACCEPT_OBSERVED.json')
        record['implementation']=old;put(task/'ACCEPT_OBSERVED.json',record)
        with self.assertRaisesRegex(ValueError,'same whole implementation epoch'):ev.validate_pair(task)

    def test_source_capsule_excludes_old_acceptance_and_seals_every_source(self):
        task=self.root/'prepared';src.prepare(self.archive,task)
        self.assertFalse((task/'capsule/COUNT41_ACCEPTED.json').exists())
        (task/'capsule/kernel0.py').write_bytes(b'changed')
        with self.assertRaises(ValueError):src.verify_task(task)

    def test_unbound_helper_or_directory_fails(self):
        for name in('extra.py','extra-dir'):
            task=self.root/name;src.prepare(self.archive,task);p=task/'capsule'/name
            p.mkdir()if name.endswith('dir')else p.write_bytes(b'pass')
            with self.assertRaises(ValueError):src.verify_task(task)

    def test_bad_transport_fails_before_any_output(self):
        self.archive.write_bytes(self.archive.read_bytes()+b'changed')
        with self.assertRaises(ValueError):src.prepare(self.archive,self.root/'absent')
        self.assertFalse((self.root/'absent').exists())

    def test_constructor_zero_exit_and_complete_forest_do_not_override_incomplete_packet(self):
        def bad(*a,**kw):
            o=self.fake_supervisor(*a,**kw);p=Path(kw['cwd'])/'CONSTRUCTION_RUN.json';packet=src.read(p)
            packet['status']='BOUNDED_CONSTRUCTION_NOT_COMPLETE';packet['error']='finite count construction budget';put(p,packet)
            return self.recapture(kw['output_dir'],o,packet=packet)
        with patch.object(run.linux_supervisor,'run',side_effect=bad)as execute,self.assertRaises(ValueError):run.execute(self.root/'bad',self.archive)
        self.assertEqual(execute.call_count,1)
        self.assertFalse((self.root/'bad/capsule/COUNT41_ACCEPTED.json').exists())

    def test_original_caught_budget_failure_is_exported_with_actual_stderr(self):
        def failed(*a,**kw):
            o=self.fake_supervisor(*a,**kw);p=Path(kw['cwd'])/'CONSTRUCTION_RUN.json';v=src.read(p)
            v['status']='BOUNDED_CONSTRUCTION_NOT_COMPLETE';v['error']='finite count construction budget';put(p,v)
            d=Path(kw['output_dir']);(d/'stderr.txt').write_bytes(b'ValueError: finite count construction budget\n')
            o['stderr_sha256']=src.digest(d/'stderr.txt');return self.recapture(d,o,packet=v)
        with patch.object(src,'obtain_archive',return_value=self.archive),patch.object(run,'LogBackups'),\
                patch.object(run.linux_supervisor,'run',side_effect=failed)as execute:
            result=run.run_colab(durable_root=self.root/'durable',work_root=self.root/'runs')
        self.assertEqual(execute.call_count,1);self.assertIn('finite count construction budget',result['status']['error'])
        self.assertTrue(Path(result['bundle']).is_file());self.assertFalse(result['status']['conditional_arithmetic_completed'])

    def test_launch_context_guard_boolean_exit_and_capture_mutations_fail(self):
        for i,kind in enumerate(('cwd','guard','rc','hash','capture')):
            def bad(*a,**kw):
                o=self.fake_supervisor(*a,**kw);d=Path(kw['output_dir'])
                if kind=='cwd':p=d/'launch.json';v=src.read(p);v['cwd']=str(self.root);put(p,v)
                if kind=='guard':o['guard_scope']['aggregate_kernel_memory_limit']=True
                if kind=='rc':o['returncode']=False
                if kind=='hash':o['stderr_sha256']='0'*64
                if kind=='capture':o['checkpoints'][0]['trusted_certificate']=True
                put(d/'supervisor-result.json',o);return o
            with self.subTest(kind=kind),self.assertRaises(ValueError):self.complete('bad'+str(i),bad)

    def test_all_geometry_header_and_root_coverage_remain_mandatory(self):
        task,_=self.complete();p=task/'capsule/COUNT41_FOREST.json';base=src.read(p)
        mutations=[lambda x:x.update(n=True),lambda x:x.update(target='1/2'),lambda x:x['roots'].pop(),
            lambda x:x['roots'][0].update(k=False),lambda x:x['roots'][0]['tree'].update(axis=True),
            lambda x:x['roots'][0]['tree'].update(cut='1'),lambda x:x['roots'][1]['tree']['box'][0].__setitem__(0,'0'),
            lambda x:x['roots'][1]['tree'].update(extra=True)]
        for mutate in mutations:
            packet=copy.deepcopy(base);mutate(packet);put(p,packet)
            with self.assertRaises(ValueError):ev.forest_census(task/'capsule')
        put(p,base)

    def test_acceptor_control_or_leaf_counter_change_fails_even_when_recaptured(self):
        for i,key in enumerate(('negative_controls','fresh_leaf_evaluations')):
            def bad(*a,**kw):
                o=self.fake_supervisor(*a,**kw)
                if Path(a[0][3]).name=='count_protocol.py':
                    p=Path(kw['cwd'])/'COUNT41_ACCEPTED.json';v=src.read(p);v[key]=[]if key=='negative_controls'else 1;put(p,v)
                    self.recapture(kw['output_dir'],o,packet=v)
                return o
            with self.subTest(key=key),self.assertRaises(ValueError):self.complete('accept'+str(i),bad)

    def test_constructor_forest_cannot_change_between_actions(self):
        def bad(*a,**kw):
            if Path(a[0][3]).name=='count_protocol.py':
                p=Path(kw['cwd'])/'COUNT41_FOREST.json';v=src.read(p);v['roots'][1]['tree']['result']['extra']='changed';put(p,v)
            return self.fake_supervisor(*a,**kw)
        with self.assertRaises(ValueError):self.complete(effect=bad)

    def test_relocated_pair_preserves_original_bytes_and_exact_evidence(self):
        task,result=self.complete();restored=self.root/'relocated';shutil.copytree(task,restored)
        before={p.relative_to(restored).as_posix():p.read_bytes()for p in restored.rglob('*')if p.is_file()}
        self.assertEqual(ev.validate_completed(restored),result)
        self.assertEqual(before,{p.relative_to(restored).as_posix():p.read_bytes()for p in restored.rglob('*')if p.is_file()})

    def test_complete_pair_cache_roundtrip_and_bad_cache_rejection(self):
        task,result=self.complete();cache=self.root/'cache';run.save_completed(task,cache)
        restored=run.restore_completed(cache,self.root/'restored');self.assertEqual(restored[1],result)
        p=cache/'zz-complete.zip';p.write_bytes(b'notzip');p.with_suffix('.zip.sha256').write_text(src.digest(p)+'  '+p.name+'\n')
        self.assertEqual(run.restore_completed(cache,self.root/'again')[1],result)

    def test_cache_traversal_case_collision_and_link_rejected_before_extraction(self):
        for name,mode in(('../escape',0),('SOURCES.JSON',0),('link',stat.S_IFLNK<<16)):
            rows=[zipfile.ZipInfo(n)for n in('SOURCES.json','CONSTRUCT_OBSERVED.json','ACCEPT_OBSERVED.json','COMPLETED.json',
                'capsule/CONSTRUCTION_RUN.json','capsule/COUNT41_FOREST.json','capsule/COUNT41_ACCEPTED.json')]
            item=zipfile.ZipInfo(name);item.external_attr=mode;rows.append(item)
            class Fake:
                def infolist(self):return rows
            with self.subTest(name=name),self.assertRaises(ValueError):run.cache_members(Fake())

    def test_run_all_reuses_only_complete_two_action_pair(self):
        opts=dict(durable_root=self.root/'durable',work_root=self.root/'runs')
        with patch.object(src,'obtain_archive',return_value=self.archive),patch.object(run,'LogBackups'),\
                patch.object(run.linux_supervisor,'run',side_effect=self.fake_supervisor)as execute:
            first=run.run_colab(**opts)
        self.assertEqual(execute.call_count,2);self.assertTrue(first['status']['conditional_arithmetic_completed'])
        with patch.object(src,'obtain_archive',side_effect=AssertionError('No download for validated pair')),patch.object(run,'LogBackups'),\
                patch.object(run.linux_supervisor,'run',side_effect=AssertionError('No duplicate numerical call')):
            second=run.run_colab(**opts)
        self.assertTrue(second['status']['reused_completed_pair']);self.assertTrue(Path(second['bundle']).is_file())
        for f in ev.FLAGS:self.assertIs(second['status'][f],False)

    def test_failure_exports_bundle_without_promoting_any_flag(self):
        with patch.object(src,'obtain_archive',side_effect=ValueError('Synthetic missing source')),patch.object(run,'LogBackups'):
            result=run.run_colab(durable_root=self.root/'durable',work_root=self.root/'runs')
        self.assertFalse(result['status']['conditional_arithmetic_completed']);self.assertTrue(Path(result['bundle']).is_file())
        for f in ev.FLAGS:self.assertIs(result['status'][f],False)


if __name__=='__main__':unittest.main()
