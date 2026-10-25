"""Complete three-action fixture, prefix relocation and rejection tests.

The only program in the fixture is a trap; linux_supervisor.run is mocked.
These tests are execution/evidence infrastructure, not n25 computations.
"""
from copy import deepcopy
from pathlib import Path
import hashlib,json,shutil,sys,tempfile,unittest
from unittest.mock import patch
from be_replay import n25_acquisitions as r,linux_supervisor

def put(p,obj):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(r.src.base.encoded(obj));return r.sha(p)

class Acquisition(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name);self.task=self.root/'task'
  self.folder='canonical';self.trap=b'raise AssertionError("NO MATHEMATICAL SOURCE EXECUTION IN LOCAL TESTS")\n'
  initial=dict(schema='SYNTHETIC_COMPLETE_INITIAL',profile=dict(n=25),rows=list(range(100)))
  resource=dict(schema='SYNTHETIC_COMPLETE_RESOURCE',profile=dict(n=25),rows=list(range(100)),initial_acceptance_sha256='0'*64)
  self.proofs={'initial-accept':initial,'resource-construct':resource,'resource-accept':resource}
  self.actions=[];self.refs={}
  for name,proof,out,parents in [('initial-accept','INITIAL.json','INITIAL_ACCEPTED.json',[]),('resource-construct','RESOURCE.json',None,['initial_acceptance_sha256']),('resource-accept','RESOURCE.json','RESOURCE_ACCEPTED.json',['initial_acceptance_sha256'])]:
   view=deepcopy(self.proofs[name]);[view.pop(k)for k in parents]
   a=dict(id=name,folder=self.folder,script='trap.py',args=[name],kind='initial'if name=='initial-accept'else'global_resource',proof=proof,receipt=out,
    native_checker=self.folder+'/trap.py',fresh_parent_metadata_fields=parents,proof_schema=view['schema'],proof_mathematical_projection_sha256=r.src.base.sha(r.src.base.encoded(view)))
   if out:
    ref=dict(status='SYNTHETIC_NOT_PROOF',proof_sha256='0'*64,checker_sha256=hashlib.sha256(self.trap).hexdigest(),seconds=.1,negative_controls=['control'+str(i)for i in range(12)])
    if name!='initial-accept':ref['initial_acceptance_sha256']='0'*64
    a.update(receipt_fields=list(ref),expected_receipt_status=ref['status'],negative_controls=ref['negative_controls']);self.refs['fixture/'+name]=ref
   self.actions.append(a)
  self.spec=dict(id='fixture',actions=self.actions,local_aliases=[],canonical_directory=self.folder)
  self.task.mkdir();source=self.task/'source'/r.src.PREFIX/self.folder;source.mkdir(parents=True)
  (source/'trap.py').write_bytes(self.trap);put(source/'INITIAL.json',initial)
  shutil.copytree(self.task/'source',self.task/'epoch')
  self.selected={r.src.PREFIX+self.folder+'/'+p.name:dict(bytes=p.stat().st_size,sha256=r.sha(p))for p in source.iterdir()}
  for obj,name,value in [(r.src,'definition',lambda f:self.spec),(r.src,'selected',lambda f:self.selected),
   (r.src,'verify',lambda t,f:True),(r.src,'epoch_rows',lambda t,f:self.selected),(r,'references',lambda:self.refs),
   (r.linux_supervisor,'run',self.fake)]:
   q=patch.object(obj,name,value);q.start();self.addCleanup(q.stop)
  put(self.task/'ACQUISITION.json',dict(schema='N25_ORIGINAL_ACQUISITION_TASK_V1',family='fixture',source_plan_sha256=r.src.PLAN_SHA256,
   implementation=r.implementation(),original_task_root=str(self.task),python_executable=sys.executable,python_version=sys.version,**r.FLAGS))
  put(self.task/'ACTIONS.json',dict(actions=[]))

 def fake(self,argv,*,cwd,output_dir,**kw):
  directory=Path(output_dir);directory.mkdir(parents=True);cwd=Path(cwd);name=argv[-1];a=next(a for a in self.actions if a['id']==name)
  if name=='resource-construct':
   proof=deepcopy(self.proofs[name]);proof['initial_acceptance_sha256']=r.sha(cwd/'INITIAL_ACCEPTED.json');put(cwd/a['proof'],proof)
  if a['receipt']:
   ref=deepcopy(self.refs['fixture/'+name]);ref['seconds']=.2;ref['proof_sha256']=r.sha(cwd/a['proof'])
   if 'initial_acceptance_sha256'in ref:ref['initial_acceptance_sha256']=r.sha(cwd/'INITIAL_ACCEPTED.json')
   put(cwd/a['receipt'],ref)
  (directory/'stdout.txt').write_text('SYNTHETIC FIXTURE ONLY\n');(directory/'stderr.txt').write_bytes(b'')
  launch=dict(argv=argv,cwd=str(cwd),output_dir=str(directory),sample_seconds=.2,**kw);launch['checkpoint_paths']=[str(p)for p in kw['checkpoint_paths']]
  put(directory/'launch.json',launch);checkpoints=linux_supervisor._capture_checkpoints(dict(output_dir=str(directory),cwd=str(cwd),checkpoint_paths=launch['checkpoint_paths'],disk_bytes=kw['disk_bytes']))
  guard=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(r.WALL),per_process_RLIMIT_AS_bytes=r.MEMORY,
   per_process_RLIMIT_CPU_seconds=r.CPU,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=r.MEMORY,
   sampled_group_CPU_limit_seconds=r.CPU,sampled_file_limit_bytes=512*r.io.MIB,sampled_log_limit_bytes=16*r.io.MIB,
   descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False,sampled_group_CPU_includes_waited_descendants=True)
  result=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,guard_scope=guard,checkpoints=checkpoints,
   elapsed_seconds=.1,maximum_sampled_group_CPU_seconds=.1,maximum_sampled_group_RSS_bytes=10*r.io.MIB)
  for key in ('stdout','stderr'):result[key+'_path']=str(directory/(key+'.txt'));result[key+'_sha256']=r.sha(directory/(key+'.txt'))
  if hasattr(self,'mutate'):self.mutate(result)
  put(directory/'supervisor-result.json',result);return result

 def test_all_three_actions_and_duration_dependent_parent_identity(self):
  for a in self.actions:r.execute_next(self.task,'fixture',log_root=self.root)
  checked=r.validate_prefix(self.task,require_complete=True);self.assertEqual(checked['completed_actions'],3);self.assertTrue(checked['complete_family'])
  self.assertFalse(checked['full66_complete']);self.assertFalse(checked['all_index_conclusion_verified'])

 def test_complete_prefix_relocation_then_remaining_real_invocation_context(self):
  r.execute_next(self.task,'fixture',log_root=self.root);relocated=self.root/'moved';shutil.copytree(self.task,relocated)
  self.assertEqual(r.validate_prefix(self.task),r.validate_prefix(relocated))
  for a in self.actions[1:]:r.execute_next(relocated,'fixture',log_root=self.root)
  self.assertTrue(r.validate_prefix(relocated,require_complete=True)['complete_family'])

 def test_bad_transport_never_advances_completed_prefix(self):
  self.mutate=lambda d:d.update(returncode=False)
  with self.assertRaises(ValueError):r.execute_next(self.task,'fixture',log_root=self.root)
  self.assertEqual(r.read(self.task/'ACTIONS.json')['actions'],[])

 def test_no_missing_stage_as_complete_and_no_changed_math_payload(self):
  r.execute_next(self.task,'fixture',log_root=self.root)
  with self.assertRaises(ValueError):r.validate_prefix(self.task,require_complete=True)
  p=r.family_root(self.task)/self.folder/'INITIAL.json';d=r.read(p);d['rows'].pop();put(p,d)
  with self.assertRaises(ValueError):r.validate_prefix(self.task)

if __name__=='__main__':unittest.main()
