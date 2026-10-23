"""Infrastructure/receipt fixtures only; no numerical capsule is executed."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from be_replay import strong24_branches as s
from be_replay import aux24_sources, colab_batch, linux_supervisor


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2)+"\n", encoding="utf-8")
    return path


class BranchFixtures(unittest.TestCase):
    def setUp(self):
        base = Path(__file__).resolve().parents[1]/"work"/"test-fixtures"
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="strong24-", dir=base)
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def count_fixture(self, root=None):
        root = root or self.root
        stage = s._stage("count-p37-accept", s.X10+"count_b0", "accept_strict.py", ["37"],
                         proof="candidate_37.json", receipt="accepted_strict_37.json", kind="count", index=37)
        d = root/stage["folder"]
        d.mkdir(parents=True)
        (d/"accept_strict.py").write_text("# synthetic fixture, never executed\n", encoding="utf-8")
        write(d/"contract.json", {"n":24,"indices":[37]})
        write(d/stage["proof"], {"leaves":[{"k":0},{"k":1}],"target_lower":"1/2"})
        record = dict(status="PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES", n=24,index=37,K="3/10",
                      candidate_sha256=s.sha(d/stage["proof"]),contract_sha256=s.sha(d/"contract.json"),
                      all_closed_leaves=2,negative_controls=24,maximum_score="1/3",target_lower="1/2",
                      source_sha256={n:s.sha(d/n) for n in ("accept_strict.py","contract.json")})
        write(d/stage["receipt"],record)
        config=dict(s.BRANCHES["b0"],counts=[37],leaves=2,contract=record["contract_sha256"])
        return stage,d,record,config

    def observed(self, directory):
        directory.mkdir(parents=True)
        stdout=directory/"stdout.txt"
        stderr=directory/"stderr.txt"
        stdout.write_text("ACCEPTED fixture\n",encoding="utf-8")
        stderr.write_bytes(b"")
        return dict(status="completed",returncode=0,mode="untrusted_search",sample_count=2,
                    stdout_path=str(stdout),stderr_path=str(stderr),stdout_sha256=s.sha(stdout),stderr_sha256=s.sha(stderr),
                    guard_scope=dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",proof_acceptance=False))

    def test_complete_six_branch_selection_counts(self):
        self.assertEqual(sum(len(s.count_jobs(b)) for b in s.BRANCHES),53)
        self.assertEqual(sum(s.BRANCHES[b]["leaves"] for b in s.BRANCHES),57453)
        self.assertEqual(set(s.SELECTION_SHA),set(s.BRANCHES))
        for b in s.BRANCHES:
            names=[r["name"] for r in s.stages(b)]
            self.assertEqual(len(names),len(set(names)))
            self.assertEqual([r["index"] for r in s.stages(b) if r["kind"]=="count"],s.BRANCHES[b]["counts"])
        self.assertIn("selected_v2",s.locations("b3")["composition"])

    def test_b2_selected_patch_replaces_four_old_forests(self):
        jobs=s.count_jobs("b2")
        self.assertEqual([i for p,i in jobs if p.endswith("count_b2")],[28,29,30,31,32])
        self.assertEqual([i for p,i in jobs if "meanfloor_patch" in p],[33,34,35,36])
        self.assertFalse(any(r["kind"]=="count_join" and r["folder"].endswith("count_b2") for r in s.stages("b2")))

    def test_every_local_survivor_has_unchanged_accept_action(self):
        for b in ("b3","b4","b5"):
            local=[r for r in s.stages(b) if r["kind"]=="local"]
            self.assertEqual([r["index"] for r in local],s.BRANCHES[b]["local"])
            self.assertTrue(all(r["args"]==["accept",str(r["index"])] for r in local))
        self.assertTrue(all(any(r["kind"]=="equivalence" for r in s.stages(b)) for b in ("b0","b1","b2")))

    def test_count_receipt_checks_real_candidate_source_target_and_types(self):
        stage,d,original,config=self.count_fixture()
        with patch.dict(s.BRANCHES,{"b0":config}):
            self.assertEqual(s.validate_artifact(self.root,"b0",stage)["leaves"],2)
            for field,value in [("index",True),("negative_controls",23),("maximum_score","1/2"),("all_closed_leaves",1)]:
                bad=dict(original,**{field:value})
                write(d/stage["receipt"],bad)
                with self.subTest(field=field), self.assertRaises(ValueError):
                    s.validate_artifact(self.root,"b0",stage)
            write(d/stage["receipt"],original)
            (d/stage["proof"]).write_text("{}",encoding="utf-8")
            with self.assertRaises(ValueError):s.validate_artifact(self.root,"b0",stage)

    def test_changed_numeric_source_rejects(self):
        stage,d,record,config=self.count_fixture()
        (d/"accept_strict.py").write_text("# changed\n",encoding="utf-8")
        with patch.dict(s.BRANCHES,{"b0":config}),self.assertRaises(ValueError):
            s.validate_artifact(self.root,"b0",stage)

    def test_captures_bound_even_when_stderr_is_empty(self):
        observed=self.observed(self.root/"captures")
        s.validate_execution(observed,["python"],self.root)
        (self.root/"captures"/"stdout.txt").write_text("changed",encoding="utf-8")
        with self.assertRaises(ValueError):s.validate_execution(observed,["python"],self.root)

    def test_nonempty_stderr_and_boolean_exit_reject(self):
        observed=self.observed(self.root/"captures")
        stderr=Path(observed["stderr_path"])
        stderr.write_text("warning",encoding="utf-8")
        observed["stderr_sha256"]=s.sha(stderr)
        with self.assertRaises(ValueError):s.validate_execution(observed,["python"],self.root)
        stderr.write_bytes(b"")
        observed["stderr_sha256"]=s.sha(stderr)
        observed["returncode"]=False
        with self.assertRaises(ValueError):s.validate_execution(observed,["python"],self.root)

    def test_local_candidate_metadata_rebind_preserves_numerical_fields(self):
        root=self.root/"sources"
        folder=root/"continuation_20261011/stronger24/b3_resource_exact_v1"
        receipt=write(folder/"RESOURCE_B3_GLOBAL_ACCEPTED.json",{"seconds":12,"proof_sha256":"x"})
        name="b3_resource_exact_v1/RESOURCE_B3_GLOBAL_ACCEPTED.json"
        candidate=write(self.root/"candidate.json",dict(parent_binding_sha256={name:"0"*64},rows=[{"all_numeric_cells":["1/3","5/7"]}]))
        old=s.read(candidate)
        report=s.rebind_local_candidate(candidate,root,"b3",ledger=self.root/"rebind.json")
        self.assertFalse(report["numeric_fields_changed"])
        self.assertEqual(s.read(candidate)["rows"],old["rows"])
        self.assertEqual(s.read(candidate)["parent_binding_sha256"][name],s.sha(receipt))

    def test_other_changed_parent_hash_cannot_be_rebound(self):
        root=self.root/"sources"
        write(root/"continuation_20261011/stronger24/b3_initial_exact_v1/proof.json",{})
        candidate=write(self.root/"candidate.json",dict(parent_binding_sha256={"b3_initial_exact_v1/proof.json":"0"*64},rows=[]))
        with self.assertRaises(ValueError):s.rebind_local_candidate(candidate,root,"b3",ledger=self.root/"rebind.json")

    def test_warning_filter_is_narrow_and_prior_environment_restored(self):
        with patch.dict(s.os.environ,{"PYTHONWARNINGS":"default"}):
            with s._warnings() as policy:
                self.assertEqual(policy,"ignore:invalid escape sequence:SyntaxWarning")
                self.assertEqual(s.os.environ["PYTHONWARNINGS"],"default,"+policy)
            self.assertEqual(s.os.environ["PYTHONWARNINGS"],"default")

    def completed_fixture(self):
        task=self.root/"original-task"
        task.mkdir()
        root=task/"execution-epoch/cutoff25_20261011"
        stage,d,record,config=self.count_fixture(root)
        capture=task/"captures"/stage["name"]
        observed=self.observed(capture)
        command=["/original/python","-B","-u",str(d/stage["script"]),"37"]
        write(capture/"launch.json",dict(argv=command,cwd=str(d),mode="untrusted_search"))
        write(capture/"supervisor-result.json",observed)
        manifest=dict(files={s.PREFIX+f.relative_to(root).as_posix():dict(sha256=s.sha(f)) for f in root.rglob("*")if f.is_file()})
        report=dict(schema="OBSERVED_STRONG24_BRANCH_STAGE_V1",branch="b0",stage=stage,command=command,observed=observed,
                    original_task_root=str(task),supervisor_sha256=s.sha(linux_supervisor.__file__),
                    launch_sha256=s.sha(capture/"launch.json"),supervisor_result_sha256=s.sha(capture/"supervisor-result.json"),
                    preceding_stage_sha256={},native_arithmetic_accepted=False,arithmetic_computed=True,
                    artifact_sha256={f.relative_to(root).as_posix():s.sha(f)for f in d.iterdir()},
                    result=None)
        with patch.dict(s.BRANCHES,{"b0":config}):report["result"]=s.validate_artifact(root,"b0",stage)
        report_path=write(task/(stage["name"]+"-COMPLETED.json"),report)
        write(task/"BRANCH.json",dict(driver_sha256=s.sha(s.__file__),manifest_sha256=s.SELECTION_SHA["b0"]))
        write(task/"RESULT.json",dict(schema="CONDITIONAL_STRONG24_BRANCH_ARITHMETIC_V1",branch="b0",n=24,K="3/10",
              contact_allowance="15/46",effective_contact_allowance="15/46",predecessor_statement_sha256=s.PREDECESSOR_SHA,driver_sha256=s.sha(s.__file__),
              state="complete_conditional_arithmetic_basic",arithmetic_computed=True,native_arithmetic_accepted=False,
              all_index_conclusion_verified=False,branch_theorem_acquired=False,stronger24_acquisition_verified=False,
              source_manifest_sha256=s.SELECTION_SHA["b0"],original_task_root=str(task),
              stage_receipts={stage["name"]:s.sha(report_path)},completed_stage_count=1,
              interface_evidence_sha256={},rho_interval=config["rho"],probability_panels=100,
              count_indices=[37],count_forests=1,count_leaves=2,resource_to_count_numeric_interfaces_computed=True))
        return task,stage,config,manifest

    def test_restored_task_revalidation_keeps_original_receipt_bytes(self):
        task,stage,config,manifest=self.completed_fixture()
        restored=self.root/"restored-task"
        shutil.copytree(task,restored)
        before=(restored/(stage["name"]+"-COMPLETED.json")).read_bytes()
        with patch.dict(s.BRANCHES,{"b0":config}),patch.object(s,"stages",return_value=[stage]),patch.object(aux24_sources,"verify_prepared",return_value=manifest):
            result=s.validate_completed(restored,original_task_root=task)
            self.assertEqual(result["count_leaves"],2)
            self.assertFalse(result["native_arithmetic_accepted"])
        self.assertEqual((restored/(stage["name"]+"-COMPLETED.json")).read_bytes(),before)

    def test_restored_capture_tamper_and_missing_stage_reject(self):
        task,stage,config,manifest=self.completed_fixture()
        with patch.dict(s.BRANCHES,{"b0":config}),patch.object(s,"stages",return_value=[stage]),patch.object(aux24_sources,"verify_prepared",return_value=manifest):
            stdout=task/"captures"/stage["name"]/"stdout.txt"
            stdout.write_text("foreign capture",encoding="utf-8")
            with self.assertRaises(ValueError):s.validate_completed(task)
            stdout.write_text("ACCEPTED fixture\n",encoding="utf-8")
            summary=s.read(task/"RESULT.json")
            summary["stage_receipts"]={}
            write(task/"RESULT.json",summary)
            with self.assertRaises(ValueError):s.validate_completed(task)

    def test_failed_preparation_still_has_final_bundle(self):
        with patch.object(s,"prepare",side_effect=ValueError("fixture missing source")),patch("be_replay.environment.snapshot",return_value={}),patch.object(colab_batch.Backups,"start"),patch.object(colab_batch.Backups,"close"):
            result=s.run_colab("b0",durable_root=self.root/"durable",work_root=self.root/"work")
        self.assertEqual(result["status"]["state"],"partial_not_accepted")
        self.assertTrue(Path(result["bundle"]).is_file())
        self.assertIn("stronger24-b0",result["bundle"])
        self.assertFalse(result["status"]["arithmetic_computed"])

    def test_actual_interface_packet_binds_mixed_proof_and_contract(self):
        branch="b3"
        p=s.locations(branch)
        mixed=write(self.root/p["local"]/"B3_FINITE_FEEDBACK_PROOF.json",{"rows":[]})
        contract=write(self.root/p["count"]/"contract.json",{"n":24,"K":"3/10"})
        packet=dict(status="PASS_EXACT_B3_ALL_COUNT_RESOURCE_INTERFACES",mixed_proof_sha256=s.sha(mixed),
                    contract_sha256=s.sha(contract),rows=[dict(index=i,scalar_and_moment_guards=True,
                    quadratic_interfaces=[{"reserve":"1/5"}])for i in s.BRANCHES[branch]["counts"]])
        stdout=write(self.root/"stdout.json",packet)
        config=dict(s.BRANCHES[branch],contract=s.sha(contract))
        with patch.dict(s.BRANCHES,{branch:config}):
            self.assertEqual(len(s._interface_packet(self.root,branch,{"stdout_path":str(stdout)})["rows"]),8)
            for bad in [dict(packet,mixed_proof_sha256="0"*64),dict(packet,rows=packet["rows"][:-1])]:
                write(stdout,bad)
                with self.assertRaises(ValueError):s._interface_packet(self.root,branch,{"stdout_path":str(stdout)})
            bad=copy.deepcopy(packet)
            bad["rows"][0]["quadratic_interfaces"]=[]
            write(stdout,bad)
            with self.assertRaises(ValueError):s._interface_packet(self.root,branch,{"stdout_path":str(stdout)})

    def test_summary_cannot_promote_scope_or_change_leaf_census(self):
        task,stage,config,manifest=self.completed_fixture()
        original=s.read(task/"RESULT.json")
        with patch.dict(s.BRANCHES,{"b0":config}),patch.object(s,"stages",return_value=[stage]),patch.object(aux24_sources,"verify_prepared",return_value=manifest):
            for field,value in [("native_arithmetic_accepted",True),("count_leaves",999),("contact_allowance","0")]:
                write(task/"RESULT.json",dict(original,**{field:value}))
                with self.subTest(field=field),self.assertRaises(ValueError):s.validate_completed(task)

    def test_b4_b5_effective_allowance_is_distinct_from_predecessor_allowance(self):
        for branch in ("b4","b5"):
            root=self.root/branch
            stage=s.stages(branch)[0]
            directory=root/stage["folder"]
            directory.mkdir(parents=True)
            script=directory/stage["script"]
            script.write_text("# synthetic initial schema fixture\n",encoding="utf-8")
            profile=dict(n=24,barrier="3/10")
            sources={script.name:s.sha(script)}
            panels=[dict(pl=str(s.Fraction(i,100)),pu=str(s.Fraction(i+1,100)),rho_lo=s.BRANCHES[branch]["rho"][0],
                         rho_branch_upper=s.BRANCHES[branch]["rho"][1])for i in range(100)]
            cover=dict(total=18432,active=0,excluded=18432)
            proof=dict(profile=profile,stages=[dict(cover=cover)for _ in range(8)],export=dict(cover,panels=panels),
                       predecessor_sha256=s.PREDECESSOR_SHA,source_sha256=sources,
                       support=dict(q=s.EFFECTIVE_Q[branch],global_predecessor_allowance="15/46",same_law_allowance=s.EFFECTIVE_Q[branch]))
            write(directory/stage["proof"],proof)
            receipt=dict(status="PASS_FRESH_EXACT_FIXTURE",signed_rectangles=165888,probability_panels=100,
                         negative_controls=[str(i)for i in range(9)],profile=profile,source_sha256=sources,
                         checker_sha256=s.sha(script),proof_sha256=s.sha(directory/stage["proof"]))
            write(directory/stage["receipt"],receipt)
            s.validate_artifact(root,branch,stage)
            proof["support"]["q"]="15/46"
            write(directory/stage["proof"],proof)
            receipt["proof_sha256"]=s.sha(directory/stage["proof"])
            write(directory/stage["receipt"],receipt)
            with self.assertRaises(ValueError):s.validate_artifact(root,branch,stage)


if __name__ == "__main__":
    unittest.main()
