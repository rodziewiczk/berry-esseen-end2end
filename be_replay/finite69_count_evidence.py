"""Revalidate full finite6--9 COUNT replay evidence without importing a kernel.

These are new BASIC execution receipts for unchanged original acceptors. A
completed stage proves no INITIAL/resource acquisition or finite-index theorem.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import re

from . import finite69_sources as src

OBSERVED="OBSERVED_CONDITIONAL_FINITE69_COUNT_V1"
COMPLETED="COMPLETED_CONDITIONAL_FINITE69_COUNT_V1"
SCOPE="UNCHANGED_FULL_SELECTED_FINITE69_COUNT_BASIC_V1"
CPU_SECONDS=43200
WALL_SECONDS=54000
MEMORY_BYTES=2048*src.MIB
FLAGS=("native_arithmetic_accepted","parent_acquisitions_verified",
       "fresh_parent_fact_joins_verified","full_finite69_verified","all_index_conclusion_verified")


def implementation():
    names=("finite69_counts.py","finite69_count_evidence.py","finite69_sources.py",
           "n5_remaining_sources.py","linux_supervisor.py","colab_batch.py")
    return {name:src.digest(src.ROOT/"be_replay"/name)for name in names}|{
        "catalog_sha256":src.CATALOG_SHA256,"snapshot_sha256":src.catalog()["snapshot_sha256"]}


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
    return [python,"-B","-S",str(cls(original)/"capsule"/row["selection"]["capsule"]/"count_protocol.py"),"accept"]


def inventory(task):
    result={}
    for p in sorted(Path(task).rglob("*")):
        src.ordinary(p)
        if p.is_file()and p.relative_to(task).as_posix()not in("STAGE_OBSERVED.json","STAGE_COMPLETED.json"):
            result[p.relative_to(task).as_posix()]=dict(bytes=p.stat().st_size,sha256=src.digest(p))
    return result


def terminal(text):
    decoder=json.JSONDecoder(object_pairs_hook=src.unique)
    for pos in[0]+[m.end()for m in re.finditer("\n",text)]:
        if not text[pos:].startswith("{"):continue
        try:packet,end=decoder.raw_decode(text,pos)
        except ValueError:continue
        if not text[end:].strip():return packet
    raise ValueError("Full original native receipt at the end of actual stdout")


def census(forest,n):
    """Read complete candidate topology and saved decisions; no oracle call."""
    src.need(type(forest)is dict and type(forest.get("n"))is int and forest["n"]==n,
             "Literal original nearest-count index")
    roots=forest["roots"]
    src.need(type(roots)is list and len(roots)==n+1,"Every original count root")
    nodes=leaves=depthmax=0;statuses=Counter();maximum=Fraction(0)
    for k,root in enumerate(roots):
        src.need(type(root)is dict and set(root)=={"k","tree"}and type(root["k"])is int and root["k"]==k,
                 "Ordered complete original roots")
        todo=[(root["tree"],0)]
        while todo:
            node,depth=todo.pop();nodes+=1;depthmax=max(depthmax,depth)
            src.need(nodes<=1000000 and depth<=128,"Bounded complete original candidate tree")
            if node["kind"]=="split":
                src.need(set(node)=={"kind","axis","cut","left","right"}and type(node["axis"])is int
                         and 0<=node["axis"]<5 and type(node["cut"])is str,"Literal complete binary split")
                Fraction(node["cut"]);todo.extend(((node["left"],depth+1),(node["right"],depth+1)))
            else:
                src.need(node["kind"]=="leaf"and set(node)=={"kind","box","decision","result"}
                         and type(node["decision"])is str and type(node["result"])is dict,"Complete saved leaf")
                leaves+=1;statuses[node["decision"]]+=1
                if node["decision"]=="PASS_TARGET":maximum=max(maximum,Fraction(node["result"]["score_upper"]))
    return dict(roots=n+1,nodes=nodes,leaves=leaves,maximum_depth=depthmax,
                closed_statuses=dict(statuses),maximum_score=str(maximum))


def summarize(task,row,packet):
    s=row["selection"];directory=Path(task)/"capsule"/s["capsule"]
    receipt_path=directory/s["receipt_name"];receipt=src.read(receipt_path)
    src.need(type(packet)is dict and receipt==packet,"Actual native stdout equals the whole fresh receipt")
    schema=row["native_schema"]
    src.need(set(receipt)==set(schema["fields"])and receipt["status"]==schema["status"]
             and receipt["scope"]==schema["scope"]and type(receipt["n"])is int and receipt["n"]==s["n"]
             and type(receipt["index"])is int and receipt["index"]==s["index"],"Literal selected native acceptance schema")
    # The selected original n6/B2 panel50 payload is about31MiB. Its exact
    # catalog hash/size is sealed; the ordinary metadata default16MiB is too
    # small for that unchanged full forest.
    forest=src.read(directory/s["forest_name"],limit=64*src.MIB);structural=census(forest,s["n"])
    src.need({k:structural[k]for k in row["candidate_census"]}==row["candidate_census"],"Whole selected original candidate census")
    bound=src.read(directory/"KERNEL_COPY_MANIFEST.json")["files"]
    src.need(type(bound)is dict and bound and receipt["kernel_sha256"]==bound==forest["kernel_sha256"],"Complete original kernel manifest/header")
    for name,pin in bound.items():
        src.parts(name);key=s["capsule"]+"/"+name
        src.need(row["source_files_sha256"].get(key)==pin and src.digest(directory/name)==pin,"Every actual frozen numerical kernel byte")
    for key,pin in(("forest_sha256",s["forest_pin"]),("contract_sha256",s["contract_pin"]),
                  ("checker_sha256",row["source_files_sha256"][s["capsule"]+"/count_protocol.py"])):
        src.need(receipt[key]==pin,"Exact selected forest/contract/checker identity")
    src.need(forest["contract_sha256"]==receipt["contract_sha256"]and forest["checker_sha256"]==receipt["checker_sha256"]
             and forest["target"]==s["target"]and type(forest["index"])is int and forest["index"]==s["index"],"Original exact native header")
    expected_stats={k:v for k,v in structural.items()if k!="roots"}
    src.need(receipt["statistics"]==expected_stats and type(receipt["fresh_leaf_evaluations"])is int
             and receipt["fresh_leaf_evaluations"]==structural["leaves"],"All original leaves freshly recomputed")
    src.need(receipt["negative_controls"]==schema["controls"]and len(schema["controls"])==24
             and len(set(schema["controls"]))==24,"Every original named corruption control")
    src.need(type(receipt["seconds"])in(int,float)and math.isfinite(receipt["seconds"])
             and receipt["seconds"]>=0,"Finite ordinary original elapsed metadata")
    return dict(job_id=row["job_id"],n=s["n"],band=s["band"],index=s["index"],target=s["target"],
        rho_interval=s["band_rho"],census={k:structural[k]for k in("roots","nodes","leaves","maximum_depth")},
        capsule_relative="capsule/"+s["capsule"],receipt_relative="capsule/"+s["capsule"]+"/"+s["receipt_name"],
        contract_relative="capsule/"+s["capsule"]+"/contract.json",forest_relative="capsule/"+s["capsule"]+"/"+s["forest_name"],
        forest_sha256=s["forest_pin"],contract_sha256=s["contract_pin"],checker_sha256=receipt["checker_sha256"],
        kernel_sha256=bound,receipt_sha256=src.digest(receipt_path),native_controls=receipt["negative_controls"],
        fresh_leaf_evaluations=receipt["fresh_leaf_evaluations"],parent_acquisitions_verified=False,
        fresh_parent_fact_joins_verified=False,full_finite69_verified=False,all_index_conclusion_verified=False)


def validate_run(task,row,report):
    task=Path(task);request=src.verify_job(task,row);original=request["original_task_root"]
    src.need(report["schema"]==OBSERVED and report["scope"]==SCOPE and report["job_id"]==row["job_id"]
             and report["implementation"]==implementation()and report["original_task_root"]==original
             and report["conditional_arithmetic_completed"]is False and all(report[f]is False for f in FLAGS),
             "Exact implementation and observed false-to-completed transition")
    observed=report["observed"]
    src.need(observed.get("status")=="completed"and type(observed.get("returncode"))is int and observed["returncode"]==0
             and observed.get("reason")is None and observed.get("proof_accepted")is False
             and observed.get("mode")=="untrusted_search"and type(observed.get("sample_count"))is int
             and observed["sample_count"]>0,"Actual successful BASIC execution")
    src.need(src.read(task/"execution/supervisor-result.json")==observed,"Actual stopped supervisor result")
    launch=src.read(task/"execution/launch.json")
    cwd=task/"capsule"/row["selection"]["capsule"]
    src.need(launch["argv"]==command(request,row,report["python_executable"])
             and mapped(task,launch["cwd"],original)==cwd and mapped(task,launch["output_dir"],original)==task/"execution"
             and launch["mode"]=="untrusted_search"and launch["sample_seconds"]==.2 and launch["heartbeat_seconds"]==20
             and launch["checkpoint_paths"]==[],"Actual original acceptor launch and capture context")
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
    return summarize(task,row,terminal(paths["stdout"].read_text("utf-8")))


def validate_completed(task, *,original_task_root=None):
    task=Path(task);request=src.verify_job(task);row=src.job(request["job_id"])
    src.need(original_task_root is None or str(original_task_root)==request["original_task_root"],"One explicit original root")
    observed=src.read(task/"STAGE_OBSERVED.json");complete=src.read(task/"STAGE_COMPLETED.json")
    summary=validate_run(task,row,observed)
    src.need(complete["schema"]==COMPLETED and complete["scope"]==SCOPE and complete["job_id"]==row["job_id"]
             and complete["implementation"]==implementation()and complete["observed_sha256"]==src.digest(task/"STAGE_OBSERVED.json")
             and complete["conditional_arithmetic_completed"]is True and complete["summary"]==summary
             and complete["artifacts"]==inventory(task)and all(complete[f]is False for f in FLAGS),
             "Full source/candidate/capture/receipt inventory, exact completed transition")
    return dict(schema="REVALIDATED_CONDITIONAL_FINITE69_COUNT_V1",job_id=row["job_id"],n=row["selection"]["n"],
                summary=summary,catalog_sha256=src.CATALOG_SHA256,stage_result_sha256=src.digest(task/"STAGE_COMPLETED.json"),
                source_manifest_sha256=src.digest(task/"SOURCES.json"),original_task_root=request["original_task_root"],
                conditional_arithmetic_completed=True,**{f:False for f in FLAGS})
