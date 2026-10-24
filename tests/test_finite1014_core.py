"""Synthetic transport/epoch fixtures; archived math is trap bytes, never run."""
from __future__ import annotations
import copy
import io
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import Mock,patch
import zipfile
from be_replay import finite1014_core_sources as s,finite1014_core_evidence as e,finite1014_core as r


def put(path,packet):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(s.dump(packet));return s.digest(path)


class Core(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=s.ROOT.parent,prefix='t56c-');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.cache=self.root/'cache';self.cache.mkdir()
        initial='work/example/analytic/initial';resource='work/example/root/resource'
        cp=initial+'/n10/B0_RESULT.json';ap=initial+'/n10/B0_REPLAY_CHECKED.json'
        rp=resource+'/B0/CANDIDATE.json';ra=resource+'/B0/ACCEPTED.json'
        trap=b'raise AssertionError("Original mathematics must never be executed by local fixtures")\n'
        files={}
        for name in(initial+'/construct.py',initial+'/replay.py',resource+'/resources.py'):
            p=self.cache/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(trap);files[name]=s.digest(p)
        self.high='runs/upstream_HIGH_construct01/metadata.json';missing={self.high:'0'*64}
        prefix='runs/cutoff10_20261018/analytic/initial10_B0'
        for suffix in('_construct01','_replay01'):
            for n in('metadata.json','stdout.txt','stderr.txt'):missing[prefix+suffix+'/'+n]='1'*64
        supplied_own_captures={}
        for suffix in('_construct01','_replay01'):
            name=prefix+suffix+'/stderr.txt';path=self.cache/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b'')
            supplied_own_captures[name]=files[name]=s.digest(path);del missing[name]
        ip=initial+'/PREPARED.json';pp=resource+'/PREPARED.json'
        files[ip]=put(self.cache/ip,dict(status='ORIGINAL_INITIAL_PREPARED',inputs=dict(high_caps={'B0':'69/200'},rho=['1','11/10']),
            files_sha256={initial+'/construct.py':files[initial+'/construct.py'],self.high:missing[self.high]}))
        oldc=dict(status='COMPLETE_UNSEEDED_SIGNED_INITIAL10_14_CONDITIONAL',n=10,band='B0',K='0',q='99/1000',
            high_cap='69/200',profile=dict(grid=[12,12,6,3],radius='23/10',rho=['1','11/10']),
            stages=[dict(seconds=.1,input_raw=None if i==0 else'1',next_raw='1',next_D='1/2')for i in range(8)],
            export=dict(panels=[dict(index=i)for i in range(100)]),files_sha256={})
        files[cp]=put(self.cache/cp,oldc)
        olda=dict(status='PASS_FRESH_UNSEEDED_SIGNED_INITIAL10_14_REPLAY_CONDITIONAL',n=10,band='B0',candidate_sha256=files[cp],
            files_sha256={},fresh_complete_covers=9,signed_cells_per_cover=2592,original_probability_panels=100,
            malformed_controls=24,parser_controls=2,high_cap='69/200',full_cutoff_proved=False)
        files[ap]=put(self.cache/ap,olda)
        files[pp]=put(self.cache/pp,dict(status='ORIGINAL_RESOURCE_PREPARED',n=10,
            files_sha256={resource+'/resources.py':files[resource+'/resources.py'],ip:files[ip],cp:files[cp],ap:files[ap],**missing,**supplied_own_captures}))
        rows=[];rowpaths=[]
        for i in range(100):
            p=resource+f'/B0/rows/{i:03d}.json';files[p]=put(self.cache/p,dict(index=i,result='SYNTHETIC_NOT_A_PROOF'))
            rows.append(dict(n=10,band='B0',index=i,p=[str(e.Fraction(i,100)),str(e.Fraction(i+1,100))],path=f'rows/{i:03d}.json',sha256=files[p],status='SYNTHETIC'))
            rowpaths.append(p)
        oldr=dict(status='COMPLETE_CONDITIONAL_ACTUAL10_REFRESHED_RESOURCE_INVENTORY',n=10,band='B0',K='0',q='99/1000',
            initial_candidate_sha256=files[cp],initial_acceptance_sha256=files[ap],rows=rows,status_counts={'SYNTHETIC':100},
            files_sha256={},global_bound_proved=False)
        files[rp]=put(self.cache/rp,oldr)
        oldra=dict(status='PASS_FRESH_FULL_CONDITIONAL_ACTUAL10_REFRESHED_RESOURCE_REPLAY',n=10,band='B0',candidate_sha256=files[rp],
            rows=rows,status_counts={'SYNTHETIC':100},negative_controls=dict(malformed_inventories=12,parser_controls=2),
            timings_seconds=[.1]*100,files_sha256={},global_bound_proved=False)
        files[ra]=put(self.cache/ra,oldra)
        self.row=dict(case_id='n10-b0',n=10,band='B0',initial_directory=initial,resource_directory=resource,
            initial_candidate=cp,initial_receipt=ap,resource_candidate=rp,resource_receipt=ra,
            initial_capture_prefix=prefix,initial_prepared=ip,resource_prepared=pp,
            original_source_commitments=files|missing,own_outputs=[cp,ap,rp,ra,resource+'/B0/CONSTRUCT_TIMINGS.json']+rowpaths,
            complete_covers=9,signed_cells_per_cover=2592,probability_panels=100,
            initial_controls=dict(malformed_controls=24,parser_controls=2),resource_controls=dict(malformed_inventories=12,parser_controls=2))
        legacy=self.root/'proof/legacy.json';legacy.parent.mkdir();pin=put(legacy,dict(commitments={'synthetic':'2'*64}))
        self.plan=dict(cases=[self.row],source_files={name:dict(sha256=pin,bytes=(self.cache/name).stat().st_size)for name,pin in files.items()},
            unavailable_historical_captures=missing,legacy_commitments_file='proof/legacy.json',legacy_commitments_sha256=pin)
        self.impl=dict(synthetic_only='NO_ORIGINAL_MATH_EXECUTION')
        for target,name,value in((s,'ROOT',self.root),(s,'plan',Mock(return_value=self.plan)),(e,'implementation',Mock(return_value=self.impl)),
                                  (r.sys,'platform','linux'),(r.sys,'stdout',io.StringIO())):
            patcher=patch.object(target,name,value);patcher.start();self.addCleanup(patcher.stop)

    def fake(self,argv,*,cwd,output_dir,**kwargs):
        task=Path(output_dir).parent.parent;row=self.row;action=Path(output_dir).name;capsule=task/'capsule'
        oldkey={'initial_construct':'initial_candidate','initial_replay':'initial_receipt',
                'resource_construct':'resource_candidate','resource_accept':'resource_receipt'}[action]
        packet=s.read(task/'provenance'/row[oldkey],128*s.MIB)
        kind='initial'if action.startswith('initial_')else'resource';prep=row[kind+'_prepared']
        graph=dict(s.read(capsule/prep)['files_sha256']);graph[prep]=s.digest(capsule/prep)
        packet['files_sha256']=graph
        if action=='initial_construct':
            for stage in packet['stages']:stage['seconds']=.2
        elif action=='initial_replay':
            packet['candidate_sha256']=s.digest(capsule/row['initial_candidate']);packet['files_sha256']=s.input_map(task,row,action)
        elif action=='resource_construct':
            packet['initial_candidate_sha256']=s.digest(capsule/row['initial_candidate'])
            packet['initial_acceptance_sha256']=s.digest(capsule/row['initial_receipt'])
            for name in s.outputs(row,action)[2:]:
                p=capsule/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(task/'provenance'/name,p)
            put(capsule/s.outputs(row,action)[1],[.2]*100)
        else:
            packet['candidate_sha256']=s.digest(capsule/row['resource_candidate']);packet['timings_seconds']=[.2]*100
        if hasattr(self,'native_mutator'):self.native_mutator(action,packet)
        put(capsule/row[oldkey],packet);directory=Path(output_dir);directory.mkdir(parents=True)
        if action.startswith('initial_'):stdout=packet['status']+f" {row['n']} {row['band']} "+s.digest(capsule/row[oldkey])+'\n'
        else:stdout=('RESOURCE_CANDIDATE'if action=='resource_construct'else'RESOURCE_ACCEPTED')+' '+row['band']+' '+repr(packet['status_counts'])+' '+s.digest(capsule/row[oldkey])+'\n'
        (directory/'stdout.txt').write_bytes(stdout.encode());(directory/'stderr.txt').write_bytes(b'')
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,**kwargs)
        launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds'])
        launch['checkpoint_paths']=[str(p)for p in kwargs['checkpoint_paths']]
        if hasattr(self,'launch_mutator'):self.launch_mutator(action,launch)
        put(directory/'launch.json',launch);checkpoints=[]
        for path in kwargs['checkpoint_paths']:
            path=Path(path);copied=directory/'checkpoints'/path.relative_to(cwd);copied.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,copied)
            checkpoints.append(dict(source_path=str(path),exists=True,trusted_certificate=False,path=str(copied),bytes=path.stat().st_size,sha256=s.digest(path)))
        observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,
            elapsed_seconds=.1,maximum_sampled_group_RSS_bytes=10*s.MIB,maximum_sampled_group_CPU_seconds=.1,guard_scope=e.guard(),
            checkpoints=checkpoints,**{kind+suffix:value for kind in('stdout','stderr')for suffix,value in(
                ('_path',str(directory/(kind+'.txt'))),('_sha256',s.digest(directory/(kind+'.txt'))))})
        if hasattr(self,'observed_mutator'):self.observed_mutator(action,observed)
        finished=dict(event='linux_supervisor_finished',stage='untrusted_search',status=observed['status'],reason=observed['reason'],
                      elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
        put(directory/'progress.json',finished);(directory/'progress.jsonl').write_bytes(s.dump(finished).replace(b'\n',b'')+b'\n')
        put(directory/'supervisor-result.json',observed);return observed

    def complete(self,name='task'):
        task=self.root/name
        with patch.object(r.linux_supervisor,'run',side_effect=self.fake)as child,patch.object(r,'Follow'):
            checked=r.execute(self.row['case_id'],self.cache,task,root=self.root)
        self.assertEqual(child.call_count,4);return task,checked

    def test_full_four_original_calls_and_all_other_proof_flags_false(self):
        task,checked=self.complete();self.assertEqual(checked['summary']['native_actions'],4)
        self.assertEqual(checked['summary']['resource_panels'],100)
        self.assertEqual([x['action']for x in s.read(task/'CASE_OBSERVED.json')['actions']],list(s.ACTIONS))
        for flag in e.FLAGS:self.assertIs(checked[flag],False)
        self.assertTrue(checked['conditional_core_arithmetic_completed'])

    def test_strict_data_projection_preserves_caps_domains_and_all_original_provenance(self):
        task,_=self.complete();epoch=s.read(task/s.EPOCH)
        for kind in('initial','resource'):
            name=self.row[kind+'_prepared'];old=s.read(task/'provenance'/name);new=s.read(task/'capsule'/name)
            self.assertEqual({k:v for k,v in old.items()if k!='files_sha256'},{k:v for k,v in new.items()if k!='files_sha256'})
            self.assertNotIn(self.high,new['files_sha256']);self.assertEqual(epoch['prepared_derivations'][name]['changes'][self.high]['reason'],'UNACQUIRED_NOT_STAGED')
        self.assertEqual((task/'provenance'/self.row['initial_prepared']).read_bytes(),(self.cache/self.row['initial_prepared']).read_bytes())
        self.assertFalse(epoch['upstream_HIGH_acquired'])

    def test_real_constructor_capture_has_current_command_cwd_and_complete_source_map(self):
        task,_=self.complete();request=s.read(task/'SOURCES.json');row=self.row
        p=task/'capsule'/s.capture_relative(row,'initial_construct')/'metadata.json';m=s.read(p)
        self.assertEqual(m['command'][1:],['-B','../construct.py','10','B0'])
        self.assertEqual(m['cwd'],e.original(request,'capsule/'+s.cwd_relative(row,'initial_construct')))
        self.assertEqual(m['input_sha256'],s.relative_inputs(row,'initial_construct',s.input_map(task,row,'initial_construct')))
        self.assertFalse(m['historical_capture_impersonated'])

    def test_source_math_mutation_unknown_files_and_omitted_doc_fail_closed(self):
        task=self.root/'prepared';s.prepare(self.row['case_id'],self.cache,task)
        p=task/'capsule'/self.row['initial_directory']/'construct.py';p.write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify(task)
        shutil.copyfile(self.cache/self.row['initial_directory']/'construct.py',p)
        (task/'capsule/unbound.py').write_bytes(b'bad')
        with self.assertRaises(ValueError):s.verify(task)

    def test_supplied_historical_empty_stderr_never_populates_current_capture_destinations(self):
        task=self.root/'fresh-capture-case';request=s.prepare(self.row['case_id'],self.cache,task)
        for action in s.ACTIONS:
            directory=s.capture_relative(self.row,action)
            self.assertFalse((task/'capsule'/directory).exists())
        for action in s.ACTIONS[:2]:
            name=s.capture_relative(self.row,action)+'/stderr.txt'
            self.assertIn(name,request['original_provenance']);self.assertNotIn(name,request['static_inputs'])
            self.assertEqual((task/'provenance'/name).read_bytes(),b'')
        s.verify(task)

    def test_current_math_or_control_changes_never_complete_even_with_coherent_captures(self):
        for i,change in enumerate((lambda a,p:p.update(high_cap='1')if a=='initial_construct'else None,
                                   lambda a,p:p.update(malformed_controls=23)if a=='initial_replay'else None,
                                   lambda a,p:p['rows'].pop()if a=='resource_construct'else None,
                                   lambda a,p:p['negative_controls'].update(parser_controls=0)if a=='resource_accept'else None)):
            self.native_mutator=change
            with self.assertRaises((ValueError,KeyError,IndexError)):self.complete('badmath'+str(i))
            self.assertFalse((self.root/('badmath'+str(i))/'CASE_COMPLETED.json').exists())

    def test_wrong_argv_cwd_budget_boolean_exit_and_missing_stopped_proof_rejected(self):
        for i,change in enumerate((lambda a,p:p.update(returncode=False),lambda a,p:p.update(checkpoints=[]),
                                   lambda a,p:p['guard_scope'].update(proof_acceptance=True))):
            self.observed_mutator=change
            with self.assertRaises(ValueError):self.complete('badexec'+str(i))
        del self.observed_mutator
        self.launch_mutator=lambda a,p:p['argv'].append('--quick')
        with self.assertRaises(ValueError):self.complete('badargv')

    def test_after_stop_source_captures_and_stderr_hashes_are_revalidated(self):
        task,_=self.complete();p=task/'executions/initial_replay/stdout.txt';p.write_bytes(b'changed')
        with self.assertRaises(ValueError):e.validate_completed(task)
        task,_=self.complete('capture2');p=task/'capsule'/s.capture_relative(self.row,'initial_construct')/'metadata.json'
        m=s.read(p);m['cwd']='/historical/other';put(p,m)
        with self.assertRaises(ValueError):e.validate_completed(task)

    def test_relocation_preserves_native_receipts_and_absolute_capture_context(self):
        task,checked=self.complete();other=self.root/'relocated';shutil.copytree(task,other)
        before={p.relative_to(other).as_posix():p.read_bytes()for p in other.rglob('*')if p.is_file()}
        self.assertEqual(e.validate_completed(other),checked)
        self.assertEqual(before,{p.relative_to(other).as_posix():p.read_bytes()for p in other.rglob('*')if p.is_file()})

    def test_complete_case_cache_only_skips_four_calls_after_full_revalidation(self):
        task,checked=self.complete();cache=self.root/'saved';out=r.save_completed(task,cache)
        with patch.object(r.linux_supervisor,'run',side_effect=AssertionError('No original call on completed cache'))as child:
            got=r.restore_completed(self.row['case_id'],cache,self.root/'restore',root=self.root)
        self.assertEqual(got[1],checked);child.assert_not_called()
        Path(out['path']).with_suffix('.zip.sha256').write_bytes(b'bad')
        self.assertIsNone(r.restore_completed(self.row['case_id'],cache,self.root/'bad-restore',root=self.root))

    def test_partial_case_unknown_zip_and_false_complete_scope_rejected(self):
        z=Mock();z.infolist.return_value=[zipfile.ZipInfo('../escape')]
        with self.assertRaises(ValueError):r.cache_members(z)
        z.infolist.return_value=[zipfile.ZipInfo('SOURCES.json')]
        with self.assertRaises(ValueError):r.cache_members(z)
        task,_=self.complete();p=task/'CASE_COMPLETED.json';d=s.read(p);d['HIGH_acquisition_verified']=True;put(p,d)
        with self.assertRaises(ValueError):e.validate_completed(task)


class ActualPlan(unittest.TestCase):
    def test_all10_literal_cases_40calls_fine_grid_402controls_and3072provenance(self):
        d=s.plan();self.assertEqual(len(d['source_files']),1558)
        self.assertEqual(sum(x['bytes']for x in d['source_files'].values()),130269328)
        self.assertEqual(sum(sum(r['initial_controls'].values())+sum(r['resource_controls'].values())for r in d['cases']),402)
        self.assertEqual({r['case_id']for r in d['cases']},{f'n{n}-{b}'for n in range(10,15)for b in('b0','bn')})
        self.assertEqual([r['signed_cells_per_cover']for r in d['cases']if r['case_id']=='n10-bn'],[10368])
        self.assertEqual({a['name']for a in d['assets']},{'cutoff5_10_15.zip','cutoff5_20261020.zip'})
        self.assertEqual(len(s.read(s.ROOT/d['legacy_commitments_file'],4*s.MIB)['commitments']),3072)


if __name__=='__main__':unittest.main()
