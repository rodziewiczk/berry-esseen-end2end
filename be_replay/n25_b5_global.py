"""Resumable complete-stage Colab acquisition of the two lower-B5 global parents."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import shutil
import stat
import sys
import traceback
import uuid
import zipfile
import zlib

from . import aux24_evidence as paths, count_task as common
from . import n25_b5_global_sources as sources, n25_b5_global_evidence as evidence
from .colab_batch import atomic_json, event, utc, bundle

MIB = 1024**2
need = sources.need


def cache_files(task, branch, count):
    task = Path(task)
    names = {sources.source.MANIFEST, sources.source.TASK}
    for name in sources.selected(branch):
        names.add("source/"+name)
        names.add("epoch/"+name)
    prefix = "epoch/"+sources.source.PREFIX
    names.update(prefix+name for name in evidence.outputs(branch, count))
    for stage in sources.stages(branch)[:count]:
        names.add("ledgers/"+stage["name"]+".json")
        names.update("execution/"+stage["name"]+"/"+filename for filename in
                     ("launch.json", "supervisor-result.json", "stdout.txt", "stderr.txt"))
    return sorted(names)


def save_prefix(task, branch, count, destination):
    evidence.validate_prefix(task, branch, count)
    task, destination = Path(task).resolve(), Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    manifest = dict(schema="N25_B5_GLOBAL_COMPLETED_PREFIX_ZIP_V1", branch=branch, completed=count,
                    implementation=evidence.implementation(), files={})
    for name in cache_files(task, branch, count):
        path = paths.inside(task, name)
        need(path.stat().st_size <= 128*MIB, "Bounded completed prefix artifact")
        manifest["files"][name] = dict(bytes=path.stat().st_size, sha256=common.digest(path))
    need(sum(r["bytes"] for r in manifest["files"].values()) <= 512*MIB, "Bounded complete prefix expansion")
    name = f'{branch}-{count}-'+uuid.uuid4().hex+".zip"
    temporary = destination/(name+".pending")
    with zipfile.ZipFile(temporary, "x", compression=zipfile.ZIP_DEFLATED, strict_timestamps=False) as archive:
        import json
        archive.writestr("COMPLETED_PREFIX.json", json.dumps(manifest, sort_keys=True, indent=2)+"\n")
        for relative in manifest["files"]:
            archive.write(task/relative, relative)
    output = destination/name
    temporary.replace(output)
    sidecar = output.with_suffix(".zip.sha256")
    temporary_sidecar = sidecar.with_suffix(".pending")
    temporary_sidecar.write_text(common.digest(output)+"  "+output.name+"\n", encoding="ascii")
    temporary_sidecar.replace(sidecar)
    return output


def restore_prefix(archive_path, task, branch, count):
    """Safe bounded transport followed by complete unchanged evidence readback."""
    import json
    archive_path, task = Path(archive_path), Path(task)
    need(not task.exists() and not task.is_symlink(), "New exact prefix restore destination")
    need(archive_path.is_file() and not archive_path.is_symlink() and archive_path.stat().st_size <= 512*MIB,
         "Bounded ordinary completed prefix ZIP")
    sidecar = archive_path.with_suffix(".zip.sha256")
    need(sidecar.is_file() and not sidecar.is_symlink() and sidecar.stat().st_size < 4096
         and sidecar.read_text("ascii").split() == [common.digest(archive_path), archive_path.name],
         "Exact complete prefix ZIP sidecar")
    expected = set(cache_files(task, branch, count))
    with zipfile.ZipFile(archive_path) as archive:
        infos = archive.infolist()
        names = [row.filename for row in infos]
        need(len(names) <= 2048 and len(set(n.casefold() for n in names)) == len(names)
             and set(names) == expected | {"COMPLETED_PREFIX.json"}, "Exact unique completed prefix member set")
        need(sum(row.file_size for row in infos) <= 512*MIB, "Bounded declared prefix expansion")
        for row in infos:
            sources.source._name(row.filename, full=False)
            need(not row.is_dir() and not row.flag_bits & 1
                 and stat.S_IFMT(row.external_attr >> 16) in (0, stat.S_IFREG)
                 and 0 <= row.file_size <= 128*MIB, "Ordinary bounded unencrypted prefix member")
        info = archive.getinfo("COMPLETED_PREFIX.json")
        need(info.file_size <= 4*MIB, "Bounded prefix manifest")
        packet = json.loads(archive.read(info), object_pairs_hook=common.unique)
        need(set(packet) == {"schema", "branch", "completed", "implementation", "files"}
             and packet["schema"] == "N25_B5_GLOBAL_COMPLETED_PREFIX_ZIP_V1" and packet["branch"] == branch
             and type(packet["completed"]) is int and packet["completed"] == count
             and paths.same(packet["implementation"], evidence.implementation())
             and set(packet["files"]) == expected, "Exact current branch/prefix/runtime identity")
        # Check every decompressed byte before creating the destination.
        for name, row in packet["files"].items():
            info = archive.getinfo(name)
            need(set(row) == {"bytes", "sha256"} and type(row["bytes"]) is int
                 and row["bytes"] == info.file_size, "Exact serialized prefix member length")
            h, size = hashlib.sha256(), 0
            with archive.open(info) as stream:
                for block in iter(lambda: stream.read(MIB), b""):
                    size += len(block)
                    need(size <= row["bytes"], "No oversized member read")
                    h.update(block)
            need(size == row["bytes"] and h.hexdigest() == row["sha256"], "Exact complete prefix member digest")
        task.mkdir(parents=True)
        for name in packet["files"]:
            target = task/paths.relative(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name) as incoming, target.open("xb") as outgoing:
                shutil.copyfileobj(incoming, outgoing, MIB)
    # All old absolute paths remain unchanged in records and are mapped by each
    # stage's original_task_root. Timed parent receipts are never rewritten.
    evidence.validate_prefix(task, branch, count)
    return count


def execute(task, branch, position, *, log_root=None, supervise=None):
    from .small_indices import FollowOutput, Progress
    task = Path(task).resolve()
    stages = sources.stages(branch)
    need(type(position) is int and 0 <= position < len(stages), "One next complete stage")
    evidence.validate_prefix(task, branch, position)
    stage = stages[position]
    folder = evidence.root(task)/stage["folder"]
    command = [sys.executable, "-B", "-S", str(folder/stage["script"]), *stage["args"]]
    out = task/"execution"/stage["name"]
    need(not out.exists(), "Fresh isolated stage execution")
    previous = {"ledgers/"+s["name"]+".json": common.digest(task/"ledgers"/(s["name"]+".json"))
                for s in stages[:position]}
    # Python3.12 diagnoses inherited prose escape sequences. This only disables
    # that syntax warning; no arithmetic assertion or runtime warning is removed.
    old = os.environ.get("PYTHONWARNINGS")
    policy = "ignore:invalid escape sequence:SyntaxWarning"
    os.environ["PYTHONWARNINGS"] = (old+"," if old else "")+policy
    progress = Progress(task/(stage["name"]+"-stdout-progress.jsonl"))
    try:
        with FollowOutput("n25-"+branch+"-"+stage["name"], out/"stdout.txt", progress, 20):
            observed = (supervise or common.supervise)(command, cwd=folder, output_dir=out,
                mode="untrusted_search", wall_seconds=evidence.WALL, cpu_seconds=evidence.CPU,
                memory_bytes=evidence.MEMORY, disk_bytes=evidence.DISK, log_bytes=16*MIB,
                checkpoint_paths=[], heartbeat_seconds=20.)
    finally:
        progress.close()
        if old is None:
            os.environ.pop("PYTHONWARNINGS", None)
        else:
            os.environ["PYTHONWARNINGS"] = old
    report = dict(schema="N25_B5_GLOBAL_BASIC_STAGE_V1", branch=branch, stage=stage,
        original_task_root=str(task), implementation=evidence.implementation(),
        preceding_ledger_sha256=previous, source_manifest_sha256=sources.selection_sha(branch),
        observed=observed, warning_policy=policy, native_arithmetic_accepted=False,
        all_index_conclusion_verified=False)
    evidence.verify_epoch(task, branch, position+1)
    evidence.transport(task, branch, stage, report)
    report["validated_artifact"] = evidence.artifact(task, branch, stage)
    atomic_json(task/"ledgers"/(stage["name"]+".json"), report)
    return evidence.validate_prefix(task, branch, position+1)


def run_colab(*, durable_root, work_root="/content/berry-esseen-runs",
              archives="/content/berry-esseen-archives", backup_interval=60):
    from .environment import snapshot
    branch = "b5"
    from .retained_n25 import LogBackups
    class AcquisitionLogs(LogBackups):
        def save(self):
            copied = super().save()
            with self.lock:
                selected = list(self.active.glob("*")) if self.active is not None else []
                selected += list((self.root/"task").glob("*-stdout-progress.jsonl"))
                for path in selected:
                    if not path.is_file() or path.is_symlink() or path.stat().st_size > 16*MIB:
                        continue
                    try:
                        before = path.stat()
                        raw = path.read_bytes()
                        after = path.stat()
                        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                            continue
                        target = self.destination/"live"/path.relative_to(self.root)
                        target.parent.mkdir(parents=True, exist_ok=True)
                        temporary = target.with_name(target.name+".pending")
                        temporary.write_bytes(raw)
                        temporary.replace(target)
                        copied += 1
                    except FileNotFoundError:
                        continue
            return copied
    need(sys.platform.startswith("linux"), "Original numerical actions run only on Linux Colab")
    need(type(backup_interval) in (int, float) and 1 <= backup_interval <= 3600,
         "Finite bounded live-log backup interval")
    stages = sources.stages(branch)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
    root = Path(work_root).resolve()/("n25-global-parents-"+branch)/stamp
    root.mkdir(parents=True, exist_ok=False)
    durable_branch = Path(durable_root)/("n25-global-parents-"+branch)
    durable = durable_branch/"runs"/stamp
    task = root/"task"
    status = dict(schema="N25_B5_GLOBAL_BATCH_V1", branch=branch, n=25, contact_allowance="5/16", state="started",
        completed_actions=0, selected_actions=len(stages), reused_actions=0,
        conditional_parent_arithmetic_replayed=False, resource_interfaces_verified=False,
        native_arithmetic_accepted=False, stronger24_premise_acquired=False,
        count_forests_accepted=False, full_n25_verified=False, all_index_conclusion_verified=False,
        cpu_seconds_per_action=evidence.CPU, wall_seconds_per_action=evidence.WALL,
        memory_bytes=evidence.MEMORY)
    atomic_json(root/"ENVIRONMENT.json", snapshot())
    atomic_json(root/"SESSION_RESULT.json", status)
    monitor = AcquisitionLogs(root, durable, backup_interval)
    monitor.start()
    try:
        event(root, "n25_parent_acquisition_started", branch=branch, actions=len(stages),
              cpu_seconds_per_action=evidence.CPU, wall_seconds_per_action=evidence.WALL,
              memory_bytes=evidence.MEMORY)
        # Prefer the largest valid completed prefix. Corrupt/incompatible bundles
        # are retained on Drive and reported; they never become partial proofs.
        completed = 0
        cache = durable_branch/"completed"
        for count in range(len(stages), 0, -1):
            candidates = sorted(cache.glob(f'{branch}-{count}-*.zip'))
            if len(candidates) > 1:
                event(root, "multiple_completed_prefixes", completed=count, copies=len(candidates))
            for candidate in candidates:
                restored = root/("restore-"+uuid.uuid4().hex[:12])
                try:
                    restore_prefix(candidate, restored, branch, count)
                except (ValueError, OSError, KeyError, zipfile.BadZipFile, RuntimeError, EOFError, zlib.error) as error:
                    event(root, "completed_prefix_rejected", archive=str(candidate), reason=str(error))
                    continue
                restored.rename(task)
                completed = count
                status.update(completed_actions=count, reused_actions=count)
                event(root, "completed_prefix_revalidated", actions=count, archive=str(candidate))
                break
            if completed:
                break
        if not completed:
            sources.prepare(task, branch, archives=archives, download=True, progress=root)
            shutil.copytree(sources.source.source_root(task), evidence.root(task))
        for position in range(completed, len(stages)):
            event(root, "n25_parent_action_started", action=stages[position]["name"], position=position+1, total=len(stages))
            monitor.set_active(task/"execution"/stages[position]["name"])
            execute(task, branch, position, log_root=root)
            saved = save_prefix(task, branch, position+1, cache)
            status["completed_actions"] = position+1
            atomic_json(root/"SESSION_RESULT.json", status)
            event(root, "n25_parent_action_completed", action=stages[position]["name"],
                  completed_actions=position+1, total=len(stages), cache=str(saved))
            monitor.set_active(None)
            monitor.save()
        checked = evidence.validate_completed(task)
        atomic_json(task/"PARENT_RESULT.json", checked)
        status.update(state="conditional_global_parent_arithmetic_complete",
                      conditional_parent_arithmetic_replayed=True)

    except BaseException as error:
        status.update(state="incomplete_error", error=type(error).__name__+": "+str(error))
        (root/"ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        event(root, "incomplete_error", error=status["error"], completed_actions=status["completed_actions"])
    finally:
        status["finished_utc"] = utc()
        atomic_json(root/"SESSION_RESULT.json", status)
        try:
            monitor.close()
        except Exception as error:
            event(root, "final_log_backup_failed", error=str(error))
        output = bundle(root, durable)
        event(root, "results_bundle_saved", path=str(output), state=status["state"], all_index_conclusion_verified=False)
    print("\nRESULT:", status["state"], "\nZIP:", output, flush=True)
    return dict(status=status, bundle=str(output), work=str(root))
