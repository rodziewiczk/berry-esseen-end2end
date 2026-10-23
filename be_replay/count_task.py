"""Run frozen n25 count sources on Linux; search and native acceptance are separate.

An accepted count is conditional on its original parent acquisitions.  This
module never promotes a regional count to a C25 or all-index theorem.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time
import urllib.request
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor/count_75a9470"
COMMIT = "75a94708872e2bc053f42a279559b23ed91e4402"
REPOSITORY = "rodziewiczk/berry-esseen-045-certificate"
MIB = 1024 ** 2
VENDOR_PINS = {
    'count_discovery.py': '6bb3e8c68570653d8e2f91670f1e18fc8287ea2f6d314d59535c1533b4b6af32',
    'prefix2_original/MANIFEST.json': '67d805875f1f3d4d0ae7e478882c1f9bc228fd81e1454435bb559b18a2784b48',
    'prefix2_original/common_bound_memo_discovery_v12.py': '2e69b968d5fa781db6c7728c1863a82b874dbc867b5e4852dcaa9187a09f128c',
    'prefix2_original/discovery_hoist_alpha_stoploss2.py': 'cf198f062b8ac0fc98431a6e9954ef18c38f49a1a8e752af3e1504f74a71ad69',
    'prefix2_original/feasible_a0.py': 'bea087de1f6d18e4ddc034270b351ee81d43e76ab36a5827dc599dec16aeefbb',
    'prefix2_original/geometry_memo_discovery_v12.py': '380e791e558713f33f668a0d7f999923f5d7b28959ac5b581bee99d3216d4170',
    'prefix2_original/integer_exponential_discovery_v1.py': '174b96fd8814402faa6ae881dfdbb3ebbc23118c7027c3f7b1148abb74f72515',
    'prefix2_original/parent_prefix_bypass.py': 'b8f71b052b6580a4863d8782f7ce1ec8186f73e0dbe36b6b5e817ebec8837e52',
    'prefix2_original/physical_prefix_lookahead.py': '50a4f6161eb589ecc6238804afbbd184e4bb458b9fe159f01a2ea94db07a7fa6',
    'prefix2_original/split_policy.py': '013086ffff8d265b54a79f14a23d0aedede7e0361ed450ac0eddfcd406081fbd',
    'prefix2_runtime.py': '877e2c465fad271d6452b722ff7307e72704c504d0f5898fc906729d1198029c',
    'prefix2_strategy.py': '2d7e6748b585bf65fc84ea63f392af6b268a061668dc41c001c7415333a60d93',
    'prepare_b3_v14_epoch_2026_10_22.py': '4116a054c2f725794d82cc4bd7b954023c9b8525d8f943c6cea2a8096aceb647',
    'prepare_missing_count.py': 'b22f807a41982f017af14e88451d82fcda129ab13a2b09210ab543420f4aa410',
}
PORTABLE_V14_PREPARER = Path(__file__).with_name("prepare_v14_portable.py")
PORTABLE_V14_PREPARER_SHA256 = "b4896cae54058bb63f3c68a295131a83ceace34e71d180c0b228bd4a28ce44f6"
TARGETS = {
    "b4-q0": ("original-v12", 29, "4d91657ddbab41e3324c00f9f28a9223526c0c1dc79bad5c5e77176240c231f7"),
    "b4-q1": ("original-v12", 29, "a3cbdb1852bc51054ecc8cd3c71bd1c7121b6b201385e481b73195ad729189c4"),
    "b4-q2": ("original-v12", 29, "2517c1b8c79949bad93eecdcaa43e389344411fd4c71d5d516dde1e40b732e2a"),
    "b4-q3": ("original-v12", 29, "c8555b500c3e7d1ca1240b5f229f7fff5ed307571012209e022431ecd195b7ac"),
    "b3-p33": ("original-v12", 33, "e55bb3eeac06923f897263a65f2cde9fe77006313dd86f47bbba3f6047f30f08"),
    "b3-p31-v14-new": ("new-conditional-v14", 31, "bc699a2d539b4aafc193049c8074b02e0b77a38fb01b594c1ba3e2fde6b7b3ff"),
    "b3-p32-v14-new": ("new-conditional-v14", 32, "cfe934b1385f9a26f36b6bf94cda9e5caeb6593700a54eeac7e7b1638df61627"),
}
# The published archive predates the portable V14 source epoch. Its complete
# manifest remains pinned independently of the current executable designs.
PUBLISHED_HINT_DESIGNS = {
    "b4-q0": "4d91657ddbab41e3324c00f9f28a9223526c0c1dc79bad5c5e77176240c231f7",
    "b4-q1": "a3cbdb1852bc51054ecc8cd3c71bd1c7121b6b201385e481b73195ad729189c4",
    "b4-q2": "2517c1b8c79949bad93eecdcaa43e389344411fd4c71d5d516dde1e40b732e2a",
    "b4-q3": "c8555b500c3e7d1ca1240b5f229f7fff5ed307571012209e022431ecd195b7ac",
    "b3-p33": "e55bb3eeac06923f897263a65f2cde9fe77006313dd86f47bbba3f6047f30f08",
    "b3-p31-v14-new": "6ca73188c5a6969c1f0ec69f41cb0fac660003cf0515fdcadeeda83afcf654f0",
    "b3-p32-v14-new": "230a6bb37696c1e79d62847d89090d4187d78d41aa6c98ccbe91c54e1f8f950b",
}
ASSETS = {
    "old": dict(name="cutoff25_20261011.zip", tag="cutoff20-sources-2026-10-17",
                bytes=514958998, sha256="17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb"),
    "base13": dict(name="cutoff25_20261013.zip", tag="cutoff25-base-sources-2026-10-22",
                   bytes=529557492, sha256="a97f3e6e50e428df0893304bcd2f746851c9fccef2079b1ec66be9ab909d7f2c"),
    "hints": dict(name="untrusted_count_search_hints_2026-10-22.zip", tag="count-search-hints-2026-10-22",
                  bytes=161372, sha256="9e9e45befa5590d2166f4aa5c55edd6d2595b1eb6c4ac6adcd1fd24855aead2a"),
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while block := stream.read(MIB):
            value.update(block)
    return value.hexdigest()


def read(path, limit=128 * MIB):
    path = Path(path)
    need(path.is_file() and not path.is_symlink() and path.stat().st_size <= limit,
         "Bounded regular input required: " + str(path))
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def write(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def event(directory, stage, **values):
    """Durable observed progress; no pending work is labelled an acceptance."""
    directory = Path(directory)
    record = dict(event="count_task_progress", stage=stage,
                  utc=datetime.now(timezone.utc).isoformat(), **values)
    record["all_index_conclusion_verified"] = False
    with (directory / "progress.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, separators=(",", ":")) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps(record), flush=True)


def scope(target):
    need(target in TARGETS, "One of the seven reviewed targets")
    return ("NEW_CONDITIONAL_V14_NOT_HISTORICAL_IDENTITY" if TARGETS[target][0] == "new-conditional-v14"
            else "ORIGINAL_V12_CONDITIONAL_COUNT_ONLY")


def verify_vendor(directory=None):
    directory = Path(directory) if directory is not None else VENDOR
    for name, pin in VENDOR_PINS.items():
        path = directory / name
        need(path.is_file() and not path.is_symlink() and digest(path) == pin,
             "Frozen public commit source mismatch: " + name)
    return dict(commit=COMMIT, files_sha256=dict(VENDOR_PINS))


def verify_asset(path, asset):
    path = Path(path)
    need(path.is_file() and not path.is_symlink() and path.stat().st_size == asset["bytes"]
         and digest(path) == asset["sha256"], "Pinned source asset size/SHA mismatch: " + asset["name"])
    return path


def obtain_asset(directory, key, download=False, progress=None):
    asset = ASSETS[key]
    directory = Path(directory).resolve()
    need(not directory.is_symlink(), "No symlink source cache")
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / asset["name"]
    if path.exists():
        if progress is not None:
            event(progress, "source_verification_started", asset=asset["name"], bytes=asset["bytes"])
        result = verify_asset(path, asset)
        if progress is not None:
            event(progress, "source_verified", asset=asset["name"], bytes=asset["bytes"])
        return result
    need(download, "Missing public source asset; pass --download: " + str(path))
    url = "https://github.com/" + REPOSITORY + "/releases/download/" + asset["tag"] + "/" + asset["name"]
    partial = directory / (asset["name"] + ".download-" + uuid.uuid4().hex)
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "berry-esseen-end2end/1"})
        total = 0
        last_progress = time.monotonic() - 5
        last_bytes = 0
        with urllib.request.urlopen(request, timeout=60) as source, partial.open("xb") as output:
            while block := source.read(MIB):
                total += len(block)
                need(total <= asset["bytes"], "Source download exceeds the pinned exact size")
                output.write(block)
                if progress is not None and (time.monotonic() - last_progress >= 5 or total - last_bytes >= 16 * MIB):
                    event(progress, "source_download", asset=asset["name"], bytes=total,
                          expected_bytes=asset["bytes"])
                    last_progress = time.monotonic()
                    last_bytes = total
        verify_asset(partial, asset)
        need(not path.exists(), "Do not overwrite a concurrently populated source cache")
        partial.rename(path)
        if progress is not None:
            event(progress, "source_verified", asset=asset["name"], bytes=total)
    except BaseException:
        # Keep bounded partial downloads as diagnostics; never use them as inputs.
        raise
    return path


def preparation_command(target, archives, capsule):
    kind, index, _ = TARGETS[target]
    archives, capsule = Path(archives), Path(capsule)
    if kind == "original-v12":
        return [sys.executable, "-B", "-S", str(VENDOR / "prepare_missing_count.py"),
                "--archive", str(archives / ASSETS["old"]["name"]), "--target", target, "--output", str(capsule)]
    need(PORTABLE_V14_PREPARER.is_file() and not PORTABLE_V14_PREPARER.is_symlink()
         and digest(PORTABLE_V14_PREPARER) == PORTABLE_V14_PREPARER_SHA256,
         "Exact reviewed portable V14 producer")
    return [sys.executable, "-B", "-S", str(PORTABLE_V14_PREPARER),
            "--old-archive", str(archives / ASSETS["old"]["name"]),
            "--base13-archive", str(archives / ASSETS["base13"]["name"]),
            "--index", str(index), "--output", str(capsule)]


def verify_capsule(target, capsule):
    kind, index, expected = TARGETS[target]
    capsule = Path(capsule).resolve()
    need(capsule.is_dir() and not capsule.is_symlink(), "Regular prepared capsule")
    design_path = capsule / "FROZEN_DESIGN.json"
    need(digest(design_path) == expected, "Externally pinned target-specific source design")
    design = read(design_path, MIB)
    files = design.get("files")
    need(type(files) is dict and 1 <= len(files) <= 256, "Complete bounded flat source design")
    for name, pin in files.items():
        need(type(name) is str and Path(name).name == name and "/" not in name and "\\" not in name,
             "Flat frozen source name")
        path = capsule / name
        need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 16 * MIB and digest(path) == pin,
             "Exact original/explicitly derived native source: " + name)
    need({"count_protocol.py", "contract.json", "KERNEL_COPY_MANIFEST.json"} <= set(files),
         "Design binds the actual native checker, contract and full kernel")
    if kind == "new-conditional-v14":
        epoch = read(capsule / "B3_V14_SOURCE_EPOCH.json")
        need(epoch["schema"] == "NEW_CONDITIONAL_B3_V14_SOURCE_EPOCH_20261022_V1"
             and type(epoch["n"]) is int and epoch["n"] == 25
             and type(epoch["index"]) is int and epoch["index"] == index
             and epoch["preparer_sha256"] == PORTABLE_V14_PREPARER_SHA256
             and epoch["arithmetic_accepted"] is False and epoch["native_acceptance_run"] is False,
             "Honest new conditional portable V14 source epoch")
        need("ORIGINAL_V12_CONTRACT.json" in files
             and "ORIGINAL_V12_contract.json" not in files,
             "The exact runtime contract filename belongs to the sealed portable source closure")
    return files


def native_header(capsule, target):
    """Read literal identity without importing or evaluating mathematical code."""
    capsule = Path(capsule)
    tree = ast.parse((capsule / "count_protocol.py").read_bytes())
    headers = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "header"]
    need(len(headers) == 1 and len(headers[0].body) == 1 and isinstance(headers[0].body[0], ast.Return),
         "Reviewed simple literal native header")
    call = headers[0].body[0].value
    need(isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == "dict",
         "Reviewed native dict header")
    keywords = {item.arg: item.value for item in call.keywords}
    result = {key: ast.literal_eval(keywords[key]) for key in ("schema", "n", "index")}
    need(type(result["n"]) is int and result["n"] == 25 and type(result["index"]) is int
         and result["index"] == TARGETS[target][1], "Literal original sample size/panel")
    result.update(contract_sha256=digest(capsule / "contract.json"),
                  checker_sha256=digest(capsule / "count_protocol.py"),
                  kernel_sha256=read(capsule / "KERNEL_COPY_MANIFEST.json")["files"])
    return result


def check_checkpoint(packet, target, capsule):
    need(type(packet) is dict and packet.get("schema") == "UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1"
         and packet.get("arithmetic_accepted") is False, "Checkpoint is explicitly untrusted")
    binding = packet["binding"]
    need(binding["design_sha256"] == TARGETS[target][2] and binding["alpha_priority"] == "4",
         "Checkpoint matches the exact native source epoch and strategy")
    header = native_header(capsule, target)
    need(all(binding["native_header"].get(key) == value for key, value in header.items()),
         "Checkpoint full native contract/header/kernel binding")
    roots = packet["roots"]
    need(type(roots) is list and len(roots) == 26 and all(
        type(root) is dict and set(root) == {"k", "tree"} and type(root["k"]) is int
        and root["k"] == k and type(root["tree"]) is dict for k, root in enumerate(roots)),
        "All 26 ordered original roots, including still-pending boxes")


def extract_published_hint(archive, target, capsule, output):
    verify_asset(archive, ASSETS["hints"])
    with zipfile.ZipFile(archive) as zipped:
        names = zipped.namelist()
        expected = {"manifest.json"} | {"checkpoints/" + name + "/CHECKPOINT.json" for name in TARGETS}
        need(len(names) == len(expected) and set(names) == expected, "Only the eight unique pinned hint members")
        for name in names:
            info = zipped.getinfo(name)
            need(not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16)
                 and info.file_size <= 8 * MIB, "Bounded regular hints ZIP member")
        manifest = json.loads(zipped.read("manifest.json"), object_pairs_hook=unique)
        need(manifest["schema"] == "UNTRUSTED_COUNT_SEARCH_HINTS_V1"
             and manifest["arithmetic_accepted"] is False and set(manifest["targets"]) == set(TARGETS),
             "All seven hints, never an acceptance record")
        for name, row in manifest["targets"].items():
            need(row["member"] == "checkpoints/" + name + "/CHECKPOINT.json"
                 and row["design_sha256"] == PUBLISHED_HINT_DESIGNS[name],
                 "Every published hint has its own exact historical source epoch")
        row = manifest["targets"][target]
        need(row["design_sha256"] == TARGETS[target][2],
             "Published hint cannot cross into a different executable source epoch")
        raw = zipped.read(row["member"])
        need(type(row["bytes"]) is int and len(raw) == row["bytes"]
             and hashlib.sha256(raw).hexdigest() == row["sha256"], "Exact selected hint payload")
    check_checkpoint(json.loads(raw, object_pairs_hook=unique), target, capsule)
    with Path(output).open("xb") as stream:
        stream.write(raw)
    return Path(output)


def supervise(argv, **options):
    # Imported lazily: --help and source inventory work without Linux facilities.
    from .linux_supervisor import run
    return run(argv, **options)


def execution_diagnostics(observed):
    """Expose bounded failure evidence without treating any output as acceptance."""
    details = {key: observed.get(key) for key in
               ("status", "reason", "returncode", "stdout_path", "stderr_path")}
    details["stderr_tail"] = ""
    name = observed.get("stderr_path")
    if name:
        path = Path(name)
        try:
            if path.is_file() and not path.is_symlink() and path.stat().st_size <= 16 * MIB:
                with path.open("rb") as stream:
                    stream.seek(max(0, path.stat().st_size - 8192))
                    details["stderr_tail"] = stream.read(8192).decode("utf-8", errors="replace").strip()
        except OSError as error:
            details["stderr_read_error"] = type(error).__name__
    return details


def require_completed(observed):
    if observed.get("status") != "completed" or observed.get("returncode") != 0:
        details = execution_diagnostics(observed)
        print(json.dumps(dict(event="guarded_child_failure", **details,
                              arithmetic_accepted=False, all_index_conclusion_verified=False)), flush=True)
        raise ValueError("Guarded child did not complete successfully; preserved output is not acceptance. "
                         + json.dumps(details, ensure_ascii=True))


def final_packet(observed):
    require_completed(observed)
    path = Path(observed["stdout_path"])
    need(path.is_file() and path.stat().st_size <= 16 * MIB, "Bounded actual child stdout")
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    need(lines, "Actual child must emit its complete terminal result")
    return json.loads(lines[-1], object_pairs_hook=unique)


def implementation():
    supervisor = Path(__file__).with_name("linux_supervisor.py")
    return dict(count_task_sha256=digest(__file__), vendor=verify_vendor(),
                supervisor_sha256=digest(supervisor) if supervisor.exists() else None,
                python=sys.version)


def prepare(target, archives, output, *, download=False):
    scope(target)
    verify_vendor()
    output = Path(output).resolve()
    need(not output.exists(), "Each task gets a new directory; existing evidence is retained")
    output.mkdir(parents=True)
    event(output, "preparation_started", target=target, arithmetic_accepted=False)
    archives = Path(archives).resolve()
    obtain_asset(archives, "old", download, progress=output)
    if TARGETS[target][0] == "new-conditional-v14":
        obtain_asset(archives, "base13", download, progress=output)
    command = preparation_command(target, archives, output / "capsule")
    observed = supervise(command, cwd=output, output_dir=output / "preparation",
                         wall_seconds=1800, cpu_seconds=1800, memory_bytes=512 * MIB,
                         mode="untrusted_search")
    write(output / "PREPARATION_EXECUTION.json", observed)
    packet = final_packet(observed)
    files = verify_capsule(target, output / "capsule")
    verify_vendor()
    report = dict(schema="COUNT_TASK_V1", target=target, scope=scope(target),
                  source_commit=COMMIT, design_sha256=TARGETS[target][2],
                  prepared_source_files=len(files), source_archives={"old": ASSETS["old"]},
                  preparation_result=packet, implementation=implementation(),
                  arithmetic_accepted=False, parent_acquisitions_verified=False,
                  all_index_conclusion_verified=False)
    if TARGETS[target][0] == "new-conditional-v14":
        report["source_archives"]["base13"] = ASSETS["base13"]
    write(output / "TASK.json", report)
    event(output, "preparation_finished", target=target, source_files=len(files), arithmetic_accepted=False)
    return report


def load_task(task):
    task = Path(task).resolve()
    record = read(task / "TASK.json", 4 * MIB)
    need(record["schema"] == "COUNT_TASK_V1" and record["source_commit"] == COMMIT
         and record["target"] in TARGETS and record["design_sha256"] == TARGETS[record["target"]][2],
         "Reviewed public source task identity")
    verify_vendor()
    verify_capsule(record["target"], task / "capsule")
    return task, record["target"]


def copy_resume(source, target, capsule, directory):
    source = Path(source).resolve()
    paths = [source, source.with_suffix(".backup.json")]
    usable = 0
    for index, path in enumerate(paths):
        if not path.exists():
            continue
        need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 128 * MIB,
             "Bounded regular primary/backup candidate")
        try:
            packet = read(path)
        except (ValueError, UnicodeError):
            packet = None
        if packet is not None:
            check_checkpoint(packet, target, capsule)
            usable += 1
        shutil.copyfile(path, directory / ("resume.json" if index == 0 else "resume.backup.json"))
    need(usable > 0, "At least one valid, exactly source-bound primary/backup checkpoint")
    primary = directory / "resume.json"
    if not primary.exists():
        shutil.copyfile(directory / "resume.backup.json", primary)
    return primary


def search(task, seconds=60, wall_seconds=120, *, resume=None, published_hints=False,
           archives=None, download=False):
    need(type(seconds) is int and 1 <= seconds <= 7200 and type(wall_seconds) is int
         and seconds <= wall_seconds <= seconds + 120,
         "Bounded original search slice and at most120s external wall reserve")
    need(not (resume is not None and published_hints), "Choose one untrusted checkpoint source")
    task, target = load_task(task)
    capsule = task / "capsule"
    epoch = task / ("search-" + uuid.uuid4().hex[:12])
    epoch.mkdir()
    event(task, "search_started", target=target, epoch=str(epoch), search_seconds=seconds,
          external_wall_seconds=wall_seconds, arithmetic_accepted=False)
    previous = None
    if published_hints and TARGETS[target][0] == "new-conditional-v14":
        event(task, "historical_hint_skipped", target=target,
              reason="Portable V14 source epoch requires fresh roots or a matching new checkpoint",
              arithmetic_accepted=False)
    elif published_hints:
        need(archives is not None, "Explicit source cache for the fixed published hints ZIP")
        archive = obtain_asset(archives, "hints", download, progress=task)
        previous = extract_published_hint(archive, target, capsule, epoch / "resume.json")
    elif resume is not None:
        previous = copy_resume(resume, target, capsule, epoch)
    command = [sys.executable, "-B", "-S", str(VENDOR / "count_discovery.py"),
               "--capsule", str(capsule), "--design-sha256", TARGETS[target][2],
               "--output", str(epoch / "candidate"), "--seconds", str(seconds),
               "--alpha-priority", "4", "--order", "root-first"]
    if previous is not None:
        command += ["--resume", str(previous)]
    observed = supervise(command, cwd=epoch, output_dir=epoch / "execution",
                         wall_seconds=wall_seconds, cpu_seconds=wall_seconds,
                         memory_bytes=512 * MIB, mode="untrusted_search",
                         checkpoint_paths=[epoch / "candidate/CHECKPOINT.json",
                                           epoch / "candidate/CHECKPOINT.backup.json"])
    verify_capsule(target, capsule)
    verify_vendor()
    packet = None
    if observed.get("status") == "completed" and observed.get("returncode") == 0:
        packet = final_packet(observed)
        need(packet.get("status") in ("SEARCH_CHECKPOINTED_INCOMPLETE", "CANDIDATE_COMPLETE_NOT_ACCEPTED")
             and packet.get("arithmetic_accepted") is False, "Search can never produce native acceptance")
    status = ("COMPLETE_CANDIDATE_NATIVE_ACCEPT_REQUIRED" if packet is not None
              and packet["status"] == "CANDIDATE_COMPLETE_NOT_ACCEPTED" else
              "PARTIAL_CANDIDATE_CHECKPOINT_ONLY")
    report = dict(schema="COUNT_SEARCH_EXECUTION_V1", status=status, target=target, scope=scope(target),
                  epoch=str(epoch), observed=observed, search_result=packet,
                  candidate=str(epoch / "candidate/CANDIDATE_FOREST.json"),
                  checkpoint=str(epoch / "candidate/CHECKPOINT.json"),
                  backup_checkpoint=str(epoch / "candidate/CHECKPOINT.backup.json"),
                  implementation=implementation(), arithmetic_accepted=False,
                  native_acceptance_run=False, parent_acquisitions_verified=False,
                  all_index_conclusion_verified=False)
    write(epoch / "SEARCH_EXECUTION.json", report)
    statistics = {key: packet[key] for key in ("nodes", "leaves", "pending") if packet is not None and key in packet}
    event(task, "search_finished", target=target, epoch=str(epoch),
          status="PARTIAL_CANDIDATE_NOT_ACCEPTED", child_status=observed.get("status"),
          arithmetic_accepted=False, **statistics)
    return report


def forest_census(forest, target, capsule):
    need(type(forest) is dict, "Native candidate dictionary")
    for key, value in native_header(capsule, target).items():
        need(forest.get(key) == value, "Exact native candidate header: " + key)
    roots = forest.get("roots")
    need(type(roots) is list and len(roots) == 26, "Complete 26-root candidate before native acceptance")
    nodes = leaves = 0
    for k, root in enumerate(roots):
        need(type(root) is dict and set(root) == {"k", "tree"} and type(root["k"]) is int
             and root["k"] == k, "All original roots, ordered without duplicates")
        stack = [(root["tree"], 0)]
        while stack:
            node, depth = stack.pop()
            nodes += 1
            need(nodes <= 10000 and depth <= 128 and type(node) is dict, "Original finite native tree limits")
            if node.get("kind") == "leaf":
                need(set(node) == {"kind", "box", "decision", "result"} and node["decision"] is not None,
                     "Complete leaf payload; its arithmetic remains UNTRUSTED")
                leaves += 1
            else:
                need(set(node) == {"kind", "axis", "cut", "left", "right"} and node["kind"] == "split"
                     and type(node["axis"]) is int and 0 <= node["axis"] < 5 and type(node["cut"]) is str,
                     "Complete canonical binary split; no pending root or missing child")
                Fraction(node["cut"])
                stack.extend(((node["left"], depth + 1), (node["right"], depth + 1)))
    need(nodes == 2 * leaves - 26, "Full 26-root binary forest census")
    return dict(nodes=nodes, leaves=leaves, roots=26)


def validate_native(receipt, target, capsule, census):
    kind, index, _ = TARGETS[target]
    expected = ("PASS_FRESH_CONDITIONAL_B3_V14_EPOCH_20261022_COUNT" + str(index)
                if kind == "new-conditional-v14" else "PASS_FRESH_CONDITIONAL_EXACT_COUNT" + str(index))
    need(receipt.get("status") == expected, "Exact original/new-epoch native result identity")
    controls = receipt.get("negative_controls")
    need(type(controls) is list and len(controls) == 24 and all(type(item) is str for item in controls)
         and len(set(controls)) == 24, "All 24 distinct original native corruption controls")
    need(type(receipt.get("fresh_leaf_evaluations")) is int
         and receipt["fresh_leaf_evaluations"] == census["leaves"], "Every leaf freshly evaluated by the native checker")
    statistics = receipt["statistics"]
    need(all(type(statistics[key]) is int and statistics[key] == census[key] for key in ("nodes", "leaves")),
         "Actual native census equals every original candidate root")
    for name, key in (("COUNT" + str(index) + "_FOREST.json", "forest_sha256"),
                      ("contract.json", "contract_sha256"), ("count_protocol.py", "checker_sha256")):
        need(receipt[key] == digest(Path(capsule) / name), "Native receipt binds actual fresh inputs")
    manifest = read(Path(capsule) / "KERNEL_COPY_MANIFEST.json")["files"]
    need(receipt["kernel_sha256"] == manifest
         and all(digest(Path(capsule) / name) == pin for name, pin in manifest.items()),
         "Native receipt binds every unchanged mathematical kernel byte")


def accept(task, candidate, *, wall_seconds=7260, cpu_seconds=7200):
    need(type(cpu_seconds) is int and 1 <= cpu_seconds <= 7200
         and type(wall_seconds) is int and 1 <= wall_seconds <= 7260,
         "Original bounded native CPU policy with an external wall watchdog")
    task, target = load_task(task)
    candidate = Path(candidate).resolve()
    forest = read(candidate)
    census = forest_census(forest, target, task / "capsule")
    epoch = task / ("accept-" + uuid.uuid4().hex[:12])
    capsule = epoch / "capsule"
    capsule.mkdir(parents=True)
    event(task, "native_acceptance_started", target=target, epoch=str(epoch),
          nodes=census["nodes"], leaves=census["leaves"], arithmetic_accepted=False)
    files = verify_capsule(target, task / "capsule")
    for name in list(files) + ["FROZEN_DESIGN.json"]:
        shutil.copyfile(task / "capsule" / name, capsule / name)
    verify_capsule(target, capsule)
    index = TARGETS[target][1]
    forest_path = capsule / ("COUNT" + str(index) + "_FOREST.json")
    need(not forest_path.exists() and not (capsule / ("COUNT" + str(index) + "_ACCEPTED.json")).exists(),
         "No historical acceptance/forest is a fresh input")
    shutil.copyfile(candidate, forest_path)
    # Detect changes between parsing and copying before launching the native checker.
    need(read(forest_path) == forest, "Stable candidate bytes during private copy")
    command = [sys.executable, "-B", "-S", str(capsule / "count_protocol.py"), "accept"]
    observed = supervise(command, cwd=capsule, output_dir=epoch / "execution",
                         wall_seconds=wall_seconds, cpu_seconds=cpu_seconds,
                         memory_bytes=512 * MIB, mode="trusted_native")
    report = dict(schema="COUNT_NATIVE_EXECUTION_V1", target=target, scope=scope(target),
                  epoch=str(epoch), observed=observed, census=census, implementation=implementation(),
                  arithmetic_accepted=False, parent_acquisitions_verified=False,
                  all_index_conclusion_verified=False)
    write(epoch / "NATIVE_OBSERVED.json", report)
    # Resource protection may be unsupported in a given VM. Never rerun native
    # accept through search mode or reinterpret a partial/old receipt as success.
    require_completed(observed)
    guard = observed.get("guard_scope")
    need(type(guard) is dict and guard.get("kind") == "LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1"
         and guard.get("capability_established") is True and guard.get("native_python_execution") is True
         and guard.get("hard_sum_RLIMIT_AS_bytes") == 512 * MIB
         and guard.get("worker_RLIMIT_AS_bytes") == 448 * MIB
         and guard.get("supervisor_RLIMIT_AS_bytes") == 64 * MIB
         and guard.get("hard_sum_RLIMIT_CPU_seconds") == cpu_seconds
         and guard.get("script_sha256") == digest(capsule / "count_protocol.py"),
         "Actual bounded native platform contract required; discovery guards cannot accept arithmetic")
    need(Path(observed["stderr_path"]).stat().st_size == 0, "Successful native checker has empty stderr")
    receipt_path = capsule / ("COUNT" + str(index) + "_ACCEPTED.json")
    receipt = read(receipt_path)
    verify_capsule(target, capsule)
    verify_capsule(target, task / "capsule")
    verify_vendor()
    validate_native(receipt, target, capsule, census)
    report.update(arithmetic_accepted=True, native_receipt=str(receipt_path),
                  native_receipt_sha256=digest(receipt_path), negative_controls=24,
                  conditional_premises=["Correct original whole-parent INITIAL/resource acquisitions",
                                        "Same-witness attainment/contact/Fourier/count framework"])
    if TARGETS[target][0] == "new-conditional-v14":
        report["conditional_premises"].append("Global C24 auxiliary bound and attained positive-closed q25<=5/16")
    write(epoch / "NATIVE_ACCEPTED.json", report)
    event(task, "native_acceptance_finished", target=target, epoch=str(epoch),
          nodes=census["nodes"], leaves=census["leaves"], negative_controls=24,
          arithmetic_accepted=True, parent_acquisitions_verified=False)
    return report


def bundle_task(task, output=None):
    """Transport all task sources, logs and BOTH checkpoint files, even on failure."""
    task = Path(task).resolve()
    need(task.is_dir() and not task.is_symlink(), "Owned task directory for checkpoint export")
    output = (Path(output).resolve() if output is not None else
              task.with_name(task.name + "-checkpoints-" + uuid.uuid4().hex[:12] + ".zip"))
    need(not output.exists() and not output.is_relative_to(task), "New checkpoint ZIP outside the task")
    rows = []
    total = 0
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as zipped:
        for directory, names, files in os.walk(task, followlinks=False):
            for name in names:
                need(not (Path(directory) / name).is_symlink(), "No symlink checkpoint directories")
            for name in sorted(files):
                path = Path(directory) / name
                need(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(task),
                     "Only regular owned checkpoint/source/log files")
                size = path.stat().st_size
                total += size
                need(total <= 512 * MIB and len(rows) < 20000, "Bounded complete task checkpoint export")
                relative = path.relative_to(task).as_posix()
                pin = digest(path)
                zipped.write(path, "task/" + relative)
                need(path.stat().st_size == size and digest(path) == pin, "Stable checkpoint/source bytes during export")
                rows.append(dict(path="task/" + relative, bytes=size, sha256=pin))
        zipped.writestr("BUNDLE_MANIFEST.json", json.dumps(dict(
            schema="COUNT_CHECKPOINT_TRANSPORT_V1", files=rows, bytes=total,
            source_commit=COMMIT, transport_is_not_arithmetic_acceptance=True,
            all_index_conclusion_verified=False), indent=2) + "\n")
    result = dict(path=str(output), sha256=digest(output), bytes=output.stat().st_size,
                  files=len(rows), transport_is_not_arithmetic_acceptance=True)
    event(task, "checkpoint_bundle_written", **result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    prep = sub.add_parser("prepare", help="Fetch/verify fixed public assets and execute the frozen source preparer")
    prep.add_argument("--target", choices=tuple(TARGETS), required=True)
    prep.add_argument("--archives", type=Path, required=True)
    prep.add_argument("--output", type=Path, required=True)
    prep.add_argument("--download", action="store_true")
    find = sub.add_parser("search", help="Bounded UNTRUSTED pilot/slice; never native acceptance")
    find.add_argument("--task", type=Path, required=True)
    find.add_argument("--seconds", type=int, default=60)
    find.add_argument("--wall-seconds", type=int, default=120)
    find.add_argument("--resume", type=Path)
    find.add_argument("--published-hints", action="store_true")
    find.add_argument("--archives", type=Path)
    find.add_argument("--download", action="store_true")
    check = sub.add_parser("accept", help="Separate fresh canonical 26-root/24-control native acceptance")
    check.add_argument("--task", type=Path, required=True)
    check.add_argument("--candidate", type=Path, required=True)
    check.add_argument("--wall-seconds", type=int, default=7260)
    check.add_argument("--cpu-seconds", type=int, default=7200)
    pack = sub.add_parser("bundle", help="Export all sources, logs and primary/backup checkpoints without running mathematics")
    pack.add_argument("--task", type=Path, required=True)
    pack.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    need(__debug__ and not sys.flags.optimize, "Ordinary Python without -O/-OO")
    sys.dont_write_bytecode = True
    if args.action == "bundle":
        print(json.dumps(bundle_task(args.task, args.output)), flush=True)
        return 0
    task = args.output if args.action == "prepare" else args.task
    try:
        if args.action == "prepare":
            report = prepare(args.target, args.archives, args.output, download=args.download)
        elif args.action == "search":
            report = search(args.task, args.seconds, args.wall_seconds, resume=args.resume,
                            published_hints=args.published_hints, archives=args.archives, download=args.download)
        else:
            report = accept(args.task, args.candidate, wall_seconds=args.wall_seconds, cpu_seconds=args.cpu_seconds)
    except BaseException as error:
        if Path(task).is_dir():
            event(task, "task_incomplete", error=str(error), status="PARTIAL_NOT_ACCEPTED", arithmetic_accepted=False)
            try:
                bundle = bundle_task(task)
                print(json.dumps(dict(status="PARTIAL_NOT_ACCEPTED", checkpoint_bundle=bundle,
                                      arithmetic_accepted=False, all_index_conclusion_verified=False)), flush=True)
            except Exception as bundle_error:
                event(task, "checkpoint_export_incomplete", error=str(bundle_error), arithmetic_accepted=False)
        raise
    report["checkpoint_bundle"] = bundle_task(task)
    print(json.dumps(report), flush=True)
    return 2 if args.action == "search" and report["status"] == "PARTIAL_CANDIDATE_CHECKPOINT_ONLY" else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("COUNT_TASK_INCOMPLETE_NO_ACCEPTANCE: " + str(error), file=sys.stderr, flush=True)
        raise SystemExit(1)
