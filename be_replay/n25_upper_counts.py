"""Colab batches for 10 additional retained B3/B4/B5/middle/upper forests, with verified stage reuse.

Only the supervised original acceptor performs numerical evaluation. Completed
stages are reusable only after full source/guard/capture/receipt revalidation.
Partial native acceptances have no internal resume and never become proofs.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import json
import re
import shutil
import stat
import sys
import threading
import traceback
import uuid
import zipfile

from . import count_task as common, n25_upper_counts_sources as sources
from . import n25_upper_counts_evidence as evidence
from .colab_batch import atomic_json, bundle, event, utc
from .delivery_transport import final_bundle

MIB = 1024**2
NATIVE_CPU_SECONDS = 82800
NATIVE_WALL_SECONDS = 82800
NATIVE_MEMORY_BYTES = 2048*MIB
MAX_CACHE_BYTES = 512*MIB
MAX_CACHE_FILES = 1024


def _ordinary(path):
    path = Path(path)
    common.need(not path.is_symlink() and not (
        hasattr(path, "is_junction") and path.is_junction()), "No linked evidence/cache paths")
    return path


def accept(task, job, *, on_epoch=None):
    """One complete fresh original accept; no old acceptance input is copied."""
    task = Path(task).resolve()
    manifest = sources.verify(task)
    row = next(r for r in manifest["jobs"] if r["job_id"] == job["job_id"])
    run = task/("accept-"+uuid.uuid4().hex[:12])
    capsule = run/"capsule"
    capsule.mkdir(parents=True, exist_ok=False)
    source = task/job["capsule_relative"]
    for item in row["files"]:
        shutil.copyfile(source/item["filename"], capsule/item["filename"])
    census = sources.census(job, capsule)
    if on_epoch:
        on_epoch(run)
    observed = common.supervise(
        [sys.executable, "-B", "-S", str(capsule/"count_protocol.py"), "accept"],
        cwd=capsule, output_dir=run/"execution", mode="trusted_native",
        cpu_seconds=NATIVE_CPU_SECONDS, wall_seconds=NATIVE_WALL_SECONDS,
        memory_bytes=NATIVE_MEMORY_BYTES, disk_bytes=256*MIB, log_bytes=16*MIB,
        checkpoint_paths=[])
    report = dict(schema=evidence.SCHEMA, job_id=job["job_id"], branch=job["branch"],
        index=job["index"], scope=evidence.SCOPE, epoch=str(run), observed=observed,
        census=census, implementation=evidence.implementation(), arithmetic_accepted=False,
        parent_acquisitions_verified=False, all_index_conclusion_verified=False)
    atomic_json(run/"NATIVE_OBSERVED.json", report)
    evidence.validate_run(task, job, run, observed, census)
    receipt = capsule/job["acceptance_filename"]
    report.update(arithmetic_accepted=True, native_receipt=str(receipt),
        native_receipt_sha256=common.digest(receipt), negative_controls=24,
        conditional_premises=evidence.premises(job))
    atomic_json(run/"NATIVE_ACCEPTED.json", report)
    return run, evidence.validate_stage(task, job, run)


def _cache_members(archive):
    """Preflight the entire untrusted ZIP before writing even its first member."""
    rows = archive.infolist()
    common.need(0 < len(rows) <= MAX_CACHE_FILES, "Bounded retained stage ZIP inventory")
    names, folded, epochs, total = set(), set(), set(), 0
    for row in rows:
        name = row.filename
        parts = name.split("/")
        mode = row.external_attr >> 16
        common.need(type(name) is str and "\\" not in name and ":" not in name
            and "\x00" not in name and not PurePosixPath(name).is_absolute()
            and all(p and p not in (".", "..") and p == p.rstrip(" .") for p in parts)
            and 2 <= len(parts) <= 3 and re.fullmatch(r"accept-[0-9a-f]{12,32}", parts[0])
            and name not in names and name.casefold() not in folded
            and not row.is_dir() and not row.flag_bits & 1
            and not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0, stat.S_IFREG)
            and 0 <= row.file_size <= 128*MIB, "Safe unique regular retained stage ZIP member")
        common.need((len(parts) == 2 and parts[1] in ("NATIVE_OBSERVED.json", "NATIVE_ACCEPTED.json"))
            or (len(parts) == 3 and parts[1] in ("capsule", "execution")),
            "Stage ZIP contains only its capsule, execution and two acceptance ledgers")
        names.add(name); folded.add(name.casefold()); epochs.add(parts[0])
        total += row.file_size
    common.need(len(epochs) == 1 and total <= MAX_CACHE_BYTES, "One bounded complete native epoch")
    epoch = next(iter(epochs))
    common.need({epoch+"/NATIVE_OBSERVED.json", epoch+"/NATIVE_ACCEPTED.json"} <= names,
                "Both original stage ledgers are present")
    return epoch, rows


def restore_stage(task, job, cache, *, log_root=None):
    """Treat Drive cache as untrusted until the entire completed stage passes."""
    task, cache = Path(task).resolve(), Path(cache)
    if not cache.exists():
        return None
    _ordinary(cache)
    common.need(cache.is_dir(), "Regular selected completed-stage cache")
    for path in sorted(cache.glob("accept-*-native.zip"), reverse=True):
        try:
            _ordinary(path)
            sidecar = _ordinary(path.with_suffix(".zip.sha256"))
            common.need(path.is_file() and path.stat().st_size <= MAX_CACHE_BYTES
                and sidecar.is_file() and sidecar.stat().st_size <= 1024,
                "Bounded completed stage ZIP and SHA sidecar")
            common.need(sidecar.read_text("ascii") == common.digest(path)+"  "+path.name+"\n",
                        "Actual complete stage ZIP hash")
            with zipfile.ZipFile(path) as archive:
                name, rows = _cache_members(archive)
                destination = task/name
                common.need(not destination.exists(), "Restore never overwrites an existing native epoch")
                destination.mkdir()
                for row in rows:
                    output = task/Path(*row.filename.split("/"))
                    output.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(row) as src, output.open("xb") as dst:
                        shutil.copyfileobj(src, dst, MIB)
            checked = evidence.validate_stage(task, job, destination)
            if log_root:
                event(log_root, "completed_stage_revalidated", job_id=job["job_id"],
                      cache=str(path), leaves=job["leaf_count"])
            return destination, checked
        except Exception as error:
            # A malformed cache may raise decompressor-specific exceptions.
            # It is advisory input; reject it and try another complete stage.
            # Interruptions remain outside this boundary (BaseException).
            if log_root:
                event(log_root, "completed_stage_cache_rejected", job_id=job["job_id"],
                      cache=str(path), error=type(error).__name__+": "+str(error))
    return None


def save_stage(task, job, epoch, cache):
    """Export only a stopped, fully validated complete native execution."""
    task, epoch, cache = Path(task).resolve(), Path(epoch).resolve(), Path(cache)
    evidence.validate_stage(task, job, epoch)
    _ordinary(cache)
    cache.mkdir(parents=True, exist_ok=True)
    output = cache/(epoch.name+"-native.zip")
    temporary = output.with_name(output.name+".pending-"+uuid.uuid4().hex[:8])
    common.need(not output.exists(), "Completed stage exports are append-only")
    with zipfile.ZipFile(temporary, "x", compression=zipfile.ZIP_DEFLATED, strict_timestamps=False) as archive:
        for path in sorted(epoch.rglob("*")):
            _ordinary(path)
            if path.is_file():
                archive.write(path, path.relative_to(task).as_posix())
        _cache_members(archive)
    common.need(temporary.stat().st_size <= MAX_CACHE_BYTES, "Bounded completed native stage export")
    pin = common.digest(temporary)
    temporary.replace(output)
    marker = output.with_suffix(".zip.sha256")
    marker_tmp = marker.with_name(marker.name+".pending")
    marker_tmp.write_text(pin+"  "+output.name+"\n", encoding="ascii")
    marker_tmp.replace(marker)
    return output


class LogBackups:
    """Minute-scale logs only; immutable inputs are reconstructed from their pins.

    Complete numerical work is independently saved by save_stage immediately.
    This avoids copying thousands of unchanged mathematical files every minute.
    """
    def __init__(self, root, destination, interval=60):
        self.root, self.destination, self.interval = Path(root), Path(destination), interval
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.active = None
        self.worker = threading.Thread(target=self._run, daemon=True)

    def set_active(self, epoch):
        with self.lock:
            self.active = Path(epoch) if epoch is not None else None

    def save(self):
        with self.lock:
            names = ["ENVIRONMENT.json", "SESSION_RESULT.json", "PROGRESS.jsonl", "ERROR.txt",
                     "task/SOURCES.json", "task/SOURCE_PREPARATION.json", "task/JOB_RESULT.json"]
            paths = [self.root/name for name in names]
            if self.active is not None:
                paths += list((self.active/"execution").glob("*"))
                paths += [self.active/"NATIVE_OBSERVED.json", self.active/"NATIVE_ACCEPTED.json"]
            copied = 0
            for path in paths:
                _ordinary(path)
                if not path.is_file() or path.stat().st_size > 16*MIB:
                    continue
                try:
                    before = path.stat()
                    raw = path.read_bytes()
                    after = path.stat()
                    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                        continue
                    if path.suffix == ".json":
                        json.loads(raw, object_pairs_hook=common.unique)
                    target = self.destination/"live"/path.relative_to(self.root)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    temporary = target.with_name(target.name+".pending")
                    temporary.write_bytes(raw)
                    temporary.replace(target)
                    copied += 1
                except (FileNotFoundError, ValueError, UnicodeError):
                    continue
            atomic_json(self.destination/"live/LIVE_SNAPSHOT.json", dict(
                scope="LIVE_LOG_BACKUP_NOT_CERTIFICATE", utc=utc(), copied=copied,
                all_index_conclusion_verified=False))
            return copied

    def _run(self):
        while not self.stop.wait(self.interval):
            try:
                event(self.root, "log_backup_saved", files=self.save())
            except Exception as error:
                event(self.root, "log_backup_failed", error=str(error))

    def start(self):
        self.worker.start()

    def close(self):
        self.stop.set()
        self.worker.join()
        self.save()


def run_colab(branch, *, durable_root, work_root="/content/berry-esseen-runs",
              archives="/content/berry-esseen-archives", backup_interval=60):
    from .environment import snapshot
    jobs = sources.jobs(branch)
    common.need(type(backup_interval) is int and 1 <= backup_interval <= 3600,
                "Bounded positive live-log backup interval")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
    root = Path(work_root).resolve()/("n25-upper10-"+branch)/stamp
    root.mkdir(parents=True, exist_ok=False)
    durable_branch = Path(durable_root)/("n25-upper10-"+branch)
    durable = durable_branch/"runs"/stamp
    task = root/"task"
    status = dict(schema="N25_ADDITIONAL_UPPER_COUNT_BATCH_EXECUTION_V1", branch=branch, scope=evidence.SCOPE,
        state="started", started_utc=utc(), selected_jobs=len(jobs),
        selected_leaves=sum(j["leaf_count"] for j in jobs), completed_jobs=0,
        completed_leaves=0, new_native_calls=0, reused_completed_stages=0, stages=[],
        native_arithmetic_accepted=False, parent_acquisitions_verified=False,
        full_n25_verified=False, all_index_conclusion_verified=False)
    atomic_json(root/"ENVIRONMENT.json", snapshot())
    atomic_json(root/"SESSION_RESULT.json", status)
    monitor = LogBackups(root, durable, backup_interval)
    monitor.start()
    try:
        event(root, "retained_n25_prepare_started", branch=branch, jobs=len(jobs),
              leaves=status["selected_leaves"], historical_acceptance_used=False)
        asset = common.obtain_asset(Path(archives), "old", download=True, progress=root)
        sources.prepare(branch, asset, task)
        sources.verify(task)
        for position, job in enumerate(jobs, 1):
            event(root, "retained_count_started", position=position, total=len(jobs),
                  job_id=job["job_id"], leaves=job["leaf_count"])
            cache = durable_branch/"completed"/job["job_id"]
            restored = restore_stage(task, job, cache, log_root=root)
            if restored is None:
                status["new_native_calls"] += 1
                atomic_json(root/"SESSION_RESULT.json", status)
                epoch, checked = accept(task, job, on_epoch=monitor.set_active)
                saved = save_stage(task, job, epoch, cache)
                event(root, "completed_stage_saved", job_id=job["job_id"], path=str(saved))
                reused = False
            else:
                epoch, checked = restored
                status["reused_completed_stages"] += 1
                reused = True
            monitor.set_active(None)
            status["stages"].append(dict(job_id=job["job_id"], epoch=epoch.name,
                                        reused=reused, evidence=checked))
            status["completed_jobs"] += 1
            status["completed_leaves"] += job["leaf_count"]
            atomic_json(task/"JOB_RESULT.json", status)
            atomic_json(root/"SESSION_RESULT.json", status)
            event(root, "retained_count_accepted", job_id=job["job_id"],
                  completed_jobs=status["completed_jobs"], total_jobs=len(jobs),
                  completed_leaves=status["completed_leaves"], negative_controls=24,
                  reused=reused, parent_acquisitions_verified=False,
                  all_index_conclusion_verified=False)
            monitor.save()
        sources.verify(task)
        for job, stage in zip(jobs, status["stages"]):
            evidence.validate_stage(task, job, task/stage["epoch"])
        status.update(state="selected_retained_count_arithmetic_accepted", native_arithmetic_accepted=True)
    except BaseException as error:
        status.update(state="incomplete_error", error=type(error).__name__+": "+str(error))
        (root/"ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        event(root, "incomplete_error", error=status["error"], completed_jobs=status["completed_jobs"])
    finally:
        status["finished_utc"] = utc()
        atomic_json(root/"SESSION_RESULT.json", status)
        if task.exists():
            atomic_json(task/"JOB_RESULT.json", status)
        try:
            monitor.close()
        except Exception as error:
            status.update(state="INCOMPLETE", synchronization_error=str(error))
            atomic_json(root/"SESSION_RESULT.json", status)
            event(root, "final_log_backup_failed", error=str(error))
        output = final_bundle(root, durable, Path(work_root)/"n25-upper10-local"/stamp, status)
        event(root, "results_bundle_saved", path=str(output), state=status["state"],
              completed_jobs=status["completed_jobs"], all_index_conclusion_verified=False)
    print("\nRESULT:", status["state"], "\nZIP:", output, flush=True)
    return dict(status=status, bundle=str(output), work=str(root))
