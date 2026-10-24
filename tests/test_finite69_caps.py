"""Synthetic/source-only fixtures; original mathematical kernels are not run."""
from __future__ import annotations
import copy
import hashlib
import io
import json
from pathlib import Path
import shutil
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import finite69_caps as runner,finite69_caps_sources as src,finite69_caps_evidence as ev


def write(path,raw):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(raw if isinstance(raw,bytes)else src.dump(raw));return path


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.numpy=patch.object(runner,"numpy_context",return_value=dict(scope="SYNTHETIC_NO_NUMPY_IMPORT"));self.numpy.start()
    def tearDown(self):self.numpy.stop();self.temp.cleanup()
    def transport_fixture(self):
        task=self.root/"task";task.mkdir();original=str(task.resolve())
        request=dict(kind="resource",job_id="synthetic",original_task_root=original)
        relative="work/native/case/REPLAY_CHECKED.json"
        spec=dict(label="resource",directory="work/native/",argv=["python","-B","-S",str(task/"capsule/work/native/FRESH_REPLAY.py"),"7","B0"],outputs=[relative])
        output=write(task/"capsule"/relative,dict(status="SYNTHETIC_ONLY"))
        directory=task/"executions/resource";copied=write(directory/"checkpoints"/relative,output.read_bytes())
        stdout=write(directory/"stdout.txt",b"SYNTHETIC_ONLY\n");stderr=write(directory/"stderr.txt",b"")
        scope=dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",proof_acceptance=False,external_wall_seconds=float(ev.WALL),
            per_process_RLIMIT_AS_bytes=ev.MEMORY,per_process_RLIMIT_CPU_seconds=ev.CPU,aggregate_kernel_memory_limit=False,
            aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=ev.MEMORY,sampled_group_CPU_limit_seconds=ev.CPU,
            sampled_file_limit_bytes=ev.DISK,sampled_log_limit_bytes=16*src.MIB,descendants_changing_session_are_contained=False,
            equivalent_to_Windows_Job_or_cgroup=False)
        observed=dict(status="completed",returncode=0,reason=None,proof_accepted=False,mode="untrusted_search",sample_count=1,
            guard_scope=scope,stdout_path=str(stdout),stderr_path=str(stderr),stdout_sha256=src.digest(stdout),stderr_sha256=src.digest(stderr),
            checkpoints=[dict(source_path=str(output),exists=True,trusted_certificate=False,path=str(copied),bytes=output.stat().st_size,sha256=src.digest(output))])
        launch=dict(argv=spec["argv"],cwd=str(task/"capsule"),output_dir=str(directory),mode="untrusted_search",
            sample_seconds=.2,heartbeat_seconds=20.0,cpu_seconds=ev.CPU,wall_seconds=float(ev.WALL),memory_bytes=ev.MEMORY,
            disk_bytes=ev.DISK,log_bytes=16*src.MIB,checkpoint_paths=[str(output)])
        write(directory/"launch.json",launch);write(directory/"supervisor-result.json",observed)
        return task,request,spec,dict(label="resource",observed=observed),launch


class SourceAndRouting(Fixture):
    def test_actual_catalog_scope_and_no_old_dynamic_inputs(self):
        d=src.catalog();self.assertEqual(770,len(d["source_files"]))
        self.assertEqual(232629254,sum(r["bytes"]for r in d["source_files"].values()))
        self.assertEqual(9,len(src.resource_rows()))
        self.assertFalse(set(src.epoch.DYNAMIC)&set(d["source_files"]))
        self.assertFalse(set(d["original_initial_outputs_as_provenance_only"])&set(d["source_files"]))
        self.assertEqual(src.EPOCH_SHA256,src.digest(src.epoch.__file__))

    def test_exact_five_calls_and_outer_cwd_can_capture_workspace_outputs(self):
        request=dict(kind="owncaps",original_task_root="/content/private/stage")
        specs=ev.action_specs(request,"/usr/bin/python3")
        self.assertEqual(["plan","construct","replay","readback","caps"],[s["label"]for s in specs])
        self.assertEqual(14,sum(len(s["outputs"])for s in specs))
        self.assertTrue(all(s["argv"][:3]==["/usr/bin/python3","-B","-S"]for s in specs))
        self.assertIn("/content/private/stage/capsule/runs/",specs[1]["argv"][-1])
        self.assertEqual("construct",specs[1]["argv"][4])
        self.assertEqual("replay",specs[2]["argv"][4])

    def test_synthetic_source_preparation_seals_bytes_without_importing_trap(self):
        cache=self.root/"cache";trap="work/native/trap.py";raw=b"raise AssertionError('MATH MUST NOT RUN')\n"
        write(cache/trap,raw);old={"files_sha256":{trap:hashlib.sha256(raw).hexdigest()}}
        write(cache/src.CAPS,old);old_sha=src.digest(cache/src.CAPS)
        d=dict(entry_sources={},original_source_pins=old["files_sha256"])
        with patch.object(src,"catalog",return_value=d),patch.object(src.epoch,"ORIGINAL_CAPS_SHA",old_sha):
            task=self.root/"stage";r=src.prepare_own(cache,task)
            self.assertFalse((task/"capsule"/src.CAPS).exists())
            self.assertEqual(raw,(task/"capsule"/trap).read_bytes())
            self.assertEqual([trap],list(r["static_inputs"]))
            write(task/"capsule/extra_import.py",b"pass\n")
            with self.assertRaisesRegex(ValueError,"Exact sealed"):src.verify_job(task)

    def test_pinned_sources_cannot_be_moved_into_generated_partition(self):
        row=src.resource_rows()[0];case=row["output"].split("/")[0]
        parent=row["reference"]["native_answer"]["initial_receipt"]
        changed=set(src.epoch.DYNAMIC)|{src.CAPS,parent}
        pins={k:v for k,v in row["source_files_sha256"].items()if k not in changed}
        add={src.RESOURCE+"FRESH_REPLAY.py",src.RESOURCE+case+"/FRESH_PREPARED.json",src.RESOURCE+case+"/FRESH_SOURCE_RESULT.json"}
        r=dict(schema=src.SCHEMA,kind="resource",job_id=row["job_id"],catalog_sha256=src.CATALOG_SHA256,
            source_adapter_sha256=src.digest(src.__file__),arithmetic_computed=False,static_inputs=pins,
            generated_inputs={k:"0"*64 for k in set(row["source_files_sha256"])&changed|add},added_inputs=sorted(add),allowed_outputs=[src.base.output_relative(row)])
        name=next(k for k in pins if k.endswith(".py"));r["generated_inputs"][name]=r["static_inputs"].pop(name)
        task=self.root/"task";write(task/"SOURCES.json",r)
        with self.assertRaisesRegex(ValueError,"static/generated partition"):src.verify_job(task)


class Transport(Fixture):
    def test_actual_supervisor_normalized_float_wall_and_nested_stopped_copy(self):
        t,r,s,c,_=self.transport_fixture()
        self.assertEqual("SYNTHETIC_ONLY\n",ev.transport(t,r,s,c,"python"))
        restored=self.root/"restored";shutil.copytree(t,restored)
        self.assertEqual("SYNTHETIC_ONLY\n",ev.transport(restored,r,s,c,"python"))

    def test_false_rc_missing_guard_wrong_hash_and_live_metadata_rejected(self):
        t,r,s,c,launch=self.transport_fixture()
        mutations=[lambda z:z["observed"].update(returncode=False),lambda z:z["observed"].update(proof_accepted=True),
            lambda z:z["observed"].update(sample_count=True),lambda z:z["observed"].update(mode="trusted_native"),
            lambda z:z["observed"].update(stderr_sha256="0"*64),lambda z:z["observed"]["guard_scope"].update(aggregate_kernel_memory_limit=True),
            lambda z:z["observed"]["checkpoints"][0].update(trusted_certificate=True),lambda z:z["observed"].update(checkpoints=[])]
        for mutate in mutations:
            bad=copy.deepcopy(c);mutate(bad);write(t/"executions/resource/supervisor-result.json",bad["observed"])
            with self.subTest(bad=bad),self.assertRaises((ValueError,KeyError)):ev.transport(t,r,s,bad,"python")
        write(t/"executions/resource/supervisor-result.json",c["observed"])
        for key,value in(("wall_seconds",True),("memory_bytes",1),("disk_bytes",256*src.MIB),("argv",["python","-c","pass"])):
            bad=copy.deepcopy(launch);bad[key]=value;write(t/"executions/resource/launch.json",bad)
            with self.subTest(key=key),self.assertRaises(ValueError):ev.transport(t,r,s,c,"python")

    def test_nonempty_actual_stderr_and_altered_captured_receipt_rejected(self):
        t,r,s,c,_=self.transport_fixture();p=t/"executions/resource/stderr.txt";p.write_bytes(b"warning")
        c["observed"]["stderr_sha256"]=src.digest(p);write(t/"executions/resource/supervisor-result.json",c["observed"])
        with self.assertRaisesRegex(ValueError,"Empty successful"):ev.transport(t,r,s,c,"python")
        p.write_bytes(b"");c["observed"]["stderr_sha256"]=src.digest(p);write(t/"executions/resource/supervisor-result.json",c["observed"])
        write(t/"capsule"/s["outputs"][0],{"status":"MUTATED"})
        with self.assertRaisesRegex(ValueError,"stopped output"):ev.transport(t,r,s,c,"python")

    def test_original_success_terminals_reject_incomplete_or_wrong_strip_count(self):
        good="EXACT_SUPPORTED_OWNCAPS6_9_WHOLE_COVER_PASS STRIPS 86 SECONDS 1.25\n"
        ev.action_terminal(self.root,{"label":"construct"},good)
        for bad in(good.replace("PASS","NOT_CLOSED"),good.replace("86","85"),good.replace("1.25","nan")):
            with self.subTest(bad=bad),self.assertRaises(ValueError):ev.action_terminal(self.root,{"label":"construct"},bad)


class StageCaches(Fixture):
    def test_preflight_rejects_unsafe_duplicate_link_oversized_missing_ledgers(self):
        required=["SOURCES.json","STAGE_OBSERVED.json","STAGE_COMPLETED.json"]
        for extra in("../outside","a\\b","SOURCES.json","sources.json","link","large",None):
            class Fake:
                def infolist(self):
                    rows=[zipfile.ZipInfo(x)for x in required]
                    if extra is None:return rows[:-1]
                    x=zipfile.ZipInfo("x");x.filename=extra;x.orig_filename=extra
                    if extra=="link":x.external_attr=(stat.S_IFLNK|0o777)<<16
                    if extra=="large":x.file_size=257*src.MIB
                    rows.append(x);return rows
            with self.subTest(extra=extra),self.assertRaises(ValueError):runner.cache_members(Fake())

    def cache_fixture(self):
        task=self.root/"task";write(task/"SOURCES.json",dict(job_id="owncaps6_9"))
        write(task/"STAGE_OBSERVED.json",dict(conditional_arithmetic_completed=False))
        write(task/"STAGE_COMPLETED.json",dict(conditional_arithmetic_completed=True))
        write(task/"receipt.json",dict(status="SYNTHETIC_ACCEPTED"))
        def validate(path):
            if src.read(Path(path)/"receipt.json")["status"]!="SYNTHETIC_ACCEPTED":raise ValueError("mutated receipt")
            return dict(job_id="owncaps6_9",stage_result_sha256=src.digest(Path(path)/"STAGE_COMPLETED.json"),summary={"fresh_caps_stage_sha256":"a"})
        return task,validate

    def test_save_restore_requires_full_validation_and_zip_sidecar(self):
        task,validate=self.cache_fixture();cache=self.root/"cache";log=self.root/"log";log.mkdir()
        with patch.object(ev,"validate_completed",side_effect=validate)as checked:
            export=runner.save_stage(task,cache)
            hit=runner.restore_stage(cache,self.root/"restored","owncaps6_9",root=log)
            self.assertIsNotNone(hit);self.assertGreaterEqual(checked.call_count,2)
            marker=Path(export["path"]).with_suffix(".zip.sha256");marker.write_text("0"*64,encoding="ascii")
            self.assertIsNone(runner.restore_stage(cache,self.root/"other","owncaps6_9",root=log))


class CompleteNativeLayers(Fixture):
    cache_fixture=StageCaches.cache_fixture
    def own_fixture(self):
        task=self.root/"own";capsule=task/"capsule";original=str(task.resolve());python="python";version="SYNTHETIC PYTHON"
        trap="work/native/trap.py";write(capsule/trap,b"raise AssertionError('MATH MUST NOT RUN')\n")
        manifest=dict(files_sha256={trap:src.digest(capsule/trap)})
        write(capsule/src.OWN/"MANIFEST.json",manifest)
        for name in(src.AUDIT+"readback.py",src.AUDIT+"REVIEW.txt","work/cutoff6_20261020/entry/resource7_9_v2/check_caps.py"):
            write(capsule/name,b"SYNTHETIC SOURCE ONLY\n")
        plan_path=src.epoch.OWN+"plan01/PLAN.json"
        plan=dict(schema="SUPPORTED_OWNCAPS6_9_PLAN_V1",n=[6,7,8,9],bands=[dict(strips=[{}]*86)])
        write(capsule/plan_path,plan)
        controls=dict(complex_power=16,quadratic_completion=140,moment_factorizations=7,malformed_domains=4,plan_negative_controls=17)
        result=dict(status="EXACT_SUPPORTED_OWNCAPS6_9_WHOLE_COVER_PASS",theorem="SYNTHETIC CONDITIONAL STATEMENT",n=[6,7,8,9],
            bands=[],targets={},rows=[{}]*344,attempts=[],controls=controls,per_band_per_n_upper={},
            plan_sha256=src.digest(capsule/plan_path),manifest_sha256=src.digest(capsule/src.OWN/"MANIFEST.json"),seconds=1.0)
        stdout={}
        base=dict(manifest["files_sha256"]);base[src.OWN+"MANIFEST.json"]=src.digest(capsule/src.OWN/"MANIFEST.json")
        for action,label in(("plan","plan01"),("construct","construct01"),("replay","replay01")):
            directory=capsule/src.epoch.OWN/label;inputs=dict(base)
            output="PLAN.json"if action=="plan"else"RESULT.json"
            if action!="plan":
                write(directory/output,result);inputs[plan_path]=src.digest(capsule/plan_path)
            prefix="HEURISTIC_ONLY"if action=="plan"else result["status"]
            stdout[action]=prefix+" STRIPS 86 SECONDS 1.0\n"
            write(directory/"stdout.txt",stdout[action].encode());write(directory/"stderr.txt",b"")
            command=[python,"-B","planner.py",ev.original_path(original,src.epoch.OWN+label+"/PLAN.json")]if action=="plan"else[
                python,"-B","protocol.py",action,ev.original_path(original,plan_path),ev.original_path(original,src.epoch.OWN+label+"/RESULT.json")]
            write(directory/"metadata.json",dict(returncode=0,changed_inputs=[],command=command,cwd=ev.original_path(original,src.OWN),
                input_sha256=inputs,python=version,stdout_sha256=src.digest(directory/"stdout.txt"),stderr_sha256=src.digest(directory/"stderr.txt"),
                elapsed_seconds=1.0,**{output+"_sha256":src.digest(directory/output)}))
        write(capsule/src.AUDIT/"OWN_REQUEST.json",ev.request_bytes(capsule))
        graph=dict(manifest["files_sha256"])
        for name in(src.OWN+"MANIFEST.json",plan_path,src.AUDIT+"OWN_REQUEST.json",src.AUDIT+"readback.py",src.AUDIT+"REVIEW.txt"):
            graph[name]=src.digest(capsule/name)
        for label in("construct01","replay01"):
            for name in("metadata.json","RESULT.json","stdout.txt","stderr.txt"):
                p=src.epoch.OWN+label+"/"+name;graph[p]=src.digest(capsule/p)
        readback=dict(status="PASS_INDEPENDENT_SUPPORTED_FOURIER6_9_READBACK",family="own",mathematical_status=result["theorem"],
            execution_status="fresh independent whole-coverage/normalization/capture readback with complete native construction/replay; no integral oracle calls here",
            n=[6,7,8,9],bands=[],targets={},strips=86,exact_rows=344,attempts=0,per_band_per_n_upper={},negative_controls=28,
            actual_support_acquired=False,cutoff6_proved=False,files_sha256=dict(graph))
        write(capsule/src.AUDIT/"OWN_RESULT.json",readback)
        stdout["readback"]=json.dumps({k:v for k,v in readback.items()if k!="files_sha256"})
        for name in(src.AUDIT+"OWN_RESULT.json",src.epoch.OWN+"construct01/RESULT.json",src.epoch.OWN+"replay01/RESULT.json",
            "work/cutoff6_20261020/entry/resource7_9_v2/check_caps.py"):
            graph[name]=src.digest(capsule/name)
        control_names=["missing row","duplicate row","reordered row","wrong actual n","boolean n",
            "wrong normalization","wrong radius","wrong seam","too-small cap B07","too-small cap B08",
            "too-small cap B09","too-small cap BN7","too-small cap BN8","too-small cap BN9",
            "too-small cap B27","too-small cap B28","too-small cap B29"]
        caps=dict(status="PASS_EXACT_TIGHTER_LITERAL7_9_OWNCAPS",negative_controls=control_names,files_sha256=graph,accepted_upper={})
        write(capsule/src.CAPS,caps);write(task/"provenance/ORIGINAL_CAPS.json",dict(negative_controls=control_names))
        stdout["caps"]=caps["status"]+" 17\n"
        request=dict(original_task_root=original);report=dict(python_executable=python,python_version=version)
        return task,request,stdout,report

    def test_full_inner_capture_and_readback_metadata_accepts_relocation(self):
        task,r,out,report=self.own_fixture()
        with patch.object(src.epoch,"cap_binding"):
            summary=ev.own_summary(task,r,out,report)
            restored=self.root/"restored";shutil.copytree(task,restored)
            self.assertEqual(summary,ev.own_summary(restored,r,out,report))
        self.assertEqual(344,summary["whole_rows"])
        self.assertEqual(28,summary["readback_controls"])

    def test_failed_readback_status_or_omitted_capture_graph_never_accepted(self):
        task,r,out,report=self.own_fixture();p=task/"capsule"/src.AUDIT/"OWN_RESULT.json";old=src.read(p)
        for bad in(copy.deepcopy(old),copy.deepcopy(old),copy.deepcopy(old)):
            index=getattr(self,"case_index",0);self.case_index=index+1
            if index==0:bad["status"]="DELIBERATE_FAILED_RECEIPT"
            elif index==1:bad["negative_controls"]=True
            else:bad["files_sha256"].pop(next(iter(bad["files_sha256"])))
            write(p,bad);changed=dict(out);changed["readback"]=json.dumps({k:v for k,v in bad.items()if k!="files_sha256"})
            with patch.object(src.epoch,"cap_binding"),self.assertRaisesRegex(ValueError,"whole-result readback"):
                ev.own_summary(task,r,changed,report)

    def test_false_inner_rc_or_wrong_contemporaneous_input_map_rejected(self):
        task,r,out,report=self.own_fixture();p=task/"capsule"/src.epoch.OWN/"plan01/metadata.json";old=src.read(p)
        for mutate in(lambda z:z.update(returncode=False),lambda z:z.update(input_sha256={}),lambda z:z.update(command=["python","-c","pass"])):
            bad=copy.deepcopy(old);mutate(bad);write(p,bad)
            with patch.object(src.epoch,"cap_binding"),self.assertRaisesRegex(ValueError,"inner invocation"):
                ev.own_summary(task,r,out,report)

    def test_rehashed_mutated_receipt_and_wrong_upstream_lineage_not_reused(self):
        task,validate=self.cache_fixture();cache=self.root/"cache";log=self.root/"log";log.mkdir()
        with patch.object(ev,"validate_completed",side_effect=validate):
            export=runner.save_stage(task,cache)
            self.assertIsNone(runner.restore_stage(cache,self.root/"restored","owncaps6_9",root=log,bindings={"fresh_caps_stage_sha256":"different"}))
            path=Path(export["path"])
            with zipfile.ZipFile(path)as z:contents={r.filename:z.read(r)for r in z.infolist()}
            contents["receipt.json"]=src.dump(dict(status="MUTATED"))
            with zipfile.ZipFile(path,"w")as z:
                for name,raw in contents.items():z.writestr(name,raw)
            path.with_suffix(".zip.sha256").write_text(src.digest(path)+"  "+path.name+"\n",encoding="ascii")
            self.assertIsNone(runner.restore_stage(cache,self.root/"other","owncaps6_9",root=log))


class Orchestration(Fixture):
    def test_observed_rejects_bad_python_context_before_native_action_readback(self):
        request=dict(job_id="synthetic",original_task_root="/content/original")
        report=dict(schema=ev.OBSERVED,scope=ev.SCOPE,job_id="synthetic",implementation={},original_task_root=request["original_task_root"],
            conditional_arithmetic_completed=False,python_executable=True,python_version="synthetic",actions=[],**{f:False for f in ev.FLAGS})
        with patch.object(src,"verify_job",return_value=request),patch.object(ev,"implementation",return_value={}):
            with self.assertRaisesRegex(ValueError,"Python execution context"):ev.validate_run(self.root,report)

    def test_observed_false_written_before_validation_completed_only_after(self):
        task=self.root/"task";task.mkdir();root=self.root/"log";root.mkdir()
        request=dict(job_id="synthetic",original_task_root=str(task))
        def validate(t,report):
            self.assertFalse(src.read(t/"STAGE_OBSERVED.json")["conditional_arithmetic_completed"])
            self.assertFalse((t/"STAGE_COMPLETED.json").exists())
            return dict(status="SYNTHETIC_ONLY")
        with patch.object(ev,"implementation",return_value={}),patch.object(ev,"validate_run",side_effect=validate),patch.object(ev,"validate_completed",return_value=dict(job_id="synthetic")):
            runner.complete(task,request,[],root=root)
        self.assertTrue(src.read(task/"STAGE_COMPLETED.json")["conditional_arithmetic_completed"])
        self.assertTrue(all(src.read(task/"STAGE_COMPLETED.json")[f]is False for f in ev.FLAGS))

    def test_failed_validation_never_writes_completed(self):
        task=self.root/"task";task.mkdir();root=self.root/"log";root.mkdir()
        request=dict(job_id="synthetic",original_task_root=str(task))
        with patch.object(ev,"implementation",return_value={}),patch.object(ev,"validate_run",side_effect=ValueError("failed native")):
            with self.assertRaisesRegex(ValueError,"failed native"):runner.complete(task,request,[],root=root)
        self.assertFalse((task/"STAGE_COMPLETED.json").exists())

    def test_batch_failure_always_exports_and_retains_false_flags(self):
        class Backups:
            def __init__(self,*a):pass
            def start(self):pass
            def close(self):pass
        with patch.object(runner.parents,"LogBackups",Backups),patch.object(src,"obtain_assets",side_effect=ValueError("synthetic missing archive")):
            result=runner.run_colab(durable_root=self.root/"durable",work_root=self.root/"work",archives=self.root/"archives")
        self.assertTrue(Path(result["bundle"]).is_file())
        self.assertTrue(Path(result["bundle"]+".sha256").is_file())
        self.assertFalse(result["status"]["conditional_arithmetic_completed"])
        self.assertTrue(all(result["status"][f]is False for f in ev.FLAGS))


class ResourceEpochReadback(Fixture):
    def resource_fixture(self):
        task=self.root/"resource";capsule=task/"capsule";case="n7_B0"
        parent_path="work/original/INITIAL_CHECKED.json"
        parent=write(task/"inputs/initial/receipt.json",dict(files_sha256={}))
        caps=dict(files_sha256={})
        write(task/"inputs/owncaps/capsule"/src.CAPS,caps);write(capsule/src.CAPS,caps)
        write(capsule/parent_path,parent.read_bytes());write(task/"provenance/ORIGINAL_CAPS.json",b"TEMPLATE ONLY")
        files={src.RESOURCE+"FRESH_REPLAY.py":b"raise AssertionError('NEVER IMPORT MATH')\n",
            src.RESOURCE+case+"/FRESH_PREPARED.json":src.dump(dict(files_sha256={})),
            src.RESOURCE+case+"/FRESH_SOURCE_RESULT.json":src.dump(dict(rows=["SYNTHETIC"]*100))}
        for name,raw in files.items():write(capsule/name,raw)
        for name in("replay.py","prepare.py","PROOF.txt"):write(capsule/src.RESOURCE/name,b"SYNTHETIC ORIGINAL SOURCE\n")
        derived=dict(replay_bytes=files[src.RESOURCE+"FRESH_REPLAY.py"],fresh_prepared_bytes=files[src.RESOURCE+case+"/FRESH_PREPARED.json"],
            fresh_source_result_bytes=files[src.RESOURCE+case+"/FRESH_SOURCE_RESULT.json"],report=dict(scope="SYNTHETIC METADATA ONLY"))
        write(task/"DERIVATION.json",dict(report=derived["report"]))
        old=dict(status="PASS_FRESH_CONDITIONAL_FULL_RESOURCE7_9_V2_ACQUISITION",n=7,band="B0",panels=100,excluded=[],retained=list(range(100)),
            negative_controls=["original control"],initial_receipt=parent_path,initial_receipt_sha256="old",source_result_sha256="old",files_sha256={},seconds=1.0,
            unchanged_numeric_field="SYNTHETIC ORIGINAL ANSWER")
        row=dict(kind="resource",job_id="n7.resource.B0",directory=src.RESOURCE.rstrip("/"),output=case+"/REPLAY_CHECKED.json",reference=dict(native_answer=old))
        graph={parent_path:src.digest(parent),src.CAPS:src.digest(capsule/src.CAPS)}
        for name in(src.RESOURCE+"replay.py",src.RESOURCE+"prepare.py",src.RESOURCE+"PROOF.txt",src.RESOURCE+case+"/FRESH_PREPARED.json"):
            graph[name]=src.digest(capsule/name)
        receipt=copy.deepcopy(old);receipt.update(initial_receipt_sha256=src.digest(parent),
            source_result_sha256=src.digest(capsule/src.RESOURCE/case/"FRESH_SOURCE_RESULT.json"),files_sha256=graph,seconds=2.0)
        output=write(capsule/src.base.output_relative(row),receipt)
        return task,row,derived,parent_path,parent,caps,output

    def checks(self,task,row,derived,parent_path,parent,caps,output):
        return patch.multiple(ev,validate_completed=unittest.mock.Mock(return_value=dict(stage_result_sha256="own-fresh"))),\
            patch.object(ev.parent_ev,"validate_completed",return_value=dict(stage_result_sha256="initial-fresh")),\
            patch.object(src.base,"job",return_value=row),\
            patch.object(src,"derived_resource",return_value=(derived,parent_path,parent,caps))

    def test_entire_original_resource_payload_and_fresh_bindings_checked(self):
        fixture=self.resource_fixture();task,row,*_=fixture
        a,b,c,d=self.checks(*fixture)
        with a,b,c,d:
            result=ev.resource_summary(task,dict(job_id=row["job_id"]),"PASS_FRESH_CONDITIONAL_FULL_RESOURCE7_9_V2_ACQUISITION 7 B0\n")
        self.assertEqual(100,result["panels"])
        self.assertEqual("initial-fresh",result["fresh_initial_stage_sha256"])
        self.assertEqual("own-fresh",result["fresh_caps_stage_sha256"])

    def test_mutated_numeric_row_controls_port_or_parent_bytes_rejected(self):
        fixture=self.resource_fixture();task,row,derived,parent_path,parent,caps,output=fixture
        original=src.read(output)
        for name,value in(("unchanged_numeric_field","CHANGED"),("negative_controls",[]),("panels",True)):
            altered=copy.deepcopy(original);altered[name]=value;write(output,altered)
            a,b,c,d=self.checks(*fixture)
            with a,b,c,d,self.assertRaisesRegex(ValueError,"Every original full100-panel"):
                ev.resource_summary(task,dict(job_id=row["job_id"]),"unused")
        write(output,original)
        fresh_source=task/"capsule"/src.RESOURCE/"n7_B0/FRESH_SOURCE_RESULT.json";fresh_source.write_bytes(b"CHANGED")
        a,b,c,d=self.checks(*fixture)
        with a,b,c,d,self.assertRaisesRegex(ValueError,"Exact byte-only resource epoch"):
            ev.resource_summary(task,dict(job_id=row["job_id"]),"unused")
        fresh_source.write_bytes(derived["fresh_source_result_bytes"])
        (task/"capsule"/parent_path).write_bytes(b"UNATTESTED PARENT")
        a,b,c,d=self.checks(*fixture)
        with a,b,c,d,self.assertRaisesRegex(ValueError,"Actual fresh INITIAL/CAPS"):
            ev.resource_summary(task,dict(job_id=row["job_id"]),"unused")


class BatchResume(Fixture):
    def test_successful_final_readback_binds_unchanged_final_session_bytes(self):
        class Backups:
            def __init__(self,*a):pass
            def start(self):pass
            def close(self):pass
        def validated(root):
            packet=src.read(root/"SESSION_RESULT.json")
            self.assertTrue(packet["conditional_arithmetic_completed"])
            self.assertTrue(all(packet[f]is False for f in ev.FLAGS))
            return dict(scope="SYNTHETIC_INFRASTRUCTURE_ONLY",session_result_sha256=src.digest(root/"SESSION_RESULT.json"))
        with patch.object(runner.parents,"LogBackups",Backups),patch.object(src,"obtain_assets",return_value={}),\
             patch.object(src,"prepare_cache",return_value=self.root/"cache"),patch.object(runner,"run_stages"),\
             patch.object(ev,"validate_batch",side_effect=validated)as gate:
            result=runner.run_colab(durable_root=self.root/"durable",work_root=self.root/"work",archives=self.root/"archives")
        root=Path(result["work"]);self.assertEqual(1,gate.call_count)
        self.assertEqual(src.digest(root/"SESSION_RESULT.json"),src.read(root/"BATCH_VALIDATED.json")["session_result_sha256"])

    def test_final_join_rejection_resets_false_before_failure_export(self):
        class Backups:
            def __init__(self,*a):pass
            def start(self):pass
            def close(self):pass
        with patch.object(runner.parents,"LogBackups",Backups),patch.object(src,"obtain_assets",return_value={}),\
             patch.object(src,"prepare_cache",return_value=self.root/"cache"),patch.object(runner,"run_stages"),\
             patch.object(ev,"validate_batch",side_effect=ValueError("synthetic cross-join failure")):
            result=runner.run_colab(durable_root=self.root/"durable",work_root=self.root/"work",archives=self.root/"archives")
        self.assertFalse(result["status"]["conditional_arithmetic_completed"])
        self.assertTrue(Path(result["bundle"]).is_file())
        self.assertFalse((Path(result["work"])/"BATCH_VALIDATED.json").exists())
        self.assertEqual(result["status"],src.read(Path(result["work"])/"SESSION_RESULT.json"))


    def test_completed_nineteen_stage_resume_runs_zero_native_actions(self):
        root=self.root/"run";root.mkdir();status=dict(jobs=[])
        initial_rows=[dict(job_id=f"n{n}.initial.{b}")for n in(7,8,9)for b in("B0","BN","B2")]
        resource_rows=[dict(job_id=r["job_id"].replace("initial","resource"))for r in initial_rows]
        def parent_hit(cache,destination,row,**unused):
            task=Path(destination)/row["job_id"];task.mkdir(parents=True)
            return task,dict(job_id=row["job_id"],stage_result_sha256=row["job_id"]),dict(sha256="synthetic")
        def hit(cache,destination,job_id,**kwargs):
            task=Path(destination)/job_id;task.mkdir(parents=True)
            return task,dict(job_id=job_id,stage_result_sha256=job_id,summary=kwargs.get("bindings",{})),dict(sha256="synthetic")
        with patch.object(runner.ps,"job",side_effect=lambda key:next(r for r in initial_rows if r["job_id"]==key)),patch.object(src,"resource_rows",return_value=resource_rows),\
             patch.object(runner.parents,"restore_stage",side_effect=parent_hit),patch.object(runner,"restore_stage",side_effect=hit),\
             patch.object(runner,"execute_prepared",side_effect=AssertionError("NO NUMERICAL REPLAY")),\
             patch.object(runner.parents,"execute",side_effect=AssertionError("NO INITIAL REPLAY")):
            runner.run_stages(root,self.root/"durable",self.root/"cache",status)
        self.assertEqual(19,len(status["jobs"]))
        self.assertEqual([r["job_id"]for r in initial_rows],[r["job_id"]for r in status["jobs"][:9]])
        self.assertTrue(all(r["reused_completed_stage"]for r in status["jobs"]))

    def test_failure_after_four_cached_initials_retains_them_and_exports(self):
        class Backups:
            def __init__(self,*a):pass
            def start(self):pass
            def close(self):pass
        rows=[dict(job_id=f"n{n}.initial.{b}")for n in(7,8,9)for b in("B0","BN","B2")]
        calls=[]
        def hit(cache,destination,row,**unused):
            calls.append(row["job_id"])
            if len(calls)>4:return None
            task=Path(destination)/row["job_id"];task.mkdir(parents=True)
            return task,dict(job_id=row["job_id"],stage_result_sha256="synthetic"),dict(sha256="synthetic")
        with patch.object(runner.parents,"LogBackups",Backups),patch.object(src,"obtain_assets",return_value={}),\
             patch.object(src,"prepare_cache",return_value=self.root/"cache"),patch.object(runner.ps,"job",side_effect=lambda key:next(r for r in rows if r["job_id"]==key)),\
             patch.object(runner.parents,"restore_stage",side_effect=hit),\
             patch.object(runner.parents,"execute",side_effect=ValueError("synthetic fifth-stage failure")):
            result=runner.run_colab(durable_root=self.root/"durable",work_root=self.root/"work",archives=self.root/"archives")
        self.assertEqual(4,len(result["status"]["jobs"]))
        self.assertTrue(Path(result["bundle"]).is_file())
        self.assertFalse(result["status"]["conditional_arithmetic_completed"])

    def test_exported_batch_join_requires_same_fresh_parent_and_all_nineteen(self):
        initials=[f"n{n}.initial.{b}"for n in(7,8,9)for b in("B0","BN","B2")]
        resources=[x.replace("initial","resource")for x in initials]
        results={x:dict(job_id=x,stage_result_sha256=x,summary={})for x in initials+["owncaps6_9"]+resources}
        for x in resources:results[x]["summary"]=dict(fresh_initial_stage_sha256=x.replace("resource","initial"),fresh_caps_stage_sha256="owncaps6_9")
        root=self.root/"batch";root.mkdir()
        packet=dict(schema="CONDITIONAL_FINITE69_CAPS_BATCH_V1",state="complete_selected_conditional_caps_resource_arithmetic_basic",
            catalog_sha256=src.CATALOG_SHA256,expected_stages=19,expected_native_actions=23,conditional_arithmetic_completed=True,
            jobs=[dict(job_id=x,task_relative="jobs/"+x,validated=results[x])for x in initials+["owncaps6_9"]+resources],**{f:False for f in ev.FLAGS})
        write(root/"SESSION_RESULT.json",packet)
        def validate(path):return results[Path(path).name]
        with patch.object(src,"catalog",return_value=dict(initial_job_ids=initials,resource_job_ids=resources)),\
             patch.object(ev.parent_ev,"validate_completed",side_effect=validate),patch.object(ev,"validate_completed",side_effect=validate):
            self.assertEqual(900,ev.validate_batch(root)["resource_panels"])
            results[resources[0]]["summary"]["fresh_initial_stage_sha256"]="another lineage"
            write(root/"SESSION_RESULT.json",packet)
            with self.assertRaisesRegex(ValueError,"Same actual fresh upstream"):ev.validate_batch(root)
            packet["jobs"].pop();write(root/"SESSION_RESULT.json",packet)
            with self.assertRaisesRegex(ValueError,"Every fixed complete"):ev.validate_batch(root)


if __name__=="__main__":unittest.main()
