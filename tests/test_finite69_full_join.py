"""65 infrastructure fixtures and optional whole original-source interfaces.

No test invokes a numerical oracle. Synthetic stopped captures are test data,
never production artifacts. BE_65_SOURCE/CONTRACTS enable the full284 data test.
"""
from pathlib import Path
import copy,json,os,shutil,tempfile,unittest
from unittest.mock import patch
from be_replay import finite69_join_sources as src,finite69_remaining as run,finite69_join as join
from be_replay import finite69_join_interfaces as interfaces,finite69_sources as counts,delivery_transport as tx
from be_replay.colab_batch import atomic_json

class Infrastructure(unittest.TestCase):
 def test_origin_paths_preserve_actual_platform_and_posix_captures(self):
  self.assertEqual(run.original({'original_task_root':'/content/run'},'work/input.json'),'/content/run/capsule/work/input.json')
  self.assertEqual(run.originating({'original_task_root':'C:\\run'},'executions','construct'),'C:\\run\\executions\\construct')
  self.assertEqual(run.original({'original_task_root':'C:\\run'},'work/input.json'),'C:\\run\\capsule\\work\\input.json')

 def test_all_remaining19_original_invocations_and_full_native_families(self):
  p=src.plan();self.assertEqual(sum(len(s['actions'])for s in p['stages'].values()),19)
  self.assertEqual(len(p['semantic_inputs']),300)
  self.assertEqual(len(counts.jobs('count')),284)
  self.assertEqual(run.CPU_SECONDS,82800);self.assertEqual(run.WALL_SECONDS,82800)
  self.assertFalse(p['arithmetic_computed']);self.assertFalse(p['global_proof_accepted'])
  self.assertEqual(set(p['stages']['support']['parents']),{'owncaps','auxiliary','bridge','radius'})

 def test_handled_failure_writes_complete_error_zip_and_no_acceptance(self):
  with tempfile.TemporaryDirectory()as d,patch.object(join,'import_inputs',side_effect=ValueError('fixture failed parent')):
   result=join.run_colab(durable_root=Path(d)/'drive',work_root=Path(d)/'work',backup_interval=1)
   self.assertEqual(result['status']['state'],'INCOMPLETE');self.assertTrue(Path(result['bundle']).is_file())
   self.assertFalse(result['status']['conditional_finite_chain_verified']);self.assertFalse(result['status']['global_proof_accepted'])

 def test_waiting_inputs_do_not_set_finite_conclusion(self):
  def import_(root,durable,status):status['imports']=[];return ['scalar56K','count:n6.B0.p37']
  def restore_(cache,dest,validator,log):
   stage=Path(cache).name;p=Path(dest)/stage;p.mkdir(parents=True)
   return p,dict(stage=stage,fixture=True),{}
  with tempfile.TemporaryDirectory()as d,patch.object(join,'import_inputs',side_effect=import_),\
   patch.object(src,'obtain_assets',return_value={}),patch.object(src,'prepare_cache',return_value=Path(d)),\
   patch.object(src,'plan',return_value=dict(semantic_inputs={},stages={})),\
   patch.object(tx,'restore',side_effect=restore_),patch.object(run,'execute')as execute:
   result=join.run_colab(durable_root=Path(d)/'drive',work_root=Path(d)/'work',backup_interval=1)
   execute.assert_not_called();self.assertEqual(result['status']['state'],'WAITING')
   self.assertFalse(result['status']['conditional_finite_chain_verified']);self.assertTrue(Path(result['bundle']).is_file())

 def test_finite_only_induction_has_all14_controls_and_no_incoming_tail(self):
  finite=dict(conditional_same_law_interfaces=True,bands=[dict(n=n,band=b,rho=list(interfaces.BANDS[b][:2]))
   for n in range(6,10)for b in sorted(interfaces.BANDS)])
  result=interfaces.induction(finite,global_auxiliary5=True)
  self.assertEqual(len(result['negative_controls']),14);self.assertIsNone(result['chain']['incoming_eventual10_tail'])
  self.assertFalse(result['global_proof_accepted'])
  finite['conditional_same_law_interfaces']=False
  with self.assertRaises(ValueError):interfaces.induction(finite,global_auxiliary5=True)

class OriginalSourceInterfaces(unittest.TestCase):
 def setUp(self):
  self.source=Path(os.environ.get('BE_65_SOURCE','/nonexistent-complete65-source'))
  self.contracts=Path(os.environ.get('BE_65_CONTRACTS','/nonexistent-complete65-contracts'))
  if not(self.source.is_dir()and self.contracts.is_dir()):self.skipTest('Optional original source-only preparation absent')

 def test_all284_physical_interfaces_and1200_closed_panels(self):
  items={r['job_id']:dict(task=self.contracts)for r in counts.jobs('count')}
  r=interfaces.finite_cover(self.source,items,{}, {},bind=False)
  self.assertEqual(len(r['count_interfaces']),284);self.assertEqual(r['panels'],1200)
  self.assertEqual(r['census'],dict(resource=910,sign_mass=6,count=284));self.assertFalse(r['conditional_same_law_interfaces'])

 def test_directed_prices_signed_gamma_and_probability_mutations_rejected(self):
  row=counts.jobs('count')[0];s=row['selection'];contract=src.read(self.contracts/'capsule'/s['capsule']/'contract.json')
  physical=src.read(self.source/contract['resource_path']);readers=interfaces.programs(self.source)
  for key,value in [('noise_charge','1'),('acquired_gamma',['0','0']),('p',['0','1']),('acquired_inward_upper','1'),('geometry_gap_lower','0')]:
   bad=copy.deepcopy(contract);bad['rows'][0][key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):interfaces.interface(physical,bad,s,readers)

 def test_high_three_action_synthetic_transport_reader_relocation_and_mutation(self):
  def fake(argv,**kw):
   out=Path(kw['output_dir']);out.mkdir(parents=True);cwd=Path(kw['cwd']);c=task/'capsule';stage=src.plan()['stages']['high'];a=stage['actions'][len(calls)]
   for n in sorted(a['outputs'],key=lambda n:'/engine/'not in n):
    p=c/n;p.parent.mkdir(parents=True,exist_ok=True)
    if '/engine/'in n:shutil.copyfile(c/stage['native']/p.name,p)
    elif n in stage['output_references']:atomic_json(p,stage['output_references'][n])
    else:
     packet=copy.deepcopy(stage['reference']);g=dict(src.read(c/stage['native']/'MANIFEST.json')['files_sha256'])
     for n2 in[stage['native']+'/MANIFEST.json',stage['native']+'/RESULT.json',stage['native']+'/REPLAY_RESULT.json',stage['audit']+'/check.py',stage['audit']+'/REVIEW.txt']+[stage['audit']+'/engine/'+v for v in('bound.py','kernel.py','universal.py')]:g[n2]=src.digest(c/n2)
     for act in stage['actions']:
      if 'capture'in act:
       for stream in('metadata.json','stdout.txt','stderr.txt'):
        n2=act['capture']+'/'+stream;g[n2]=src.digest(c/n2)
     packet['files_sha256']=g;atomic_json(p,packet)
   packet=src.read(c/stage['result'])if a['id']=='readback'else src.read(c/a['outputs'][0])
   (out/'stdout.txt').write_text(json.dumps({k:v for k,v in packet.items()if k not in(('files_sha256','rows','cell_tests')if a['id']=='readback'else('files_sha256',))})+'\n');(out/'stderr.txt').write_text('')
   launch=dict(argv=argv,cwd=str(cwd),output_dir=str(out),**{k:v for k,v in kw.items()if k not in('cwd','output_dir','checkpoint_paths')},checkpoint_paths=[str(p)for p in kw['checkpoint_paths']])
   launch['wall_seconds']=float(launch['wall_seconds']);launch['sample_seconds']=float(launch['sample_seconds']);launch['heartbeat_seconds']=float(launch['heartbeat_seconds'])
   atomic_json(out/'launch.json',launch);checks=[]
   for p in kw['checkpoint_paths']:
    p=Path(p);copy_=out/'checkpoints'/p.relative_to(cwd);copy_.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy_)
    checks.append(dict(source_path=str(p),exists=True,trusted_certificate=False,path=str(copy_),bytes=p.stat().st_size,sha256=src.digest(p)))
   observed=dict(status='completed',returncode=0,reason=None,mode='untrusted_search',proof_accepted=False,sample_count=1,
    elapsed_seconds=.001,maximum_sampled_group_RSS_bytes=1,maximum_sampled_group_CPU_seconds=.001,guard_scope=run.guard_scope(),checkpoints=checks)
   for stream in('stdout','stderr'):observed.update({stream+'_path':str(out/(stream+'.txt')),stream+'_sha256':src.digest(out/(stream+'.txt'))})
   atomic_json(out/'supervisor-result.json',observed);calls.append(a['id']);return observed
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);task=root/'high';calls=[]
   with patch.object(run.supervisor,'run',side_effect=fake):checked=run.execute(self.source,task,'high',root=root)
   self.assertEqual(calls,['construct','replay','readback']);self.assertTrue(checked['arithmetic_completed']);self.assertFalse(checked['global_proof_accepted'])
   moved=root/'relocated';shutil.copytree(task,moved);self.assertEqual(run.validate_completed(moved),checked)
   result=moved/'capsule'/src.plan()['stages']['high']['result'];packet=src.read(result);packet['counts']['domain_negative_controls']-=1;atomic_json(result,packet)
   with self.assertRaises(ValueError):run.validate_completed(moved)

if __name__=='__main__':unittest.main()
