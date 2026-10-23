"""Source/JSON-only inventory of the literal n6--9 count and parent selection.

No mathematical module is imported. The only upstream imports are frozen
stdlib-only archive, AST and composer-selection adapters.
"""
from __future__ import annotations
from dataclasses import asdict
import ast
import hashlib
import importlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
VENDOR=ROOT/"vendor/finite69_snapshot_v1"
NAMES=("reproduction/all_indices/__init__.py","reproduction/all_indices/c5_counts.py",
       "reproduction/all_indices/c5_inputs.py","reproduction/continuations/__init__.py",
       "reproduction/continuations/catalog.py","reproduction/continuations/count_catalog.py",
       "reproduction/continuations/support_port.py")


def digest(raw):return hashlib.sha256(raw).hexdigest()
def dump(path,value):
    raw=(json.dumps(value,sort_keys=True,indent=2)+"\n").encode();path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(raw);return digest(raw)
def freeze(old):
    rows=[]
    for name in NAMES:
        raw=(old/name).read_bytes();p=VENDOR/name;p.parent.mkdir(parents=True,exist_ok=True)
        if p.exists()and p.read_bytes()!=raw:raise ValueError("Changed frozen selector: "+name)
        p.write_bytes(raw);rows.append(dict(path=name,sha256=digest(raw),bytes=len(raw)))
    raw=(ROOT/"vendor/n5_remaining_snapshot_v1/LICENSE").read_bytes();(VENDOR/"LICENSE").write_bytes(raw)
    rows.append(dict(path="LICENSE",sha256=digest(raw),bytes=len(raw)))
    return dump(VENDOR/"SNAPSHOT.json",dict(schema="UNCHANGED_FINITE69_SOURCE_SELECTORS_V1",files=rows,
        mathematical_modules_imported=False,arithmetic_computed=False))


def census(forest,n):
    roots=forest["roots"]
    if type(forest["n"])is not int or forest["n"]!=n or [r["k"]for r in roots]!=list(range(n+1)):
        raise ValueError("All literal original nearest-count roots")
    nodes=leaves=depth=0
    for root in roots:
        if type(root["k"])is not int:raise ValueError("Integer root")
        todo=[(root["tree"],0)]
        while todo:
            node,level=todo.pop();nodes+=1;depth=max(depth,level)
            if level>128 or nodes>1000000:raise ValueError("Bounded original candidate topology")
            if node["kind"]=="leaf":leaves+=1
            elif node["kind"]=="split":todo.extend(((node["left"],level+1),(node["right"],level+1)))
            else:raise ValueError("Original complete binary candidate tree")
    return dict(roots=n+1,nodes=nodes,leaves=leaves,maximum_depth=depth)


def build(old,cutoff6,combined):
    snapshot=freeze(old);sys.path.insert(0,str(VENDOR))
    sys.path.insert(0,str(ROOT))
    from be_replay.finite69_metadata import reconstruct_prepared,BASE,ORIGIN
    original=importlib.import_module("reproduction.continuations.catalog")
    selectors=importlib.import_module("reproduction.continuations.count_catalog")
    rows=[];files={};resource_references={};parents=[]
    def record(sources,name,pin):
        try:
            if not name.startswith("work/"):raise FileNotFoundError("Exact run capture absent from the primary work-source assets: "+name)
            raw=sources.read(name,pin,max_bytes=64*1024**2);archive,info=sources.member(name,max_bytes=64*1024**2)
            row=dict(archive=Path(archive.filename).name,member=info.filename,sha256=pin,bytes=len(raw))
        except FileNotFoundError:
            relative=name.removeprefix(BASE+"/")
            if name.startswith(BASE+"/") and relative.count("/")==1 and relative.endswith("/INPUT.json"):
                case=relative.split("/")[0];n,band=case.split("_")
                alias=ORIGIN+f"/INITIAL{int(n[1:])}_{band}.json"
                raw=record(sources,alias,pin)
                row=dict(files[alias],alias_of=alias)
            elif name.startswith(BASE+"/") and relative.count("/")==1 and relative.endswith("/PREPARED.json"):
                case=relative.split("/")[0];n,band=case.split("_");n=int(n[1:])
                manifest_name=BASE+"/SOURCE_PREPARED.json"
                manifest_raw=record(sources,manifest_name,graph[manifest_name]);manifest=original.parse(manifest_raw)
                candidate_name=ORIGIN+f"/INITIAL{n}_{band}.json"
                candidate=record(sources,candidate_name,graph[candidate_name])
                required=set(manifest["files_sha256"])|set(manifest["original_source_graph"])|{
                    candidate_name,BASE+f"/{case}/INPUT.json",manifest_name,
                    BASE+"/prepare.py",BASE+"/replay.py",BASE+"/PROOF.txt",name}
                pins={p:graph[p]for p in sorted(required)}
                for p in required-{name}:record(sources,p,pins[p])
                raw=reconstruct_prepared(manifest_raw,candidate,n=n,band=band,source_pins=pins)
                row=dict(sha256=pin,bytes=len(raw),reconstruction="ORIGINAL_POSIX_PREPARED_V1",
                    n=n,band=band,source_pins=pins,source_prepared=manifest_name,candidate=candidate_name,
                    metadata_adapter_sha256=digest((ROOT/"be_replay/finite69_metadata.py").read_bytes()))
            else:raise
        if digest(raw)!=pin:raise ValueError("Every exact original source/reconstruction pin")
        if name in files and files[name]!=row:raise ValueError("Conflicting source byte identity")
        files[name]=row;return raw
    with original.Sources(cutoff6,combined)as sources:
        jobs,graph=selectors.count_jobs(sources)
        for ordinal,job in enumerate(jobs):
            inspected=selectors.job_sources(sources,job,graph,verify_bytes=False)
            pins=inspected["source_files_sha256"]
            raw={name:record(sources,name,pin)for name,pin in pins.items()}
            forest=json.loads(raw[job.capsule+"/"+job.forest_name]);structural=census(forest,job.n)
            rows.append(dict(job_id=job.job_id,kind="count",selection=asdict(job),source_files_sha256=pins,
                native_schema=inspected["native_schema"],candidate_census=structural,
                candidate_is_untrusted=True,parent_acquisitions_verified=False,all_index_conclusion_verified=False))
            contract=inspected["contract"]
            for key in("resource_path","resource_receipt","resource_receipt_path","initial_receipt"):
                if key in contract:resource_references.setdefault(contract[key],[]).append(job.job_id)
            if ordinal%25==0:print("Source-only n6--9 count catalog",ordinal,"/",len(jobs),flush=True)
        support=original.support_plan(sources)
        for name,pin in support["source_files_sha256"].items():record(sources,name,pin)
        # These are source requirements, not inferred fresh acquisitions. The
        # actual selected count contracts provide the deduplicated pointer list.
        for name,using in sorted(resource_references.items()):
            if name not in graph:raise ValueError("Selected contract reference outside frozen final graph")
            record(sources,name,graph[name])
        def parent(kind,job_id,directory,args,output):
            name=directory+"/"+output
            try:old=original.parse(sources.read(name,graph[name]))
            except FileNotFoundError:old=None
            pins={}
            if old is None:
                if directory!="work/cutoff6_20261018/analytic/initial7_9_accept_v1":
                    raise ValueError("Unspecified absent native reference: "+name)
                case=output.rsplit("/",1)[0];prepared_name=directory+"/"+case+"/PREPARED.json"
                prepared=original.parse(record(sources,prepared_name,graph[prepared_name]))
                native_pins=dict(prepared["files_sha256"])
                for local in("replay.py","PROOF.txt","prepare.py","SOURCE_PREPARED.json",case+"/PREPARED.json"):
                    native_pins[directory+"/"+local]=graph[directory+"/"+local]
            else:native_pins=old["files_sha256"]
            for key,pin in native_pins.items():
                normalized=key.replace("\\","/")
                if normalized in pins and pins[normalized]!=pin:raise ValueError("Conflicting native host-path alias")
                pins[normalized]=pin
            if name in pins:raise ValueError("Own old acceptance must not be an arithmetic input")
            missing=[]
            for key,pin in pins.items():
                try:record(sources,key,pin)
                except FileNotFoundError:missing.append(dict(path=key,sha256=pin))
            if directory+"/replay.py"not in pins:raise ValueError("Native script is in the full original source closure")
            source=record(sources,directory+"/replay.py",pins[directory+"/replay.py"])
            tree=ast.parse(source)
            controls=[]
            if old is not None:controls=old["negative_controls"]
            else:
                values=[n.value for n in ast.walk(tree)if isinstance(n,ast.Assign)and
                        any(isinstance(t,ast.Name)and t.id=="mutations"for t in n.targets)]
                if len(values)!=1 or not isinstance(values[0],ast.List):raise ValueError("Exact complete native INITIAL mutations")
                controls=[ast.literal_eval(n.elts[0])for n in values[0].elts]
                controls.extend(n.args[0].value for n in ast.walk(tree)if isinstance(n,ast.Call)
                    and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=="controls"
                    and n.func.attr=="append"and n.args and isinstance(n.args[0],ast.Constant)and type(n.args[0].value)is str)
                if len(controls)!=27 or len(set(controls))!=27:raise ValueError("Every original INITIAL7_9 control")
            parents.append(dict(job_id=job_id,kind=kind,directory=directory,arguments=args,output=output,
                source_files_sha256=pins,reference=dict(path=name,sha256=graph[name],native_answer=old,bytes_available=old is not None),
                native_controls=controls,conditional_receipt_inputs=[key for key in pins if key.endswith("REPLAY_CHECKED.json")],
                missing_archived_inputs=missing,original_runtime_source_closure_complete=not missing,
                fresh_parent_metadata_epoch_required=bool(missing),
                parent_acquisitions_verified=False,all_index_conclusion_verified=False))
        for band in("B0","BN","B2"):
            parent("initial","n6.initial."+band,"work/cutoff6_20261018/root/initial6_accept_v1",[band],band+"/REPLAY_CHECKED.json")
            parent("resource","n6.resource."+band,"work/cutoff6_20261018/root/resource6_accept_v1",[band],band+"/REPLAY_CHECKED.json")
        parent("initial","n6.initial.outer.BN","work/cutoff6_20261018/root/initial6_outer_accept_v1",["BN"],"BN/REPLAY_CHECKED.json")
        for n in range(7,10):
            for band in("B0","BN","B2"):
                case=f"n{n}_{band}"
                parent("initial",f"n{n}.initial.{band}","work/cutoff6_20261018/analytic/initial7_9_accept_v1",[str(n),band],case+"/REPLAY_CHECKED.json")
                parent("resource",f"n{n}.resource.{band}","work/cutoff6_20261020/entry/resource7_9_accept_v2",[str(n),band],case+"/REPLAY_CHECKED.json")
        # Exact source-selected local acquisitions. These are separate from
        # the baseline whole100-panel resource jobs, never substituted for them.
        for case in("B040","BN42lower"):
            parent("local_resource","n6.refined."+case,"work/cutoff6_20261018/root/refined_resource6_accept_v2",[case],case+"/REPLAY_CHECKED.json")
        for i in range(34,49):
            case=f"BN{i:03}"
            parent("local_resource","n6.refined."+case,"work/cutoff6_20261020/root/BN_resource_accept_v1",[case],case+"/REPLAY_CHECKED.json")
        panel_outputs=sorted({name for row in parents for name in row["conditional_receipt_inputs"]
                              if name.startswith("work/cutoff6_20261018/analytic/panel_accept_v1/")})
        for name in panel_outputs:
            case=name.rsplit("/",2)[1]
            parent("local_initial","n6.panel."+case,"work/cutoff6_20261018/analytic/panel_accept_v1",[case],case+"/REPLAY_CHECKED.json")
        totals=dict(forests=len(rows),roots=sum(r["candidate_census"]["roots"]for r in rows),
            nodes=sum(r["candidate_census"]["nodes"]for r in rows),leaves=sum(r["candidate_census"]["leaves"]for r in rows))
        if totals!=dict(forests=284,roots=2362,nodes=511816,leaves=257089):raise ValueError("Exact complete final selected census")
        d=dict(schema="FINITE69_SELECTED_SOURCE_CATALOG_V1",snapshot_sha256=snapshot,
            assets=[dict(name=a.name,bytes=a.size,sha256=a.sha256)for a in(original.CUTOFF6,original.COMBINED)],
            final_selection=dict(path=original.FINAL,sha256=original.FINAL_SHA),jobs=rows,source_files=files,
            support=support,census=totals,parent_jobs=parents,
            selected_contract_parent_references=[dict(path=n,sha256=graph[n],used_by=using)for n,using in sorted(resource_references.items())],
            remaining_obligations=["Complete selected INITIAL/resource/Fourier/HIGH parent runtime catalog",
                "Fresh same-witness acquisition and resource-to-count semantic joins",
                "Global predecessor/contact/analytic/literature premises and final regional composition"],
            arithmetic_computed=False,parent_acquisitions_verified=False,full_finite69_verified=False,all_index_conclusion_verified=False)
        pin=dump(ROOT/"proof/finite69_sources_catalog.json",d)
        print(json.dumps(dict(catalog_sha256=pin,snapshot_sha256=snapshot,census=totals,
            files=len(files),source_bytes=sum(r["bytes"]for r in files.values()),contract_parent_references=len(resource_references),
            parents=len(parents),arithmetic_computed=False)),flush=True)


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--old-root",type=Path,required=True)
    p.add_argument("--cutoff6",type=Path,required=True);p.add_argument("--combined",type=Path,required=True);a=p.parse_args()
    build(a.old_root,a.cutoff6,a.combined)
