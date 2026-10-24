"""Pure57E stopped/source/port evidence; no original numerical imports."""
from __future__ import annotations
import math,re
from pathlib import Path,PureWindowsPath,PurePosixPath
from . import finite1519_high_sources as src
from .finite1039_count_evidence import same,mapped,inventory,terminal
SCOPE='ORIGINAL_COMPENSATED_HIGH15_19_CURRENT_CAPTURE_ONLY_EPOCH_BASIC_V1'
OBSERVED='OBSERVED_FINITE1519_COMPENSATED_HIGH_V1'
COMPLETED='COMPLETED_FINITE1519_COMPENSATED_HIGH_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
FLAGS=('native_arithmetic_accepted','full_notebook57_completed','parent_acquisitions_verified','support_acquisition_verified',
 'support_high_initial_resource_acquired','resource_to_count147_interfaces_verified','full_finite1039_verified','all_index_conclusion_verified')
def implementation():
 names=('finite1519_high.py','finite1519_high_sources.py','finite1519_high_evidence.py','finite1519_high_worker.py',
  'finite1039_sources.py','finite1039_count_evidence.py','n5_remaining_sources.py','linux_supervisor.py','colab_batch.py')
 return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)
def path(request,relative):
 root=request['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
 src.need(cls(root).is_absolute(),'Original absolute task root');return str(cls(root)/relative)
def original_path(request,relative):return path(request,'capsule/'+relative)
def command(request,action,python):
 src.need(action in src.ACTIONS and type(python)is str and(PureWindowsPath(python).is_absolute()or PurePosixPath(python).is_absolute()),'Actual original interpreter/action')
 if action=='readback':return[python,'-B',original_path(request,src.FRESH)]
 return[python,'-B','-S',path(request,src.WORKER),'--task',request['original_task_root'],'--action',action]
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



def inner(task,request,action,report,outer):
 c=Path(task)/'capsule';directory=c/src.RUNS/src.LABELS[action];meta=src.read(directory/'metadata.json')
 expected={'schema','command','cwd','input_sha256','python','returncode','elapsed_seconds','stdout_sha256','stderr_sha256',
  'result_sha256','outer_launch_sha256','scope','proof_accepted'}
 expected_command=[report['python_executable'],'-B','bound.py',original_path(request,src.RUNS+'/'+src.LABELS[action]+'/RESULT.json')]
 inputs={n:src.digest(c/src.NATIVE/n)for n in('MANIFEST.json','bound.py','kernel.py','universal.py')}
 src.need(set(meta)==expected and meta['schema']=='CURRENT_REAL_CHILD_COMPENSATED_HIGH_CAPTURE_V1'
  and same(meta['command'],expected_command)and meta['cwd']==original_path(request,src.NATIVE)and same(meta['input_sha256'],inputs)
  and meta['python']==report['python_version']and type(meta['returncode'])is int and meta['returncode']==0
  and meta['outer_launch_sha256']==src.digest(Path(task)/'executions'/action/'launch.json')
  and meta['scope']=='Genuine original child under outer BASIC process-group supervision; not historical/native acceptance'
  and meta['proof_accepted']is False,'Genuine current original inner OS command/cwd/source/context, without native promotion')
 finite(meta['elapsed_seconds'])
 for kind in('stdout','stderr'):
  src.need(src.digest(directory/(kind+'.txt'))==meta[kind+'_sha256'],'Actual original child stream bytes')
 src.need((directory/'stderr.txt').stat().st_size==0 and(directory/'stdout.txt').read_text('utf-8')==outer,
  'Original child stdout propagates exactly; successful stderr empty')
 src.need(meta['result_sha256']==src.digest(directory/'RESULT.json')==src.plan()['original_native_result_sha256'],
  'Fresh whole deterministic proof equals unchanged original result commitment')
 result=src.read(directory/'RESULT.json')
 src.need(result['status']=='PASS_SUPPORTED_COMPENSATED_HIGH15_19'and result['manifest_sha256']==src.plan()['original_manifest_sha256']
  and same(result['controls'],dict(malformed_domains=8))and type(result['rows'])is list and len(result['rows'])==15,
  'Full original five-index three-band supported HIGH, all8 original domain controls')
 lines=outer.splitlines();src.need(lines and lines[-1]=='PASS_SUPPORTED_COMPENSATED_HIGH15_19','Actual original successful native terminal')
 return result

def summarize(task,request,report,stdout):
 c=Path(task)/'capsule';a=inner(task,request,'construct',report,stdout['construct']);b=inner(task,request,'replay',report,stdout['replay'])
 src.need(same(a,b),'Whole exact original native proof equality from both genuine runs')
 epoch=src.read(Path(task)/'CAPTURE_EPOCH.json');derived,expected_epoch=src.current_derivation(task)
 src.need(same(epoch,expected_epoch)and(c/src.FRESH).read_bytes()==derived,'Byte/AST checked sole CAPTURE_SHA replacement')
 result=src.read(c/src.RESULT);body={k:v for k,v in result.items()if k!='files_sha256'}
 src.need(same(body,src.plan()['expected_readback'])and same(terminal(stdout['readback']),body),
  'Complete unchanged independent readback fields, all34 controls, exact current terminal')
 graph=dict(src.read(c/src.NATIVE/'MANIFEST.json')['files_sha256'])
 src.need(len(graph)==71,'Complete unchanged original native source graph')
 for name in(src.NATIVE+'/MANIFEST.json',src.AUDIT+'/check.py',src.AUDIT+'/REVIEW.txt'):
  graph[name]=src.digest(c/name)
 for action in('construct','replay'):
  for name in src.output_paths(action):graph[name]=src.digest(c/name)
 src.need(same(result['files_sha256'],graph),'Full exact readback source and current-capture graph')
 for name,pin in graph.items():src.need(src.digest(c/name)==pin,'Every readback graph row binds actual bytes')
 return dict(n_values=list(range(15,20)),support_radius='3',rho_upper=['11/10','23/20','33/25'],
  rows=15,native_domain_controls=8,readback_controls=34,original_manifest_sha256=src.plan()['original_manifest_sha256'],
  native_result_sha256=src.plan()['original_native_result_sha256'],original_readback_sha256=src.plan()['original_readback_sha256'],
  derived_readback_sha256=epoch['derived_readback_sha256'],capture_epoch_sha256=src.digest(Path(task)/'CAPTURE_EPOCH.json'),
  actual_capture_sha256=epoch['actual_capture_sha256'],receipt_sha256=src.digest(c/src.RESULT),per_band_per_n_upper=result['per_band_per_n_upper'],
  only_capture_hash_dictionary_changed=True,original_numerical_functions_unchanged=True,actual_support_acquired=False)

def validate_run(task,report):
 task=src.ordinary(task);request=src.verify_job(task)
 src.need(report['schema']==OBSERVED and report['scope']==SCOPE and report['original_task_root']==request['original_task_root']
  and same(report['implementation'],implementation())and type(report['python_version'])is str and bool(report['python_version'])
  and report['conditional_compensated_high_arithmetic_completed']is False and all(report[k]is False for k in FLAGS),
  'Exact current HIGH execution epoch and truthful unaccepted observed ledger')
 actions=report['actions'];src.need(type(actions)is list and[x['action']for x in actions]==list(src.ACTIONS),'All three complete original HIGH actions')
 stdout={x['action']:transport(task,request,x['action'],x['observed'],report)for x in actions}
 return summarize(task,request,report,stdout)
def validate_completed(task, *,original_task_root=None):
 task=src.ordinary(task);request=src.verify_job(task)
 if original_task_root is not None:src.need(str(original_task_root)==request['original_task_root'],'One preserved original task context')
 d=src.read(task/'STAGE_COMPLETED.json');o=src.read(task/'STAGE_OBSERVED.json')
 src.need(d['schema']==COMPLETED and d['scope']==SCOPE and same(d['implementation'],implementation())
  and d['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')and d['conditional_compensated_high_arithmetic_completed']is True
  and all(d[k]is False for k in FLAGS),'Complete strict HIGH ledger without support/framework promotion')
 summary=validate_run(task,o)
 src.need(same(d['summary'],summary)and same(d['artifacts'],inventory(task)),'Full stopped source/capture/port/output inventory')
 return dict(schema='REVALIDATED_CONDITIONAL_COMPENSATED_HIGH15_19_V1',source_plan_sha256=src.PLAN_SHA256,
  stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),summary=summary,conditional_compensated_high_arithmetic_completed=True,**{k:False for k in FLAGS})
