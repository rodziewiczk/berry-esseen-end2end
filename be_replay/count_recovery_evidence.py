"""Read-only relocated evidence for seven pinned resource-limit source epochs.

Only LIMIT changes from10000 to100000 in a new sealed source epoch. Original
contracts/kernels/closed roots/depth128/strict target/24 controls stay unchanged.
This module never imports or evaluates an archived mathematical kernel.
"""
from __future__ import annotations
import json
import hashlib
import math
from pathlib import Path
import re

from . import count_task as count, count_limit_epoch as limit
from . import count_implementation_history as history
from .n25_count_evidence import (same, path_class, original_context, relative,
    control_labels, full_statistics, guard_files, OBSERVED_FIELDS, ACCEPTED_FIELDS, PREMISES)

MIB = count.MIB
TARGET = "b4-q2"
SCOPE = "NEW_RESOURCE_LIMIT_EPOCH_CONDITIONAL_COUNT_ONLY"
# The one previously published q2 pair (commit3c10084). No open-ended source
# history is accepted. The complete pre-PREFIX2 tuple is also retained for all
# seven targets, so discovery upgrades do not invalidate completed exports.
LEGACY_Q2_IMPLEMENTATION = {
    "count_recovery_sha256": "d43057eb2f5fbf41466b74ac030491a93b72d1481cd22a3114332623b7ca64c0",
    "count_limit_epoch_sha256": "9dc980c2e23580feb9402f9f15c533cc76582808656cc7c23b1b3fc37b5082dc",
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def recovery_path():
    path = Path(__file__).with_name("count_recovery.py")
    need(path.is_file() and not path.is_symlink(), "Actual recovery implementation source")
    return path


def resource_epoch(target=TARGET, *, native_memory_bytes=2 * 1024**3):
    profile = limit.profile(target)
    need(type(native_memory_bytes) is int and native_memory_bytes in (512*MIB, 2*1024**3),
         "One explicit reviewed native memory policy")
    result = dict(schema="FIXED_B4_Q2_RESOURCE_LIMIT_EPOCH_V1" if target == TARGET else "N25_COUNT_RESOURCE_LIMIT_EPOCH_V1",
        node_limit=100000, original_node_limit=10000, maximum_depth=128,
        original_design_sha256=profile["original_design_sha256"],
        new_design_sha256=profile["new_design_sha256"], contract_and_mathematical_kernels_unchanged=True,
        native_memory_bytes=native_memory_bytes)
    if target != TARGET:
        result.update(target=target, index=profile["index"])
    return result


def implementation(record, target=TARGET):
    expected = dict(count.implementation(), count_recovery_sha256=count.digest(recovery_path()),
                    count_limit_epoch_sha256=count.digest(limit.__file__))
    need(type(record) is dict and set(record) == set(expected)
         and type(record["python"]) is str and record["python"], "Complete recovery implementation context")
    current = all(same(record[k], expected[k]) for k in expected if k != "python")
    midpoint = history.matches(record, history.recovery())
    legacy_q2 = target == TARGET and history.matches(record, history.recovery(legacy_q2=True))
    need(current or midpoint or legacy_q2,
         "One complete current, published midpoint, or explicitly published q2 implementation")


def memory_policy(record, target):
    implementation(record["implementation"], target)
    legacy = target == TARGET and all(record["implementation"][k] == v
                                     for k, v in LEGACY_Q2_IMPLEMENTATION.items())
    memory = record.get("native_memory_bytes", 512*MIB if legacy else None)
    need(type(memory) is int and memory == (512*MIB if legacy else 2*1024**3),
         "Explicit2GiB current native policy, or the sole published512MiB q2 policy")
    return memory


def budget_policy(record, target, cpu_seconds, wall_seconds):
    """Current epochs permit12 CPU hours; the sole legacy profile stays fixed."""
    memory = memory_policy(record, target)
    cpu_max, wall_max = (7200, 7260) if memory == 512*MIB else (43200, 43500)
    need(type(cpu_seconds) is int and 2 <= cpu_seconds <= cpu_max
         and type(wall_seconds) in (int, float) and math.isfinite(wall_seconds)
         and 0 < wall_seconds <= wall_max, "Native CPU/wall policy for this exact implementation epoch")
    for field, actual in (("native_cpu_seconds", cpu_seconds), ("native_wall_seconds", wall_seconds)):
        if field in record:
            declared = record[field]
            need(type(declared) in ((int,) if field == "native_cpu_seconds" else (int, float))
                 and declared == actual, "Actual native launch matches the explicitly declared task budget")
    return cpu_max, wall_max


def trusted_guard(result, *, script_sha, supervisor_sha, memory_bytes, cpu_seconds):
    """New exact resource policy; never weaken or patch an original helper.

    The caller must separately establish the2GiB current/512MiB legacy identity
    and verify actual guard sidecars/captures. The supervisor accepts no maths.
    """
    if (type(memory_bytes) is not int or memory_bytes not in (512*MIB, 2*1024**3)
            or type(cpu_seconds) is not int or not 2 <= cpu_seconds <= (7200 if memory_bytes == 512*MIB else 43200)
            or type(script_sha) is not str or type(supervisor_sha) is not str
            or type(result) is not dict or result.get("status") != "completed"
            or type(result.get("returncode")) is not int or result["returncode"] != 0
            or result.get("mode") != "trusted_native" or result.get("proof_accepted") is not False):
        return False
    scope = result.get("guard_scope")
    if type(scope) is not dict:
        return False
    controller_cpu = min(30, max(1, cpu_seconds // 10))
    caps = dict(hard_sum_RLIMIT_AS_bytes=memory_bytes,
        worker_RLIMIT_AS_bytes=memory_bytes-64*MIB, supervisor_RLIMIT_AS_bytes=64*MIB,
        hard_sum_RLIMIT_CPU_seconds=cpu_seconds, supervisor_RLIMIT_CPU_seconds=controller_cpu,
        worker_RLIMIT_CPU_seconds=cpu_seconds-controller_cpu)
    return (scope.get("kind") == "LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1"
        and scope.get("capability_established") is True
        and scope.get("native_python_execution") is True
        and all(type(scope.get(k)) is int and scope[k] == v for k, v in caps.items())
        and scope.get("script_sha256") == script_sha
        and scope.get("supervisor_source_sha256") == supervisor_sha)


def sealed(target, capsule, *, native=False):
    profile = limit.profile(target)
    files = limit.verify(target, capsule)
    allowed = set(files) | {"FROZEN_DESIGN.json"}
    if native:
        allowed |= {f"COUNT{profile['index']}_FOREST.json", f"COUNT{profile['index']}_ACCEPTED.json"}
    actual = set()
    for path in Path(capsule).iterdir():
        need(path.is_file() and not path.is_symlink(), "Flat sealed recovery capsule")
        actual.add(path.name)
    need(actual == allowed, "Complete fixed new design capsule without unlisted outputs")
    return files


def source_and_migration(task, record, files):
    """Verify the preserved source epoch and untrusted checkpoint migration."""
    from . import count_recovery as recovery
    target = record["target"]
    profile = limit.profile(target)
    original = task / "original-capsule"
    need(original.is_dir() and not original.is_symlink(), "Ordinary preserved original source capsule")
    original_files = count.verify_capsule(target, original)
    need({p.name for p in original.iterdir()} == set(original_files) | {"FROZEN_DESIGN.json"}
         and all(p.is_file() and not p.is_symlink() for p in original.iterdir()),
         "Only exact original source files in the preserved original capsule")
    metadata = limit.metadata(target)
    source_epoch = dict(schema="N25_COUNT_LIMIT_SOURCE_BUILD_V1", target=target, scope=metadata["scope"],
        original_design_sha256=profile["original_design_sha256"], design_sha256=profile["new_design_sha256"],
        checker_sha256=profile["checker_sha256"], contract_sha256=profile["contract_sha256"], files=len(files),
        source_adapter_sha256=record["implementation"]["count_limit_epoch_sha256"],
        resource_epoch=count.read(task / "capsule" / limit.EPOCH, MIB), arithmetic_accepted=False,
        parent_acquisitions_verified=False, all_index_conclusion_verified=False)
    need(same(record["source_epoch"], source_epoch), "Exact source-only build report and sealed epoch")
    need(same(source_epoch["resource_epoch"], metadata), "Exact target-specific sealed resource metadata")
    need(same(record["source_provenance"], dict(source_design_sha256=profile["original_design_sha256"],
        copied_source_files=len(original_files), historical_receipts_copied=False)),
        "Original source provenance without historical acceptance inputs")
    before = count.read(task / "SOURCE_CHECKPOINT.json")
    after = count.read(task / "INPUT_CHECKPOINT.json")
    if before["binding"]["design_sha256"] == profile["original_design_sha256"]:
        expected = limit.migrate_checkpoint(before, original, task / "capsule", target=target)
    else:
        recovery.check_extended_checkpoint(before, task / "capsule", target=target)
        expected = before
    restored = record.get("migration", {}).get("migration_type") == recovery.MIGRATION_TYPE
    if restored:
        need(record["implementation"]["count_recovery_sha256"] == count.digest(recovery_path())
             and record["implementation"]["count_limit_epoch_sha256"] == count.digest(limit.__file__),
             "The explicit PREFIX2 migration belongs to its current reviewed implementation")
        expected = recovery.migrate_discovery_checkpoint(expected, task / "capsule", target)
    need(same(expected, after), "Only reviewed resource and explicitly recorded discovery bindings migrate")
    statistics = recovery.check_extended_checkpoint(after, task / "capsule", target=target,
        **({"require_restored": True} if restored else {}))
    migration = dict(source_checkpoint_sha256=count.digest(task / "SOURCE_CHECKPOINT.json"),
        source_checkpoint_bytes=(task / "SOURCE_CHECKPOINT.json").stat().st_size,
        source_design_sha256=before["binding"]["design_sha256"], execution_design_sha256=profile["new_design_sha256"],
        roots_sha256=hashlib.sha256(json.dumps(before["roots"], sort_keys=True,
            separators=(",", ":")).encode()).hexdigest(), roots_preserved=same(before["roots"], after["roots"]),
        arithmetic_accepted=False, statistics=statistics)
    if restored:
        declared = record["migration"]
        source = original if before["binding"]["design_sha256"] == profile["original_design_sha256"] else task / "capsule"
        before_statistics = limit.checkpoint_geometry(before, source, target,
            node_limit=10000 if source == original else 100000)
        source_path = declared.get("source_checkpoint_path")
        need(type(source_path) is str and source_path and path_class(source_path)(source_path).is_absolute(),
             "Recorded absolute source checkpoint location")
        rejected = declared.get("rejected_checkpoints")
        need(type(rejected) is list and len(rejected) <= 100000
             and all(type(row) is dict and set(row) == {"path", "error"}
                     and type(row["path"]) is str and type(row["error"]) is str for row in rejected),
             "Bounded cache diagnostics remain explicitly recorded provenance")
        migration.update(migration_type=recovery.MIGRATION_TYPE, source_checkpoint_path=source_path,
            source_strategy=recovery._strategy(before["binding"]), target_strategy=recovery.discovery_binding(),
            source_binding_sha256=hashlib.sha256(limit.canonical(before["binding"])).hexdigest(),
            execution_binding_sha256=hashlib.sha256(limit.canonical(after["binding"])).hexdigest(),
            input_checkpoint_sha256=count.digest(task / "INPUT_CHECKPOINT.json"),
            before_statistics=before_statistics, after_statistics=statistics,
            resource_epoch_migrated=before["binding"]["design_sha256"] != after["binding"]["design_sha256"],
            rejected_checkpoints=rejected)
        need(before_statistics == statistics, "Lossless PREFIX2 migration preserves the complete saved census")
    need(migration["roots_preserved"] is True and same(record["migration"], migration),
         "Preserved original candidate bytes and complete explicitly untrusted migration ledger")


def validate_epoch(task, target, epoch, *, original_task_root=None):
    profile = limit.profile(target)
    task_record = count.read(task / "TASK.json", 4*MIB)
    memory = memory_policy(task_record, target)
    accepted_path = epoch / "NATIVE_ACCEPTED.json"
    accepted = count.read(accepted_path, 4*MIB)
    observed_path = epoch / "NATIVE_OBSERVED.json"
    before = count.read(observed_path, 4*MIB)
    need(set(before) == OBSERVED_FIELDS and set(accepted) == OBSERVED_FIELDS | ACCEPTED_FIELDS,
         "Exact observed-to-accepted native execution protocol")
    need(before["schema"] == "COUNT_LIMIT_RECOVERY_EXECUTION_V1" and before["target"] == target
         and before["scope"] == SCOPE and before["arithmetic_accepted"] is False
         and accepted["arithmetic_accepted"] is True
         and all(before[k] is False and accepted[k] is False for k in ("parent_acquisitions_verified", "all_index_conclusion_verified"))
         and all(same(before[k], accepted[k]) for k in before if k != "arithmetic_accepted"),
         "Preserved original unaccepted observation and sole validated acceptance transition")
    implementation(accepted["implementation"], target)
    need(same(accepted["implementation"], task_record["implementation"]),
         "Native execution and source task have one exact implementation context")
    original = original_context(accepted["epoch"], epoch.name, original_task_root)
    need(relative(accepted["epoch"], original) == epoch.relative_to(task), "Recorded accept epoch is this restored epoch")
    capsule, execution = epoch / "capsule", epoch / "execution"
    files = sealed(target, capsule, native=True)
    need(same(files, sealed(target, task / "capsule")), "Same exact sealed source design in source and acceptance clone")
    index = count.TARGETS[target][1]
    forest_path, receipt_path = capsule / f"COUNT{index}_FOREST.json", capsule / f"COUNT{index}_ACCEPTED.json"
    forest, receipt = count.read(forest_path), count.read(receipt_path, 4*MIB)
    census = limit.forest_census(forest, target, capsule)
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
    budget_policy(task_record, target, cpu, launch["wall_seconds"])
    need(launch["mode"] == "trusted_native" and type(launch["memory_bytes"]) is int and launch["memory_bytes"] == memory
         and launch["checkpoint_paths"] == [] and launch["disk_bytes"] == 256*MIB and launch["log_bytes"] == 16*MIB,
         "Actual original bounded native launch policy")
    controller_cpu = min(30, max(1, cpu//10))
    need(launch["supervisor_memory_bytes"] == 64*MIB and launch["worker_memory_bytes"] == memory-64*MIB
         and launch["supervisor_cpu_seconds"] == controller_cpu and launch["worker_cpu_seconds"] == cpu-controller_cpu,
         "Complete declared memory and CPU split in the actual launch")
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
         supervisor_sha=accepted["implementation"]["supervisor_sha256"], memory_bytes=memory, cpu_seconds=cpu), "Established unchanged native platform capability")
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
                design_sha256=profile["new_design_sha256"], new_design_sha256=profile["new_design_sha256"],
                original_design_sha256=profile["original_design_sha256"], native_memory_bytes=memory,
                native_cpu_seconds=cpu, native_wall_seconds=launch["wall_seconds"],
                resource_epoch=resource_epoch(target, native_memory_bytes=memory), source_manifest_sha256=count.digest(capsule / "KERNEL_COPY_MANIFEST.json"),
                source_resource_epoch=count.read(capsule / limit.EPOCH, MIB),
                contract_sha256=count.digest(capsule / "contract.json"), forest_sha256=count.digest(forest_path),
                receipt_sha256=count.digest(receipt_path), census=census, statistics=statistics,
                accepted_capsule_relative=capsule.relative_to(task).as_posix(),
                accepted_report_relative=accepted_path.relative_to(task).as_posix(), accepted_report_sha256=count.digest(accepted_path),
                native_receipt_relative=receipt_path.relative_to(task).as_posix(), execution_relative=execution.relative_to(task).as_posix(),
                original_task_root=str(original), driver_sha256=accepted["implementation"]["count_recovery_sha256"],
                evidence_verifier_sha256=count.digest(__file__), supervisor_sha256=accepted["implementation"]["supervisor_sha256"],
                implementation=accepted["implementation"], conditional_premises=premises,
                evidence_sha256={p.relative_to(task).as_posix(): count.digest(p) for p in
                    [task / "TASK.json", task / "SOURCE_CHECKPOINT.json", task / "INPUT_CHECKPOINT.json",
                     observed_path, execution / "native-launch.json", execution / "launch.json", execution / "supervisor-result.json",
                     execution / "native-worker-guard.json", execution / "native-controller-guard.json", execution / "native-controller-result.json",
                     execution / "stdout.txt", execution / "stderr.txt"]},
                native_arithmetic_accepted=True, parent_acquisitions_verified=False, all_index_conclusion_verified=False)


def validate_completed(task, *, original_task_root=None, expected_target=None):
    """Accept the matching pinned epoch and its complete native execution chain."""
    task = Path(task)
    need(task.is_dir() and not task.is_symlink(), "Ordinary restored recovery task")
    task = task.resolve()
    record = count.read(task / "TASK.json", 4*MIB)
    target = record["target"]
    need(type(target) is str and target in count.TARGETS, "One reviewed logical count target")
    profile = limit.profile(target)
    need(record["schema"] == "COUNT_LIMIT_RECOVERY_TASK_V1"
         and (expected_target is None or expected_target == target), "Exact recovery task identity")
    need(record["scope"] == SCOPE and record["source_commit"] == count.COMMIT
         and record["original_design_sha256"] == profile["original_design_sha256"]
         and record["design_sha256"] == profile["new_design_sha256"]
         and all(record[k] is False for k in ("arithmetic_accepted", "parent_acquisitions_verified", "all_index_conclusion_verified")),
         "Explicit new resource epoch, original design and false acquisition/global flags")
    need(type(record["node_limit"]) is int and record["node_limit"] == 100000
         and type(record["original_node_limit"]) is int and record["original_node_limit"] == 10000,
         "Fixed original and enlarged finite node limits")
    implementation(record["implementation"], target)
    memory_policy(record, target)
    files = sealed(target, task / "capsule")
    need(type(record["prepared_source_files"]) is int and record["prepared_source_files"] == len(files),
         "Complete recovery prepared source inventory")
    archives = {"old": count.ASSETS["old"]}
    if count.TARGETS[target][0] == "new-conditional-v14":
        archives["base13"] = count.ASSETS["base13"]
    need(same(record["source_archives"], archives), "Exact original pinned source archives")
    source_and_migration(task, record, files)
    candidates = []
    for path in task.glob("accept-*/NATIVE_ACCEPTED.json"):
        need(re.fullmatch(r"accept-[0-9a-f]{12}", path.parent.name) is not None
             and not path.parent.is_symlink(), "Ordinary literal recovery acceptance epoch")
        candidates.append(path)
    candidates.sort(key=lambda p: (p.stat().st_mtime_ns, p.parent.name), reverse=True)
    failures = []
    for path in candidates:
        try:
            return validate_epoch(task, target, path.parent, original_task_root=original_task_root)
        except (ValueError, OSError, KeyError, TypeError, IndexError) as error:
            failures.append(path.parent.name + ": " + type(error).__name__ + ": " + str(error))
    raise ValueError("No fully revalidated completed recovery acceptance; " + "; ".join(failures[:8]))


validate_export = validate_completed
