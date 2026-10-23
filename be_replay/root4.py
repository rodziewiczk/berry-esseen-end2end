"""Derive a sealed Linux ROOT4 resource epoch, then run the entire two-pass kernel.

The original 73 Python sources remain byte-pinned. Only the Windows memory
monitor and four transitive literal source hashes change in a private capsule.
All other ASTs must agree after replacing source hashes by their file names.
The actual producer and replay each rebuild all 1300 HIGH slots and 260 parents.
No checkpoint is an input to either calculation. No all-law claim is made here.
"""
from __future__ import annotations

import argparse
import ast
from contextlib import contextmanager
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import traceback
import uuid
import warnings

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor" / "root4_75a9470"
COMMIT = "75a94708872e2bc053f42a279559b23ed91e4402"
MANIFEST_SHA256 = "eb3541112dd78d0bcef22ae8bb7fa4b307760199e478d43e35ad0c255b76053d"
ENTRY = "n4_cpu_time_entire_root_2026_10_09.py"
MONITOR = "n4_windows_resource_guard_2026_10_09.py"
EPOCH_SCHEMA = "ROOT4_LINUX_RSS_RESOURCE_EPOCH_V1"
EPOCH_SHA256 = "63f409204df8b1a786ce049dfdd1868f6b7fb736fc4053729b228f7675ce3a90"
MIB = 1024 ** 2
WORKER_MEMORY = 256 * MIB
CONTROLLER_MEMORY = 64 * MIB
TOTAL_MEMORY = WORKER_MEMORY + CONTROLLER_MEMORY
WORKER_CPU = 43200
TOTAL_CPU = WORKER_CPU + 30
TARGET = Fraction(4097, 10000)
OUTPUT_NAME = Path(ENTRY).stem + "_ALL260_W20_B13_N256_H1_8_ETA16_five_budget.json"
EXPECTED_CHANGED = {
    MONITOR,
    "n4_cpu_time_quadrature_cache_2026_10_09.py",
    "n4_cpu_time_cheap_linked_leaf_2026_10_09.py",
    "n4_cpu_time_geometry_join_2026_10_09.py",
    ENTRY,
}

# This is the entire reviewed resource-only replacement. Linux ru_maxrss is
# a kernel-maintained maximum resident-set size in KiB, not Windows working set.
# The strict original 64MiB HIGH and 256MiB whole-process gates remain intact.
LINUX_MONITOR = b'''"""Linux self RSS monitor for the separate ROOT4 resource epoch.

This resource module supplies no mathematical values. ru_maxrss is the Linux
kernel's process lifetime maximum RSS, in KiB. Query failure fails closed.
The externally guarded worker retains a hard 256MiB address-space cap.
The original Windows monitor remains unchanged in the frozen vendor tree.
"""
from __future__ import annotations
import os
import resource
import sys


def peak_bytes():
    if sys.platform != "linux":
        raise RuntimeError("The derived ROOT4 resource epoch requires actual Linux")
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if type(value) is not int or value <= 0:
        raise RuntimeError("Missing positive kernel-maintained Linux peak RSS")
    return value * 1024


def current_working_set_bytes():
    if sys.platform != "linux":
        raise RuntimeError("The derived ROOT4 resource epoch requires actual Linux")
    with open("/proc/self/statm", "r", encoding="ascii") as stream:
        fields = stream.read(1024).split()
    if len(fields) < 2 or not fields[1].isdigit():
        raise RuntimeError("Missing Linux self resident-page count")
    value = int(fields[1]) * os.sysconf("SC_PAGE_SIZE")
    if value <= 0:
        raise RuntimeError("Missing positive Linux current RSS")
    return value


current_working_set = current_working_set_bytes
'''


def need(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while block := stream.read(MIB):
            value.update(block)
    return value.hexdigest()


def read(path, limit=4 * MIB):
    path = Path(path)
    need(path.is_file() and not path.is_symlink() and path.stat().st_size <= limit,
         "Bounded regular JSON input")
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def tree(raw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        return ast.parse(raw)


def verify_frozen(directory=None):
    """Verify every source/note/license byte before any source can execute."""
    directory = VENDOR if directory is None else Path(directory)
    need(directory.is_dir() and not directory.is_symlink(), "Ordinary frozen ROOT4 directory")
    manifest_path = directory / "MANIFEST.json"
    need(manifest_path.is_file() and not manifest_path.is_symlink()
         and digest(manifest_path) == MANIFEST_SHA256, "Pinned ROOT4 source manifest")
    manifest = read(manifest_path)
    need(manifest["schema"] == "FROZEN_ROOT4_SOURCE_CLOSURE_V1"
         and manifest["source_commit"] == COMMIT and manifest["entry"] == ENTRY
         and manifest["python_files"] == 73 and manifest["arithmetic_accepted"] is False,
         "Exact historical ROOT4 source identity, never acceptance")
    names = set(manifest["files"])
    need({p.name for p in directory.iterdir()} == names | {"MANIFEST.json"},
         "Exact frozen ROOT4 file inventory")
    files = {}
    for name, record in manifest["files"].items():
        path = directory / name
        need(Path(name).name == name and path.is_file() and not path.is_symlink()
             and path.stat().st_size == record["bytes"], "Bounded ordinary frozen source: " + name)
        raw = path.read_bytes()
        need(sha(raw) == record["sha256"], "Frozen ROOT4 source SHA mismatch: " + name)
        files[name] = raw
    need(sum(name.endswith(".py") for name in files) == 73, "All 73 original Python sources")
    return files


def pin_graph(files):
    """Literal source hashes form an acyclic graph; never infer math from pins."""
    old = {sha(raw): name for name, raw in files.items() if name.endswith(".py")}
    need(len(old) == 73, "Unique original Python source hashes")
    graph = {}
    for name, raw in files.items():
        if not name.endswith(".py"):
            continue
        literals = {node.value for node in ast.walk(tree(raw))
                    if isinstance(node, ast.Constant) and type(node.value) is str}
        hexes = {value for value in literals if len(value) == 64
                 and all(char in "0123456789abcdef" for char in value)}
        need(hexes <= set(old), "Every literal ROOT4 source pin resolves inside the frozen closure")
        graph[name] = sorted(old[value] for value in hexes)
    ordered, active, done = [], set(), set()

    def visit(name):
        need(name not in active, "No cyclic literal source-pin dependency")
        if name in done:
            return
        active.add(name)
        for dependency in graph[name]:
            visit(dependency)
        active.remove(name)
        done.add(name)
        ordered.append(name)

    for name in sorted(graph):
        visit(name)
    return graph, ordered


def ast_projection(raw, hash_names):
    class SourcePins(ast.NodeTransformer):
        def visit_Constant(self, node):
            if type(node.value) is str and node.value in hash_names:
                return ast.copy_location(ast.Constant("SOURCE_SHA256:" + hash_names[node.value]), node)
            return node
    def stable(node):
        if isinstance(node, ast.AST):
            # CPython 3.12 added empty type_params to FunctionDef/ClassDef.
            # They carry no semantics here and must not make a source epoch
            # depend on the preparer's or Colab's Python minor version.
            return (type(node).__name__, tuple(
                (name, stable(value)) for name, value in ast.iter_fields(node)
                if not (name == "type_params" and value == [])))
        if isinstance(node, list):
            return tuple(stable(value) for value in node)
        return node
    return repr(stable(SourcePins().visit(tree(raw))))


def _derive_sources(files):
    """Deterministically replace one resource module and rebind four callers."""
    graph, order = pin_graph(files)
    result = dict(files)
    original_pins = {name: sha(raw) for name, raw in files.items() if name.endswith(".py")}
    new_pins = {}
    changes = {}
    for name in order:
        raw = files[name]
        if name == MONITOR:
            result[name] = LINUX_MONITOR
            changes[name] = {"resource_helper_replacement": True}
        else:
            replacements = {}
            for dependency in graph[name]:
                before, after = original_pins[dependency], new_pins[dependency]
                if before != after:
                    need(before.encode("ascii") in raw, "Literal pin replacement is present")
                    raw = raw.replace(before.encode("ascii"), after.encode("ascii"))
                    replacements[dependency] = {"old_sha256": before, "new_sha256": after}
            result[name] = raw
            if replacements:
                changes[name] = {"literal_source_pin_rebindings": replacements}
        new_pins[name] = sha(result[name])
    need(set(changes) == EXPECTED_CHANGED and sum(map(len, graph.values())) == 125,
         "Exactly one monitor and four source-pin callers; original 125 pin edges")
    names = {pin: name for name, pin in original_pins.items()}
    names.update({pin: name for name, pin in new_pins.items()})
    projections = {}
    for name in order:
        if name == MONITOR:
            continue
        before, after = ast_projection(files[name], names), ast_projection(result[name], names)
        need(before == after, "Every mathematical AST remains unchanged: " + name)
        if name not in changes:
            need(result[name] == files[name], "Unchanged source bytes outside the five derived files")
        projections[name] = sha(before.encode("utf-8"))
    epoch = dict(schema=EPOCH_SCHEMA, source_commit=COMMIT,
                 original_manifest_sha256=MANIFEST_SHA256, entry=ENTRY,
                 files={name: {"bytes": len(raw), "sha256": sha(raw)} for name, raw in sorted(result.items())},
                 changes=changes, mathematical_ast_projections=projections,
                 original_pin_graph_edges=125, python_sources=73,
                 memory_measure="Linux kernel RUSAGE_SELF ru_maxrss * 1024; RSS, not Windows working set",
                 worker_RLIMIT_AS_bytes=WORKER_MEMORY, supervisor_RLIMIT_AS_bytes=CONTROLLER_MEMORY,
                 original_cooperative_HIGH_RSS_limit_bytes=64 * MIB,
                 original_cooperative_ROOT_RSS_limit_bytes=WORKER_MEMORY,
                 original_CPU_limit_seconds=WORKER_CPU,
                 mathematical_arithmetic_accepted=False, all_index_conclusion_verified=False)
    return result, epoch


def derive_sources(files):
    result, epoch = _derive_sources(files)
    need(sha(canonical(epoch)) == EPOCH_SHA256, "Exact sealed portable ROOT4 epoch")
    return result, epoch


def prepare(output, *, vendor=None):
    output = Path(output).resolve()
    need(not output.exists(), "Fresh private ROOT4 capsule; no overwrite or resume")
    sources, epoch = derive_sources(verify_frozen(vendor))
    output.mkdir(parents=True, exist_ok=False)
    for name, raw in sources.items():
        with (output / name).open("xb") as stream:
            stream.write(raw)
    with (output / "SOURCE_EPOCH.json").open("xb") as stream:
        stream.write(canonical(epoch))
    return epoch


def verify_capsule(capsule):
    capsule = Path(capsule)
    need(not capsule.is_symlink(), "Ordinary private ROOT4 capsule")
    capsule = capsule.resolve()
    sources, epoch = derive_sources(verify_frozen())
    need(capsule.is_dir() and not capsule.is_symlink(), "Ordinary private ROOT4 capsule")
    need(read(capsule / "SOURCE_EPOCH.json") == epoch, "Exact portable source epoch record")
    need({p.name for p in capsule.iterdir() if p.suffix == ".py"} ==
         {name for name in sources if name.endswith(".py")}, "No extra executable Python source")
    for name, raw in sources.items():
        path = capsule / name
        need(path.is_file() and not path.is_symlink() and path.stat().st_size == len(raw)
             and digest(path) == sha(raw), "Private ROOT4 source drift: " + name)
    return epoch


def command(capsule, stage):
    need(stage in ("produce", "replay"), "The two original ROOT4 CLI modes only")
    capsule = Path(capsule).resolve()
    return [sys.executable, "-B", "-S", str(capsule / ENTRY),
            "--produce" if stage == "produce" else "--replay-existing"]


def supervise(argv, **options):
    from .linux_supervisor import run
    return run(argv, **options)


@contextmanager
def syntax_warning_policy():
    """Only suppress the pinned legacy docstring invalid-escape SyntaxWarning.

    No source byte or mathematical AST changes. Other warning settings survive;
    exceptions and other warnings remain visible and fail stderr.
    """
    previous = os.environ.get("PYTHONWARNINGS")
    os.environ["PYTHONWARNINGS"] = (((previous + ",") if previous else "")
                                   + "ignore:invalid escape sequence:SyntaxWarning")
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop("PYTHONWARNINGS", None)
        else:
            os.environ["PYTHONWARNINGS"] = previous


def guard_verified(observed, capsule):
    guard = observed.get("guard_scope") or {}
    supervisor = Path(__file__).with_name("linux_supervisor.py")
    return (guard.get("kind") == "LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1"
            and guard.get("capability_established") is True
            and guard.get("native_python_execution") is True
            and guard.get("hard_sum_RLIMIT_AS_bytes") == TOTAL_MEMORY
            and guard.get("worker_RLIMIT_AS_bytes") == WORKER_MEMORY
            and guard.get("supervisor_RLIMIT_AS_bytes") == CONTROLLER_MEMORY
            and guard.get("hard_sum_RLIMIT_CPU_seconds") == TOTAL_CPU
            and guard.get("worker_RLIMIT_CPU_seconds") == WORKER_CPU
            and guard.get("supervisor_RLIMIT_CPU_seconds") == 30
            and guard.get("script_sha256") == digest(Path(capsule) / ENTRY)
            and guard.get("supervisor_source_sha256") == digest(supervisor))


def terminal_packet(observed):
    if not (observed.get("status") == "completed" and type(observed.get("returncode")) is int
            and observed["returncode"] == 0):
        details = {key: observed.get(key) for key in
                   ("status", "reason", "returncode", "stdout_path", "stderr_path")}
        name = observed.get("stderr_path")
        if name:
            path = Path(name)
            if path.is_file() and not path.is_symlink() and path.stat().st_size <= 16 * MIB:
                with path.open("rb") as stream:
                    stream.seek(max(0, path.stat().st_size - 8192))
                    details["stderr_tail"] = stream.read(8192).decode("utf-8", errors="replace")
        raise ValueError("The full guarded ROOT4 process did not finish; no acceptance. "
                         + json.dumps(details, ensure_ascii=True))
    path = Path(observed["stdout_path"])
    need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 16 * MIB,
         "Bounded actual ROOT4 stdout")
    need(digest(path) == observed.get("stdout_sha256"), "Actual stdout capture matches its supervisor SHA")
    stderr = Path(observed["stderr_path"])
    need(stderr.is_file() and not stderr.is_symlink() and stderr.stat().st_size <= 16 * MIB
         and digest(stderr) == observed.get("stderr_sha256"),
         "Actual stderr capture matches its supervisor SHA")
    need(stderr.stat().st_size == 0, "Successful ROOT4 native execution has empty stderr")
    with path.open("rb") as stream:
        last = None
        for line in stream:
            if line.strip():
                last = line
    need(last is not None, "Actual ROOT4 terminal result")
    need(digest(path) == observed["stdout_sha256"], "Stdout capture remains stable while parsing")
    return json.loads(last, object_pairs_hook=unique)


def validate_terminal(packet, stage, capsule):
    expected = {"EXACT_CONDITIONAL_ENTIRE_PHYSICAL_ROOT_PORTFOLIO",
                "UNKNOWN_WITH_ENTIRE_ROOT_AND_ALL_PORTFOLIO_GAPS_RETAINED"}
    need(packet.get("status") in (expected if stage == "produce" else
                                 {"READ_ONLY_REPLAY_ALL_NONRESOURCE_FIELDS_MATCH"}),
         "Exact original full-producer or full-replay terminal identity")
    need(Path(packet["result"]).resolve() == (Path(capsule) / OUTPUT_NAME).resolve(),
         "The complete result belongs to this exact private capsule")
    summary, pending = packet["summary"], packet["unresolved_geometry_indices"]
    need(type(pending) is list and all(type(i) is int and 0 <= i < 260 for i in pending)
         and pending == sorted(set(pending)), "Every unresolved geometry retained in order")
    counts = {"geometry_classes_total": 260, "closed_geometry_classes": 260 - len(pending),
              "unresolved_geometry_classes": len(pending), "ALL_high_request_slots_accounted": 1300,
              "fixed_geometry_max_depth": 1}
    need(all(type(summary.get(k)) is int and summary[k] == v for k, v in counts.items()),
         "All 260 parent classes, all 1300 HIGH slots, original closed-child depth")
    upper_text = summary["entire_conditional_root_score_upper_exact"]
    need(type(upper_text) is str, "Exact rational root bound")
    upper = Fraction(upper_text)
    passed = not pending and upper <= TARGET
    if stage == "produce":
        need((packet["status"] == "EXACT_CONDITIONAL_ENTIRE_PHYSICAL_ROOT_PORTFOLIO") == passed,
             "Producer status agrees with the complete exact result")
    resources = packet["resources"]
    need(resources.get("budget_clock_basis") == "time.process_time"
         and resources.get("time_limit_seconds") == WORKER_CPU
         and resources.get("memory_limit_bytes") == WORKER_MEMORY
         and resources.get("read_only_replay_wrote_any_checkpoint") is False,
         "Original CPU and memory policy, no replay checkpoint writer")
    for key, limit in (("actual_CLI_cpu_seconds", WORKER_CPU),
                       ("actual_CLI_peak_working_set_bytes", WORKER_MEMORY)):
        value = resources.get(key)
        need(type(value) in (int, float) and math.isfinite(value) and 0 <= value <= limit,
             "Actual full-CLI resource observation: " + key)
    need(resources["actual_CLI_peak_working_set_bytes"] > 0, "Real kernel RSS observation")
    return dict(complete_full_root_computation=True, conditional_target_closed=passed,
                root_bound_exact=str(upper), unresolved_geometry_indices=pending, summary=summary)


def run(output, *, wall_seconds=54000, heartbeat_seconds=60):
    """Compute both complete passes. Unsupported native guards never fall back."""
    from .colab_batch import atomic_json, event
    need(type(wall_seconds) is int and 1 <= wall_seconds <= 86400,
         "External wall cap per full pass, at most 24 hours")
    output = Path(output).resolve()
    need(not output.exists(), "Fresh ROOT4 run directory")
    output.mkdir(parents=True, exist_ok=False)
    capsule = output / "capsule"
    epoch = prepare(capsule)
    report = dict(schema="ROOT4_TWO_FRESH_FULL_PASSES_V1", source_epoch_sha256=EPOCH_SHA256,
                  source_commit=COMMIT, source_epoch=epoch, stages=[],
                  legacy_docstring_warning_policy="ignore:invalid escape sequence:SyntaxWarning; other warnings preserved",
                  all_required_stages_computed=False, native_arithmetic_accepted=False,
                  conditional_physical_root_verified=False, all_law_C4_verified=False,
                  all_index_conclusion_verified=False)
    atomic_json(output / "ROOT4_RESULT.json", report)
    receipt = capsule / OUTPUT_NAME
    for stage in ("produce", "replay"):
        verify_capsule(capsule)
        before = digest(receipt) if receipt.exists() else None
        need((stage == "produce" and before is None) or (stage == "replay" and before is not None),
             "Fresh producer first; complete produced receipt is the replay comparison input")
        event(output, "root4_full_" + stage + "_started", source_epoch_sha256=EPOCH_SHA256,
              worker_memory_bytes=WORKER_MEMORY, HIGH_memory_bytes=64 * MIB,
              worker_CPU_seconds=WORKER_CPU, full_parents=260, HIGH_slots=1300,
              native_arithmetic_accepted=False)
        with syntax_warning_policy():
            observed = supervise(command(capsule, stage), cwd=capsule,
                                 output_dir=output / (stage + "-execution"),
                                 wall_seconds=wall_seconds, cpu_seconds=TOTAL_CPU,
                                 memory_bytes=TOTAL_MEMORY, mode="trusted_native",
                                 disk_bytes=512 * MIB, log_bytes=16 * MIB,
                                 heartbeat_seconds=heartbeat_seconds)
        row = dict(stage=stage, observed=observed, completed=False, native_guard_verified=False)
        report["stages"].append(row)
        atomic_json(output / "ROOT4_RESULT.json", report)
        # Guard/source errors retain every produced checkpoint and actual log.
        packet = terminal_packet(observed)
        verify_capsule(capsule)
        need(receipt.is_file() and not receipt.is_symlink() and receipt.stat().st_size <= 48 * MIB,
             "Complete original bounded ROOT4 receipt")
        after = digest(receipt)
        need(stage != "replay" or before == after, "Read-only replay preserves every receipt byte")
        need(guard_verified(observed, capsule),
             "Established single-process native contract required; no basic-guard acceptance")
        checked = validate_terminal(packet, stage, capsule)
        row.update(completed=True, native_guard_verified=True, terminal_result=packet,
                   receipt_sha256=after, **checked)
        atomic_json(output / "ROOT4_RESULT.json", report)
        event(output, "root4_full_" + stage + "_finished", **checked,
              native_arithmetic_accepted=False)
    first, second = report["stages"]
    need(first["receipt_sha256"] == second["receipt_sha256"]
         and first["summary"] == second["summary"], "Both full passes agree on all mathematical output")
    accepted = first["conditional_target_closed"] and second["conditional_target_closed"]
    report.update(all_required_stages_computed=True, native_arithmetic_accepted=accepted,
                  conditional_physical_root_verified=accepted,
                  root_bound_exact=second["root_bound_exact"],
                  state="conditional_physical_root_verified" if accepted else
                        "complete_two_pass_arithmetic_with_unresolved_root_classes")
    atomic_json(output / "ROOT4_RESULT.json", report)
    return report


def run_colab(*, durable_root, work_root="/content/berry-esseen-runs",
              wall_seconds=54000, backup_interval=60):
    from .colab_batch import Backups, atomic_json, bundle, event, utc
    from .environment import snapshot
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    root = Path(work_root).resolve() / "root4" / stamp
    root.mkdir(parents=True, exist_ok=False)
    durable = Path(durable_root).resolve() / "root4" / stamp
    status = dict(scope="CONDITIONAL_PHYSICAL_ROOT4_ONLY", state="started", started_utc=utc(),
                  source_epoch_sha256=EPOCH_SHA256, native_arithmetic_accepted=False,
                  all_law_C4_verified=False, all_index_conclusion_verified=False,
                  work=str(root), durable=str(durable))
    atomic_json(root / "ENVIRONMENT.json", snapshot())
    atomic_json(root / "SESSION_RESULT.json", status)
    monitor = Backups(root, durable, interval=backup_interval)
    monitor.start()
    try:
        event(root, "root4_two_complete_passes_started", full_parents_per_pass=260,
              HIGH_slots_per_pass=1300, full_recomputations=2, wall_seconds_per_pass=wall_seconds,
              worker_CPU_seconds_per_pass=WORKER_CPU, all_index_conclusion_verified=False)
        result = run(root / "arithmetic", wall_seconds=wall_seconds, heartbeat_seconds=60)
        status.update(state=result["state"], arithmetic_result=result,
                      native_arithmetic_accepted=result["native_arithmetic_accepted"])
    except BaseException as error:
        status.update(state="incomplete_error", error=type(error).__name__ + ": " + str(error))
        (root / "ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        event(root, "root4_incomplete_error", error=status["error"], native_arithmetic_accepted=False)
    finally:
        status["finished_utc"] = utc()
        atomic_json(root / "SESSION_RESULT.json", status)
        try:
            monitor.close()
        except Exception as error:
            event(root, "root4_final_backup_failed", error=str(error))
        archive = bundle(root, durable)
        event(root, "root4_results_bundle_saved", path=str(archive), state=status["state"],
              all_law_C4_verified=False, all_index_conclusion_verified=False)
    print("\nRESULT:", status["state"], "\nZIP:", archive, flush=True)
    return dict(status=status, bundle=str(archive.resolve()), work=str(root.resolve()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--wall-seconds", type=int, default=54000)
    args = parser.parse_args()
    result = prepare(args.output) if args.prepare_only else run(args.output, wall_seconds=args.wall_seconds)
    print(json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
