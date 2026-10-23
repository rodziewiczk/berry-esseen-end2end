"""Source/JSON preparation for the fixed finite6--9 replay catalog.

No original mathematical module is imported or evaluated. Missing byte-bound
inputs are errors; neither an old PASS nor an unlocated graph reference is
substituted for a source file.
"""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import stat
import time
import urllib.request
import zipfile
from .n5_remaining_sources import digest,read,unique,parts,ordinary,need,MIB

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"proof/finite69_sources_catalog.json"
# The complete selected COUNT inputs are available. Parent rows separately
# preserve explicit missing-reference obligations; they are not runnable here.
CATALOG_SHA256="2a0575f59f9d6c8e95c53f68767b1cbae28b1ed2f5cd72c27a240b50d1367232"
VENDOR=ROOT/"vendor/finite69_snapshot_v1"
RELEASE="https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/download/cutoff5-sources-2026-10-20/"
SCHEMA="FINITE69_EXACT_JOB_INPUTS_V1"


def catalog():
    need(digest(CATALOG)==CATALOG_SHA256,"Exact externally pinned finite69 catalog")
    d=read(CATALOG,limit=32*MIB)
    need(d["schema"]=="FINITE69_SELECTED_SOURCE_CATALOG_V1"and d["census"]==
         dict(forests=284,roots=2362,nodes=511816,leaves=257089),"Every selected finite69 count forest")
    need(d["arithmetic_computed"]is False and d["full_finite69_verified"]is False,"Catalog is source selection only")
    return d


def jobs(kind=None):
    d=catalog();rows=d["jobs"]+d.get("parent_jobs",[])
    need(len({r["job_id"]for r in rows})==len(rows),"Unique complete selected native job identifiers")
    return [r for r in rows if kind is None or r["kind"]==kind]


def job(job_id):
    rows=[r for r in jobs()if r["job_id"]==job_id]
    need(len(rows)==1,"One fixed source-selected finite69 job")
    return rows[0]


def verify_vendor():
    d=catalog();path=VENDOR/"SNAPSHOT.json"
    need(digest(path)==d["snapshot_sha256"],"Exact frozen finite source-selector snapshot")
    manifest=read(path);expected={r["path"]:r for r in manifest["files"]}
    actual=set()
    for p in VENDOR.rglob("*"):
        ordinary(p)
        if p.is_file():actual.add(p.relative_to(VENDOR).as_posix())
    need(actual==set(expected)|{"SNAPSHOT.json"},"No unbound frozen finite helper")
    for name,row in expected.items():
        p=VENDOR.joinpath(*parts(name))
        need(p.stat().st_size==row["bytes"]and digest(p)==row["sha256"],"Every frozen source-selector byte")
    return expected


def zip_index(z):
    result={};folded=set();total=0
    need(len(z.infolist())<=200000,"Bounded source archive directory")
    for row in z.infolist():
        name=row.filename[:-1]if row.is_dir()else row.filename;parts(name)
        mode=row.external_attr>>16
        need(row.filename not in result and row.filename.casefold()not in folded and not row.flag_bits&1
             and not stat.S_ISLNK(mode)and stat.S_IFMT(mode)in(0,stat.S_IFREG,stat.S_IFDIR)
             and 0<=row.file_size<=256*MIB,"Unique ordinary nonlinked bounded source archive member")
        result[row.filename]=row;folded.add(row.filename.casefold());total+=row.file_size
    need(total<=8*1024*MIB,"Bounded total expanded source transport")
    return result


def obtain_assets(directory, *,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);result={}
    for asset in catalog()["assets"]:
        name=asset["name"];need(tuple(parts(name))==(name,),"Fixed archive basename")
        path=ordinary(directory/name)
        if not path.exists():
            pending=ordinary(path.with_suffix(path.suffix+".pending"));received=0;last=time.monotonic();block_at=0
            progress("finite69_source_download_started",archive=name,total_bytes=asset["bytes"])
            with urllib.request.urlopen(asset.get("url",RELEASE+name))as source,pending.open("wb")as out:
                while block:=source.read(MIB):
                    received+=len(block);need(received<=asset["bytes"],"Bounded pinned finite source download");out.write(block)
                    now=time.monotonic()
                    if received-block_at>=16*MIB or now-last>=5:
                        progress("finite69_source_download",archive=name,bytes=received,total_bytes=asset["bytes"]);last=now;block_at=received
            need(received==asset["bytes"]and digest(pending)==asset["sha256"],"Actual complete source archive SHA")
            pending.replace(path)
        need(path.is_file()and path.stat().st_size==asset["bytes"]and digest(path)==asset["sha256"],"Exact immutable finite source archive")
        result[name]=path.resolve();progress("finite69_source_archive_verified",archive=name,bytes=asset["bytes"],sha256=asset["sha256"])
    return result


def selected_files(n):
    need(type(n)is int and n in(6,7,8,9),"Literal selected finite index")
    names={name for row in jobs("count")if row["selection"]["n"]==n for name in row["source_files_sha256"]}
    d=catalog();return {name:d["source_files"][name]for name in sorted(names)}


def prepare_cache(assets,output, *,n=None,progress=lambda *a,**k:None):
    d=catalog();output=ordinary(output);output.mkdir(parents=True,exist_ok=True);opened={}
    selected=d["source_files"]if n is None else selected_files(n)
    try:
        for asset in d["assets"]:
            path=ordinary(assets[asset["name"]])
            need(path.stat().st_size==asset["bytes"]and digest(path)==asset["sha256"],"Exact source preparation transport")
            z=zipfile.ZipFile(path);zip_index(z);opened[asset["name"]]=z
        for ordinal,(name,row)in enumerate(selected.items()):
            path=output.joinpath(*parts(name));ordinary(path)
            if path.exists():need(path.is_file()and path.stat().st_size==row["bytes"]and digest(path)==row["sha256"],"Existing exact finite source-cache byte")
            else:
                need("archive"in row,"A reconstructed parent input is outside the independently runnable COUNT lane")
                z=opened[row["archive"]];info=z.getinfo(row["member"])
                need(info.file_size==row["bytes"],"Exact selected native source member size")
                path.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info)as source,path.open("xb")as dest:shutil.copyfileobj(source,dest,MIB)
                need(digest(path)==row["sha256"],"Every actual selected finite source byte")
            if ordinal%1000==0:progress("finite69_source_cache",files=ordinal,total=len(selected),arithmetic_computed=False)
        verify_cache(output,selected)
    finally:
        for z in opened.values():z.close()
    return output.resolve()


def verify_cache(cache,selected=None):
    selected=catalog()["source_files"]if selected is None else selected;cache=ordinary(cache);found=set()
    for p in cache.rglob("*"):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(cache).as_posix())
    need(found==set(selected),"Exact complete selected finite source-cache inventory")
    for name,row in selected.items():
        path=cache.joinpath(*parts(name));need(path.stat().st_size==row["bytes"]and digest(path)==row["sha256"],"Sealed finite source cache")


def prepare_job(job_id,cache,output):
    row=job(job_id);need(row["kind"]=="count","Only the source-complete fixed COUNT lane is enabled")
    output=ordinary(output);need(not output.exists(),"Fresh exclusive finite job capsule");output.mkdir(parents=True)
    pins=row["source_files_sha256"];capsule=output/"capsule"
    for name,pin in pins.items():
        source=Path(cache).joinpath(*parts(name));need(digest(source)==pin,"Actual selected original finite input/candidate")
        dest=capsule.joinpath(*parts(name));dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
    manifest=dict(schema=SCHEMA,job_id=job_id,original_task_root=str(output.resolve()),catalog_sha256=CATALOG_SHA256,
        sources=pins,source_adapter_sha256=digest(__file__),arithmetic_computed=False,
        parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    (output/"SOURCES.json").write_bytes((json.dumps(manifest,sort_keys=True,indent=2)+"\n").encode())
    verify_job(output,row);return manifest


def output_relative(row):
    if row["kind"]=="count":return row["selection"]["capsule"]+"/"+row["selection"]["receipt_name"]
    return row["directory"]+"/"+row["output"]


def verify_job(task,row=None):
    task=ordinary(task);m=read(task/"SOURCES.json");row=job(m["job_id"])if row is None else row
    need(row==job(row["job_id"])and m["schema"]==SCHEMA and m["job_id"]==row["job_id"]
         and m["catalog_sha256"]==CATALOG_SHA256 and m["source_adapter_sha256"]==digest(__file__)
         and m["sources"]==row["source_files_sha256"]and m["arithmetic_computed"]is False
         and m["parent_acquisitions_verified"]is False and m["all_index_conclusion_verified"]is False,"Exact finite source epoch, no historical acceptance")
    allowed=set(m["sources"])|{output_relative(row)};actual=set()
    for p in(task/"capsule").rglob("*"):
        ordinary(p)
        if p.is_file():actual.add(p.relative_to(task/"capsule").as_posix())
    need(set(m["sources"])<=actual<=allowed,"Only sealed source inputs and the one actual fresh native output")
    for name,pin in m["sources"].items():
        need(digest(task/"capsule"/name)==pin,"Every actual finite source/candidate remains unchanged")
    return m
