"""Synthetic source/transport/cache fixtures; never execute original math."""
from copy import deepcopy
from fractions import Fraction as F
import importlib.util
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from be_replay import aux24_evidence as paths,count_task as common
from be_replay import high_beta3_acquisition as runner,high_beta3_acquisition_sources as source,high_beta3_acquisition_evidence as evidence
from be_replay.colab_batch import atomic_json

B=source.BRANCH

def temporary():
    parent=Path(__file__).resolve().parents[1]/'work/test-tmp'
    parent.mkdir(parents=True,exist_ok=True)
    return tempfile.TemporaryDirectory(dir=parent)

class Catalog(unittest.TestCase):
    def test_published_catalog_has_stable_lf_bytes(self):
        path=Path(__file__).resolve().parents[1]/'proof/high_beta3_acquisition_sources.json'
        raw=path.read_bytes()
        self.assertNotIn(b'\r',raw)
        self.assertTrue(raw.endswith(b'\n'))
        self.assertEqual(hashlib.sha256(raw).hexdigest(),source.CATALOG_SHA)

    def test_exact_final_selection(self):
        p=source.definition();stages=source.stages();rows=source.selected()
        self.assertEqual(len(rows),94);self.assertEqual(len(stages),14)
        self.assertEqual([s['action']for s in stages[:3]],['accept','construct','accept'])
        self.assertEqual([s['index']for s in stages[3:]if s['cached']],[16,22,23,24,25,26])
        self.assertEqual([s['index']for s in stages[3:]if not s['cached']],[17,18,19,20,21])
        self.assertEqual(sum(r['mathematical_cover_calls']for r in p['locals']),241)
        self.assertFalse(any('ACCEPTED'in Path(n).name or Path(n).name=='GLOBAL_RESOURCES_PROOF.json'for n in rows))
        self.assertEqual(len(source.selection_sha()),64)
        with self.assertRaises(ValueError):source.definition('b4')

    def test_projection_only_rebinds_explicit_transport(self):
        with temporary()as t:
            task=Path(t);directory=source.source.PREFIX+'cached';name=directory+'/FROZEN_SOURCES.json'
            mapping={'original/kernel.py':'a'*64,'unrelated/OLD_ACCEPTED.json':'b'*64}
            original=dict(schema='NAMED_HIGH_BETA3_EXACT_STAGE_CACHE_V1',files_sha256=mapping,scope='old')
            path=task/'source'/name;path.parent.mkdir(parents=True);atomic_json(path,original);raw=path.read_bytes()
            packet=dict(cache_directory=directory,source_file_rows=[dict(member=source.source.PREFIX+'original/kernel.py',sha256='a'*64),dict(member=name,sha256=common.digest(path))])
            with patch.object(source,'definition',return_value=packet):
                projection=source.cache_projection(task)
                new=json.loads(projection['cached/FROZEN_SOURCES.json']);epoch=json.loads(projection['cached/CACHE_SOURCE_EPOCH.json'])
                self.assertEqual(new['files_sha256'],{'original/kernel.py':'a'*64})
                self.assertIs(epoch['historical_manifest_acceptance_claimed'],False)
                self.assertEqual(path.read_bytes(),raw)
                packet['source_file_rows'][0]['sha256']='c'*64
                with self.assertRaises(ValueError):source.cache_projection(task)

    def test_notebook(self):
        path=Path(__file__).resolve().parents[1]/'tools/make_high_beta3_acquisition_notebook.py'
        spec=importlib.util.spec_from_file_location('high_beta3_notebook',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        nb=module.build('a'*40)
        for cell in nb['cells']:
            if cell['cell_type']=='code':compile(''.join(cell['source']),'49','exec')
        text=json.dumps(nb);self.assertIn('high_beta3_acquisition',text);self.assertIn('high-beta3-acquisition',text)
        with self.assertRaises(ValueError):module.build('main')


class SyntheticChain(unittest.TestCase):
    """Real evidence checks on fake five-stage artifacts, no source execution."""
    def setUp(self):
        self.temp=temporary();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name);self.task=self.base/'task';self.task.mkdir()
        self.stages=[dict(name='initial-accept',kind='initial',action='accept',folder='fixture/canonical',script='initial_beta3.py',args=['accept'],proof='INITIAL_BETA3_PROOF.json',receipt='INITIAL_BETA3_ACCEPTED.json')]
        for action in('construct','accept'):
            self.stages.append(dict(name='global_resource-'+action,kind='global_resource',action=action,folder='fixture/canonical',script='global_resources.py',args=[action],proof='GLOBAL_RESOURCES_PROOF.json',receipt='GLOBAL_RESOURCES_ACCEPTED.json'if action=='accept'else None))
        for index,cached in[(17,False),(22,True)]:
            self.stages.append(dict(name=f'local-{index}-accept',kind='local',action='accept',index=index,cached=cached,
                folder='fixture/cache'if cached else'fixture/canonical',script='acquire_panel_cached.py'if cached else'acquire_panel.py',
                args=['accept',str(index)],proof=f'PANEL{index}_PROOF.json',receipt=f'PANEL{index}_ACCEPTED.json'))
        self.profile=dict(n=25,fixture='Synthetic only');self.controls=['synthetic corruption control']
        self.packet=dict(branch=B,canonical_directory=source.source.PREFIX+'fixture/canonical',cache_directory=source.source.PREFIX+'fixture/cache',
            cache_helper_directory=source.source.PREFIX+'fixture/helper',profile=self.profile,contact_allowance='1366497/14000000',
            initial=dict(expected_status='PASS_FRESH_EXACT_HIGH25_BETA3_INITIAL',negative_controls=self.controls),
            global_resource=dict(expected_status='PASS_FRESH_EXACT_BETA3_GLOBAL_RESOURCES',negative_controls=self.controls,survivors=[17,22]),
            locals=[dict(index=i,cycle_limit=8,cycles=2,mathematical_cover_calls=8,excluded=False,
                expected_status='PASS_FRESH_EXACT_HIGH25_BETA3_PANEL_ACQUISITION',negative_controls=self.controls)for i in(17,22)])
        base=evidence.root(self.task);canonical=base/'fixture/canonical';cache=base/'fixture/cache';helper=base/'fixture/helper'
        for folder in(canonical,cache,helper):folder.mkdir(parents=True)
        self.canonical,self.cache,self.helper=canonical,cache,helper
        for script in('initial_beta3.py','global_resources.py','acquire_panel.py'):(canonical/script).write_text("raise RuntimeError('Never execute synthetic source')\n")
        (cache/'acquire_panel_cached.py').write_text("raise RuntimeError('Never execute synthetic source')\n")
        (helper/'exact_stage_cache.py').write_text("raise RuntimeError('Never import synthetic helper')\n")
        atomic_json(helper/'INDEPENDENT_REVIEW.json',dict(synthetic=True))
        atomic_json(cache/'FROZEN_SOURCES.json',dict(synthetic=True));atomic_json(cache/'CACHE_SOURCE_EPOCH.json',dict(synthetic=True))
        im={'initial_beta3.py':common.digest(canonical/'initial_beta3.py')};pm={n:common.digest(canonical/n)for n in('initial_beta3.py','global_resources.py','acquire_panel.py')}
        atomic_json(canonical/'COPY_MANIFEST.json',dict(files=im));atomic_json(canonical/'PANEL_COPY_MANIFEST.json',dict(files=pm))
        self.cover=dict(total=9216,active=1,excluded=9215,reasons=dict(synthetic=9215),panels=[dict(pl=str(F(i,100)),pu=str(F(i+1,100)))for i in range(100)])
        atomic_json(canonical/'INITIAL_BETA3_PROOF.json',dict(schema='EXACT_HIGH25_BETA3_INITIAL_COARSENED_HIGH_V1',profile=self.profile,source_sha256=im,
            contact_allowance='1366497/14000000',stages=[dict(cover=self.cover)for _ in range(11)],export=self.cover))
        self.initial_sha=common.digest(canonical/'INITIAL_BETA3_PROOF.json')
        self.global_rows=[dict(index=i,derivation=dict(excluded=i not in(17,22)))for i in range(100)]
        for index,folder in[(17,canonical),(22,cache)]:
            atomic_json(folder/f'PANEL{index}_PROOF.json',dict(schema='EXACT_HIGH25_BETA3_PANEL_FINITE_RESOURCES_V1',profile=self.profile,index=index,
                p_interval=[str(F(index,100)),str(F(index+1,100))],source_sha256=pm,cycle_limit=8,initial_covers_per_cycle=4,mean_floor_grid=10**12,
                initial_proof_sha256=self.initial_sha,excluded=False,global_resource=self.global_rows[index],
                cycles=[dict(cycle=i+1,profile=self.profile,stages=[dict(input_raw='1',input_D='1',cover=self.cover)for _ in range(4)])for i in range(2)]))
        self.rows={};self.sealed={}
        for path in base.rglob('*'):
            if not path.is_file():continue
            name=path.relative_to(base).as_posix();row=dict(bytes=path.stat().st_size,sha256=common.digest(path),kind='source')
            self.sealed[name]=row
            if not name.endswith('CACHE_SOURCE_EPOCH.json'):
                self.rows[source.source.PREFIX+name]=row
                target=self.task/'source'/source.source.PREFIX/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
        for filename in(source.source.MANIFEST,source.source.TASK):atomic_json(self.task/filename,dict(synthetic=True))
        for name,value in [('stages',self.stages),('definition',self.packet),('selected',self.rows),('epoch_rows',self.sealed),('verify',{})]:
            p=patch.object(source,name,return_value=value);p.start();self.addCleanup(p.stop)

    def fake(self,command,**options):
        stage=next(s for s in self.stages if s['script']==Path(command[3]).name and s['args']==command[4:])
        folder=options['cwd']
        # Resolve current relocated task from the command's fixed epoch layout.
        task=next(p for p in folder.parents if p.name=='epoch').parent;base=evidence.root(task);canonical=base/'fixture/canonical'
        source_map=common.read(canonical/('COPY_MANIFEST.json'if stage['kind']=='initial'else'PANEL_COPY_MANIFEST.json'))['files']
        if stage['kind']=='global_resource'and stage['action']=='construct':
            atomic_json(folder/stage['proof'],dict(schema='EXACT_HIGH25_BETA3_GLOBAL_RESOURCES_V1',profile=self.profile,source_sha256=source_map,
                initial_proof_sha256=self.initial_sha,initial_acceptance_sha256=common.digest(canonical/'INITIAL_BETA3_ACCEPTED.json'),rows=self.global_rows))
            terminal='GLOBAL_RESOURCES_CONSTRUCTED 1.25\n'
        else:
            section=self.packet['locals'][0]if stage['kind']=='local'else self.packet[stage['kind']]
            receipt=dict(status=section['expected_status'],proof_sha256=common.digest(folder/stage['proof']),checker_sha256=common.digest(canonical/('acquire_panel.py'if stage['kind']=='local'else stage['script'])),source_sha256=source_map,negative_controls=self.controls,seconds=1.25)
            if stage['kind']=='initial':receipt.update(profile=self.profile,signed_rectangles=110592,probability_panels=100);terminal='INITIAL_BETA3_ACCEPTED 1.25\n'
            elif stage['kind']=='global_resource':
                proof=common.read(folder/stage['proof']);receipt.update(initial_proof_sha256=proof['initial_proof_sha256'],initial_acceptance_sha256=proof['initial_acceptance_sha256'],probability_panels=100,survivors=[17,22]);terminal='GLOBAL_RESOURCES_ACCEPTED [17, 22] 1.25\n'
            else:
                receipt.update(index=stage['index'],excluded=False,initial_proof_sha256=self.initial_sha,cycles=2,local_signed_rectangles=8*9216)
                terminal=f"PANEL_ACCEPTED {stage['index']} 1.25\n"
            atomic_json(folder/stage['receipt'],receipt)
            if stage['kind']=='local'and stage['cached']:
                index=stage['index'];helper=base/'fixture/helper';after=dict(hits=7,misses=1,size=1,maxsize=128)
                atomic_json(folder/f'local_{index}_accept.runtime.json',dict(status='PASS_NAMED_CACHED_HIGH_BETA3_COMPLETE_LOCAL_EXECUTION',index=index,action='accept',
                    fresh_cache_before=dict(hits=0,misses=0,size=0,maxsize=128),cache_after=after,mathematical_cover_calls=8,distinct_complete_argument_keys=1,
                    original_full_stage_evaluations=1,memoized_identical_calls=7,actual_wrapper_sha256=common.digest(folder/stage['script']),original_checker_sha256=common.digest(canonical/'acquire_panel.py'),
                    helper_sha256=common.digest(helper/'exact_stage_cache.py'),helper_review_sha256=common.digest(helper/'INDEPENDENT_REVIEW.json'),
                    parent_snapshot_sha256=common.digest(folder/'PARENTS_BOUND.json'),frozen_sources_sha256=common.digest(folder/'FROZEN_SOURCES.json'),output_sha256={n:common.digest(folder/n)for n in(stage['proof'],stage['receipt'])}))
                terminal+=f'PASS_NAMED_CACHED_HIGH_BETA3_COMPLETE_LOCAL_EXECUTION accept {index} '+str(after)+'\n'
        out=options['output_dir'];out.mkdir(parents=True);(out/'stdout.txt').write_text(terminal);(out/'stderr.txt').write_text('')
        launch=dict(argv=command,cwd=str(folder),output_dir=str(out),mode='untrusted_search',wall_seconds=float(evidence.WALL),cpu_seconds=evidence.CPU,memory_bytes=evidence.MEMORY,checkpoint_paths=[],disk_bytes=evidence.DISK,log_bytes=16*evidence.MIB,sample_seconds=.2,heartbeat_seconds=20.)
        observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,guard_scope=paths._group_scope(launch),stdout_path=str(out/'stdout.txt'),stderr_path=str(out/'stderr.txt'),stdout_sha256=common.digest(out/'stdout.txt'),stderr_sha256=common.digest(out/'stderr.txt'))
        atomic_json(out/'launch.json',launch);atomic_json(out/'supervisor-result.json',observed);return observed

    def complete(self,task=None,start=0,end=None):
        for i in range(start,len(self.stages)if end is None else end):runner.execute(task or self.task,B,i,supervise=self.fake)

    def test_full_chain_and_relocated_cache(self):
        self.complete();checked=evidence.validate_completed(self.task)
        self.assertEqual(checked['selected_full_actions'],5)
        for flag in('native_arithmetic_accepted','resource_interfaces_verified','count_forests_accepted','full_n25_verified','all_index_conclusion_verified'):self.assertIs(checked[flag],False)
        saved=runner.save_prefix(self.task,B,5,self.base/'cache');moved=self.base/'moved';runner.restore_prefix(saved,moved,B,5)
        self.assertEqual(checked,evidence.validate_completed(moved))

    def test_restore_constructed_prefix_then_accept(self):
        self.complete(end=2);saved=runner.save_prefix(self.task,B,2,self.base/'cache');moved=self.base/'moved'
        runner.restore_prefix(saved,moved,B,2);self.complete(moved,start=2)
        self.assertTrue(evidence.validate_completed(moved)['conditional_acquisition_arithmetic_replayed'])
        self.assertNotEqual(common.read(moved/'ledgers/initial-accept.json')['original_task_root'],common.read(moved/'ledgers/local-22-accept.json')['original_task_root'])

    def test_partial_is_not_complete(self):
        self.complete(end=4)
        with self.assertRaises((ValueError,FileNotFoundError)):evidence.validate_completed(self.task)

    def test_timed_parent_hash_and_alias_tampering(self):
        self.complete();path=self.canonical/'GLOBAL_RESOURCES_PROOF.json';raw=path.read_bytes();p=common.read(path);p['initial_acceptance_sha256']='0'*64;atomic_json(path,p)
        with self.assertRaises(ValueError):evidence.artifact(self.task,B,self.stages[1])
        path.write_bytes(raw);(self.cache/'INITIAL_BETA3_ACCEPTED.json').write_text('{}')
        with self.assertRaises(ValueError):evidence.validate_completed(self.task)

    def test_empty_cache_counts_and_actual_receipt_identity(self):
        self.complete();path=self.cache/'local_22_accept.runtime.json';raw=path.read_bytes();p=common.read(path);p['fresh_cache_before']['size']=1;atomic_json(path,p)
        with self.assertRaises(ValueError):evidence.artifact(self.task,B,self.stages[-1])
        path.write_bytes(raw);p=common.read(path);p['output_sha256']['PANEL22_ACCEPTED.json']='0'*64;atomic_json(path,p)
        with self.assertRaises(ValueError):evidence.artifact(self.task,B,self.stages[-1])
        path.write_bytes(raw);receipt=self.cache/'PANEL22_ACCEPTED.json';p=common.read(receipt);p['negative_controls']=[];atomic_json(receipt,p)
        with self.assertRaises(ValueError):evidence.artifact(self.task,B,self.stages[-1])

    def test_captures_and_launches_bound_not_embedded_only(self):
        self.complete();out=self.task/'execution/local-22-accept';p=common.read(out/'supervisor-result.json');(out/'stderr.txt').write_text('warning')
        with self.assertRaises(ValueError):evidence.validate_completed(self.task)
        (out/'stderr.txt').write_text('');p=common.read(out/'launch.json');p['cpu_seconds']=True;atomic_json(out/'launch.json',p)
        with self.assertRaises(ValueError):evidence.validate_completed(self.task)

    def test_rehashed_stderr_and_false_guard_promotion_rejected(self):
        self.complete(end=1);stage=self.stages[0];out=self.task/'execution'/stage['name']
        report=common.read(self.task/'ledgers'/str(stage['name']+'.json'))
        (out/'stderr.txt').write_text('warning\n');observed=common.read(out/'supervisor-result.json')
        observed['stderr_sha256']=common.digest(out/'stderr.txt');atomic_json(out/'supervisor-result.json',observed);report['observed']=observed
        with self.assertRaises(ValueError):evidence.transport(self.task,B,stage,report)
        (out/'stderr.txt').write_text('');observed['stderr_sha256']=common.digest(out/'stderr.txt')
        observed['guard_scope']['aggregate_kernel_memory_limit']=True;atomic_json(out/'supervisor-result.json',observed)
        with self.assertRaises(ValueError):evidence.transport(self.task,B,stage,report)

    def test_rehashed_wrong_terminal_and_incompatible_cache_rejected(self):
        self.complete(end=1);stage=self.stages[0];out=self.task/'execution'/stage['name']
        report=common.read(self.task/'ledgers'/str(stage['name']+'.json'));stdout=out/'stdout.txt';original=stdout.read_bytes()
        stdout.write_text('INITIAL_BETA3_CONSTRUCTED 1.25\n');observed=common.read(out/'supervisor-result.json');saved=deepcopy(observed)
        observed['stdout_sha256']=common.digest(stdout);atomic_json(out/'supervisor-result.json',observed);report['observed']=observed
        with self.assertRaises(ValueError):evidence.transport(self.task,B,stage,report)
        stdout.write_bytes(original);atomic_json(out/'supervisor-result.json',saved)
        archive=runner.save_prefix(self.task,B,1,self.base/'cache')
        with zipfile.ZipFile(archive)as z:rows=[(i.filename,z.read(i))for i in z.infolist()]
        with zipfile.ZipFile(archive,'w')as z:
            for n,b in rows:
                if n=='COMPLETED_PREFIX.json':
                    p=json.loads(b);p['implementation']['linux_supervisor.py']='0'*64;b=json.dumps(p).encode()
                z.writestr(n,b)
        archive.with_suffix('.zip.sha256').write_text(common.digest(archive)+'  '+archive.name+'\n')
        target=self.base/'incompatible'
        with self.assertRaises(ValueError):runner.restore_prefix(archive,target,B,1)
        self.assertFalse(target.exists())

    def test_safe_restore_rejects_changed_source_and_traversal(self):
        self.complete(end=1);saved=runner.save_prefix(self.task,B,1,self.base/'cache')
        with zipfile.ZipFile(saved)as z:rows=[(i.filename,z.read(i))for i in z.infolist()]
        for suffix,changed in [('source',[(n,b'corrupt'if n.endswith('initial_beta3.py')else b)for n,b in rows]),('traversal',rows+[('../escape',b'bad')])]:
            archive=self.base/(suffix+'.zip')
            with zipfile.ZipFile(archive,'w')as z:
                for n,b in changed:z.writestr(n,b)
            archive.with_suffix('.zip.sha256').write_text(common.digest(archive)+'  '+archive.name+'\n')
            target=self.base/('restore-'+suffix)
            with self.assertRaises(ValueError):runner.restore_prefix(archive,target,B,1)
            self.assertFalse(target.exists())

if __name__=='__main__':unittest.main()
