"""Synthetic transport/semantic fixtures only; no archived kernel execution."""
from copy import deepcopy
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import aux24_evidence as paths, count_task as common
from be_replay import n25_b012_acquisition as runner
from be_replay import n25_b012_acquisition_sources as source
from be_replay import n25_b012_acquisition_evidence as evidence
from be_replay import n25_b012_interfaces as join
from be_replay.colab_batch import atomic_json


class Catalog(unittest.TestCase):
    def test_exact_ten_actions_no_old_receipts_or_local_candidates(self):
        self.assertEqual([len(source.stages(b)) for b in ('b0','b1','b2')], [2,4,4])
        for branch in ('b0','b1','b2'):
            rows = source.selected(branch)
            self.assertTrue(all('ACCEPTED' not in n for n in rows))
            self.assertFalse(any('/local25_' in n and n.endswith('_PROOF.json') for n in rows))
            self.assertEqual(sum(n.endswith('/contract.json') for n in rows), {'b0':17,'b1':35,'b2':23}[branch])
            self.assertEqual(len(source.selection_sha(branch)),64)

    def test_bad_branch(self):
        with self.assertRaises(ValueError):
            source.stages('b3')

    def test_notebook_pin_and_routes(self):
        spec = importlib.util.spec_from_file_location('parent_notebooks', Path(__file__).resolve().parents[1]/'tools/make_n25_b012_acquisition_notebooks.py')
        module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        for name,(branch,_,_) in module.JOBS.items():
            value = module.build('a'*40,name)
            text = json.dumps(value)
            self.assertIn('n25_b012_acquisition',text)
            self.assertIn('n25-parents-'+branch,text)
            self.assertIn('a'*40,text)
            for cell in value['cells']:
                if cell['cell_type']=='code':compile(''.join(cell['source']),name,'exec')
        with self.assertRaises(ValueError):module.build('main',next(iter(module.JOBS)))


class Transport(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.task=Path(self.temp.name)/'original';self.task.mkdir()
        self.stage=source.stages('b0')[0]
        execution=self.task/'execution'/self.stage['name'];execution.mkdir(parents=True)
        folder=evidence.root(self.task)/self.stage['folder'];folder.mkdir(parents=True)
        (folder/self.stage['script']).write_text('synthetic source only\n')
        (execution/'stdout.txt').write_text('PASS_FRESH_EXACT_INITIAL25_B0\n')
        (execution/'stderr.txt').write_text('')
        self.launch=dict(argv=[str(Path(self.temp.name)/'python'),' -B'.strip(),'-S',str(folder/self.stage['script']),'accept'],
            cwd=str(folder),output_dir=str(execution),mode='untrusted_search',wall_seconds=float(evidence.WALL),
            cpu_seconds=evidence.CPU,memory_bytes=evidence.MEMORY,checkpoint_paths=[],disk_bytes=evidence.DISK,
            log_bytes=16*evidence.MIB,sample_seconds=.2,heartbeat_seconds=20.)
        self.observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,
            sample_count=1,guard_scope=paths._group_scope(self.launch),stdout_path=str(execution/'stdout.txt'),
            stderr_path=str(execution/'stderr.txt'),stdout_sha256=common.digest(execution/'stdout.txt'),
            stderr_sha256=common.digest(execution/'stderr.txt'))
        self.report=dict(original_task_root=str(self.task),observed=self.observed)
        self.execution=execution
        self.write()

    def write(self):
        atomic_json(self.execution/'launch.json',self.launch)
        atomic_json(self.execution/'supervisor-result.json',self.observed)

    def check(self,task=None):
        return evidence.transport(task or self.task,'b0',self.stage,self.report)

    def test_complete_and_relocated(self):
        self.check()
        moved=Path(self.temp.name)/'relocated';shutil.copytree(self.task,moved)
        self.check(moved)

    def test_tampered_capture(self):
        (self.execution/'stdout.txt').write_text('different')
        with self.assertRaises(ValueError):self.check()

    def test_rehashed_garbage_terminal(self):
        (self.execution/'stdout.txt').write_text('garbage\n')
        self.observed['stdout_sha256']=common.digest(self.execution/'stdout.txt');self.write()
        with self.assertRaises(ValueError):self.check()

    def test_failed_action(self):
        self.observed['returncode']=1;self.write()
        with self.assertRaises(ValueError):self.check()

    def test_wrong_command(self):
        self.launch['argv'][-1]='construct';self.write()
        with self.assertRaises(ValueError):self.check()

    def test_budget_and_false_native_upgrade(self):
        self.launch['cpu_seconds']=True;self.write()
        with self.assertRaises(ValueError):self.check()

    def test_scope_upgrade(self):
        self.observed['guard_scope']['aggregate_kernel_memory_limit']=True;self.write()
        with self.assertRaises(ValueError):self.check()


class Cache(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name);self.task=self.base/'task';self.task.mkdir()
        self.row={'cutoff25_20261011/test/source.py':dict(bytes=1,sha256='a'*64,kind='source')}
        self.selected=patch.object(source,'selected',return_value=self.row);self.selected.start();self.addCleanup(self.selected.stop)
        self.validate=patch.object(evidence,'validate_prefix',return_value=[]);self.validate.start();self.addCleanup(self.validate.stop)
        for name in runner.cache_files(self.task,'b0',0):
            p=self.task/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}\n')
        self.archive=runner.save_prefix(self.task,'b0',0,self.base/'cache')

    def mutate(self,change):
        with zipfile.ZipFile(self.archive)as z:rows=[(i.filename,z.read(i))for i in z.infolist()]
        rows=change(rows)
        with zipfile.ZipFile(self.archive,'w',compression=zipfile.ZIP_DEFLATED)as z:
            for name,raw in rows:z.writestr(name,raw)
        self.archive.with_suffix('.zip.sha256').write_text(common.digest(self.archive)+'  '+self.archive.name+'\n')

    def test_roundtrip_revalidates_whole_prefix(self):
        target=self.base/'restored'
        runner.restore_prefix(self.archive,target,'b0',0)
        self.assertTrue((target/'SOURCES.json').exists())
        self.assertGreaterEqual(evidence.validate_prefix.call_count,2)

    def test_corrupt_archive_before_destination_created(self):
        self.archive.write_bytes(b'bad')
        target=self.base/'bad-target'
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b0',0)
        self.assertFalse(target.exists())

    def test_traversal_rejected_before_destination(self):
        self.mutate(lambda rows:rows+[('../escaped',b'bad')])
        target=self.base/'bad-target'
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b0',0)
        self.assertFalse(target.exists())

    def test_changed_member_hash_rejected(self):
        self.mutate(lambda rows:[(n,b'changed' if n=='SOURCES.json' else b)for n,b in rows])
        target=self.base/'bad-target'
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b0',0)
        self.assertFalse(target.exists())

    def test_incompatible_runtime_rejected(self):
        def change(rows):
            result=[]
            for n,b in rows:
                if n=='COMPLETED_PREFIX.json':
                    p=json.loads(b);p['implementation']['linux_supervisor.py']='0'*64;b=json.dumps(p).encode()
                result.append((n,b))
            return result
        self.mutate(change)
        target=self.base/'bad-target'
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b0',0)
        self.assertFalse(target.exists())


class Semantic(unittest.TestCase):
    def setUp(self):
        rr=dict(pl='2/5',pu='41/100',rho_lo='1',rho_hi='11/10',beta_lo='0',beta_hi_signed='1/2',
                beta='1/2',mean_lo='1/10',mean_hi='1/2',theta='1/10',A='1/2',B='1/2')
        acq=dict(rr,D='1',d0='1',lambda_max='1',H_minus='1',H_plus='1',radius_minus='1',radius_plus='1',
                 outer0='1',outer1='1',charge_b='1',charge_g='1',charge_h='1',
                 quadratics=[dict(A='1',Fplus='0',Fminus='0',Qbudget='1')])
        self.resource=dict(excluded=False,raw_row=rr,initial=deepcopy(rr),result=acq)
        self.cfg=dict(n=25,K='0',index=40,p=['2/5','41/100'],rho_lower='1',rho_upper='11/10',D='1',d0='1',
            Lambda='1',Hminus='1',Hplus='1',radius_minus='1',radius_plus='1',outer0='1',outer1='1',
            binary_charge='1',gap_charge='1',noise_charge='1',quadratics=deepcopy(acq['quadratics']),
            sign_premise=dict(schema='ACTUAL_SIGN_CONDITIONED_MARGINAL_V1',conditional_means_zero=True,
                              negative_endpoint_lower='1/2',positive_endpoint_lower='1/2'),
            acquired_beta=['0','1/2'],acquired_mean=['0','1/2'],acquired_theta_upper='1/10')

    def check(self):return join.interface(self.resource,self.cfg,F(11,10))

    def test_complete_closed_equality_allowed(self):
        self.assertEqual(len(self.check()['signed_quadratic_domination']),2)

    def test_exact_quadratic_interior_minimum(self):
        self.assertEqual(join.minimum(F(1,8),F(-1),F(1),F(1)),F(-1,8))
        self.assertEqual(join.minimum(F(1),F(0),F(-1),F(1)),0)

    def test_each_missing_implication_rejected(self):
        changes=[lambda:self.cfg.update(n=True),lambda:self.cfg.update(D='1/2'),
            lambda:self.cfg.update(binary_charge='2'),lambda:self.cfg.update(acquired_theta_upper='1/20'),
            lambda:self.cfg.update(p=['2/5','1/2']),lambda:self.cfg.update(acquired_beta=['0','1/4']),
            lambda:self.cfg.update(acquired_mean=['0','1/4']),
            lambda:self.cfg['sign_premise'].update(negative_endpoint_lower='3/4'),
            lambda:self.cfg['quadratics'][0].update(A='1/2')]
        original=deepcopy(self.cfg)
        for mutate in changes:
            self.cfg=deepcopy(original);mutate()
            with self.assertRaises(ValueError):self.check()


class CompleteSyntheticStage(unittest.TestCase):
    """Exercise the real validators/cache around a fabricated non-math worker."""
    def test_actual_complete_evidence_roundtrip_and_corruption(self):
        with tempfile.TemporaryDirectory() as temporary:
            task=Path(temporary)/'original';task.mkdir()
            stage=dict(name='initial-accept',kind='initial',action='accept',folder='fixture/initial',
                script='initial25_b0.py',args=['accept'],proof='INITIAL25_B0_PROOF.json',receipt='INITIAL25_B0_ACCEPTED.json')
            d=evidence.root(task)/stage['folder'];d.mkdir(parents=True)
            (d/stage['script']).write_text('# synthetic non-mathematical source\n')
            frozen={stage['script']:common.digest(d/stage['script'])}
            atomic_json(d/'FROZEN_SOURCES.json',frozen)
            cover=dict(total=18432,active=0,excluded=18432)
            profile=dict(n=25)
            proof=dict(profile=profile,source_sha256=frozen,maximum_covers=12,
                stages=[dict(cover=cover)for _ in range(12)],export=dict(cover,panels=[{}for _ in range(100)]))
            atomic_json(d/stage['proof'],proof)
            receipt=dict(status='PASS_FRESH_EXACT_INITIAL25_B0',proof_sha256=common.digest(d/stage['proof']),
                checker_sha256=frozen[stage['script']],profile=profile,source_sha256=frozen,
                negative_controls=['synthetic control'],signed_rectangles=239616,probability_panels=100)
            receipt_raw=json.dumps(receipt,indent=2)+'\n'
            import hashlib
            parent=dict(profile=profile,initial=dict(controls=['synthetic control'],
                checker=dict(member='synthetic/'+stage['script']),
                historical_acceptance=dict(sha256=hashlib.sha256(receipt_raw.encode()).hexdigest())))
            selected={}
            for path in d.iterdir():
                member=source.source.PREFIX+stage['folder']+'/'+path.name
                selected[member]=dict(bytes=path.stat().st_size,sha256=common.digest(path),kind='source')
                destination=task/'source'/member;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,destination)
            atomic_json(task/source.source.MANIFEST,dict(synthetic=True))
            atomic_json(task/source.source.TASK,dict(synthetic=True))
            def fake(command,**options):
                output=options['output_dir'];output.mkdir(parents=True)
                (d/stage['receipt']).write_bytes(receipt_raw.encode())
                (output/'stdout.txt').write_text(receipt['status']+'\n');(output/'stderr.txt').write_text('')
                launch=dict(argv=command,cwd=str(options['cwd']),output_dir=str(output),mode='untrusted_search',
                    wall_seconds=float(evidence.WALL),cpu_seconds=evidence.CPU,memory_bytes=evidence.MEMORY,
                    checkpoint_paths=[],disk_bytes=evidence.DISK,log_bytes=16*evidence.MIB,sample_seconds=.2,heartbeat_seconds=20.)
                observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,
                    sample_count=1,guard_scope=paths._group_scope(launch),stdout_path=str(output/'stdout.txt'),
                    stderr_path=str(output/'stderr.txt'),stdout_sha256=common.digest(output/'stdout.txt'),
                    stderr_sha256=common.digest(output/'stderr.txt'))
                atomic_json(output/'launch.json',launch);atomic_json(output/'supervisor-result.json',observed)
                return observed
            with patch.object(source,'stages',return_value=[stage]),patch.object(source,'selected',return_value=selected),\
                 patch.object(source,'definition',return_value=(parent,None,[])),patch.object(source,'verify',return_value={}):
                checked=runner.execute(task,'b0',0,supervise=fake)
                self.assertTrue(checked[0]['conditional_arithmetic_replayed'])
                archive=runner.save_prefix(task,'b0',1,Path(temporary)/'cache')
                moved=Path(temporary)/'relocated';runner.restore_prefix(archive,moved,'b0',1)
                evidence.validate_prefix(moved,'b0',1)
                capture=moved/'execution'/stage['name']/'stdout.txt';capture.write_text('garbage\n')
                with self.assertRaises(ValueError):evidence.validate_prefix(moved,'b0',1)


if __name__=='__main__':unittest.main()
