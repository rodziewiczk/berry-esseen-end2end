"""All40 selected original n25 acquisition calls, ten complete families.

This is the numerical acquisition component of66. It deliberately does not
claim the20-piece semantic union. Each call receives its own23-hour CPU/wall
ceiling. Full successful prefixes resume through an exact stopped-run reader.
"""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath,PureWindowsPath
import ast,hashlib,json,math,re,shutil,sys,traceback,uuid,zipfile
from . import n25_full_acquisition_sources as src,action_supervisor as linux_supervisor
from . import delivery_transport as io
from .colab_batch import atomic_json,event,utc

CPU=WALL=82800
MEMORY=2048*io.MIB
REFS=src.ROOT/'proof/n25_acquisition_receipt_references.json'
REFS_SHA='026ee9950ac50b36207313f83a7d7bfd885a447b6c610a9bf95599ea5848f10a'
FLAGS=dict(parent_acquisitions_verified=False,mixed_exclusion_verified=False,full66_complete=False,all_index_conclusion_verified=False)

def read(path):return src.base.parsed(src.base._regular(path,128*io.MIB))
def same(a,b):return src.base._same(a,b)
def sha(path):return io.digest(path)
def family_root(task):return Path(task)/'epoch'/src.PREFIX.rstrip('/')

def implementation():
 return {n:sha(src.ROOT/'be_replay'/n)for n in ('n25_acquisitions.py','n25_full_acquisition_sources.py','delivery_transport.py','action_supervisor.py')}|dict(source_plan=src.PLAN_SHA256,receipt_references=REFS_SHA)

def references():
 src.need(sha(REFS)==REFS_SHA,'Pinned complete historical receipt payload references')
 d=read(REFS);src.need(d['historical_acceptance_is_fresh']is False,'References are not execution evidence');return d['receipts']

def action_outputs(a):
 result=[a['folder']+'/'+a['proof']]
 if a['receipt']:result.append(a['folder']+'/'+a['receipt'])
 if a['script']=='acquire_panel_cached.py':result.append(a['folder']+'/local_'+a['args'][-1]+'_accept.runtime.json')
 return result

def prefix_key(family,count):return family+'-'+str(count).zfill(2)

def cached_parent_packet(task,family,alias):
 root=family_root(task);spec=src.definition(family);original=root/spec['canonical_directory'];folder=root/alias['folder']
 protocol=read_source=folder/'cached_protocol.py'
 if not protocol.is_file():return None
 tree=ast.parse(protocol.read_bytes());strings=[n.value for n in ast.walk(tree)if isinstance(n,ast.Constant)and type(n.value)is str and n.value.startswith('PASS_BYTE_IDENTICAL_ACCEPTED_')]
 src.need(len(set(strings))==1,'Exact native byte-identity parent-snapshot condition')
 copies={name:sha(original/name)for name in alias['parent_names']}
 for name,pin in copies.items():src.need(sha(folder/name)==pin,'Actual fresh accepted parent alias bytes')
 # The complete original canonical source inventory and all current parent
 # artifacts are included, beyond the native consumer's minimal assertions.
 files={n.removeprefix(src.PREFIX):sha(Path(task)/'epoch'/n)for n in src.selected(family)
  if n.startswith(src.PREFIX+spec['canonical_directory']+'/')and not n.endswith('FROZEN_SOURCES.json')}
 files.update({spec['canonical_directory']+'/'+name:pin for name,pin in copies.items()})
 return dict(status=strings[0],copies_sha256=copies,files_sha256=files,
  capture_origin='CURRENT_FULLY_READ_BACK_ACCEPTANCE_AND_EXACT_COPY',historical_receipt_impersonated=False)

def bind_aliases(task,family):
 root=family_root(task);spec=src.definition(family);canonical=root/spec['canonical_directory'];bindings={}
 for alias in spec['local_aliases']:
  if not all((canonical/n).is_file()for n in alias['parent_names']):continue
  for name in alias['parent_names']:
   p=root/alias['folder']/name;p.parent.mkdir(parents=True,exist_ok=True)
   if p.exists():src.need(p.read_bytes()==(canonical/name).read_bytes(),'No overwriting a different parent snapshot')
   else:shutil.copyfile(canonical/name,p)
  if (root/alias['folder']/'cached_protocol.py').exists()and (canonical/'COPY_MANIFEST.json').is_file():
   for name,pin in read(canonical/'COPY_MANIFEST.json')['files'].items():
    io.parts(name);source=canonical/name;src.need(sha(source)==pin,'Exact pinned original alias helper')
    dest=root/alias['folder']/name
    if dest.exists():src.need(sha(dest)==pin,'Existing alias helper is byte-identical')
    else:dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
  packet=cached_parent_packet(task,family,alias)
  if packet is not None:
   dest=root/alias['folder']/'PARENTS_BOUND.json'
   raw=src.base.encoded(packet)
   if dest.exists():src.need(dest.read_bytes()==raw,'Stable truthful current parent alias manifest')
   else:dest.write_bytes(raw)
   bindings[alias['folder']]=sha(dest)
 return bindings

def verify_sources(task,family):
 src.verify(task,family);root=family_root(task);expected=src.epoch_rows(task,family)
 for name,row in expected.items():
  p=Path(task)/'epoch'/name
  src.need(p.is_file()and p.stat().st_size==row['bytes']and sha(p)==row['sha256'],'Every original/projected source byte is still exact')
 allowed=set(n.removeprefix(src.PREFIX)for n in expected)
 for a in src.definition(family)['actions']:allowed.update(action_outputs(a))
 for alias in src.definition(family)['local_aliases']:
  allowed.update(alias['folder']+'/'+n for n in alias['parent_names']);allowed.add(alias['folder']+'/PARENTS_BOUND.json')
  canonical=root/src.definition(family)['canonical_directory']
  if (root/alias['folder']/'cached_protocol.py').exists()and (canonical/'COPY_MANIFEST.json').exists():
   for name,pin in read(canonical/'COPY_MANIFEST.json')['files'].items():
    p=root/alias['folder']/name
    if p.exists():src.need(sha(p)==pin,'Every copied cache-parent helper remains exact')
    allowed.add(alias['folder']+'/'+name)
 for p in root.rglob('*'):
  io.ordinary(p)
  if not p.is_file():continue
  rel=p.relative_to(root).as_posix()
  src.need(p.suffix not in ('.pyc','.pyo','.so','.dll','.pth'),'No new import/bytecode helper')
  src.need(rel in allowed or (p.name in ('PROGRESS.json','LOCAL_PROGRESS.json','INITIAL_PROGRESS.json','RESOURCE_PROGRESS.json')
   and p.suffix=='.json'),'Only selected source, output, parent-alias and progress artifacts: '+rel)
 for alias in src.definition(family)['local_aliases']:
  p=root/alias['folder']/'PARENTS_BOUND.json'
  if p.exists():src.need(p.read_bytes()==src.base.encoded(cached_parent_packet(task,family,alias)),'Whole current parent alias binding, no historical receipt')
 return expected

def mathematical_proof(task,family,a):
 root=family_root(task);proof=read(root/a['folder']/a['proof']);view=deepcopy(proof)
 for field in a['fresh_parent_metadata_fields']:
  src.need(field in view and type(view[field])is str and re.fullmatch('[0-9a-f]{64}',view[field]),'One declared parent-identity metadata field')
  view.pop(field)
 src.need(src.base.sha(src.base.encoded(view))==a['proof_mathematical_projection_sha256']
  and proof['schema']==a['proof_schema'],'Whole original mathematical proof, every profile/cycle/row preserved')
 # Bind fresh duration-dependent parents independently of mathematical view.
 spec=src.definition(family);initial=spec['actions'][0]
 if 'initial_acceptance_sha256'in a['fresh_parent_metadata_fields']:
  src.need(proof['initial_acceptance_sha256']==sha(root/initial['folder']/initial['receipt']),'Actual freshly accepted INITIAL, never its historical SHA')
 if 'parent_sha256'in a['fresh_parent_metadata_fields']:
  parent=next(r for r in spec['actions']if r['id']=='global-resource-construct')
  src.need(proof['parent_sha256']==sha(root/parent['folder']/parent['proof']),'Actual complete global resource proof')
 return proof

def receipt(task,family,a):
 if not a['receipt']:return None
 root=family_root(task);p=root/a['folder']/a['receipt'];obj=read(p);expected=deepcopy(references()[family+'/'+a['id']])
 src.need(set(obj)==set(a['receipt_fields'])and obj['status']==a['expected_receipt_status']
  and same(obj['negative_controls'],a['negative_controls']),'All exact original receipt fields and corruption controls')
 src.need(type(obj['seconds'])in(int,float)and math.isfinite(obj['seconds'])and obj['seconds']>=0,'Actual finite execution duration')
 expected['seconds']=obj['seconds'];expected['proof_sha256']=sha(root/a['folder']/a['proof'])
 if 'initial_acceptance_sha256'in expected:
  first=src.definition(family)['actions'][0];expected['initial_acceptance_sha256']=sha(root/first['folder']/first['receipt'])
 src.need(same(obj,expected),'Every full native acceptance field, with only actual time and declared fresh parent identities changed')
 src.need(obj['checker_sha256']==sha(root/a['native_checker']),'Original complete checker, including cached wrapper distinction')
 return obj

def map_path(task,value,original):
 cls=PureWindowsPath if re.match(r'^[A-Za-z]:',original)else PurePosixPath
 p,base=cls(value),cls(original);src.need(p.is_absolute()and base.is_absolute(),'One absolute originating task context')
 try:rel=p.relative_to(base)
 except ValueError:raise ValueError('Capture escapes originating task')
 return io.ordinary(Path(task).joinpath(*rel.parts))

def validate_action(task,family,a,record,context):
 root=family_root(task);directory=Path(task)/'executions'/a['id'];observed=read(directory/'supervisor-result.json')
 src.need(same(observed,record['observed'])and observed['status']=='completed'and type(observed['returncode'])is int
  and observed['returncode']==0 and observed['reason']is None and observed['mode']=='untrusted_search'
  and observed['proof_accepted']is False and type(observed['sample_count'])is int and observed['sample_count']>0,'Actual completed stopped original acquisition')
 execution_context=record['context'];src.need(type(execution_context['python_version'])is str and execution_context['python_version'],'Actual action interpreter context')
 launch=read(directory/'launch.json');cwd=root/a['folder'];origin=execution_context['original_task_root']
 expected_guard=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(WALL),
  per_process_RLIMIT_AS_bytes=MEMORY,per_process_RLIMIT_CPU_seconds=CPU,aggregate_kernel_memory_limit=False,
  aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY,sampled_group_CPU_limit_seconds=CPU,
  sampled_file_limit_bytes=512*io.MIB,sampled_log_limit_bytes=16*io.MIB,descendants_changing_session_are_contained=False,
  equivalent_to_Windows_Job_or_cgroup=False,sampled_group_CPU_includes_waited_descendants=True)
 src.need(same(observed['guard_scope'],expected_guard),'Complete honest per-action BASIC supervision policy')
 src.need(launch['argv']==[execution_context['python_executable'],'-B','-S',a['script'],*a['args']]
  and map_path(task,launch['cwd'],origin)==cwd and map_path(task,launch['output_dir'],origin)==directory
  and launch['cpu_seconds']==CPU and launch['wall_seconds']==WALL and launch['memory_bytes']==MEMORY
  and launch['disk_bytes']==512*io.MIB and launch['log_bytes']==16*io.MIB and launch['mode']=='untrusted_search'
  and launch['sample_seconds']==.2 and launch['heartbeat_seconds']==20,'Exact original action and23-hour per-action budgets')
 outputs=action_outputs(a)
 src.need([map_path(task,p,origin)for p in launch['checkpoint_paths']]==[root/n for n in outputs],'Every proof/receipt/cache-runtime stopped checkpoint requested')
 for kind in ('stdout','stderr'):
  p=directory/(kind+'.txt');src.need(map_path(task,observed[kind+'_path'],origin)==p and sha(p)==observed[kind+'_sha256'],'Actual whole captured stream')
 src.need((directory/'stderr.txt').stat().st_size==0 and (directory/'stdout.txt').stat().st_size>0,'Original successful capture, empty stderr')
 src.need(len(observed['checkpoints'])==len(outputs),'All stopped outputs captured')
 for packet,name in zip(observed['checkpoints'],outputs):
  p=root/name;cp=directory/'checkpoints'/p.relative_to(cwd)
  src.need(packet['exists']is True and packet['trusted_certificate']is False and map_path(task,packet['source_path'],origin)==p
   and map_path(task,packet['path'],origin)==cp and packet['bytes']==p.stat().st_size==cp.stat().st_size
   and packet['sha256']==sha(p)==sha(cp),'Whole actual stopped output equality')
 for name,pin in record['inputs_sha256'].items():src.need(sha(root/name)==pin,'All bound original/previous-result input bytes unchanged')
 proof=mathematical_proof(task,family,a);accepted=receipt(task,family,a)
 if a['script']=='acquire_panel_cached.py':
  runtime=read(root/outputs[-1]);info=runtime['cache_after'];calls=sum(len(c['stages'])for c in proof['cycles'])
  src.need(runtime['action']=='accept'and runtime['index']==int(a['args'][-1])and runtime['mathematical_cover_calls']==calls
   and info['misses']==info['size']==runtime['distinct_complete_argument_keys']==runtime['original_full_stage_evaluations']
   and info['hits']==runtime['memoized_identical_calls']==calls-info['misses']
   and runtime['fresh_cache_before']==dict(hits=0,misses=0,size=0,maxsize=info['maxsize']),
   'Every original complete local cover accounted for, fresh exact process-local memoization')
  src.need(runtime['actual_wrapper_sha256']==sha(cwd/a['script'])and runtime['original_checker_sha256']==sha(root/a['native_checker'])
   and runtime['parent_snapshot_sha256']==sha(cwd/'PARENTS_BOUND.json')and runtime['frozen_sources_sha256']==sha(cwd/'FROZEN_SOURCES.json'),
   'Actual named cache wrapper, sources and genuinely accepted parent snapshot')
  for name,pin in runtime['output_sha256'].items():src.need(sha(cwd/name)==pin,'Every full cached wrapper output')
 return dict(id=a['id'],proof_sha256=sha(root/a['folder']/a['proof']),receipt_sha256=sha(root/a['folder']/a['receipt'])if accepted else None,
  negative_controls=len(a.get('negative_controls',[])),whole_mathematical_payload_preserved=True)

def validate_prefix(task,*,require_complete=False):
 task=io.ordinary(task);context=read(task/'ACQUISITION.json');family=context['family'];spec=src.definition(family);verify_sources(task,family)
 src.need(context['schema']=='N25_ORIGINAL_ACQUISITION_TASK_V1'and same(context['implementation'],implementation())
  and context['source_plan_sha256']==src.PLAN_SHA256 and all(context[k]is False for k in FLAGS),'Exact source epoch, explicit conditional scope')
 records=read(task/'ACTIONS.json')['actions'];src.need(0<len(records)<=len(spec['actions'])
  and [r['id']for r in records]==[a['id']for a in spec['actions'][:len(records)]],'Complete unskipped original action prefix')
 if require_complete:src.need(len(records)==len(spec['actions']),'Every assigned full original action completed')
 summaries=[validate_action(task,family,a,r,context)for a,r in zip(spec['actions'],records)]
 return dict(schema='REVALIDATED_N25_ACQUISITION_PREFIX_V1',family=family,completed_actions=len(records),total_actions=len(spec['actions']),
  complete_family=len(records)==len(spec['actions']),actions=summaries,conditional_arithmetic_completed=True,**FLAGS)

def execute_next(task,family,*,log_root):
 task=Path(task).resolve();context=read(task/'ACQUISITION.json');ledger=read(task/'ACTIONS.json');spec=src.definition(family)
 if ledger['actions']:validate_prefix(task)
 ordinal=len(ledger['actions']);src.need(ordinal<len(spec['actions']),'An uncompleted full original action')
 bind_aliases(task,family);verify_sources(task,family);a=spec['actions'][ordinal];root=family_root(task);cwd=root/a['folder'];outputs=action_outputs(a)
 created=[a['folder']+'/'+(a['receipt']if a['receipt']else a['proof'])]
 if a['script']=='acquire_panel_cached.py':created.append(outputs[-1])
 src.need(all(not(root/n).exists()for n in created),'A complete new proof/receipt slot; no old acceptance pre-staged')
 before={n:row['sha256']for n,row in io.inventory(root).items()if Path(n).name not in ('PROGRESS.json','LOCAL_PROGRESS.json','INITIAL_PROGRESS.json','RESOURCE_PROGRESS.json')}
 with io.Follow(log_root,task/'executions'/a['id'],family+'/'+a['id']):
  observed=linux_supervisor.run([sys.executable,'-B','-S',a['script'],*a['args']],cwd=cwd,output_dir=task/'executions'/a['id'],
   mode='untrusted_search',cpu_seconds=CPU,wall_seconds=WALL,memory_bytes=MEMORY,disk_bytes=512*io.MIB,log_bytes=16*io.MIB,
   heartbeat_seconds=20,checkpoint_paths=[root/n for n in outputs])
 record=dict(id=a['id'],observed=observed,inputs_sha256=before,
  context=dict(original_task_root=str(task),python_executable=sys.executable,python_version=sys.version))
 atomic_json(task/'CURRENT_ACTION.json',record);validate_action(task,family,a,record,context)
 ledger['actions'].append(record);atomic_json(task/'ACTIONS.json',ledger);checked=validate_prefix(task)
 event(log_root,'n25_acquisition_action_complete',family=family,completed=checked['completed_actions'],total=checked['total_actions'],per_action_cpu=CPU,per_action_wall=WALL)
 return checked

def prepare(task,family,*,archive):
 src.prepare(task,family,archive=archive)
 context=dict(schema='N25_ORIGINAL_ACQUISITION_TASK_V1',family=family,source_plan_sha256=src.PLAN_SHA256,
  implementation=implementation(),original_task_root=str(Path(task).resolve()),python_executable=sys.executable,python_version=sys.version,**FLAGS)
 atomic_json(Path(task)/'ACQUISITION.json',context);atomic_json(Path(task)/'ACTIONS.json',dict(actions=[]));return context

def run_family(family,*,durable_root,work_root,archive,log_root=None):
 spec=src.definition(family);root=Path(work_root);cache=Path(durable_root)/'n25-acquisitions/completed'/src.PLAN_SHA256[:16]/family
 log_root=Path(log_root or root);log=lambda name,**data:event(log_root,name,**data)
 task=None;checked=None
 for count in range(len(spec['actions']),0,-1):
  hit=io.restore(cache/str(count),root/family,validator=validate_prefix,log=log)
  if hit:
   task,checked,_=hit
   if checked['family']!=family or checked['completed_actions']!=count:raise ValueError('No cross-family/cross-prefix cache')
   break
 if task is None:
  task=root/(family+'-'+uuid.uuid4().hex[:12]);prepare(task,family,archive=archive)
 while checked is None or not checked['complete_family']:
  checked=execute_next(task,family,log_root=log_root)
  io.save(task,cache/str(checked['completed_actions']),validator=validate_prefix,label=prefix_key(family,checked['completed_actions']))
 return task,validate_prefix(task,require_complete=True)

def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
 from . import count_task
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
 root=Path(work_root)/'n25-acquisitions'/stamp;root.mkdir(parents=True,exist_ok=False);durable=Path(durable_root)/'n25-acquisitions'/stamp
 status=dict(schema='N25_ALL40_ACQUISITION_ACTIONS_SESSION_V1',state='INCOMPLETE',families=[],per_action_cpu_seconds=CPU,
  per_action_wall_seconds=WALL,batch_wall_deadline=None,**FLAGS)
 backups=io.Backups(root,durable,backup_interval);backups.start()
 try:
  archive=count_task.obtain_asset(archives,'old',download=True,progress=root)
  for family in src.families():
   task,checked=run_family(family,durable_root=durable_root,work_root=root/'families',archive=archive,log_root=root)
   status['families'].append(dict(family=family,task_relative=task.relative_to(root).as_posix(),validated=checked));atomic_json(root/'SESSION_RESULT.json',status)
  status.update(state='COMPLETE_CONDITIONAL_40_ACTION_ACQUISITION_COMPONENT',conditional_arithmetic_completed=True)
 except BaseException as error:
  status.update(state='INCOMPLETE',error=type(error).__name__+': '+str(error));(root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8')
 finally:
  try:backups.close()
  except Exception as error:status.update(state='INCOMPLETE',synchronization_error=str(error))
  status['finished_utc']=utc();path=io.final_bundle(root,durable,Path(work_root)/'n25-acquisitions-local'/stamp,status)
 return dict(status=status,bundle=path,work=str(root))
