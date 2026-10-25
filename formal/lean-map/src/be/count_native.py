"""Source-replay adapter for one COMPLETE ordinary COUNT forest.

It neither acquires the contract hypotheses nor proves the all-law C6 bound.
Only reviewed, exact native code runs, in a new directory and process per role.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import struct
import sys
import sysconfig
import time
from typing import Callable
import uuid
import zipfile

MANIFEST_SHA256 = "194a1bd4a2a0f1dfbd6227c67c37f253048e8f4e643e59db55c4166431aa2c95"
DEFAULT_CAPSULE = Path(__file__).resolve().parents[2] / "vendor" / "count_native_n6_b0_p61"
PROTOCOL = "be.count-native/1"
JOB = "n6.B0.p61"
TRUST = "native-python-source-replay-conditional-v1"
MAX_FILE = 1024 * 1024
MAX_LOG = 1024 * 1024
MAX_NODES = 10000
MAX_DEPTH = 128
SOURCE_NAME = "count_protocol.py"
FOREST_NAME = "COUNT_FOREST.json"
RECEIPT_NAME = "COUNT_ACCEPTED.json"
TARGET = Fraction("76824784444199314310731654405729617052063596250011448874609/187500000000000000000000000000000000000000000000000000000000")
RATIONAL_TEXT = re.compile(r"-?[0-9]+(?:/[0-9]+)?\Z")
NativeSupervisor = Callable[[list[str], Path, Path, int], dict]


class CountError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def need(value, code: str, message: str):
    if not value:
        raise CountError(code, message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value) -> bytes:
    """Adapter metadata codec, DISTINCT from frozen be.arch/local-pilot codecs."""
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def identity(kind: str, value) -> str:
    return sha(("BECOUNTNATIVE/1\n" + kind + "\n").encode("ascii") + canonical(value))


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate_key", "Duplicate native JSON key")
        result[key] = value
    return result


def read_regular(path: Path, limit: int = MAX_FILE) -> bytes:
    need(path.is_file() and not path.is_symlink(), "regular_file", str(path))
    need(path.stat().st_size <= limit, "input_limit", str(path))
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    need(len(raw) <= limit, "input_limit", str(path))
    return raw


def native_json(raw: bytes):
    need(len(raw) <= MAX_FILE, "input_limit", "Native JSON exceeds one MiB")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=unique,
                          parse_constant=lambda _: (_ for _ in ()).throw(
                              CountError("nonfinite_json", "Nonfinite JSON number")))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise CountError("invalid_native_json", str(error)) from error


def q(text) -> Fraction:
    need(type(text) is str and len(text) <= 4096 and RATIONAL_TEXT.fullmatch(text),
         "rational_text", "Literal exact rational text required")
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError) as error:
        raise CountError("invalid_rational", str(error)) from error


def manifest() -> dict:
    raw = read_regular(DEFAULT_CAPSULE / "capsule-manifest.json")
    need(sha(raw) == MANIFEST_SHA256, "manifest_pin", "Exact reviewed source design")
    return native_json(raw)


def verify_capsule(directory: Path, *, include_original_forest=False) -> dict[str, bytes]:
    """Read each pinned byte before execution; never import the mathematical code."""
    descriptor = manifest()
    need(directory.is_dir() and not directory.is_symlink(), "capsule_directory", str(directory))
    result = {}
    for name, pin in descriptor["files"].items():
        if name == FOREST_NAME and not include_original_forest:
            continue
        need(Path(name).name == name and not any(x in name for x in ("/", "\\", ":")),
             "flat_source", "Flat reviewed source names")
        raw = read_regular(directory / name)
        need(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"],
             "source_pin", "Source design mismatch: " + name)
        result[name] = raw
    return result


def extract_archive(archive: Path, output: Path) -> dict:
    """Extract ONLY 29 source members; historical forests/receipts are not inputs."""
    d = manifest()
    need(not output.exists(), "fresh_directory", "Extraction never overwrites a capsule")
    need(archive.is_file() and not archive.is_symlink(), "archive_file", str(archive))
    need(archive.stat().st_size == d["asset"]["bytes"], "archive_size", "Exact source ZIP size")
    value = hashlib.sha256()
    with archive.open("rb") as stream:
        while block := stream.read(MAX_FILE):
            value.update(block)
    need(value.hexdigest() == d["asset"]["sha256"], "archive_pin", "Exact source ZIP SHA256")
    with zipfile.ZipFile(archive) as source:
        names = source.namelist()
        blobs = {}
        for name, pin in d["files"].items():
            if name == FOREST_NAME:
                continue
            need(names.count(pin["member"]) == 1, "archive_member", "One exact source member")
            info = source.getinfo(pin["member"])
            need(info.file_size == pin["bytes"] <= MAX_FILE,
                 "archive_member_limit", "Exact bounded source member")
            with source.open(info) as member:
                raw = member.read(MAX_FILE + 1)
            need(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"],
                 "archive_member_pin", "Exact archive source member: " + name)
            blobs[name] = raw
    output.mkdir(parents=True, exist_ok=False)
    for name, raw in blobs.items():
        with (output / name).open("xb") as stream:
            stream.write(raw)
    verify_capsule(output)
    return {"capsule_manifest_sha256": MANIFEST_SHA256, "files": len(blobs),
            "source_epoch": d["source_epoch"], "source_epoch_digest": source_epoch(),
            "historical_candidate_extracted": False, "historical_acceptance_extracted": False}


def source_epoch() -> str:
    d = manifest()
    return identity("source-epoch", {"epoch": d["source_epoch"],
                    "catalog_sha256": d["catalog_sha256"],
                    "files": {k: v["sha256"] for k, v in d["files"].items()
                              if k != FOREST_NAME}})


def statement(directory: Path) -> dict:
    """Unknown law is quantified by this scope, never supplied as runtime data."""
    blobs = verify_capsule(directory)
    return {"job_id": JOB, "n": "6", "probability": ["61/100", "31/50"],
            "orientation": "literal-positive-class-no-reflection",
            "axes": ["p", "lambda=n*noiseVariance", "alpha", "u", "a0"],
            "roots": [str(k) for k in range(7)],
            "phase": ["-1/2", "1/2"], "target": str(TARGET), "relation": "strict",
            "contract_sha256": sha(blobs["contract.json"]),
            "source_epoch_digest": source_epoch(),
            "conclusion": "conditional-positive-closed-point-score-below-target",
            "score": "sqrt(6)/rho*(CDF(sum6,H)-Phi(H/sqrt(6)))",
            "same_law_resource_acquisition": "required-external-not-established",
            "all_law_C6": False, "all_index_conclusion": False}


def precheck_forest(raw: bytes, directory: Path) -> dict:
    """Independent topology/type/header guard; arithmetic still uses native replay."""
    candidate = native_json(raw)
    blobs = verify_capsule(directory)
    cfg = native_json(blobs["contract.json"])["rows"][0]
    kernel = native_json(blobs["KERNEL_COPY_MANIFEST.json"])["files"]
    expected = {"schema": "ACTUAL6_GAMMA_SHARP_B0_P61_FRESH_COMPENSATED_RESOURCE_JOINT_CLOSED_COUNT_FOREST_V1",
                "n": 6, "index": 61, "target": str(TARGET),
                "contract_sha256": sha(blobs["contract.json"]),
                "kernel_sha256": kernel, "checker_sha256": sha(blobs[SOURCE_NAME])}
    need(type(candidate) is dict and set(candidate) == set(expected) | {"roots"},
         "forest_schema", "Exact native header and roots")
    for key, value in expected.items():
        need(type(candidate[key]) is type(value) and candidate[key] == value,
             "forest_header", "Exact native header: " + key)
    roots = candidate["roots"]
    need(type(roots) is list and len(roots) == 7, "all_roots", "All original k=0..6 roots")
    box = [[q(x) for x in cfg["p"]], [Fraction(0), q(cfg["Lambda"])],
           [Fraction(0), Fraction(1)], [Fraction(-1, 2), Fraction(1, 2)],
           [Fraction(0), q(cfg["d0"])]]
    nodes = leaves = max_depth = 0
    statuses = Counter()

    def walk(node, current, depth):
        nonlocal nodes, leaves, max_depth
        nodes += 1
        max_depth = max(max_depth, depth)
        need(nodes <= MAX_NODES and depth <= MAX_DEPTH, "forest_limit", "Finite complete tree budget")
        need(type(node) is dict, "tree_node", "Native tree node object")
        if node.get("kind") == "split":
            need(set(node) == {"kind", "axis", "cut", "left", "right"},
                 "complete_children", "Both closed children and no extra claims")
            axis = node["axis"]
            need(type(axis) is int and 0 <= axis < 5, "split_axis", "Exact five-dimensional axis")
            cut = q(node["cut"])
            need(current[axis][0] < cut < current[axis][1], "strict_cut", "Strict interior cut")
            left, right = ([x[:] for x in current] for _ in range(2))
            left[axis][1] = cut
            right[axis][0] = cut
            walk(node["left"], left, depth + 1)
            walk(node["right"], right, depth + 1)
            return
        need(node.get("kind") == "leaf" and set(node) == {"kind", "box", "decision", "result"},
             "leaf_schema", "Complete native leaf, without success shortcuts")
        expected_box = [[str(a), str(b)] for a, b in current]
        need(node["box"] == expected_box, "leaf_box", "Reconstruct original closed box before contractions")
        need(type(node["decision"]) is str and type(node["result"]) is dict,
             "leaf_payload", "Native leaf decision and full result")
        statuses[node["decision"]] += 1
        leaves += 1

    for k, root in enumerate(roots):
        need(type(root) is dict and set(root) == {"k", "tree"}
             and type(root["k"]) is int and root["k"] == k,
             "root_order", "Exactly ordered original count roots")
        walk(root["tree"], box, 0)
    return {"roots": len(roots), "nodes": nodes, "leaves": leaves,
            "maximum_depth": max_depth, "closed_statuses": dict(statuses)}


def _runtime_directories(directory: Path, checked: set) -> None:
    for item in (directory, *directory.parents):
        name = str(item)
        if name not in checked:
            need(not item.is_symlink() and not getattr(item, "is_junction", lambda: False)(),
                 "runtime_directory_link", "Runtime path directory aliases require a separately approved inventory")
            need(item.is_dir(), "runtime_directory", "Ordinary runtime parent directory required")
            checked.add(name)


def _runtime_file(path: Path, label: str, files: dict, links: dict, *, checked_directories=None) -> None:
    """Pin a literal file link chain and its final ordinary bytes, without omission."""
    original = Path(os.path.abspath(path))
    current = original
    checked_directories = set() if checked_directories is None else checked_directories
    chain, seen = [], set()
    try:
        while True:
            _runtime_directories(current.parent, checked_directories)
            if not current.is_symlink():
                break
            need(str(current) not in seen and len(chain) < 16,
                 "runtime_link_cycle", "Runtime file links must have a finite bounded chain")
            seen.add(str(current))
            target_text = os.readlink(current)
            chain.append({"path": str(current), "literal_target": target_text})
            target = Path(target_text)
            current = Path(os.path.abspath(target if target.is_absolute() else current.parent / target))
        resolved = current.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise CountError("runtime_link_target", "Runtime file target must exist and resolve") from error
    need(resolved.is_file() and not resolved.is_symlink(),
         "runtime_link_target", "Runtime file link must resolve to an ordinary file")
    raw = read_regular(resolved, 32 * MAX_FILE)
    digest = sha(raw)
    files[label] = digest
    if chain:
        links[label] = {"chain": chain, "resolved_path": str(resolved),
                        "resolved_sha256": digest, "resolved_bytes": str(len(raw))}


def runtime_profile() -> dict:
    """Pin Python executable/stdlib/extension bytes; no site packages are used (-S)."""
    need(sys.implementation.name == "cpython" and sys.version_info[:2] == (3, 12),
         "runtime_profile", "This first execution profile supports CPython 3.12 only")
    base = Path(sys.base_prefix)
    lib = Path(sysconfig.get_path("stdlib"))
    files, links, checked_directories = {}, {}, set()
    _runtime_file(Path(sys.executable), "interpreter", files, links, checked_directories=checked_directories)
    _runtime_directories(lib, checked_directories)
    candidates = []
    for folder, directories, names in os.walk(lib, followlinks=False):
        directories[:] = sorted(d for d in directories if d not in ("site-packages", "__pycache__"))
        # File links are explicitly pinned. This first Unix profile deliberately
        # fails on a linked import directory instead of silently skipping it.
        for name in directories:
            need(not (Path(folder) / name).is_symlink(), "runtime_directory_link",
                 "Linked runtime directories require a separately approved inventory")
        for name in names:
            path = Path(folder) / name
            if path.suffix in (".py", ".pyd", ".dll", ".so"):
                candidates.append(path)
    for path in sorted(candidates):
        _runtime_file(path, "stdlib/" + path.relative_to(lib).as_posix(), files, links,
                      checked_directories=checked_directories)
    if os.name == "nt":
        for folder in (base, base / "DLLs"):
            for path in sorted(folder.glob("*")):
                if path.is_file() and path.suffix in (".exe", ".dll", ".pyd"):
                    _runtime_file(path, "base/" + path.relative_to(base).as_posix(), files, links,
                                  checked_directories=checked_directories)
    # platform.platform()/uname() can invoke Windows WMI and block indefinitely.
    # These process-local values avoid discovery subprocesses and remote services.
    system_version = list(sys.getwindowsversion()[:5]) if os.name == "nt" else list(os.uname())
    profile = {"schema": "be.native-python-runtime/2", "python_version": sys.version, "implementation": "CPython",
               "system": sys.platform, "pointer_bits": struct.calcsize("P") * 8,
               "system_version": system_version, "files": files, "file_links": links,
               "flags": ["-E", "-B", "-S"], "external_numeric_packages": []}
    return {"profile": profile, "digest": identity("runtime-profile", profile)}


def cache_key(candidate_raw: bytes, directory: Path, runtime_digest: str) -> str:
    return identity("verification-key", {
        "statement_digest": identity("statement", statement(directory)),
        "candidate_bytes_sha256": sha(candidate_raw), "source_epoch_digest": source_epoch(),
        "native_checker_sha256": manifest()["files"][SOURCE_NAME]["sha256"],
        "adapter_sha256": sha(read_regular(Path(__file__))),
        "runtime_profile_digest": runtime_digest, "trust_profile": TRUST})


def _new_execution(directory: Path, workspace: Path, role: str) -> Path:
    blobs = verify_capsule(directory)
    workspace.mkdir(parents=True, exist_ok=True)
    out = workspace / (role[0] + "-" + uuid.uuid4().hex[:10])
    out.mkdir(exist_ok=False)
    for name, raw in blobs.items():
        with (out / name).open("xb") as stream:
            stream.write(raw)
    return out


def _default_supervisor(command: list[str], directory: Path, log: Path, timeout: int) -> dict:
    """Local direct-child execution; durable runners can replace this one port."""
    began = time.monotonic()
    with log.open("xb") as stream:
        child = subprocess.Popen(command, cwd=directory, stdout=stream, stderr=subprocess.STDOUT,
                                 stdin=subprocess.DEVNULL, shell=False)
        try:
            while child.poll() is None:
                need(time.monotonic() - began <= timeout, "native_timeout", "Native subprocess wall deadline")
                need(log.stat().st_size <= MAX_LOG, "native_log_limit", "Bounded native subprocess log")
                time.sleep(0.05)
        except BaseException:
            child.kill()
            child.wait()
            raise
    return {"returncode": child.returncode, "elapsed_seconds_observed": time.monotonic() - began}


def _native(directory: Path, action: str, timeout: int,
            supervisor: NativeSupervisor | None = None) -> dict:
    need(type(timeout) is int and 1 <= timeout <= 600, "timeout", "Bounded native wall time")
    before = verify_capsule(directory)
    need(not (directory / RECEIPT_NAME).exists(), "fresh_acceptance", "No historical acceptance is copied")
    log = directory / "native.log"
    need(not log.exists(), "fresh_log", "Supervisor receives a fresh private log path")
    command = [sys.executable, "-E", "-B", "-S", str(directory / SOURCE_NAME), action]
    metadata = (supervisor or _default_supervisor)(command, directory, log, timeout)
    need(type(metadata) is dict and type(metadata.get("returncode")) is int,
         "supervisor_result", "Supervisor must return the direct native child exit code")
    need(metadata["returncode"] == 0, "native_failure", "Native subprocess rejected or failed; see " + str(log))
    log_raw = read_regular(log, MAX_LOG)
    need(before == verify_capsule(directory), "source_changed", "Unchanged exact source through replay")
    return {"command": ["python", "-E", "-B", "-S", SOURCE_NAME, action],
            "returncode": "0", "log_sha256": sha(log_raw),
            "execution_directory": str(directory), "supervisor_metadata": metadata}


def construct(capsule: Path, workspace: Path, *, timeout=300,
              supervisor: NativeSupervisor | None = None) -> dict:
    run = _new_execution(capsule, workspace, "produce")
    process = _native(run, "construct", timeout, supervisor)
    raw = read_regular(run / FOREST_NAME)
    census = precheck_forest(raw, run)
    return {"schema_version": PROTOCOL, "operation": "produce", "job_id": JOB,
            "candidate": str(run / FOREST_NAME), "candidate_bytes_sha256": sha(raw),
            "original_candidate_bytes_sha256": manifest()["files"][FOREST_NAME]["sha256"],
            "matches_original_bytes": sha(raw) == manifest()["files"][FOREST_NAME]["sha256"],
            "census": census, "process": process, "mathematically_accepted": False}


def accept(capsule: Path, candidate: Path, workspace: Path, *, timeout=300,
           supervisor: NativeSupervisor | None = None) -> dict:
    adapter_pin = sha(read_regular(Path(__file__)))
    raw = read_regular(candidate)
    census = precheck_forest(raw, capsule)
    environment = runtime_profile()
    run = _new_execution(capsule, workspace, "verify")
    with (run / FOREST_NAME).open("xb") as stream:
        stream.write(raw)
    process = _native(run, "accept", timeout, supervisor)
    receipt_raw = read_regular(run / RECEIPT_NAME)
    receipt = native_json(receipt_raw)
    d = manifest()
    expected = d["native_receipt_schema"]
    need(type(receipt) is dict and set(receipt) == set(expected["fields"]),
         "receipt_schema", "Exact native success schema")
    for field in ("status", "n", "index", "scope"):
        need(type(receipt[field]) is type(expected[field]) and receipt[field] == expected[field],
             "receipt_binding", "Native receipt literal " + field)
    blobs = verify_capsule(capsule)
    for field, name in (("forest_sha256", FOREST_NAME), ("contract_sha256", "contract.json"),
                        ("checker_sha256", SOURCE_NAME)):
        expected_sha = sha(raw) if name == FOREST_NAME else sha(blobs[name])
        need(receipt[field] == expected_sha, "receipt_binding", "Native receipt " + field)
    need(receipt["kernel_sha256"] == native_json(blobs["KERNEL_COPY_MANIFEST.json"])["files"],
         "receipt_kernel", "Exact frozen kernel closure")
    need(receipt["negative_controls"] == expected["controls"],
         "receipt_controls", "All twenty-four native negative controls")
    stats = receipt["statistics"]
    need(type(stats) is dict and set(stats) == {"nodes", "leaves", "closed_statuses", "maximum_score", "maximum_depth"},
         "receipt_statistics", "Complete native census")
    for key in ("nodes", "leaves", "maximum_depth", "closed_statuses"):
        need(type(stats[key]) is type(census[key]) and stats[key] == census[key],
             "receipt_statistics", "Native census matches the complete candidate")
    need(type(receipt["fresh_leaf_evaluations"]) is int
         and receipt["fresh_leaf_evaluations"] == census["leaves"],
         "fresh_leaf_count", "Every original leaf freshly evaluated")
    need(q(stats["maximum_score"]) < TARGET, "strict_target", "Strict ordinary COUNT target")
    need(type(receipt["seconds"]) in (int, float) and math.isfinite(receipt["seconds"])
         and receipt["seconds"] >= 0, "receipt_timing", "Finite observed timing only")
    need(sha(read_regular(run / FOREST_NAME)) == sha(raw), "candidate_changed", "Unchanged candidate through replay")
    need(runtime_profile()["digest"] == environment["digest"], "runtime_changed", "Unchanged Python source/ABI profile")
    need(sha(read_regular(Path(__file__))) == adapter_pin, "adapter_changed", "Unchanged adapter through replay")
    fixed_statement = statement(capsule)
    return {"schema_version": PROTOCOL, "outcome": "SCOPED_COUNT_PASS", "job_id": JOB,
            "statement": fixed_statement, "statement_digest": identity("statement", fixed_statement),
            "verification_key": cache_key(raw, capsule, environment["digest"]),
            "candidate_bytes_sha256": sha(raw), "source_epoch_digest": source_epoch(),
            "native_receipt_bytes_sha256": sha(receipt_raw), "native_receipt": str(run / RECEIPT_NAME),
            "native_statistics": stats, "negative_controls": receipt["negative_controls"],
            "runtime_profile_digest": environment["digest"], "runtime_profile": environment["profile"],
            "trust_profile": TRUST, "parent_acquisitions_verified": False,
            "all_law_C6_verified": False, "all_index_conclusion_verified": False,
            "full_proof_pass": False, "process": process}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    extract = commands.add_parser("extract")
    extract.add_argument("--archive", type=Path, required=True)
    extract.add_argument("--output", type=Path, required=True)
    for action in ("produce", "verify"):
        sub = commands.add_parser(action)
        sub.add_argument("--capsule", type=Path, required=True)
        sub.add_argument("--workspace", type=Path, required=True)
        sub.add_argument("--output", type=Path, required=True)
        sub.add_argument("--timeout", type=int, default=300)
        if action == "verify":
            sub.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    try:
        need(__debug__ and not sys.flags.optimize, "optimization_forbidden", "Source replay requires assertions enabled")
        if args.action == "extract":
            result = extract_archive(args.archive.resolve(), args.output.resolve())
            print(canonical(result).decode("ascii"))
            return
        need(not args.output.exists(), "fresh_output", "Do not overwrite an adapter observation")
        capsule, workspace = args.capsule.resolve(), args.workspace.resolve()
        if args.action == "produce":
            result = construct(capsule, workspace, timeout=args.timeout)
        else:
            result = accept(capsule, args.candidate.resolve(), workspace, timeout=args.timeout)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as stream:
            stream.write(canonical(result))
        print(canonical({"operation": args.action, "outcome": result.get("outcome", "CANDIDATE_PRODUCED"),
                         "full_proof_pass": False, "output": str(args.output)}).decode("ascii"))
    except CountError as error:
        print(canonical({"error": error.code, "message": str(error), "full_proof_pass": False}).decode("ascii"), file=sys.stderr)
        raise SystemExit(3) from error


if __name__ == "__main__":
    main()
