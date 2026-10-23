"""Source/JSON and synthetic transport fixtures; no original math is imported."""
import ast
from contextlib import ExitStack, nullcontext, redirect_stdout
import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import sys
import unittest
from unittest.mock import patch
import zipfile

from be_replay import n5_remaining as run, n5_remaining_sources as src
from be_replay import n5_remaining_evidence as ev, n5_remaining_bridge as bridge


def put(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,sort_keys=True,indent=2)+"\n",encoding="utf-8")


def fixture(task):
    """Fake mathematical source raises if somebody accidentally evaluates it."""
    task=Path(task).resolve();task.mkdir(parents=True)
    capsule=task/"runtime/work/count-candidate/capsule";capsule.mkdir(parents=True)
    (capsule/"count_protocol.py").write_text("raise AssertionError('MUST NEVER RUN SYNTHETIC KERNEL')\n")
    put(capsule/"contract.json",{"synthetic":True});put(capsule/"COUNT_FOREST.json",{"synthetic":True})
    put(capsule/"KERNEL_COPY_MANIFEST.json",{"files":{"trap.py":"0"*64}})
    row=dict(job_id="count-000",kind="count",entry="c5_count_one.py",arguments=[],index=12,
        expected_status="SYNTHETIC_ACCEPTED",source_files={n:src.digest(capsule/n)for n in
        ("count_protocol.py","contract.json","COUNT_FOREST.json")},
        census=dict(roots=6,nodes=6,leaves=6,maximum_depth=0),negative_controls=["false score","duplicate JSON key"])
    receipt=dict(status=row["expected_status"],n=5,index=12,forest_sha256=row["source_files"]["COUNT_FOREST.json"],
        checker_sha256=row["source_files"]["count_protocol.py"],contract_sha256=row["source_files"]["contract.json"],
        kernel_sha256={"trap.py":"0"*64},statistics=dict(nodes=6,leaves=6,maximum_depth=0),
        fresh_leaf_evaluations=6,negative_controls=row["negative_controls"])
    put(capsule/"COUNT_ACCEPTED.json",receipt)
    put(capsule.parent/"c5-count-native.stdout.txt",receipt)
    request=dict(job_id=row["job_id"],original_task_root=str(task),source_cache=str(task.parent/"external-cache"))
    put(task/"JOB_SOURCE.json",request)
    execution=task/"execution";execution.mkdir()
    packet=dict(event="fresh_native_count_process_completed",receipt=str(capsule/"COUNT_ACCEPTED.json"))
    (execution/"stdout.txt").write_text(json.dumps(packet)+"\n",encoding="utf-8");(execution/"stderr.txt").write_bytes(b"")
    guard=dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",proof_acceptance=False,
        external_wall_seconds=run.WALL_SECONDS,per_process_RLIMIT_AS_bytes=run.MEMORY_BYTES,
        per_process_RLIMIT_CPU_seconds=run.CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,
        sampled_group_RSS_limit_bytes=run.MEMORY_BYTES,sampled_group_CPU_limit_seconds=run.CPU_SECONDS,
        sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
    observed=dict(status="completed",mode="untrusted_search",returncode=0,reason=None,proof_accepted=False,
        sample_count=1,guard_scope=guard,**{k+"_path":str(execution/(k+".txt"))for k in("stdout","stderr")},
        **{k+"_sha256":src.digest(execution/(k+".txt"))for k in("stdout","stderr")})
    put(execution/"supervisor-result.json",observed)
    launch=dict(argv=ev.command(request,row,"/synthetic/python"),cwd=str(task/"runtime"),output_dir=str(execution),
        mode="untrusted_search",cpu_seconds=run.CPU_SECONDS,wall_seconds=run.WALL_SECONDS,memory_bytes=run.MEMORY_BYTES,
        disk_bytes=512*src.MIB,log_bytes=16*src.MIB,heartbeat_seconds=20,sample_seconds=.2,checkpoint_paths=[])
    put(execution/"launch.json",launch)
    report=dict(schema=ev.OBSERVED,scope=ev.SCOPE,job_id=row["job_id"],implementation=ev.implementation(),
        original_task_root=str(task),python_executable="/synthetic/python",cpu_seconds=run.CPU_SECONDS,
        wall_seconds=run.WALL_SECONDS,memory_bytes=run.MEMORY_BYTES,observed=observed,
        conditional_arithmetic_completed=False,native_arithmetic_accepted=False,
        fresh_parent_fact_joins_verified=False,full_n5_verified=False,all_index_conclusion_verified=False)
    put(task/"STAGE_OBSERVED.json",report)
    return task,row,request,report


class N5Remaining(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def context(self,request,row):
        stack=ExitStack();stack.enter_context(patch.object(src,"verify_job",return_value=request))
        stack.enter_context(patch.object(src,"job",return_value=row));return stack
    def completed(self):
        task,row,request,report=fixture(self.root/"original")
        with self.context(request,row):
            summary=ev.validate_run(task,row,report)
            put(task/"STAGE_COMPLETED.json",dict(schema=ev.SCHEMA,scope=ev.SCOPE,job_id=row["job_id"],
                implementation=ev.implementation(),observed_sha256=src.digest(task/"STAGE_OBSERVED.json"),
                summary=summary,artifacts=ev.inventory(task),conditional_arithmetic_completed=True,
                native_arithmetic_accepted=False,fresh_parent_fact_joins_verified=False,
                full_n5_verified=False,all_index_conclusion_verified=False))
        return task,row,request,report

    def test_fixed_source_catalog_and_all_controls(self):
        d=src.catalog();self.assertEqual(len(src.jobs()),326)
        self.assertEqual(d["census"],dict(jobs=326,initial=12,resources=15,resource_panels=1200,
            count_forests=295,count_roots=1770,count_nodes=148586,count_leaves=75178))
        self.assertEqual(len(d["source_cache_files"]),16619);self.assertEqual(len(src.verify_vendor()),333)
        for row in src.jobs():
            if row["kind"]=="count":self.assertEqual(row["census"]["roots"],6);self.assertTrue(row["negative_controls"])
        self.assertEqual(len(src.job("complement")["independent_fourier_negative_controls"]),16)
        self.assertEqual(len(src.job("complement")["native_negative_controls"]),10)
    def test_bridge_only_changes_resource_function(self):
        raw=(src.VENDOR/"run_reproduction.py").read_bytes();new=bridge.derive(raw)
        before,after=ast.parse(raw),ast.parse(new)
        changed=[a.name for a,b in zip(before.body,after.body)if isinstance(a,(ast.FunctionDef,ast.AsyncFunctionDef))
                 and ast.dump(a)!=ast.dump(b)]
        self.assertEqual(changed,["run_child"])
        expected=raw
        for old,replacement in bridge.EDITS:
            self.assertEqual(raw.count(old),1);expected=expected.replace(old,replacement,1)
        self.assertEqual(new,expected)
        with self.assertRaises(ValueError):bridge.derive(raw+b"\n")
    def test_source_preparation_never_runs_count_kernel(self):
        row=src.job("count-000");cache=self.root/"cache"
        # Only synthetic bytes are used, with source selection mocked; the real
        # source preparation/sealing implementation still copies and rehashes.
        fake=copy.deepcopy(row);fake["source_files"]={"count_protocol.py":hashlib.sha256(b"raise AssertionError('trap')\n").hexdigest()}
        p=cache/fake["source_capsule"]/"count_protocol.py";p.parent.mkdir(parents=True);p.write_bytes(b"raise AssertionError('trap')\n")
        with patch.object(src,"job",return_value=fake):
            src.prepare_job(self.root/"prepared",fake,cache);src.verify_job(self.root/"prepared",fake)
            bad=self.root/"prepared/runtime/work/count-candidate/capsule/unbound.py";bad.write_text("raise RuntimeError")
            with self.assertRaises(ValueError):src.verify_job(self.root/"prepared",fake)
    def test_completed_capture_and_relocation(self):
        task,row,request,_=self.completed()
        import shutil
        relocated=self.root/"relocated";shutil.copytree(task,relocated)
        with self.context(request,row):
            checked=ev.validate_completed(relocated)
            self.assertTrue(checked["conditional_arithmetic_completed"]);self.assertFalse(checked["full_n5_verified"])
            with self.assertRaises(ValueError):ev.validate_completed(relocated,original_task_root="/different/root")
    def test_reject_boolean_exit_and_missing_guard(self):
        for field,value in(("returncode",False),("guard_scope",{}),("sample_count",False),("mode","trusted_native")):
            with self.subTest(field=field):
                task,row,request,report=fixture(self.root/field)
                report["observed"][field]=value;put(task/"execution/supervisor-result.json",report["observed"])
                with self.context(request,row),self.assertRaises((ValueError,KeyError)):ev.validate_run(task,row,report)
    def test_reject_changed_budgets_and_context(self):
        for key,value in(("cpu_seconds",1),("wall_seconds",1),("memory_bytes",64*src.MIB),
                          ("disk_bytes",1),("output_dir",str(self.root/"elsewhere"))):
            with self.subTest(key=key):
                task,row,request,report=fixture(self.root/key)
                launch=src.read(task/"execution/launch.json");launch[key]=value;put(task/"execution/launch.json",launch)
                if key in report:report[key]=value
                with self.context(request,row),self.assertRaises(ValueError):ev.validate_run(task,row,report)
    def test_reject_empty_stderr_with_wrong_hash_and_nonempty(self):
        for kind in("hash","bytes"):
            task,row,request,report=fixture(self.root/kind)
            if kind=="hash":report["observed"]["stderr_sha256"]="0"*64
            else:
                (task/"execution/stderr.txt").write_text("unexpected")
                report["observed"]["stderr_sha256"]=src.digest(task/"execution/stderr.txt")
            put(task/"execution/supervisor-result.json",report["observed"])
            with self.context(request,row),self.assertRaises(ValueError):ev.validate_run(task,row,report)
    def test_inner_native_stdout_prevents_receipt_only_edit(self):
        task,row,request,report=fixture(self.root/"changed")
        path=task/"runtime/work/count-candidate/capsule/COUNT_ACCEPTED.json"
        d=src.read(path);d["unused_but_recorded"]="tamper";put(path,d)
        with self.context(request,row),self.assertRaisesRegex(ValueError,"stdout"):ev.validate_run(task,row,report)
    def test_exact_original_control_names_and_full_leaf_count(self):
        for key,value in(("negative_controls",["invented","labels"]),("fresh_leaf_evaluations",5),("status","FAILED")):
            task,row,request,report=fixture(self.root/key)
            path=task/"runtime/work/count-candidate/capsule/COUNT_ACCEPTED.json";d=src.read(path);d[key]=value
            put(path,d);put(path.parent.parent/"c5-count-native.stdout.txt",d)
            with self.context(request,row),self.assertRaises(ValueError):ev.validate_run(task,row,report)
    def test_completed_inventory_rejects_extra_or_mutated_receipt(self):
        task,row,request,_=self.completed();(task/"unexpected.bin").write_bytes(b"extra")
        with self.context(request,row),self.assertRaises(ValueError):ev.validate_completed(task)
    def test_stage_cache_revalidates_and_rejects_bad_sha(self):
        task,row,request,_=self.completed()
        with self.context(request,row):
            saved=run.save_stage(task,self.root/"cache")
            restored=run.restore_stage(self.root/"cache",self.root/"restore",row)
            self.assertIsNotNone(restored);self.assertEqual(restored[1]["job_id"],row["job_id"])
            Path(saved["path"]).with_suffix(".zip.sha256").write_text("0"*64+"  bad\n")
            self.assertIsNone(run.restore_stage(self.root/"cache",self.root/"bad-restore",row))
    def test_stage_cache_mutation_is_rejected_even_with_new_zip_hash(self):
        task,row,request,_=self.completed()
        with self.context(request,row):
            saved=run.save_stage(task,self.root/"cache");path=Path(saved["path"])
            with zipfile.ZipFile(path)as z:members={i.filename:z.read(i)for i in z.infolist()}
            members["runtime/work/count-candidate/capsule/COUNT_ACCEPTED.json"]=b"{}\n"
            with zipfile.ZipFile(path,"w")as z:
                for name,raw in members.items():z.writestr(name,raw)
            path.with_suffix(".zip.sha256").write_text(src.digest(path)+"  "+path.name+"\n",encoding="ascii")
            self.assertIsNone(run.restore_stage(self.root/"cache",self.root/"bad",row))
    def test_zip_preflight_rejects_unsafe_duplicate_and_missing(self):
        mandatory=["JOB_SOURCE.json","STAGE_OBSERVED.json","STAGE_COMPLETED.json","execution/launch.json",
                   "execution/supervisor-result.json","execution/stdout.txt","execution/stderr.txt"]
        for bad in("../x","a\\b","A/../../x","JOB_SOURCE.json",None):
            with self.subTest(bad=bad):
                infos=[zipfile.ZipInfo(n)for n in mandatory]
                if bad is None:infos.pop()
                else:
                    i=zipfile.ZipInfo("safe");i.filename=bad;i.orig_filename=bad;infos.append(i)
                class Metadata:
                    def infolist(self):return infos
                with self.assertRaises(ValueError):run.cache_members(Metadata())
        infos=[zipfile.ZipInfo(n)for n in mandatory];infos[0].file_size=129*src.MIB
        class Large:
            def infolist(self):return infos
        with self.assertRaises(ValueError):run.cache_members(Large())
    def test_context_mapping_and_duplicate_json_are_strict(self):
        with self.assertRaises(ValueError):ev.mapped(self.root,"/other/a","/original")
        self.assertTrue(ev.context_equal(self.root,"/original",{"path":"/original/a"},{"path":str(self.root/"a")}))
        self.assertFalse(ev.context_equal(self.root,"/original",{"n":True},{"n":1}))
        with self.assertRaises(ValueError):json.loads('{"x":1,"x":2}',object_pairs_hook=src.unique)

    def test_source_dictionary_subset_cannot_become_complete(self):
        pins={"work/a.py":"a"*64,"work/b.py":"b"*64}
        with self.assertRaisesRegex(ValueError,"complete source-selection"):
            ev._pins(self.root,{"work/a.py":"a"*64},pins)

    def test_high_failed_native_status_is_rejected_before_capture(self):
        base=self.root/"runtime/work/h5-test";directory=base/"work/cutoff5_20261020/high/high5_v1"
        path=directory/"HIGH_CHECKED.json";put(path,dict(status="DELIBERATE_FAILED_RECEIPT",n=5,negative_controls=["made up"]*8))
        row=src.job("high");packet=dict(status="FRESH_BOTH_NATIVE_HIGH_PROTOCOLS_ACCEPTED",fresh_arithmetic=True,
            all_index_conclusion_verified=False,source_files_sha256=row["source_files_sha256"],
            receipts=[dict(variant=v["name"],native_receipt=str(path),sha256=src.digest(path))for v in row["variants"]])
        with patch.object(ev,"_pins"),self.assertRaisesRegex(ValueError,"corruption control"):
            ev.summarize(self.root,row,packet,str(self.root),"/synthetic/python")

    def test_execute_observed_false_then_complete_only_after_validation(self):
        for failed in(False,True):
            task,row,request,report=fixture(self.root/("failed"if failed else"success"))
            launch=src.read(task/"execution/launch.json");launch["argv"][0]=sys.executable;put(task/"execution/launch.json",launch)
            observed=report["observed"]
            if failed:observed["returncode"]=False
            put(task/"execution/supervisor-result.json",observed)
            real=ev.validate_run
            def observed_first(task_arg,row_arg,report_arg):
                self.assertFalse(src.read(task/"STAGE_OBSERVED.json")["conditional_arithmetic_completed"])
                self.assertFalse((task/"STAGE_COMPLETED.json").exists())
                return real(task_arg,row_arg,report_arg)
            with self.context(request,row),patch.object(src,"prepare_job",return_value=request),\
                 patch.object(run.sys,"platform","linux"),patch.object(run.linux_supervisor,"run",return_value=observed),\
                 patch.object(run,"Follow",return_value=nullcontext()),patch.object(ev,"validate_run",side_effect=observed_first),\
                 redirect_stdout(io.StringIO()):
                if failed:
                    with self.assertRaises(ValueError):run.execute(task,row,self.root/"cache")
                    self.assertFalse((task/"STAGE_COMPLETED.json").exists())
                else:
                    # execute revalidates the saved completed stage: after the
                    # first false-to-complete check, allow the ordinary reread.
                    calls=[0]
                    def check(t,r,p):
                        calls[0]+=1
                        return observed_first(t,r,p)if calls[0]==1 else real(t,r,p)
                    with patch.object(ev,"validate_run",side_effect=check):checked=run.execute(task,row,self.root/"cache")
                    self.assertTrue(checked["conditional_arithmetic_completed"])
                    self.assertFalse(checked["native_arithmetic_accepted"])

    def test_two_job_batch_resume_skips_only_validated_saved_jobs(self):
        rows=[dict(job_id="first",kind="count"),dict(job_id="second",kind="resource")];saved={}
        (self.root/"batch1").mkdir();(self.root/"batch2").mkdir()
        def restore(cache,destination,row,**unused):
            if row["job_id"]in saved:return Path(destination)/row["job_id"],saved[row["job_id"]],dict(path="cached",sha256="f"*64)
        def execute(task,row,cache,**unused):return dict(job_id=row["job_id"],stage_result_sha256="a"*64,conditional_arithmetic_completed=True)
        def save(task,cache):
            job_id="first"if "first-"in Path(task).name else"second"
            saved[job_id]=dict(job_id=job_id,stage_result_sha256="a"*64,conditional_arithmetic_completed=True)
            return dict(path="saved",sha256="b"*64)
        with patch.object(run,"restore_stage",side_effect=restore),patch.object(run,"execute",side_effect=execute)as native,\
             patch.object(run,"save_stage",side_effect=save),redirect_stdout(io.StringIO()):
            first=dict(jobs=[],full_n5_verified=False);run.batch_jobs(self.root/"batch1",self.root/"cache",self.root/"source",first,rows)
            self.assertEqual(native.call_count,2);native.reset_mock()
            second=dict(jobs=[],full_n5_verified=False);run.batch_jobs(self.root/"batch2",self.root/"cache",self.root/"source",second,rows)
            native.assert_not_called();self.assertTrue(all(j["reused_completed_stage"]for j in second["jobs"]))
            self.assertFalse(second["full_n5_verified"])
    def test_batch_failure_preserves_preceding_completed_stage(self):
        rows=[dict(job_id="first",kind="count"),dict(job_id="second",kind="resource")];status=dict(jobs=[],full_n5_verified=False)
        (self.root/"batch").mkdir()
        with patch.object(run,"restore_stage",return_value=None),\
             patch.object(run,"execute",side_effect=[dict(stage_result_sha256="a"*64),ValueError("interrupted")]),\
             patch.object(run,"save_stage",return_value=dict(path="saved",sha256="b"*64))as save,redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError,"interrupted"):run.batch_jobs(self.root/"batch",self.root/"cache",self.root/"source",status,rows)
            save.assert_called_once();self.assertEqual([j["job_id"]for j in status["jobs"]],["first"])
            self.assertFalse(status["full_n5_verified"])
    def test_failed_preparation_and_backup_still_export_incomplete_zip(self):
        with patch.object(run.src,"obtain_archive",side_effect=ValueError("download interrupted")),\
             patch("be_replay.environment.snapshot",return_value={"synthetic":True}),\
             patch.object(run.LogBackups,"start"),patch.object(run.LogBackups,"close",side_effect=ValueError("Drive backup")),\
             redirect_stdout(io.StringIO()):
            result=run.run_colab(durable_root=self.root/"durable",work_root=self.root/"work",archives=self.root/"archives")
        self.assertEqual(result["status"]["state"],"incomplete_selected_arithmetic")
        self.assertFalse(result["status"]["full_n5_verified"]);self.assertTrue(Path(result["bundle"]).is_file())
        with zipfile.ZipFile(result["bundle"])as z:self.assertTrue(any(n.endswith("/ERROR.txt")for n in z.namelist()))


if __name__=="__main__":unittest.main()
