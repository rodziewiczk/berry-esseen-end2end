"""59A: both complete original actual26--30 B1 Fourier passes."""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import shutil,stat,sys,threading,time,traceback,uuid,zipfile
from . import finite2630_b1_sources as s,finite2630_b1_evidence as e,linux_supervisor
from .colab_batch import Backups,atomic_json,bundle,event,utc

CACHE_BYTES=128*s.MIB

class Follow:
    def __init__(self,root,task,action):
        self.root,self.task,self.action=Path(root),Path(task),action
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def loop(self):
        offset=0;partial=b'';started=time.monotonic();last=-20;draining=False
        while True:
            try:
                with(self.task/'executions'/self.action/'stdout.txt').open('rb')as f:f.seek(offset);raw=f.read(s.MIB)
                offset+=len(raw);lines=(partial+raw).split(b'\n');partial=lines.pop()
                for line in lines:event(self.root,'finite2630_b1_original_stdout',action=self.action,
                    line=line.decode('utf-8',errors='replace')[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:
                event(self.root,'finite2630_b1_heartbeat',action=self.action,elapsed_seconds=elapsed,
                      stdout_bytes=offset,conditional_fourier_arithmetic_completed=False);last=elapsed
            if self.stop.wait(.2):
                if draining:break
                draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):
        self.stop.set();self.thread.join(timeout=5);s.need(not self.thread.is_alive(),'Stopped support progress observer')

def execute(task,cache,*,root):
    s.need(sys.platform=='linux','Actual Linux process-group supervision required')
    task=Path(task).resolve();request=s.prepare(cache,task);actions=[]
    for action in s.ACTIONS:
        s.verify_job(task);output=task/'capsule'/s.NATIVE/s.OUTPUTS[action]
        s.need(not output.exists(),'Exclusive fresh original output')
        event(root,'finite2630_b1_original_action_started',action=action,cpu_seconds=e.CPU,
              wall_seconds=e.WALL,memory_bytes=e.MEMORY,full_notebook59_completed=False)
        with Follow(root,task,action):
            observed=linux_supervisor.run(e.command(request,action,sys.executable),
                cwd=task/'capsule'/s.NATIVE,output_dir=task/'executions'/action,
                mode='untrusted_search',cpu_seconds=e.CPU,wall_seconds=e.WALL,memory_bytes=e.MEMORY,
                disk_bytes=e.DISK,log_bytes=e.LOG,heartbeat_seconds=20,checkpoint_paths=[output])
        try:e.transport(task,request,action,observed,sys.executable)
        except Exception as error:
            tail='';p=task/'executions'/action/'stderr.txt'
            if p.is_file()and not p.is_symlink()and p.stat().st_size<=e.LOG:
                with p.open('rb')as f:f.seek(max(0,p.stat().st_size-4096));tail=f.read(4096).decode('utf-8',errors='replace')
            event(root,'finite2630_b1_action_incomplete',action=action,error=str(error),stderr_tail=tail)
            raise ValueError('Original B1 Fourier '+action+' did not complete: '+str(error)+'; stderr: '+tail)from error
        s.verify_job(task);actions.append(dict(action=action,observed=observed))
        event(root,'finite2630_b1_original_action_completed',action=action,completed_actions=len(actions),total_actions=2)
    report=dict(schema='OBSERVED_FINITE2630_B1_V1',scope=e.SCOPE,implementation=e.implementation(),
        python_executable=sys.executable,python_version=sys.version,actions=actions,
        conditional_fourier_arithmetic_completed=False,**{k:False for k in e.FLAGS})
    atomic_json(task/'STAGE_OBSERVED.json',report);summary=e.validate_run(task,report)
    done=dict(schema='COMPLETED_FINITE2630_B1_V1',scope=e.SCOPE,implementation=e.implementation(),
        observed_sha256=s.digest(task/'STAGE_OBSERVED.json'),summary=summary,artifacts=e.inventory(task),
        conditional_fourier_arithmetic_completed=True,**{k:False for k in e.FLAGS})
    atomic_json(task/'STAGE_COMPLETED.json',done);return e.validate_completed(task)

def cache_members(z):
    rows=z.infolist();s.need(0<len(rows)<=256,'Bounded support transaction ZIP');names=set();folded=set();total=0
    for row in rows:
        s.parts(row.filename);mode=row.external_attr>>16
        s.need(not row.is_dir()and not row.flag_bits&1 and not stat.S_ISLNK(mode)
               and stat.S_IFMT(mode)in(0,stat.S_IFREG)and row.filename not in names
               and row.filename.casefold()not in folded and 0<=row.file_size<=128*s.MIB,'Unique ordinary bounded transaction member')
        names.add(row.filename);folded.add(row.filename.casefold());total+=row.file_size
    required={'SOURCES.json','LOCATION_EPOCH.json','STAGE_OBSERVED.json','STAGE_COMPLETED.json',
              'provenance/'+s.RECORD,'provenance/'+s.MANIFEST}
    required|={'capsule/'+n for n in s.plan()['source_files']}
    required|={'capsule/'+s.NATIVE+'/'+n for n in s.OUTPUTS.values()}
    required|={'executions/'+a+'/'+n for a in s.ACTIONS for n in
               ('launch.json','supervisor-result.json','stdout.txt','stderr.txt','progress.json','progress.jsonl',
                'checkpoints/'+s.OUTPUTS[a])}
    s.need(total<=CACHE_BYTES and names==required,'Exact whole two-pass source/capture/output transaction');return rows

def save_completed(task,cache):
    checked=e.validate_completed(task);cache=s.ordinary(Path(cache));cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip'
    output=cache/name;pending=cache/(name+'.pending')
    with zipfile.ZipFile(pending,'x',compression=zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for p in sorted(Path(task).rglob('*')):
            s.ordinary(p)
            if p.is_file():z.write(p,p.relative_to(task).as_posix())
        cache_members(z)
    s.need(pending.stat().st_size<=CACHE_BYTES,'Bounded completed ZIP');pin=s.digest(pending);pending.replace(output)
    output.with_suffix('.zip.sha256').write_bytes((pin+'  '+name+'\n').encode('ascii'))
    return dict(path=str(output),sha256=pin,stage_result_sha256=checked['stage_result_sha256'])

def restore_completed(cache,destination,*,root):
    cache=s.ordinary(Path(cache));destination=s.ordinary(Path(destination))
    if not cache.exists():return None
    s.need(cache.is_dir(),'Ordinary completed cache')
    for p in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
        try:
            s.ordinary(p);sidecar=s.ordinary(p.with_suffix('.zip.sha256'))
            s.need(p.is_file()and p.stat().st_size<=CACHE_BYTES and sidecar.is_file()and sidecar.stat().st_size<=1024
                   and sidecar.read_text(encoding='ascii')==s.digest(p)+'  '+p.name+'\n','Actual ZIP SHA sidecar')
            restored=destination/('restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(p)as z:
                rows=cache_members(z);restored.mkdir(parents=True,exist_ok=False)
                for row in rows:
                    target=restored.joinpath(*s.parts(row.filename));target.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(row)as source,target.open('xb')as dest:shutil.copyfileobj(source,dest,s.MIB)
            checked=e.validate_completed(restored)
            event(root,'finite2630_b1_completed_cache_revalidated',sha256=s.digest(p),numerical_replay_skipped=True)
            return restored,checked,dict(path=str(p),sha256=s.digest(p))
        except Exception as error:event(root,'finite2630_b1_cache_rejected',error=type(error).__name__+': '+str(error))
    return None

def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
    from .environment import snapshot
    s.need(type(backup_interval)in(int,float)and 1<=backup_interval<=3600,'Bounded backup interval')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root=Path(work_root).resolve()/'finite2630-b1'/stamp;root.mkdir(parents=True,exist_ok=False)
    durable=Path(durable_root).resolve()/'finite2630-b1'/stamp
    completed=Path(durable_root).resolve()/'finite2630-b1/completed'/s.PLAN_SHA256[:16]
    status=dict(schema='FINITE2630_B1_SESSION_V1',state='started',started_utc=utc(),source_plan_sha256=s.PLAN_SHA256,
        conditional_fourier_arithmetic_completed=False,partial_numerical_resume=False,**{k:False for k in e.FLAGS})
    atomic_json(root/'ENVIRONMENT.json',snapshot());atomic_json(root/'SESSION_RESULT.json',status)
    backups=Backups(root,durable,backup_interval);backups.start()
    try:
        loaded=restore_completed(completed,root/'restored',root=root)
        if loaded:task,checked,export=loaded;status['reused_complete_transaction']=True
        else:
            assets=s.obtain_assets(archives,progress=lambda name,**values:event(root,name,**values))
            cache=s.prepare_cache(assets,Path(work_root).resolve()/'finite2630-b1-source-cache'/s.PLAN_SHA256[:16]);task=root/'arithmetic'
            checked=execute(task,cache,root=root);export=save_completed(task,completed)
            status['reused_complete_transaction']=False
        status.update(state='complete_conditional_B1_fourier26_30_sublane_basic',
            task_relative=task.relative_to(root).as_posix(),validated=checked,completed_export=export,
            conditional_fourier_arithmetic_completed=True)
    except BaseException as error:
        status.update(state='incomplete_B1_fourier26_30',error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8',newline='\n')
        event(root,'finite2630_b1_incomplete',error=status['error'])
    finally:
        status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
        try:backups.close()
        except Exception as error:event(root,'finite2630_b1_final_backup_failed',error=str(error))
        archive=bundle(root,durable)
    print('59A B1 FOURIER RESULT:',status['state'],'\nZIP:',archive,flush=True)
    return dict(status=status,bundle=str(archive.resolve()),work=str(root.resolve()))
