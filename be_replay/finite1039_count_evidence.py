"""Pure evidence readback for the selected finite10--39 COUNT lanes.

No original mathematical module is imported. Both native representations retain
their original complete acceptor, candidate, contract and controls. BASIC
execution does not acquire parent facts or an unrestricted finite theorem.
"""
from __future__ import annotations
import json
import math
from fractions import Fraction
from pathlib import Path, PurePosixPath, PureWindowsPath
import re

from . import finite1039_sources as src

OBSERVED = "OBSERVED_CONDITIONAL_FINITE1039_COUNT_V1"
COMPLETED = "COMPLETED_CONDITIONAL_FINITE1039_COUNT_V1"
SCOPE = "UNCHANGED_FULL_SELECTED_FINITE1039_COUNT_BASIC_V1"
CPU_SECONDS = 43200
WALL_SECONDS = 54000
MEMORY_BYTES = 2048*src.MIB
FLAGS = ("native_arithmetic_accepted", "parent_acquisitions_verified",
         "fresh_parent_fact_joins_verified", "full_finite1039_verified", "all_index_conclusion_verified")


def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def implementation():
    names = ("finite1039_counts.py", "finite1039_count_evidence.py", "finite1039_sources.py",
             "n5_remaining_sources.py", "n5_remaining_bridge.py", "linux_supervisor.py", "colab_batch.py")
    return {name: src.digest(src.ROOT/"be_replay"/name) for name in names} | {"catalog_sha256": src.CATALOG_SHA256}


# Exact published runtime4d2020e36a2ffc521815d03f58284058d6dce3ef.
# Its complete native stages are valid; only batch summary finalization read
# an absent catalog field. Never mix hashes or rewrite old completed evidence.
PRE_FINISH_FIX_IMPLEMENTATION = {
    "catalog_sha256": "67a647a00111fda930391bda90345ece419bbf54c44a70c0390969ad0fab3d6d",
    "colab_batch.py": "136bc2bb9b25cb8cd36118041bf593821f3cbdea5debee82b27ccb7626c0d1e6",
    "finite1039_count_evidence.py": "6e38c9c99ecebcfce7d1c09d8233da1b5905bbd9f46e60c4a73883fdcd8f03e9",
    "finite1039_counts.py": "5652bce423b4949c49c17e00ff95188390ab65efd41a5912ff110ec969dfac85",
    "finite1039_sources.py": "6a34be3e362d2a9cfe34b52bf1c0f1872cd4fe45afa8cf2acf82a232b4da1c95",
    "linux_supervisor.py": "61e71dd4a9653de2bbbee8c54928a1f5c5bffd0bf083dd324851716c3a1eaea2",
    "n5_remaining_bridge.py": "f0459a0570ca9a4fc11e507f25474e67bf5e3e958a60513bb7be364d707a069a",
    "n5_remaining_sources.py": "17f8d9b3bcdce510574901be83684a630d54cc8d2f6251856b7737bbd85aaaab",
}


def known_implementation(packet):
    return same(packet, implementation()) or same(packet, PRE_FINISH_FIX_IMPLEMENTATION)


def mapped(task, value, original):
    src.need(type(value) is str and type(original) is str and "\0" not in value and "\0" not in original,
             "Recorded original path strings")
    cls = PureWindowsPath if re.match(r"^[A-Za-z]:", original) else PurePosixPath
    p, root = cls(value), cls(original)
    src.need(p.is_absolute() and root.is_absolute() and ".." not in root.parts, "One absolute originating task root")
    try:
        relative = p.relative_to(root)
    except ValueError:
        raise ValueError("Evidence path leaves its explicit originating task root")
    src.need(relative.parts and all(x not in (".", "..") for x in relative.parts), "Contained evidence path")
    result = Path(task).joinpath(*relative.parts)
    for parent in (result, *result.parents):
        if parent == Path(task).parent:
            break
        src.ordinary(parent)
    return result


def command(request, row, python):
    original = request["original_task_root"]
    cls = PureWindowsPath if re.match(r"^[A-Za-z]:", original) else PurePosixPath
    src.need(type(python) is str and cls(python).is_absolute(), "Original absolute interpreter path")
    return [python, "-B", "-S", str(cls(original)/"capsule"/row["directory"]/row["script"]), *row["arguments"]]


def inventory(task):
    result = {}
    for p in sorted(Path(task).rglob("*")):
        src.ordinary(p)
        if p.is_file() and p.relative_to(task).as_posix() not in ("STAGE_OBSERVED.json", "STAGE_COMPLETED.json"):
            result[p.relative_to(task).as_posix()] = dict(bytes=p.stat().st_size, sha256=src.digest(p))
    return result


def terminal(text):
    decoder = json.JSONDecoder(object_pairs_hook=src.unique)
    for pos in [0] + [m.end() for m in re.finditer("\n", text)]:
        if not text[pos:].startswith("{"):
            continue
        try:
            packet, end = decoder.raw_decode(text, pos)
        except ValueError:
            continue
        if not text[end:].strip():
            return packet
    raise ValueError("Whole original native receipt at the end of actual stdout")


def stdout_matches(stdout, row, receipt):
    rule = row["stdout_rule"]
    if rule["kind"] == "json_receipt":
        src.need(same(terminal(stdout), receipt), "Actual terminal JSON equals the whole fresh native receipt")
    else:
        src.need(rule["kind"] == "text" and set(rule) == {"kind", "prefix", "tokens", "index_token"},
                 "Exact source-derived original text terminal rule")
        lines = [line for line in stdout.splitlines() if line.strip()]
        src.need(lines, "Actual original text terminal")
        tokens = lines[-1].split()
        src.need(type(rule["tokens"]) is int and len(tokens) == rule["tokens"]
                 and type(rule["index_token"]) is int and 0 < rule["index_token"] < len(tokens)
                 and tokens[0] == rule["prefix"] and tokens[rule["index_token"]] == str(row["index"]),
                 "Source-specific original terminal marker, arity and selected literal index")
        # Every selected strict writer has this exact eight-argument print:
        # marker, index, passed, empty, len(contexts), nc, float(maximum), elapsed.
        src.need(rule["tokens"] == 8 and rule["index_token"] == 1
                 and tokens[2:6] == [str(receipt[name]) for name in
                                     ("passed_cells", "empty_cells", "all_closed_leaves", "negative_controls")]
                 and tokens[6] == str(float(Fraction(receipt["maximum_score"]))),
                 "Actual strict terminal counts and maximum equal the whole fresh receipt")
        try:
            elapsed = float(tokens[7])
        except ValueError:
            raise ValueError("Finite nonnegative original strict elapsed terminal metadata")
        src.need(math.isfinite(elapsed) and elapsed >= 0,
                 "Finite nonnegative original strict elapsed terminal metadata")


def untimed_receipt(receipt, row, *, python_executable, python_version):
    ignored = row["ignored_runtime_fields"]
    src.need(ignored in (["seconds"], ["child_runtime"]), "One explicitly reviewed runtime metadata exception")
    expected = row["expected_receipt"]
    src.need(type(receipt) is dict and type(expected) is dict
             and same({k: v for k, v in receipt.items() if k not in ignored},
                      {k: v for k, v in expected.items() if k not in ignored}),
             "Every fresh mathematical, scope, control and source field equals the fixed selected statement")
    if ignored == ["seconds"]:
        src.need("seconds" in receipt and type(receipt["seconds"]) in (int, float)
                 and math.isfinite(receipt["seconds"]) and receipt["seconds"] >= 0,
                 "Finite ordinary original elapsed metadata")
    else:
        required = row["child_runtime_required"]
        src.need(type(required) is bool and ("child_runtime" in receipt) is required,
                 "Source-specific presence of original child runtime metadata")
        if required:
            runtime = receipt["child_runtime"]
            src.need(type(runtime) is dict and set(runtime) == {"executable", "version", "optimize"}
                     and type(runtime["optimize"]) is int and runtime["optimize"] == 0
                     and type(python_executable) is str and type(python_version) is str
                     and type(runtime["executable"]) is str and runtime["executable"] == python_executable
                     and type(runtime["version"]) is str and runtime["version"] == python_version,
                     "Exact original unoptimized child executable and version equal actual launch/report context")


def summarize(task, row, stdout, observed, original, *, python_executable, python_version):
    directory = Path(task)/"capsule"/row["directory"]
    path = directory/row["output"]
    receipt = src.read(path, limit=64*src.MIB)
    untimed_receipt(receipt, row, python_executable=python_executable, python_version=python_version)
    stdout_matches(stdout, row, receipt)
    src.need(type(receipt["n"]) is int and receipt["n"] == row["n"]
             and type(receipt["index"]) is int and receipt["index"] == row["index"], "Literal native index and probability panel")
    controls = row["expected_controls"]
    src.need(same(receipt["negative_controls"], controls)
             and ((type(controls) is int and controls > 0) or
                  (type(controls) is list and controls and len(set(controls)) == len(controls))),
             "Every original source-specific corruption control")
    candidate = directory/row["candidate"]
    contract = directory/row["contract_name"]
    src.need(src.digest(candidate) == row["candidate_sha256"] and src.digest(contract) == row["contract_sha256"]
             and receipt["contract_sha256"] == row["contract_sha256"], "Exact whole selected candidate and literal contract bytes")
    packet = src.read(candidate, limit=128*src.MIB)
    structural = src.inspect_candidate(row, packet)
    src.need(same(structural, row["census"]), "Every original closed root, split and leaf in the selected candidate")
    src.need(type(structural["roots"]) is int and structural["roots"] == row["n"]+1,
             "All logical nearest-count roots, in the original representation")
    if row["family"] == "count_protocol":
        src.need(row["script"] == "count_protocol.py" and row["arguments"] == ["accept"]
                 and receipt["forest_sha256"] == row["candidate_sha256"]
                 and receipt["checker_sha256"] == src.digest(directory/row["script"]),
                 "Unchanged full count_protocol acceptance and complete input bindings")
        bound = src.read(directory/"KERNEL_COPY_MANIFEST.json")["files"]
        src.need(type(bound) is dict and bound and same(receipt["kernel_sha256"], bound)
                 and same(packet["kernel_sha256"], bound), "Complete unchanged kernel manifest and forest header")
        for name, pin in bound.items():
            src.parts(name)
            src.need(row["source_files_sha256"].get(row["directory"]+"/"+name) == pin
                     and src.digest(directory/name) == pin, "Every actual original count kernel helper byte")
        stats = receipt["statistics"]
        src.need(all(type(stats[k]) is int and stats[k] == structural[k] for k in ("nodes", "leaves", "maximum_depth"))
                 and type(receipt["fresh_leaf_evaluations"]) is int
                 and receipt["fresh_leaf_evaluations"] == structural["leaves"], "Every original count_protocol leaf freshly recomputed")
        score, target = stats["maximum_score"], packet["target"]
    else:
        src.need(row["family"] == "strict" and row["script"] in ("accept_strict.py", "accept_strict_v2.py")
                 and row["arguments"] == [str(row["index"])]
                 and receipt["candidate_sha256"] == row["candidate_sha256"], "Unchanged full strict acceptance and candidate binding")
        sources = receipt["source_sha256"]
        src.need(type(sources) is dict and sources, "Complete original strict source graph")
        for name, pin in sources.items():
            src.need(len(src.parts(name)) == 1
                     and row["source_files_sha256"].get(row["directory"]+"/"+name) == pin
                     and src.digest(directory/name) == pin, "Every actual original strict numerical source byte")
        src.need(all(type(receipt[k]) is int and receipt[k] >= 0
                     for k in ("passed_cells", "empty_cells", "all_closed_leaves"))
                 and receipt["passed_cells"]+receipt["empty_cells"] == receipt["all_closed_leaves"] == structural["leaves"],
                 "All original strict passing and excluded leaves freshly recomputed")
        score, target = receipt["maximum_score"], receipt["target_lower"]
    src.need(type(score) is str and type(target) is str and Fraction(score) < Fraction(target),
             "The original exact strict target, without a rounded substitute")
    captures = observed["checkpoints"]
    src.need(type(captures) is list and len(captures) == 1, "Exactly one stopped-supervisor whole native output capture")
    capture = captures[0]
    src.need(set(capture) == {"source_path", "exists", "trusted_certificate", "path", "bytes", "sha256"}
             and capture["exists"] is True and capture["trusted_certificate"] is False
             and mapped(task, capture["source_path"], original) == path, "Actual captured fresh output identity")
    copied = mapped(task, capture["path"], original)
    src.need(copied == Path(task)/"execution/checkpoints"/row["output"] and copied.is_file()
             and type(capture["bytes"]) is int and capture["bytes"] == path.stat().st_size == copied.stat().st_size
             and capture["sha256"] == src.digest(path) == src.digest(copied), "Complete stopped output bytes and SHA match the native receipt")
    return dict(job_id=row["job_id"], lane=row["lane"], family=row["family"], n=row["n"], index=row["index"],
        band=row.get("band"), census=structural, native_status=receipt["status"], native_controls=controls,
        candidate_sha256=row["candidate_sha256"], contract_sha256=row["contract_sha256"],
        receipt_relative="capsule/"+src.output_relative(row), receipt_sha256=src.digest(path),
        source_files_sha256=row["source_files_sha256"], ignored_runtime_fields=row["ignored_runtime_fields"],
        fresh_parent_fact_joins_verified=False, parent_acquisitions_verified=False,
        full_finite1039_verified=False, all_index_conclusion_verified=False)


def validate_run(task, row, report):
    task = Path(task)
    request = src.verify_job(task, row)
    original = request["original_task_root"]
    src.need(report["schema"] == OBSERVED and report["scope"] == SCOPE and report["job_id"] == row["job_id"]
             and known_implementation(report["implementation"]) and report["original_task_root"] == original
             and report["conditional_arithmetic_completed"] is False and all(report[f] is False for f in FLAGS),
             "Exact current or complete published prior implementation and false observed-to-completed transition")
    observed = report["observed"]
    src.need(observed.get("status") == "completed" and type(observed.get("returncode")) is int and observed["returncode"] == 0
             and observed.get("reason") is None and observed.get("proof_accepted") is False
             and observed.get("mode") == "untrusted_search" and type(observed.get("sample_count")) is int
             and observed["sample_count"] > 0, "Actual successful stopped BASIC execution")
    for key in ("elapsed_seconds", "maximum_sampled_group_RSS_bytes", "maximum_sampled_group_CPU_seconds"):
        value = observed.get(key)
        src.need(type(value) in (int, float) and math.isfinite(value) and value >= 0,
                 "Finite original process diagnostic: "+key)
    src.need(same(src.read(task/"execution/supervisor-result.json"), observed), "Actual stopped supervisor result")
    launch = src.read(task/"execution/launch.json")
    base_fields = {"argv", "cwd", "output_dir", "mode", "wall_seconds", "cpu_seconds", "memory_bytes", "checkpoint_paths",
                   "disk_bytes", "log_bytes", "sample_seconds", "heartbeat_seconds"}
    src.need(set(launch) == base_fields and same(launch["argv"], command(request, row, report["python_executable"]))
             and mapped(task, launch["cwd"], original) == task/"capsule"/row["directory"]
             and mapped(task, launch["output_dir"], original) == task/"execution"
             and launch["mode"] == "untrusted_search" and launch["sample_seconds"] == .2 and launch["heartbeat_seconds"] == 20
             and type(launch["checkpoint_paths"]) is list and len(launch["checkpoint_paths"]) == 1
             and mapped(task, launch["checkpoint_paths"][0], original) == task/"capsule"/src.output_relative(row),
             "Actual source-specific acceptor command, cwd, output and complete stopped capture request")
    for key, value in (("cpu_seconds", CPU_SECONDS), ("wall_seconds", WALL_SECONDS), ("memory_bytes", MEMORY_BYTES)):
        allowed = (int, float) if key == "wall_seconds" else (int,)
        src.need(type(report[key]) is int and report[key] == value and type(launch[key]) in allowed and launch[key] == value,
                 "Exact documented BASIC execution budget")
    src.need(type(launch["disk_bytes"]) is int and launch["disk_bytes"] == 512*src.MIB
             and type(launch["log_bytes"]) is int and launch["log_bytes"] == 16*src.MIB, "Bounded original disk and capture policy")
    scope = dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP", proof_acceptance=False,
        external_wall_seconds=float(WALL_SECONDS), per_process_RLIMIT_AS_bytes=MEMORY_BYTES,
        per_process_RLIMIT_CPU_seconds=CPU_SECONDS, aggregate_kernel_memory_limit=False, aggregate_kernel_cpu_limit=False,
        sampled_group_RSS_limit_bytes=MEMORY_BYTES, sampled_group_CPU_limit_seconds=CPU_SECONDS,
        sampled_file_limit_bytes=512*src.MIB, sampled_log_limit_bytes=16*src.MIB,
        descendants_changing_session_are_contained=False, equivalent_to_Windows_Job_or_cgroup=False)
    src.need(same(observed["guard_scope"], scope), "Honest exact BASIC guard without a native-platform promotion")
    capture_paths = {}
    for kind in ("stdout", "stderr"):
        p = mapped(task, observed[kind+"_path"], original)
        src.need(p == task/"execution"/(kind+".txt") and p.is_file() and p.stat().st_size <= 16*src.MIB
                 and src.digest(p) == observed[kind+"_sha256"], "Actual supervisor-bound captured bytes: "+kind)
        capture_paths[kind] = p
    src.need(capture_paths["stderr"].stat().st_size == 0, "Successful original stderr is empty")
    stdout = capture_paths["stdout"].read_text("utf-8")
    result = summarize(task, row, stdout, observed, original,
                       python_executable=report["python_executable"], python_version=report["python_version"])
    src.need(src.digest(capture_paths["stdout"]) == observed["stdout_sha256"], "Actual stdout remained stable while parsing")
    return result


def validate_completed(task, *, original_task_root=None):
    task = Path(task)
    request = src.verify_job(task)
    row = src.job(request["job_id"])
    src.need(original_task_root is None or str(original_task_root) == request["original_task_root"], "One explicit originating root")
    observed = src.read(task/"STAGE_OBSERVED.json")
    complete = src.read(task/"STAGE_COMPLETED.json", limit=64*src.MIB)
    summary = validate_run(task, row, observed)
    src.need(complete["schema"] == COMPLETED and complete["scope"] == SCOPE and complete["job_id"] == row["job_id"]
             and same(complete["implementation"], observed["implementation"]) and complete["observed_sha256"] == src.digest(task/"STAGE_OBSERVED.json")
             and complete["conditional_arithmetic_completed"] is True and same(complete["summary"], summary)
             and same(complete["artifacts"], inventory(task)) and all(complete[f] is False for f in FLAGS),
             "Exact complete source/candidate/capture/receipt inventory and completed transition")
    return dict(schema="REVALIDATED_CONDITIONAL_FINITE1039_COUNT_V1", job_id=row["job_id"], lane=row["lane"],
        summary=summary, catalog_sha256=src.CATALOG_SHA256, stage_result_sha256=src.digest(task/"STAGE_COMPLETED.json"),
        source_manifest_sha256=src.digest(task/"SOURCES.json"), original_task_root=request["original_task_root"],
        conditional_arithmetic_completed=True, **{f: False for f in FLAGS})
