"""Fresh full n2/n3 arithmetic from frozen portable kernels.

Basic mode really runs the checkers, including fresh n3 C++ compilation, but
its weak process-group guard cannot produce trusted certificate acceptance.
No historical PASS receipt is an input. Mathematical all-law reductions and
literature remain separate obligations even after native arithmetic accepts.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import sys
import threading
import time
import traceback
import uuid

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor/n2_n3_75a9470"
COMMIT = "75a94708872e2bc053f42a279559b23ed91e4402"
MANIFEST_SHA256 = "8ca0f5c30991b50c61fc998c7c873873c2ac7d2bde6611123ce74651e1a3c26b"
MIB = 1024 ** 2
STAGES = {
    "n2-scalars": {"script": "n2/tensor_certificate.py", "function": "verify_reductions",
                   "marker": "FRESH_SCALARS_COMPLETED n2-scalars verify_reductions"},
    "n2-primary": {"script": "n2/tensor_certificate.py", "args": ["check"],
                   "marker": "ACCEPTED_ALL_70_TENSOR_CELLS 35878 134", "cells": 70},
    "n2-independent": {"script": "n2/independent_integer_check.py", "args": [],
                       "marker": "ACCEPTED_ALL_70_BY_INDEPENDENT_INTEGER_CHECK 35878 18426 134",
                       "cells": 70},
    "n3-scalars": {"script": "n3/verify.py", "function": "analytic_constants",
                   "marker": "FRESH_SCALARS_COMPLETED n3-scalars analytic_constants"},
    "n3-identities": {"script": "n3/audit_initial_polynomials.py", "args": [],
                      "marker": "ACCEPTED_ALL_INITIAL_IDENTITIES cells=111 orthants=444 exact_grid_identities=95904"},
    "n3-full": {"script": "n3/verify.py", "args": [], "cells": 111,
                "marker": "ACCEPTED_FULL_N3 111 501156 219860 349",
                "requires_subprocesses": True},
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(MIB), b""):
            digest.update(block)
    return digest.hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result


def write_json(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def verify_vendor(directory=VENDOR):
    """Check every immutable source byte and the complete selected inventory."""
    directory = Path(directory).resolve()
    manifest_path = directory / "MANIFEST.json"
    need(not manifest_path.is_symlink() and sha(manifest_path) == MANIFEST_SHA256,
         "Pinned small-index manifest identity")
    data = json.loads(manifest_path.read_text("utf-8"), object_pairs_hook=unique)
    need(data["schema"] == "FROZEN_N2_N3_SOURCE_INVENTORY_V1" and data["commit"] == COMMIT,
         "Literal upstream small-index source epoch")
    need(data["certificate_counts"] == {"n2": 70, "n3": 111}, "Full n2/n3 inventories")
    paths = set()
    for row in data["files"]:
        name = row["path"]
        need(type(name) is str and "\\" not in name, "Portable literal source path")
        relative = Path(name)
        need(not relative.is_absolute() and ".." not in relative.parts and name not in paths,
             "Unique contained source path")
        paths.add(name)
        path = directory / relative
        need(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(directory),
             "Ordinary contained frozen source: " + name)
        need(path.stat().st_size == row["bytes"] and sha(path) == row["sha256"],
             "Unchanged native source: " + name)
    expected = {"LICENSE", "n2/README.md", "n2/tensor_certificate.py",
                "n2/independent_integer_check.py", "n3/README.md", "n3/verify.py",
                "n3/audit_initial_polynomials.py", "n3/check_cube.cpp"}
    expected |= {f"n2/certificate/{i:03d}.json" for i in range(70)}
    expected |= {f"n3/certificate/{i:03d}.json" for i in range(111)}
    need(paths == expected, "Exactly the selected kernels and all 181 certificates")
    actual = set()
    for path in directory.rglob("*"):
        need(not path.is_symlink(), "No source-tree symlinks")
        if path.is_file():
            actual.add(path.relative_to(directory).as_posix())
    need(actual == paths | {"MANIFEST.json"}, "No missing or extra source-tree files")
    return data


def validate_output(stage, text):
    """Historical markers are expectations; only this observed output is checked."""
    spec = STAGES[stage]
    lines = text.splitlines()
    need(lines.count(spec["marker"]) == 1, "One exact full native marker: " + stage)
    need(not any(line.startswith(("REJECTED", "PARTIAL_INTEGER_CHECK_ONLY")) for line in lines),
         "No rejection or partial-run marker")
    pattern = {
        "n2-primary": r"CHECKED (\d+) \d+ \d+",
        "n2-independent": r"INTEGER_CHECK (\d+): triangles=\d+, leaves=\d+, moment_boxes=\d+",
        "n3-full": r"CELL (\d+) \[[^\]]+\] nodes=\d+ leaves=\d+ depth=\d+ moment_boxes=\d+ sha256=([0-9a-f]{64})",
    }.get(stage)
    indices = []
    cell_hashes = []
    if pattern:
        for line in lines:
            match = re.fullmatch(pattern, line)
            if match:
                indices.append(int(match[1]))
                if stage == "n3-full":
                    cell_hashes.append(match[2])
        need(indices == list(range(spec["cells"])), "Complete ordered fresh cell census")
    return {"exact_marker": spec["marker"], "ordered_cells": len(indices),
            "n3_source_cell_hashes": cell_hashes}


def trusted_guard(result, *, script_sha=None, supervisor_sha=None,
                  memory_bytes=None, cpu_seconds=None):
    """Validate the established resource capability, not a proof Boolean.

    The supervisor deliberately never accepts mathematics. The caller checks
    native output and source bindings after both kernel guard receipts pass.
    """
    scope = result.get("guard_scope", {})
    if (type(script_sha) is not str or type(supervisor_sha) is not str
            or type(memory_bytes) is not int or not 128*MIB <= memory_bytes <= 512*MIB
            or type(cpu_seconds) is not int or cpu_seconds < 2):
        return False
    controller_cpu = min(30, max(1, cpu_seconds // 10))
    return (result.get("mode") in (None, "trusted_native")
            and scope.get("kind") == "LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1"
            and scope.get("capability_established") is True
            and scope.get("native_python_execution") is True
            and scope.get("hard_sum_RLIMIT_AS_bytes") == memory_bytes
            and scope.get("worker_RLIMIT_AS_bytes") == memory_bytes-64*MIB
            and scope.get("supervisor_RLIMIT_AS_bytes") == 64*MIB
            and scope.get("hard_sum_RLIMIT_CPU_seconds") == cpu_seconds
            and scope.get("supervisor_RLIMIT_CPU_seconds") == controller_cpu
            and scope.get("worker_RLIMIT_CPU_seconds") == cpu_seconds-controller_cpu
            and scope.get("script_sha256") == script_sha
            and scope.get("supervisor_source_sha256") == supervisor_sha)


def classify(stage, receipt, stdout, **guard_expectations):
    need(receipt.get("status") == "completed" and type(receipt.get("returncode")) is int
         and receipt["returncode"] == 0, "Observed successful bounded native execution")
    checked = validate_output(stage, stdout)
    accepted = trusted_guard(receipt, **guard_expectations) and not STAGES[stage].get("requires_subprocesses", False)
    return {"status": "CONDITIONAL_NATIVE_ARITHMETIC_ACCEPTED" if accepted
            else "EXACT_NATIVE_OUTPUT_OBSERVED_UNTRUSTED_GUARD",
            "native_arithmetic_accepted": accepted,
            "conditional_on_analytic_reduction": True,
            "all_law_theorem_verified": False, "all_index_conclusion_verified": False,
            **checked}


class Progress:
    def __init__(self, path):
        self.stream = Path(path).open("x", encoding="utf-8")
        self.lock = threading.Lock()

    def emit(self, event, **fields):
        row = {"event": event, "utc": datetime.now(timezone.utc).isoformat(), **fields}
        line = json.dumps(row, sort_keys=True)
        with self.lock:
            self.stream.write(line + "\n")
            self.stream.flush()
            print(line, flush=True)

    def close(self):
        self.stream.close()


class FollowOutput:
    """Relay actual new worker lines and heartbeat while the guard is running."""
    def __init__(self, stage, path, progress, heartbeat):
        self.stage, self.path, self.progress = stage, Path(path), progress
        self.heartbeat = heartbeat
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self._follow, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def _follow(self):
        position, partial, last = 0, b"", 0.0
        start = time.monotonic()
        while True:
            try:
                with self.path.open("rb") as stream:
                    stream.seek(position)
                    block = stream.read(1024 * 1024)
                    position += len(block)
                chunks = (partial + block).split(b"\n")
                partial = chunks.pop()
                for line in chunks:
                    self.progress.emit("native_stdout", stage=self.stage,
                                       line=line.decode("utf-8", errors="replace")[:4096])
            except FileNotFoundError:
                pass
            now = time.monotonic()
            if now - last >= self.heartbeat:
                self.progress.emit("small_indices_heartbeat", stage=self.stage,
                                   elapsed_seconds=now-start, observed_stdout_bytes=position,
                                   certificate_accepted=False)
                last = now
            if self.stop.wait(.2):
                # One final read on the next iteration drains the completed log.
                if getattr(self, "draining", False):
                    break
                self.draining = True
        if partial:
            self.progress.emit("native_stdout", stage=self.stage,
                               line=partial.decode("utf-8", errors="replace")[:4096])

    def __exit__(self, *unused):
        self.stop.set()
        self.thread.join(timeout=5)
        need(not self.thread.is_alive(), "Output follower stopped")


def native_worker(config_path):
    """No guard monkeypatch: execute unchanged frozen functions or CLI entries."""
    need(not sys.flags.optimize and sys.dont_write_bytecode, "Unoptimized no-bytecode worker")
    config = json.loads(Path(config_path).read_text("utf-8"), object_pairs_hook=unique)
    need(set(config) == {"stage", "source", "tmp"}, "Exact internal worker schema")
    stage = config["stage"]
    need(stage in STAGES, "Known immutable native stage")
    source = Path(config["source"]).resolve()
    verify_vendor(source)
    temporary = Path(config["tmp"]).resolve()
    need(temporary.is_dir() and temporary.is_relative_to(source.parent), "Owned compiler temp")
    os.environ["TMPDIR"] = str(temporary)
    script = source / STAGES[stage]["script"]
    sys.path.insert(0, str(script.parent))
    if "function" in STAGES[stage]:
        module = runpy.run_path(str(script), run_name="frozen_scalar_audit")
        function = module[STAGES[stage]["function"]]
        need(callable(function), "Original exact scalar function")
        function()
        print(STAGES[stage]["marker"], flush=True)
    else:
        sys.argv = [str(script), *STAGES[stage]["args"]]
        runpy.run_path(str(script), run_name="__main__")
    verify_vendor(source)


def run(output, *, mode="basic", stages=None, wall_seconds=7200,
        cpu_seconds=7200, memory_bytes=512*MIB, heartbeat_seconds=20):
    from be_replay import linux_supervisor
    selected = list(STAGES) if stages is None else list(stages)
    need(mode in ("basic", "native") and selected and len(set(selected)) == len(selected)
         and all(stage in STAGES for stage in selected), "Explicit unique native stages")
    need(type(memory_bytes) is int and 64*MIB <= memory_bytes <= 512*MIB,
         "Memory allowance between64 and512MiB")
    verify_vendor()
    output = Path(output).absolute()
    need(not output.exists() and not output.is_symlink(), "Fresh exclusive run directory")
    output.mkdir(parents=True)
    output = output.resolve()
    work = output / "work"
    work.mkdir()
    # The audited native supervisor only runs a script inside its owned cwd.
    # This is a byte-identical driver copy; no frozen mathematical source is edited.
    worker_driver = work / "small_indices_driver.py"
    shutil.copyfile(Path(__file__).resolve(), worker_driver)
    need(sha(worker_driver) == sha(__file__), "Exact owned worker driver")
    source = work / "source"
    shutil.copytree(VENDOR, source)
    verify_vendor(source)
    temporary = work / "tmp"
    temporary.mkdir()
    progress = Progress(output / "progress.jsonl")
    rows = []
    started = time.monotonic()
    compiler = shutil.which("g++")
    context = {"source_commit": COMMIT, "source_manifest_sha256": MANIFEST_SHA256,
               "driver_sha256": sha(__file__), "python": sys.version,
               "supervisor_sha256": sha(linux_supervisor.__file__),
               "compiler_path": compiler,
               "compiler_sha256": sha(Path(compiler).resolve()) if compiler else None,
               "requested_mode": mode, "selected_stages": selected,
               "historical_receipts_used": False}
    write_json(output / "run-context.json", context)
    try:
        for stage in selected:
            progress.emit("small_indices_stage_started", stage=stage,
                          certificate_accepted=False, exact_bound={
                              "n2": "C_2 <= 2*sqrt(2)/7",
                              "n3": "C_3 <= 59*sqrt(3)/250"}[stage[:2]])
            if mode == "native" and STAGES[stage].get("requires_subprocesses"):
                rows.append({"stage": stage, "status": "UNSUPPORTED_NATIVE_PROCESS_TREE_CONTRACT",
                             "native_arithmetic_accepted": False,
                             "reason": "The unchanged n3 verifier spawns g++ and C++; basic mode can compute it without trusted acceptance."})
                progress.emit("small_indices_stage_incomplete", **rows[-1])
                break
            if stage == "n3-full" and compiler is None:
                rows.append({"stage": stage, "status": "INCOMPLETE_MISSING_COMPILER",
                             "native_arithmetic_accepted": False})
                progress.emit("small_indices_stage_incomplete", **rows[-1])
                break
            verify_vendor(source)
            config_path = work / (stage + "-worker.json")
            write_json(config_path, {"stage": stage, "source": str(source), "tmp": str(temporary)})
            stage_output = output / "stages" / stage
            command = [sys.executable, "-B", "-S", str(worker_driver),
                       "--_worker", str(config_path)]
            with FollowOutput(stage, stage_output / "stdout.txt", progress, heartbeat_seconds):
                receipt = linux_supervisor.run(
                    command, cwd=work, output_dir=stage_output, wall_seconds=wall_seconds,
                    cpu_seconds=cpu_seconds, memory_bytes=memory_bytes,
                    mode="trusted_native" if mode == "native" else "untrusted_search",
                    disk_bytes=128*MIB, log_bytes=16*MIB, heartbeat_seconds=heartbeat_seconds)
            try:
                text = Path(receipt["stdout_path"]).read_text("utf-8")
                need(sha(receipt["stdout_path"]) == receipt.get("stdout_sha256"),
                     "Observed stdout still matches the execution receipt")
                need(Path(receipt["stderr_path"]).stat().st_size == 0,
                     "Successful native stage has empty stderr")
                checked = classify(stage, receipt, text,
                                   script_sha=context["driver_sha256"],
                                   supervisor_sha=context["supervisor_sha256"],
                                   memory_bytes=memory_bytes, cpu_seconds=cpu_seconds)
                if stage == "n3-full":
                    data = verify_vendor(source)
                    expected = [row["sha256"] for row in data["files"]
                                if row["path"].startswith("n3/certificate/")]
                    need(checked["n3_source_cell_hashes"] == expected,
                         "Each n3 cell came from its frozen certificate bytes")
                row = {"stage": stage, **checked, "execution": receipt}
            except (OSError, ValueError, KeyError) as exc:
                row = {"stage": stage, "status": "INCOMPLETE_NO_ARITHMETIC_ACCEPTANCE",
                       "reason": str(exc), "native_arithmetic_accepted": False,
                       "execution": receipt}
            rows.append(row)
            need(sha(worker_driver) == context["driver_sha256"], "Unchanged owned worker driver")
            verify_vendor(source)
            write_json(output / (stage + "-result.json"), row)
            progress.emit("small_indices_stage_finished", stage=stage, status=row["status"],
                          native_arithmetic_accepted=row["native_arithmetic_accepted"])
            if row["status"].startswith("INCOMPLETE"):
                break
        computed = len(rows) == len(selected) and all(
            row["status"] in ("CONDITIONAL_NATIVE_ARITHMETIC_ACCEPTED",
                              "EXACT_NATIVE_OUTPUT_OBSERVED_UNTRUSTED_GUARD") for row in rows)
        complete_selection = selected == list(STAGES)
        accepted = computed and complete_selection and all(row["native_arithmetic_accepted"] for row in rows)
        result = {"status": "CONDITIONAL_SMALL_INDEX_ARITHMETIC_ACCEPTED" if accepted else
                  "COMPUTED_EXACT_OUTPUTS_UNTRUSTED_GUARD" if computed else "INCOMPLETE_NO_ACCEPTANCE",
                  "all_selected_stages_computed": computed,
                  "all_required_stages_selected": complete_selection,
                  "native_arithmetic_accepted": accepted,
                  "all_law_theorems_verified": False, "all_index_conclusion_verified": False,
                  "elapsed_seconds": time.monotonic()-started, "context": context,
                  "conditional_bound_targets": {"n2": "2*sqrt(2)/7", "n3": "59*sqrt(3)/250"},
                  "rows": rows}
        write_json(output / "SMALL_INDICES_RESULT.json", result)
        progress.emit("small_indices_finished", status=result["status"],
                      native_arithmetic_accepted=accepted, output=str(output))
        return result
    finally:
        progress.close()


def run_colab(*, durable_root, work_root="/content/berry-esseen-runs",
              wall_seconds=7200, cpu_seconds=7200, backup_interval=60):
    """Upload + RunAll entry point: six actual stages, visible logs, final ZIP.

    Uses basic mode for the unchanged compile/spawn n3 checker. Its exact
    outputs are evidence for later trusted acceptance, never a trusted proof
    on the basis of the weaker process-group resource contract.
    """
    from be_replay.colab_batch import Backups, atomic_json, bundle, event, utc
    from be_replay.environment import snapshot
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    root = Path(work_root) / "small-indices" / stamp
    root.mkdir(parents=True, exist_ok=False)
    durable = Path(durable_root) / "small-indices" / stamp
    status = {"scope": "COLAB_N2_N3_ARITHMETIC_NOT_ALL_INDEX_PROOF", "state": "started",
              "started_utc": utc(), "source_commit": COMMIT,
              "native_arithmetic_accepted": False, "all_law_theorems_verified": False,
              "all_index_conclusion_verified": False, "work": str(root),
              "durable": str(durable), "required_stages": list(STAGES)}
    atomic_json(root / "ENVIRONMENT.json", snapshot())
    atomic_json(root / "SESSION_RESULT.json", status)
    monitor = Backups(root, durable, interval=backup_interval)
    monitor.start()
    try:
        event(root, "small_indices_actual_replay_started", stages=list(STAGES),
              mode="basic", native_arithmetic_accepted=False)
        result = run(root / "arithmetic", mode="basic", wall_seconds=wall_seconds,
                     cpu_seconds=cpu_seconds, heartbeat_seconds=20)
        computed = result["all_selected_stages_computed"] and result["all_required_stages_selected"]
        status.update(state="exact_arithmetic_completed_untrusted_guard" if computed else
                      "incomplete_arithmetic_replay", arithmetic_result=result,
                      all_six_stages_computed=computed)
        event(root, "small_indices_actual_replay_finished", state=status["state"],
              native_arithmetic_accepted=False, all_index_conclusion_verified=False)
    except BaseException as error:
        status.update(state="incomplete_error", error=type(error).__name__ + ": " + str(error))
        (root / "ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        event(root, "small_indices_incomplete_error", error=status["error"])
    finally:
        status["finished_utc"] = utc()
        atomic_json(root / "SESSION_RESULT.json", status)
        try:
            monitor.close()
        except Exception as error:
            event(root, "final_backup_failed", error=str(error))
        output = bundle(root, durable)
        event(root, "small_indices_results_bundle_saved", path=str(output),
              state=status["state"], native_arithmetic_accepted=False)
    print("\nRESULT:", status["state"], "\nZIP:", output, flush=True)
    return {"status": status, "bundle": str(output.resolve()), "work": str(root.resolve())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--mode", choices=("basic", "native"), default="basic")
    parser.add_argument("--stages", nargs="+", choices=tuple(STAGES))
    parser.add_argument("--wall-seconds", type=int, default=7200, help="External wall cap per stage")
    parser.add_argument("--cpu-seconds", type=int, default=7200)
    parser.add_argument("--memory-mib", type=int, default=512)
    parser.add_argument("--heartbeat-seconds", type=int, default=20)
    parser.add_argument("--_worker", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args._worker:
        native_worker(args._worker)
        return 0
    if args.output is None:
        parser.error("--output must name a fresh run directory")
    result = run(args.output, mode=args.mode, stages=args.stages,
                 wall_seconds=args.wall_seconds, cpu_seconds=args.cpu_seconds,
                 memory_bytes=args.memory_mib*MIB, heartbeat_seconds=args.heartbeat_seconds)
    # Exit0 means the selected computations finished; inspect the explicit
    # trust fields. Basic mode NEVER establishes certificate acceptance.
    return 0 if result["all_selected_stages_computed"] else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status": "INCOMPLETE_NO_ACCEPTANCE", "reason": str(exc),
                          "native_arithmetic_accepted": False}), file=sys.stderr, flush=True)
        raise SystemExit(2)
