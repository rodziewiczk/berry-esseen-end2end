"""Source-only preparation for the explicit fresh finite7--9 CAPS epoch.

The original CAPS receipt is a template, never a fresh accepted input. No
original numerical module is imported by this adapter.
"""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import time
import urllib.request
import zipfile

from . import finite69_sources as base, finite69_metadata as metadata
from . import finite69_cap_epoch as epoch, finite69_parent_sources as parents

ROOT=base.ROOT
MIB=base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
CATALOG=ROOT/"proof/finite69_caps_sources.json"
CATALOG_SHA256="9fa49a947abce7060a9954b32afcc1e7256d596aeca01e1771e02420dfab321b"
EPOCH_SHA256="3d9bfeef746674d283e21ed36fdb10a4128ad8fddb1ef45d79f2b67d0e75ffed"
OWN="work/cutoff6_20261018/fourier/owncaps6_9_v1/"
AUDIT="work/cutoff6_20261018/audit/supported_fourier_readback_v1/"
RESOURCE="work/cutoff6_20261020/entry/resource7_9_accept_v2/"
CAPS=epoch.CAPS_PATH
SCHEMA="SEALED_FRESH_FINITE69_CAPS_STAGE_V1"
PLAN_EXTRA={epoch.OWN+"plan01/"+n for n in("metadata.json","stdout.txt","stderr.txt")}
OWN_OUTPUTS=set(epoch.DYNAMIC)|PLAN_EXTRA|{CAPS}


def dump(packet):return(json.dumps(packet,indent=2,sort_keys=True)+"\n").encode("utf-8")


def catalog():
    need(digest(CATALOG)==CATALOG_SHA256 and digest(epoch.__file__)==EPOCH_SHA256,
         "Exact externally pinned CAPS catalog and metadata adapter")
    d=read(CATALOG,limit=32*MIB)
    need(d["schema"]=="FRESH_FINITE69_CAPS_STATIC_SOURCE_CATALOG_V1"
         and len(d["source_files"])==770 and d["source_only"]is True
         and d["arithmetic_computed"]is False and d["cap_epoch_adapter_sha256"]==EPOCH_SHA256,
         "Complete770-file static source inventory, not accepted mathematics")
    return d


def resource_rows():
    ids=catalog()["resource_job_ids"]
    rows=[base.job(name)for name in ids]
    need(len(rows)==9 and all(r["kind"]=="resource"for r in rows),"Nine literal resource jobs")
    return rows


def obtain_assets(directory, *,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);result={}
    for a in catalog()["assets"]:
        name=a["name"];need(tuple(parts(name))==(name,),"Pinned asset basename")
        path=ordinary(directory/name)
        if not path.exists():
            pending=ordinary(path.with_suffix(".zip.pending"));received=0;at=0;last=time.monotonic()
            progress("finite69_caps_download_started",archive=name,total_bytes=a["bytes"])
            with urllib.request.urlopen(a["url"])as source,pending.open("wb")as target:
                while block:=source.read(MIB):
                    received+=len(block);need(received<=a["bytes"],"Pinned bounded archive download");target.write(block)
                    if received-at>=16*MIB or time.monotonic()-last>=5:
                        progress("finite69_caps_download",archive=name,bytes=received,total_bytes=a["bytes"])
                        at=received;last=time.monotonic()
            need(received==a["bytes"]and digest(pending)==a["sha256"],"Whole pinned source transport")
            pending.replace(path)
        need(path.is_file()and path.stat().st_size==a["bytes"]and digest(path)==a["sha256"],"Actual complete source archive SHA")
        result[name]=path.resolve();progress("finite69_caps_archive_verified",archive=name,bytes=a["bytes"],sha256=a["sha256"])
    return result


def prepare_cache(assets,output, *,progress=lambda *a,**k:None):
    d=catalog();output=ordinary(output);output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for a in d["assets"]:
            p=ordinary(assets[a["name"]]);need(p.stat().st_size==a["bytes"]and digest(p)==a["sha256"],"Whole exact source transport")
            z=zipfile.ZipFile(p);base.zip_index(z);opened[a["name"]]=z
        for i,(name,row)in enumerate(d["source_files"].items()):
            if "reconstruction"in row:continue
            p=output.joinpath(*parts(name));ordinary(p)
            if not p.exists():
                z=opened[row["archive"]];info=z.getinfo(row["member"])
                need(info.file_size==row["bytes"],"Exact selected member size")
                p.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info)as source,p.open("xb")as target:shutil.copyfileobj(source,target,MIB)
            need(p.is_file()and p.stat().st_size==row["bytes"]and digest(p)==row["sha256"],"Every selected unchanged static byte")
            if i%100==0:progress("finite69_caps_source_cache",files=i,total=770,arithmetic_computed=False)
        for name,row in d["source_files"].items():
            if "reconstruction"not in row:continue
            raw=metadata.reconstruct_prepared((output/row["source_prepared"]).read_bytes(),(output/row["candidate"]).read_bytes(),
                n=row["n"],band=row["band"],source_pins=row["source_pins"])
            p=output.joinpath(*parts(name));p.parent.mkdir(parents=True,exist_ok=True)
            if p.exists():need(p.read_bytes()==raw,"Existing exact original PREPARED")
            else:p.write_bytes(raw)
        base.verify_cache(output,d["source_files"])
    finally:
        for z in opened.values():z.close()
    return output.resolve()


def copy_inputs(cache,capsule,pins):
    for name,pin in pins.items():
        p=Path(cache).joinpath(*parts(name));need(digest(p)==pin,"Every selected original static input")
        q=Path(capsule).joinpath(*parts(name));q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)


def prepare_own(cache,task):
    task=ordinary(task);need(not task.exists(),"Exclusive fresh owncaps stage");task.mkdir(parents=True)
    d=catalog();old=read(Path(cache)/CAPS);pins={n:p for n,p in old["files_sha256"].items()if n not in epoch.DYNAMIC}
    pins.update(d["entry_sources"])
    # The old CAPS template is preserved outside its native fresh-output slot.
    need(CAPS not in pins and not(set(pins)&OWN_OUTPUTS),"No historical accepted output in the fresh owncaps tree")
    copy_inputs(cache,task/"capsule",pins)
    provenance=task/"provenance/ORIGINAL_CAPS.json";provenance.parent.mkdir();shutil.copyfile(Path(cache)/CAPS,provenance)
    request=dict(schema=SCHEMA,kind="owncaps",job_id="owncaps6_9",original_task_root=str(task.resolve()),
        catalog_sha256=CATALOG_SHA256,source_adapter_sha256=digest(__file__),static_inputs=pins,
        generated_inputs={},allowed_outputs=sorted(OWN_OUTPUTS),arithmetic_computed=False)
    (task/"SOURCES.json").write_bytes(dump(request));verify_job(task);return request


def verify_job(task):
    task=ordinary(task);r=read(task/"SOURCES.json");d=catalog()
    need(r["schema"]==SCHEMA and r["catalog_sha256"]==CATALOG_SHA256 and r["source_adapter_sha256"]==digest(__file__)
         and r["arithmetic_computed"]is False,"Exact source-only preparation epoch")
    if r["kind"]=="owncaps":
        old=read(task/"provenance/ORIGINAL_CAPS.json")
        need(digest(task/"provenance/ORIGINAL_CAPS.json")==epoch.ORIGINAL_CAPS_SHA,"Pinned old CAPS template only")
        pins={n:p for n,p in old["files_sha256"].items()if n not in epoch.DYNAMIC};pins.update(d["entry_sources"])
        need(r["job_id"]=="owncaps6_9"and r["static_inputs"]==pins and r["generated_inputs"]=={}
             and r["allowed_outputs"]==sorted(OWN_OUTPUTS),"Complete fixed owncaps static and output domains")
    else:
        need(r["kind"]=="resource"and r["job_id"]in d["resource_job_ids"],"One literal fresh resource epoch")
        row=base.job(r["job_id"])
        case=row["output"].split("/")[0];parent_path=row["reference"]["native_answer"]["initial_receipt"]
        changed=set(epoch.DYNAMIC)|{CAPS,parent_path}
        pins={name:pin for name,pin in row["source_files_sha256"].items()if name not in changed}
        additions={RESOURCE+"FRESH_REPLAY.py",RESOURCE+case+"/FRESH_PREPARED.json",RESOURCE+case+"/FRESH_SOURCE_RESULT.json"}
        need(r["static_inputs"]==pins and r["added_inputs"]==sorted(additions)
             and set(r["generated_inputs"])==(set(row["source_files_sha256"])&changed)|additions,
             "Exact fixed static/generated partition; no numerical source may be promoted to mutable input")
        need(r["allowed_outputs"]==[base.output_relative(row)],"Only the selected fresh resource receipt may appear")
    names=set()
    for p in(task/"capsule").rglob("*"):
        ordinary(p)
        if p.is_file():names.add(p.relative_to(task/"capsule").as_posix())
    inputs=r["static_inputs"]|r["generated_inputs"]
    need(set(inputs)<=names<=set(inputs)|set(r["allowed_outputs"]),"Exact sealed source/input tree, no unbound import or output")
    for name,pin in inputs.items():need(digest(task/"capsule"/name)==pin,"Actual unchanged source or explicitly derived input")
    return r


def derived_resource(cache,row,initial_task,own_task, *,old_caps=None):
    """Deterministic metadata only; execution evidence is checked by the caller."""
    from . import finite69_parent_evidence as pe
    initial=pe.validate_completed(initial_task)
    receipt=Path(initial_task)/initial["summary"]["receipt_relative"]
    old=read(Path(cache)/row["directory"]/row["output"].split("/")[0]/"PREPARED.json")
    # The case lives directly below resource7_9_accept_v2; preserve its original
    # source candidate, nested timings and all100 original numeric rows.
    case=row["output"].split("/")[0];n=int(case.split("_")[0][1:]);band=case.split("_")[1]
    need(initial["job_id"]==f"n{n}.initial.{band}","Same literal fresh INITIAL parent")
    own_capsule=Path(own_task)/"capsule";fresh=own_capsule/CAPS;caps=read(fresh)
    actual={name:digest(own_capsule/name)for name in caps["files_sha256"]}|{CAPS:digest(fresh)}
    directory=Path(cache)/RESOURCE/case
    derived=epoch.derive_resource_epoch((Path(cache)/RESOURCE/"replay.py").read_bytes(),
        (directory/"PREPARED.json").read_bytes(),(directory/"SOURCE_RESULT.json").read_bytes(),
        receipt.read_bytes(),(Path(cache)/CAPS if old_caps is None else Path(old_caps)).read_bytes(),fresh.read_bytes(),n=n,band=band,
        source_pins=catalog()["original_source_pins"],fresh_files_sha256=actual)
    return derived,old["initial_receipt"],receipt,caps


def prepare_resource(cache,task,row,initial_task,own_task):
    from . import finite69_caps_evidence as evidence
    evidence.validate_completed(own_task)
    derived,parent_path,parent_receipt,caps=derived_resource(cache,row,initial_task,own_task)
    task=ordinary(task);need(not task.exists(),"Exclusive fresh resource stage");task.mkdir(parents=True)
    # Export the complete upstream evidence bytes, rather than importing an
    # unattested PASS or only its digest. Validators can relocate this tree.
    for name,source in(("initial",initial_task),("owncaps",own_task)):
        shutil.copytree(source,task/"inputs"/name,symlinks=False)
    changed=set(epoch.DYNAMIC)|{CAPS,parent_path}
    pins={name:pin for name,pin in row["source_files_sha256"].items()if name not in changed}
    copy_inputs(cache,task/"capsule",pins)
    generated={}
    own_capsule=Path(own_task)/"capsule"
    for name in set(caps["files_sha256"])|{CAPS}:
        if name in pins:
            need(digest(own_capsule/name)==pins[name],"Upstream static source identity");continue
        p=task/"capsule"/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(own_capsule/name,p);generated[name]=digest(p)
    p=task/"capsule"/parent_path;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(parent_receipt,p);generated[parent_path]=digest(p)
    case=row["output"].split("/")[0]
    additions={RESOURCE+"FRESH_REPLAY.py":derived["replay_bytes"],
        RESOURCE+case+"/FRESH_PREPARED.json":derived["fresh_prepared_bytes"],
        RESOURCE+case+"/FRESH_SOURCE_RESULT.json":derived["fresh_source_result_bytes"]}
    for name,raw in additions.items():
        p=task/"capsule"/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);generated[name]=digest(p)
    prov=task/"provenance";prov.mkdir();shutil.copyfile(Path(cache)/CAPS,prov/"ORIGINAL_CAPS.json")
    (task/"DERIVATION.json").write_bytes(dump({k:v for k,v in derived.items()if not k.endswith("_bytes")}))
    request=dict(schema=SCHEMA,kind="resource",job_id=row["job_id"],original_task_root=str(task.resolve()),
        catalog_sha256=CATALOG_SHA256,source_adapter_sha256=digest(__file__),static_inputs=pins,
        generated_inputs=generated,added_inputs=sorted(additions),allowed_outputs=[base.output_relative(row)],arithmetic_computed=False)
    (task/"SOURCES.json").write_bytes(dump(request));verify_job(task);return request
