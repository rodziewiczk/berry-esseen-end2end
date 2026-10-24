"""57D: two original support15--19 actions, with complete-only cache reuse."""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import os
import shutil
import stat
import sys
import threading
import time
import traceback
import uuid
import zipfile
from . import finite1519_support_sources as src,finite1519_support_evidence as ev,linux_supervisor
from .colab_batch import atomic_json,bundle,event,utc

CACHE_BYTES=512*src.MIB


class Follow:
    def __init__(self,root,task,action):
        self.root,self.task,self.action=Path(root),Path(task),action
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def loop(self):
        position=0;partial=b'';started=time.monotonic();last=-20;draining=False
        while True:
            try:
                with(self.task/'executions'/self.action/'stdout.txt').open('rb')as stream:stream.seek(position);raw=stream.read(src.MIB)
                position+=len(raw);lines=(partial+raw).split(b'\n');partial=lines.pop()
                for line in lines:event(self.root,'finite1519_support_original_stdout',action=self.action,line=line.decode('utf-8',errors='replace')[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:
                event(self.root,'finite1519_support_heartbeat',action=self.action,elapsed_seconds=elapsed,
                      stdout_bytes=position,conditional_support_arithmetic_completed=False,full_notebook57_completed=False);last=elapsed
            if self.stop.wait(.2):
                if draining:break
                draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):
        self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped bounded progress observer')


def execute(task,cache, *,root):
    src.need(sys.platform=='linux','Actual Linux process-tree supervision required')
    task=Path(task).resolve();request=src.prepare(cache,task)
    actions=[]
    for action in src.ACTIONS:
        src.verify_job(task);paths=src.output_paths(action)
        src.need(all(not(task/'capsule'/name).exists()for name in paths),'Exclusive fresh original action outputs')
        event(root,'finite1519_support_original_action_started',action=action,cpu_seconds=ev.CPU_SECONDS,
              wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,full_notebook57_completed=False)
        with Follow(root,task,action):
            observed=linux_supervisor.run(ev.command(request,action,sys.executable),cwd=task/'capsule'/(src.NATIVE if action=='construct'else src.AUDIT),
                output_dir=task/'executions'/action,mode='untrusted_search',cpu_seconds=ev.CPU_SECONDS,
                wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,disk_bytes=512*src.MIB,
                log_bytes=16*src.MIB,heartbeat_seconds=20,checkpoint_paths=[task/'capsule'/p for p in paths])
        actions.append(dict(action=action,observed=observed))
        atomic_json(task/'ACTIONS_PARTIAL.json',dict(actions=actions,conditional_support_arithmetic_completed=False,
                                                   **{f:False for f in ev.FLAGS}))
        context_report=dict(python_executable=sys.executable,python_version=sys.version)
        try:ev.transport(task,request,action,observed,context_report)
        except Exception as error:
            tail='';p=task/'executions'/action/'stderr.txt'
            if p.is_file()and not p.is_symlink()and p.stat().st_size<=16*src.MIB:
                with p.open('rb')as stream:stream.seek(max(0,p.stat().st_size-4096));tail=stream.read(4096).decode('utf-8',errors='replace')
            event(root,'finite1519_support_action_incomplete',action=action,reason=observed.get('reason'),
                  returncode=observed.get('returncode'),stderr_tail=tail,error=str(error),full_notebook57_completed=False)
            raise ValueError('Original support '+action+' did not complete: '+str(error)+'; stderr tail: '+tail)from error
        if action=='construct':
            p=task/'capsule'/src.RUNS;p.mkdir(parents=True,exist_ok=False)
            for name in('stdout','stderr'):shutil.copyfile(task/'executions'/action/(name+'.txt'),p/(name+'.txt'))
            atomic_json(p/'metadata.json',ev.constructor_metadata(task,request,context_report,observed))
        src.verify_job(task)
        event(root,'finite1519_support_original_action_stopped_successfully',action=action,completed_actions=len(actions),
              total_actions=2,conditional_support_arithmetic_completed=False,full_notebook57_completed=False)
    report=dict(schema=ev.OBSERVED,scope=ev.SCOPE,original_task_root=request['original_task_root'],implementation=ev.implementation(),
                python_executable=sys.executable,python_version=sys.version,actions=actions,
                conditional_support_arithmetic_completed=False,**{f:False for f in ev.FLAGS})
    atomic_json(task/'STAGE_OBSERVED.json',report);summary=ev.validate_run(task,report)
    complete=dict(schema=ev.COMPLETED,scope=ev.SCOPE,implementation=ev.implementation(),
        observed_sha256=src.digest(task/'STAGE_OBSERVED.json'),summary=summary,artifacts=ev.inventory(task),
        conditional_support_arithmetic_completed=True,**{f:False for f in ev.FLAGS})
    atomic_json(task/'STAGE_COMPLETED.json',complete);return ev.validate_completed(task)


def cache_members(z):
    rows=z.infolist();src.need(0<len(rows)<=1000,'Bounded complete two-action ZIP inventory');names=set();folded=set();total=0
    for r in rows:
        src.parts(r.filename);mode=r.external_attr>>16
        src.need(not r.is_dir()and not r.flag_bits&1 and not stat.S_ISLNK(mode)and stat.S_IFMT(mode)in(0,stat.S_IFREG)
                 and r.filename not in names and r.filename.casefold()not in folded and 0<=r.file_size<=128*src.MIB,
                 'Unique ordinary nonlinked bounded complete ZIP member')
        names.add(r.filename);folded.add(r.filename.casefold());total+=r.file_size
    required={'SOURCES.json','STAGE_OBSERVED.json','STAGE_COMPLETED.json'}
    required|={'executions/'+a+'/'+n for a in src.ACTIONS for n in('launch.json','supervisor-result.json','stdout.txt','stderr.txt')}
    required|={'capsule/'+p for a in src.ACTIONS for p in src.output_paths(a)}|{'capsule/'+p for p in src.capture_paths()}
    src.need(total<=CACHE_BYTES and required<=names,'Both complete source/launch/capture/native-output ledgers');return rows


def save_completed(task,cache):
    task=Path(task);checked=ev.validate_completed(task);cache=src.ordinary(cache);cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip';p=cache/name;pending=cache/(name+'.pending')
    with zipfile.ZipFile(pending,'x',compression=zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for f in sorted(task.rglob('*')):
            src.ordinary(f)
            if f.is_file():z.write(f,f.relative_to(task).as_posix())
        cache_members(z)
    src.need(pending.stat().st_size<=CACHE_BYTES,'Bounded completed transaction export');pin=src.digest(pending);pending.replace(p)
    p.with_suffix('.zip.sha256').write_bytes((pin+'  '+p.name+'\n').encode('ascii'))
    return dict(path=str(p),sha256=pin,stage_result_sha256=checked['stage_result_sha256'])


def restore_completed(cache,destination, *,root):
    cache=src.ordinary(cache);destination=Path(destination)
    if not cache.exists():return None
    src.need(cache.is_dir(),'Ordinary complete transaction cache')
    for p in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
        try:
            src.ordinary(p);marker=src.ordinary(p.with_suffix('.zip.sha256'))
            src.need(p.is_file()and p.stat().st_size<=CACHE_BYTES and marker.is_file()and marker.stat().st_size<=1024
                     and marker.read_text('ascii')==src.digest(p)+'  '+p.name+'\n','Actual complete transaction ZIP SHA sidecar')
            restored=destination/('support-restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(p)as z:
                rows=cache_members(z);restored.mkdir(parents=True,exist_ok=False)
                for r in rows:
                    target=restored.joinpath(*src.parts(r.filename));target.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(r)as source,target.open('xb')as output:shutil.copyfileobj(source,output,src.MIB)
            checked=ev.validate_completed(restored)
            event(root,'finite1519_support_completed_transaction_revalidated',cache=str(p),sha256=src.digest(p),
                  numerical_replay_skipped=True,full_notebook57_completed=False)
            return restored,checked,dict(path=str(p),sha256=src.digest(p))
        except Exception as error:event(root,'finite1519_support_complete_cache_rejected',cache=str(p),error=type(error).__name__+': '+str(error))
    return None


class Backups:
    def __init__(self,root,durable,interval):
        self.root,self.durable=Path(root),Path(durable);self.interval=interval
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def copy(self):
        for p in self.root.rglob('*'):
            src.ordinary(p)
            if not p.is_file()or p.stat().st_size>16*src.MIB:continue
            rel=p.relative_to(self.root).as_posix()
            if '/capsule/'in rel or p.suffix not in('.json','.jsonl','.txt'):continue
            target=self.durable/'live'/rel;target.parent.mkdir(parents=True,exist_ok=True)
            pending=target.with_name(target.name+'.pending');shutil.copyfile(p,pending);pending.replace(target)
    def loop(self):
        while not self.stop.wait(self.interval):
            try:self.copy();event(self.root,'finite1519_support_live_backup_saved',partial_numerical_resume=False)
            except Exception as error:event(self.root,'finite1519_support_backup_failed',error=str(error))
    def start(self):self.thread.start()
    def close(self):
        self.stop.set();self.thread.join(timeout=30);src.need(not self.thread.is_alive(),'Stopped live backup observer');self.copy()


def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
    from .environment import snapshot
    src.plan();src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=3600,'Bounded live backup interval')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root=Path(work_root).resolve()/'finite1519-support'/stamp;root.mkdir(parents=True,exist_ok=False)
    durable=Path(durable_root).resolve()/'finite1519-support'/stamp
    cache=Path(durable_root).resolve()/'finite1519-support/completed'/src.PLAN_SHA256[:16]
    status=dict(schema='CONDITIONAL_FINITE1519_SUPPORT_SESSION_V1',state='started',started_utc=utc(),source_plan_sha256=src.PLAN_SHA256,
        conditional_support_arithmetic_completed=False,partial_numerical_resume=False,**{f:False for f in ev.FLAGS})
    atomic_json(root/'ENVIRONMENT.json',snapshot());atomic_json(root/'SESSION_RESULT.json',status)
    backups=Backups(root,durable,backup_interval);backups.start()
    try:
        event(root,'finite1519_support_sublane_started',original_actions=list(src.ACTIONS),source_files=26,
              full_ray_rows=10,cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,
              whole_notebook57=False,resource_to_count147_interfaces_verified=False)
        loaded=restore_completed(cache,root/'restored',root=root)
        if loaded:task,checked,export=loaded;status['reused_complete_transaction']=True
        else:
            assets=src.obtain_assets(archives,progress=lambda name,**fields:event(root,name,**fields))
            source_cache=src.prepare_cache(assets,Path(work_root).resolve()/'finite1519-support-source-cache'/src.PLAN_SHA256[:16],
                                           progress=lambda name,**fields:event(root,name,**fields))
            task=root/'arithmetic';checked=execute(task,source_cache,root=root);export=save_completed(task,cache)
            status['reused_complete_transaction']=False
        status.update(state='complete_conditional_support15_19_sublane_basic',task_relative=task.relative_to(root).as_posix(),
                      validated=checked,completed_export=export,conditional_support_arithmetic_completed=True)
    except BaseException as error:
        status.update(state='incomplete_support_sublane_no_acceptance',conditional_support_arithmetic_completed=False,
                      error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8',newline='\n')
        event(root,'finite1519_support_sublane_incomplete',error=status['error'],full_notebook57_completed=False)
    finally:
        status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
        try:backups.close()
        except Exception as error:event(root,'finite1519_support_final_backup_failed',error=str(error))
        archive=bundle(root,durable)
    print('57D SUPPORT SUBLANE RESULT:',status['state'],'\nZIP:',archive,flush=True)
    return dict(status=status,bundle=str(archive.resolve()),work=str(root.resolve()))
