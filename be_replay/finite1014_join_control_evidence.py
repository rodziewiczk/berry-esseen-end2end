"""Pure readback of actual56I bounded-control executions; no kernel imports."""
from __future__ import annotations
import math
from pathlib import Path
from . import finite1014_join_sources as src
from .finite1014_join_epoch import same
from .finite1014_kappa_evidence import pathclass
SCOPE='FINITE1014_FULL_BOUNDED_CONTROLS_CURRENT_METADATA_BASIC_23H_V1'
OBSERVED='OBSERVED_FINITE1014_JOIN_CONTROL_V1'
COMPLETED='COMPLETED_FINITE1014_JOIN_CONTROL_V1'
CPU_SECONDS=WALL_SECONDS=82800
MEMORY_BYTES=2048*src.MIB
DISK_BYTES=512*src.MIB
LOG_BYTES=16*src.MIB
FLAGS=('native_arithmetic_accepted','parent_acquisitions_verified','full_notebook56_completed',
       'all_law_conclusion_verified','all_index_conclusion_verified')


def implementation():
 names=('finite1014_join_sources.py','finite1014_join_epoch.py','finite1014_join_control_evidence.py',
  'finite1014_join.py','finite1014_kappa_sources.py','finite1014_kappa_evidence.py',
  'finite1014_core_sources.py','linux_supervisor.py','colab_batch.py','environment.py')
 return{n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)


def mapped(task,value,original):
 cls=pathclass(original);src.need(type(value)is str and '\0'not in value,'Recorded ordinary evidence path');p=cls(value)
 src.need(p.is_absolute(),'Absolute originating evidence context')
 try:rel=p.relative_to(cls(original))
 except ValueError:raise ValueError('Evidence escapes its explicit originating task root')
 src.need(rel.parts and all(x not in('.','..')for x in rel.parts),'Contained restored evidence')
 return src.ordinary(Path(task).joinpath(*rel.parts))


def command(row,python):
 src.need(type(python)is str and bool(python),'Recorded actual Python executable')
 return[python,'-B',row['script'],*row['arguments']]


def guard():
 return dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(WALL_SECONDS),
  per_process_RLIMIT_AS_bytes=MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=CPU_SECONDS,aggregate_kernel_memory_limit=False,
  aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY_BYTES,sampled_group_CPU_limit_seconds=CPU_SECONDS,
  sampled_file_limit_bytes=DISK_BYTES,sampled_log_limit_bytes=LOG_BYTES,descendants_changing_session_are_contained=False,
  equivalent_to_Windows_Job_or_cgroup=False)


def inventory(task):
 root=Path(task);out={}
 for p in sorted(root.rglob('*')):
  src.ordinary(p)
  if not p.is_file():continue
  rel=p.relative_to(root).as_posix()
  if rel=='STAGE_COMPLETED.json':continue
  src.need(p.stat().st_size<=64*src.MIB,'Bounded actual control artifact');out[rel]=dict(bytes=p.stat().st_size,sha256=src.digest(p))
 src.need(len(out)<=10000 and sum(r['bytes']for r in out.values())<=512*src.MIB,'Bounded full completed control task')
 return out


def _finite(v):src.need(type(v)in(int,float)and math.isfinite(v)and v>=0,'Finite actual resource observation')


def transport(task,row,report,request):
 task=Path(task);original=request['original_task_root'];observed=report['observed'];directory=task/'execution'
 src.need(same(src.read(directory/'supervisor-result.json'),observed)and observed['status']=='completed'
  and type(observed['returncode'])is int and observed['returncode']==0 and observed['reason']is None
  and observed['mode']=='untrusted_search'and observed['proof_accepted']is False
  and type(observed['sample_count'])is int and observed['sample_count']>0,'Actual stopped successful BASIC control execution')
 for k in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):_finite(observed[k])
 launch=src.read(directory/'launch.json');fields={'argv','cwd','output_dir','mode','cpu_seconds','wall_seconds','memory_bytes',
  'disk_bytes','log_bytes','sample_seconds','heartbeat_seconds','checkpoint_paths'}
 src.need(set(launch)==fields and same(launch['argv'],command(row,report['python_executable']))
  and mapped(task,launch['cwd'],original)==task/'capsule'/row['directory']
  and mapped(task,launch['output_dir'],original)==directory and launch['mode']=='untrusted_search'
  and type(launch['cpu_seconds'])is int and launch['cpu_seconds']==CPU_SECONDS
  and type(launch['wall_seconds'])in(int,float)and launch['wall_seconds']==WALL_SECONDS
  and type(launch['memory_bytes'])is int and launch['memory_bytes']==MEMORY_BYTES
  and type(launch['disk_bytes'])is int and launch['disk_bytes']==DISK_BYTES
  and type(launch['log_bytes'])is int and launch['log_bytes']==LOG_BYTES
  and type(launch['sample_seconds'])in(int,float)and launch['sample_seconds']==.2
  and type(launch['heartbeat_seconds'])in(int,float)and launch['heartbeat_seconds']==20
  and type(launch['checkpoint_paths'])is list and len(launch['checkpoint_paths'])==1
  and mapped(task,launch['checkpoint_paths'][0],original)==task/'capsule'/row['output'],
  'Literal unchanged control command/cwd, actual requested stopped capture and fixed23h budgets')
 src.need(same(observed['guard_scope'],guard()),'Honest per-process and sampled-live-group BASIC resource contract')
 finished=dict(event='linux_supervisor_finished',stage='untrusted_search',status='completed',reason=None,
  elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
 lines=src.ordinary(directory/'progress.jsonl').read_text(encoding='utf-8').splitlines()
 src.need(lines and same(src.base.loads(lines[-1]),finished)and same(src.read(directory/'progress.json'),finished),'Actual final stopped supervisor history')
 streams={}
 for kind in('stdout','stderr'):
  p=mapped(task,observed[kind+'_path'],original);src.need(p==directory/(kind+'.txt')and p.is_file()
   and p.stat().st_size<=LOG_BYTES and src.digest(p)==observed[kind+'_sha256'],'Actual bounded supervisor capture SHA')
  streams[kind]=p
 src.need(streams['stderr'].stat().st_size==0,'Successful unchanged control stderr is empty')
 captures=observed['checkpoints'];src.need(type(captures)is list and len(captures)==1,'One whole stopped result/reference capture')
 cp=captures[0];output=task/'capsule'/row['output'];cwd=task/'capsule'/row['directory'];copy=directory/'checkpoints'/output.relative_to(cwd)
 src.need(set(cp)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}and cp['exists']is True
  and cp['trusted_certificate']is False and mapped(task,cp['source_path'],original)==output
  and mapped(task,cp['path'],original)==copy and output.is_file()and copy.is_file()
  and type(cp['bytes'])is int and 0<cp['bytes']<=16*src.MIB and cp['bytes']==output.stat().st_size==copy.stat().st_size
  and cp['sha256']==src.digest(output)==src.digest(copy),'Full actual stopped output bytes, including readonly source record when selected')
 return streams


def summarize(task,row,streams):
 task=Path(task);output=task/'capsule'/row['output'];current=src.read(output,16*src.MIB);old=src.read(task/'provenance/reference.json',16*src.MIB)
 src.need(type(current)is dict and type(old)is dict and current.get('status')==row['expected_status']
  and set(current)==set(old)and same({k:v for k,v in current.items()if k!='files_sha256'},
   {k:v for k,v in old.items()if k!='files_sha256'}),'Every original mathematical/control/status/schema field retained; no recursive timing erasure')
 missing=src.plan()['unavailable_historical_inputs'];expected={}
 for name in old['files_sha256']:
  if name in missing:continue
  p=src.ordinary(task/'capsule'/name);src.need(p.is_file(),'Every original available result source edge remains actual');expected[name]=src.digest(p)
 src.need(same(current['files_sha256'],expected),'Exact complete current result source graph, with only declared missing historical run edges omitted')
 for name,pin in row['generated_sources'].items():src.need(src.digest(task/'capsule'/name)==pin,'Every generated copied helper is original')
 stdout=streams['stdout'].read_text(encoding='utf-8').strip();sha=src.digest(output)
 if row['slot']=='range':src.need(same(src.base.loads(stdout),current),'Full native range terminal object equals actual output')
 elif row['slot']in('signed_low','resource_count_port'):
  src.need(same(src.base.loads(stdout),{k:v for k,v in current.items()if k!='files_sha256'}),'Full native bounded-control terminal object equals actual mathematical output')
 elif row['slot']=='subpanel_baseline':src.need(stdout==current['status']+' '+row['arguments'][0]+' '+sha,'Original closed-subpanel successful terminal and exact result hash')
 elif row['slot']=='subpanel_fine':src.need(stdout==current['status']+' 42 '+sha,'Original fine closed-subpanel successful terminal and exact result hash')
 elif row['slot']=='fine_initial':src.need(stdout==current['status']+' '+sha,'Original fine-INITIAL successful terminal and exact result hash')
 else:src.need(row['slot']=='fine_bn_record'and stdout=='SOURCE_REVIEW_IDENTITIES_CURRENT '+sha,'Original retained source-record identity check, never new theorem acquisition')
 return dict(job_id=row['job_id'],slot=row['slot'],status=current['status'],output_relative='capsule/'+row['output'],
  output_sha256=sha,reference_sha256=src.digest(task/'provenance/reference.json'),metadata_epoch_sha256=src.digest(task/src.META),
  mathematical_projection_identical=True,original_python_unchanged=True,read_only_record=row['read_only_record'],
  original_source_graph_rows=len(old['files_sha256']),current_source_graph_rows=len(current['files_sha256']),
  control_counts=current.get('counts'),negative_controls=current.get('negative_controls'),**{f:False for f in FLAGS})


def validate_run(task,report):
 request,row=src.verify(task)
 src.need(report['schema']==OBSERVED and report['scope']==SCOPE and report['job_id']==row['job_id']
  and same(report['implementation'],implementation())and report['original_task_root']==request['original_task_root']
  and report['conditional_controls_completed']is False and all(report[k]is False for k in FLAGS),
  'Exact source-bound observed-false control implementation and scope')
 for key,value in(('cpu_seconds',CPU_SECONDS),('wall_seconds',WALL_SECONDS),('memory_bytes',MEMORY_BYTES)):
  src.need(type(report[key])is int and report[key]==value,'Fixed control execution budgets')
 streams=transport(task,row,report,request);summary=summarize(task,row,streams);src.verify(task);return summary


def validate_completed(task):
 task=Path(task);report=src.read(task/'STAGE_OBSERVED.json',8*src.MIB);summary=validate_run(task,report);done=src.read(task/'STAGE_COMPLETED.json',16*src.MIB)
 src.need(done['schema']==COMPLETED and done['scope']==SCOPE and done['job_id']==summary['job_id']
  and same(done['implementation'],report['implementation'])and done['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')
  and done['conditional_controls_completed']is True and same(done['summary'],summary)
  and same(done['artifacts'],inventory(task))and all(done[k]is False for k in FLAGS),'Complete genuine control task with full source/capture/result inventory')
 return dict(schema='REVALIDATED_FINITE1014_JOIN_CONTROL_V1',summary=summary,
  completed_sha256=src.digest(task/'STAGE_COMPLETED.json'),source_manifest_sha256=src.digest(task/'SOURCES.json'),
  conditional_controls_completed=True,**{f:False for f in FLAGS})
