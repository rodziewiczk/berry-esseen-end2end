"""Independent finite closed-union geometry; no native evaluator is imported."""
from fractions import Fraction as F
from collections import Counter
from copy import deepcopy
import common as c
need=c.need

def partition(cfg,parts):
    """A fixed four-piece exact closed partition of one ORIGINAL p panel."""
    need(type(parts)is list and len(parts)==4,'exactly four selected closed components')
    original=list(map(c.rational,cfg['p']));lo,hi=original
    need(lo<hi,'positive original probability width')
    want=[lo+(hi-lo)*j/4 for j in range(5)]
    for j,part in enumerate(parts):
        need(type(part)is dict and set(part)=={'component','p'},'exact normalized component descriptor')
        need(c.integer(part['component'])==j,'ordered unique component indices')
        need(type(part['p'])is list and len(part['p'])==2,'closed component endpoints')
        a,b=map(c.rational,part['p'])
        need([a,b]==want[j:j+2]and a<b,'complete equal closed original-panel partition')
    need(parts[0]['p'][0]==cfg['p'][0]and parts[-1]['p'][1]==cfg['p'][1],'both original endpoints retained')
    return parts

def geometry(f,cfg,n,part):
    """Only the geometric p root is restricted; the contract stays original."""
    p=list(map(c.rational,part['p']));lo,hi=map(c.rational,cfg['p'])
    need(lo<=p[0]<p[1]<=hi,'component inside ORIGINAL acquired contract')
    local=deepcopy(cfg);local['p']=part['p'][:]
    need(all(c.same(local[k],v)for k,v in cfg.items()if k!='p'),'all original non-p contract data preserved')
    return c.geometry(f,local,n)

def aggregate(n,parts,statistics):
    need(type(n)is int and 10<=n<=14,'literal component forest index')
    need(len(parts)==len(statistics)==4,'all four complete component statistics')
    statuses=Counter();nodes=leaves=0;depth=0;score=F(0)
    component=[]
    for j,st in enumerate(statistics):
        nn,ll,dd=map(c.integer,[st['nodes'],st['leaves'],st['maximum_depth']])
        need(0<nn<=10000 and 0<ll and 0<=dd<=128 and nn==2*ll-(n+1),'each original finite forest bound')
        statuses.update(st['closed_statuses']);nodes+=nn;leaves+=ll;depth=max(depth,dd);score=max(score,c.rational(st['maximum_score']))
        component.append(dict(component=j,p=parts[j]['p'],**st))
    need(nodes==2*leaves-4*(n+1),'finite union aggregate root identity')
    return dict(nodes=nodes,leaves=leaves,closed_statuses=dict(statuses),maximum_score=str(score),maximum_depth=depth,component_forests=4,total_roots=4*(n+1),component_statistics=component)

def controls(cfg):
    lo,hi=map(F,cfg['p']);cuts=[lo+(hi-lo)*j/4 for j in range(5)]
    good=[dict(component=j,p=list(map(str,cuts[j:j+2])))for j in range(4)]
    partition(cfg,good)
    cases=[('missing subpanel',lambda z:z.pop()),('duplicate subpanel',lambda z:z.__setitem__(1,deepcopy(z[0]))),('reordered subpanels',lambda z:z.reverse()),('boolean component',lambda z:z[0].update(component=False)),('gap at subpanel seam',lambda z:z[1]['p'].__setitem__(0,str((cuts[1]+cuts[2])/2))),('overlap at subpanel seam',lambda z:z[1]['p'].__setitem__(0,str((cuts[0]+cuts[1])/2))),('omitted left endpoint',lambda z:z[0]['p'].__setitem__(0,str((cuts[0]+cuts[1])/2))),('omitted right endpoint',lambda z:z[-1]['p'].__setitem__(1,str((cuts[-2]+cuts[-1])/2))),('zero-width component',lambda z:z[0]['p'].__setitem__(1,z[0]['p'][0])),('noncanonical endpoint',lambda z:z[0]['p'].__setitem__(0,'0'+z[0]['p'][0]))]
    for label,mutate in cases:
        bad=deepcopy(good);mutate(bad);c.reject(lambda:partition(cfg,bad),label)
