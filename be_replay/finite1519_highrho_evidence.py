"""Pure evidence readback for57C; no original numerical module imports."""
from __future__ import annotations
from fractions import Fraction as F
import math
from pathlib import Path,PurePosixPath,PureWindowsPath
import re
from . import finite1519_highrho_sources as src
from .finite1039_count_evidence import same,mapped,terminal,inventory

SCOPE='UNCHANGED_INDEPENDENT_HIGHRHO14_19_FOURIER_BASIC_SUBLANE_V1'
OBSERVED='OBSERVED_FINITE1519_HIGHRHO_SUBLANE_V1'
COMPLETED='COMPLETED_FINITE1519_HIGHRHO_SUBLANE_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
FLAGS=('native_arithmetic_accepted','full_notebook57_completed','parent_acquisitions_verified',
       'support_acquisition_verified','support_high_initial_resource_acquired','resource_to_count147_interfaces_verified',
       'full_finite1039_verified','all_index_conclusion_verified')


def implementation():
    names=('finite1519_highrho.py','finite1519_highrho_sources.py','finite1519_highrho_evidence.py',
           'finite1039_sources.py','finite1039_count_evidence.py','n5_remaining_sources.py',
           'linux_supervisor.py','colab_batch.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)


def original_path(request,relative):
    root=request['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
    src.need(cls(root).is_absolute(),'Recorded absolute originating task root')
    return str(cls(root)/'capsule'/relative)


def command(request,action,python):
    src.need(action in src.ACTIONS and type(python)is str and (PureWindowsPath(python).is_absolute()or PurePosixPath(python).is_absolute()),'Exact action and original interpreter')
    if action=='readback':return [python,'-B','-S',original_path(request,src.AUDIT+'/readback.py'),original_path(request,src.REQUEST)]
    argv=[python,'-B','-S',original_path(request,src.NATIVE+'/run.py'),action,src.LABELS[action]]
    if action!='plan':argv.append(original_path(request,src.RUNS+'/plan01/PLAN.json'))
    return argv


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
             and mapped(task,launch['cwd'],original)==task/'capsule'
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
        p=task/'capsule'/name;copied=directory/'checkpoints'/name
        src.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
                 and packet['exists']is True and packet['trusted_certificate']is False
                 and mapped(task,packet['source_path'],original)==p and mapped(task,packet['path'],original)==copied
                 and p.is_file()and copied.is_file()and type(packet['bytes'])is int
                 and packet['bytes']==p.stat().st_size==copied.stat().st_size
                 and packet['sha256']==src.digest(p)==src.digest(copied),'Whole stopped native output identity: '+name)
    return captures['stdout'].read_text('utf-8')


def inner_capture(task,request,action,report,outer_stdout):
    c=Path(task)/'capsule';d=c/src.RUNS/src.LABELS[action];m=src.read(d/'metadata.json')
    result='PLAN.json'if action=='plan'else'RESULT.json';p=d/result
    native_manifest=src.read(c/src.NATIVE/'MANIFEST.json');inputs=dict(native_manifest['files_sha256'])
    inputs[src.NATIVE+'/MANIFEST.json']=src.digest(c/src.NATIVE/'MANIFEST.json')
    if action=='plan':argv=[report['python_executable'],'-B','planner.py',original_path(request,src.RUNS+'/plan01/PLAN.json')]
    else:
        inputs[src.RUNS+'/plan01/PLAN.json']=src.digest(c/src.RUNS/'plan01/PLAN.json')
        argv=[report['python_executable'],'-B','protocol.py',action,
              original_path(request,src.RUNS+'/plan01/PLAN.json'),original_path(request,src.RUNS+'/'+src.LABELS[action]+'/RESULT.json')]
    fields={'command','cwd','input_sha256','python','platform','started_utc','returncode','elapsed_seconds','finished_utc',
            'changed_inputs','stdout_sha256','stderr_sha256',result+'_sha256'}
    src.need(set(m)==fields and same(m['command'],argv)and m['cwd']==original_path(request,src.NATIVE)
             and same(m['input_sha256'],inputs)and m['python']==report['python_version']
             and type(m['platform'])is str and bool(m['platform'])
             and type(m['returncode'])is int and m['returncode']==0 and m['changed_inputs']==[]
             and m[result+'_sha256']==src.digest(p),'Genuine current original child command/source/result capture')
    finite(m['elapsed_seconds'])
    for key in('started_utc','finished_utc'):src.need(type(m[key])is str and bool(m[key]),'Original child time context')
    for kind in('stdout','stderr'):
        src.need(src.digest(d/(kind+'.txt'))==m[kind+'_sha256'],'Actual original child stream SHA')
    src.need((d/'stderr.txt').stat().st_size==0 and (d/'stdout.txt').read_text('utf-8')==outer_stdout,
             'Actual original child stdout propagates through the source-pinned run wrapper')
    return src.read(p,limit=128*src.MIB)


THEOREM='For every iid standardized real law with finite third absolute moment, rho>=33/25 implies sqrt(n)*Delta_n/rho <4097/10000 for each literal n=14,...,19; conditional on published Prawitz smoothing and Shevtsova tail inputs.'
MATHEMATICAL_STATUS='Universal normalized score <4097/10000 for each actual n14..19 on rho>=33/25 under stated Prawitz and Shevtsova inputs; no support, attained witness or predecessor assumption.'
EXECUTION_STATUS='Fresh independent exact coverage/normalization/source/capture acceptance of full native construction and replay; Fourier integrals were reproduced by the native implementation, not recomputed here.'

def plan_census(p):
    src.need(type(p)is dict and set(p)=={'schema','n','target','rho','strips'}
             and p['schema']=='HIGHRHO14_19_UNCONDITIONAL_PLAN_V1'
             and same(p['n'],list(range(14,20)))and p['target']=='4097/10000'and p['rho']==['33/25','19/10']
             and type(p['strips'])is list and 0<len(p['strips'])<=10000,'Complete original untrusted plan domain')
    cursor=F(33,25)
    for row in p['strips']:
        src.need(type(row)is dict and set(row)=={'rho','c','tau','heuristic_upper'}and type(row['rho'])is list
                 and len(row['rho'])==2 and all(type(v)is str for v in row['rho']+[row['c'],row['tau']]),'Original plan strip fields')
        lo,hi=map(F,row['rho']);c,tau=F(row['c']),F(row['tau'])
        src.need(str(lo)==row['rho'][0]and str(hi)==row['rho'][1]and lo==cursor<hi<=F(19,10)
                 and str(c)==row['c']and str(tau)==row['tau']and 0<c<F(3141592653589793238462643383279,10**30)
                 and F(1,1024)<tau<=F(3,10),'Exact closed seams and original frequency gates')
        src.need(type(row['heuristic_upper'])in(int,float)and math.isfinite(row['heuristic_upper']),'Untrusted finite discovery display')
        cursor=hi
    src.need(cursor==F(19,10),'Complete last closed rho endpoint');return len(p['strips'])


TARGET='4097/10000'
FINITE_RHO=['33/25', '19/10']
NATIVE_SUCCESS='EXACT_HIGHRHO14_19_UNCONDITIONAL_PASS'
READBACK_SUCCESS='PASS_INDEPENDENT_GLOBAL_HIGHRHO14_19_READBACK'
EXTRA_FIELDS=set()

def summarize(task,request,report,stdout):
    c=Path(task)/'capsule';p=inner_capture(task,request,'plan',report,stdout['plan']);strips=plan_census(p)
    construction=inner_capture(task,request,'construct',report,stdout['construct'])
    replay=inner_capture(task,request,'replay',report,stdout['replay'])
    src.need('seconds'in construction and 'seconds'in replay
             and same({k:v for k,v in construction.items()if k!='seconds'},
                      {k:v for k,v in replay.items()if k!='seconds'}),'Whole exact native construction/replay equality')
    for result in(construction,replay):
        finite(result['seconds'])
        src.need(set(result)=={'status','theorem','n','target','finite_rho','rows','attempts','published_tail',
                              'uniform_upper','uniform_upper_float','per_n_upper','controls','plan_sha256','manifest_sha256','seconds'}
                 and result['status']==NATIVE_SUCCESS and result['theorem']==THEOREM
                 and same(result['n'],list(range(14,20)))and result['target']==TARGET and result['finite_rho']==FINITE_RHO
                 and type(result['rows'])is list and len(result['rows'])==6*strips
                 and type(result['attempts'])is list and len(result['attempts'])>=strips
                 and same(result['controls'],dict(negative_controls=13,finite_sum_identities=4))
                 and result['plan_sha256']==src.digest(c/src.RUNS/'plan01/PLAN.json')
                 and result['manifest_sha256']==src.plan()['original_manifest_sha256']
                 and type(result['uniform_upper'])is str and str(F(result['uniform_upper']))==result['uniform_upper']
                 and 0<=F(result['uniform_upper'])<F(TARGET),
                 'Full native exact rows, original target, complete controls and input commitments')
        src.need(all(type(r['strip_index'])is int and type(r['n'])is int for r in result['rows'])
                 and [(r['strip_index'],r['n'])for r in result['rows']]==[(i,n)for i in range(strips)for n in range(14,20)],
                 'Every original literal index in every plan strip, without gaps or duplicates')
        values=result['per_n_upper']
        src.need(type(values)is dict and set(values)=={str(n)for n in range(14,20)}
                 and all(type(v)is str and str(F(v))==v and 0<=F(v)<F(TARGET)for v in values.values()),
                 'Complete six-index exact maxima and original ceiling')
    src.need((c/src.REQUEST).read_bytes()==src.dump(src.fresh_request(task)),'Readback request derives only from current real outputs')
    result=src.read(c/src.RESULT,limit=128*src.MIB)
    fields={'status','mathematical_status','execution_status','n','finite_rho','target','strips','exact_rows','attempts',
            'per_n_upper','uniform_upper','negative_controls','files_sha256'}|EXTRA_FIELDS
    src.need(set(result)==fields and same(terminal(stdout['readback']),{k:v for k,v in result.items()if k!='files_sha256'})
             and result['status']==READBACK_SUCCESS and result['mathematical_status']==MATHEMATICAL_STATUS
             and result['execution_status']==EXECUTION_STATUS and same(result['n'],list(range(14,20)))
             and result['finite_rho']==FINITE_RHO and result['target']==TARGET
             and type(result['strips'])is int and result['strips']==strips
             and type(result['exact_rows'])is int and result['exact_rows']==6*strips
             and type(result['attempts'])is int and result['attempts']==len(construction['attempts'])
             and type(result['negative_controls'])is int and result['negative_controls']==24
             and same(result['per_n_upper'],construction['per_n_upper'])and result['uniform_upper']==construction['uniform_upper'],
             'Actual independent readback terminal/whole receipt, full original domain/census and24controls')
    for field in EXTRA_FIELDS:
        value=result[field];src.need(type(value)is str and str(F(value))==value and F(value)>=0,'Original readback scalar export remains a canonical nonnegative rational')
    graph=dict(src.read(c/src.NATIVE/'MANIFEST.json')['files_sha256'])
    for name in[src.NATIVE+'/MANIFEST.json',src.RUNS+'/plan01/PLAN.json',src.REQUEST,src.AUDIT+'/readback.py',src.AUDIT+'/REVIEW.txt']+src.output_paths('construct')+src.output_paths('replay'):
        graph[name]=src.digest(c/name)
    src.need(same(result['files_sha256'],graph),'Complete original readback source/current-capture graph')
    found={p.relative_to(c).as_posix()for p in c.rglob('*')if p.is_file()}
    src.need(found==set(request['sources'])|{src.REQUEST}|{n for a in src.ACTIONS for n in src.output_paths(a)},
             'Complete sealed original capsule and exactly declared fresh outputs')
    return dict(schema='CONDITIONAL_HIGHRHO14_19_ARITHMETIC_ONLY_V1',n=list(range(14,20)),finite_rho=FINITE_RHO,
                target=TARGET,strips=strips,exact_rows=6*strips,native_controls=13,finite_sum_identities=4,
                independent_controls=24,uniform_upper=result['uniform_upper'],per_n_upper=result['per_n_upper'],
                original_scalar_exports={k:result[k]for k in EXTRA_FIELDS},
                plan_sha256=src.digest(c/src.RUNS/'plan01/PLAN.json'),readback_sha256=src.digest(c/src.RESULT),
                original_manifest_sha256=src.plan()['original_manifest_sha256'],source_plan_sha256=src.PLAN_SHA256,
                conditional_premises=['Original pointwise Prawitz/Fourier reduction and analytic kappa lemmas',
                                      'Published Shevtsova same-marginal upper tail input'],**{f:False for f in FLAGS})


def validate_run(task,report):
    task=Path(task);request=src.verify_job(task)
    src.need(report['schema']==OBSERVED and report['scope']==SCOPE and same(report['implementation'],implementation())
             and report['original_task_root']==request['original_task_root']
             and report['conditional_highrho_arithmetic_completed']is False and all(report[f]is False for f in FLAGS)
             and [x['action']for x in report['actions']]==list(src.ACTIONS),'Exact4-action observed-false implementation epoch')
    context=src.read(task/'DISCOVERY_CONTEXT.json')
    src.need(same(context,report['discovery_context'])and context['distribution']=='numpy'
             and context['scope']=='UNTRUSTED_FLOATING_DISCOVERY_ONLY'and context['acceptance_arithmetic_depends_on_numpy']is False
             and same(context['thread_environment'],{n:'1'for n in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')})
             and type(context['version'])is str and bool(context['version'])
             and type(context['entry_sha256'])is str and re.fullmatch('[0-9a-f]{64}',context['entry_sha256']),
             'Explicit installed NumPy discovery context, without an exact-arithmetic claim')
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
             and complete['conditional_highrho_arithmetic_completed']is True and same(complete['summary'],summary)
             and same(complete['artifacts'],inventory(task))and all(complete[f]is False for f in FLAGS),
             'All four genuine stopped actions and exact source/capture/output inventory')
    return dict(schema='REVALIDATED_CONDITIONAL_HIGHRHO14_19_SUBLANE_V1',summary=summary,
                source_plan_sha256=src.PLAN_SHA256,stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),
                original_task_root=request['original_task_root'],conditional_highrho_arithmetic_completed=True,
                **{f:False for f in FLAGS})
