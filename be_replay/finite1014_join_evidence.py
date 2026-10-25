"""Pure complete-export and finite10--14 interface readback for56I."""
from __future__ import annotations
from collections import Counter,defaultdict
from copy import deepcopy
from fractions import Fraction as F
import importlib
from pathlib import Path
from . import finite1014_join_sources as src,finite1014_join_control_evidence as controls
from .finite1014_join_epoch import same
from .finite1014_join_interfaces import BANDS,interface,ceilgrid,verify_reference_projection
from .colab_batch import atomic_json,event
PARENTS=(
 ('56A','finite1014_parents','finite1014_parent_evidence','finite1014_parent_sources','finite1014-auxiliary'),
 ('56B','finite1014_supported','finite1014_supported_evidence','finite1014_supported_sources','finite1014-supported'),
 ('56C','finite1014_highrho','finite1014_highrho_evidence','finite1014_highrho_sources','finite1014-highrho'),
 ('56D','finite1014_corner','finite1014_corner_evidence','finite1014_corner_sources','finite1014-corner'),
 ('56E','finite1014_high','finite1014_high_evidence','finite1014_high_sources','finite1014-supported-high'),
 ('56F','finite1014_coarse','finite1014_coarse_evidence','finite1014_coarse_sources','finite1014-coarse-support'),
 ('56K','finite1014_kappa','finite1014_kappa_evidence','finite1014_kappa_sources','finite1014-kappa'))
COMPOSITES={(10,'BN',42),(11,'BN',39),(11,'BN',40),(11,'BN',41),(11,'BN',42)}
ANALYTIC_PREMISES=(
 'Unrestricted positive-closed attainment/reflection/contact and the same-law sign/physical-resource/count implications.',
 'The original signed LOW, support Gaussian, supported-HIGH and complete Fourier/Prawitz reduction theorems on the declared domains.',
 'The exact published Shevtsova upper-tail input and boundary conventions retained by the unchanged Fourier certificates.',
 'Bounded source/control passes are implementation checks, not external independent proofs of these universal analytic lemmas.')


def module(name):return importlib.import_module('be_replay.'+name)


def implementation():
 names=('finite1014_join.py','finite1014_join_sources.py','finite1014_join_epoch.py','finite1014_join_control_evidence.py',
        'finite1014_join_evidence.py','finite1014_join_interfaces.py')
 out={n:src.digest(src.ROOT/'be_replay'/n)for n in names}
 out['source_plan_sha256']=src.PLAN_SHA256
 out['original_interface_source_sha256']=verify_reference_projection()
 for _,_,e,s,_ in PARENTS:
  out[e+'.py']=src.digest(src.ROOT/'be_replay'/(e+'.py'));out[s+'.py']=src.digest(src.ROOT/'be_replay'/(s+'.py'))
 for name in('finite1014_core','finite1014_core_evidence','finite1014_core_sources','finite1039_counts','finite1039_count_evidence','finite1039_sources'):
  out[name+'.py']=src.digest(src.ROOT/'be_replay'/(name+'.py'))
 return out


def _record(root,key,result):
 task,checked,export=result
 return dict(key=key,task_relative=Path(task).relative_to(root).as_posix(),validated=checked,export=export)


def import_completed_inputs(root,durable_root,status):
 root=Path(root);durable=Path(durable_root).resolve();missing=[];status['imports']=[]
 for key,r,e,s,folder in PARENTS:
  run,source=module(r),module(s);cache=durable/folder/'completed'/source.PLAN_SHA256[:16]
  result=run.restore_completed(cache,root/'imports'/key,root=root)
  if result is None:missing.append(dict(key=key,requirement='Actual complete original transaction with ZIP SHA sidecar and current pure validation'))
  else:status['imports'].append(_record(root,key,result))
  atomic_json(root/'SESSION_RESULT.json',status)
 core=module('finite1014_core');source=module('finite1014_core_sources')
 for row in source.plan()['cases']:
  key='core:'+row['case_id'];cache=durable/'finite1014-core/completed'/source.PLAN_SHA256[:16]/row['case_id']
  result=core.restore_completed(row['case_id'],cache,root/'imports/core',root=root)
  if result is None:missing.append(dict(key=key,requirement='Whole unchanged INITIAL construct/replay and resource construct/accept transaction'))
  else:status['imports'].append(_record(root,key,result))
  atomic_json(root/'SESSION_RESULT.json',status)
 counts=module('finite1039_counts');source=module('finite1039_sources')
 for row in source.jobs('n10_14'):
  key='count:'+row['job_id'];cache=durable/'finite1039-counts-n10_14/completed'/source.CATALOG_SHA256[:16]/counts.slug(row['job_id'])
  result=counts.restore_stage(cache,root/'imports/counts',row,log_root=root)
  if result is None:missing.append(dict(key=key,requirement='Full selected fresh native acceptance and original complete controls'))
  else:status['imports'].append(_record(root,key,result))
  atomic_json(root/'SESSION_RESULT.json',status)
 event(root,'finite1014_join_inputs_revalidated',available=len(status['imports']),required=234,missing=len(missing),numerical_replays_started=0,
       full_notebook56_completed=False)
 return missing


def _task(root,record):
 parts=src.parts(record['task_relative']);p=src.ordinary(Path(root).joinpath(*parts));src.need(p.is_dir(),'Actual contained restored complete input');return p


def _validated_inputs(root,records):
 src.need(type(records)is list,'Exact imported complete input records');lookup={r['key']:r for r in records}
 src.need(len(lookup)==len(records),'No duplicate imported source task')
 wanted={k for k,*_ in PARENTS};parents={}
 for key,_,e,s,_ in PARENTS:
  src.need(key in lookup,'Missing complete source-bound input: '+key);record=lookup[key];task=_task(root,record);checked=module(e).validate_completed(task)
  src.need(same(checked,record['validated']),'Whole imported parent evidence still matches its recorded readback')
  source=module(s);parents[key]=dict(task=task,checked=checked,source=source)
 core_source=module('finite1014_core_sources');core_ev=module('finite1014_core_evidence');cores={}
 for row in core_source.plan()['cases']:
  key='core:'+row['case_id'];wanted.add(key);src.need(key in lookup,'Missing complete four-call INITIAL/resource case: '+key)
  record=lookup[key];task=_task(root,record);checked=core_ev.validate_completed(task)
  src.need(same(checked,record['validated'])and checked['summary']['case_id']==row['case_id'],'Exact current full case, without historical receipt rewriting')
  cores[(row['n'],row['band'])]=dict(task=task,row=row,checked=checked)
 count_src=module('finite1039_sources');count_ev=module('finite1039_count_evidence');counts={}
 for row in count_src.jobs('n10_14'):
  key='count:'+row['job_id'];wanted.add(key);src.need(key in lookup,'Missing selected full native acceptance: '+key)
  record=lookup[key];task=_task(root,record);checked=count_ev.validate_completed(task)
  src.need(same(checked,record['validated'])and checked['job_id']==row['job_id'],'Exact current or wholly admitted prior50 count evidence epoch')
  counts[row['job_id']]=dict(task=task,row=row,checked=checked)
 src.need(set(lookup)==wanted and len(wanted)==234,'Only and all234 required complete imports')
 return parents,cores,counts


def _native(parent):
 source=parent['source'];return src.read(parent['task']/'capsule'/source.RESULT,128*src.MIB)


def fourier_and_coarse(parents):
 a,b,c,d,e={k:_native(parents[k])for k in('56A','56B','56C','56D','56E')}.values()
 ns=list(range(10,15));prev=list(range(9,15))
 src.need(a['status']=='PASS_INDEPENDENT_GLOBAL_AUXILIARY9_14_READBACK'and same(a['n'],prev)
  and a['finite_rho']==['1','19/10']and a['target']=='423/1000'
  and set(a['per_n_upper'])==set(map(str,prev))and all(F(v)<F(423,1000)for v in a['per_n_upper'].values()),'Complete unrestricted predecessor ceilings, including n9')
 src.need(a['regional_rho']==['7/5','71/50']and set(a['regional_per_n_upper'])==set(map(str,prev))
  and all(F(v)<F(209,500)for v in a['regional_per_n_upper'].values()),'Separate regional same-law predecessor ceilings; sharp global9 cannot replace them')
 src.need(b['status']=='PASS_INDEPENDENT_SUPPORTED_SAME_LAW9_14_TWO_BAND_READBACK'and same(b['n'],prev)
  and b['support_absolute_upper']=='3','Same supported marginal Fourier applicability')
 for band,(lo,hi,own,_,_,_)in BANDS.items():
  hits=[v for v in b['bands']if v['name']==band];values=b['per_band_per_n_upper'][band]
  src.need(len(hits)==1 and hits[0]['rho']==[lo,hi]and set(values)==set(map(str,prev)),'Literal supported closed low-band scope')
  predecessor='1049/2500'if band=='B0'else'52/125'
  src.need(F(values['9'])<F(predecessor)and all(F(values[str(n)])<F(own)for n in ns),'Distinct supported predecessor and own marginal ceilings')
 src.need(c['status']=='PASS_INDEPENDENT_GLOBAL_HIGHRHO10_14_READBACK'and same(c['n'],ns)
  and c['finite_rho']==['71/50','15/8']and c['target']=='4097/10000'
  and all(F(c['per_n_upper'][str(n)])<F(4097,10000)for n in ns),'Complete universal high-rho route including native infinite tail')
 src.need(d['status']=='PASS_INDEPENDENT_SUPPORTED_CORNER10_14_BH_READBACK'and same(d['n'],ns)
  and d['rho']==['23/20','71/50']and d['support_absolute_upper']=='3'and d['target']=='4097/10000'
  and all(F(d['per_n_upper'][str(n)])<F(4097,10000)for n in ns),'Closed supported corner before high-rho seam')
 src.need(e['status']=='PASS_SUPPORTED_MOMENT_CENTERED_HIGH10_14_COMPLETE_NATIVE_REPLAY_AND_BOUNDED_INDEPENDENT_AUDIT'
  and same(e['n'],ns)and e['complete_native_rows']==20 and len(e['rows'])==10,'All narrow-radius native HIGH rows and original independent controls')
 for band,(_,hi,_,_,radius,hcap)in BANDS.items():
  for n in ns:
   rows=[r for r in e['rows']if type(r['n'])is int and r['n']==n and r['band']==band]
   src.need(len(rows)==1 and rows[0]['rho_upper']==hi and rows[0]['support_radius']==radius
    and rows[0]['target']==hcap and F(rows[0]['upper'])<F(hcap),'HIGH licensed only at its actual refined support radius/rho/n')
 source=parents['56F']['source'];coarse=src.read(parents['56F']['task']/'capsule'/source.NATIVE/'RESULT.json',128*src.MIB)
 src.need(coarse['n']==ns and coarse['radius']=='3'and coarse['rho_interval']==['1','71/50']and len(coarse['rows'])==10,'Coarse full support before supported Fourier/moments')
 for j,row in enumerate(coarse['rows']):
  n=10+j//2;label,lo,hi,cap=('global','1','7/5','423/1000')if j%2==0 else('localized','7/5','71/50','209/500')
  q=n*(F(cap)-F(4097,10000));src.need(type(row['n'])is int and row['n']==n and row['band']==label and row['rho_interval']==[lo,hi]
   and row['predecessor_cap']==cap and F(row['q'])==q,'Actual index-scaled global/regional support license')
  support_scope(row['proof'],n,hi,'3',str(q))
 src.need(parents['56K']['checked']['summary']['kappa']=='62/625','Actual complete scalar-kappa certificate, not an old PASS alias')
 return dict(auxiliary9_global='423/1000',regional_predecessor_rho=['7/5','71/50'],regional_predecessor_cap='209/500',
  same_law_supported9_caps=dict(B0='1049/2500',BN='52/125'),closed_rho_union=[['1','11/10'],['11/10','23/20'],['23/20','71/50'],['71/50','infinity']],
  coarse_support_radius='3',refined_support_before_HIGH=dict(B0='23/10',BN='12/5'),kappa='62/625')


def support_scope(p,n,rho,radius,q):
 src.need(type(p['n'])is int and p['n']==n and p['K']=='0'and p['schema']=='DIRECT_SAME_LAW_CONTACT_SUPPORT_DISCOVERY_V1'
  and p['rho_upper']==rho and p['radius']==radius and p['q_contact']==q and type(p['support_sign'])is int and p['support_sign']==0,
  'Literal same-witness full two-ray support premise')
 src.need(type(p['ray_rows'])is list and len(p['ray_rows'])==2 and [r['sign']for r in p['ray_rows']]==[-1,1]
  and all(type(r['sign'])is int and all(F(r[k])<0 for k in('contact_upper','coefficient_at_R','contact_derivative_at_R','contact_derivative_slope_at_R'))for r in p['ray_rows']),
  'Strict finite support endpoints and both complete outward rays')


def initial_scope(c,a,row):
 n,band=row['n'],row['band'];lo,hi,own,q10,radius,hcap=BANDS[band];q=q10 if n==10 else'0';pcap=('1049/2500'if band=='B0'else'52/125')if n==10 else'CE'
 src.need(type(c['n'])is int and c['n']==n and c['K']=='0'and c['target']=='CE'and c['band']==band
  and c['rho_interval']==[lo,hi]and c['q']==q and c['owncap']==own and c['predecessor_cap']==pcap and c['high_cap']==hcap,
  'Literal actual-index support, predecessor and own/HIGH ceilings')
 src.need(type(c['predecessor_globally_sharp_assumed'])is bool and c['predecessor_globally_sharp_assumed']==(n!=10)
  and c['predecessor']==('GLOBAL C9<.423; then SAME-law supported C9 cap'if n==10 else f'ASSUMED GLOBAL C_{n-1}<CE at every threshold and standardized iid law'),
  'Same-law bounded base9 input or genuine global previous-index hypothesis, never monotonicity')
 src.need(all(c[k]is False for k in('predecessor_discharged_here','owncap_verified','high_acceptance_joined','physical_defect_seed_imported','full_cutoff_proved'))
  and len(c['stages'])==8 and c['stages'][0]['input_D']is None and c['stages'][0]['input_raw']is None,'Unseeded full INITIAL feedback, with conditional native flags')
 src.need(all(c['profile'][k]==radius for k in('radius','radius_minus','radius_plus'))and c['profile']['cap']==own
  and c['profile']['grid']==([12,24,12,3]if n==10 and band=='BN'else[12,12,6,3])and 'p_interval'not in c['profile'],
  'Support acquired before higher moments and entire selected grid/p domain')
 previous=(None,None)
 for stage in c['stages']:
  src.need((stage['input_raw'],stage['input_D'])==previous,'One ordered same-witness feedback chain')
  vals=[]
  for field,old in(('R',previous[0]),('D',previous[1])):
   v=ceilgrid(stage['cover'][field],10**8)+F(1,100000);vals.append(min(v,F(old))if old is not None else v)
  src.need(list(map(F,[stage['next_raw'],stage['next_D']]))==vals and 0<vals[0]<F(2*n,5)and 0<vals[1]<6,'Actual first-raw unweighting license and directed updates')
  previous=stage['next_raw'],stage['next_D']
 for cover in[s['cover']for s in c['stages']]+[c['export']]:
  src.need(all(type(cover[k])is int and cover[k]>=0 for k in('total','active','excluded'))and cover['total']==row['signed_cells_per_cover']
   and cover['active']+cover['excluded']==cover['total']and sum(cover['reasons'].values())==cover['excluded']and len(cover['panels'])==100,'All cells, including every empty/active disposition')
  for i,p in enumerate(cover['panels']):src.need([p['pl'],p['pu']]==[str(F(i,100)),str(F(i+1,100))],'All100 closed original probability panels')
 src.need(same(c['final_invariants'],a['final_invariants'])and c['final_invariants']==dict(raw=previous[0],D=previous[1])
  and (F(previous[1])+1)**2<10,'Final common physical gap and invariant identity')
 support_scope(c['refined_support'],n,hi,radius,q)
 if n==10:
  src.need(F(q)==n*(F(pcap)-F(4097,10000)),'Supported predecessor contact allowance')
  support_scope(c['coarse_support'],n,hi,'3',str(n*(F(423,1000)-F(4097,10000))))
 else:src.need(c['coarse_support']is None,'Sharp global predecessor directly licenses q0 refined support')


def _projection(packet,omitted):return{k:v for k,v in packet.items()if k not in omitted}


def _parent_binding(core,contract,current_row):
 root=core['task'];row=core['row'];oldc=root/'provenance'/row['resource_candidate'];olda=root/'provenance'/row['resource_receipt']
 newc=root/'capsule'/row['resource_candidate'];newa=root/'capsule'/row['resource_receipt']
 src.need(contract['resource_candidate_sha256']==src.digest(oldc)and contract['resource_replay_sha256']==src.digest(olda)
  and contract['resource_row_sha256']==src.digest(current_row),'Old immutable contract is bound to the exact freshly recomputed mathematical row')
 src.need(same(_projection(src.read(oldc,128*src.MIB),{'files_sha256','initial_candidate_sha256','initial_acceptance_sha256'}),
  _projection(src.read(newc,128*src.MIB),{'files_sha256','initial_candidate_sha256','initial_acceptance_sha256'}))
  and same(_projection(src.read(olda,128*src.MIB),{'files_sha256','candidate_sha256','timings_seconds'}),
  _projection(src.read(newa,128*src.MIB),{'files_sha256','candidate_sha256','timings_seconds'})),
  'Whole current/old parent mathematical equivalence; no recursive timing or arbitrary metadata removal')
 return dict(original_candidate_sha256=src.digest(oldc),current_candidate_sha256=src.digest(newc),original_replay_sha256=src.digest(olda),
  current_replay_sha256=src.digest(newa),row_sha256=src.digest(current_row),historical_acceptance_promoted=False,all_mathematical_fields_identical=True)


def _restriction(group,cfg,n,index):
 src.need(len(group)==4,'Exactly four whole closed component acceptances');parts=[]
 for item in group:
  root=item['task']/'capsule'/item['row']['directory'];sub=src.read(root/'SUBDOMAIN.json');parent=src.read(root/'PARENT.json');accepted=src.read(root/item['row']['output'],16*src.MIB)
  part=sub['part'];src.need(type(part)is int and part in range(4)and sub['parts']==4 and sub['n']==n and sub['index']==index
   and sub['original_p']==cfg['p']and sub['schema']=='ORIGINAL_CONTRACT_FOUR_CLOSED_P_SUBPANELS_V1','Literal original-parent component scope')
  cuts=[str(F(cfg['p'][0])+(F(cfg['p'][1])-F(cfg['p'][0]))*j/4)for j in range(5)]
  src.need(sub['cuts']==cuts and sub['p']==cuts[part:part+2]and sub['contract_sha256']==parent['contract_sha256']==item['row']['contract_sha256'],
   'Same original contract and exact closed quarter interval')
  manifest=src.read(root/'KERNEL_COPY_MANIFEST.json');src.need(same(parent['kernel_sha256'],manifest['files']),'Unchanged complete common numerical kernel')
  for key in('resource_candidate_sha256','resource_replay_sha256','resource_row_sha256'):
   src.need(sub[key]==parent[key]==src.read(root/'contract.json')[key],'All resource lineage fields retained as explicit provenance')
  wanted=[sub['p'],['0',cfg['Lambda']],['0','1'],['-1/2','1/2'],['0',cfg['d0']]]
  src.need(same(accepted['root_domain'],wanted)and accepted['part']==part and accepted['parts']==4
   and len(accepted['negative_controls'])==34 and len(accepted['subdomain_negative_controls'])==22,
   'All four other axes retained; full current native and restriction controls')
  parts.append(dict(part=part,p=sub['p'],job_id=item['row']['job_id'],native_receipt_sha256=src.digest(root/item['row']['output'])))
 parts.sort(key=lambda p:p['part']);src.need([p['part']for p in parts]==[0,1,2,3]and parts[0]['p'][0]==cfg['p'][0]
  and parts[-1]['p'][1]==cfg['p'][1]and all(parts[j]['p'][1]==parts[j+1]['p'][0]for j in range(3)), 'Unique ordered complete closed p union')
 return parts


def finite_families(cores,counts):
 groups=defaultdict(list)
 for item in counts.values():r=item['row'];groups[(r['n'],r['band'],r['index'])].append(item)
 src.need(len(groups)==202 and len(counts)==217,'All202 simultaneous parent contracts and217 full native acceptances')
 rows=[];used=set();totals=Counter();component_rows=[];interfaces=[]
 for key in sorted(cores):
  core=cores[key];r=core['row'];root=core['task']/'capsule';n,band=key;c=src.read(root/r['initial_candidate'],128*src.MIB);a=src.read(root/r['initial_receipt'],128*src.MIB)
  initial_scope(c,a,r);candidate=src.read(root/r['resource_candidate'],128*src.MIB);accepted=src.read(root/r['resource_receipt'],128*src.MIB)
  src.need(candidate['n']==accepted['n']==n and candidate['band']==accepted['band']==band and candidate['K']=='0'
   and candidate['q']==c['q']and candidate['owncap']==c['owncap']and candidate['rho_interval']==c['rho_interval']
   and candidate['initial_candidate_sha256']==src.digest(root/r['initial_candidate'])and candidate['initial_acceptance_sha256']==src.digest(root/r['initial_receipt'])
   and accepted['candidate_sha256']==src.digest(root/r['resource_candidate'])and same(accepted['rows'],candidate['rows'])
   and same(accepted['status_counts'],candidate['status_counts'])and same(accepted['files_sha256'],candidate['files_sha256'])
   and accepted['negative_controls']==dict(malformed_inventories=12,parser_controls=2)and len(candidate['rows'])==100,'One full fresh INITIAL/resource witness and complete100-row native replay')
  family_counts=Counter();dispositions=[]
  for i,desc in enumerate(candidate['rows']):
   src.need(type(desc['n'])is int and desc['n']==n and type(desc['index'])is int and desc['index']==i and desc['band']==band
    and desc['p']==[str(F(i,100)),str(F(i+1,100))]and desc['path']==f'rows/{i:03d}.json','All canonical closed p intervals, including seams/endpoints')
   path=root/r['resource_directory']/band/desc['path'];src.need(src.digest(path)==desc['sha256'],'Whole actual resource row');row=src.read(path,16*src.MIB)
   source=deepcopy(c['export']['panels'][i]);source['rho_lo']=BANDS[band][0]
   src.need(same(source,row['source'])and row['n']==n and row['band']==band and row['index']==i and row['status']==desc['status'],'Same complete INITIAL p export and physical resource row')
   status=row['status'];family_counts[status]+=1;totals[status]+=1;group=groups.get((n,band,i),[])
   if status=='EXCLUDED_BY_SAME_LAW_RESOURCE':src.need(row['result']['excluded']is True and not group,'A genuine same-law exclusion needs no count and cannot hide a selected count')
   else:
    src.need(status=='RESOURCE_ROW_ACQUIRED_FOR_COUNT'and row['result']['excluded']is False and group,'Criterion failure or missing count never excludes a marginal')
    contracts=[src.read(item['task']/'capsule'/item['row']['directory']/'contract.json')for item in group]
    src.need(all(same(contracts[0],q)for q in contracts)and len(contracts[0]['rows'])==1,'One simultaneous whole original parent contract')
    cfg=contracts[0]['rows'][0];interface(row,cfg,band,i,n);bridge=_parent_binding(core,contracts[0],path)
    interfaces.append(dict(n=n,band=band,index=i,contract_sha256=group[0]['row']['contract_sha256'],fresh_parent_bridge=bridge))
    if(n,band,i)in COMPOSITES:
     parts=_restriction(group,cfg,n,i);component_rows.append(dict(n=n,band=band,index=i,parts=parts))
    else:src.need(len(group)==1 and len(group[0]['row']['expected_controls'])==24,'One whole original panel; no partial replacement')
    used.add((n,band,i))
   dispositions.append(dict(index=i,p=desc['p'],status=status))
  src.need(dict(family_counts)==candidate['status_counts'],'Independent full100 resource disposition census')
  rows.append(dict(n=n,band=band,original_panels=100,closed_panels=100,status_counts=dict(family_counts),dispositions=dispositions))
 src.need(used==set(groups)and len(interfaces)==202 and len(component_rows)==5 and sum(len(p['parts'])for p in component_rows)==20
  and totals==Counter(EXCLUDED_BY_SAME_LAW_RESOURCE=798,RESOURCE_ROW_ACQUIRED_FOR_COUNT=202),'Exactly all1000 dispositions,202 contracts,5 overrides and20 restrictions')
 return dict(families=rows,resource_dispositions=1000,resource_excluded=798,parent_contract_interfaces=interfaces,composite_restrictions=component_rows,
  complete_native_forests=217,ordinary_whole_panel_forests=197,composite_original_panels=5,component_forests=20)


def sequential(base,local):
 src.need(type(base)is bool and type(local)is dict and set(local)=={11,12,13,14}
  and all(type(k)is int and type(v)is bool for k,v in local.items()),'Exact finite predecessor induction scope')
 current=base;rows=[]
 for n in range(11,15):
  previous=current;current=previous and local[n];rows.append(dict(n=n,global_predecessor=n-1,predecessor_established=previous,
   conditional_local_implication_complete=local[n],conditional_finite_result_established=current))
 return rows


def validate_batch(root,status=None):
 root=Path(root);status=src.read(root/'SESSION_RESULT.json',64*src.MIB)if status is None else status
 src.need(status['schema']=='FINITE1014_FULL_FINITE_JOIN_SESSION_V1'and all(status[f]is False for f in controls.FLAGS),
  'Finite conditional scope without all-law/native/parent promotion')
 records=status['controls'];src.need([r['job_id']for r in records]==[r['job_id']for r in src.jobs()],'All ten unchanged original bounded calls')
 dependencies={}
 for record in records:
  task=_task(root,record);checked=controls.validate_completed(task);src.need(same(checked,record['validated']),'Actual complete source-bound control epoch')
  request,row=src.verify(task);wanted={n:src.digest(p)for n,p in dependencies.items()if n in request['original_sources']}
  src.need(same(request['dependency_files_sha256'],wanted),'Every current control binds the actual complete preceding control evidence')
  if row['output']in src.DEPENDENCIES:dependencies[row['output']]=task/'capsule'/row['output']
 parents,cores,counts=_validated_inputs(root,status['imports']);fourier=fourier_and_coarse(parents);finite=finite_families(cores,counts)
 chain=sequential(True,{n:True for n in range(11,15)})
 src.need(all(r['conditional_finite_result_established']for r in chain),'Consecutive global predecessors, without eventual15 or global9 shortcuts')
 return dict(schema='CONDITIONAL_FINITE10_14_COMPLETE_INTERFACE_JOIN_V1',implementation=implementation(),
  finite_indices=list(range(10,15)),base10_freshly_reconstructed=True,base9_input='Actual56A unrestricted/regional and56B same-law supported n9 ceilings, after actual10coarse support',
  sequential_chain=chain,analytic_premises=list(ANALYTIC_PREMISES),Fourier_support_HIGH_interfaces=fourier,finite_interfaces=finite,
  control_invocations=10,retained_review_scopes=7,completed_imports=234,incoming_eventual15_used=False,
  incoming_sharp_global9_used=False,old_capture_impersonated=False,old_timed_parent_hashes_rewritten=False,
  conditional_finite_chain_verified=True,**{f:False for f in controls.FLAGS})


def validate_completed(root):
 root=Path(root);status=src.read(root/'SESSION_RESULT.json',64*src.MIB)
 src.need(status['state']=='complete_finite10_14_under_explicit_analytic_premises'and status['conditional_controls_completed']is True
  and status['conditional_finite_chain_verified']is True,'Completed actual56Ifinite conditional session')
 summary=validate_batch(root,status);src.need(same(summary,status['finite_summary']),'Whole source/capture/control/interface/finite-induction summary')
 return dict(schema='REVALIDATED_FINITE1014_FINITE_JOIN_V1',session_result_sha256=src.digest(root/'SESSION_RESULT.json'),summary=summary,
  conditional_finite_chain_verified=True,**{f:False for f in controls.FLAGS})
