"""Read-only validation of completed n25 parent evidence after relocation.

No frozen mathematical module is imported and no numerical action is launched.
Recorded argv, receipt and capture bytes remain unchanged.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re

from . import n25_parents as parents
from . import count_task as common

MIB = parents.MIB


def need(condition, message):
    if not condition:
        raise ValueError(message)


def _same(left, right):
    return parents._same(left, right)


def _relative(value):
    need(type(value) is str and value and "\\" not in value and ":" not in value,
         "Literal portable relative evidence path")
    path = PurePosixPath(value)
    need(not path.is_absolute() and all(p not in (".", "..") for p in value.split("/"))
         and path.as_posix() == value, "Canonical contained relative evidence path")
    return Path(*path.parts)


def _inside(task, relative, *, directory=False):
    path = task / _relative(relative)
    for part in (path, *path.parents):
        if part == task.parent:
            break
        need(not part.is_symlink() and not (hasattr(part, "is_junction") and part.is_junction()),
             "No evidence path symlink or junction")
    need(path.resolve().is_relative_to(task) and (path.is_dir() if directory else path.is_file()),
         "Existing ordinary contained evidence artifact")
    return path


def _original_path(value):
    need(type(value) is str and value and "\x00" not in value, "Literal original absolute path")
    cls = PureWindowsPath if len(value) > 1 and value[1] == ":" else PurePosixPath
    path = cls(value)
    need(path.is_absolute() and ".." not in path.parts, "Absolute traversal-free original context")
    return path


def _map(value, original):
    path = _original_path(value)
    need(type(path) is type(original), "One original platform path convention")
    relative = path.relative_to(original)
    need(relative.parts and ".." not in relative.parts, "Original path is within the recorded task")
    return Path(*relative.parts).as_posix()


def _read(task, relative, limit=2*MIB):
    return common.read(_inside(task, relative), limit)


def _guard_sidecars(task, execution, observed, script_sha, cpu):
    from .linux_supervisor import _filter_instructions
    scope = observed["guard_scope"]
    records = {}
    for role, memory, seconds in (("worker", 448*MIB, cpu-min(30, max(1, cpu//10))),
                                  ("controller", 64*MIB, min(30, max(1, cpu//10)))):
        relative = execution + "/native-" + role + "-guard.json"
        guard = _read(task, relative)
        rows, architecture, denied, prlimit = _filter_instructions(guard["machine"])
        need(type(guard["seccomp_mode"]) is int and guard["seccomp_mode"] == 2
             and guard["no_new_privileges"] is True and guard["address_space_bytes"] == memory
             and guard["cpu_seconds"] == seconds and guard["audit_architecture"] == architecture
             and guard["denied_syscalls"] == denied and guard["prlimit64_query_only"] == prlimit
             and guard["x32_or_unknown_syscall_ABI_killed"] is True
             and guard["filter_instructions_sha256"] == hashlib.sha256(json.dumps(rows).encode()).hexdigest(),
             "Actual matching single-process kernel guard sidecar")
        need(_same(guard, scope["worker_guard" if role == "worker" else "supervisor_guard"]),
             "Supervisor embeds these exact actual kernel guard receipts")
        records[role] = guard
    worker = records["worker"]
    result = _read(task, execution + "/native-controller-result.json")
    need(type(result["returncode"]) is int and result["returncode"] == 0
         and type(worker["pid"]) is int and worker["pid"] > 0
         and type(worker["birth_tick"]) is int and worker["birth_tick"] > 0
         and result["worker_pid"] == worker["pid"]
         and worker["script_sha256"] == result["worker_source_sha256_after"] == script_sha,
         "Completed worker identity and unchanged native script")
    return {name: common.digest(_inside(task, execution + "/" + name)) for name in
            ("native-worker-guard.json", "native-controller-guard.json", "native-controller-result.json")}


def _execution(task, original, branch, stage, report, root_relative):
    from .small_indices import trusted_guard
    kind, action = stage.split("-")
    paths = parents.names(branch)
    root = _inside(task, root_relative, directory=True)
    execution = str(PurePosixPath(root_relative).parent / "execution")
    _inside(task, execution, directory=True)
    command = report["command"]
    script_relative = root_relative + "/" + paths[kind + "_dir"] + "/" + paths[kind + "_script"]
    script = _inside(task, script_relative)
    need(type(command) is list and len(command) == 5 and all(type(v) is str for v in command)
         and command[1:3] == ["-B", "-S"] and command[-1] == action
         and _map(command[3], original) == script_relative, "Original unchanged native command and action")
    _original_path(command[0])
    cpu, wall = report["cpu_seconds"], report["wall_seconds"]
    need(type(cpu) is int and 2 <= cpu <= 7200 and type(wall) is int and 1 <= wall <= 7260,
         "Original bounded per-stage CPU and wall ceilings")
    supervisor_sha = common.digest(Path(parents.__file__).with_name("linux_supervisor.py"))
    need(report["supervisor_sha256"] == supervisor_sha, "Unchanged original supervisor source")
    observed = report["observed"]
    need(observed["status"] == "completed" and type(observed["returncode"]) is int
         and observed["returncode"] == 0 and observed["mode"] == "trusted_native"
         and observed.get("reason") is None and observed.get("proof_accepted") is False,
         "Complete original native execution, without a theorem promotion")
    need(trusted_guard(observed, script_sha=common.digest(script), supervisor_sha=supervisor_sha,
                       memory_bytes=512*MIB, cpu_seconds=cpu), "Established original bounded native guard")
    hashes = {}
    for key in ("stdout", "stderr"):
        relative = execution + "/" + key + ".txt"
        need(_map(observed[key + "_path"], original) == relative, "Exact original capture context")
        path = _inside(task, relative)
        need(path.stat().st_size <= 16*MIB and common.digest(path) == observed[key + "_sha256"]
             == report[key + "_sha256"], "Actual capture matches both original execution bindings")
        hashes[key + "_sha256"] = common.digest(path)
    need(_inside(task, execution + "/stderr.txt").stat().st_size == 0, "Successful native stderr is empty")
    lines = _inside(task, execution + "/stdout.txt").read_text("utf-8").splitlines()
    marker = parents._marker(branch, stage)
    need(sum(line == marker or line.startswith(marker + " ") for line in lines) == 1,
         "Exactly one actual complete original native marker")
    need(_same(_read(task, execution + "/supervisor-result.json"), observed),
         "Actual supervisor-result exactly matches the recorded observation")
    native = _read(task, execution + "/native-launch.json")
    need(_same(native["argv"], command) and _map(native["cwd"], original) == root_relative
         and _map(native["output_dir"], original) == execution and native["mode"] == "trusted_native"
         and native["checkpoint_paths"] == [] and native["cpu_seconds"] == cpu
         and native["wall_seconds"] == wall and native["memory_bytes"] == 512*MIB
         and native["disk_bytes"] == 256*MIB and native["log_bytes"] == 16*MIB,
         "Actual native launch used the original new_root and exact bounded action")
    need(native["worker_memory_bytes"] == 448*MIB and native["supervisor_memory_bytes"] == 64*MIB
         and native["supervisor_cpu_seconds"] == min(30, max(1, cpu//10))
         and native["worker_cpu_seconds"] == cpu-native["supervisor_cpu_seconds"], "Native launch split hard limits")
    launch = _read(task, execution + "/launch.json")
    outer = launch["argv"]
    need(type(outer) is list and len(outer) == 6 and outer[:3] == command[:3]
         and _original_path(outer[3]).name == "linux_supervisor.py" and outer[4] == "--_native-controller"
         and _map(outer[5], original) == execution + "/native-launch.json"
         and _same(launch, dict(native, argv=outer)), "Actual outer launch and native controller context")
    hashes.update(_guard_sidecars(task, execution, observed, common.digest(script), cpu))
    for filename in ("launch.json", "native-launch.json", "supervisor-result.json"):
        hashes[filename] = common.digest(_inside(task, execution + "/" + filename))
    need(not (task / execution / "never-created-native-pycache").exists(), "No unexpected native bytecode prefix")
    result = parents.validate_native(root, branch, kind, accepted=action == "accept")
    need(_same(result, report["native_result"]), "Original native result still matches every proof and receipt")
    return hashes


def validate_completed(task, *, original_task_root=None, expected_branch=None):
    """Revalidate all four completed stages, mapping an original absolute prefix.

    The original prefix may be inferred from the first capture path; an explicit
    prefix is checked against every launch/capture path. No evidence is rewritten.
    """
    raw_task = Path(task).absolute()
    need(not raw_task.is_symlink() and not (hasattr(raw_task, "is_junction") and raw_task.is_junction()),
         "Ordinary restored parent task root")
    task, branch = parents._task(raw_task)
    need(expected_branch is None or type(expected_branch) is str and expected_branch == branch,
         "Expected whole-parent branch")
    packet = common.read(_inside(task, "TASK.json"), MIB)
    manifests = {kind: parents.BRANCHES[branch][kind + "_manifest"] for kind in ("initial", "resource")}
    need(_same(packet, dict(schema="FRESH_N25_PARENT_TASK_V1", branch=branch, source_asset=common.ASSETS["old"],
         driver_sha256=common.digest(parents.__file__), manifests=manifests,
         imported_stronger24_sha256=parents.PREDECESSOR_SHA256, conditional_premises=parents.PREMISES,
         stronger24_acquisition_verified=False, count_interface_join_verified=False, all_index_conclusion_verified=False)),
         "Exact original task identity, premises and false theorem flags")
    _inside(task, "source", directory=True)
    reports, hashes, captures, roots, artifacts = {}, {}, {}, {}, {}
    original = _original_path(str(original_task_root)) if original_task_root is not None else None
    paths = parents.names(branch)
    for stage in parents.STAGES:
        ledger = stage + "-COMPLETED.json"
        report = _read(task, ledger)
        need(report["schema"] == "FRESH_N25_PARENT_STAGE_V1" and report["stage"] == stage
             and report["branch"] == branch and report["status"] == "completed"
             and report["driver_sha256"] == common.digest(parents.__file__)
             and _same(report["dependencies"], hashes) and _same(report["conditional_premises"], parents.PREMISES)
             and all(report[name] is False for name in ("stronger24_acquisition_verified", "count_interface_join_verified", "all_index_conclusion_verified"))
             and report["native_arithmetic_accepted"] is stage.endswith("-accept"),
             "Complete original stage ledger, dependency chain and scoped flags")
        relative = report["capsule_relative"]
        parts = _relative(relative).parts
        need(len(parts) == 3 and parts[0] == "attempts" and parts[2] == "new_root"
             and re.fullmatch(re.escape(stage) + r"-[0-9a-f]{12}", parts[1]), "Distinct original private stage capsule")
        execution = "/".join(parts[:2]) + "/execution"
        if original is None:
            stdout = _original_path(report["observed"]["stdout_path"])
            suffix = (*parts[:2], "execution", "stdout.txt")
            need(tuple(stdout.parts[-len(suffix):]) == suffix, "Infer one original task prefix from its exact stage suffix")
            original = stdout.parents[len(suffix)-1]
        roots[stage] = _inside(task, relative, directory=True)
        parents.verify_sources(roots[stage], branch)
        kind, action = stage.split("-")
        required = {paths[kind + "_dir"] + "/" + paths[kind + "_proof"]}
        if action == "accept":
            required.add(paths[kind + "_dir"] + "/" + paths[kind + "_receipt"])
        if stage != "initial-construct":
            required.add(paths["initial_dir"] + "/" + paths["initial_proof"])
        if kind == "resource":
            required.add(paths["initial_dir"] + "/" + paths["initial_receipt"])
        need(type(report["artifact_sha256"]) is dict and set(report["artifact_sha256"]) == required,
             "Exact complete generated/input artifact inventory")
        for name, pin in report["artifact_sha256"].items():
            need(common.digest(_inside(task, relative + "/" + name)) == pin, "Unchanged original fresh stage artifact")
        artifacts[stage] = report["artifact_sha256"]
        captures[stage] = _execution(task, original, branch, stage, report, relative)
        result_path = "/".join(parts[:2]) + "/RESULT.json"
        need(common.digest(_inside(task, result_path)) == common.digest(_inside(task, ledger)),
             "Original attempt result and completed stage ledger have identical bytes")
        reports[stage] = report
        hashes[stage] = common.digest(_inside(task, ledger))
    initial_proof = paths["initial_dir"] + "/" + paths["initial_proof"]
    initial_receipt = paths["initial_dir"] + "/" + paths["initial_receipt"]
    resource_proof = paths["resource_dir"] + "/" + paths["resource_proof"]
    resource_receipt = paths["resource_dir"] + "/" + paths["resource_receipt"]
    need(len({artifacts[s][initial_proof] for s in parents.STAGES}) == 1,
         "Every stage consumes the exact fresh INITIAL construction")
    need(len({artifacts[s][initial_receipt] for s in parents.STAGES if s.startswith("resource-")}
             | {artifacts["initial-accept"][initial_receipt]}) == 1,
         "Every resource stage consumes the exact fresh INITIAL acceptance")
    need(artifacts["resource-construct"][resource_proof] == artifacts["resource-accept"][resource_proof],
         "Resource acceptance consumes the exact fresh complete construction")
    final = reports["resource-accept"]
    final_root = roots["resource-accept"]
    parents.validate_native(final_root, branch, "initial", accepted=True)
    resource = parents.validate_native(final_root, branch, "resource", accepted=True)
    return dict(schema="REVALIDATED_N25_PARENT_V1", branch=branch, n=25, contact_allowance="5/16",
                resource_capsule_relative=final["capsule_relative"],
                resource_proof_sha256=artifacts["resource-accept"][resource_proof],
                resource_receipt_sha256=artifacts["resource-accept"][resource_receipt],
                initial_proof_sha256=artifacts["initial-accept"][initial_proof],
                initial_receipt_sha256=artifacts["initial-accept"][initial_receipt],
                source_manifest_sha256=manifests, stage_ledger_sha256=hashes, capture_bindings=captures,
                original_task_root=str(original), driver_sha256=common.digest(parents.__file__),
                conditional_premises=parents.PREMISES, signed_rectangles=239616, probability_panels=100,
                initial_negative_controls=12, resource_negative_controls=12,
                surviving_panels=resource["surviving_panels"], excluded_panels=resource["excluded_panels"],
                native_arithmetic_accepted=True, stronger24_acquisition_verified=False,
                count_interface_join_verified=False, all_index_conclusion_verified=False)
