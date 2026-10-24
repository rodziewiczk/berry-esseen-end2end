"""Pure source-bound resource/contract comparisons for full57H.

The two literal-index interface functions retain the complete original ASTs,
apart from their names. No original mathematical module is imported. Full
numerical evidence must already have been validated before these comparisons.
Copyright (c)2026 Kacper Rodziewicz and Bartosz Kolodziejek; MIT, see reference LICENSE.
"""
from fractions import Fraction as F
from pathlib import Path
import ast
from .finite1519_join_control_sources import need,digest,ROOT
from .finite1014_join_epoch import same
BANDS={'B0':('1','11/10','417/1000','219/2000','23/10','191/500'),
       'BN':('11/10','23/20','827/2000','57/1000','12/5','409/1000')}
REFERENCE_SHA256={'actual15.py': '4dbfc5a885686af60ee118866051d84d32ab2673fbd298ebc23f231985ddb9ac', 'sequential.py': 'a6f2aa278ff7cbe80916c76442f86412dd5a00b44cca9637df0ba2e490c710f6'}

def floorgrid(x,grid):x=F(x);return F(x.numerator*grid//x.denominator,grid)

def ceilgrid(x,grid):return-floorgrid(-F(x),grid)

def polymin(a,b,c,upper):
    vals=[a,a+b*upper+c*upper*upper]
    if c>0 and 0<-b/(2*c)<upper:vals.append(a-b*b/(4*c))
    return min(vals)

def interface_actual15(row,cfg,band,index):
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

def interface_sequential(row,cfg,band,index,n):
    lo,hi,_,_,_,_=BANDS[band];r=row['result']['result'];raw=row['result']['raw_row'];s=row['source']
    need(type(n)is int and 16<=n<=19,'literal sequential count index')
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


def verify_reference_projection():
    root=ROOT/'vendor/finite1519_join_reference_v1'
    own={n.name:n for n in ast.parse(Path(__file__).read_text('utf-8')).body if isinstance(n,ast.FunctionDef)}
    for source,selected in(('actual15.py',{'interface':'interface_actual15'}),
            ('sequential.py',{'floorgrid':'floorgrid','ceilgrid':'ceilgrid','polymin':'polymin','interface':'interface_sequential'})):
        need(digest(root/source)==REFERENCE_SHA256[source],'Pinned complete original literal-index interface source')
        original={n.name:n for n in ast.parse((root/source).read_text('utf-8')).body if isinstance(n,ast.FunctionDef)}
        for old,new in selected.items():
            node=original[old];node.name=new
            need(ast.dump(node,include_attributes=False)==ast.dump(own[new],include_attributes=False),
                 'Every original simultaneous resource/contract condition and directed rounding retained')
    return dict(REFERENCE_SHA256)


def interface(row,cfg,band,index,n):
    need(type(n)is int and 15<=n<=19,'Literal complete finite15--19 interface domain')
    need(type(index)is int and 0<=index<100 and type(band)is str and band in BANDS,'Literal original probability panel and band')
    if n==15:return interface_actual15(row,cfg,band,index)
    return interface_sequential(row,cfg,band,index,n)


def sequential(base,local):
    need(type(base)is bool and type(local)is dict and set(local)=={15,16,17,18,19}
         and all(type(n)is int and type(v)is bool for n,v in local.items()),'Exact consecutive finite15--19 scope')
    current=base;out=[]
    for n in range(15,20):
        previous=current;current=previous and local[n]
        out.append(dict(n=n,global_predecessor=n-1,predecessor_established=previous,
            conditional_local_implication_complete=local[n],conditional_finite_result_established=current))
    return out
