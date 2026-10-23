"""Fresh conditional auxiliary21--23 arithmetic from unchanged exact acceptors.

Archived proof objects are untrusted candidates. No historical accepted receipt
is an input. This new execution/edge protocol does not acquire predecessor or
analytic premises, the stronger24 bound, or an all-law/global conclusion.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import shutil
import sys
import traceback
import uuid

ROOT = Path(__file__).resolve().parents[1]
MIB = 1024**2
BASE = "cutoff25_20261011/continuation_20261010/"
EPOCH_PINS = {
    "21": "ae5f29977948bbfb1e439fdf58f38fee449b7d7bb636d51aad4afa065f00491c",
    "22": "d0a35f509e75282a4887c6e1048a0852496873318c5f50498798ee47edec37d9",
    "23": "69fc6eed8940a7b5f4b447ad79c375d16a5b27c40ee9baeaddd817030ddef7a8",
}
INITIAL_COMMON = "initial34.py kernel.py high_window_core.py direct_gaussian_support.py small_index_support.py heat_support50.py finite_binomial_core.py".split()
RESOURCE_COMMON = "candidate_charged_score_v2.py contracted_kernel.py kernel.py high_window_core.py paired_extended.py signed_variance_resource.py geometric_moment_both.py corrected_phase_callback_extended.py direct_gaussian_support.py finite_binomial_core.py small_index_support.py heat_support50.py".split()
COUNT_COMMON = "accept_strict.py exact35_core.py exact_count_core_v5.py finite_gaussian.py variance_geometry.py joint_cubic.py joint_cubic_defect.py joint_cubic_normalized.py JOINT_PROOF.txt CUBIC_REVIEW.tex DENOMINATOR_REVIEW.txt contract.json profile.py construct.py COUNT_PROOF.txt GUARD_PROVENANCE.json join_counts.py".split()
COUNT_FAST = "optimized_arithmetic.py bernstein_fast.py interval_scalar_fast.py joint_cubic_normalized_fast.py OPTIMIZATION_REVIEW.txt".split()
INITIAL22_CONTROLS = ["wrong positive target", "wrong index", "boolean index", "wrong predecessor premise",
                      "wrong support selection", "wrong allowance", "missing stage", "duplicate stage",
                      "reordered stages", "false next guard", "noncanonical guard", "boolean covered count",
                      "corrupt final gap", "missing panel", "reordered panels", "extra field", "missing dependency", "duplicate JSON key"]
INITIAL23_CONTROLS = ["wrong n", "boolean n", "wrong K", "missing stage", "missing panel", "wrong allowance", "missing exact backend", "unsupported predecessor"]
RESOURCE_CONTROLS = ["wrong theorem", "wrong n", "wrong positive barrier", "wrong contact allowance", "wrong radius",
                     "missing panel", "duplicate panel", "reordered panels", "boolean panel index", "missing arithmetic source",
                     "changed INITIAL bytes", "changed target bytes", "extra success field", "false empty surviving panel",
                     "false final defect", "omitted signed interface", "missing refinement", "unsupported smaller support radius",
                     "noncanonical support radius", "duplicate JSON key"]
PREMISES = {
    "21": ["Universal C20 <= 469/1000", "4095/10000 < CE", "Retained fixed-index attainment, positive closed contact, same-law support and charged INITIAL implications"],
    "22": ["C21 < CE + 11/210", "Retained attainment/contact/support/charged INITIAL/resource/count implications"],
    "23": ["C22 < CE + 9/220", "Retained attainment/contact/support/charged INITIAL/resource/count implications", "Exact optimized interval-arithmetic identities stated in OPTIMIZATION_REVIEW.txt"],
}
SPECS = {
    "21": dict(n=21, K="11/10", allowance="299/2000", initial="toward25/exact21", script="check21.py", rectangles=92160),
    "22": dict(n=22, K="9/10", allowance="53/210", initial="toward25/exact22", script="initial22.py", resource="toward25/resource22", count="count22", indices=list(range(31, 40)), leaves=258, rectangles=129024),
    "23": dict(n=23, K="3/5", allowance="15/44", initial="shared/exact23", script="initial23.py", resource="toward25/resource23", count="count23/optimized_v1", indices=list(range(24, 45)), leaves=18377, rectangles=165888),
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def target(value):
    need(type(value) is str and value in SPECS, "Exactly one target: '21', '22', or '23'")
    return SPECS[value]


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(MIB), b""):
            h.update(block)
    return h.hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def read(path, limit=64*MIB):
    path = Path(path)
    need(path.is_file() and not path.is_symlink() and path.stat().st_size <= limit, "Bounded ordinary evidence file")
    return json.loads(path.read_text("utf-8"), object_pairs_hook=unique)


def write(path, packet):
    with Path(path).open("x", encoding="utf-8") as out:
        json.dump(packet, out, indent=2, sort_keys=True)
        out.write("\n")


def members(value):
    """Complete explicit selected closure; accepted receipts are never copied."""
    spec = target(value)
    selection = {}
    def add(folder, names, kind="source"):
        for name in names:
            key = BASE + folder + "/" + name
            need(key not in selection, "Unique selected archive member")
            selection[key] = kind
    add(spec["initial"], INITIAL_COMMON + [spec["script"]])
    if value == "21":
        return selection
    add(spec["initial"], [f"POSITIVE{value}_INITIAL_PROOF.json"], "candidate")
    if value == "23":
        add(spec["initial"], ["integer_exphi.py", "INTEGER_EXPHI_PROOF.txt", "COPY_MANIFEST.json"])
    add(spec["resource"], RESOURCE_COMMON + [f"resource{value}_core.py", f"protocol{value}.py", f"accept_resources{value}.py", f"contract{value}.json"])
    add(spec["resource"], [f"initial{value}_proof.json", f"resources{value}_proof.json"], "candidate")
    if value == "23":
        add(spec["resource"], ["integer_exphi.py", "INTEGER_EXPHI_PROOF.txt", "BETA_INTERSECTION_PROOF.txt", "MEMOIZATION_IDENTITY_PROOF.txt", "COPY_MANIFEST.json"])
    add(spec["count"], COUNT_COMMON + ["COPY_MANIFEST.json"])
    add(spec["count"], [f"candidate_{i}.json" for i in spec["indices"]], "candidate")
    if value == "22":
        add(spec["count"], ["ARCHIVED_KERNEL_SCOPE.txt"])
    else:
        add(spec["count"], COUNT_FAST + ["SCALAR_SCOPE.txt", "check_optimization.py"])
        # Original check_optimization launches its unmodified slow sibling.
        add("count23", COUNT_COMMON)
        add("count23", [f"candidate_{i}.json" for i in (26, 27, 33, 34, 44)], "candidate")
    return selection


def stages(value):
    spec = target(value)
    initial = "continuation_20261010/" + spec["initial"]
    if value == "21":
        return [dict(name="initial", directory=initial, script="check21.py", args=[], output="EXACT21_CHECKED.json", mode="trusted_native")]
    resource = "continuation_20261010/" + spec["resource"]
    count = "continuation_20261010/" + spec["count"]
    result = [dict(name="initial", directory=initial, script=spec["script"], args=["accept"], output=f"POSITIVE{value}_INITIAL_ACCEPTED.json", mode="trusted_native"),
              dict(name="resource", directory=resource, script=f"accept_resources{value}.py", args=[], output=f"RESOURCES{value}_ACCEPTED.json", mode="trusted_native")]
    if value == "23":
        result.append(dict(name="optimization", directory=count, script="check_optimization.py", args=[], output="OPTIMIZATION_EQUIVALENCE.json", mode="untrusted_search"))
    result += [dict(name=f"count-{i}", directory=count, script="accept_strict.py", args=[str(i)], output=f"accepted_strict_{i}.json", mode="trusted_native") for i in spec["indices"]]
    result.append(dict(name="count-join", directory=count, script="join_counts.py", args=[], output="COUNT22_CONDITIONAL_JOINED.json" if value == "22" else "COUNT23_OPTIMIZED_CONDITIONAL_JOINED.json", mode="trusted_native"))
    return result


def allowed_outputs(value):
    output = {s["directory"] + "/" + s["output"] for s in stages(value)}
    spec = target(value)
    progress = "EXACT21_PROGRESS.json" if value == "21" else "PROGRESS.json" if value == "23" else None
    if progress:
        output.add("continuation_20261010/" + spec["initial"] + "/" + progress)
    return output


def prepare(value, archives, output, *, download=False):
    from . import aux24_sources as sources
    target(value)
    need(type(EPOCH_PINS[value]) is str, "Externally pinned selected source inventory")
    task = sources.prepare(output, archives=archives, members=members(value), download=download)
    sources.verify_prepared(task, expected_manifest_sha=EPOCH_PINS[value])
    write(Path(task) / "JOB.json", dict(schema="FRESH_AUX21_23_JOB_V1", target=value, manifest_sha256=EPOCH_PINS[value],
          driver_sha256=digest(__file__), premises=PREMISES[value], predecessor_acquisition_verified=False,
          full_auxiliary_bound_verified=False, stronger24_acquisition_verified=False, all_index_conclusion_verified=False))
    validate_candidates(task, value)
    return Path(task)


def root_for(task):
    from . import aux24_sources as sources
    return sources.source_root(task)


def bind_files(directory, mapping, expected_names=None):
    need(type(mapping) is dict and mapping, "Nonempty complete native source bindings")
    need(expected_names is None or set(mapping) == set(expected_names), "Complete exact native source binding inventory")
    for name, pin in mapping.items():
        need(type(name) is str and Path(name).name == name and digest(Path(directory) / name) == pin,
             "Every source/candidate byte in the fresh native binding")


def validate_candidates(task, value):
    """Read only JSON geometry/identities; never import an arithmetic module."""
    spec = target(value)
    root = root_for(task) / "continuation_20261010"
    if value == "21":
        return
    initial = root / spec["initial"] / f"POSITIVE{value}_INITIAL_PROOF.json"
    copied = root / spec["resource"] / f"initial{value}_proof.json"
    need(digest(initial) == digest(copied), "Resource candidate consumes exactly the INITIAL object replayed in this job")
    proof = read(initial)
    need(type(proof["profile"]["n"]) is int and proof["profile"]["n"] == spec["n"]
         and proof["profile"]["barrier"] == spec["K"] and proof["predecessor_allowance"] == spec["allowance"], "Exact conditional INITIAL profile and allowance")
    resource = read(root / spec["resource"] / f"resources{value}_proof.json")
    need(resource["profile"] == proof["profile"] and len(resource["rows"]) == 100
         and [r["index"] for r in resource["rows"]] == list(range(100)), "Same fixed profile and all resource candidate rows")
    expected_sources = RESOURCE_COMMON + [f"resource{value}_core.py", f"protocol{value}.py", f"initial{value}_proof.json", f"contract{value}.json"]
    if value == "23":
        expected_sources += ["integer_exphi.py", "INTEGER_EXPHI_PROOF.txt"]
    bind_files(root / spec["resource"], resource["input_sha256"], expected_sources)
    need(digest(root / spec["resource"] / f"contract{value}.json") == digest(root / spec["count"] / "contract.json"),
         "Exactly the same simultaneous resource/count contract")
    total = 0
    for index in spec["indices"]:
        candidate = read(root / spec["count"] / f"candidate_{index}.json")
        need(type(candidate["index"]) is int and candidate["index"] == index
             and candidate["contract_sha256"] == digest(root / spec["count"] / "contract.json")
             and type(candidate["leaves"]) is list and candidate["leaves"], "Exact candidate count panel and contract")
        total += len(candidate["leaves"])
    need(total == spec["leaves"], "Complete selected historical candidate census; no leaf evaluation yet")


def validate_receipt(task, value, stage):
    """Validate actual complete native output and same-object source identities."""
    spec = target(value)
    directory = root_for(task) / stage["directory"]
    receipt = read(directory / stage["output"])
    name = stage["name"]
    if value == "21":
        need(receipt["status"] == "EXACT_FINITE_COVER_PASS_CONDITIONAL_ANALYTIC_INTERFACES"
             and receipt["profile"]["n"] == 21 and receipt["predecessor_allowance"] == "299/2000"
             and receipt["signed_rectangles"] == 92160 and len(receipt["stages"]) == 5
             and F(receipt["stages"][-1]["D"]) < 0, "All five fresh INITIAL covers and final negative defect")
        need(all(type(r["total"]) is int and r["total"] == 18432 and r["active"] + r["excluded"] == 18432 for r in receipt["stages"]), "Complete five-cover signed rectangle accounting")
        bind_files(directory, receipt["source_sha256"], INITIAL_COMMON)
        need(receipt["checker_sha256"] == digest(directory / stage["script"]), "Actual unchanged seed checker")
    elif name == "initial":
        status = "FRESH_EXACT_CONDITIONAL_POSITIVE22_INITIAL_PASS" if value == "22" else "PASS_FRESH_CONDITIONAL_POSITIVE23_INITIAL"
        proof = read(directory / f"POSITIVE{value}_INITIAL_PROOF.json")
        controls = receipt["fixed_expected_object_controls"] if value == "22" else receipt["negative_controls"]
        need(receipt["status"] == status and receipt["profile"] == proof["profile"]
             and receipt["signed_rectangles"] == spec["rectangles"] and receipt["probability_panels"] == 100
             and receipt["proof_sha256"] == digest(directory / f"POSITIVE{value}_INITIAL_PROOF.json")
             and receipt["checker_sha256"] == digest(directory / stage["script"])
             and controls == (INITIAL22_CONTROLS if value == "22" else INITIAL23_CONTROLS), "Full freshly recomputed INITIAL and every original control")
        expected_sources = ["initial34.py", "kernel.py", "high_window_core.py"] if value == "22" else INITIAL_COMMON + ["integer_exphi.py", "INTEGER_EXPHI_PROOF.txt"]
        bind_files(directory, receipt["source_sha256"], expected_sources)
    elif name == "resource":
        proof = read(directory / f"resources{value}_proof.json")
        need(receipt["status"] == f"PASS_POSITIVE{value}_RESOURCES" and receipt["probability_panels"] == 100
             and receipt["profile"] == proof["profile"] and receipt["theorem"] == proof["theorem"]
             and receipt["negative_controls"] == RESOURCE_CONTROLS
             and receipt["resource_sha256"] == digest(directory / f"resources{value}_proof.json")
             and receipt["acceptor_sha256"] == digest(directory / stage["script"]), "Full100 resource rows and all20 original controls")
        expected_sources = RESOURCE_COMMON + [f"resource{value}_core.py", f"protocol{value}.py", f"initial{value}_proof.json", f"contract{value}.json"]
        if value == "23":
            expected_sources += ["integer_exphi.py", "INTEGER_EXPHI_PROOF.txt"]
        bind_files(directory, receipt["input_sha256"], expected_sources)
        active, excluded = receipt["surviving_panels"], receipt["excluded_panels"]
        need(all(type(i) is int for i in active + excluded) and active == sorted(set(active))
             and excluded == sorted(set(excluded)) and sorted(active+excluded) == list(range(100)), "Disjoint complete100-panel resource classification")
        need(active == [r["index"] for r in proof["rows"] if not r["result"].get("excluded")], "Classification agrees with the wholly replayed resource candidate")
    elif name == "optimization":
        need(receipt["status"] == "PASS_EXACT_OUTPUT_EQUIVALENCE_COUNT23"
             and type(receipt["complete_cell_dicts"]) is int and receipt["complete_cell_dicts"] == 70
             and type(receipt["random_quartics"]) is int and receipt["random_quartics"] == 1000,
             "Fresh unchanged slow/optimized full-cell and quartic comparison")
        bind_files(directory, receipt["source_sha256"], ["exact35_core.py", "optimized_arithmetic.py", "bernstein_fast.py", "interval_scalar_fast.py", "joint_cubic_normalized_fast.py", "check_optimization.py"])
    elif name == "count-join":
        need(receipt["status"] == "PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES" and receipt["n"] == spec["n"]
             and receipt["indices"] == spec["indices"] and receipt["all_closed_leaves"] == spec["leaves"]
             and receipt["contract_sha256"] == digest(directory / "contract.json")
             and F(receipt["maximum_score"]) < F(receipt["target_lower"]), "Complete original conditional count aggregation")
        bind_files(directory, receipt["source_sha256"], COUNT_COMMON + (COUNT_FAST if value == "23" else []))
        need(len(receipt["rows"]) == len(spec["indices"]), "All selected count aggregate rows")
        for index, row in zip(spec["indices"], receipt["rows"]):
            need(row["index"] == index and row["candidate_sha256"] == digest(directory / f"candidate_{index}.json")
                 and row["receipt_sha256"] == digest(directory / f"accepted_strict_{index}.json"), "Fresh candidate/acceptance pair in complete count aggregate")
    else:
        index = int(name.split("-")[1])
        candidate = read(directory / f"candidate_{index}.json")
        count = len(candidate["leaves"])
        need(receipt["status"] == "PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES"
             and type(receipt["n"]) is int and receipt["n"] == spec["n"] and receipt["K"] == spec["K"]
             and type(receipt["index"]) is int and receipt["index"] == index
             and receipt["candidate_sha256"] == digest(directory / f"candidate_{index}.json")
             and receipt["contract_sha256"] == digest(directory / "contract.json")
             and type(receipt["negative_controls"]) is int and receipt["negative_controls"] == 24
             and type(receipt["all_closed_leaves"]) is int and receipt["all_closed_leaves"] == count
             and receipt["passed_cells"] + receipt["empty_cells"] == count
             and receipt["maximum_score"] == candidate["maximum_score"]
             and F(receipt["maximum_score"]) < F(receipt["target_lower"]), "Every count leaf and all24 original corruption/parser controls")
        bind_files(directory, receipt["source_sha256"], COUNT_COMMON + (COUNT_FAST if value == "23" else []))
    return receipt


def semantic_edges(task, value, reports):
    """New explicit same-object edge protocol; historical composers are unused."""
    spec = target(value)
    validate_candidates(task, value)
    result = dict(schema="FRESH_AUX21_23_CONDITIONAL_EDGES_V1", target=value, premises=PREMISES[value],
                  source_manifest_sha256=EPOCH_PINS[value], stages={name: r["receipt_sha256"] for name, r in reports.items()},
                  predecessor_acquisition_verified=False, full_auxiliary_bound_verified=False,
                  stronger24_acquisition_verified=False, all_index_conclusion_verified=False)
    if value == "21":
        result["signed_rectangles"] = 92160
        result["allowance"] = "299/2000"
        return result
    root = root_for(task) / "continuation_20261010"
    initial = read(root / spec["initial"] / f"POSITIVE{value}_INITIAL_ACCEPTED.json")
    resource = read(root / spec["resource"] / f"RESOURCES{value}_ACCEPTED.json")
    count = read(root / spec["count"] / stages(value)[-1]["output"])
    need(resource["input_sha256"][f"initial{value}_proof.json"] == initial["proof_sha256"], "Resource consumes this fully replayed INITIAL proof")
    need(resource["input_sha256"][f"contract{value}.json"] == count["contract_sha256"], "All signed resource implications acquire this exact count contract")
    need(resource["profile"] == initial["profile"] and resource["theorem"]["contact_allowance"] == spec["allowance"]
         and resource["theorem"]["n"] == spec["n"] and resource["theorem"]["K"] == spec["K"], "Same physical profile, target and contact allowance")
    need(set(resource["surviving_panels"]) <= set(count["indices"]), "Every surviving closed panel is covered by the freshly replayed count contract")
    result.update(initial_proof_sha256=initial["proof_sha256"], resource_proof_sha256=resource["resource_sha256"],
                  resource_count_contract_sha256=count["contract_sha256"], initial_signed_rectangles=spec["rectangles"],
                  probability_panels=100, surviving_panels=resource["surviving_panels"], excluded_panels=resource["excluded_panels"],
                  count_indices=spec["indices"], count_leaves=spec["leaves"], maximum_count_score=count["maximum_score"],
                  count_target_lower=count["target_lower"], allowance=spec["allowance"],
                  signed_resource_implications="Original protocol.one/core.interface fully replayed: closed p, rho, all scalar upper/lower prices and every signed quadratic polynomial margin over full H intervals")
    return result


def recorded_relative(path, original_task_root):
    """Interpret recorded context without rewriting receipt bytes after relocation."""
    cls = PureWindowsPath if len(str(original_task_root)) > 1 and str(original_task_root)[1] == ":" else PurePosixPath
    root, value = cls(str(original_task_root)), cls(str(path))
    need(root.is_absolute() and value.is_absolute() and ".." not in value.parts, "Absolute contained original execution context")
    relative = value.relative_to(root)
    need(relative.parts and ".." not in relative.parts, "Recorded artifact is inside its original task")
    return Path(*relative.parts)


def _check_execution(task, value, stage, report, *, original_task_root=None):
    from .small_indices import trusted_guard
    task = Path(task).resolve()
    original = report["original_task_root"]
    need(original_task_root is None or str(original_task_root) == original, "Explicit original task context agrees with unchanged execution record")
    need(report["schema"] == "FRESH_AUX21_23_STAGE_V1" and report["target"] == value
         and report["stage"] == stage["name"] and report["driver_sha256"] == digest(__file__)
         and report["source_manifest_sha256"] == EPOCH_PINS[value]
         and report["supervisor_sha256"] == digest(Path(__file__).with_name("linux_supervisor.py")), "Same reviewed driver, supervisor and selected source epoch")
    observed = report["observed"]
    need(observed.get("status") == "completed" and type(observed.get("returncode")) is int and observed["returncode"] == 0,
         "Exact integer successful bounded native completion")
    directory = root_for(task) / stage["directory"]
    script = directory / stage["script"]
    command = report["command"]
    need(command[1:3] == ["-B", "-S"] and command[4:] == stage["args"]
         and recorded_relative(command[3], original) == script.relative_to(task), "Original unchanged command and sibling context")
    need(type(report["cpu_seconds"]) is int and 2 <= report["cpu_seconds"] <= 7200
         and type(report["wall_seconds"]) is int and 1 <= report["wall_seconds"] <= 7260, "Bounded per-action resources")
    if stage["mode"] == "trusted_native":
        need(trusted_guard(observed, script_sha=digest(script), supervisor_sha=report["supervisor_sha256"],
                           memory_bytes=512*MIB, cpu_seconds=report["cpu_seconds"]), "Established64+448MiB single-process native guard")
    else:
        scope = observed.get("guard_scope", {})
        need(observed.get("mode") == "untrusted_search" and scope.get("kind") == "UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP"
             and scope.get("proof_acceptance") is False, "Explicit BASIC process-group evidence; no native acceptance")
    for kind in ("stdout", "stderr"):
        relative = recorded_relative(observed[kind + "_path"], original)
        need(relative.as_posix() == report["execution_relative"] + "/" + kind + ".txt", "Original captured artifact path")
        path = task / relative
        need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 16*MIB
             and digest(path) == observed.get(kind + "_sha256") == report[kind + "_sha256"], "Actual capture matches supervisor and stage hashes")
    stdout = (task / report["execution_relative"] / "stdout.txt").read_text("utf-8")
    need((task / report["execution_relative"] / "stderr.txt").stat().st_size == 0, "Successful exact replay has empty stderr")
    receipt = validate_receipt(task, value, stage)
    receipt_path = directory / stage["output"]
    need(report["receipt_relative"] == receipt_path.relative_to(task).as_posix()
         and report["receipt_sha256"] == digest(receipt_path), "Same actual freshly produced receipt after relocation")
    if value == "21":
        need(stdout.splitlines().count("EXACT21_PASS") == 1, "One actual complete five-cover terminal marker")
    elif stage["name"].startswith("count-") and stage["name"] != "count-join":
        index = int(stage["name"].split("-")[1])
        prefix = "ACCEPTED_CONDITIONAL_COUNT22_K090_COUNT" if value == "22" else "ACCEPTED_CONDITIONAL_COUNT23_K060_OPTIMIZED_V1_COUNT"
        marker = f"{prefix} {index} {receipt['passed_cells']} {receipt['empty_cells']} {receipt['all_closed_leaves']} 24 "
        need(sum(line.startswith(marker) for line in stdout.splitlines()) == 1 and stdout.splitlines()[-1].startswith(marker), "Actual complete count terminal marker")
    elif stage["name"] == "count-join":
        printed = json.loads(stdout, object_pairs_hook=unique)
        need(printed == {k: receipt[k] for k in ("status", "n", "K", "all_closed_leaves", "maximum_score", "target_lower", "strict_margin")}, "Actual complete original count-join summary")
    elif stage["name"] == "initial" and value == "22":
        need(stdout.rstrip().endswith(json.dumps(receipt, indent=2)), "Actual complete INITIAL22 terminal object")
    elif stage["name"] == "optimization":
        need(json.loads(stdout, object_pairs_hook=unique) == receipt, "Actual whole optimization comparison terminal object")
    else:
        need(stdout.splitlines() and json.loads(stdout.splitlines()[-1], object_pairs_hook=unique) == receipt,
             "Actual complete native terminal object")
    return receipt


def _job(task):
    from . import aux24_sources as sources
    task = Path(task).resolve()
    job = read(task / "JOB.json")
    value = job["target"]
    target(value)
    need(job == dict(schema="FRESH_AUX21_23_JOB_V1", target=value, manifest_sha256=EPOCH_PINS[value],
         driver_sha256=digest(__file__), premises=PREMISES[value], predecessor_acquisition_verified=False,
         full_auxiliary_bound_verified=False, stronger24_acquisition_verified=False, all_index_conclusion_verified=False),
         "Same reviewed scoped auxiliary job")
    manifest = sources.verify_prepared(task, expected_manifest_sha=EPOCH_PINS[value], outputs=allowed_outputs(value))
    need({name: row["kind"] for name, row in manifest["files"].items()} == members(value), "Exact selected source/candidate classification")
    validate_candidates(task, value)
    return task, value


def _ledger_path(task, stage):
    return Path(task) / (stage["name"] + "-COMPLETED.json")


def _completed(task, value, stage, previous, *, original_task_root=None):
    path = _ledger_path(task, stage)
    if not path.exists():
        return None
    report = read(path)
    need(report["status"] == "completed" and report["mode"] == stage["mode"]
         and report["native_arithmetic_accepted"] is (stage["mode"] == "trusted_native")
         and report["predecessor_acquisition_verified"] is False and report["full_auxiliary_bound_verified"] is False
         and report["all_index_conclusion_verified"] is False and report["dependencies"] == {
        name: digest(Path(task) / (name + "-COMPLETED.json")) for name in previous}, "Complete unchanged preceding fresh-stage ledger")
    _check_execution(task, value, stage, report, original_task_root=original_task_root)
    return report


def completion_result(task, value, reports, edges):
    return dict(schema="FRESH_AUX21_23_JOB_RESULT_V1", status="FRESH_CONDITIONAL_ARITHMETIC_REPLAY_COMPLETED",
                target=value, n=SPECS[value]["n"], K=SPECS[value]["K"], allowance=SPECS[value]["allowance"],
                conditional_arithmetic_replayed=True, semantics_verified=True,
                native_arithmetic_accepted=all(r["native_arithmetic_accepted"] for r in reports.values()),
                source_manifest_sha256=EPOCH_PINS[value], driver_sha256=digest(__file__), premises=PREMISES[value],
                semantic_edges_sha256=digest(Path(task) / "SEMANTIC_EDGES.json"), semantic_edges=edges,
                stage_ledger_sha256={name: digest(Path(task) / (name + "-COMPLETED.json")) for name in reports},
                predecessor_acquisition_verified=False, full_auxiliary_bound_verified=False,
                stronger24_acquisition_verified=False, all_index_conclusion_verified=False)


def validate_completed(task, *, original_task_root=None):
    """Revalidate exported evidence at any path, without executing numeric code.

    Absolute paths in original receipts/argv remain unchanged. Recorded captures
    are read through their contained relative paths under the restored task.
    """
    task, value = _job(task)
    reports = {}
    for stage in stages(value):
        report = _completed(task, value, stage, reports, original_task_root=original_task_root)
        need(report is not None, "Every original numeric stage has a completed fresh execution ledger")
        reports[stage["name"]] = report
    expected = semantic_edges(task, value, reports)
    need(read(task / "SEMANTIC_EDGES.json") == expected, "Exact source-bound same-object semantic edge packet")
    completed = read(task / "JOB_RESULT.json")
    need(completed == completion_result(task, value, reports, expected)
         and completed["conditional_arithmetic_replayed"] is True and completed["semantics_verified"] is True
         and all(completed[k] is False for k in ("predecessor_acquisition_verified", "full_auxiliary_bound_verified",
                                                 "stronger24_acquisition_verified", "all_index_conclusion_verified")),
         "Complete exact scoped arithmetic evidence without an acquired auxiliary theorem")
    return completed


def run(task, *, wall_seconds=7260, cpu_seconds=7200):
    from . import count_task as common
    from . import aux24_sources as sources
    from .small_indices import FollowOutput, Progress
    need(type(wall_seconds) is int and 1 <= wall_seconds <= 7260 and type(cpu_seconds) is int
         and 2 <= cpu_seconds <= 7200, "Bounded action wall/CPU budgets")
    task, value = _job(task)
    reports = {}
    for stage in stages(value):
        done = _completed(task, value, stage, reports)
        if done is not None:
            reports[stage["name"]] = done
            common.event(task, "aux_completed_stage_revalidated", target=value, stage_name=stage["name"])
            continue
        directory = root_for(task) / stage["directory"]
        receipt_path = directory / stage["output"]
        epoch = task / "attempts" / (stage["name"] + "-" + uuid.uuid4().hex[:12])
        epoch.mkdir(parents=True)
        # A receipt without a successful complete guard record is only evidence
        # of an interrupted attempt. Preserve it; never relabel it as accepted.
        if receipt_path.exists():
            need(receipt_path.is_file() and not receipt_path.is_symlink(), "Ordinary incomplete native output")
            shutil.copyfile(receipt_path, epoch / "UNACCEPTED_PREVIOUS_OUTPUT.json")
            receipt_path.unlink()
        sources.verify_prepared(task, EPOCH_PINS[value], outputs=allowed_outputs(value))
        script = directory / stage["script"]
        command = [sys.executable, "-B", "-S", str(script), *stage["args"]]
        report = dict(schema="FRESH_AUX21_23_STAGE_V1", target=value, stage=stage["name"], status="partial",
                      command=command, original_task_root=str(task), driver_sha256=digest(__file__),
                      source_manifest_sha256=EPOCH_PINS[value], supervisor_sha256=digest(Path(__file__).with_name("linux_supervisor.py")),
                      cpu_seconds=cpu_seconds, wall_seconds=wall_seconds, mode=stage["mode"],
                      execution_relative=(epoch / "execution").relative_to(task).as_posix(),
                      receipt_relative=receipt_path.relative_to(task).as_posix(),
                      dependencies={name: digest(task / (name + "-COMPLETED.json")) for name in reports},
                      native_arithmetic_accepted=False, predecessor_acquisition_verified=False,
                      full_auxiliary_bound_verified=False, all_index_conclusion_verified=False)
        progress = Progress(epoch / "FOLLOW_PROGRESS.jsonl")
        try:
            progress.emit("aux_exact_stage_started", target=value, stage=stage["name"], mode=stage["mode"],
                          arithmetic_accepted=False, cpu_seconds=cpu_seconds, wall_seconds=wall_seconds)
            with FollowOutput(stage["name"], epoch / "execution/stdout.txt", progress, 20):
                observed = common.supervise(command, cwd=directory, output_dir=epoch / "execution",
                           wall_seconds=wall_seconds, cpu_seconds=cpu_seconds, memory_bytes=512*MIB,
                           mode=stage["mode"], disk_bytes=256*MIB, log_bytes=16*MIB)
            report["observed"] = observed
            for key in ("stdout", "stderr"):
                path = Path(observed[key + "_path"]) if observed.get(key + "_path") else None
                report[key + "_sha256"] = digest(path) if path is not None and path.is_file() else None
            report["receipt_sha256"] = digest(receipt_path) if receipt_path.is_file() else None
            _check_execution(task, value, stage, report)
            sources.verify_prepared(task, EPOCH_PINS[value], outputs=allowed_outputs(value))
            report.update(status="completed", native_arithmetic_accepted=stage["mode"] == "trusted_native")
        except BaseException as error:
            report["error"] = type(error).__name__ + ": " + str(error)
            (epoch / "ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        finally:
            progress.emit("aux_exact_stage_finished", target=value, stage=stage["name"], status=report["status"],
                          native_arithmetic_accepted=report["native_arithmetic_accepted"], all_index_conclusion_verified=False)
            progress.close()
            write(epoch / "RESULT.json", report)
        if report["status"] != "completed":
            return dict(status="PARTIAL_NOT_ACCEPTED", target=value, failed_stage=stage["name"], attempt=report,
                        conditional_arithmetic_replayed=False, native_arithmetic_accepted=False, semantics_verified=False,
                        predecessor_acquisition_verified=False, full_auxiliary_bound_verified=False,
                        stronger24_acquisition_verified=False, all_index_conclusion_verified=False)
        write(_ledger_path(task, stage), report)
        reports[stage["name"]] = report
    edges = semantic_edges(task, value, reports)
    edge_path = task / "SEMANTIC_EDGES.json"
    if edge_path.exists():
        need(read(edge_path) == edges, "Same fully revalidated semantic edges")
    else:
        write(edge_path, edges)
    result = completion_result(task, value, reports, edges)
    result_path = task / "JOB_RESULT.json"
    if result_path.exists():
        need(read(result_path) == result, "Same completed scoped job result")
    else:
        write(result_path, result)
    return validate_completed(task)


def restore_latest(value, durable_root, work_root):
    """Restore matching live evidence; completed stages still need full validation."""
    target(value)
    candidates = sorted((Path(durable_root) / ("auxiliary" + value)).glob("*/live/task/JOB.json"),
                        key=lambda p: p.parent.parent.parent.name, reverse=True)
    for path in candidates:
        try:
            data = read(path)
            if data.get("target") != value or data.get("driver_sha256") != digest(__file__) or data.get("manifest_sha256") != EPOCH_PINS[value]:
                continue
            stamp = path.parent.parent.parent.name
            local = Path(work_root) / ("auxiliary" + value) / stamp
            if not local.exists():
                shutil.copytree(path.parent.parent, local)
                (local / "LIVE_SNAPSHOT.json").unlink(missing_ok=True)
            _job(local / "task")
            return local
        except (ValueError, OSError, KeyError):
            continue
    return None


def run_colab(value, *, durable_root, work_root="/content/berry-esseen-runs", archives="/content/berry-esseen-archives",
              backup_interval=60, wall_seconds=7260, cpu_seconds=7200, resume=True):
    """Independent conditional job;20s progress,60s live copies, final ZIP on failure."""
    from . import colab_batch
    from .environment import snapshot
    target(value)
    need(type(backup_interval) in (int, float) and backup_interval > 0 and type(resume) is bool, "Explicit live-backup/resume options")
    root = restore_latest(value, durable_root, work_root) if resume else None
    restored = root is not None
    if root is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
        root = Path(work_root) / ("auxiliary" + value) / stamp
        root.mkdir(parents=True)
    durable = Path(durable_root) / ("auxiliary" + value) / root.name
    status = dict(scope="CONDITIONAL_AUXILIARY" + value + "_ARITHMETIC_ONLY", target=value, state="started",
                  conditional_arithmetic_replayed=False, native_arithmetic_accepted=False, semantics_verified=False,
                  predecessor_acquisition_verified=False, full_auxiliary_bound_verified=False,
                  stronger24_acquisition_verified=False, all_index_conclusion_verified=False)
    colab_batch.atomic_json(root / "SESSION_RESULT.json", status)
    monitor = colab_batch.Backups(root, durable, interval=backup_interval)
    monitor.start()
    try:
        colab_batch.event(root, "auxiliary_job_started", target=value, restored_live_evidence=restored,
                          premises=PREMISES[value], full_auxiliary_bound_verified=False)
        colab_batch.atomic_json(root / "ENVIRONMENT.json", snapshot())
        task = root / "task"
        if not task.exists():
            prepare(value, archives, task, download=True)
        result = run(task, wall_seconds=wall_seconds, cpu_seconds=cpu_seconds)
        status.update(state=result["status"], conditional_arithmetic_replayed=result["conditional_arithmetic_replayed"],
                      native_arithmetic_accepted=result["native_arithmetic_accepted"], semantics_verified=result["semantics_verified"], result=result)
    except BaseException as error:
        status.update(state="PARTIAL_ERROR_NOT_ACCEPTED", error=type(error).__name__ + ": " + str(error))
        (root / "ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        colab_batch.event(root, "auxiliary_job_incomplete", target=value, error=status["error"])
    finally:
        colab_batch.atomic_json(root / "SESSION_RESULT.json", status)
        try:
            monitor.close()
        except Exception as error:
            colab_batch.event(root, "final_backup_failed", error=str(error))
        # A restart may already have produced a bundle at the durable location.
        bundles = durable / "bundles" / uuid.uuid4().hex[:8]
        output = colab_batch.bundle(root, bundles)
        colab_batch.event(root, "auxiliary_results_bundle_saved", target=value, path=str(output), state=status["state"],
                          full_auxiliary_bound_verified=False, all_index_conclusion_verified=False)
    print("\nRESULT:", status["state"], "\nZIP:", output, flush=True)
    return dict(status=status, bundle=str(output), work=str(root))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare", help="Prepare only pinned source and untrusted candidates")
    prep.add_argument("target", choices=tuple(SPECS))
    prep.add_argument("output", type=Path)
    prep.add_argument("--archives", type=Path, required=True)
    prep.add_argument("--download", action="store_true")
    run_parser = commands.add_parser("run", help="Fresh full acceptor replay; resume only verified complete stage ledgers")
    run_parser.add_argument("task", type=Path)
    check = commands.add_parser("validate", help="Revalidate completed exported evidence without numerical replay")
    check.add_argument("task", type=Path)
    args = parser.parse_args()
    if args.command == "prepare":
        print(prepare(args.target, args.archives, args.output, download=args.download))
        return 0
    result = run(args.task) if args.command == "run" else validate_completed(args.task)
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if result["conditional_arithmetic_replayed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
