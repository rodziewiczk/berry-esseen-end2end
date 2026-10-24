"""Check-only selected actual15 chain; independently rebuild coverage/geometry.
Usage: python -B check.py SNAPSHOT_NAME.json. No inherited module is imported.
Missing final receipts remain pending and never imply a theorem.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from math import isqrt
from collections import Counter
from copy import deepcopy
import json,sys
H=Path(__file__).resolve().parent;R=H.parents[3];N=H.parents[1]
G={};pending=[];summary={};controls=Counter()
BANDS={'B0':('1','11/10','417/1000','219/2000','23/10','191/500'),
       'BN':('11/10','23/20','827/2000','57/1000','12/5','409/1000')}
EMPTY={'EMPTY_JOINT_INWARD_MOMENT','EMPTY_ACQUIRED_INWARD_NOISE','EMPTY_PHASE','EMPTY_NEGATIVE_BUDGET','EMPTY_PHASE_RESOURCE','EMPTY_SUPPORT_VARIANCE','EMPTY_SHARP_BOX','EMPTY_SHARP_GAP','EMPTY_RHO_BRANCH','EMPTY_RHO_UPPER','EMPTY_VARIANCE_IDENTITY','EMPTY_JOINT_CUBICS','EMPTY_ACQUIRED_RHO_VARIANCE','EMPTY_ACQUIRED_BETA_VARIANCE','EMPTY_ACQUIRED_BETA','EMPTY_ACQUIRED_MEAN','EMPTY_ACQUIRED_ALPHA'}

def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return sha256(p.read_bytes()).hexdigest()
def unique(pairs):
    z={}
    for k,v in pairs:need(k not in z,'duplicate JSON key');z[k]=v
    return z
def invalid(_):raise ValueError('nonfinite JSON')
def read(p):return json.loads(p.read_text(),object_pairs_hook=unique,parse_constant=invalid)
def same(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    return a==b
def untimed(a):
    if type(a)is dict:return{k:untimed(v)for k,v in a.items()if k not in ['seconds','initial_seconds']}
    if type(a)is list:return[untimed(v)for v in a]
    return a
def integer(x):need(type(x)is int,'literal integer');return x
def rational(x):
    need(type(x)is str,'rational string');z=F(x);need(str(z)==x,'canonical rational');return z
def bind(p,digest=None):
    p=p.resolve();need(p.is_relative_to(R)and p.is_file(),'existing workspace file '+str(p));v=sha(p)
    need(digest is None or v==digest,'source mismatch '+str(p));k=str(p.relative_to(R))
    need(k not in G or G[k]==v,'conflicting source epoch '+k);G[k]=v;return v
def merge(g):
    need(type(g)is dict and g,'nonempty source graph')
    for p,v in g.items():
        need(type(p)is str and not Path(p).is_absolute()and'..'not in Path(p).parts,'safe source path')
        need(type(v)is str and len(v)==64,'source digest');bind(R/p,v)
def load(p,graph=True):
    bind(p);z=read(p)
    if graph and 'files_sha256'in z:merge(z['files_sha256'])
    return z
def missing(p,edge):
    if p.exists():return False
    pending.append(dict(edge=edge,path=str(p.relative_to(R)),status='MISSING_FINAL_RECEIPT'));return True
def reject(fun,label):
    try:fun()
    except(ValueError,KeyError,TypeError,IndexError,ZeroDivisionError):controls[label]+=1
    else:raise ValueError('negative control accepted '+label)
def floorgrid(x,grid):x=F(x);return F(x.numerator*grid//x.denominator,grid)
def ceilgrid(x,grid):return-floorgrid(-F(x),grid)
def sqrtlo(x,grid=10**24):return F(isqrt(x.numerator*grid*grid//x.denominator),grid)
def sqrthi(x,grid=10**24):
    a=sqrtlo(x,grid);return a if a*a==x else a+F(1,grid)
def atan_pair(q,terms):
    a=sum((F((-1)**j,(2*j+1)*q**(2*j+1))for j in range(terms)),F(0))
    b=a+F((-1)**terms,(2*terms+1)*q**(2*terms+1));return min(a,b),max(a,b)
al,ah=atan_pair(5,100);bl,bh=atan_pair(239,40)
PIlo,PIhi=16*al-4*bh,16*ah-4*bl
CElo=(3+sqrtlo(F(10),10**60))*sqrtlo(1/(2*PIhi),10**60)/6
need(F(4097,10000)<CElo<F(40974,100000),'independent CE interval')
def polymin(a,b,c,upper):
    vals=[a,a+b*upper+c*upper*upper]
    if c>0 and 0<-b/(2*c)<upper:vals.append(a-b*b/(4*c))
    return min(vals)
def capture(directory):
    m=load(directory/'metadata.json',False)
    need(integer(m['returncode'])==0,'successful exact capture')
    need(not(directory/'stderr.txt').read_bytes(),'empty captured stderr')
    for stream in ['stdout','stderr']:
        bind(directory/(stream+'.txt'),m[stream+'_sha256'])
    need('-B'in m['command'] and '-O'not in m['command'] and '-OO'not in m['command'],'ordinary exact Python')
    if 'changed_inputs'in m:need(m['changed_inputs']==[],'unchanged runtime inputs')
    return m

def support():
    p=N/'analytic/support15_19_replay_v1/REPLAY_CHECKED.json';a=load(p)
    need(a['status']=='PASS_FRESH_ACTUAL15_19_TWO_RAY_SUPPORT_REPLAY_CONDITIONAL'and same(a['n_values'],list(range(15,20)))and a['rho_interval']==['1','33/25']and a['radius']=='3','full coarse support scope')
    need(a['full_ray_rows']==10 and a['malformed_controls']==14 and a['parser_controls']==2 and a['predecessor_premise_discharged_here']is False,'coarse support replay scope')
    c=load(N/'analytic/initial15_v1/SUPPORT15_19_BRIDGE.json')
    need(sha(N/'analytic/initial15_v1/SUPPORT15_19_BRIDGE.json')==a['candidate_sha256'],'support candidate identity')
    row=c['rows'][0];need(integer(row['n'])==15 and F(row['q'])==15*F(103,10000),'same-law actual15 allowance')
    z=row['proof'];need(z['radius']=='3'and z['rho_upper']=='33/25'and z['support_sign']==0,'coarse two-ray physical scope')
    need([integer(t['sign'])for t in z['ray_rows']]==[-1,1]and all(F(t['contact_upper'])<0 for t in z['ray_rows']),'both strictly excluded rays')
    capture(R/'runs/cutoff15_20261017/analytic/support15_19_bridge01');capture(R/'runs/cutoff15_20261017/analytic/support15_19_replay01')
    summary['coarse_support']=dict(execution='fresh native replay plus independent scope check',radius='3',q=row['q'],retained_A=True)

def high():
    for rel in ['audit/cancellation_high_review_v1/CHECKED.json','fourier/cancellation_high_readback_v1/CHECKED.json','audit/resource15_range_v1/CHECKED.json','audit/count15_range_v1/CHECKED.json']:
        load(N/rel)
    d=R/'runs/cutoff15_20261017/root/cancellation_high_construct01';c=load(d/'RESULT.json',False)
    d2=R/'runs/cutoff15_20261017/root/cancellation_high_replay01';a=load(d2/'RESULT.json',False)
    need(same(untimed(c),untimed(a)),'complete compensated HIGH construction/replay identity')
    capture(d);capture(d2)
    need(c['status']=='PASS_SUPPORTED_COMPENSATED_HIGH15_19'and len(c['rows'])==15,'complete supported HIGH table')
    for band,(_,rh,_,_,_,hc)in BANDS.items():
        rows=[r for r in c['rows']if integer(r['n'])==15 and r['band']==band]
        need(len(rows)==1 and rows[0]['rho_upper']==rh and rows[0]['support_radius']=='3'and rows[0]['strict_target_pass']is True and F(rows[0]['upper'])<F(hc),'same-law HIGH scope')
    summary['compensated_high']=dict(execution='fresh full native replay and independent mathematical/receipt audits',support_upper='3',caps={b:x[-1]for b,x in BANDS.items()})

def initial(band):
    lo,hi,cap,q,radius,hcap=BANDS[band]
    cp=N/'analytic/initial15_compensated_v1'/f'{band}_RESULT.json';ap=N/'analytic/initial15_compensated_replay_v1'/f'{band}_REPLAY_CHECKED.json'
    c,a=load(cp),load(ap)
    need(c['status']=='EXACT_SHARP15_CONDITIONAL_INITIAL_CANDIDATE_READY_FOR_RESOURCE_REVIEW'and a['status']=='PASS_FRESH_UNSEEDED_ACTUAL15_COMPENSATED_INITIAL_REPLAY_CONDITIONAL','fresh complete INITIAL')
    need(a['candidate_sha256']==sha(cp) and c['n']==a['n']==15 and type(c['n'])is type(a['n'])is int,'actual15 INITIAL identity')
    for z in [c,a]:
        need(z['band']==band and z['rho_interval']==[lo,hi]and z['q']==q and z['owncap']==cap,'same-law INITIAL band and caps')
        for k in ['predecessor_verified','owncap_verified','cutoff15_proved']:need(z[k]is False,'retained scope flags')
    need(a['physical_defect_seed_imported']is False and 'universal_moment_defect_seed'not in c,'no refuted seed')
    need(a['fresh_complete_covers']==9 and a['signed_cells_per_cover']==2592 and a['original_probability_panels']==100 and a['malformed_controls']==20 and a['parser_controls']==2,'full native INITIAL replay coverage')
    need(len(c['stages'])==8 and c['stages'][0]['input_raw']is None and c['stages'][0]['input_D']is None,'unseeded eight updates')
    previous=(None,None)
    for stage in c['stages']:
        need((stage['input_raw'],stage['input_D'])==previous,'ordered same-law INITIAL feedback')
        z=stage['cover']
        vals=[]
        for field,old in [('R',previous[0]),('D',previous[1])]:
            v=ceilgrid(z[field],10**8)+F(1,100000)
            if old is not None:v=min(v,F(old))
            vals.append(v)
        need([F(stage['next_raw']),F(stage['next_D'])]==vals and all(0<x<6 for x in vals),'independent outward update')
        previous=(stage['next_raw'],stage['next_D'])
    for z in [x['cover']for x in c['stages']]+[c['export']]:
        need(integer(z['total'])==2592 and integer(z['active'])+integer(z['excluded'])==2592 and sum(integer(v)for v in z['reasons'].values())==z['excluded'],'complete signed finite cover accounting')
        need(len(z['panels'])==100,'all original p panels')
        for i,row in enumerate(z['panels']):need([row['pl'],row['pu']]==[str(F(i,100)),str(F(i+1,100))]and integer(row['cells'])>=0,'closed p cover with shared seams')
    need(same(c['final_invariants'],a['final_invariants'])and c['final_invariants']==dict(raw=previous[0],D=previous[1]),'final INITIAL identity')
    need(F(previous[1])<sqrtlo(F(10),10**50)-1,'strict physical central gap threshold')
    need(c['chosen_support']['radius']==radius,'independently acquired radius')
    sp=c['chosen_support']['proof'];need(sp['n']==15 and sp['q_contact']==q and sp['rho_upper']==hi and sp['radius']==radius and sp['support_sign']==0,'refined support exact same-law edge')
    need([r['sign']for r in sp['ray_rows']]==[-1,1]and all(F(r['contact_upper'])<0 for r in sp['ray_rows']),'both refined support rays')
    need(F(q)==15*(F(cap)-F(4097,10000))and F(radius)<=3,'acyclic supported allowance/HIGH premise')
    for action in ['construct','replay']:capture(R/f'runs/cutoff15_20261017/analytic/initial15_compensated_{band}_{action}01')
    return c

def interface(row,cfg,band,index):
    lo,hi,_,_,_,_=BANDS[band];r=row['result']['result'];raw=row['result']['raw_row'];s=row['source']
    need(cfg['n']==15 and type(cfg['n'])is int and cfg['K']=='0'and cfg['index']==index and type(cfg['index'])is int,'literal original count target')
    need(cfg['p']==[str(F(index,100)),str(F(index+1,100))]==[r['pl'],r['pu']]==[s['pl'],s['pu']]==[raw['pl'],raw['pu']],'same whole original p panel')
    need(cfg['rho_lower']==lo and F(cfg['rho_upper'])>=F(r['rho_hi'])and F(r['rho_hi'])<=F(hi),'rho band domination')
    need(F(r['D'])-F(r['charge_b'])==F(r['charge_g'])*F(r['d0'])==F(r['charge_h'])*F(r['lambda_max'])>0,'original shared resource identity')
    for a,b in [('D','D'),('d0','d0'),('lambda_max','Lambda'),('H_minus','Hminus'),('H_plus','Hplus'),('radius_minus','radius_minus'),('radius_plus','radius_plus'),('outer0','outer0'),('outer1','outer1')]:need(F(cfg[b])==ceilgrid(r[a],10**6),'exact outward upper '+b)
    for a,b in [('charge_b','binary_charge'),('charge_g','gap_charge'),('charge_h','noise_charge')]:need(F(cfg[b])==floorgrid(r[a],10**6),'exact outward price '+b)
    need(cfg['acquired_lambda_upper']==cfg['Lambda'],'original Lambda retained; redundant cap only')
    need(0<F(cfg['d0'])<F(1,2)and F(cfg['Lambda'])>0 and F(cfg['gap_charge'])>0 and F(cfg['noise_charge'])>0,'positive acquired resource domain')
    need(F(1,4)+F(cfg['Lambda'])/15<1 and 15*F(cfg['p'][0])>F(cfg['Hminus'])and 15*F(cfg['p'][1])+F(cfg['Hplus'])<15,'all16 nearest-count roots')
    sign=cfg['sign_premise'];need(sign['conditional_means_zero']is True and sign['schema']=='ACTUAL_SIGN_CONDITIONED_MARGINAL_V1'and sign['resource_status']=='ASSUMED_ACQUIRED_FOR_CONDITIONAL_TEST','same centered sign marginals')
    for key,src in [('negative_endpoint_lower','A'),('positive_endpoint_lower','B')]:need(0<F(sign[key])==floorgrid(raw[src],10**6),'positive physical endpoint floor')
    beta=[floorgrid(max(F(s['beta_lo']),F(raw['beta_lo'])),10**6),min(F(1),ceilgrid(min(F(s['beta']),F(raw['beta_hi_signed'])),10**6))]
    mean=[max(F(0),floorgrid(s['mean_lo'],10**6)),min(F(1,2),ceilgrid(min(F(s['mean_hi']),F(raw['mean_hi'])),10**6))]
    need(list(map(F,cfg['acquired_beta']))==beta and -1<=beta[0]<=beta[1]<=1,'signed physical beta intersection')
    need(list(map(F,cfg['acquired_mean']))==mean and 0<=mean[0]<=mean[1]<=F(1,2),'physical mean intersection')
    need(len(cfg['quadratics'])==len(r['quadratics']),'all original phase quadratics')
    for t,z in zip(cfg['quadratics'],r['quadratics']):
        for key in ['A','Fplus','Fminus','Qbudget']:need(F(t[key])==(floorgrid if key=='Qbudget'else ceilgrid)(z[key],10**6),'directed phase coefficient')
        need(F(t['Qbudget'])>0,'positive phase curvature')
        for sign in ['plus','minus']:
            need(polymin(F(t['A'])-F(z['A']),F(t['F'+sign])-F(z['F'+sign]),F(z['Qbudget'])-F(t['Qbudget']),F(cfg['H'+sign]))>=0,'whole signed phase interval domination')

def geometry(f,cfg):
    need(integer(f['n'])==15 and integer(f['index'])==cfg['index'],'literal actual15 forest')
    target=rational(f['target']);need(F(4097,10000)<target<CElo,'unchanged safe sharp rational target')
    need(type(f['roots'])is list and len(f['roots'])==16,'all16 roots')
    root=[list(map(F,cfg['p'])),[F(0),F(cfg['Lambda'])],[F(0),F(1)],[F(-1,2),F(1,2)],[F(0),F(cfg['d0'])]]
    nodes=leaves=depthmax=0;statuses=Counter();maximum=F(0)
    def walk(z,box,depth):
        nonlocal nodes,leaves,depthmax,maximum
        nodes+=1;depthmax=max(depthmax,depth);need(nodes<=10000 and depth<=128,'finite forest bounds')
        need(type(z)is dict and z.get('kind')in ['split','leaf'],'known node')
        if z['kind']=='split':
            need(set(z)=={'kind','axis','cut','left','right'},'both closed children')
            axis=integer(z['axis']);need(0<=axis<5,'split axis');cut=rational(z['cut']);need(box[axis][0]<cut<box[axis][1],'strict interior cut')
            l,h=deepcopy(box),deepcopy(box);l[axis][1]=cut;h[axis][0]=cut
            walk(z['left'],l,depth+1);walk(z['right'],h,depth+1);return
        need(set(z)=={'kind','box','decision','result'},'exact leaf fields')
        need(same(z['box'],[[str(x)for x in q]for q in box]),'leaf reconstructed from original root')
        decision=z['decision'];need(decision in EMPTY or decision=='PASS_TARGET','known proved closure')
        need(type(z['result'])is dict,'complete stored arithmetic result')
        if decision=='PASS_TARGET':
            score=rational(z['result']['score_upper']);need(0<=score<target,'strict leaf score');maximum=max(maximum,score)
            need(z['result']['status']in ['PASS','UNRESOLVED'],'native score classification')
        else:need(z['result']['status']==decision,'native empty classification')
        leaves+=1;statuses[decision]+=1
    for k,z in enumerate(f['roots']):
        need(type(z)is dict and set(z)=={'k','tree'}and integer(z['k'])==k,'canonical nearest-count order')
        walk(z['tree'],root,0)
    need(nodes==2*leaves-16,'full binary forest identity')
    return dict(nodes=nodes,leaves=leaves,closed_statuses=dict(statuses),maximum_score=str(maximum),maximum_depth=depthmax)

def count_receipt(band,index,desc,cfg):
    d=N/f'analytic/count15_v1/{band}/capsule{index}';rp=d/'ROW_RESULT.json'
    if missing(rp,f'{band} p{index} full count run'):return None
    row=load(rp,False)
    if row['status']!='FRESH_NATIVE_ACTUAL15_FULL_PANEL_ACCEPTED_CONDITIONAL':
        pending.append(dict(edge=f'{band} p{index} full count',path=str(rp.relative_to(R)),status=row['status']));return None
    fp=d/f'COUNT{index}_FOREST.json';ap=d/f'COUNT{index}_ACCEPTED.json';forest=load(fp,False);accepted=load(ap,False)
    m=load(d/'KERNEL_COPY_MANIFEST.json',False);need(len(m['files'])==24,'all generic count math modules')
    for name,v in m['files'].items():bind(d/name,v)
    bind(d/'count_protocol.py');bind(d/'construct_alpha4.py');bind(d/'SOURCE_PORT.diff');bind(d/'SOURCE_TRANSFORMS.json')
    need(accepted['status']==desc['status']and integer(accepted['n'])==15 and integer(accepted['index'])==index,'native literal acceptance')
    need(accepted['forest_sha256']==row['forest_sha256']==sha(fp)and row['accepted_sha256']==sha(ap),'same selected count proof')
    need(forest['contract_sha256']==accepted['contract_sha256']==row['contract_sha256']==sha(d/'contract.json'),'same acquired contract')
    need(forest['checker_sha256']==accepted['checker_sha256']==sha(d/'count_protocol.py')and forest['kernel_sha256']==accepted['kernel_sha256']==m['files'],'exact frozen mathematical evaluator')
    stats=geometry(forest,cfg);need(same(stats,accepted['statistics'])and same(stats,row['statistics']),'independent whole forest geometry and aggregates')
    need(integer(accepted['fresh_leaf_evaluations'])==stats['leaves']and len(set(accepted['negative_controls']))==len(accepted['negative_controls'])==24,'fresh all-leaf native arithmetic replay and controls')
    for action in ['construct','accept']:
        run=row['runs'][action];cap=R/run['path'];z=load(cap/'EXECUTION.json',False);need(sha(cap/'EXECUTION.json')==run['execution_sha256'],'count execution identity')
        need(integer(z['returncode'])==0 and z['timed_out']is False and z['interrupted']is False and z['action']==action and z['n']==15 and z['index']==index and z['band']==band,'successful selected native count action')
        for stream in ['stdout','stderr']:bind(cap/(stream+'.txt'),z[stream+'_sha256'])
        need(not(cap/'stderr.txt').read_bytes()and '-B'in z['command'],'ordinary exact count replay')
        if action=='accept':need(same(read(cap/'stdout.txt'),accepted),'whole captured acceptance equality')
    # Alter only disposable in-memory copies. Every control must reject.
    for label,mut in [('missing count',lambda z:z['roots'].pop()),('duplicate count',lambda z:z['roots'].__setitem__(1,deepcopy(z['roots'][0]))),('reordered counts',lambda z:z['roots'].reverse()),('boolean n',lambda z:z.update(n=True)),('inflated target',lambda z:z.update(target='1'))]:
        bad=deepcopy(forest);mut(bad);reject(lambda:geometry(bad,cfg),'forest '+label)
    leaf=next(node for node in flatten(forest)if node['kind']=='leaf')
    bad=deepcopy(forest);next(node for node in flatten(bad)if node['kind']=='leaf')['box'][0][0]='0';reject(lambda:geometry(bad,cfg),'forest changed leaf box')
    return stats
def flatten(f):
    todo=[x['tree']for x in f['roots']]
    while todo:
        x=todo.pop();yield x
        if x['kind']=='split':todo.extend([x['left'],x['right']])

def resource_counts(band,c):
    d=N/f'analytic/resource15_refreshed_v1/{band}';cp=d/'CANDIDATE.json';ap=d/'ACCEPTED.json'
    if missing(cp,f'{band} complete100 resource candidate')or missing(ap,f'{band} full resource replay'):return
    a,z=load(ap),load(cp)
    need(z['status']=='COMPLETE_CONDITIONAL_ACTUAL15_REFRESHED_RESOURCE_INVENTORY'and a['status']=='PASS_FRESH_FULL_CONDITIONAL_ACTUAL15_REFRESHED_RESOURCE_REPLAY','complete refreshed resource status')
    need(a['candidate_sha256']==sha(cp)and a['n']==z['n']==15 and type(a['n'])is type(z['n'])is int and a['band']==z['band']==band,'literal resource identity')
    need(same(a['rows'],z['rows'])and same(a['status_counts'],z['status_counts'])and same(a['files_sha256'],z['files_sha256']),'full resource replay inventory')
    need(len(z['rows'])==len(a['timings_seconds'])==100 and a['negative_controls']==dict(malformed_inventories=12,parser_controls=2),'all100 resource native controls')
    need(z['initial_candidate_sha256']==sha(N/f'analytic/initial15_compensated_v1/{band}_RESULT.json')and z['initial_acceptance_sha256']==sha(N/f'analytic/initial15_compensated_replay_v1/{band}_REPLAY_CHECKED.json'),'selected INITIAL edge')
    for obj in [a,z]:
        for key in ['predecessor_verified','owncap_verified','global_bound_proved','cutoff15_proved']:need(obj[key]is False,'native conditional scope retained')
    for action in ['construct','accept']:capture(R/f'runs/cutoff15_20261017/analytic/resource15_refreshed_{band}_{action}01')
    freeze=N/f'analytic/count15_v1/{band}/FROZEN.json'
    frozen=None if missing(freeze,f'{band} original count family')else load(freeze)
    if frozen:
        need(frozen['parent_candidate_sha256']==sha(cp)and frozen['parent_acceptance_sha256']==sha(ap)and frozen['n']==15 and frozen['band']==band,'count family selected resource edge')
        need(len(frozen['dispositions'])==100,'all original count dispositions')
        countdescs={r['index']:r for r in frozen['rows']};need(len(countdescs)==len(frozen['rows']),'unique count panels')
    statuses=Counter();closed=0;acquired=[];foreststats=[];dispositions=[]
    for i,desc in enumerate(z['rows']):
        need(integer(desc['n'])==15 and integer(desc['index'])==i and desc['band']==band and desc['p']==[str(F(i,100)),str(F(i+1,100))]and desc['path']==f'rows/{i:03d}.json','canonical100 closed p panels')
        p=d/desc['path'];bind(p,desc['sha256']);row=read(p);need(row['status']==desc['status']and row['n']==15 and row['band']==band and row['index']==i,'full row descriptor')
        src=deepcopy(c['export']['panels'][i]);src['rho_lo']=BANDS[band][0];need(same(src,row['source']),'same complete original INITIAL panel')
        status=row['status'];statuses[status]+=1
        if status=='EXCLUDED_BY_SAME_LAW_RESOURCE':
            need(row['result']['excluded']is True,'necessary-condition exclusion');closed+=1
        elif status=='RESOURCE_ROW_ACQUIRED_FOR_COUNT':
            acquired.append(i);need(row['result']['excluded']is False,'genuine acquired count row')
            if frozen and i in countdescs:
                desc2=countdescs[i];dc=N/f'analytic/count15_v1/{band}/capsule{i}';contract=load(dc/'contract.json',False)
                need(len(contract['rows'])==1 and contract['resource_candidate_sha256']==sha(cp)and contract['resource_replay_sha256']==sha(ap)and contract['resource_row_sha256']==sha(p),'literal resource/count row edge')
                cfg=contract['rows'][0];interface(row,cfg,band,i)
                bad=deepcopy(cfg);bad['Lambda']=str(F(cfg['Lambda'])/2);bad['acquired_lambda_upper']=bad['Lambda'];reject(lambda:interface(row,bad,band,i),'replacing original Lambda')
                bad=deepcopy(cfg);bad['acquired_lambda_upper']='0';reject(lambda:interface(row,bad,band,i),'unsupported extra noise cap')
                stats=count_receipt(band,i,desc2,cfg)
                if stats is not None:closed+=1;foreststats.append(dict(index=i,**stats))
            else:pending.append(dict(edge=f'{band} p{i} acquired row needs count',path=str(p.relative_to(R)),status='NO_PREPARED_COUNT_CONTRACT'))
        else:
            need(status=='RESOURCE_CRITERION_FAILED_NO_EXCLUSION','known unresolved resource disposition')
            pending.append(dict(edge=f'{band} p{i}',path=str(p.relative_to(R)),status=status))
        dispositions.append(dict(index=i,p=desc['p'],resource_status=status))
    need(dict(statuses)==z['status_counts'],'independent resource accounting')
    if frozen:
        for i,dd in enumerate(frozen['dispositions']):need(integer(dd['index'])==i,'count disposition order')
        need(set(countdescs)<=set(acquired),'no invented count panels')
    summary[band]=dict(original_panels=100,resource_statuses=dict(statuses),acquired_count_panels=acquired,closed_panels=closed,forest_statistics=foreststats,dispositions=dispositions,all100_closed=closed==100)

def fourier(name,kind):
    rb=N/f'fourier/{name}_readback_v1/READBACK.json'
    if missing(rb,name+' complete Fourier readback'):return
    receipt=load(rb);native=N/f'fourier/{name}_v1';run=R/f'runs/cutoff15_20261017/fourier/{name}_v1'
    manifest=load(native/'MANIFEST.json');plan=load(run/'plan01/PLAN.json',False)
    c=load(run/'construct01/RESULT.json',False);a=load(run/'replay01/RESULT.json',False)
    need(same(untimed(c),untimed(a)),'whole Fourier construction/replay identity '+name)
    for act in ['construct','replay']:
        meta=capture(run/(act+'01'));need(meta.get('RESULT.json_sha256')==sha(run/(act+'01')/'RESULT.json'),'captured Fourier result')
    need(c['plan_sha256']==sha(run/'plan01/PLAN.json')and c['manifest_sha256']==sha(native/'MANIFEST.json'),'Fourier input identities')
    need(same(c['n'],list(range(14,20))),'all six literal indices')
    if kind=='supported':
        bands=[('B0',F(1),F(11,10),F(417,1000)),('BN',F(11,10),F(23,20),F(827,2000)),('BH',F(23,20),F(33,25),F(4097,10000))]
        need(c['support_absolute_upper']=='3'and plan['support_absolute_upper']=='3','explicit radius3 Fourier premise')
        need(c['status']=='EXACT_SUPPORTED_SAME_LAW14_19_WHOLE_B0_BN_BH_PASS','supported complete pass')
        strips=[]
        need(len(plan['bands'])==3,'all three bands')
        for b,(label,lo,hi,target)in zip(plan['bands'],bands):
            need(b['name']==label and b['rho']==[str(lo),str(hi)]and b['target']==str(target),'literal supported band')
            cursor=lo
            for i,p in enumerate(b['strips']):
                l,u=map(rational,p['rho']);need(l==cursor<u<=hi,'complete closed Fourier rho seam');cursor=u;strips.append((label,i,p,target))
            need(cursor==hi,'complete supported right endpoint')
    else:
        start=F(1)if kind=='auxiliary'else F(33,25);target=F(21,50)if kind=='auxiliary'else F(4097,10000)
        need(plan['rho']==[str(start),'19/10']and plan['target']==str(target)and c['target']==str(target),'literal unconditional Fourier scope')
        strips=[];cursor=start
        for i,p in enumerate(plan['strips']):
            l,u=map(rational,p['rho']);need(l==cursor<u<=F(19,10),'complete closed unconditional seams');cursor=u;strips.append((None,i,p,target))
        need(cursor==F(19,10),'full unconditional finite endpoint')
        tail=F(208,625)*(1+F(429,1000)/F(19,10));need(F(c['published_tail']['upper'])==tail<target,'exact published tail')
    need(len(c['rows'])==6*len(strips),'six rows for every closed strip')
    maxima={}
    for pos,(band,i,p,target)in enumerate(strips):
        lo,hi=map(F,p['rho'])
        for n,row in zip(range(14,20),c['rows'][6*pos:6*pos+6]):
            need(integer(row['n'])==n and integer(row['strip_index'])==i and row['rho']==p['rho'],'literal whole strip row')
            if band:need(row['band']==band and row['support_absolute_upper']=='3','same supported row')
            need(row['target']==str(target)and row['strict_target_pass']is True and row['epsilon']=='1/1024'and row['kappa']=='62/625','fixed Fourier target/profile/endpoints')
            need(set(row['terms'])=={'low','normal','high','tail'}and all(rational(v)>=0 for v in row['terms'].values()),'four entire nonnegative Prawitz terms')
            exact=sqrthi(F(n))*sum(map(F,row['terms'].values()))/lo
            need(F(row['normalized_upper'])==exact<target,'independent actual-n normalization and strict score')
            eta,zeta=F(row['eta_upper']),F(row['zeta_lower']);need(0<zeta and zeta*zeta+hi*zeta<=2,'universal sine circle root')
            if kind=='supported':need(0<eta<=1 and eta*eta+lo*eta>=2 and 9<=lo*lo+8,'same-law supported eta root')
            else:need(eta==1,'unconditional eta')
            key=(band,str(n));maxima[key]=max(maxima.get(key,F(0)),exact)
    if kind=='supported':
        for (band,n),v in maxima.items():need(F(c['per_band_per_n_upper'][band][n])==v,'exact supported maximum')
    else:
        for (_,n),v in maxima.items():need(F(c['per_n_upper'][n])==max(v,tail),'exact universal maximum')
    # Independent structural parser controls are scoped to this routine's
    # simple coverage checker; the receipt separately records native mutations.
    for bad in ['{"a":1,"a":2}','{"a":NaN}']:
        reject(lambda:json.loads(bad,object_pairs_hook=unique,parse_constant=invalid),'Fourier ambiguous JSON')
    summary[name]=dict(execution='fresh complete native integration/replay plus independent row/coverage/readback',rows=len(c['rows']),strips=len(strips),support_premise='3'if kind=='supported'else None,all_targets_strict=True)

def main():
    need(__debug__ and sys.flags.dont_write_bytecode and not sys.flags.optimize and len(sys.argv)==2,'ordinary -B and new snapshot basename')
    name=sys.argv[1];need(Path(name).name==name and name.endswith('.json')and not(H/name).exists(),'new local snapshot')
    for p in [Path(__file__),H/'PROOF.txt']:bind(p)
    support();high()
    for band in BANDS:
        c=initial(band);resource_counts(band,c)
    for name,kind in [('auxiliary14_19','auxiliary'),('supported14_19','supported'),('highrho14_19','high')]:fourier(name,kind)
    # Coverage can close only when every required edge has finished, never from
    # a status label or a missing input interpreted as an empty panel.
    closed=not pending and all(summary.get(b,{}).get('all100_closed',False)for b in BANDS)
    out=dict(status='PASS_CONDITIONAL_ACTUAL15_SELECTED_CHAIN_READBACK'if closed else'PASS_AVAILABLE_ACTUAL15_SELECTED_CHAIN_WITH_PENDING_EDGES',conditional_actual15_closed=closed,retained_analytic_A=True,global_bound_proved=False,cutoff15_proved=False,math_status='Conditional implication under retained unrestricted contact/attainment, physical-gap resource reduction and named Fourier analytic inputs; see PROOF.txt.',execution_status='Independent exact receipt, coverage, outward interface and closed-forest geometry checks; native full replays supply Fourier/leaf arithmetic.',pending=pending,summary=summary,negative_controls=dict(controls),native_score_evaluator_calls=0,Fourier_integrations=0,files_sha256=G)
    for path,digest in G.items():need(sha(R/path)==digest,'all selected sources unchanged')
    with(H/sys.argv[1]).open('x')as f:json.dump(out,f,indent=2);f.write('\n')
    print(out['status'],'PENDING',len(pending),'FILES',len(G),sha(H/sys.argv[1]))
if __name__=='__main__':main()
