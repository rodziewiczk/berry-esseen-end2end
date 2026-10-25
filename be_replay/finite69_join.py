"""65: complete conditional finite6--9, independent of any eventual10 tail."""
from datetime import datetime,timezone
from pathlib import Path
import importlib,shutil,traceback,uuid
from fractions import Fraction as F
from . import finite69_join_sources as src,finite69_remaining as rem,finite69_join_interfaces as interfaces
from . import finite69_sources as cs,finite69_counts as cr,finite69_count_evidence as ce
from . import finite69_parent_sources as ps,finite69_parents as pr,finite69_parent_evidence as pe
from . import finite69_caps_sources as caps,finite69_caps as capr,finite69_caps_evidence as cape
from . import finite1014_kappa_sources as ks,finite1014_kappa as kr,finite1014_kappa_evidence as ke
from . import delivery_transport as tx
from .colab_batch import atomic_json,event,utc
from .finite1014_join_evidence import ANALYTIC_PREMISES
SCHEMA='COMPLETE65_FINITE69_JOIN_SESSION_V1'
COMPLETE='COMPLETE_CONDITIONAL_FINITE6_9'
def task_of(root,row):return src.ordinary(Path(root).joinpath(*src.parts(row['task_relative'])))
def record(root,key,hit):
 task,checked,export=hit
 return dict(key=key,task_relative=Path(task).relative_to(root).as_posix(),validated=checked,export=export)
def import_inputs(root,durable,status):
 root=Path(root);durable=Path(durable);rows=[];missing=[]
 for row in ps.jobs('n6')+ps.jobs('initial7_9'):
  cache=durable/('finite69-parents-'+row['lane'])/'completed'/ps.CATALOG_SHA256[:16]/pr.slug(row['job_id'])
  hit=pr.restore_stage(cache,root/'imports/parents',row,log_root=root)
  if hit:rows.append(record(root,row['job_id'],hit))
  else:missing.append(row['job_id'])
 for key in ['owncaps6_9']+[r['job_id']for r in caps.resource_rows()]:
  cache=durable/'finite69-caps/completed'/caps.CATALOG_SHA256[:16]/pr.slug(key)
  hit=capr.restore_stage(cache,root/'imports/caps',key,root=root)
  if hit:rows.append(record(root,'caps:'+key,hit))
  else:missing.append('caps:'+key)
 for row in cs.jobs('count'):
  cache=durable/('finite'+str(row['selection']['n'])+'-counts')/'completed'/cs.CATALOG_SHA256[:16]/cr.slug(row['job_id'])
  hit=cr.restore_stage(cache,root/'imports/counts',row,log_root=root)
  if hit:rows.append(record(root,'count:'+row['job_id'],hit))
  else:missing.append('count:'+row['job_id'])
 hit=kr.restore_completed(durable/'finite1014-kappa/completed'/ks.PLAN_SHA256[:16],root/'imports/kappa',root=root)
 if hit:rows.append(record(root,'scalar56K',hit))
 else:missing.append('scalar56K')
 status['imports']=rows;atomic_json(root/'SESSION_RESULT.json',status)
 event(root,'finite69_inputs_revalidated',available=len(rows),required=345,missing=len(missing));return missing
def validate_imports(root,status):
 lookup={r['key']:r for r in status['imports']};src.need(len(lookup)==len(status['imports'])==345,'Every complete65 parent/count/scalar input')
 wanted={'scalar56K'};parents={};resources={};counts={};own=None
 for row in ps.jobs('n6')+ps.jobs('initial7_9'):
  key=row['job_id'];wanted.add(key);record=lookup[key];task=task_of(root,record);checked=pe.validate_completed(task)
  src.need(rem.same(checked,record['validated']),'Genuine complete original parent arithmetic')
  item=dict(task=task,checked=checked,row=row);parents[key]=item
  if row['kind']=='resource':resources[(checked['summary']['n'],checked['summary']['band'])]=item
 for key in ['owncaps6_9']+[r['job_id']for r in caps.resource_rows()]:
  name='caps:'+key;wanted.add(name);r=lookup[name];task=task_of(root,r);checked=cape.validate_completed(task)
  src.need(rem.same(checked,r['validated']),'Full current46 arithmetic, owncaps and fresh INITIAL binding')
  item=dict(task=task,checked=checked)
  if key=='owncaps6_9':own=item
  else:resources[(checked['summary']['n'],checked['summary']['band'])]=item
 for row in cs.jobs('count'):
  key='count:'+row['job_id'];wanted.add(key);r=lookup[key];task=task_of(root,r);checked=ce.validate_completed(task)
  src.need(rem.same(checked,r['validated']),'Whole original native forest acceptance and all24 controls')
  counts[row['job_id']]=dict(task=task,checked=checked)
 r=lookup['scalar56K'];task=task_of(root,r);scalar=dict(task=task,checked=ke.validate_completed(task))
 src.need(rem.same(scalar['checked'],r['validated'])and set(lookup)==wanted and len(resources)==12,'Exact complete finite6--9 input set')
 return parents,resources,counts,own,scalar
def scalar_binding(scalar,stages):
 s=scalar['checked']['summary'];src.need(s['kappa']=='62/625'and s['global_domain']=='all real x'
  and s['certificate_domain']==['0','625/124']and s['cells']==81,'Genuinely revalidated complete scalar domain')
 prefix='work/cutoff25_rethink_20261015/scale_analytic/kappa_62_625_v1/';pins={}
 for stage in ('auxiliary','bridge','radius'):
  for name in('CERTIFICATE.json','controls.py','kernel.py','PROOF.txt'):
   a=scalar['task']/'capsule'/name;b=stages[stage]['task']/'capsule'/prefix/name
   src.need(a.read_bytes()==b.read_bytes(),'Every retained scalar input equals the actually acquired scalar execution')
   pins[prefix+name]=src.digest(a)
 return dict(current_scalar_stage_result_sha256=scalar['checked']['stage_result_sha256'],source_and_certificate_sha256=pins,
  historical_scalar_capture_claimed_current=False,current_full_scalar_execution_revalidated=True)
def parent_interfaces(parents,resources,own,stages):
 high=stages['high']['checked']['summary'];support=stages['support']['checked']['summary']
 aux=stages['auxiliary']['checked']['summary'];own_receipt=src.read(own['task']/'capsule/work/cutoff6_20261018/audit/supported_fourier_readback_v1/OWN_RESULT.json')
 src.need(aux['n']==[5]and aux['finite_rho']==['1','19/10']and aux['target']=='429/1000'
  and F(aux['uniform_upper'])<F(429,1000)and 6*(F(429,1000)-F(4097,10000))==F(579,5000),
  'Universal auxiliary5, full Fourier/published tail and correct same-law n6 allowance')
 src.need(support['n']==[6,7,8,9]and support['support_targets']==36 and support['signed_rays']==72
  and support['q6']=='579/5000'and support['later_q']=='0'and support['complement_rho']==['237/200','infinity'],
  'Whole both-ray support and closed Fourier/published complement')
 edges=[]
 for (n,band),item in sorted(resources.items()):
  initial=parents[f'n{n}.initial.{band}'];receipt=src.read(initial['task']/initial['checked']['summary']['receipt_relative'])
  profile=receipt['profile'];premise=receipt['numerical_premises'];lo,hi,rad,_,_=interfaces.BANDS[band]
  h=next(r for r in high['rows']if r['n']==n and r['band']==('BH'if band=='B2'else band))
  chosen=next(r for r in src.read(stages['support']['task']/'capsule'/src.plan()['stages']['support']['native']/'REPLAY_CHECKED.json')['rows']if r['n']==n and r['region']==band)
  src.need(receipt['n']==n and type(receipt['n'])is int and receipt['rho_interval']==[lo,hi]
   and profile['n']==n and profile['barrier']=='0'and F(profile['q_contact'])==(F(579,5000)if n==6 else F(0))
   and F(profile['radius'])==F(profile['radius_minus'])==F(profile['radius_plus'])and F(chosen['radius'])<=F(profile['radius'])
   and F(h['support_radius'])>=F(chosen['radius'])and F(h['rho_upper'])>=F(hi)and F(h['upper'])<F(premise['HIGH']),
   'Actual same-law INITIAL support/HIGH domain and exact independently acquired HIGH upper')
  b='BC'if band=='B2'else band;cap=own_receipt['per_band_per_n_upper'][b][str(n)]
  src.need(F(cap)<F(premise['owncap']),'Actual literal-index supported owncap licenses complete INITIAL')
  if n==6:
   src.need(premise['predecessor']=='429/1000','GLOBAL5, never a selected-law predecessor')
  else:
   src.need(premise['predecessor_theorem']=='sharp_CE_minimal_counterexample'and premise['contact_error']=='0',
    'Sharp equality-inclusive immediate predecessor, no physical error seed')
  edges.append(dict(n=n,band=band,actual_HIGH=h['upper'],assumed_HIGH=premise['HIGH'],actual_owncap=cap,
   acquired_absolute_support=chosen['radius'],INITIAL_stage_sha256=initial['checked']['stage_result_sha256']))
 # Native40 parent stages keep immutable old parent hashes. They are linked
 # to genuine current facts by the existing exact whole-receipt bridge.
 ordered=[];bridges=[]
 for row in ps.jobs('n6'):
  item=parents[row['job_id']];stage=dict(job_id=row['job_id'],task_relative=item['task'].relative_to(root_of(parents)).as_posix())
  bridges.extend(pr.join_fresh_inputs(root_of(parents),item['task'],row,dict(jobs=ordered)))
  ordered.append(stage)
 return dict(interfaces=edges,current_n6_parent_bridges=bridges,GLOBAL5='complete original auxiliary5_v2',
  new_support_before_supported_Fourier=True,retained_tail10_used=False)
def root_of(parents):
 # Tasks are restored below root/imports/parents/<unique>; resolve the common
 # session ancestor from the declared import layout, never an old absolute cwd.
 tasks=[v['task']for v in parents.values()]
 import os
 common=Path(os.path.commonpath([str(t)for t in tasks]))
 src.need(common.name=='parents'and common.parent.name=='imports','Contained current session parent tree')
 return common.parent.parent
def validate_batch(root,status=None):
 root=Path(root);status=src.read(root/'SESSION_RESULT.json',128*src.MIB)if status is None else status
 src.need(status['schema']==SCHEMA and all(status[k]is False for k in rem.FALSE),'Explicit conditional finite scope')
 parents,resources,counts,own,scalar=validate_imports(root,status);stages={}
 for r in status['stages']:
  task=task_of(root,r);checked=rem.validate_completed(task);src.need(rem.same(checked,r['validated']),'Whole real remaining65 producer transaction')
  src.need(checked['stage']not in stages,'Unique complete producer');stages[checked['stage']]=dict(task=task,checked=checked)
 src.need(set(stages)==set(src.plan()['stages']),'All19 original remaining producer calls, no omitted family')
 semantic=root/'semantic-inputs'
 for n,pin in src.plan()['semantic_inputs'].items():src.need(src.digest(semantic/n)==pin,'Every original immutable semantic interface source')
 finite=interfaces.finite_cover(semantic,counts,resources,parents)
 conclusion=interfaces.induction(finite,global_auxiliary5=True)
 return dict(schema='CONDITIONAL_COMPLETE_FINITE6_9_CURRENT_JOIN_V1',source_plan_sha256=src.PLAN_SHA256,
  parent_interfaces=parent_interfaces(parents,resources,own,stages),current_scalar=scalar_binding(scalar,stages),
  finite_interfaces=finite,sequential_induction=conclusion,
  finite_indices=[6,7,8,9],original_remaining_invocations=19,full_native_forests=284,
  conditional_finite_chain_verified=True,analytic_premises=list(ANALYTIC_PREMISES),eventual10_or20_tail_used=False,**rem.FALSE)
def validate_completed(root):
 root=Path(root);s=src.read(root/'SESSION_RESULT.json',128*src.MIB)
 src.need(s['state']==COMPLETE and s['conditional_finite_chain_verified']is True,'Entire finite6--9 completed conditional export')
 summary=validate_batch(root,s);src.need(rem.same(summary,s['finite_summary']),'Whole finite source/semantic/current-input summary')
 return dict(session_result_sha256=src.digest(root/'SESSION_RESULT.json'),summary=summary,conditional_finite_chain_verified=True,**rem.FALSE)
def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
 root=Path(work_root).resolve()/'finite69-join'/stamp;root.mkdir(parents=True,exist_ok=False);durable=Path(durable_root)/'finite69-join'/stamp
 status=dict(schema=SCHEMA,state='INCOMPLETE',imports=[],stages=[],started_utc=utc(),conditional_finite_chain_verified=False,**rem.FALSE)
 atomic_json(root/'SESSION_RESULT.json',status);backup=tx.Backups(root,durable,backup_interval);backup.start()
 try:
  missing=import_inputs(root,durable_root,status)
  assets=src.obtain_assets(archives,progress=lambda name,**fields:event(root,name,**fields))
  source=src.prepare_cache(assets,Path(work_root)/'finite69-join-sources'/src.PLAN_SHA256[:16],progress=lambda name,**fields:event(root,name,**fields))
  for n,pin in src.plan()['semantic_inputs'].items():
   dest=root/'semantic-inputs'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/n,dest)
  actual={}
  own=next((r for r in status['imports']if r['key']=='caps:owncaps6_9'),None)
  for stage in ('auxiliary','bridge','radius','high','support'):
   if stage=='support'and own is None:missing.append('support: full current owncaps46 required');continue
   cache=Path(durable_root)/'finite69-join/completed-producers'/src.PLAN_SHA256[:16]/stage
   hit=tx.restore(cache,root/'stages',validator=rem.validate_completed,log=lambda name,**fields:event(root,name,**fields))
   if hit:src.need(hit[1]['stage']==stage,'Exact selected complete producer cache')
   else:
    parents=[]
    if stage=='support':parents=[(task_of(root,own),cape.validate_completed)]+[(actual[k][0],rem.validate_completed)for k in('auxiliary','bridge','radius')]
    task=root/'stages'/stage;checked=rem.execute(source,task,stage,root=root,parents=parents)
    hit=(task,checked,tx.save(task,cache,validator=rem.validate_completed,label=stage))
   actual[stage]=hit;status['stages'].append(record(root,stage,hit));atomic_json(root/'SESSION_RESULT.json',status)
  if missing:status.update(state='WAITING',missing=missing)
  else:
   summary=validate_batch(root,status);status.update(state=COMPLETE,conditional_finite_chain_verified=True,finite_summary=summary)
   atomic_json(root/'SESSION_RESULT.json',status);validate_completed(root)
 except BaseException as error:
  status.update(state='INCOMPLETE',conditional_finite_chain_verified=False,error=type(error).__name__+': '+str(error))
  (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8');event(root,'finite69_join_incomplete',error=status['error'])
 finally:
  status['finished_utc']=utc()
  try:backup.close()
  except BaseException as error:status.update(state='INCOMPLETE',backup_error=str(error),conditional_finite_chain_verified=False)
  bundle=tx.final_bundle(root,durable,Path(work_root)/'finite69-local-exports'/stamp,status)
 return dict(status=status,bundle=bundle,work=str(root))
