"""Pure stopped-evidence readback; never imports the original scalar checker."""
from __future__ import annotations
from fractions import Fraction as F
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
from . import finite1014_kappa_sources as src

SCOPE='UNCHANGED_GLOBAL_SCALAR_KAPPA_62_625_BASIC_ONLY_V1'
OBSERVED='OBSERVED_FINITE1014_KAPPA_V1'
COMPLETED='COMPLETED_FINITE1014_KAPPA_V1'
STATUS='PASS_GLOBAL_COSINE_KAPPA_62_625_AND_CONVEX_SPLICE_V1'
MATHEMATICAL_STATUS='Exact scalar polynomial and splice certificate; no Fourier integration or cutoff claim'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
DISK_BYTES,LOG_BYTES=256*src.MIB,16*src.MIB
FLAGS=('native_arithmetic_accepted','support_acquisition_verified','prawitz_verified',
       'fourier_integrations_completed','full_notebook56_completed','parent_acquisitions_verified',
       'all_index_conclusion_verified')


def same(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    return a==b


def implementation():
    names=('finite1014_kappa.py','finite1014_kappa_sources.py','finite1014_kappa_evidence.py',
           'linux_supervisor.py','colab_batch.py','environment.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)


def pathclass(root):
    src.need(type(root)is str and '\0'not in root,'Original path string')
    cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
    src.need(cls(root).is_absolute()and '..'not in cls(root).parts,'Absolute explicit original task root');return cls


def original(request,relative):
    cls=pathclass(request['original_task_root']);return str(cls(request['original_task_root']).joinpath(*src.parts(relative)))


def mapped(task,value,request):
    cls=pathclass(request['original_task_root']);src.need(type(value)is str and '\0'not in value,'Recorded evidence path')
    p=cls(value);src.need(p.is_absolute(),'Absolute recorded evidence path')
    try:relative=p.relative_to(cls(request['original_task_root']))
    except ValueError:raise ValueError('Recorded evidence leaves its originating task root')
    src.need(relative.parts and all(x not in('.','..')for x in relative.parts),'Contained evidence path')
    return src.ordinary(Path(task).joinpath(*relative.parts))


def command(request,python):
    src.need(type(python)is str and (PurePosixPath(python).is_absolute()or PureWindowsPath(python).is_absolute()),
             'Absolute original interpreter')
    return [python,'-B','-S',original(request,'capsule/controls.py')]


def guard():
    return dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,
        external_wall_seconds=float(WALL_SECONDS),per_process_RLIMIT_AS_bytes=MEMORY_BYTES,
        per_process_RLIMIT_CPU_seconds=CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,
        sampled_group_RSS_limit_bytes=MEMORY_BYTES,sampled_group_CPU_limit_seconds=CPU_SECONDS,
        sampled_file_limit_bytes=DISK_BYTES,sampled_log_limit_bytes=LOG_BYTES,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)


def transport(task,request,observed,python):
    task=Path(task);directory=task/'execution'
    src.need(same(src.read(directory/'supervisor-result.json'),observed)
             and observed.get('status')=='completed'and type(observed.get('returncode'))is int and observed['returncode']==0
             and observed.get('reason')is None and observed.get('mode')=='untrusted_search'
             and observed.get('proof_accepted')is False and type(observed.get('sample_count'))is int and observed['sample_count']>0,
             'Actual successful stopped BASIC scalar execution')
    for key in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):
        value=observed[key];src.need(type(value)in(int,float)and math.isfinite(value)and value>=0,'Finite execution measurement')
    launch=src.read(directory/'launch.json')
    fields={'argv','cwd','output_dir','mode','wall_seconds','cpu_seconds','memory_bytes','checkpoint_paths',
            'disk_bytes','log_bytes','sample_seconds','heartbeat_seconds'}
    src.need(set(launch)==fields and same(launch['argv'],command(request,python))
             and mapped(task,launch['cwd'],request)==task/'capsule'
             and mapped(task,launch['output_dir'],request)==directory and launch['mode']=='untrusted_search'
             and type(launch['cpu_seconds'])is int and launch['cpu_seconds']==CPU_SECONDS
             and type(launch['memory_bytes'])is int and launch['memory_bytes']==MEMORY_BYTES
             and type(launch['disk_bytes'])is int and launch['disk_bytes']==DISK_BYTES
             and type(launch['log_bytes'])is int and launch['log_bytes']==LOG_BYTES
             and type(launch['wall_seconds'])in(int,float)and launch['wall_seconds']==WALL_SECONDS
             and type(launch['sample_seconds'])in(int,float)and launch['sample_seconds']==.2
             and type(launch['heartbeat_seconds'])in(int,float)and launch['heartbeat_seconds']==20
             and type(launch['checkpoint_paths'])is list
             and [mapped(task,p,request)for p in launch['checkpoint_paths']]==[task/'capsule'/n for n in src.OUTPUTS],
             'Exact scalar command, cwd, stopped outputs and declared budgets')
    src.need(same(observed['guard_scope'],guard()),'Actual honest BASIC guard scope')
    finished=dict(event='linux_supervisor_finished',stage='untrusted_search',status=observed['status'],
                  reason=observed['reason'],elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
    history=src.ordinary(directory/'progress.jsonl')
    src.need(history.is_file()and 0<history.stat().st_size<=LOG_BYTES,'Bounded actual supervisor progress history')
    rows=history.read_text(encoding='utf-8').splitlines()
    src.need(rows and same(src.loads(rows[-1]),finished)and same(src.read(directory/'progress.json'),finished),
             'Actual final stopped supervisor progress agrees with its result')
    captures={}
    for kind in('stdout','stderr'):
        p=mapped(task,observed[kind+'_path'],request)
        src.need(p==directory/(kind+'.txt')and p.is_file()and p.stat().st_size<=LOG_BYTES
                 and src.digest(p)==observed[kind+'_sha256'],'Actual bounded '+kind+' capture')
        captures[kind]=p
    src.need(captures['stderr'].stat().st_size==0,'Scalar stderr must be empty')
    packets=observed['checkpoints'];src.need(type(packets)is list and len(packets)==2,'Both whole stopped scalar outputs')
    for packet,name in zip(packets,src.OUTPUTS):
        current=task/'capsule'/name;copied=directory/'checkpoints'/name
        src.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
                 and packet['exists']is True and packet['trusted_certificate']is False
                 and mapped(task,packet['source_path'],request)==current and mapped(task,packet['path'],request)==copied
                 and src.ordinary(current).is_file()and src.ordinary(copied).is_file()
                 and type(packet['bytes'])is int and 0<packet['bytes']<=4*src.MIB
                 and packet['bytes']==current.stat().st_size==copied.stat().st_size
                 and packet['sha256']==src.digest(current)==src.digest(copied),'Whole stopped output identity '+name)
    return src.loads(captures['stdout'].read_text(encoding='utf-8'))


def rat(value):
    src.need(type(value)is str,'Canonical scalar fraction string');v=F(value)
    src.need(str(v)==value,'Canonical scalar fraction');return v


COEFFICIENTS=['62/625','-1/24','0','1/720','0','-1/40320','0','1/3628800','0',
              '-1/479001600','0','1/87178291200','0','-1/20922789888000']


def scalar_outputs(task,request,stdout_packet):
    """Schema/census readback of stored data, not another polynomial checker."""
    capsule=Path(task)/'capsule';cert=src.read(capsule/'CERTIFICATE.json');checked=src.read(capsule/'CHECKED.json')
    src.need(type(cert)is dict and set(cert)=={'version','kappa','upper','degree','coefficients','cells','splice'}
             and cert['version']=='KAPPA_62_625_SCALAR_V1'and cert['kappa']=='62/625'and cert['upper']=='625/124'
             and type(cert['degree'])is int and cert['degree']==13 and same(cert['coefficients'],COEFFICIENTS),
             'Fixed scalar polynomial and full domain')
    src.need(type(cert['cells'])is list and len(cert['cells'])==81,'All81 closed scalar cells')
    values=[]
    for i,row in enumerate(cert['cells']):
        bounds=[str(F(i,16)),str(F(i+1,16))]if i<80 else['5','625/124']
        src.need(type(row)is dict and set(row)=={'interval','bernstein'}and same(row['interval'],bounds)
                 and type(row['bernstein'])is list and len(row['bernstein'])==14,'Whole fixed ordered scalar cover')
        bs=[rat(v)for v in row['bernstein']];src.need(all(v>0 for v in bs),'Positive recorded scalar coefficients');values+=bs
    splice=cert['splice'];src.need(type(splice)is dict and set(splice)=={'cosine_deficit','sine_lower','scale_A','join_numerator_lower','pi_bracket'},
                                  'Complete changed-splice certificate')
    for key in('cosine_deficit','scale_A','pi_bracket'):
        src.need(type(splice[key])is list and len(splice[key])==2,'Exact splice endpoint pair')
        lo,hi=map(rat,splice[key]);src.need(0<lo<=hi,'Positive ordered splice interval')
    rat(splice['sine_lower']);src.need(rat(splice['join_numerator_lower'])>0,'Positive recorded changed-splice margin')
    fields={'status','mathematical_status','receipt','negative_controls','additional_identity_checks','source_sha256'}
    expected_sources={original(request,'capsule/'+n):src.digest(capsule/n)for n in src.FILES+('CERTIFICATE.json',)}
    expected_receipt=dict(cells=81,positive_coefficients=1134,minimum_bernstein=str(min(values)))
    src.need(type(checked)is dict and set(checked)==fields and checked['status']==STATUS
             and checked['mathematical_status']==MATHEMATICAL_STATUS and same(checked['receipt'],expected_receipt)
             and type(checked['negative_controls'])is int and checked['negative_controls']==21
             and type(checked['additional_identity_checks'])is int and checked['additional_identity_checks']==324
             and same(checked['source_sha256'],expected_sources)and same(stdout_packet,checked),
             'Current whole scalar receipt,21negative+324identity controls and actual source/certificate identity')
    return dict(kappa='62/625',global_domain='all real x',certificate_domain=['0','625/124'],
                cells=81,bernstein_coefficients=1134,negative_controls=21,additional_identity_checks=324,
                certificate_sha256=src.digest(capsule/'CERTIFICATE.json'),checked_sha256=src.digest(capsule/'CHECKED.json'),
                scalar_fact='cos(x)<=1-x^2/2+(62/625)*abs(x)^3; associated nonnegative convex decreasing splice on z>=0')


def inventory(task):
    task=Path(task);out={}
    for p in sorted(task.rglob('*')):
        src.ordinary(p)
        if p.is_file()and p.relative_to(task).as_posix()not in('STAGE_OBSERVED.json','STAGE_COMPLETED.json'):
            out[p.relative_to(task).as_posix()]=dict(bytes=p.stat().st_size,sha256=src.digest(p))
    return out


def validate_run(task,report):
    task=Path(task).resolve();request=src.verify(task)
    fields={'schema','scope','original_task_root','implementation','python_executable','python_version','observed',
            'scalar_certificate_arithmetic_completed',*FLAGS}
    src.need(type(report)is dict and set(report)==fields and report['schema']==OBSERVED and report['scope']==SCOPE
             and same(report['implementation'],implementation())and report['original_task_root']==request['original_task_root']
             and type(report['python_version'])is str and bool(report['python_version'])
             and report['scalar_certificate_arithmetic_completed']is False and all(report[k]is False for k in FLAGS),
             'Exact current scalar-only observed stage, without promoted proof flags')
    packet=transport(task,request,report['observed'],report['python_executable'])
    return scalar_outputs(task,request,packet)


def validate_completed(task):
    task=Path(task).resolve();observed=src.read(task/'STAGE_OBSERVED.json');summary=validate_run(task,observed)
    done=src.read(task/'STAGE_COMPLETED.json')
    fields={'schema','scope','implementation','observed_sha256','summary','artifacts','scalar_certificate_arithmetic_completed',*FLAGS}
    src.need(type(done)is dict and set(done)==fields and done['schema']==COMPLETED and done['scope']==SCOPE
             and same(done['implementation'],implementation())and done['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')
             and same(done['summary'],summary)and same(done['artifacts'],inventory(task))
             and done['scalar_certificate_arithmetic_completed']is True and all(done[k]is False for k in FLAGS),
             'Whole current completed scalar transaction and actual sealed evidence')
    return dict(schema='REVALIDATED_FINITE1014_KAPPA_V1',scope=SCOPE,summary=summary,
                stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),
                scalar_certificate_arithmetic_completed=True,**{k:False for k in FLAGS})
