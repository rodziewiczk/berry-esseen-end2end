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
from be_replay import middle_n25_acquisition as runner
from be_replay import middle_n25_acquisition_sources as source
from be_replay import middle_n25_acquisition_evidence as evidence
from be_replay.colab_batch import atomic_json


class Catalog(unittest.TestCase):
    def test_exact_selected_actions_and_inputs(self):
        self.assertEqual([len(source.stages(b))for b in ('b4','b5')],[14,12])
        for branch,total,locals_ in [('b4',169,11),('b5',89,9)]:
            rows=source.selected(branch);self.assertEqual(len(rows),total)
            self.assertFalse(any('ACCEPTED'in Path(n).name or Path(n).name=='GLOBAL_RESOURCES_PROOF.json'for n in rows))
            self.assertEqual(len(source.definition(branch)['locals']),locals_)
            self.assertEqual([s['action']for s in source.stages(branch)[:3]],['accept','construct','accept'])
            self.assertEqual(len(source.selection_sha(branch)),64)
        self.assertEqual(len(evidence.aliases('b4')),3)
        self.assertEqual(evidence.aliases('b5'),[])

    def test_bad_branch(self):
        with self.assertRaises(ValueError):
            source.stages('b0')

    def test_notebook_pin_and_routes(self):
        spec=importlib.util.spec_from_file_location('middle_notebooks',Path(__file__).resolve().parents[1]/'tools/make_middle_n25_acquisition_notebooks.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        self.assertEqual({n[:2]for n in module.JOBS},{'47','48'})
        for name,(branch,_,_,_)in module.JOBS.items():
            value=module.build('a'*40,name);text=json.dumps(value)
            self.assertIn('middle_n25_acquisition',text);self.assertIn('middle-n25-'+branch,text);self.assertIn('a'*40,text)
            for cell in value['cells']:
                if cell['cell_type']=='code':compile(''.join(cell['source']),name,'exec')
        with self.assertRaises(ValueError):module.build('main',next(iter(module.JOBS)))



class Transport(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.task=Path(self.temp.name)/'original';self.task.mkdir()
        self.stage=source.stages('b4')[0]
        execution=self.task/'execution'/self.stage['name'];execution.mkdir(parents=True)
        folder=evidence.root(self.task)/self.stage['folder'];folder.mkdir(parents=True)
        (folder/self.stage['script']).write_text('synthetic source only\n')
        (execution/'stdout.txt').write_text('INITIAL_MIDDLE_B4_ACCEPTED 1.25\n')
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
        return evidence.transport(task or self.task,'b4',self.stage,self.report)

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
        for name in runner.cache_files(self.task,'b4',0):
            p=self.task/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}\n')
        self.archive=runner.save_prefix(self.task,'b4',0,self.base/'cache')

    def mutate(self,change):
        with zipfile.ZipFile(self.archive)as z:rows=[(i.filename,z.read(i))for i in z.infolist()]
        rows=change(rows)
        with zipfile.ZipFile(self.archive,'w',compression=zipfile.ZIP_DEFLATED)as z:
            for name,raw in rows:z.writestr(name,raw)
        self.archive.with_suffix('.zip.sha256').write_text(common.digest(self.archive)+'  '+self.archive.name+'\n')

    def test_roundtrip_revalidates_whole_prefix(self):
        target=self.base/'restored'
        runner.restore_prefix(self.archive,target,'b4',0)
        self.assertTrue((target/'SOURCES.json').exists())
        self.assertGreaterEqual(evidence.validate_prefix.call_count,2)

    def test_corrupt_archive_before_destination_created(self):
        self.archive.write_bytes(b'bad')
        target=self.base/'bad-target'
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b4',0)
        self.assertFalse(target.exists())

    def test_traversal_rejected_before_destination(self):
        self.mutate(lambda rows:rows+[('../escaped',b'bad')])
        target=self.base/'bad-target'
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b4',0)
        self.assertFalse(target.exists())

    def test_changed_member_hash_rejected(self):
        self.mutate(lambda rows:[(n,b'changed' if n=='SOURCES.json' else b)for n,b in rows])
        target=self.base/'bad-target'
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b4',0)
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
        with self.assertRaises(ValueError):runner.restore_prefix(self.archive,target,'b4',0)
        self.assertFalse(target.exists())


class FourStageSyntheticChain(unittest.TestCase):
    """A fake full INITIAL/global/local chain, with the real evidence checks."""
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name);self.task=self.base/'task';self.task.mkdir()
        self.stages=[dict(name='initial-accept',kind='initial',action='accept',folder='fixture/canonical',script='initial_middle.py',
            args=['accept'],proof='INITIAL_MIDDLE_B4_PROOF.json',receipt='INITIAL_MIDDLE_B4_ACCEPTED.json')]
        for action in('construct','accept'):
            self.stages.append(dict(name='global_resource-'+action,kind='global_resource',action=action,folder='fixture/canonical',
                script='global_resources.py',args=[action],proof='GLOBAL_RESOURCES_PROOF.json',receipt='GLOBAL_RESOURCES_ACCEPTED.json'if action=='accept'else None))
        self.stages.append(dict(name='local-20-accept',kind='local',action='accept',index=20,folder='fixture/alias',
            script='acquire_panel_memoized.py',args=['accept','20'],proof='PANEL20_PROOF.json',receipt='PANEL20_ACCEPTED.json'))
        self.profile=dict(n=25,invariants=dict(rho_lo='33/20',rho='7/4'),fixture='No mathematical source executed')
        self.controls=['synthetic source-bound control']
        self.packet=dict(branch='b4',band=4,canonical_directory=source.source.PREFIX+'fixture/canonical',
            alias_directories=[source.source.PREFIX+'fixture/alias'],profile=self.profile,contact_allowance='441991/2000000',
            initial=dict(expected_status='PASS_FRESH_EXACT_MIDDLE25_MIDDLE_B4_INITIAL',negative_controls=self.controls),
            global_resource=dict(expected_status='PASS_FRESH_EXACT_MIDDLE_B4_GLOBAL_RESOURCES',negative_controls=self.controls,survivors=[20]),
            locals=[dict(index=20,cycle_limit=2,cycles=2,mathematical_cover_calls=8,excluded=False,
                expected_status='PASS_FRESH_EXACT_MIDDLE25_MIDDLE_B4_TWO_CYCLE_PANEL_ACQUISITION',negative_controls=self.controls)])
        self.cover=dict(total=9216,active=1,excluded=9215,reasons=dict(synthetic=9215),
            panels=[dict(pl=str(F(i,100)),pu=str(F(i+1,100)))for i in range(100)])
        for folder_name in('fixture/canonical','fixture/alias'):
            folder=evidence.root(self.task)/folder_name;folder.mkdir(parents=True)
            for script in('initial_middle.py','global_resources.py','acquire_panel.py','acquire_panel_memoized.py'):
                text="raise RuntimeError('Never execute a mathematical fixture')\n"
                if script=='acquire_panel.py'and folder_name.endswith('alias'):text+='# different selected two-cycle source\n'
                (folder/script).write_text(text)
            initial={'initial_middle.py':common.digest(folder/'initial_middle.py')}
            panel={n:common.digest(folder/n)for n in('initial_middle.py','global_resources.py','acquire_panel.py','acquire_panel_memoized.py')}
            atomic_json(folder/'COPY_MANIFEST.json',dict(files=initial));atomic_json(folder/'PANEL_COPY_MANIFEST.json',dict(files=panel))
            proof=dict(schema='EXACT_MIDDLE25_MIDDLE_B4_INITIAL_COARSENED_HIGH_V1',profile=self.profile,
                source_sha256=initial,contact_allowance='441991/2000000',stages=[dict(cover=self.cover)for _ in range(12)],export=self.cover)
            atomic_json(folder/'INITIAL_MIDDLE_B4_PROOF.json',proof)
        self.canonical=evidence.root(self.task)/'fixture/canonical';self.alias=evidence.root(self.task)/'fixture/alias'
        self.initial_sha=common.digest(self.canonical/'INITIAL_MIDDLE_B4_PROOF.json')
        self.global_rows=[dict(index=i,input_source=dict(fixture=True),derivation=dict(excluded=i!=20))for i in range(100)]
        profile=self.profile
        local=dict(profile=profile,index=20,p_interval=['1/5','21/100'],source_sha256=common.read(self.alias/'PANEL_COPY_MANIFEST.json')['files'],
            cycle_limit=2,initial_covers_per_cycle=4,mean_floor_grid=10**12,initial_proof_sha256=self.initial_sha,
            excluded=False,global_resource=self.global_rows[20],cycles=[dict(cycle=i+1,profile=profile,
                stages=[dict(input_raw='1',input_D='1',cover=self.cover)for _ in range(4)])for i in range(2)])
        atomic_json(self.alias/'PANEL20_PROOF.json',local)
        helper=evidence.root(self.task)/'new_middle/stage_cache_v2';helper.mkdir(parents=True)
        (helper/'exact_stage_cache.py').write_text("raise RuntimeError('Never import this fixture')\n")
        atomic_json(helper/'INDEPENDENT_REVIEW.json',dict(synthetic=True))
        self.selected={}
        for p in evidence.root(self.task).rglob('*'):
            if not p.is_file():continue
            member=source.source.PREFIX+p.relative_to(evidence.root(self.task)).as_posix()
            self.selected[member]=dict(bytes=p.stat().st_size,sha256=common.digest(p),kind='source')
            dest=self.task/'source'/member;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        atomic_json(self.task/source.source.MANIFEST,dict(synthetic=True));atomic_json(self.task/source.source.TASK,dict(synthetic=True))
        for name,value in(('stages',self.stages),('selected',self.selected),('definition',self.packet),('verify',{})):
            patcher=patch.object(source,name,return_value=value);patcher.start();self.addCleanup(patcher.stop)

    def fake(self,command,**options):
        stage=next(s for s in self.stages if s['script']==Path(command[3]).name and s['args']==command[4:])
        folder=options['cwd'];base=folder.parent.parent;canonical=base/'fixture/canonical'
        source_map=common.read(folder/('COPY_MANIFEST.json'if stage['kind']=='initial'else'PANEL_COPY_MANIFEST.json'))['files']
        if stage['kind']=='global_resource'and stage['action']=='construct':
            atomic_json(folder/stage['proof'],dict(schema='EXACT_MIDDLE25_MIDDLE_B4_GLOBAL_RESOURCES_V1',profile=self.profile,
                source_sha256=source_map,initial_proof_sha256=self.initial_sha,
                initial_acceptance_sha256=common.digest(canonical/'INITIAL_MIDDLE_B4_ACCEPTED.json'),rows=self.global_rows))
            terminal='GLOBAL_RESOURCES_CONSTRUCTED 1.25\n'
        else:
            section=self.packet['locals'][0]if stage['kind']=='local'else self.packet[stage['kind']]
            receipt=dict(status=section['expected_status'],proof_sha256=common.digest(folder/stage['proof']),
                checker_sha256=common.digest(folder/('acquire_panel.py'if stage['kind']=='local'else stage['script'])),
                source_sha256=source_map,negative_controls=self.controls,seconds=1.25)
            if stage['kind']=='initial':
                receipt.update(profile=self.profile,signed_rectangles=119808,probability_panels=100)
                terminal='INITIAL_MIDDLE_B4_ACCEPTED 1.25\n'
            elif stage['kind']=='global_resource':
                proof=common.read(folder/stage['proof']);receipt.update(initial_proof_sha256=proof['initial_proof_sha256'],
                    initial_acceptance_sha256=proof['initial_acceptance_sha256'],probability_panels=100,survivors=[20])
                terminal='GLOBAL_RESOURCES_ACCEPTED [20] 1.25\n'
            else:
                receipt.update(index=20,excluded=False,initial_proof_sha256=self.initial_sha,cycles=2,local_signed_rectangles=8*9216)
                terminal='PANEL_ACCEPTED 20 1.25\n'
            atomic_json(folder/stage['receipt'],receipt)
            if stage['kind']=='local':
                helper=base/'new_middle/stage_cache_v2';after=dict(hits=7,misses=1,size=1,maxsize=128)
                atomic_json(folder/'PANEL20_accept_CACHE_RUNTIME.json',dict(status='PASS_FRESH_NAMED_EXACT_LOCAL_CACHE',index=20,action='accept',
                    cache_before=dict(hits=0,misses=0,size=0,maxsize=128),cache_after=after,mathematical_cover_calls=8,
                    full_stage_evaluations=1,memoized_calls=7,wrapper_sha256=common.digest(folder/stage['script']),
                    original_checker_sha256=common.digest(folder/'acquire_panel.py'),helper_sha256=common.digest(helper/'exact_stage_cache.py'),
                    helper_review_sha256=common.digest(helper/'INDEPENDENT_REVIEW.json'),source_sha256=source_map,
                    output_sha256={n:common.digest(folder/n)for n in(stage['proof'],stage['receipt'])}))
                terminal+='PASS_FRESH_NAMED_EXACT_LOCAL_CACHE 20 accept '+str(after)+'\n'
        out=options['output_dir'];out.mkdir(parents=True);(out/'stdout.txt').write_text(terminal);(out/'stderr.txt').write_text('')
        launch=dict(argv=command,cwd=str(folder),output_dir=str(out),mode='untrusted_search',wall_seconds=float(evidence.WALL),
            cpu_seconds=evidence.CPU,memory_bytes=evidence.MEMORY,checkpoint_paths=[],disk_bytes=evidence.DISK,
            log_bytes=16*evidence.MIB,sample_seconds=.2,heartbeat_seconds=20.)
        observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,
            guard_scope=paths._group_scope(launch),stdout_path=str(out/'stdout.txt'),stderr_path=str(out/'stderr.txt'),
            stdout_sha256=common.digest(out/'stdout.txt'),stderr_sha256=common.digest(out/'stderr.txt'))
        atomic_json(out/'launch.json',launch);atomic_json(out/'supervisor-result.json',observed);return observed

    def complete(self,task=None,start=0):
        task=task or self.task
        for position in range(start,len(self.stages)):runner.execute(task,'b4',position,supervise=self.fake)

    def test_all_actions_and_aliases_complete_without_theorem_promotion(self):
        self.complete();checked=evidence.validate_completed(self.task,'b4')
        self.assertTrue(checked['conditional_acquisition_arithmetic_replayed'])
        for flag in('native_arithmetic_accepted','resource_interfaces_verified','count_forests_accepted','full_n25_verified','all_index_conclusion_verified'):
            self.assertIs(checked[flag],False)
        self.assertEqual(len(evidence.alias_bindings(self.task,'b4')),3)
        archive=runner.save_prefix(self.task,'b4',4,self.base/'cache');moved=self.base/'moved'
        runner.restore_prefix(archive,moved,'b4',4)
        self.assertEqual(evidence.validate_completed(moved,'b4'),checked)

    def test_constructed_prefix_restores_then_accepts_with_fresh_aliases(self):
        for position in range(2):runner.execute(self.task,'b4',position,supervise=self.fake)
        self.assertFalse((self.alias/'GLOBAL_RESOURCES_PROOF.json').exists())
        saved=runner.save_prefix(self.task,'b4',2,self.base/'cache');moved=self.base/'moved'
        runner.restore_prefix(saved,moved,'b4',2);self.complete(moved,start=2)
        self.assertTrue(evidence.validate_completed(moved,'b4')['conditional_acquisition_arithmetic_replayed'])
        first=common.read(moved/'ledgers/initial-accept.json');last=common.read(moved/'ledgers/local-20-accept.json')
        self.assertNotEqual(first['original_task_root'],last['original_task_root'])

    def test_stale_alias_parent_and_forged_cache_counts_rejected(self):
        self.complete();alias=self.alias/'GLOBAL_RESOURCES_ACCEPTED.json';old=alias.read_bytes();alias.write_text('{}')
        with self.assertRaises(ValueError):evidence.validate_completed(self.task,'b4')
        alias.write_bytes(old)
        cache=self.alias/'PANEL20_accept_CACHE_RUNTIME.json';packet=common.read(cache);packet['cache_after']['misses']=0;atomic_json(cache,packet)
        with self.assertRaises(ValueError):evidence.validate_completed(self.task,'b4')

    def test_mutated_fresh_timed_initial_edge_rejected(self):
        self.complete();glob=self.canonical/'GLOBAL_RESOURCES_PROOF.json';packet=common.read(glob)
        packet['initial_acceptance_sha256']='0'*64;atomic_json(glob,packet)
        with self.assertRaises(ValueError):evidence.artifact(self.task,'b4',self.stages[1])


if __name__=='__main__':unittest.main()
