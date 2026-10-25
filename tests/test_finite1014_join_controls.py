from copy import deepcopy
import io,json,stat,sys,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
from be_replay import finite1014_join as run,finite1014_join_sources as src,finite1014_join_control_evidence as ev,linux_supervisor as sup


class ControlProtocolTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.cache=self.root/'source-cache';self.cache.mkdir()
  self.directory='work/fixture/control';self.entry=self.directory+'/check.py';self.output=self.directory+'/CHECKED.json'
  self.raw={self.entry:b"raise AssertionError('Original mathematical trap must never execute locally')\n",'work/kernel.py':b"raise AssertionError('Synthetic kernel trap')\n"}
  graph={n:src.epoch.digest(b)for n,b in self.raw.items()};self.reference=dict(status='PASS_SYNTHETIC_CONTROL',counts={'all_controls':3},arithmetic_scope='synthetic only',files_sha256=graph)
  self.reference_raw=src.epoch.encode(self.reference)
  self.row=dict(job_id='synthetic',slot='range',directory=self.directory,script='check.py',arguments=[],output=self.output,
   read_only_record=False,reference='reference/synthetic.json',expected_status=self.reference['status'],metadata_documents=[],generated_sources={})
  self.plan=dict(source_files={n:dict(bytes=len(b),sha256=src.epoch.digest(b))for n,b in self.raw.items()},
   reference_files={self.row['reference']:dict(bytes=len(self.reference_raw),sha256=src.epoch.digest(self.reference_raw))},
   jobs=[self.row],unavailable_historical_inputs={})
  for name,raw in self.raw.items():p=self.cache/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
  p=self.cache/self.row['reference'];p.parent.mkdir(parents=True);p.write_bytes(self.reference_raw)
  self.addCleanup(patch.stopall);patch.object(src,'plan',return_value=self.plan).start();patch.object(src,'PLAN_SHA256','a'*64).start()
  self.logs=self.root/'batch';self.logs.mkdir();self.native_calls=0

 def fake(self,argv,**kw):
  self.native_calls+=1;cwd=Path(kw['cwd']);task=Path(kw['output_dir']).parent;output=task/'capsule'/self.output;output.write_bytes(self.reference_raw)
  config=sup._settings(argv,kw['cwd'],kw['output_dir'],kw['wall_seconds'],kw['cpu_seconds'],kw['memory_bytes'],kw['checkpoint_paths'],kw['mode'],.2,kw['disk_bytes'],kw['log_bytes']);config['heartbeat_seconds']=20.0
  directory=Path(config['output_dir']);(directory/'launch.json').write_bytes(src.dump(config));(directory/'stdout.txt').write_bytes(self.reference_raw);(directory/'stderr.txt').write_bytes(b'')
  captures=sup._capture_checkpoints(config)
  observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,
   elapsed_seconds=.01,maximum_sampled_group_RSS_bytes=4096,maximum_sampled_group_CPU_seconds=.001,guard_scope=ev.guard(),
   stdout_path=str(directory/'stdout.txt'),stdout_sha256=src.digest(directory/'stdout.txt'),stderr_path=str(directory/'stderr.txt'),stderr_sha256=src.digest(directory/'stderr.txt'),checkpoints=captures)
  finished=dict(event='linux_supervisor_finished',stage='untrusted_search',status='completed',reason=None,elapsed_seconds=.01,proof_accepted=False)
  (directory/'progress.json').write_bytes(src.dump(finished));(directory/'progress.jsonl').write_bytes(src.dump(finished).replace(b'\n',b'')+b'\n');(directory/'supervisor-result.json').write_bytes(src.dump(observed))
  return observed

 def execute(self,**extra):
  task=self.root/('task'+str(self.native_calls))
  with patch.object(run.sys,'platform','linux'),patch.object(run.linux_supervisor,'run',side_effect=lambda *a,**k:self.fake(*a,**k)),patch.object(run,'Follow',side_effect=lambda *args,**kw:io.StringIO()):
   checked=run.execute('synthetic',self.cache,task,root=self.logs,**extra)
  return task,checked

 def test_false_observed_then_full_validation_then_true_completion(self):
  seen=[];original=ev.validate_run
  def verify(task,report):seen.append(src.read(Path(task)/'STAGE_OBSERVED.json')['conditional_controls_completed']);return original(task,report)
  with patch.object(ev,'validate_run',side_effect=verify):task,checked=self.execute()
  self.assertTrue(seen and all(v is False for v in seen));self.assertTrue(checked['conditional_controls_completed']);self.assertTrue(src.read(task/'STAGE_COMPLETED.json')['conditional_controls_completed'])
  self.assertEqual(src.read(task/'execution/launch.json')['wall_seconds'],82800.0)
  self.assertEqual(src.read(task/'execution/supervisor-result.json')['checkpoints'][0]['path'],str(task/'execution/checkpoints/CHECKED.json'))
  self.assertFalse(checked['native_arithmetic_accepted'])

 def test_failure_modes_never_write_completion(self):
  original=self.fake
  for mode in('rcfalse','stderr_hash','nonempty_stderr','terminal','capture'):
   with self.subTest(mode=mode):
    self.native_calls+=1;task=self.root/('negative-'+mode)
    def fake(argv,**kw):
     observed=original(argv,**kw);d=Path(kw['output_dir'])
     if mode=='rcfalse':observed['returncode']=False
     elif mode=='stderr_hash':observed['stderr_sha256']='0'*64
     elif mode=='nonempty_stderr':(d/'stderr.txt').write_bytes(b'failure');observed['stderr_sha256']=src.digest(d/'stderr.txt')
     elif mode=='terminal':(d/'stdout.txt').write_bytes(b'{}\n');observed['stdout_sha256']=src.digest(d/'stdout.txt')
     else:observed['checkpoints'][0]['sha256']='0'*64
     (d/'supervisor-result.json').write_bytes(src.dump(observed));return observed
    with patch.object(run.sys,'platform','linux'),patch.object(run.linux_supervisor,'run',side_effect=fake),patch.object(run,'Follow',side_effect=lambda *args,**kw:io.StringIO()),self.assertRaises(ValueError):run.execute('synthetic',self.cache,task,root=self.logs)
    self.assertTrue((task/'STAGE_OBSERVED.json').is_file());self.assertFalse((task/'STAGE_COMPLETED.json').exists())

 def test_math_or_control_receipt_mutation_rejected(self):
  task,_=self.execute();observed=src.read(task/'STAGE_OBSERVED.json');v=src.read(task/'capsule'/self.output);v['counts']['all_controls']=2;(task/'capsule'/self.output).write_bytes(src.dump(v))
  with self.assertRaises(ValueError):ev.validate_run(task,observed)
  (task/'capsule'/self.output).write_bytes(self.reference_raw);(task/'capsule/work/kernel.py').write_bytes(b'mutated source')
  with self.assertRaises(ValueError):src.verify(task)

 def test_complete_cache_save_restore_and_bad_sidecar(self):
  task,checked=self.execute();cache=self.root/'completed';saved=run.save_completed(task,cache)
  restored=run.restore_completed('synthetic',cache,self.root/'restored',root=self.logs)
  self.assertIsNotNone(restored);self.assertEqual(restored[1],checked)
  Path(saved['path']).with_suffix('.zip.sha256').write_text('0'*64+'  '+Path(saved['path']).name+'\n',encoding='ascii')
  self.assertIsNone(run.restore_completed('synthetic',cache,self.root/'bad-restore',root=self.logs))

 def test_cache_preflight_unsafe_duplicates_links_size_missing_ledgers(self):
  required=['SOURCES.json',src.META,'STAGE_OBSERVED.json','STAGE_COMPLETED.json','execution/launch.json','execution/supervisor-result.json','execution/stdout.txt','execution/stderr.txt']
  for mode in('traversal','backslash','duplicate','case','symlink','oversized','missing'):
   with self.subTest(mode=mode):
    rows=[zipfile.ZipInfo(n)for n in required]
    if mode=='traversal':rows.append(zipfile.ZipInfo('../escape'))
    elif mode=='backslash':z=zipfile.ZipInfo('safe');z.filename='capsule\\escape';z.orig_filename=z.filename;rows.append(z)
    elif mode=='duplicate':rows.append(zipfile.ZipInfo(required[0]))
    elif mode=='case':rows.append(zipfile.ZipInfo('sources.json'))
    elif mode=='symlink':z=zipfile.ZipInfo('capsule/link');z.external_attr=(stat.S_IFLNK|0o777)<<16;rows.append(z)
    elif mode=='oversized':rows[0].file_size=65*src.MIB
    else:rows.pop()
    class FakeZip:
     def infolist(self):return rows
    with self.assertRaises(ValueError):run.cache_members(FakeZip())

 def test_prepared_sources_never_import_trap_or_allow_extra_file(self):
  task=self.root/'prepared';src.prepare('synthetic',self.cache,task);src.verify(task)
  (task/'capsule/extra.py').write_bytes(b'raise AssertionError')
  with self.assertRaises(ValueError):src.verify(task)

 def test_two_job_batch_complete_cache_resume_runs_no_native_calls(self):
  second=deepcopy(self.row);second['job_id']='synthetic2';self.plan['jobs'].append(second)
  cache=self.root/'two-stage-cache';first=self.root/'first-batch';first.mkdir();status=dict(controls=[])
  with patch.object(run.sys,'platform','linux'),patch.object(run.linux_supervisor,'run',side_effect=self.fake),patch.object(run,'Follow',side_effect=lambda *args,**kw:io.StringIO()):
   run.run_controls(first,cache,self.cache,status)
  self.assertEqual((len(status['controls']),self.native_calls),(2,2))
  self.assertEqual(len(list(cache.rglob('*-complete.zip'))),2)
  second_root=self.root/'second-batch';second_root.mkdir();again=dict(controls=[])
  with patch.object(run,'execute',side_effect=AssertionError('Completed cache must skip every native call')):
   run.run_controls(second_root,cache,self.cache,again)
  self.assertEqual(len(again['controls']),2);self.assertTrue(all(r['reused_completed_stage']for r in again['controls']))

 def test_failed_second_stage_keeps_first_complete_stage_and_resumes_only_second(self):
  second=deepcopy(self.row);second['job_id']='synthetic2';self.plan['jobs'].append(second)
  cache=self.root/'partial-cache';first=self.root/'partial-batch';first.mkdir();status=dict(controls=[]);original=run.execute
  def execute(job_id,*args,**kw):
   if job_id=='synthetic2':raise ValueError('Synthetic interrupted second action')
   return original(job_id,*args,**kw)
  with patch.object(run.sys,'platform','linux'),patch.object(run.linux_supervisor,'run',side_effect=self.fake),patch.object(run,'Follow',side_effect=lambda *args,**kw:io.StringIO()),patch.object(run,'execute',side_effect=execute):
   with self.assertRaises(ValueError):run.run_controls(first,cache,self.cache,status)
  self.assertEqual((len(status['controls']),len(list(cache.rglob('*-complete.zip'))),self.native_calls),(1,1,1))
  second_root=self.root/'resume-batch';second_root.mkdir();again=dict(controls=[])
  with patch.object(run.sys,'platform','linux'),patch.object(run.linux_supervisor,'run',side_effect=self.fake),patch.object(run,'Follow',side_effect=lambda *args,**kw:io.StringIO()):
   run.run_controls(second_root,cache,self.cache,again)
  self.assertEqual(self.native_calls,2);self.assertTrue(again['controls'][0]['reused_completed_stage']);self.assertFalse(again['controls'][1]['reused_completed_stage'])

 def test_complete_claim_requires_final_pure_readback_and_failure_still_exports(self):
  for reject in(False,True):
   with self.subTest(reject=reject):
    def final(root):
     d=src.read(Path(root)/'SESSION_RESULT.json');self.assertIs(d['conditional_finite_chain_verified'],True)
     if reject:raise ValueError('Synthetic final crossjoin rejection')
     return dict(conditional_finite_chain_verified=True)
    with patch.object(run.sys,'platform','linux'),patch.object(src,'obtain_assets',return_value={}),patch.object(src,'prepare_cache',return_value=self.cache),patch.object(run,'run_controls'),patch('be_replay.finite1014_join_evidence.import_completed_inputs',return_value=[]),patch('be_replay.finite1014_join_evidence.validate_batch',return_value={'synthetic':'full crossjoin'}),patch('be_replay.finite1014_join_evidence.validate_completed',side_effect=final):
     result=run.run_colab(durable_root=self.root/('complete-drive-'+str(reject)),work_root=self.root/('complete-work-'+str(reject)))
    self.assertEqual(result['status']['conditional_finite_chain_verified'],not reject);self.assertTrue(Path(result['bundle']['path']).is_file())
    indexes=list((self.root/('complete-drive-'+str(reject))).rglob('completed-finite/**/*.json'));self.assertEqual(len(indexes),0 if reject else 1)

 def test_drive_export_failure_preserves_local_failure_bundle(self):
  original=run.bundle;calls=[]
  def export(root,destination):
   calls.append(Path(destination))
   if len(calls)==1:raise OSError('Synthetic disconnected Drive')
   return original(root,destination)
  with patch.object(run.sys,'platform','linux'),patch.object(src,'obtain_assets',side_effect=ValueError('Synthetic preflight rejection')),patch.object(run,'bundle',side_effect=export):
   result=run.run_colab(durable_root=self.root/'offline-drive',work_root=self.root/'offline-work')
  self.assertEqual(result['status']['state'],'incomplete');self.assertFalse(result['status']['conditional_finite_chain_verified']);self.assertIn('bundle_error',result['status']);self.assertTrue(Path(result['bundle']['path']).is_file());self.assertEqual(len(calls),2)

 def test_missing_upstream_wait_and_failure_always_export_bundle(self):
  for error in(False,True):
   with self.subTest(error=error):
    durable=self.root/('durable-'+str(error));work=self.root/('work-'+str(error));stage=[]
    def controls(root,cache,source,status):
     status['controls'].append(dict(job_id='first-completed',conditional_controls_completed=True))
     if error:raise ValueError('synthetic second stage failed')
    with patch.object(run.sys,'platform','linux'),patch.object(src,'obtain_assets',return_value={}),patch.object(src,'prepare_cache',return_value=self.cache),patch.object(run,'run_controls',side_effect=controls),patch('be_replay.finite1014_join_evidence.import_completed_inputs',return_value=[dict(key='56A')]):
     result=run.run_colab(durable_root=durable,work_root=work)
    self.assertEqual(result['status']['state'],'incomplete'if error else'waiting_for_prerequisite_exports');self.assertFalse(result['status']['conditional_finite_chain_verified']);self.assertFalse(result['status']['all_index_conclusion_verified']);self.assertTrue(Path(result['bundle']['path']).is_file());self.assertEqual(len(result['status']['controls']),1)


if __name__=='__main__':unittest.main()
