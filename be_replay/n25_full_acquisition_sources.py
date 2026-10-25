"""Immutable original inputs and explicit cache metadata epochs inside66.

This module performs source/JSON/AST operations only. Fresh constructors and
full acceptors run exclusively in separate supervised Colab children.
"""
from __future__ import annotations
import ast
from copy import deepcopy
from pathlib import Path
import shutil
import sys
from . import n25_b5_reconstruction_sources as base,count_task as common

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/"proof/n25_full_acquisition_source_plan.json"
PLAN_SHA256="71d45fc0c4885f728a0e7373b4af5e71204b14975c407b1f32ac49f4cc34ccbd"
PREFIX="cutoff25_20261011/"
need=base.need


def plan():
    raw=base._regular(PLAN,8*1024**2)
    need(base.sha(raw)==PLAN_SHA256,"Externally fixed complete remaining acquisition source plan")
    data=base.parsed(raw)
    need(data["schema"]=="N25_FULL66_ACQUISITION_SOURCE_PLAN_V1" and data["archive"]==common.ASSETS["old"]
         and data["mathematical_code_executed"] is False and data["historical_acceptances_staged"]==0
         and data["arithmetic_accepted"] is False and data["full66_complete"] is False,
         "Source-only acquisition plan, never an old acceptance transport")
    return data


def families():return tuple(f["id"] for f in plan()["families"])


def definition(family):
    need(type(family) is str,"Literal acquisition family")
    matches=[r for r in plan()["families"] if r["id"]==family]
    need(len(matches)==1,"One exact selected acquisition family")
    return deepcopy(matches[0])


def selected(family):
    data=plan();spec=definition(family)
    return {n:data["inputs"][n] for n in spec["input_members"]}


def _imports(rows,family):
    """All literal archived imports are standard-library or exact local files."""
    py={n for n in rows if n.endswith(".py")}
    spec=definition(family)
    for name,raw in rows.items():
        if not name.endswith(".py"):continue
        parent=Path(name).parent
        for node in ast.walk(ast.parse(raw)):
            if isinstance(node,ast.Import):names=[a.name for a in node.names]
            elif isinstance(node,ast.ImportFrom):
                need(not node.level,"Original flat module imports only");names=[node.module or ""]
            else:continue
            for imported in names:
                root=imported.split(".")[0]
                present=root in sys.stdlib_module_names or (parent/(root+".py")).as_posix() in py
                cache=next((c for c in spec["cache_directories"] if PREFIX+c["folder"]==parent.as_posix()),None)
                if not present and cache is not None:
                    present=(PREFIX+cache["original_directory"]+"/"+root+".py") in py
                    if root=="exact_stage_cache":
                        matches=[p for p in py if "/stage_cache" in p and p.endswith("/exact_stage_cache.py")]
                        present=bool(matches) and len({base.sha(rows[p]) for p in matches})==1
                need(present,
                     "Every original literal import has exact source bytes: "+name+" -> "+imported)


def prepare(task,family,*,archive):
    task=Path(task).absolute();base._no_link_ancestors(task)
    need(not task.exists(),"Fresh acquisition source task only")
    rows=selected(family)
    request=dict(archives={"old":plan()["archive"]},inputs={"old:"+n:r for n,r in rows.items()})
    inputs=base._read_inputs(request,{"old":archive})
    data={n:inputs["old:"+n] for n in rows}
    return _prepare_data(task,family,data)


def prepare_from_cache(task,family,*,cache):
    """Use only bytes matching every externally pinned selected archive member."""
    task=Path(task).absolute();base._no_link_ancestors(task)
    need(not task.exists(),"Fresh acquisition source task only")
    data={}
    for name,row in selected(family).items():
        raw=base._regular(Path(cache)/name)
        need(len(raw)==row["bytes"] and base.sha(raw)==row["sha256"],"Actual exact cached original member: "+name)
        data[name]=raw
    return _prepare_data(task,family,data)


def _prepare_data(task,family,data):
    task=Path(task);rows=selected(family)
    _imports(data,family)
    manifest=dict(schema="N25_FULL66_ACQUISITION_INPUTS_V1",family=family,source_plan_sha256=PLAN_SHA256,
        files=rows,arithmetic_accepted=False,full66_complete=False)
    task.mkdir(parents=True,exist_ok=False)
    for name,raw in data.items():
        path=task/"source"/name;path.parent.mkdir(parents=True,exist_ok=True)
        with path.open("xb") as stream:stream.write(raw)
    (task/"SOURCES.json").write_bytes(base.encoded(manifest))
    verify(task,family)
    initialize_epoch(task,family)
    return manifest


def verify(task,family):
    task=Path(task);base._no_link_ancestors(task)
    rows=selected(family)
    expected=dict(schema="N25_FULL66_ACQUISITION_INPUTS_V1",family=family,source_plan_sha256=PLAN_SHA256,
        files=rows,arithmetic_accepted=False,full66_complete=False)
    actual=base.parsed(base._regular(task/"SOURCES.json",8*1024**2))
    need(base._same(expected,actual),"Exact source-only family selection")
    files=set()
    for path in (task/"source").rglob("*"):
        base._no_link_ancestors(path)
        if path.is_file():files.add(path.relative_to(task/"source").as_posix())
        else:need(path.is_dir(),"Regular original source directory")
    need(files==set(rows),"All exact original selected source/candidate bytes, without receipts")
    for name,row in rows.items():
        raw=base._regular(task/"source"/name)
        need(len(raw)==row["bytes"] and base.sha(raw)==row["sha256"],"Immutable original input: "+name)
    return expected


def projections(task,family):
    rows=selected(family);result={}
    for cache in definition(family)["cache_directories"]:
        name=PREFIX+cache["folder"]+"/FROZEN_SOURCES.json"
        old=base.parsed(base._regular(Path(task)/"source"/name))
        need(old["schema"]==cache["schema"],"Original flexible named cache source gate")
        wanted={n.removeprefix(PREFIX):r["sha256"] for n,r in rows.items()
            if r["role"] not in ("untrusted_candidate","historical_cache_manifest")
            and old["files_sha256"].get(n.removeprefix(PREFIX))==r["sha256"]}
        need(wanted and cache["original_directory"]+"/acquire_panel.py" in wanted,
             "Projection retains the actual complete original local checker")
        projected=dict(old,files_sha256=wanted,scope="New source-only transport epoch. Exact original mathematics remains bound by the complete independent source plan; historical executions and receipts are not input evidence. Fresh accepted parent aliases are checked separately.")
        raw=base.encoded(projected)
        descriptor=dict(schema="N25_FULL66_NAMED_CACHE_SOURCE_PROJECTION_V1",family=family,
            source_plan_sha256=PLAN_SHA256,original_manifest_sha256=base.sha(base._regular(Path(task)/"source"/name)),
            original_manifest_rows=len(old["files_sha256"]),projected_manifest_sha256=base.sha(raw),
            projected_source_rows=len(wanted),projected_files_sha256=wanted,
            mathematical_source_changed=False,historical_manifest_acceptance_claimed=False,
            historical_acceptances_imported=0,arithmetic_accepted=False,full66_complete=False)
        result[name]=raw
        result[PREFIX+cache["folder"]+"/CACHE_SOURCE_EPOCH.json"]=base.encoded(descriptor)
    return result


def initialize_epoch(task,family):
    verify(task,family);task=Path(task)
    destination=task/"epoch"
    need(not destination.exists(),"Fresh current-context execution epoch")
    shutil.copytree(task/"source",destination)
    for name,raw in projections(task,family).items():
        path=destination/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    return destination/PREFIX.rstrip("/")


def epoch_rows(task,family):
    result={n:dict(bytes=r["bytes"],sha256=r["sha256"]) for n,r in selected(family).items()}
    for name,raw in projections(task,family).items():result[name]=dict(bytes=len(raw),sha256=base.sha(raw))
    return result
