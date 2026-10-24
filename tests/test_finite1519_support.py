"""57D synthetic transport fixtures; every numerical file is a trap."""
import copy,io,json,shutil,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch,Mock
from be_replay import finite1519_support_sources as s,finite1519_support_evidence as e,finite1519_support as r

def put(p,d):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.dump(d));return s.digest(p)

class Support(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(dir=s.ROOT.parent,prefix='t57d-');self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.assertTrue(self.root.resolve().is_relative_to(s.ROOT.parent.resolve()))
  self.cache=self.root/'inputs';native=self.cache/s.NATIVE;audit=self.cache/s.AUDIT
  native.mkdir(parents=True);audit.mkdir(parents=True)
  for p in[native/n for n in(*s.ENGINES,'support_bridge.py')]+[audit/'check.py']:
   p.write_bytes(b'raise AssertionError("Do not import or run original mathematical modules in fixtures")\n')
  (audit/'PROOF.txt').write_bytes(b'SYNTHETIC ONLY\n');put(native/'COPIED_SOURCES.json',{'synthetic':True})
  graph={p.relative_to(self.cache).as_posix():s.digest(p)for p in native.glob('*.py')}
  self.candidate=dict(schema='CONDITIONAL_ACTUAL15_19_SUPPORT_BRIDGE_V1',status='FRESH_CONDITIONAL_SUPPORT_ALL_ROWS',rho_interval=['1','33/25'],radius='3',
   rows=[dict(n=n,status='CONDITIONAL_FULL_RAY_SUPPORT',proof='SYNTHETIC ONLY')for n in range(15,20)],files_sha256=graph,
   predecessor_verified=False,retained_contact_framework_verified_here=False,cutoff15_proved=False)
  import hashlib
  self.plan=dict(source_files={p.relative_to(self.cache).as_posix():dict(bytes=p.stat().st_size,sha256=s.digest(p))for p in self.cache.rglob('*')if p.is_file()},
   original_candidate_source_graph=graph,original_candidate_sha256=hashlib.sha256(s.dump(self.candidate)).hexdigest())
  for obj,name,value in((s,'plan',self.plan),(r.sys,'platform','linux'),(r.sys,'stdout',io.StringIO())):
   patcher=patch.object(obj,name,return_value=value)if name=='plan'else patch.object(obj,name,value);patcher.start();self.addCleanup(patcher.stop)

 def fake(self,argv, *,cwd,output_dir,**kw):
  cwd=Path(cwd);output_dir=Path(output_dir);action=output_dir.name;task=output_dir.parent.parent;c=task/'capsule'
  if action=='construct':
   d=copy.deepcopy(self.candidate)
   if hasattr(self,'mutate_candidate'):self.mutate_candidate(d)
   put(c/s.CANDIDATE,d)
   text='\n'.join([str(n)+' CONDITIONAL_FULL_RAY_SUPPORT'for n in range(15,20)]+['FRESH_CONDITIONAL_SUPPORT_ALL_ROWS '+s.digest(c/s.CANDIDATE)])+'\n'
  else:
   meta=s.read(c/s.RUNS/'metadata.json')
   for name in s.ENGINES:
    p=c/s.AUDIT/'engine'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(c/s.NATIVE/name,p)
   graph={s.CANDIDATE:s.digest(c/s.CANDIDATE)}|self.plan['original_candidate_source_graph']
   for name in s.capture_paths()+[s.NATIVE+'/'+n for n in meta['input_sha256']]+[s.AUDIT+'/engine/'+n for n in s.ENGINES]+[s.AUDIT+'/check.py',s.AUDIT+'/PROOF.txt']:graph[name]=s.digest(c/name)
   d=dict(status='PASS_FRESH_ACTUAL15_19_TWO_RAY_SUPPORT_REPLAY_CONDITIONAL',n_values=list(range(15,20)),rho_interval=['1','33/25'],radius='3',
    candidate_sha256=s.digest(c/s.CANDIDATE),full_ray_rows=10,malformed_controls=14,parser_controls=2,predecessor_premise_discharged_here=False,
    execution_scope='Fresh exact full-object reproduction with byte-identical copied arithmetic helpers; independent driver and scalar reconstruction, not an independent Gaussian arithmetic implementation.',files_sha256=graph)
   if hasattr(self,'mutate_receipt'):self.mutate_receipt(d)
   put(c/s.RESULT,d);text=d['status']+' '+s.digest(c/s.RESULT)+'\n'
  output_dir.mkdir(parents=True);(output_dir/'stdout.txt').write_bytes(text.encode());(output_dir/'stderr.txt').write_bytes(b'')
  launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,**kw)
  launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds'])
  launch['checkpoint_paths']=[str(p)for p in launch['checkpoint_paths']];put(output_dir/'launch.json',launch)
  checks=[]
  for p in kw['checkpoint_paths']:
   p=Path(p);dest=output_dir/'checkpoints'/p.relative_to(cwd);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
   checks.append(dict(source_path=str(p),exists=True,trusted_certificate=False,path=str(dest),bytes=p.stat().st_size,sha256=s.digest(p)))
  scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(e.WALL_SECONDS),
   per_process_RLIMIT_AS_bytes=e.MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=e.CPU_SECONDS,aggregate_kernel_memory_limit=False,
   aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=e.MEMORY_BYTES,sampled_group_CPU_limit_seconds=e.CPU_SECONDS,
   sampled_file_limit_bytes=512*s.MIB,sampled_log_limit_bytes=16*s.MIB,descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
  out=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,elapsed_seconds=.1,
   maximum_sampled_group_RSS_bytes=10*s.MIB,maximum_sampled_group_CPU_seconds=.1,guard_scope=scope,checkpoints=checks,
   **{k+suffix:v for k in('stdout','stderr')for suffix,v in(('_path',str(output_dir/(k+'.txt'))),('_sha256',s.digest(output_dir/(k+'.txt'))))})
  put(output_dir/'supervisor-result.json',out);return out

 def complete(self,name='task',effect=None):
  task=self.root/name
  with patch.object(r.linux_supervisor,'run',side_effect=effect or self.fake),patch.object(r,'Follow'):
   out=r.execute(task,self.cache,root=self.root)
  return task,out

 def test_two_full_original_passes_and_genuine_new_constructor_capture(self):
  task,out=self.complete();self.assertTrue(out['conditional_support_arithmetic_completed'])
  self.assertEqual(out['summary']['full_ray_rows'],10)
  for k in e.FLAGS:self.assertIs(out[k],False)
  meta=s.read(task/'capsule'/s.RUNS/'metadata.json');self.assertEqual(meta['schema'],'CURRENT_STOPPED_SUPPORT_CONSTRUCTOR_CAPTURE_V1')
  self.assertEqual(meta['command'],[r.sys.executable,'-B','support_bridge.py']);self.assertIs(meta['proof_accepted'],False)
  self.assertEqual(s.digest(task/'capsule'/s.CANDIDATE),self.plan['original_candidate_sha256'])

 def test_candidate_is_fresh_not_copied_from_historical_accepted_output(self):
  task=self.root/'prepared';s.prepare(self.cache,task);self.assertFalse((task/'capsule'/s.CANDIDATE).exists())
  self.assertFalse((task/'capsule'/s.RESULT).exists());self.assertFalse((task/'capsule'/s.RUNS).exists())

 def test_failed_native_status_or_candidate_hash_never_accepted(self):
  self.mutate_candidate=lambda d:d.update(status='INCOMPLETE_SUPPORT_BRIDGE')
  with self.assertRaises(ValueError):self.complete('failed-candidate')
  self.assertFalse((self.root/'failed-candidate/STAGE_COMPLETED.json').exists())

 def test_all_original_controls_and_both_rays_required(self):
  for field,value in(('malformed_controls',13),('parser_controls',0),('full_ray_rows',5),('status','FAILED'),('predecessor_premise_discharged_here',True)):
   self.mutate_receipt=lambda d,f=field,v=value:d.update({f:v})
   with self.assertRaises(ValueError):self.complete('bad-'+field)
   self.assertFalse((self.root/('bad-'+field)/'STAGE_COMPLETED.json').exists())

 def test_boolean_rc_guard_or_actual_stream_hash_fail_closed(self):
  for i,mutate in enumerate((lambda d:d.update(returncode=False),lambda d:d['guard_scope'].update(proof_acceptance=True),lambda d:d.update(stderr_sha256='0'*64))):
   def fake(*a,**kw):
    d=self.fake(*a,**kw);mutate(d);put(Path(kw['output_dir'])/'supervisor-result.json',d);return d
   with self.assertRaises(ValueError):self.complete('transport'+str(i),fake)
   self.assertFalse((self.root/('transport'+str(i))/'STAGE_COMPLETED.json').exists())

 def test_capture_metadata_reconstruction_rejects_rehashed_wrong_command_or_inputs(self):
  task,_=self.complete();report=s.read(task/'STAGE_OBSERVED.json');p=task/'capsule'/s.RUNS/'metadata.json';original=s.read(p)
  for mutate in(lambda d:d.update(command=['fake','-B','support_bridge.py']),lambda d:d.update(input_sha256={})):
   d=copy.deepcopy(original);mutate(d);put(p,d)
   with self.assertRaises(ValueError):e.validate_run(task,report)
  put(p,original)

 def test_copied_engine_and_unknown_source_files_are_rejected(self):
  task,_=self.complete();p=task/'capsule'/s.AUDIT/'engine'/s.ENGINES[0];p.write_bytes(b'changed')
  with self.assertRaises(ValueError):e.validate_completed(task)
  p=task/'capsule'/s.NATIVE/'unbound.py';p.write_bytes(b'unbound')
  with self.assertRaises(ValueError):s.verify_job(task)

 def test_complete_relocated_export_preserves_every_original_byte(self):
  task,out=self.complete();dest=self.root/'relocated';shutil.copytree(task,dest)
  before={p.relative_to(dest).as_posix():p.read_bytes()for p in dest.rglob('*')if p.is_file()}
  self.assertEqual(e.validate_completed(dest),out)
  self.assertEqual(before,{p.relative_to(dest).as_posix():p.read_bytes()for p in dest.rglob('*')if p.is_file()})

 def test_complete_cache_reuse_skips_both_actions_and_downloads(self):
  task,out=self.complete();cache=self.root/'drive/finite1519-support/completed'/s.PLAN_SHA256[:16];export=r.save_completed(task,cache)
  with patch.object(r.linux_supervisor,'run')as native,patch.object(s,'obtain_assets')as download:
   result=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'runs')
  self.assertTrue(result['status']['conditional_support_arithmetic_completed']);native.assert_not_called();download.assert_not_called()
  Path(export['path']).with_suffix('.zip.sha256').write_bytes(b'bad')
  self.assertIsNone(r.restore_completed(cache,self.root/'bad-restore',root=self.root))

 def test_actual_pure_supervisor_copies_each_checkpoint_relative_to_native_cwd(self):
  task,_=self.complete()
  for action in s.ACTIONS:
   cwd=task/'capsule'/(s.NATIVE if action=='construct'else s.AUDIT);out=self.root/('pure-capture-'+action)
   paths=[task/'capsule'/p for p in s.output_paths(action)]
   rows=r.linux_supervisor._capture_checkpoints(dict(output_dir=str(out),cwd=str(cwd),checkpoint_paths=[str(p)for p in paths],disk_bytes=512*s.MIB))
   self.assertEqual(len(rows),len(paths))
   for row,path in zip(rows,paths):
    self.assertEqual(Path(row['path']),out/'checkpoints'/path.relative_to(cwd))
    self.assertEqual(Path(row['path']).read_bytes(),path.read_bytes());self.assertEqual(row['sha256'],s.digest(path))

 def test_bad_zip_inventory_is_rejected_before_extraction(self):
  z=Mock()
  for name in('../escape','/absolute','a//b','a\\b','SOURCES.json'):
   info=zipfile.ZipInfo();info.filename=info.orig_filename=name;z.infolist.return_value=[info]
   with self.assertRaises(ValueError):r.cache_members(z)

 def test_failed_action_exports_false_final_bundle_with_actual_diagnostic(self):
  def fail(*a,**kw):
   d=self.fake(*a,**kw);p=Path(kw['output_dir']);(p/'stderr.txt').write_bytes(b'ACTUAL SYNTHETIC FAILURE')
   d.update(status='incomplete',returncode=1,reason='nonzero_subprocess_exit',stderr_sha256=s.digest(p/'stderr.txt'));put(p/'supervisor-result.json',d);return d
  with patch.object(s,'obtain_assets',return_value={}),patch.object(s,'prepare_cache',return_value=self.cache),patch.object(r.linux_supervisor,'run',side_effect=fail),patch.object(r,'Follow'):
   out=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'runs')
  self.assertFalse(out['status']['conditional_support_arithmetic_completed']);self.assertIn('ACTUAL SYNTHETIC FAILURE',out['status']['error'])
  self.assertTrue(Path(out['bundle']).is_file())

class OriginalPlan(unittest.TestCase):
 def test_source_only_original26_inputs_23_graph_and_full_ray_controls(self):
  d=s.plan();self.assertEqual(len(d['source_files']),26);self.assertEqual(len(d['original_candidate_source_graph']),23)
  self.assertEqual(d['n'],list(range(15,20)));self.assertEqual(d['full_ray_rows'],10)
  self.assertEqual((d['malformed_controls'],d['parser_controls']),(14,2))
  self.assertNotIn(s.CANDIDATE,d['source_files']);self.assertTrue(d['original_mathematical_programs_unchanged'])

if __name__=='__main__':unittest.main()
