"""Closed count-tree construction and strict fresh leaf replay.
All conclusions are conditional on contract.json until exact acquisition is
separately composed. Original boxes are replayed before any inner contraction.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,sys,time
from joint_filter import cell35
from optimized_arithmetic import CE_LO
HERE=Path(__file__).resolve().parent
EMPTY={'EMPTY_JOINT_INWARD_MOMENT','EMPTY_ACQUIRED_INWARD_NOISE','EMPTY_PHASE','EMPTY_NEGATIVE_BUDGET','EMPTY_PHASE_RESOURCE','EMPTY_SUPPORT_VARIANCE','EMPTY_SHARP_BOX','EMPTY_SHARP_GAP','EMPTY_RHO_BRANCH','EMPTY_RHO_UPPER','EMPTY_VARIANCE_IDENTITY','EMPTY_JOINT_CUBICS','EMPTY_ACQUIRED_RHO_VARIANCE','EMPTY_ACQUIRED_BETA_VARIANCE','EMPTY_ACQUIRED_BETA','EMPTY_ACQUIRED_MEAN','EMPTY_ACQUIRED_ALPHA'}
LIMIT=10000
CONTRACT_SHA='4f1627bad19c93fca6ee95700c578217fc4fa2df88441fe81faaa651681dfd4f'
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(p):return sha256(p.read_bytes()).hexdigest()
def enc(x):
 if type(x)is F:return str(x)
 if isinstance(x,dict):return{k:enc(v)for k,v in x.items()}
 if isinstance(x,(list,tuple)):return[enc(v)for v in x]
 return x
def same(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
 return a==b
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def load():
 manifest=json.loads((HERE/'KERNEL_COPY_MANIFEST.json').read_text(),object_pairs_hook=unique)
 bound={n:sha(HERE/n)for n in manifest['files']};need(bound==manifest['files'],'frozen exact kernel')
 need(sha(HERE/'contract.json')==CONTRACT_SHA,'fixed acquired contract')
 contract=json.loads((HERE/'contract.json').read_text(),object_pairs_hook=unique)
 need(len(contract['rows'])==1,'one fixed conditional panel')
 cfg=contract['rows'][0]
 need(type(cfg['n'])is int and cfg['n']==6 and type(cfg['index'])is int and cfg['index']==61,'fixed actual6 B0 gamma sharp panel61')
 need(cfg['K']=='0'and cfg['p']==['61/100', '31/50'],'literal target/p domain')
 need(F(cfg['rho_lower'])==F('1') and F(cfg['rho_upper'])==F('273539/250000'),'literal low-rho branch')
 return cfg,bound
def rootbox(cfg):return[[F(x)for x in cfg['p']],[F(0),F(cfg['Lambda'])],[F(0),F(1)],[-F(1,2),F(1,2)],[F(0),F(cfg['d0'])]]
def children(box,axis,cut):
 need(type(axis)is int and 0<=axis<5,'literal split coordinate')
 need(type(cut)is F and box[axis][0]<cut<box[axis][1],'strict interior rational cut')
 a,b=deepcopy(box),deepcopy(box);a[axis][1]=cut;b[axis][0]=cut;return a,b
def evaluate(cfg,k,b):
 z=cell35(cfg,pl=b[0][0],pu=b[0][1],lo=b[1][0],hi=b[1][1],al=b[2][0],ah=b[2][1],k=k,ul=b[3][0],uh=b[3][1],a0l=b[4][0],a0h=b[4][1])
 status=z.get('status')
 if status in EMPTY:return status,enc(z)
 need(status in('PASS','UNRESOLVED'),'named retained kernel result')
 if z.get('score_upper')is not None and F(z['score_upper'])<CE_LO:return'PASS_TARGET',enc(z)
 return None,enc(z)
def header(bound):return dict(schema='ACTUAL6_GAMMA_SHARP_B0_P61_FRESH_COMPENSATED_RESOURCE_JOINT_CLOSED_COUNT_FOREST_V1',n=6,index=61,target=str(CE_LO),contract_sha256=sha(HERE/'contract.json'),kernel_sha256=bound,checker_sha256=sha(Path(__file__)))
def construct():
 cfg,bound=load();began=time.time();visited=0;scales=[F('.001'),F('.006'),F('.15'),F('.02'),F(1)]
 def build(k,b,depth):
  nonlocal visited
  visited+=1;need(visited<=LIMIT and depth<=128 and time.time()-began<=300,'finite count construction budget')
  decision,z=evaluate(cfg,k,b)
  if decision is not None:return dict(kind='leaf',box=enc(b),decision=decision,result=z)
  widths=[(b[i][1]-b[i][0])/scales[i]for i in range(5)];widths[2]*=max(b[1][1]/F(cfg['Lambda']),F(1,10000))
  axis=max(range(5),key=lambda i:widths[i]);mid=sum(b[axis])/2;a,c=children(b,axis,mid)
  return dict(kind='split',axis=axis,cut=str(mid),left=build(k,a,depth+1),right=build(k,c,depth+1))
 roots=[dict(k=k,tree=build(k,rootbox(cfg),0))for k in range(7)]
 need(load()[1]==bound,'unchanged count runtime')
 result=dict(**header(bound),roots=roots);dest=HERE/'COUNT_FOREST.json';need(not dest.exists(),'fresh construction only')
 dest.write_text(json.dumps(result,indent=2)+'\n');print('COUNT_CONSTRUCTED',visited,time.time()-began,flush=True)

def replay(candidate,cfg,bound,cache):
 need(type(candidate)is dict and set(candidate)==set(header(bound))|{'roots'},'exact forest schema')
 for key,value in header(bound).items():need(same(candidate[key],value),'fixed forest '+key)
 roots=candidate['roots'];need(type(roots)is list and len(roots)==7,'all nearest counts0 through6')
 visited=leaves=0;statuses=Counter();maximum=F(0);depthmax=0
 def walk(node,k,b,depth):
  nonlocal visited,leaves,maximum,depthmax
  visited+=1;depthmax=max(depthmax,depth);need(visited<=LIMIT and depth<=128,'finite stored tree bounds')
  need(type(node)is dict and node.get('kind')in('leaf','split'),'named closed-tree node')
  if node['kind']=='split':
   need(set(node)=={'kind','axis','cut','left','right'},'complete binary split')
   need(type(node['cut'])is str,'exact rational cut text');a,c=children(b,node['axis'],F(node['cut']))
   walk(node['left'],k,a,depth+1);walk(node['right'],k,c,depth+1);return
  need(set(node)=={'kind','box','decision','result'},'exact leaf schema')
  need(same(node['box'],enc(b)),'original closed leaf box reconstructed from root')
  key=(k,tuple(x for pair in b for x in pair))
  if key not in cache:cache[key]=evaluate(cfg,k,b)
  decision,z=cache[key];need(decision is not None,'fresh leaf must close')
  need(node['decision']==decision and same(node['result'],z),'complete fresh leaf result equality')
  leaves+=1;statuses[decision]+=1
  if decision=='PASS_TARGET':maximum=max(maximum,F(z['score_upper']))
 for k,root in enumerate(roots):
  need(type(root)is dict and set(root)=={'k','tree'}and type(root['k'])is int and root['k']==k,'ordered complete nearest-count roots')
  walk(root['tree'],k,rootbox(cfg),0)
 return dict(nodes=visited,leaves=leaves,closed_statuses=dict(statuses),maximum_score=str(maximum),maximum_depth=depthmax)

def first(candidate,kind):
 stack=[r['tree']for r in candidate['roots']]
 while stack:
  node=stack.pop(0)
  if node['kind']==kind:return node
  if node['kind']=='split':stack[0:0]=[node['left'],node['right']]
 # All original roots can close without subdivision. For negative controls
 # only, install a synthetic split in this disposable mutated candidate.
 # Each caller immediately corrupts a split field; replay must reject before
 # it reaches either deliberately unchanged wide-box leaf.
 need(kind=='split','required leaf mutation fixture absent')
 root=candidate['roots'][0];leaf=root['tree'];need(leaf['kind']=='leaf','leaf-only fixture')
 cut=str(sum(map(F,leaf['box'][0]))/2)
 root['tree']=dict(kind='split',axis=0,cut=cut,left=deepcopy(leaf),right=deepcopy(leaf))
 return root['tree']
def accept():
 cfg,bound=load();path=HERE/'COUNT_FOREST.json';candidate=json.loads(path.read_text(),object_pairs_hook=unique)
 began=time.time();cache={};stats=replay(candidate,cfg,bound,cache)
 mutations=[('wrong n',lambda x:x.update(n=27)),('boolean n',lambda x:x.update(n=True)),('wrong index',lambda x:x.update(index=99)),('boolean index',lambda x:x.update(index=True)),('wrong target',lambda x:x.update(target='1')),('wrong contract',lambda x:x.update(contract_sha256='0'*64)),('missing kernel source',lambda x:x['kernel_sha256'].pop(next(iter(x['kernel_sha256'])))),('wrong checker',lambda x:x.update(checker_sha256='0'*64)),('missing count',lambda x:x['roots'].pop()),('reordered counts',lambda x:x['roots'].reverse()),('wrong count',lambda x:x['roots'][0].update(k=1)),('boolean count',lambda x:x['roots'][0].update(k=False)),('missing child',lambda x:first(x,'split').pop('left')),('invalid axis',lambda x:first(x,'split').update(axis=5)),('boolean axis',lambda x:first(x,'split').update(axis=True)),('outside cut',lambda x:first(x,'split').update(cut='100')),('nontext cut',lambda x:first(x,'split').update(cut=0)),('changed leaf box',lambda x:first(x,'leaf')['box'][0].__setitem__(0,'0')),('false decision',lambda x:first(x,'leaf').update(decision='EMPTY_FAKE')),('false leaf arithmetic',lambda x:first(x,'leaf')['result'].update(score_upper='0')),('missing result',lambda x:first(x,'leaf').pop('result')),('unknown node',lambda x:first(x,'leaf').update(kind='shortcut')),('extra success claim',lambda x:x.update(success=True)),('extra leaf claim',lambda x:first(x,'leaf').update(accepted=True))]
 controls=[]
 for name,mutation in mutations:
  bad=deepcopy(candidate);mutation(bad)
  try:replay(bad,cfg,bound,cache)
  except(ValueError,KeyError,TypeError,ZeroDivisionError)as error:
   expected={'missing child':'complete binary split','invalid axis':'literal split coordinate','boolean axis':'literal split coordinate','outside cut':'strict interior rational cut','nontext cut':'exact rational cut text'}
   if name in expected:need(type(error)is ValueError and str(error)==expected[name],'split control must reject before synthetic children')
   controls.append(name)
  else:raise ValueError('negative control passed: '+name)
 need(load()[1]==bound,'unchanged kernel after fresh replay')
 out=dict(status='PASS_FRESH_CONDITIONAL_ACTUAL6_GAMMA_SHARP_B0_JOINT_PANEL61',n=6,index=61,forest_sha256=sha(path),contract_sha256=sha(HERE/'contract.json'),checker_sha256=sha(Path(__file__)),kernel_sha256=bound,statistics=stats,negative_controls=controls,fresh_leaf_evaluations=stats['leaves'],seconds=time.time()-began,scope='Conditional fixed count proof only. Exact same-law resource acquisition and parent proof composition remain separate obligations. Every original root box and leaf is reconstructed; rho/beta/alpha contractions are recomputed by the frozen wrapper.')
 dest=HERE/'COUNT_ACCEPTED.json';need(not dest.exists(),'fresh acceptance only');dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':
 need(__debug__ and not sys.flags.optimize and len(sys.argv)==2 and sys.argv[1]in('construct','accept'),'fixed exact action')
 (construct if sys.argv[1]=='construct'else accept)()
