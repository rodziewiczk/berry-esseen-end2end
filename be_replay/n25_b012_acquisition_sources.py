"""Exact source-only selection for the ten remaining B0--B2 parent actions.

The historical INITIAL and resource objects are untrusted candidates. Historical
acceptance receipts and local candidates are deliberately absent from this lane.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath

from . import aux24_sources as source, count_task as common

ROOT = Path(__file__).resolve().parents[1]
PARENT = "proof/n25_b012_parent_sources.json"
PARENT_SHA = "74c99c35bd189bbfef521c41659082eed82cdb055c670a955300e4bbbd13fbf9"
LOCAL = "proof/n25_b012_local_interfaces.json"
COUNTS = "proof/n25_retained_b012_catalog.json"
# These independent, literal pins are finalized from the reviewed catalog bytes.
LOCAL_SHA = "0f1cea303dd535b168646728c4c8fe03a976becf84d352d703f1d7f82c3158e8"
COUNTS_SHA = "f055b5017d4e1fd14f2b48a6a95fef4a4c61a025dea6174c424cd5968de801f7"
MIB = 1024**2


def need(ok, message):
    if not ok:
        raise ValueError(message)


def catalogs():
    packets = []
    for name, pin in ((PARENT, PARENT_SHA), (LOCAL, LOCAL_SHA), (COUNTS, COUNTS_SHA)):
        need(common.digest(ROOT/name) == pin, "Independently pinned acquisition catalog: " + name)
        packets.append(common.read(ROOT/name, 16*MIB))
    return packets


def definition(branch):
    need(branch in ("b0", "b1", "b2"), "One explicit lower n25 branch")
    parents, locals_, counts = catalogs()
    parent = next(row for row in parents["branches"] if row["branch"] == branch)
    local = next((row for row in locals_["branches"] if row["branch"] == branch), None)
    jobs = [row for row in counts["jobs"] if row["branch"] == branch]
    need(len(jobs) == {"b0": 17, "b1": 35, "b2": 23}[branch], "Complete fixed retained-count selection")
    return parent, local, jobs


def selected(branch):
    parent, local, jobs = definition(branch)
    rows = {}

    def add(row, kind):
        name = row["member"]
        source._kind(name, kind)
        value = dict(sha256=row["sha256"], bytes=row["bytes"], kind=kind)
        need(name not in rows or rows[name] == value, "Consistent deduplicated acquisition input")
        rows[name] = value

    for key in ("initial", "global_resource"):
        section = parent[key]
        add(section["closure"]["manifest"], "source")
        for row in section["closure"]["source_file_rows"]:
            add(row, "premise" if row["role"] == "conditional_statement_premise" else "source")
        add(section["proof_candidate"], "candidate")
    if local:
        manifest = local["source_manifests"][0]
        add(manifest, "source")
        prefix = PurePosixPath(manifest["member"]).parent.as_posix()+"/"
        for row in manifest["files"]:
            add(dict(row, member=prefix+row["filename"]), "source")
    for job in jobs:
        contract = next(row for row in job["source_file_rows"] if row["filename"] == "contract.json")
        add(contract, "candidate")
    need(len({n.casefold() for n in rows}) == len(rows), "Unique portable source paths")
    return rows


def selection_manifest(branch):
    return dict(schema=source.SCHEMA, archive=source.ARCHIVE, files=selected(branch),
                mathematical_code_executed=False, historical_acceptances_imported=0,
                premises_acquired=False, all_index_conclusion_verified=False)


def selection_sha(branch):
    raw = json.dumps(selection_manifest(branch), sort_keys=True, indent=2, ensure_ascii=True)+"\n"
    return hashlib.sha256(raw.encode()).hexdigest()


def prepare(task, branch, *, archives, download=False, progress=None):
    rows = selected(branch)
    source.prepare(task, archives=archives, members={n: row["kind"] for n, row in rows.items()},
                   download=download, progress=progress)
    verify(task, branch)
    return Path(task)


def verify(task, branch):
    source.verify_prepared(task, expected_manifest_sha=selection_sha(branch))
    manifest = common.read(Path(task)/source.MANIFEST, 16*MIB)
    need(manifest == selection_manifest(branch), "Exact complete independently selected input bytes")
    return manifest


def stages(branch):
    parent, local, _ = definition(branch)
    result = []
    for kind in ("initial", "global_resource"):
        section = parent[kind]
        result.append(dict(name=kind+"-accept", kind=kind, action="accept",
            folder=section["directory"].removeprefix(source.PREFIX),
            script=PurePosixPath(section["checker"]["member"]).name, args=["accept"],
            proof=PurePosixPath(section["proof_candidate"]["member"]).name,
            receipt=PurePosixPath(section["historical_acceptance"]["member"]).name))
    if local:
        for action in ("construct", "accept"):
            result.append(dict(name="local-"+action, kind="local", action=action,
                folder=local["cwd_member_prefix"].removeprefix(source.PREFIX).rstrip("/"),
                script=PurePosixPath(local["local_memoized_checker"]["member"]).name,
                args=[action, str(local["panel"])], proof=f'PANEL_{local["panel"]}_PROOF.json',
                receipt=f'PANEL_{local["panel"]}_ACCEPTED.json' if action == "accept" else None))
    return result
