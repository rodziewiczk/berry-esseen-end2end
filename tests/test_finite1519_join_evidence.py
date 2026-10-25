"""Full finite57H synthetic semantic fixtures; no original arithmetic runs."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import tempfile,types,unittest
from unittest.mock import patch
from be_replay import finite1519_join_evidence as ev,finite1519_join_control_sources as src
from tests.test_finite1519_join_interfaces import fixture as interface_fixture


def put(path,value):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(src.encoded(value));return src.digest(path)


def support(n=15,band='B0',resource=False):
 _,hi,_,q,_,_=ev.BANDS[band];radius=ev.refined_radius(n,band)
 return dict(n=n,K='0',schema='DIRECT_FIXED_INDEX_GAUSSIAN_SUPPORT_V1'if resource else'DIRECT_SAME_LAW_CONTACT_SUPPORT_DISCOVERY_V1',
  rho_upper=hi,radius=radius,**{'q'if resource else'q_contact':q if n==15 else'0'},support_sign=0,
  ray_rows=[dict(sign=s,contact_upper='-1',coefficient_at_R='-1',contact_derivative_at_R='-1',contact_derivative_slope_at_R='-1')for s in(-1,1)])


def initial(n=15,band='B0'):
 lo,hi,own,q,_,_=ev.BANDS[band];radius=ev.refined_radius(n,band)
 panels=[dict(pl=str(F(i,100)),pu=str(F(i+1,100)),beta_lo='-1/2',beta='1/2',mean_lo='1/10',mean_hi='1/5')for i in range(100)]
 cover=dict(R='1/10',D='1/10',total=1,active=0,excluded=1,reasons={'synthetic':1},panels=panels)
 stages=[];previous=(None,None)
 for _ in range(8):
  stages.append(dict(input_raw=previous[0],input_D=previous[1],cover=deepcopy(cover),next_raw='10001/100000',next_D='10001/100000'));previous=('10001/100000','10001/100000')
 c=dict(n=n,K='0',target='CE',band=band,rho_interval=[lo,hi],q=q if n==15 else'0',owncap=own,old_support_radius='3',failure=None,
  stages=stages,export=deepcopy(cover),final_invariants=dict(raw=previous[0],D=previous[1]),chosen_support=dict(radius=radius,proof=support(n,band)),
  profile=dict(n=n,nmax=n,radius=radius,radius_minus=radius,radius_plus=radius,cap=own,grid=[12,12,6,3]))
 c.update({k:False for k in('predecessor_verified','owncap_verified','same_law_fourier_verified','old_target_specific_resources_imported','cutoff15_proved')})
 return c,dict(final_invariants=deepcopy(c['final_invariants'])),dict(n=n,band=band,signed_cells_per_cover=1)


class Semantic(unittest.TestCase):
 def setUp(self):
  scratch=src.ROOT/'work/finite1519-join-fixtures';scratch.mkdir(parents=True,exist_ok=True)
  self.tmp=tempfile.TemporaryDirectory(dir=scratch);self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)

 def test_unseeded_initial_all_cases_including_original_n19_bn_radius(self):
  for n in range(15,20):
   for band in ev.BANDS:ev.initial_scope(*initial(n,band))
  self.assertEqual(ev.refined_radius(19,'BN'),'23/10');self.assertEqual(ev.refined_radius(18,'BN'),'12/5')
  for mutation in('seed','rounding','seam','ray','radius','q','flag'):
   c,a,row=initial(19,'BN')
   if mutation=='seed':c['stages'][0]['input_D']='0'
   elif mutation=='rounding':c['stages'][0]['next_raw']='1/10'
   elif mutation=='seam':c['export']['panels'][-1]['pu']='99/100'
   elif mutation=='ray':c['chosen_support']['proof']['ray_rows'][0]['contact_upper']='0'
   elif mutation=='radius':c['profile']['radius']='12/5'
   elif mutation=='q':c['q']='1/1000'
   else:c['predecessor_verified']=True
   with self.subTest(mutation=mutation),self.assertRaises(ValueError):ev.initial_scope(c,a,row)

 def test_whole_current_parent_math_bridge_rejects_nested_field_changes(self):
  task=self.root/'parent';spec=dict(resource_candidate='resource/CANDIDATE.json',resource_receipt='resource/ACCEPTED.json')
  c=dict(n=15,rows=[dict(index=3,seconds_mathematical=7)],files_sha256={'old':'a'},initial_candidate_sha256='a',initial_acceptance_sha256='b')
  a=dict(n=15,rows=deepcopy(c['rows']),files_sha256={'old':'a'},candidate_sha256='c',timings_seconds=[1])
  for prefix in('provenance','capsule'):
   put(task/prefix/spec['resource_candidate'],c);put(task/prefix/spec['resource_receipt'],a)
  fresh=deepcopy(c);fresh.update(files_sha256={'new':'z'},initial_candidate_sha256='d',initial_acceptance_sha256='e');put(task/'capsule'/spec['resource_candidate'],fresh)
  rec=deepcopy(a);rec.update(files_sha256={'new':'z'},candidate_sha256='f',timings_seconds=[2]);put(task/'capsule'/spec['resource_receipt'],rec)
  row=task/'row.json';put(row,dict(index=3));contract=dict(resource_candidate_sha256=src.digest(task/'provenance'/spec['resource_candidate']),
   resource_replay_sha256=src.digest(task/'provenance'/spec['resource_receipt']),resource_row_sha256=src.digest(row))
  bridge=ev._parent_binding(dict(task=task,row=spec),contract,row);self.assertTrue(bridge['all_mathematical_fields_identical'])
  fresh['rows'][0]['seconds_mathematical']=8;put(task/'capsule'/spec['resource_candidate'],fresh)
  with self.assertRaises(ValueError):ev._parent_binding(dict(task=task,row=spec),contract,row)

 def test_exact164_imports_require_whole_validators_and_full_predecessor(self):
  records=[];modules={};calls=[]
  def add(key,checked):
   p=self.root/key.replace(':','-');p.mkdir();records.append(dict(key=key,task_relative=p.name,validated=checked,export={}))
  for key,_,e,s,_ in ev.PARENTS:
   add(key,dict(key=key));modules[e]=types.SimpleNamespace(validate_completed=lambda task,k=key:(calls.append(k)or dict(key=k)));modules[s]=types.SimpleNamespace()
  previous=dict(conditional_finite_chain_verified=True,summary=dict(finite_indices=list(range(10,15)),analytic_premises=['Synthetic predecessor analytic premise']))
  add('56I',previous);modules['finite1014_join_evidence']=types.SimpleNamespace(validate_completed=lambda task:(calls.append('56I')or previous))
  core=[dict(case_id='case'+str(i),n=15+i//2,band=('B0','BN')[i%2])for i in range(10)]
  counts=[dict(job_id='count'+str(i))for i in range(147)]
  for row in core:add('core:'+row['case_id'],dict(summary=dict(case_id=row['case_id'])))
  for row in counts:add('count:'+row['job_id'],dict(job_id=row['job_id']))
  modules['finite1519_core_sources']=types.SimpleNamespace(plan=lambda:dict(cases=core))
  modules['finite1519_core_evidence']=types.SimpleNamespace(validate_completed=lambda task:(calls.append('core')or dict(summary=dict(case_id=task.name.removeprefix('core-')))))
  modules['finite1039_sources']=types.SimpleNamespace(jobs=lambda lane:counts)
  modules['finite1039_count_evidence']=types.SimpleNamespace(validate_completed=lambda task:(calls.append('count')or dict(job_id=task.name.removeprefix('count-'))))
  with patch.object(ev,'module',side_effect=lambda name:modules[name]):
   result=ev._validated_inputs(self.root,records);self.assertEqual(tuple(map(len,result[:3])),(6,10,147));self.assertEqual(len(calls),164)
   for bad in(records[:-1],records+[records[0]],deepcopy(records)):
    if len(bad)==164:bad[-1]['validated']['job_id']='different'
    with self.assertRaises(ValueError):ev._validated_inputs(self.root,bad)
   previous['conditional_finite_chain_verified']=False
   with self.assertRaises(ValueError):ev._validated_inputs(self.root,records)

 def make_families(self):
  cores={};counts={};remaining=147
  for n in range(15,20):
   for band in ev.BANDS:
    task=self.root/(str(n)+band);c,a,spec=initial(n,band);spec.update(initial_candidate='initial.json',initial_receipt='initial-accepted.json',resource_candidate='resource/'+band+'/CANDIDATE.json',resource_receipt='resource/'+band+'/ACCEPTED.json',resource_directory='resource')
    cp=put(task/'capsule'/spec['initial_candidate'],c);ap=put(task/'capsule'/spec['initial_receipt'],a);descs=[];active=min(15,remaining);remaining-=active
    for i in range(100):
     source=deepcopy(c['export']['panels'][i]);source['rho_lo']=ev.BANDS[band][0];acquired=40<=i<40+active
     if acquired:
      row,cfg=interface_fixture(n);p=[str(F(i,100)),str(F(i+1,100))]
      row['source']=source;row['result']['result'].update(index=i,pl=p[0],pu=p[1],rho_hi=ev.BANDS[band][1]);row['result']['raw_row'].update(pl=p[0],pu=p[1]);cfg.update(index=i,p=p,rho_lower=ev.BANDS[band][0],rho_upper=ev.BANDS[band][1])
      row['result']['excluded']=False;status='RESOURCE_ROW_ACQUIRED_FOR_COUNT'
      count_id=f'n{n}.{band}.{i}';ct=self.root/('count-'+count_id);count_row=dict(n=n,band=band,index=i,directory='native',expected_controls=list(range(24)),job_id=count_id)
      counts[count_id]=dict(task=ct,row=count_row,checked={});counts[count_id]['_cfg']=cfg
     else:row=dict(source=source,result=dict(excluded=True));status='EXCLUDED_BY_SAME_LAW_RESOURCE'
     row.update(n=n,band=band,index=i,status=status);pin=put(task/'capsule/resource'/band/f'rows/{i:03d}.json',row)
     descs.append(dict(n=n,band=band,index=i,p=[str(F(i,100)),str(F(i+1,100))],path=f'rows/{i:03d}.json',sha256=pin,status=status))
    census={status:sum(d['status']==status for d in descs)for status in('EXCLUDED_BY_SAME_LAW_RESOURCE','RESOURCE_ROW_ACQUIRED_FOR_COUNT')}
    candidate=dict(n=n,band=band,K='0',q=c['q'],owncap=c['owncap'],rho_interval=c['rho_interval'],initial_candidate_sha256=cp,initial_acceptance_sha256=ap,rows=descs,status_counts=census,files_sha256={},support=support(n,band,True))
    rp=put(task/'capsule'/spec['resource_candidate'],candidate);put(task/'provenance'/spec['resource_candidate'],candidate)
    accepted=dict(n=n,band=band,candidate_sha256=rp,rows=descs,status_counts=census,files_sha256={},negative_controls=dict(malformed_inventories=12,parser_controls=2),timings_seconds=[1]*100)
    ra=put(task/'capsule'/spec['resource_receipt'],accepted);put(task/'provenance'/spec['resource_receipt'],accepted)
    cores[(n,band)]=dict(task=task,row=spec,checked={})
    for item in counts.values():
     if item['row']['n']!=n or item['row']['band']!=band:continue
     contract=dict(rows=[item.pop('_cfg')],resource_candidate_sha256=rp,resource_replay_sha256=ra,resource_row_sha256=descs[item['row']['index']]['sha256'])
     item['row']['contract_sha256']=put(item['task']/'capsule/native/contract.json',contract)
  return cores,counts

 def test_all1000_dispositions147_interfaces_and_no_failed_criterion_exclusion(self):
  cores,counts=self.make_families();result=ev.finite_families(cores,counts)
  self.assertEqual((result['resource_dispositions'],result['resource_excluded'],len(result['parent_contract_interfaces'])),(1000,853,147))
  self.assertEqual(len(result['families']),10)
  missing=dict(counts);missing.pop(next(iter(missing)))
  with self.assertRaises(ValueError):ev.finite_families(cores,missing)
  task=cores[(15,'B0')]['task'];path=task/'capsule/resource/B0/rows/000.json';row=ev.read(path);row['status']='RESOURCE_CRITERION_FAILED_NO_EXCLUSION';row['result']['excluded']=False;pin=put(path,row)
  for name in('CANDIDATE.json','ACCEPTED.json'):
   p=task/'capsule/resource/B0'/name;d=ev.read(p);d['rows'][0].update(status=row['status'],sha256=pin);put(p,d)
  # Coherently rehashing a failed disposition still cannot acquire an exclusion.
  p=task/'capsule/resource/B0/ACCEPTED.json';d=ev.read(p);d['candidate_sha256']=src.digest(task/'capsule/resource/B0/CANDIDATE.json');put(p,d)
  with self.assertRaises(ValueError):ev.finite_families(cores,counts)

 def parents(self):
  parents={}
  for key,*_ in ev.PARENTS:
   task=self.root/('parent-'+key);parents[key]=dict(task=task,source=types.SimpleNamespace(RESULT='READBACK.json',CANDIDATE='BRIDGE.json'),checked={})
  ns=list(range(14,20));uppers={str(n):'409/1000'for n in ns}
  rows={
   '57A':dict(status='PASS_INDEPENDENT_GLOBAL_AUXILIARY14_19_READBACK',n=ns,finite_rho=['1','19/10'],target='21/50',per_n_upper=uppers),
   '57B':dict(status='PASS_INDEPENDENT_SUPPORTED_SAME_LAW14_19_THREE_BAND_READBACK',n=ns,support_absolute_upper='3',
    bands=[dict(name='B0',rho=['1','11/10'],target='417/1000'),dict(name='BN',rho=['11/10','23/20'],target='827/2000'),dict(name='BH',rho=['23/20','33/25'],target='4097/10000')],
    per_band_per_n_upper={b:uppers for b in('B0','BN','BH')}),
   '57C':dict(status='PASS_INDEPENDENT_GLOBAL_HIGHRHO14_19_READBACK',n=ns,finite_rho=['33/25','19/10'],target='4097/10000',per_n_upper=uppers),
   '57D':dict(status='PASS_FRESH_ACTUAL15_19_TWO_RAY_SUPPORT_REPLAY_CONDITIONAL',n_values=list(range(15,20)),rho_interval=['1','33/25'],radius='3',full_ray_rows=10,predecessor_premise_discharged_here=False),
   '57E':dict(status='PASS_INDEPENDENT_SUPPORTED_COMPENSATED_HIGH15_19_READBACK',n=list(range(15,20)),support_radius='3',rho_upper=['11/10','23/20','33/25'],
    per_band_per_n_upper={b:{str(n):'3/8'if b=='B0'else'2/5'for n in range(15,20)}for b in('B0','BN')})}
  for key,value in rows.items():put(parents[key]['task']/'capsule/READBACK.json',value)
  bridge=[]
  for n in range(15,20):
   q=str(n*F(103,10000));proof=support(n);proof.update(rho_upper='33/25',radius='3',q_contact=q);bridge.append(dict(n=n,q=q,proof=proof))
  put(parents['57D']['task']/'capsule/BRIDGE.json',dict(rows=bridge));parents['56K']['checked']=dict(summary=dict(kappa='62/625'))
  return parents

 def test_closed_fourier_union_requires_both_support_rays_and_original_allowances(self):
  parents=self.parents();summary=ev.fourier_and_support(parents)
  self.assertEqual(summary['closed_rho_union'][-1],['33/25','infinity'])
  for mutation in('allowance','ray','seam','high','owncap','n'):
   parents=self.parents()
   if mutation in('allowance','ray'):
    path=parents['57D']['task']/'capsule/BRIDGE.json';d=ev.read(path)
    if mutation=='allowance':d['rows'][1]['q']='0'
    else:d['rows'][0]['proof']['ray_rows'][0]['contact_upper']='0'
   elif mutation in('seam','owncap'):
    path=parents['57B']['task']/'capsule/READBACK.json';d=ev.read(path)
    if mutation=='seam':d['bands'][2]['rho'][0]='6/5'
    else:d['per_band_per_n_upper']['B0']['15']='417/1000'
   elif mutation=='high':
    path=parents['57E']['task']/'capsule/READBACK.json';d=ev.read(path);d['per_band_per_n_upper']['B0']['19']='191/500'
   else:path=parents['57C']['task']/'capsule/READBACK.json';d=ev.read(path);d['n']=[15,16,17,18,19]
   put(path,d)
   with self.subTest(mutation=mutation),self.assertRaises(ValueError):ev.fourier_and_support(parents)

 def test_full_finite_summary_reconstructs_all1000_and_rejects_edited_completion(self):
  from be_replay import finite1519_join_control_evidence as controls
  cores,counts=self.make_families();parents=self.parents();control=self.root/'controls';control.mkdir()
  d=src.plan()['fresh_geometry_fixture'];genuine={'actual':'synthetic complete COUNT56'}
  item=counts.pop(next(iter(counts)));counts[d['job_id']]=item;item['checked']=genuine
  put(control/'CURRENT_GEOMETRY_FIXTURE.json',dict(validated_native_count=genuine))
  prior=dict(conditional_finite_chain_verified=True,session_result_sha256='a'*64,summary=dict(analytic_premises=['Synthetic predecessor analytic premise']))
  status=dict(schema=ev.SCHEMA,state=ev.COMPLETE,started_utc='synthetic-start',finished_utc='synthetic-stop',
   controls=dict(task_relative='controls',validated={'six':'synthetic validated'},export={},reused_completed_stage=False),imports=[],
   conditional_controls_completed=True,conditional_finite_chain_verified=True,**{f:False for f in controls.FLAGS})
  with patch.object(controls,'validate_completed',return_value={'six':'synthetic validated'}),patch.object(ev,'_validated_inputs',return_value=(parents,cores,counts,prior)):
   status['finite_summary']=ev.validate_batch(self.root,status);put(self.root/'SESSION_RESULT.json',status)
   checked=ev.validate_completed(self.root);self.assertEqual(checked['summary']['finite_interfaces']['resource_dispositions'],1000)
   self.assertEqual([r['n']for r in checked['summary']['sequential_chain']],[15,16,17,18,19]);self.assertFalse(checked['all_index_conclusion_verified'])
   status['finite_summary']['finite_interfaces']['resource_dispositions']=999;put(self.root/'SESSION_RESULT.json',status)
   with self.assertRaises(ValueError):ev.validate_completed(self.root)


if __name__=='__main__':unittest.main()
