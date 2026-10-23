"""Independent new n26--30 source/transport epoch and complete80 readback.

Only the original pure receipt/geometry summarizers are reused. No mathematical
kernel is imported, no old source-adapter execution is claimed, and a completed
64 pair must still pass its independent unchanged public validator.
"""
from __future__ import annotations
import math
from pathlib import Path
import zipfile
from . import finite2630_sources as src
from . import finite1039_count_evidence as pure
from . import n27_p41_recovery_evidence as recovered
from . import n27_p41_recovery as recovery

same,mapped,command,summarize,inventory = pure.same,pure.mapped,pure.command,pure.summarize,pure.inventory
OBSERVED='OBSERVED_CONDITIONAL_FINITE2630_COUNT_V1'
COMPLETED='COMPLETED_CONDITIONAL_FINITE2630_COUNT_V1'
SCOPE='UNCHANGED_FULL_FINITE2630_WITH_IDENTICAL_RECOVERED_CANDIDATE_BASIC_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
FLAGS=('native_arithmetic_accepted','parent_acquisitions_verified','fresh_parent_fact_joins_verified',
       'full_finite1039_verified','all_index_conclusion_verified')


def implementation():
    names=('finite2630_sources.py','finite2630_counts.py','finite2630_evidence.py',
           'finite1039_sources.py','finite1039_count_evidence.py','n5_remaining_sources.py',
           'n5_remaining_bridge.py','linux_supervisor.py','colab_batch.py',
           'n27_p41_recovery.py','n27_p41_recovery_sources.py','n27_p41_recovery_evidence.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(
        selection_sha256=src.SELECTION_SHA256,original_catalog_sha256=src.old.CATALOG_SHA256,
        recovery_plan_sha256=recovery.src.PLAN_SHA256)


def validate_run(task, row, report):
    task = Path(task)
    request = src.verify_job(task, row)
    original = request["original_task_root"]
    src.need(report["schema"] == OBSERVED and report["scope"] == SCOPE and report["job_id"] == row["job_id"]
             and same(report["implementation"], implementation()) and report["original_task_root"] == original
             and report["conditional_arithmetic_completed"] is False and all(report[f] is False for f in FLAGS),
             "Exact new implementation and false observed-to-completed transition")
    observed = report["observed"]
    src.need(observed.get("status") == "completed" and type(observed.get("returncode")) is int and observed["returncode"] == 0
             and observed.get("reason") is None and observed.get("proof_accepted") is False
             and observed.get("mode") == "untrusted_search" and type(observed.get("sample_count")) is int
             and observed["sample_count"] > 0, "Actual successful stopped BASIC execution")
    for key in ("elapsed_seconds", "maximum_sampled_group_RSS_bytes", "maximum_sampled_group_CPU_seconds"):
        value = observed.get(key)
        src.need(type(value) in (int, float) and math.isfinite(value) and value >= 0,
                 "Finite original process diagnostic: "+key)
    src.need(same(src.read(task/"execution/supervisor-result.json"), observed), "Actual stopped supervisor result")
    launch = src.read(task/"execution/launch.json")
    base_fields = {"argv", "cwd", "output_dir", "mode", "wall_seconds", "cpu_seconds", "memory_bytes", "checkpoint_paths",
                   "disk_bytes", "log_bytes", "sample_seconds", "heartbeat_seconds"}
    src.need(set(launch) == base_fields and same(launch["argv"], command(request, row, report["python_executable"]))
             and mapped(task, launch["cwd"], original) == task/"capsule"/row["directory"]
             and mapped(task, launch["output_dir"], original) == task/"execution"
             and launch["mode"] == "untrusted_search" and launch["sample_seconds"] == .2 and launch["heartbeat_seconds"] == 20
             and type(launch["checkpoint_paths"]) is list and len(launch["checkpoint_paths"]) == 1
             and mapped(task, launch["checkpoint_paths"][0], original) == task/"capsule"/src.output_relative(row),
             "Actual source-specific acceptor command, cwd, output and complete stopped capture request")
    for key, value in (("cpu_seconds", CPU_SECONDS), ("wall_seconds", WALL_SECONDS), ("memory_bytes", MEMORY_BYTES)):
        allowed = (int, float) if key == "wall_seconds" else (int,)
        src.need(type(report[key]) is int and report[key] == value and type(launch[key]) in allowed and launch[key] == value,
                 "Exact documented BASIC execution budget")
    src.need(type(launch["disk_bytes"]) is int and launch["disk_bytes"] == 512*src.MIB
             and type(launch["log_bytes"]) is int and launch["log_bytes"] == 16*src.MIB, "Bounded original disk and capture policy")
    scope = dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP", proof_acceptance=False,
        external_wall_seconds=float(WALL_SECONDS), per_process_RLIMIT_AS_bytes=MEMORY_BYTES,
        per_process_RLIMIT_CPU_seconds=CPU_SECONDS, aggregate_kernel_memory_limit=False, aggregate_kernel_cpu_limit=False,
        sampled_group_RSS_limit_bytes=MEMORY_BYTES, sampled_group_CPU_limit_seconds=CPU_SECONDS,
        sampled_file_limit_bytes=512*src.MIB, sampled_log_limit_bytes=16*src.MIB,
        descendants_changing_session_are_contained=False, equivalent_to_Windows_Job_or_cgroup=False)
    src.need(same(observed["guard_scope"], scope), "Honest exact BASIC guard without a native-platform promotion")
    capture_paths = {}
    for kind in ("stdout", "stderr"):
        p = mapped(task, observed[kind+"_path"], original)
        src.need(p == task/"execution"/(kind+".txt") and p.is_file() and p.stat().st_size <= 16*src.MIB
                 and src.digest(p) == observed[kind+"_sha256"], "Actual supervisor-bound captured bytes: "+kind)
        capture_paths[kind] = p
    src.need(capture_paths["stderr"].stat().st_size == 0, "Successful original stderr is empty")
    stdout = capture_paths["stdout"].read_text("utf-8")
    result = summarize(task, row, stdout, observed, original,
                       python_executable=report["python_executable"], python_version=report["python_version"])
    src.need(src.digest(capture_paths["stdout"]) == observed["stdout_sha256"], "Actual stdout remained stable while parsing")
    return result


def validate_completed(task, *,original_task_root=None):
    task=Path(task);request=src.verify_job(task);row=src.job(request['job_id'])
    src.need(original_task_root is None or str(original_task_root)==request['original_task_root'],'One explicit originating stage root')
    observed=src.read(task/'STAGE_OBSERVED.json');complete=src.read(task/'STAGE_COMPLETED.json',limit=64*src.MIB)
    summary=validate_run(task,row,observed)
    src.need(complete['schema']==COMPLETED and complete['scope']==SCOPE and complete['job_id']==row['job_id']
             and same(complete['implementation'],observed['implementation'])
             and complete['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')
             and complete['conditional_arithmetic_completed']is True and same(complete['summary'],summary)
             and same(complete['artifacts'],inventory(task))and all(complete[f]is False for f in FLAGS),
             'Full new-epoch source/capture/receipt inventory and observed-false to completed-true transition')
    return dict(schema='REVALIDATED_CONDITIONAL_FINITE2630_COUNT_V1',job_id=row['job_id'],lane='n26_30',
                summary=summary,selection_sha256=src.SELECTION_SHA256,
                stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),
                source_manifest_sha256=src.digest(task/'SOURCES.json'),original_task_root=request['original_task_root'],
                conditional_arithmetic_completed=True,**{f:False for f in FLAGS})


def relative(root,value):
    src.need(type(value)is str,'Explicit relative artifact path')
    p=Path(root).joinpath(*src.parts(value));src.ordinary(p)
    for parent in p.parents:
        if parent==Path(root).parent:break
        src.ordinary(parent)
    return p


def validate_recovered(root):
    """Revalidate both64 actions and the exact historical-candidate identity edge."""
    root=Path(root);record=src.read(root/'RECOVERED64.json');expected=src.selection()['recovered']
    src.need(record['schema']=='IMPORTED_FULL_N27_P41_PAIR_FOR_FINITE2630_V1'
             and record['selection_sha256']==src.SELECTION_SHA256
             and record['conditional_arithmetic_completed']is False
             and all(record[f]is False for f in FLAGS),'Imported provenance is not itself accepted evidence')
    task=relative(root,record['task_relative']);archive=relative(root,record['source_zip_relative'])
    src.need(archive.is_file()and archive.stat().st_size<=recovery.CACHE_BYTES
             and src.digest(archive)==record['source_zip_sha256'],'Actual imported complete-pair ZIP bytes')
    with zipfile.ZipFile(archive)as z:
        members=recovery.cache_members(z)
        found={p.relative_to(task).as_posix()for p in task.rglob('*')if p.is_file()}
        src.need(found=={i.filename for i in members},'Imported pair exactly equals its stopped complete export')
        import hashlib
        for info in members:
            p=relative(task,info.filename)
            with z.open(info)as stream:
                h=hashlib.sha256()
                while block:=stream.read(src.MIB):h.update(block)
            src.need(p.is_file()and p.stat().st_size==info.file_size and src.digest(p)==h.hexdigest(),
                     'Every independently imported pair byte remains unchanged')
    checked=recovered.validate_completed(task)
    src.need(same(checked,record['validated']),'Full original64 constructor/acceptance validator readback')
    s=checked['summary'];capsule=task/'capsule'
    for key in('source_plan_sha256','candidate_sha256','contract_sha256','n','index','p','rho','contact_allowance'):
        src.need(same(s[key],expected[key]),'Recovered exact original same-contract profile: '+key)
    src.need(src.digest(capsule/'COUNT41_FOREST.json')==expected['candidate_sha256']
             and src.digest(capsule/'contract.json')==expected['contract_sha256']
             and src.digest(capsule/'count_protocol.py')==expected['checker_sha256']
             and all(same(s['census'][k],v)for k,v in expected['census'].items())
             and s['historical_candidate_sha256']==expected['candidate_sha256']
             and s['historical_acceptance_sha256']==expected['historical_receipt_sha256']
             and s['acceptance_receipt_sha256']==src.digest(capsule/'COUNT41_ACCEPTED.json'),
             'Exact original forest/source/contract identity, all28 roots and fresh acceptance binding')
    src.need(all(checked[f]is False for f in recovered.FLAGS),'Imported64 retains its explicitly conditional scope')
    return dict(schema='VERIFIED_IDENTICAL_N27_P41_CANDIDATE_EDGE_V1',
                completed_sha256=checked['completed_sha256'],source_zip_sha256=record['source_zip_sha256'],
                source_plan_sha256=expected['source_plan_sha256'],candidate_sha256=expected['candidate_sha256'],
                contract_sha256=expected['contract_sha256'],checker_sha256=expected['checker_sha256'],
                historical_acceptance_sha256=expected['historical_receipt_sha256'],
                fresh_acceptance_sha256=s['acceptance_receipt_sha256'],census=s['census'],
                same_candidate_and_contract_verified=True,parent_acquisitions_verified=False,
                all_index_conclusion_verified=False)


def validate_batch(root):
    root=Path(root);status=src.read(root/'SESSION_RESULT.json',limit=64*src.MIB);rows=src.jobs();d=src.selection()
    src.need(status['schema']=='CONDITIONAL_FINITE2630_COMPLETE_COUNT_BATCH_V1'
             and status['selection_sha256']==src.SELECTION_SHA256
             and same(status['implementation'],implementation())
             and status['state']=='complete_selected_conditional_count_arithmetic_basic'
             and status['conditional_arithmetic_completed']is True
             and status['all_selected_arithmetic_completed']is True
             and all(status[f]is False for f in FLAGS),'Full proposed80 selection, exact implementation and conditional scope')
    entries=status['jobs'];src.need([e['job_id']for e in entries]==[r['job_id']for r in rows],
                                  'Every one of the79 archived jobs exactly once in original order')
    summaries=[]
    for entry,row in zip(entries,rows):
        task=relative(root,entry['task_relative']);checked=validate_completed(task)
        src.need(checked['job_id']==row['job_id']and same(checked,entry['validated']),
                 'Complete independent source/launch/capture/native receipt revalidation per selected job')
        summaries.append(checked['summary'])
    pair=validate_recovered(root);src.need(same(pair,status['recovered64']),'Exact imported64 edge in the full selection ledger')
    actual=dict(forests=len(summaries)+1,**{k:sum(s['census'][k]for s in summaries)+pair['census'][k]
                                        for k in('roots','nodes','leaves')})
    src.need(same(actual,d['complete_census'])and same(status['actual_census'],actual),
             'Full80 forests,2316 roots,150296 nodes and76306 leaves, without omission or double counting')
    return dict(schema='REVALIDATED_FULL_CONDITIONAL_FINITE2630_COUNT_V1',selection_sha256=src.SELECTION_SHA256,
                session_result_sha256=src.digest(root/'SESSION_RESULT.json'),actual_census=actual,
                archived_stage_result_sha256={e['job_id']:e['validated']['stage_result_sha256']for e in entries},
                recovered64=pair,conditional_arithmetic_completed=True,**{f:False for f in FLAGS})
