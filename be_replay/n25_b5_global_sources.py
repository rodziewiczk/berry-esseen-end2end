"""Source-only selection for two unchanged lower-B5 full parent acceptances.

The two complete proof objects are untrusted candidates. No historical accepted
output, progress file, count forest or local feedback result is selected.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath

from . import aux24_sources as source, count_task as common

ROOT = Path(__file__).resolve().parents[1]
CATALOG = "proof/n25_b5_global_sources.json"
CATALOG_SHA = "951fcef1722dd2c9f5c868ac364dd3b01cc8837d86c9d76b6670da9646f50827"
MIB = 1024**2


def need(ok, message):
    if not ok: raise ValueError(message)


def definition(branch="b5"):
    need(branch == "b5", "Only the exact lower-B5 global parent pair")
    need(common.digest(ROOT/CATALOG) == CATALOG_SHA, "Independent exact lower-B5 source catalog")
    parent = common.read(ROOT/CATALOG, 16*MIB)
    need(parent["schema"] == "N25_B5_GLOBAL_PARENT_SOURCE_CATALOG_V1"
         and parent["branch"] == "b5" and type(parent["n"]) is int and parent["n"] == 25
         and parent["selected_full_actions"] == 2 and parent["contact_allowance"] == "5/16"
         and parent["mathematical_code_executed"] is False
         and parent["historical_acceptances_imported_as_inputs"] == 0
         and parent["full_n25_verified"] is False and parent["all_index_conclusion_verified"] is False,
         "Exact conditional source selection")
    return parent


def selected(branch="b5"):
    parent = definition(branch)
    rows = {}
    def add(row, kind):
        name = row["member"]; source._kind(name, kind)
        value = dict(sha256=row["sha256"], bytes=row["bytes"], kind=kind)
        need(name not in rows or rows[name] == value, "Consistent deduplicated parent input")
        rows[name] = value
    for kind in ("initial", "global_resource"):
        section = parent[kind]
        add(section["closure"]["manifest"], "source")
        for row in section["closure"]["source_file_rows"]:
            add(row, "premise" if row["role"] == "conditional_statement_premise" else "source")
        add(section["proof_candidate"], "candidate")
    need(len(rows) == 66 and len({n.casefold() for n in rows}) == len(rows),
         "All66 original source/candidate inputs, with no accepted receipts")
    return rows


def selection_manifest(branch="b5"):
    return dict(schema=source.SCHEMA, archive=source.ARCHIVE, files=selected(branch),
                mathematical_code_executed=False, historical_acceptances_imported=0,
                premises_acquired=False, all_index_conclusion_verified=False)


def selection_sha(branch="b5"):
    raw = json.dumps(selection_manifest(branch), sort_keys=True, indent=2, ensure_ascii=True)+"\n"
    return hashlib.sha256(raw.encode()).hexdigest()


def prepare(task, branch="b5", *, archives, download=False, progress=None):
    rows = selected(branch)
    source.prepare(task, archives=archives, members={n:r["kind"] for n,r in rows.items()},
                   download=download, progress=progress)
    verify(task, branch)
    return Path(task)


def verify(task, branch="b5"):
    source.verify_prepared(task, expected_manifest_sha=selection_sha(branch))
    manifest = common.read(Path(task)/source.MANIFEST, 16*MIB)
    need(manifest == selection_manifest(branch), "Exact complete independently selected input bytes")
    return manifest


def stages(branch="b5"):
    parent = definition(branch)
    result = []
    for kind in ("initial", "global_resource"):
        section = parent[kind]
        result.append(dict(name=kind+"-accept", kind=kind, action="accept",
            folder=section["directory"].removeprefix(source.PREFIX),
            script=PurePosixPath(section["checker"]["member"]).name, args=["accept"],
            proof=PurePosixPath(section["proof_candidate"]["member"]).name,
            receipt=PurePosixPath(section["historical_acceptance"]["member"]).name))
    return result
