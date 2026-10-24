"""Pure evidence readback for56F; no original numerical module imports."""
from __future__ import annotations
from fractions import Fraction as F
import math
from pathlib import Path,PurePosixPath,PureWindowsPath
import re
from . import finite1014_coarse_sources as src
from .finite1039_count_evidence import same,mapped,terminal,inventory

SCOPE='UNCHANGED_CONDITIONAL_COARSE_SUPPORT10_14_BASIC_SUBLANE_V1'
OBSERVED='OBSERVED_FINITE1014_COARSE_SUPPORT_SUBLANE_V1'
COMPLETED='COMPLETED_FINITE1014_COARSE_SUPPORT_SUBLANE_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
FLAGS=('native_arithmetic_accepted','full_notebook56_completed','parent_acquisitions_verified',
       'support_high_initial_resource_acquired','support_acquisition_verified','resource_to_count217_interfaces_verified',
       'actual_support_acquired','physical_D_seed_used','cutoff10_claimed','all_index_conclusion_verified')
FLAGS+=('predecessor_caps_verified','owncap_proved','physical_defect_seed_imported','cutoff_proved')


NATIVE_STATUS='COMPLETE_CONDITIONAL_COARSE_SUPPORT10_14'
REPLAY_STATUS='PASS_FRESH_CONDITIONAL_COARSE_SUPPORT10_14_REPLAY'
BRIDGE='FRESH_COARSE_SUPPORT_CAPTURE_FROM_STOPPED_BASIC_V1'


def implementation():
    names=('finite1014_coarse.py','finite1014_coarse_sources.py','finite1014_coarse_evidence.py',
           'finite1039_sources.py','finite1039_count_evidence.py','n5_remaining_sources.py',
           'linux_supervisor.py','colab_batch.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)


def original_path(request,relative):
    root=request['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
    src.need(cls(root).is_absolute(),'Recorded absolute originating task root')
    return str(cls(root)/'capsule'/relative)


def command(request,action,python):
    src.need(action in src.ACTIONS and type(python)is str and (PureWindowsPath(python).is_absolute()or PurePosixPath(python).is_absolute()),'Exact original action/interpreter')
    return [python,'-B','construct.py'if action=='construct'else'replay.py']


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
             and mapped(task,launch['cwd'],original)==task/'capsule'/src.NATIVE
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
    action_cwd=task/'capsule'/src.NATIVE
    for packet,name in zip(checks,outputs):
        p=task/'capsule'/name;copied=directory/'checkpoints'/p.relative_to(action_cwd)
        src.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
                 and packet['exists']is True and packet['trusted_certificate']is False
                 and mapped(task,packet['source_path'],original)==p and mapped(task,packet['path'],original)==copied
                 and p.is_file()and copied.is_file()and type(packet['bytes'])is int
                 and packet['bytes']==p.stat().st_size==copied.stat().st_size
                 and packet['sha256']==src.digest(p)==src.digest(copied),'Whole stopped native output identity: '+name)
    return captures['stdout'].read_text('utf-8')


def inner_capture(task,request,action,report,observed,outer_stdout):
    c=Path(task)/'capsule';d=c/src.RUNS/src.LABELS[action];m=src.read(d/'metadata.json')
    name=src.OUTPUT_NAMES[action];p=c/src.NATIVE/name;execution=Path(task)/'executions'/action
    fields={'command','cwd','input_sha256','python','platform','started_utc','returncode','elapsed_seconds','finished_utc',
            'changed_inputs','stdout_sha256','stderr_sha256',name+'_sha256','capture_bridge'}
    src.need(set(m)==fields and same(m['command'],command(request,action,report['python_executable']))
             and m['cwd']==original_path(request,src.NATIVE)and same(m['input_sha256'],src.native_input_map(request))
             and m['python']==report['python_version']and m['platform']==report['platform']
             and type(m['platform'])is str and bool(m['platform'])and type(m['returncode'])is int and m['returncode']==0
             and same(m['elapsed_seconds'],observed['elapsed_seconds'])and m['changed_inputs']==[]
             and m[name+'_sha256']==src.digest(p),'Truthful current original-format capture and whole81-input source graph')
    for k in('started_utc','finished_utc'):src.need(type(m[k])is str and bool(m[k]),'Current capture time display')
    bridge=m['capture_bridge']
    src.need(type(bridge)is dict and set(bridge)=={'schema','action','writer_sha256','source_plan_sha256',
                                                 'outer_launch_sha256','outer_supervisor_result_sha256','outer_output_dir'}
             and bridge['schema']==BRIDGE and bridge['action']==action
             and bridge['writer_sha256']==implementation()['finite1014_coarse.py']and bridge['source_plan_sha256']==src.PLAN_SHA256
             and bridge['outer_launch_sha256']==src.digest(execution/'launch.json')
             and bridge['outer_supervisor_result_sha256']==src.digest(execution/'supervisor-result.json')
             and mapped(task,bridge['outer_output_dir'],request['original_task_root'])==execution,
             'Explicit new capture bridge binds actual stopped launch/result, never a historical execution hash')
    for kind in('stdout','stderr'):
        src.need(src.digest(d/(kind+'.txt'))==m[kind+'_sha256']==observed[kind+'_sha256'],
                 'Actual stopped outer bytes equal original-consumed capture stream')
    src.need((d/'stderr.txt').stat().st_size==0 and (d/'stdout.txt').read_text('utf-8')==outer_stdout,
             'Empty current stderr and whole truthful native stdout')
    return src.read(p,limit=128*src.MIB)


def summarize(task,request,report,stdout):
    c=Path(task)/'capsule';records={x['action']:x['observed']for x in report['actions']}
    native=inner_capture(task,request,'construct',report,records['construct'],stdout['construct'])
    fields={'status','n','radius','rho_interval','rows','predecessor_caps_verified','owncap_proved',
            'physical_defect_seed_imported','cutoff_proved','files_sha256'}
    src.need(set(native)==fields and native['status']==NATIVE_STATUS
             and same(native['n'],list(range(10,15)))and native['radius']=='3'
             and same(native['rho_interval'],['1','71/50'])
             and all(native[k]is False for k in('predecessor_caps_verified','owncap_proved','physical_defect_seed_imported','cutoff_proved'))
             and same(native['files_sha256'],request['sources']),
             'Whole unchanged-source conditional constructor output; no imported predecessor acceptance')
    candidate=c/src.NATIVE/'RESULT.json'
    src.need(stdout['construct'].splitlines()[-1:]==[NATIVE_STATUS+' '+src.digest(candidate)],'Actual native terminal and new candidate hash')
    wanted=[(n,b)for n in range(10,15)for b in src.plan()['bands']]
    src.need(type(native['rows'])is list and len(native['rows'])==10,'All ten index/band rows')
    for row,(n,band)in zip(native['rows'],wanted):
        q=str(n*(F(band['predecessor_cap'])-F(4097,10000)));beta=F(band['beta_upper']);proof=row['proof']
        src.need(set(row)=={'n','band','rho_interval','predecessor_cap','q','beta_upper','proof'}
                 and type(row['n'])is int and row['n']==n and row['band']==band['name']
                 and same(row['rho_interval'],band['rho_interval'])and row['predecessor_cap']==band['predecessor_cap']
                 and row['q']==q and row['beta_upper']==band['beta_upper']
                 and type(proof['n'])is int and proof['n']==n and proof['K']=='0'and proof['radius']=='3'
                 and type(proof['support_sign'])is int and proof['support_sign']==0
                 and proof['q_contact']==q and proof['rho_upper']==band['rho_interval'][1]
                 and same(proof['beta_interval'],[str(-beta),str(beta)])
                 and type(proof['ray_rows'])is list and len(proof['ray_rows'])==2
                 and same([r['sign']for r in proof['ray_rows']],[-1,1]),
                 'Literal indices, both closed rho bands, n-scaled predecessor allowance, signed beta and both full rays')
    result=src.read(c/src.RESULT,limit=128*src.MIB)
    fields={'status','n','rho_interval','radius','complete_index_band_rows','both_support_rays','full_threshold_line_and_tails',
            'candidate_sha256','malformed_controls','parser_controls','predecessor_caps_verified','cutoff_proved','files_sha256','execution_scope'}
    src.need(set(result)==fields and result['status']==REPLAY_STATUS and same(result['n'],list(range(10,15)))
             and same(result['rho_interval'],['1','71/50'])and result['radius']=='3'
             and type(result['complete_index_band_rows'])is int and result['complete_index_band_rows']==10
             and result['both_support_rays']is True and result['full_threshold_line_and_tails']is True
             and result['candidate_sha256']==src.digest(candidate)
             and type(result['malformed_controls'])is int and result['malformed_controls']==20
             and type(result['parser_controls'])is int and result['parser_controls']==2
             and result['predecessor_caps_verified']is False and result['cutoff_proved']is False,
             'Complete fresh original two-ray replay, full controls and explicitly conditional predecessor scope')
    replay=c/src.RESULT
    src.need(stdout['replay'].splitlines()[-1:]==[REPLAY_STATUS+' '+src.digest(replay)],'Whole actual replay terminal and output identity')
    graph=dict(request['sources']);graph[src.NATIVE+'/RESULT.json']=src.digest(candidate)
    for name in src.capture_paths('construct'):graph[name]=src.digest(c/name)
    src.need(same(result['files_sha256'],graph),'Complete81-source, actual new candidate and truthful current capture graph')
    found={p.relative_to(c).as_posix()for p in c.rglob('*')if p.is_file()}
    src.need(found==set(request['sources'])|{n for a in src.ACTIONS for n in src.generated_paths(a)},
             'Complete81-static-input capsule plus only declared genuine outputs')
    return dict(schema='CONDITIONAL_COARSE_SUPPORT10_14_ARITHMETIC_ONLY_V1',n=list(range(10,15)),radius='3',
                rho_interval=['1','71/50'],complete_index_band_rows=10,both_support_rays=True,full_threshold_line_and_tails=True,
                malformed_controls=20,parser_controls=2,source_plan_sha256=src.PLAN_SHA256,
                candidate_sha256=src.digest(candidate),replay_sha256=src.digest(replay),capture_bridge_schema=BRIDGE,
                conditional_premises=src.plan()['conditional_premises'],**{f:False for f in FLAGS})


def validate_run(task,report):
    task=Path(task);request=src.verify_job(task)
    src.need(report['schema']==OBSERVED and report['scope']==SCOPE and same(report['implementation'],implementation())
             and report['original_task_root']==request['original_task_root']
             and report['conditional_coarse_support_arithmetic_completed']is False and all(report[f]is False for f in FLAGS)
             and [x['action']for x in report['actions']]==list(src.ACTIONS),'Exact2-action observed-false implementation epoch')
    outputs={x['action']:transport(task,request,x['action'],x['observed'],report)for x in report['actions']}
    result=summarize(task,request,report,outputs);src.verify_job(task);return result


def validate_completed(task, *,original_task_root=None):
    task=Path(task);request=src.verify_job(task)
    src.need(original_task_root is None or str(original_task_root)==request['original_task_root'],'One original absolute task context')
    report=src.read(task/'STAGE_OBSERVED.json');complete=src.read(task/'STAGE_COMPLETED.json',limit=32*src.MIB)
    summary=validate_run(task,report)
    src.need(complete['schema']==COMPLETED and complete['scope']==SCOPE
             and same(complete['implementation'],report['implementation'])
             and complete['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')
             and complete['conditional_coarse_support_arithmetic_completed']is True and same(complete['summary'],summary)
             and same(complete['artifacts'],inventory(task))and all(complete[f]is False for f in FLAGS),
             'Both genuine stopped actions and exact source/capture/output inventory')
    return dict(schema='REVALIDATED_CONDITIONAL_COARSE_SUPPORT10_14_SUBLANE_V1',summary=summary,
                source_plan_sha256=src.PLAN_SHA256,stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),
                original_task_root=request['original_task_root'],conditional_coarse_support_arithmetic_completed=True,
                **{f:False for f in FLAGS})
