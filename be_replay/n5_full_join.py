"""Full67:22 original calls, complete08/11/13/35 readback and25 semantic joins.

Numerical programs run only in actual guarded Colab Linux children. Fourteen
control stages cache separately. The four support and four complement actions
share one atomic physical epoch because original acceptors bind actual cwd;
their historical capture paths are never rewritten to fake new executions.
"""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import shutil,stat,sys,threading,time,traceback,uuid,zipfile
from . import linux_supervisor,n5_full_join_sources as src,n5_full_join_control_evidence as evidence
from .colab_batch import atomic_json,bundle,event,utc

CACHE_BYTES=1024**3

class Follow:
    def __init__(self,root,execution,action):
        self.root,self.execution,self.action=Path(root),Path(execution),action
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def loop(self):
        offset=0;partial=b'';started=time.monotonic();last=-20;draining=False
        while True:
            try:
                with(self.execution/'stdout.txt').open('rb')as stream:stream.seek(offset);raw=stream.read(src.MIB)
                offset+=len(raw);lines=(partial+raw).split(b'\n');partial=lines.pop()
                for line in lines:event(self.root,'n5_full_original_stdout',action=self.action,line=line.decode('utf-8',errors='replace')[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:
                event(self.root,'n5_full_action_heartbeat',action=self.action,elapsed_seconds=elapsed,stdout_bytes=offset,full_n5_verified=False);last=elapsed
            if self.stop.wait(.2):
                if draining:break
                draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):
        self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped original stdout observer')

def capture_original(task,action,launch,observed,local_inputs):
    """Save only actual stopped streams into the unchanged original slots."""
    label=action.get('capture_label')
    if label is None:return
    task=Path(task);directory=task/'capsule'/action['cwd'];capture=task/'capsule/runs/cutoff5_20261020/high'/label
    src.need(not capture.exists(),'Never reuse or overwrite historical native capture')
    for name,pin in local_inputs.items():src.need(src.digest(directory/name)==pin,'Actual inputs unchanged during original call')
    capture.mkdir(parents=True,exist_ok=False)
    for kind in('stdout','stderr'):
        path=task/'executions'/action['id']/(kind+'.txt');src.need(src.digest(path)==observed[kind+'_sha256'],'Actual stopped native stream')
        shutil.copyfile(path,capture/(kind+'.txt'))
    atomic_json(capture/'metadata.json',dict(command=launch,cwd=str(directory),returncode=observed['returncode'],
        input_sha256=local_inputs,stdout_sha256=observed['stdout_sha256'],stderr_sha256=observed['stderr_sha256'],
        changed_inputs=[],scope='NEW_ACTUAL_GUARDED_NOTEBOOK67_EXECUTION'))

def execute(group_id,cache,task,*,root):
    src.need(sys.platform=='linux','Full original67 mathematical actions require actual Colab Linux')
    task=Path(task).resolve();request=src.prepare(group_id,cache,task);records=[]
    observed=dict(schema=evidence.OBSERVED,group_id=group_id,implementation=evidence.implementation(),
        actions=records,conditional_arithmetic_completed=False,**{k:False for k in evidence.FLAGS})
    atomic_json(task/'OBSERVED.json',observed)
    for action in src.actions(group_id):
        src.verify(task,allow_missing_outputs=True)
        for output in action['outputs']:src.need(not(task/'capsule'/output).exists(),'Fresh native output slot, never historical receipt input')
        directory=task/'capsule'/action['cwd'];local_inputs={p.name:src.digest(p)for p in directory.iterdir()if p.is_file()}
        argv=[sys.executable,*action['argv']];execution=task/'executions'/action['id']
        event(root,'n5_full_original_action_started',group_id=group_id,action=action['id'],
            cpu_seconds=evidence.CPU_SECONDS,wall_seconds=evidence.WALL_SECONDS,memory_bytes=evidence.MEMORY_BYTES,
            partial_numerical_resume=False,full_n5_verified=False)
        with Follow(root,execution,action['id']):
            result=linux_supervisor.run(argv,cwd=directory,output_dir=execution,mode='untrusted_search',
                cpu_seconds=evidence.CPU_SECONDS,wall_seconds=evidence.WALL_SECONDS,memory_bytes=evidence.MEMORY_BYTES,
                disk_bytes=evidence.DISK_BYTES,log_bytes=evidence.LOG_BYTES,heartbeat_seconds=20,checkpoint_paths=[])
        record=dict(action_id=action['id'],python=sys.executable,observed=result)
        records.append(record);atomic_json(task/'OBSERVED.json',observed)
        src.need(result.get('status')=='completed'and type(result.get('returncode'))is int and result['returncode']==0
            and result.get('reason')is None,'Original full67 action completed without timeout/failure')
        src.need((execution/'stderr.txt').stat().st_size==0,'Original successful action has empty actual stderr')
        capture_original(task,action,argv,result,local_inputs)
        evidence.capture(task,action,record)
        event(root,'n5_full_original_action_completed',action=action['id'],completed_actions=len(records),total_actions=len(src.actions(group_id)),full_n5_verified=False)
    summary=evidence.validate_observed(task,observed)
    completed=dict(schema=evidence.SCHEMA,implementation=evidence.implementation(),observed_sha256=src.digest(task/'OBSERVED.json'),
        summary=summary,artifacts=evidence.inventory(task),conditional_arithmetic_completed=True,**{k:False for k in evidence.FLAGS})
    atomic_json(task/'COMPLETED.json',completed);return evidence.validate_completed(task)

def cache_members(z):
    rows=z.infolist();src.need(0<len(rows)<=20000,'Bounded complete67 group ZIP inventory');seen=set();total=0
    for row in rows:
        src.parts(row.filename);src.need(row.filename.casefold()not in seen and not row.is_dir()and not row.flag_bits&1
            and stat.S_IFMT(row.external_attr>>16)in(0,stat.S_IFREG)and 0<=row.file_size<=128*src.MIB,
            'Unique ordinary nonlinked complete67 member')
        seen.add(row.filename.casefold());total+=row.file_size
    src.need(total<=CACHE_BYTES and {'REQUEST.json','OBSERVED.json','COMPLETED.json'}<={r.filename for r in rows},
        'Entire bounded original67 source/capture/completed epoch')
    return rows

def save_completed(task,cache):
    task=Path(task);checked=evidence.validate_completed(task);cache=src.ordinary(cache);cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip'
    output=cache/name;pending=cache/(name+'.pending')
    with zipfile.ZipFile(pending,'x',zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for p in sorted(task.rglob('*')):
            src.ordinary(p)
            if p.is_file():z.write(p,p.relative_to(task).as_posix())
    with zipfile.ZipFile(pending)as z:cache_members(z)
    src.need(pending.stat().st_size<=CACHE_BYTES,'Bounded67 complete ZIP');pin=src.digest(pending);pending.replace(output)
    marker=output.with_suffix('.zip.sha256');temporary=marker.with_name(marker.name+'.pending')
    temporary.write_text(pin+'  '+name+'\n',encoding='ascii',newline='\n');temporary.replace(marker)
    return dict(path=str(output),sha256=pin,completed_sha256=checked['completed_sha256'])

def restore_completed(group_id,cache,destination,*,root):
    cache=src.ordinary(cache)
    if not cache.exists():return None
    for path in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
        try:
            src.ordinary(path);marker=src.ordinary(path.with_suffix('.zip.sha256'))
            src.need(path.is_file()and path.stat().st_size<=CACHE_BYTES and marker.is_file()and marker.stat().st_size<=1024
                and marker.read_text('ascii')==src.digest(path)+'  '+path.name+'\n','Actual67 cache ZIP and exact SHA sidecar')
            task=Path(destination)/(group_id+'-restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(path)as z:
                rows=cache_members(z);task.mkdir(parents=True,exist_ok=False)
                for row in rows:
                    target=task.joinpath(*src.parts(row.filename));target.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(row)as source,target.open('xb')as output:shutil.copyfileobj(source,output,src.MIB)
            checked=evidence.validate_completed(task);src.need(checked['group_id']==group_id,'Exact same67 group identity')
            event(root,'n5_full_completed_group_revalidated',group_id=group_id,path=str(path),sha256=src.digest(path),numerical_replays_skipped=True)
            return task,checked,dict(path=str(path),sha256=src.digest(path))
        except Exception as error:event(root,'n5_full_completed_cache_rejected',group_id=group_id,path=str(path),error=type(error).__name__+': '+str(error))
    return None

class Backups:
    def __init__(self,root,durable,interval):
        self.root,self.durable,self.interval=Path(root),Path(durable),interval;self.error=None
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def copy(self):
        for p in self.root.rglob('*'):
            if not p.is_file():continue
            rel=p.relative_to(self.root)
            if any(x in rel.parts for x in('capsule','source-cache','imports','semantic-current','provenance'))or p.stat().st_size>16*src.MIB:continue
            if p.suffix not in('.json','.jsonl','.txt'):continue
            src.ordinary(p);target=self.durable/'live'/rel;target.parent.mkdir(parents=True,exist_ok=True)
            tmp=target.with_name(target.name+'.pending');shutil.copyfile(p,tmp);tmp.replace(target)
    def loop(self):
        while not self.stop.wait(self.interval):
            try:self.copy();event(self.root,'n5_full_live_backup_saved',completed_stage_ZIPs_are_separate=True)
            except BaseException as error:self.error=type(error).__name__+': '+str(error);event(self.root,'n5_full_live_backup_failed',error=self.error)
    def start(self):self.thread.start()
    def close(self):self.stop.set();self.thread.join(timeout=30);src.need(not self.thread.is_alive(),'Stopped67 backup worker');self.copy()

def run_groups(root,cache,source_cache,status):
    for g in src.plan()['groups']:
        found=restore_completed(g['id'],Path(cache)/g['id'],Path(root)/'groups',root=root)
        if found:task,checked,export=found;reused=True
        else:
            task=Path(root)/'groups'/(g['id']+'-'+uuid.uuid4().hex[:8]);reused=False
            checked=execute(g['id'],source_cache,task,root=root);export=save_completed(task,Path(cache)/g['id'])
        status['groups'].append(dict(group_id=g['id'],task_relative=task.relative_to(root).as_posix(),validated=checked,
            export=export,reused_completed_stage=reused))
        atomic_json(Path(root)/'SESSION_RESULT.json',status)
        event(root,'n5_full_group_progress',completed_groups=len(status['groups']),total_groups=15,
            completed_original_calls=sum(len(src.group(r['group_id'])['action_ids'])for r in status['groups']),total_original_calls=22,
            full_n5_verified=False)

def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
    from . import n5_full_join_evidence as semantic
    from .environment import snapshot
    src.need(sys.platform=='linux','Full67 original actions require actual Linux')
    src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=300,'Bounded67 log backup interval')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root=Path(work_root).resolve()/'n5-full-join'/stamp;root.mkdir(parents=True,exist_ok=False)
    durable=Path(durable_root).resolve()/'n5-full-join'/stamp;cache=Path(durable_root).resolve()/'n5-full-join/completed'/src.PLAN_SHA256[:16]
    status=dict(schema=semantic.SCHEMA,state='incomplete',started_utc=utc(),groups=[],imports=[],conditional_finite_chain_verified=False,
        original_calls_required=22,semantic_resource_regions_required=12,semantic_count_regions_required=12,
        unacquired_universal_analytic_premises=list(semantic.UNIVERSAL_PREMISES),**{k:False for k in evidence.FLAGS})
    atomic_json(root/'ENVIRONMENT.json',snapshot());atomic_json(root/'SESSION_RESULT.json',status)
    backups=Backups(root,durable,backup_interval);backups.start()
    event(root,'n5_full_join_started',original_calls=22,physical_atomic_groups=15,resource_semantic_regions=12,count_semantic_regions=12,
        cpu_seconds_per_action=82800,wall_seconds_per_action=82800,full_n5_verified=False)
    try:
        archive=src.obtain_archive(archives,progress=lambda name,**data:event(root,name,**data))
        source_cache=src.prepare_cache(archive,root/'source-cache',progress=lambda name,**data:event(root,name,**data))
        run_groups(root,cache,source_cache,status)
        missing=semantic.import_completed_inputs(root,durable_root,status)
        if missing:status.update(state='waiting_for_complete_prerequisite_exports',missing=missing)
        else:
            chain=semantic.validate_batch(root,status,prepare=True);atomic_json(root/'FINITE_CHAIN.json',chain)
            status.update(state=semantic.COMPLETE,conditional_finite_chain_verified=True,finite_chain_sha256=src.digest(root/'FINITE_CHAIN.json'))
            atomic_json(root/'SESSION_RESULT.json',status);semantic.validate_completed(root)
    except BaseException as error:
        status.update(state='incomplete',conditional_finite_chain_verified=False,error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8',newline='\n')
        event(root,'n5_full_join_incomplete',error=status['error'],completed_groups=len(status['groups']),full_n5_verified=False)
    finally:
        status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
        try:backups.close()
        except BaseException as error:status.update(state='incomplete',conditional_finite_chain_verified=False,backup_error=type(error).__name__+': '+str(error))
        if backups.error:status.update(state='incomplete',conditional_finite_chain_verified=False,backup_error=backups.error)
        atomic_json(root/'SESSION_RESULT.json',status)
        try:archive=bundle(root,durable)
        except BaseException as error:
            status.update(state='incomplete',conditional_finite_chain_verified=False,bundle_error=type(error).__name__+': '+str(error));atomic_json(root/'SESSION_RESULT.json',status)
            archive=bundle(root,Path(work_root).resolve()/'n5-full-join-local-exports'/stamp)
        event(root,'n5_full_final_bundle_saved',state=status['state'],path=str(archive),sha256=src.digest(archive),full_n5_verified=False)
    print('67 FULL CONDITIONAL CHAIN RESULT:',status['state'],'\nZIP:',archive,flush=True)
    return dict(status=status,bundle=str(archive),work=str(root))
