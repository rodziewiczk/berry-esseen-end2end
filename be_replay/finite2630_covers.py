"""59B/C: two full original n26--30 Fourier-cover pipelines, with complete-only cache reuse."""
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
from . import finite2630_covers_sources as src,finite2630_covers_evidence as ev,linux_supervisor
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
                for line in lines:event(self.root,'finite2630_covers_original_stdout',action=self.action,line=line.decode('utf-8',errors='replace')[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:
                event(self.root,'finite2630_covers_heartbeat',action=self.action,elapsed_seconds=elapsed,
                      stdout_bytes=position,conditional_cover_arithmetic_completed=False,full_notebook59_completed=False);last=elapsed
            if self.stop.wait(.2):
                if draining:break
                draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):
        self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped bounded progress observer')


def execute(name,task,cache, *,root):
    src.need(sys.platform=='linux','Actual Linux process-tree supervision required')
    task=Path(task).resolve();request=src.prepare(name,cache,task);profile=src.lane(name);actions=[]
    context=dict(python_executable=sys.executable,python_version=sys.version)
    for pass_name in src.PASSES:
        for step in profile['stages']:
            src.prepare_stage(task,pass_name,step);c=src.capsule(task,pass_name);paths=src.output_paths(step);label=pass_name+'-'+step
            src.need(all(not(c/p).exists()for p in paths),'Exclusive fresh complete native output slots; no historical pilot/control reuse')
            event(root,'finite2630_covers_original_action_started',lane=name,pass_name=pass_name,stage=step,
                  completed_actions=len(actions),total_actions=2*len(profile['stages']),cpu_seconds=ev.CPU_SECONDS,
                  wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,full_notebook59_completed=False)
            with Follow(root,task,label):
                observed=linux_supervisor.run(ev.command(request,pass_name,step,sys.executable),cwd=c,
                    output_dir=task/'executions'/label,mode='untrusted_search',cpu_seconds=ev.CPU_SECONDS,
                    wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,disk_bytes=512*src.MIB,
                    log_bytes=16*src.MIB,heartbeat_seconds=20,checkpoint_paths=[c/p for p in paths])
            actions.append(dict(pass_name=pass_name,stage=step,observed=observed))
            atomic_json(task/'ACTIONS_PARTIAL.json',dict(actions=actions,conditional_cover_arithmetic_completed=False,**{f:False for f in ev.FLAGS}))
            try:ev.validate_stage(task,request,pass_name,step,observed,context)
            except Exception as error:
                tail='';p=task/'executions'/label/'stderr.txt'
                if p.is_file()and not p.is_symlink()and p.stat().st_size<=16*src.MIB:
                    with p.open('rb')as stream:stream.seek(max(0,p.stat().st_size-4096));tail=stream.read(4096).decode('utf-8',errors='replace')
                event(root,'finite2630_covers_action_incomplete',lane=name,pass_name=pass_name,stage=step,reason=observed.get('reason'),
                      returncode=observed.get('returncode'),stderr_tail=tail,error=str(error),full_notebook59_completed=False)
                raise ValueError('Original '+name+' '+label+' did not complete: '+str(error)+'; stderr tail: '+tail)from error
            src.verify(task)
            event(root,'finite2630_covers_original_action_stopped_successfully',lane=name,pass_name=pass_name,stage=step,
                  completed_actions=len(actions),total_actions=2*len(profile['stages']),conditional_cover_arithmetic_completed=False,full_notebook59_completed=False)
    report=dict(schema=ev.OBSERVED,scope=ev.SCOPE,lane=name,original_task_root=request['original_task_root'],implementation=ev.implementation(),
                python_executable=sys.executable,python_version=sys.version,actions=actions,
                conditional_cover_arithmetic_completed=False,**{f:False for f in ev.FLAGS})
    atomic_json(task/'STAGE_OBSERVED.json',report);summary=ev.validate_run(task,report)
    complete=dict(schema=ev.COMPLETED,scope=ev.SCOPE,lane=name,implementation=ev.implementation(),
        observed_sha256=src.digest(task/'STAGE_OBSERVED.json'),summary=summary,artifacts=ev.inventory(task),
        conditional_cover_arithmetic_completed=True,**{f:False for f in ev.FLAGS})
    atomic_json(task/'STAGE_COMPLETED.json',complete);return ev.validate_completed(task)


def cache_members(z,name):
    rows=z.infolist();src.need(0<len(rows)<=5000,'Bounded complete two-pass ZIP inventory');names=set();folded=set();total=0
    for r in rows:
        src.parts(r.filename);mode=r.external_attr>>16
        src.need(not r.is_dir()and not r.flag_bits&1 and not stat.S_ISLNK(mode)and stat.S_IFMT(mode)in(0,stat.S_IFREG)
                 and r.filename not in names and r.filename.casefold()not in folded and 0<=r.file_size<=128*src.MIB,
                 'Unique ordinary nonlinked bounded complete ZIP member')
        names.add(r.filename);folded.add(r.filename.casefold());total+=r.file_size
    profile=src.lane(name);required={'SOURCES.json','STAGE_OBSERVED.json','STAGE_COMPLETED.json'}
    for pass_name in src.PASSES:
        required.add('passes/'+pass_name+'/PORTS.json')
        for step in profile['stages']:
            required|={'executions/'+pass_name+'-'+step+'/'+n for n in('launch.json','supervisor-result.json','stdout.txt','stderr.txt')}
            required|={'passes/'+pass_name+'/capsule/'+p for p in src.output_paths(step)}
    src.need(total<=CACHE_BYTES and required<=names,'All four complete source/launch/capture/native-output ledgers');return rows


def save_completed(task,cache):
    task=Path(task);checked=ev.validate_completed(task);cache=src.ordinary(cache);cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip';p=cache/name;pending=cache/(name+'.pending')
    with zipfile.ZipFile(pending,'x',compression=zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for f in sorted(task.rglob('*')):
            src.ordinary(f)
            if f.is_file():z.write(f,f.relative_to(task).as_posix())
        cache_members(z,checked['lane'])
    src.need(pending.stat().st_size<=CACHE_BYTES,'Bounded completed transaction export');pin=src.digest(pending);pending.replace(p)
    p.with_suffix('.zip.sha256').write_bytes((pin+'  '+p.name+'\n').encode('ascii'))
    return dict(path=str(p),sha256=pin,stage_result_sha256=checked['stage_result_sha256'])


def restore_completed(name,cache,destination, *,root):
    cache=src.ordinary(cache);destination=Path(destination)
    if not cache.exists():return None
    src.need(cache.is_dir(),'Ordinary complete transaction cache')
    for p in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
        try:
            src.ordinary(p);marker=src.ordinary(p.with_suffix('.zip.sha256'))
            src.need(p.is_file()and p.stat().st_size<=CACHE_BYTES and marker.is_file()and marker.stat().st_size<=1024
                     and marker.read_text('ascii')==src.digest(p)+'  '+p.name+'\n','Actual complete transaction ZIP SHA sidecar')
            restored=destination/('covers-restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(p)as z:
                rows=cache_members(z,name);restored.mkdir(parents=True,exist_ok=False)
                for r in rows:
                    target=restored.joinpath(*src.parts(r.filename));target.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(r)as source,target.open('xb')as output:shutil.copyfileobj(source,output,src.MIB)
            checked=ev.validate_completed(restored);src.need(checked['lane']==name,'Exact lane-specific completed cache')
            event(root,'finite2630_covers_completed_transaction_revalidated',cache=str(p),sha256=src.digest(p),
                  numerical_replay_skipped=True,full_notebook59_completed=False)
            return restored,checked,dict(path=str(p),sha256=src.digest(p))
        except Exception as error:event(root,'finite2630_covers_complete_cache_rejected',cache=str(p),error=type(error).__name__+': '+str(error))
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
            try:self.copy();event(self.root,'finite2630_covers_live_backup_saved',partial_numerical_resume=False)
            except Exception as error:event(self.root,'finite2630_covers_backup_failed',error=str(error))
    def start(self):self.thread.start()
    def close(self):
        self.stop.set();self.thread.join(timeout=30);src.need(not self.thread.is_alive(),'Stopped live backup observer');self.copy()


def run_colab(name, *,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
    from .environment import snapshot
    profile=src.lane(name);src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=3600,'Bounded live backup interval')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    folder='finite2630-covers-'+name;root=Path(work_root).resolve()/folder/stamp;root.mkdir(parents=True,exist_ok=False)
    durable=Path(durable_root).resolve()/folder/stamp;cache=Path(durable_root).resolve()/folder/'completed'/src.PLAN_SHA256[:16]
    status=dict(schema='CONDITIONAL_FINITE2630_COVERS_SESSION_V1',lane=name,state='started',started_utc=utc(),source_plan_sha256=src.PLAN_SHA256,
        conditional_cover_arithmetic_completed=False,partial_numerical_resume=False,**{f:False for f in ev.FLAGS})
    atomic_json(root/'ENVIRONMENT.json',snapshot());atomic_json(root/'SESSION_RESULT.json',status)
    backups=Backups(root,durable,backup_interval);backups.start()
    try:
        event(root,'finite2630_covers_sublane_started',lane=name,rows_per_pass=profile['rows'],closed_strips=profile['closed_strips'],
              original_actions_per_pass=profile['stages'],genuine_passes=2,total_native_actions=2*len(profile['stages']),
              cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,full_notebook59_completed=False)
        loaded=restore_completed(name,cache,root/'restored',root=root)
        if loaded:task,checked,export=loaded;status['reused_complete_transaction']=True
        else:
            archive=src.obtain_assets(archives,progress=lambda event_name,**fields:event(root,event_name,**fields))
            source_cache=src.prepare_cache(archive,Path(work_root).resolve()/'finite2630-covers-source-cache'/src.PLAN_SHA256[:16],
                                           progress=lambda event_name,**fields:event(root,event_name,**fields))
            task=root/'arithmetic';checked=execute(name,task,source_cache,root=root);export=save_completed(task,cache)
            status['reused_complete_transaction']=False
        status.update(state='complete_conditional_original_fourier_covers_basic',task_relative=task.relative_to(root).as_posix(),
                      validated=checked,completed_export=export,conditional_cover_arithmetic_completed=True)
    except BaseException as error:
        status.update(state='incomplete_fourier_cover_sublane_no_acceptance',conditional_cover_arithmetic_completed=False,error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8',newline='\n')
        event(root,'finite2630_covers_sublane_incomplete',lane=name,error=status['error'],full_notebook59_completed=False)
    finally:
        status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
        try:backups.close()
        except Exception as error:event(root,'finite2630_covers_final_backup_failed',error=str(error))
        archive=bundle(root,durable)
    print('59B/C COVER SUBLANE RESULT:',name,status['state'],'\nZIP:',archive,flush=True)
    return dict(status=status,bundle=str(archive.resolve()),work=str(root.resolve()))
