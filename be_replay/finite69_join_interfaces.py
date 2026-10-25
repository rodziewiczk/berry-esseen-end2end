"""65: all284 exact native resource interfaces and closed1200-panel cover."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
from . import finite69_join_sources as src,finite69_sources as counts
from .finite69_remaining import namespace,same,no_times

BANDS={'B0':('1','11/10','23/10','423/1000','69/200'),
 'BN':('11/10','23/20','12/5','209/500','3/8'),
 'B2':('23/20','237/200','5/2','83/200','83/200')}
PROGRAMS={'n6_plain':'work/cutoff6_20261018/audit/count_B0_batch21_readback_v1/common.py',
 'n6_mean':'work/cutoff6_20261020/audit/b2_count_readback_v1/common.py',
 'later':'work/cutoff6_20261020/audit/count7_9_readback_v1/common.py'}
def programs(source):
 result={};p=src.plan()
 for key,name in PROGRAMS.items():
  f=Path(source)/name;src.need(src.digest(f)==p['semantic_inputs'][name],'Exact original independent interface source')
  result[key]=namespace(f)
 return result
def interface(row,contract,selection,readers):
 n,band,i=selection['n'],selection['band'],selection['index'];cfg=contract['rows'][0]
 src.need(type(n)is int and 6<=n<=9 and len(contract['rows'])==1 and contract['n']==n
  and type(contract['n'])is int and contract['band']==band and contract['index']==i and type(contract['index'])is int,
  'One complete actual-index native contract, never a selected subdomain')
 reader=readers['later'if n>6 else'n6_mean'if'acquired_scale_upper'in cfg else'n6_plain']
 reader['interface'](row,cfg,band,i,n)
 raw=row['result']['raw_row'];r=row['result']['result']
 if 'acquired_gamma'in cfg:
  src.need(list(map(F,cfg['acquired_gamma']))==[reader['floorgrid'](raw['gamma_lo'],10**6),reader['ceilgrid'](raw['gamma_hi'],10**6)],
   'Both signed third-moment endpoints from the same acquired law')
 else:src.need((n,band,i)==(6,'B0',42),'Only the original geometry42 kernel omits the explicit gamma polygon')
 SL=F(3162277660,10**9);rho,D,gh,mu=map(F,[r['rho_lo'],r['D'],raw['gamma_hi'],raw['mean_hi']])
 price=max((SL-1)*rho,SL*rho-gh)-D
 src.need(SL*SL<10 and price>0 and mu>0,'Positive licensed physical gap price')
 gap=max(F(raw['A'])+F(raw['B']),reader['sqrtlo'](max(F(0),2*rho-2*D/(SL-1),2*price/(3*mu)),10**12))
 lo,hi=map(F,cfg['p']);upper=reader['ceilgrid'](1-gap*reader['sqrtlo'](min(lo*(1-lo),hi*(1-hi)),10**12),10**6)
 src.need(F(cfg['geometry_gap_lower'])==gap and F(cfg['acquired_inward_upper'])==upper,
  'Whole original physical inward contraction, signed gamma and gap')
 return dict(n=n,band=band,index=i,p=cfg['p'],rho=list(selection['band_rho']),
  resource_path=contract['resource_path'],resource_sha256=contract['resource_sha256'],
  contract_sha256=selection['contract_pin'],signed_gamma=cfg.get('acquired_gamma'),whole_native_domain=True)
def parent_result(task,checked,index):
 """The complete parent reader has replayed these exact numerical objects."""
 c=Path(task)/'capsule';summary=checked['summary'];receipt=src.read(Path(task)/summary['receipt_relative'],128*src.MIB)
 if 'result'in receipt:return receipt['result']
 source_relative=summary['receipt_relative'].removeprefix('capsule/').rsplit('/',1)[0]
 # Only the current46 metadata epoch has a FRESH_SOURCE_RESULT slot.
 source=c/source_relative/('FRESH_SOURCE_RESULT.json'if checked.get('kind')=='resource'else'SOURCE_RESULT.json')
 result=src.read(source,128*src.MIB)
 src.need(type(result['rows'])is list and len(result['rows'])==100,'All100 source rows replayed by the full parent acceptor')
 row=result['rows'][index];src.need(type(row['index'])is int and row['index']==index,'Same actual probability panel')
 return row['result']
def bind_parent(physical,selection,resources,locals_):
 n,band,i=selection['n'],selection['band'],selection['index']
 choices=[]
 if n==6:
  choices=[v for v in locals_.values()if v['checked']['summary']['kind']=='local_resource'
   and v['checked']['summary']['band']==band and v['checked']['summary']['index']==i]
 choices+= [resources[(n,band)]]
 for parent in choices:
  result=parent_result(parent['task'],parent['checked'],i)
  if same(no_times(result),no_times(physical['result'])):
   return dict(job_id=parent['checked']['job_id'],stage_result_sha256=parent['checked']['stage_result_sha256'],
    entire_same_law_resource_equal=True)
 raise ValueError('No genuine complete parent supplies the immutable contract resource: '+selection['job_id'])
def finite_cover(source,counts_by_id,resources,locals_,*,bind=True):
 source=Path(source);p=src.plan();readers=programs(source);selected=counts.jobs('count')
 src.need(len(counts_by_id)==len(selected)==284 and set(counts_by_id)=={r['job_id']for r in selected},'All284 full native COUNT transactions')
 edges=[];by_band={};used=set();totals=Counter()
 for row in selected:
  item=counts_by_id[row['job_id']];s=row['selection'];path=s['capsule']+'/contract.json';contract=src.read(Path(item['task'])/'capsule'/path)
  src.need(src.digest(Path(item['task'])/'capsule'/path)==s['contract_pin'],'Immutable original native contract SHA')
  physical_path=source/contract['resource_path'];pin=p['semantic_inputs'][contract['resource_path']]
  src.need(src.digest(physical_path)==pin==contract['resource_sha256'],'Whole immutable resource bytes, historical identity retained')
  physical=src.read(physical_path,128*src.MIB);edge=interface(physical,contract,s,readers)
  if bind:edge['current_parent_binding']=bind_parent(physical,s,resources,locals_)
  edges.append(edge);key=(s['n'],s['band']);by_band.setdefault(key,{})[s['index']]=edge
  used.add(row['job_id'])
 covers=[]
 for key,lookup in sorted(by_band.items()):
  n,band=key;job=next(r for r in selected if(r['selection']['n'],r['selection']['band'])==key)
  name=job['selection']['composer_receipt'];src.need(src.digest(source/name)==p['semantic_inputs'][name],'Exact whole reference cover geometry')
  ref=src.read(source/name,128*src.MIB);cover=ref['coverage'];rows=cover['rows']
  src.need(cover['n']==n and type(cover['n'])is int and cover['band']==band and cover['rho']==list(BANDS[band][:2])
   and len(rows)==100 and cover['target']==job['selection']['target'],'Whole same-index, same-law probability cover')
  current=None
  if bind:
   parent=resources[key];current=src.read(parent['task']/parent['checked']['summary']['receipt_relative'],128*src.MIB)
  local=Counter()
  for i,r in enumerate(rows):
   src.need(type(r['index'])is int and r['index']==i and r['p']==[str(F(i,100)),str(F(i+1,100))],'All closed probability seams and endpoint cases')
   kind=r['closure'];local[kind]+=1;totals[kind]+=1
   if kind=='count':src.need(i in lookup,'Complete original COUNT for this entire panel')
   elif kind=='resource':
    src.need(i not in lookup and (current is None or i in current['excluded']),'Fresh whole-panel resource exclusion')
   else:
    src.need(kind=='sign_mass'and n==6 and i in{'B0':[35,36],'BN':[32,33],'B2':[30,31]}[band]
     and i not in lookup and F(i+1,100)*F(BANDS[band][1])**2<F(11261,25000),'Exact whole sign-mass exclusion')
  src.need(dict(local)==ref['census']and set(lookup)=={r['index']for r in rows if r['closure']=='count'},'Every and only original retained COUNT panel')
  covers.append(dict(n=n,band=band,rho=list(BANDS[band][:2]),census=dict(local),probability=['0','1'],rows=rows))
 src.need(len(covers)==12 and totals==Counter(resource=910,sign_mass=6,count=284),'Whole1200-panel disjoint disposition census')
 return dict(finite_indices=[6,7,8,9],panels=1200,census=dict(totals),count_interfaces=edges,bands=covers,
  conditional_same_law_interfaces=bind,global_proof_accepted=False)

def induction(finite,*,global_auxiliary5):
 """Finite-only epoch of the original composer; no imported eventual10 tail."""
 src.need(global_auxiliary5 is True and finite['conditional_same_law_interfaces']is True,
  'Acquired whole global auxiliary5 and all same-law finite interfaces')
 expected=deepcopy(finite['bands']);indices=[6,7,8,9]
 chain=dict(indices=indices,branches=[dict(n=n,current_score='C_n>=C_E',
  predecessor='GLOBAL_C5<429/1000'if n==6 else f'GLOBAL_C{n-1}<C_E',q='579/5000'if n==6 else'0')for n in indices],
  bands=expected,complement_from='237/200',incoming_eventual10_tail=None,unqualified=False)
 def validate(z):
  src.need(type(z)is dict and set(z)==set(chain)and z['indices']==[6,7,8,9]
   and all(type(n)is int for n in z['indices'])and z['unqualified']is False
   and z['complement_from']=='237/200'and z['incoming_eventual10_tail']is None,'Exact finite conditional domain, no circular incoming tail')
  src.need(same(z['bands'],expected)and len(z['branches'])==4,'All12 actual closed bands')
  done=set()
  for n,r in zip(indices,z['branches']):
   src.need(type(r)is dict and set(r)=={'n','current_score','predecessor','q'}and type(r['n'])is int and r['n']==n
    and r['current_score']=='C_n>=C_E'and r['q']==('579/5000'if n==6 else'0'),'Equality-inclusive contrary branch and correct contact allowance')
   src.need(r['predecessor']==('GLOBAL_C5<429/1000'if n==6 else f'GLOBAL_C{n-1}<C_E')
    and(n==6 or n-1 in done),'Whole global predecessor, established in order')
   src.need([b['band']for b in z['bands']if b['n']==n]==['B0','B2','BN'],'All three actual regional exclusions')
   done.add(n)
  src.need(done==set(indices),'All finite conclusions6--9')
 validate(chain);controls=[]
 mutations=[('missing base',lambda z:z['branches'].pop(0)),('reordered branches',lambda z:z['branches'].reverse()),
  ('equality omitted',lambda z:z['branches'][0].update(current_score='C_n>C_E')),
  ('wrong base contact allowance',lambda z:z['branches'][0].update(q='0')),
  ('selected-law precursor',lambda z:z['branches'][0].update(predecessor='C5(P) at one threshold')),
  ('missing band',lambda z:z['bands'].pop()),('duplicate band',lambda z:z['bands'].__setitem__(1,deepcopy(z['bands'][0]))),
  ('changed target',lambda z:z['bands'][0].update(target='1')),
  ('open moment seam',lambda z:z.update(complement_from='6/5')),
  ('false unconditional claim',lambda z:z.update(unqualified=True)),('boolean index',lambda z:z['indices'].__setitem__(0,True)),
  ('spurious incoming eventual10 tail',lambda z:z.update(incoming_eventual10_tail={'old_PASS':True})),
  ('missing intermediate predecessor',lambda z:z['branches'][2].update(predecessor='GLOBAL_C6<C_E'))]
 for label,mutate in mutations:
  bad=deepcopy(chain);mutate(bad)
  try:validate(bad)
  except(ValueError,KeyError,TypeError):controls.append(label)
  else:raise ValueError('Malformed finite composition accepted: '+label)
 from .n5_remaining_sources import unique
 import json
 try:json.loads('{"n":6,"n":7}',object_pairs_hook=unique)
 except ValueError:controls.append('duplicate JSON key')
 else:raise ValueError('Ambiguous finite composition JSON accepted')
 src.need(len(controls)==14,'All finite-epoch composition controls')
 return dict(chain=chain,negative_controls=controls,conditional_finite_chain_verified=True,
  historical_T10_tail_imported=False,global_proof_accepted=False)
