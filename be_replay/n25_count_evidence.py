"""Read-only, relocated verification of completed n25 count-job evidence.

No numerical kernel is imported or evaluated. A search checkpoint or a native
receipt without its complete observed guard/capture chain is never acceptance.
The accepted count remains conditional on its parent acquisitions/framework.
"""
from __future__ import annotations
import ast
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import re

from . import count_task as count

MIB = 1024**2
OBSERVED_FIELDS = {"schema", "target", "scope", "epoch", "observed", "census", "implementation",
                   "arithmetic_accepted", "parent_acquisitions_verified", "all_index_conclusion_verified"}
ACCEPTED_FIELDS = {"native_receipt", "native_receipt_sha256", "negative_controls", "conditional_premises"}
PREMISES = ["Correct original whole-parent INITIAL/resource acquisitions",
            "Same-witness attainment/contact/Fourier/count framework"]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def same(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(same(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
    return left == right


def path_class(value):
    return PureWindowsPath if len(str(value)) > 1 and str(value)[1] == ":" else PurePosixPath


def original_context(epoch, name, explicit=None):
    cls = path_class(epoch)
    value = cls(epoch)
    need(value.is_absolute() and ".." not in value.parts and value.name == name,
         "One absolute original task root derived from the recorded accept epoch")
    root = value.parent
    need(explicit is None or cls(str(explicit)) == root, "Expected original task context")
    return root


def relative(path, original):
    value = type(original)(str(path))
    need(value.is_absolute() and ".." not in value.parts, "Absolute contained recorded artifact")
    result = value.relative_to(original)
    need(result.parts and ".." not in result.parts, "Recorded artifact belongs to this original task")
    return Path(*result.parts)


def implementation(record):
    from . import count_implementation_history as history
    expected = count.implementation()
    need(type(record) is dict and set(record) == set(expected)
         and type(record["python"]) is str and record["python"], "Complete recorded implementation context")
    need(all(same(record[k], expected[k]) for k in expected if k != "python")
         or history.matches(record, history.ordinary()),
         "Current or exactly published pre-PREFIX2 implementation pins")


def sealed(target, capsule, *, native=False):
    files = count.verify_capsule(target, capsule)
    index = count.TARGETS[target][1]
    allowed = set(files) | {"FROZEN_DESIGN.json"}
    if native:
        allowed |= {f"COUNT{index}_FOREST.json", f"COUNT{index}_ACCEPTED.json"}
    elif count.TARGETS[target][0] == "new-conditional-v14":
        allowed.add("SOURCE_PREPARATION_REPORT.json")
    actual = set()
    for path in Path(capsule).iterdir():
        need(path.is_file() and not path.is_symlink(), "Flat sealed source/candidate capsule")
        actual.add(path.name)
    need(actual == allowed, "Complete exact source capsule; no unknown native or historical outputs")
    return files


def control_labels(protocol):
    tree = ast.parse(Path(protocol).read_bytes())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "accept"]
    need(len(functions) == 1, "One pinned native accept function")
    assignments = [n for n in functions[0].body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "mutations" for t in n.targets)]
    need(len(assignments) == 1 and isinstance(assignments[0].value, ast.List), "Literal original native control inventory")
    result = []
    for node in assignments[0].value.elts:
        need(isinstance(node, ast.Tuple) and len(node.elts) == 2 and isinstance(node.elts[0], ast.Constant)
             and type(node.elts[0].value) is str, "Literal original corruption-control label")
        result.append(node.elts[0].value)
    need(len(result) == len(set(result)) == 24, "Exactly24 distinct original corruption controls")
    return result


def full_statistics(forest):
    statuses = Counter()
    depth = 0
    maximum = Fraction(0)
    for root in forest["roots"]:
        stack = [(root["tree"], 0)]
        while stack:
            node, level = stack.pop()
            depth = max(depth, level)
            if node["kind"] == "split":
                stack += [(node["left"], level+1), (node["right"], level+1)]
            else:
                need(type(node["decision"]) is str and node["decision"], "Typed closed-leaf decision")
                statuses[node["decision"]] += 1
                if node["decision"] == "PASS_TARGET":
                    maximum = max(maximum, Fraction(node["result"]["score_upper"]))
    return dict(closed_statuses=dict(statuses), maximum_depth=depth, maximum_score=str(maximum))


def guard_files(execution, observed, launch, script_sha):
    """Check preserved worker/controller receipts against the pinned guard code."""
    from . import linux_supervisor
    scope = observed["guard_scope"]
    for filename, key, memory_key, cpu_key in (
        ("native-worker-guard.json", "worker_guard", "worker_memory_bytes", "worker_cpu_seconds"),
        ("native-controller-guard.json", "supervisor_guard", "supervisor_memory_bytes", "supervisor_cpu_seconds"),
    ):
        row = count.read(execution / filename, MIB)
        need(same(row, scope[key]), "Actual guard artifact equals captured supervisor scope")
        instructions, architecture, denied, prlimit = linux_supervisor._filter_instructions(row["machine"])
        need(type(row["seccomp_mode"]) is int and row["seccomp_mode"] == 2 and row["no_new_privileges"] is True
             and row["address_space_bytes"] == launch[memory_key] and row["cpu_seconds"] == launch[cpu_key]
             and row["audit_architecture"] == architecture and row["denied_syscalls"] == denied
             and row["prlimit64_query_only"] == prlimit and row["x32_or_unknown_syscall_ABI_killed"] is True
             and row["filter_instructions_sha256"] == hashlib.sha256(json.dumps(instructions).encode()).hexdigest(),
             "Both original exact seccomp policies and hard resource caps")
    worker = scope["worker_guard"]
    controller = count.read(execution / "native-controller-result.json", MIB)
    need(type(controller["returncode"]) is int and controller["returncode"] == 0
         and controller["worker_pid"] == worker["pid"]
         and controller["worker_source_sha256_after"] == worker["script_sha256"] == script_sha,
         "Actual completed worker PID and unchanged native source after execution")


def validate_epoch(task, target, epoch, *, original_task_root=None):
    from .small_indices import trusted_guard
    accepted_path = epoch / "NATIVE_ACCEPTED.json"
    accepted = count.read(accepted_path, 4*MIB)
    observed_path = epoch / "NATIVE_OBSERVED.json"
    before = count.read(observed_path, 4*MIB)
    need(set(before) == OBSERVED_FIELDS and set(accepted) == OBSERVED_FIELDS | ACCEPTED_FIELDS,
         "Exact observed-to-accepted native execution protocol")
    need(before["schema"] == "COUNT_NATIVE_EXECUTION_V1" and before["target"] == target
         and before["scope"] == count.scope(target) and before["arithmetic_accepted"] is False
         and accepted["arithmetic_accepted"] is True
         and all(before[k] is False and accepted[k] is False for k in ("parent_acquisitions_verified", "all_index_conclusion_verified"))
         and all(same(before[k], accepted[k]) for k in before if k != "arithmetic_accepted"),
         "Preserved original unaccepted observation and sole validated acceptance transition")
    implementation(accepted["implementation"])
    original = original_context(accepted["epoch"], epoch.name, original_task_root)
    need(relative(accepted["epoch"], original) == epoch.relative_to(task), "Recorded accept epoch is this restored epoch")
    capsule, execution = epoch / "capsule", epoch / "execution"
    files = sealed(target, capsule, native=True)
    need(same(files, sealed(target, task / "capsule")), "Same exact sealed source design in source and acceptance clone")
    index = count.TARGETS[target][1]
    forest_path, receipt_path = capsule / f"COUNT{index}_FOREST.json", capsule / f"COUNT{index}_ACCEPTED.json"
    forest, receipt = count.read(forest_path), count.read(receipt_path, 4*MIB)
    census = count.forest_census(forest, target, capsule)
    need(same(accepted["census"], census), "Full ordered26-root complete forest census")
    count.validate_native(receipt, target, capsule, census)
    need(receipt["negative_controls"] == control_labels(capsule / "count_protocol.py"), "Every original control in its exact order")
    statistics = dict(nodes=census["nodes"], leaves=census["leaves"], **full_statistics(forest))
    need(same(receipt["statistics"], statistics), "Actual native statistics match every stored closed leaf and split")
    need(type(accepted["negative_controls"]) is int and accepted["negative_controls"] == 24
         and accepted["native_receipt_sha256"] == count.digest(receipt_path)
         and relative(accepted["native_receipt"], original) == receipt_path.relative_to(task), "Actual complete native acceptance receipt identity")
    premises = PREMISES + (["Global C24 auxiliary bound and attained positive-closed q25<=5/16"]
                           if count.TARGETS[target][0] == "new-conditional-v14" else [])
    need(accepted["conditional_premises"] == premises, "Explicit unchanged conditional parent/framework premises")
    observed = accepted["observed"]
    need(same(observed, count.read(execution / "supervisor-result.json", 4*MIB)), "Actual final supervisor result equals observed native record")
    need(observed["status"] == "completed" and type(observed["returncode"]) is int and observed["returncode"] == 0
         and observed["mode"] == "trusted_native" and observed["proof_accepted"] is False, "Successful exact native completion without a supervisor theorem claim")
    launch = count.read(execution / "native-launch.json", MIB)
    cpu = launch["cpu_seconds"]
    need(type(cpu) is int and 2 <= cpu <= 7200 and type(launch["wall_seconds"]) in (int, float)
         and math.isfinite(launch["wall_seconds"]) and 0 < launch["wall_seconds"] <= 7260
         and launch["mode"] == "trusted_native" and type(launch["memory_bytes"]) is int and launch["memory_bytes"] == 512*MIB
         and launch["checkpoint_paths"] == [] and launch["disk_bytes"] == 256*MIB and launch["log_bytes"] == 16*MIB,
         "Actual original bounded native launch policy")
    controller_cpu = min(30, max(1, cpu//10))
    need(launch["supervisor_memory_bytes"] == 64*MIB and launch["worker_memory_bytes"] == 448*MIB
         and launch["supervisor_cpu_seconds"] == controller_cpu and launch["worker_cpu_seconds"] == cpu-controller_cpu,
         "Complete512MiB and CPU split in the actual launch")
    argv = launch["argv"]
    need(type(argv) is list and len(argv) == 5 and argv[1:3] == ["-B", "-S"] and argv[-1] == "accept"
         and relative(argv[3], original) == (capsule / "count_protocol.py").relative_to(task)
         and relative(launch["cwd"], original) == capsule.relative_to(task)
         and relative(launch["output_dir"], original) == execution.relative_to(task), "Original exact command, working directory and output context")
    outer = count.read(execution / "launch.json", MIB)
    command = outer["argv"]
    need(type(command) is list and len(command) == 6 and command[:3] == argv[:3]
         and path_class(command[3])(command[3]).name == "linux_supervisor.py"
         and command[4] == "--_native-controller"
         and relative(command[5], original) == (execution / "native-launch.json").relative_to(task)
         and same(outer, dict(launch, argv=command)), "Actual original controller launch derives exactly from native launch")
    need(trusted_guard(observed, script_sha=count.digest(capsule / "count_protocol.py"),
         supervisor_sha=accepted["implementation"]["supervisor_sha256"], memory_bytes=512*MIB, cpu_seconds=cpu), "Established unchanged native platform capability")
    guard_files(execution, observed, launch, count.digest(capsule / "count_protocol.py"))
    for key in ("stdout", "stderr"):
        path = execution / (key + ".txt")
        need(relative(observed[key + "_path"], original) == path.relative_to(task)
             and path.is_file() and not path.is_symlink() and path.stat().st_size <= 16*MIB
             and count.digest(path) == observed[key + "_sha256"], "Actual captured bytes and original contained log context")
    need((execution / "stderr.txt").stat().st_size == 0, "Successful original native replay has empty stderr")
    stdout = (execution / "stdout.txt").read_text("utf-8")
    need(same(json.loads(stdout, object_pairs_hook=count.unique), receipt), "Actual complete native terminal JSON equals the accepted receipt")
    return dict(schema="REVALIDATED_N25_COUNT_V1", target=target, branch=target.split("-")[0], n=25, index=index,
                design_sha256=count.TARGETS[target][2], source_manifest_sha256=count.digest(capsule / "KERNEL_COPY_MANIFEST.json"),
                contract_sha256=count.digest(capsule / "contract.json"), forest_sha256=count.digest(forest_path),
                receipt_sha256=count.digest(receipt_path), census=census, statistics=statistics,
                accepted_capsule_relative=capsule.relative_to(task).as_posix(),
                accepted_report_relative=accepted_path.relative_to(task).as_posix(), accepted_report_sha256=count.digest(accepted_path),
                native_receipt_relative=receipt_path.relative_to(task).as_posix(), execution_relative=execution.relative_to(task).as_posix(),
                original_task_root=str(original), driver_sha256=count.digest(count.__file__),
                evidence_verifier_sha256=count.digest(__file__), supervisor_sha256=accepted["implementation"]["supervisor_sha256"],
                implementation=accepted["implementation"], conditional_premises=premises,
                evidence_sha256={p.relative_to(task).as_posix(): count.digest(p) for p in
                    [observed_path, execution / "native-launch.json", execution / "launch.json", execution / "supervisor-result.json",
                     execution / "native-worker-guard.json", execution / "native-controller-guard.json", execution / "native-controller-result.json",
                     execution / "stdout.txt", execution / "stderr.txt"]},
                native_arithmetic_accepted=True, parent_acquisitions_verified=False, all_index_conclusion_verified=False)


def validate_completed(task, *, original_task_root=None, expected_target=None):
    """Select the newest fully valid native acceptance in an exported task."""
    task = Path(task)
    need(task.is_dir() and not task.is_symlink(), "Ordinary restored count task")
    task = task.resolve()
    record = count.read(task / "TASK.json", 4*MIB)
    target = record["target"]
    need(type(target) is str and target in count.TARGETS and (expected_target is None or target == expected_target), "Exact expected count target")
    need(record["schema"] == "COUNT_TASK_V1" and record["scope"] == count.scope(target)
         and record["source_commit"] == count.COMMIT and record["design_sha256"] == count.TARGETS[target][2]
         and all(record[k] is False for k in ("arithmetic_accepted", "parent_acquisitions_verified", "all_index_conclusion_verified")), "Original unaccepted source task identity")
    implementation(record["implementation"])
    files = sealed(target, task / "capsule")
    need(type(record["prepared_source_files"]) is int and record["prepared_source_files"] == len(files), "Complete prepared source inventory")
    assets = {"old": count.ASSETS["old"]}
    if count.TARGETS[target][0] == "new-conditional-v14":
        need(count.PORTABLE_V14_PREPARER.is_file() and not count.PORTABLE_V14_PREPARER.is_symlink()
             and count.digest(count.PORTABLE_V14_PREPARER) == count.PORTABLE_V14_PREPARER_SHA256,
             "Unchanged reviewed portable V14 source producer")
        assets["base13"] = count.ASSETS["base13"]
        need(same(record["preparation_result"], count.read(task / "capsule/SOURCE_PREPARATION_REPORT.json", 4*MIB)), "Original portable preparation metadata retained without source aliases")
    need(same(record["source_archives"], assets), "Exact original public source-archive identities")
    candidates = []
    for path in task.glob("accept-*/NATIVE_ACCEPTED.json"):
        need(re.fullmatch(r"accept-[0-9a-f]{12}", path.parent.name) is not None and not path.parent.is_symlink(), "Ordinary literal acceptance epoch")
        candidates.append(path)
    candidates.sort(key=lambda p: p.stat().st_mtime_ns, reverse=True)
    failures = []
    for path in candidates:
        try:
            return validate_epoch(task, target, path.parent, original_task_root=original_task_root)
        except (ValueError, OSError, KeyError, TypeError, IndexError) as error:
            failures.append(path.parent.name + ": " + type(error).__name__ + ": " + str(error))
    raise ValueError("No fully revalidated completed native count acceptance; " + "; ".join(failures[:8]))
