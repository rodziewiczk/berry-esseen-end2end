"""Pure57D stopped-evidence readback; no original numerical module imports."""
from __future__ import annotations
import math
from pathlib import Path,PureWindowsPath,PurePosixPath
import re
from . import finite1519_support_sources as src
from .finite1039_count_evidence import same,mapped,inventory
SCOPE='UNCHANGED_TWO_PASS_FULL_RAY_SUPPORT15_19_BASIC_V1'
OBSERVED='OBSERVED_FINITE1519_FULL_RAY_SUPPORT_V1'
COMPLETED='COMPLETED_FINITE1519_FULL_RAY_SUPPORT_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
FLAGS=('native_arithmetic_accepted','full_notebook57_completed','parent_acquisitions_verified',
 'support_acquisition_verified','support_high_initial_resource_acquired','resource_to_count147_interfaces_verified',
 'full_finite1039_verified','all_index_conclusion_verified')
def implementation():
 names=('finite1519_support.py','finite1519_support_sources.py','finite1519_support_evidence.py',
  'finite1039_sources.py','finite1039_count_evidence.py','n5_remaining_sources.py','linux_supervisor.py','colab_batch.py')
 return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)
def original_path(request,relative):
 root=request['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
 src.need(cls(root).is_absolute(),'Recorded absolute originating task root');return str(cls(root)/'capsule'/relative)
def command(request,action,python):
 src.need(action in src.ACTIONS and type(python)is str and(PureWindowsPath(python).is_absolute()or PurePosixPath(python).is_absolute()),'Exact original support action/interpreter')
 return[python,'-B','support_bridge.py'if action=='construct'else'check.py']
def finite(value):
    src.need(type(value)in(int,float)and math.isfinite(value)and value>=0,'Finite nonnegative execution display');return value


def transport(task,request,action,observed,report):
    task=Path(task);original=request['original_task_root'];directory=task/'executions'/action
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
    src.need(set(launch)==fields and same(launch['argv'],command(request,action,report['python_executable']))
             and mapped(task,launch['cwd'],original)==task/'capsule'/(src.NATIVE if action=='construct'else src.AUDIT)
             and mapped(task,launch['output_dir'],original)==directory and launch['mode']=='untrusted_search'
             and type(launch['cpu_seconds'])is int and launch['cpu_seconds']==CPU_SECONDS
             and type(launch['memory_bytes'])is int and launch['memory_bytes']==MEMORY_BYTES
             and type(launch['wall_seconds'])in(int,float)and launch['wall_seconds']==WALL_SECONDS
             and type(launch['disk_bytes'])is int and launch['disk_bytes']==512*src.MIB
             and type(launch['log_bytes'])is int and launch['log_bytes']==16*src.MIB
             and launch['sample_seconds']==.2 and launch['heartbeat_seconds']==20
             and type(launch['checkpoint_paths'])is list
             and [mapped(task,v,original)for v in launch['checkpoint_paths']]==[task/'capsule'/p for p in outputs],
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
        p=task/'capsule'/name;copied=directory/'checkpoints'/Path(name).relative_to(src.NATIVE if action=='construct'else src.AUDIT)
        src.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
                 and packet['exists']is True and packet['trusted_certificate']is False
                 and mapped(task,packet['source_path'],original)==p and mapped(task,packet['path'],original)==copied
                 and p.is_file()and copied.is_file()and type(packet['bytes'])is int
                 and packet['bytes']==p.stat().st_size==copied.stat().st_size
                 and packet['sha256']==src.digest(p)==src.digest(copied),'Whole stopped native output identity: '+name)
    return captures['stdout'].read_text('utf-8')



def constructor_metadata(task,request,report,observed):
 """New explicit capture epoch, derived only after actual stopped transport."""
 c=Path(task)/'capsule';launch=src.read(Path(task)/'executions/construct/launch.json')
 sources=src.plan()['source_files'];prefix=src.NATIVE+'/'
 inputs={n[len(prefix):]:r['sha256']for n,r in sources.items()if n.startswith(prefix)}
 return dict(schema='CURRENT_STOPPED_SUPPORT_CONSTRUCTOR_CAPTURE_V1',command=launch['argv'],cwd=launch['cwd'],
  returncode=observed['returncode'],python=report['python_version'],input_sha256=inputs,
  stdout_sha256=observed['stdout_sha256'],stderr_sha256=observed['stderr_sha256'],
  candidate_sha256=src.digest(c/src.CANDIDATE),supervisor_result_sha256=src.digest(Path(task)/'executions/construct/supervisor-result.json'),
  scope='Genuine stopped current BASIC execution; no historical guard or capture claim',proof_accepted=False)

def summarize(task,request,report,stdout):
 c=Path(task)/'capsule';d=src.plan();candidate=src.read(c/src.CANDIDATE)
 src.need(src.digest(c/src.CANDIDATE)==d['original_candidate_sha256'],'Fresh deterministic support candidate equals original exact commitment')
 src.need(candidate['schema']=='CONDITIONAL_ACTUAL15_19_SUPPORT_BRIDGE_V1'and candidate['status']=='FRESH_CONDITIONAL_SUPPORT_ALL_ROWS'
  and candidate['rho_interval']==['1','33/25']and candidate['radius']=='3'and type(candidate['rows'])is list
  and len(candidate['rows'])==5 and [x['n']for x in candidate['rows']]==list(range(15,20))
  and all(type(x['n'])is int and x['status']=='CONDITIONAL_FULL_RAY_SUPPORT'for x in candidate['rows'])
  and same(candidate['files_sha256'],d['original_candidate_source_graph'])
  and all(candidate[k]is False for k in('predecessor_verified','retained_contact_framework_verified_here','cutoff15_proved')),
  'Complete conditional five-index support candidate and explicit unacquired premises')
 expected_lines=[str(n)+' CONDITIONAL_FULL_RAY_SUPPORT'for n in range(15,20)]+['FRESH_CONDITIONAL_SUPPORT_ALL_ROWS '+d['original_candidate_sha256']]
 src.need(stdout['construct'].splitlines()==expected_lines,'Whole actual original constructor terminal and per-index statuses')
 observed=report['actions'][0]['observed'];meta=src.read(c/src.RUNS/'metadata.json')
 src.need(same(meta,constructor_metadata(task,request,report,observed)),'Fresh capture is exactly derived from the actual stopped constructor')
 for name in('stdout','stderr'):
  src.need(src.digest(c/src.RUNS/(name+'.txt'))==observed[name+'_sha256']
   and(c/src.RUNS/(name+'.txt')).read_bytes()==(Path(task)/'executions/construct'/(name+'.txt')).read_bytes(),'Copied genuine constructor streams')
 src.need((c/src.RUNS/'stderr.txt').stat().st_size==0,'Actual constructor stderr empty')
 for name in src.ENGINES:
  src.need(src.digest(c/src.AUDIT/'engine'/name)==src.digest(c/src.NATIVE/name),'Replay uses exact freshly copied support helper')
 result=src.read(c/src.RESULT)
 fields={'status','n_values','rho_interval','radius','candidate_sha256','full_ray_rows','malformed_controls','parser_controls',
  'predecessor_premise_discharged_here','execution_scope','files_sha256'}
 src.need(set(result)==fields and result['status']=='PASS_FRESH_ACTUAL15_19_TWO_RAY_SUPPORT_REPLAY_CONDITIONAL'
  and same(result['n_values'],list(range(15,20)))and result['rho_interval']==['1','33/25']and result['radius']=='3'
  and result['candidate_sha256']==d['original_candidate_sha256']and type(result['full_ray_rows'])is int and result['full_ray_rows']==10
  and type(result['malformed_controls'])is int and result['malformed_controls']==14
  and type(result['parser_controls'])is int and result['parser_controls']==2
  and result['predecessor_premise_discharged_here']is False
  and result['execution_scope']=='Fresh exact full-object reproduction with byte-identical copied arithmetic helpers; independent driver and scalar reconstruction, not an independent Gaussian arithmetic implementation.',
  'Full unchanged two-ray replay and complete14+2 controls, without parent promotion')
 graph={src.CANDIDATE:d['original_candidate_sha256']}|d['original_candidate_source_graph']
 for name in src.capture_paths()+[src.NATIVE+'/'+name for name in meta['input_sha256']]+[src.AUDIT+'/engine/'+name for name in src.ENGINES]+[src.AUDIT+'/check.py',src.AUDIT+'/PROOF.txt']:
  graph[name]=src.digest(c/name)
 src.need(same(result['files_sha256'],graph),'Exact replay source/current-capture graph, not a subset')
 for name,pin in graph.items():src.need(src.digest(c/name)==pin,'Replay graph bound to actual bytes')
 src.need(stdout['replay']=='PASS_FRESH_ACTUAL15_19_TWO_RAY_SUPPORT_REPLAY_CONDITIONAL '+src.digest(c/src.RESULT)+'\n','Actual replay stdout binds complete saved result')
 return dict(n_values=list(range(15,20)),rho_interval=['1','33/25'],radius='3',full_ray_rows=10,malformed_controls=14,parser_controls=2,
  candidate_sha256=src.digest(c/src.CANDIDATE),receipt_sha256=src.digest(c/src.RESULT),constructor_capture_sha256=src.digest(c/src.RUNS/'metadata.json'),
  predecessor_premise_discharged_here=False,original_programs_unchanged=True)

def validate_run(task,report):
 task=src.ordinary(task);request=src.verify_job(task)
 src.need(report['schema']==OBSERVED and report['scope']==SCOPE and report['original_task_root']==request['original_task_root']
  and same(report['implementation'],implementation())and type(report['python_version'])is str and bool(report['python_version'])
  and report['conditional_support_arithmetic_completed']is False and all(report[k]is False for k in FLAGS),'Exact current support implementation and unaccepted observed ledger')
 actions=report['actions'];src.need(type(actions)is list and[action['action']for action in actions]==list(src.ACTIONS),'Both mandatory original support passes')
 stdout={a['action']:transport(task,request,a['action'],a['observed'],report)for a in actions}
 return summarize(task,request,report,stdout)

def validate_completed(task, *,original_task_root=None):
 task=src.ordinary(task);m=src.verify_job(task)
 if original_task_root is not None:src.need(str(original_task_root)==m['original_task_root'],'Single preserved original capture root')
 p=src.read(task/'STAGE_COMPLETED.json');o=src.read(task/'STAGE_OBSERVED.json')
 src.need(p['schema']==COMPLETED and p['scope']==SCOPE and same(p['implementation'],implementation())
  and p['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')and p['conditional_support_arithmetic_completed']is True
  and all(p[k]is False for k in FLAGS),'Exact complete support ledger, with no acquisition/global promotion')
 summary=validate_run(task,o)
 src.need(same(p['summary'],summary)and same(p['artifacts'],inventory(task)),'Whole completed source/capture/native-output inventory')
 return dict(schema='REVALIDATED_CONDITIONAL_SUPPORT15_19_V1',source_plan_sha256=src.PLAN_SHA256,
  stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),summary=summary,conditional_support_arithmetic_completed=True,
  **{k:False for k in FLAGS})
