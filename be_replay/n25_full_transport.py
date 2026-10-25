"""Pure stopped-execution transport checks for full66's new source epochs.

This module checks actual files, limits and command identity. It does not
interpret a numerical result or turn BASIC execution into native acceptance.
"""
from __future__ import annotations
import math
from pathlib import Path
import re
from . import count_task as common
from .n25_count_evidence import same,path_class,relative,guard_files

MIB=1024**2
MEMORY=2048*MIB
CEILING=82800
need=common.need


def ordinary(path, *, directory=False, limit=None):
    path=Path(path)
    need(not path.is_symlink() and not (hasattr(path,"is_junction") and path.is_junction()),"No linked evidence paths")
    for parent in path.parents:
        need(not parent.is_symlink() and not (hasattr(parent,"is_junction") and parent.is_junction()),"No linked evidence ancestors")
    need(path.is_dir() if directory else path.is_file(),"Existing regular evidence artifact")
    if limit is not None:need(path.stat().st_size<=limit,"Bounded regular evidence artifact")
    return path


def policy(launch, *, native):
    cpu,wall=launch["cpu_seconds"],launch["wall_seconds"]
    need(type(cpu) is int and 2<=cpu<=CEILING
         and type(wall) in (int,float) and math.isfinite(wall) and 0<wall<=CEILING,
         "Explicit at-most23-hour CPU and wall policy")
    need(launch["mode"]==("trusted_native" if native else "untrusted_search")
         and type(launch["memory_bytes"]) is int and launch["memory_bytes"]==MEMORY
         and type(launch["disk_bytes"]) is int and launch["disk_bytes"]==256*MIB
         and type(launch["log_bytes"]) is int and launch["log_bytes"]==16*MIB,
         "Exact2GiB,256MiB disk,16MiB captures and execution mode")
    if native:
        controller=min(30,max(1,cpu//10))
        need(all(type(launch[k]) is int and launch[k]==v for k,v in dict(
            supervisor_memory_bytes=64*MIB,worker_memory_bytes=MEMORY-64*MIB,
            supervisor_cpu_seconds=controller,worker_cpu_seconds=cpu-controller).items())
            and launch["checkpoint_paths"]==[],"Exact native worker/controller hard-cap split")
    return cpu,wall


def trusted_guard(observed,launch,script_sha,supervisor_sha):
    cpu,_=policy(launch,native=True)
    need(type(observed) is dict and observed.get("status")=="completed"
         and type(observed.get("returncode")) is int and observed["returncode"]==0
         and observed.get("mode")=="trusted_native" and observed.get("proof_accepted") is False,
         "Stopped successful native result with no supervisor proof claim")
    scope=observed["guard_scope"]
    controller=min(30,max(1,cpu//10))
    caps=dict(hard_sum_RLIMIT_AS_bytes=MEMORY,worker_RLIMIT_AS_bytes=MEMORY-64*MIB,
        supervisor_RLIMIT_AS_bytes=64*MIB,hard_sum_RLIMIT_CPU_seconds=cpu,
        supervisor_RLIMIT_CPU_seconds=controller,worker_RLIMIT_CPU_seconds=cpu-controller)
    need(scope.get("kind")=="LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1"
        and scope.get("capability_established") is True and scope.get("native_python_execution") is True
        and all(type(scope.get(k)) is int and scope[k]==v for k,v in caps.items())
        and scope.get("script_sha256")==script_sha and scope.get("supervisor_source_sha256")==supervisor_sha,
        "Actual single-process seccomp capability and bound source/limit policy")


def group_scope(launch):
    return dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",proof_acceptance=False,
        external_wall_seconds=launch["wall_seconds"],per_process_RLIMIT_AS_bytes=launch["memory_bytes"],
        per_process_RLIMIT_CPU_seconds=launch["cpu_seconds"],aggregate_kernel_memory_limit=False,
        aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=launch["memory_bytes"],
        sampled_group_CPU_limit_seconds=launch["cpu_seconds"],sampled_file_limit_bytes=launch["disk_bytes"],
        sampled_log_limit_bytes=launch["log_bytes"],descendants_changing_session_are_contained=False,
        equivalent_to_Windows_Job_or_cgroup=False)


def context(task,execution,observed,original_task_root=None):
    """Map original absolute paths without changing any captured receipt byte."""
    task,execution=Path(task).resolve(),Path(execution).resolve()
    rel=execution.relative_to(task)
    cls=path_class(observed["stdout_path"])
    recorded=cls(observed["stdout_path"])
    need(recorded.is_absolute() and recorded.name=="stdout.txt" and ".." not in recorded.parts,
         "Absolute original stdout context")
    original=recorded.parent
    for part in reversed(rel.parts):
        need(original.name==part,"Exact relocated execution path suffix")
        original=original.parent
    need(original_task_root is None or cls(str(original_task_root))==original,
         "Explicit original task context agrees with actual capture")
    return original


def validate(task,execution,observed,*,script_relative,args,cwd_relative,native,original_task_root=None):
    """Validate actual source command, stopped sidecars and complete captures."""
    task=ordinary(task,directory=True).resolve()
    execution=ordinary(execution,directory=True).resolve()
    execution.relative_to(task)
    need(type(script_relative) is str and type(cwd_relative) is str
         and type(args) is list and all(type(v) is str for v in args),"Explicit literal current action command")
    script=ordinary(task/script_relative,limit=8*MIB)
    cwd=ordinary(task/cwd_relative,directory=True)
    script.resolve().relative_to(cwd.resolve())
    original=context(task,execution,observed,original_task_root)
    actual=common.read(execution/"supervisor-result.json",4*MIB)
    need(same(actual,observed) and actual["status"]=="completed"
         and type(actual["returncode"]) is int and actual["returncode"]==0
         and actual["mode"]==("trusted_native" if native else "untrusted_search")
         and actual["proof_accepted"] is False,"Actual stopped successful execution is transport only")
    launch=common.read(execution/("native-launch.json" if native else "launch.json"),MIB)
    policy(launch,native=native)
    argv=launch["argv"]
    need(type(argv) is list and len(argv)==4+len(args) and all(type(v) is str for v in argv)
        and path_class(argv[0])(argv[0]).is_absolute() and argv[1:3]==["-B","-S"]
        and relative(argv[3],original)==Path(script_relative) and argv[4:]==args
        and relative(launch["cwd"],original)==Path(cwd_relative)
        and relative(launch["output_dir"],original)==execution.relative_to(task),
        "Exact source-relative action command, working directory and capture location")
    if native:
        outer=common.read(execution/"launch.json",MIB);command=outer["argv"]
        need(type(command) is list and len(command)==6 and command[:3]==argv[:3]
            and path_class(command[3])(command[3]).is_absolute()
            and path_class(command[3])(command[3]).name=="linux_supervisor.py"
            and command[4]=="--_native-controller"
            and relative(command[5],original)==(execution/"native-launch.json").relative_to(task)
            and same(outer,dict(launch,argv=command)),"Actual native controller launch relation")
        trusted_guard(observed,launch,common.digest(script),common.digest(Path(__file__).with_name("linux_supervisor.py")))
        guard_files(execution,observed,launch,common.digest(script))
    else:
        need(same(observed["guard_scope"],group_scope(launch)),"Exact honest BASIC process-group limits; no native/cgroup promotion")
    for kind in ("stdout","stderr"):
        path=ordinary(execution/(kind+".txt"),limit=16*MIB)
        need(relative(actual[kind+"_path"],original)==path.relative_to(task)
             and common.digest(path)==actual[kind+"_sha256"],"Complete actual capture bytes match execution hashes")
    need((execution/"stderr.txt").stat().st_size==0,"Successful original checker has empty bound stderr")
    paths=[execution/n for n in ("launch.json","supervisor-result.json","stdout.txt","stderr.txt")]
    if native:paths += [execution/n for n in ("native-launch.json","native-worker-guard.json",
        "native-controller-guard.json","native-controller-result.json")]
    return dict(schema="N25_FULL66_STOPPED_TRANSPORT_V1",mode=actual["mode"],
        native_capability_established=bool(native),original_task_root=str(original),
        evidence_sha256={p.relative_to(task).as_posix():common.digest(p) for p in paths},
        launch=launch,arithmetic_accepted=False,full66_complete=False)
