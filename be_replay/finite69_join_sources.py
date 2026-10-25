"""Complete65 source-only selection. Historical answers are comparison data."""
from pathlib import Path
import shutil,zipfile
from . import finite69_caps_sources as base
from .colab_batch import atomic_json
ROOT,MIB=base.ROOT,base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
PLAN=ROOT/'proof/finite69_join_source_plan.json'
PLAN_SHA256='e6d259b80f2f54a76c596f995b174f5a9434267876ee41b5ffadb1174d96514c'
def plan():
 need(digest(PLAN)==PLAN_SHA256,'Exact complete65 source inventory')
 p=read(PLAN,64*MIB);need(p['schema']=='FINITE69_REMAINING_FULL_ORIGINAL_PRODUCER_PLAN_V1'
  and set(p['stages'])=={'auxiliary','bridge','radius','high','support'}
  and sum(len(s['actions'])for s in p['stages'].values())==19
  and p['arithmetic_computed']is False and p['global_proof_accepted']is False,'All19 original65 producer calls')
 return p
def obtain_assets(directory,*,progress=lambda *a,**k:None):
 # The six source transports are exactly the established46 transports.
 need(plan()['assets']==base.catalog()['assets'],'Same complete source transports as46')
 return base.obtain_assets(directory,progress=progress)
def prepare_cache(assets,directory,*,progress=lambda *a,**k:None):
 p=plan();directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);opened={}
 try:
  for a in p['assets']:
   f=ordinary(assets[a['name']]);need(f.stat().st_size==a['bytes']and digest(f)==a['sha256'],'Entire source transport SHA256')
   z=zipfile.ZipFile(f);base.base.zip_index(z);opened[a['name']]=z
  for i,(name,row)in enumerate(p['source_files'].items()):
   f=ordinary(directory.joinpath(*parts(name)))
   if not f.exists():
    f.parent.mkdir(parents=True,exist_ok=True)
    with opened[row['archive']].open(row['member'])as s,f.open('xb')as d:shutil.copyfileobj(s,d,MIB)
   need(f.stat().st_size==row['bytes']and digest(f)==row['sha256'],'Exact unchanged original source '+name)
   if i%40==0:progress('finite69_remaining_source',files=i,total=len(p['source_files']),arithmetic_computed=False)
 finally:
  for z in opened.values():z.close()
 return directory
def outputs(stage):
 s=plan()['stages'][stage];names={x for a in s['actions']for x in a['outputs']}
 if 'request'in s:names.add(s['request'])
 for a in s['actions']:
  if 'capture'in a:names.update(a['capture']+'/'+n for n in('metadata.json','stdout.txt','stderr.txt'))
 return names
def prepare(cache,task,stage,parents=()):
 s=plan()['stages'][stage];task=ordinary(task);need(not task.exists(),'Exclusive complete65 producer stage');task.mkdir(parents=True)
 pins=dict(s['sources_sha256']);imports=[]
 for parent,validator in parents:
  parent=ordinary(parent);checked=validator(parent);key=checked.get('stage', 'owncaps')
  dest=task/'inputs'/key;need(not dest.exists(),'One genuine parent per producer');shutil.copytree(parent,dest)
  imports.append(dict(key=key,validated=checked,task_relative=dest.relative_to(task).as_posix()))
  for f in (parent/'capsule').rglob('*'):
   ordinary(f)
   if not f.is_file():continue
   name=f.relative_to(parent/'capsule').as_posix();pin=digest(f)
   need(name not in pins or pins[name]==pin,'No source conflict between whole actual parents')
   pins[name]=pin;q=task/'capsule'/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,q)
 for name,pin in s['sources_sha256'].items():
  f=ordinary(Path(cache)/name);need(digest(f)==pin,'Original native source')
  q=task/'capsule'/name;q.parent.mkdir(parents=True,exist_ok=True)
  if q.exists():need(digest(q)==pin,'Same exact shared source')
  else:shutil.copyfile(f,q)
 need(not(set(pins)&outputs(stage)),'No old producer answer in a fresh native output slot')
 r=dict(schema='SEALED_COMPLETE65_ORIGINAL_PRODUCER_V1',stage=stage,original_task_root=str(task),source_plan_sha256=PLAN_SHA256,
  sources=pins,imports=imports,arithmetic_computed=False,global_proof_accepted=False)
 atomic_json(task/'SOURCES.json',r);verify(task);return r
def verify(task):
 task=ordinary(task);r=read(task/'SOURCES.json',64*MIB);s=plan()['stages'][r['stage']]
 need(r['schema']=='SEALED_COMPLETE65_ORIGINAL_PRODUCER_V1'and r['source_plan_sha256']==PLAN_SHA256
  and r['arithmetic_computed']is False and r['global_proof_accepted']is False,'Exact source preparation epoch')
 pins=dict(s['sources_sha256'])
 for record in r['imports']:
  from . import finite69_remaining as runtime
  from . import finite69_caps_evidence as caps
  validator=caps.validate_completed if record['key']=='owncaps'else runtime.validate_completed
  parent=task.joinpath(*parts(record['task_relative']));checked=validator(parent)
  need(runtime.same(checked,record['validated']),'Whole actual parent is independently revalidated')
  for f in(parent/'capsule').rglob('*'):
   ordinary(f)
   if f.is_file():
    n=f.relative_to(parent/'capsule').as_posix();pin=digest(f)
    need(n not in pins or pins[n]==pin,'Consistent whole parent source graph');pins[n]=pin
 expected=set(s.get('parents',[]));actual={r['key']for r in r['imports']}
 need(actual==expected and len(actual)==len(r['imports'])and pins==r['sources'],'Only and all genuine producer parents')
 found=set()
 for f in(task/'capsule').rglob('*'):
  ordinary(f)
  if f.is_file():found.add(f.relative_to(task/'capsule').as_posix())
 need(set(pins)<=found<=set(pins)|outputs(r['stage']),'Exact full producer source/output inventory')
 for name,pin in pins.items():need(digest(task/'capsule'/name)==pin,'Every unchanged native or genuine parent byte')
 return r
def request(task):
 task=Path(task);r=read(task/'SOURCES.json');s=plan()['stages'][r['stage']];c=task/'capsule';runs=s['runs']
 result=dict(plan=runs+'/plan01/PLAN.json',plan_sha256=digest(c/runs/'plan01/PLAN.json'),
  manifest_sha256=digest(c/s['native']/'MANIFEST.json'),construct_capture=runs+'/construct01',
  construct_metadata_sha256=digest(c/runs/'construct01/metadata.json'),replay_capture=runs+'/replay01',
  replay_metadata_sha256=digest(c/runs/'replay01/metadata.json'),output=s['result'])
 if r['stage']!='auxiliary':result['family']=r['stage']
 return result
