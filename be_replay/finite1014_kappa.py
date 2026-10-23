"""56K: one unchanged complete original scalar-certificate execution on Colab."""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import shutil
import stat
import sys
import threading
import time
import traceback
import uuid
import zipfile
from . import finite1014_kappa_sources as src,finite1014_kappa_evidence as ev,linux_supervisor
from .colab_batch import Backups,atomic_json,bundle,event,utc

CACHE_BYTES=64*src.MIB


class Follow:
    def __init__(self,root,task):
        self.root,self.task=Path(root),Path(task);self.stop=threading.Event()
        self.thread=threading.Thread(target=self.loop,daemon=True)
    def loop(self):
        position=0;partial=b'';started=time.monotonic();last=-20;draining=False
        while True:
            try:
                with(self.task/'execution/stdout.txt').open('rb')as stream:stream.seek(position);raw=stream.read(src.MIB)
                position+=len(raw);lines=(partial+raw).split(b'\n');partial=lines.pop()
                for line in lines:event(self.root,'finite1014_kappa_original_stdout',line=line.decode('utf-8',errors='replace')[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:
                event(self.root,'finite1014_kappa_heartbeat',elapsed_seconds=elapsed,stdout_bytes=position,
                      scalar_certificate_arithmetic_completed=False,full_notebook56_completed=False);last=elapsed
            if self.stop.wait(.2):
                if draining:break
                draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):
        self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped progress observer')


def execute(task,*,root):
    src.need(sys.platform=='linux','Actual Linux process-tree supervision required')
    task=Path(task).resolve();request=src.prepare(task)
    src.need(all(not(task/'capsule'/n).exists()for n in src.OUTPUTS),'Exclusive fresh original scalar outputs')
    event(root,'finite1014_kappa_original_started',source_files=3,cells=81,bernstein_coefficients=1134,
          negative_controls=21,identity_checks=324,cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,
          memory_bytes=ev.MEMORY_BYTES,full_notebook56_completed=False)
    with Follow(root,task):
        observed=linux_supervisor.run(ev.command(request,sys.executable),cwd=task/'capsule',output_dir=task/'execution',
            mode='untrusted_search',cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,
            disk_bytes=ev.DISK_BYTES,log_bytes=ev.LOG_BYTES,heartbeat_seconds=20,
            checkpoint_paths=[task/'capsule'/n for n in src.OUTPUTS])
    report=dict(schema=ev.OBSERVED,scope=ev.SCOPE,original_task_root=request['original_task_root'],implementation=ev.implementation(),
                python_executable=sys.executable,python_version=sys.version,observed=observed,
                scalar_certificate_arithmetic_completed=False,**{k:False for k in ev.FLAGS})
    atomic_json(task/'STAGE_OBSERVED.json',report)
    try:summary=ev.validate_run(task,report)
    except Exception as error:
        tail='';p=task/'execution/stderr.txt'
        if p.is_file()and not p.is_symlink()and p.stat().st_size<=ev.LOG_BYTES:
            with p.open('rb')as stream:stream.seek(max(0,p.stat().st_size-4096));tail=stream.read(4096).decode('utf-8',errors='replace')
        event(root,'finite1014_kappa_incomplete',reason=observed.get('reason'),returncode=observed.get('returncode'),
              stderr_tail=tail,error=str(error),scalar_certificate_arithmetic_completed=False)
        raise ValueError('Original scalar controls did not complete: '+str(error)+'; stderr tail: '+tail)from error
    complete=dict(schema=ev.COMPLETED,scope=ev.SCOPE,implementation=ev.implementation(),
        observed_sha256=src.digest(task/'STAGE_OBSERVED.json'),summary=summary,artifacts=ev.inventory(task),
        scalar_certificate_arithmetic_completed=True,**{k:False for k in ev.FLAGS})
    atomic_json(task/'STAGE_COMPLETED.json',complete);checked=ev.validate_completed(task)
    event(root,'finite1014_kappa_original_stopped_successfully',scalar_certificate_arithmetic_completed=True,
          negative_controls=21,identity_checks=324,full_notebook56_completed=False)
    return checked


def cache_members(z):
    rows=z.infolist();src.need(0<len(rows)<=64,'Bounded complete scalar ZIP inventory')
    names=set();folded=set();total=0
    for row in rows:
        src.parts(row.filename);mode=row.external_attr>>16
        src.need(not row.is_dir()and not row.flag_bits&1 and not stat.S_ISLNK(mode)and stat.S_IFMT(mode)in(0,stat.S_IFREG)
                 and row.filename not in names and row.filename.casefold()not in folded
                 and 0<=row.file_size<=ev.LOG_BYTES,'Unique ordinary bounded complete ZIP file')
        names.add(row.filename);folded.add(row.filename.casefold());total+=row.file_size
    required={'SOURCES.json','STAGE_OBSERVED.json','STAGE_COMPLETED.json'}
    required|={'capsule/'+n for n in src.FILES+src.OUTPUTS}
    required|={'execution/'+n for n in('launch.json','supervisor-result.json','stdout.txt','stderr.txt','progress.json','progress.jsonl')}
    required|={'execution/checkpoints/'+n for n in src.OUTPUTS}
    src.need(total<=CACHE_BYTES and names==required,'Exact complete scalar source/capture/output transaction');return rows


def save_completed(task,cache):
    task=Path(task);checked=ev.validate_completed(task);cache=src.ordinary(cache);cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip'
    p=cache/name;pending=cache/(name+'.pending')
    with zipfile.ZipFile(pending,'x',compression=zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for f in sorted(task.rglob('*')):
            src.ordinary(f)
            if f.is_file():z.write(f,f.relative_to(task).as_posix())
        cache_members(z)
    src.need(pending.stat().st_size<=CACHE_BYTES,'Bounded complete scalar ZIP')
    pin=src.digest(pending);pending.replace(p);p.with_suffix('.zip.sha256').write_bytes((pin+'  '+p.name+'\n').encode('ascii'))
    return dict(path=str(p),sha256=pin,stage_result_sha256=checked['stage_result_sha256'])


def restore_completed(cache,destination,*,root):
    cache=src.ordinary(cache);destination=src.ordinary(destination)
    if not cache.exists():return None
    src.need(cache.is_dir(),'Ordinary completed scalar cache')
    for p in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
        try:
            src.ordinary(p);marker=src.ordinary(p.with_suffix('.zip.sha256'))
            src.need(p.is_file()and p.stat().st_size<=CACHE_BYTES and marker.is_file()and marker.stat().st_size<=1024
                     and marker.read_text(encoding='ascii')==src.digest(p)+'  '+p.name+'\n','Actual complete ZIP SHA sidecar')
            restored=destination/('kappa-restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(p)as z:
                rows=cache_members(z);restored.mkdir(parents=True,exist_ok=False)
                for row in rows:
                    target=restored.joinpath(*src.parts(row.filename));target.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(row)as source,target.open('xb')as out:shutil.copyfileobj(source,out,src.MIB)
            checked=ev.validate_completed(restored)
            event(root,'finite1014_kappa_completed_cache_revalidated',cache=str(p),sha256=src.digest(p),
                  numerical_replay_skipped=True,full_notebook56_completed=False)
            return restored,checked,dict(path=str(p),sha256=src.digest(p))
        except Exception as error:event(root,'finite1014_kappa_complete_cache_rejected',cache=str(p),error=type(error).__name__+': '+str(error))
    return None


def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',backup_interval=60):
    from .environment import snapshot
    src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=3600,'Bounded live backup interval')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root=Path(work_root).resolve()/'finite1014-kappa'/stamp;root.mkdir(parents=True,exist_ok=False)
    durable=Path(durable_root).resolve()/'finite1014-kappa'/stamp
    cache=Path(durable_root).resolve()/'finite1014-kappa/completed'/src.PLAN_SHA256[:16]
    status=dict(schema='FINITE1014_KAPPA_SESSION_V1',state='started',started_utc=utc(),source_plan_sha256=src.PLAN_SHA256,
                scalar_certificate_arithmetic_completed=False,partial_numerical_resume=False,**{k:False for k in ev.FLAGS})
    atomic_json(root/'ENVIRONMENT.json',snapshot());atomic_json(root/'SESSION_RESULT.json',status)
    backups=Backups(root,durable,backup_interval);backups.start()
    try:
        src.verify_vendor()
        event(root,'finite1014_kappa_session_started',original_actions=1,source_files=3,partial_numerical_resume=False,
              full_notebook56_completed=False,all_index_conclusion_verified=False)
        loaded=restore_completed(cache,root/'restored',root=root)
        if loaded:task,checked,export=loaded;status['reused_complete_transaction']=True
        else:
            task=root/'arithmetic';checked=execute(task,root=root);export=save_completed(task,cache)
            status['reused_complete_transaction']=False
        status.update(state='complete_scalar_kappa_62_625_basic',task_relative=task.relative_to(root).as_posix(),
                      validated=checked,completed_export=export,scalar_certificate_arithmetic_completed=True)
    except BaseException as error:
        status.update(state='incomplete_scalar_kappa_no_acceptance',scalar_certificate_arithmetic_completed=False,
                      error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8',newline='\n')
        event(root,'finite1014_kappa_session_incomplete',error=status['error'],scalar_certificate_arithmetic_completed=False)
    finally:
        status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
        try:backups.close()
        except Exception as error:event(root,'finite1014_kappa_final_backup_failed',error=str(error))
        archive=bundle(root,durable)
    print('56K SCALAR CERTIFICATE RESULT:',status['state'],'\nZIP:',archive,flush=True)
    return dict(status=status,bundle=str(archive.resolve()),work=str(root.resolve()))
