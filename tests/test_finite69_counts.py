"""Synthetic infrastructure only; every fake numerical module is an import trap."""
from __future__ import annotations
import copy
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import finite69_sources as src, finite69_counts as run, finite69_count_evidence as ev


def put(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((json.dumps(value,indent=2)+"\n").encode());return src.digest(path)


class Counts(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.cache=self.root/"inputs";prefix="work/finite6/count/panel001"
        directory=self.cache/prefix;directory.mkdir(parents=True)
        (directory/"count_protocol.py").write_bytes(b"raise AssertionError('Do not import a mathematical module in infrastructure tests')\n")
        (directory/"kernel.py").write_bytes(b"raise AssertionError('Do not evaluate the fake kernel')\n")
        contract_pin=put(directory/"contract.json",dict(rows=[dict(n=6,index=1)]))
        checker_pin=src.digest(directory/"count_protocol.py");kernel=dict(files={"kernel.py":src.digest(directory/"kernel.py")})
        put(directory/"KERNEL_COPY_MANIFEST.json",kernel)
        leaf=dict(kind="leaf",box=[["0","1"]]*5,decision="PASS_TARGET",result=dict(score_upper="1/4"))
        forest=dict(schema="FAKE_ORIGINAL_FOREST",n=6,index=1,target="2/5",contract_sha256=contract_pin,
                    kernel_sha256=kernel["files"],checker_sha256=checker_pin,
                    roots=[dict(k=k,tree=copy.deepcopy(leaf))for k in range(7)])
        forest_pin=put(directory/"COUNT_FOREST.json",forest)
        pins={p.relative_to(self.cache).as_posix():src.digest(p)for p in directory.iterdir()}
        self.row=dict(job_id="n6.B0.p1",kind="count",selection=dict(n=6,index=1,band="B0",band_rho=["1","11/10"],
            target="2/5",capsule=prefix,contract_pin=contract_pin,forest_pin=forest_pin,forest_name="COUNT_FOREST.json",
            receipt_name="COUNT_ACCEPTED.json"),source_files_sha256=pins,
            candidate_census=dict(roots=7,nodes=7,leaves=7,maximum_depth=0),
            native_schema=dict(status="PASS_SYNTHETIC_COUNT",scope="SYNTHETIC_ONLY",
                controls=[f"control {i}"for i in range(24)],fields=["status","scope","n","index","forest_sha256",
                    "contract_sha256","checker_sha256","kernel_sha256","statistics","fresh_leaf_evaluations","negative_controls","seconds"]))
        self.cat=dict(jobs=[self.row],parent_jobs=[],source_files={name:dict(sha256=pin,bytes=(self.cache/name).stat().st_size)
                      for name,pin in pins.items()},snapshot_sha256="a"*64,remaining_obligations=["Parents remain unacquired"])
        p=patch.object(src,"catalog",return_value=self.cat);p.start();self.addCleanup(p.stop)
        p=patch.object(run.sys,"platform","linux");p.start();self.addCleanup(p.stop)
        p=patch.object(run.sys,"stdout",io.StringIO());p.start();self.addCleanup(p.stop)

    def fake_supervisor(self,argv,*,cwd,output_dir,**kwargs):
        task=Path(output_dir).parent;directory=Path(cwd);receipt=self.receipt(directory)
        put(directory/"COUNT_ACCEPTED.json",receipt)
        output_dir=Path(output_dir);output_dir.mkdir()
        (output_dir/"stdout.txt").write_bytes((json.dumps(receipt,indent=2)+"\n").encode())
        (output_dir/"stderr.txt").write_bytes(b"")
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,checkpoint_paths=[],**kwargs)
        # Match linux_supervisor._settings rather than retaining caller types.
        launch["wall_seconds"]=float(launch["wall_seconds"])
        launch["heartbeat_seconds"]=float(launch["heartbeat_seconds"])
        put(output_dir/"launch.json",launch)
        guard=dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",proof_acceptance=False,
            external_wall_seconds=ev.WALL_SECONDS,per_process_RLIMIT_AS_bytes=ev.MEMORY_BYTES,
            per_process_RLIMIT_CPU_seconds=ev.CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,
            sampled_group_RSS_limit_bytes=ev.MEMORY_BYTES,sampled_group_CPU_limit_seconds=ev.CPU_SECONDS,
            sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,
            descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
        observed=dict(status="completed",returncode=0,reason=None,proof_accepted=False,mode="untrusted_search",sample_count=1,
            guard_scope=guard,**{kind+suffix:value for kind in("stdout","stderr")for suffix,value in(
                ("_path",str(output_dir/(kind+".txt"))),("_sha256",src.digest(output_dir/(kind+".txt"))))})
        put(output_dir/"supervisor-result.json",observed);return observed

    def receipt(self,directory):
        row=self.row;s=row["selection"];forest=src.read(directory/"COUNT_FOREST.json")
        stats=ev.census(forest,6);stats.pop("roots")
        return dict(status=row["native_schema"]["status"],scope=row["native_schema"]["scope"],n=6,index=1,
            forest_sha256=s["forest_pin"],contract_sha256=s["contract_pin"],checker_sha256=forest["checker_sha256"],
            kernel_sha256=forest["kernel_sha256"],statistics=stats,fresh_leaf_evaluations=7,
            negative_controls=row["native_schema"]["controls"],seconds=0)

    def complete(self,name="task",effect=None):
        task=self.root/name
        with patch.object(run.linux_supervisor,"run",side_effect=effect or self.fake_supervisor),patch.object(run,"Follow"):
            checked=run.execute(task,self.row,self.cache)
        return task,checked

    def test_real_driver_dispatch_false_observation_then_complete_and_relocation(self):
        seen=[];original=ev.validate_run
        def observe(task,row,report):
            self.assertFalse(report["conditional_arithmetic_completed"])
            if not seen:self.assertFalse((Path(task)/"STAGE_COMPLETED.json").exists())
            seen.append(report)
            return original(task,row,report)
        with patch.object(ev,"validate_run",side_effect=observe):task,checked=self.complete()
        self.assertEqual(checked["summary"]["fresh_leaf_evaluations"],7);self.assertTrue(seen)
        copied=self.root/"relocated";shutil.copytree(task,copied)
        self.assertEqual(ev.validate_completed(copied),checked)
        for flag in ev.FLAGS:self.assertIs(checked[flag],False)

    def test_boolean_rc_failed_status_or_stderr_never_completes(self):
        for field,value in(("returncode",False),("status","incomplete"),("reason","resource_limit")):
            with self.subTest(field=field):
                def bad(*a,**kw):
                    observed=self.fake_supervisor(*a,**kw);observed[field]=value
                    put(Path(kw["output_dir"])/"supervisor-result.json",observed);return observed
                task=self.root/field
                with self.assertRaises(ValueError):self.complete(field,bad)
                self.assertTrue((task/"STAGE_OBSERVED.json").exists());self.assertFalse((task/"STAGE_COMPLETED.json").exists())

    def test_nonempty_actual_stderr_never_completes_even_with_matching_sha(self):
        def noisy(*a,**kw):
            observed=self.fake_supervisor(*a,**kw);path=Path(kw["output_dir"])/"stderr.txt"
            path.write_bytes(b"unexpected warning\n");observed["stderr_sha256"]=src.digest(path)
            put(Path(kw["output_dir"])/"supervisor-result.json",observed);return observed
        with self.assertRaisesRegex(ValueError,"stderr"):self.complete("noisy",noisy)
        self.assertFalse((self.root/"noisy/STAGE_COMPLETED.json").exists())

    def test_native_receipt_cannot_detach_from_actual_stdout(self):
        task,_=self.complete();path=task/"capsule"/self.row["selection"]["capsule"]/"COUNT_ACCEPTED.json"
        data=src.read(path);data["negative_controls"][0]="invented";put(path,data)
        with self.assertRaisesRegex(ValueError,"stdout"):ev.validate_completed(task)

    def test_strict_capture_budget_guard_and_unmodified_sources(self):
        task,_=self.complete();baseline=src.read(task/"STAGE_OBSERVED.json")
        mutations=[lambda x:x["observed"].update(stderr_sha256="0"*64),lambda x:x.update(cpu_seconds=1),
                   lambda x:x["observed"]["guard_scope"].update(aggregate_kernel_memory_limit=True),
                   lambda x:x.update(parent_acquisitions_verified=True)]
        for mutate in mutations:
            data=copy.deepcopy(baseline);mutate(data);put(task/"STAGE_OBSERVED.json",data)
            put(task/"execution/supervisor-result.json",data["observed"])
            with self.assertRaises(ValueError):ev.validate_completed(task)
        put(task/"STAGE_OBSERVED.json",baseline);put(task/"execution/supervisor-result.json",baseline["observed"])
        extra=task/"capsule"/self.row["selection"]["capsule"]/"unbound.py";extra.write_text("pass")
        with self.assertRaisesRegex(ValueError,"sealed"):ev.validate_completed(task)

    def test_literal_native_status_and_complete_named_controls(self):
        for field,value in(("status","FAIL"),("n",True),("fresh_leaf_evaluations",False),
                            ("negative_controls",["invented"]*24)):
            with self.subTest(field=field):
                def bad(*a,**kw):
                    observed=self.fake_supervisor(*a,**kw);directory=Path(kw["cwd"])
                    data=src.read(directory/"COUNT_ACCEPTED.json");data[field]=value;put(directory/"COUNT_ACCEPTED.json",data)
                    stdout=Path(kw["output_dir"])/"stdout.txt";stdout.write_bytes((json.dumps(data)+"\n").encode())
                    observed["stdout_sha256"]=src.digest(stdout);put(Path(kw["output_dir"])/"supervisor-result.json",observed)
                    return observed
                with self.assertRaises(ValueError):self.complete("bad-"+field,bad)
                self.assertFalse((self.root/("bad-"+field)/"STAGE_COMPLETED.json").exists())

    def test_complete_cache_sha_and_readback_only_then_skip(self):
        task,checked=self.complete();folder=self.root/"durable";saved=run.save_stage(task,folder)
        restored=run.restore_stage(folder,self.root/"restores",self.row)
        self.assertEqual(restored[1],checked)
        marker=Path(saved["path"]+".sha256");marker.write_text("0"*64+"  "+Path(saved["path"]).name+"\n")
        self.assertIsNone(run.restore_stage(folder,self.root/"bad-restores",self.row))

    def test_completed_cache_reinventoried_receipt_forgery_is_rejected(self):
        task,_=self.complete();path=task/"capsule"/self.row["selection"]["capsule"]/"COUNT_ACCEPTED.json"
        data=src.read(path);data["status"]="DELIBERATE_FAILURE";put(path,data)
        complete=src.read(task/"STAGE_COMPLETED.json");complete["artifacts"]=ev.inventory(task);put(task/"STAGE_COMPLETED.json",complete)
        with self.assertRaises(ValueError):run.save_stage(task,self.root/"fake-cache")

    def test_batch_reuses_only_revalidated_complete_stage(self):
        root=self.root/"batch";root.mkdir();status=dict(jobs=[])
        with patch.object(run.linux_supervisor,"run",side_effect=self.fake_supervisor)as launch,patch.object(run,"Follow"):
            run.batch_jobs(root,self.root/"stages",self.cache,status,[self.row]);self.assertEqual(launch.call_count,1)
        status2=dict(jobs=[]);again=self.root/"again";again.mkdir()
        with patch.object(run.linux_supervisor,"run",side_effect=AssertionError("Completed acceptance must be reused")):
            run.batch_jobs(again,self.root/"stages",self.cache,status2,[self.row])
        self.assertTrue(status2["jobs"][0]["reused_completed_stage"])

    def test_cache_zip_preflight_rejects_bad_shape(self):
        base=["SOURCES.json","STAGE_OBSERVED.json","STAGE_COMPLETED.json","execution/launch.json",
              "execution/supervisor-result.json","execution/stdout.txt","execution/stderr.txt"]
        for bad in("../escape","D:/escape","a\\b","execution/STDOUT.txt","SOURCES.json"):
            class Fake:
                def infolist(self):
                    rows=[]
                    for name in[*base,bad]:
                        row=zipfile.ZipInfo("safe");row.filename=name;row.orig_filename=name;rows.append(row)
                    return rows
            with self.subTest(bad=bad),self.assertRaises(ValueError):run.cache_members(Fake())
        class Missing:
            def infolist(self):return [zipfile.ZipInfo("SOURCES.json")]
        with self.assertRaises(ValueError):run.cache_members(Missing())

    def test_source_zip_preflight_bounds_links_and_case_aliases(self):
        def fake(names):
            class Archive:
                def infolist(self):return names
            return Archive()
        symlink=zipfile.ZipInfo("link");symlink.external_attr=(0o120777<<16)
        huge=zipfile.ZipInfo("huge");huge.file_size=257*src.MIB
        for rows in([zipfile.ZipInfo("../x")],[zipfile.ZipInfo("A"),zipfile.ZipInfo("a")],[symlink],[huge]):
            with self.subTest(rows=[r.filename for r in rows]),self.assertRaises(ValueError):src.zip_index(fake(rows))

    def test_invalid_index_fails_before_work_or_download(self):
        for n in(5,10,True,"6"):
            with patch.object(src,"obtain_assets")as obtain,self.assertRaises(ValueError):
                run.run_colab(n,durable_root=self.root/"durable",work_root=self.root/"not-created")
            obtain.assert_not_called();self.assertFalse((self.root/"not-created").exists())

    def test_source_candidate_tamper_cross_job_and_topology_fail(self):
        task=self.root/"prepared";src.prepare_job(self.row["job_id"],self.cache,task)
        with self.assertRaises(ValueError):src.job("n7.B0.p1")
        forest=src.read(task/"capsule"/self.row["selection"]["capsule"]/"COUNT_FOREST.json")
        forest["roots"].pop()
        with self.assertRaises(ValueError):ev.census(forest,6)
        (task/"capsule"/self.row["selection"]["capsule"]/"kernel.py").write_text("changed")
        with self.assertRaises(ValueError):src.verify_job(task)

    def test_run_colab_failure_exports_explicit_partial(self):
        with patch.object(src,"obtain_assets",side_effect=ValueError("Synthetic download failure")),patch.object(run,"LogBackups"):
            result=run.run_colab(6,durable_root=self.root/"durable",work_root=self.root/"work",archives=self.root/"archives")
        self.assertEqual(result["status"]["state"],"incomplete_selected_count_arithmetic")
        self.assertEqual(result["status"]["jobs"],[]);self.assertTrue(Path(result["bundle"]).is_file())
        for flag in ev.FLAGS:self.assertIs(result["status"][flag],False)


if __name__=="__main__":unittest.main()
