"""Pure source, capture and parent-edge validation for lower-B5 global parents.

No archived kernel is imported. BASIC execution is reported literally: it has
per-process limits and a sampled process-group watchdog, without native proof
acceptance or a whole-tree hard resource contract.
"""
from __future__ import annotations

import math
from pathlib import Path

from . import aux24_evidence as paths, count_task as common
from . import n25_b5_global_sources as sources

MIB = 1024**2
MEMORY = 2*1024**3
CPU = WALL = 64800
DISK = 512*MIB
need = sources.need
same = paths.same


def implementation():
    base = Path(__file__).resolve().parent
    return {name: common.digest(base/name) for name in (
        "n25_b5_global.py", "n25_b5_global_sources.py",
        "n25_b5_global_evidence.py",
        "aux24_sources.py", "aux24_evidence.py", "linux_supervisor.py",
        "count_task.py", "colab_batch.py", "small_indices.py")}


def root(task):
    return Path(task)/"epoch"/sources.source.PREFIX.rstrip("/")


def outputs(branch, count):
    result = set()
    for stage in sources.stages(branch)[:count]:
        prefix = stage["folder"]+"/"
        result.add(prefix+stage["receipt"])
    return result


def progress_files(branch):
    result = set()
    for stage in sources.stages(branch):
        filename = "PROGRESS_accept.json" if stage["kind"] == "initial" else "PROGRESS.json"
        result.add(stage["folder"]+"/"+filename)
    return result


def verify_epoch(task, branch, count, *, progress=True):
    sources.verify(task, branch)
    base = root(task)
    need(base.is_dir() and not base.is_symlink(), "Existing ordinary acquisition epoch")
    sealed = sources.selected(branch)
    immutable = {n.removeprefix(sources.source.PREFIX): r for n, r in sealed.items()}
    derived = outputs(branch, count)
    allowed = set(immutable) | derived | (progress_files(branch) if progress else set())
    actual = set()
    for path in base.rglob("*"):
        need(not path.is_symlink() and not (hasattr(path, "is_junction") and path.is_junction()),
             "No link in acquisition epoch")
        if path.is_file():
            name = path.relative_to(base).as_posix()
            need(name in allowed, "Only selected sources and named current outputs: "+name)
            actual.add(name)
            if name in immutable:
                row = immutable[name]
                need(path.stat().st_size == row["bytes"] and common.digest(path) == row["sha256"],
                     "Unchanged complete selected source/candidate: "+name)
            else:
                need(path.stat().st_size <= 128*MIB, "Bounded fresh output")
    need(set(immutable) | derived <= actual, "All sealed inputs and completed outputs exist")
    return base


def read(base, name):
    return common.read(base/name, 128*MIB)


def _bindings(base, mapping):
    need(type(mapping) is dict and mapping, "Nonempty complete binding map")
    for name, pin in mapping.items():
        path = base/paths.relative(name)
        need(path.is_file() and not path.is_symlink() and common.digest(path) == pin,
             "Actual fresh parent/source binding: "+name)


def _cover(cover):
    need(type(cover["total"]) is int and cover["total"] == 18432
         and type(cover["active"]) is int and type(cover["excluded"]) is int
         and cover["active"] >= 0 and cover["excluded"] >= 0
         and cover["active"]+cover["excluded"] == 18432,
         "Every signed INITIAL rectangle accounted exactly once")


def artifact(task, branch, stage):
    parent = sources.definition(branch)
    base = root(task)
    folder = base/stage["folder"]
    proof = read(folder, stage["proof"])
    need(same(proof["profile"], parent["profile"]), "Literal fixed n25 sharp profile")
    frozen = read(folder, "FROZEN_SOURCES.json")
    expected_sources = (dict(frozen, **{"FROZEN_SOURCES.json": common.digest(folder/"FROZEN_SOURCES.json")})
                        if stage["kind"] == "global_resource" else frozen)
    need(same(proof["source_sha256"], expected_sources), "Exact full original proof source keyset and hashes")
    need(stage["action"] == "accept" and stage["kind"] in ("initial", "global_resource"), "Only two full unchanged global acceptances")
    receipt = read(folder, stage["receipt"])
    checker = parent[stage["kind"]]["checker"]["member"].split("/")[-1]
    need(receipt["proof_sha256"] == common.digest(folder/stage["proof"])
         and receipt["checker_sha256"] == common.digest(folder/checker)
         and same(receipt["profile"], parent["profile"]), "Exact fresh accepted proof/checker/profile binding")
    controls = parent[stage["kind"]]["controls"]
    need(same(receipt["negative_controls"], controls), "Every original corruption control in fixed order")
    _bindings(folder, receipt["source_sha256"])
    need(same(receipt["source_sha256"], proof["source_sha256"]), "Same complete accepted source closure")
    if stage["kind"] == "initial":
        need(receipt["status"] == "PASS_FRESH_EXACT_INITIAL25_"+branch.upper()
             and type(receipt["signed_rectangles"]) is int and receipt["signed_rectangles"] == 239616
             and type(receipt["probability_panels"]) is int and receipt["probability_panels"] == 100
             and type(proof["maximum_covers"]) is int and proof["maximum_covers"] == 12 and len(proof["stages"]) == 12,
             "Complete unseeded twelve-step feedback and thirteenth export cover")
        for item in proof["stages"]:
            _cover(item["cover"])
        _cover(proof["export"])
        need(len(proof["export"]["panels"]) == 100, "Complete original probability export")
        # This exact deterministic receipt is independently reconstructed in the
        # source audit; the archived receipt itself is never a task input.
        need(common.digest(folder/stage["receipt"]) == parent["initial"]["historical_acceptance"]["sha256"],
             "Fresh deterministic INITIAL receipt supports unchanged resource candidate")
    elif stage["kind"] == "global_resource":
        initial = base/parent["initial"]["directory"].removeprefix(sources.source.PREFIX)
        for key, name in (("parent_proof_sha256", "INITIAL25_"+branch.upper()+"_PROOF.json"),
                          ("parent_acceptance_sha256", "INITIAL25_"+branch.upper()+"_ACCEPTED.json")):
            need(receipt[key] == proof[key] == common.digest(initial/name), "Resource uses freshly accepted INITIAL")
        need(receipt["status"] == "PASS_FRESH_EXACT_SHARP25_"+branch.upper()+"_GLOBAL_RESOURCES"
             and type(receipt["probability_panels"]) is int and receipt["probability_panels"] == 100
             and len(proof["rows"]) == 100, "Complete all100 probability-panel resource acquisition")
        for i, row in enumerate(proof["rows"]):
            need(type(row["index"]) is int and row["index"] == i
                 and type(row["result"]["excluded"]) is bool, "Typed complete ordered resource cover")
        for flag, key in ((False, "surviving_panels"), (True, "excluded_panels")):
            need(same(receipt[key], [r["index"] for r in proof["rows"] if r["result"]["excluded"] is flag])
                 and same(receipt[key], parent["global_resource"][key]), "Exact fixed resource dispositions")
        seconds = receipt["seconds"]
        need(type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0,
             "Finite nonnegative measured resource time")
    return dict(kind=stage["kind"], action=stage["action"], proof_sha256=common.digest(folder/stage["proof"]),
                receipt_sha256=common.digest(folder/stage["receipt"]) if receipt else None,
                conditional_arithmetic_replayed=receipt is not None,
                native_arithmetic_accepted=False, all_index_conclusion_verified=False)


def transport(task, branch, stage, report):
    task = Path(task).resolve()
    original = paths.original_path(report["original_task_root"])
    execution = "execution/"+stage["name"]
    launch = paths.read(task, execution+"/launch.json")
    observed = paths.read(task, execution+"/supervisor-result.json")
    need(same(observed, report["observed"]) and observed["status"] == "completed"
         and type(observed["returncode"]) is int and observed["returncode"] == 0
         and observed["reason"] is None and observed["mode"] == "untrusted_search"
         and observed["proof_accepted"] is False and type(observed["sample_count"]) is int
         and observed["sample_count"] > 0, "Completed actual BASIC observation")
    cwd = "epoch/"+sources.source.PREFIX+stage["folder"]
    argv = launch["argv"]
    need(type(argv) is list and len(argv) == 4+len(stage["args"])
         and paths.original_path(argv[0]).is_absolute() and argv[1:3] == ["-B", "-S"]
         and paths.mapped(argv[3], original) == cwd+"/"+stage["script"]
         and argv[4:] == stage["args"] and paths.mapped(launch["cwd"], original) == cwd
         and paths.mapped(launch["output_dir"], original) == execution,
         "Exact original command and contained relocated context")
    expected = dict(argv=argv, cwd=launch["cwd"], output_dir=launch["output_dir"],
        mode="untrusted_search", wall_seconds=float(WALL), cpu_seconds=CPU, memory_bytes=MEMORY,
        checkpoint_paths=[], disk_bytes=DISK, log_bytes=16*MIB, sample_seconds=.2, heartbeat_seconds=20.)
    need(same(launch, expected) and same(observed["guard_scope"], paths._group_scope(launch)),
         "Exact18h2GiB BASIC policy, without native or aggregate-hard-limit upgrade")
    for kind in ("stdout", "stderr"):
        name = execution+"/"+kind+".txt"
        path = paths.inside(task, name)
        need(paths.mapped(observed[kind+"_path"], original) == name and path.stat().st_size <= 16*MIB
             and common.digest(path) == observed[kind+"_sha256"], "Actual complete bound capture")
    need((task/execution/"stderr.txt").stat().st_size == 0
         and (task/execution/"stdout.txt").stat().st_size > 0, "Successful action actual stdout and empty stderr")
    lines = (task/execution/"stdout.txt").read_text("utf-8").splitlines()
    terminal = lines[-1] if lines else ""
    if stage["kind"] == "initial":
        need(terminal == "PASS_FRESH_EXACT_INITIAL25_"+branch.upper(), "Actual original INITIAL terminal status")
    elif stage["kind"] == "global_resource":
        marker = "PASS_FRESH_EXACT_SHARP25_"+branch.upper()+"_GLOBAL_RESOURCES"
        tokens = terminal.split()
        need(len(tokens) == 2 and tokens[0] == marker, "Actual original resource terminal status")
        elapsed = float(tokens[1])
        need(math.isfinite(elapsed) and elapsed >= 0, "Actual finite resource terminal timing")



def validate_prefix(task, branch, count):
    stages = sources.stages(branch)
    need(type(count) is int and 0 <= count <= len(stages), "Exact finite completed-stage prefix")
    verify_epoch(task, branch, count)
    previous = {}
    results = []
    for stage in stages[:count]:
        filename = "ledgers/"+stage["name"]+".json"
        report = paths.read(Path(task).resolve(), filename, 16*MIB)
        need(report["schema"] == "N25_B5_GLOBAL_BASIC_STAGE_V1"
             and report["branch"] == branch and same(report["stage"], stage)
             and same(report["implementation"], implementation())
             and same(report["preceding_ledger_sha256"], previous)
             and report["source_manifest_sha256"] == sources.selection_sha(branch)
             and report["native_arithmetic_accepted"] is False
             and report["all_index_conclusion_verified"] is False, "Exact current stage and preceding evidence chain")
        transport(task, branch, stage, report)
        result = artifact(task, branch, stage)
        need(same(report["validated_artifact"], result), "Revalidated complete actual artifact")
        previous[filename] = common.digest(Path(task)/filename)
        results.append(result)
    return results


def validate_completed(task):
    """Read a relocated full two-stage export without importing a kernel."""
    results = validate_prefix(task, "b5", 2)
    stages = sources.stages()
    resource = root(task)/stages[1]["folder"]
    initial = root(task)/stages[0]["folder"]
    return dict(schema="REVALIDATED_N25_B5_GLOBAL_PARENTS_V1", branch="b5", n=25,
        contact_allowance="5/16", source_manifest_sha256=sources.selection_sha(), stages=results,
        resource_directory_relative=resource.relative_to(task).as_posix(),
        resource_proof_sha256=common.digest(resource/stages[1]["proof"]),
        resource_receipt_sha256=common.digest(resource/stages[1]["receipt"]),
        initial_proof_sha256=common.digest(initial/stages[0]["proof"]),
        initial_receipt_sha256=common.digest(initial/stages[0]["receipt"]),
        conditional_parent_arithmetic_replayed=True, native_arithmetic_accepted=False,
        stronger24_premise_acquired=False, resource_interfaces_verified=False,
        count_forests_accepted=False, full_n25_verified=False, all_index_conclusion_verified=False)
