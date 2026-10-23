"""Fake execution/capture/metadata tests; no original numerical module loads."""
from __future__ import annotations
import copy
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import finite69_parent_sources as src, finite69_parents as run, finite69_parent_evidence as ev


def put(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((json.dumps(value,indent=2)+"\n").encode());return src.digest(path)


class Parents(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.cache=self.root/"inputs"
        rows=[]
        for kind in("initial","resource"):
            directory="work/finite6/"+kind;path=self.cache/directory;path.mkdir(parents=True)
            (path/"replay.py").write_bytes(b"raise AssertionError('Never import an original mathematical module locally')\n")
            put(path/"INPUT.json",dict(n=6,band="B0",candidate_only=True))
            files={p.relative_to(self.cache).as_posix():src.digest(p)for p in path.iterdir()}
            conditional=[];deps=[]
            if rows:
                previous=rows[0];parent_path=previous["directory"]+"/"+previous["output"]
                files.update(previous["source_files_sha256"]);files[parent_path]=src.digest(self.cache/parent_path)
                conditional=[parent_path];deps=[dict(job_id=previous["job_id"],path=parent_path,sha256=files[parent_path])]
            answer=dict(status="PASS_FAKE_"+kind.upper(),scope="SYNTHETIC_CONDITIONAL_ONLY",n=6,band="B0",
                numerical_premises=dict(predecessor="429/1000"),final_D="1/10",negative_controls=["bad n","changed D"],
                files_sha256=files,seconds=123.0)
            if rows:answer.update(initial_receipt=parent_path,initial_receipt_sha256=files[parent_path])
            row=dict(job_id="n6."+kind+".B0",kind=kind,lane="n6",directory=directory,arguments=["B0"],
                output="B0/REPLAY_CHECKED.json",source_files_sha256=files,conditional_receipt_inputs=conditional,
                direct_fresh_dependencies=deps,native_controls=answer["negative_controls"],
                reference=dict(native_answer=answer,candidate_only=True))
            put(path/row["output"],answer);rows.append(row)
        self.rows=rows;self.row=rows[0]
        self.cat=dict(jobs=rows,base_catalog_sha256=src.base.CATALOG_SHA256,remaining_obligations=["External premises remain conditional"])
        for target,name,value in((src,"catalog",self.cat),(run.sys,"platform","linux"),(run.sys,"stdout",io.StringIO())):
            p=patch.object(target,name,return_value=value)if name=="catalog"else patch.object(target,name,value)
            p.start();self.addCleanup(p.stop)

    def fake_supervisor(self,argv,*,cwd,output_dir,**kwargs):
        output_dir=Path(output_dir);task=output_dir.parent;request=src.read(task/"SOURCES.json");row=src.job(request["job_id"])
        native=task/"capsule"/src.output_relative(row);answer=copy.deepcopy(row["reference"]["native_answer"])
        answer["seconds"]=.5;put(native,answer)
        output_dir.mkdir();(output_dir/"stdout.txt").write_text("FRESH_PROGRESS 1\n"+answer["status"]+" B0\n",encoding="utf-8")
        (output_dir/"stderr.txt").write_bytes(b"")
        kwargs["checkpoint_paths"]=[str(Path(p).resolve())for p in kwargs["checkpoint_paths"]]
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,**kwargs)
        launch["wall_seconds"]=float(launch["wall_seconds"]);launch["heartbeat_seconds"]=float(launch["heartbeat_seconds"])
        put(output_dir/"launch.json",launch)
        captured=output_dir/"checkpoints"/row["output"];captured.parent.mkdir(parents=True);shutil.copyfile(native,captured)
        guard=dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",proof_acceptance=False,
            external_wall_seconds=ev.WALL_SECONDS,per_process_RLIMIT_AS_bytes=ev.MEMORY_BYTES,
            per_process_RLIMIT_CPU_seconds=ev.CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,
            sampled_group_RSS_limit_bytes=ev.MEMORY_BYTES,sampled_group_CPU_limit_seconds=ev.CPU_SECONDS,
            sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,
            descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
        observed=dict(status="completed",reason=None,returncode=0,proof_accepted=False,mode="untrusted_search",sample_count=1,
            guard_scope=guard,checkpoints=[dict(source_path=str(native),path=str(captured),exists=True,trusted_certificate=False,
                bytes=native.stat().st_size,sha256=src.digest(native))],
            **{kind+suffix:value for kind in("stdout","stderr")for suffix,value in(
                ("_path",str(output_dir/(kind+".txt"))),("_sha256",src.digest(output_dir/(kind+".txt"))))})
        put(output_dir/"supervisor-result.json",observed);return observed

    def complete(self,name="task",row=None,effect=None):
        task=self.root/name
        with patch.object(run.linux_supervisor,"run",side_effect=effect or self.fake_supervisor),patch.object(run,"Follow"):
            checked=run.execute(task,row or self.row,self.cache)
        return task,checked

    def test_no_old_own_acceptance_is_copied(self):
        task=self.root/"prepared";src.prepare_job(self.row["job_id"],self.cache,task)
        self.assertFalse((task/"capsule"/src.output_relative(self.row)).exists())
        self.assertEqual(src.verify_job(task)["source_files_sha256"],self.row["source_files_sha256"])

    def test_actual_full_output_capture_and_relocated_readback(self):
        task,checked=self.complete();copied=self.root/"elsewhere";shutil.copytree(task,copied)
        self.assertEqual(ev.validate_completed(copied),checked)
        self.assertEqual(checked["summary"]["status"],"PASS_FAKE_INITIAL")
        for field in ev.FLAGS:self.assertIs(checked[field],False)

    def test_native_receipt_cannot_change_independently_of_supervisor_copy(self):
        task,_=self.complete();path=task/"capsule"/src.output_relative(self.row);data=src.read(path)
        data["seconds"]=.75;put(path,data)
        with self.assertRaisesRegex(ValueError,"stopped native receipt"):ev.validate_completed(task)

    def test_bad_checkpoint_or_rc_never_creates_completed_ledger(self):
        variants=(lambda z:z.update(returncode=False),lambda z:z.update(checkpoints=[]),
                  lambda z:z["checkpoints"][0].update(sha256="0"*64),lambda z:z["checkpoints"][0].update(trusted_certificate=True))
        for i,mutate in enumerate(variants):
            def bad(*a,**kw):
                observed=self.fake_supervisor(*a,**kw);mutate(observed);put(Path(kw["output_dir"])/"supervisor-result.json",observed);return observed
            with self.subTest(i=i),self.assertRaises(ValueError):self.complete("bad"+str(i),effect=bad)
            self.assertFalse((self.root/("bad"+str(i))/"STAGE_COMPLETED.json").exists())

    def test_mathematical_field_or_control_change_fails_even_if_recaptured(self):
        for key,value in(("final_D","0"),("status","FAIL"),("negative_controls",["invented"]),("n",True)):
            def changed(*a,**kw):
                observed=self.fake_supervisor(*a,**kw);row=src.job(src.read(Path(kw["output_dir"]).parent/"SOURCES.json")["job_id"])
                native=Path(kw["output_dir"]).parent/"capsule"/src.output_relative(row)
                d=src.read(native);d[key]=value;put(native,d)
                capture=observed["checkpoints"][0];shutil.copyfile(native,capture["path"])
                capture.update(bytes=native.stat().st_size,sha256=src.digest(native));put(Path(kw["output_dir"])/"supervisor-result.json",observed)
                return observed
            with self.subTest(key=key),self.assertRaises(ValueError):self.complete("changed-"+key,effect=changed)

    def test_entire_fresh_parent_join_ignores_only_top_elapsed_seconds(self):
        root=self.root/"batch";root.mkdir();status=dict(jobs=[])
        with patch.object(run.linux_supervisor,"run",side_effect=self.fake_supervisor)as launch,patch.object(run,"Follow"):
            run.batch_jobs(root,self.root/"complete-cache",self.cache,status,self.rows)
        self.assertEqual(launch.call_count,2);edges=status["jobs"][1]["fresh_parent_metadata_interfaces"]
        self.assertEqual(len(edges),1);self.assertNotEqual(edges[0]["conditional_statement_sha256"],edges[0]["fresh_receipt_sha256"])
        status2=dict(jobs=[]);again=self.root/"again";again.mkdir()
        with patch.object(run.linux_supervisor,"run",side_effect=AssertionError("Completed work must be reused")):
            run.batch_jobs(again,self.root/"complete-cache",self.cache,status2,self.rows)
        self.assertTrue(all(row["reused_completed_stage"]for row in status2["jobs"]))

    def test_missing_fresh_parent_dependency_cannot_join(self):
        task,_=self.complete("resource-only",self.rows[1])
        with self.assertRaisesRegex(ValueError,"freshly replayed parent"):run.join_fresh_inputs(self.root,task,self.rows[1],dict(jobs=[]))

    def test_parent_join_does_not_ignore_nested_duration_fields(self):
        parent,checked=self.complete("parent")
        child,_=self.complete("child",self.rows[1])
        receipt=parent/checked["summary"]["receipt_relative"];data=src.read(receipt)
        data["numerical_premises"]["seconds"]=.25;put(receipt,data)
        ledger=dict(jobs=[dict(job_id=self.row["job_id"],task_relative="parent")])
        # Isolate the join relation; full stage validation already rejects this
        # mutation independently, and is not treated as actual arithmetic here.
        with patch.object(ev,"validate_completed",return_value=checked),self.assertRaisesRegex(ValueError,"beyond"):
            run.join_fresh_inputs(self.root,child,self.rows[1],ledger)

    def test_missing_timed_initial_expected_metadata_is_not_acceptance(self):
        directory=self.root/"static-only/capsule/work/initial7_9"
        case="n7_B0";candidate=dict(n=7,band="B0",profile=dict(q_contact="0",invariants=dict(rho_lo="1",rho="11/10")),
            assumed_owncap=".423",assumed_HIGH=".345",signed_support_rows=[{}]*4,
            stages=[dict(cover=dict(active=2,gap_active=2))for _ in range(9)],final_invariants=dict(raw="1/2",D="1/10"))
        pin=put(directory/case/"INPUT.json",candidate);put(directory/case/"PREPARED.json",dict(input_sha256=pin))
        (directory/"replay.py").write_text("raise AssertionError('never execute')\nresult=dict(status='PASS_INITIAL',scope='CONDITIONAL_ONLY')\n")
        row=dict(lane="initial7_9",kind="initial",directory="work/initial7_9",output=case+"/REPLAY_CHECKED.json",
                 reference=dict(native_answer=None),source_files_sha256={},native_controls=[str(i)for i in range(27)])
        expected=src.expected_native(self.root/"static-only",row)
        self.assertEqual(expected["numerical_premises"]["HIGH"],"69/200");self.assertEqual(expected["final_D"],"1/10")
        self.assertNotIn("seconds",expected);self.assertFalse((directory/case/"REPLAY_CHECKED.json").exists())

    def test_extra_source_false_global_or_wrong_capture_context_fails(self):
        task,_=self.complete();observed=src.read(task/"STAGE_OBSERVED.json")
        observed["parent_acquisitions_verified"]=True;put(task/"STAGE_OBSERVED.json",observed)
        with self.assertRaises(ValueError):ev.validate_completed(task)
        prepared=self.root/"extra";src.prepare_job(self.row["job_id"],self.cache,prepared)
        (prepared/"capsule/unbound.py").write_text("pass")
        with self.assertRaises(ValueError):src.verify_job(prepared)

    def test_failure_bundle_keeps_explicit_false_scope(self):
        with patch.object(src,"obtain_assets",side_effect=ValueError("Synthetic transport failure")),patch.object(run,"LogBackups"):
            result=run.run_colab("n6",durable_root=self.root/"durable",work_root=self.root/"work")
        self.assertEqual(result["status"]["state"],"incomplete_selected_parent_arithmetic")
        self.assertTrue(Path(result["bundle"]).is_file());self.assertFalse(result["status"]["fresh_parent_metadata_interfaces_verified"])
        for flag in ev.FLAGS:self.assertIs(result["status"][flag],False)

    def test_cache_preflight_still_requires_full_ledgers(self):
        class Incomplete:
            def infolist(self):return[zipfile.ZipInfo("SOURCES.json")]
        with self.assertRaises(ValueError):run.cache_members(Incomplete())

    def test_unknown_lane_rejected_before_work(self):
        for lane in("n7","all",6,True):
            with self.subTest(lane=lane),self.assertRaises(ValueError):run.run_colab(lane,durable_root=self.root/"durable",work_root=self.root/"unused")
        self.assertFalse((self.root/"unused").exists())

    def test_every_actual_catalog_identifier_routes_including_fifth_underscore(self):
        # Read metadata only; the fixture does not prepare or run these sources.
        rows=src.read(src.CATALOG,limit=32*src.MIB)["jobs"]
        names=[run.slug(row["job_id"])for row in rows]
        self.assertEqual(len(names),50);self.assertEqual(len(set(names)),50)
        selected=[r for r in rows if r["lane"]=="n6"]
        self.assertEqual(selected[4]["job_id"],"n6.panel.b0_40")
        self.assertEqual(run.slug(selected[4]["job_id"]),"n6-panel-b0_40")
        for identifier in("../escape","a/b","a\\b","C:drive","a b","a\n",True,None,"zażółć"):
            with self.subTest(identifier=identifier),self.assertRaises(ValueError):run.slug(identifier)

    def test_exact_historical_implementation_has_no_wildcard(self):
        old=copy.deepcopy(ev.PRE_SLUG_FIX_IMPLEMENTATION)
        self.assertTrue(ev.implementation_allowed(old));self.assertTrue(ev.implementation_allowed(ev.implementation()))
        for key in old:
            bad=dict(old);bad[key]="0"*64
            with self.subTest(key=key):self.assertFalse(ev.implementation_allowed(bad))
        for bad in(dict(old,unknown="0"*64),{k:v for k,v in old.items()if k!="linux_supervisor.py"}):
            self.assertFalse(ev.implementation_allowed(bad))

    def test_four_old_completed_caches_are_preserved_and_only_fifth_underscore_executes(self):
        ids=("n6.initial.B0","n6.initial.B2","n6.initial.BN","n6.initial.outer.BN","n6.panel.b0_40")
        rows=[]
        for identifier in ids:
            row=copy.deepcopy(self.row);row["job_id"]=identifier
            row["kind"]="local_initial"if"panel"in identifier else"initial";rows.append(row)
        self.cat["jobs"]=rows;cache=self.root/"legacy-cache";saved={}
        old=copy.deepcopy(ev.PRE_SLUG_FIX_IMPLEMENTATION)
        for i,row in enumerate(rows[:4]):
            # Generate synthetic old-context evidence, not a historical proof.
            with patch.object(ev,"implementation",return_value=old):
                task,_=self.complete("old"+str(i),row)
                result=run.save_stage(task,cache/run.slug(row["job_id"]))
            saved[Path(result["path"])]=src.digest(result["path"])
        root=self.root/"resumed-five";root.mkdir();status=dict(jobs=[])
        with patch.object(run.linux_supervisor,"run",side_effect=self.fake_supervisor)as launch,patch.object(run,"Follow"):
            run.batch_jobs(root,cache,self.cache,status,rows)
        self.assertEqual(launch.call_count,1)
        self.assertEqual([r["reused_completed_stage"]for r in status["jobs"]],[True,True,True,True,False])
        self.assertEqual(status["jobs"][-1]["job_id"],"n6.panel.b0_40")
        for path,pin in saved.items():self.assertEqual(src.digest(path),pin)
        for row in status["jobs"]:
            for flag in ev.FLAGS:self.assertIs(row["validated"][flag],False)
        again=self.root/"all-five-cached";again.mkdir();second=dict(jobs=[])
        with patch.object(run.linux_supervisor,"run",side_effect=AssertionError("No completed stage should rerun")):
            run.batch_jobs(again,cache,self.cache,second,rows)
        self.assertTrue(all(r["reused_completed_stage"]for r in second["jobs"]))

    def test_historical_context_still_rejects_native_mutation_and_mixed_epoch(self):
        old=copy.deepcopy(ev.PRE_SLUG_FIX_IMPLEMENTATION)
        with patch.object(ev,"implementation",return_value=old):task,_=self.complete("historical")
        ev.validate_completed(task)
        complete=src.read(task/"STAGE_COMPLETED.json");complete["implementation"]=ev.implementation();put(task/"STAGE_COMPLETED.json",complete)
        with self.assertRaisesRegex(ValueError,"completed transition"):ev.validate_completed(task)
        with patch.object(ev,"implementation",return_value=old):task,_=self.complete("historical-native")
        packet=src.read(task/"STAGE_OBSERVED.json");packet["observed"]["returncode"]=False
        put(task/"execution/supervisor-result.json",packet["observed"]);put(task/"STAGE_OBSERVED.json",packet)
        complete=src.read(task/"STAGE_COMPLETED.json");complete["observed_sha256"]=src.digest(task/"STAGE_OBSERVED.json");put(task/"STAGE_COMPLETED.json",complete)
        with self.assertRaisesRegex(ValueError,"successful BASIC"):ev.validate_completed(task)


if __name__=="__main__":unittest.main()
