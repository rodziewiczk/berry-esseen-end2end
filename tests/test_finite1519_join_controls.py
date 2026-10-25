"""Synthetic six-control OS-capture/cache traps; no original program executes."""
from copy import deepcopy
from hashlib import sha256
import io,json,stat,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
from be_replay import finite1519_join_controls as run,finite1519_join_control_sources as src
from be_replay import finite1519_join_control_evidence as ev,finite1039_count_evidence as count_ev,linux_supervisor as sup


def put(path,raw):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw);return src.digest(path)


class SixControls(unittest.TestCase):
 def setUp(self):
  scratch=src.ROOT/'work/finite1519-join-fixtures';scratch.mkdir(parents=True,exist_ok=True)
  self.tmp=tempfile.TemporaryDirectory(dir=scratch);self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.cache=self.root/'cache';self.logs=self.root/'batch';self.logs.mkdir();self.calls=0
  self.upstream=self.root/'upstream';d='fixture/count56';files={}
  for name in('contract.json','candidate.json','ACCEPTED.json'):
   raw=src.encoded(dict(synthetic=name,not_a_mathematical_result=True));files[name]=put(self.upstream/'capsule'/d/name,raw)
  for name in('STAGE_OBSERVED.json','STAGE_COMPLETED.json'):put(self.upstream/name,b'{"synthetic": true}\n')
  self.checked=dict(job_id='n15.B0.p56.3ccb81760515',conditional_arithmetic_completed=True,synthetic_fixture_only=True)
  fixture=dict(job_id=self.checked['job_id'],directory=d,catalog_sha256='e'*64,contract_name='contract.json',forest_name='candidate.json',
   acceptance_name='ACCEPTED.json',contract_sha256=files['contract.json'],forest_sha256=files['candidate.json'])
  rawfiles={};cases=[];references={};previous=None
  for action in src.IDS:
   directory='work/synthetic/'+action;script=directory+'/check.py';output=directory+'/CHECKED.json'
   rawfiles[script]=b'raise AssertionError("Original mathematical trap must not execute locally")\n'
   inputs={script:sha256(rawfiles[script]).hexdigest()}
   if previous:inputs[previous['output']]=references[previous['id']]['pin']
   generated={}
   if action in('contact-high','compensated-high'):
    name=directory+'/engine/math.py';rawfiles[name]=b'# unchanged native-created synthetic helper\n';generated[name]=dict(bytes=len(rawfiles[name]),sha256=sha256(rawfiles[name]).hexdigest());inputs[name]=generated[name]['sha256']
   if action=='join-geometry':
    for key in('contract_name','forest_name','acceptance_name'):
     name='work/'+d+'/'+fixture[key];rawfiles[name]=(self.upstream/'capsule'/d/fixture[key]).read_bytes();inputs[name]=sha256(rawfiles[name]).hexdigest()
   reference=dict(status='PASS_SYNTHETIC_'+action,all_rows=3,files_sha256=inputs)
   if action=='join-geometry':reference['geometry_mutations_rejected']=['a','b']
   raw=src.encoded(reference);rawfiles[output]=raw;references[action]=dict(raw=raw,pin=sha256(raw).hexdigest())
   row=dict(id=action,script=script,output=output,cwd=directory,command_tail=['-B','check.py'],original_python_sha256=inputs[script],
    dependencies=[previous['id']]if previous else[],generated_engine_copies=generated,input_reference_graph=inputs,
    expected_reference_fields=dict(status=reference['status'],all_rows=3),reference=dict(bytes=len(raw),sha256=sha256(raw).hexdigest()))
   cases.append(row);previous=row
  plan=dict(source_files={n:dict(bytes=len(raw),sha256=sha256(raw).hexdigest())for n,raw in rawfiles.items()},
   original_files_sha256={n:sha256(raw).hexdigest()for n,raw in rawfiles.items()},metadata_documents=[],cases=cases,
   fresh_geometry_fixture=fixture,own_outputs_never_staged_from_history=[r['output']for r in cases],
   generated_engine_copies_not_staged_before_native_calls=[n for r in cases for n in r['generated_engine_copies']])
  for name,raw in rawfiles.items():put(self.cache/'original'/name,raw)
  for action,row in references.items():put(self.cache/'reference'/(action+'.json'),row['raw'])
  put(self.cache/'SOURCE_CACHE.json',src.encoded(dict(schema='FINITE1519_JOIN_CONTROL_CACHE_V1',source_plan_sha256=src.PLAN_SHA256,files=src.cache_inventory(plan),**src.FALSE_FLAGS)))
  self.plan=plan;self.references=references;self.addCleanup(patch.stopall)
  patch.object(src,'plan',return_value=plan).start()
  patch.object(count_ev,'validate_completed',return_value=self.checked).start()

 def fake(self,argv,**kw):
  self.calls+=1;directory=Path(kw['output_dir']);task=directory.parent.parent;action=directory.name;row=src.case(action)
  prior={}
  for previous in src.cases():
   if previous['id']==action:break
   prior[previous['id']]=dict(output_sha256=src.digest(task/'capsule'/previous['output']))
  acceptance=ev.fixture(task);inputs=src.input_map(task,action,validated_prior_actions=prior,fixture_acceptance_sha256=acceptance)
  for name in row['generated_engine_copies']:put(task/'capsule'/name,(self.cache/'original'/name).read_bytes())
  value=src.parsed(self.references[action]['raw']);value['files_sha256']=src.output_graph(task,action,inputs)
  output=task/'capsule'/row['output'];put(output,src.encoded(value))
  if action=='resource-range':text=value['status']+' '+src.digest(output)
  elif action=='join-geometry':text=value['status']+' '+str(len(value['geometry_mutations_rejected']))+' '+src.digest(output)
  else:
   omitted={'finite-high':{'quartic_rows','modulus_rows','files_sha256'},'contact-high':{'rows','files_sha256'},'compensated-high':{'rows','files_sha256'},'count-range':set()}[action]
   text=json.dumps({k:v for k,v in value.items()if k not in omitted})
  config=sup._settings(argv,kw['cwd'],directory,kw['wall_seconds'],kw['cpu_seconds'],kw['memory_bytes'],kw['checkpoint_paths'],kw['mode'],.2,kw['disk_bytes'],kw['log_bytes']);config['heartbeat_seconds']=20.0
  put(directory/'launch.json',src.encoded(config));put(directory/'stdout.txt',(text+'\n').encode());put(directory/'stderr.txt',b'')
  observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,
   elapsed_seconds=.01,maximum_sampled_group_RSS_bytes=4096,maximum_sampled_group_CPU_seconds=.001,guard_scope=ev.guard(),
   stdout_path=str(directory/'stdout.txt'),stdout_sha256=src.digest(directory/'stdout.txt'),stderr_path=str(directory/'stderr.txt'),stderr_sha256=src.digest(directory/'stderr.txt'),checkpoints=sup._capture_checkpoints(config))
  finished=dict(event='linux_supervisor_finished',stage='untrusted_search',status='completed',reason=None,elapsed_seconds=.01,proof_accepted=False)
  put(directory/'progress.json',src.encoded(finished));put(directory/'progress.jsonl',(json.dumps(finished)+'\n').encode());put(directory/'supervisor-result.json',src.encoded(observed))
  return observed

 def execute(self,name='task',fake=None):
  task=self.root/name
  with patch.object(run.sys,'platform','linux'),patch.object(run.linux_supervisor,'run',side_effect=fake or self.fake),patch.object(run,'Follow',side_effect=lambda *a,**k:io.StringIO()):
   checked=run.execute(self.cache,task,root=self.logs,upstream_count56=self.upstream)
  return task,checked

 def test_full_six_actions_current_fixture_and_relocated_cache(self):
  task,checked=self.execute();self.assertEqual(self.calls,6);self.assertTrue(checked['conditional_controls_completed']);self.assertFalse(checked['all_index_conclusion_verified'])
  saved=run.save_completed(task,self.root/'completed');restored=run.restore_completed(self.root/'completed',self.root/'restored',root=self.logs)
  self.assertEqual(restored[1],checked);self.assertEqual(self.calls,6)
  self.assertEqual((restored[0]/'upstream/count56/STAGE_COMPLETED.json').read_bytes(),(self.upstream/'STAGE_COMPLETED.json').read_bytes())
  marker=Path(saved['path']).with_suffix('.zip.sha256');marker.write_text('0'*64+'  '+Path(saved['path']).name+'\n',encoding='ascii')
  self.assertIsNone(run.restore_completed(self.root/'completed',self.root/'badcache',root=self.logs))

 def test_boolean_rc_missing_checkpoint_changed_stream_or_helper_fail_closed(self):
  for mode in('boolean','checkpoint','stream','helper','guard'):
   def fake(argv,**kw):
    observed=self.fake(argv,**kw);directory=Path(kw['output_dir'])
    if mode=='boolean':observed['returncode']=True
    elif mode=='checkpoint':observed['checkpoints']=[]
    elif mode=='stream':observed['stdout_sha256']='0'*64
    elif mode=='guard':observed['guard_scope']['proof_acceptance']=True
    else:put(directory.parent.parent/'capsule'/src.case(directory.name)['script'],b'changed source')
    put(directory/'supervisor-result.json',src.encoded(observed));return observed
   with self.subTest(mode=mode),self.assertRaises(ValueError):self.execute('bad-'+mode,fake)
   self.assertFalse((self.root/('bad-'+mode)/'CONTROLS_COMPLETED.json').exists())

 def test_rehashed_mathematical_receipt_or_prior_dependency_cannot_complete(self):
  task,_=self.execute();row=src.case('finite-high');output=task/'capsule'/row['output'];value=src.parsed(output.read_bytes());value['all_rows']=2;put(output,src.encoded(value))
  with self.assertRaises(ValueError):ev.validate_completed(task)

 def test_complete_cache_unsafe_namespace_duplicates_links_and_missing_ledgers(self):
  required=['SOURCES.json','CURRENT_GEOMETRY_FIXTURE.json','CONTROLS_OBSERVED.json','CONTROLS_COMPLETED.json','upstream/count56/STAGE_COMPLETED.json','upstream/count56/STAGE_OBSERVED.json']
  required += ['executions/'+a+'/'+name for a in src.IDS for name in('launch.json','supervisor-result.json','stdout.txt','stderr.txt')]
  for mode in('missing','traversal','backslash','case','linked','extra'):
   rows=[zipfile.ZipInfo(n)for n in required]
   if mode=='missing':rows.pop()
   elif mode=='traversal':rows.append(zipfile.ZipInfo('../outside'))
   elif mode=='backslash':row=zipfile.ZipInfo('plain');row.filename='capsule\\wrong';rows.append(row)
   elif mode=='case':rows.append(zipfile.ZipInfo('sources.json'))
   elif mode=='extra':rows.append(zipfile.ZipInfo('unbound/helper.py'))
   else:row=zipfile.ZipInfo('capsule/link');row.external_attr=(stat.S_IFLNK|0o777)<<16;rows.append(row)
   class Archive:
    def infolist(self):return rows
   with self.subTest(mode=mode),self.assertRaises(ValueError):run.cache_members(Archive())


if __name__=='__main__':unittest.main()
