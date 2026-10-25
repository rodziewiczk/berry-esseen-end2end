"""Source-only exact current-receipt epochs for original n26--30 covers."""
from __future__ import annotations
import ast,copy,hashlib,json,re,shutil,time,urllib.request,zipfile
from pathlib import Path
from . import finite1039_sources as base
from .finite1039_count_evidence import same
ROOT,MIB=base.ROOT,base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
PLAN=ROOT/'proof/finite2630_covers_source_plan.json'
PLAN_SHA256='86692f3f8f170e6fe53e578f9c129409028303ef8831684a8b4cfb8eaceef8b9'
SCHEMA='SEALED_ORIGINAL_FINITE2630_COVERS_V1'
PASSES=('construct','replay')
# Exact published source-adapter epochs. Pure completed-export admission may
# request one after validating the complete corresponding implementation map.
# New preparation/execution always requires this file's actual current hash.
PRIOR_SOURCE_ADAPTERS=frozenset({
 '0a03ca05ae2788118ea7c7c55e16d6b37443a222c0e21b9ee14f30fd267d167a',
 '35213d6c838122bdd3df92b9f89c9097ef4c2d4f2f4eb8ef4211372c0b3f380b'})
def dump(d):return(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()
def plan():
 need(digest(PLAN)==PLAN_SHA256,'Externally pinned full original cover selection');d=read(PLAN)
 need(d['schema']=='FINITE2630_ORIGINAL_FOURIER_COVERS_SOURCE_PLAN_V1'and len(d['source_files'])==48 and len(d['active_source_files'])==34
  and d['original_kernels_and_schedules_unchanged']is True and d['only_approved_receipt_hash_literals_may_change']is True
  and d['two_genuine_passes_required']is True,'Exact48 original commitments,34 active sources and two complete native passes')
 need(all(d[k]is False for k in('arithmetic_computed','parent_acquisitions_verified','full_notebook59_completed','all_index_conclusion_verified')),'No parent or global acquisition')
 return d
def lane(name):
 need(type(name)is str and name in('b2','higher'),'One fixed original full-cover lane');return plan()['lanes'][name]
def obtain_assets(directory, *,progress=lambda *a,**k:None):
 a=plan()['asset'];directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);p=ordinary(directory/a['name'])
 if not p.exists():
  pending=p.with_suffix('.zip.pending');total=0;last=time.monotonic();at=0
  progress('finite2630_covers_download_started',archive=a['name'],total_bytes=a['bytes'])
  with urllib.request.urlopen(a['url'])as source,pending.open('wb')as out:
   while b:=source.read(MIB):
    total+=len(b);need(total<=a['bytes'],'Bounded original cover asset');out.write(b)
    if total-at>=16*MIB or time.monotonic()-last>=5:progress('finite2630_covers_download',bytes=total,total_bytes=a['bytes']);at=total;last=time.monotonic()
  need(total==a['bytes']and digest(pending)==a['sha256'],'Exact complete original asset');pending.replace(p)
 need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Actual immutable source-archive bytes')
 progress('finite2630_covers_archive_verified',archive=a['name'],sha256=a['sha256']);return p

def prepare_cache(archive,output, *,progress=lambda *a,**k:None):
 d=plan();a=d['asset'];archive=ordinary(archive);need(archive.stat().st_size==a['bytes']and digest(archive)==a['sha256'],'Original asset transport pin')
 output=ordinary(output);output.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(archive)as z:
  base.zip_index(z)
  for i,(name,row)in enumerate(d['source_files'].items()):
   p=ordinary(output/name)
   if not p.exists():
    info=z.getinfo(row['member']);need(info.file_size==row['bytes'],'Original member size');p.parent.mkdir(parents=True,exist_ok=True)
    with z.open(info)as source,p.open('xb')as target:shutil.copyfileobj(source,target,MIB)
   need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every selected original source/provenance byte')
   if i%10==0:progress('finite2630_covers_source_cache',files=i,total=48,arithmetic_computed=False)
 base.verify_cache(output,d['source_files']);return output.resolve()
def capsule(task,pass_name):
 need(pass_name in PASSES,'One exact complete pass');return Path(task)/'passes'/pass_name/'capsule'
def stage(name):
 need(type(name)is str and name in plan()['stages'],'Fixed original native action');return plan()['stages'][name]
def output_paths(name):
 r=stage(name);return[r['directory']+'/'+n for n in r['outputs']]
def prepare(name,cache,task):
 profile=lane(name);d=plan();task=ordinary(task);need(not task.exists(),'Fresh isolated two-pass cover task');task.mkdir(parents=True)
 for key,row in d['source_files'].items():
  p=ordinary(Path(cache)/key);need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Original raw source/provenance input')
  target=task/'provenance'/key;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
 for pass_name in PASSES:
  c=capsule(task,pass_name)
  for key in d['active_source_files']:
   target=c/key;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(task/'provenance'/key,target)
  (c.parent/'PORTS.json').write_bytes(dump(dict(schema='EXPLICIT_ORIGINAL_RECEIPT_HASH_PORTS_V1',lane=name,pass_name=pass_name,entries=[])))
 request=dict(schema=SCHEMA,lane=name,original_task_root=str(task.resolve()),source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),
  sources={n:r['sha256']for n,r in d['source_files'].items()},active_original_sources={n:r['sha256']for n,r in d['active_source_files'].items()},
  historical_outputs_are_provenance_only=True,arithmetic_computed=False,parent_acquisitions_verified=False,full_notebook59_completed=False,all_index_conclusion_verified=False)
 (task/'SOURCES.json').write_bytes(dump(request));verify(task);return request

def node_at(tree,path):
 node=tree
 for field in path:node=node[field]if type(field)is int else getattr(node,field)
 return node

def frozen_ast_dump(node):
 """Preserve the sealed Python3.12 AST spelling, including empty list fields.

 Python3.13 ast.dump omits empty optional lists by default. These frozen
 descriptors intentionally bind the full3.12 field spelling. Format actual
 AST fields directly; never evaluate or parse a descriptor as Python code.
 Optional None fields follow the original3.12 ast.dump rule.
 """
 need(isinstance(node,ast.AST),'An actual parsed AST node is required')
 def format_value(value):
  if isinstance(value,ast.AST):
   fields=[]
   for name in value._fields:
    if not hasattr(value,name):continue
    child=getattr(value,name)
    if child is None and getattr(type(value),name,...)is None:continue
    fields.append(name+'='+format_value(child))
   return type(value).__name__+'('+', '.join(fields)+')'
  if isinstance(value,list):return'['+', '.join(format_value(v)for v in value)+']'
  return repr(value)
 return format_value(node)

def derive_source(original,row,dependencies):
 need(type(original)is bytes and hashlib.sha256(original).hexdigest()==row['script_sha256'],'Exact original native control/wrapper source')
 ports=row['receipt_ports'];need(type(dependencies)is dict and set(dependencies)=={p['dependency']for p in ports},'Exactly the preceding genuine receipt inputs')
 tree=ast.parse(original.decode('utf-8'));edits=[];paths=[];evidence=[];lines=original.splitlines(keepends=True)
 for spec in ports:
  node=node_at(tree,spec['constant_ast_path']);old=spec['original_sha256'];new=dependencies[spec['dependency']]
  need(type(new)is str and re.fullmatch('[0-9a-f]{64}',new)and isinstance(node,ast.Constant)and type(node.value)is str and node.value==old,'Exact approved source-check constant position/value')
  need(sum(isinstance(n,ast.Constant)and n.value==old for n in ast.walk(tree))==1,'No duplicate original checksum constant')
  assignment=spec['assignment']
  if assignment is not None:
   assignments=[n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==assignment for t in n.targets)]
   need(len(assignments)==1 and len(assignments[0].targets)==1 and any(n is node for n in ast.walk(assignments[0])),'Unique exact top-level configuration assignment')
   if spec['key_ast']is not None:
    value=assignments[0].value;need(isinstance(value,ast.Dict),'Literal source-pin dictionary')
    keys=[k for k,v in zip(value.keys,value.values)if v is node];need(len(keys)==1 and frozen_ast_dump(keys[0])==spec['key_ast'],'Exact original dictionary key position')
  else:
   comparisons=[n for n in ast.walk(tree)if isinstance(n,ast.Compare)and any(v is node for v in n.comparators)]
   need(len(comparisons)==1 and frozen_ast_dump(comparisons[0].left)==spec['inline_comparison_left_ast'],'Exact original inline source-hash comparison')
  a=sum(map(len,lines[:node.lineno-1]))+node.col_offset;b=sum(map(len,lines[:node.end_lineno-1]))+node.end_col_offset
  token=original[a:b];need(token in[(q+old+q).encode()for q in("'",'"')],'One ordinary literal SHA token only')
  edits.append((a,b,token,token[:1]+new.encode()+token[-1:]));paths.append(spec['constant_ast_path']);evidence.append(dict(original_sha256=old,current_sha256=new,dependency=spec['dependency'],constant_ast_path=spec['constant_ast_path']))
 derived=original
 for a,b,old,new in sorted(edits,reverse=True):derived=derived[:a]+new+derived[b:]
 reverse=derived
 for a,b,old,new in sorted(edits,reverse=True):reverse=reverse[:a]+old+reverse[b:]
 need(reverse==original,'Byte-exact inverse of only approved receipt-checksum literals')
 after=ast.parse(derived.decode('utf-8'))
 for module in(tree,after):
  for path in paths:node_at(module,path).value='APPROVED_RECEIPT_SHA_ONLY'
 need(frozen_ast_dump(tree)==frozen_ast_dump(after),'Whole module AST identity except exact receipt checksum constants')
 return derived,dict(original_source_sha256=hashlib.sha256(original).hexdigest(),derived_source_sha256=hashlib.sha256(derived).hexdigest(),
  receipt_bindings=evidence,all_other_bytes_unchanged=True,all_other_module_ast_nodes_unchanged=True)

def prepare_stage(task,pass_name,name):
 task=Path(task);request=verify(task);profile=lane(request['lane']);c=capsule(task,pass_name);p=c.parent/'PORTS.json';log=read(p)
 need(len(log['entries'])<len(profile['stages'])and profile['stages'][len(log['entries'])]==name,'Exact unskipped action order')
 row=stage(name);dependencies={v['dependency']:digest(c/v['dependency'])for v in row['receipt_ports']}
 b,report=derive_source((task/'provenance'/row['directory']/row['script']).read_bytes(),row,dependencies)
 (c/row['directory']/row['script']).write_bytes(b);log['entries'].append(dict(stage=name,report=report));p.write_bytes(dump(log));verify(task);return report

def verify(task, *,completed_adapter_sha256=None):
 task=ordinary(task);d=plan();request=read(task/'SOURCES.json');profile=lane(request['lane'])
 adapter=digest(__file__)if completed_adapter_sha256 is None else completed_adapter_sha256
 need(type(adapter)is str and(adapter==digest(__file__)or adapter in PRIOR_SOURCE_ADAPTERS),'Known exact completed source-adapter epoch')
 need(request['schema']==SCHEMA and request['source_plan_sha256']==PLAN_SHA256 and request['source_adapter_sha256']==adapter
  and request['sources']=={n:r['sha256']for n,r in d['source_files'].items()}and request['active_original_sources']=={n:r['sha256']for n,r in d['active_source_files'].items()}
  and request['historical_outputs_are_provenance_only']is True and all(request[k]is False for k in('arithmetic_computed','parent_acquisitions_verified','full_notebook59_completed','all_index_conclusion_verified')),'Exact truthful original cover source epoch')
 found=set()
 for p in(task/'provenance').rglob('*'):
  ordinary(p)
  if p.is_file():found.add(p.relative_to(task/'provenance').as_posix())
 need(found==set(d['source_files']),'Complete sealed raw original provenance inventory')
 for name,row in d['source_files'].items():need(digest(task/'provenance'/name)==row['sha256'],'Every original raw source/provenance input unchanged')
 for pass_name in PASSES:
  c=capsule(task,pass_name);log=read(c.parent/'PORTS.json');entries=log['entries']
  need(log['schema']=='EXPLICIT_ORIGINAL_RECEIPT_HASH_PORTS_V1'and log['lane']==request['lane']and log['pass_name']==pass_name
   and type(entries)is list and[e['stage']for e in entries]==profile['stages'][:len(entries)]and len(entries)<=len(profile['stages']),'Exact source-epoch action prefix')
  expected={n:r['sha256']for n,r in d['active_source_files'].items()}
  for entry in entries:
   row=stage(entry['stage']);dependencies={v['dependency']:digest(c/v['dependency'])for v in row['receipt_ports']}
   b,report=derive_source((task/'provenance'/row['directory']/row['script']).read_bytes(),row,dependencies)
   need(same(entry,dict(stage=entry['stage'],report=report)),'Typed exact current receipt literal epoch')
   expected[row['directory']+'/'+row['script']]=hashlib.sha256(b).hexdigest()
  found=set()
  for p in c.rglob('*'):
   ordinary(p)
   if p.is_file():found.add(p.relative_to(c).as_posix())
  allowed={p for step in profile['stages']for p in output_paths(step)}
  need(set(expected)<=found<=set(expected)|allowed,'Sealed active originals/approved ports plus only selected current native output slots')
  for name,pin in expected.items():need(digest(c/name)==pin,'Exact source/receipt-configuration bytes before and after original native execution')
 return request
