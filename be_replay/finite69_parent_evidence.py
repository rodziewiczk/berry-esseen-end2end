"""Revalidate full finite6--9 parent replay evidence without importing a kernel.

These are new BASIC execution receipts for unchanged original acceptors. A
completed stage proves no INITIAL/resource acquisition or finite-index theorem.
"""
from __future__ import annotations
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import re

from . import finite69_parent_sources as src

OBSERVED="OBSERVED_CONDITIONAL_FINITE69_PARENT_V1"
COMPLETED="COMPLETED_CONDITIONAL_FINITE69_PARENT_V1"
SCOPE="UNCHANGED_FULL_SELECTED_FINITE69_PARENT_BASIC_V1"
CPU_SECONDS=43200
WALL_SECONDS=54000
MEMORY_BYTES=2048*src.MIB
FLAGS=("native_arithmetic_accepted","parent_acquisitions_verified",
       "fresh_parent_fact_joins_verified","full_finite69_verified","all_index_conclusion_verified")

# Exact previously published runtime. Its completed receipts remain byte-for-byte
# valid after the routing-only underscore repair. No mathematical source,
# source-preparer, catalog, guard or validation rule is migrated or wildcarded.
PRE_SLUG_FIX_IMPLEMENTATION={
    "finite69_parents.py":"e6ad5f17b99b831a0e0d0ac52b794086da7dfcf36ff12c12ce6e0e542ffc7a57",
    "finite69_parent_evidence.py":"380c5496a5868ef3a67687e29f0b15e8d8888a4c1b9097351999da549e5b40fd",
    "finite69_parent_sources.py":"4328f3df13956dfd5727b18f11c87ad9522cf6c491482b7aa467ac7982875b91",
    "finite69_metadata.py":"594536b187e2fa8d51bb06d47a56f9b165a8da4a197e2a8933d3aa8dd48e9a3c",
    "finite69_sources.py":"67e9e2bb1009d8a2c03c3b4d42480c7b06254998d70dd3f8c6bfbb63df2d3791",
    "n5_remaining_sources.py":"17f8d9b3bcdce510574901be83684a630d54cc8d2f6251856b7737bbd85aaaab",
    "linux_supervisor.py":"61e71dd4a9653de2bbbee8c54928a1f5c5bffd0bf083dd324851716c3a1eaea2",
    "colab_batch.py":"136bc2bb9b25cb8cd36118041bf593821f3cbdea5debee82b27ccb7626c0d1e6",
    "catalog_sha256":"9eef9a7c11abaa6a239fbcd0890acc32e420ac56bca1a09043e4a87187c244bf",
    "base_catalog_sha256":"2a0575f59f9d6c8e95c53f68767b1cbae28b1ed2f5cd72c27a240b50d1367232",
}


def implementation():
    names=("finite69_parents.py","finite69_parent_evidence.py","finite69_parent_sources.py","finite69_metadata.py","finite69_sources.py",
           "n5_remaining_sources.py","linux_supervisor.py","colab_batch.py")
    return {name:src.digest(src.ROOT/"be_replay"/name)for name in names}|{
        "catalog_sha256":src.CATALOG_SHA256,"base_catalog_sha256":src.catalog()["base_catalog_sha256"]}


def implementation_allowed(recorded):
    return same(recorded,implementation())or same(recorded,PRE_SLUG_FIX_IMPLEMENTATION)


def mapped(task,value,original):
    src.need(type(value)is str and type(original)is str,"Recorded original path strings")
    cls=PureWindowsPath if re.match(r"^[A-Za-z]:",original)else PurePosixPath
    p,root=cls(value),cls(original)
    src.need(p.is_absolute()and root.is_absolute(),"One absolute originating execution root")
    try:relative=p.relative_to(root)
    except ValueError:raise ValueError("Capture leaves its explicit originating task root")
    src.need(relative.parts and all(x not in(".","..")for x in relative.parts),"Contained evidence path")
    result=Path(task).joinpath(*relative.parts)
    for parent in(result,*result.parents):
        if parent==Path(task).parent:break
        src.ordinary(parent)
    return result


def command(request,row,python):
    original=request["original_task_root"]
    cls=PureWindowsPath if re.match(r"^[A-Za-z]:",original)else PurePosixPath
    return [python,"-B","-S",str(cls(original)/"capsule"/row["directory"]/"replay.py"),*row["arguments"]]


def inventory(task):
    result={}
    for p in sorted(Path(task).rglob("*")):
        src.ordinary(p)
        if p.is_file()and p.relative_to(task).as_posix()not in("STAGE_OBSERVED.json","STAGE_COMPLETED.json"):
            result[p.relative_to(task).as_posix()]=dict(bytes=p.stat().st_size,sha256=src.digest(p))
    return result


def same(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    return a==b


def summarize(task,row,stdout,observed,original):
    path=Path(task)/"capsule"/src.output_relative(row);receipt=src.read(path,limit=64*src.MIB)
    expected=src.expected_native(task,row)
    src.need(type(receipt)is dict and set(receipt)==set(expected)|{"seconds"},"Whole native parent receipt schema")
    src.need(same({k:v for k,v in receipt.items()if k!="seconds"},expected),"Every native numeric result, profile, control and source commitment")
    src.need(type(receipt["seconds"])in(int,float)and math.isfinite(receipt["seconds"])and receipt["seconds"]>=0,
             "Finite ordinary fresh elapsed metadata")
    lines=[line for line in stdout.splitlines()if line.strip()]
    src.need(lines and lines[-1].split()[0]==receipt["status"],"Actual original successful terminal status")
    captures=observed["checkpoints"]
    src.need(type(captures)is list and len(captures)==1,"Exactly one stopped-supervisor native output capture")
    capture=captures[0]
    src.need(set(capture)=={"source_path","exists","trusted_certificate","path","bytes","sha256"}
             and capture["exists"]is True and capture["trusted_certificate"]is False
             and mapped(task,capture["source_path"],original)==path,"Actual captured fresh output identity")
    copied=mapped(task,capture["path"],original)
    src.need(copied==Path(task)/"execution/checkpoints"/row["output"]and copied.is_file()
             and type(capture["bytes"])is int and capture["bytes"]==path.stat().st_size==copied.stat().st_size
             and capture["sha256"]==src.digest(path)==src.digest(copied),"Whole stopped native receipt bytes and SHA")
    return dict(job_id=row["job_id"],kind=row["kind"],lane=row["lane"],n=receipt["n"],band=receipt["band"],
        index=receipt.get("index"),status=receipt["status"],receipt_relative="capsule/"+src.output_relative(row),
        receipt_sha256=src.digest(path),source_files_sha256=receipt["files_sha256"],native_controls=receipt["negative_controls"],
        numerical_metadata={k:v for k,v in expected.items()if k not in("files_sha256","negative_controls","result","scope")},
        conditional_receipt_inputs=row["conditional_receipt_inputs"],direct_fresh_dependencies=row["direct_fresh_dependencies"],
        fresh_parent_fact_joins_verified=False,parent_acquisitions_verified=False,full_finite69_verified=False,all_index_conclusion_verified=False)


def validate_run(task,row,report):
    task=Path(task);request=src.verify_job(task,row);original=request["original_task_root"]
    src.need(report["schema"]==OBSERVED and report["scope"]==SCOPE and report["job_id"]==row["job_id"]
             and implementation_allowed(report["implementation"])and report["original_task_root"]==original
             and report["conditional_arithmetic_completed"]is False and all(report[f]is False for f in FLAGS),
             "Exact implementation and observed false-to-completed transition")
    observed=report["observed"]
    src.need(observed.get("status")=="completed"and type(observed.get("returncode"))is int and observed["returncode"]==0
             and observed.get("reason")is None and observed.get("proof_accepted")is False
             and observed.get("mode")=="untrusted_search"and type(observed.get("sample_count"))is int
             and observed["sample_count"]>0,"Actual successful BASIC execution")
    src.need(src.read(task/"execution/supervisor-result.json")==observed,"Actual stopped supervisor result")
    launch=src.read(task/"execution/launch.json")
    cwd=task/"capsule"/row["directory"]
    src.need(launch["argv"]==command(request,row,report["python_executable"])
             and mapped(task,launch["cwd"],original)==cwd and mapped(task,launch["output_dir"],original)==task/"execution"
             and launch["mode"]=="untrusted_search"and launch["sample_seconds"]==.2 and launch["heartbeat_seconds"]==20
             and len(launch["checkpoint_paths"])==1 and mapped(task,launch["checkpoint_paths"][0],original)==task/"capsule"/src.output_relative(row),"Actual original acceptor launch and capture context")
    for key,value in(("cpu_seconds",CPU_SECONDS),("wall_seconds",WALL_SECONDS),("memory_bytes",MEMORY_BYTES)):
        # The supervisor normalizes wall duration to float, while CPU and byte
        # ceilings remain exact integers. A bool is never a valid duration.
        allowed=(int,float)if key=="wall_seconds"else(int,)
        src.need(type(report[key])is int and report[key]==value and type(launch[key])in allowed and launch[key]==value,
                 "Exact documented BASIC execution budget")
    src.need(launch["disk_bytes"]==512*src.MIB and launch["log_bytes"]==16*src.MIB,"Bounded original output capture")
    src.need(observed["guard_scope"]==dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",proof_acceptance=False,
        external_wall_seconds=WALL_SECONDS,per_process_RLIMIT_AS_bytes=MEMORY_BYTES,
        per_process_RLIMIT_CPU_seconds=CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,
        sampled_group_RSS_limit_bytes=MEMORY_BYTES,sampled_group_CPU_limit_seconds=CPU_SECONDS,
        sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False),"Honest exact BASIC guard contract")
    paths={}
    for kind in("stdout","stderr"):
        p=mapped(task,observed[kind+"_path"],original)
        src.need(p==task/"execution"/(kind+".txt")and p.is_file()and p.stat().st_size<=16*src.MIB
                 and src.digest(p)==observed[kind+"_sha256"],"Actual supervisor-bound capture SHA")
        paths[kind]=p
    src.need(paths["stderr"].stat().st_size==0,"Empty successful original stderr")
    return summarize(task,row,paths["stdout"].read_text("utf-8"),observed,original)


def validate_completed(task, *,original_task_root=None):
    task=Path(task);request=src.verify_job(task);row=src.job(request["job_id"])
    src.need(original_task_root is None or str(original_task_root)==request["original_task_root"],"One explicit original root")
    observed=src.read(task/"STAGE_OBSERVED.json");complete=src.read(task/"STAGE_COMPLETED.json")
    summary=validate_run(task,row,observed)
    src.need(complete["schema"]==COMPLETED and complete["scope"]==SCOPE and complete["job_id"]==row["job_id"]
             and implementation_allowed(complete["implementation"])and same(complete["implementation"],observed["implementation"])
             and complete["observed_sha256"]==src.digest(task/"STAGE_OBSERVED.json")
             and complete["conditional_arithmetic_completed"]is True and complete["summary"]==summary
             and complete["artifacts"]==inventory(task)and all(complete[f]is False for f in FLAGS),
             "Full source/candidate/capture/receipt inventory, exact completed transition")
    return dict(schema="REVALIDATED_CONDITIONAL_FINITE69_PARENT_V1",job_id=row["job_id"],lane=row["lane"],
                summary=summary,catalog_sha256=src.CATALOG_SHA256,stage_result_sha256=src.digest(task/"STAGE_COMPLETED.json"),
                source_manifest_sha256=src.digest(task/"SOURCES.json"),original_task_root=request["original_task_root"],
                conditional_arithmetic_completed=True,**{f:False for f in FLAGS})
