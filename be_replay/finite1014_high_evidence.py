"""Pure evidence readback for56E; no original numerical module imports."""
from __future__ import annotations
from fractions import Fraction as F
import math
from pathlib import Path,PurePosixPath,PureWindowsPath
import re
from . import finite1014_high_sources as src
from .finite1039_count_evidence import same,mapped,terminal,inventory

SCOPE='UNCHANGED_CONDITIONAL_SUPPORTED_HIGH10_14_FOURIER_BASIC_SUBLANE_V1'
OBSERVED='OBSERVED_FINITE1014_HIGH_SUBLANE_V1'
COMPLETED='COMPLETED_FINITE1014_HIGH_SUBLANE_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
FLAGS=('native_arithmetic_accepted','full_notebook56_completed','parent_acquisitions_verified',
       'support_high_initial_resource_acquired','support_acquisition_verified','resource_to_count217_interfaces_verified',
       'actual_support_acquired','physical_D_seed_used','cutoff10_claimed','all_index_conclusion_verified')


NATIVE_STATUS='EXACT_MOMENT_CENTERED_HIGH10_DIAGNOSTIC_COMPLETE_NOT_SELECTED_ACCEPTANCE'
READBACK_STATUS='PASS_SUPPORTED_MOMENT_CENTERED_HIGH10_14_COMPLETE_NATIVE_REPLAY_AND_BOUNDED_INDEPENDENT_AUDIT'
BRIDGE='FRESH_SUPPORTED_HIGH_CAPTURE_FROM_STOPPED_BASIC_V1'
COUNTS=dict(moment_identities=3,ratio_derivatives=2,finite_law_moment_controls=24,moment_endpoint_controls=1,
            independent_centered_point_controls=1152,finite_law_HIGH_controls=1200,exact_power_controls=35,
            full_weight_meshes=2,domain_negative_controls=17,result_negative_controls=22,complete_native_captures=2)


def implementation():
    names=('finite1014_high.py','finite1014_high_sources.py','finite1014_high_evidence.py',
           'finite1039_sources.py','finite1039_count_evidence.py','n5_remaining_sources.py',
           'linux_supervisor.py','colab_batch.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)


def original_path(request,relative):
    root=request['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
    src.need(cls(root).is_absolute(),'Recorded absolute originating task root')
    return str(cls(root)/'capsule'/relative)


def command(request,action,python):
    src.need(action in src.ACTIONS and type(python)is str and (PureWindowsPath(python).is_absolute()or PurePosixPath(python).is_absolute()),'Exact original action/interpreter')
    if action=='readback':return [python,'-B','check.py']
    return [python,'-B','bound.py',src.OUTPUT_NAMES[action]]


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
             and mapped(task,launch['cwd'],original)==task/'capsule'/(src.AUDIT if action=='readback'else src.NATIVE)
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
    action_cwd=task/'capsule'/(src.AUDIT if action=='readback'else src.NATIVE)
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
             and m[name+'_sha256']==src.digest(p),'Truthful current original-format capture and whole98-input source graph')
    for k in('started_utc','finished_utc'):src.need(type(m[k])is str and bool(m[k]),'Current capture time display')
    bridge=m['capture_bridge']
    src.need(type(bridge)is dict and set(bridge)=={'schema','action','writer_sha256','source_plan_sha256',
                                                 'outer_launch_sha256','outer_supervisor_result_sha256','outer_output_dir'}
             and bridge['schema']==BRIDGE and bridge['action']==action
             and bridge['writer_sha256']==implementation()['finite1014_high.py']and bridge['source_plan_sha256']==src.PLAN_SHA256
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
    native=[inner_capture(task,request,a,report,records[a],stdout[a])for a in('construct','replay')]
    for action in('construct','replay'):
        src.need(stdout[action].splitlines()[-1:]==[NATIVE_STATUS],
                 'Original native success terminal, not merely a zero process return code')
    src.need((c/src.NATIVE/'RESULT.json').read_bytes()==(c/src.NATIVE/'REPLAY_RESULT.json').read_bytes(),
             'Complete byte-identical current native construction and replay')
    expected=[(b['name'],b['rho_upper'],b['support_radius'],mesh)for b in src.plan()['bands']for mesh in(512,1024)]
    for packet in native:
        src.need(set(packet)=={'status','n','attempts','pi','manifest_sha256','scope'}and packet['status']==NATIVE_STATUS
                 and same(packet['n'],list(range(10,15)))and packet['manifest_sha256']==src.plan()['original_manifest_sha256']
                 and type(packet['attempts'])is list and len(packet['attempts'])==4,
                 'Full original supported-HIGH diagnostic output, without a selected/global inference')
        for attempt,(band,rho,radius,mesh)in zip(packet['attempts'],expected):
            src.need(attempt['name']==band and attempt['rho_upper']==rho and attempt['support_radius']==radius
                     and type(attempt['mesh'])is int and attempt['mesh']==mesh
                     and type(attempt['all_cells'])is int and attempt['all_cells']==mesh
                     and type(attempt['rows'])is list and len(attempt['rows'])==5
                     and same([r['n']for r in attempt['rows']],list(range(10,15))),
                     'Every literal band/complete512and1024mesh and all five native indices')
    result=src.read(c/src.RESULT,limit=128*src.MIB)
    fields={'status','mathematical_status','execution_status','n','rows','counts','independent_closed_cells','cell_tests',
            'complete_native_rows','selected_fixed_target_rows','full_integrations_in_this_readback',
            'actual_support_acquired','physical_D_seed_used','cutoff10_claimed','files_sha256'}
    src.need(set(result)==fields and result['status']==READBACK_STATUS and same(result['n'],list(range(10,15)))
             and same(terminal(stdout['readback']),{k:v for k,v in result.items()if k not in('files_sha256','cell_tests','rows')})
             and same(result['counts'],COUNTS)and type(result['independent_closed_cells'])is int and result['independent_closed_cells']==64
             and type(result['cell_tests'])is list and len(result['cell_tests'])==64
             and type(result['complete_native_rows'])is int and result['complete_native_rows']==20
             and type(result['selected_fixed_target_rows'])is int and result['selected_fixed_target_rows']==10
             and type(result['full_integrations_in_this_readback'])is int and result['full_integrations_in_this_readback']==0
             and all(result[k]is False for k in('actual_support_acquired','physical_D_seed_used','cutoff10_claimed')),
             'Whole actual original HIGH readback, every bounded control and honest unacquired support/cutoff scope')
    wanted=[(b,n)for b in src.plan()['bands']for n in range(10,15)]
    src.need(type(result['rows'])is list and len(result['rows'])==10,'All ten selected supported-HIGH rows')
    for row,(band,n)in zip(result['rows'],wanted):
        src.need(set(row)=={'band','n','rho_upper','support_radius','upper','target'}and row['band']==band['name']
                 and type(row['n'])is int and row['n']==n and row['rho_upper']==band['rho_upper']
                 and row['support_radius']==band['support_radius']and row['target']==band['target']
                 and type(row['upper'])is str and str(F(row['upper']))==row['upper']and 0<=F(row['upper'])<F(band['target']),
                 'Exact selected same-law radius/rho/n/target interfaces, without support acquisition')
    graph=dict(src.read(c/src.NATIVE/'MANIFEST.json')['files_sha256'])
    names=[src.NATIVE+'/MANIFEST.json',src.NATIVE+'/RESULT.json',src.NATIVE+'/REPLAY_RESULT.json',src.AUDIT+'/check.py',src.AUDIT+'/REVIEW.txt']
    names += [src.AUDIT+'/engine/'+n for n in src.ENGINE_NAMES]
    names += [n for a in('construct','replay')for n in src.capture_paths(a)]
    for n in names:graph[n]=src.digest(c/n)
    src.need(same(result['files_sha256'],graph),'Complete unchanged95-source and current result/engine/capture graph')
    for n in src.ENGINE_NAMES:src.need(src.digest(c/src.AUDIT/'engine'/n)==src.digest(c/src.NATIVE/n),'Actual unchanged readback engine copy')
    found={p.relative_to(c).as_posix()for p in c.rglob('*')if p.is_file()}
    src.need(found==set(request['sources'])|{n for a in src.ACTIONS for n in src.generated_paths(a)},
             'Complete98-static-input capsule plus only declared current outputs')
    return dict(schema='CONDITIONAL_SUPPORTED_HIGH10_14_ARITHMETIC_ONLY_V1',n=list(range(10,15)),
                complete_attempts=4,complete_native_rows=20,selected_fixed_target_rows=10,rows=result['rows'],
                counts=COUNTS,independent_closed_cells=64,full_integrations_in_readback=0,
                original_manifest_sha256=src.plan()['original_manifest_sha256'],source_plan_sha256=src.PLAN_SHA256,
                readback_sha256=src.digest(c/src.RESULT),capture_bridge_schema=BRIDGE,
                conditional_premises=['Same-law support23/10 for rho<=11/10 and12/5 for rho<=23/20 must be acquired separately',
                                      'Retained universal CF/kappa and supported-HIGH analytic lemmas'],**{f:False for f in FLAGS})


def validate_run(task,report):
    task=Path(task);request=src.verify_job(task)
    src.need(report['schema']==OBSERVED and report['scope']==SCOPE and same(report['implementation'],implementation())
             and report['original_task_root']==request['original_task_root']
             and report['conditional_supported_high_arithmetic_completed']is False and all(report[f]is False for f in FLAGS)
             and [x['action']for x in report['actions']]==list(src.ACTIONS),'Exact3-action observed-false implementation epoch')
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
             and complete['conditional_supported_high_arithmetic_completed']is True and same(complete['summary'],summary)
             and same(complete['artifacts'],inventory(task))and all(complete[f]is False for f in FLAGS),
             'All three genuine stopped actions and exact source/capture/output inventory')
    return dict(schema='REVALIDATED_CONDITIONAL_HIGH10_14_SUBLANE_V1',summary=summary,
                source_plan_sha256=src.PLAN_SHA256,stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),
                original_task_root=request['original_task_root'],conditional_supported_high_arithmetic_completed=True,
                **{f:False for f in FLAGS})
