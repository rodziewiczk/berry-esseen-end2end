"""Synthetic metadata/interface traps only; no original numerical imports."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import tempfile,types,unittest
from unittest.mock import patch
from be_replay import finite1014_join_evidence as ev,finite1014_join_sources as src,finite1014_join_interfaces as it


def support(n=10,rho='11/10',radius='23/10',q='99/1000'):
 return dict(n=n,K='0',schema='DIRECT_SAME_LAW_CONTACT_SUPPORT_DISCOVERY_V1',rho_upper=rho,radius=radius,q_contact=q,support_sign=0,
  ray_rows=[dict(sign=s,contact_upper='-1',coefficient_at_R='-1',contact_derivative_at_R='-1',contact_derivative_slope_at_R='-1')for s in(-1,1)])


def initial():
 panels=[dict(pl=str(F(i,100)),pu=str(F(i+1,100)))for i in range(100)]
 cover=dict(R='1/10',D='1/10',total=1,active=0,excluded=1,reasons={'synthetic':1},panels=panels)
 stages=[];previous=(None,None)
 for _ in range(8):
  stages.append(dict(input_raw=previous[0],input_D=previous[1],cover=deepcopy(cover),next_raw='10001/100000',next_D='10001/100000'));previous=('10001/100000','10001/100000')
 c=dict(n=10,K='0',target='CE',band='B0',rho_interval=['1','11/10'],q='99/1000',owncap='1047/2500',predecessor_cap='1049/2500',high_cap='69/200',
  predecessor_globally_sharp_assumed=False,predecessor='GLOBAL C9<.423; then SAME-law supported C9 cap',stages=stages,
  profile=dict(radius='23/10',radius_minus='23/10',radius_plus='23/10',cap='1047/2500',grid=[12,12,6,3]),export=deepcopy(cover),
  final_invariants=dict(raw=previous[0],D=previous[1]),refined_support=support(),coarse_support=support(radius='3',q='133/1000'))
 c.update({k:False for k in('predecessor_discharged_here','owncap_verified','high_acceptance_joined','physical_defect_seed_imported','full_cutoff_proved')})
 return c,dict(final_invariants=deepcopy(c['final_invariants'])),dict(n=10,band='B0',signed_cells_per_cover=1)


def resource_interface():
 r=dict(N=10,index=40,K='0',pl='2/5',pu='41/100',rho_hi='11/10',D='3/25',charge_b='1/10',charge_g='1/5',charge_h='3/10',d0='1/10',lambda_max='1/15',
  H_minus='1/10',H_plus='1/10',radius_minus='23/10',radius_plus='23/10',outer0='1',outer1='1',quadratics=[dict(A='1',Fplus='0',Fminus='0',Qbudget='1')])
 raw=dict(pl=r['pl'],pu=r['pu'],A='1/2',B='1/2',beta_lo='-1/20',beta_hi_signed='3/20',mean_hi='1/5')
 s=dict(pl=r['pl'],pu=r['pu'],beta_lo='-1/10',beta='1/5',mean_lo='1/10',mean_hi='1/4')
 cfg=dict(n=10,index=40,K='0',p=[r['pl'],r['pu']],rho_lower='1',rho_upper='11/10',D='3/25',d0='1/10',Lambda='66667/1000000',acquired_lambda_upper='66667/1000000',
  Hminus='1/10',Hplus='1/10',radius_minus='23/10',radius_plus='23/10',outer0='1',outer1='1',binary_charge='1/10',gap_charge='1/5',noise_charge='3/10',
  sign_premise=dict(conditional_means_zero=True,schema='ACTUAL_SIGN_CONDITIONED_MARGINAL_V1',resource_status='ASSUMED_ACQUIRED_FOR_CONDITIONAL_TEST',negative_endpoint_lower='1/2',positive_endpoint_lower='1/2'),
  acquired_beta=['-1/20','3/20'],acquired_mean=['1/10','1/5'],quadratics=deepcopy(r['quadratics']))
 return dict(result=dict(result=r,raw_row=raw),source=s),cfg


class MetadataInterfaces(unittest.TestCase):
 def test_original_complete_interface_asts_retained_without_import(self):
  self.assertEqual(it.verify_reference_projection(),it.REFERENCE_SHA)

 def test_unseeded_initial_chain_support_and_100_closed_panels(self):
  c,a,row=initial();ev.initial_scope(c,a,row)
  for mutation in('seed','rounding','grid','p_seam','global9','flag','ray'):
   with self.subTest(mutation=mutation):
    v=deepcopy(c)
    if mutation=='seed':v['stages'][0]['input_D']='0'
    elif mutation=='rounding':v['stages'][0]['next_raw']='1/10'
    elif mutation=='grid':v['profile']['grid']=[1,1,1,1]
    elif mutation=='p_seam':v['export']['panels'][-1]['pu']='99/100'
    elif mutation=='global9':v['predecessor_globally_sharp_assumed']=True
    elif mutation=='flag':v['physical_defect_seed_imported']=True
    else:v['refined_support']['ray_rows'][0]['contact_derivative_slope_at_R']='0'
    with self.assertRaises(ValueError):ev.initial_scope(v,a,row)

 def test_whole_simultaneous_interface_and_directed_rounding(self):
  row,cfg=resource_interface();it.interface(row,cfg,'B0',40,10)
  for mutation in('bool_n','rho','shared_D','endpoint','beta','price','curvature','missing_quadratic'):
   with self.subTest(mutation=mutation):
    r,c=deepcopy(row),deepcopy(cfg)
    if mutation=='bool_n':c['n']=True
    elif mutation=='rho':c['rho_upper']='1'
    elif mutation=='shared_D':r['result']['result']['D']='1/10'
    elif mutation=='endpoint':c['sign_premise']['negative_endpoint_lower']='0'
    elif mutation=='beta':c['acquired_beta']=['-1/10','1/5']
    elif mutation=='price':c['gap_charge']='1/4'
    elif mutation=='curvature':c['quadratics'][0]['Qbudget']='0'
    else:c['quadratics']=[]
    with self.assertRaises(ValueError):it.interface(r,c,'B0',40,10)

 def test_finite_induction_cannot_jump_failed_predecessor(self):
  rows=ev.sequential(True,{11:True,12:False,13:True,14:True})
  self.assertEqual([r['conditional_finite_result_established']for r in rows],[True,False,False,False])
  self.assertFalse(ev.sequential(False,{11:True,12:True,13:True,14:True})[-1]['conditional_finite_result_established'])
  for v in({11:True,12:True,13:True,14:True,15:True},{11:1,12:True,13:True,14:True}):
   with self.assertRaises(ValueError):ev.sequential(True,v)

 def test_four_closed_restrictions_keep_other_axes_and_no_duplicate_part(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);cfg=dict(p=['2/5','41/100'],Lambda='1/10',d0='1/10');cuts=[str(F(2,5)+F(1,100)*j/4)for j in range(5)];group=[]
   for part in range(4):
    task=root/str(part);cap=task/'capsule/native';cap.mkdir(parents=True)
    lineage=dict(resource_candidate_sha256='a'*64,resource_replay_sha256='b'*64,resource_row_sha256='c'*64)
    sub=dict(part=part,parts=4,n=10,index=40,original_p=cfg['p'],schema='ORIGINAL_CONTRACT_FOUR_CLOSED_P_SUBPANELS_V1',cuts=cuts,p=cuts[part:part+2],contract_sha256='d'*64,**lineage)
    for name,d in(('SUBDOMAIN.json',sub),('PARENT.json',dict(contract_sha256='d'*64,kernel_sha256={'kernel.py':'e'*64},**lineage)),('contract.json',lineage),('KERNEL_COPY_MANIFEST.json',dict(files={'kernel.py':'e'*64})),('ACCEPTED.json',dict(root_domain=[sub['p'],['0','1/10'],['0','1'],['-1/2','1/2'],['0','1/10']],part=part,parts=4,negative_controls=list(range(34)),subdomain_negative_controls=list(range(22))))):
     (cap/name).write_bytes(src.dump(d))
    group.append(dict(task=task,row=dict(directory='native',output='ACCEPTED.json',contract_sha256='d'*64,job_id='part'+str(part))))
   self.assertEqual([p['part']for p in ev._restriction(group,cfg,10,40)],[0,1,2,3])
   accepted=root/'2/capsule/native/ACCEPTED.json';v=src.read(accepted);v['root_domain'][1]=['0','1/20'];accepted.write_bytes(src.dump(v))
   with self.assertRaises(ValueError):ev._restriction(group,cfg,10,40)

 def test_cross_control_dependency_must_equal_actual_preceding_output(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);name=src.DEPENDENCIES[0];rows=[dict(job_id='first',output=name),dict(job_id='second',output='work/second.json')];records=[]
   for row in rows:
    task=root/row['job_id'];p=task/'capsule'/row['output'];p.parent.mkdir(parents=True);p.write_bytes(src.dump({'current':row['job_id']}));records.append(dict(job_id=row['job_id'],task_relative=row['job_id'],validated={'checked':row['job_id']}))
   pin=src.digest(root/'first/capsule'/name);bad=False
   def verify(task):
    second=Path(task).name=='second';return(dict(original_sources={name:{}},dependency_files_sha256=({name:('0'*64 if bad else pin)}if second else{})),rows[1 if second else 0])
   status=dict(schema='FINITE1014_FULL_FINITE_JOIN_SESSION_V1',controls=records,imports=[],**{f:False for f in ev.controls.FLAGS})
   with patch.object(src,'jobs',return_value=rows),patch.object(src,'verify',side_effect=verify),patch.object(ev.controls,'validate_completed',side_effect=lambda task:{'checked':Path(task).name}),patch.object(ev,'_validated_inputs',return_value=({},{},{})),patch.object(ev,'fourier_and_coarse',return_value={}),patch.object(ev,'finite_families',return_value={}),patch.object(ev,'implementation',return_value={}):
    self.assertTrue(ev.validate_batch(root,status)['conditional_finite_chain_verified']);bad=True
    with self.assertRaises(ValueError):ev.validate_batch(root,status)

 def test_current_parent_equivalence_omits_only_named_top_level_metadata(self):
  with tempfile.TemporaryDirectory()as tmp:
   task=Path(tmp);row=dict(resource_candidate='resource/CANDIDATE.json',resource_receipt='resource/ACCEPTED.json');payload=dict(n=10,rows=[{'index':0,'mathematical_seconds':5}],files_sha256={'old':'a'},initial_candidate_sha256='a',initial_acceptance_sha256='b')
   receipt=dict(n=10,rows=deepcopy(payload['rows']),files_sha256={'old':'a'},candidate_sha256='c',timings_seconds=[1])
   for prefix in('provenance','capsule'):
    for name,d in((row['resource_candidate'],payload),(row['resource_receipt'],receipt)):
     p=task/prefix/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(src.dump(d))
   fresh=deepcopy(payload);fresh.update(files_sha256={'fresh':'z'},initial_candidate_sha256='d',initial_acceptance_sha256='e');(task/'capsule'/row['resource_candidate']).write_bytes(src.dump(fresh))
   native=deepcopy(receipt);native.update(files_sha256={'fresh':'z'},candidate_sha256='f',timings_seconds=[2]);(task/'capsule'/row['resource_receipt']).write_bytes(src.dump(native))
   current_row=task/'row.json';current_row.write_bytes(src.dump({'index':0,'actual':'row'}));contract=dict(resource_candidate_sha256=src.digest(task/'provenance'/row['resource_candidate']),resource_replay_sha256=src.digest(task/'provenance'/row['resource_receipt']),resource_row_sha256=src.digest(current_row))
   bridge=ev._parent_binding(dict(task=task,row=row),contract,current_row);self.assertTrue(bridge['all_mathematical_fields_identical']);self.assertFalse(bridge['historical_acceptance_promoted'])
   fresh['rows'][0]['mathematical_seconds']=6;(task/'capsule'/row['resource_candidate']).write_bytes(src.dump(fresh))
   with self.assertRaises(ValueError):ev._parent_binding(dict(task=task,row=row),contract,current_row)

 def test_exact234_import_set_full_validators_and_tampered_record(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);records=[];calls=[];mods={};core_rows=[dict(case_id='case'+str(i),n=10+i//2,band=('B0','BN')[i%2])for i in range(10)];count_rows=[dict(job_id='count'+str(i))for i in range(217)]
   def add(key,checked):
    p=root/key.replace(':','-');p.mkdir();records.append(dict(key=key,task_relative=p.name,validated=checked));return p
   for key,_,e,s,_ in ev.PARENTS:
    add(key,{'key':key});mods[e]=types.SimpleNamespace(validate_completed=lambda task,k=key:(calls.append(k)or {'key':k}));mods[s]=types.SimpleNamespace()
   for row in core_rows:add('core:'+row['case_id'],dict(summary=dict(case_id=row['case_id'])))
   for row in count_rows:add('count:'+row['job_id'],dict(job_id=row['job_id']))
   mods['finite1014_core_sources']=types.SimpleNamespace(plan=lambda:dict(cases=core_rows));mods['finite1014_core_evidence']=types.SimpleNamespace(validate_completed=lambda task:(calls.append('core')or dict(summary=dict(case_id=task.name.removeprefix('core-')))))
   mods['finite1039_sources']=types.SimpleNamespace(jobs=lambda lane:count_rows);mods['finite1039_count_evidence']=types.SimpleNamespace(validate_completed=lambda task:(calls.append('count')or dict(job_id=task.name.removeprefix('count-'))))
   with patch.object(ev,'module',side_effect=lambda name:mods[name]):
    parents,cores,counts=ev._validated_inputs(root,records);self.assertEqual((len(parents),len(cores),len(counts),len(calls)),(7,10,217,234))
    for bad in(records[:-1],records+[records[0]],deepcopy(records)):
     if len(bad)==234:bad[-1]['validated']['job_id']='different'
     with self.assertRaises(ValueError):ev._validated_inputs(root,bad)


if __name__=='__main__':unittest.main()
