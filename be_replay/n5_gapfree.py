"""Fresh, bounded Linux replay of the positive closed n5 gap-free rectangle.

The old arithmetic checker and its independent worker are byte-identical.
This adapter defines a new Linux execution protocol and adds five controls.
It never establishes the unrestricted n5 theorem or an all-index conclusion.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import runpy
import shutil
import sys
import traceback
import uuid

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor/n5_gapfree_75a9470"
COMMIT = "75a94708872e2bc053f42a279559b23ed91e4402"
MANIFEST_SHA256 = "3f38d156e97f82132772b6c21aeffe4f6ad6ca254417882331fe8a9738617a40"
MIB = 1024**2
ENTRY = "n5_gapfree.py"
RESULT = "LINUX_GAPFREE_RESULT.json"
OLD_RESULT = "FRESH_GAPFREE_RESULT.json"
SOURCE_NAMES = {"check.py", "FOREST.json", "EXTERIOR.json", "c5_gapfree_worker.py", "LICENSE"}
INPUT_NAMES = {"check.py", "FOREST.json", "EXTERIOR.json"}
DOMAIN = dict(n=5, rho=["477/400", "6/5"], beta=["17/50", "35139006743001/100000000000000"],
              target="4097/10000", cdf_orientation="POSITIVE_CLOSED", phase="ALL_REAL")
CENSUS = dict(roots=60, nodes=1994, leaves=1027)
ORIGINAL_CONTROLS = ["missing root", "duplicate root", "reordered roots", "wrong rho", "wrong target",
                     "boolean root", "boolean phase", "root-domain gap", "missing tree", "false leaf",
                     "boolean leaf", "extra forest field", "false exterior n", "false exterior left_score_upper",
                     "false exterior right_score_upper", "false exterior beta"]
ADDED_CONTROLS = ["compact wrong beta", "invalid split axis", "boolean split axis", "missing split child",
                  "duplicate JSON key"]
ACCEPTED = "FRESH_LINUX_POSITIVE_CLOSED_N5_GAPFREE_RECTANGLE_ACCEPTED"


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(MIB), b""):
            result.update(block)
    return result.hexdigest()


def unique(pairs):
    output = {}
    for key, value in pairs:
        need(key not in output, "Duplicate JSON field: " + key)
        output[key] = value
    return output


def read(path, limit=2*MIB):
    path = Path(path)
    need(path.is_file() and not path.is_symlink() and path.stat().st_size <= limit,
         "Bounded ordinary JSON input: " + str(path))
    return json.loads(path.read_text("utf-8"), object_pairs_hook=unique)


def write(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")


def verify_sources(directory, *, capsule=False, outputs=()):
    """Hash the entire selected closure without importing mathematical code."""
    directory = Path(directory).resolve()
    manifest = directory / "MANIFEST.json"
    need(not manifest.is_symlink() and digest(manifest) == MANIFEST_SHA256, "Exact frozen source inventory")
    data = read(manifest)
    need(data.get("schema") == "FROZEN_N5_GAPFREE_WHOLE_LINE_INPUTS_V1"
         and data.get("source_commit") == COMMIT and set(data["files"]) == SOURCE_NAMES,
         "Complete five-file upstream closure and literal source epoch")
    need(data["domain"] == DOMAIN and data["census"] == CENSUS, "Exact positive closed whole-line rectangle")
    for name, row in data["files"].items():
        path = directory / name
        need(path.is_file() and not path.is_symlink() and path.stat().st_size == row["bytes"]
             and digest(path) == row["sha256"], "Unchanged frozen source: " + name)
    expected = SOURCE_NAMES | {"MANIFEST.json"} | set(outputs)
    if capsule:
        need(len(directory.parents) >= 4, "Deep capsule preserves the unchanged checker's parents[3] import")
        expected |= {ENTRY, "INPUTS.json", "REQUEST.json"}
        request = read(directory / "REQUEST.json")
        need(request == dict(schema="FRESH_LINUX_N5_GAPFREE_REQUEST_V1", domain=DOMAIN, census=CENSUS,
                             manifest_sha256=MANIFEST_SHA256, driver_sha256=digest(directory / ENTRY),
                             full_n5_verified=False, all_index_conclusion_verified=False),
             "This exact adapter source and complete selected request")
        need(read(directory / "INPUTS.json") == inputs(data), "Exact unchanged-worker arithmetic inputs")
    actual = set()
    for path in directory.rglob("*"):
        need(not path.is_symlink() and path.is_file(), "Flat ordinary sealed source capsule")
        actual.add(path.relative_to(directory).as_posix())
    need(actual == expected, "No missing, extra, or historical output files in the selected closure")
    return data


def inputs(manifest):
    return dict(schema="C5_GAPFREE_INDEPENDENT_REPLAY_INPUTS_V1",
                files={name: manifest["files"][name]["sha256"] for name in sorted(INPUT_NAMES)})


def census(directory):
    """Structural census only; the guarded original checker reconstructs domains."""
    forest = read(Path(directory) / "FOREST.json")
    need(set(forest) == {"schema", "rho", "beta", "target", "roots"}
         and forest["schema"] == "GAPFREE_SIGN_COUNT5_EXACT_FOREST_V1"
         and all(forest[k] == DOMAIN[k] for k in ("rho", "beta", "target")), "Literal forest region")
    roots = forest["roots"]
    need(type(roots) is list and len(roots) == 60, "All sixty compact roots")
    nodes = leaves = splits = 0
    for index, entry in enumerate(roots):
        need(set(entry) == {"domain", "tree"} and type(entry["domain"]["beta_index"]) is int
             and type(entry["domain"]["phase"]) is int
             and (entry["domain"]["beta_index"], entry["domain"]["phase"]) == divmod(index, 5),
             "Complete ordered 12 by 5 compact geometry")
        stack = [(entry["tree"], 0)]
        while stack:
            node, depth = stack.pop()
            nodes += 1
            need(type(node) is list and node and depth <= 60 and nodes <= 2000000, "Finite complete binary forest")
            if node[0] == "L":
                need(len(node) == 2 and type(node[1]) is int, "Typed compact leaf")
                leaves += 1
            else:
                need(len(node) == 4 and node[0] == "S" and type(node[1]) is int and node[1] in (0, 1),
                     "Typed split with both children")
                splits += 1
                stack.extend([(node[2], depth+1), (node[3], depth+1)])
    result = dict(roots=len(roots), nodes=nodes, leaves=leaves)
    need(result == CENSUS and nodes == 2*leaves-60 and splits > 0, "Exact whole compact census")
    exterior = read(Path(directory) / "EXTERIOR.json")["exterior"]
    need(type(exterior["n"]) is int and exterior["n"] == 5
         and all(exterior[k] == DOMAIN[k] for k in ("rho", "beta")), "Both candidate exterior rays have the same domain")
    return result


def prepare(output, *, vendor=VENDOR):
    """Create a fresh sealed capsule, without running any mathematical checker."""
    original = verify_sources(vendor)
    census(vendor)
    output = Path(output).resolve()
    need(not output.exists(), "A new private task is required; historical acceptance is never resumed")
    capsule = output / "arithmetic" / "private" / "capsule"
    capsule.mkdir(parents=True)
    for name in SOURCE_NAMES | {"MANIFEST.json"}:
        shutil.copyfile(Path(vendor) / name, capsule / name)
    shutil.copyfile(__file__, capsule / ENTRY)
    write(capsule / "INPUTS.json", inputs(original))
    write(capsule / "REQUEST.json", dict(schema="FRESH_LINUX_N5_GAPFREE_REQUEST_V1", domain=DOMAIN,
          census=CENSUS, manifest_sha256=MANIFEST_SHA256, driver_sha256=digest(__file__),
          full_n5_verified=False, all_index_conclusion_verified=False))
    verify_sources(capsule, capsule=True)
    census(capsule)
    write(output / "TASK.json", dict(schema="FRESH_LINUX_N5_GAPFREE_TASK_V1", capsule="arithmetic/private/capsule",
          driver_sha256=digest(__file__), manifest_sha256=MANIFEST_SHA256, domain=DOMAIN, census=CENSUS,
          native_arithmetic_accepted=False, full_n5_verified=False, all_index_conclusion_verified=False))
    return output


def additional_controls(module, forest):
    """Five malformed-input controls added by this explicitly new protocol."""
    controls = []
    def reject(call, label):
        try:
            call()
        except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError):
            controls.append(label)
        else:
            raise ValueError("Corruption accepted: " + label)
    split = next(i for i, root in enumerate(forest["roots"]) if root["tree"][0] == "S")
    mutations = [(ADDED_CONTROLS[0], lambda q: q["beta"].__setitem__(0, "347/1000")),
                 (ADDED_CONTROLS[1], lambda q: q["roots"][split]["tree"].__setitem__(1, 2)),
                 (ADDED_CONTROLS[2], lambda q: q["roots"][split]["tree"].__setitem__(1, True)),
                 (ADDED_CONTROLS[3], lambda q: q["roots"][split]["tree"].pop())]
    for label, change in mutations:
        bad = deepcopy(forest)
        change(bad)
        reject(lambda: module.validate(bad), label)
    reject(lambda: json.loads('{"n":5,"n":6}', object_pairs_hook=module.unique), ADDED_CONTROLS[4])
    need(controls == ADDED_CONTROLS, "All five additional parser and coverage controls")
    return controls


def validate_original(packet, manifest):
    need(packet["status"] == "PASS_FRESH_C5_GAPFREE_INDEPENDENT_WHOLE_LINE"
         and type(packet["n"]) is int and packet["n"] == 5
         and all(packet[k] == DOMAIN[k] for k in ("rho", "beta", "target")), "Exact observed independent whole-line result")
    need(packet["inputs"] == inputs(manifest)
         and packet["adapter_sha256"] == manifest["files"]["c5_gapfree_worker.py"]["sha256"],
         "Original independent worker and exact mathematical input identities")
    compact = packet["compact"]
    need(all(type(compact[k]) is int and compact[k] == CENSUS[k] for k in CENSUS), "All original compact roots, nodes and leaves")
    need(Fraction(compact["independent_upper"]) <= Fraction(compact["stored_upper"]) < Fraction(DOMAIN["target"]),
         "Fresh strict compact score")
    rays = packet["exteriors"]
    need(rays["left_domain"] == "z<=0" and rays["right_domain"] == "z>=5"
         and 0 <= Fraction(rays["left_upper"]) < Fraction(331, 1000)
         and 0 <= Fraction(rays["right_upper"]) < Fraction(187, 1000), "Both complete infinite exterior rays")
    need(packet["negative_controls"] == ORIGINAL_CONTROLS, "All sixteen unchanged independent-worker controls")
    need(packet["old_capture_metadata_used_as_a_mathematical_premise"] is False
         and packet["unrestricted_C5_or_all_indices_verified_by_this_stage"] is False, "No historical or unrestricted theorem premise")
    return dict(compact=compact, exteriors=rays)


def worker():
    """Only the bounded native child calls this; never used by preparation fixtures."""
    need(__debug__ and sys.dont_write_bytecode and not sys.flags.optimize, "Ordinary unoptimized -B Python")
    capsule = Path(__file__).resolve().parent
    manifest = verify_sources(capsule, capsule=True)
    census(capsule)
    print(json.dumps(dict(event="n5_gapfree_native_arithmetic_started", census=CENSUS, domain=DOMAIN,
                          native_arithmetic_accepted=False)), flush=True)
    # Run the unchanged worker main, which independently evaluates every leaf,
    # reconstructs both rays, runs its sixteen controls, and hashes its inputs.
    original = runpy.run_path(str(capsule / "c5_gapfree_worker.py"), run_name="frozen_independent_worker")
    original["main"]()
    old = read(capsule / OLD_RESULT)
    details = validate_original(old, manifest)
    spec = importlib.util.spec_from_file_location("unchanged_gapfree_extra_controls", capsule / "check.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    added = additional_controls(module, read(capsule / "FOREST.json"))
    verify_sources(capsule, capsule=True, outputs={OLD_RESULT})
    census(capsule)
    packet = dict(schema="FRESH_LINUX_N5_GAPFREE_WHOLE_LINE_RESULT_V1", status="NATIVE_WORKER_COMPLETED",
                  domain=DOMAIN, census=CENSUS, **details, original_controls=ORIGINAL_CONTROLS,
                  added_controls=added, control_count=21, manifest_sha256=MANIFEST_SHA256,
                  driver_sha256=digest(__file__), original_result_sha256=digest(capsule / OLD_RESULT),
                  inputs_sha256={name: digest(capsule / name) for name in sorted(SOURCE_NAMES)},
                  original_checker_main_called=False, historical_execution_used_as_a_premise=False,
                  full_n5_verified=False, all_index_conclusion_verified=False)
    write(capsule / RESULT, packet)
    print(json.dumps(packet, sort_keys=True), flush=True)


def check_execution(task, observed, *, supervisor_sha, cpu_seconds):
    """Accept actual bounded native execution plus the exact new protocol packet."""
    from .small_indices import trusted_guard
    task = Path(task).resolve()
    capsule = task / "arithmetic/private/capsule"
    need(observed.get("status") == "completed" and type(observed.get("returncode")) is int
         and observed["returncode"] == 0, "Exact integer successful bounded native completion")
    need(supervisor_sha == digest(Path(__file__).with_name("linux_supervisor.py"))
         and digest(capsule / ENTRY) == digest(__file__), "Same reviewed supervisor and adapter source after execution")
    need(trusted_guard(observed, script_sha=digest(capsule / ENTRY), supervisor_sha=supervisor_sha,
                       memory_bytes=512*MIB, cpu_seconds=cpu_seconds), "Established 64+448 MiB single-process native guard")
    for kind in ("stdout", "stderr"):
        path = Path(observed[kind + "_path"])
        need(path.resolve() == (task / "execution" / (kind + ".txt")).resolve()
             and path.is_file() and not path.is_symlink() and path.stat().st_size <= 16*MIB
             and digest(path) == observed.get(kind + "_sha256"), "Actual bounded log matches supervisor capture")
    need(Path(observed["stderr_path"]).stat().st_size == 0, "Successful whole-line native replay has empty stderr")
    manifest = verify_sources(capsule, capsule=True, outputs={OLD_RESULT, RESULT})
    census(capsule)
    details = validate_original(read(capsule / OLD_RESULT), manifest)
    result = read(capsule / RESULT)
    expected = dict(schema="FRESH_LINUX_N5_GAPFREE_WHOLE_LINE_RESULT_V1", status="NATIVE_WORKER_COMPLETED",
                    domain=DOMAIN, census=CENSUS, **details, original_controls=ORIGINAL_CONTROLS,
                    added_controls=ADDED_CONTROLS, control_count=21, manifest_sha256=MANIFEST_SHA256,
                    driver_sha256=digest(__file__), original_result_sha256=digest(capsule / OLD_RESULT),
                    inputs_sha256={name: digest(capsule / name) for name in sorted(SOURCE_NAMES)},
                    original_checker_main_called=False, historical_execution_used_as_a_premise=False,
                    full_n5_verified=False, all_index_conclusion_verified=False)
    need(result == expected and type(result["control_count"]) is int, "Complete exact Linux whole-line protocol packet")
    lines = Path(observed["stdout_path"]).read_text("utf-8").splitlines()
    need(lines and json.loads(lines[-1], object_pairs_hook=unique) == result, "Actual complete native terminal packet")
    return result


def run(task, *, wall_seconds=7260, cpu_seconds=7200):
    from . import count_task as common
    from .small_indices import FollowOutput, Progress
    need(type(wall_seconds) is int and 1 <= wall_seconds <= 7260
         and type(cpu_seconds) is int and 2 <= cpu_seconds <= 7200, "At most 7260 wall seconds and 7200 total native CPU seconds")
    task = Path(task).resolve()
    capsule = task / "arithmetic/private/capsule"
    need(read(task / "TASK.json") == dict(schema="FRESH_LINUX_N5_GAPFREE_TASK_V1", capsule="arithmetic/private/capsule",
         driver_sha256=digest(__file__), manifest_sha256=MANIFEST_SHA256, domain=DOMAIN, census=CENSUS,
         native_arithmetic_accepted=False, full_n5_verified=False, all_index_conclusion_verified=False), "Exact fresh task/source binding")
    verify_sources(capsule, capsule=True)
    census(capsule)
    need(not (task / "execution").exists(), "Every native attempt requires a new fresh capsule")
    supervisor_sha = digest(Path(__file__).with_name("linux_supervisor.py"))
    command = [sys.executable, "-B", "-S", str(capsule / ENTRY), "--_worker"]
    report = dict(schema="FRESH_LINUX_N5_GAPFREE_EXECUTION_V1", status="PARTIAL_NOT_ACCEPTED", command=command,
                  domain=DOMAIN, census=CENSUS, manifest_sha256=MANIFEST_SHA256, driver_sha256=digest(__file__),
                  supervisor_sha256=supervisor_sha, wall_seconds=wall_seconds, cpu_seconds=cpu_seconds,
                  native_arithmetic_accepted=False, full_n5_verified=False, all_index_conclusion_verified=False)
    progress = Progress(task / "FOLLOW_PROGRESS.jsonl")
    try:
        progress.emit("n5_gapfree_guarded_execution_started", census=CENSUS, original_controls=16,
                      added_controls=5, wall_seconds=wall_seconds, cpu_seconds=cpu_seconds,
                      native_arithmetic_accepted=False)
        with FollowOutput("n5-gapfree-whole-line", task / "execution/stdout.txt", progress, 20):
            observed = common.supervise(command, cwd=capsule, output_dir=task / "execution",
                       wall_seconds=wall_seconds, cpu_seconds=cpu_seconds, memory_bytes=512*MIB,
                       mode="trusted_native", disk_bytes=256*MIB, log_bytes=16*MIB)
        report["observed"] = observed
        report["native_result"] = check_execution(task, observed, supervisor_sha=supervisor_sha, cpu_seconds=cpu_seconds)
        report.update(status=ACCEPTED, native_arithmetic_accepted=True)
    except BaseException as error:
        report["error"] = type(error).__name__ + ": " + str(error)
        (task / "ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
    finally:
        progress.emit("n5_gapfree_guarded_execution_finished", status=report["status"],
                      native_arithmetic_accepted=report["native_arithmetic_accepted"],
                      full_n5_verified=False, all_index_conclusion_verified=False)
        progress.close()
        write(task / "EXECUTION_RESULT.json", report)
    return report


def run_colab(*, durable_root, work_root="/content/berry-esseen-runs", backup_interval=60,
              wall_seconds=7260, cpu_seconds=7200):
    """Fresh unchanged arithmetic, visible progress, live copies, final evidence ZIP."""
    from . import colab_batch
    from .environment import snapshot
    need(type(backup_interval) in (int, float) and backup_interval > 0, "Positive backup interval")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    root = Path(work_root) / "n5-gapfree" / stamp
    root.mkdir(parents=True)
    durable = Path(durable_root) / "n5-gapfree" / stamp
    status = dict(scope="POSITIVE_CLOSED_N5_GAPFREE_RECTANGLE_ONLY", state="started", domain=DOMAIN,
                  census=CENSUS, native_arithmetic_accepted=False, full_n5_verified=False,
                  all_index_conclusion_verified=False)
    colab_batch.atomic_json(root / "SESSION_RESULT.json", status)
    monitor = colab_batch.Backups(root, durable, interval=backup_interval)
    monitor.start()
    try:
        colab_batch.event(root, "n5_gapfree_job_started", domain=DOMAIN, census=CENSUS, controls=21,
                          full_n5_verified=False, all_index_conclusion_verified=False)
        colab_batch.atomic_json(root / "ENVIRONMENT.json", snapshot())
        task = prepare(root / "task")
        result = run(task, wall_seconds=wall_seconds, cpu_seconds=cpu_seconds)
        status.update(state=result["status"], native_arithmetic_accepted=result["native_arithmetic_accepted"], result=result)
    except BaseException as error:
        status.update(state="PARTIAL_ERROR_NOT_ACCEPTED", error=type(error).__name__ + ": " + str(error))
        (root / "ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        colab_batch.event(root, "n5_gapfree_job_incomplete", error=status["error"])
    finally:
        colab_batch.atomic_json(root / "SESSION_RESULT.json", status)
        try:
            monitor.close()
        except Exception as error:
            colab_batch.event(root, "final_backup_failed", error=str(error))
        output = colab_batch.bundle(root, durable)
        colab_batch.event(root, "n5_gapfree_results_bundle_saved", path=str(output), state=status["state"],
                          full_n5_verified=False, all_index_conclusion_verified=False)
    print("\nRESULT:", status["state"], "\nZIP:", output, flush=True)
    return dict(status=status, bundle=str(output), work=str(root))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare", help="Freeze a fresh private capsule; no arithmetic is executed")
    prep.add_argument("output", type=Path)
    execution = commands.add_parser("run", help="Run the unchanged whole-line arithmetic under the native Linux guard")
    execution.add_argument("task", type=Path)
    execution.add_argument("--wall-seconds", type=int, default=7260)
    execution.add_argument("--cpu-seconds", type=int, default=7200)
    args = parser.parse_args()
    if args.command == "prepare":
        print(prepare(args.output), flush=True)
        return 0
    result = run(args.task, wall_seconds=args.wall_seconds, cpu_seconds=args.cpu_seconds)
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if result["native_arithmetic_accepted"] else 2


if __name__ == "__main__":
    if sys.argv[1:] == ["--_worker"]:
        try:
            worker()
        except Exception as error:
            print("FRESH_LINUX_N5_GAPFREE_INCOMPLETE: " + str(error), file=sys.stderr, flush=True)
            raise SystemExit(1)
    else:
        raise SystemExit(main())
