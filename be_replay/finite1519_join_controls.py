"""Internal full six-call57H control transaction, not a standalone notebook."""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import shutil,stat,sys,threading,time,uuid,zipfile
from . import finite1519_join_control_sources as src,finite1519_join_control_evidence as ev,linux_supervisor
from .colab_batch import atomic_json,event

CACHE_BYTES=512*src.MIB


def bind_current_geometry(task,upstream):
    from . import finite1039_count_evidence as native
    task=src.ordinary(task);upstream=src.ordinary(upstream);d=src.plan()['fresh_geometry_fixture']
    checked=native.validate_completed(upstream)
    src.need(checked['job_id']==d['job_id']and checked['conditional_arithmetic_completed']is True,
             'Genuine complete current selected COUNT56 required before geometry control')
    members=native.inventory(upstream);destination=task/'upstream/count56'
    src.need(not destination.exists(),'Exclusive genuine upstream transaction copy')
    for name in members:
        source=src.child(upstream,name);target=src.child(destination,name);target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
    # The native inventory intentionally excludes both transaction ledgers.
    for name in('STAGE_OBSERVED.json','STAGE_COMPLETED.json'):
        shutil.copyfile(upstream/name,destination/name)
    src.need(ev.same(native.validate_completed(destination),checked),'Complete relocated upstream execution preserves its original context')
    files={};prefix='work/'+d['directory']+'/'
    for key in('contract_name','forest_name','acceptance_name'):
        name=d[key];source=src.child(destination,'capsule/'+d['directory']+'/'+name);target=src.child(task,'capsule/'+prefix+name)
        src.need(not target.exists(),'Historical geometry payload is never pre-staged as fresh')
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);files[name]=src.digest(target)
    packet=dict(schema='FINITE1519_CURRENT_GENUINE_COUNT56_FIXTURE_V1',validated_native_count=checked,
        catalog_sha256=d['catalog_sha256'],files_sha256=files,current_execution_required=True,historical_acceptance_promoted=False)
    atomic_json(task/'CURRENT_GEOMETRY_FIXTURE.json',packet);ev.fixture(task)


class Follow:
    def __init__(self,root,task,action):
        self.root,self.task,self.action=Path(root),Path(task),action
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def loop(self):
        position=0;partial=b'';started=time.monotonic();last=-20;draining=False
        while True:
            try:
                with(self.task/'executions'/self.action/'stdout.txt').open('rb')as f:f.seek(position);raw=f.read(src.MIB)
                position+=len(raw);lines=(partial+raw).split(b'\n');partial=lines.pop()
                for line in lines:event(self.root,'finite1519_join_original_stdout',action=self.action,line=line.decode('utf-8',errors='replace')[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:
                event(self.root,'finite1519_join_control_heartbeat',action=self.action,elapsed_seconds=elapsed,
                      stdout_bytes=position,full_notebook57_completed=False);last=elapsed
            if self.stop.wait(.2):
                if draining:break
                draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):
        self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),'Stopped bounded progress reader')


def execute(source_cache,task,*,root,upstream_count56):
    src.need(sys.platform=='linux','Actual Linux process-tree supervision required')
    task=src.ordinary(task);request=src.prepare_task(source_cache,task);bind_current_geometry(task,upstream_count56)
    acceptance=ev.fixture(task);actions=[];prior={}
    for row in src.cases():
        action=row['id'];ev.source_task(task);epoch=src.derive_current_metadata(task,validated_prior_actions=prior)
        inputs=src.input_map(task,action,validated_prior_actions=prior,fixture_acceptance_sha256=acceptance)
        src.need(not(task/'capsule'/row['output']).exists()
                 and all(not(task/'capsule'/name).exists()for name in row['generated_engine_copies']),
                 'Exclusive original result and genuinely native-generated helpers')
        event(root,'finite1519_join_original_control_started',action=action,completed=len(actions),total=6,
              cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,memory_bytes=ev.MEMORY_BYTES,full_notebook57_completed=False)
        with Follow(root,task,action):
            observed=linux_supervisor.run(ev.command(row,sys.executable),cwd=task/'capsule'/row['cwd'],
                output_dir=task/'executions'/action,mode='untrusted_search',cpu_seconds=ev.CPU_SECONDS,wall_seconds=ev.WALL_SECONDS,
                memory_bytes=ev.MEMORY_BYTES,disk_bytes=ev.DISK_BYTES,log_bytes=ev.LOG_BYTES,heartbeat_seconds=20,
                checkpoint_paths=[task/'capsule'/row['output']])
        record=dict(id=action,observed=observed,inputs_before=inputs,
                    inputs_after=src.input_map(task,action,validated_prior_actions=prior,fixture_acceptance_sha256=acceptance),
                    metadata_epoch=epoch,output_sha256=src.digest(task/'capsule'/row['output'])if(task/'capsule'/row['output']).is_file()else None)
        atomic_json(task/'CURRENT_ACTION_OBSERVED.json',record)
        streams=ev.transport(task,row,record,request,sys.executable)
        src.need(ev.same(record['inputs_before'],record['inputs_after']),'All actual bounded-control inputs unchanged across stop')
        summary=ev.mathematical_reference(task,row,inputs,streams);prior[action]=summary;actions.append(record)
        atomic_json(task/'ACTIONS_PARTIAL.json',dict(actions=actions,conditional_controls_completed=False,**{k:False for k in ev.FLAGS}))
        event(root,'finite1519_join_original_control_completed',action=action,completed=len(actions),total=6,full_notebook57_completed=False)
    report=dict(schema=ev.OBSERVED,scope=ev.SCOPE,original_task_root=request['original_task_root'],implementation=ev.implementation(),
                python_executable=sys.executable,python_version=sys.version,actions=actions,conditional_controls_completed=False,**{k:False for k in ev.FLAGS})
    atomic_json(task/'CONTROLS_OBSERVED.json',report);summary=ev.validate_run(task,report)
    done=dict(schema=ev.COMPLETED,scope=ev.SCOPE,implementation=ev.implementation(),observed_sha256=src.digest(task/'CONTROLS_OBSERVED.json'),
              summary=summary,artifacts=ev.inventory(task),conditional_controls_completed=True,**{k:False for k in ev.FLAGS})
    atomic_json(task/'CONTROLS_COMPLETED.json',done);return ev.validate_completed(task)


def cache_members(archive):
    rows=archive.infolist();names=set();folded=set();total=0
    src.need(0<len(rows)<=10000,'Bounded complete six-control inventory')
    for row in rows:
        src.base.parts(row.filename);mode=row.external_attr>>16
        src.need(not row.is_dir()and not row.flag_bits&1 and stat.S_IFMT(mode)in(0,stat.S_IFREG)
                 and row.filename not in names and row.filename.casefold()not in folded
                 and 0<=row.file_size<=128*src.MIB,'Unique ordinary bounded complete control ZIP member')
        src.need(row.filename.split('/')[0]in('capsule','provenance','upstream','executions','SOURCES.json',
             'CURRENT_GEOMETRY_FIXTURE.json','CURRENT_ACTION_OBSERVED.json','ACTIONS_PARTIAL.json',
             'CONTROLS_OBSERVED.json','CONTROLS_COMPLETED.json'),'Exact complete control cache namespace')
        names.add(row.filename);folded.add(row.filename.casefold());total+=row.file_size
    required={'SOURCES.json','CURRENT_GEOMETRY_FIXTURE.json','CONTROLS_OBSERVED.json','CONTROLS_COMPLETED.json',
              'upstream/count56/STAGE_COMPLETED.json','upstream/count56/STAGE_OBSERVED.json'}
    required|={'executions/'+action+'/'+file for action in src.IDS for file in('launch.json','supervisor-result.json','stdout.txt','stderr.txt')}
    src.need(total<=CACHE_BYTES and required<=names,'Entire genuine stopped six-action and upstream COUNT execution')
    return rows


def save_completed(task,cache):
    task=src.ordinary(task);checked=ev.validate_completed(task);cache=src.ordinary(cache);cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]+'-complete.zip';p=cache/name;pending=cache/(name+'.pending')
    with zipfile.ZipFile(pending,'x',zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for f in sorted(task.rglob('*')):
            src.ordinary(f)
            if f.is_file():z.write(f,f.relative_to(task).as_posix())
        cache_members(z)
    src.need(pending.stat().st_size<=CACHE_BYTES,'Bounded complete control transport');pin=src.digest(pending);pending.replace(p)
    p.with_suffix('.zip.sha256').write_bytes((pin+'  '+p.name+'\n').encode('ascii'))
    return dict(path=str(p),sha256=pin,controls_result_sha256=checked['controls_result_sha256'])


def restore_completed(cache,destination,*,root):
    cache=src.ordinary(cache);destination=src.ordinary(destination)
    if not cache.exists():return None
    for p in sorted(cache.glob('*-complete.zip'),reverse=True)[:8]:
        try:
            src.ordinary(p);marker=src.ordinary(p.with_suffix('.zip.sha256'))
            src.need(p.is_file()and p.stat().st_size<=CACHE_BYTES and marker.is_file()and marker.stat().st_size<=1024
                     and marker.read_text('ascii')==src.digest(p)+'  '+p.name+'\n','Actual complete six-control SHA sidecar')
            restored=destination/('restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(p)as z:
                rows=cache_members(z);restored.mkdir(parents=True,exist_ok=False)
                for row in rows:
                    out=src.child(restored,row.filename);out.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(row)as source,out.open('xb')as target:shutil.copyfileobj(source,target,src.MIB)
            checked=ev.validate_completed(restored)
            event(root,'finite1519_join_controls_cache_revalidated',cache=str(p),sha256=src.digest(p),numerical_replays_skipped=True)
            return restored,checked,dict(path=str(p),sha256=src.digest(p))
        except Exception as error:event(root,'finite1519_join_controls_cache_rejected',cache=str(p),error=type(error).__name__+': '+str(error))
    return None
