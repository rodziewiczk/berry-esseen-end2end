"""58B/C: four original full calls per actual-index case, complete-case cache only."""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import platform,shutil,stat,sys,threading,time,traceback,uuid,zipfile
from . import finite2124_core_sources as src,finite2124_core_evidence as ev,linux_supervisor
from .colab_batch import atomic_json,bundle,event,utc

CACHE_BYTES=512*src.MIB

class Follow:
    def __init__(self,root,task,action):
        self.root,self.task,self.action=Path(root),Path(task),action;self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def loop(self):
        position=0;partial=b'';started=time.monotonic();last=-20;draining=False
        while True:
            try:
                with(self.task/'executions'/self.action/'stdout.txt').open('rb')as stream:stream.seek(position);raw=stream.read(src.MIB)
                position+=len(raw);lines=(partial+raw).split(b'\n');partial=lines.pop()
                for line in lines:event(self.root,'finite2124_core_original_stdout',action=self.action,line=line.decode('utf-8',errors='replace')[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:event(self.root,'finite2124_core_heartbeat',action=self.action,elapsed_seconds=elapsed,stdout_bytes=position,full_notebook58_completed=False);last=elapsed
            if self.stop.wait(.2):
                if draining:break
                draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped bounded progress observer')

def write_capture(task,request,action,observed,context,started,finished):
    src.need(action in('initial_construct','initial_accept'),'Only actual stopped INITIAL actions have this capture')
    task=Path(task);c=task/'capsule';d=task/'executions'/action;launch=src.read(d/'launch.json')
    folder=c/src.INITIAL/'captures'/(src.case(request['n'],request['band'])+'_'+action.split('_')[1]);folder.mkdir(parents=True,exist_ok=False)
    for kind in('stdout','stderr'):
        shutil.copyfile(d/(kind+'.txt'),folder/(kind+'.txt'));src.need(src.digest(folder/(kind+'.txt'))==observed[kind+'_sha256'],'Exact current stream copy')
    output=c/src.output_paths(action,request['n'],request['band'])[0]
    packet=dict(schema=ev.CAPTURE,status='COMPLETED',n=request['n'],band=request['band'],action=action.split('_')[1],
        command=launch['argv'],cwd=launch['cwd'],started_utc=started,finished_utc=finished,elapsed_seconds=observed['elapsed_seconds'],
        timeout_seconds=ev.WALL_SECONDS,returncode=observed['returncode'],timed_out=False,
        executable_sha256=context['python_executable_sha256'],python_version=context['python_version'],platform=context['platform'],
        source_freeze_sha256=src.INITIAL_FREEZE,source_review_sha256=src.digest(c/src.INITIAL_REVIEW),launcher_sha256=src.digest(__file__),
        stdout_sha256=observed['stdout_sha256'],stderr_sha256=observed['stderr_sha256'],result_sha256=src.digest(output),
        capture_bridge=dict(schema='ACTUAL21_24_INITIAL_CAPTURE_OUTER_BINDING_V1',action=action,n=request['n'],band=request['band'],
            source_plan_sha256=src.PLAN_SHA256,launch_sha256=src.digest(d/'launch.json'),supervisor_result_sha256=src.digest(d/'supervisor-result.json'),
            source_files_sha256=request['sources']))
    atomic_json(folder/'EXECUTION.json',packet)

def execute(task,cache,n,band,*,root):
    src.need(sys.platform=='linux','Actual Linux process-group supervision required')
    task=Path(task).resolve();request=src.prepare(cache,task,n,band);actions=[]
    context=dict(python_executable=sys.executable,python_executable_sha256=src.digest(Path(sys.executable).resolve()),python_version=sys.version,platform=platform.platform())
    for action in src.ACTIONS:
        src.verify_job(task,n,band)
        if action=='resource_construct':
            records={x['action']:x['observed']for x in actions};ev.validate_initial(task,request,context,records)
            src.write_review_epoch(task,n,band);event(root,'finite2124_core_current_review_epoch_created',n=n,band=band,historical_parent_reused=False)
        outputs=src.output_paths(action,n,band)
        src.need(all(not(task/'capsule'/name).exists()for name in outputs+src.capture_paths(action,n,band)),'Exclusive fresh action outputs')
        event(root,'finite2124_core_action_started',n=n,band=band,action=action,completed_actions=len(actions),total_actions=4,
              cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,full_notebook58_completed=False)
        started=utc()
        with Follow(root,task,action):
            observed=linux_supervisor.run(ev.command(request,action,sys.executable),
                cwd=task/'capsule'/(src.INITIAL if action.startswith('initial_')else src.RESOURCE),
                output_dir=task/'executions'/action,mode='untrusted_search',cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,
                memory_bytes=ev.MEMORY_BYTES,disk_bytes=512*src.MIB,log_bytes=16*src.MIB,heartbeat_seconds=20,
                checkpoint_paths=[task/'capsule'/v for v in outputs])
        finished=utc();actions.append(dict(action=action,observed=observed))
        atomic_json(task/'ACTIONS_PARTIAL.json',dict(actions=actions,conditional_core_arithmetic_completed=False,**{f:False for f in ev.FLAGS}))
        try:ev.transport(task,request,action,observed,context)
        except Exception as error:
            tail='';p=task/'executions'/action/'stderr.txt'
            if p.is_file()and not p.is_symlink()and p.stat().st_size<=16*src.MIB:
                with p.open('rb')as stream:stream.seek(max(0,p.stat().st_size-4096));tail=stream.read(4096).decode('utf-8',errors='replace')
            event(root,'finite2124_core_action_incomplete',n=n,band=band,action=action,reason=observed.get('reason'),returncode=observed.get('returncode'),stderr_tail=tail,error=str(error))
            raise ValueError('Original actual-index '+action+' did not complete: '+str(error)+'; stderr tail: '+tail)from error
        src.verify_job(task,n,band)
        if action.startswith('initial_'):write_capture(task,request,action,observed,context,started,finished)
        src.verify_job(task,n,band)
        event(root,'finite2124_core_action_stopped',n=n,band=band,action=action,completed_actions=len(actions),total_actions=4,full_notebook58_completed=False)
    report=dict(schema=ev.OBSERVED,scope=ev.SCOPE,n=n,band=band,original_task_root=request['original_task_root'],implementation=ev.implementation(),
                **context,actions=actions,conditional_core_arithmetic_completed=False,**{f:False for f in ev.FLAGS})
    atomic_json(task/'STAGE_OBSERVED.json',report);summary=ev.validate_run(task,report)
    complete=dict(schema=ev.COMPLETED,scope=ev.SCOPE,implementation=ev.implementation(),observed_sha256=src.digest(task/'STAGE_OBSERVED.json'),
        summary=summary,artifacts=ev.inventory(task),conditional_core_arithmetic_completed=True,**{f:False for f in ev.FLAGS})
    atomic_json(task/'STAGE_COMPLETED.json',complete);return ev.validate_completed(task,expected_n=n,expected_band=band)

def cache_members(z):
    rows=z.infolist();src.need(0<len(rows)<=1500,'Bounded complete four-call ZIP');names=set();folded=set();total=0
    for r in rows:
        src.parts(r.filename);mode=r.external_attr>>16
        src.need(not r.is_dir()and not r.flag_bits&1 and not stat.S_ISLNK(mode)and stat.S_IFMT(mode)in(0,stat.S_IFREG)
                 and r.filename not in names and r.filename.casefold()not in folded and 0<=r.file_size<=128*src.MIB,'Unique ordinary bounded nonlinked cache member')
        names.add(r.filename);folded.add(r.filename.casefold());total+=r.file_size
    required={'SOURCES.json','STAGE_OBSERVED.json','STAGE_COMPLETED.json'}|{'executions/'+a+'/'+n for a in src.ACTIONS for n in('launch.json','supervisor-result.json','stdout.txt','stderr.txt')}
    src.need(total<=CACHE_BYTES and required<=names,'Entire four-call completed ledger required before extraction');return rows

def save_completed(task,cache):
    task=Path(task);checked=ev.validate_completed(task);cache=src.ordinary(Path(cache));cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip';p=cache/name;pending=cache/(name+'.pending')
    with zipfile.ZipFile(pending,'x',compression=zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for f in sorted(task.rglob('*')):
            src.ordinary(f)
            if f.is_file():z.write(f,f.relative_to(task).as_posix())
        cache_members(z)
    src.need(pending.stat().st_size<=CACHE_BYTES,'Bounded complete-case cache');pin=src.digest(pending);pending.replace(p)
    p.with_suffix('.zip.sha256').write_bytes((pin+'  '+p.name+'\n').encode('ascii'))
    return dict(path=str(p),sha256=pin,stage_result_sha256=checked['stage_result_sha256'])

def restore_completed(cache,destination,n,band,*,root):
    src.case(n,band);cache=src.ordinary(Path(cache));destination=Path(destination)
    if not cache.exists():return None
    src.need(cache.is_dir(),'Ordinary complete-case cache')
    for p in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
        try:
            src.ordinary(p);marker=src.ordinary(p.with_suffix('.zip.sha256'))
            src.need(p.is_file()and p.stat().st_size<=CACHE_BYTES and marker.is_file()and marker.stat().st_size<=1024
                     and marker.read_text('ascii')==src.digest(p)+'  '+p.name+'\n','Actual cache ZIP hash sidecar')
            restored=destination/('core-restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(p)as z:
                rows=cache_members(z);restored.mkdir(parents=True,exist_ok=False)
                for row in rows:
                    q=restored.joinpath(*src.parts(row.filename));q.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(row)as source,q.open('xb')as target:shutil.copyfileobj(source,target,src.MIB)
            checked=ev.validate_completed(restored,expected_n=n,expected_band=band)
            event(root,'finite2124_core_complete_case_revalidated',n=n,band=band,cache=str(p),sha256=src.digest(p),numerical_replay_skipped=True,full_notebook58_completed=False)
            return restored,checked,dict(path=str(p),sha256=src.digest(p))
        except Exception as error:event(root,'finite2124_core_cache_rejected',n=n,band=band,cache=str(p),error=type(error).__name__+': '+str(error))
    return None

class Backups:
    def __init__(self,root,durable,interval):
        self.root,self.durable=Path(root),Path(durable);self.interval=interval;self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def copy(self):
        for p in self.root.rglob('*'):
            src.ordinary(p)
            if not p.is_file()or p.stat().st_size>16*src.MIB:continue
            rel=p.relative_to(self.root).as_posix()
            if '/capsule/'in rel or '/checkpoints/'in rel or p.suffix not in('.json','.jsonl','.txt'):continue
            target=self.durable/'live'/rel;target.parent.mkdir(parents=True,exist_ok=True);pending=target.with_name(target.name+'.pending');shutil.copyfile(p,pending);pending.replace(target)
    def loop(self):
        while not self.stop.wait(self.interval):
            try:self.copy();event(self.root,'finite2124_core_live_backup_saved',partial_numerical_resume=False)
            except Exception as error:event(self.root,'finite2124_core_backup_failed',error=str(error))
    def start(self):self.thread.start()
    def close(self):self.stop.set();self.thread.join(timeout=30);src.need(not self.thread.is_alive(),'Stopped live backup observer');self.copy()

def run_colab(band,*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
    from .environment import snapshot
    src.case(21,band);src.plan();src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=3600,'Bounded backup interval')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8];label='finite2124-core-'+band
    root=Path(work_root).resolve()/label/stamp;root.mkdir(parents=True,exist_ok=False);durable=Path(durable_root).resolve()/label/stamp
    completed=Path(durable_root).resolve()/label/'completed'/src.PLAN_SHA256[:16]
    status=dict(schema='CONDITIONAL_FINITE2124_CORE_SESSION_V1',state='started',band=band,actual_n=[21,22,23,24],started_utc=utc(),
                cases=[],conditional_band_core_arithmetic_completed=False,partial_numerical_resume=False,source_plan_sha256=src.PLAN_SHA256,**{f:False for f in ev.FLAGS})
    atomic_json(root/'ENVIRONMENT.json',snapshot());atomic_json(root/'SESSION_RESULT.json',status)
    backups=Backups(root,durable,backup_interval);backups.start()
    try:
        assets=None;source_cache=None
        for n in(21,22,23,24):
            case=src.case(n,band);loaded=restore_completed(completed/case,root/'restored',n,band,root=root)
            if loaded:task,checked,export=loaded;reused=True
            else:
                if source_cache is None:
                    assets=src.obtain_assets(archives,progress=lambda name,**fields:event(root,name,**fields))
                    source_cache=src.prepare_cache(assets,Path(work_root).resolve()/'finite2124-core-source-cache'/src.PLAN_SHA256[:16])
                task=root/'arithmetic'/case;checked=execute(task,source_cache,n,band,root=root);export=save_completed(task,completed/case);reused=False
            status['cases'].append(dict(n=n,band=band,task_relative=task.relative_to(root).as_posix(),validated=checked,completed_export=export,reused_complete_case=reused))
            atomic_json(root/'SESSION_RESULT.json',status);event(root,'finite2124_core_case_finished',n=n,band=band,completed_cases=len(status['cases']),total_cases=4,full_notebook58_completed=False)
        status.update(state='complete_conditional_actual21_24_'+band+'_initial_resources_basic',conditional_band_core_arithmetic_completed=True)
    except BaseException as error:
        status.update(state='incomplete_actual21_24_core_no_global_acceptance',error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8',newline='\n');event(root,'finite2124_core_incomplete',error=status['error'],completed_cases=len(status['cases']))
    finally:
        status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
        try:backups.close()
        except Exception as error:event(root,'finite2124_core_final_backup_failed',error=str(error))
        archive=bundle(root,durable)
    print('58B/C INITIAL RESOURCE RESULT:',status['state'],'\nZIP:',archive,flush=True)
    return dict(status=status,bundle=str(archive.resolve()),work=str(root.resolve()))
