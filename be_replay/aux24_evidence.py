"""Strict readback of preserved auxiliary execution evidence, without replay.

This supplements the unchanged arithmetic/source validators. It does not import
an archived kernel, execute a subprocess, rewrite a receipt or acquire a theorem.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath

MIB = 1024**2


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def same(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(same(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
    return left == right


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(MIB), b""):
            h.update(block)
    return h.hexdigest()


def relative(value):
    need(type(value) is str and value and "\\" not in value and ":" not in value,
         "Literal portable evidence-relative path")
    parts = value.split("/")
    need(all(p and p not in (".", "..") for p in parts)
         and not PurePosixPath(value).is_absolute(), "Contained canonical evidence-relative path")
    return Path(*parts)


def inside(task, value, *, directory=False):
    path = task / relative(value)
    for parent in (path, *path.parents):
        if parent == task.parent:
            break
        need(not parent.is_symlink() and not (hasattr(parent, "is_junction") and parent.is_junction()),
             "No evidence symlink or junction")
    need(path.resolve().is_relative_to(task) and (path.is_dir() if directory else path.is_file()),
         "Existing ordinary contained evidence artifact: " + value)
    return path


def original_path(value):
    need(type(value) is str and value and "\x00" not in value, "Literal original absolute evidence path")
    cls = PureWindowsPath if len(value) > 1 and value[1] == ":" else PurePosixPath
    path = cls(value)
    need(path.is_absolute() and ".." not in path.parts, "Absolute traversal-free original context")
    return path


def mapped(value, original):
    path = original_path(value)
    need(type(path) is type(original), "One original evidence platform convention")
    result = path.relative_to(original)
    need(result.parts, "Artifact is strictly inside the original task")
    return Path(*result.parts).as_posix()


def read(task, value, limit=4*MIB):
    path = inside(task, value)
    need(path.stat().st_size <= limit, "Bounded execution JSON artifact")
    def unique(pairs):
        packet = {}
        for key, value in pairs:
            need(key not in packet, "Unique execution JSON keys")
            packet[key] = value
        return packet
    return json.loads(path.read_text("utf-8"), object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError("Finite JSON numbers")))


def _group_scope(launch):
    return dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP", proof_acceptance=False,
                external_wall_seconds=launch["wall_seconds"], per_process_RLIMIT_AS_bytes=launch["memory_bytes"],
                per_process_RLIMIT_CPU_seconds=launch["cpu_seconds"], aggregate_kernel_memory_limit=False,
                aggregate_kernel_cpu_limit=False, sampled_group_RSS_limit_bytes=launch["memory_bytes"],
                sampled_group_CPU_limit_seconds=launch["cpu_seconds"], sampled_file_limit_bytes=launch["disk_bytes"],
                sampled_log_limit_bytes=launch["log_bytes"], descendants_changing_session_are_contained=False,
                equivalent_to_Windows_Job_or_cgroup=False)


def _native_guards(task, execution, observed, launch, script_sha):
    from . import linux_supervisor
    from .small_indices import trusted_guard
    need(trusted_guard(observed, script_sha=script_sha, supervisor_sha=digest(linux_supervisor.__file__),
                       memory_bytes=512*MIB, cpu_seconds=launch["cpu_seconds"]),
         "Original native scope and split hard limits")
    scope, records, hashes = observed["guard_scope"], {}, {}
    need(scope.get("proof_acceptance") is False
         and same(scope.get("external_group_watchdog"), _group_scope(launch)),
         "Original external native watchdog policy; no mathematical acceptance")
    for role, key, memory_key, cpu_key in (
        ("worker", "worker_guard", "worker_memory_bytes", "worker_cpu_seconds"),
        ("controller", "supervisor_guard", "supervisor_memory_bytes", "supervisor_cpu_seconds"),
    ):
        filename = execution + "/native-" + role + "-guard.json"
        guard = read(task, filename)
        rows, architecture, denied, prlimit = linux_supervisor._filter_instructions(guard["machine"])
        need(same(guard, scope[key]) and type(guard["seccomp_mode"]) is int and guard["seccomp_mode"] == 2
             and guard["no_new_privileges"] is True and type(guard["address_space_bytes"]) is int
             and guard["address_space_bytes"] == launch[memory_key] and type(guard["cpu_seconds"]) is int
             and guard["cpu_seconds"] == launch[cpu_key] and guard["audit_architecture"] == architecture
             and same(guard["denied_syscalls"], denied) and same(guard["prlimit64_query_only"], prlimit)
             and guard["x32_or_unknown_syscall_ABI_killed"] is True
             and guard["filter_instructions_sha256"] == hashlib.sha256(json.dumps(rows).encode()).hexdigest()
             and type(guard["pid"]) is int and guard["pid"] > 0
             and type(guard["birth_tick"]) is int and guard["birth_tick"] > 0,
             "Actual exact kernel guard receipt and process identity: " + role)
        records[role] = guard
        hashes[filename] = digest(inside(task, filename))
    need(records["controller"]["pid"] != records["worker"]["pid"], "Distinct original controller and worker")
    filename = execution + "/native-controller-result.json"
    result = read(task, filename)
    need(set(result) == {"returncode", "worker_pid", "worker_source_sha256_after"}
         and type(result["returncode"]) is int and result["returncode"] == 0
         and type(result["worker_pid"]) is int and result["worker_pid"] == records["worker"]["pid"]
         and result["worker_source_sha256_after"] == records["worker"]["script_sha256"] == script_sha,
         "Actual completed native worker and unchanged source after execution")
    hashes[filename] = digest(inside(task, filename))
    prefix = task / execution / "never-created-native-pycache"
    need(not prefix.exists() and not prefix.is_symlink(), "No native bytecode prefix")
    return hashes


def validate_execution(task, original, *, execution, command, cwd, mode, observed,
                       disk_bytes, report=None):
    """Revalidate preserved transport only; mathematical output is checked elsewhere."""
    from . import linux_supervisor
    task = Path(task).resolve()
    original = original_path(str(original))
    inside(task, execution, directory=True)
    need(type(command) is list and len(command) >= 4 and all(type(v) is str for v in command),
         "Literal original stage command")
    original_path(command[0])
    need(command[1] == "-B" and command[2] in ("-S", "-u")
         and (mode != "trusted_native" or command[2] == "-S"),
         "Original ordinary interpreter flags; native worker starts without site imports")
    script_relative = mapped(command[3], original)
    script = inside(task, script_relative)
    need(mode in ("trusted_native", "untrusted_search") and observed.get("mode") == mode
         and observed.get("status") == "completed" and type(observed.get("returncode")) is int
         and observed["returncode"] == 0 and observed.get("reason") is None
         and observed.get("proof_accepted") is False and type(observed.get("sample_count")) is int
         and observed["sample_count"] > 0, "Actual complete sampled execution; no supervisor proof claim")
    need(same(read(task, execution + "/supervisor-result.json"), observed),
         "Actual supervisor result equals the preserved stage observation")
    hashes = {execution + "/supervisor-result.json": digest(inside(task, execution + "/supervisor-result.json"))}
    for kind in ("stdout", "stderr"):
        filename = execution + "/" + kind + ".txt"
        path = inside(task, filename)
        need(mapped(observed[kind + "_path"], original) == filename and path.stat().st_size <= 16*MIB
             and digest(path) == observed[kind + "_sha256"], "Actual exact original captured bytes: " + kind)
        if report is not None and kind + "_sha256" in report:
            need(digest(path) == report[kind + "_sha256"], "Stage ledger also binds actual capture")
        hashes[filename] = digest(path)
    need(inside(task, execution + "/stderr.txt").stat().st_size == 0, "Successful execution stderr is empty")
    filename = execution + ("/native-launch.json" if mode == "trusted_native" else "/launch.json")
    launch = read(task, filename)
    cpu = launch["cpu_seconds"]
    need(same(launch["argv"], command) and mapped(launch["cwd"], original) == cwd
         and mapped(launch["output_dir"], original) == execution and launch["mode"] == mode
         and type(cpu) is int and 2 <= cpu <= 7200 and type(launch["wall_seconds"]) is float
         and math.isfinite(launch["wall_seconds"]) and 0 < launch["wall_seconds"] <= 7260
         and type(launch["memory_bytes"]) is int and launch["memory_bytes"] == 512*MIB
         and launch["checkpoint_paths"] == [] and type(launch["disk_bytes"]) is int
         and launch["disk_bytes"] == disk_bytes and type(launch["log_bytes"]) is int
         and launch["log_bytes"] == 16*MIB and type(launch["sample_seconds"]) is float
         and launch["sample_seconds"] == .2 and type(launch["heartbeat_seconds"]) is float
         and launch["heartbeat_seconds"] == 20., "Actual original command, cwd and exact bounded launch policy")
    inside(task, cwd, directory=True)
    if report is not None and "cpu_seconds" in report:
        need(type(report["cpu_seconds"]) is int and report["cpu_seconds"] == cpu
             and type(report["wall_seconds"]) is int and float(report["wall_seconds"]) == launch["wall_seconds"],
             "Launch budgets match the original stage ledger")
    base_fields = {"argv", "cwd", "output_dir", "mode", "wall_seconds", "cpu_seconds", "memory_bytes",
                   "checkpoint_paths", "disk_bytes", "log_bytes", "sample_seconds", "heartbeat_seconds"}
    hashes[filename] = digest(inside(task, filename))
    if mode == "trusted_native":
        control_cpu = min(30, max(1, cpu//10))
        split = dict(worker_memory_bytes=448*MIB, supervisor_memory_bytes=64*MIB,
                     worker_cpu_seconds=cpu-control_cpu, supervisor_cpu_seconds=control_cpu)
        need(set(launch) == base_fields | set(split)
             and all(type(launch[k]) is int and launch[k] == v for k, v in split.items()),
             "Exact original native launch and hard-limit split")
        outer = read(task, execution + "/launch.json")
        argv = outer["argv"]
        need(type(argv) is list and len(argv) == 6 and argv[:3] == command[:3]
             and original_path(argv[3]).name == "linux_supervisor.py" and argv[4] == "--_native-controller"
             and mapped(argv[5], original) == execution + "/native-launch.json"
             and same(outer, dict(launch, argv=argv)), "Original outer controller command and unchanged native context")
        hashes[execution + "/launch.json"] = digest(inside(task, execution + "/launch.json"))
        hashes.update(_native_guards(task, execution, observed, launch, digest(script)))
    else:
        need(set(launch) == base_fields and same(observed["guard_scope"], _group_scope(launch)),
             "Exact BASIC sampled process-group policy without native upgrade")
    need(report is None or report.get("supervisor_sha256") == digest(linux_supervisor.__file__),
         "Same reviewed current supervisor source")
    return dict(mode=mode, native_platform_contract_revalidated=mode == "trusted_native",
                command=command, cwd_relative=cwd, execution_relative=execution, script_sha256=digest(script),
                artifact_sha256=hashes, native_arithmetic_accepted=False, all_index_conclusion_verified=False)


def validate_task_transport(task, key, *, original_task_root=None):
    """Check every expected stage; caller also runs its unchanged arithmetic validator."""
    from . import aux21_23, strong24_branches
    task = Path(task).resolve()
    rows, ledgers, original = {}, {}, None
    if key.startswith("auxiliary"):
        value = key[len("auxiliary"):]
        aux21_23.target(value)
        definitions = aux21_23.stages(value)
        for stage in definitions:
            name = stage["name"]
            ledger = name + "-COMPLETED.json"
            report = read(task, ledger, 32*MIB)
            context = original_path(report["original_task_root"])
            need(original is None or context == original, "One original auxiliary task for every stage")
            original = context
            need(report["schema"] == "FRESH_AUX21_23_STAGE_V1" and report["target"] == value
                 and report["stage"] == name and report["status"] == "completed" and report["mode"] == stage["mode"]
                 and report["driver_sha256"] == digest(aux21_23.__file__)
                 and report["source_manifest_sha256"] == aux21_23.EPOCH_PINS[value]
                 and same(report["dependencies"], ledgers), "Complete original auxiliary execution ledger chain")
            cwd = "source/cutoff25_20261011/" + stage["directory"]
            need(mapped(report["command"][3], original) == cwd + "/" + stage["script"]
                 and report["command"][1:3] == ["-B", "-S"] and report["command"][4:] == stage["args"],
                 "Exact expected auxiliary entrypoint and arguments")
            rows[name] = validate_execution(task, original, execution=report["execution_relative"],
                command=report["command"], cwd=cwd, mode=stage["mode"], observed=report["observed"],
                disk_bytes=256*MIB, report=report)
            ledgers[name] = digest(inside(task, ledger))
    else:
        need(key.startswith("stronger24-"), "Known auxiliary or stronger24 job")
        branch = key[len("stronger24-"):]
        definitions = strong24_branches.stages(branch)
        result = read(task, "RESULT.json", 8*MIB)
        original = original_path(result["original_task_root"])
        for stage in definitions:
            name, ledger = stage["name"], stage["name"] + "-COMPLETED.json"
            report = read(task, ledger, 32*MIB)
            need(report["schema"] == "OBSERVED_STRONG24_BRANCH_STAGE_V1" and report["branch"] == branch
                 and same(report["stage"], stage) and original_path(report["original_task_root"]) == original
                 and same(report["preceding_stage_sha256"], ledgers) and report["native_arithmetic_accepted"] is False,
                 "Complete original conditional BASIC stage ledger chain")
            cwd = "execution-epoch/cutoff25_20261011/" + stage["folder"]
            need(mapped(report["command"][3], original) == cwd + "/" + stage["script"]
                 and report["command"][1:3] == ["-B", "-u"] and report["command"][4:] == stage["args"],
                 "Exact expected original branch entrypoint and arguments")
            rows[name] = validate_execution(task, original, execution="captures/" + name,
                command=report["command"], cwd=cwd, mode="untrusted_search", observed=report["observed"],
                disk_bytes=1024*MIB, report=report)
            need(report["launch_sha256"] == rows[name]["artifact_sha256"]["captures/" + name + "/launch.json"]
                 and report["supervisor_result_sha256"] == rows[name]["artifact_sha256"]["captures/" + name + "/supervisor-result.json"],
                 "Original branch stage binds actual launch and supervisor hashes")
            ledgers[name] = digest(inside(task, ledger))
    need(original_task_root is None or original_path(str(original_task_root)) == original,
         "Explicit original prefix agrees with every preserved execution")
    return dict(schema="AUX21_24_STRICT_TRANSPORT_READBACK_V1", job=key, stages=rows,
                stage_ledger_sha256=ledgers, original_task_root=str(original),
                validator_sha256=digest(__file__), execution_transport_revalidated=True,
                native_arithmetic_accepted=False, full_auxiliary_bound_verified=False,
                stronger24_acquisition_verified=False, all_index_conclusion_verified=False)
