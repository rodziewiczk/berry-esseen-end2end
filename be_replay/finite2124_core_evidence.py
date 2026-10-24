"""Pure full-output/capture readback for58B/C; no original mathematical imports."""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import math
from pathlib import Path,PurePosixPath,PureWindowsPath
import re
from . import finite2124_core_sources as src
from .finite1039_count_evidence import same,mapped,inventory

SCOPE='UNCHANGED_ACTUAL21_24_INITIAL_RESOURCE_BASIC_CURRENT_REVIEW_EPOCH_V1'
OBSERVED='OBSERVED_ACTUAL21_24_CORE_CASE_V1'
COMPLETED='COMPLETED_ACTUAL21_24_CORE_CASE_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
FLAGS=('native_arithmetic_accepted','full_notebook58_completed','full_actual20_24_verified','predecessor_verified',
       'historical_fourier_replayed','parent_acquisitions_verified','resource_count_join_verified',
       'sharp20_proved','global_bound_proved','cutoff20_proved','all_index_conclusion_verified')
INITIAL_CANDIDATE='CONDITIONAL_ACTUAL_INDEX_INITIAL_FULL_CANDIDATE'
INITIAL_ACCEPTED='PASS_FRESH_FULL_CONDITIONAL_ACTUAL21_24_INITIAL_REPLAY'
RESOURCE_CANDIDATE='COMPLETE_CONDITIONAL_ACTUAL21_24_RESOURCE_INVENTORY'
RESOURCE_ACCEPTED='PASS_FRESH_FULL_CONDITIONAL_ACTUAL21_24_RESOURCE_REPLAY'
CAPTURE='ACTUAL21_24_INITIAL_STOPPED_BASIC_CAPTURE_V1'

def implementation():
    names=('finite2124_core.py','finite2124_core_sources.py','finite2124_core_evidence.py',
           'finite1039_sources.py','finite1039_count_evidence.py','n5_remaining_sources.py','linux_supervisor.py','colab_batch.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)

def finite(v):
    src.need(type(v)in(int,float)and math.isfinite(v)and v>=0,'Finite nonnegative execution metadata');return v

def original_path(request,relative):
    root=request['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
    src.need(cls(root).is_absolute(),'One absolute originating task root');return str(cls(root)/'capsule'/relative)

def command(request,action,python):
    src.need(action in src.ACTIONS and type(python)is str and(PureWindowsPath(python).is_absolute()or PurePosixPath(python).is_absolute()),'Literal stage/interpreter')
    initial=action.startswith('initial_');folder=src.INITIAL if initial else src.RESOURCE
    script=folder+('/initial.py'if initial else'/resources_v2.py')
    review=src.INITIAL_REVIEW if initial else src.review_paths(request['n'],request['band'])[0]
    return [python,'-B','-u',original_path(request,script),action.split('_')[1],str(request['n']),request['band'],original_path(request,review)]

def transport(task,request,action,observed,context):
    task=Path(task);old=request['original_task_root'];d=task/'executions'/action
    src.need(same(src.read(d/'supervisor-result.json'),observed)and observed.get('status')=='completed'
             and type(observed.get('returncode'))is int and observed['returncode']==0 and observed.get('reason')is None
             and observed.get('mode')=='untrusted_search'and observed.get('proof_accepted')is False
             and type(observed.get('sample_count'))is int and observed['sample_count']>0,'Actual completed stopped BASIC stage')
    for key in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):finite(observed[key])
    launch=src.read(d/'launch.json');cwd=task/'capsule'/(src.INITIAL if action.startswith('initial_')else src.RESOURCE)
    fields={'argv','cwd','output_dir','mode','wall_seconds','cpu_seconds','memory_bytes','checkpoint_paths',
            'disk_bytes','log_bytes','sample_seconds','heartbeat_seconds'}
    outputs=src.output_paths(action,request['n'],request['band'])
    src.need(set(launch)==fields and same(launch['argv'],command(request,action,context['python_executable']))
             and mapped(task,launch['cwd'],old)==cwd and mapped(task,launch['output_dir'],old)==d
             and launch['mode']=='untrusted_search'and type(launch['cpu_seconds'])is int and launch['cpu_seconds']==CPU_SECONDS
             and type(launch['memory_bytes'])is int and launch['memory_bytes']==MEMORY_BYTES
             and type(launch['wall_seconds'])in(int,float)and launch['wall_seconds']==WALL_SECONDS
             and type(launch['disk_bytes'])is int and launch['disk_bytes']==512*src.MIB
             and type(launch['log_bytes'])is int and launch['log_bytes']==16*src.MIB
             and launch['sample_seconds']==.2 and launch['heartbeat_seconds']==20
             and type(launch['checkpoint_paths'])is list
             and [mapped(task,p,old)for p in launch['checkpoint_paths']]==[task/'capsule'/p for p in outputs],
             'Exact original argv/cwd/review epoch, complete stopped outputs and BASIC budgets')
    scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(WALL_SECONDS),
        per_process_RLIMIT_AS_bytes=MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=CPU_SECONDS,aggregate_kernel_memory_limit=False,
        aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY_BYTES,sampled_group_CPU_limit_seconds=CPU_SECONDS,
        sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,descendants_changing_session_are_contained=False,
        equivalent_to_Windows_Job_or_cgroup=False)
    src.need(same(observed['guard_scope'],scope),'Honest BASIC whole process-group scope, without native promotion')
    for kind in('stdout','stderr'):
        p=mapped(task,observed[kind+'_path'],old)
        src.need(p==d/(kind+'.txt')and p.is_file()and p.stat().st_size<=16*src.MIB
                 and src.digest(p)==observed[kind+'_sha256'],'Actual entire current '+kind)
    src.need((d/'stderr.txt').stat().st_size==0,'Empty successful original stderr')
    copies=observed['checkpoints'];src.need(type(copies)is list and len(copies)==len(outputs),'All whole output copies present')
    for packet,name in zip(copies,outputs):
        p=task/'capsule'/name;copy=d/'checkpoints'/p.relative_to(cwd)
        src.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
                 and packet['exists']is True and packet['trusted_certificate']is False
                 and mapped(task,packet['source_path'],old)==p and mapped(task,packet['path'],old)==copy
                 and p.is_file()and copy.is_file()and type(packet['bytes'])is int
                 and packet['bytes']==p.stat().st_size==copy.stat().st_size and packet['sha256']==src.digest(p)==src.digest(copy),
                 'Whole stopped output identity and actual cwd-relative capture layout')
    return (d/'stdout.txt').read_text('utf-8')

def initial_capture(task,request,action,observed,context):
    c=Path(task)/'capsule';n,b=request['n'],request['band'];folder=c/src.INITIAL/'captures'/(src.case(n,b)+'_'+action.split('_')[1])
    m=src.read(folder/'EXECUTION.json');execution=Path(task)/'executions'/action
    output=c/src.output_paths(action,n,b)[0]
    fields={'schema','status','n','band','action','command','cwd','started_utc','finished_utc','elapsed_seconds',
        'timeout_seconds','returncode','timed_out','executable_sha256','python_version','platform','source_freeze_sha256',
        'source_review_sha256','launcher_sha256','stdout_sha256','stderr_sha256','result_sha256','capture_bridge'}
    src.need(set(m)==fields and m['schema']==CAPTURE and m['status']=='COMPLETED'and type(m['n'])is int and m['n']==n
             and m['band']==b and m['action']==action.split('_')[1]and same(m['command'],command(request,action,context['python_executable']))
             and m['cwd']==original_path(request,src.INITIAL)and type(m['returncode'])is int and m['returncode']==0 and m['timed_out']is False
             and same(m['elapsed_seconds'],observed['elapsed_seconds'])and type(m['timeout_seconds'])is int and m['timeout_seconds']==WALL_SECONDS
             and m['executable_sha256']==context['python_executable_sha256']and m['python_version']==context['python_version']and m['platform']==context['platform']
             and m['source_freeze_sha256']==src.INITIAL_FREEZE and m['source_review_sha256']==src.digest(c/src.INITIAL_REVIEW)
             and m['launcher_sha256']==implementation()['finite2124_core.py']and m['result_sha256']==src.digest(output),
             'Genuine current INITIAL capture; exact status/cwd/argv/source/review/result/interpreter')
    for key in('started_utc','finished_utc'):src.need(type(m[key])is str and bool(m[key]),'Current capture time display')
    bridge=dict(schema='ACTUAL21_24_INITIAL_CAPTURE_OUTER_BINDING_V1',action=action,n=n,band=b,source_plan_sha256=src.PLAN_SHA256,
        launch_sha256=src.digest(execution/'launch.json'),supervisor_result_sha256=src.digest(execution/'supervisor-result.json'),
        source_files_sha256=request['sources'])
    src.need(same(m['capture_bridge'],bridge),'Typed bridge binds actual stopped launch/result and complete immutable input graph')
    for kind in('stdout','stderr'):
        src.need(src.digest(folder/(kind+'.txt'))==m[kind+'_sha256']==observed[kind+'_sha256']
                 and(folder/(kind+'.txt')).read_bytes()==(execution/(kind+'.txt')).read_bytes(),'Entire original-consumed streams are actual stopped outer bytes')

def cover(packet):
    src.need(type(packet['total'])is int and packet['total']==2592
             and type(packet['active'])is int and type(packet['excluded'])is int and packet['active']>=0 and packet['excluded']>=0
             and packet['active']+packet['excluded']==2592 and type(packet['reasons'])is dict
             and all(type(x)is int and x>=0 for x in packet['reasons'].values())and sum(packet['reasons'].values())==packet['excluded'],
             'Every complete signed2592-cell cover accounted')

def validate_initial(task,request,context,records):
    c=Path(task)/'capsule';n,b=request['n'],request['band'];folder=c/src.INITIAL/src.case(n,b)
    z,a=src.read(folder/'CANDIDATE.json',limit=128*src.MIB),src.read(folder/'ACCEPTED.json')
    rho,radius=src.BANDS[b];req=dict(n=n,nmax=n,K='0',q='0',owncap='419/1000',band=b,rho_interval=rho,radius=radius,grid=[12,12,6,3])
    fields={'status','request','beta_upper','support','profile','stages','export','final_invariants','predecessor_verified','owncap_source','sharp20_proved','cutoff20_proved','source_freeze_sha256'}
    src.need(set(z)==fields and z['status']==INITIAL_CANDIDATE and same(z['request'],req)
             and z['source_freeze_sha256']==src.INITIAL_FREEZE and all(z[k]is False for k in('predecessor_verified','sharp20_proved','cutoff20_proved')),
             'Exact literal full fresh INITIAL candidate and conditional zero allowance')
    beta=F(z['beta_upper']);src.need(str(beta)==z['beta_upper']and 0<beta<1,'Canonical signed beta enclosure')
    profile=dict(n=n,nmax=n,radius=radius,radius_minus=radius,radius_plus=radius,cap='419/1000',barrier='0',grid=[12,12,6,3],
                 invariants=dict(rho=rho[1],rho_lo=rho[0],beta_lo=str(-beta),beta_hi=str(beta)))
    support=z['support']
    src.need(same(z['profile'],profile)and type(support['n'])is int and support['n']==n and support['K']==support['q_contact']=='0'
             and support['radius']==radius and type(support['support_sign'])is int and support['support_sign']==0
             and support['rho_upper']==rho[1]and same(support['beta_interval'],[str(-beta),str(beta)])
             and same([x['sign']for x in support['ray_rows']],[-1,1]),'Same-law profile and both complete signed support rays')
    src.need(type(z['stages'])is list and len(z['stages'])==8,'Eight genuine INITIAL refinements before ninth export')
    raw=d=None
    for stage in z['stages']:
        src.need(set(stage)=={'input_raw','input_D','next_raw','next_D','cover'}and same(stage['input_raw'],raw)and same(stage['input_D'],d),'Exact staged invariant chain')
        cover(stage['cover']);raw,d=stage['next_raw'],stage['next_D'];src.need(0<F(raw)<F(2,5)*n and 0<F(d)<6,'Original positive INITIAL invariant range')
    cover(z['export']);src.need(same(z['final_invariants'],dict(raw=raw,D=d))and type(z['export']['panels'])is list and len(z['export']['panels'])==100,'Ninth full cover and complete invariant/panel export')
    for i,row in enumerate(z['export']['panels']):src.need(row['pl']==str(F(i,100))and row['pu']==str(F(i+1,100)),'All100 ordered original closed p panels')
    fields={'status','n','band','request','candidate_sha256','source_freeze_sha256','source_review_sha256','negative_controls','final_invariants',
            'fresh_support_calls','fresh_complete_signed_covers','signed_cells_per_cover','original_probability_panels','predecessor_verified','sharp20_proved','cutoff20_proved','elapsed_seconds'}
    src.need(set(a)==fields and a['status']==INITIAL_ACCEPTED and type(a['n'])is int and a['n']==n and a['band']==b and same(a['request'],req)
             and a['candidate_sha256']==src.digest(folder/'CANDIDATE.json')and a['source_freeze_sha256']==src.INITIAL_FREEZE
             and a['source_review_sha256']==src.digest(c/src.INITIAL_REVIEW)and same(a['negative_controls'],src.plan()['initial_negative_controls'])
             and same(a['final_invariants'],z['final_invariants'])and all(a[k]is False for k in('predecessor_verified','sharp20_proved','cutoff20_proved')),
             'Whole genuine INITIAL acceptance with exact source/review/candidate/control bindings')
    for key,value in dict(fresh_support_calls=1,fresh_complete_signed_covers=9,signed_cells_per_cover=2592,original_probability_panels=100).items():
        src.need(type(a[key])is int and a[key]==value,'Complete original INITIAL census')
    finite(a['elapsed_seconds'])
    for action,label in(('initial_construct','CANDIDATE_STORED'),('initial_accept','ACCEPTED_STORED')):
        text=transport(task,request,action,records[action],context);initial_capture(task,request,action,records[action],context)
        output=c/src.output_paths(action,n,b)[0]
        src.need(text.splitlines()[-1:]==[label+' '+str(n)+' '+b+' '+src.digest(output)],'Actual INITIAL success terminal and whole current output hash')
    return z,a

def resource_graph(task,request):
    c=Path(task)/'capsule';g=dict(src.read(c/src.RESOURCE/'FROZEN_SOURCES_V2.json')['files_sha256'])
    other=dict(src.read(c/src.INITIAL/'FROZEN_SOURCES.json')['files_sha256']);other.update(src.fresh_parent_graph(task,request['n'],request['band']))
    for name in(src.INITIAL+'/FROZEN_SOURCES.json',src.INITIAL_REVIEW,src.review_paths(request['n'],request['band'])[0],src.RESOURCE+'/FROZEN_SOURCES_V2.json'):other[name]=src.digest(c/name)
    for name,pin in other.items():src.need(name not in g or g[name]==pin,'Exact common parent/source binding');g[name]=pin
    return g

def summarize(task,report):
    task=Path(task);request=src.verify_job(task);n,b=request['n'],request['band'];c=task/'capsule';folder=c/src.RESOURCE/src.case(n,b)
    records={x['action']:x['observed']for x in report['actions']};initial,ia=validate_initial(task,request,report,records)
    bridge=src.verify_review_epoch(task,n,b);graph=resource_graph(task,request)
    candidate=src.read(folder/'CANDIDATE.json',limit=128*src.MIB);accepted=src.read(folder/'ACCEPTED.json',limit=128*src.MIB)
    fields={'status','n','K','q','owncap','band','rho_interval','rows','status_counts','initial_candidate_sha256','initial_acceptance_sha256',
            'support','files_sha256','predecessor_verified','global_bound_proved','cutoff20_proved'}
    src.need(set(candidate)==fields and candidate['status']==RESOURCE_CANDIDATE and type(candidate['n'])is int and candidate['n']==n
             and candidate['K']==candidate['q']=='0'and candidate['owncap']=='419/1000'and candidate['band']==b and same(candidate['rho_interval'],src.BANDS[b][0])
             and candidate['initial_candidate_sha256']==src.digest(c/src.INITIAL/src.case(n,b)/'CANDIDATE.json')
             and candidate['initial_acceptance_sha256']==src.digest(c/src.INITIAL/src.case(n,b)/'ACCEPTED.json')and same(candidate['files_sha256'],graph)
             and all(candidate[k]is False for k in('predecessor_verified','global_bound_proved','cutoff20_proved')),'Whole literal fresh resource inventory and actual complete INITIAL edge')
    normalized=deepcopy(initial['support']);normalized['schema']='DIRECT_FIXED_INDEX_GAUSSIAN_SUPPORT_V1';normalized['q']=normalized.pop('q_contact')
    normalized['scope']='Attained positive closed maximizer at the stated fixed index, C_n>=CE+K/n and delta_n<=q, with any additionally declared same-law moment caps. Excludes every support point on the specified full ray(s), uniformly in H. This is not a score exclusion.'
    src.need(initial['support']['schema']=='DIRECT_SAME_LAW_CONTACT_SUPPORT_DISCOVERY_V1'and same(candidate['support'],normalized),'Exact original support-schema translation, all arithmetic payload preserved')
    src.need(type(candidate['rows'])is list and len(candidate['rows'])==100,'All100 actual resource rows')
    statuses=[]
    for i,desc in enumerate(candidate['rows']):
        path='rows/'+format(i,'03d')+'.json';row=src.read(folder/path,limit=128*src.MIB)
        src.need(set(desc)=={'n','band','index','p','path','sha256','status'}and type(desc['n'])is int and desc['n']==n and desc['band']==b
                 and type(desc['index'])is int and desc['index']==i and same(desc['p'],[str(F(i,100)),str(F(i+1,100))])
                 and desc['path']==path and desc['sha256']==src.digest(folder/path)and row['status']==desc['status'],
                 'Every literal whole resource row, closed endpoint and actual file binding')
        source=deepcopy(initial['export']['panels'][i]);source['rho_lo']=src.BANDS[b][0][0]
        src.need(type(row['n'])is int and row['n']==n and row['band']==b and type(row['index'])is int and row['index']==i
                 and same(row['source'],source),'Full resource source is the same fresh INITIAL panel')
        status=row['status'];src.need(status in('EXCLUDED_BY_SAME_LAW_RESOURCE','RESOURCE_ROW_ACQUIRED_FOR_COUNT','RESOURCE_CRITERION_FAILED_NO_EXCLUSION'),'Known resource outcome without a false exclusion')
        if status=='RESOURCE_CRITERION_FAILED_NO_EXCLUSION':
            src.need(set(row)=={'n','band','index','source','status','failure_type','reason'}and row['failure_type']in('ValueError','AssertionError')and type(row['reason'])is str,'Failed criterion retained as no exclusion')
        else:
            src.need(set(row)=={'n','band','index','source','plan','status','result'}and type(row['plan'])is list and type(row['result'])is dict
                     and(status=='EXCLUDED_BY_SAME_LAW_RESOURCE')is bool(row['result'].get('excluded')),'Exact full row outcome and replay plan')
        statuses.append(status)
    src.need(same(candidate['status_counts'],dict(Counter(statuses))),'All100 status counters, including every non-excluded outcome')
    fields={'status','n','band','candidate_sha256','rows','status_counts','negative_controls','timings_seconds','files_sha256','predecessor_verified','global_bound_proved','cutoff20_proved'}
    src.need(set(accepted)==fields and accepted['status']==RESOURCE_ACCEPTED and type(accepted['n'])is int and accepted['n']==n and accepted['band']==b
             and accepted['candidate_sha256']==src.digest(folder/'CANDIDATE.json')and same(accepted['rows'],candidate['rows'])
             and same(accepted['status_counts'],candidate['status_counts'])and same(accepted['files_sha256'],graph)
             and same(accepted['negative_controls'],src.plan()['resource_negative_controls'])
             and all(accepted[k]is False for k in('predecessor_verified','global_bound_proved','cutoff20_proved')),'Whole fresh full resource acceptance and exact controls/parent/source graph')
    for times in(src.read(folder/'CONSTRUCT_TIMINGS.json'),accepted['timings_seconds']):
        src.need(type(times)is list and len(times)==100,'All100 per-row timings');[finite(x)for x in times]
    for action,label in(('resource_construct','RESOURCE_CANDIDATE'),('resource_accept','RESOURCE_ACCEPTED')):
        text=transport(task,request,action,records[action],report);output=c/src.output_paths(action,n,b)[0]
        # Python prints the insertion-ordered dict. Parse just this literal metadata safely.
        line=text.splitlines()[-1:] or [''];prefix=label+' '+str(n)+' '+b+' '
        src.need(line[0].startswith(prefix)and line[0].endswith(' '+src.digest(output)),'Actual resource terminal and whole output hash')
        import ast
        counts=ast.literal_eval(line[0][len(prefix):-(65)])
        src.need(same(counts,candidate['status_counts']),'Actual terminal complete resource counts')
    found={p.relative_to(c).as_posix()for p in c.rglob('*')if p.is_file()}
    src.need(found==set(request['sources'])|set(src.generated_paths(n,b)),'Complete source/current-output inventory, no unbound files')
    return dict(schema='CONDITIONAL_ACTUAL21_24_CORE_ARITHMETIC_CASE_V1',n=n,band=b,request=initial['request'],
        initial_candidate_sha256=ia['candidate_sha256'],initial_acceptance_sha256=src.digest(c/src.INITIAL/src.case(n,b)/'ACCEPTED.json'),
        initial_covers_per_action=9,signed_cells_per_cover=2592,original_probability_panels=100,resource_rows_per_action=100,
        status_counts=candidate['status_counts'],resource_candidate_sha256=src.digest(folder/'CANDIDATE.json'),resource_acceptance_sha256=src.digest(folder/'ACCEPTED.json'),
        review_epoch_sha256=src.digest(c/src.review_paths(n,b)[1]),source_plan_sha256=src.PLAN_SHA256,**{k:False for k in FLAGS})

def validate_run(task,report):
    request=src.verify_job(task)
    fields={'schema','scope','n','band','original_task_root','implementation','python_executable','python_executable_sha256',
            'python_version','platform','actions','conditional_core_arithmetic_completed'}|set(FLAGS)
    src.need(set(report)==fields and report['schema']==OBSERVED and report['scope']==SCOPE and same(report['implementation'],implementation())
             and report['n']==request['n']and type(report['n'])is int and report['band']==request['band']
             and type(report['python_executable_sha256'])is str and re.fullmatch('[0-9a-f]{64}',report['python_executable_sha256'])is not None
             and all(type(report[k])is str and bool(report[k])for k in('python_version','platform'))
             and report['original_task_root']==request['original_task_root']and report['conditional_core_arithmetic_completed']is False
             and all(report[k]is False for k in FLAGS)and [v['action']for v in report['actions']]==list(src.ACTIONS)
             and all(set(v)=={'action','observed'}for v in report['actions']),'Exact four-call implementation/case and observed-false ledger')
    return summarize(task,report)

def validate_completed(task,*,expected_n=None,expected_band=None):
    request=src.verify_job(task,expected_n,expected_band);report=src.read(Path(task)/'STAGE_OBSERVED.json')
    complete=src.read(Path(task)/'STAGE_COMPLETED.json',limit=32*src.MIB);summary=validate_run(task,report)
    fields={'schema','scope','implementation','observed_sha256','summary','artifacts','conditional_core_arithmetic_completed'}|set(FLAGS)
    src.need(set(complete)==fields and complete['schema']==COMPLETED and complete['scope']==SCOPE and same(complete['implementation'],report['implementation'])
             and complete['observed_sha256']==src.digest(Path(task)/'STAGE_OBSERVED.json')and same(complete['summary'],summary)
             and same(complete['artifacts'],inventory(task))and complete['conditional_core_arithmetic_completed']is True
             and all(complete[k]is False for k in FLAGS),'Four actual full actions and complete immutable/current evidence inventory')
    return dict(schema='REVALIDATED_CONDITIONAL_ACTUAL21_24_CORE_CASE_V1',n=request['n'],band=request['band'],summary=summary,
                stage_result_sha256=src.digest(Path(task)/'STAGE_COMPLETED.json'),original_task_root=request['original_task_root'],
                conditional_core_arithmetic_completed=True,**{k:False for k in FLAGS})
