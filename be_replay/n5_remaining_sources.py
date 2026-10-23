"""Pinned source preparation for the selected remaining n5 arithmetic.

Only bytes, JSON and candidate-tree structure are inspected here. The old
mathematical modules are never imported by preparation or evidence validation.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import time
import urllib.request
import uuid
import zipfile
from .n5_remaining_bridge import RESOURCE_POLICY

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor/n5_remaining_snapshot_v1"
CATALOG = ROOT / "proof/n5_remaining_catalog.json"
CATALOG_SHA256 = "29cd3d9f8c30d8391b19792d5197a5a9d6b26b67e294500f53b2827441553ca3"
SNAPSHOT_SHA256 = "53257e64c0712ea4b8ceac81472b57f6623754f55636fc56f29586670e330f8d"
ASSET_URL = "https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/download/cutoff5-sources-2026-10-20/cutoff5_20261020.zip"
MIB = 1024**2


def need(ok, reason):
    if not ok: raise ValueError(reason)


def digest(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(MIB), b""): h.update(b)
    return h.hexdigest()


def unique(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,"Duplicate JSON field: "+k);out[k]=v
    return out


def read(path, limit=16*MIB):
    path=Path(path);ordinary(path)
    need(path.is_file() and path.stat().st_size<=limit,"Bounded ordinary JSON")
    return json.loads(path.read_text("utf-8"),object_pairs_hook=unique)


def ordinary(path):
    p=Path(path)
    need(not p.is_symlink() and not (hasattr(p,"is_junction") and p.is_junction()),"No linked source/evidence path")
    return p


def parts(name):
    need(type(name)is str and name and not any(c in name for c in ("\\",":","\0")),"Portable relative source path")
    p=name.split("/")
    need(all(s and s not in (".","..") and s==s.rstrip(" .") for s in p),"No source traversal or alias")
    return p


def catalog():
    need(digest(CATALOG)==CATALOG_SHA256,"Exact external n5 source catalog pin")
    d=read(CATALOG)
    need(d["schema"]=="PINNED_N5_REMAINING_ARITHMETIC_CATALOG_V1" and d["census"]==dict(
        jobs=326,initial=12,resources=15,resource_panels=1200,count_forests=295,count_roots=1770,
        count_nodes=148586,count_leaves=75178),"Complete selected n5 census")
    need(len(d["jobs"])==326 and len({r["job_id"]for r in d["jobs"]})==326,"Unique full job selection")
    need(d["supervisory_snapshot_sha256"]==SNAPSHOT_SHA256,"Exact original supervisory snapshot")
    return d


def jobs(): return catalog()["jobs"]


def job(job_id):
    found=[r for r in jobs() if r["job_id"]==job_id]
    need(len(found)==1,"One catalog-selected n5 job, never an arbitrary script")
    return found[0]


def verify_vendor():
    need(digest(VENDOR/"SNAPSHOT.json")==SNAPSHOT_SHA256,"Exact immutable supervisory source inventory")
    d=read(VENDOR/"SNAPSHOT.json")
    expected={r["path"]:r for r in d["files"]}
    actual=set()
    for p in VENDOR.rglob("*"):
        ordinary(p)
        if p.is_file():actual.add(p.relative_to(VENDOR).as_posix())
    need(actual==set(expected)|{"SNAPSHOT.json"},"No unbound supervisory import/helper")
    for name,r in expected.items():
        p=VENDOR.joinpath(*parts(name))
        need(p.stat().st_size==r["bytes"] and digest(p)==r["sha256"],"Unchanged supervisory source: "+name)
    return expected


def zip_members(z):
    rows=z.infolist();need(0<len(rows)<=100000,"Bounded source ZIP inventory")
    names=set();folded=set();total=0
    for row in rows:
        name=row.filename[:-1]if row.is_dir()else row.filename
        parts(name);mode=row.external_attr>>16
        need(name not in names and name.casefold() not in folded and not row.flag_bits&1
             and not stat.S_ISLNK(mode) and stat.S_IFMT(mode)in(0,stat.S_IFREG,stat.S_IFDIR),
             "Unique nonlinked ordinary source ZIP member")
        need(0<=row.file_size<=256*MIB,"Bounded individual source ZIP member")
        names.add(name);folded.add(name.casefold());total+=row.file_size
    need(total<=2*1024**3,"Bounded complete source ZIP expansion")


def obtain_archive(archives, *, download=True, progress=lambda *a,**k:None):
    asset=catalog()["archive"];directory=ordinary(archives);directory.mkdir(parents=True,exist_ok=True)
    path=ordinary(directory/asset["name"])
    if not path.exists():
        need(download,"Pinned n5 source ZIP is absent")
        temporary=path.with_name(path.name+".partial-"+uuid.uuid4().hex[:8]);used=0;last=time.monotonic()
        try:
            progress("n5_source_download_started",expected_bytes=asset["bytes"])
            with urllib.request.urlopen(ASSET_URL,timeout=60)as src,temporary.open("xb")as dst:
                while block:=src.read(MIB):
                    used+=len(block);need(used<=asset["bytes"],"Exact source download size bound");dst.write(block)
                    if used%(16*MIB)==0 or time.monotonic()-last>=5:
                        progress("n5_source_download",bytes=used,expected_bytes=asset["bytes"]);last=time.monotonic()
            need(used==asset["bytes"]and digest(temporary)==asset["sha256"],"Exact downloaded source ZIP")
            temporary.replace(path)
        finally:
            if temporary.exists():temporary.unlink()
    need(path.is_file()and path.stat().st_size==asset["bytes"]and digest(path)==asset["sha256"],"Exact pinned n5 source ZIP")
    progress("n5_source_archive_verified",bytes=asset["bytes"],sha256=asset["sha256"])
    return path


def prepare_cache(archive, destination, *, progress=lambda *a,**k:None):
    d=catalog();asset=d["archive"];archive=ordinary(archive)
    need(archive.stat().st_size==asset["bytes"]and digest(archive)==asset["sha256"],"Pinned source ZIP before extraction")
    root=ordinary(destination);root.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive)as z:
        zip_members(z)
        for i,(name,row)in enumerate(d["source_cache_files"].items()):
            output=root.joinpath(*parts(name))
            for p in [output,*output.parents]:
                if p==root.parent:break
                ordinary(p)
            if output.exists():need(output.is_file()and digest(output)==row["sha256"],"Existing source cache bytes unchanged")
            else:
                info=z.getinfo(asset["prefix"]+name)
                need(info.file_size==row["bytes"],"Selected source member size")
                output.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info)as src,output.open("xb")as dst:shutil.copyfileobj(src,dst,MIB)
                need(digest(output)==row["sha256"],"Selected source member SHA")
            if i%1000==0:progress("n5_source_cache",completed=i,total=len(d["source_cache_files"]),arithmetic_computed=False)
    verify_cache(root,d)
    return root.resolve()


def verify_cache(root, d=None):
    d=catalog()if d is None else d;root=ordinary(root);actual=set()
    for p in root.rglob("*"):
        ordinary(p)
        if p.is_file():actual.add(p.relative_to(root).as_posix())
    need(actual==set(d["source_cache_files"]),"Exact selected source-cache inventory")
    for name,row in d["source_cache_files"].items():
        p=root.joinpath(*parts(name));need(p.stat().st_size==row["bytes"]and digest(p)==row["sha256"],"Sealed source cache: "+name)


def expected_inputs(row):
    expected={}
    for name,r in verify_vendor().items():
        new="ORIGINAL_RUN_REPRODUCTION.py"if name=="run_reproduction.py"else name
        expected["runtime/"+new]=r["sha256"]
    expected["runtime/run_reproduction.py"]=digest(ROOT/"be_replay/n5_remaining_bridge.py")
    if row["kind"]=="count":
        expected.update({"runtime/work/count-candidate/capsule/"+name:pin for name,pin in row["source_files"].items()})
    if row["kind"]=="support":
        for protocol in row["protocols"]:
            expected.update({"support-inputs/"+name.replace("\\","/"):pin
                             for name,pin in protocol["source_files_sha256"].items()})
    return expected


def prepare_job(task, row, cache):
    need(row==job(row["job_id"]),"Exact source-selected job")
    task=ordinary(task);need(not task.exists(),"Fresh exclusive n5 arithmetic stage")
    task.mkdir(parents=True);runtime=task/"runtime"
    for name in verify_vendor():
        dest=runtime/("ORIGINAL_RUN_REPRODUCTION.py"if name=="run_reproduction.py"else name)
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(VENDOR/name,dest)
    shutil.copyfile(ROOT/"be_replay/n5_remaining_bridge.py",runtime/"run_reproduction.py")
    if row["kind"]=="support":
        for name,pin in expected_inputs(row).items():
            if not name.startswith("support-inputs/"):continue
            source=Path(cache)/name.removeprefix("support-inputs/")
            need(digest(source)==pin,"Exact retained support mathematical input byte")
            output=task/name;output.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,output)
    if row["kind"]=="count":
        capsule=runtime/"work/count-candidate/capsule";capsule.mkdir(parents=True)
        for name,pin in row["source_files"].items():
            source=Path(cache)/row["source_capsule"]/name
            need(digest(source)==pin,"Exact selected count input/candidate")
            shutil.copyfile(source,capsule/name)
    request=dict(schema="FRESH_N5_REMAINING_JOB_SOURCE_V1",job_id=row["job_id"],catalog_sha256=CATALOG_SHA256,
                 snapshot_sha256=SNAPSHOT_SHA256,original_task_root=str(task.resolve()),
                 resource_policy=RESOURCE_POLICY,
                 source_cache=str(Path(cache).resolve()),inputs=expected_inputs(row),
                 full_n5_verified=False,all_index_conclusion_verified=False)
    (task/"JOB_SOURCE.json").write_text(json.dumps(request,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    verify_job(task,row)
    return request


def verify_job(task,row=None):
    task=ordinary(task);request=read(task/"JOB_SOURCE.json");row=job(request["job_id"])if row is None else row
    need(row==job(row["job_id"])and request["job_id"]==row["job_id"]and
         request["schema"]=="FRESH_N5_REMAINING_JOB_SOURCE_V1"and request["catalog_sha256"]==CATALOG_SHA256
         and request["snapshot_sha256"]==SNAPSHOT_SHA256 and request["inputs"]==expected_inputs(row)
         and request["resource_policy"]==RESOURCE_POLICY
         and request["full_n5_verified"]is False and request["all_index_conclusion_verified"]is False,
         "Exact source epoch, selected job and non-global scope")
    expected=request["inputs"]
    native_sources=(row.get("source_selection",{}).get("source_files_sha256",{})
                    if row["kind"]in("initial","resource")else row.get("source_files_sha256",{}))
    worker={"owncaps":"c5_extension_worker.py","resource":"c5_resource_accept_port.py",
            "complement":"c5_complement_worker.py"}.get(row["kind"])
    for name,pin in expected.items():
        p=task.joinpath(*parts(name));ordinary(p);need(p.is_file()and digest(p)==pin,"Immutable job input: "+name)
    for p in task.rglob("*"):
        ordinary(p)
        if not p.is_file():continue
        name=p.relative_to(task).as_posix()
        if name in expected:continue
        need(name in("JOB_SOURCE.json","STAGE_OBSERVED.json","STAGE_COMPLETED.json","ERROR.txt")
             or name.startswith("execution/")or name.startswith("runtime/work/"),"No unbound stage-root artifact")
        need(p.suffix.lower()not in(".pyc",".pyo",".so",".pyd",".dll",".pth"),"No unbound executable import/bytecode proof input")
        if p.suffix==".py":
            tail=name.split("/")
            need(len(tail)>=4 and tail[:2]==["runtime","work"]
                 and re.fullmatch(r"[A-Za-z0-9-]+",tail[2]),"One original private arithmetic epoch")
            relative="/".join(tail[3:]);pin=native_sources.get(relative)
            if worker and relative==worker:
                pin=digest(VENDOR/"reproduction/all_indices"/worker)
            need(pin is not None and digest(p)==pin,"Exact source path/pin, no relocated unbound import helper")
    return request
