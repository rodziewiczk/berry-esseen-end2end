"""57E source/port/transport/cache fixtures; no original numerical execution."""
import copy,hashlib,importlib.util,io,json,shutil,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch,Mock
from be_replay import finite1519_high_sources as s,finite1519_high_evidence as e,finite1519_high as r

def put(p,d):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.dump(d));return s.digest(p)

class High(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(dir=s.ROOT.parent,prefix='t57e-');self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.assertTrue(self.root.resolve().is_relative_to(s.ROOT.parent.resolve()));self.cache=self.root/'inputs'
  native=self.cache/s.NATIVE;audit=self.cache/s.AUDIT;native.mkdir(parents=True);audit.mkdir(parents=True)
  original_plan=s.plan();self.original_plan=copy.deepcopy(original_plan)
  for name in('bound.py','kernel.py','universal.py'):(native/name).write_bytes(b'raise AssertionError("Never import or execute original mathematical kernels in local fixtures")\n')
  for i in range(68):
   p=self.cache/'work/synthetic-provenance'/('p'+str(i)+'.txt');p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'SYNTHETIC ONLY\n')
  graph={p.relative_to(self.cache).as_posix():s.digest(p)for p in self.cache.rglob('*')if p.is_file()}
  self.manifest=put(native/'MANIFEST.json',dict(files_sha256=graph))
  self.native=dict(status='PASS_SUPPORTED_COMPENSATED_HIGH15_19',scope='SYNTHETIC ONLY',
   rows=[dict(n=n,band=b)for b in('B0','BN','BH')for n in range(15,20)],attempts=[],controls=dict(malformed_domains=8),pi='SYNTHETIC',manifest_sha256=self.manifest)
  self.original=b'CAPTURE_SHA = '+repr(original_plan['original_capture_sha256']).encode()+b'\nRESULT_SHA = "SYNTHETIC ONLY"\ndef numerical():\n raise AssertionError("Never execute mathematics")\n'
  (audit/'check.py').write_bytes(self.original);(audit/'REVIEW.txt').write_bytes(b'SYNTHETIC PROVENANCE ONLY\n')
  self.plan=dict(source_files={p.relative_to(self.cache).as_posix():dict(bytes=p.stat().st_size,sha256=s.digest(p))for p in self.cache.rglob('*')if p.is_file()},
   original_manifest_sha256=self.manifest,original_readback_sha256=hashlib.sha256(self.original).hexdigest(),original_capture_sha256=copy.deepcopy(original_plan['original_capture_sha256']),
   original_native_result_sha256=hashlib.sha256(s.dump(self.native)).hexdigest(),expected_readback=copy.deepcopy(original_plan['expected_readback']))
  p=patch.object(s,'plan',return_value=self.plan);p.start();self.addCleanup(p.stop)
  for obj,name,value in((r.sys,'platform','linux'),(r.sys,'stdout',io.StringIO())):
   p=patch.object(obj,name,value);p.start();self.addCleanup(p.stop)

 def fake(self,argv, *,cwd,output_dir,**kw):
  cwd=Path(cwd);output_dir=Path(output_dir);action=output_dir.name;task=output_dir.parent.parent;c=task/'capsule';output_dir.mkdir(parents=True)
  launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,**kw)
  launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds']);launch['checkpoint_paths']=[str(p)for p in launch['checkpoint_paths']]
  put(output_dir/'launch.json',launch)
  if action=='readback':
   graph=dict(s.read(c/s.NATIVE/'MANIFEST.json')['files_sha256'])
   for name in(s.NATIVE+'/MANIFEST.json',s.AUDIT+'/check.py',s.AUDIT+'/REVIEW.txt'):
    graph[name]=s.digest(c/name)
   for a in('construct','replay'):
    for name in s.output_paths(a):graph[name]=s.digest(c/name)
   result=copy.deepcopy(self.plan['expected_readback']);result['files_sha256']=graph
   if hasattr(self,'mutate_readback'):self.mutate_readback(result)
   put(c/s.RESULT,result);text=json.dumps({k:v for k,v in result.items()if k!='files_sha256'})+'\n'
  else:
   d=c/s.RUNS/s.LABELS[action];d.mkdir(parents=True)
   result=copy.deepcopy(self.native)
   if hasattr(self,'mutate_native'):self.mutate_native(result)
   put(d/'RESULT.json',result);text='COMPENSATED_HIGH SYNTHETIC\n'+result['status']+'\n'
   (d/'stdout.txt').write_bytes(text.encode());(d/'stderr.txt').write_bytes(b'')
   meta=dict(schema='CURRENT_REAL_CHILD_COMPENSATED_HIGH_CAPTURE_V1',command=[argv[0],'-B','bound.py',str(d/'RESULT.json')],cwd=str(c/s.NATIVE),
    input_sha256={n:s.digest(c/s.NATIVE/n)for n in('MANIFEST.json','bound.py','kernel.py','universal.py')},python=r.sys.version,returncode=0,elapsed_seconds=.1,
    stdout_sha256=s.digest(d/'stdout.txt'),stderr_sha256=s.digest(d/'stderr.txt'),result_sha256=s.digest(d/'RESULT.json'),outer_launch_sha256=s.digest(output_dir/'launch.json'),
    scope='Genuine original child under outer BASIC process-group supervision; not historical/native acceptance',proof_accepted=False)
   put(d/'metadata.json',meta)
  (output_dir/'stdout.txt').write_bytes(text.encode());(output_dir/'stderr.txt').write_bytes(b'')
  # Exercise the actual unchanged pure supervisor capture routine, not a model
  # with a guessed relative-root convention.
  checks=r.linux_supervisor._capture_checkpoints(dict(output_dir=str(output_dir),cwd=str(cwd),checkpoint_paths=[str(p)for p in kw['checkpoint_paths']],disk_bytes=kw['disk_bytes']))
  scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(e.WALL_SECONDS),per_process_RLIMIT_AS_bytes=e.MEMORY_BYTES,
   per_process_RLIMIT_CPU_seconds=e.CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=e.MEMORY_BYTES,
   sampled_group_CPU_limit_seconds=e.CPU_SECONDS,sampled_file_limit_bytes=512*s.MIB,sampled_log_limit_bytes=16*s.MIB,descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
  out=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,elapsed_seconds=.1,
   maximum_sampled_group_RSS_bytes=10*s.MIB,maximum_sampled_group_CPU_seconds=.1,guard_scope=scope,checkpoints=checks,
   **{k+suffix:v for k in('stdout','stderr')for suffix,v in(('_path',str(output_dir/(k+'.txt'))),('_sha256',s.digest(output_dir/(k+'.txt'))))})
  put(output_dir/'supervisor-result.json',out);return out

 def complete(self,name='task',effect=None):
  task=self.root/name
  with patch.object(r.linux_supervisor,'run',side_effect=effect or self.fake),patch.object(r,'Follow'):
   out=r.execute(task,self.cache,root=self.root)
  return task,out

 def test_all_three_complete_original_actions_with_current_capture_epoch(self):
  task,out=self.complete();self.assertTrue(out['conditional_compensated_high_arithmetic_completed'])
  self.assertEqual(out['summary']['rows'],15);self.assertEqual(out['summary']['readback_controls'],34)
  for k in e.FLAGS:self.assertIs(out[k],False)
  epoch=s.read(task/'CAPTURE_EPOCH.json');self.assertTrue(epoch['all_other_bytes_unchanged']);self.assertTrue(epoch['all_mathematical_function_asts_unchanged'])
  self.assertEqual((task/'capsule'/s.AUDIT/'check.py').read_bytes(),self.original)
  for action in s.ACTIONS:
   observed=s.read(task/'executions'/action/'supervisor-result.json')
   for row in observed['checkpoints']:
    self.assertEqual(Path(row['path']),task/'executions'/action/'checkpoints'/Path(row['source_path']).relative_to(task/'capsule'))

 def test_exact_byte_and_ast_derivation_rejects_other_changes_or_incomplete_pins(self):
  b,epoch=s.derive_check(self.original,dict(construct='1'*64,replay='2'*64));self.assertNotEqual(b,self.original)
  self.assertTrue(epoch['only_top_level_capture_sha_dictionary_changed'])
  for pins in({},dict(construct='1'*64),dict(construct=True,replay='2'*64),dict(construct='x'*64,replay='2'*64)):
   with self.assertRaises(ValueError):s.derive_check(self.original,pins)
  with self.assertRaises(ValueError):s.derive_check(self.original+b'# changed math provenance\n',dict(construct='1'*64,replay='2'*64))

 def test_derivation_rejects_a_second_capture_assignment_even_if_bytes_are_resealed(self):
  bad=self.original+b'CAPTURE_SHA = {}\n';packet=dict(self.plan,original_readback_sha256=hashlib.sha256(bad).hexdigest())
  with patch.object(s,'plan',return_value=packet):
   with self.assertRaises(ValueError):s.derive_check(bad,dict(construct='1'*64,replay='2'*64))

 def test_fresh_native_proof_or_missing_controls_never_completes(self):
  for i,change in enumerate((lambda d:d.update(status='SUPPORTED_COMPENSATED_HIGH15_19_NOT_CLOSED'),lambda d:d['controls'].update(malformed_domains=0))):
   self.mutate_native=change
   with self.assertRaises(ValueError):self.complete('native'+str(i))
   self.assertFalse((self.root/('native'+str(i))/'STAGE_COMPLETED.json').exists())

 def test_all34_readback_controls_and_full_supported_scope_required(self):
  for i,change in enumerate((lambda d:d.update(negative_controls=33),lambda d:d.update(support_radius='4'),lambda d:d.update(mathematical_status='unconditional'))):
   self.mutate_readback=change
   with self.assertRaises(ValueError):self.complete('readback'+str(i))
   self.assertFalse((self.root/('readback'+str(i))/'STAGE_COMPLETED.json').exists())

 def test_boolean_rc_wrong_guard_stream_or_stopped_copy_rejected(self):
  for i,change in enumerate((lambda o:o.update(returncode=False),lambda o:o['guard_scope'].update(proof_acceptance=True),lambda o:o.update(stderr_sha256='0'*64),lambda o:o.update(checkpoints=[]))):
   def fake(*a,**kw):
    out=self.fake(*a,**kw);change(out);put(Path(kw['output_dir'])/'supervisor-result.json',out);return out
   with self.assertRaises(ValueError):self.complete('transport'+str(i),fake)
   self.assertFalse((self.root/('transport'+str(i))/'STAGE_COMPLETED.json').exists())

 def test_derived_source_or_capture_epoch_tampering_is_rejected(self):
  task,_=self.complete();p=task/'capsule'/s.FRESH;original=p.read_bytes();p.write_bytes(original+b'# extra code\n')
  with self.assertRaises(ValueError):s.verify_job(task)
  p.write_bytes(original);epoch=s.read(task/'CAPTURE_EPOCH.json');epoch['all_other_bytes_unchanged']=False;put(task/'CAPTURE_EPOCH.json',epoch)
  with self.assertRaises(ValueError):e.validate_completed(task)

 def test_genuine_inner_os_command_and_entire_source_input_map_are_bound(self):
  task,_=self.complete();o=s.read(task/'STAGE_OBSERVED.json');p=task/'capsule'/s.RUNS/s.LABELS['construct']/'metadata.json';m=s.read(p)
  for change in(lambda d:d.update(command=['fake','bound.py']),lambda d:d.update(input_sha256={}),lambda d:d.update(proof_accepted=True)):
   d=copy.deepcopy(m);change(d);put(p,d)
   with self.assertRaises(ValueError):e.validate_run(task,o)
  put(p,m)

 def test_worker_source_and_sealed_original_inventory_reject_extra_helpers(self):
  task=self.root/'prepared';s.prepare(self.cache,task);p=task/s.WORKER;p.write_bytes(b'changed launcher')
  with self.assertRaises(ValueError):s.verify_job(task)
  task=self.root/'extra';s.prepare(self.cache,task);p=task/'capsule'/s.NATIVE/'unbound.py';p.write_bytes(b'bad')
  with self.assertRaises(ValueError):s.verify_job(task)

 def test_complete_cache_sha_and_relocation_revalidate_without_math(self):
  task,out=self.complete();cache=self.root/'saved';export=r.save_completed(task,cache)
  with patch.object(r.linux_supervisor,'run')as native:
   restored=r.restore_completed(cache,self.root/'restored',root=self.root)
  self.assertEqual(restored[1],out);native.assert_not_called()
  copied=restored[0];self.assertEqual((copied/'capsule'/s.FRESH).read_bytes(),(task/'capsule'/s.FRESH).read_bytes())
  Path(export['path']).with_suffix('.zip.sha256').write_bytes(b'bad');self.assertIsNone(r.restore_completed(cache,self.root/'bad',root=self.root))

 def test_second_session_reuses_only_full_three_action_cache(self):
  task,_=self.complete();cache=self.root/'drive/finite1519-high/completed'/s.PLAN_SHA256[:16];r.save_completed(task,cache)
  with patch.object(r.linux_supervisor,'run')as native,patch.object(s,'obtain_assets')as download:
   out=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'runs')
  self.assertTrue(out['status']['conditional_compensated_high_arithmetic_completed']);native.assert_not_called();download.assert_not_called()

 def test_native_failure_still_exports_false_final_zip_with_diagnostic(self):
  def fake(*a,**kw):
   d=self.fake(*a,**kw);p=Path(kw['output_dir']);(p/'stderr.txt').write_bytes(b'ACTUAL SYNTHETIC HIGH FAILURE')
   d.update(status='incomplete',reason='nonzero_subprocess_exit',returncode=1,stderr_sha256=s.digest(p/'stderr.txt'));put(p/'supervisor-result.json',d);return d
  with patch.object(s,'obtain_assets',return_value={}),patch.object(s,'prepare_cache',return_value=self.cache),patch.object(r.linux_supervisor,'run',side_effect=fake),patch.object(r,'Follow'):
   out=r.run_colab(durable_root=self.root/'drive',work_root=self.root/'runs')
  self.assertFalse(out['status']['conditional_compensated_high_arithmetic_completed']);self.assertIn('ACTUAL SYNTHETIC HIGH FAILURE',out['status']['error']);self.assertTrue(Path(out['bundle']).is_file())

 def test_cache_preflight_rejects_missing_ledgers_and_unsafe_or_oversized_members(self):
  import zipfile
  z=Mock()
  for name in('../escape','/absolute','a//b','a\\b','STAGE_COMPLETED.json'):
   info=zipfile.ZipInfo();info.filename=info.orig_filename=name;z.infolist.return_value=[info]
   with self.assertRaises(ValueError):r.cache_members(z)
  info=zipfile.ZipInfo('oversized');info.file_size=129*s.MIB;z.infolist.return_value=[info]
  with self.assertRaises(ValueError):r.cache_members(z)

 def test_stdlib_worker_uses_real_child_schema_without_importing_original_kernel(self):
  from be_replay import finite1519_high_worker as worker
  task=self.root/'worker';s.prepare(self.cache,task);put(task/'executions/construct/launch.json',dict(synthetic=True));seen=[]
  class Child:
   def __init__(self,command,**kw):
    seen.append((command,kw));put(Path(command[-1]),self_outer.native)
    self.stdout=io.BytesIO(b'SYNTHETIC CHILD STDOUT\n');self.stderr=io.BytesIO(b'')
   def wait(self,*a,**kw):return 0
   def poll(self):return 0
  self_outer=self
  with patch.object(worker.subprocess,'Popen',Child),patch.object(worker.sys,'stdout',SimpleNamespace(buffer=io.BytesIO())),patch.object(worker.sys,'stderr',SimpleNamespace(buffer=io.BytesIO())):
   self.assertEqual(worker.run(task,'construct'),0)
  command,kw=seen[0];self.assertEqual(command,[r.sys.executable,'-B','bound.py',str(task/'capsule'/s.RUNS/s.LABELS['construct']/'RESULT.json')])
  self.assertEqual(kw['cwd'],task/'capsule'/s.NATIVE);self.assertNotIn('shell',kw);self.assertNotIn('start_new_session',kw)
  m=s.read(task/'capsule'/s.RUNS/s.LABELS['construct']/'metadata.json');self.assertIs(m['proof_accepted'],False);self.assertEqual(m['input_sha256'].keys(),{'MANIFEST.json','bound.py','kernel.py','universal.py'})

 def test_stdlib_worker_preserves_actual_failed_child_capture_and_cannot_accept(self):
  from be_replay import finite1519_high_worker as worker
  task=self.root/'failed-worker';s.prepare(self.cache,task);put(task/'executions/construct/launch.json',dict(synthetic=True))
  class Child:
   def __init__(self,command,**kw):
    self.stdout=io.BytesIO(b'ACTUAL SYNTHETIC FAILED CHILD\n');self.stderr=io.BytesIO(b'FAILURE\n')
   def wait(self,*a,**kw):return 1
   def poll(self):return 1
  with patch.object(worker.subprocess,'Popen',Child),patch.object(worker.sys,'stdout',SimpleNamespace(buffer=io.BytesIO())),patch.object(worker.sys,'stderr',SimpleNamespace(buffer=io.BytesIO())):
   with self.assertRaisesRegex(ValueError,'Original HIGH child failed'):worker.run(task,'construct')
  m=s.read(task/'capsule'/s.RUNS/s.LABELS['construct']/'metadata.json')
  self.assertIs(type(m['returncode']),int);self.assertEqual(m['returncode'],1);self.assertIs(m['proof_accepted'],False)
  self.assertIsNone(m['result_sha256']);self.assertFalse((task/'STAGE_COMPLETED.json').exists())

class OriginalSourcePlan(unittest.TestCase):
 def test_actual74_input_71_manifest_original_result_and_controls_pins(self):
  d=s.plan();self.assertEqual(len(d['source_files']),74);self.assertEqual(d['original_manifest_graph_rows'],71)
  self.assertEqual(d['expected_readback']['negative_controls'],34);self.assertEqual(d['expected_readback']['n'],list(range(15,20)))
  for a in('construct','replay'):
   for p in s.output_paths(a):self.assertNotIn(p,d['source_files'])
  self.assertTrue(d['original_numerical_programs_unchanged']);self.assertTrue(d['only_derived_capture_hash_dictionary_replaced'])

if __name__=='__main__':unittest.main()
