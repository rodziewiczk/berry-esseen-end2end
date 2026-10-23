"""Preconfigured Colab count jobs with visible progress and durable backups.

The batch driver never establishes the all-index theorem.  Live backups are
restart advice, not accepted proofs. Native acceptance remains a separate call.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import threading
import time
import traceback
import uuid
import zipfile

MIB = 1024**2

def utc():
    return datetime.now(timezone.utc).isoformat()

def atomic_json(path, packet):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".pending")
    with temporary.open("w", encoding="utf-8") as output:
        json.dump(packet, output, indent=2)
        output.write("\n")
    temporary.replace(path)

def event(root, name, **fields):
    row = dict(utc=utc(), event=name, **fields)
    with (Path(root)/"PROGRESS.jsonl").open("a", encoding="utf-8") as out:
        out.write(json.dumps(row, sort_keys=True) + "\n")
        out.flush()
    print("[" + row["utc"] + "] " + name + " " + json.dumps(fields, sort_keys=True), flush=True)
    return row

def live_backup(root, destination):
    """Copy only parseable JSON and ordinary evidence. No acceptance implied."""
    root, destination = Path(root), Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    copied, skipped = 0, []
    for original in sorted(root.rglob("*")):
        if original.is_symlink():
            raise ValueError("No symlinks in a checkpoint backup")
        if not original.is_file() or original.name.endswith(".pending"):
            continue
        if original.stat().st_size > 128*MIB:
            skipped.append(str(original.relative_to(root)))
            continue
        try:
            before = original.stat()
            raw = original.read_bytes()
            after = original.stat()
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                skipped.append(str(original.relative_to(root)))
                continue
            if original.suffix == ".json":
                json.loads(raw)
            target = destination/original.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(target.name + ".copying")
            temporary.write_bytes(raw)
            temporary.replace(target)
            os.utime(target, ns=(after.st_atime_ns, after.st_mtime_ns))
            copied += 1
        except (FileNotFoundError, json.JSONDecodeError, UnicodeError):
            skipped.append(str(original.relative_to(root)))
    atomic_json(destination/"LIVE_SNAPSHOT.json",
                dict(scope="LIVE_BACKUP_NOT_CERTIFICATE", utc=utc(),
                     copied=copied, skipped=skipped, all_index_conclusion_verified=False))
    return copied

class Backups:
    def __init__(self, root, destination, interval=60):
        self.root, self.destination, self.interval = Path(root), Path(destination), interval
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.worker = threading.Thread(target=self._run, daemon=True)
    def save(self):
        with self.lock:
            return live_backup(self.root, self.destination/"live")
    def _run(self):
        while not self.stop.wait(self.interval):
            try:
                copied = self.save()
                event(self.root, "backup_saved", files=copied)
            except Exception as error:
                event(self.root, "backup_failed", error=str(error))
    def start(self):
        self.worker.start()
    def close(self):
        self.stop.set()
        self.worker.join()
        self.save()

def latest_checkpoint(destination):
    candidates = []
    for pattern in ("CHECKPOINT.json", "CHECKPOINT.backup.json"):
        for path in Path(destination).rglob(pattern):
            if path.is_symlink() or not path.is_file() or path.stat().st_size > 128*MIB:
                continue
            try:
                packet = json.loads(path.read_text(encoding="utf-8"))
                if packet.get("schema") == "UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1":
                    candidates.append(path)
            except (OSError, ValueError, UnicodeError):
                continue
    return max(candidates, key=lambda p: p.stat().st_mtime_ns) if candidates else None

def bundle(root, destination):
    """Call only after native/search subprocesses and live backup have stopped."""
    root, destination = Path(root), Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    output = destination/(root.name + "-results.zip")
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED, strict_timestamps=False) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                raise ValueError("No symlink proof artifacts")
            if path.is_file():
                archive.write(path, str(Path(root.name)/path.relative_to(root)))
    digest = hashlib.sha256()
    with output.open("rb") as stream:
        for chunk in iter(lambda: stream.read(MIB), b""):
            digest.update(chunk)
    (output.with_suffix(".zip.sha256")).write_text(digest.hexdigest() + "  " + output.name + "\n", encoding="ascii")
    return output

def run_count(target, *, durable_root, work_root="/content/berry-esseen-runs",
              archives="/content/berry-esseen-archives", total_seconds=10800,
              slice_seconds=1800, backup_interval=60):
    from . import count_task
    from .environment import snapshot
    if target not in count_task.TARGETS:
        raise ValueError("Exactly one reviewed count target")
    if type(total_seconds) is not int or total_seconds < 1 or type(slice_seconds) is not int or not 1 <= slice_seconds <= 7200:
        raise ValueError("Positive total budget and bounded search slices")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    root = Path(work_root)/target/stamp
    root.mkdir(parents=True, exist_ok=False)
    durable = Path(durable_root)/target/stamp
    previous = latest_checkpoint(Path(durable_root)/target)
    status = dict(scope="COLAB_REGIONAL_COUNT_JOB_NOT_GLOBAL_PROOF", target=target,
                  started_utc=utc(), state="started", native_arithmetic_accepted=False,
                  parent_acquisitions_verified=False, all_index_conclusion_verified=False,
                  work=str(root), durable=str(durable), slices=[])
    atomic_json(root/"ENVIRONMENT.json", snapshot())
    atomic_json(root/"SESSION_RESULT.json", status)
    monitor = Backups(root, durable, interval=backup_interval)
    monitor.start()
    try:
        event(root, "prepare_started", target=target)
        count_task.prepare(target, Path(archives), root/"task", download=True)
        event(root, "prepare_finished", target=target)
        remaining, attempt = total_seconds, 0
        # The first short slice measures the actual host instead of estimating it.
        while remaining > 0:
            attempt += 1
            allotted = min(60 if attempt == 1 else slice_seconds, remaining)
            event(root, "search_started", slice=attempt, seconds=allotted,
                  remaining_allocated_seconds=remaining, resume=bool(previous))
            started = time.monotonic()
            result = count_task.search(root/"task", seconds=allotted, wall_seconds=allotted+120,
                                       resume=previous, published_hints=previous is None,
                                       archives=Path(archives), download=True)
            elapsed = time.monotonic()-started
            status["slices"].append(dict(slice=attempt, allotted_seconds=allotted,
                                        elapsed_seconds=elapsed, epoch=result["epoch"],
                                        observed_status=result["observed"]["status"],
                                        search_result=result.get("search_result")))
            atomic_json(root/"SESSION_RESULT.json", status)
            previous_path = latest_checkpoint(root/"task")
            if previous_path is not None:
                previous = previous_path
            packet = result.get("search_result") or {}
            event(root, "search_finished", slice=attempt, elapsed_seconds=round(elapsed, 3),
                  status=packet.get("status", result["observed"]["status"]),
                  nodes=packet.get("nodes"), leaves=packet.get("leaves"),
                  pending=packet.get("pending"), checkpoint=str(previous) if previous else None)
            monitor.save()
            candidate = Path(result["candidate"])
            if packet.get("status") == "CANDIDATE_COMPLETE_NOT_ACCEPTED" and candidate.is_file():
                event(root, "native_replay_started", candidate=str(candidate))
                accepted = count_task.accept(root/"task", candidate)
                if accepted.get("arithmetic_accepted") is not True:
                    raise ValueError("Native replay did not establish scoped arithmetic acceptance")
                status.update(state="regional_count_arithmetic_accepted",
                              native_arithmetic_accepted=True, native_result=accepted)
                event(root, "regional_count_arithmetic_accepted",
                      parent_acquisitions_verified=False, all_index_conclusion_verified=False)
                break
            if result["observed"]["status"] != "completed":
                status["state"] = "incomplete_guarded_stop"
                break
            remaining -= allotted
            status["state"] = "candidate_incomplete"
        else:
            status["state"] = "candidate_incomplete_budget_exhausted"
    except BaseException as error:
        status.update(state="incomplete_error", error=type(error).__name__ + ": " + str(error))
        (root/"ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        event(root, "incomplete_error", error=status["error"])
    finally:
        status["finished_utc"] = utc()
        atomic_json(root/"SESSION_RESULT.json", status)
        try:
            monitor.close()
        except Exception as error:
            event(root, "final_backup_failed", error=str(error))
        output = bundle(root, durable)
        event(root, "results_bundle_saved", path=str(output), state=status["state"],
              all_index_conclusion_verified=False)
    print("\nRESULT:", status["state"], "\nZIP:", output, flush=True)
    return dict(status=status, bundle=str(output), work=str(root))
