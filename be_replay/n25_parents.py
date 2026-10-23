"""Fresh, conditional n25 B3/B4 INITIAL and resource acquisitions.

The four unchanged native actions really construct and independently replay
the complete objects.  The stronger24 auxiliary receipt is an imported
premise.  Neither its acquisition nor any subsequent count/interface join is
established here.  A stopped action has no internal restart checkpoint.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import sys
import traceback
import uuid
import zipfile

from . import count_task as common

MIB = 1024**2
STAGES = ("initial-construct", "initial-accept", "resource-construct", "resource-accept")
BRANCHES = {
    "b3": dict(initial_manifest="924d0f64a8f7454ead9c36ff28d7026f1ba0fa56ecdc05ff4333b175cdc09b12",
               resource_manifest="109e5298997f69d0efaeb4831412d575915972e2916fe6a205f188a74fa011a7",
               radius="31/10", cap="434477/1000000", rho_lo="13/10", rho_hi="7/5"),
    "b4": dict(initial_manifest="f5c63d15fefd27090068c31ef080c4de4929c5ebefae62c27b7084baed50a0dc",
               resource_manifest="e5b5cba616eab39d73e3540f5950d2050b3f43ecd7fe386c4b203bf18b8b5fb3",
               radius="33/10", cap="3037969/7000000", rho_lo="7/5", rho_hi="3/2"),
}
PREDECESSOR_SHA256 = "f3c6a95c5fa814cc024872c0b4212d7d5272d8b7696306dfc0f5a3b74d12167f"
INITIAL_CONTROLS = ["boolean n", "wrong index", "wrong rho", "wrong radius", "missing stage",
                    "missing panel", "wrong predecessor", "false guard", "wrong q", "seeded raw",
                    "wrong schedule", "extra success"]
RESOURCE_CONTROLS = ["wrong n", "boolean n", "wrong barrier", "wrong rho floor", "wrong support",
                     "wrong owncap", "missing panel", "reordered panels", "wrong initial proof",
                     "wrong initial receipt", "missing source", "extra success"]
PREMISES = [
    "Imported stronger24 auxiliary receipt: C24 < CE + 1/80 (not freshly acquired here)",
    "Retained attainment, same-witness, contact and Fourier analytic framework",
    "Published external estimates used by the unchanged native sources",
]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def profile(branch):
    spec = BRANCHES[branch]
    return dict(n=25, nmax=25, radius=spec["radius"], radius_minus=spec["radius"],
                radius_plus=spec["radius"], cap=spec["cap"], barrier="0", grid=[24, 24, 8, 4],
                invariants=dict(rho_lo=spec["rho_lo"], rho=spec["rho_hi"]))


def names(branch):
    need(branch in BRANCHES, "Reviewed n25 parent branch: b3 or b4")
    upper = branch.upper()
    return dict(initial_dir="initial25_" + branch + "_exact_v1", resource_dir="resource25_" + branch + "_v1",
                initial_script="initial25_" + branch + ".py", resource_script="resources_" + branch + ".py",
                initial_proof="INITIAL25_" + upper + "_PROOF.json",
                initial_receipt="INITIAL25_" + upper + "_ACCEPTED.json",
                resource_proof="RESOURCE_" + upper + "_GLOBAL_PROOF.json",
                resource_receipt="RESOURCE_" + upper + "_GLOBAL_ACCEPTED.json")


def _flat_manifest(raw, branch, kind):
    need(hashlib.sha256(raw).hexdigest() == BRANCHES[branch][kind + "_manifest"],
         "Externally pinned complete " + kind + " source manifest")
    manifest = json.loads(raw.decode("utf-8"), object_pairs_hook=common.unique)
    need(type(manifest) is dict and len(manifest) == (30 if kind == "initial" else 32),
         "Complete native source closure cardinality")
    for name, pin in manifest.items():
        need(type(name) is str and name and Path(name).name == name and name not in (".", "..")
             and "/" not in name and "\\" not in name and ":" not in name,
             "Flat portable source name")
        need(type(pin) is str and len(pin) == 64 and all(c in "0123456789abcdef" for c in pin),
             "Literal source SHA256")
    return manifest


def verify_sources(root, branch, *, allow_outputs=True):
    root = Path(root).resolve()
    need(root.is_dir() and {p.name for p in root.iterdir()} ==
         {names(branch)["initial_dir"], names(branch)["resource_dir"]},
         "Exactly the two complete native source capsules")
    result = {}
    for kind in ("initial", "resource"):
        directory = root / names(branch)[kind + "_dir"]
        need(directory.is_dir() and not directory.is_symlink(), "Ordinary native source capsule")
        manifest_path = directory / "FROZEN_SOURCES.json"
        need(manifest_path.is_file() and not manifest_path.is_symlink() and manifest_path.stat().st_size < MIB,
             "Bounded regular frozen manifest")
        manifest = _flat_manifest(manifest_path.read_bytes(), branch, kind)
        permitted = set(manifest) | {"FROZEN_SOURCES.json"}
        if allow_outputs:
            permitted |= {names(branch)[kind + "_proof"], names(branch)[kind + "_receipt"]}
            permitted |= ({"PROGRESS_construct.json", "PROGRESS_accept.json", "SCALAR_SUPPORT_PREFLIGHT.json"}
                          if kind == "initial" else {"PROGRESS.json"})
        need(all(p.is_file() and not p.is_symlink() and p.name in permitted for p in directory.iterdir()),
             "No unbound files, import helpers or directories in the sealed native capsule")
        for name, pin in manifest.items():
            path = directory / name
            need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 16*MIB
                 and common.digest(path) == pin, "Unchanged complete native source: " + name)
        result[kind] = manifest
    return result


def prepare(branch, archives, output, *, download=False):
    """Copy only externally pinned sources; never copy parent proof/acceptance outputs."""
    names(branch)
    output = Path(output).resolve()
    need(not output.exists(), "Fresh parent task directory; prior evidence is preserved")
    output.mkdir(parents=True)
    common.event(output, "n25_parent_preparation_started", branch=branch, arithmetic_accepted=False)
    archive = common.obtain_asset(archives, "old", download, progress=output)
    source = output / "source"
    source.mkdir()
    copied = 0
    with zipfile.ZipFile(archive) as zipped:
        inventory = zipped.namelist()
        for kind in ("initial", "resource"):
            directory = names(branch)[kind + "_dir"]
            prefix = "cutoff25_20261011/new_root/" + directory + "/"
            manifest_name = prefix + "FROZEN_SOURCES.json"
            need(inventory.count(manifest_name) == 1 and zipped.getinfo(manifest_name).file_size < MIB,
                 "One bounded source manifest in the pinned archive")
            raw = zipped.read(manifest_name)
            manifest = _flat_manifest(raw, branch, kind)
            destination = source / directory
            destination.mkdir()
            (destination / "FROZEN_SOURCES.json").write_bytes(raw)
            for name, pin in manifest.items():
                member = prefix + name
                need(inventory.count(member) == 1 and zipped.getinfo(member).file_size <= 16*MIB,
                     "One bounded exact source archive member: " + name)
                payload = zipped.read(member)
                need(hashlib.sha256(payload).hexdigest() == pin, "Pinned archive source bytes: " + name)
                (destination / name).write_bytes(payload)
                copied += 1
    verify_sources(source, branch, allow_outputs=False)
    for kind in ("initial", "resource"):
        directory = source / names(branch)[kind + "_dir"]
        manifest = common.read(directory / "FROZEN_SOURCES.json")
        need({p.name for p in directory.iterdir()} == set(manifest) | {"FROZEN_SOURCES.json"},
             "Only frozen source inputs, without archived native outputs")
    common.write(output / "TASK.json", dict(schema="FRESH_N25_PARENT_TASK_V1", branch=branch,
                 source_asset=common.ASSETS["old"], driver_sha256=common.digest(__file__),
                 manifests={kind: BRANCHES[branch][kind + "_manifest"] for kind in ("initial", "resource")},
                 imported_stronger24_sha256=PREDECESSOR_SHA256, conditional_premises=PREMISES,
                 stronger24_acquisition_verified=False, count_interface_join_verified=False,
                 all_index_conclusion_verified=False))
    common.event(output, "n25_parent_sources_prepared", branch=branch, pinned_source_files=copied,
                 historical_parent_proofs_imported=0, historical_parent_acceptances_imported=0)
    return output


def _task(task):
    task = Path(task).resolve()
    need(task.is_dir() and not task.is_symlink(), "Ordinary parent task directory")
    packet = common.read(task / "TASK.json", MIB)
    branch = packet.get("branch")
    names(branch)
    need(packet.get("schema") == "FRESH_N25_PARENT_TASK_V1"
         and packet.get("driver_sha256") == common.digest(__file__)
         and packet.get("source_asset") == common.ASSETS["old"]
         and packet.get("manifests") == {k: BRANCHES[branch][k + "_manifest"] for k in ("initial", "resource")},
         "Same pinned parent source epoch and driver")
    verify_sources(task / "source", branch, allow_outputs=False)
    return task, branch


def _same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    return a == b


def validate_native(root, branch, kind, *, accepted):
    """Check observed native bindings and full inventories after successful replay."""
    manifests = verify_sources(root, branch)
    paths = names(branch)
    directory = Path(root) / paths[kind + "_dir"]
    proof_path = directory / paths[kind + "_proof"]
    proof = common.read(proof_path, 32*MIB)
    need(_same(proof.get("profile"), profile(branch)), "Literal typed whole-parent profile")
    expected_sources = dict(manifests[kind])
    if kind == "resource":
        expected_sources["FROZEN_SOURCES.json"] = BRANCHES[branch]["resource_manifest"]
    need(proof.get("source_sha256") == expected_sources, "Complete output-to-source binding")
    if kind == "initial":
        need(proof.get("schema") == "SHARP25_" + branch.upper() + "_UNSEEDED_INITIAL_V1"
             and type(proof.get("maximum_covers")) is int and proof["maximum_covers"] == 12
             and proof.get("predecessor_sha256") == PREDECESSOR_SHA256,
             "Unseeded thirteen-cover INITIAL schema and imported auxiliary premise")
        stages = proof.get("stages")
        need(type(stages) is list and len(stages) == 12 and stages[0].get("input_raw") is None
             and stages[0].get("input_D") is None, "Twelve unseeded feedback covers")
        for cover in [stage["cover"] for stage in stages] + [proof["export"]]:
            need(type(cover.get("total")) is int and cover["total"] == 18432
                 and type(cover.get("active")) is int and type(cover.get("excluded")) is int
                 and cover["active"] + cover["excluded"] == 18432,
                 "All 239616 signed rectangles are accounted for")
        panels = proof["export"]["panels"]
        need(type(panels) is list and len(panels) == 100, "All 100 INITIAL probability panels")
        need(all(row.get("pl") == str(Fraction(i, 100)) and row.get("pu") == str(Fraction(i+1, 100))
                 and row.get("rho_lo") == BRANCHES[branch]["rho_lo"]
                 and row.get("rho_branch_upper") == BRANCHES[branch]["rho_hi"]
                 for i, row in enumerate(panels)), "Ordered closed whole-parent p cover and rho branch")
        need(proof["support"]["q"] == "5/16", "Actual n25 same-witness contact allowance")
    else:
        initial = Path(root) / paths["initial_dir"]
        need(proof.get("schema") == "EXACT_SHARP25_" + branch.upper() + "_GLOBAL_RESOURCES_V1"
             and proof.get("parent_proof_sha256") == common.digest(initial / paths["initial_proof"])
             and proof.get("parent_acceptance_sha256") == common.digest(initial / paths["initial_receipt"])
             and proof.get("parent_manifest_sha256") == BRANCHES[branch]["initial_manifest"]
             and proof.get("parent_source_sha256") == manifests["initial"],
             "Resources bind this freshly acquired whole-parent INITIAL")
        rows = proof.get("rows")
        need(type(rows) is list and len(rows) == 100
             and all(type(row.get("index")) is int and row["index"] == i
                     and type(row["result"].get("excluded")) is bool for i, row in enumerate(rows)),
             "All 100 typed ordered terminal resource rows")
    if not accepted:
        return dict(proof_sha256=common.digest(proof_path), probability_panels=100,
                    constructed_only=True, native_arithmetic_accepted=False)
    receipt_path = directory / paths[kind + "_receipt"]
    receipt = common.read(receipt_path, MIB)
    expected_status = ("PASS_FRESH_EXACT_INITIAL25_" + branch.upper() if kind == "initial" else
                       "PASS_FRESH_EXACT_SHARP25_" + branch.upper() + "_GLOBAL_RESOURCES")
    need(receipt.get("status") == expected_status and receipt.get("proof_sha256") == common.digest(proof_path)
         and receipt.get("checker_sha256") == common.digest(directory / paths[kind + "_script"])
         and receipt.get("source_sha256") == expected_sources
         and _same(receipt.get("profile"), profile(branch))
         and type(receipt.get("probability_panels")) is int and receipt["probability_panels"] == 100
         and receipt.get("negative_controls") == (INITIAL_CONTROLS if kind == "initial" else RESOURCE_CONTROLS),
         "Fresh native receipt, full source binding, 100 panels and all twelve named negative controls")
    details = dict(proof_sha256=common.digest(proof_path), receipt_sha256=common.digest(receipt_path),
                   probability_panels=100, negative_controls=12, native_arithmetic_accepted=True)
    if kind == "initial":
        need(type(receipt.get("signed_rectangles")) is int and receipt["signed_rectangles"] == 239616
             and receipt.get("final_invariants") == proof.get("final_invariants"), "Whole thirteen-cover receipt")
        details["signed_rectangles"] = 239616
    else:
        survivors = [row["index"] for row in rows if row["result"]["excluded"] is False]
        exclusions = [row["index"] for row in rows if row["result"]["excluded"] is True]
        support_objects = sum(len(step["support"]) for row in rows for step in row["result"].get("history", []))
        need(_same(receipt.get("surviving_panels"), survivors) and _same(receipt.get("excluded_panels"), exclusions)
             and type(receipt.get("signed_support_objects")) is int
             and receipt["signed_support_objects"] == support_objects
             and receipt.get("parent_proof_sha256") == proof["parent_proof_sha256"]
             and receipt.get("parent_acceptance_sha256") == proof["parent_acceptance_sha256"],
             "Complete resource census and this INITIAL proof/receipt pair")
        details.update(surviving_panels=survivors, excluded_panels=exclusions, signed_support_objects=support_objects)
    return details


def _marker(branch, stage):
    kind, action = stage.split("-")
    upper = branch.upper()
    if action == "accept":
        return "PASS_FRESH_EXACT_INITIAL25_" + upper if kind == "initial" else "PASS_FRESH_EXACT_SHARP25_" + upper + "_GLOBAL_RESOURCES"
    return "EXACT25_" + upper + "_CONSTRUCTED" if kind == "initial" else upper + "_GLOBAL_RESOURCE_CONSTRUCTED"


def _check_execution(report, root, branch, stage):
    from .small_indices import trusted_guard
    kind, action = stage.split("-")
    script = Path(root) / names(branch)[kind + "_dir"] / names(branch)[kind + "_script"]
    observed = report["observed"]
    common.require_completed(observed)
    need(type(observed.get("returncode")) is int and observed["returncode"] == 0,
         "Exact integer successful native return code")
    need(report["supervisor_sha256"] == common.digest(Path(__file__).with_name("linux_supervisor.py")),
         "Same reviewed native supervisor source before and after execution")
    need(trusted_guard(observed, script_sha=common.digest(script), supervisor_sha=report["supervisor_sha256"],
                       memory_bytes=512*MIB, cpu_seconds=report["cpu_seconds"]),
         "Established bounded single-process native capability; no discovery fallback")
    for key in ("stdout", "stderr"):
        path = Path(observed[key + "_path"])
        need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 16*MIB
             and common.digest(path) == report[key + "_sha256"] == observed.get(key + "_sha256"),
             "Stable actual log bound to the supervisor capture")
    need(Path(observed["stderr_path"]).stat().st_size == 0, "Successful native action has empty stderr")
    lines = Path(observed["stdout_path"]).read_text("utf-8").splitlines()
    marker = _marker(branch, stage)
    need(sum(line == marker or line.startswith(marker + " ") for line in lines) == 1,
         "One actual complete native terminal marker")
    return validate_native(root, branch, kind, accepted=action == "accept")


def _completed(task, branch, stage, previous):
    path = task / (stage + "-COMPLETED.json")
    if not path.exists():
        return None
    report = common.read(path, 2*MIB)
    need(report.get("schema") == "FRESH_N25_PARENT_STAGE_V1" and report.get("stage") == stage
         and report.get("branch") == branch and report.get("status") == "completed"
         and report.get("driver_sha256") == common.digest(__file__)
         and report.get("dependencies") == {s: common.digest(task / (s + "-COMPLETED.json")) for s in previous},
         "Same observed stage and complete preceding guarded execution chain")
    root = task / report["capsule_relative"]
    need(root.resolve().is_relative_to(task) and not root.is_symlink(), "Contained private native capsule")
    for name, pin in report["artifact_sha256"].items():
        path = root / name
        need(path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
             and common.digest(path) == pin, "Unchanged freshly observed parent artifact")
    need(_check_execution(report, root, branch, stage) == report["native_result"],
         "Previously observed guarded stage still has its exact native bindings")
    return report


def run(task, *, stage="all", wall_seconds=7260, cpu_seconds=7200):
    """Run real native actions. Reuse only completed, fully revalidated local stages."""
    from .small_indices import FollowOutput, Progress
    need(stage == "all" or stage in STAGES, "One native action or the complete four-action chain")
    need(type(wall_seconds) is int and 1 <= wall_seconds <= 7260
         and type(cpu_seconds) is int and 2 <= cpu_seconds <= 7200,
         "Per-action ceiling: 7260 wall seconds and 7200 total native CPU seconds")
    task, branch = _task(task)
    reports = {}
    wanted = STAGES if stage == "all" else STAGES[:STAGES.index(stage)+1]
    for current in wanted:
        done = _completed(task, branch, current, reports)
        if done is not None:
            reports[current] = done
            common.event(task, "n25_parent_completed_stage_revalidated", branch=branch, stage_name=current)
            continue
        need(stage == "all" or current == stage, "Complete preceding native stage first: " + current)
        kind, action = current.split("-")
        epoch = task / "attempts" / (current + "-" + uuid.uuid4().hex[:12])
        root = epoch / "new_root"
        shutil.copytree(task / "source", root)
        paths = names(branch)
        inputs = []
        if current != "initial-construct":
            inputs.append(("initial-construct", "initial", "proof"))
        if kind == "resource":
            inputs.append(("initial-accept", "initial", "receipt"))
        if current == "resource-accept":
            inputs.append(("resource-construct", "resource", "proof"))
        for parent_stage, parent_kind, artifact in inputs:
            relative = Path(paths[parent_kind + "_dir"]) / paths[parent_kind + "_" + artifact]
            previous_root = task / reports[parent_stage]["capsule_relative"]
            shutil.copyfile(previous_root / relative, root / relative)
            need(common.digest(root / relative) == common.digest(previous_root / relative), "Stable fresh predecessor copy")
        directory = root / paths[kind + "_dir"]
        output = directory / paths[kind + ("_proof" if action == "construct" else "_receipt")]
        need(not output.exists(), "Fresh native action output, without a historical acceptance")
        verify_sources(root, branch)
        script = directory / paths[kind + "_script"]
        command = [sys.executable, "-B", "-S", str(script), action]
        supervisor_sha = common.digest(Path(__file__).with_name("linux_supervisor.py"))
        common.event(task, "n25_parent_native_started", branch=branch, stage_name=current,
                     wall_seconds=wall_seconds, cpu_seconds=cpu_seconds, arithmetic_accepted=False)
        progress = Progress(epoch / "FOLLOW_PROGRESS.jsonl")
        try:
            with FollowOutput(current, epoch / "execution" / "stdout.txt", progress, 20):
                observed = common.supervise(command, cwd=root, output_dir=epoch / "execution",
                           wall_seconds=wall_seconds, cpu_seconds=cpu_seconds, memory_bytes=512*MIB,
                           mode="trusted_native", disk_bytes=256*MIB, log_bytes=16*MIB)
        finally:
            progress.close()
        report = dict(schema="FRESH_N25_PARENT_STAGE_V1", branch=branch, stage=current, status="partial",
                      observed=observed, command=command, cpu_seconds=cpu_seconds, wall_seconds=wall_seconds,
                      capsule_relative=root.relative_to(task).as_posix(), driver_sha256=common.digest(__file__),
                      supervisor_sha256=supervisor_sha,
                      dependencies={s: common.digest(task / (s + "-COMPLETED.json")) for s in reports},
                      conditional_premises=PREMISES, stronger24_acquisition_verified=False,
                      count_interface_join_verified=False, all_index_conclusion_verified=False,
                      native_arithmetic_accepted=False)
        for key in ("stdout", "stderr"):
            path = Path(observed[key + "_path"]) if observed.get(key + "_path") else None
            report[key + "_sha256"] = common.digest(path) if path is not None and path.is_file() else None
        try:
            report["native_result"] = _check_execution(report, root, branch, current)
            verify_sources(task / "source", branch, allow_outputs=False)
            report.update(status="completed", native_arithmetic_accepted=action == "accept")
            artifacts = [(kind, "proof")] + ([(kind, "receipt")] if action == "accept" else [])
            artifacts += [(parent_kind, artifact) for _, parent_kind, artifact in inputs]
            report["artifact_sha256"] = {
                (Path(paths[k + "_dir"]) / paths[k + "_" + a]).as_posix():
                    common.digest(root / paths[k + "_dir"] / paths[k + "_" + a]) for k, a in artifacts}
        except Exception as error:
            report["error"] = type(error).__name__ + ": " + str(error)
        common.write(epoch / "RESULT.json", report)
        common.event(task, "n25_parent_native_finished", branch=branch, stage_name=current,
                     status=report["status"], native_arithmetic_accepted=report["native_arithmetic_accepted"],
                     error=report.get("error"))
        if report["status"] != "completed":
            return dict(status="PARTIAL_NOT_ACCEPTED", failed_stage=current, stages=reports, attempt=report,
                        native_parent_chain_accepted=False, conditional_premises=PREMISES,
                        stronger24_acquisition_verified=False, count_interface_join_verified=False,
                        all_index_conclusion_verified=False)
        common.write(task / (current + "-COMPLETED.json"), report)
        reports[current] = report
    complete = all(s in reports for s in STAGES)
    return dict(status="CONDITIONAL_FRESH_PARENT_CHAIN_ACCEPTED" if complete else "REQUESTED_NATIVE_STAGE_COMPLETED",
                stages=reports, native_parent_chain_accepted=complete, conditional_premises=PREMISES,
                stronger24_acquisition_verified=False, count_interface_join_verified=False,
                all_index_conclusion_verified=False)


def run_colab(branch, *, durable_root, work_root="/content/berry-esseen-runs",
              archives="/content/berry-esseen-archives", wall_seconds=7260, cpu_seconds=7200,
              backup_interval=60):
    """Four bounded real actions, visible native output, live backups and final ZIP."""
    from . import colab_batch
    from .environment import snapshot
    names(branch)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    root = Path(work_root) / ("n25-parents-" + branch) / stamp
    root.mkdir(parents=True)
    durable = Path(durable_root) / ("n25-parents-" + branch) / stamp
    status = dict(scope="CONDITIONAL_N25_INITIAL_AND_RESOURCE_ACQUISITIONS", branch=branch,
                  state="started", native_parent_chain_accepted=False, conditional_premises=PREMISES,
                  stronger24_acquisition_verified=False, count_interface_join_verified=False,
                  all_index_conclusion_verified=False, per_stage_wall_seconds=wall_seconds,
                  per_stage_cpu_seconds=cpu_seconds, maximum_native_actions=4)
    colab_batch.atomic_json(root / "ENVIRONMENT.json", snapshot())
    colab_batch.atomic_json(root / "SESSION_RESULT.json", status)
    monitor = colab_batch.Backups(root, durable, interval=backup_interval)
    monitor.start()
    try:
        colab_batch.event(root, "n25_parent_job_started", branch=branch, signed_rectangles=239616,
                          probability_panels=100, initial_negative_controls=12, resource_negative_controls=12,
                          native_actions=4, stronger24_acquisition_verified=False, count_interface_join_verified=False)
        task = prepare(branch, archives, root / "task", download=True)
        result = run(task, wall_seconds=wall_seconds, cpu_seconds=cpu_seconds)
        status.update(state=result["status"], native_parent_chain_accepted=result["native_parent_chain_accepted"], result=result)
    except BaseException as error:
        status.update(state="PARTIAL_ERROR_NOT_ACCEPTED", error=type(error).__name__ + ": " + str(error))
        (root / "ERROR.txt").write_text(traceback.format_exc(), encoding="utf-8")
        colab_batch.event(root, "n25_parent_job_incomplete", error=status["error"])
    finally:
        colab_batch.atomic_json(root / "SESSION_RESULT.json", status)
        try:
            monitor.close()
        except Exception as error:
            colab_batch.event(root, "final_backup_failed", error=str(error))
        output = colab_batch.bundle(root, durable)
        colab_batch.event(root, "n25_parent_results_bundle_saved", path=str(output), state=status["state"],
                          all_index_conclusion_verified=False)
    print("\nRESULT:", status["state"], "\nZIP:", output, flush=True)
    return dict(status=status, bundle=str(output), work=str(root))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare", help="Copy the complete pinned sources without archived parent outputs")
    prepare_parser.add_argument("branch", choices=BRANCHES)
    prepare_parser.add_argument("--archives", type=Path, required=True)
    prepare_parser.add_argument("--output", type=Path, required=True)
    prepare_parser.add_argument("--download", action="store_true")
    run_parser = commands.add_parser("run", help="Run actual bounded construction/replay; a timeout is PARTIAL")
    run_parser.add_argument("task", type=Path)
    run_parser.add_argument("--stage", choices=("all",) + STAGES, default="all")
    run_parser.add_argument("--wall-seconds", type=int, default=7260)
    run_parser.add_argument("--cpu-seconds", type=int, default=7200)
    args = parser.parse_args()
    if args.command == "prepare":
        print(prepare(args.branch, args.archives, args.output, download=args.download))
    else:
        result = run(args.task, stage=args.stage, wall_seconds=args.wall_seconds, cpu_seconds=args.cpu_seconds)
        print(json.dumps(result), flush=True)
        return 0 if result["status"] != "PARTIAL_NOT_ACCEPTED" else 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
