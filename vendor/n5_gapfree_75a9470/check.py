"""Independent rational Gaussian and complete sign-count forest evaluation."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt,comb
from hashlib import sha256
from functools import lru_cache
from copy import deepcopy
import json,sys
H=Path(__file__).resolve().parent;R=H.parents[3];V=H.parent.parent
K=V/'root/gapfree5_exact_v1';GRAPH={}
RL,RH=F(477,400),F(6,5);BL,BH=F(17,50),F(35139006743001,10**14);TARGET=F(4097,10000)
def need(v,s):
    if not v:raise ValueError(s)
def digest(p):return sha256(p.read_bytes()).hexdigest()
def bind(p):GRAPH[str(p.relative_to(R))]=digest(p);return p
def unique(pairs):
    d={}
    for k,v in pairs:need(k not in d,'duplicate JSON field');d[k]=v
    return d
def read(p):return json.loads(bind(p).read_text(),object_pairs_hook=unique)
def graph(g):
    need(type(g)is dict and g,'nonempty graph')
    for p,h in g.items():need(digest(R/p)==h,'source changed '+p);bind(R/p)
def receipt(p,status):
    z=read(p);need(z['status']==status,'exact acquisition');graph(z['files_sha256']);return z
def root(x,d=60):
    need(x>=0,'square root domain');g=10**d;a=F(isqrt(x.numerator*g*g//x.denominator),g)
    b=a+F(1,g);need(a*a<=x<b*b,'integer square root enclosure');return a,b
def atan_bounds(q,n):
    need(n%2==0 and q>1,'even alternating arctangent')
    s=sum((F((-1)**k,(2*k+1)*q**(2*k+1))for k in range(n)),F(0))
    return s,s+F(1,(2*n+1)*q**(2*n+1))
a,b=atan_bounds(5,100);c,d=atan_bounds(239,40)
PILO,PIHI=16*a-4*d,16*b-4*c
PHILO=root(1/(2*PIHI),100)[0];PHIHI=root(1/(2*PILO),100)[1]
S5=root(F(5))[1]
need((3+root(F(10))[0])*PHILO/6>TARGET,'sharp constant strict lower')
expterm=F(1);expsum=expterm
for j in range(1,101):expterm*=F(25,2*j);expsum+=expterm
need(PHIHI/(5*expsum)<F(3,10**7),'Mills tail at five')
@lru_cache(None)
def gaussian_grid(t):
    need(type(t)is int,'Gaussian integer grid')
    if t<=-5*10**10:return F(0)
    if t>=5*10**10:return 1-F(3,10**7)
    x=F(abs(t),10**10);term=x;total=F(0)
    # Exact integrated Taylor polynomial; no term-by-term interval rounding.
    for k in range(100):
        total+=(-1)**k*term
        term*=x*x*F(2*k+1,2*(k+1)*(2*k+3))
    lo=max(F(0),total-term);hi=total+term
    need(0<=lo<=hi,'integrated Taylor enclosure')
    return F(1,2)+PHILO*lo if t>=0 else F(1,2)-PHIHI*hi
@lru_cache(None)
def leaf(beta,box):
    bl,bu=beta;l,u,a,b=box
    need(BL<=bl<bu<=BH and 0<l<u<F(1,2) and 0<=a<b<=5,'whole closed leaf domain')
    ml=(1+bl*bl)/(2*RH)
    v0=max(F(0),u*u*((1-l)*(1-bl)/(2*ml*ml)-1))
    v1=max(F(0),(1-l)**2*(u*(1+bu)/(2*ml*ml)-1))
    cdf=F(0)
    for j in range(6):
        p=min(u,max(l,F(j,5)));weight=comb(5,j)*p**j*(1-p)**(5-j)
        variance=(5-j)*v0+j*v1;distance=j-b
        factor=F(1) if distance<=0 else variance/(variance+distance*distance)
        cdf+=weight*factor
    cdf=min(F(1),cdf);nu=a-5*u
    x=nu*ml/(S5*u*(1-u)) if nu>=0 else nu/root(5*u*(1-u))[0]
    t=x.numerator*10**10//x.denominator
    score=S5/RL*max(F(0),cdf-gaussian_grid(t))
    return F(-((-score.numerator*10**12)//score.denominator),10**12)
def expected_roots():
    e=[BL]+[F(k,1000)for k in range(341,352)]+[BH];out=[]
    need(e==sorted(set(e)),'ordered beta partition')
    for i,(bl,bu)in enumerate(zip(e,e[1:])):
        ml=(1+bl*bl)/(2*RH);pl=2*ml*ml/(1+bu);pu=1-2*ml*ml/(1-bl)
        pl=F(pl.numerator*10**6//pl.denominator,10**6)
        pu=F(-((-pu.numerator*10**6)//pu.denominator),10**6)
        need(0<pl<pu<F(1,2),'outward p domain')
        for j in range(5):out.append(dict(beta_index=i,phase=j,beta=list(map(str,(bl,bu))),p=list(map(str,(pl,pu))),z=[str(j),str(j+1)]))
    return out
def validate(z):
    need(type(z)is dict and set(z)=={'schema','rho','beta','target','roots'},'exact forest schema')
    need(z['schema']=='GAPFREE_SIGN_COUNT5_EXACT_FOREST_V1' and z['rho']==list(map(str,(RL,RH))) and
         z['beta']==list(map(str,(BL,BH))) and z['target']==str(TARGET),'literal scope')
    expected=expected_roots();need(type(z['roots'])is list and len(z['roots'])==60,'sixty complete roots')
    leaves=nodes=0;maximum=F(0);storedmaximum=F(0)
    for entry,domain in zip(z['roots'],expected):
        need(type(entry)is dict and set(entry)=={'domain','tree'},'exact root object')
        d=entry['domain'];need(type(d)is dict and set(d)==set(domain),'exact root domain')
        need(type(d['beta_index'])is int and type(d['phase'])is int and d==domain,'typed ordered root')
        stack=[(entry['tree'],tuple(map(F,d['p']+d['z'])),0)]
        while stack:
            t,box,depth=stack.pop();nodes+=1
            need(nodes<=2000000 and depth<=60 and type(t)is list and t,'bounded node schema')
            if t[0]=='L':
                need(len(t)==2 and type(t[1])is int,'literal integer leaf')
                value=leaf(tuple(map(F,d['beta'])),box);stored=F(t[1],10**12)
                need(value<=stored<TARGET,'independent strict whole-cell score')
                leaves+=1;maximum=max(maximum,value);storedmaximum=max(storedmaximum,stored)
            else:
                need(len(t)==4 and t[0]=='S'and type(t[1])is int and t[1]in(0,1),'literal split axis')
                l,u,a,b=box
                if t[1]==0:m=(l+u)/2;left=(l,m,a,b);right=(m,u,a,b)
                else:m=(a+b)/2;left=(l,u,a,m);right=(l,u,m,b)
                stack.extend([(t[3],right,depth+1),(t[2],left,depth+1)])
    need(nodes==2*leaves-60,'complete binary forest census')
    return dict(roots=60,nodes=nodes,leaves=leaves,independent_upper=str(maximum),stored_upper=str(storedmaximum))
def exterior(e):
    need(type(e['n'])is int and e['n']==5 and e['rho']==list(map(str,(RL,RH))) and e['beta']==list(map(str,(BL,BH))),'exact whole-line exterior scope')
    ml=(1+BL*BL)/(2*RH);pl=2*ml*ml/(1+BH);pu=1-2*ml*ml/(1-BL)
    need(0<pl<pu<F(1,2),'exterior p enclosure')
    vu=pu*(1-pu);su=vu*vu/(ml*ml)-vu;need(su>=0,'variance domain')
    vs=[max(F(j)/pl,F(5-j)/(1-pu))*su for j in range(6)]
    for k,v in [('mL',ml),('pL',pl),('pU',pu),('sU',su)]:need(F(e[k])==v,'independent exterior '+k)
    need(e['conditional_variance_uppers']==list(map(str,vs)),'all same-law conditional variances')
    total=sum((comb(5,j)*pu**j*(1-pl)**(5-j)*(1 if j==0 else vs[j]/(vs[j]+j*j))for j in range(6)),F(0))
    left=S5/RL*total;right=S5/RL/(1+5*ml*ml/(pu*pu))
    need(left<=F(e['left_score_upper'])<F(331,1000)<TARGET and right<=F(e['right_score_upper'])<F(187,1000)<TARGET,'both infinite rays strictly excluded')
    return dict(left_upper=str(F(e['left_score_upper'])),right_upper=str(F(e['right_score_upper'])),left_domain='z<=0',right_domain='z>=5')
def capture(name,cwd,command,last):
    p=R/'runs/cutoff5_20261020'/name;m=read(p/'metadata.json')
    need(type(m['returncode'])is int and m['returncode']==0 and m['cwd']==str(cwd)and m['command'][1:]==command,'fresh exact successful capture')
    for k in('stdout','stderr'):need(digest(p/(k+'.txt'))==m[k+'_sha256'],'capture hash');bind(p/(k+'.txt'))
    need(not(p/'stderr.txt').read_bytes()and(p/'stdout.txt').read_text().splitlines()[-1]==last,'native successful terminal marker')
    for f,h in m['input_sha256'].items():need(digest(cwd/f)==h,'captured input');bind(cwd/f)
def main():
    need(__debug__ and sys.dont_write_bytecode and not sys.flags.optimize,'ordinary -B');dest=H/'READBACK.json';need(not dest.exists(),'fresh epoch')
    native=receipt(K/'REPLAY_CHECKED.json','PASS_FRESH_EXACT_GAPFREE5_COMPACT_REPLAY')
    ext=receipt(V/'high/gap_free_count_review_v2/CHECKED.json','PASS_INDEPENDENT_GAP_FREE_SIGN_COUNT_IDENTITIES_AND_EXTERIORS')
    review=receipt(V/'high/gap_free_kernel_review_v1/CHECKED.json','PASS_INDEPENDENT_GAPFREE5_CONTINUOUS_GAUSSIAN_KERNEL_REVIEW')
    z=read(K/'FOREST.json');result=validate(z);rays=exterior(ext['exterior'])
    need(result['nodes']==native['nodes']==1994 and result['leaves']==native['leaves']==1027 and native['roots']==60,'independent whole-forest census')
    need(native['maximum']==result['stored_upper']and native['rho']==z['rho']and native['beta']==z['beta']and native['target']==z['target'],'same acquired theorem')
    capture('root/gapfree5_replay01',K,['-B','replay.py'],'PASS_FRESH_EXACT_GAPFREE5_COMPACT_REPLAY ROOTS 60 LEAVES 1027 CONTROLS 15')
    controls=[]
    def reject(fun,label):
        try:fun()
        except(ValueError,KeyError,TypeError,IndexError,ZeroDivisionError):controls.append(label)
        else:raise ValueError('mutation accepted '+label)
    def first_leaf(tree):
        while tree[0]=='S':tree=tree[2]
        return tree
    changes=[('missing root',lambda x:x['roots'].pop()),('duplicated root',lambda x:x['roots'].__setitem__(1,deepcopy(x['roots'][0]))),
      ('reordered roots',lambda x:x['roots'].reverse()),('wrong rho',lambda x:x['rho'].__setitem__(0,'1')),('weakened target',lambda x:x.update(target='1/2')),
      ('boolean root index',lambda x:x['roots'][0]['domain'].update(beta_index=False)),('boolean phase',lambda x:x['roots'][0]['domain'].update(phase=False)),
      ('root domain gap',lambda x:x['roots'][0]['domain']['p'].__setitem__(0,'1/3')),('missing tree',lambda x:x['roots'][0].pop('tree')),
      ('false leaf',lambda x:first_leaf(x['roots'][0]['tree']).__setitem__(1,-1)),('boolean leaf',lambda x:first_leaf(x['roots'][0]['tree']).__setitem__(1,True)),
      ('extra forest field',lambda x:x.update(extra=0))]
    split_index=next(i for i,q in enumerate(z['roots'])if q['tree'][0]=='S')
    changes += [('bad split axis',lambda x:x['roots'][split_index]['tree'].__setitem__(1,2)),('boolean split',lambda x:x['roots'][split_index]['tree'].__setitem__(1,True)),('missing child',lambda x:x['roots'][split_index]['tree'].pop())]
    for label,change in changes:
        bad=deepcopy(z);change(bad);reject(lambda:validate(bad),label)
    for key,value in [('beta',['347/1000',str(BH)]),('left_score_upper','0'),('n',True)]:
        bad=deepcopy(ext['exterior']);bad[key]=value;reject(lambda:exterior(bad),'false exterior '+key)
    reject(lambda:json.loads('{"n":5,"n":6}',object_pairs_hook=unique),'duplicate JSON key')
    for f in('check.py','PROOF.txt'):bind(H/f)
    for p,h in GRAPH.items():need(digest(R/p)==h,'unchanged final source graph')
    out=dict(status='PASS_INDEPENDENT_GAPFREE5_WHOLE_LINE_READBACK',n=5,rho=z['rho'],beta=z['beta'],target=str(TARGET),**result,
      exteriors=rays,negative_controls=controls,files_sha256=GRAPH,c5_proved=False,
      mathematical_status='Positive closed CDF normalized score strictly below .4097 for every standardized iid marginal in the stated rho/beta rectangle and every real threshold. No contact, support or C4 premise.',
      execution_status='All1027 compact leaves independently evaluated with exact rational Gaussian polynomial; both full exterior rays independently reconstructed; native proof/source graph bound.')
    with dest.open('x')as f:json.dump(out,f,indent=2);f.write('\n')
    print(out['status'],'ROOTS',result['roots'],'LEAVES',result['leaves'],'CONTROLS',len(controls),flush=True)
if __name__=='__main__':main()
