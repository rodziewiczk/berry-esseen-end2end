"""Pure evidence readback for58D/E/F; no original numerical module imports."""
from __future__ import annotations
from fractions import Fraction as F
import math
from pathlib import Path,PurePosixPath,PureWindowsPath
import re
from . import finite2024_fourier_sources as src
from .finite1039_count_evidence import same,mapped,terminal,inventory

SCOPE='UNCHANGED_ACTUAL20_24_FOURIER_FULL_BASIC_UNIT_V1'
OBSERVED='OBSERVED_FINITE2024_FOURIER_UNIT_V1'
COMPLETED='COMPLETED_FINITE2024_FOURIER_UNIT_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
FLAGS=('native_arithmetic_accepted','full_notebook58_completed','actual20_sharp_verified','predecessor_verified',
       'support_acquisition_verified','parent_acquisitions_verified','resource_count_join_verified','all_index_conclusion_verified')


def implementation():
    names=('finite2024_fourier.py','finite2024_fourier_sources.py','finite2024_fourier_evidence.py',
           'finite1039_sources.py','finite1039_count_evidence.py','n5_remaining_sources.py',
           'linux_supervisor.py','colab_batch.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)


def original_path(request,relative):
    root=request['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
    src.need(cls(root).is_absolute(),'Recorded absolute originating task root')
    return str(cls(root)/'capsule'/relative)


def command(request,action,python):
    cfg=src.family(request['family'])
    src.need(action in src.ACTIONS and type(python)is str and (PureWindowsPath(python).is_absolute()or PurePosixPath(python).is_absolute()),'Exact action and original interpreter')
    if action=='readback':return [python,'-B','-S',original_path(request,cfg['audit']+'/readback.py'),original_path(request,src.request_path(cfg))]
    argv=[python,'-B','-S',original_path(request,cfg['native']+'/run.py'),action,src.LABELS[action]]
    if action=='plan':argv.extend(cfg['plan_extra_arguments'])
    else:argv.append(original_path(request,cfg['runs']+'/plan01/PLAN.json'))
    return argv


def finite(value):
    src.need(type(value)in(int,float)and math.isfinite(value)and value>=0,'Finite nonnegative execution display');return value


def transport(task,request,action,observed,report):
    cfg=src.family(request['family']);task=Path(task);original=request['original_task_root'];directory=task/'executions'/action
    src.need(same(src.read(directory/'supervisor-result.json'),observed)
             and observed.get('status')=='completed'and type(observed.get('returncode'))is int and observed['returncode']==0
             and observed.get('reason')is None and observed.get('mode')=='untrusted_search'
             and observed.get('proof_accepted')is False and type(observed.get('sample_count'))is int and observed['sample_count']>0,
             'Actual successful stopped BASIC execution for '+action)
    for k in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):finite(observed[k])
    launch=src.read(directory/'launch.json')
    fields={'argv','cwd','output_dir','mode','wall_seconds','cpu_seconds','memory_bytes','checkpoint_paths',
            'disk_bytes','log_bytes','sample_seconds','heartbeat_seconds'}
    outputs=src.output_paths(action,cfg)
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
    cfg=src.family(request['family']);c=Path(task)/'capsule';d=c/cfg['runs']/src.LABELS[action];m=src.read(d/'metadata.json')
    result='PLAN.json'if action=='plan'else'RESULT.json';p=d/result
    native_manifest=src.read(c/cfg['native']/'MANIFEST.json');inputs=dict(native_manifest['files_sha256'])
    inputs[cfg['native']+'/MANIFEST.json']=src.digest(c/cfg['native']/'MANIFEST.json')
    if action=='plan':argv=[report['python_executable'],'-B','planner.py',*cfg['plan_extra_arguments'],original_path(request,cfg['runs']+'/plan01/PLAN.json')]
    else:
        inputs[cfg['runs']+'/plan01/PLAN.json']=src.digest(c/cfg['runs']/'plan01/PLAN.json')
        argv=[report['python_executable'],'-B','protocol.py',action,
              original_path(request,cfg['runs']+'/plan01/PLAN.json'),original_path(request,cfg['runs']+'/'+src.LABELS[action]+'/RESULT.json')]
    fields={'command','cwd','input_sha256','python','platform','started_utc','returncode','elapsed_seconds','finished_utc',
            'changed_inputs','stdout_sha256','stderr_sha256',result+'_sha256'}
    src.need(set(m)==fields and same(m['command'],argv)and m['cwd']==original_path(request,cfg['native'])
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


def rat(value):
    src.need(type(value)is str,'Literal rational metadata');q=F(value);src.need(str(q)==value,'Canonical rational metadata');return q

def plan_census(p,cfg,key):
    fields={'schema','n','target','rho','strips'}|({'support_absolute_upper'}if key=='supported'else set())
    src.need(type(p)is dict and set(p)==fields and p['schema']==cfg['plan_schema']and same(p['n'],cfg['n'])
             and p['target']==cfg['target']and same(p['rho'],cfg['rho'])and type(p['strips'])is list and 0<len(p['strips'])<=10000,
             'Full literal-index/target/rho discovery plan, without dropping n19')
    if key=='supported':src.need(p['support_absolute_upper']=='3','Explicit unacquired support premise')
    cursor=F(cfg['rho'][0]);end=F(cfg['rho'][1]);cells=[]
    for i,row in enumerate(p['strips']):
        src.need(set(row)==({'rho','h_panels'}if key=='universal'else{'rho','c','tau','heuristic_upper'})and type(row['rho'])is list and len(row['rho'])==2,'Complete plan strip schema')
        lo,hi=map(rat,row['rho']);src.need(lo==cursor<hi<=end,'Ordered closed complete rho seams');cursor=hi
        panels=row['h_panels']if key=='universal'else[row]
        src.need(type(panels)is list and 0<len(panels)<=10000,'Nonempty complete surrogate cover')
        hcursor=None
        for j,cell in enumerate(panels):
            if key=='universal':
                src.need(set(cell)=={'h','c','tau','heuristic_upper'}and type(cell['h'])is list and len(cell['h'])==2,'Exact original H-cell fields')
                hl,hu=map(rat,cell['h']);src.need(0<hl<hu<=1 and(hl*hl+hi*hl<=2 if hcursor is None else hl==hcursor),'Full closed H-cell coverage from beta lower to1');hcursor=hu
            c,tau=rat(cell['c']),rat(cell['tau']);src.need(0<c<F(3141592653589793238462643383279,10**30)and F(1,1024)<tau<=F(3,10),'Original frequency parameter bounds')
            src.need(type(cell['heuristic_upper'])in(int,float)and math.isfinite(cell['heuristic_upper']),'Finite untrusted discovery display')
            cells.append((i,j)if key=='universal'else(i,))
        if key=='universal':src.need(hcursor==1,'Complete H upper endpoint')
    src.need(cursor==end,'Complete final rho endpoint');return cells

def summarize(task,request,report,stdout):
    c=Path(task)/'capsule';key=request['family'];cfg=src.family(key)
    p=inner_capture(task,request,'plan',report,stdout['plan']);cells=plan_census(p,cfg,key);ns=cfg['n'];target=F(cfg['target'])
    construct=inner_capture(task,request,'construct',report,stdout['construct']);replay=inner_capture(task,request,'replay',report,stdout['replay'])
    src.need('seconds'in construct and'seconds'in replay and same({k:v for k,v in construct.items()if k!='seconds'},
             {k:v for k,v in replay.items()if k!='seconds'}),'Whole fresh native equality excluding only top-level elapsed seconds')
    for value in(construct,replay):
        finite(value['seconds']);src.need(set(value)==set(cfg['native_fields'])and value['status']==cfg['native_status']
            and same(value['n'],ns)and value['target']==cfg['target']and same(value.get('finite_rho',value.get('rho')),cfg['rho'])
            and value['plan_sha256']==src.digest(c/cfg['runs']/'plan01/PLAN.json')and value['manifest_sha256']==cfg['original_manifest_sha256']
            and same(value['negative_controls']if key=='universal'else value['controls'],cfg['native_controls'])
            and type(value['rows'])is list and len(value['rows'])==len(cells)*len(ns),'Every exact native row, original controls, literal scope and input commitments')
        if key=='supported':src.need(value['support_absolute_upper']=='3','Native supported theorem scope')
        expected=[(*cell,n)for cell in cells for n in ns];actual=[]
        for row in value['rows']:
            indexes=(row['rho_strip_index'],row['h_cell_index'])if key=='universal'else(row['strip_index'],)
            src.need(all(type(i)is int for i in indexes)and type(row['n'])is int and row['target']==cfg['target']and row['strict_target_pass']is True
                     and 0<=rat(row['normalized_upper'])<target,'Every typed full native cell/index and strict exact bound')
            actual.append((*indexes,row['n']))
        src.need(same(actual,expected),'All literal indices in every declared cell, without gaps/duplicates')
        attempts=value['attempts'];src.need(type(attempts)is list and len(cells)<=len(attempts)<=len(cells)*(4 if key=='supported'else 3),'Complete bounded deterministic mesh path')
        cursor=0;meshes=[128,256,512,1024]if key=='supported'else[128,256,512]
        for number,cell in enumerate(cells):
            group=[]
            while cursor<len(attempts):
                a=attempts[cursor];location=(a['rho_strip_index'],a['h_cell_index'])if key=='universal'else(a['strip_index'],)
                if location!=cell:break
                group.append(a);cursor+=1
            src.need(0<len(group)<=len(meshes)and[type(a['mesh'])for a in group]==[int]*len(group)
                     and[a['mesh']for a in group]==meshes[:len(group)],'Original whole mesh prefix for every cell')
            flag='passed'if key=='universal'else'strict_target_pass'
            src.need(all(a[flag]is False for a in group[:-1])and group[-1][flag]is True
                     and same(group[-1]['normalized_uppers'],[row['normalized_upper']for row in value['rows'][number*len(ns):(number+1)*len(ns)]]),
                     'Exact final successful attempt and every preceding failed refinement')
        src.need(cursor==len(attempts),'No extra or reordered mesh attempts')
    src.need((c/src.request_path(cfg)).read_bytes()==src.dump(src.fresh_request(task)),'Readback request binds only genuine current outputs')
    result=src.read(c/src.result_path(cfg),limit=128*src.MIB)
    src.need(set(result)==set(cfg['readback_fields'])and same(terminal(stdout['readback']),{k:v for k,v in result.items()if k!='files_sha256'})
             and result['status']==cfg['readback_status']and same(result['n'],ns)and result['target']==cfg['target']
             and same(result.get('finite_rho',result.get('rho')),cfg['rho'])
             and type(result['negative_controls'])is int and result['negative_controls']==cfg['readback_negative_controls']
             and type(result['exact_rows'])is int and result['exact_rows']==len(cells)*len(ns)
             and type(result['attempts'])is int and result['attempts']==len(construct['attempts']),
             'Whole original independent readback/terminal and every fresh native row/control')
    if key=='universal':
        src.need(type(result['rho_strips'])is int and result['rho_strips']==len(p['strips'])and type(result['h_cells'])is int and result['h_cells']==len(cells)
                 and result['external_tail_from']=='19/10'and rat(result['external_tail_upper'])<target
                 and rat(result['normalized_upper_max'])==max(rat(row['normalized_upper'])for row in construct['rows']),
                 'Full rho/H census, complete tail and exact finite maximum')
    else:
        src.need(type(result['strips'])is int and result['strips']==len(p['strips'])and same(result['per_n_upper'],construct['per_n_upper'])
                 and result['uniform_upper']==construct['uniform_upper']and rat(result['uniform_upper'])==max(rat(x)for x in result['per_n_upper'].values())
                 and set(result['per_n_upper'])=={str(n)for n in ns},'Full per-index and uniform bound interfaces')
        if key=='supported':src.need(result['support_absolute_upper']=='3','Supported readback keeps its premise')
    interfaces={}
    if key=='auxiliary':
        q1=max(F(0),20*(rat(result['per_n_upper']['19'])-F(819,2000)))
        q2=max(F(0),20*(rat(result['per_n_upper']['19'])-F(40973218,10**8)))
        src.need(result['sharp20_contact_allowance_using_CE_gt_4095_10000']==str(q1)
                 and result['sharp20_contact_allowance_using_CE_gt_40973218_100000000']==str(q2)
                 and q1<F(21,100)and all(rat(result['per_n_upper'][str(n)])<F(419,1000)for n in range(20,25)),
                 'Fresh numeric actual20 allowance and419/1000 owncap gates; native21/50 alone is insufficient')
        interfaces=dict(actual20_24_owncap419_numeric_gate=True,actual20_q21_over100_numeric_gate=True,
                        conservative_contact_allowance=str(q1),sharper_contact_allowance=str(q2),per_n_upper=result['per_n_upper'])
    graph=dict(src.read(c/cfg['native']/'MANIFEST.json')['files_sha256'])
    names=[cfg['native']+'/MANIFEST.json',cfg['runs']+'/plan01/PLAN.json',src.request_path(cfg),cfg['audit']+'/readback.py',cfg['audit']+'/REVIEW.txt']
    names+=src.output_paths('construct',cfg)+src.output_paths('replay',cfg)
    for name in names:graph[name]=src.digest(c/name)
    src.need(same(result['files_sha256'],graph),'Entire original manifest/current request/native captures/readback source graph')
    found={q.relative_to(c).as_posix()for q in c.rglob('*')if q.is_file()}
    src.need(found==set(request['sources'])|{src.request_path(cfg)}|{n for a in src.ACTIONS for n in src.output_paths(a,cfg)},'Exactly the full sealed input and genuine current-output inventory')
    return dict(schema='CONDITIONAL_ACTUAL20_24_FOURIER_ARITHMETIC_UNIT_V1',family=key,n=ns,rho=cfg['rho'],target=cfg['target'],
        support_absolute_upper=cfg['support_absolute_upper'],rho_strips=len(p['strips']),cells=len(cells),exact_rows=len(cells)*len(ns),attempts=len(construct['attempts']),
        native_controls=cfg['native_controls'],independent_controls=cfg['readback_negative_controls'],interfaces=interfaces,
        readback_sha256=src.digest(c/src.result_path(cfg)),original_manifest_sha256=cfg['original_manifest_sha256'],source_plan_sha256=src.PLAN_SHA256,
        **{k:False for k in FLAGS})

def validate_run(task,report):
    task=Path(task);request=src.verify_job(task)
    src.need(report['schema']==OBSERVED and report['scope']==SCOPE and report['family']==request['family']and same(report['implementation'],implementation())
             and report['original_task_root']==request['original_task_root']and report['conditional_fourier_arithmetic_completed']is False
             and all(report[k]is False for k in FLAGS)and[x['action']for x in report['actions']]==list(src.ACTIONS),'Exact four-action observed-false implementation/family epoch')
    context=src.read(task/'DISCOVERY_CONTEXT.json')
    src.need(same(context,report['discovery_context'])and context['distribution']=='numpy'and context['scope']=='UNTRUSTED_FLOATING_DISCOVERY_ONLY'
             and context['acceptance_arithmetic_depends_on_numpy']is False
             and same(context['thread_environment'],{n:'1'for n in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')})
             and type(context['version'])is str and bool(context['version'])and type(context['entry_sha256'])is str and re.fullmatch('[0-9a-f]{64}',context['entry_sha256']),
             'Installed original planner dependency/context, no exact-arithmetic claim')
    stdout={x['action']:transport(task,request,x['action'],x['observed'],report)for x in report['actions']}
    result=summarize(task,request,report,stdout);src.verify_job(task);return result

def validate_completed(task,*,expected_family=None):
    task=Path(task);request=src.verify_job(task,expected_family);report=src.read(task/'STAGE_OBSERVED.json');complete=src.read(task/'STAGE_COMPLETED.json',limit=32*src.MIB)
    summary=validate_run(task,report)
    src.need(complete['schema']==COMPLETED and complete['scope']==SCOPE and same(complete['implementation'],report['implementation'])
             and complete['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')and same(complete['summary'],summary)
             and same(complete['artifacts'],inventory(task))and complete['conditional_fourier_arithmetic_completed']is True
             and all(complete[k]is False for k in FLAGS),'All four full original calls and entire evidence inventory')
    return dict(schema='REVALIDATED_CONDITIONAL_ACTUAL20_24_FOURIER_UNIT_V1',family=request['family'],summary=summary,
        stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),original_task_root=request['original_task_root'],
        conditional_fourier_arithmetic_completed=True,**{k:False for k in FLAGS})
