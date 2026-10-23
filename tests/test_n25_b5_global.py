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
from be_replay import n25_b5_global as runner
from be_replay import n25_b5_global_sources as source
from be_replay import n25_b5_global_evidence as evidence
from be_replay.colab_batch import atomic_json


class Catalog(unittest.TestCase):
    def test_exact_two_actions_no_old_receipts_or_local_candidates(self):
        self.assertEqual(len(source.stages()),2)
        rows=source.selected()
        self.assertEqual(len(rows),66)
        self.assertTrue(all('ACCEPTED' not in n and 'PROGRESS' not in n for n in rows))
        self.assertFalse(any('/local25_' in n or n.endswith('/contract.json') for n in rows))
        self.assertEqual(sum(r['kind']=='candidate'for r in rows.values()),2)
        self.assertEqual(sum(r['kind']=='premise'for r in rows.values()),1)
        self.assertEqual(len(source.selection_sha()),64)
        parent=source.definition()
        self.assertTrue(parent['initial']['deterministic_receipt_serialization_verified'])
        self.assertEqual(parent['global_resource']['parent_acceptance_sha256'],parent['initial']['historical_acceptance']['sha256'])

    def test_bad_branch(self):
        with self.assertRaises(ValueError):
            source.stages('b0')

    def test_notebook_pin_and_routes(self):
        spec=importlib.util.spec_from_file_location('b5_notebook',Path(__file__).resolve().parents[1]/'tools/make_n25_b5_global_notebook.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        value=module.build('a'*40)
        text=json.dumps(value)
        self.assertIn('39_n25_global_parents_b5',text)
        self.assertIn('n25-global-parents-b5',text)
        self.assertIn('a'*40,text)
        self.assertIn('n25_b5_global import run_colab',text)
        for cell in value['cells']:
            if cell['cell_type']=='code':compile(''.join(cell['source']),module.NAME,'exec')
        with self.assertRaises(ValueError):module.build('main')
        with self.assertRaises(ValueError):module.build('a'*40,'wrong')



class Transport(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.task=Path(self.temp.name)/'original';self.task.mkdir()
        self.stage=source.stages('b5')[0]
        execution=self.task/'execution'/self.stage['name'];execution.mkdir(parents=True)
        folder=evidence.root(self.task)/self.stage['folder'];folder.mkdir(parents=True)
        (folder/self.stage['script']).write_text('synthetic source only\n')
        (execution/'stdout.txt').write_text('PASS_FRESH_EXACT_INITIAL25_B5\n')
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
        return evidence.transport(task or self.task,'b5',self.stage,self.report)

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
        for name in runner.cache_files(self.task,'b5',0):
            p=self.task/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}\n')
        self.archive=runner.save_prefix(self.task,'b5',0,self.base/'cache')

    def mutate(self,change):
        with zipfile.ZipFile(self.archive)as z:rows=[(i.filename,z.read(i))for i in z.infolist()]
        rows=change(rows)
        with zipfile.ZipFile(self.archive,'w',compression=zipfile.ZIP_DEFLATED)as z:
            for name,raw in rows:z.writestr(name,raw)
        self.archive.with_suffix('.zip.sha256').write_text(common.digest(self.archive)+'  '+self.archive.name+'\n')

    def test_roundtrip_revalidates_whole_prefix(self):
        target=self.base/'restored'
        runner.restore_prefix(self.archive,target,'b5',0)
        self.assertTrue((target/'SOURCES.json').exists())
        self.assertGreaterEqual(evidence.validate_prefix.call_count,2)

    def test_corrupt_archive_before_destination_created(self):
        self.archive.write_bytes(b'bad')
        target=self.base/'bad-target'
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b5',0)
        self.assertFalse(target.exists())

    def test_traversal_rejected_before_destination(self):
        self.mutate(lambda rows:rows+[('../escaped',b'bad')])
        target=self.base/'bad-target'
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b5',0)
        self.assertFalse(target.exists())

    def test_changed_member_hash_rejected(self):
        self.mutate(lambda rows:[(n,b'changed' if n=='SOURCES.json' else b)for n,b in rows])
        target=self.base/'bad-target'
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b5',0)
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
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b5',0)
        self.assertFalse(target.exists())


class CompleteSyntheticStage(unittest.TestCase):
    """Exercise the real validators/cache around a fabricated non-math worker."""
    def test_actual_complete_evidence_roundtrip_and_corruption(self):
        with tempfile.TemporaryDirectory() as temporary:
            task=Path(temporary)/'original';task.mkdir()
            stage=dict(name='initial-accept',kind='initial',action='accept',folder='fixture/initial',
                script='initial25_b5.py',args=['accept'],proof='INITIAL25_B5_PROOF.json',receipt='INITIAL25_B5_ACCEPTED.json')
            d=evidence.root(task)/stage['folder'];d.mkdir(parents=True)
            (d/stage['script']).write_text('# synthetic non-mathematical source\n')
            frozen={stage['script']:common.digest(d/stage['script'])}
            atomic_json(d/'FROZEN_SOURCES.json',frozen)
            cover=dict(total=18432,active=0,excluded=18432)
            profile=dict(n=25)
            proof=dict(profile=profile,source_sha256=frozen,maximum_covers=12,
                stages=[dict(cover=cover)for _ in range(12)],export=dict(cover,panels=[{}for _ in range(100)]))
            atomic_json(d/stage['proof'],proof)
            receipt=dict(status='PASS_FRESH_EXACT_INITIAL25_B5',proof_sha256=common.digest(d/stage['proof']),
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
                 patch.object(source,'definition',return_value=parent),patch.object(source,'verify',return_value={}):
                checked=runner.execute(task,'b5',0,supervise=fake)
                self.assertTrue(checked[0]['conditional_arithmetic_replayed'])
                archive=runner.save_prefix(task,'b5',1,Path(temporary)/'cache')
                moved=Path(temporary)/'relocated';runner.restore_prefix(archive,moved,'b5',1)
                evidence.validate_prefix(moved,'b5',1)
                capture=moved/'execution'/stage['name']/'stdout.txt';capture.write_text('garbage\n')
                with self.assertRaises(ValueError):evidence.validate_prefix(moved,'b5',1)


class TwoStageSyntheticChain(unittest.TestCase):
    """Both real evidence validators around fabricated, non-mathematical files."""
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name);self.task=self.base/'task';self.task.mkdir()
        self.stages=[dict(name='initial-accept',kind='initial',action='accept',folder='fixture/initial',
            script='initial25_b5.py',args=['accept'],proof='INITIAL25_B5_PROOF.json',receipt='INITIAL25_B5_ACCEPTED.json'),
            dict(name='global_resource-accept',kind='global_resource',action='accept',folder='fixture/resource',
            script='resources_b5.py',args=['accept'],proof='RESOURCE_B5_GLOBAL_PROOF.json',receipt='RESOURCE_B5_GLOBAL_ACCEPTED.json')]
        profile=dict(n=25,fixture='No mathematical source was executed')
        controls=['synthetic non-mathematical control']
        cover=dict(total=18432,active=0,excluded=18432)
        self.parent=dict(profile=profile)
        for stage in self.stages:
            folder=evidence.root(self.task)/stage['folder'];folder.mkdir(parents=True)
            (folder/stage['script']).write_text("raise RuntimeError('Original kernels must never execute in these fixtures')\n")
            frozen={stage['script']:common.digest(folder/stage['script'])}
            atomic_json(folder/'FROZEN_SOURCES.json',frozen)
            bound=dict(frozen,**{'FROZEN_SOURCES.json':common.digest(folder/'FROZEN_SOURCES.json')})
            proof=dict(profile=profile,source_sha256=frozen if stage['kind']=='initial' else bound)
            if stage['kind']=='initial':
                proof.update(maximum_covers=12,stages=[dict(cover=cover)for _ in range(12)],
                    export=dict(cover,panels=[{}for _ in range(100)]))
            else:
                proof.update(parent_proof_sha256=self.initial_proof_sha,parent_acceptance_sha256=self.initial_receipt_sha,
                    rows=[dict(index=i,result=dict(excluded=i!=20))for i in range(100)])
            atomic_json(folder/stage['proof'],proof)
            receipt=dict(status='PASS_FRESH_EXACT_INITIAL25_B5'if stage['kind']=='initial'else 'PASS_FRESH_EXACT_SHARP25_B5_GLOBAL_RESOURCES',
                proof_sha256=common.digest(folder/stage['proof']),checker_sha256=frozen[stage['script']],
                profile=profile,source_sha256=proof['source_sha256'],negative_controls=controls,probability_panels=100)
            if stage['kind']=='initial':
                receipt['signed_rectangles']=239616
            else:
                receipt.update(parent_proof_sha256=self.initial_proof_sha,parent_acceptance_sha256=self.initial_receipt_sha,
                    surviving_panels=[20],excluded_panels=[i for i in range(100)if i!=20],seconds=1.25)
            raw=(json.dumps(receipt,indent=2)+'\n').encode()
            import hashlib
            if stage['kind']=='initial':
                self.initial_receipt_sha=hashlib.sha256(raw).hexdigest();self.initial_proof_sha=receipt['proof_sha256']
            stage['synthetic_receipt_bytes']=raw
            section=dict(controls=controls,checker=dict(member='synthetic/'+stage['script']),
                directory=source.source.PREFIX+stage['folder'],historical_acceptance=dict(sha256=hashlib.sha256(raw).hexdigest()))
            if stage['kind']=='global_resource':section.update(surviving_panels=receipt['surviving_panels'],excluded_panels=receipt['excluded_panels'])
            self.parent[stage['kind']]=section
        # Keep bytes outside the public stage descriptor; real ledger stage
        # descriptors are JSON objects with no synthetic payload fields.
        self.receipts={s['name']:s.pop('synthetic_receipt_bytes')for s in self.stages}
        self.selected={}
        for path in evidence.root(self.task).rglob('*'):
            if path.is_file():
                member=source.source.PREFIX+path.relative_to(evidence.root(self.task)).as_posix()
                self.selected[member]=dict(bytes=path.stat().st_size,sha256=common.digest(path),kind='source')
                target=self.task/'source'/member;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
        atomic_json(self.task/source.source.MANIFEST,dict(synthetic=True));atomic_json(self.task/source.source.TASK,dict(synthetic=True))
        for name,value in [('stages',self.stages),('selected',self.selected),('definition',self.parent),('verify',{})]:
            patcher=patch.object(source,name,return_value=value);patcher.start();self.addCleanup(patcher.stop)

    def fake(self,command,**options):
        stage=next(s for s in self.stages if s['script']==Path(command[3]).name)
        folder=options['cwd'];output=options['output_dir'];output.mkdir(parents=True)
        (folder/stage['receipt']).write_bytes(self.receipts[stage['name']])
        status=json.loads(self.receipts[stage['name']])['status']
        (output/'stdout.txt').write_text(status+(' 1.25'if stage['kind']=='global_resource'else '')+'\n')
        (output/'stderr.txt').write_text('')
        launch=dict(argv=command,cwd=str(folder),output_dir=str(output),mode='untrusted_search',wall_seconds=float(evidence.WALL),
            cpu_seconds=evidence.CPU,memory_bytes=evidence.MEMORY,checkpoint_paths=[],disk_bytes=evidence.DISK,
            log_bytes=16*evidence.MIB,sample_seconds=.2,heartbeat_seconds=20.)
        observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,
            guard_scope=paths._group_scope(launch),stdout_path=str(output/'stdout.txt'),stderr_path=str(output/'stderr.txt'),
            stdout_sha256=common.digest(output/'stdout.txt'),stderr_sha256=common.digest(output/'stderr.txt'))
        atomic_json(output/'launch.json',launch);atomic_json(output/'supervisor-result.json',observed)
        return observed

    def complete(self):
        runner.execute(self.task,'b5',0,supervise=self.fake)
        runner.execute(self.task,'b5',1,supervise=self.fake)

    def test_two_full_actions_relocated_prefix_and_false_theorem_flags(self):
        self.complete()
        checked=evidence.validate_completed(self.task)
        self.assertTrue(checked['conditional_parent_arithmetic_replayed'])
        for flag in ('native_arithmetic_accepted','stronger24_premise_acquired','resource_interfaces_verified',
                     'count_forests_accepted','full_n25_verified','all_index_conclusion_verified'):
            self.assertIs(checked[flag],False)
        saved=runner.save_prefix(self.task,'b5',2,self.base/'cache')
        restored=self.base/'restored';runner.restore_prefix(saved,restored,'b5',2)
        self.assertEqual(evidence.validate_completed(restored),checked)

    def test_only_completed_first_action_reused_then_new_resource_cwd(self):
        runner.execute(self.task,'b5',0,supervise=self.fake)
        saved=runner.save_prefix(self.task,'b5',1,self.base/'cache')
        moved=self.base/'moved';runner.restore_prefix(saved,moved,'b5',1)
        runner.execute(moved,'b5',1,supervise=self.fake)
        self.assertTrue(evidence.validate_completed(moved)['conditional_parent_arithmetic_replayed'])
        first=common.read(moved/'ledgers/initial-accept.json');second=common.read(moved/'ledgers/global_resource-accept.json')
        self.assertEqual(first['original_task_root'],str(self.task.resolve()))
        self.assertEqual(second['original_task_root'],str(moved.resolve()))

    def test_mutated_resource_parent_or_control_never_becomes_completed(self):
        self.complete()
        folder=evidence.root(self.task)/self.stages[1]['folder'];path=folder/self.stages[1]['receipt']
        original=path.read_bytes()
        for key,value in [('parent_acceptance_sha256','0'*64),('negative_controls',[]),('source_sha256',{})]:
            receipt=json.loads(original);receipt[key]=value;path.write_text(json.dumps(receipt))
            with self.assertRaises(ValueError):evidence.validate_completed(self.task)
            path.write_bytes(original)


if __name__=='__main__':unittest.main()
