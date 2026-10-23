"""Fixed parent source preparation; reconstructed transport is not acceptance."""
from __future__ import annotations
import ast
import copy
from fractions import Fraction
import json
from pathlib import Path
import shutil
import zipfile

from . import finite69_sources as base, finite69_metadata as metadata

ROOT=base.ROOT
MIB=base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
obtain_assets=base.obtain_assets
CATALOG=ROOT/"proof/finite69_parent_sources.json"
CATALOG_SHA256="9eef9a7c11abaa6a239fbcd0890acc32e420ac56bca1a09043e4a87187c244bf"
SCHEMA="SEALED_CONDITIONAL_FINITE69_PARENT_INPUTS_V1"


def catalog():
    need(digest(CATALOG)==CATALOG_SHA256,"Exact isolated fixed parent catalog")
    d=read(CATALOG,limit=32*MIB)
    need(d["schema"]=="FIXED_FINITE69_PARENT_SOURCE_CATALOG_V1"and d["base_catalog_sha256"]==base.CATALOG_SHA256
         and d["metadata_adapter_sha256"]==digest(metadata.__file__)and len(d["jobs"])==50
         and d["arithmetic_computed"]is False and d["parent_acquisitions_verified"]is False,"Exact source-only parent epoch")
    return d


def jobs(lane):
    need(lane in("n6","initial7_9"),"One fixed complete selected parent lane")
    rows=[r for r in catalog()["jobs"]if r["lane"]==lane]
    need(len(rows)==(41 if lane=="n6"else 9),"Every selected native parent action")
    return rows


def job(job_id):
    rows=[r for r in catalog()["jobs"]if r["job_id"]==job_id]
    need(len(rows)==1,"One fixed native parent job")
    return rows[0]


def source_files(lane):
    d=catalog();names={name for row in jobs(lane)for name in row["source_files_sha256"]}
    return {name:d["source_files"][name]for name in sorted(names)}


def prepare_cache(assets,output,lane, *,progress=lambda *a,**k:None):
    selected=source_files(lane);d=catalog();output=ordinary(output);output.mkdir(parents=True,exist_ok=True)
    opened={}
    try:
        for asset in d["assets"]:
            p=ordinary(assets[asset["name"]]);need(p.stat().st_size==asset["bytes"]and digest(p)==asset["sha256"],"Exact original parent transport")
            z=zipfile.ZipFile(p);base.zip_index(z);opened[asset["name"]]=z
        for i,(name,row)in enumerate(selected.items()):
            if "reconstruction"in row:continue
            dest=output.joinpath(*parts(name));ordinary(dest)
            if dest.exists():need(dest.is_file()and dest.stat().st_size==row["bytes"]and digest(dest)==row["sha256"],"Existing exact source-cache byte")
            else:
                z=opened[row["archive"]];info=z.getinfo(row["member"])
                need(info.file_size==row["bytes"],"Exact original parent source member size")
                dest.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info)as source,dest.open("xb")as target:shutil.copyfileobj(source,target,MIB)
                need(digest(dest)==row["sha256"],"Actual unchanged parent source/candidate")
            if i%200==0:progress("finite69_parent_source_cache",files=i,total=len(selected),arithmetic_computed=False)
        for name,row in selected.items():
            if "reconstruction"not in row:continue
            need(row["reconstruction"]=="ORIGINAL_POSIX_PREPARED_V1"and row["metadata_adapter_sha256"]==digest(metadata.__file__),"Exact original preparation-only reconstruction")
            raw=metadata.reconstruct_prepared((output/row["source_prepared"]).read_bytes(),(output/row["candidate"]).read_bytes(),
                n=row["n"],band=row["band"],source_pins=row["source_pins"])
            p=output.joinpath(*parts(name));ordinary(p);p.parent.mkdir(parents=True,exist_ok=True)
            if p.exists():need(p.read_bytes()==raw,"Existing externally pinned original PREPARED")
            else:p.write_bytes(raw)
            need(p.stat().st_size==row["bytes"]and digest(p)==row["sha256"],"Reconstructed bytes equal original external PREPARED pin")
        base.verify_cache(output,selected)
    finally:
        for z in opened.values():z.close()
    return output.resolve()


def output_relative(row):return row["directory"]+"/"+row["output"]


def prepare_job(job_id,cache,task):
    row=job(job_id);task=ordinary(task);need(not task.exists(),"Fresh exclusive parent stage")
    task.mkdir(parents=True);pins=row["source_files_sha256"]
    for name,pin in pins.items():
        source=Path(cache).joinpath(*parts(name));need(digest(source)==pin,"Every unchanged selected parent input")
        target=task/"capsule"/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    need(not(task/"capsule"/output_relative(row)).exists(),"Own historical acceptance is not copied")
    request=dict(schema=SCHEMA,job_id=job_id,lane=row["lane"],original_task_root=str(task.resolve()),
        catalog_sha256=CATALOG_SHA256,source_adapter_sha256=digest(__file__),source_files_sha256=pins,
        conditional_receipt_inputs=row["conditional_receipt_inputs"],arithmetic_computed=False,
        parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    (task/"SOURCES.json").write_bytes((json.dumps(request,indent=2,sort_keys=True)+"\n").encode())
    verify_job(task,row);return request


def verify_job(task,row=None):
    task=ordinary(task);r=read(task/"SOURCES.json");row=job(r["job_id"])if row is None else row
    need(row==job(row["job_id"])and r["schema"]==SCHEMA and r["job_id"]==row["job_id"]and r["lane"]==row["lane"]
         and r["catalog_sha256"]==CATALOG_SHA256 and r["source_adapter_sha256"]==digest(__file__)
         and r["source_files_sha256"]==row["source_files_sha256"]and r["conditional_receipt_inputs"]==row["conditional_receipt_inputs"]
         and r["arithmetic_computed"]is False and r["parent_acquisitions_verified"]is False and r["all_index_conclusion_verified"]is False,
         "Exact sealed parent source epoch, original receipts remain conditional inputs")
    names=set()
    for p in(task/"capsule").rglob("*"):
        ordinary(p)
        if p.is_file():names.add(p.relative_to(task/"capsule").as_posix())
    need(set(r["source_files_sha256"])<=names<=set(r["source_files_sha256"])|{output_relative(row)},"Exact parent source tree and one fresh output")
    for name,pin in r["source_files_sha256"].items():need(digest(task/"capsule"/name)==pin,"No changed parent source/input")
    return r


def expected_native(task,row):
    """Expected result metadata from candidates; never a mathematical replay."""
    old=row["reference"]["native_answer"]
    if old is not None:
        result=copy.deepcopy(old);result.pop("seconds")
        result["files_sha256"]={key.replace("\\","/"):pin for key,pin in result["files_sha256"].items()}
        need(result["files_sha256"]==row["source_files_sha256"],"Exact complete original parent result source graph")
        return result
    need(row["lane"]=="initial7_9"and row["kind"]=="initial","Only missing timed INITIAL metadata is reconstructed")
    case=row["output"].split("/")[0];directory=Path(task)/"capsule"/row["directory"]
    candidate=read(directory/case/"INPUT.json",limit=64*MIB);prepared=read(directory/case/"PREPARED.json")
    n,band=candidate["n"],candidate["band"];final=candidate["stages"][-1]["cover"]
    need(type(n)is int and n in(7,8,9)and case==f"n{n}_{band}"and len(candidate["stages"])==9,
         "Literal complete original INITIAL candidate")
    tree=ast.parse((directory/"replay.py").read_bytes());values=[node.value for node in tree.body if isinstance(node,ast.Assign)
        and any(isinstance(target,ast.Name)and target.id=="result"for target in node.targets)]
    need(len(values)==1 and isinstance(values[0],ast.Call),"One original native result schema")
    literals={key.arg:ast.literal_eval(key.value)for key in values[0].keywords if key.arg in("status","scope")}
    return dict(**literals,n=n,band=band,rho_interval=[candidate["profile"]["invariants"]["rho_lo"],candidate["profile"]["invariants"]["rho"]],
        profile=candidate["profile"],numerical_premises=dict(predecessor_theorem="sharp_CE_minimal_counterexample",contact_error="0",
            owncap=str(Fraction(candidate["assumed_owncap"])),HIGH=str(Fraction(candidate["assumed_HIGH"]))),
        stages=9,total_cells_per_stage=2592,final_active=final["active"],final_gap_active=final["gap_active"],
        final_raw=candidate["final_invariants"]["raw"],final_D=candidate["final_invariants"]["D"],panels=100,
        signed_support_rows=len(candidate["signed_support_rows"]),negative_controls=row["native_controls"],
        input_sha256=prepared["input_sha256"],files_sha256=row["source_files_sha256"])
