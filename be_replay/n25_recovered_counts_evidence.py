"""Pure full readback of unchanged original recovered B5 counts inside delivery66.

An accepted stage acquires conditional count arithmetic only. Same-law parent
resources, contact hypotheses and the n25 physical union are separate checks.
"""
from __future__ import annotations
import ast
import json
import math
from pathlib import Path
import re
import sys
from . import count_task as common,n25_recovery_sources as sources,n25_full_transport as transport
from .n25_count_evidence import same,control_labels,relative,path_class

SCHEMA="N25_RECOVERED_ORIGINAL_COUNT_EXECUTION_V1"
SCOPE="FRESH_RECOVERED_ORIGINAL_B5_CONDITIONAL_COUNT_ONLY"
OBSERVED={"schema","target","epoch","scope","observed","census","implementation",
          "arithmetic_accepted","parent_acquisitions_verified","full66_complete"}
ACCEPTED={"native_receipt","native_receipt_sha256","negative_controls","conditional_premises"}
RECEIPT={"status","forest_sha256","contract_sha256","checker_sha256","kernel_sha256",
         "statistics","negative_controls","fresh_leaf_evaluations","seconds","scope"}
need=common.need
MIB=1024**2


def implementation():
    root=Path(__file__).resolve().parent
    return dict(count_runner_sha256=common.digest(root/"n25_recovered_counts.py"),
        count_source_adapter_sha256=common.digest(sources.__file__),count_source_plan_sha256=sources.PLAN_SHA256,
        transport_sha256=common.digest(transport.__file__),evidence_sha256=common.digest(__file__),
        supervisor_sha256=common.digest(root/"linux_supervisor.py"),
        native_evidence_helpers_sha256=common.digest(root/"n25_count_evidence.py"),
        common_runtime_sha256=common.digest(common.__file__),
        source_helpers_sha256=common.digest(sources.base.__file__),python=sys.version)


def premises(target):
    spec=sources.profile(target, ordinary=True)
    items=["Entire literal simultaneous same-law B5 resource contract",
        "Current complete B5 INITIAL/resource acquisition and exact outward resource-to-contract mapping",
        "One unrestricted attained positive closed witness with score at least CE",
        "Sharp C24<=CE or complete acquired auxiliary C24<CE+1/80, giving q25<=5/16",
        "Retained physical count kernel and all closed-domain analytic implications"]
    if spec["kind"]=="ordinary-v14":items.append("Exact local-contact V14 premise and complete original V12 physical row")
    return items


def _implementation(row):
    expected=implementation()
    need(type(row) is dict and set(row)==set(expected) and type(row["python"]) is str and row["python"]
        and all(same(row[k],v) for k,v in expected.items() if k!="python"),"Exact recovered-original count implementation")


def _literal(protocol):
    tree=ast.parse(Path(protocol).read_bytes())
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="accept"]
    need(len(functions)==1,"One unchanged original full native acceptance function")
    out=[n.value for n in functions[0].body if isinstance(n,ast.Assign)
         and any(isinstance(t,ast.Name) and t.id=="out" for t in n.targets)]
    need(len(out)==1 and isinstance(out[0],ast.Call) and isinstance(out[0].func,ast.Name)
         and out[0].func.id=="dict","Literal original acceptance output")
    kw={k.arg:k.value for k in out[0].keywords}
    return {k:ast.literal_eval(kw[k]) for k in ("status","scope")}


def validate_run(task,target,epoch,observed,census,*,original_task_root=None):
    task=transport.ordinary(task,directory=True).resolve()
    epoch=transport.ordinary(epoch,directory=True).resolve()
    need(epoch.parent==task and re.fullmatch(r"accept-[0-9a-f]{12,32}",epoch.name),"Direct complete count execution epoch")
    sources.verify_preparation(target, task)
    spec=sources.verify(target,task/"capsule")
    need(same(spec,sources.verify(target,epoch/"capsule",outputs=True)),"Exact sealed current count source clone")
    capsule=epoch/"capsule";index=spec["index"]
    forest_name,receipt_name=f"COUNT{index}_FOREST.json",f"COUNT{index}_ACCEPTED.json"
    need({p.name for p in capsule.iterdir()}==set(spec["files"])|{forest_name,receipt_name},
         "Only exact source, complete candidate and fresh receipt in native clone")
    forest=common.read(capsule/forest_name)
    actual=sources.geometry(target,capsule,forest)
    need(same(actual,census) and actual["pending"]==0,"Complete26-root stored geometry and no pending work")
    receipt=common.read(capsule/receipt_name,4*MIB)
    need(type(receipt) is dict and set(receipt)==RECEIPT,"Exact complete native count receipt")
    literals=_literal(capsule/"count_protocol.py")
    need(all(type(v) is str and v and same(receipt[k],v) for k,v in literals.items()),"Exact unchanged conditional scope and honest new native status")
    for key,name in (("forest_sha256",forest_name),("contract_sha256","contract.json"),("checker_sha256","count_protocol.py")):
        need(receipt[key]==common.digest(capsule/name),"Actual fresh native source/input binding")
    kernel=common.read(capsule/"KERNEL_COPY_MANIFEST.json",16*MIB)["files"]
    need(same(receipt["kernel_sha256"],kernel) and all(common.digest(capsule/n)==v for n,v in kernel.items()),
         "Every exact unchanged numerical byte remains bound")
    stats={k:actual[k] for k in ("nodes","leaves","closed_statuses","maximum_score","maximum_depth")}
    need(same(receipt["statistics"],stats) and type(receipt["fresh_leaf_evaluations"]) is int
         and receipt["fresh_leaf_evaluations"]==actual["leaves"],"All saved leaves freshly evaluated in the separate native process")
    need(same(receipt["negative_controls"],control_labels(capsule/"count_protocol.py")),"All24 unchanged original corruption controls")
    need(type(receipt["seconds"]) in (int,float) and math.isfinite(receipt["seconds"]) and receipt["seconds"]>=0,
         "Finite nonnegative original elapsed field")
    checked=transport.validate(task,epoch/"execution",observed,
        script_relative=(capsule/"count_protocol.py").relative_to(task).as_posix(),args=["accept"],
        cwd_relative=capsule.relative_to(task).as_posix(),native=True,original_task_root=original_task_root)
    stdout=(epoch/"execution/stdout.txt").read_text("utf-8")
    need(same(json.loads(stdout,object_pairs_hook=common.unique),receipt),"Complete actual terminal JSON equals fresh native receipt")
    return receipt,checked


def validate_stage(task,target,epoch,*,original_task_root=None):
    target=sources.normalize(target)
    task=transport.ordinary(task,directory=True).resolve()
    epoch=transport.ordinary(epoch,directory=True).resolve()
    for name in ("NATIVE_OBSERVED.json","NATIVE_ACCEPTED.json"):
        transport.ordinary(epoch/name,limit=4*MIB)
    before=common.read(epoch/"NATIVE_OBSERVED.json",4*MIB)
    accepted=common.read(epoch/"NATIVE_ACCEPTED.json",4*MIB)
    need(type(before) is dict and set(before)==OBSERVED and type(accepted) is dict and set(accepted)==OBSERVED|ACCEPTED,
         "Exact unaccepted observation and sole accepted arithmetic transition")
    need(before["schema"]==SCHEMA and before["target"]==target and before["scope"]==SCOPE
         and before["arithmetic_accepted"] is False and accepted["arithmetic_accepted"] is True
         and all(before[k] is False and accepted[k] is False for k in ("parent_acquisitions_verified","full66_complete"))
         and all(same(before[k],accepted[k]) for k in before if k!="arithmetic_accepted"),"Only validated conditional count arithmetic changes")
    _implementation(before["implementation"])
    receipt,checked=validate_run(task,target,epoch,before["observed"],before["census"],original_task_root=original_task_root)
    original=path_class(checked["original_task_root"])(checked["original_task_root"])
    need(relative(before["epoch"],original)==epoch.relative_to(task),"Preserved original count epoch maps exactly")
    native=epoch/"capsule"/f"COUNT{sources.profile(target)['index']}_ACCEPTED.json"
    need(relative(accepted["native_receipt"],original)==native.relative_to(task)
         and accepted["native_receipt_sha256"]==common.digest(native)
         and type(accepted["negative_controls"]) is int and accepted["negative_controls"]==24
         and same(accepted["conditional_premises"],premises(target)),"Actual fresh receipt and exact still-conditional semantic premises")
    return dict(schema="REVALIDATED_N25_RECOVERED_ORIGINAL_COUNT_V1",target=target,index=sources.profile(target)["index"],
        census=before["census"],contract_sha256=receipt["contract_sha256"],checker_sha256=receipt["checker_sha256"],
        forest_sha256=receipt["forest_sha256"],native_receipt_sha256=common.digest(native),
        source_plan_sha256=sources.PLAN_SHA256,source_asset_sha256=sources.ARCHIVE_SHA256,source_design_sha256=sources.profile(target)["design_sha256"],
        transport=checked,negative_controls=24,conditional_premises=premises(target),
        native_arithmetic_accepted=True,parent_acquisitions_verified=False,full66_complete=False)
