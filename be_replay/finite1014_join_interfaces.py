"""Pure typed resource/config metadata comparisons for current56I.

The four directed-rounding/interface functions below retain the complete ASTs
of the original selected join. This module never imports the original source
or evaluates a resource/count/Fourier kernel. Fresh arithmetic comes from the
separately validated complete upstream exports.
"""
from fractions import Fraction as F
from pathlib import Path
import ast
from .finite1014_join_sources import need,digest,ROOT
from .finite1014_join_epoch import same
BANDS={'B0':('1','11/10','1047/2500','99/1000','23/10','69/200'),
       'BN':('11/10','23/20','519/1250','63/1000','12/5','93/250')}
REFERENCE_SHA='d36ae540058d64a8d9b83fe19a92d8adcb7812c6576e0d1778fc31af2b7e8b2a'


def verify_reference_projection():
    path=ROOT/'vendor/finite1014_join_reference_v1/common.py'
    need(digest(path)==REFERENCE_SHA,'Exact original finite10--14 interface source')
    def selected(text):
        out={}
        for n in ast.parse(text).body:
            if isinstance(n,ast.FunctionDef)and n.name in{'floorgrid','ceilgrid','polymin','interface'}:out[n.name]=ast.dump(n,include_attributes=False)
            if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='BANDS'for t in n.targets):
                need('BANDS'not in out,'Unique original/current band assignment');out['BANDS']=ast.dump(n,include_attributes=False)
        need(set(out)=={'BANDS','floorgrid','ceilgrid','polymin','interface'},'Complete literal-band and interface projection')
        return out
    need(selected(path.read_text('utf-8'))==selected(Path(__file__).read_text('utf-8')),'Complete original directed-rounding/whole-interface function ASTs retained')
    return REFERENCE_SHA


def floorgrid(x,grid):x=F(x);return F(x.numerator*grid//x.denominator,grid)

def ceilgrid(x,grid):return-floorgrid(-F(x),grid)

def polymin(a,b,c,upper):
    vals=[a,a+b*upper+c*upper*upper]
    if c>0 and 0<-b/(2*c)<upper:vals.append(a-b*b/(4*c))
    return min(vals)

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
