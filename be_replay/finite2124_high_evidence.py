"""Pure stopped evidence and full original support result readback for58A."""
from __future__ import annotations
import math,re
from pathlib import Path,PurePosixPath,PureWindowsPath
from . import finite2124_high_sources as s

SCOPE='ACTUAL21_24_HIGH_RHO_SUPPORT_WITH_RETAINED_FOURIER_BASIC_V1'
CPU,WALL,MEMORY=43200,54000,2048*s.MIB
DISK,LOG=256*s.MIB,16*s.MIB
FLAGS=('native_arithmetic_accepted','historical_fourier_replayed','global_predecessors_verified',
       'parent_acquisitions_verified','full_actual20_24_verified','all_index_conclusion_verified')
CONTROL_NAMES=['missing actual index','wrong actual index','boolean index','wrong allowance','wrong radius',
               'wrong rho seam','missing ray','wrong beta','false predecessor discharge','false cutoff claim']
CONSTRUCT='CONDITIONAL_ACTUAL21_24_HIGH_RHO_EXCLUSION_CANDIDATE'
ACCEPT='PASS_FRESH_ACTUAL21_24_HIGH_RHO_REDUCTION_CONDITIONAL_ON_SHARP_PREDECESSORS'

def same(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    return a==b

def implementation():
    names=('finite2124_high.py','finite2124_high_sources.py','finite2124_high_evidence.py',
           'finite1039_sources.py','n5_remaining_sources.py','linux_supervisor.py','colab_batch.py','environment.py')
    return {n:s.digest(s.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=s.PLAN_SHA256)

def pathclass(request):
    value=request['original_task_root'];s.need(type(value)is str and '\0'not in value,'Original task path')
    cls=PureWindowsPath if re.match(r'^[A-Za-z]:',value)else PurePosixPath
    s.need(cls(value).is_absolute()and '..'not in cls(value).parts,'Absolute originating task root');return cls

def original(request,name):return str(pathclass(request)(request['original_task_root']).joinpath(*s.parts(name)))

def mapped(task,request,value):
    cls=pathclass(request);s.need(type(value)is str and '\0'not in value,'Recorded path string')
    p=cls(value);s.need(p.is_absolute(),'Absolute originating path')
    try:rel=p.relative_to(cls(request['original_task_root']))
    except ValueError:raise ValueError('Evidence outside originating task root')
    s.need(rel.parts and all(x not in('.','..')for x in rel.parts),'Contained evidence path')
    return s.ordinary(Path(task).joinpath(*rel.parts))

def command(request,action,python):
    s.need(action in s.ACTIONS and type(python)is str and
           (PurePosixPath(python).is_absolute()or PureWindowsPath(python).is_absolute()),'Exact action and interpreter')
    return [python,'-B','-S',original(request,'capsule/'+s.NATIVE+'/check.py'),action,
            original(request,'capsule/'+s.REVIEW)]

def guard():
    return dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,
        external_wall_seconds=float(WALL),per_process_RLIMIT_AS_bytes=MEMORY,per_process_RLIMIT_CPU_seconds=CPU,
        aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY,
        sampled_group_CPU_limit_seconds=CPU,sampled_file_limit_bytes=DISK,sampled_log_limit_bytes=LOG,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)

def transport(task,request,action,observed,python):
    task=Path(task);directory=task/'executions'/action
    s.need(same(s.read(directory/'supervisor-result.json'),observed)and observed.get('status')=='completed'
           and type(observed.get('returncode'))is int and observed['returncode']==0
           and observed.get('reason')is None and observed.get('mode')=='untrusted_search'
           and observed.get('proof_accepted')is False and same(observed.get('guard_scope'),guard())
           and type(observed.get('sample_count'))is int and observed['sample_count']>0,'Actual complete BASIC execution')
    for key in('elapsed_seconds','maximum_sampled_group_CPU_seconds','maximum_sampled_group_RSS_bytes'):
        value=observed[key];s.need(type(value)in(int,float)and math.isfinite(value)and value>=0,'Finite actual measurement')
    launch=s.read(directory/'launch.json');name=s.OUTPUTS[action];output=task/'capsule'/s.NATIVE/name
    s.need(set(launch)=={'argv','cwd','output_dir','mode','wall_seconds','cpu_seconds','memory_bytes',
                        'checkpoint_paths','disk_bytes','log_bytes','sample_seconds','heartbeat_seconds'}
           and same(launch['argv'],command(request,action,python))
           and mapped(task,request,launch['cwd'])==task/'capsule'/s.NATIVE
           and mapped(task,request,launch['output_dir'])==directory and launch['mode']=='untrusted_search'
           and type(launch['cpu_seconds'])is int and launch['cpu_seconds']==CPU
           and type(launch['memory_bytes'])is int and launch['memory_bytes']==MEMORY
           and type(launch['disk_bytes'])is int and launch['disk_bytes']==DISK
           and type(launch['log_bytes'])is int and launch['log_bytes']==LOG
           and type(launch['wall_seconds'])in(int,float)and launch['wall_seconds']==WALL
           and type(launch['sample_seconds'])in(int,float)and launch['sample_seconds']==.2
           and type(launch['heartbeat_seconds'])in(int,float)and launch['heartbeat_seconds']==20
           and type(launch['checkpoint_paths'])is list
           and [mapped(task,request,p)for p in launch['checkpoint_paths']]==[output],
           'Exact unchanged original command, working directory and output/budgets')
    paths={}
    for kind in('stdout','stderr'):
        p=mapped(task,request,observed[kind+'_path']);s.need(p==directory/(kind+'.txt')and p.is_file()
          and p.stat().st_size<=LOG and s.digest(p)==observed[kind+'_sha256'],'Actual bounded '+kind+' bytes');paths[kind]=p
    s.need(paths['stderr'].stat().st_size==0,'Successful original support stderr must be empty')
    packets=observed['checkpoints'];s.need(type(packets)is list and len(packets)==1,'One whole stopped original output')
    packet=packets[0];copied=directory/'checkpoints'/name
    s.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
           and packet['exists']is True and packet['trusted_certificate']is False
           and mapped(task,request,packet['source_path'])==output and mapped(task,request,packet['path'])==copied
           and s.ordinary(output).is_file()and s.ordinary(copied).is_file()
           and type(packet['bytes'])is int and 0<packet['bytes']<=4*s.MIB
           and packet['bytes']==output.stat().st_size==copied.stat().st_size
           and packet['sha256']==s.digest(output)==s.digest(copied),'Whole stopped output identity')
    final=dict(event='linux_supervisor_finished',stage='untrusted_search',status='completed',reason=None,
               elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
    history=s.ordinary(directory/'progress.jsonl');s.need(history.is_file()and 0<history.stat().st_size<=LOG,'Bounded supervisor history')
    last=history.read_text(encoding='utf-8').splitlines()[-1]
    s.need(same(s.loads(last),final)and same(s.read(directory/'progress.json'),final),'Actual stopped supervisor progress')
    result=s.read(output);terminal=paths['stdout'].read_text(encoding='utf-8').splitlines()
    s.need(terminal and terminal[-1]==result['status']+' '+s.digest(output),'Original terminal binds actual output')
    return result

def results(task,request,construct,accept):
    c=Path(task)/'capsule';cp=c/s.NATIVE/'CANDIDATE.json';ap=c/s.NATIVE/'ACCEPTED.json'
    freeze=s.digest(c/s.NATIVE/'FROZEN_SOURCES.json');review=s.digest(c/s.REVIEW)
    for p in(construct,accept):
        s.need(same(p['actual_n'],[21,22,23,24])and same(p['excluded_rho'],['9/8','infinity'])
               and same(p['remaining_rho'],['1','9/8'])and p['remaining_upper_endpoint_open']is True
               and p['source_freeze_sha256']==freeze
               and all(p[k]is False for k in('global_predecessors_verified','historical_fourier_replayed','sharp20_proved','cutoff20_proved')),
               'Exact conditional literal-index/domain scope with all global flags false')
    s.need(construct['status']==CONSTRUCT and accept['status']==ACCEPT and accept['candidate_sha256']==s.digest(cp)
           and accept['source_review_sha256']==review and type(accept['fresh_support_calls'])is int
           and accept['fresh_support_calls']==4 and same(accept['negative_controls'],CONTROL_NAMES),
           'Full original support acceptance and all ten original controls')
    s.need(type(construct['rows'])is list and len(construct['rows'])==4 and construct['strict_fourier_target']=='4097/10000',
           'All four original support rows and strict retained Fourier target')
    for n,row in zip((21,22,23,24),construct['rows']):
        s.need(same(row['request'],dict(n=n,K='0',q='0',rho_upper='6/5',radius='3',sign=0,mesh=10)),
               'Exact actual-index support request')
        proof=row['proof'];s.need(type(proof['n'])is int and proof['n']==n and proof['K']==proof['q_contact']=='0'
          and proof['radius']=='3'and proof['rho_upper']=='6/5'and type(proof['support_sign'])is int
          and proof['support_sign']==0 and type(proof['ray_rows'])is list and len(proof['ray_rows'])==2
          and all(type(q['sign'])is int for q in proof['ray_rows'])and [q['sign']for q in proof['ray_rows']]==[-1,1],
          'Both full original support rays for each actual index')
    for field,path in(('universal_readback_sha256','cutoff20_20261016/analytic/fourier_cover_review_v1/READBACK.json'),
                       ('supported_readback_sha256','cutoff20_20261016/analytic/supported1125_review_v1/READBACK.json')):
        s.need(construct[field]==s.digest(c/path),'Unchanged explicitly retained Fourier evidence identity')
    return dict(actual_n=[21,22,23,24],fresh_support_calls_per_pass=4,full_original_passes=2,
        excluded_rho=['9/8','infinity'],negative_controls=10,candidate_sha256=s.digest(cp),acceptance_sha256=s.digest(ap),
        retained_fourier_inputs_freshly_replayed=False)

def inventory(task):
    task=Path(task);out={}
    for p in sorted(task.rglob('*')):
        s.ordinary(p);rel=p.relative_to(task).as_posix()
        if p.is_file()and rel not in('STAGE_OBSERVED.json','STAGE_COMPLETED.json'):
            out[rel]=dict(bytes=p.stat().st_size,sha256=s.digest(p))
    return out

def validate_run(task,report):
    task=Path(task).resolve();request=s.verify_job(task)
    s.need(set(report)=={'schema','scope','implementation','python_executable','python_version','actions',
                        'conditional_support_arithmetic_completed',*FLAGS}
           and report['schema']=='OBSERVED_FINITE2124_HIGH_V1'and report['scope']==SCOPE
           and same(report['implementation'],implementation())and report['conditional_support_arithmetic_completed']is False
           and all(report[k]is False for k in FLAGS)and type(report['python_version'])is str
           and type(report['actions'])is list and len(report['actions'])==2,'Exact current two-action conditional ledger')
    outputs=[]
    for action,row in zip(s.ACTIONS,report['actions']):
        s.need(set(row)=={'action','observed'}and row['action']==action,'Original ordered action pair')
        outputs.append(transport(task,request,action,row['observed'],report['python_executable']))
    return results(task,request,*outputs)

def validate_completed(task):
    task=Path(task).resolve();observed=s.read(task/'STAGE_OBSERVED.json');summary=validate_run(task,observed)
    done=s.read(task/'STAGE_COMPLETED.json')
    s.need(set(done)=={'schema','scope','implementation','observed_sha256','summary','artifacts',
                      'conditional_support_arithmetic_completed',*FLAGS}
           and done['schema']=='COMPLETED_FINITE2124_HIGH_V1'and done['scope']==SCOPE
           and same(done['implementation'],implementation())and done['observed_sha256']==s.digest(task/'STAGE_OBSERVED.json')
           and same(done['summary'],summary)and same(done['artifacts'],inventory(task))
           and done['conditional_support_arithmetic_completed']is True and all(done[k]is False for k in FLAGS),
           'Exact completed original pair and full artifact/source/capture inventory')
    return dict(schema='REVALIDATED_FINITE2124_HIGH_V1',summary=summary,
                stage_result_sha256=s.digest(task/'STAGE_COMPLETED.json'),conditional_support_arithmetic_completed=True,
                **{k:False for k in FLAGS})
