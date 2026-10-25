"""Revalidate completed C5 arithmetic exports without importing any kernel."""
from __future__ import annotations
from fractions import Fraction
import importlib.util
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys

from . import n5_remaining_sources as src

SCHEMA="COMPLETED_CONDITIONAL_N5_REMAINING_STAGE_V1"
OBSERVED="OBSERVED_CONDITIONAL_N5_REMAINING_STAGE_V1"
SCOPE="SELECTED_N5_ARITHMETIC_BASIC_CURRENT_EXEC_PEAK64_RESOURCE_EPOCH_V2"
CPU_SECONDS=43200
WALL_SECONDS=54000
MEMORY_BYTES=2048*src.MIB


def metadata_module(name):
    """Load a pinned stdlib-only source/JSON adapter, never a math module."""
    import importlib
    src.need(name in("c5_initial_one","c5_acquisition_plan","c5_resources_arithmetic","c5_resource_accept_port"),"Fixed metadata-only adapter")
    directory=src.VENDOR/"reproduction/all_indices";before=sys.path[:]
    closure=("c5_counts","c5_inputs","c5_high_one","c5_acquisition_plan","c5_initial_one",
             "c5_resources_arithmetic","c5_resource_accept_port","stable_guard","supervised")
    if any(key in sys.modules and Path(getattr(sys.modules[key],"__file__","")).resolve()!=
           (directory/(key+".py")).resolve()for key in closure):
        for key in closure:sys.modules.pop(key,None)
    previous_bytecode=sys.dont_write_bytecode
    try:
        # A notebook kernel normally has no -B flag. Set this before get_code:
        # assigning it inside a loaded adapter is too late to prevent that
        # adapter's own .pyc from contaminating the immutable snapshot.
        sys.dont_write_bytecode=True
        sys.path.insert(0,str(directory));module=importlib.import_module(name)
        src.need(Path(module.__file__).resolve()==(directory/(name+".py")).resolve(),"Actual pinned metadata adapter import")
        return module
    finally:
        sys.path[:]=before
        sys.dont_write_bytecode=previous_bytecode


def context_equal(task,original,recorded,expected):
    """Compare metadata, mapping only path values under this one original root."""
    if type(expected)is dict:
        return type(recorded)is dict and recorded.keys()==expected.keys()and all(context_equal(task,original,recorded[k],v)for k,v in expected.items())
    if type(expected)is list:
        return type(recorded)is list and len(recorded)==len(expected)and all(context_equal(task,original,a,b)for a,b in zip(recorded,expected))
    if type(expected)is str and Path(expected).is_absolute():
        # Only actual absolute paths inside the relocated task are interpreted.
        try:
            Path(expected).relative_to(task)
        except ValueError:pass
        else:return mapped(task,recorded,original)==Path(expected)
    return type(recorded)is type(expected)and recorded==expected


def implementation():
    names=("n5_remaining.py","n5_remaining_sources.py","n5_remaining_evidence.py",
           "n5_remaining_bridge.py","linux_supervisor.py","colab_batch.py")
    return {name:src.digest(src.ROOT/"be_replay"/name)for name in names}|{
        "catalog":src.CATALOG_SHA256,"supervisory_snapshot":src.SNAPSHOT_SHA256,"resource_policy":src.RESOURCE_POLICY}


LEGACY_METADATA_READER_SHA256="c18d64bbd0691d90c7a89e359e659e2cbb6cc8d856149ce038cae37b5cf655b5"
PRIOR_METADATA_IMPORT_READER_SHA256="85d110e15645fd7fdc3b0793177397c9e18f47348f2d76ab66afdaee87b76b72"


def compatible_implementation(value):
    """Exact prior metadata readers; numerical/source/guard/controller pins unchanged."""
    current=implementation()
    return value==current or any(value==dict(current,**{"n5_remaining_evidence.py":pin})
        for pin in(LEGACY_METADATA_READER_SHA256,PRIOR_METADATA_IMPORT_READER_SHA256))


def mapped(task, value, original):
    src.need(type(value)is str and value and type(original)is str,"Literal recorded originating path")
    cls=PureWindowsPath if re.match(r"^[A-Za-z]:",original)else PurePosixPath
    p,root=cls(value),cls(original)
    src.need(p.is_absolute()and root.is_absolute(),"Absolute original execution context")
    try:relative=p.relative_to(root)
    except ValueError:raise ValueError("Evidence path leaves its one original task root")
    src.need(relative.parts and all(x not in(".","..")for x in relative.parts),"Contained original evidence path")
    result=Path(task).joinpath(*relative.parts)
    for parent in [result,*result.parents]:
        if parent==Path(task).parent:break
        src.ordinary(parent)
    return result


def command(request,row,python):
    root=request["original_task_root"]
    cls=PureWindowsPath if re.match(r"^[A-Za-z]:",root)else PurePosixPath
    runtime=cls(root)/"runtime"
    entry=runtime/"reproduction/all_indices"/row["entry"]
    args=["--work",str(runtime/"work/count-candidate")]if row["kind"]=="count"else ["--cache",request["source_cache"],*row["arguments"]]
    return [python,"-B","-S",str(entry),*args]


def inventory(task):
    out={}
    for p in sorted(Path(task).rglob("*")):
        src.ordinary(p)
        if p.is_file()and p.relative_to(task).as_posix() not in("STAGE_OBSERVED.json","STAGE_COMPLETED.json"):
            out[p.relative_to(task).as_posix()]=dict(bytes=p.stat().st_size,sha256=src.digest(p))
    return out


def terminal(text):
    lines=[line for line in text.splitlines()if line.strip()]
    src.need(lines,"Actual successful stage stdout")
    import json
    return json.loads(lines[-1],object_pairs_hook=src.unique)


def _file(task,original,path,pin):
    p=mapped(task,path,original)
    src.need(p.is_file()and src.digest(p)==pin,"Actual unchanged referenced arithmetic result")
    return p,src.read(p)


def _pins(base,pins,expected):
    known=src.catalog()["source_cache_files"]
    src.need(type(pins)is dict and pins and pins==expected,"Exact complete source-selection dictionary")
    for name,pin in pins.items():
        normal=name.replace("\\","/");src.parts(normal)
        src.need(normal in known and known[normal]["sha256"]==pin,"Source commitment matches pinned original catalog")
        p=base.joinpath(*src.parts(normal))
        src.need(p.is_file()and src.digest(p)==pin,"Actual mirrored original mathematical source")


def json_suffix(text):
    decoder=json.JSONDecoder(object_pairs_hook=src.unique)
    positions=[0]+[m.end()for m in re.finditer("\n",text)]
    for pos in positions:
        if not text[pos:].startswith("{"):continue
        try:value,end=decoder.raw_decode(text,pos)
        except ValueError:continue
        if not text[end:].strip():return value
    raise ValueError("Complete original JSON object at end of actual native stdout")


def _native_graph(base,native,keys,static):
    pins=native["files_sha256"]
    canonical={}
    for name,pin in pins.items():
        normal=name.replace("\\","/")
        src.need(normal not in canonical or canonical[normal]==pin,"Consistent host-native metadata path aliases")
        canonical[normal]=pin
    src.need(sorted(canonical)==keys,"Every exact original native source/capture commitment")
    for name,pin in pins.items():
        normal=name.replace("\\","/");p=base.joinpath(*src.parts(normal));src.ordinary(p)
        src.need(p.is_file()and src.digest(p)==pin,"Actual full native source/capture graph")
        if normal in static:src.need(pin==static[normal],"Unchanged catalog-bound native mathematical input")


def _capture(task,original,base,capture,directory,command,inputs,log, *,workspace=False):
    meta=src.read(capture/"metadata.json")
    src.need(type(meta["returncode"])is int and meta["returncode"]==0 and
             meta["command"]==command and mapped(task,meta["cwd"],original)==directory,
             "Actual exact inner command/cwd/integer-zero exit")
    if "changed_inputs"in meta:src.need(meta["changed_inputs"]==[],"No changed native capture input")
    src.need(meta["input_sha256"]==inputs,"Complete exact inner input commitment")
    for name,pin in inputs.items():
        p=base.joinpath(*src.parts(name.replace("\\","/")))if workspace else directory.joinpath(*src.parts(name))
        src.need(src.digest(p)==pin,"Every actual captured native input byte")
    for kind in("stdout","stderr"):
        p=capture/(kind+".txt");src.ordinary(p)
        src.need(p.is_file()and p.stat().st_size<=16*src.MIB and src.digest(p)==meta[kind+"_sha256"],"Actual inner capture SHA")
    src.need((capture/"stderr.txt").stat().st_size==0,"Empty actual successful inner stderr")
    src.need(src.digest(capture/"stdout.txt")==src.digest(log),"Native stdout agrees with the original runner's actual log")
    return meta


def _local_inputs(base,directory,source_pins,construct_log=None):
    prefix=directory.relative_to(base).as_posix()+"/"
    result={name[len(prefix):]:pin for name,pin in source_pins.items()
            if name.startswith(prefix)and "/"not in name[len(prefix):]}
    src.need(result,"Complete local original native source inputs")
    if construct_log is not None:
        result["CONSTRUCTED.json"]=src.digest(directory/"CONSTRUCTED.json")
        result[construct_log.name]=src.digest(construct_log)
    return result


def _integration_pair(task,original,base,directory,source_pins,prefix,python, *,high=False):
    records=[];construct_log=None
    for action,output in(("construct","CONSTRUCTED.json"),("replay","REPLAY.json")):
        capture=base/"runs/cutoff5_20261020/high"/(prefix+"_"+action+"01")
        label=prefix.replace("_","-")+"-"+action
        log=directory/(label+".stdout.txt")
        argv=[python,"-B","bound.py",output]if high else [python,"-B","protocol.py",action,"PLAN.json",output]
        inputs=_local_inputs(base,directory,source_pins,construct_log)
        _capture(task,original,base,capture,directory,argv,inputs,log)
        records.append(dict(action=action,metadata_sha256=src.digest(capture/"metadata.json"),result_sha256=src.digest(directory/output)))
        if action=="construct":construct_log=log
    return records


def _resource_ports(task,original,base,row,d,python):
    selection=row["selection"];pins=row["source_selection"]["source_files_sha256"]
    request_path=base/"RESOURCE_REQUEST.json";request=src.read(request_path);request_sha=src.digest(request_path)
    adapter=base/"c5_resource_accept_port.py";adapter_sha=src.digest(src.VENDOR/"reproduction/all_indices/c5_resource_accept_port.py")
    src.need(src.digest(adapter)==adapter_sha and request["job"]==selection and request["source_files_sha256"]==pins
             and request["adapter_sha256"]==adapter_sha,"Exact fresh resource request/adapter/complete selection")
    directory=base/selection["directory"]
    capture=base/selection["capture"]
    src.need(mapped(task,d["real_replay_capture"],original)==capture and
             src.digest(capture/"metadata.json")==d["real_replay_metadata_sha256"],"Original actual replay metadata commitment")
    # This frozen module is a stdlib-only AST/metadata adapter. transform()
    # parses original source and returns a whitelist report; no native AST is
    # compiled or executed by evidence validation.
    port=metadata_module("c5_resource_accept_port")
    for stage in("replay","accept"):
        script=directory/(stage+".py")
        _,edits=port.transform(script.read_bytes(),selection["family"],stage)
        expected_command=[python,"-B","-S",str(adapter),"--request",str(request_path),"--request-sha256",request_sha,"--stage",stage]
        # Preserve recorded absolute paths when validating a relocated export.
        recorded=d["actual_os_"+stage+"_command"]
        src.need(recorded[:3]==expected_command[:3]and recorded[4]=="--request"and recorded[6:]==expected_command[6:]
                 and mapped(task,recorded[3],original)==adapter and mapped(task,recorded[5],original)==request_path,
                 "Actual original resource metadata-port invocation")
        report_path=base/("PORT_"+stage.upper()+"_REPORT.json");report=src.read(report_path)
        src.need(src.digest(report_path)==d[stage+"_source_port_report_sha256"]and report==d[stage+"_source_port_report"]
                 and report["stage"]==stage and report["original_source_sha256"]==src.digest(script)
                 and report["adapter_sha256"]==adapter_sha and report["request_sha256"]==request_sha
                 and report["exact_ast_transforms"]==edits
                 and report["scope"]=="NEW_METADATA_ONLY_SOURCE_PORT_NOT_UNCHANGED_NATIVE_WINDOWS_EXECUTION"
                 and report["original_source_bytes_modified"]is False and report["old_json_or_hashes_modified"]is False
                 and report["mathematical_expressions_and_all_native_negative_controls_unchanged"]is True
                 and report["fresh_parent_fact_joins_verified"]is False and report["all_index_conclusion_verified"]is False,
                 "Every exact original permitted metadata AST change and actual port report")
        log=directory/("resource-native-"+stage+".stdout.txt")
        last=terminal(log.read_text("utf-8"))
        src.need(last["event"]=="resource_metadata_source_port_completed"and last["stage"]==stage
                 and mapped(task,last["report"],original)==report_path,"Original port stdout identifies the actual report")
        if stage=="replay":
            inputs={name.rsplit("/",1)[-1]:pin for name,pin in pins.items()if name.rsplit("/",1)[0]==selection["directory"]}
            meta=_capture(task,original,base,capture,directory,recorded,inputs,log)
            src.need(meta["source_semantic_command"]==[python,"-B","replay.py",*selection["arguments"]]
                     and meta["source_semantic_command_is_os_command"]is False and meta["adapter_sha256"]==adapter_sha
                     and meta["request_sha256"]==request_sha and meta["source_port_report_sha256"]==src.digest(report_path)
                     and meta["original_script"]==selection["directory"]+"/replay.py"
                     and meta["original_script_sha256"]==pins[selection["directory"]+"/replay.py"]
                     and meta["result_sha256"]==d["replay_sha256"],"Actual replay capture/semantic-reference/source-port binding")


def _coarse(task,original,base,row,packet,python):
    directory=base/"work/cutoff6_20261018/fourier/auxiliary5_v2"
    review=base/"work/cutoff6_20261018/audit/auxiliary5_readback_v1"
    plan=base/"runs/cutoff6_20261018/fourier/auxiliary5_v2/plan01/PLAN.json"
    result=review/"RESULT.json";d=src.read(result)
    src.need(mapped(task,packet["native_receipt"],original)==result and packet["sha256"]==src.digest(result),
             "Actual exact independent coarse readback path and SHA")
    manifest=src.read(directory/"MANIFEST.json");inputs=dict(manifest["files_sha256"])
    inputs[(directory/"MANIFEST.json").relative_to(base).as_posix()]=src.digest(directory/"MANIFEST.json")
    inputs[plan.relative_to(base).as_posix()]=src.digest(plan)
    request=dict(plan=plan.relative_to(base).as_posix(),plan_sha256=src.digest(plan),
                 manifest_sha256=src.digest(directory/"MANIFEST.json"),output=result.relative_to(base).as_posix())
    graph=dict(manifest["files_sha256"])
    for action in("construct","replay"):
        capture=base/"runs/cutoff6_20261018/fourier/auxiliary5_v2"/(action+"01")
        meta=src.read(capture/"metadata.json");argv=meta["command"]
        src.need(len(argv)==6 and argv[:4]==[python,"-B","protocol.py",action]
                 and mapped(task,argv[4],original)==plan and mapped(task,argv[5],original)==capture/"RESULT.json",
                 "Exact coarse native action and absolute plan/result context")
        _capture(task,original,base,capture,directory,argv,inputs,directory/("owncap-coarse-"+action+".stdout.txt"),workspace=True)
        src.need(meta["scope"]=="NEW_ACTUAL_GUARDED_NATIVE_EXECUTION"and
                 meta["RESULT.json_sha256"]==src.digest(capture/"RESULT.json"),"Actual fresh full coarse integration result")
        request[action+"_capture"]=capture.relative_to(base).as_posix()
        request[action+"_metadata_sha256"]=src.digest(capture/"metadata.json")
        for name in("metadata.json","RESULT.json","stdout.txt","stderr.txt"):
            p=capture/name;graph[p.relative_to(base).as_posix()]=src.digest(p)
    request_path=review/"FRESH_REQUEST.json"
    src.need(src.read(request_path)==request,"Complete exact fresh coarse readback request")
    for p in(directory/"MANIFEST.json",plan,request_path,review/"readback.py",review/"REVIEW.txt"):
        graph[p.relative_to(base).as_posix()]=src.digest(p)
    src.need(d["files_sha256"]==graph and json_suffix((review/"owncap-coarse-readback.stdout.txt").read_text("utf-8"))
             =={k:v for k,v in d.items()if k!="files_sha256"},"Every actual coarse source/capture byte and native stdout")
    src.need(d["status"]=="PASS_INDEPENDENT_GLOBAL_AUXILIARY5_READBACK"and d["n"]==[5]
             and type(d["n"][0])is int and d["strips"]==d["exact_rows"]==87 and d["negative_controls"]==24
             and d["finite_rho"]==["1","19/10"]and d["target"]=="429/1000"
             and d["actual_support_acquired"]is False and d["cutoff6_proved"]is False
             and Fraction(d["uniform_upper"])<Fraction(429,1000),"Complete original global coarse87-strip readback")
    for name,pin in manifest["files_sha256"].items():
        src.need(row["source_files_sha256"].get(name)==pin,"Exact catalog-bound coarse mathematical source")
    return d


def summarize(task,row,packet,original,python=None):
    """Check concrete native receipts after the source-bound observed exit."""
    kind=row["kind"];references=[];summary=dict(kind=kind)
    python=python or packet.get("python_executable")
    def ref(path,pin):
        p,d=_file(task,original,path,pin)
        references.append(dict(path=p.relative_to(task).as_posix(),sha256=pin))
        return p,d
    if kind=="count":
        p=Path(task)/"runtime/work/count-candidate/capsule/COUNT_ACCEPTED.json";d=src.read(p)
        src.need(packet["event"]=="fresh_native_count_process_completed"and
                 mapped(task,packet["receipt"],original)==p,"Actual original count supervisor receipt")
        src.need(d["status"]==row["expected_status"]and type(d["n"])is int and d["n"]==5
                 and type(d["index"])is int and d["index"]==row["index"],"Exact full selected count scope")
        files=row["source_files"]
        for key,name in (("forest_sha256","COUNT_FOREST.json"),("checker_sha256","count_protocol.py"),("contract_sha256","contract.json")):
            src.need(d[key]==files[name],"Count receipt binds actual selected source/candidate")
        src.need(d["kernel_sha256"]==src.read(p.parent/"KERNEL_COPY_MANIFEST.json")["files"],"All frozen numerical kernel pins")
        for key in("nodes","leaves","maximum_depth"):
            src.need(type(d["statistics"][key])is int and d["statistics"][key]==row["census"][key],"Complete structural count census")
        src.need(type(d["fresh_leaf_evaluations"])is int and d["fresh_leaf_evaluations"]==row["census"]["leaves"]
                 and d["negative_controls"]==row["negative_controls"],"All fresh leaf evaluations and complete original controls")
        src.need(json_suffix((p.parent.parent/"c5-count-native.stdout.txt").read_text("utf-8"))==d,
                 "Actual original native stdout equals the entire accepted count object")
        references.append(dict(path=p.relative_to(task).as_posix(),sha256=src.digest(p)))
        summary.update(index=row["index"],**row["census"],negative_controls=len(d["negative_controls"]))
    elif kind=="initial":
        src.need(packet["job_id"]==row["job_id"]and packet["fresh_arithmetic"]is True
                 and packet["fresh_parent_fact_joins_verified"]is False
                 and packet["all_index_conclusion_verified"]is False,"Complete conditional INITIAL output")
        path,d=ref(packet["report_path"],src.digest(mapped(task,packet["report_path"],original)))
        src.need(d==packet,"Actual saved and printed INITIAL report agree")
        _pins(path.parent,d["source_files_sha256"],row["source_selection"]["source_files_sha256"])
        _,native=ref(d["native_result_path"],d["native_result_sha256"])
        _native_graph(path.parent,native,row["native_source_keys"],row["source_selection"]["source_files_sha256"])
        selection=row["selection"]
        src.need(native["status"]==selection["expected_status"]and type(native["n"])is int and native["n"]==5
                 and native["band"]==selection["band"]and native["negative_controls"]==row["negative_controls"],"Original INITIAL controls/scope")
        for key,value in(("stages",selection["stages"]),("total_cells_per_stage",2592),("panels",100)):
            src.need(type(native[key])is int and native[key]==value,"Full original INITIAL stage/cell/panel inventory")
        src.need(type(native["final_active"])is int and type(native["final_gap_active"])is int
                 and 0<=native["final_active"]==native["final_gap_active"]<=2592,"Every active final cell is gap licensed")
        prepared=src.catalog()["source_cache_files"][selection["prepared"]]["sha256"]
        src.need(prepared==row["source_selection"]["prepared_sha256"],"Exact catalog-selected INITIAL candidate")
        src.need(native["input_sha256"]==src.digest(path.parent/selection["directory"]/selection["case"]/"INPUT.json"),
                 "Actual complete unseeded INITIAL candidate byte identity")
        capture=path.parent/"capture";directory=path.parent/selection["directory"]
        src.need(mapped(task,d["capture_path"],original)==capture and
                 d["capture_metadata_sha256"]==src.digest(capture/"metadata.json"),"Actual INITIAL capture metadata binding")
        meta=_capture(task,original,path.parent,capture,directory,[python,"-B","replay.py",*selection["arguments"]],
                      row["source_selection"]["source_files_sha256"],directory/"native-initial.stdout.txt",workspace=True)
        src.need(meta["native_result_sha256"]==d["native_result_sha256"]and
                 (capture/"stdout.txt").read_text("utf-8").splitlines()[-1].startswith(native["status"]+" "),
                 "Full native INITIAL result is bound by the original actual capture")
        plan=metadata_module("c5_acquisition_plan");adapter=metadata_module("c5_initial_one")
        job=next(j for j in plan.INITIAL_JOBS if j.job_id==row["job_id"])
        facts=adapter.validate_receipt(job,native,src.read(path.parent/selection["prepared"]),row["negative_controls"])
        facts.update(input_candidate_path=str(path.parent/selection["directory"]/selection["case"]/"INPUT.json"),
                     validated_p_export_json_pointer="/stages/"+str(selection["stages"]-1)+"/cover/panels")
        src.need(context_equal(task,original,d["facts"],facts),"Every exported INITIAL fact equals the actual native profile/domain/invariants")
        summary.update(stages=selection["stages"],cells_per_stage=2592,panels=100,negative_controls=len(row["negative_controls"]),
                       facts=d["facts"],input_sha256=native["input_sha256"])
    elif kind=="resource":
        src.need(packet["scope"]=="CONDITIONAL_RESOURCE_ARITHMETIC_ONLY"and packet["job_id"]==row["job_id"]
                 and packet["fresh_parent_fact_joins_verified"]is False and packet["register_as_c5_resources"]is False,
                 "Original arithmetic-only resource output")
        path,d=ref(packet["report"],packet["sha256"])
        _pins(path.parent,d["source_files_sha256"],row["source_selection"]["source_files_sha256"])
        selection=row["selection"];indices=selection["indices"]
        src.need(d["job_id"]==row["job_id"]and type(d["n"])is int and d["n"]==5 and
                 d["selected_probability_panels"]==indices and [r["index"]for r in d["full_canonical_resource_rows"]]==indices,
                 "Every exact selected resource panel/canonical answer")
        controls={"resource5_selected_accept_v1":(23,31),"resource5_gamma_accept_v1":(13,20),
                  "resource5_sector_accept_v1":(13,20),"resource5_B3_accept_v1":(13,22),
                  "resource5_B3_T3lower_accept_v1":(13,22)}[selection["family"]]
        accepted_controls=controls[1]+(selection["case"]=="B2_S3_endpoint")
        src.need(len(d["arithmetic_negative_controls"])==len(set(d["arithmetic_negative_controls"]))==controls[0]
                 and len(d["native_acceptance_negative_controls"])==len(set(d["native_acceptance_negative_controls"]))==accepted_controls,
                 "All original resource replay/acceptance controls")
        src.need(d["arithmetic_negative_controls"]==row["replay_negative_controls"]and
                 d["native_acceptance_negative_controls"]==row["native_negative_controls"],"Exact original resource control names")
        _,native=ref(d["native_accept_path"],d["native_accept_sha256"])
        _,replay=ref(d["replay_path"],d["replay_sha256"])
        _native_graph(path.parent,native,row["native_source_keys"],row["source_selection"]["source_files_sha256"])
        src.need(native["status"]==selection["expected_status"]and native["resource_replay_sha256"]==d["replay_sha256"]
                 and native["negative_controls"]==d["native_acceptance_negative_controls"]
                 and replay["negative_controls"]==d["arithmetic_negative_controls"],"Actual bound full native resource receipts")
        src.need(d["fresh_parent_fact_joins_verified"]is False and d["register_as_c5_resources"]is False
                 and d["parent_initial"]["historical_receipt_is_fresh_parent_proof"]is False,"Historical references are conditional")
        _resource_ports(task,original,path.parent,row,d,python)
        plan=metadata_module("c5_acquisition_plan");adapter=metadata_module("c5_resources_arithmetic")
        job=next(j for j in plan.RESOURCE_JOBS if j.job_id==row["job_id"])
        expected=adapter.summarize_job(path.parent,job,src.read(path.parent/selection["prepared"]),
            src.read(path.parent/selection["directory"]/selection["case"]/"INITIAL.json"),replay,native)
        src.need(context_equal(task,original,{k:d[k]for k in expected},expected),
                 "All resource canonical answers, predecessor references and semantic exports are recomputed from actual JSON")
        summary.update(panels=len(indices),excluded=len(d["excluded"]),retained=len(d["retained"]),
                       replay_controls=controls[0],acceptance_controls=accepted_controls,
                       semantic_report_relative=path.relative_to(task).as_posix())
    else:
        statuses={"support":"FRESH_SUPPORT_PROTOCOLS_ACCEPTED","high":"FRESH_BOTH_NATIVE_HIGH_PROTOCOLS_ACCEPTED",
                  "owncaps":"FRESH_COARSE_AND_SELECTED_OWNCAPS_ACCEPTED","complement":"FRESH_C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_ACCEPTED"}
        src.need(packet["status"]==statuses[kind]and packet["fresh_arithmetic"]is True
                 and packet["all_index_conclusion_verified"]is False,"Full original selected arithmetic component")
        if kind=="support":
            src.need([r["protocol"]for r in packet["receipts"]]==row["expected_protocols"],"All three support protocols")
            for receipt,count,expected in zip(packet["receipts"],row["rows"],row["protocols"]):
                receipt_path,d=ref(receipt["receipt"],receipt["sha256"])
                src.need(d["status"]==expected["status"]and type(d["n"])is int and d["n"]==5 and len(d["rows"])==count
                         and d["action"]=="replay"and d["q"]==d["K"]=="0"
                         and d["files_sha256"]==expected["source_files_sha256"]
                         and all(r["status"]=="CONDITIONAL_SUPPORT_PASS"for r in d["rows"]),"All complete exact support rays/rows")
                for name,pin in d["files_sha256"].items():
                    src.need(src.catalog()["source_cache_files"][name.replace("\\","/")]["sha256"]==pin,"Support candidate/source reference pin")
                    src.need(src.digest(Path(task)/"support-inputs"/name.replace("\\","/"))==pin,"Actual exported support source/candidate byte")
                log=receipt_path.parent/(receipt["protocol"].replace("_","-").lower()+".stdout.txt")
                src.need(log.read_text("utf-8").splitlines()[-1]==d["status"],"Actual unchanged support protocol terminal stdout")
            summary.update(protocols=3,rows=sum(row["rows"]))
        elif kind in("high","owncaps"):
            variants=row["variants"]if kind=="owncaps"else [v["name"]for v in row["variants"]]
            src.need([r["variant"]for r in packet["receipts"]]==variants,"Complete selected protocol variants")
            first=mapped(task,packet["receipts"][0]["native_receipt"],original)
            # All original paths have the fixed work/cutoff5/high/... suffix.
            base=first.parents[4]
            _pins(base,packet["source_files_sha256"],row["source_files_sha256"])
            for i,receipt in enumerate(packet["receipts"]):
                receipt_path,d=ref(receipt["native_receipt"],receipt["sha256"])
                expected=row["variants"][i]if kind=="high"else row["native_variants"][i]
                count=row["variants"][i]["controls"]if kind=="high"else 10
                src.need(d["status"]==expected["status"]and type(d["n"])is int and d["n"]==5
                         and d["negative_controls"]==expected["negative_controls"]
                         and len(d["negative_controls"])==len(set(d["negative_controls"]))==count,
                         "Every original HIGH/owncap native corruption control")
                directory=base/"work/cutoff5_20261020/high"/variants[i]
                src.need(receipt_path==directory/("HIGH_CHECKED.json"if kind=="high"else"OWNCAPS_CHECKED.json"),"Exact original native receipt path")
                prefix=["high5","high5_eta"][i]if kind=="high"else ["owncaps","owncap_B3_ext"][i]
                _integration_pair(task,original,base,directory,row["source_files_sha256"],prefix,python,high=kind=="high")
                _native_graph(base,d,expected["native_source_keys"],row["source_files_sha256"])
                printed=json_suffix((directory/(prefix.replace("_","-")+"-accept.stdout.txt")).read_text("utf-8"))
                omitted={"files_sha256"}if kind=="high"else {"rows","files_sha256"}
                src.need(printed=={k:v for k,v in d.items()if k not in omitted},"Original native accept stdout agrees with receipt")
                if kind=="high":src.need(len(d["rows"])==row["variants"][i]["rows"],"Every HIGH row")
                else:src.need(len(d["bands"])==[3,1][i],"All selected supported owncap bands")
            if kind=="owncaps":
                _coarse(task,original,base,row,packet["coarse_429"],python)
                summary.update(coarse_strips=87,coarse_controls=24,supported_controls=20)
            summary.update(variants=variants)
        else:
            receipt_path,d=ref(packet["receipt"],packet["sha256"]);base=receipt_path.parent
            _pins(base,packet["source_files_sha256"],row["source_files_sha256"])
            src.need(d["status"]=="PASS_FRESH_C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_ONLY"
                     and d["strips"]==41 and d["attempts"]==42 and len(d["native_controls"])==10
                     and len(d["independent_fourier_controls"])==16
                     and d["fresh_support_and_fourier_parent_joins_verified"]is False
                     and d["independent_support_controls_not_claimed"]==3,"All two-integration complement arithmetic, no missing-parent claim")
            src.need(d["native_controls"]==row["native_negative_controls"]and
                     d["independent_fourier_controls"]==row["independent_fourier_negative_controls"],"Every exact original complement control name")
            directory=base/"work/cutoff5_20261020/high/complement5_v1"
            captures=_integration_pair(task,original,base,directory,row["source_files_sha256"],"complement",python)
            src.need(d["actual_native_captures"]==captures and d["two_complete_native_integrations"]is True
                     and d["constructed_sha256"]==src.digest(directory/"CONSTRUCTED.json")
                     and d["replay_sha256"]==src.digest(directory/"REPLAY.json")
                     and d["input_document_sha256"]==src.digest(base/"COMPLEMENT_INPUTS.json"),"Both actual full complement integrations and input document")
            for record,action in zip(packet["actual_execution_captures"],("construct","replay")):
                metadata=base/"runs/cutoff5_20261020/high"/("complement_"+action+"01")/"metadata.json"
                src.need(record["action"]==action and mapped(task,record["actual_metadata"],original)==metadata
                         and record["sha256"]==src.digest(metadata),"Owning supervisor binds both actual complement captures")
            src.need(len(packet["actual_execution_captures"])==2,"Exactly two observed complement integrations")
            src.need(d["native_arithmetic_acceptor_sha256"]==src.digest(directory/"accept.py")
                     and d["independent_arithmetic_readback_sha256"]==src.digest(base/"work/cutoff5_20261020/audit/complement5_readback_v1/check.py")
                     and d["fresh_arithmetic"]is True and type(d["n"])is int and d["n"]==5
                     and d["native_full_complement_acceptance_claimed"]is False
                     and d["historical_captures_or_PASS_used_as_mathematical_premise"]is False,
                     "Unchanged complementary arithmetic sources and exact conditional execution scope")
            document=src.read(base/"COMPLEMENT_INPUTS.json")
            src.need(document["source_files_sha256"]==row["source_files_sha256"],"Complete exact complement independent replay inputs")
            worker=base/"c5_complement_worker.py"
            src.need(src.digest(worker)==packet["adapter_worker_sha256"]==src.digest(src.VENDOR/"reproduction/all_indices/c5_complement_worker.py"),
                     "Exact original independent Fourier arithmetic worker")
            summary.update(strips=41,attempts=42,complete_integrations=2,native_controls=10,independent_fourier_controls=16,
                           independent_support_controls_not_claimed=3)
    summary["references"]=references
    return summary


def validate_run(task, row, report):
    task=Path(task);request=src.verify_job(task,row);original=request["original_task_root"]
    src.need(report["schema"]==OBSERVED and report["scope"]==SCOPE and report["job_id"]==row["job_id"]
             and compatible_implementation(report["implementation"])and report["original_task_root"]==original
             and report["conditional_arithmetic_completed"]is False
             and report["native_arithmetic_accepted"]is False and report["full_n5_verified"]is False
             and report["fresh_parent_fact_joins_verified"]is False and report["all_index_conclusion_verified"]is False,
             "Observed false-to-completed stage transition and exact current implementation")
    observed=report["observed"]
    src.need(observed.get("status")=="completed"and type(observed.get("returncode"))is int and observed["returncode"]==0
             and observed.get("reason")is None and observed.get("proof_accepted")is False,"Actual successful BASIC execution")
    stored=src.read(task/"execution/supervisor-result.json")
    src.need(stored==observed,"Actual stopped supervisor receipt, not a copied terminal marker")
    launch=src.read(task/"execution/launch.json");python=report["python_executable"]
    src.need(launch["argv"]==command(request,row,python)and mapped(task,launch["cwd"],original)==task/"runtime"
             and mapped(task,launch["output_dir"],original)==task/"execution"
             and observed["mode"]=="untrusted_search"and type(observed["sample_count"])is int and observed["sample_count"]>0
             and launch["mode"]=="untrusted_search"and type(report["cpu_seconds"])is int and report["cpu_seconds"]==CPU_SECONDS
             and type(report["wall_seconds"])is int and report["wall_seconds"]==WALL_SECONDS
             and type(report["memory_bytes"])is int and report["memory_bytes"]==MEMORY_BYTES
             and launch["cpu_seconds"]==CPU_SECONDS and launch["wall_seconds"]==WALL_SECONDS and launch["memory_bytes"]==MEMORY_BYTES
             and launch["disk_bytes"]==512*src.MIB and launch["log_bytes"]==16*src.MIB
             and launch["heartbeat_seconds"]==20 and launch["sample_seconds"]==.2 and launch["checkpoint_paths"]==[],
             "Exact actual original job command and explicit BASIC budgets")
    guard=observed["guard_scope"]
    src.need(guard==dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",proof_acceptance=False,
             external_wall_seconds=WALL_SECONDS,per_process_RLIMIT_AS_bytes=MEMORY_BYTES,
             per_process_RLIMIT_CPU_seconds=CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,
             sampled_group_RSS_limit_bytes=MEMORY_BYTES,sampled_group_CPU_limit_seconds=CPU_SECONDS,
             sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,
             descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False),
             "Exact honest BASIC resource contract, without cgroup/native promotion")
    paths={}
    for kind in("stdout","stderr"):
        p=mapped(task,observed[kind+"_path"],original)
        src.need(p==task/"execution"/(kind+".txt")and p.is_file()and p.stat().st_size<=16*src.MIB
                 and src.digest(p)==observed[kind+"_sha256"],"Actual bounded "+kind+" capture and supervisor SHA")
        paths[kind]=p
    src.need(paths["stderr"].stat().st_size==0,"Empty successful original supervisor stderr")
    packet=terminal(paths["stdout"].read_text("utf-8"))
    return summarize(task,row,packet,original,python)


def validate_completed(task, *, original_task_root=None):
    task=Path(task);request=src.verify_job(task);row=src.job(request["job_id"])
    src.need(original_task_root is None or str(original_task_root)==request["original_task_root"],"One explicit originating task root")
    observed=src.read(task/"STAGE_OBSERVED.json");complete=src.read(task/"STAGE_COMPLETED.json")
    summary=validate_run(task,row,observed)
    src.need(complete["schema"]==SCHEMA and complete["job_id"]==row["job_id"]and complete["scope"]==SCOPE
             and compatible_implementation(complete["implementation"])and complete["implementation"]==observed["implementation"]
             and complete["observed_sha256"]==src.digest(task/"STAGE_OBSERVED.json")
             and complete["conditional_arithmetic_completed"]is True and complete["summary"]==summary
             and complete["artifacts"]==inventory(task),"Complete unmodified stage, full source/receipt/capture inventory")
    for flag in("native_arithmetic_accepted","fresh_parent_fact_joins_verified","full_n5_verified","all_index_conclusion_verified"):
        src.need(complete[flag]is False,"No conditional arithmetic-to-theorem promotion")
    return dict(schema="REVALIDATED_CONDITIONAL_N5_REMAINING_STAGE_V1",job_id=row["job_id"],kind=row["kind"],
                summary=summary,catalog_sha256=src.CATALOG_SHA256,stage_result_sha256=src.digest(task/"STAGE_COMPLETED.json"),
                conditional_arithmetic_completed=True,native_arithmetic_accepted=False,
                fresh_parent_fact_joins_verified=False,full_n5_verified=False,all_index_conclusion_verified=False)
