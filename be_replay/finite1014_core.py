"""56G/H: five complete four-action original INITIAL/resource cases per band."""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import platform
import shutil
import stat
import sys
import threading
import time
import traceback
import uuid
import zipfile
from . import finite1014_core_sources as src,finite1014_core_evidence as ev,linux_supervisor
from .colab_batch import atomic_json,bundle,event,utc

CACHE_BYTES=512*src.MIB


class Follow:
    def __init__(self,root,task,row,action):
        self.root,self.task,self.row,self.action=Path(root),Path(task),row,action
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def loop(self):
        position=0;partial=b'';started=time.monotonic();last=-20;draining=False
        while True:
            try:
                with(self.task/'executions'/self.action/'stdout.txt').open('rb')as stream:stream.seek(position);raw=stream.read(src.MIB)
                position+=len(raw);lines=(partial+raw).split(b'\n');partial=lines.pop()
                for line in lines:event(self.root,'finite1014_core_original_stdout',case_id=self.row['case_id'],action=self.action,
                                        line=line.decode('utf-8',errors='replace')[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:
                event(self.root,'finite1014_core_heartbeat',case_id=self.row['case_id'],action=self.action,
                      elapsed_seconds=elapsed,stdout_bytes=position,conditional_core_arithmetic_completed=False,
                      full_notebook56_completed=False);last=elapsed
            if self.stop.wait(.2):
                if draining:break
                draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):
        self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped bounded progress reader')


def current_capture(task,row,action,request,observed,inputs,outputs,started,finished):
    directory=Path(task)/'capsule'/src.capture_relative(row,action)
    src.need(not directory.exists(),'Fresh current-context capture, never overwrite a historical input')
    directory.mkdir(parents=True)
    for stream in('stdout','stderr'):shutil.copyfile(Path(task)/'executions'/action/(stream+'.txt'),directory/(stream+'.txt'))
    meta=dict(schema='CURRENT_FINITE1014_CORE_GENUINE_ACTION_CAPTURE_V1',action=action,
        capture_origin='CURRENT_STOPPED_LINUX_SUPERVISOR_EXECUTION',historical_capture_impersonated=False,
        command=ev.command(row,action,sys.executable),cwd=ev.original(request,'capsule/'+src.cwd_relative(row,action)),
        input_sha256=src.relative_inputs(row,action,inputs),outputs_sha256=outputs,returncode=observed['returncode'],
        elapsed_seconds=observed['elapsed_seconds'],started_utc=started,finished_utc=finished,
        python=sys.version,platform=platform.platform(),stdout_sha256=src.digest(directory/'stdout.txt'),
        stderr_sha256=src.digest(directory/'stderr.txt'))
    (directory/'metadata.json').write_bytes(src.dump(meta))
    ledger=src.read(Path(task)/src.EPOCH,16*src.MIB)
    ledger['own_action_captures'][action]=dict(relative=src.capture_relative(row,action),metadata_sha256=src.digest(directory/'metadata.json'),
        stdout_sha256=src.digest(directory/'stdout.txt'),stderr_sha256=src.digest(directory/'stderr.txt'))
    (Path(task)/src.EPOCH).write_bytes(src.dump(ledger))


def execute(case_id,cache,task,*,root):
    src.need(sys.platform=='linux','Actual Linux process-tree supervision required')
    task=Path(task).resolve();request=src.prepare(case_id,cache,task);row=src.case(case_id);actions=[]
    for action in src.ACTIONS:
        src.verify(task)
        if action in('initial_construct','resource_construct'):src.derive_prepared(task,row,action.split('_')[0])
        src.need(all(not(task/'capsule'/name).exists()for name in src.outputs(row,action)),'Exclusive fresh original outputs')
        inputs=src.input_map(task,row,action);started=utc()
        event(root,'finite1014_core_original_started',case_id=case_id,action=action,complete_actions=len(actions),total_actions=4,
              cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,
              full_notebook56_completed=False,parent_acquisitions_verified=False)
        with Follow(root,task,row,action):
            observed=linux_supervisor.run(ev.command(row,action,sys.executable),cwd=task/'capsule'/src.cwd_relative(row,action),
                output_dir=task/'executions'/action,mode='untrusted_search',cpu_seconds=ev.CPU_SECONDS,
                wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,disk_bytes=ev.DISK_BYTES,log_bytes=ev.LOG_BYTES,
                heartbeat_seconds=20,checkpoint_paths=[task/'capsule'/name for name in src.checkpoints(row,action)])
        finished=utc()
        partial=dict(case_id=case_id,action=action,observed=observed,complete_actions=len(actions),
                     conditional_core_arithmetic_completed=False,**{f:False for f in ev.FLAGS})
        atomic_json(task/'CURRENT_ACTION_OBSERVED.json',partial)
        try:
            ev.transport(task,row,action,observed,request,sys.executable)
            after=src.input_map(task,row,action);src.need(ev.same(after,inputs),'All original action inputs unchanged after stop')
            outputs={name:src.digest(task/'capsule'/name)for name in src.outputs(row,action)}
            ev.numerical_reference(task,row,action)
        except Exception as error:
            tail='';p=task/'executions'/action/'stderr.txt'
            if p.is_file()and not p.is_symlink()and p.stat().st_size<=ev.LOG_BYTES:
                with p.open('rb')as stream:stream.seek(max(0,p.stat().st_size-4096));tail=stream.read(4096).decode('utf-8',errors='replace')
            event(root,'finite1014_core_action_incomplete',case_id=case_id,action=action,reason=observed.get('reason'),
                  returncode=observed.get('returncode'),stderr_tail=tail,error=str(error),full_notebook56_completed=False)
            raise ValueError('Original '+case_id+' '+action+' incomplete: '+str(error)+'; stderr tail: '+tail)from error
        current_capture(task,row,action,request,observed,inputs,outputs,started,finished)
        actions.append(dict(action=action,observed=observed,inputs_before=inputs,inputs_after=after,outputs=outputs))
        atomic_json(task/'ACTIONS_PARTIAL.json',dict(actions=actions,conditional_core_arithmetic_completed=False,
                                                  **{f:False for f in ev.FLAGS}))
        src.verify(task)
        event(root,'finite1014_core_original_stopped_successfully',case_id=case_id,action=action,complete_actions=len(actions),
              total_actions=4,conditional_core_arithmetic_completed=False,full_notebook56_completed=False)
    report=dict(schema=ev.OBSERVED,scope=ev.SCOPE,case_id=case_id,original_task_root=request['original_task_root'],
                implementation=ev.implementation(),python_executable=sys.executable,python_version=sys.version,
                actions=actions,conditional_core_arithmetic_completed=False,**{f:False for f in ev.FLAGS})
    atomic_json(task/'CASE_OBSERVED.json',report);summary=ev.validate_run(task,report)
    done=dict(schema=ev.COMPLETED,scope=ev.SCOPE,case_id=case_id,implementation=ev.implementation(),
        observed_sha256=src.digest(task/'CASE_OBSERVED.json'),summary=summary,artifacts=ev.inventory(task),
        conditional_core_arithmetic_completed=True,**{f:False for f in ev.FLAGS})
    atomic_json(task/'CASE_COMPLETED.json',done);return ev.validate_completed(task)


def cache_members(z):
    rows=z.infolist();src.need(0<len(rows)<=6000,'Bounded complete case inventory');names=set();folded=set();total=0
    for row in rows:
        src.parts(row.filename);mode=row.external_attr>>16
        src.need(not row.is_dir()and not row.flag_bits&1 and not stat.S_ISLNK(mode)and stat.S_IFMT(mode)in(0,stat.S_IFREG)
                 and row.filename not in names and row.filename.casefold()not in folded and 0<=row.file_size<=128*src.MIB,
                 'Unique bounded ordinary complete-case ZIP entry')
        names.add(row.filename);folded.add(row.filename.casefold());total+=row.file_size
    required={'SOURCES.json',src.EPOCH,'CASE_OBSERVED.json','CASE_COMPLETED.json','provenance/ORIGINAL3072.json'}
    required|={'executions/'+a+'/'+n for a in src.ACTIONS for n in('launch.json','supervisor-result.json','stdout.txt','stderr.txt')}
    src.need(total<=CACHE_BYTES and required<=names,'All four genuine source/capture/current-case ledgers');return rows


def save_completed(task,cache):
    task=Path(task);checked=ev.validate_completed(task);cache=src.ordinary(cache);cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip'
    p=cache/name;pending=cache/(name+'.pending')
    with zipfile.ZipFile(pending,'x',compression=zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for file in sorted(task.rglob('*')):
            src.ordinary(file)
            if file.is_file():z.write(file,file.relative_to(task).as_posix())
        cache_members(z)
    src.need(pending.stat().st_size<=CACHE_BYTES,'Bounded complete case transport');pin=src.digest(pending);pending.replace(p)
    p.with_suffix('.zip.sha256').write_bytes((pin+'  '+p.name+'\n').encode('ascii'))
    return dict(path=str(p),sha256=pin,case_result_sha256=checked['case_result_sha256'])


def restore_completed(case_id,cache,destination,*,root):
    cache=src.ordinary(cache);destination=src.ordinary(destination)
    if not cache.exists():return None
    for p in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
        try:
            src.ordinary(p);marker=src.ordinary(p.with_suffix('.zip.sha256'))
            src.need(p.is_file()and p.stat().st_size<=CACHE_BYTES and marker.is_file()and marker.stat().st_size<=1024
                     and marker.read_text(encoding='ascii')==src.digest(p)+'  '+p.name+'\n','Actual complete-case archive SHA sidecar')
            restored=destination/(case_id+'-restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(p)as z:
                rows=cache_members(z);restored.mkdir(parents=True,exist_ok=False)
                for row in rows:
                    target=restored.joinpath(*src.parts(row.filename));target.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(row)as source,target.open('xb')as dest:shutil.copyfileobj(source,dest,src.MIB)
            checked=ev.validate_completed(restored);src.need(checked['summary']['case_id']==case_id,'No different case cache substitution')
            event(root,'finite1014_core_completed_case_revalidated',case_id=case_id,cache=str(p),sha256=src.digest(p),
                  skipped_original_actions=4,full_notebook56_completed=False)
            return restored,checked,dict(path=str(p),sha256=src.digest(p))
        except Exception as error:event(root,'finite1014_core_complete_cache_rejected',case_id=case_id,cache=str(p),error=str(error))
    return None


class Backups:
    def __init__(self,root,durable,interval):
        self.root,self.durable,self.interval=Path(root),Path(durable),interval
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def copy(self):
        for p in self.root.rglob('*'):
            src.ordinary(p)
            if not p.is_file()or p.stat().st_size>16*src.MIB:continue
            rel=p.relative_to(self.root).as_posix()
            if '/capsule/'in rel or '/provenance/'in rel or p.suffix not in('.json','.jsonl','.txt'):continue
            target=self.durable/'live'/rel;target.parent.mkdir(parents=True,exist_ok=True)
            pending=target.with_name(target.name+'.pending');shutil.copyfile(p,pending);pending.replace(target)
    def loop(self):
        while not self.stop.wait(self.interval):
            try:self.copy();event(self.root,'finite1014_core_live_backup_saved',partial_case_resume=False)
            except Exception as error:event(self.root,'finite1014_core_backup_failed',error=str(error))
    def start(self):self.thread.start()
    def close(self):
        self.stop.set();self.thread.join(timeout=30);src.need(not self.thread.is_alive(),'Stopped live backup observer');self.copy()


def run_colab(band,*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
    from .environment import snapshot
    rows=src.cases(band);src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=3600,'Bounded backup interval')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root=Path(work_root).resolve()/('finite1014-core-'+band.lower())/stamp;root.mkdir(parents=True,exist_ok=False)
    durable=Path(durable_root).resolve()/('finite1014-core-'+band.lower())/stamp
    status=dict(schema='FINITE1014_CORE_BAND_SESSION_V1',scope=ev.SCOPE,state='started',band=band,started_utc=utc(),
                source_plan_sha256=src.PLAN_SHA256,completed_cases=[],expected_cases=5,expected_original_actions=20,
                conditional_core_arithmetic_completed=False,partial_case_resume=False,**{f:False for f in ev.FLAGS})
    atomic_json(root/'ENVIRONMENT.json',snapshot());atomic_json(root/'SESSION_RESULT.json',status)
    backups=Backups(root,durable,backup_interval);backups.start();source_cache=None
    try:
        for row in rows:
            cache=Path(durable_root).resolve()/'finite1014-core/completed'/src.PLAN_SHA256[:16]/row['case_id']
            loaded=restore_completed(row['case_id'],cache,root/'restored',root=root)
            if loaded:task,checked,export=loaded;reused=True
            else:
                if source_cache is None:
                    assets=src.obtain_assets(archives,progress=lambda name,**fields:event(root,name,**fields))
                    source_cache=src.prepare_cache(assets,Path(work_root).resolve()/'finite1014-core-source-cache'/src.PLAN_SHA256[:16],
                                                  progress=lambda name,**fields:event(root,name,**fields))
                task=root/row['case_id'];checked=execute(row['case_id'],source_cache,task,root=root)
                export=save_completed(task,cache);reused=False
            status['completed_cases'].append(dict(case_id=row['case_id'],task_relative=task.relative_to(root).as_posix(),
                validated=checked,completed_export=export,reused_complete_case=reused))
            atomic_json(root/'SESSION_RESULT.json',status)
            event(root,'finite1014_core_case_saved',case_id=row['case_id'],completed_cases=len(status['completed_cases']),
                  expected_cases=5,original_actions_per_case=4,full_notebook56_completed=False)
        src.need([r['case_id']for r in status['completed_cases']]==[r['case_id']for r in rows],'All five full original cases')
        status.update(state='complete_conditional_initial_resource10_14_'+band.lower()+'_basic',conditional_core_arithmetic_completed=True)
    except BaseException as error:
        status.update(state='incomplete_initial_resource_core_no_full_acceptance',conditional_core_arithmetic_completed=False,error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8',newline='\n')
        event(root,'finite1014_core_band_incomplete',band=band,error=status['error'],full_notebook56_completed=False)
    finally:
        status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
        try:backups.close()
        except Exception as error:event(root,'finite1014_core_final_backup_failed',error=str(error))
        archive=bundle(root,durable)
    print('56 CORE',band,'RESULT:',status['state'],'\nZIP:',archive,flush=True)
    return dict(status=status,bundle=str(archive.resolve()),work=str(root.resolve()))
