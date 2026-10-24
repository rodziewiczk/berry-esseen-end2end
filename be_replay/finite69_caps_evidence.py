"""Relocatable evidence checks for the new BASIC owncaps/resource execution.

No numerical kernel is imported. Full unchanged native executions remain the
arithmetic authority; this layer binds their sources, commands, stopped output
copies, complete original controls and the explicit metadata derivation.
"""
from __future__ import annotations
import copy
import json
import math
from pathlib import Path,PurePosixPath,PureWindowsPath
import re

from . import finite69_caps_sources as src, finite69_cap_epoch as epoch
from . import finite69_parent_evidence as parent_ev

OBSERVED="OBSERVED_FRESH_FINITE69_CAPS_BASIC_V1"
COMPLETED="COMPLETED_FRESH_FINITE69_CAPS_BASIC_V1"
SCOPE="FRESH_SUPPORTED_FINITE69_OWNCAPS_AND_RESOURCE_BASIC_V1"
CPU=43200
WALL=54000
MEMORY=2048*src.MIB
DISK=2048*src.MIB
FLAGS=("native_arithmetic_accepted","actual_support_acquired","parent_acquisitions_verified",
       "full_finite69_verified","all_index_conclusion_verified")
same,mapped=parent_ev.same,parent_ev.mapped


def implementation():
    names=("finite69_caps.py","finite69_caps_sources.py","finite69_caps_evidence.py","finite69_cap_epoch.py",
           "finite69_parent_sources.py","finite69_parent_evidence.py","finite69_parents.py","finite69_metadata.py",
           "finite69_sources.py","linux_supervisor.py","colab_batch.py","n5_remaining_sources.py")
    return {n:src.digest(src.ROOT/"be_replay"/n)for n in names}|{"catalog_sha256":src.CATALOG_SHA256}


LEGACY_CAPS_READER_SHA256="3951a1f31e8eb8b4655e5220f939784eab72b18cac4f40b3792a3bb914ce7743"
RECOVERY_BUNDLE_SHA256="4f356469cf741ebeb054fbcbb8b93f4264b5064ffa872e33a2b196240265c2a7"


def compatible_observed_implementation(value):
    current=implementation()
    return same(value,current)or same(value,dict(current,**{"finite69_caps_evidence.py":LEGACY_CAPS_READER_SHA256}))


def saved_observed_admission(task):
    """Explicit current-reader recovery of preserved original execution bytes."""
    report=src.read(Path(task)/"STAGE_OBSERVED.json")
    src.need(compatible_observed_implementation(report["implementation"])
             and report["implementation"]["finite69_caps_evidence.py"]==LEGACY_CAPS_READER_SHA256,
             "One exact previous execution reader, all other implementation/source pins unchanged")
    return dict(schema="FINITE69_CAPS_CURRENT_READER_RECOVERY_ADMISSION_V1",source_bundle_sha256=RECOVERY_BUNDLE_SHA256,
        original_observed_sha256=src.digest(Path(task)/"STAGE_OBSERVED.json"),
        original_execution_implementation=report["implementation"],current_reader_implementation=implementation(),
        original_execution_bytes_unchanged=True,mathematical_replay=False,**{f:False for f in FLAGS})


def validate_caps_controls(caps,stdout,expected):
    src.need(type(expected)is list and len(expected)==17 and all(type(name)is str for name in expected)
        and len(set(expected))==17 and type(caps["negative_controls"])is list
        and same(caps["negative_controls"],expected)and stdout.strip()==caps["status"]+" 17",
        "Fresh tighter CAPS receipt with the exact original list of17 controls")


def inventory(task):
    result={}
    for p in sorted(Path(task).rglob("*")):
        src.ordinary(p)
        if p.is_file()and p.relative_to(task).as_posix()not in("STAGE_OBSERVED.json","STAGE_COMPLETED.json"):
            result[p.relative_to(task).as_posix()]=dict(bytes=p.stat().st_size,sha256=src.digest(p))
    return result


def original_path(original,relative):
    cls=PureWindowsPath if re.match(r"^[A-Za-z]:",original)else PurePosixPath
    return str(cls(original)/"capsule"/relative)


def action_specs(request,python):
    original=request["original_task_root"]
    def entry(label,directory,script,args,outputs):
        return dict(label=label,directory=directory,argv=[python,"-B","-S",original_path(original,directory+script),*args],outputs=outputs)
    if request["kind"]=="resource":
        row=src.base.job(request["job_id"])
        return[entry("resource",src.RESOURCE,"FRESH_REPLAY.py",row["arguments"],[src.base.output_relative(row)])]
    plan=epoch.OWN+"plan01/PLAN.json"
    specs=[]
    for action,label in(("plan","plan01"),("construct","construct01"),("replay","replay01")):
        outputs=[epoch.OWN+label+"/"+n for n in("metadata.json","stdout.txt","stderr.txt","PLAN.json"if action=="plan"else"RESULT.json")]
        args=[action,label]+([]if action=="plan"else[original_path(original,plan)])
        specs.append(entry(action,src.OWN,"run.py",args,outputs))
    specs.append(entry("readback",src.AUDIT,"readback.py",[original_path(original,src.AUDIT+"OWN_REQUEST.json")],[src.AUDIT+"OWN_RESULT.json"]))
    specs.append(entry("caps","work/cutoff6_20261020/entry/resource7_9_v2/","check_caps.py",[],[src.CAPS]))
    return specs


def duration(value):return type(value)in(int,float)and math.isfinite(value)and value>=0


def action_terminal(task,spec,stdout):
    """Fail closed before an expensive later action; no numerical evaluation."""
    if spec["label"]not in("plan","construct","replay"):return
    tokens=stdout.splitlines()[-1].split()
    prefix="HEURISTIC_ONLY"if spec["label"]=="plan"else"EXACT_SUPPORTED_OWNCAPS6_9_WHOLE_COVER_PASS"
    src.need(len(tokens)==5 and tokens[:4]==[prefix,"STRIPS","86","SECONDS"]
        and math.isfinite(float(tokens[4]))and float(tokens[4])>=0,"Complete original86-strip successful terminal")
    if spec["label"]=="plan":
        p=src.read(Path(task)/"capsule"/epoch.OWN/"plan01/PLAN.json")
        src.need(sum(len(b["strips"])for b in p["bands"])==86,"The unchanged check_caps protocol requires exactly86 planned strips")


def transport(task,request,spec,call,python):
    task=Path(task);original=request["original_task_root"];label=spec["label"];directory=task/"executions"/label
    observed=call["observed"]
    src.need(call["label"]==label and observed.get("status")=="completed"
        and type(observed.get("returncode"))is int and observed["returncode"]==0 and observed.get("reason")is None
        and observed.get("proof_accepted")is False and observed.get("mode")=="untrusted_search"
        and type(observed.get("sample_count"))is int and observed["sample_count"]>0,"Actual successful stopped BASIC action")
    src.need(same(src.read(directory/"supervisor-result.json"),observed),"Whole actual supervisor result")
    launch=src.read(directory/"launch.json")
    src.need(launch["argv"]==spec["argv"]and mapped(task,launch["cwd"],original)==task/"capsule"
        and mapped(task,launch["output_dir"],original)==directory and launch["mode"]=="untrusted_search"
        and launch["sample_seconds"]==.2 and launch["heartbeat_seconds"]==20,"Exact original launch and stopped-capture context")
    for name,value in(("cpu_seconds",CPU),("wall_seconds",WALL),("memory_bytes",MEMORY),("disk_bytes",DISK),("log_bytes",16*src.MIB)):
        types=(int,float)if name=="wall_seconds"else(int,)
        src.need(type(launch[name])in types and launch[name]==value,"Exact documented BASIC resource ceiling")
    scope=dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",proof_acceptance=False,external_wall_seconds=float(WALL),
        per_process_RLIMIT_AS_bytes=MEMORY,per_process_RLIMIT_CPU_seconds=CPU,aggregate_kernel_memory_limit=False,
        aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY,sampled_group_CPU_limit_seconds=CPU,
        sampled_file_limit_bytes=DISK,sampled_log_limit_bytes=16*src.MIB,descendants_changing_session_are_contained=False,
        equivalent_to_Windows_Job_or_cgroup=False)
    src.need(same(observed["guard_scope"],scope),"Honest complete process-group resource contract")
    paths={}
    for kind in("stdout","stderr"):
        p=mapped(task,observed[kind+"_path"],original)
        src.need(p==directory/(kind+".txt")and p.is_file()and p.stat().st_size<=16*src.MIB
            and src.digest(p)==observed[kind+"_sha256"],"Actual captured stdout/stderr SHA")
        paths[kind]=p
    src.need(paths["stderr"].stat().st_size==0,"Empty successful original stderr")
    outputs=spec["outputs"]
    src.need([mapped(task,p,original)for p in launch["checkpoint_paths"]]==[task/"capsule"/p for p in outputs],"Full declared output capture list")
    captures=observed["checkpoints"]
    src.need(type(captures)is list and len(captures)==len(outputs),"Every stopped native output captured")
    for relative,capture in zip(outputs,captures):
        p=task/"capsule"/relative;copied=mapped(task,capture["path"],original)
        src.need(set(capture)=={"source_path","exists","trusted_certificate","path","bytes","sha256"}
            and capture["exists"]is True and capture["trusted_certificate"]is False
            and mapped(task,capture["source_path"],original)==p and copied==directory/"checkpoints"/relative
            and type(capture["bytes"])is int and capture["bytes"]==p.stat().st_size==copied.stat().st_size
            and capture["sha256"]==src.digest(p)==src.digest(copied),"Exact whole stopped output bytes, not receipt claims")
    return paths["stdout"].read_text("utf-8")


def request_bytes(capsule):
    capsule=Path(capsule);plan=epoch.OWN+"plan01/PLAN.json"
    return src.dump(dict(family="own",plan=plan,plan_sha256=src.digest(capsule/plan),manifest_sha256=src.digest(capsule/src.OWN/"MANIFEST.json"),
        construct_capture=epoch.OWN+"construct01",construct_metadata_sha256=src.digest(capsule/epoch.OWN/"construct01/metadata.json"),
        replay_capture=epoch.OWN+"replay01",replay_metadata_sha256=src.digest(capsule/epoch.OWN/"replay01/metadata.json"),output=src.AUDIT+"OWN_RESULT.json"))


def own_summary(task,request,stdout,report):
    capsule=Path(task)/"capsule";original=request["original_task_root"]
    manifest=src.read(capsule/src.OWN/"MANIFEST.json");plan_path=epoch.OWN+"plan01/PLAN.json"
    plan=src.read(capsule/plan_path);base=dict(manifest["files_sha256"])
    base[src.OWN+"MANIFEST.json"]=src.digest(capsule/src.OWN/"MANIFEST.json")
    for action,label in(("plan","plan01"),("construct","construct01"),("replay","replay01")):
        directory=capsule/epoch.OWN/label;meta=src.read(directory/"metadata.json")
        output="PLAN.json"if action=="plan"else"RESULT.json";inputs=dict(base)
        if action!="plan":inputs[plan_path]=src.digest(capsule/plan_path)
        args=[report["python_executable"],"-B","planner.py",original_path(original,epoch.OWN+label+"/PLAN.json")]if action=="plan"else[
            report["python_executable"],"-B","protocol.py",action,original_path(original,plan_path),original_path(original,epoch.OWN+label+"/RESULT.json")]
        src.need(type(meta["returncode"])is int and meta["returncode"]==0 and meta["changed_inputs"]==[]
            and meta["command"]==args and mapped(task,meta["cwd"],original)==capsule/src.OWN
            and same(meta["input_sha256"],inputs)and meta["python"]==report["python_version"]
            and meta["stdout_sha256"]==src.digest(directory/"stdout.txt")and meta["stderr_sha256"]==src.digest(directory/"stderr.txt")
            and(directory/"stderr.txt").stat().st_size==0 and meta[output+"_sha256"]==src.digest(directory/output)
            and duration(meta["elapsed_seconds"]),"Exact actual inner invocation/input/result/capture commitments")
        # run.py forwards the child's actual output without changing it.
        src.need(stdout[action]==(directory/"stdout.txt").read_text("utf-8"),"Outer capture equals actual original child stdout")
        action_terminal(task,{"label":action},stdout[action])
    src.need((capsule/src.AUDIT/"OWN_REQUEST.json").read_bytes()==request_bytes(capsule),"Exact fresh readback request, not historical input")
    construct=src.read(capsule/epoch.OWN/"construct01/RESULT.json",limit=128*src.MIB)
    replay=src.read(capsule/epoch.OWN/"replay01/RESULT.json",limit=128*src.MIB)
    src.need(same({k:v for k,v in construct.items()if k!="seconds"},{k:v for k,v in replay.items()if k!="seconds"})
        and duration(construct["seconds"])and duration(replay["seconds"]),"Entire native construct/replay equality except elapsed metadata")
    native_controls=dict(complex_power=16,quadratic_completion=140,moment_factorizations=7,malformed_domains=4,plan_negative_controls=17)
    strips=sum(len(b["strips"])for b in plan["bands"])
    src.need(plan["schema"]=="SUPPORTED_OWNCAPS6_9_PLAN_V1"and same(plan["n"],[6,7,8,9])and strips==86
        and construct["status"]=="EXACT_SUPPORTED_OWNCAPS6_9_WHOLE_COVER_PASS"and len(construct["rows"])==344
        and same(construct["controls"],native_controls)and construct["plan_sha256"]==src.digest(capsule/plan_path)
        and construct["manifest_sha256"]==src.digest(capsule/src.OWN/"MANIFEST.json"),"Full86-strip/344-row native scope and all original controls")
    graph=dict(manifest["files_sha256"])
    for name in(src.OWN+"MANIFEST.json",plan_path,src.AUDIT+"OWN_REQUEST.json",src.AUDIT+"readback.py",src.AUDIT+"REVIEW.txt"):
        graph[name]=src.digest(capsule/name)
    for label in("construct01","replay01"):
        for name in("metadata.json","RESULT.json","stdout.txt","stderr.txt"):
            path=epoch.OWN+label+"/"+name;graph[path]=src.digest(capsule/path)
    result=src.read(capsule/src.AUDIT/"OWN_RESULT.json")
    expected=dict(status="PASS_INDEPENDENT_SUPPORTED_FOURIER6_9_READBACK",family="own",mathematical_status=construct["theorem"],
        execution_status="fresh independent whole-coverage/normalization/capture readback with complete native construction/replay; no integral oracle calls here",
        n=[6,7,8,9],bands=construct["bands"],targets=construct["targets"],strips=86,exact_rows=344,attempts=len(construct["attempts"]),
        per_band_per_n_upper=construct["per_band_per_n_upper"],negative_controls=28,actual_support_acquired=False,cutoff6_proved=False,files_sha256=graph)
    src.need(same(result,expected)
        and same(json.loads(stdout["readback"],object_pairs_hook=src.base.unique),{k:v for k,v in result.items()if k!="files_sha256"}),"Actual independent whole-result readback and28 controls")
    caps=src.read(capsule/src.CAPS);actual={p:src.digest(capsule/p)for p in caps["files_sha256"]}|{src.CAPS:src.digest(capsule/src.CAPS)}
    for name in(src.AUDIT+"OWN_RESULT.json",epoch.OWN+"construct01/RESULT.json",epoch.OWN+"replay01/RESULT.json",
        "work/cutoff6_20261020/entry/resource7_9_v2/check_caps.py"):
        graph[name]=src.digest(capsule/name)
    src.need(same(caps["files_sha256"],graph),"Exact complete original readback-to-CAPS source/capture extension")
    epoch.cap_binding((Path(task)/"provenance/ORIGINAL_CAPS.json").read_bytes(),(capsule/src.CAPS).read_bytes(),
        src.catalog()["original_source_pins"],actual)
    for packet in(result,caps):
        src.need(all(src.digest(capsule/p)==pin for p,pin in packet["files_sha256"].items()),"Whole actual native readback ancestor graph")
    validate_caps_controls(caps,stdout["caps"],src.read(Path(task)/"provenance/ORIGINAL_CAPS.json")["negative_controls"])
    return dict(kind="owncaps",job_id="owncaps6_9",receipt_relative="capsule/"+src.CAPS,receipt_sha256=src.digest(capsule/src.CAPS),
        strips=86,whole_rows=344,selected_n_rows=258,native_controls=native_controls,readback_controls=28,caps_controls=17,
        accepted_upper=caps["accepted_upper"],fresh_initial_binding_verified=False,conditional_arithmetic_completed=True)


def resource_summary(task,request,stdout):
    task=Path(task);row=src.base.job(request["job_id"]);capsule=task/"capsule"
    upstream=validate_completed(task/"inputs/owncaps")
    initial=parent_ev.validate_completed(task/"inputs/initial")
    case=row["output"].split("/")[0]
    # Recompute the complete source-only reverse-checked derivation from sealed
    # originals retained in this very stage, including all182 CAPS ancestors.
    derived,parent_path,parent_receipt,caps=src.derived_resource(capsule,row,task/"inputs/initial",task/"inputs/owncaps",
        old_caps=task/"provenance/ORIGINAL_CAPS.json")
    src.need((task/"DERIVATION.json").read_bytes()==src.dump({k:v for k,v in derived.items()if not k.endswith("_bytes")}),"Entire deterministic metadata derivation report")
    for relative,raw in((src.RESOURCE+"FRESH_REPLAY.py",derived["replay_bytes"]),
        (src.RESOURCE+case+"/FRESH_PREPARED.json",derived["fresh_prepared_bytes"]),
        (src.RESOURCE+case+"/FRESH_SOURCE_RESULT.json",derived["fresh_source_result_bytes"])):
        src.need((capsule/relative).read_bytes()==raw,"Exact byte-only resource epoch, no kernel or candidate changes")
    src.need((capsule/parent_path).read_bytes()==parent_receipt.read_bytes()
        and(capsule/src.CAPS).read_bytes()==(task/"inputs/owncaps/capsule"/src.CAPS).read_bytes(),"Actual fresh INITIAL/CAPS input bytes")
    old=row["reference"]["native_answer"];expected=copy.deepcopy(old);expected.pop("seconds")
    prepared=src.read(capsule/src.RESOURCE/case/"FRESH_PREPARED.json")
    graph=dict(prepared["files_sha256"])
    fresh_initial=src.read(parent_receipt)
    graph.update(fresh_initial["files_sha256"]);graph[parent_path]=src.digest(parent_receipt)
    graph.update(caps["files_sha256"]);graph[src.CAPS]=src.digest(capsule/src.CAPS)
    for name in(src.RESOURCE+"replay.py",src.RESOURCE+"prepare.py",src.RESOURCE+"PROOF.txt",src.RESOURCE+case+"/FRESH_PREPARED.json"):
        graph[name]=src.digest(capsule/name)
    src.need(all(src.digest(capsule/name)==pin for name,pin in graph.items()),"Every actual fresh resource source/parent/CAPS ancestor, not only a declared graph")
    expected.update(initial_receipt_sha256=src.digest(parent_receipt),
        source_result_sha256=src.digest(capsule/src.RESOURCE/case/"FRESH_SOURCE_RESULT.json"),files_sha256=graph)
    output=capsule/src.base.output_relative(row);receipt=src.read(output,limit=64*src.MIB)
    src.need(type(receipt)is dict and receipt.keys()==expected.keys()|{"seconds"}
        and same({k:v for k,v in receipt.items()if k!="seconds"},expected)and duration(receipt["seconds"]),
        "Every original full100-panel result/control/profile/source field under the exact fresh metadata epoch")
    src.need(stdout.splitlines()[-1].split()==[receipt["status"],str(receipt["n"]),receipt["band"]],"Actual successful resource terminal")
    return dict(kind="resource",job_id=row["job_id"],n=receipt["n"],band=receipt["band"],panels=100,
        excluded=len(receipt["excluded"]),retained=len(receipt["retained"]),negative_controls=receipt["negative_controls"],
        receipt_relative="capsule/"+src.base.output_relative(row),receipt_sha256=src.digest(output),
        fresh_initial_stage_sha256=initial["stage_result_sha256"],fresh_caps_stage_sha256=upstream["stage_result_sha256"],
        fresh_initial_binding_verified=True,fresh_caps_binding_verified=True,conditional_arithmetic_completed=True)


def validate_run(task,report):
    task=Path(task);request=src.verify_job(task)
    src.need(report["schema"]==OBSERVED and report["scope"]==SCOPE and report["job_id"]==request["job_id"]
        and compatible_observed_implementation(report["implementation"])and report["original_task_root"]==request["original_task_root"]
        and report["conditional_arithmetic_completed"]is False and all(report[f]is False for f in FLAGS),"Exact observed source epoch and false-to-complete transition")
    src.need(type(report["python_executable"])is str and PurePosixPath(report["python_executable"]).is_absolute()
        and PurePosixPath(report["python_executable"]).name.startswith("python")
        and type(report["python_version"])is str and bool(report["python_version"]),"Recorded original Python execution context")
    specs=action_specs(request,report["python_executable"])
    src.need(type(report["actions"])is list and len(report["actions"])==len(specs),"Every original native action, no omitted stage")
    stdout={s["label"]:transport(task,request,s,c,report["python_executable"])for s,c in zip(specs,report["actions"])}
    return own_summary(task,request,stdout,report)if request["kind"]=="owncaps"else resource_summary(task,request,stdout["resource"])


def validate_completed(task, *,original_task_root=None):
    task=Path(task);request=src.verify_job(task)
    src.need(original_task_root is None or str(original_task_root)==request["original_task_root"],"One explicit original execution root")
    observed=src.read(task/"STAGE_OBSERVED.json");complete=src.read(task/"STAGE_COMPLETED.json");summary=validate_run(task,observed)
    if not same(observed["implementation"],implementation()):
        src.need((task/"RECOVERY_ADMISSION.json").read_bytes()==src.dump(saved_observed_admission(task)),
                 "Explicit current-reader admission for the exact original saved execution")
    src.need(complete["schema"]==COMPLETED and complete["scope"]==SCOPE and complete["job_id"]==request["job_id"]
        and same(complete["implementation"],observed["implementation"])and complete["observed_sha256"]==src.digest(task/"STAGE_OBSERVED.json")
        and complete["conditional_arithmetic_completed"]is True and same(complete["summary"],summary)
        and same(complete["artifacts"],inventory(task))and all(complete[f]is False for f in FLAGS),"Exact completed source/capture/receipt inventory")
    return dict(schema="REVALIDATED_FRESH_FINITE69_CAPS_BASIC_V1",job_id=request["job_id"],kind=request["kind"],summary=summary,
        original_task_root=request["original_task_root"],stage_result_sha256=src.digest(task/"STAGE_COMPLETED.json"),
        source_manifest_sha256=src.digest(task/"SOURCES.json"),conditional_arithmetic_completed=True,**{f:False for f in FLAGS})


def validate_batch(root):
    """Revalidate an exported complete19-stage batch at any restored path."""
    root=Path(root);packet=src.read(root/"SESSION_RESULT.json")
    expected=src.catalog()["initial_job_ids"]+["owncaps6_9"]+src.catalog()["resource_job_ids"]
    src.need(packet["schema"]=="CONDITIONAL_FINITE69_CAPS_BATCH_V1"
        and packet["state"]=="complete_selected_conditional_caps_resource_arithmetic_basic"
        and packet["catalog_sha256"]==src.CATALOG_SHA256 and packet["expected_stages"]==19
        and packet["expected_native_actions"]==23 and packet["conditional_arithmetic_completed"]is True
        and all(packet[f]is False for f in FLAGS)and [r["job_id"]for r in packet["jobs"]]==expected,
        "Every fixed complete INITIAL/owncaps/resource stage and no global promotion")
    checked={}
    for row in packet["jobs"]:
        task=root.joinpath(*src.parts(row["task_relative"]))
        result=parent_ev.validate_completed(task)if ".initial."in row["job_id"]else validate_completed(task)
        src.need(same(row["validated"],result),"Whole freshly revalidated exported stage summary")
        checked[row["job_id"]]=result
    for job_id in src.catalog()["resource_job_ids"]:
        summary=checked[job_id]["summary"];initial=checked[job_id.replace(".resource.",".initial.")]
        src.need(summary["fresh_initial_stage_sha256"]==initial["stage_result_sha256"]
            and summary["fresh_caps_stage_sha256"]==checked["owncaps6_9"]["stage_result_sha256"],"Same actual fresh upstream evidence throughout the completed batch")
    return dict(schema="REVALIDATED_FINITE69_CAPS_BATCH_V1",catalog_sha256=src.CATALOG_SHA256,
        session_result_sha256=src.digest(root/"SESSION_RESULT.json"),completed_stages=19,original_native_actions=23,
        resource_panels=900,conditional_arithmetic_completed=True,stages=checked,**{f:False for f in FLAGS})
