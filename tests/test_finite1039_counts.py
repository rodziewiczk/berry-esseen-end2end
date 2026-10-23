"""Synthetic original-acceptor evidence/cache tests; no numerical source loads."""
from __future__ import annotations
import copy
import io
import json
from pathlib import Path
import shutil
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import finite1039_sources as src, finite1039_counts as run, finite1039_count_evidence as ev


def put(path, packet):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(packet, indent=2)+"\n").encode())
    return src.digest(path)


class Counts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cache = self.root/"inputs"
        self.rows = []
        for family, n, lane in (("count_protocol",10,"n10_14"),("strict",31,"n31_34"),("strict",32,"n31_34")):
            index=40 if n==10 else 36 if n==31 else 44
            dimensions=4 if n==32 else 5
            contract_field="targets_sha256" if n==32 else "contract_sha256"
            allowance="27/50" if n==32 else "0"
            directory=f"work/{family}{n}/capsule{index}"
            folder=self.cache/directory
            folder.mkdir(parents=True)
            script="count_protocol.py" if family=="count_protocol" else "accept_strict.py"
            for name in (script,"engine.py"):
                (folder/name).write_bytes(b"raise AssertionError('Never execute or import original numerical source locally')\n")
            contract_pin=put(folder/"contract.json",dict(n=n,index=index,K=allowance,premise="SYNTHETIC_CONDITIONAL_ONLY"))
            local_sources={name:src.digest(folder/name)for name in(script,"engine.py","contract.json")}
            root=[["0","1"] for _ in range(dimensions)]
            if family=="count_protocol":
                kernels={"engine.py":local_sources["engine.py"]}
                put(folder/"KERNEL_COPY_MANIFEST.json",dict(files=kernels))
                candidate_name="COUNT_FOREST.json";output="COUNT_ACCEPTED.json"
                candidate=dict(n=n,index=index,target="2/5",contract_sha256=contract_pin,
                    checker_sha256=local_sources[script],kernel_sha256=kernels,
                    roots=[dict(k=k,tree=dict(kind="leaf",box=root,decision="PASS_TARGET",result=dict(score_upper="1/4")))for k in range(n+1)])
                candidate_pin=put(folder/candidate_name,candidate)
                controls=["synthetic-control-"+str(i)for i in range(24)]
                answer=dict(status="PASS_FAKE_COUNT",scope="SYNTHETIC_CONDITIONAL_ONLY",n=n,index=index,
                    kernel_sha256=kernels,forest_sha256=candidate_pin,contract_sha256=contract_pin,
                    checker_sha256=local_sources[script],negative_controls=controls,
                    statistics=dict(nodes=n+1,leaves=n+1,maximum_depth=0,closed_statuses=dict(PASS_TARGET=n+1),maximum_score="1/4"),
                    fresh_leaf_evaluations=n+1,seconds=123.0)
                rule=dict(kind="json_receipt");ignored=["seconds"]
            else:
                candidate_name=f"candidate_{index}.json";output=f"accepted_strict_{index}.json"
                candidate=dict(schema="FAKE_FLAT",status="EXACT_CONSTRUCTION_COMPLETE",index=index,
                    root=root,splits=[],leaves=[dict(k=k,path=[],status="PASS_BELOW_CE",score_upper="1/4")for k in range(n+1)],
                    visited=n+1,maximum_score="1/4",target_lower="2/5")
                candidate[contract_field]=contract_pin
                candidate_pin=put(folder/candidate_name,candidate)
                controls=15 if n==32 else 19
                answer=dict(schema="FAKE_STRICT_RECEIPT",status="PASS",n=n,index=index,K=allowance,contract_sha256=contract_pin,
                    candidate_sha256=candidate_pin,source_sha256=local_sources,passed_cells=n+1,empty_cells=0,
                    all_closed_leaves=n+1,maximum_score="1/4",target_lower="2/5",negative_controls=controls)
                rule=dict(kind="text",prefix="ACCEPTED_FAKE_STRICT",tokens=8,index_token=1);ignored=["child_runtime"]
            files={p.relative_to(self.cache).as_posix():src.digest(p)for p in folder.iterdir()}
            row=dict(job_id=f"n{n}.fake.p{index}",lane=lane,family=family,n=n,index=index,directory=directory,
                script=script,arguments=["accept"]if family=="count_protocol"else[str(index)],output=output,candidate=candidate_name,
                contract_name="contract.json",contract_sha256=contract_pin,candidate_sha256=candidate_pin,
                source_files_sha256=files,expected_receipt=answer,expected_controls=controls,ignored_runtime_fields=ignored,
                stdout_rule=rule,child_runtime_required=family=="strict"and n==31,
                dimensions=dimensions,candidate_contract_field=contract_field)
            row["census"]=src.inspect_candidate(row,candidate)
            # An old output exists in the cache, but is not one of the sealed inputs.
            put(folder/output,answer)
            self.rows.append(row)
        self.row=self.rows[0]
        lanes={lane:dict(forests=sum(r["lane"]==lane for r in self.rows),available_forests=sum(r["lane"]==lane for r in self.rows),
                        **{k:sum(r["census"][k]for r in self.rows if r["lane"]==lane)for k in("roots","nodes","leaves")})
               for lane in {r["lane"]for r in self.rows}}
        self.cat=dict(jobs=self.rows,lane_ready={row["lane"]:True for row in self.rows},
                      remaining_obligations=["External predecessor/support/resource facts remain conditional"],lanes=lanes)
        for target,name,value in ((src,"catalog",self.cat),(run.sys,"platform","linux"),(run.sys,"stdout",io.StringIO())):
            p=patch.object(target,name,return_value=value)if name=="catalog"else patch.object(target,name,value)
            p.start();self.addCleanup(p.stop)

    def fake_supervisor(self,argv, *,cwd,output_dir,**kwargs):
        output_dir=Path(output_dir);task=output_dir.parent;request=src.read(task/"SOURCES.json");row=src.job(request["job_id"])
        answer=copy.deepcopy(row["expected_receipt"])
        if "seconds"in answer:answer["seconds"]=.25
        if row["child_runtime_required"]:
            answer["child_runtime"]=dict(executable=argv[0],version=run.sys.version,optimize=0)
        native=task/"capsule"/src.output_relative(row);put(native,answer)
        output_dir.mkdir()
        if row["family"]=="count_protocol":stdout="ORIGINAL_PROGRESS 1\n"+json.dumps(answer,indent=2)+"\n"
        else:stdout=f"ORIGINAL_PROGRESS 1\nACCEPTED_FAKE_STRICT {row['index']} {row['n']+1} 0 {row['n']+1} {row['expected_controls']} 0.25 0.1\n"
        (output_dir/"stdout.txt").write_bytes(stdout.encode());(output_dir/"stderr.txt").write_bytes(b"")
        kwargs["checkpoint_paths"]=[str(Path(p).resolve())for p in kwargs["checkpoint_paths"]]
        launch=dict(argv=argv,cwd=str(cwd),output_dir=str(output_dir),sample_seconds=.2,**kwargs)
        launch["wall_seconds"]=float(launch["wall_seconds"]);launch["heartbeat_seconds"]=float(launch["heartbeat_seconds"])
        put(output_dir/"launch.json",launch)
        captured=output_dir/"checkpoints"/row["output"];captured.parent.mkdir(parents=True);shutil.copyfile(native,captured)
        guard=dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",proof_acceptance=False,
            external_wall_seconds=float(ev.WALL_SECONDS),per_process_RLIMIT_AS_bytes=ev.MEMORY_BYTES,
            per_process_RLIMIT_CPU_seconds=ev.CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,
            sampled_group_RSS_limit_bytes=ev.MEMORY_BYTES,sampled_group_CPU_limit_seconds=ev.CPU_SECONDS,
            sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,
            descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
        observed=dict(status="completed",reason=None,returncode=0,proof_accepted=False,mode="untrusted_search",sample_count=1,
            elapsed_seconds=.5,maximum_sampled_group_RSS_bytes=src.MIB,maximum_sampled_group_CPU_seconds=.25,
            guard_scope=guard,checkpoints=[dict(source_path=str(native),path=str(captured),exists=True,trusted_certificate=False,
                bytes=native.stat().st_size,sha256=src.digest(native))],
            **{kind+suffix:value for kind in("stdout","stderr")for suffix,value in(
                ("_path",str(output_dir/(kind+".txt"))),("_sha256",src.digest(output_dir/(kind+".txt"))))})
        put(output_dir/"supervisor-result.json",observed)
        return observed

    def complete(self,name="task",row=None,effect=None):
        task=self.root/name
        with patch.object(run.linux_supervisor,"run",side_effect=effect or self.fake_supervisor),patch.object(run,"Follow"):
            checked=run.execute(task,row or self.row,self.cache)
        return task,checked

    def test_both_original_representations_capture_whole_fresh_receipt(self):
        for i,row in enumerate(self.rows):
            task,checked=self.complete("family"+str(i),row)
            self.assertEqual(checked["summary"]["family"],row["family"])
            self.assertEqual(checked["summary"]["census"]["roots"],row["n"]+1)
            for flag in ev.FLAGS:self.assertIs(checked[flag],False)
            captured=task/"execution/checkpoints"/row["output"]
            self.assertEqual(captured.read_bytes(),(task/checked["summary"]["receipt_relative"]).read_bytes())

    def test_old_own_output_is_not_copied(self):
        task=self.root/"prepared";src.prepare_job(self.row["job_id"],self.cache,task)
        self.assertFalse((task/"capsule"/src.output_relative(self.row)).exists())

    def test_four_coordinate_auxiliary_contract_keeps_nonzero_allowance(self):
        row=self.rows[2];task,checked=self.complete("auxiliary",row)
        receipt=src.read(task/checked["summary"]["receipt_relative"])
        self.assertEqual(receipt["K"],"27/50")
        self.assertEqual(receipt["negative_controls"],15)
        self.assertEqual(checked["summary"]["census"]["roots"],33)
        self.assertEqual(len(src.read(task/"capsule"/row["directory"]/row["candidate"])["root"]),4)

    def test_relocated_whole_stage_revalidates_without_rewriting(self):
        task,checked=self.complete();other=self.root/"relocated";shutil.copytree(task,other)
        before={p.relative_to(other).as_posix():p.read_bytes()for p in other.rglob("*")if p.is_file()}
        self.assertEqual(ev.validate_completed(other),checked)
        self.assertEqual(before,{p.relative_to(other).as_posix():p.read_bytes()for p in other.rglob("*")if p.is_file()})

    def test_bad_return_status_checkpoint_or_guard_never_completes(self):
        changes=(lambda x:x.update(returncode=False),lambda x:x.update(status="incomplete"),
                 lambda x:x.update(checkpoints=[]),lambda x:x["checkpoints"][0].update(sha256="0"*64),
                 lambda x:x["checkpoints"][0].update(trusted_certificate=True),
                 lambda x:x.update(elapsed_seconds=float("nan")),
                 lambda x:x["guard_scope"].update(aggregate_kernel_memory_limit=True))
        for i,change in enumerate(changes):
            def bad(*a,**kw):
                obs=self.fake_supervisor(*a,**kw);change(obs);put(Path(kw["output_dir"])/"supervisor-result.json",obs);return obs
            with self.subTest(i=i),self.assertRaises(ValueError):self.complete("bad"+str(i),effect=bad)
            self.assertFalse((self.root/("bad"+str(i))/"STAGE_COMPLETED.json").exists())

    def test_wrong_launch_cwd_or_literal_command_fails(self):
        for i,key in enumerate(("cwd","argv","checkpoint_paths")):
            def bad(*a,**kw):
                obs=self.fake_supervisor(*a,**kw);p=Path(kw["output_dir"])/"launch.json";launch=src.read(p)
                if key=="cwd":launch[key]=str(Path(kw["output_dir"]).parent)
                elif key=="argv":launch[key][-1]="different"
                else:launch[key]=[]
                put(p,launch);return obs
            with self.subTest(key=key),self.assertRaises(ValueError):self.complete("launch"+str(i),effect=bad)

    def test_full_receipt_changes_fail_even_when_recaptured(self):
        for i,(row,key,value)in enumerate(((self.rows[0],"negative_controls",["fewer"]),
                (self.rows[0],"fresh_leaf_evaluations",1),(self.rows[0],"n",True),
                (self.rows[1],"negative_controls",True),(self.rows[1],"maximum_score","0"),
                (self.rows[1],"contract_sha256","0"*64))):
            def bad(*a,**kw):
                obs=self.fake_supervisor(*a,**kw);task=Path(kw["output_dir"]).parent;native=task/"capsule"/src.output_relative(row)
                answer=src.read(native);answer[key]=value;put(native,answer)
                cap=obs["checkpoints"][0];shutil.copyfile(native,cap["path"]);cap.update(bytes=native.stat().st_size,sha256=src.digest(native))
                put(Path(kw["output_dir"])/"supervisor-result.json",obs);return obs
            with self.subTest(key=key,family=row["family"]),self.assertRaises(ValueError):self.complete("receipt"+str(i),row,effect=bad)

    def test_changed_receipt_after_stopped_capture_fails(self):
        task,_=self.complete();native=task/"capsule"/src.output_relative(self.row);answer=src.read(native)
        answer["seconds"]=.75;put(native,answer)
        with self.assertRaises(ValueError):ev.validate_completed(task)

    def test_actual_stderr_and_stdout_hashes_are_required(self):
        for i,kind in enumerate(("stdout","stderr")):
            def bad(*a,**kw):
                obs=self.fake_supervisor(*a,**kw);obs[kind+"_sha256"]="0"*64
                put(Path(kw["output_dir"])/"supervisor-result.json",obs);return obs
            with self.subTest(kind=kind),self.assertRaises(ValueError):self.complete("capture"+str(i),effect=bad)

    def test_nonempty_stderr_is_not_a_success(self):
        def bad(*a,**kw):
            obs=self.fake_supervisor(*a,**kw);path=Path(kw["output_dir"])/"stderr.txt";path.write_bytes(b"warning\n")
            obs["stderr_sha256"]=src.digest(path);put(Path(kw["output_dir"])/"supervisor-result.json",obs);return obs
        with self.assertRaisesRegex(ValueError,"stderr"):self.complete(effect=bad)

    def test_strict_marker_and_index_are_source_specific(self):
        row=self.rows[1]
        for i,text in enumerate(("PASS 36\n","ACCEPTED_FAKE_STRICT 37 32 0 32 19 0.25 0.1\n")):
            def bad(*a,**kw):
                obs=self.fake_supervisor(*a,**kw);p=Path(kw["output_dir"])/"stdout.txt";p.write_bytes(text.encode())
                obs["stdout_sha256"]=src.digest(p);put(Path(kw["output_dir"])/"supervisor-result.json",obs);return obs
            with self.subTest(i=i),self.assertRaises(ValueError):self.complete("marker"+str(i),row,effect=bad)

    def test_strict_terminal_counts_score_and_elapsed_match_fresh_receipt(self):
        row=self.rows[1];answer=copy.deepcopy(row["expected_receipt"])
        valid="ACCEPTED_FAKE_STRICT 36 32 0 32 19 0.25 0.1"
        ev.stdout_matches(valid,row,answer)
        for index,value in ((2,"31"),(3,"1"),(4,"31"),(5,"24"),(6,"0.2"),(7,"nan"),(7,"-1"),(7,"bad")):
            tokens=valid.split();tokens[index]=value
            with self.subTest(index=index,value=value),self.assertRaises(ValueError):
                ev.stdout_matches(" ".join(tokens),row,answer)

    def test_only_declared_runtime_field_is_ignored(self):
        row=self.rows[1];answer=copy.deepcopy(row["expected_receipt"])
        context=dict(python_executable=run.sys.executable,python_version=run.sys.version)
        answer["child_runtime"]=dict(executable=run.sys.executable,version=run.sys.version,optimize=0)
        ev.untimed_receipt(answer,row,**context)
        answer["child_runtime"]["optimize"]=True
        with self.assertRaises(ValueError):ev.untimed_receipt(answer,row,**context)
        answer=copy.deepcopy(self.row["expected_receipt"]);answer["statistics"]["seconds"]=.5
        with self.assertRaises(ValueError):ev.untimed_receipt(answer,self.row,**context)

    def test_strict_runtime_schema_executable_and_version_are_not_discarded(self):
        row=self.rows[1];base=copy.deepcopy(row["expected_receipt"])
        base["child_runtime"]=dict(executable=run.sys.executable,version=run.sys.version,optimize=0)
        context=dict(python_executable=run.sys.executable,python_version=run.sys.version)
        for field,value in (("executable","/different/python"),("version","invented"),("optimize",False),("extra","unbound")):
            answer=copy.deepcopy(base);answer["child_runtime"][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):ev.untimed_receipt(answer,row,**context)
        del base["child_runtime"]
        with self.assertRaises(ValueError):ev.untimed_receipt(base,row,**context)

    def test_unbound_source_or_false_acceptance_flag_fails(self):
        task,_=self.complete();(task/"capsule"/self.row["directory"]/"unbound.py").write_bytes(b"pass\n")
        with self.assertRaises(ValueError):ev.validate_completed(task)
        task,_=self.complete("other");report=src.read(task/"STAGE_OBSERVED.json");report["native_arithmetic_accepted"]=True;put(task/"STAGE_OBSERVED.json",report)
        with self.assertRaises(ValueError):ev.validate_completed(task)

    def test_cache_roundtrip_reuses_only_fully_validated_completed_job(self):
        task,checked=self.complete();cache=self.root/"completed";run.save_stage(task,cache)
        restored=run.restore_stage(cache,self.root/"restored",self.row)
        self.assertIsNotNone(restored);self.assertEqual(restored[1],checked)
        self.assertEqual(ev.validate_completed(restored[0]),checked)

    def test_corrupt_completed_zip_is_advisory_and_rejected(self):
        cache=self.root/"completed";cache.mkdir();p=cache/"zz-complete.zip";p.write_bytes(b"not-a-zip")
        p.with_suffix(".zip.sha256").write_text(src.digest(p)+"  "+p.name+"\n",encoding="ascii")
        self.assertIsNone(run.restore_stage(cache,self.root/"restored",self.row))

    def test_cache_traversal_duplicate_case_and_links_fail_preflight(self):
        required=["SOURCES.json","STAGE_OBSERVED.json","STAGE_COMPLETED.json","execution/launch.json",
                  "execution/supervisor-result.json","execution/stdout.txt","execution/stderr.txt"]
        for name,mode in (("../escape",0),("SOURCES.JSON",0),("link",stat.S_IFLNK<<16)):
            rows=[zipfile.ZipInfo(n)for n in required];extra=zipfile.ZipInfo(name);extra.external_attr=mode;rows.append(extra)
            class Fake:
                def infolist(self):return rows
            with self.subTest(name=name),self.assertRaises(ValueError):run.cache_members(Fake())

    def test_failure_still_exports_a_false_scope_bundle(self):
        with patch.object(src,"obtain_assets",side_effect=ValueError("Synthetic unavailable source")),patch.object(run,"LogBackups"),patch.object(run,"FOREST_COUNTS",{"n10_14":1}):
            result=run.run_colab("n10_14",durable_root=self.root/"durable",work_root=self.root/"work")
        self.assertTrue(Path(result["bundle"]).is_file());self.assertEqual(result["status"]["state"],"incomplete_selected_count_arithmetic")
        for flag in ev.FLAGS:self.assertIs(result["status"][flag],False)

    def test_whole_batch_completes_then_reuses_only_verified_stage_zips(self):
        options=dict(durable_root=self.root/"durable",work_root=self.root/"runs")
        with patch.object(src,"obtain_assets",return_value={}),patch.object(src,"prepare_cache",return_value=self.cache),\
                patch.object(run,"LogBackups"),patch.object(run,"Follow"),patch.object(run,"FOREST_COUNTS",{"n10_14":1}),\
                patch.object(run.linux_supervisor,"run",side_effect=self.fake_supervisor)as called:
            first=run.run_colab("n10_14",**options)
        self.assertEqual(called.call_count,1)
        self.assertEqual(first["status"]["state"],"complete_selected_conditional_count_arithmetic_basic")
        self.assertEqual(first["status"]["actual_census"],{k:v for k,v in self.cat["lanes"]["n10_14"].items()if k!="available_forests"})
        with patch.object(src,"obtain_assets",return_value={}),patch.object(src,"prepare_cache",return_value=self.cache),\
                patch.object(run,"LogBackups"),patch.object(run,"FOREST_COUNTS",{"n10_14":1}),\
                patch.object(run.linux_supervisor,"run",side_effect=AssertionError("No completed stage numerical rerun")):
            second=run.run_colab("n10_14",**options)
        self.assertEqual(second["status"]["state"],"complete_selected_conditional_count_arithmetic_basic")
        self.assertIs(second["status"]["jobs"][0]["reused_completed_stage"],True)
        for flag in ev.FLAGS:self.assertIs(second["status"][flag],False)

    def test_unknown_lane_rejects_before_work(self):
        for lane in (10,True,"n25","all"):
            with self.subTest(lane=lane),self.assertRaises(ValueError):run.run_colab(lane,durable_root=self.root/"durable",work_root=self.root/"absent")
        self.assertFalse((self.root/"absent").exists())

    def test_source_incomplete_lane_rejects_before_work_or_download(self):
        self.cat["not_ready_lanes"]={"n10_14":dict(reason="Synthetic missing selected candidate")}
        with patch.object(src,"obtain_assets",side_effect=AssertionError("No incomplete-lane download")),\
                self.assertRaisesRegex(ValueError,"not source-complete"):
            run.run_colab("n10_14",durable_root=self.root/"durable",work_root=self.root/"absent")
        self.assertFalse((self.root/"absent").exists())

    def test_actual_catalog_ready_census_reaches_transport_without_starting_math(self):
        declaration=src.read(src.CATALOG,limit=64*src.MIB)
        with patch.object(src,"catalog",return_value=declaration),\
                patch.object(src,"obtain_assets",side_effect=ValueError("Synthetic transport barrier reached"))as transport,\
                patch.object(run,"LogBackups"),\
                patch.object(run.linux_supervisor,"run",side_effect=AssertionError("No mathematical worker")):
            result=run.run_colab("n10_14",durable_root=self.root/"durable",work_root=self.root/"actual-catalog")
        self.assertIn("Synthetic transport barrier reached",result["status"]["error"])
        self.assertEqual(result["status"]["expected_census"],
                         {k:v for k,v in declaration["lanes"]["n10_14"].items()if k!="available_forests"})
        transport.assert_called_once()

    def test_ready_flag_cannot_override_an_incomplete_available_census(self):
        self.cat["lanes"]["n10_14"]["available_forests"]=2
        with patch.object(src,"obtain_assets",side_effect=AssertionError("No inconsistent-lane download")),\
                patch.object(run,"FOREST_COUNTS",{"n10_14":1}),\
                self.assertRaisesRegex(ValueError,"lane census"):
            run.run_colab("n10_14",durable_root=self.root/"durable",work_root=self.root/"absent")
        self.assertFalse((self.root/"absent").exists())


if __name__=="__main__":unittest.main()
