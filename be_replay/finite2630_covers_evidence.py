"""Pure source/current-receipt/stopped evidence for full59B/C covers."""
from __future__ import annotations
import copy,hashlib,json,math,re
from fractions import Fraction as F
from pathlib import Path,PureWindowsPath,PurePosixPath
from . import finite2630_covers_sources as src
from .finite1039_count_evidence import same,mapped,inventory,terminal
SCOPE='TWO_COMPLETE_ORIGINAL_FINITE2630_FOURIER_COVER_PASSES_CURRENT_RECEIPT_EPOCH_V1'
OBSERVED='OBSERVED_CONDITIONAL_FINITE2630_COVERS_V1'
COMPLETED='COMPLETED_CONDITIONAL_FINITE2630_COVERS_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
FLAGS=('native_arithmetic_accepted','parent_acquisitions_verified','support_acquisition_verified','full_notebook59_completed',
 'full_finite2630_verified','resource_to_count80_interfaces_verified','kappa_analytic_framework_acquired','all_index_conclusion_verified')
def implementation():
 names=('finite2630_covers.py','finite2630_covers_sources.py','finite2630_covers_evidence.py','finite1039_sources.py',
  'finite1039_count_evidence.py','n5_remaining_sources.py','linux_supervisor.py','colab_batch.py')
 return{n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)

# Both published readers have identical numerical/evidence predicates. The
# later source adapter only restores the Python3.12 AST spelling on3.13.
# Compatibility is for the exact WHOLE recorded map, never one arbitrary hash.
PRIOR_IMPLEMENTATION_BASE={
 'finite2630_covers.py':'abc92fcb461c16a77696e7991d760cc2dbd7bf33db753e3bba0ba52b58f01714',
 'finite2630_covers_evidence.py':'d2dc8cbe3513e55f2e06c246f5351231671f1f2482f05a497ae2621d9052f3c1',
 'finite1039_sources.py':'6a34be3e362d2a9cfe34b52bf1c0f1872cd4fe45afa8cf2acf82a232b4da1c95',
 'finite1039_count_evidence.py':'7dae50a7d2756faa30d229ae02fb15d678db4cbaa837be43518c10af5af85cfa',
 'n5_remaining_sources.py':'17f8d9b3bcdce510574901be83684a630d54cc8d2f6251856b7737bbd85aaaab',
 'linux_supervisor.py':'61e71dd4a9653de2bbbee8c54928a1f5c5bffd0bf083dd324851716c3a1eaea2',
 'colab_batch.py':'136bc2bb9b25cb8cd36118041bf593821f3cbdea5debee82b27ccb7626c0d1e6',
 'source_plan_sha256':'86692f3f8f170e6fe53e578f9c129409028303ef8831684a8b4cfb8eaceef8b9'}

def completed_implementation_adapter(record):
 src.need(type(record)is dict,'Exact whole recorded implementation map')
 if same(record,implementation()):return record['finite2630_covers_sources.py']
 for adapter in src.PRIOR_SOURCE_ADAPTERS:
  expected=PRIOR_IMPLEMENTATION_BASE|{'finite2630_covers_sources.py':adapter}
  if same(record,expected):return adapter
 raise ValueError('Unknown completed original cover implementation epoch')
def original_path(request,pass_name,relative=''):
 root=request['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
 src.need(cls(root).is_absolute(),'One original absolute task context');return str(cls(root)/'passes'/pass_name/'capsule'/relative)
def command(request,pass_name,name,python):
 src.need(pass_name in src.PASSES and type(python)is str and(PureWindowsPath(python).is_absolute()or PurePosixPath(python).is_absolute()),'Exact original pass/interpreter')
 row=src.stage(name);return[python,'-B','-S',original_path(request,pass_name,row['directory']+'/'+row['script'])]
def finite(value):
    src.need(type(value)in(int,float)and math.isfinite(value)and value>=0,'Finite nonnegative execution display');return value


def transport(task,request,pass_name,action,observed,report):
    task=Path(task);original=request['original_task_root'];directory=task/'executions'/(pass_name+'-'+action);c=src.capsule(task,pass_name)
    src.need(same(src.read(directory/'supervisor-result.json'),observed)
             and observed.get('status')=='completed'and type(observed.get('returncode'))is int and observed['returncode']==0
             and observed.get('reason')is None and observed.get('mode')=='untrusted_search'
             and observed.get('proof_accepted')is False and type(observed.get('sample_count'))is int and observed['sample_count']>0,
             'Actual successful stopped BASIC execution for '+action)
    for k in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):finite(observed[k])
    launch=src.read(directory/'launch.json')
    fields={'argv','cwd','output_dir','mode','wall_seconds','cpu_seconds','memory_bytes','checkpoint_paths',
            'disk_bytes','log_bytes','sample_seconds','heartbeat_seconds'}
    outputs=src.output_paths(action)
    src.need(set(launch)==fields and same(launch['argv'],command(request,pass_name,action,report['python_executable']))
             and mapped(task,launch['cwd'],original)==c
             and mapped(task,launch['output_dir'],original)==directory and launch['mode']=='untrusted_search'
             and type(launch['cpu_seconds'])is int and launch['cpu_seconds']==CPU_SECONDS
             and type(launch['memory_bytes'])is int and launch['memory_bytes']==MEMORY_BYTES
             and type(launch['wall_seconds'])in(int,float)and launch['wall_seconds']==WALL_SECONDS
             and type(launch['disk_bytes'])is int and launch['disk_bytes']==512*src.MIB
             and type(launch['log_bytes'])is int and launch['log_bytes']==16*src.MIB
             and launch['sample_seconds']==.2 and launch['heartbeat_seconds']==20
             and type(launch['checkpoint_paths'])is list
             and [mapped(task,v,original)for v in launch['checkpoint_paths']]==[c/p for p in outputs],
             'Exact original action, source cwd, capture requests and documented budgets')
    scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,
        external_wall_seconds=float(WALL_SECONDS),per_process_RLIMIT_AS_bytes=MEMORY_BYTES,
        per_process_RLIMIT_CPU_seconds=CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,
        sampled_group_RSS_limit_bytes=MEMORY_BYTES,sampled_group_CPU_limit_seconds=CPU_SECONDS,
        sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
    src.need(same(observed['guard_scope'],scope),'Honest process-tree BASIC policy, without a native promotion')
    captures={}
    for kind in('stdout','stderr'):
        p=mapped(task,observed[kind+'_path'],original)
        src.need(p==directory/(kind+'.txt')and p.is_file()and p.stat().st_size<=16*src.MIB
                 and src.digest(p)==observed[kind+'_sha256'],'Actual captured '+kind+' bytes')
        captures[kind]=p
    src.need(captures['stderr'].stat().st_size==0,'Successful original stderr is empty')
    checks=observed['checkpoints'];src.need(type(checks)is list and len(checks)==len(outputs),'Every stopped native output copied')
    for packet,name in zip(checks,outputs):
        p=c/name;copied=directory/'checkpoints'/name
        src.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
                 and packet['exists']is True and packet['trusted_certificate']is False
                 and mapped(task,packet['source_path'],original)==p and mapped(task,packet['path'],original)==copied
                 and p.is_file()and copied.is_file()and type(packet['bytes'])is int
                 and packet['bytes']==p.stat().st_size==copied.stat().st_size
                 and packet['sha256']==src.digest(p)==src.digest(copied),'Whole stopped native output identity: '+name)
    return captures['stdout'].read_text('utf-8')



def projection(record,expected):
 src.need(type(record)is dict,'Whole original JSON object');body=copy.deepcopy(record)
 if expected['source_graph_paths']:src.need(type(body.get('source_sha256'))is dict,'Complete explicit top-level source map');body.pop('source_sha256')
 else:src.need('source_sha256'not in body,'No invented source map in native scalar certificate')
 for pointer in expected['timing_pointers']:
  parts=pointer.split('/')[1:];target=body
  for p in parts[:-1]:target=target[int(p)]if type(target)is list else target[p]
  src.need(parts[-1]=='seconds'and type(target)is dict and parts[-1]in target,'Only explicit enumerated native execution timing slots')
  finite(target.pop(parts[-1]))
 return body

def stdout_matches(text,name,record,output):
 row=src.stage(name);kind=row['stdout_rule']['kind'];status=record.get('status');pin=src.digest(output)
 if kind=='json':src.need(same(terminal(text),record),'Actual complete terminal JSON equals whole current native object');return
 if kind=='utility':parts=[status,record['arithmetic_controls'],record['elementary_controls'],record['exact_bernstein_transform_identities'],record['negative_controls'],pin]
 elif kind=='batch_controls':parts=[status,record['power_or_geometric_prefix_comparisons'],record['exact_per_n_cell_comparisons'],record['negative_controls'],pin]
 elif kind=='b2_controls':parts=[status,record['negative_controls'],pin]
 elif kind=='b3_controls':parts=[status,21,105,5,record['negative_controls'],pin]
 elif kind=='extension_controls':parts=[status,15,75,21,record['negative_controls'],pin]
 elif kind in('b2_pilot','rho130_pilot'):
  values=[(r['n'],r['normalized_upper_float'],r['strict_target_pass'])for r in record['result']['rows']]
  parts=[status,values]+([record['result']['seconds']]if kind=='rho130_pilot'else[])+[pin]
 else:
  src.need(kind in('b2_cover','b3_cover','b5_cover','extension_cover'),'Fixed original stdout source rule')
  count={'b2_cover':115,'b3_cover':110,'b5_cover':30,'extension_cover':75}[kind]
  start=1 if kind in('b2_cover','b3_cover')else 0
  parts=[status,record['passing_rows'],'of'+str(count),sum(b['result']['seconds']for b in record['bands'][start:]),pin]
 lines=text.splitlines();src.need(lines and lines[-1]==' '.join(map(str,parts)),'Exact source-derived native terminal fields and actual output SHA')

def validate_stage(task,request,pass_name,name,observed,report):
 c=src.capsule(task,pass_name);row=src.stage(name);stdout=transport(task,request,pass_name,name,observed,report);objects={};bodies={}
 for relative in src.output_paths(name):
  record=src.read(c/relative,limit=128*src.MIB);expected=row['expected'][relative]
  if expected['source_graph_paths']:
   graph={original_path(request,pass_name,p):src.digest(c/p)for p in expected['source_graph_paths']}
   src.need(same(record['source_sha256'],graph),'Complete current native source graph, exact original paths and actual hashes')
  body=projection(record,expected);pin=hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  src.need(pin==expected['mathematical_body_sha256'],'Every original mathematical/control field equals its frozen exact commitment')
  if expected['status']is not None:src.need(record.get('status')==expected['status'],'Exact successful original native status')
  for key,value in expected['scalar_census'].items():src.need(same(record[key],value),'Exact typed original full control/result census')
  if expected['row_profiles']:
   blocks=([dict(parameters=None,result=record['result'])]if'result'in record else record['bands'])
   src.need(type(blocks)is list and len(blocks)==len(expected['row_profiles']),'All original closed strips, without omission')
   for block,profile in zip(blocks,expected['row_profiles']):
    rows=block['result']['rows'];src.need(type(rows)is list and len(rows)==5 and same([r['n']for r in rows],list(range(26,31)))
     and same(block.get('parameters'),profile['parameters']),'Every literal n26..30 in each exact ordered parameter strip')
    for native in rows:
     q=F(native['normalized_upper']);src.need(type(native['normalized_upper'])is str and str(q)==native['normalized_upper']and 0<=q<F(4097,10000)
      and native['strict_target_pass']is True and native['target']=='4097/10000'and native['rho']==profile['rho']
      and type(native['n'])is int,'Full current strict bounds, exact rational normalization/domain, no n-monotonicity shortcut')
     if request['lane']=='b2':src.need(native['absmean_upper']=='122/125','Explicit conditional absolute-mean support boundary')
  objects[relative]=record;bodies[relative]=body
 stdout_matches(stdout,name,objects[src.output_paths(name)[-1]],c/src.output_paths(name)[-1]);return objects,bodies

def validate_run(task,report):
 task=src.ordinary(task);adapter=completed_implementation_adapter(report['implementation'])
 request=src.verify(task,completed_adapter_sha256=adapter);profile=src.lane(request['lane'])
 src.need(report['schema']==OBSERVED and report['scope']==SCOPE and report['original_task_root']==request['original_task_root']
  and report['lane']==request['lane']and type(report['python_version'])is str and bool(report['python_version'])
  and report['conditional_cover_arithmetic_completed']is False and all(report[k]is False for k in FLAGS),'Exact current two-pass source epoch and unaccepted observed ledger')
 expected=[(p,n)for p in src.PASSES for n in profile['stages']];actions=report['actions']
 src.need(type(actions)is list and[(a['pass_name'],a['stage'])for a in actions]==expected,'Both complete unskipped original native pipelines')
 mathematical={};objects={}
 for a in actions:
  current,bodies=validate_stage(task,request,a['pass_name'],a['stage'],a['observed'],report)
  mathematical[(a['pass_name'],a['stage'])]=bodies;objects[(a['pass_name'],a['stage'])]=current
 for name in profile['stages']:src.need(same(mathematical[('construct',name)],mathematical[('replay',name)]),'Whole mathematical/control object equality from two genuine full current passes')
 for pass_name in src.PASSES:
  c=src.capsule(task,pass_name);ports=src.read(c.parent/'PORTS.json')
  src.need([e['stage']for e in ports['entries']]==profile['stages'],'Complete exact source-checksum epoch ledger')
  pilot_name='b2_pilot'if request['lane']=='b2'else'rho130_pilot';cover_name='b2_cover'if request['lane']=='b2'else'b3_cover'
  pilot=objects[(pass_name,pilot_name)][src.output_paths(pilot_name)[-1]];cover=objects[(pass_name,cover_name)][src.output_paths(cover_name)[-1]]
  src.need(same(pilot['result'],cover['bands'][0]['result']),'Five reused pilot rows are genuinely fresh in this same pass, including their actual timing object')
  bands=list(cover['bands'])
  if request['lane']=='higher':
   for name in('b5_cover','extension_cover'):bands+=objects[(pass_name,name)][src.output_paths(name)[-1]]['bands']
  intervals=[]
  for band in bands:
   rows=band['result']['rows'];src.need(len(rows)==5 and[r['n']for r in rows]==list(range(26,31)),'Five explicit actual indices per covered strip')
   rho=rows[0]['rho'];src.need(all(r['rho']==rho for r in rows),'One exact closed rho interval per complete five-n strip');intervals.append(tuple(map(F,rho)))
  intervals.sort();lo,hi=map(F,profile['rho_intervals'][0])
  src.need(len(intervals)==profile['closed_strips']and 5*len(intervals)==profile['rows']and intervals[0][0]==lo and intervals[-1][1]==hi
   and all(a<b for a,b in intervals)and all(a[1]==b[0]for a,b in zip(intervals,intervals[1:])),
   'Full115/215-row closed no-gap rho cover, including all joins and endpoints')
 return dict(lane=request['lane'],n_values=list(range(26,31)),rho_intervals=profile['rho_intervals'],absmean_upper=profile['absmean_upper'],target='4097/10000',
  rows_per_pass=profile['rows'],closed_strips=profile['closed_strips'],genuine_passes=2,mathematical_rows_recomputed=2*profile['rows'],
  actions_per_pass=len(profile['stages']),total_native_actions=2*len(profile['stages']),negative_controls_per_pass=93 if request['lane']=='b2'else 70,
  all_original_native_controls_replayed=True,all_original_kernel_and_schedule_bytes_unchanged=True,only_explicit_receipt_sha_source_literals_changed=True,
  fresh_five_row_pilot_in_each_pass=True,all_closed_seams_verified=True,source_plan_sha256=src.PLAN_SHA256)

def validate_completed(task, *,original_task_root=None):
 task=src.ordinary(task);d=src.read(task/'STAGE_COMPLETED.json');o=src.read(task/'STAGE_OBSERVED.json')
 adapter=completed_implementation_adapter(d['implementation']);request=src.verify(task,completed_adapter_sha256=adapter)
 if original_task_root is not None:src.need(str(original_task_root)==request['original_task_root'],'Single preserved originating source/capture context')
 src.need(d['schema']==COMPLETED and d['scope']==SCOPE and d['lane']==request['lane']and same(d['implementation'],o['implementation'])
  and d['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')and d['conditional_cover_arithmetic_completed']is True
  and all(d[k]is False for k in FLAGS),'Complete typed two-pass ledger, without support/parent/global promotion')
 summary=validate_run(task,o);src.need(same(d['summary'],summary)and same(d['artifacts'],inventory(task)),'Full original/provenance/port/stopped-output inventory')
 return dict(schema='REVALIDATED_CONDITIONAL_FINITE2630_COVERS_V1',lane=request['lane'],source_plan_sha256=src.PLAN_SHA256,
  stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),summary=summary,conditional_cover_arithmetic_completed=True,**{k:False for k in FLAGS})
