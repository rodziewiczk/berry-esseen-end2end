"""Pinned, source-only preparation for the auxiliary 21--24 replay jobs.

Nothing in this module imports or executes a mathematical capsule. Candidates
are untrusted input objects; explicitly selected premises remain conditional.
Historical acceptance outputs are never extracted as fresh acceptance.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

from . import count_task as common

ARCHIVE = dict(name="cutoff25_20261011.zip", tag="cutoff20-sources-2026-10-17",
               bytes=514958998, sha256="17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb")
PREFIX = "cutoff25_20261011/"
MANIFEST = "SOURCES.json"
TASK = "SOURCE_TASK.json"
SCHEMA = "PINNED_AUX21_24_SOURCE_SELECTION_V1"
KINDS = {"source", "candidate", "premise"}
MIB = 1024**2
MAX_MEMBER = 128*MIB
MAX_TOTAL = 1024*MIB
MAX_FILES = 20000
_DEVICE = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", re.I)
_ACCEPTANCE = re.compile(r"(?:^|[_-])(ACCEPTED|ACCEPTANCE|RECEIPT|EXECUTION|PROGRESS|COMPLETED)(?:[_\-.]|$)", re.I)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return common.digest(path)


def _name(name, *, full=True):
    need(type(name) is str and name and "\\" not in name and ":" not in name,
         "Literal portable ZIP member path")
    parts = name.split("/")
    need(all(p and p not in (".", "..") and p == p.rstrip(" .")
             and not _DEVICE.match(p) and not any(ord(c) < 32 for c in p) for p in parts)
         and not PurePosixPath(name).is_absolute(), "No unsafe or ambiguous member path")
    if full:
        need(name.startswith(PREFIX) and len(parts) > 1, "Member belongs to the exact cutoff25 source root")
    return name


def _kind(name, kind):
    _name(name)
    need(kind in KINDS, "Explicit source, candidate or conditional premise classification")
    base = PurePosixPath(name).name
    if base.lower().endswith(".json"):
        need(not _ACCEPTANCE.search(base) and base.upper() != "OPTIMIZATION_EQUIVALENCE.JSON"
             and not base.upper().endswith("_BACKEND.JSON"),
             "Historical acceptance/execution outputs are not source inputs")
        if "JOINED" in base.upper() or "CHECKED" in base.upper():
            need(kind in ("candidate", "premise"),
                 "Historical numeric objects require an explicit untrusted candidate or conditional premise")
    if kind in ("candidate", "premise"):
        need(base.lower().endswith(".json"), "Candidate and premise inputs are explicit JSON objects")
    return kind


def archive(archives, *, download=False, progress=None):
    """Locate/download the exact public asset using the existing bounded fetcher."""
    need(common.ASSETS["old"] == ARCHIVE, "Same reviewed public source asset")
    return common.obtain_asset(archives, "old", download=download, progress=progress)


def _zip(path):
    common.verify_asset(path, ARCHIVE)
    return zipfile.ZipFile(path)


def _selected_info(z, names):
    wanted = set(names)
    found = {}
    for info in z.infolist():
        if info.filename not in wanted:
            continue
        need(info.filename not in found, "No duplicate selected ZIP member")
        mode = stat.S_IFMT(info.external_attr >> 16)
        need(not info.is_dir() and mode in (0, stat.S_IFREG)
             and not info.flag_bits & 1 and 0 <= info.file_size <= MAX_MEMBER,
             "Bounded ordinary unencrypted selected ZIP file")
        found[info.filename] = info
    need(set(found) == wanted, "Every exact selected ZIP member exists")
    need(sum(i.file_size for i in found.values()) <= MAX_TOTAL, "Bounded selected expansion")
    return found


def _copy_hash(z, info, output=None):
    value = hashlib.sha256()
    size = 0
    with z.open(info) as stream:
        while block := stream.read(MIB):
            size += len(block)
            need(size <= info.file_size and size <= MAX_MEMBER, "Exact bounded selected member length")
            value.update(block)
            if output is not None:
                output.write(block)
    need(size == info.file_size, "Complete selected member read")
    return dict(bytes=size, sha256=value.hexdigest())


def inspect_members(archive_path, prefixes=()):
    """Return exact member size/hash inventory for selected prefixes; no extraction."""
    prefixes = tuple(prefixes)
    for prefix in prefixes:
        if prefix.rstrip("/") != PREFIX.rstrip("/"):
            _name(prefix.rstrip("/"))
    with _zip(archive_path) as z:
        names = [i.filename for i in z.infolist() if not i.is_dir()
                 and i.filename.startswith(PREFIX)
                 and (not prefixes or any(i.filename == p.rstrip("/") or i.filename.startswith(p.rstrip("/")+"/")
                                          for p in prefixes))]
        need(len(names) <= MAX_FILES, "Bounded source inventory; select narrower prefixes")
        for name in names:
            _name(name)
        info = _selected_info(z, names)
        return {name: _copy_hash(z, info[name]) for name in sorted(info)}


def source_root(task):
    return Path(task).resolve() / "source" / PREFIX.rstrip("/")


def _json(path):
    return common.read(path, limit=16*MIB)


def _write(path, data):
    # The exact encoding/order is part of the deterministic selection pin.
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, sort_keys=True, indent=2, ensure_ascii=True)
        stream.write("\n")


def prepare(output, *, archives, members, download=False, progress=None):
    """Copy only explicit inputs to a new source tree and write a deterministic pin.

    Keys are complete archive paths. Runners may explicitly classify numeric
    proof objects as candidates, but must not select historical acceptances.
    """
    need(type(members) is dict and 0 < len(members) <= MAX_FILES, "Nonempty explicit selected member dictionary")
    for name, kind in members.items():
        _kind(name, kind)
    need(len({n.casefold() for n in members}) == len(members), "No case-insensitive selected path collisions")
    output = Path(output)
    need(not output.is_symlink() and not output.exists(), "New private source task; no historical output reuse")
    output = output.resolve()
    path = archive(archives, download=download, progress=progress)
    # Validate selection completely before creating any destination.
    with _zip(path) as z:
        selected = _selected_info(z, members)
        output.mkdir(parents=True)
        files = {}
        for name in sorted(members):
            target = output / "source" / name
            need(target.resolve().is_relative_to(output / "source"), "Selected output stays inside private source tree")
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                row = _copy_hash(z, selected[name], stream)
            files[name] = dict(kind=members[name], **row)
    manifest = dict(schema=SCHEMA, archive=ARCHIVE, files=files,
                    mathematical_code_executed=False, historical_acceptances_imported=0,
                    premises_acquired=False, all_index_conclusion_verified=False)
    _write(output / MANIFEST, manifest)
    _write(output / TASK, dict(schema="AUX21_24_SOURCE_TASK_V1", manifest_sha256=digest(output / MANIFEST),
          preparer_sha256=digest(__file__), selected_files=len(files),
          native_arithmetic_accepted=False, premises_acquired=False, all_index_conclusion_verified=False))
    verify_prepared(output)
    return output


def verify_prepared(task, expected_manifest_sha=None, *, outputs=(), expected_preparer_sha=None):
    """Rehash immutable inputs; allow only explicitly named fresh source-tree outputs.

    Output names are relative to source_root(task), without the cutoff25 root
    prefix. Task-root execution ledgers are outside this sealed source subtree.
    The caller remains responsible for validating every declared fresh output.
    """
    task = Path(task)
    need(not task.is_symlink(), "Ordinary private source task")
    task = task.resolve()
    for name in (MANIFEST, TASK):
        p = task / name
        need(p.is_file() and not p.is_symlink(), "Ordinary source selection metadata")
    manifest_hash = digest(task / MANIFEST)
    need(expected_manifest_sha is None or manifest_hash == expected_manifest_sha,
         "Expected exact source/candidate selection manifest")
    m = _json(task / MANIFEST)
    need(set(m) == {"schema", "archive", "files", "mathematical_code_executed", "historical_acceptances_imported",
                    "premises_acquired", "all_index_conclusion_verified"}
         and m["schema"] == SCHEMA and m["archive"] == ARCHIVE
         and m["mathematical_code_executed"] is False and type(m["historical_acceptances_imported"]) is int
         and m["historical_acceptances_imported"] == 0 and m["premises_acquired"] is False
         and m["all_index_conclusion_verified"] is False, "Exact source-only selection scope")
    files = m["files"]
    need(type(files) is dict and 0 < len(files) <= MAX_FILES, "Complete finite selected input inventory")
    need(len({n.casefold() for n in files}) == len(files)
         and sum(row.get("bytes", MAX_TOTAL+1) for row in files.values()
                 if type(row) is dict and type(row.get("bytes")) is int) <= MAX_TOTAL,
         "Portable finite selected input inventory")
    record = _json(task / TASK)
    prep = record.get("preparer_sha256")
    need(type(prep) is str and re.fullmatch(r"[0-9a-f]{64}", prep)
         and (expected_preparer_sha is None or prep == expected_preparer_sha)
         and type(record.get("selected_files")) is int
         and record.get("native_arithmetic_accepted") is False and record.get("premises_acquired") is False
         and record.get("all_index_conclusion_verified") is False
         and record == dict(schema="AUX21_24_SOURCE_TASK_V1", manifest_sha256=manifest_hash,
             preparer_sha256=prep, selected_files=len(files), native_arithmetic_accepted=False,
             premises_acquired=False, all_index_conclusion_verified=False), "Selection and recorded preparer source binding")
    for name, row in files.items():
        need(type(row) is dict and set(row) == {"kind", "bytes", "sha256"}, "Exact member identity row")
        _kind(name, row["kind"])
        p = task / "source" / name
        need(type(row["bytes"]) is int and 0 <= row["bytes"] <= MAX_MEMBER
             and type(row["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", row["sha256"])
             and p.is_file() and not p.is_symlink() and p.stat().st_size == row["bytes"]
             and digest(p) == row["sha256"], "Unchanged exact selected input: " + name)
    allowed = set()
    for name in outputs:
        _name(name, full=False)
        full = PREFIX + name
        need(full not in files and full not in allowed, "Fresh output is distinct from every selected input")
        allowed.add(full)
    tree = task / "source"
    need(tree.is_dir() and not tree.is_symlink(), "Ordinary sealed source tree")
    required_dirs = set()
    for name in set(files) | allowed:
        required_dirs.update(parent.as_posix() for parent in PurePosixPath(name).parents if parent.as_posix() != ".")
    actual = set()
    for p in tree.rglob("*"):
        need(not p.is_symlink(), "No source tree symlinks")
        if p.is_dir():
            need(p.relative_to(tree).as_posix() in required_dirs, "No unknown source tree directories")
            continue
        need(p.is_file(), "Ordinary selected source or declared fresh output")
        actual.add(p.relative_to(task / "source").as_posix())
    need(actual - set(files) <= allowed and set(files) <= actual,
         "No unknown, missing or historical acceptance outputs in source tree")
    return m
