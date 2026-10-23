"""Pure source, capture and parent-edge validation for lower n25 acquisitions.

No archived kernel is imported. BASIC execution is reported literally: it has
per-process limits and a sampled process-group watchdog, without native proof
acceptance or a whole-tree hard resource contract.
"""
from __future__ import annotations

import math
from pathlib import Path

from . import aux24_evidence as paths, count_task as common
from . import n25_b012_acquisition_sources as sources

MIB = 1024**2
MEMORY = 2*1024**3
CPU = WALL = 64800
DISK = 512*MIB
need = sources.need
same = paths.same


def implementation():
    base = Path(__file__).resolve().parent
    return {name: common.digest(base/name) for name in (
        "n25_b012_acquisition.py", "n25_b012_acquisition_sources.py",
        "n25_b012_acquisition_evidence.py", "n25_b012_interfaces.py",
        "aux24_sources.py", "aux24_evidence.py", "linux_supervisor.py",
        "count_task.py", "colab_batch.py", "small_indices.py")}


def root(task):
    return Path(task)/"epoch"/sources.source.PREFIX.rstrip("/")


def outputs(branch, count):
    result = set()
    for stage in sources.stages(branch)[:count]:
        prefix = stage["folder"]+"/"
        if stage["receipt"]:
            result.add(prefix+stage["receipt"])
        if stage["kind"] == "local":
            result.add(prefix+stage["proof"])
            panel = stage["args"][-1]
            result.add(prefix+f'PANEL_{panel}_{stage["action"]}_CACHE_RUNTIME.json')
    return result


def progress_files(branch):
    result = set()
    for stage in sources.stages(branch):
        filename = ("PROGRESS_accept.json" if stage["kind"] == "initial" else
                    "PROGRESS.json" if stage["kind"] == "global_resource" else
                    f'PROGRESS_{stage["args"][-1]}.json')
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
    parent, local, _ = sources.definition(branch)
    base = root(task)
    folder = base/stage["folder"]
    proof = read(folder, stage["proof"])
    need(same(proof["profile"], parent["profile"]), "Literal fixed n25 sharp profile")
    frozen = read(folder, "FROZEN_SOURCES.json")
    expected_sources = (dict(frozen, **{"FROZEN_SOURCES.json": common.digest(folder/"FROZEN_SOURCES.json")})
                        if stage["kind"] == "global_resource" else frozen)
    need(same(proof["source_sha256"], expected_sources), "Exact full original proof source keyset and hashes")
    if stage["action"] == "construct":
        need(stage["kind"] == "local", "Only explicit local candidate construction")
        receipt = None
    else:
        receipt = read(folder, stage["receipt"])
        checker = (parent[stage["kind"]]["checker"]["member"].split("/")[-1]
                   if stage["kind"] != "local" else local["local_checker"]["member"].split("/")[-1])
        need(receipt["proof_sha256"] == common.digest(folder/stage["proof"])
             and receipt["checker_sha256"] == common.digest(folder/checker)
             and same(receipt["profile"], parent["profile"]), "Exact fresh accepted proof/checker/profile binding")
        controls = parent[stage["kind"]]["controls"] if stage["kind"] != "local" else local["negative_controls"]
        need(same(receipt["negative_controls"], controls), "Every original corruption control in fixed order")
        _bindings(folder, receipt["source_sha256"])
        need(same(receipt["source_sha256"], proof["source_sha256"]), "Same complete accepted source closure")
    if stage["kind"] == "initial":
        need(receipt["status"] == "PASS_FRESH_EXACT_INITIAL25_"+branch.upper()
             and receipt["signed_rectangles"] == 239616 and receipt["probability_panels"] == 100
             and proof["maximum_covers"] == 12 and len(proof["stages"]) == 12,
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
    else:
        panel = local["panel"]
        need(type(proof["panel"]) is int and proof["panel"] == panel
             and len(proof["rows"]) == 1 and type(proof["rows"][0]["index"]) is int
             and proof["rows"][0]["index"] == panel
             and proof["maximum_cycles"] == proof["maximum_covers_per_cycle"] == 4,
             "One selected four-cycle local panel")
        _bindings(folder.parent, proof["parent_binding_sha256"])
        _bindings(folder, proof["source_sha256"])
        expected_parents = {}
        for kind in ("initial", "global_resource"):
            parent_folder = base/parent[kind]["directory"].removeprefix(sources.source.PREFIX)
            names = set(read(parent_folder, "FROZEN_SOURCES.json")) | {"FROZEN_SOURCES.json",
                parent[kind]["proof_candidate"]["member"].split("/")[-1],
                parent[kind]["historical_acceptance"]["member"].split("/")[-1]}
            for name in names:
                expected_parents[parent_folder.relative_to(folder.parent).as_posix()+"/"+name] = common.digest(parent_folder/name)
        need(same(proof["parent_binding_sha256"], expected_parents), "Exact complete local parent keyset and hashes")
        cycles = proof["rows"][0]["cycles"]
        need(len(cycles) == 4 and proof["rows"][0]["excluded"] is False,
             "Complete selected surviving local acquisition")
        for i, cycle in enumerate(cycles):
            need(type(cycle["cycle"]) is int and cycle["cycle"] == i+1 and len(cycle["stages"]) == 4,
                 "Every original local cycle and four covers")
            for item in cycle["stages"]:
                _cover(item["cover"])
        cache_name = f'PANEL_{panel}_{stage["action"]}_CACHE_RUNTIME.json'
        cache = read(folder, cache_name)
        need(cache["status"] == "PASS_FRESH_LOW25_EXACT_LOCAL_CACHE" and cache["index"] == panel
             and cache["action"] == stage["action"]
             and same(cache["cache_before"], dict(hits=0, misses=0, size=0, maxsize=128))
             and type(cache["mathematical_cover_calls"]) is int and cache["mathematical_cover_calls"] == 16
             and cache["full_stage_evaluations"]+cache["memoized_calls"] == 16
             and cache["wrapper_sha256"] == common.digest(folder/stage["script"]),
             "Fresh empty exact-stage cache; all original calls accounted")
        need(same(cache["source_sha256"], expected_sources)
             and cache["original_checker_sha256"] == common.digest(folder/("mixed_"+branch+".py")),
             "Complete original memoized-wrapper source and checker binding")
        _bindings(folder, cache["output_sha256"])
        if receipt:
            need(receipt["status"] == "PASS_FRESH_EXACT_SHARP25_"+branch.upper()+"_FOUR_COVER_PANEL"
                 and type(receipt["panel"]) is int and receipt["panel"] == panel
                 and type(receipt["probability_panels"]) is int and receipt["probability_panels"] == 1
                 and type(receipt["local_signed_rectangles"]) is int and receipt["local_signed_rectangles"] == 294912
                 and type(receipt["finite_local_cycles"]) is int and receipt["finite_local_cycles"] == 4
                 and same(receipt["parent_binding_sha256"], proof["parent_binding_sha256"]),
                 "Complete newly constructed local proof accepted against current parents")
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
    else:
        panel = stage["args"][-1]
        cache = read(root(task)/stage["folder"], f'PANEL_{panel}_{stage["action"]}_CACHE_RUNTIME.json')
        expected = f'PASS_FRESH_LOW25_EXACT_LOCAL_CACHE {panel} {stage["action"]} '+str(cache["cache_after"])
        need(terminal == expected, "Actual original exact-cache wrapper terminal protocol")
        marker = ("PASS_FRESH_EXACT_SHARP25_"+branch.upper()+"_FOUR_COVER_PANEL" if stage["action"] == "accept"
                  else branch.upper()+"_FEEDBACK_PANEL_CONSTRUCTED")
        originals = [line.split() for line in lines[:-1] if line.startswith(marker+" ")]
        need(len(originals) == 1 and len(originals[0]) == 3 and originals[0][:2] == [marker, panel],
             "Actual complete original local action terminal status before cache report")
        elapsed = float(originals[0][-1])
        need(math.isfinite(elapsed) and elapsed >= 0, "Finite original local terminal timing")


def validate_prefix(task, branch, count):
    stages = sources.stages(branch)
    need(type(count) is int and 0 <= count <= len(stages), "Exact finite completed-stage prefix")
    verify_epoch(task, branch, count)
    previous = {}
    results = []
    for stage in stages[:count]:
        filename = "ledgers/"+stage["name"]+".json"
        report = paths.read(Path(task).resolve(), filename, 16*MIB)
        need(report["schema"] == "N25_B012_ACQUISITION_BASIC_STAGE_V1"
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
