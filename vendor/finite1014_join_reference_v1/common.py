"""Shared check-only exact parsing/geometry helpers, copied from the independently reviewed actual15 join.
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
BANDS={'B0':('1','11/10','1047/2500','99/1000','23/10','69/200'),
       'BN':('11/10','23/20','519/1250','63/1000','12/5','93/250')}
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


def interface(row,cfg,band,index,n):
    lo,hi,_,_,_,_=BANDS[band];r=row['result']['result'];raw=row['result']['raw_row'];s=row['source']
    need(type(n)is int and 10<=n<=14,'literal sequential count index')
    need(type(r['N'])is int and r['N']==n and type(r['index'])is int and r['index']==index and r['K']=='0','literal resource export index and target')
    need(cfg['n']==n and type(cfg['n'])is int and cfg['K']=='0'and cfg['index']==index and type(cfg['index'])is int,'literal original count target')
    need(cfg['p']==[str(F(index,100)),str(F(index+1,100))]==[r['pl'],r['pu']]==[s['pl'],s['pu']]==[raw['pl'],raw['pu']],'same whole original p panel')
    need(cfg['rho_lower']==lo and F(cfg['rho_upper'])>=F(r['rho_hi'])and F(r['rho_hi'])<=F(hi),'rho band domination')
    need(F(r['D'])-F(r['charge_b'])==F(r['charge_g'])*F(r['d0'])==F(r['charge_h'])*F(r['lambda_max'])>0,'original shared resource identity')
    for a,b in [('D','D'),('d0','d0'),('lambda_max','Lambda'),('H_minus','Hminus'),('H_plus','Hplus'),('radius_minus','radius_minus'),('radius_plus','radius_plus'),('outer0','outer0'),('outer1','outer1')]:need(F(cfg[b])==ceilgrid(r[a],10**6),'exact outward upper '+b)
    for a,b in [('charge_b','binary_charge'),('charge_g','gap_charge'),('charge_h','noise_charge')]:need(F(cfg[b])==floorgrid(r[a],10**6),'exact outward price '+b)
    need(cfg['acquired_lambda_upper']==cfg['Lambda'],'original Lambda retained; redundant cap only')
    need(0<F(cfg['d0'])<F(1,2)and F(cfg['Lambda'])>0 and F(cfg['gap_charge'])>0 and F(cfg['noise_charge'])>0,'positive acquired resource domain')
    need(F(1,4)+F(cfg['Lambda'])/n<1 and n*F(cfg['p'][0])>F(cfg['Hminus'])and n*F(cfg['p'][1])+F(cfg['Hplus'])<n,'all n+1 nearest-count roots')
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


def geometry(f,cfg,n):
    need(type(n)is int and 10<=n<=14,'literal sequential count index')
    need(integer(f['n'])==n and integer(f['index'])==cfg['index'],'literal actual forest')
    target=rational(f['target']);need(F(4097,10000)<target<CElo,'unchanged safe sharp rational target')
    need(type(f['roots'])is list and len(f['roots'])==n+1,'all n+1 roots')
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
    need(nodes==2*leaves-(n+1),'full binary forest identity')
    return dict(nodes=nodes,leaves=leaves,closed_statuses=dict(statuses),maximum_score=str(maximum),maximum_depth=depthmax)

