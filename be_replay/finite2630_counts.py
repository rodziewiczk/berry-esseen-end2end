"""Full selected finite26--30 COUNT arithmetic, with revalidated completed-job reuse.

This new Linux execution protocol preserves the original numerical sources and
all selected native controls. BASIC arithmetic is conditional evidence, never
an acquired finite-index theorem. No partial numerical computation is resumed.
"""
from __future__ import annotations
from datetime import datetime,timezone
import json
from pathlib import Path
import re
import shutil
import stat
import sys
import threading
import time
import traceback
import uuid
import zipfile

from . import linux_supervisor, finite2630_sources as src, finite2630_evidence as evidence
from . import n27_p41_recovery as recovery
from .colab_batch import atomic_json,bundle,event,utc

CPU_SECONDS=43200
WALL_SECONDS=54000
MEMORY_BYTES=2048*src.MIB
CACHE_BYTES=512*src.MIB
CACHE_FILES=10000


def slug(job_id):
    src.need(re.fullmatch(r"[A-Za-z0-9.-]+",job_id)is not None,"Catalog job identifier")
    return job_id.lower().replace(".","-")


class Follow:
    def __init__(self,root,task,row):
        self.root,self.task,self.row=Path(root),Path(task),row
        self.stop=threading.Event();self.thread=threading.Thread(target=self.follow,daemon=True)
    def follow(self):
        started=time.monotonic();last=-20;position=0;partial=b""
        while True:
            path=self.task/"execution/stdout.txt"
            try:
                with path.open("rb")as stream:stream.seek(position);block=stream.read(src.MIB)
                position+=len(block);lines=(partial+block).split(b"\n");partial=lines.pop()
                for line in lines:
                    event(self.root,"finite2630_count_original_stdout",job_id=self.row["job_id"],
                          line=line.decode("utf-8",errors="replace")[:4096])
            except FileNotFoundError:pass
            elapsed=time.monotonic()-started
            if elapsed-last>=20:
                event(self.root,"finite2630_count_job_heartbeat",job_id=self.row["job_id"],family=self.row["family"],
                      elapsed_seconds=elapsed,observed_stdout_bytes=position,
                      conditional_arithmetic_completed=False,full_finite1039_verified=False)
                last=elapsed
            if self.stop.wait(.2):
                if getattr(self,"draining",False):break
                self.draining=True
    def __enter__(self):self.thread.start();return self
    def __exit__(self,*unused):
        self.stop.set();self.thread.join(timeout=5);src.need(not self.thread.is_alive(),"Stopped progress observer")


def execute(task,row,cache, *, log_root=None):
    src.need(sys.platform=="linux","The new process-group resource epoch requires Linux")
    task=Path(task).resolve();request=src.prepare_job(row["job_id"],cache,task)
    # Stage artifacts are sealed at completion; batch progress belongs outside
    # the stage so later log lines cannot invalidate its exported inventory.
    root=task.parent if log_root is None else Path(log_root)
    event(root,"finite2630_count_full_job_started",job_id=row["job_id"],family=row["family"],
          cpu_seconds=CPU_SECONDS,wall_seconds=WALL_SECONDS,memory_bytes=MEMORY_BYTES,
          resource_policy=evidence.SCOPE,
          partial_numerical_resume=False,native_arithmetic_accepted=False)
    with Follow(root,task,row):
        observed=linux_supervisor.run(evidence.command(request,row,sys.executable),cwd=task/"capsule"/row["directory"],
            output_dir=task/"execution",mode="untrusted_search",cpu_seconds=CPU_SECONDS,
            wall_seconds=WALL_SECONDS,memory_bytes=MEMORY_BYTES,checkpoint_paths=[task/"capsule"/src.output_relative(row)],disk_bytes=512*src.MIB,
            log_bytes=16*src.MIB,heartbeat_seconds=20)
    report=dict(schema=evidence.OBSERVED,scope=evidence.SCOPE,job_id=row["job_id"],
        original_task_root=request["original_task_root"],implementation=evidence.implementation(),
        python_executable=sys.executable,python_version=sys.version,
        cpu_seconds=CPU_SECONDS,wall_seconds=WALL_SECONDS,memory_bytes=MEMORY_BYTES,observed=observed,
        conditional_arithmetic_completed=False,native_arithmetic_accepted=False,
        parent_acquisitions_verified=False,fresh_parent_fact_joins_verified=False,full_finite1039_verified=False,all_index_conclusion_verified=False)
    atomic_json(task/"STAGE_OBSERVED.json",report)
    try:summary=evidence.validate_run(task,row,report)
    except BaseException as error:
        details=failure_details(task,observed)
        details["validation_error"]=type(error).__name__+": "+str(error)[:2048]
        event(root,"finite2630_count_original_job_incomplete",job_id=row["job_id"],**details)
        raise ValueError("Original selected finite26--30 COUNT job did not validate: "+details["validation_error"]+
                         "; supervisor reason: "+str(observed.get("reason"))+
                         "; stderr tail: "+details["stderr_tail"])
    complete=dict(schema=evidence.COMPLETED,scope=evidence.SCOPE,job_id=row["job_id"],
        implementation=evidence.implementation(),observed_sha256=src.digest(task/"STAGE_OBSERVED.json"),
        summary=summary,artifacts=evidence.inventory(task),conditional_arithmetic_completed=True,
        native_arithmetic_accepted=False,parent_acquisitions_verified=False,fresh_parent_fact_joins_verified=False,
        full_finite1039_verified=False,all_index_conclusion_verified=False)
    atomic_json(task/"STAGE_COMPLETED.json",complete)
    checked=evidence.validate_completed(task)
    event(root,"finite2630_count_full_job_completed",job_id=row["job_id"],family=row["family"],summary=summary,
          native_arithmetic_accepted=False,full_finite1039_verified=False)
    return checked


def failure_details(task,observed):
    """Surface bounded actual diagnostics; these bytes never accept a stage."""
    result=dict(status=observed.get("status"),reason=observed.get("reason"),returncode=observed.get("returncode"),
                resource_policy=evidence.SCOPE,conditional_arithmetic_completed=False,full_finite1039_verified=False)
    for kind in("stdout","stderr"):
        path=Path(task)/"execution"/(kind+".txt")
        try:
            src.ordinary(path)
            if not path.is_file()or path.stat().st_size>16*src.MIB:raise ValueError("No bounded ordinary capture")
            with path.open("rb")as stream:
                stream.seek(max(0,path.stat().st_size-4096));raw=stream.read(4096)
            result[kind+"_tail"]=raw.decode("utf-8",errors="replace")
            result[kind+"_actual_sha256"]=src.digest(path)
            result[kind+"_supervisor_hash_matches"]=result[kind+"_actual_sha256"]==observed.get(kind+"_sha256")
        except Exception as error:result[kind+"_tail"]="[capture unavailable: "+type(error).__name__+"]"
    return result


def cache_members(z):
    rows=z.infolist();src.need(0<len(rows)<=CACHE_FILES,"Bounded completed-stage ZIP inventory")
    names=set();folded=set();total=0
    for row in rows:
        src.parts(row.filename);mode=row.external_attr>>16
        src.need(not row.is_dir()and not row.flag_bits&1 and not stat.S_ISLNK(mode)
                 and stat.S_IFMT(mode)in(0,stat.S_IFREG)and row.filename not in names
                 and row.filename.casefold()not in folded and 0<=row.file_size<=128*src.MIB,
                 "Unique ordinary nonlinked bounded stage ZIP member")
        names.add(row.filename);folded.add(row.filename.casefold());total+=row.file_size
    src.need(total<=CACHE_BYTES and {"SOURCES.json","STAGE_OBSERVED.json","STAGE_COMPLETED.json",
             "execution/launch.json","execution/supervisor-result.json","execution/stdout.txt","execution/stderr.txt"}<=names,
             "Complete source/observed/completed/launch/capture stage evidence")
    return rows


def save_stage(task,cache):
    task=Path(task).resolve();checked=evidence.validate_completed(task);cache=src.ordinary(cache)
    cache.mkdir(parents=True,exist_ok=True)
    name=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]+"-complete.zip"
    output=cache/name;temporary=cache/(name+".pending")
    with zipfile.ZipFile(temporary,"x",compression=zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
        for path in sorted(task.rglob("*")):
            src.ordinary(path)
            if path.is_file():z.write(path,path.relative_to(task).as_posix())
        cache_members(z)
    src.need(temporary.stat().st_size<=CACHE_BYTES,"Bounded completed-stage ZIP")
    pin=src.digest(temporary);temporary.replace(output)
    marker=output.with_suffix(".zip.sha256");pending=marker.with_name(marker.name+".pending")
    pending.write_text(pin+"  "+output.name+"\n",encoding="ascii");pending.replace(marker)
    return dict(path=str(output),sha256=pin,stage_result_sha256=checked["stage_result_sha256"])


def restore_stage(cache,destination,row, *, log_root=None):
    cache=src.ordinary(cache);destination=Path(destination)
    if not cache.exists():return None
    src.need(cache.is_dir(),"Ordinary selected completed-stage cache")
    # Bound advisory cache work; older cache files are preserved, not deleted.
    candidates=sorted(cache.glob("*-complete.zip"),reverse=True)[:8]
    for path in candidates:
        try:
            src.ordinary(path);marker=src.ordinary(path.with_suffix(".zip.sha256"))
            src.need(path.is_file()and path.stat().st_size<=CACHE_BYTES and marker.is_file()
                     and marker.stat().st_size<=1024 and marker.read_text("ascii")==src.digest(path)+"  "+path.name+"\n",
                     "Actual completed-stage ZIP SHA sidecar")
            restored=destination/(slug(row["job_id"])+"-restored-"+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(path)as z:
                rows=cache_members(z);restored.mkdir(parents=True,exist_ok=False)
                for member in rows:
                    output=restored.joinpath(*src.parts(member.filename));output.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(member)as source,output.open("xb")as target:shutil.copyfileobj(source,target,src.MIB)
            src.need(src.read(restored/"SOURCES.json")["job_id"]==row["job_id"],"No cross-job cache substitution")
            checked=evidence.validate_completed(restored)
            src.need(checked["job_id"]==row["job_id"],"Exact selected completed job")
            if log_root:event(log_root,"finite2630_count_completed_job_revalidated",job_id=row["job_id"],cache=str(path),
                              sha256=src.digest(path),summary=checked["summary"],numerical_replay_skipped=True)
            return restored,checked,dict(path=str(path),sha256=src.digest(path))
        except Exception as error:
            if log_root:event(log_root,"finite2630_count_completed_cache_rejected",job_id=row["job_id"],cache=str(path),
                              error=type(error).__name__+": "+str(error))
    return None


class LogBackups:
    """Minute logs/ledgers; complete stage ZIPs are exported only after checking."""
    def __init__(self,root,durable,interval):
        self.root,self.durable=Path(root),Path(durable);self.interval=interval
        self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True);self.error=None
    def copy(self):
        for path in self.root.rglob("*"):
            if not path.is_file():continue
            rel=path.relative_to(self.root).as_posix()
            selected=("/capsule/"not in rel and (path.suffix in(".json",".jsonl",".txt")or path.name=="ERROR.txt"))
            if not selected or path.stat().st_size>16*src.MIB:continue
            src.ordinary(path);target=self.durable/"live"/rel;target.parent.mkdir(parents=True,exist_ok=True)
            pending=target.with_name(target.name+".pending");shutil.copyfile(path,pending);pending.replace(target)
    def loop(self):
        while not self.stop.wait(self.interval):
            try:self.copy();event(self.root,"finite2630_count_live_backup_saved",completed_stage_ZIPs_are_separate=True)
            except Exception as error:self.error=str(error)
    def start(self):self.thread.start()
    def close(self):
        self.stop.set();self.thread.join(timeout=30);src.need(not self.thread.is_alive(),"Stopped bounded log backup")
        self.copy()


def batch_jobs(root,completed_cache,source_cache,status,rows):
    """Serial exact-job orchestration; public selection is fixed by run_colab."""
    for ordinal,row in enumerate(rows):
        cached=restore_stage(Path(completed_cache)/slug(row["job_id"]),Path(root)/"jobs",row,log_root=root)
        if cached:
            task,checked,export=cached;reused=True
        else:
            task=Path(root)/"jobs"/(slug(row["job_id"])+"-"+uuid.uuid4().hex[:8]);reused=False
            checked=execute(task,row,source_cache,log_root=root)
            export=save_stage(task,Path(completed_cache)/slug(row["job_id"]))
            event(root,"finite2630_count_completed_stage_ZIP_saved",job_id=row["job_id"],**export)
        status["jobs"].append(dict(job_id=row["job_id"],task_relative=task.relative_to(root).as_posix(),reused_completed_stage=reused,validated=checked,export=export))
        atomic_json(Path(root)/"SESSION_RESULT.json",status)
        event(root,"finite2630_count_batch_progress",completed_jobs=ordinal+1,total_jobs=len(rows),job_id=row["job_id"],
              reused_completed_stage=reused,full_finite1039_verified=False)
    src.need([r["job_id"]for r in status["jobs"]]==[r["job_id"]for r in rows],"No omitted selected arithmetic job")


def import_recovered_pair(durable_root,root):
    """Import a complete64 pair, preserving every recorded byte and context."""
    root=Path(root);cache=Path(durable_root).resolve()/'n27-p41-recovery/completed'/recovery.src.PLAN_SHA256[:16]
    loaded=recovery.restore_completed(cache,root/'recovered64',log_root=root)
    src.need(loaded is not None,'WAITING: a fully validated notebook64 completed-pair cache is required; run64 with the same Drive root')
    task,checked,export=loaded
    original=src.ordinary(Path(export['path']));src.need(src.digest(original)==export['sha256'],'Actual independently validated64 cache ZIP')
    local=root/'recovered64/SOURCE_PAIR.zip';shutil.copyfile(original,local)
    src.need(src.digest(local)==export['sha256'],'Lossless complete64 export import')
    record=dict(schema='IMPORTED_FULL_N27_P41_PAIR_FOR_FINITE2630_V1',selection_sha256=src.SELECTION_SHA256,
                task_relative=task.relative_to(root).as_posix(),source_zip_relative=local.relative_to(root).as_posix(),
                source_zip_sha256=export['sha256'],validated=checked,conditional_arithmetic_completed=False,
                **{f:False for f in evidence.FLAGS})
    atomic_json(root/'RECOVERED64.json',record);result=evidence.validate_recovered(root)
    event(root,'finite2630_full64_pair_independently_revalidated',**result)
    return result


def run_colab(*,durable_root,work_root='/content/berry-esseen-runs',archives='/content/berry-esseen-archives',backup_interval=60):
    """Exact recovered64 pair plus79 unchanged full acceptors; complete reuse only."""
    from .environment import snapshot
    src.selection();rows=src.jobs()
    src.need(type(backup_interval)in(int,float)and 1<=backup_interval<=3600,'Bounded live backup interval')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root=Path(work_root).resolve()/'finite2630-counts'/stamp;root.mkdir(parents=True,exist_ok=False)
    durable=Path(durable_root).resolve()/'finite2630-counts'/stamp
    completed_cache=Path(durable_root).resolve()/'finite2630-counts/completed'/src.SELECTION_SHA256[:16]
    status=dict(schema='CONDITIONAL_FINITE2630_COMPLETE_COUNT_BATCH_V1',state='started',started_utc=utc(),jobs=[],
                selection_sha256=src.SELECTION_SHA256,implementation=evidence.implementation(),
                expected_census=src.selection()['complete_census'],all_selected_arithmetic_completed=False,
                conditional_arithmetic_completed=False,partial_numerical_resume=False,**{f:False for f in evidence.FLAGS})
    atomic_json(root/'ENVIRONMENT.json',snapshot());atomic_json(root/'SESSION_RESULT.json',status)
    backups=LogBackups(root,durable,backup_interval);backups.start()
    try:
        event(root,'finite2630_batch_started',original_full_acceptors=79,independent_recovered_pair=1,
              cpu_seconds=CPU_SECONDS,wall_seconds=WALL_SECONDS,memory_bytes=MEMORY_BYTES,
              expected_census=status['expected_census'],resource_policy=evidence.SCOPE,
              parent_acquisitions_verified=False,all_index_conclusion_verified=False)
        status['recovered64']=import_recovered_pair(durable_root,root);atomic_json(root/'SESSION_RESULT.json',status)
        assets=src.obtain_assets(archives,progress=lambda name,**fields:event(root,name,**fields))
        source_cache=src.prepare_cache(assets,Path(work_root).resolve()/'finite2630-source-cache'/src.SELECTION_SHA256[:16],
                                       progress=lambda name,**fields:event(root,name,**fields))
        batch_jobs(root,completed_cache,source_cache,status,rows)
        status.update(state='complete_selected_conditional_count_arithmetic_basic',all_selected_arithmetic_completed=True,
                      conditional_arithmetic_completed=True,actual_census=src.selection()['complete_census'],finished_utc=utc())
        atomic_json(root/'SESSION_RESULT.json',status)
        checked=evidence.validate_batch(root);atomic_json(root/'BATCH_VALIDATED.json',checked)
        event(root,'finite2630_all80_full_replays_and_identity_edge_verified',actual_census=checked['actual_census'],
              conditional_arithmetic_completed=True,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    except BaseException as error:
        status.update(state='waiting_for_validated64'if str(error).startswith('WAITING:')else'incomplete_selected_count_arithmetic',
                      all_selected_arithmetic_completed=False,conditional_arithmetic_completed=False,
                      error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(),encoding='utf-8',newline='\n')
        event(root,'finite2630_incomplete',error=status['error'],completed_jobs=len(status['jobs']),
              conditional_arithmetic_completed=False,all_index_conclusion_verified=False)
    finally:
        # Keep the complete SESSION bytes stable after the full final validator.
        if status['conditional_arithmetic_completed']is not True:
            status['finished_utc']=utc();atomic_json(root/'SESSION_RESULT.json',status)
        try:backups.close()
        except Exception as error:event(root,'finite2630_live_backup_failed',error=str(error))
        archive=bundle(root,durable)
    print('SELECTED FINITE26--30 COUNT RESULT:',status['state'],'\nZIP:',archive,flush=True)
    return dict(status=status,bundle=str(archive.resolve()),work=str(root.resolve()))
