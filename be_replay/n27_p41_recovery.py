"""Original alpha4 construction then full acceptance in a new conditional epoch."""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import shutil
import stat
import sys
import threading
import traceback
import uuid
import zipfile
from . import linux_supervisor,n27_p41_recovery_sources as src,n27_p41_recovery_evidence as ev
from .colab_batch import atomic_json,bundle,event,utc


def execute(task,archive, *,log_root=None):
    src.need(sys.platform=='linux','Actual Linux/POSIX execution required')
    task=Path(task).resolve();request=src.prepare(archive,task);root=task.parent if log_root is None else Path(log_root)
    for action in('construct','accept'):
        src.verify_task(task);_,_,outputs=ev.ACTIONS[action]
        src.need(all(not(task/'capsule'/name).exists()for name in outputs),'Fresh exclusive native action outputs')
        event(root,'n27_p41_original_action_started',action=action,cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,
              memory_bytes=ev.MEMORY_BYTES,constructor_internal_node_limit=10000,constructor_internal_seconds=600,
              native_arithmetic_accepted=False,lane53_ready=False)
        observed=linux_supervisor.run(ev.command(request,action,sys.executable),cwd=task/'capsule',
            output_dir=task/'execution'/action,mode='untrusted_search',cpu_seconds=ev.CPU_SECONDS,
            wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,disk_bytes=256*src.MIB,log_bytes=16*src.MIB,
            heartbeat_seconds=20,checkpoint_paths=[task/'capsule'/name for name in outputs])
        record=dict(schema='OBSERVED_NEW_N27_P41_ACTION_V1',scope=ev.SCOPE,action=action,
                    implementation=ev.implementation(),python_executable=sys.executable,python_version=sys.version,
                    observed=observed,**{f:False for f in ev.FLAGS})
        atomic_json(task/(action.upper()+'_OBSERVED.json'),record)
        try:checked=ev.validate_constructor(task)if action=='construct'else ev.validate_pair(task)
        except Exception as error:
            stderr=task/'execution'/action/'stderr.txt';tail=''
            if stderr.is_file()and not stderr.is_symlink()and stderr.stat().st_size<=16*src.MIB:
                with stderr.open('rb')as stream:stream.seek(max(0,stderr.stat().st_size-4096));tail=stream.read(4096).decode('utf-8',errors='replace')
            event(root,'n27_p41_original_action_incomplete',action=action,supervisor_status=observed.get('status'),
                  supervisor_reason=observed.get('reason'),returncode=observed.get('returncode'),stderr_tail=tail,
                  validation_error=type(error).__name__+': '+str(error),conditional_arithmetic_completed=False,lane53_ready=False)
            raise ValueError('Original n27/p41 '+action+' did not validate: '+str(error)+'; stderr tail: '+tail)from error
        event(root,'n27_p41_original_action_completed',action=action,summary=checked,
              native_arithmetic_accepted=False,lane53_ready=False)
    summary=ev.validate_pair(task)
    complete=dict(schema='COMPLETED_NEW_N27_P41_PAIR_V1',implementation=ev.implementation(),summary=summary,
                  artifacts=ev.inventory(task),conditional_arithmetic_completed=True,**{f:False for f in ev.FLAGS})
    atomic_json(task/'COMPLETED.json',complete)
    return ev.validate_completed(task)


CACHE_BYTES=512*src.MIB


def cache_members(z):
    rows=z.infolist();src.need(0<len(rows)<=2000,'Bounded complete-pair ZIP member count')
    names=set();folded=set();total=0
    for r in rows:
        src.parts(r.filename);mode=r.external_attr>>16
        src.need(not r.is_dir()and not r.flag_bits&1 and not stat.S_ISLNK(mode)
                 and stat.S_IFMT(mode)in(0,stat.S_IFREG)and r.filename not in names and r.filename.casefold()not in folded
                 and 0<=r.file_size<=128*src.MIB,'Canonical unique ordinary bounded complete-pair ZIP members')
        names.add(r.filename);folded.add(r.filename.casefold());total+=r.file_size
    required={'SOURCES.json','CONSTRUCT_OBSERVED.json','ACCEPT_OBSERVED.json','COMPLETED.json',
              'capsule/CONSTRUCTION_RUN.json','capsule/COUNT41_FOREST.json','capsule/COUNT41_ACCEPTED.json'}
    src.need(total<=CACHE_BYTES and required<=names,'Complete two-action source/candidate/acceptance evidence')
    return rows


def save_completed(task,cache):
    task=Path(task);checked=ev.validate_completed(task);cache=src.ordinary(cache);cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip'
    output=cache/name;pending=cache/(name+'.pending')
    with zipfile.ZipFile(pending,'x',compression=zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for p in sorted(task.rglob('*')):
            src.ordinary(p)
            if p.is_file():z.write(p,p.relative_to(task).as_posix())
        cache_members(z)
    src.need(pending.stat().st_size<=CACHE_BYTES,'Bounded complete-pair transport');pin=src.digest(pending);pending.replace(output)
    output.with_suffix('.zip.sha256').write_bytes((pin+'  '+output.name+'\n').encode('ascii'))
    return dict(path=str(output),sha256=pin,completed_sha256=checked['completed_sha256'])


def restore_completed(cache,destination, *,log_root=None):
    cache=src.ordinary(cache);destination=Path(destination)
    if not cache.exists():return None
    src.need(cache.is_dir(),'Ordinary complete-pair cache')
    for p in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
        try:
            src.ordinary(p);sidecar=src.ordinary(p.with_suffix('.zip.sha256'))
            src.need(p.is_file()and p.stat().st_size<=CACHE_BYTES and sidecar.is_file()and sidecar.stat().st_size<=1024
                     and sidecar.read_text('ascii')==src.digest(p)+'  '+p.name+'\n','Actual complete-pair ZIP sidecar')
            restored=destination/('pair-restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(p)as z:
                rows=cache_members(z);restored.mkdir(parents=True,exist_ok=False)
                for info in rows:
                    target=restored.joinpath(*src.parts(info.filename));target.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(info)as source,target.open('xb')as out:shutil.copyfileobj(source,out,src.MIB)
            checked=ev.validate_completed(restored)
            return restored,checked,dict(path=str(p),sha256=src.digest(p))
        except Exception as error:
            if log_root:event(log_root,'n27_p41_complete_cache_rejected',error=type(error).__name__+': '+str(error))
    return None


class LogBackups:
    """Advisory logs only; a complete pair has a separately validated ZIP."""
    def __init__(self,root,durable,interval):
        self.root,self.durable=Path(root),Path(durable);self.interval=interval
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def copy(self):
        for p in self.root.rglob('*'):
            src.ordinary(p)
            if not p.is_file():continue
            rel=p.relative_to(self.root).as_posix()
            if '/capsule/'in rel or p.stat().st_size>16*src.MIB or p.suffix not in('.json','.jsonl','.txt'):continue
            target=self.durable/'live'/rel;target.parent.mkdir(parents=True,exist_ok=True)
            pending=target.with_name(target.name+'.pending');shutil.copyfile(p,pending);pending.replace(target)
    def loop(self):
        while not self.stop.wait(self.interval):
            try:self.copy();event(self.root,'n27_p41_live_logs_saved',partial_numerical_resume=False)
            except Exception as error:event(self.root,'n27_p41_live_backup_failed',error=str(error))
    def start(self):self.thread.start()
    def close(self):
        self.stop.set();self.thread.join(timeout=30);src.need(not self.thread.is_alive(),'Stopped log backup observer');self.copy()


def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
    from .environment import snapshot
    src.plan();src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=3600,'Bounded live backup interval')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root=Path(work_root).resolve()/'n27-p41-recovery'/stamp;root.mkdir(parents=True,exist_ok=False)
    durable=Path(durable_root).resolve()/'n27-p41-recovery'/stamp
    cache=Path(durable_root).resolve()/'n27-p41-recovery'/'completed'/src.PLAN_SHA256[:16]
    status=dict(schema='NEW_N27_P41_RECOVERY_SESSION_V1',state='started',started_utc=utc(),
                source_plan_sha256=src.PLAN_SHA256,new_candidate_epoch=True,conditional_arithmetic_completed=False,
                partial_numerical_resume=False,**{f:False for f in ev.FLAGS})
    atomic_json(root/'SESSION_RESULT.json',status);atomic_json(root/'ENVIRONMENT.json',snapshot())
    backups=LogBackups(root,durable,backup_interval);backups.start()
    try:
        event(root,'n27_p41_new_candidate_epoch_started',scope=ev.SCOPE,original_constructor_internal_seconds=600,
              original_global_node_limit=10000,original_depth_limit=128,native_arithmetic_accepted=False,lane53_ready=False)
        reused=restore_completed(cache,root/'restored',log_root=root)
        if reused:task,checked,export=reused;status['reused_completed_pair']=True
        else:
            archive=src.obtain_archive(archives,progress=lambda name,**fields:event(root,name,**fields))
            task=root/'arithmetic';checked=execute(task,archive,log_root=root);export=save_completed(task,cache)
            status['reused_completed_pair']=False
        status.update(state='new_candidate_full_conditional_count_computed_basic',conditional_arithmetic_completed=True,
                      validated=checked,completed_export=export,task_relative=task.relative_to(root).as_posix())
    except BaseException as error:
        status.update(state='incomplete_new_candidate_no_acceptance',error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8')
        event(root,'n27_p41_incomplete',error=status['error'],native_arithmetic_accepted=False,lane53_ready=False)
    finally:
        status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
        try:backups.close()
        except Exception as error:event(root,'n27_p41_final_backup_failed',error=str(error))
        archive=bundle(root,durable)
    print('N27/P41 NEW CANDIDATE RESULT:',status['state'],'\nZIP:',archive,flush=True)
    return dict(status=status,bundle=str(archive.resolve()),work=str(root.resolve()))
