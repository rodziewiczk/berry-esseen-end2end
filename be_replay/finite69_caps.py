"""Fresh supported owncaps and all nine conditional resource7--9 replays.

Only complete, source/capture-revalidated stages are reused. The five-call
owncaps transaction is atomic because its original inner captures bind their
originating absolute paths. No partial numerical state is resumed.
"""
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

from . import linux_supervisor,finite69_caps_sources as src,finite69_caps_evidence as evidence
from . import finite69_parents as parents,finite69_parent_sources as ps,finite69_parent_evidence as pe
from .colab_batch import atomic_json,bundle,event,utc

CACHE_BYTES=2048*src.MIB
CACHE_FILES=20000


def numpy_context():
    """Inspect installed discovery dependency metadata; do not import NumPy."""
    from importlib import metadata
    distribution=metadata.distribution("numpy");version=distribution.version
    entry=src.ordinary(Path(distribution.locate_file("numpy/__init__.py")))
    src.need(type(version)is str and bool(version)and entry.is_file(),"Installed NumPy discovery dependency")
    return dict(scope="UNTRUSTED_FLOATING_DISCOVERY_ONLY",distribution="numpy",version=version,
        entry_sha256=src.digest(entry),acceptance_arithmetic_depends_on_numpy=False)


class Follow:
    def __init__(self,root,task,label):
        self.root,self.task,self.label=Path(root),Path(task),label
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
    def loop(self):
        position=0;partial=b"";started=time.monotonic();last=-20;draining=False
        while True:
            try:
                with(self.task/"executions"/self.label/"stdout.txt").open("rb")as stream:
                    stream.seek(position);raw=stream.read(src.MIB)
                position+=len(raw);lines=(partial+raw).split(b"\n");partial=lines.pop()
                for line in lines:event(self.root,"finite69_caps_original_stdout",action=self.label,line=line.decode("utf-8",errors="replace")[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:
                event(self.root,"finite69_caps_heartbeat",action=self.label,elapsed_seconds=elapsed,stdout_bytes=position,
                    conditional_arithmetic_completed=False,all_index_conclusion_verified=False);last=elapsed
            if self.stop.wait(.2):
                if draining:break
                draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):
        self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),"Stopped bounded progress observer")


def complete(task,request,actions, *,root):
    report=dict(schema=evidence.OBSERVED,scope=evidence.SCOPE,job_id=request["job_id"],
        original_task_root=request["original_task_root"],implementation=evidence.implementation(),
        python_executable=sys.executable,python_version=sys.version,actions=actions,
        conditional_arithmetic_completed=False,**{f:False for f in evidence.FLAGS})
    atomic_json(task/"STAGE_OBSERVED.json",report)
    summary=evidence.validate_run(task,report)
    packet=dict(schema=evidence.COMPLETED,scope=evidence.SCOPE,job_id=request["job_id"],
        implementation=evidence.implementation(),observed_sha256=src.digest(task/"STAGE_OBSERVED.json"),
        artifacts=evidence.inventory(task),summary=summary,conditional_arithmetic_completed=True,
        **{f:False for f in evidence.FLAGS})
    atomic_json(task/"STAGE_COMPLETED.json",packet);checked=evidence.validate_completed(task)
    event(root,"finite69_caps_complete_stage",job_id=request["job_id"],summary=summary,all_index_conclusion_verified=False)
    return checked


def execute_prepared(task, *,root):
    src.need(sys.platform=="linux","The explicit process-group execution epoch requires Linux")
    task=Path(task);request=src.verify_job(task);actions=[]
    for spec in evidence.action_specs(request,sys.executable):
        if spec["label"]=="readback":
            output=task/"capsule"/src.AUDIT/"OWN_REQUEST.json"
            src.need(not output.exists(),"Fresh explicit readback request");output.write_bytes(evidence.request_bytes(task/"capsule"))
        event(root,"finite69_caps_full_action_started",job_id=request["job_id"],action=spec["label"],
            cpu_seconds=evidence.CPU,wall_seconds=evidence.WALL,memory_bytes=evidence.MEMORY,
            resource_policy=evidence.SCOPE,partial_numerical_resume=False)
        with Follow(root,task,spec["label"]):
            observed=linux_supervisor.run(spec["argv"],cwd=task/"capsule",output_dir=task/"executions"/spec["label"],
                wall_seconds=evidence.WALL,cpu_seconds=evidence.CPU,memory_bytes=evidence.MEMORY,
                checkpoint_paths=[task/"capsule"/p for p in spec["outputs"]],mode="untrusted_search",
                disk_bytes=evidence.DISK,log_bytes=16*src.MIB,heartbeat_seconds=20)
        call=dict(label=spec["label"],observed=observed);actions.append(call)
        atomic_json(task/"ACTION_PROGRESS.json",dict(job_id=request["job_id"],actions=actions,conditional_arithmetic_completed=False))
        try:
            stdout=evidence.transport(task,request,spec,call,sys.executable)
            evidence.action_terminal(task,spec,stdout)
        except Exception as error:
            tails={}
            for name in("stdout","stderr"):
                p=task/"executions"/spec["label"]/(name+".txt")
                if p.exists():
                    with p.open("rb")as stream:stream.seek(max(0,p.stat().st_size-4096));tails[name+"_tail"]=stream.read(4096).decode("utf-8",errors="replace")
            event(root,"finite69_caps_action_incomplete",action=spec["label"],reason=observed.get("reason"),error=str(error),**tails)
            raise ValueError("Full original action did not validate: "+spec["label"]+"; "+str(error)+"; "+str(tails))
    return complete(task,request,actions,root=root)


def cache_members(z):
    rows=z.infolist();src.need(0<len(rows)<=CACHE_FILES,"Bounded complete stage ZIP inventory")
    names=set();folded=set();total=0
    for row in rows:
        src.parts(row.filename);mode=row.external_attr>>16
        src.need(not row.is_dir()and not row.flag_bits&1 and not stat.S_ISLNK(mode)
            and stat.S_IFMT(mode)in(0,stat.S_IFREG)and row.filename not in names and row.filename.casefold()not in folded
            and 0<=row.file_size<=256*src.MIB,"Unique ordinary safe bounded completed-stage member")
        names.add(row.filename);folded.add(row.filename.casefold());total+=row.file_size
    src.need(total<=CACHE_BYTES and {"SOURCES.json","STAGE_OBSERVED.json","STAGE_COMPLETED.json"}<=names,"Whole bounded stage, not an unattested receipt")
    return rows


def save_stage(task,cache):
    task=Path(task);checked=evidence.validate_completed(task);cache=src.ordinary(cache);cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]+"-complete.zip"
    path=cache/name;pending=cache/(name+".pending")
    with zipfile.ZipFile(pending,"x",compression=zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for p in sorted(task.rglob("*")):
            src.ordinary(p)
            if p.is_file():z.write(p,p.relative_to(task).as_posix())
        cache_members(z)
    src.need(pending.stat().st_size<=CACHE_BYTES,"Bounded complete-stage transport")
    pin=src.digest(pending);pending.replace(path);marker=path.with_suffix(".zip.sha256")
    marker.write_text(pin+"  "+path.name+"\n",encoding="ascii")
    return dict(path=str(path),sha256=pin,stage_result_sha256=checked["stage_result_sha256"])


def restore_stage(cache,destination,job_id, *,root,bindings=None):
    cache=src.ordinary(cache)
    if not cache.exists():return None
    for path in sorted(cache.glob("*-complete.zip"),reverse=True)[:8]:
        try:
            src.ordinary(path);marker=src.ordinary(path.with_suffix(".zip.sha256"))
            src.need(path.is_file()and path.stat().st_size<=CACHE_BYTES and marker.is_file()and marker.stat().st_size<=1024
                and marker.read_text("ascii")==src.digest(path)+"  "+path.name+"\n","Actual whole completed-stage ZIP SHA sidecar")
            task=Path(destination)/(parents.slug(job_id)+"-restored-"+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(path)as z:
                members=cache_members(z);task.mkdir(parents=True,exist_ok=False)
                for row in members:
                    p=task.joinpath(*src.parts(row.filename));p.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(row)as source,p.open("xb")as target:shutil.copyfileobj(source,target,src.MIB)
            checked=evidence.validate_completed(task);src.need(checked["job_id"]==job_id,"No cross-job completed-stage substitution")
            if bindings:
                src.need(all(checked["summary"].get(k)==v for k,v in bindings.items()),"Exact current fresh upstream evidence, not another lineage")
            event(root,"finite69_caps_completed_stage_revalidated",job_id=job_id,cache=str(path),sha256=src.digest(path),numerical_replay_skipped=True)
            return task,checked,dict(path=str(path),sha256=src.digest(path))
        except Exception as error:event(root,"finite69_caps_cache_rejected",job_id=job_id,cache=str(path),error=type(error).__name__+": "+str(error))
    return None


def stage_record(root,task,checked,export,reused):
    return dict(job_id=checked["job_id"],task_relative=Path(task).relative_to(root).as_posix(),validated=checked,
        export=export,reused_completed_stage=reused)


def run_stages(root,durable_root,cache,status):
    root=Path(root);durable_root=Path(durable_root);initials={}
    old_cache=durable_root/"finite69-parents-initial7_9/completed"/ps.CATALOG_SHA256[:16]
    for job_id in src.catalog()["initial_job_ids"]:
        row=ps.job(job_id)
        hit=parents.restore_stage(old_cache/parents.slug(row["job_id"]),root/"jobs",row,log_root=root)
        if hit:task,checked,export=hit;reused=True
        else:
            task=root/"jobs"/(parents.slug(row["job_id"])+"-"+uuid.uuid4().hex[:8]);reused=False
            checked=parents.execute(task,row,cache,log_root=root);export=parents.save_stage(task,old_cache/parents.slug(row["job_id"]))
        initials[row["job_id"]]=(task,checked)
        status["jobs"].append(stage_record(root,task,checked,export,reused));atomic_json(root/"SESSION_RESULT.json",status)
        event(root,"finite69_caps_batch_progress",completed_stages=len(status["jobs"]),total_stages=19,job_id=row["job_id"])
    completed=durable_root/"finite69-caps/completed"/src.CATALOG_SHA256[:16]
    hit=restore_stage(completed/"owncaps6_9",root/"jobs","owncaps6_9",root=root)
    if hit:own,own_checked,export=hit;reused=True
    else:
        own=root/"jobs"/("owncaps6_9-"+uuid.uuid4().hex[:8]);src.prepare_own(cache,own)
        own_checked=execute_prepared(own,root=root);export=save_stage(own,completed/"owncaps6_9");reused=False
    status["jobs"].append(stage_record(root,own,own_checked,export,reused));atomic_json(root/"SESSION_RESULT.json",status)
    for row in src.resource_rows():
        initial_id=row["job_id"].replace(".resource.",".initial.");initial,initial_checked=initials[initial_id]
        bindings=dict(fresh_initial_stage_sha256=initial_checked["stage_result_sha256"],fresh_caps_stage_sha256=own_checked["stage_result_sha256"])
        hit=restore_stage(completed/parents.slug(row["job_id"]),root/"jobs",row["job_id"],root=root,bindings=bindings)
        if hit:task,checked,export=hit;reused=True
        else:
            task=root/"jobs"/(parents.slug(row["job_id"])+"-"+uuid.uuid4().hex[:8]);reused=False
            src.prepare_resource(cache,task,row,initial,own);checked=execute_prepared(task,root=root)
            export=save_stage(task,completed/parents.slug(row["job_id"]))
        status["jobs"].append(stage_record(root,task,checked,export,reused));atomic_json(root/"SESSION_RESULT.json",status)
        event(root,"finite69_caps_batch_progress",completed_stages=len(status["jobs"]),total_stages=19,job_id=row["job_id"])
    src.need(len(status["jobs"])==19,"Nine INITIAL, one complete owncaps transaction, nine resource stages")


def run_colab(*,durable_root,work_root="/content/berry-esseen-runs",archives="/content/berry-esseen-archives",backup_interval=60):
    from .environment import snapshot
    src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=3600,"Bounded live backup interval")
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
    root=Path(work_root).resolve()/"finite69-caps"/stamp;root.mkdir(parents=True,exist_ok=False)
    durable=Path(durable_root).resolve()/"finite69-caps"/stamp
    status=dict(schema="CONDITIONAL_FINITE69_CAPS_BATCH_V1",state="started",started_utc=utc(),jobs=[],
        catalog_sha256=src.CATALOG_SHA256,expected_stages=19,expected_native_actions=23,
        cpu_seconds=evidence.CPU,wall_seconds=evidence.WALL,memory_bytes=evidence.MEMORY,disk_bytes=evidence.DISK,
        conditional_premises=["Attained-witness and sharp minimal-counterexample framework",
            "Same-witness absolute support on the literal closed bands",
            "Kappa62/625 and the Fourier analytic framework; inherited kappa run files remain conditional inputs",
            "Remaining count, regional and all-index semantic joins"],
        conditional_arithmetic_completed=False,**{f:False for f in evidence.FLAGS})
    atomic_json(root/"ENVIRONMENT.json",snapshot());atomic_json(root/"SESSION_RESULT.json",status)
    backups=parents.LogBackups(root,durable,backup_interval);backups.start()
    try:
        event(root,"finite69_caps_batch_started",native_actions=23,completed_stage_reuse=True,partial_numerical_resume=False,
            cpu_seconds=evidence.CPU,wall_seconds=evidence.WALL,memory_bytes=evidence.MEMORY,scope=evidence.SCOPE,
            planner_dependency="NumPy for untrusted discovery; exact acceptance sources unchanged")
        status["numpy_context"]=numpy_context();atomic_json(root/"SESSION_RESULT.json",status)
        event(root,"finite69_caps_discovery_dependency",**status["numpy_context"])
        assets=src.obtain_assets(archives,progress=lambda name,**fields:event(root,name,**fields))
        cache=src.prepare_cache(assets,Path(work_root).resolve()/"finite69-caps-source-cache"/src.CATALOG_SHA256[:16],
            progress=lambda name,**fields:event(root,name,**fields))
        run_stages(root,durable_root,cache,status)
        status.update(state="complete_selected_conditional_caps_resource_arithmetic_basic",conditional_arithmetic_completed=True,finished_utc=utc())
        atomic_json(root/"SESSION_RESULT.json",status)
        validated=evidence.validate_batch(root)
        atomic_json(root/"BATCH_VALIDATED.json",validated)
    except BaseException as error:
        status.update(state="incomplete_selected_conditional_caps_resource_arithmetic",conditional_arithmetic_completed=False,
                      error=type(error).__name__+": "+str(error),finished_utc=utc())
        (root/"ERROR.txt").write_text(traceback.format_exc(),encoding="utf-8")
        event(root,"finite69_caps_incomplete",completed_stages=len(status["jobs"]),error=status["error"],all_index_conclusion_verified=False)
    finally:
        status.setdefault("finished_utc",utc());atomic_json(root/"SESSION_RESULT.json",status)
        try:backups.close()
        except Exception as error:
            status.update(state="incomplete_backup_shutdown",conditional_arithmetic_completed=False,backup_error=str(error));atomic_json(root/"SESSION_RESULT.json",status)
        archive=bundle(root,durable)
    print("FINITE6--9 CAPS RESULT:",status["state"],"\nZIP:",archive,flush=True)
    return dict(status=status,bundle=str(archive.resolve()),work=str(root.resolve()))
