"""Eleven recovered original B5 forests,23hours per native action.

Unlike the earlier subsection wrapper, this batch has no shared23-hour
deadline. Original source designs/readers/cache keys are preserved verbatim.
It never visits01--07 and does not claim full66 or any mixed exclusion.
"""
from datetime import datetime,timezone
from pathlib import Path
import traceback,uuid
from . import n25_recovered_counts as run,n25_recovery_sources as src
from . import n25_recovered_counts_evidence as ev,delivery_transport as io
from .retained_n25_extra import LogBackups
from .colab_batch import atomic_json,event,utc

def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',backup_interval=60):
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
 root=Path(work_root)/'n25-recovered-original'/stamp;root.mkdir(parents=True,exist_ok=False)
 durable=Path(durable_root)/'n25-recovered-original/runs'/stamp
 status=dict(schema='N25_ALL_ELEVEN_RECOVERED_B5_BATCH_V1',state='INCOMPLETE',stages=[],per_action_cpu_seconds=82800,
  per_action_wall_seconds=82800,batch_wall_deadline=None,full66_complete=False,mixed_exclusion_verified=False,
  parent_acquisitions_verified=False,all_index_conclusion_verified=False)
 monitor=LogBackups(root,durable,backup_interval);monitor.start()
 try:
  with src.RecoveryArchive()as archive:
   for target in src.targets():
    task=root/'tasks'/target;src._prepare(archive,target,task)
    cache=Path(durable_root)/'n25-recovered-original'/src.PLAN_SHA256/target/'completed'
    hit=run.restore_stage(task,target,cache,log_root=root)
    if hit:epoch,checked=hit;reused=True
    else:
     epoch,checked=run.accept(task,target,cpu_seconds=82800,wall_seconds=82800,on_epoch=monitor.set_active)
     run.save_stage(task,target,epoch,cache);reused=False
    monitor.set_active(None);ev.validate_stage(task,target,epoch)
    status['stages'].append(dict(target=target,epoch=epoch.relative_to(root).as_posix(),validated=checked,reused=reused))
    atomic_json(root/'SESSION_RESULT.json',status);monitor.save()
    event(root,'recovered_B5_batch_progress',completed=len(status['stages']),total=11,target=target,reused=reused)
   status.update(state='COMPLETE_ELEVEN_CONDITIONAL_ORIGINAL_B5_ACCEPTANCES',conditional_arithmetic_completed=True)
 except BaseException as error:
  status.update(state='INCOMPLETE',error=type(error).__name__+': '+str(error));(root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8')
 finally:
  try:monitor.close()
  except Exception as error:status.update(state='INCOMPLETE',synchronization_error=str(error))
  status['finished_utc']=utc();path=io.final_bundle(root,durable,Path(work_root)/'n25-recovered-local'/stamp,status)
 return dict(status=status,bundle=path,work=str(root))
