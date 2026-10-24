"""59B/C fake-supervisor infrastructure; all mathematical source files are traps."""
import ast,copy,hashlib,inspect,io,json,shutil,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch,Mock
from be_replay import finite2630_covers_sources as s,finite2630_covers_evidence as e,finite2630_covers as r

def put(p,d):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(s.dump(d));return s.digest(p)
def canonical(d):return hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ast_paths(node,path=()):
 yield path,node
 for field,value in ast.iter_fields(node):
  if isinstance(value,list):
   for i,n in enumerate(value):
    if isinstance(n,ast.AST):yield from ast_paths(n,path+(field,i))
  elif isinstance(value,ast.AST):yield from ast_paths(value,path+(field,))

class Covers(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(dir=s.ROOT.parent,prefix='t59-');self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.assertTrue(self.root.resolve().is_relative_to(s.ROOT.parent.resolve()));self.cache=self.root/'inputs';self.plan=copy.deepcopy(s.plan());self.templates={}
  for name in self.plan['source_files']:
   p=self.cache/name;p.parent.mkdir(parents=True,exist_ok=True)
   p.write_bytes(b'raise AssertionError("Original mathematical modules must never execute in local fixtures")\n'if name.endswith('.py')else b'SYNTHETIC UNTRUSTED PROVENANCE ONLY\n')
  for name,row in self.plan['stages'].items():
   path=self.cache/row['directory']/row['script'];old_ports=row['receipt_ports'];values={'p'+str(i):p['original_sha256']for i,p in enumerate(old_ports)}
   raw=('PINS = '+repr(values)+'\nraise AssertionError("Never execute synthetic numerical source")\n').encode();path.write_bytes(raw);row['script_sha256']=s.digest(path)
   tree=ast.parse(raw);ports=[]
   for i,spec in enumerate(old_ports):
    route,node=next((p,n)for p,n in ast_paths(tree)if isinstance(n,ast.Constant)and n.value==spec['original_sha256'])
    ports.append(dict(original_sha256=spec['original_sha256'],dependency=spec['dependency'],constant_ast_path=list(route),assignment='PINS',key_ast=ast.dump(ast.Constant(value='p'+str(i)),include_attributes=False)))
   row['receipt_ports']=ports
  for name,row in self.plan['stages'].items():
   for output,desc in row['expected'].items():
    record=dict(status=desc['status'],**desc['scalar_census'])if desc['status']is not None else dict(schema='SYNTHETIC_KAPPA_CERTIFICATE',kappa='62/625',**desc['scalar_census'])
    profiles=desc['row_profiles']
    if profiles:
     blocks=[]
     for profile in profiles:
      lo,hi=profile['rho'];parameters=profile['parameters'];cells=int(parameters[-1])if parameters else(4096 if name=='b2_pilot'else 2048)
      rows=[dict(n=n,rho=[lo,hi],c='1',tau='1/4',epsilon='1/1024',cells_per_piece=cells,normalized_upper='1/5',normalized_upper_float=.2,target='4097/10000',strict_target_pass=True)for n in range(26,31)]
      if name in('b2_pilot','b2_cover'):
       for nr in rows:nr['absmean_upper']='122/125'
      result=dict(rows=rows,seconds=.1,shared_cells=2*cells,per_n_cells=2*cells)
      blocks.append(dict(ordinal=len(blocks),parameters=parameters,result=result))
     if name in('b2_pilot','rho130_pilot'):record['result']=blocks[0]['result']
     else:record['bands']=blocks
    if desc['source_graph_paths']:record['source_sha256']={}
    self.templates[output]=record;desc['mathematical_body_sha256']=canonical(e.projection(record,desc))
  for name,row in self.plan['source_files'].items():
   p=self.cache/name;row.update(bytes=p.stat().st_size,sha256=s.digest(p))
  self.plan['active_source_files']={p:self.plan['source_files'][p]for p in self.plan['active_source_files']}
  self.patchers=[patch.object(s,'plan',return_value=self.plan),patch.object(r.sys,'platform','linux'),patch.object(r.sys,'stdout',io.StringIO())]
  for p in self.patchers:p.start();self.addCleanup(p.stop)

 def fake(self,argv, *,cwd,output_dir,**kw):
  c=Path(cwd);output_dir=Path(output_dir);label=output_dir.name;pass_name,name=label.split('-',1);task=output_dir.parent.parent
  output_dir.mkdir(parents=True);launch=dict(argv=argv,cwd=str(c),output_dir=str(output_dir),sample_seconds=.2,**kw)
  launch['wall_seconds']=float(launch['wall_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds']);launch['checkpoint_paths']=[str(p)for p in launch['checkpoint_paths']];put(output_dir/'launch.json',launch)
  records={}
  for output in s.output_paths(name):
   d=copy.deepcopy(self.templates[output]);desc=self.plan['stages'][name]['expected'][output]
   # Distinct execution durations demonstrate that only enumerated native
   # timer pointers are removed; reused pilot objects remain exact current data.
   for pointer in desc['timing_pointers']:
    parts=pointer.split('/')[1:];target=d
    for p in parts[:-1]:target=target[int(p)]if type(target)is list else target[p]
    target[parts[-1]]=.1 if pass_name=='construct'else.2
   if name in('b2_cover','b3_cover'):
    pilot='b2_pilot'if name=='b2_cover'else'rho130_pilot';d['bands'][0]['result']=s.read(c/s.output_paths(pilot)[-1])['result']
   if desc['source_graph_paths']:d['source_sha256']={str(c/p):s.digest(c/p)for p in desc['source_graph_paths']}
   if hasattr(self,'mutate'):self.mutate(name,d)
   put(c/output,d);records[output]=d
  d=records[s.output_paths(name)[-1]];pin=s.digest(c/s.output_paths(name)[-1]);kind=self.plan['stages'][name]['stdout_rule']['kind'];status=d.get('status')
  if kind=='json':text=json.dumps(d,indent=2)+'\n'
  else:
   if kind=='utility':parts=[status,d['arithmetic_controls'],d['elementary_controls'],d['exact_bernstein_transform_identities'],d['negative_controls'],pin]
   elif kind=='batch_controls':parts=[status,d['power_or_geometric_prefix_comparisons'],d['exact_per_n_cell_comparisons'],d['negative_controls'],pin]
   elif kind=='b2_controls':parts=[status,d['negative_controls'],pin]
   elif kind=='b3_controls':parts=[status,21,105,5,d['negative_controls'],pin]
   elif kind=='extension_controls':parts=[status,15,75,21,d['negative_controls'],pin]
   elif kind in('b2_pilot','rho130_pilot'):
    values=[(v['n'],v['normalized_upper_float'],v['strict_target_pass'])for v in d['result']['rows']];parts=[status,values]+([d['result']['seconds']]if kind=='rho130_pilot'else[])+[pin]
   else:
    count={'b2_cover':115,'b3_cover':110,'b5_cover':30,'extension_cover':75}[kind];start=1 if kind in('b2_cover','b3_cover')else 0
    parts=[status,d['passing_rows'],'of'+str(count),sum(b['result']['seconds']for b in d['bands'][start:]),pin]
   text='SYNTHETIC PROGRESS\n'+' '.join(map(str,parts))+'\n'
  (output_dir/'stdout.txt').write_bytes(text.encode());(output_dir/'stderr.txt').write_bytes(b'')
  checks=r.linux_supervisor._capture_checkpoints(dict(output_dir=str(output_dir),cwd=str(c),checkpoint_paths=[str(p)for p in kw['checkpoint_paths']],disk_bytes=kw['disk_bytes']))
  scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(e.WALL_SECONDS),per_process_RLIMIT_AS_bytes=e.MEMORY_BYTES,
   per_process_RLIMIT_CPU_seconds=e.CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=e.MEMORY_BYTES,sampled_group_CPU_limit_seconds=e.CPU_SECONDS,
   sampled_file_limit_bytes=512*s.MIB,sampled_log_limit_bytes=16*s.MIB,descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
  out=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,elapsed_seconds=.1,
   maximum_sampled_group_RSS_bytes=10*s.MIB,maximum_sampled_group_CPU_seconds=.1,guard_scope=scope,checkpoints=checks,
   **{k+suffix:v for k in('stdout','stderr')for suffix,v in(('_path',str(output_dir/(k+'.txt'))),('_sha256',s.digest(output_dir/(k+'.txt'))))})
  put(output_dir/'supervisor-result.json',out);return out

 def complete(self,name='b2',label='task',effect=None):
  task=self.root/label
  with patch.object(r.linux_supervisor,'run',side_effect=effect or self.fake),patch.object(r,'Follow'):
   result=r.execute(name,task,self.cache,root=self.root)
  return task,result

 def test_both_lanes_run_every_action_twice_and_all_full_flags_remain_false(self):
  for name,total,rows in(('b2',14,115),('higher',16,215)):
   task,result=self.complete(name,label=name);self.assertTrue(result['conditional_cover_arithmetic_completed'])
   self.assertEqual(result['summary']['total_native_actions'],total);self.assertEqual(result['summary']['rows_per_pass'],rows)
   self.assertTrue(result['summary']['fresh_five_row_pilot_in_each_pass']);self.assertTrue(result['summary']['all_closed_seams_verified'])
   for k in e.FLAGS:self.assertIs(result[k],False)
   ledger=s.read(task/'STAGE_OBSERVED.json');self.assertEqual(len(ledger['actions']),total)

 def test_old_successful_output_objects_are_provenance_only_in_both_passes(self):
  task=self.root/'prepared';s.prepare('b2',self.cache,task)
  for pass_name in s.PASSES:
   c=s.capsule(task,pass_name)
   for p in self.plan['stage_outputs']:self.assertFalse((c/p).exists())
  self.assertEqual(len(list((task/'provenance').rglob('*.json'))),14)

 def test_source_port_only_exact_assignment_key_and_old_literal_can_change(self):
  row=self.plan['stages']['absmean_controls'];raw=(self.cache/row['directory']/row['script']).read_bytes();deps={v['dependency']:'1'*64 for v in row['receipt_ports']}
  b,report=s.derive_source(raw,row,deps);self.assertNotEqual(b,raw);self.assertTrue(report['all_other_bytes_unchanged']);self.assertTrue(report['all_other_module_ast_nodes_unchanged'])
  bad=raw+b'PINS = {}\n';badrow=dict(row,script_sha256=hashlib.sha256(bad).hexdigest())
  with self.assertRaises(ValueError):s.derive_source(bad,badrow,deps)
  wrong=copy.deepcopy(row);wrong['receipt_ports'][0]['key_ast']=ast.dump(ast.Constant(value='wrong'),include_attributes=False)
  with self.assertRaises(ValueError):s.derive_source(raw,wrong,deps)
  with self.assertRaises(ValueError):s.derive_source(raw,row,{})

 def test_python313_empty_field_dump_does_not_weaken_inline_or_key_guards(self):
  pin='a'*64;raw=("def main():\n need(sha(B / 'CHECKED.json') == '"+pin+"', 'exact source')\n").encode()
  tree=ast.parse(raw);route,node=next((p,n)for p,n in ast_paths(tree)if isinstance(n,ast.Constant)and n.value==pin)
  left="Call(func=Name(id='sha', ctx=Load()), args=[BinOp(left=Name(id='B', ctx=Load()), op=Div(), right=Constant(value='CHECKED.json'))], keywords=[])"
  comparison=next(n for n in ast.walk(tree)if isinstance(n,ast.Compare));self.assertEqual(s.frozen_ast_dump(comparison.left),left)
  row=dict(script_sha256=hashlib.sha256(raw).hexdigest(),receipt_ports=[dict(original_sha256=pin,dependency='CHECKED.json',constant_ast_path=list(route),assignment=None,key_ast=None,inline_comparison_left_ast=left)])
  original_dump=ast.dump
  def python313_default(node,**kw):return original_dump(node,**kw).replace(', keywords=[]','').replace(', type_ignores=[]','')
  self.assertNotEqual(python313_default(comparison.left,include_attributes=False),left)
  with patch.object(ast,'dump',side_effect=python313_default):
   derived,report=s.derive_source(raw,row,{'CHECKED.json':'b'*64});self.assertEqual(derived,raw.replace(pin.encode(),b'b'*64))
   self.assertTrue(report['all_other_bytes_unchanged']);self.assertTrue(report['all_other_module_ast_nodes_unchanged'])
   bad=copy.deepcopy(row);bad['receipt_ports'][0]['inline_comparison_left_ast']=left.replace("id='sha'","id='wrong'")
   with self.assertRaises(ValueError):s.derive_source(raw,bad,{'CHECKED.json':'b'*64})
   configured=self.plan['stages']['absmean_controls'];source=(self.cache/configured['directory']/configured['script']).read_bytes()
   deps={v['dependency']:'1'*64 for v in configured['receipt_ports']};s.derive_source(source,configured,deps)
   bad=copy.deepcopy(configured);bad['receipt_ports'][0]['key_ast']="Constant(value='not-the-key')"
   with self.assertRaises(ValueError):s.derive_source(source,bad,deps)
  full_fields={'include_attributes':False}
  if 'show_empty'in inspect.signature(original_dump).parameters:full_fields['show_empty']=True
  for node in ast.walk(tree):self.assertEqual(s.frozen_ast_dump(node),original_dump(node,**full_fields))

 def test_unenumerated_nested_seconds_is_not_discarded_from_mathematical_projection(self):
  self.mutate=lambda name,d:d.update(unknown={'seconds':123})if name=='utility'else None
  with self.assertRaises(ValueError):self.complete(label='unknown')
  self.assertFalse((self.root/'unknown/STAGE_COMPLETED.json').exists())

 def test_full_native_source_graph_not_a_rehashed_subset(self):
  def change(name,d):
   if name=='utility':d['source_sha256'].pop(next(iter(d['source_sha256'])))
  self.mutate=change
  with self.assertRaises(ValueError):self.complete(label='subset')
  self.assertFalse((self.root/'subset/STAGE_COMPLETED.json').exists())

 def test_wrong_native_status_controls_or_missing_rows_reject_before_completion(self):
  for i,change in enumerate((lambda d:d.update(status='DELIBERATE_FAILURE'),lambda d:d.update(negative_controls=0))):
   self.mutate=lambda name,d,change=change:change(d)if name=='utility'else None
   with self.assertRaises(ValueError):self.complete(label='failed'+str(i))
   self.assertFalse((self.root/('failed'+str(i))/'STAGE_COMPLETED.json').exists())

 def test_boolean_rc_guard_stderr_hash_or_stopped_copy_fail_closed(self):
  for i,change in enumerate((lambda d:d.update(returncode=False),lambda d:d['guard_scope'].update(proof_acceptance=True),lambda d:d.update(stderr_sha256='0'*64),lambda d:d.update(checkpoints=[]))):
   def fake(*a,**kw):
    out=self.fake(*a,**kw);change(out);put(Path(kw['output_dir'])/'supervisor-result.json',out);return out
   with self.assertRaises(ValueError):self.complete(label='transport'+str(i),effect=fake)
   self.assertFalse((self.root/('transport'+str(i))/'STAGE_COMPLETED.json').exists())

 def test_completed_cache_relocation_revalidates_whole_evidence_without_math(self):
  task,result=self.complete();cache=self.root/'saved';export=r.save_completed(task,cache)
  with patch.object(r.linux_supervisor,'run')as native:
   loaded=r.restore_completed('b2',cache,self.root/'restored',root=self.root)
  self.assertEqual(loaded[1],result);native.assert_not_called()
  Path(export['path']).with_suffix('.zip.sha256').write_bytes(b'bad');self.assertIsNone(r.restore_completed('b2',cache,self.root/'bad-cache',root=self.root))

 def test_phase_source_and_port_ledger_tampering_are_rejected(self):
  task,result=self.complete();p=s.capsule(task,'construct').parent/'PORTS.json';d=s.read(p);d['entries'][2]['report']['all_other_bytes_unchanged']=False;put(p,d)
  with self.assertRaises(ValueError):e.validate_completed(task)

 def test_second_session_reuses_complete_lane_without_any_native_or_download(self):
  task,result=self.complete();cache=self.root/'drive/finite2630-covers-b2/completed'/s.PLAN_SHA256[:16];r.save_completed(task,cache)
  # Short synthetic run identifiers keep the real original relative paths
  # within Windows MAX_PATH; the production Linux naming policy is unchanged.
  with patch.object(r.linux_supervisor,'run')as native,patch.object(s,'obtain_assets')as download,patch.object(r,'datetime')as clock,patch.object(r.uuid,'uuid4',return_value=Mock(hex='x')):
   clock.now.return_value.strftime.return_value='r'
   out=r.run_colab('b2',durable_root=self.root/'drive',work_root=self.root/'runs')
  self.assertTrue(out['status']['conditional_cover_arithmetic_completed'],(out['status'],(Path(out['work'])/'PROGRESS.jsonl').read_text()));native.assert_not_called();download.assert_not_called()

 def test_bounded_safe_zip_members_required_before_extraction(self):
  z=Mock()
  for name in('../escape','/absolute','a//b','a\\b','STAGE_COMPLETED.json'):
   info=zipfile.ZipInfo();info.filename=info.orig_filename=name;z.infolist.return_value=[info]
   with self.assertRaises(ValueError):r.cache_members(z,'b2')

 def test_native_failure_exports_false_final_zip_and_actual_bounded_stderr(self):
  def fake(*a,**kw):
   out=self.fake(*a,**kw);p=Path(kw['output_dir']);(p/'stderr.txt').write_bytes(b'ACTUAL SYNTHETIC COVER FAILURE')
   out.update(status='incomplete',returncode=1,reason='nonzero_subprocess_exit',stderr_sha256=s.digest(p/'stderr.txt'));put(p/'supervisor-result.json',out);return out
  with patch.object(s,'obtain_assets',return_value=None),patch.object(s,'prepare_cache',return_value=self.cache),patch.object(r.linux_supervisor,'run',side_effect=fake),patch.object(r,'Follow'):
   out=r.run_colab('b2',durable_root=self.root/'drive',work_root=self.root/'runs')
  self.assertFalse(out['status']['conditional_cover_arithmetic_completed']);self.assertIn('ACTUAL SYNTHETIC COVER FAILURE',out['status']['error']);self.assertTrue(Path(out['bundle']).is_file())

class ActualSourcePlan(unittest.TestCase):
 def test_actual_source_only_selection_domains_and_complete_original_control_censuses(self):
  d=s.plan();self.assertEqual(len(d['source_files']),48);self.assertEqual(len(d['active_source_files']),34)
  self.assertEqual((s.lane('b2')['rows'],s.lane('higher')['rows']),(115,215));self.assertEqual((s.lane('b2')['closed_strips'],s.lane('higher')['closed_strips']),(23,43))
  self.assertEqual(len(s.lane('b2')['stages']),7);self.assertEqual(len(s.lane('higher')['stages']),8)
  for row in d['stages'].values():
   for p in s.output_paths(next(k for k,v in d['stages'].items()if v is row)):self.assertNotIn(p,d['active_source_files'])
  self.assertEqual(d['stages']['b2_controls']['expected'][s.output_paths('b2_controls')[0]]['scalar_census']['negative_controls'],21)
  self.assertEqual(d['stages']['b3_controls']['expected'][s.output_paths('b3_controls')[0]]['scalar_census']['negative_controls'],16)
if __name__=='__main__':unittest.main()
