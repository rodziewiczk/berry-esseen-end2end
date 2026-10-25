"""Full pure57H readback: stopped sources, all panels and finite14->19.

The numerical programs are never imported. Their own full readers must first
validate all native transactions; the checks here acquire only the explicitly
conditional finite consequence, retaining the universal analytic premises.
"""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import importlib
from pathlib import Path
from . import finite1519_join_control_sources as src, finite1519_join_control_evidence as controls
from .finite1014_join_epoch import same
from .finite1519_join_interfaces import BANDS,interface,ceilgrid,sequential,verify_reference_projection
from .colab_batch import atomic_json,event

SCHEMA='FINITE1519_FULL_FINITE_JOIN_SESSION_V1'
COMPLETE='complete_finite15_19_under_explicit_analytic_premises'
PARENTS=(
 ('57A','finite1519_auxiliary','finite1519_auxiliary_evidence','finite1519_auxiliary_sources','finite1519-auxiliary'),
 ('57B','finite1519_supported','finite1519_supported_evidence','finite1519_supported_sources','finite1519-supported'),
 ('57C','finite1519_highrho','finite1519_highrho_evidence','finite1519_highrho_sources','finite1519-highrho'),
 ('57D','finite1519_support','finite1519_support_evidence','finite1519_support_sources','finite1519-support'),
 ('57E','finite1519_high','finite1519_high_evidence','finite1519_high_sources','finite1519-high'),
 ('56K','finite1014_kappa','finite1014_kappa_evidence','finite1014_kappa_sources','finite1014-kappa'))
ANALYTIC_PREMISES=(
 'Unrestricted positive closed attainment, reflection and same-law contact/support implications on every threshold.',
 'The original physical-gap, centered sign marginal, resource and exact-count reduction theorems on the declared domains.',
 'The original Prawitz, pointwise Fourier, signed LOW, Gaussian support and compensated infinite-HIGH lemmas.',
 'The named published Shevtsova upper tail and analytic kappa inputs, with all original boundary conventions.',
 'Native source-bound numerical replay and bounded mutation controls do not independently prove these universal analytic lemmas.')


def refined_radius(n,band):
 # The original last BN constructor selects23/10, unlike the other BN cases.
 # It is verified again by the full core source/reference reader.
 src.need(type(n)is int and 15<=n<=19 and band in BANDS,'Literal refined-support case')
 return '23/10'if(n,band)==(19,'BN')else BANDS[band][4]


def module(name):return importlib.import_module('be_replay.'+name)


def read(path,limit=128*src.MIB):
 p=src.ordinary(path);src.need(p.is_file()and p.stat().st_size<=limit,'Bounded ordinary full finite evidence file')
 return src.parsed(p.read_bytes())


def implementation():
 names=('finite1519_join.py','finite1519_join_evidence.py','finite1519_join_interfaces.py',
        'finite1519_join_controls.py','finite1519_join_control_sources.py','finite1519_join_control_evidence.py',
        'finite_join_session_import.py','finite1014_join_evidence.py','finite1519_core.py',
        'finite1519_core_evidence.py','finite1519_core_sources.py','finite1039_counts.py',
        'finite1039_count_evidence.py','finite1039_sources.py')
 out={name:src.digest(src.ROOT/'be_replay'/name)for name in names}
 for _,_,e,s,_ in PARENTS:
  for name in(e,s):out[name+'.py']=src.digest(src.ROOT/'be_replay'/(name+'.py'))
 out.update(source_plan_sha256=src.PLAN_SHA256,original_interface_source_sha256=verify_reference_projection())
 return out


def _task(root,record):
 name=record['task_relative'];p=src.child(root,name)
 src.need(p.is_dir()and p!=src.ordinary(root),'Contained complete imported transaction')
 return p


def _record(root,key,result):
 task,checked,export=result
 return dict(key=key,task_relative=Path(task).relative_to(root).as_posix(),validated=checked,export=export)


def import_completed_inputs(root,durable_root,status):
 root=src.ordinary(root);durable=src.ordinary(durable_root);missing=[];status['imports']=[]
 for key,r,e,s,folder in PARENTS:
  source,runner=module(s),module(r);cache=durable/folder/'completed'/source.PLAN_SHA256[:16]
  found=runner.restore_completed(cache,root/'imports'/key,root=root)
  if found is None:missing.append(dict(key=key,requirement='Whole source-bound native transaction with full pure readback'))
  else:status['imports'].append(_record(root,key,found))
  atomic_json(root/'SESSION_RESULT.json',status)
 core=module('finite1519_core');source=module('finite1519_core_sources')
 for row in source.plan()['cases']:
  key='core:'+row['case_id'];cache=durable/'finite1519-core/completed'/source.PLAN_SHA256[:16]/row['case_id']
  found=core.restore_completed(row['case_id'],cache,root/'imports/core',root=root)
  if found is None:missing.append(dict(key=key,requirement='Full original four-call INITIAL/resource transaction'))
  else:status['imports'].append(_record(root,key,found))
  atomic_json(root/'SESSION_RESULT.json',status)
 source=module('finite1039_sources');runner=module('finite1039_counts')
 for row in source.jobs('n15_19'):
  key='count:'+row['job_id'];cache=durable/'finite1039-counts-n15_19/completed'/source.CATALOG_SHA256[:16]/runner.slug(row['job_id'])
  found=runner.restore_stage(cache,root/'imports/counts',row,log_root=root)
  if found is None:missing.append(dict(key=key,requirement='Genuine full selected original COUNT acceptance and all native controls'))
  else:status['imports'].append(_record(root,key,found))
  atomic_json(root/'SESSION_RESULT.json',status)
 transport=module('finite_join_session_import');prior=module('finite1014_join_evidence')
 found=transport.restore_latest(durable/'finite1014-join',root/'imports/56I',validator=prior.validate_completed,
  log=lambda name,**data:event(root,name,**data))
 if found is None:missing.append(dict(key='56I',requirement='Full finite10--14 session, all controls/imports/interfaces revalidated'))
 else:status['imports'].append(_record(root,'56I',found))
 atomic_json(root/'SESSION_RESULT.json',status)
 event(root,'finite1519_join_inputs_revalidated',available=len(status['imports']),required=164,missing=len(missing),numerical_replays_started=0)
 return missing


def _validated_inputs(root,records):
 src.need(type(records)is list and all(type(r)is dict and set(r)=={'key','task_relative','validated','export'}for r in records),
          'Exact complete input record schema')
 lookup={r['key']:r for r in records};src.need(len(lookup)==len(records),'No duplicate imported upstream')
 wanted={key for key,*_ in PARENTS}|{'56I'};parents={}
 for key,_,e,s,_ in PARENTS:
  src.need(key in lookup,'Missing complete parent '+key);r=lookup[key];task=_task(root,r);checked=module(e).validate_completed(task)
  src.need(same(checked,r['validated']),'Imported full parent readback equals actual evidence')
  parents[key]=dict(task=task,checked=checked,source=module(s))
 src.need('56I'in lookup,'Full finite14 predecessor is mandatory')
 record=lookup['56I'];predecessor=module('finite1014_join_evidence').validate_completed(_task(root,record))
 src.need(same(predecessor,record['validated'])and predecessor['conditional_finite_chain_verified']is True
          and same(predecessor['summary']['finite_indices'],list(range(10,15)))
          and type(predecessor['summary']['analytic_premises'])is list and bool(predecessor['summary']['analytic_premises'])
          and all(type(p)is str and p for p in predecessor['summary']['analytic_premises']),
          'Whole conditional finite14 result, never an assumed eventual20')
 source=module('finite1519_core_sources');cores={}
 for row in source.plan()['cases']:
  key='core:'+row['case_id'];wanted.add(key);src.need(key in lookup,'Missing complete INITIAL/resource '+key)
  r=lookup[key];task=_task(root,r);checked=module('finite1519_core_evidence').validate_completed(task)
  src.need(same(checked,r['validated'])and checked['summary']['case_id']==row['case_id'],'Exact same literal core case')
  cores[(row['n'],row['band'])]=dict(task=task,row=row,checked=checked)
 counts={}
 for row in module('finite1039_sources').jobs('n15_19'):
  key='count:'+row['job_id'];wanted.add(key);src.need(key in lookup,'Missing full native COUNT '+key)
  r=lookup[key];task=_task(root,r);checked=module('finite1039_count_evidence').validate_completed(task)
  src.need(same(checked,r['validated'])and checked['job_id']==row['job_id'],'Exact native count identity without receipt rewriting')
  counts[row['job_id']]=dict(task=task,row=row,checked=checked)
 src.need(set(lookup)==wanted and len(wanted)==164 and len(cores)==10 and len(counts)==147,'All and only164 full imports')
 return parents,cores,counts,predecessor


def _native(parent):return read(parent['task']/'capsule'/parent['source'].RESULT)


def support_scope(proof,n,rho,radius,q,*,resource=False):
 src.need(type(proof['n'])is int and proof['n']==n and proof['K']=='0'
  and proof['schema']==('DIRECT_FIXED_INDEX_GAUSSIAN_SUPPORT_V1'if resource else'DIRECT_SAME_LAW_CONTACT_SUPPORT_DISCOVERY_V1')
  and proof['rho_upper']==rho and proof['radius']==radius and proof['q'if resource else'q_contact']==q
  and type(proof['support_sign'])is int and proof['support_sign']==0,'Literal same-law support domain and allowance')
 rays=proof['ray_rows'];src.need(type(rays)is list and len(rays)==2 and [r['sign']for r in rays]==[-1,1]
  and all(type(r['sign'])is int and all(F(r[k])<0 for k in('contact_upper','coefficient_at_R','contact_derivative_at_R','contact_derivative_slope_at_R'))for r in rays),
  'Both strict entire support rays, including endpoints and slopes')


def fourier_and_support(parents):
 a,b,c,d,e={k:_native(parents[k])for k in('57A','57B','57C','57D','57E')}.values();ns=list(range(14,20))
 src.need(a['status']=='PASS_INDEPENDENT_GLOBAL_AUXILIARY14_19_READBACK'and same(a['n'],ns)
  and a['finite_rho']==['1','19/10']and a['target']=='21/50'and set(a['per_n_upper'])==set(map(str,ns))
  and all(F(v)<F(21,50)for v in a['per_n_upper'].values()),'Full unrestricted auxiliary14--19, finite range plus published infinite tail')
 src.need(b['status']=='PASS_INDEPENDENT_SUPPORTED_SAME_LAW14_19_THREE_BAND_READBACK'and same(b['n'],ns)
  and b['support_absolute_upper']=='3'and set(b['per_band_per_n_upper'])=={'B0','BN','BH'},'All supported Fourier bands and literal indices')
 bands=[dict(name='B0',rho=['1','11/10'],target='417/1000'),dict(name='BN',rho=['11/10','23/20'],target='827/2000'),
        dict(name='BH',rho=['23/20','33/25'],target='4097/10000')]
 src.need(same(b['bands'],bands),'Closed Fourier band seams and original caps')
 for band in bands:
  values=b['per_band_per_n_upper'][band['name']]
  src.need(set(values)==set(map(str,ns))and all(F(v)<F(band['target'])for v in values.values()),'Actual supported predecessor and own ceilings')
 src.need(c['status']=='PASS_INDEPENDENT_GLOBAL_HIGHRHO14_19_READBACK'and same(c['n'],ns)
  and c['finite_rho']==['33/25','19/10']and c['target']=='4097/10000'
  and set(c['per_n_upper'])==set(map(str,ns))and all(F(v)<F(4097,10000)for v in c['per_n_upper'].values()),
  'Unconditional full high-rho route including its infinite tail')
 src.need(d['status']=='PASS_FRESH_ACTUAL15_19_TWO_RAY_SUPPORT_REPLAY_CONDITIONAL'
  and same(d['n_values'],list(range(15,20)))and d['rho_interval']==['1','33/25']and d['radius']=='3'
  and d['full_ray_rows']==10 and d['predecessor_premise_discharged_here']is False,'Complete coarse support transaction stays conditional until predecessor license')
 candidate=read(parents['57D']['task']/'capsule'/parents['57D']['source'].CANDIDATE)
 src.need(len(candidate['rows'])==5,'One coarse support row for every actual index')
 for n,row in zip(range(15,20),candidate['rows']):
  q=str(n*F(103,10000))
  src.need(type(row['n'])is int and row['n']==n and row['q']==q,'Original coarse support allowance uses the actual auxiliary predecessor ceiling')
  support_scope(row['proof'],n,'33/25','3',q)
 src.need(e['status']=='PASS_INDEPENDENT_SUPPORTED_COMPENSATED_HIGH15_19_READBACK'
  and same(e['n'],list(range(15,20)))and e['support_radius']=='3'
  and e['rho_upper']==['11/10','23/20','33/25'],'Exact compensated HIGH domain after support')
 for band,(_,_,_,_,_,cap)in BANDS.items():
  values=e['per_band_per_n_upper'][band]
  src.need(set(values)=={str(n)for n in range(15,20)}and all(F(v)<F(cap)for v in values.values()),'Every original actual-index HIGH ceiling')
 src.need(parents['56K']['checked']['summary']['kappa']=='62/625','Complete original scalar kappa certificate')
 return dict(coarse_support_radius='3',coarse15_predecessor_cap='21/50',coarse15_allowance='309/2000',
  supported15_allowances={band:values[3]for band,values in BANDS.items()},
  sequential16_19_allowance='0',closed_rho_union=[['1','11/10'],['11/10','23/20'],['23/20','33/25'],['33/25','infinity']],
  support_before_supported_Fourier_and_HIGH=True,kappa='62/625')


def initial_scope(c,a,row):
 n,band=row['n'],row['band'];lo,hi,own,q15,_,_=BANDS[band];radius=refined_radius(n,band);q=q15 if n==15 else'0'
 src.need(type(c['n'])is int and c['n']==n and c['K']=='0'and c['target']=='CE'and c['band']==band
  and c['rho_interval']==[lo,hi]and c['owncap']==own and c['q']==q and c['old_support_radius']=='3'
  and c['failure']is None and all(c[k]is False for k in('predecessor_verified','owncap_verified','same_law_fourier_verified','old_target_specific_resources_imported','cutoff15_proved')),
  'Original unseeded actual-index conditional INITIAL and same-witness scope')
 src.need(len(c['stages'])==8 and c['stages'][0]['input_raw']is None and c['stages'][0]['input_D']is None
  and 'universal_moment_defect_seed'not in c,'No refuted physical defect seed')
 profile=c['profile'];src.need(type(profile['n'])is int and profile['n']==profile['nmax']==n
  and all(profile[k]==radius for k in('radius','radius_minus','radius_plus'))and profile['cap']==own
  and profile['grid']==[12,12,6,3]and 'p_interval'not in profile,'Full unchanged physical grid and refined radius')
 previous=(None,None)
 for stage in c['stages']:
  src.need((stage['input_raw'],stage['input_D'])==previous,'Same ordered eight-step invariant chain')
  vals=[]
  for field,old in(('R',previous[0]),('D',previous[1])):
   value=ceilgrid(stage['cover'][field],10**8)+F(1,100000);vals.append(min(value,F(old))if old is not None else value)
  src.need(list(map(F,[stage['next_raw'],stage['next_D']]))==vals and all(0<v<6 for v in vals),'Exact outward invariant update')
  previous=stage['next_raw'],stage['next_D']
 for cover in[s['cover']for s in c['stages']]+[c['export']]:
  src.need(all(type(cover[k])is int and cover[k]>=0 for k in('total','active','excluded'))
   and cover['total']==row['signed_cells_per_cover']and cover['active']+cover['excluded']==cover['total']
   and all(type(v)is int and v>=0 for v in cover['reasons'].values())and sum(cover['reasons'].values())==cover['excluded']
   and len(cover['panels'])==100,'Every signed cell and all100 original probability panels')
  for i,p in enumerate(cover['panels']):src.need([p['pl'],p['pu']]==[str(F(i,100)),str(F(i+1,100))],'Whole closed probability cover')
 src.need(same(c['final_invariants'],a['final_invariants'])and c['final_invariants']==dict(raw=previous[0],D=previous[1])
  and (F(previous[1])+1)**2<10,'Strict final central gap with matching replay')
 src.need(c['chosen_support']['radius']==radius,'Original refined support selection')
 support_scope(c['chosen_support']['proof'],n,hi,radius,q)
 src.need(F(q)==n*(F(own)-F(4097,10000))if n==15 else F(q)==0,'Correct index-scaled contact allowance')


def _projection(value,omitted):return{k:v for k,v in value.items()if k not in omitted}


def _parent_binding(core,contract,current_row):
 root,row=core['task'],core['row'];oldc=root/'provenance'/row['resource_candidate'];olda=root/'provenance'/row['resource_receipt']
 newc=root/'capsule'/row['resource_candidate'];newa=root/'capsule'/row['resource_receipt']
 src.need(contract['resource_candidate_sha256']==src.digest(oldc)and contract['resource_replay_sha256']==src.digest(olda)
  and contract['resource_row_sha256']==src.digest(current_row),'Immutable old contract points to the identical whole mathematical current row')
 src.need(same(_projection(read(oldc),{'files_sha256','initial_candidate_sha256','initial_acceptance_sha256'}),
               _projection(read(newc),{'files_sha256','initial_candidate_sha256','initial_acceptance_sha256'}))
  and same(_projection(read(olda),{'files_sha256','candidate_sha256','timings_seconds'}),
           _projection(read(newa),{'files_sha256','candidate_sha256','timings_seconds'})),
  'Entire original/current mathematical parent equivalence; only exact top-level metadata may differ')
 return dict(original_candidate_sha256=src.digest(oldc),current_candidate_sha256=src.digest(newc),
  original_replay_sha256=src.digest(olda),current_replay_sha256=src.digest(newa),row_sha256=src.digest(current_row),
  historical_acceptance_promoted=False,all_mathematical_fields_identical=True)


def finite_families(cores,counts):
 src.need(set(cores)=={(n,b)for n in range(15,20)for b in BANDS}and len(counts)==147,'All10 original families and147 complete forests')
 groups={}
 for item in counts.values():
  row=item['row'];key=(row['n'],row['band'],row['index']);src.need(key not in groups,'Only one whole original acceptance per parent panel');groups[key]=item
 families=[];interfaces=[];used=set();totals=Counter()
 for n,band in sorted(cores):
  core=cores[(n,band)];spec=core['row'];root=core['task']/'capsule';c=read(root/spec['initial_candidate']);a=read(root/spec['initial_receipt'])
  initial_scope(c,a,spec);candidate=read(root/spec['resource_candidate']);accepted=read(root/spec['resource_receipt'])
  src.need(type(candidate['n'])is int and candidate['n']==accepted['n']==n and candidate['band']==accepted['band']==band
   and candidate['K']=='0'and candidate['q']==c['q']and candidate['owncap']==c['owncap']and candidate['rho_interval']==c['rho_interval']
   and candidate['initial_candidate_sha256']==src.digest(root/spec['initial_candidate'])and candidate['initial_acceptance_sha256']==src.digest(root/spec['initial_receipt'])
   and accepted['candidate_sha256']==src.digest(root/spec['resource_candidate'])and same(accepted['rows'],candidate['rows'])
   and same(accepted['status_counts'],candidate['status_counts'])and same(accepted['files_sha256'],candidate['files_sha256'])
   and accepted['negative_controls']==dict(malformed_inventories=12,parser_controls=2)and len(candidate['rows'])==100,
   'Complete original INITIAL/resource chain and all native malformed/parser controls')
  support_scope(candidate['support'],n,BANDS[band][1],refined_radius(n,band),c['q'],resource=True)
  census=Counter();dispositions=[]
  for i,desc in enumerate(candidate['rows']):
   src.need(type(desc['n'])is int and desc['n']==n and type(desc['index'])is int and desc['index']==i and desc['band']==band
    and desc['p']==[str(F(i,100)),str(F(i+1,100))]and desc['path']==f'rows/{i:03d}.json','Every canonical closed probability panel')
   path=root/spec['resource_directory']/band/desc['path'];src.need(src.digest(path)==desc['sha256'],'Whole actual resource row')
   row=read(path);source=deepcopy(c['export']['panels'][i]);source['rho_lo']=BANDS[band][0]
   src.need(same(source,row['source'])and type(row['n'])is int and row['n']==n and type(row['index'])is int and row['index']==i
    and row['band']==band and row['status']==desc['status'],'Same full INITIAL export and current physical resource row')
   status=row['status'];census[status]+=1;totals[status]+=1;item=groups.get((n,band,i))
   if status=='EXCLUDED_BY_SAME_LAW_RESOURCE':src.need(row['result']['excluded']is True and item is None,'Genuine necessary-condition exclusion only')
   else:
    src.need(status=='RESOURCE_ROW_ACQUIRED_FOR_COUNT'and row['result']['excluded']is False and item is not None,
             'Failed criterion or missing native acceptance never excludes a witness')
    contract=read(item['task']/'capsule'/item['row']['directory']/'contract.json');src.need(len(contract['rows'])==1,'One complete simultaneous original row')
    interface(row,contract['rows'][0],band,i,n);bridge=_parent_binding(core,contract,path)
    src.need(len(item['row']['expected_controls'])==24,'Every original full COUNT corruption control retained')
    interfaces.append(dict(n=n,band=band,index=i,job_id=item['row']['job_id'],contract_sha256=item['row']['contract_sha256'],fresh_parent_bridge=bridge));used.add((n,band,i))
   dispositions.append(dict(index=i,p=desc['p'],resource_status=status))
  src.need(dict(census)==candidate['status_counts'],'Independent100-row original resource census')
  families.append(dict(n=n,band=band,closed_panels=100,status_counts=dict(census),dispositions=dispositions))
 src.need(used==set(groups)and len(interfaces)==147 and totals==Counter(EXCLUDED_BY_SAME_LAW_RESOURCE=853,RESOURCE_ROW_ACQUIRED_FOR_COUNT=147),
          'Exactly1000 closed dispositions and147 simultaneous current-parent COUNT interfaces')
 return dict(families=families,resource_dispositions=1000,resource_excluded=853,parent_contract_interfaces=interfaces,complete_native_forests=147)


def validate_batch(root,status=None):
 root=src.ordinary(root);status=read(root/'SESSION_RESULT.json',64*src.MIB)if status is None else status
 src.need(status['schema']==SCHEMA and all(status[f]is False for f in controls.FLAGS),'Conditional finite scope without universal/native promotion')
 record=status['controls'];src.need(type(record)is dict and set(record)=={'task_relative','validated','export','reused_completed_stage'},'One full stopped six-control transaction')
 checked=controls.validate_completed(_task(root,record));src.need(same(checked,record['validated']),'Actual all-six-control readback')
 parents,cores,counts,predecessor=_validated_inputs(root,status['imports'])
 fixture=controls.read(_task(root,record)/'CURRENT_GEOMETRY_FIXTURE.json')
 genuine=counts[src.plan()['fresh_geometry_fixture']['job_id']]
 src.need(same(fixture['validated_native_count'],genuine['checked']),'Geometry control binds the actual same selected full COUNT input')
 fourier=fourier_and_support(parents);finite=finite_families(cores,counts)
 chain=sequential(predecessor['conditional_finite_chain_verified'],{n:all(r['closed_panels']==100 for r in finite['families']if r['n']==n)for n in range(15,20)})
 src.need(all(row['conditional_finite_result_established']for row in chain),'Consecutive finite14->19 with no future theorem assumption')
 return dict(schema='CONDITIONAL_FINITE15_19_COMPLETE_INTERFACE_JOIN_V1',implementation=implementation(),finite_indices=list(range(15,20)),
  predecessor14_session_result_sha256=predecessor['session_result_sha256'],sequential_chain=chain,analytic_premises=list(ANALYTIC_PREMISES),
  inherited_predecessor14_analytic_premises=predecessor['summary']['analytic_premises'],
  Fourier_support_HIGH_interfaces=fourier,finite_interfaces=finite,control_invocations=6,completed_imports=164,
  incoming_eventual20_used=False,old_capture_impersonated=False,old_timed_parent_hashes_rewritten=False,
  conditional_finite_chain_verified=True,**{f:False for f in controls.FLAGS})


def validate_completed(root):
 root=src.ordinary(root);status=read(root/'SESSION_RESULT.json',64*src.MIB)
 fields={'schema','state','started_utc','finished_utc','controls','imports','conditional_controls_completed','conditional_finite_chain_verified','finite_summary',*controls.FLAGS}
 src.need(type(status)is dict and set(status)==fields and status['state']==COMPLETE
          and type(status['started_utc'])is str and bool(status['started_utc'])and type(status['finished_utc'])is str and bool(status['finished_utc'])
          and status['conditional_controls_completed']is True and status['conditional_finite_chain_verified']is True,
          'Full actually completed finite57H conditional session')
 summary=validate_batch(root,status);src.need(same(summary,status['finite_summary']),'Whole reconstructed finite summary without trusting flags')
 return dict(schema='REVALIDATED_FINITE1519_FINITE_JOIN_V1',session_result_sha256=src.digest(root/'SESSION_RESULT.json'),summary=summary,
  conditional_finite_chain_verified=True,**{f:False for f in controls.FLAGS})
