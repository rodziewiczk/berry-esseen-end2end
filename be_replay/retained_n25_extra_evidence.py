"""Pure relocated evidence validation for the115 established extra retained counts.

No archived source is imported or executed. A successful stage establishes
fresh fixed-contract arithmetic only; the same-law parent acquisitions and
the analytic interpretation of its kernel remain explicit premises.
"""
from __future__ import annotations

import ast
import json
import math
from pathlib import Path
import re
import sys

from . import count_task as common, retained_n25_extra_sources as sources
from .count_recovery_evidence import trusted_guard
from .n25_count_evidence import (same, path_class, original_context, relative,
                                control_labels, guard_files)

MIB = 1024**2
MEMORY = 2*1024**3
SCOPE = "FRESH_RETAINED_N25_EXTRA_CONDITIONAL_COUNT_ONLY"
SCHEMA = "RETAINED_N25_EXTRA_NATIVE_EXECUTION_V1"
OBSERVED_FIELDS = {"schema", "job_id", "branch", "index", "scope", "epoch",
                   "observed", "census", "implementation", "arithmetic_accepted",
                   "parent_acquisitions_verified", "all_index_conclusion_verified"}
ACCEPTED_FIELDS = {"native_receipt", "native_receipt_sha256", "negative_controls", "conditional_premises"}
RECEIPT_FIELDS = {"status", "forest_sha256", "contract_sha256", "checker_sha256",
                  "kernel_sha256", "statistics", "negative_controls",
                  "fresh_leaf_evaluations", "seconds", "scope"}
PREMISES = [
    "Complete original simultaneous same-law count contract",
    "Exact predecessor, own-score and contact allowance stated by this literal contract",
    "Correct selected global/local INITIAL/resource acquisitions and resource-to-count interface",
    "Retained same-witness attainment/contact and physical count-kernel analytic implications",
]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def premises(job):
    result = list(PREMISES)
    result.append("Exact selected closed domain and parent interface for "+job["target_id"])
    if job['branch'] == 'b3' and job['index'] == 30:
        result.append("Separately acquired supplemental S1 resource interface")
    return result


def implementation():
    root = Path(__file__).resolve().parent
    return dict(retained_n25_sha256=common.digest(root/"retained_n25_extra.py"),
        source_adapter_sha256=common.digest(sources.__file__), catalog_sha256=sources.CATALOG_SHA256,
        geometry_helper_sha256=common.digest(sources.base.__file__),
        supervisor_sha256=common.digest(root/"linux_supervisor.py"),
        native_guard_verifier_sha256=common.digest(root/"count_recovery_evidence.py"),
        native_evidence_helpers_sha256=common.digest(root/"n25_count_evidence.py"),
        retained_evidence_sha256=common.digest(__file__), python=sys.version)


def _implementation(record):
    expected = implementation()
    need(type(record) is dict and set(record) == set(expected)
         and type(record["python"]) is str and record["python"]
         and all(same(record[k], expected[k]) for k in expected if k != "python"),
         "Current complete retained runner/source/evidence/supervisor implementation pins")


def _ordinary(path):
    path = Path(path)
    need(path.is_dir() and not path.is_symlink()
         and not (hasattr(path, "is_junction") and path.is_junction()), "Ordinary contained evidence directory")
    return path


def _context(task, epoch, observed, explicit):
    cls = path_class(observed["stdout_path"])
    path = cls(observed["stdout_path"])
    need(path.is_absolute() and path.name == "stdout.txt" and path.parent.name == "execution"
         and path.parent.parent.name == epoch.name, "Recorded stdout belongs to the exact native epoch")
    original = original_context(str(path.parent.parent), epoch.name, explicit)
    need(relative(str(path.parent.parent), original) == epoch.relative_to(task),
         "Recorded epoch maps to the restored task without rewriting its receipts")
    return original


def _literal_output(protocol):
    """Read two literal strings from the fixed accept AST, never evaluate it."""
    functions = [n for n in ast.parse(Path(protocol).read_bytes()).body
                 if isinstance(n, ast.FunctionDef) and n.name == "accept"]
    need(len(functions) == 1, "One unchanged native accept function")
    rows = [n.value for n in functions[0].body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "out" for t in n.targets)]
    need(len(rows) == 1 and isinstance(rows[0], ast.Call) and isinstance(rows[0].func, ast.Name)
         and rows[0].func.id == "dict", "Literal original native output contract")
    keywords = {k.arg: k.value for k in rows[0].keywords}
    result = {k: ast.literal_eval(keywords[k]) for k in ("status", "scope")}
    need(all(type(v) is str and v for v in result.values()), "Literal native scope and status")
    return result


def _sealed_clone(task, job, epoch):
    manifest = sources.verify(task)
    selected = [row for row in sources.jobs(job["branch"]) if row["job_id"] == job.get("job_id")]
    need(len(selected) == 1 and same(selected[0], job), "Exact fixed retained catalog job")
    rows = [row for row in manifest["jobs"] if row["job_id"] == job["job_id"]]
    need(manifest["branch"] == job["branch"] and len(rows) == 1,
         "Exact selected branch source manifest")
    row = rows[0]
    capsule = _ordinary(epoch/"capsule")
    source = _ordinary(task/job["capsule_relative"])
    expected = {item["filename"]: item for item in row["files"]}
    need(len(expected) == len(row["files"]) and job["acceptance_filename"] not in expected,
         "Unique sealed inputs exclude historical accepted receipts")
    for directory, extra in ((source, set()), (capsule, {job["acceptance_filename"]})):
        need({p.name for p in directory.iterdir()} == set(expected) | extra,
             "Complete source clone and exactly one fresh native receipt")
        for name, item in expected.items():
            path = directory/name
            need(path.is_file() and not path.is_symlink() and path.stat().st_size == item["bytes"]
                 and common.digest(path) == item["sha256"], "Actual sealed retained source/candidate bytes")
    return row, capsule


def validate_run(task, job, epoch, observed, census, *, original_task_root=None):
    """Validate completed native arithmetic before any acceptance ledger exists."""
    task, epoch = Path(task), Path(epoch)
    _ordinary(task); _ordinary(epoch)
    task, epoch = task.resolve(), epoch.resolve()
    need(epoch.parent == task and re.fullmatch(r"accept-[0-9a-f]{12,32}", epoch.name) is not None,
         "Direct task/accept-UUID native epoch")
    row, capsule = _sealed_clone(task, job, epoch)
    actual_census = sources.census(job, capsule)
    need(same(census, actual_census) and type(census["roots"]) is int and census["roots"] == 26
         and census["nodes"] == 2*census["leaves"]-26,
         "Entire selected closed26-root geometric census")
    receipt_path = capsule/job["acceptance_filename"]
    receipt = common.read(receipt_path, 4*MIB)
    need(type(receipt) is dict and set(receipt) == RECEIPT_FIELDS,
         "Complete exact original native receipt; no extra success claims")
    literal = _literal_output(capsule/"count_protocol.py")
    need(literal["status"] == "PASS_FRESH_CONDITIONAL_EXACT_COUNT"+str(job["index"])
         and all(same(receipt[k], v) for k, v in literal.items()), "Exact original native status and conditional scope")
    for key, name in (("forest_sha256", job["forest_filename"]), ("contract_sha256", "contract.json"),
                      ("checker_sha256", "count_protocol.py")):
        need(receipt[key] == common.digest(capsule/name), "Native receipt binds actual fixed inputs")
    kernel = common.read(capsule/job["manifest_filename"], 16*MIB)["files"]
    need(same(receipt["kernel_sha256"], kernel)
         and all(common.digest(capsule/name) == pin for name, pin in kernel.items()),
         "Every unchanged mathematical kernel byte is bound")
    statistics = {k: census[k] for k in ("nodes", "leaves", "closed_statuses", "maximum_score", "maximum_depth")}
    need(same(receipt["statistics"], statistics) and type(receipt["fresh_leaf_evaluations"]) is int
         and receipt["fresh_leaf_evaluations"] == census["leaves"], "Every selected leaf freshly checked with exact statistics")
    need(same(receipt["negative_controls"], control_labels(capsule/"count_protocol.py")),
         "All24 original corruption controls in their exact order")
    need(type(receipt["seconds"]) in (int, float) and math.isfinite(receipt["seconds"])
         and receipt["seconds"] >= 0, "Finite nonnegative native elapsed time")
    execution = _ordinary(epoch/"execution")
    need(type(observed) is dict and same(observed, common.read(execution/"supervisor-result.json", 4*MIB)),
         "Actual completed supervisor result equals the captured observation")
    need(observed["status"] == "completed" and type(observed["returncode"]) is int
         and observed["returncode"] == 0 and observed["mode"] == "trusted_native"
         and observed["proof_accepted"] is False, "Successful trusted native completion without a supervisor theorem claim")
    original = _context(task, epoch, observed, original_task_root)
    launch = common.read(execution/"native-launch.json", MIB)
    cpu, wall = launch["cpu_seconds"], launch["wall_seconds"]
    need(type(cpu) is int and 2 <= cpu <= 43200 and type(wall) in (int, float)
         and math.isfinite(wall) and 0 < wall <= 43500 and launch["mode"] == "trusted_native"
         and type(launch["memory_bytes"]) is int and launch["memory_bytes"] == MEMORY
         and launch["checkpoint_paths"] == [] and type(launch["disk_bytes"]) is int
         and launch["disk_bytes"] == 256*MIB and type(launch["log_bytes"]) is int
         and launch["log_bytes"] == 16*MIB, "Exact bounded2GiB native execution policy")
    controller_cpu = min(30, max(1, cpu//10))
    need(all(type(launch[k]) is int and launch[k] == v for k, v in dict(
        supervisor_memory_bytes=64*MIB, worker_memory_bytes=MEMORY-64*MIB,
        supervisor_cpu_seconds=controller_cpu, worker_cpu_seconds=cpu-controller_cpu).items()),
        "Complete worker/controller memory and CPU split")
    argv = launch["argv"]
    need(type(argv) is list and len(argv) == 5 and all(type(x) is str for x in argv)
         and path_class(argv[0])(argv[0]).is_absolute() and argv[1:3] == ["-B", "-S"] and argv[-1] == "accept"
         and relative(argv[3], original) == (capsule/"count_protocol.py").relative_to(task)
         and relative(launch["cwd"], original) == capsule.relative_to(task)
         and relative(launch["output_dir"], original) == execution.relative_to(task),
         "Exact unchanged native command and original contained execution context")
    outer = common.read(execution/"launch.json", MIB)
    command = outer["argv"]
    need(type(command) is list and len(command) == 6 and command[:3] == argv[:3]
         and type(command[3]) is str and path_class(command[3])(command[3]).is_absolute()
         and path_class(command[3])(command[3]).name == "linux_supervisor.py"
         and command[4] == "--_native-controller"
         and relative(command[5], original) == (execution/"native-launch.json").relative_to(task)
         and same(outer, dict(launch, argv=command)), "Exact real controller-launch derivation")
    supervisor_sha = common.digest(Path(__file__).with_name("linux_supervisor.py"))
    need(trusted_guard(observed, script_sha=receipt["checker_sha256"], supervisor_sha=supervisor_sha,
                       memory_bytes=MEMORY, cpu_seconds=cpu), "Established unchanged Linux native capability")
    guard_files(execution, observed, launch, receipt["checker_sha256"])
    for key in ("stdout", "stderr"):
        path = execution/(key+".txt")
        need(relative(observed[key+"_path"], original) == path.relative_to(task)
             and path.is_file() and not path.is_symlink() and path.stat().st_size <= 16*MIB
             and common.digest(path) == observed[key+"_sha256"], "Actual bounded captured bytes and hashes")
    need((execution/"stderr.txt").stat().st_size == 0, "Empty bound native stderr")
    stdout = (execution/"stdout.txt").read_text("utf-8")
    need(same(json.loads(stdout, object_pairs_hook=common.unique), receipt),
         "Full actual terminal JSON equals the complete fresh native receipt")
    return receipt


def validate_stage(task, job, epoch, *, original_task_root=None):
    """Revalidate a completed stage after arbitrary safe task relocation."""
    task, epoch = _ordinary(task).resolve(), Path(epoch)
    before_path, accepted_path = epoch/"NATIVE_OBSERVED.json", epoch/"NATIVE_ACCEPTED.json"
    before, accepted = common.read(before_path, 4*MIB), common.read(accepted_path, 4*MIB)
    need(type(before) is dict and set(before) == OBSERVED_FIELDS
         and type(accepted) is dict and set(accepted) == OBSERVED_FIELDS | ACCEPTED_FIELDS,
         "Exact retained observed-to-accepted ledger schema")
    need(before["schema"] == SCHEMA and before["job_id"] == job["job_id"] and before["branch"] == job["branch"]
         and type(before["index"]) is int and before["index"] == job["index"] and before["scope"] == SCOPE
         and before["arithmetic_accepted"] is False and accepted["arithmetic_accepted"] is True
         and all(before[k] is False and accepted[k] is False for k in
                 ("parent_acquisitions_verified", "all_index_conclusion_verified"))
         and all(same(before[k], accepted[k]) for k in before if k != "arithmetic_accepted"),
         "Only the validated conditional-arithmetic flag changes")
    _implementation(before["implementation"])
    original = original_context(before["epoch"], epoch.name, original_task_root)
    need(relative(before["epoch"], original) == epoch.resolve().relative_to(task), "Recorded original epoch maps exactly")
    receipt = validate_run(task, job, epoch, before["observed"], before["census"], original_task_root=str(original))
    native = epoch/"capsule"/job["acceptance_filename"]
    need(type(accepted["negative_controls"]) is int and accepted["negative_controls"] == 24
         and accepted["native_receipt_sha256"] == common.digest(native)
         and relative(accepted["native_receipt"], original) == native.relative_to(task)
         and same(accepted["conditional_premises"], premises(job)), "Actual fresh native receipt and all explicit conditional premises")
    paths = [before_path, accepted_path, native] + [epoch/"execution"/n for n in (
        "native-launch.json", "launch.json", "supervisor-result.json", "native-worker-guard.json",
        "native-controller-guard.json", "native-controller-result.json", "stdout.txt", "stderr.txt")]
    return dict(schema="REVALIDATED_RETAINED_N25_EXTRA_STAGE_V1", job_id=job["job_id"], branch=job["branch"],
        index=job["index"], n=25, scope=SCOPE, census=before["census"], statistics=receipt["statistics"],
        p_interval=job.get("p_interval"), rho_interval=job.get("rho_interval"),
        source_design_sha256=common.digest(epoch/"capsule"/sources.EPOCH),
        forest_sha256=receipt["forest_sha256"], contract_sha256=receipt["contract_sha256"],
        checker_sha256=receipt["checker_sha256"], negative_controls=24,
        accepted_report_relative=accepted_path.relative_to(task).as_posix(),
        native_receipt_relative=native.relative_to(task).as_posix(), native_receipt_sha256=common.digest(native),
        source_manifest_sha256=common.digest(task/sources.MANIFEST), implementation=before["implementation"],
        original_task_root=str(original), evidence_sha256={p.relative_to(task).as_posix(): common.digest(p) for p in paths},
        conditional_premises=premises(job), native_arithmetic_accepted=True,
        parent_acquisitions_verified=False, all_index_conclusion_verified=False)
