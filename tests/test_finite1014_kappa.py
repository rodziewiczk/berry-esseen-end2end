"""Synthetic infrastructure fixtures; no original scalar module is executed."""
from __future__ import annotations
import copy
import io
import json
from pathlib import Path
import shutil
import stat
import tempfile
import unittest
from unittest.mock import Mock,patch
import zipfile
from be_replay import finite1014_kappa_sources as s,finite1014_kappa_evidence as e,finite1014_kappa as r


def put(p,packet):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.dump(packet));return s.digest(p)


class Kappa(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=s.ROOT.parent,prefix='t56k-');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.assertTrue(self.root.resolve().is_relative_to(s.ROOT.parent.resolve()))
        for target,name,value in((r.sys,'platform','linux'),(r.sys,'stdout',io.StringIO())):
            p=patch.object(target,name,value);p.start();self.addCleanup(p.stop)

    def fake(self,argv,*,cwd,output_dir,**kw):
        # Fabricated data tests transport only. It is NOT a valid scalar proof.
        task=Path(cwd).parent;request=s.read(task/'SOURCES.json');capsule=Path(cwd);directory=Path(output_dir)
        cert=dict(version='KAPPA_62_625_SCALAR_V1',kappa='62/625',upper='625/124',degree=13,
            coefficients=e.COEFFICIENTS,
            cells=[dict(interval=[str(e.F(i,16)),str(e.F(i+1,16))]if i<80 else['5','625/124'],bernstein=['1']*14)for i in range(81)],
            splice=dict(cosine_deficit=['1','2'],sine_lower='-1',scale_A=['1/2','1'],join_numerator_lower='1',pi_bracket=['3','4']))
        if hasattr(self,'certificate_mutator'):self.certificate_mutator(cert)
        put(capsule/'CERTIFICATE.json',cert)
        checked=dict(status=e.STATUS,mathematical_status=e.MATHEMATICAL_STATUS,
            receipt=dict(cells=81,positive_coefficients=1134,minimum_bernstein='1'),negative_controls=21,additional_identity_checks=324,
            source_sha256={e.original(request,'capsule/'+n):s.digest(capsule/n)for n in s.FILES+('CERTIFICATE.json',)})
        if hasattr(self,'receipt_mutator'):self.receipt_mutator(checked)
        put(capsule/'CHECKED.json',checked);directory.mkdir(parents=True)
        (directory/'stdout.txt').write_bytes(s.dump(checked));(directory/'stderr.txt').write_bytes(b'')
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,**kw)
        launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds'])
        launch['checkpoint_paths']=[str(p)for p in kw['checkpoint_paths']]
        if hasattr(self,'launch_mutator'):self.launch_mutator(launch)
        put(directory/'launch.json',launch)
        checkpoints=[]
        for p in kw['checkpoint_paths']:
            p=Path(p);dest=directory/'checkpoints'/p.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
            checkpoints.append(dict(source_path=str(p),exists=True,trusted_certificate=False,path=str(dest),bytes=p.stat().st_size,sha256=s.digest(p)))
        observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,
            elapsed_seconds=.1,maximum_sampled_group_RSS_bytes=10*s.MIB,maximum_sampled_group_CPU_seconds=.1,
            guard_scope=e.guard(),checkpoints=checkpoints,
            **{k+suffix:value for k in('stdout','stderr')for suffix,value in(
                ('_path',str(directory/(k+'.txt'))),('_sha256',s.digest(directory/(k+'.txt'))))})
        if hasattr(self,'observed_mutator'):self.observed_mutator(observed)
        finished=dict(event='linux_supervisor_finished',stage='untrusted_search',status=observed['status'],reason=observed['reason'],
                      elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
        put(directory/'progress.json',finished);(directory/'progress.jsonl').write_bytes(s.dump(finished).replace(b'\n',b'')+b'\n')
        put(directory/'supervisor-result.json',observed);return observed

    def complete(self,name='task',effect=None):
        task=self.root/name
        with patch.object(r.linux_supervisor,'run',side_effect=effect or self.fake)as child,patch.object(r,'Follow'):
            checked=r.execute(task,root=self.root)
        self.assertEqual(child.call_count,1);return task,checked

    def test_exact_one_command_and_fixed_scalar_controls_only(self):
        task,checked=self.complete();report=s.read(task/'STAGE_OBSERVED.json');request=s.read(task/'SOURCES.json')
        self.assertEqual(s.read(task/'execution/launch.json')['argv'],e.command(request,report['python_executable']))
        self.assertEqual(checked['summary']['cells'],81);self.assertEqual(checked['summary']['negative_controls'],21)
        self.assertEqual(checked['summary']['additional_identity_checks'],324)
        for flag in e.FLAGS:self.assertIs(checked[flag],False)
        self.assertTrue(checked['scalar_certificate_arithmetic_completed'])

    def test_source_closure_rejects_mutation_unknown_helpers_and_old_outputs_not_inputs(self):
        task=self.root/'source';s.prepare(task)
        with self.assertRaises(ValueError):s.prepare(task)
        self.assertEqual({p.name for p in(task/'capsule').iterdir()},set(s.FILES))
        p=task/'capsule/unbound.py';p.write_bytes(b'raise AssertionError("No source import")\n')
        with self.assertRaises(ValueError):s.verify(task)
        p.unlink();(task/'capsule/kernel.py').write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify(task)

    def test_relocation_revalidates_without_rewriting_any_original_bytes(self):
        task,checked=self.complete();other=self.root/'restored';shutil.copytree(task,other)
        before={p.relative_to(other).as_posix():p.read_bytes()for p in other.rglob('*')if p.is_file()}
        self.assertEqual(e.validate_completed(other),checked)
        self.assertEqual(before,{p.relative_to(other).as_posix():p.read_bytes()for p in other.rglob('*')if p.is_file()})

    def test_failed_execution_bool_exit_and_native_promotion_never_complete(self):
        changes=[lambda o:o.update(returncode=False),lambda o:o.update(status='stopped',reason='external_wall_timeout'),
                 lambda o:o.update(proof_accepted=True),lambda o:o['guard_scope'].update(equivalent_to_Windows_Job_or_cgroup=True),
                 lambda o:o.update(checkpoints=[]),lambda o:o.update(stderr_sha256='0'*64)]
        for i,change in enumerate(changes):
            self.observed_mutator=change
            with self.assertRaises(ValueError):self.complete('bad'+str(i))
            self.assertFalse((self.root/('bad'+str(i))/'STAGE_COMPLETED.json').exists())

    def test_full_domain_order_coefficients_and_schema_are_required(self):
        changes=[lambda p:p.update(kappa='1/10'),lambda p:p.update(upper='5'),lambda p:p.update(degree=True),
                 lambda p:p['cells'].pop(),lambda p:p['cells'].reverse(),lambda p:p['cells'][0]['bernstein'].pop(),
                 lambda p:p['cells'][0]['bernstein'].__setitem__(0,'0'),lambda p:p.update(unknown=True)]
        for i,change in enumerate(changes):
            self.certificate_mutator=change
            with self.assertRaises(ValueError):self.complete('cert'+str(i))
            self.assertFalse((self.root/('cert'+str(i))/'STAGE_COMPLETED.json').exists())

    def test_all21_and324_controls_actual_source_bindings_and_stdout_required(self):
        changes=[lambda p:p.update(status='OLD_PASS'),lambda p:p.update(negative_controls=True),
                 lambda p:p.update(negative_controls=20),lambda p:p.update(additional_identity_checks=323),
                 lambda p:p.update(source_sha256={}),lambda p:p['receipt'].update(cells=80)]
        for i,change in enumerate(changes):
            self.receipt_mutator=change
            with self.assertRaises(ValueError):self.complete('receipt'+str(i))

    def test_actual_capture_bytes_empty_stderr_and_stopped_copy_are_bound(self):
        for i,changed in enumerate(('stdout','stderr','stopped')):
            task,_=self.complete('capture'+str(i))
            if changed=='stopped':(task/'execution/checkpoints/CERTIFICATE.json').write_bytes(b'bad')
            else:
                p=task/'execution'/(changed+'.txt');p.write_bytes(b'changed')
                if changed=='stderr':
                    # Even a coherently rebound nonempty stderr is rejected.
                    report=s.read(task/'STAGE_OBSERVED.json');report['observed']['stderr_sha256']=s.digest(p)
                    put(task/'execution/supervisor-result.json',report['observed']);put(task/'STAGE_OBSERVED.json',report)
            with self.assertRaises(ValueError):e.validate_completed(task)

    def test_wrong_cwd_command_budget_and_containment_fail_before_completion(self):
        changes=[lambda p:p['argv'].append('--quick'),lambda p:p.update(cwd=str(self.root)),
                 lambda p:p.update(memory_bytes=512*s.MIB),lambda p:p.update(cpu_seconds=True),
                 lambda p:p.update(checkpoint_paths=[])]
        for i,change in enumerate(changes):
            self.launch_mutator=change
            with self.assertRaises(ValueError):self.complete('launch'+str(i))

    def test_stale_completion_and_promoted_scope_rejected(self):
        task,_=self.complete();p=task/'STAGE_COMPLETED.json';done=s.read(p)
        for field,value in(('full_notebook56_completed',True),('observed_sha256','0'*64)):
            bad=copy.deepcopy(done);bad[field]=value;put(p,bad)
            with self.assertRaises(ValueError):e.validate_completed(task)
        put(p,done);done['implementation']['linux_supervisor.py']='0'*64;put(p,done)
        with self.assertRaises(ValueError):e.validate_completed(task)

    def test_completed_cache_roundtrip_requires_sidecar_no_scalar_rerun(self):
        task,checked=self.complete();cache=self.root/'cache';export=r.save_completed(task,cache)
        with patch.object(r.linux_supervisor,'run',side_effect=AssertionError('No scalar replay'))as child:
            restored=r.restore_completed(cache,self.root/'restore',root=self.root)
        self.assertEqual(restored[1],checked);child.assert_not_called()
        Path(export['path']).with_suffix('.zip.sha256').write_bytes(b'bad')
        self.assertIsNone(r.restore_completed(cache,self.root/'bad-cache',root=self.root))

    def test_incomplete_unsafe_duplicate_and_link_zip_members_rejected(self):
        z=Mock();z.infolist.return_value=[zipfile.ZipInfo('SOURCES.json')]
        with self.assertRaises(ValueError):r.cache_members(z)
        for name in('../escape','/absolute','a//b','a\\b','C:/escape'):
            info=zipfile.ZipInfo();info.filename=info.orig_filename=name;z.infolist.return_value=[info]
            with self.assertRaises(ValueError):r.cache_members(z)
        info=zipfile.ZipInfo('linked');info.external_attr=(stat.S_IFLNK|0o777)<<16;z.infolist.return_value=[info]
        with self.assertRaises(ValueError):r.cache_members(z)

    def test_source_failure_still_bundles_false_final_status(self):
        with patch.object(s,'verify_vendor',side_effect=ValueError('Synthetic source failure')):
            out=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'work')
        self.assertFalse(out['status']['scalar_certificate_arithmetic_completed']);self.assertTrue(Path(out['bundle']).is_file())

    def test_second_session_reuses_complete_export_without_child(self):
        task,_=self.complete();cache=self.root/'drive/finite1014-kappa/completed'/s.PLAN_SHA256[:16];r.save_completed(task,cache)
        with patch.object(r.linux_supervisor,'run')as child:
            out=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'work')
        self.assertTrue(out['status']['scalar_certificate_arithmetic_completed']);self.assertTrue(out['status']['reused_complete_transaction'])
        child.assert_not_called()


class SourcePreparation(unittest.TestCase):
    def test_actual_vendor_bytes_plan_and_no_historical_outputs(self):
        vendor,plan=s.verify_vendor();self.assertEqual(len(plan['source_files']),3)
        self.assertEqual(sum(v['bytes']for v in plan['source_files'].values()),12771)
        self.assertEqual({p.name for p in vendor.iterdir()},set(s.FILES)|{'LICENSE','PROVENANCE.json'})
        self.assertFalse(plan['historical_outputs_supplied'])

    def test_duplicate_json_nonfinite_and_boolean_literal_rejected(self):
        for value in('{"x":1,"x":2}','{"x":NaN}'):
            with self.assertRaises(ValueError):s.loads(value)
        with self.assertRaises(ValueError):e.rat(True)
        with self.assertRaises(ValueError):e.rat('124/1250')


if __name__=='__main__':unittest.main()
