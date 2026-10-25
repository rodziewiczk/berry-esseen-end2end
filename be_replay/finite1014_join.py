"""56I: full original bounded controls and finite-only10--14 semantic join.

Only completed whole stages resume. No original numerical module is imported by
this controller; unchanged original controls run solely in guarded children.
"""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import shutil,stat,sys,threading,time,traceback,uuid,zipfile
from . import finite1014_join_sources as src,finite1014_join_control_evidence as ev,linux_supervisor
from .colab_batch import atomic_json,bundle,event,utc
CACHE_BYTES=512*src.MIB


class Follow:
 def __init__(self,root,task,job_id):
  self.root,self.task,self.job_id=Path(root),Path(task),job_id;self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
 def loop(self):
  position=0;partial=b'';began=time.monotonic();last=-20;draining=False
  while True:
   try:
    with(self.task/'execution/stdout.txt').open('rb')as stream:stream.seek(position);raw=stream.read(src.MIB)
    position+=len(raw);lines=(partial+raw).split(b'\n');partial=lines.pop()
    for line in lines:event(self.root,'finite1014_join_original_stdout',job_id=self.job_id,line=line.decode('utf-8',errors='replace')[:4096])
   except FileNotFoundError:pass
   elapsed=time.monotonic()-began
   if elapsed-last>=20:event(self.root,'finite1014_join_heartbeat',job_id=self.job_id,elapsed_seconds=elapsed,stdout_bytes=position,full_notebook56_completed=False);last=elapsed
   if self.stop.wait(.2):
    if draining:break
    draining=True
 def __enter__(self):self.thread.start();return self
 def __exit__(self,*unused):self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped progress reader')


def execute(job_id,cache,task,*,root,dependencies=None):
 src.need(sys.platform=='linux','Actual Linux BASIC process-tree execution required');task=Path(task).resolve();request,row=src.prepare(job_id,cache,task,dependencies=dependencies)
 event(root,'finite1014_join_original_control_started',job_id=job_id,cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,
  memory_bytes=ev.MEMORY_BYTES,partial_numerical_resume=False,full_notebook56_completed=False)
 with Follow(root,task,job_id):
  observed=linux_supervisor.run(ev.command(row,sys.executable),cwd=task/'capsule'/row['directory'],output_dir=task/'execution',
   mode='untrusted_search',cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,
   disk_bytes=ev.DISK_BYTES,log_bytes=ev.LOG_BYTES,heartbeat_seconds=20,checkpoint_paths=[task/'capsule'/row['output']])
 report=dict(schema=ev.OBSERVED,scope=ev.SCOPE,job_id=job_id,original_task_root=request['original_task_root'],
  implementation=ev.implementation(),python_executable=sys.executable,python_version=sys.version,
  cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,observed=observed,
  conditional_controls_completed=False,**{f:False for f in ev.FLAGS})
 atomic_json(task/'STAGE_OBSERVED.json',report)
 try:summary=ev.validate_run(task,report)
 except BaseException as error:
  tail='';p=task/'execution/stderr.txt'
  if p.is_file()and not p.is_symlink():
   with p.open('rb')as stream:stream.seek(max(0,p.stat().st_size-4096));tail=stream.read(4096).decode('utf-8',errors='replace')
  event(root,'finite1014_join_control_incomplete',job_id=job_id,error=type(error).__name__+': '+str(error),reason=observed.get('reason'),stderr_tail=tail,full_notebook56_completed=False)
  raise ValueError('Original56Icontrol '+job_id+' did not validate: '+str(error)+'; stderr tail: '+tail)from error
 done=dict(schema=ev.COMPLETED,scope=ev.SCOPE,job_id=job_id,implementation=ev.implementation(),observed_sha256=src.digest(task/'STAGE_OBSERVED.json'),
  summary=summary,artifacts=ev.inventory(task),conditional_controls_completed=True,**{f:False for f in ev.FLAGS})
 atomic_json(task/'STAGE_COMPLETED.json',done);checked=ev.validate_completed(task)
 event(root,'finite1014_join_control_completed',job_id=job_id,summary=summary,full_notebook56_completed=False)
 return checked


def cache_members(z):
 rows=z.infolist();src.need(0<len(rows)<=10000,'Bounded full control ZIP inventory');seen=set();total=0
 for info in rows:
  src.need(not info.is_dir(),'Completed-stage ZIP contains files only');src.parts(info.filename);fold=info.filename.casefold()
  src.need(fold not in seen,'No duplicate/case-colliding completed entry');seen.add(fold)
  src.need(stat.S_IFMT(info.external_attr>>16)in(0,stat.S_IFREG)and not info.flag_bits&1,'No linked/special/encrypted cache entry')
  src.need(0<=info.file_size<=64*src.MIB,'Bounded complete artifact');total+=info.file_size
  src.need(info.filename.split('/')[0]in('capsule','provenance','execution','SOURCES.json',src.META,'STAGE_OBSERVED.json','STAGE_COMPLETED.json'),'Exact control cache namespace')
 src.need(total<=CACHE_BYTES and {'SOURCES.json',src.META,'STAGE_OBSERVED.json','STAGE_COMPLETED.json','execution/launch.json',
  'execution/supervisor-result.json','execution/stdout.txt','execution/stderr.txt'}<=set(r.filename for r in rows),'Full source/launch/stopped capture/completion ledger required')
 return rows


def save_completed(task,cache):
 task=Path(task).resolve();checked=ev.validate_completed(task);cache=src.ordinary(cache);cache.mkdir(parents=True,exist_ok=True)
 name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip';p=cache/name;pending=cache/(name+'.pending')
 with zipfile.ZipFile(pending,'x',zipfile.ZIP_DEFLATED)as z:
  for file in sorted(task.rglob('*')):
   src.ordinary(file)
   if file.is_file():z.write(file,file.relative_to(task).as_posix())
 with zipfile.ZipFile(pending)as z:cache_members(z)
 src.need(pending.stat().st_size<=CACHE_BYTES,'Bounded complete control ZIP');pin=src.digest(pending);pending.replace(p)
 marker=p.with_suffix('.zip.sha256');tmp=marker.with_name(marker.name+'.pending');tmp.write_bytes((pin+'  '+p.name+'\n').encode('ascii'));tmp.replace(marker)
 return dict(path=str(p),sha256=pin,completed_sha256=checked['completed_sha256'])


def restore_completed(job_id,cache,destination,*,root):
 cache=src.ordinary(cache);destination=Path(destination)
 if not cache.exists():return None
 for p in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
  try:
   src.ordinary(p);marker=src.ordinary(p.with_suffix('.zip.sha256'))
   src.need(p.is_file()and p.stat().st_size<=CACHE_BYTES and marker.is_file()and marker.stat().st_size<=1024
    and marker.read_text('ascii')==src.digest(p)+'  '+p.name+'\n','Actual complete control ZIP sidecar')
   restored=destination/(job_id+'-restored-'+uuid.uuid4().hex[:8])
   with zipfile.ZipFile(p)as z:
    rows=cache_members(z);restored.mkdir(parents=True,exist_ok=False)
    for row in rows:
     out=restored.joinpath(*src.parts(row.filename));out.parent.mkdir(parents=True,exist_ok=True)
     with z.open(row)as source,out.open('xb')as target:shutil.copyfileobj(source,target,src.MIB)
   checked=ev.validate_completed(restored);src.need(checked['summary']['job_id']==job_id,'No cross-control cache')
   event(root,'finite1014_join_completed_control_revalidated',job_id=job_id,cache=str(p),sha256=src.digest(p),numerical_replay_skipped=True)
   return restored,checked,dict(path=str(p),sha256=src.digest(p))
  except Exception as error:event(root,'finite1014_join_control_cache_rejected',job_id=job_id,cache=str(p),error=type(error).__name__+': '+str(error))
 return None


class Backups:
 def __init__(self,root,durable,interval):
  self.root,self.durable,self.interval=Path(root),Path(durable),interval;self.stop=threading.Event();self.error=None;self.thread=threading.Thread(target=self.loop,daemon=True)
 def copy(self):
  for p in self.root.rglob('*'):
   if not p.is_file():continue
   rel=p.relative_to(self.root);name=rel.as_posix()
   if any(t in name for t in('/capsule/','/provenance/','/imports/'))or name.startswith(('imports/','source-cache/'))or p.stat().st_size>16*src.MIB:continue
   if p.suffix not in('.json','.jsonl','.txt'):continue
   src.ordinary(p);out=self.durable/'live'/rel;out.parent.mkdir(parents=True,exist_ok=True);tmp=out.with_name(out.name+'.pending');shutil.copyfile(p,tmp);tmp.replace(out)
 def loop(self):
  while not self.stop.wait(self.interval):
   try:self.copy();event(self.root,'finite1014_join_live_backup_saved',complete_stage_ZIPs_separate=True)
   except BaseException as error:self.error=type(error).__name__+': '+str(error);event(self.root,'finite1014_join_backup_error',error=self.error)
 def start(self):self.thread.start()
 def close(self):self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped backup worker');self.copy()


def run_controls(root,completed_cache,source_cache,status):
 dependencies={}
 for row in src.jobs():
  found=restore_completed(row['job_id'],Path(completed_cache)/row['job_id'],Path(root)/'controls',root=root)
  if found:
   task,checked,export=found;reused=True
   request,_=src.verify(task)
   wanted={n:src.digest(p)for n,p in dependencies.items()if n in request['original_sources']}
   src.need(request['dependency_files_sha256']==wanted,'Completed control retains exact earlier current-control inputs')
  else:
   task=Path(root)/'controls'/(row['job_id']+'-'+uuid.uuid4().hex[:8]);available={n:p for n,p in dependencies.items()if n in src.original_inputs(row)}
   checked=execute(row['job_id'],source_cache,task,root=root,dependencies=available);export=save_completed(task,Path(completed_cache)/row['job_id']);reused=False
  if row['output']in src.DEPENDENCIES:dependencies[row['output']]=task/'capsule'/row['output']
  status['controls'].append(dict(job_id=row['job_id'],task_relative=task.relative_to(root).as_posix(),validated=checked,export=export,reused_completed_stage=reused))
  atomic_json(Path(root)/'SESSION_RESULT.json',status);event(root,'finite1014_join_controls_progress',completed=len(status['controls']),total=len(src.jobs()),reused_completed_stage=reused,full_notebook56_completed=False)
 return status['controls']


def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
 from .environment import snapshot
 src.need(sys.platform=='linux','This full current-capture protocol requires Linux');src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=300,'Finite backup interval')
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8];root=Path(work_root).resolve()/'finite1014-join'/stamp;root.mkdir(parents=True,exist_ok=False)
 durable=Path(durable_root).resolve()/'finite1014-join'/stamp;cache=Path(durable_root).resolve()/'finite1014-join/completed'/src.PLAN_SHA256[:16]
 status=dict(schema='FINITE1014_FULL_FINITE_JOIN_SESSION_V1',state='incomplete',started_utc=utc(),controls=[],imports=[],
  conditional_controls_completed=False,conditional_finite_chain_verified=False,**{f:False for f in ev.FLAGS})
 atomic_json(root/'ENVIRONMENT.json',snapshot());atomic_json(root/'SESSION_RESULT.json',status);backups=Backups(root,durable,backup_interval);backups.start()
 event(root,'finite1014_join_started',control_calls=10,source_plan_sha256=src.PLAN_SHA256,cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,
  policy=ev.SCOPE,full_notebook56_completed=False)
 try:
  assets=src.obtain_assets(archives,progress=lambda name,**data:event(root,name,**data));source_cache=src.prepare_cache(assets,root/'source-cache',progress=lambda name,**data:event(root,name,**data))
  run_controls(root,cache,source_cache,status);status['conditional_controls_completed']=True
  from . import finite1014_join_evidence as semantic
  missing=semantic.import_completed_inputs(root,durable_root,status)
  if missing:status.update(state='waiting_for_prerequisite_exports',missing=missing)
  else:
   proposed=semantic.validate_batch(root,status);status.update(state='complete_finite10_14_under_explicit_analytic_premises',conditional_finite_chain_verified=True,finite_summary=proposed,finished_utc=utc())
   atomic_json(root/'SESSION_RESULT.json',status);semantic.validate_completed(root)
 except BaseException as error:
  status.update(state='incomplete',conditional_finite_chain_verified=False,error=type(error).__name__+': '+str(error));(root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8',newline='\n')
  event(root,'finite1014_join_incomplete',error=status['error'],completed_controls=len(status['controls']),full_notebook56_completed=False)
 finally:
  status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
  try:backups.close()
  except BaseException as error:status.update(state='incomplete',conditional_finite_chain_verified=False,backup_error=type(error).__name__+': '+str(error));atomic_json(root/'SESSION_RESULT.json',status)
  if backups.error:
   status.update(state='incomplete',conditional_finite_chain_verified=False,backup_error=backups.error);atomic_json(root/'SESSION_RESULT.json',status)
  try:archive=bundle(root,durable)
  except BaseException as error:
   status.update(state='incomplete',conditional_finite_chain_verified=False,bundle_error=type(error).__name__+': '+str(error));atomic_json(root/'SESSION_RESULT.json',status)
   archive=bundle(root,Path(work_root).resolve()/'finite1014-join-local-exports'/stamp)
  result=dict(path=str(archive),sha256=src.digest(archive));event(root,'finite1014_join_final_bundle',state=status['state'],**result)
  if status['state']=='complete_finite10_14_under_explicit_analytic_premises'and status['conditional_finite_chain_verified']is True:
   try:
    index=Path(durable_root).resolve()/'finite1014-join/completed-finite'/src.PLAN_SHA256[:16]/(stamp+'.json');index.parent.mkdir(parents=True,exist_ok=True)
    atomic_json(index,dict(schema='FINITE1014_COMPLETE_FINITE_EXPORT_INDEX_V1',source_plan_sha256=src.PLAN_SHA256,
     path=str(archive),sha256=result['sha256'],sidecar_path=str(archive.with_suffix('.zip.sha256')),session_root=stamp,
     session_result_sha256=src.digest(root/'SESSION_RESULT.json'),pure_validator='be_replay.finite1014_join_evidence.validate_completed',
     conditional_finite_chain_verified=True,**{f:False for f in ev.FLAGS}))
   except BaseException as error:event(root,'finite1014_join_discovery_index_incomplete',error=type(error).__name__+': '+str(error),actual_final_bundle_preserved=True)
 return dict(status=status,bundle=result,work=str(root))
