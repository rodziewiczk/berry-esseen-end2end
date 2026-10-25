"""57H complete six-control execution and finite15--19 semantic join."""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import shutil,sys,threading,traceback,uuid
from . import finite1519_join_control_sources as src,finite1519_join_controls as controls
from . import finite1519_join_control_evidence as ev,finite1519_join_evidence as semantic
from .colab_batch import atomic_json,bundle,event,utc


class Backups:
 def __init__(self,root,durable,interval):
  self.root,self.durable,self.interval=Path(root),Path(durable),interval
  self.stop=threading.Event();self.error=None;self.thread=threading.Thread(target=self.loop,daemon=True)
 def copy(self):
  for path in self.root.rglob('*'):
   src.ordinary(path)
   if not path.is_file():continue
   rel=path.relative_to(self.root)
   if any(part in('capsule','provenance','imports','source-cache','upstream')for part in rel.parts):continue
   if path.suffix not in('.json','.jsonl','.txt')or path.stat().st_size>16*src.MIB:continue
   destination=self.durable/'live'/rel;destination.parent.mkdir(parents=True,exist_ok=True)
   temporary=destination.with_name(destination.name+'.pending');shutil.copyfile(path,temporary);temporary.replace(destination)
 def loop(self):
  while not self.stop.wait(self.interval):
   try:self.copy();event(self.root,'finite1519_join_live_backup_saved',completed_stage_ZIPs_separate=True)
   except BaseException as error:
    self.error=type(error).__name__+': '+str(error);event(self.root,'finite1519_join_backup_error',error=self.error)
 def start(self):self.thread.start()
 def close(self):
  self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped finite-join backup worker');self.copy()


def run_controls(root,completed_cache,source_cache,status):
 root=src.ordinary(root);found=controls.restore_completed(completed_cache,root/'controls',root=root)
 d=src.plan()['fresh_geometry_fixture'];records={r['key']:r for r in status['imports']}
 src.need('count:'+d['job_id']in records,'Genuine complete current COUNT56 must be imported before control execution')
 current=records['count:'+d['job_id']]
 if found:
  fixture=ev.read(found[0]/'CURRENT_GEOMETRY_FIXTURE.json')
  if not ev.same(fixture['validated_native_count'],current['validated']):
   event(root,'finite1519_join_controls_current_fixture_changed',old_complete_cache_preserved=True,
         reason='The current fully validated COUNT56 epoch differs; rerun controls without editing historical receipts')
   found=None
 if found:
  task,checked,export=found;reused=True
 else:
  upstream=semantic._task(root,current)
  task=root/'controls'/('six-current-'+uuid.uuid4().hex[:8])
  checked=controls.execute(source_cache,task,root=root,upstream_count56=upstream)
  export=controls.save_completed(task,completed_cache);reused=False
 status['controls']=dict(task_relative=task.relative_to(root).as_posix(),validated=checked,export=export,reused_completed_stage=reused)
 status['conditional_controls_completed']=True;atomic_json(root/'SESSION_RESULT.json',status)
 event(root,'finite1519_join_controls_complete',native_actions=6,reused_completed_stage=reused,full_notebook57_completed=False)
 return status['controls']


def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
 from .environment import snapshot
 src.need(sys.platform=='linux','Actual original57H control execution requires Linux')
 src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=300,'Finite log-backup interval')
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
 root=src.ordinary(Path(work_root)/'finite1519-join'/stamp);root.mkdir(parents=True,exist_ok=False)
 durable=src.ordinary(Path(durable_root)/'finite1519-join'/stamp)
 cache=src.ordinary(Path(durable_root)/'finite1519-join/completed'/src.PLAN_SHA256[:16])
 status=dict(schema=semantic.SCHEMA,state='incomplete',started_utc=utc(),controls=None,imports=[],
  conditional_controls_completed=False,conditional_finite_chain_verified=False,**{f:False for f in ev.FLAGS})
 atomic_json(root/'ENVIRONMENT.json',snapshot());atomic_json(root/'SESSION_RESULT.json',status)
 backups=Backups(root,durable,backup_interval);backups.start()
 event(root,'finite1519_join_started',native_actions=6,complete_imports=164,probability_dispositions=1000,
  simultaneous_count_interfaces=147,cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,full_notebook57_completed=False)
 try:
  missing=semantic.import_completed_inputs(root,durable_root,status)
  if missing:status.update(state='waiting_for_prerequisite_exports',missing=missing)
  else:
   assets=src.obtain_assets(archives,progress=lambda name,**data:event(root,name,**data))
   source_cache=src.prepare_cache(assets,root/'source-cache',progress=lambda name,**data:event(root,name,**data))
   run_controls(root,cache,source_cache,status)
   summary=semantic.validate_batch(root,status)
   status.update(state=semantic.COMPLETE,conditional_finite_chain_verified=True,finite_summary=summary,finished_utc=utc())
   atomic_json(root/'SESSION_RESULT.json',status);semantic.validate_completed(root)
 except BaseException as error:
  status.update(state='incomplete',conditional_finite_chain_verified=False,error=type(error).__name__+': '+str(error))
  (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8',newline='\n')
  event(root,'finite1519_join_incomplete',error=status['error'],full_notebook57_completed=False)
 finally:
  status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
  try:backups.close()
  except BaseException as error:
   status.update(state='incomplete',conditional_finite_chain_verified=False,backup_error=type(error).__name__+': '+str(error));atomic_json(root/'SESSION_RESULT.json',status)
  if backups.error:
   status.update(state='incomplete',conditional_finite_chain_verified=False,backup_error=backups.error);atomic_json(root/'SESSION_RESULT.json',status)
  try:archive=bundle(root,durable)
  except BaseException as error:
   status.update(state='incomplete',conditional_finite_chain_verified=False,bundle_error=type(error).__name__+': '+str(error));atomic_json(root/'SESSION_RESULT.json',status)
   archive=bundle(root,Path(work_root)/'finite1519-join-local-exports'/stamp)
  exported=dict(path=str(archive),sha256=src.digest(archive));event(root,'finite1519_join_final_bundle',state=status['state'],**exported)
  if status['state']==semantic.COMPLETE and status['conditional_finite_chain_verified']is True:
   try:
    index=Path(durable_root)/'finite1519-join/completed-finite'/src.PLAN_SHA256[:16]/(stamp+'.json')
    atomic_json(index,dict(schema='FINITE1519_COMPLETE_FINITE_EXPORT_INDEX_V1',source_plan_sha256=src.PLAN_SHA256,
     path=str(archive),sha256=exported['sha256'],sidecar_path=str(archive.with_suffix('.zip.sha256')),session_root=stamp,
     session_result_sha256=src.digest(root/'SESSION_RESULT.json'),pure_validator='be_replay.finite1519_join_evidence.validate_completed',
     conditional_finite_chain_verified=True,**{f:False for f in ev.FLAGS}))
   except BaseException as error:event(root,'finite1519_join_discovery_index_incomplete',error=type(error).__name__+': '+str(error),actual_bundle_preserved=True)
 return dict(status=status,bundle=exported,work=str(root))
