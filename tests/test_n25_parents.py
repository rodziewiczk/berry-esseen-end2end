"""Bounded metadata/protocol fixtures only; no frozen mathematical evaluator runs."""
from contextlib import nullcontext
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import count_task as common
from be_replay import n25_parents as parents
from be_replay import small_indices


class ParentTaskTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.archive = self.root / "fixture.zip"
        self.specs = deepcopy(parents.BRANCHES)
        self.payloads = {}
        for branch in self.specs:
            for kind, count in (("initial", 30), ("resource", 32)):
                capsule = parents.names(branch)[kind + "_dir"]
                script = parents.names(branch)[kind + "_script"]
                files = {script: b"raise AssertionError('THIS FIXTURE MUST NEVER EXECUTE')\n"}
                files.update({f"fixture-source-{i}.txt": f"sealed fixture {branch} {kind} {i}\n".encode()
                              for i in range(count-1)})
                manifest = {name: hashlib.sha256(raw).hexdigest() for name, raw in files.items()}
                raw = (json.dumps(manifest, indent=2) + "\n").encode()
                self.specs[branch][kind + "_manifest"] = hashlib.sha256(raw).hexdigest()
                self.payloads[capsule] = dict(files, **{"FROZEN_SOURCES.json": raw})
        with zipfile.ZipFile(self.archive, "w") as archive:
            for capsule, files in self.payloads.items():
                prefix = "cutoff25_20261011/new_root/" + capsule + "/"
                for name, raw in files.items():
                    archive.writestr(prefix + name, raw)
                # A trap: no historical mathematical output may become an input.
                archive.writestr(prefix + "HISTORICAL_PROOF.json", '{"status":"PASS_OLD"}')
                archive.writestr(prefix + "HISTORICAL_ACCEPTED.json", '{"status":"PASS_OLD"}')
        self.patchers = [patch.object(parents, "BRANCHES", self.specs),
                         patch.object(common, "obtain_asset", return_value=self.archive),
                         patch.object(small_indices, "FollowOutput", side_effect=lambda *args: nullcontext())]
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self):
        for patcher in reversed(self.patchers):
            patcher.stop()
        self.temporary.cleanup()

    def task(self, branch="b3"):
        return parents.prepare(branch, self.root / "archives", self.root / (branch + "-task"))

    def proof(self, root, branch, kind):
        names = parents.names(branch)
        sources = parents.verify_sources(root, branch)
        if kind == "initial":
            cover = dict(total=18432, active=100, excluded=18332)
            panels = [dict(pl=str(Fraction(i, 100)), pu=str(Fraction(i+1, 100)),
                           rho_lo=parents.BRANCHES[branch]["rho_lo"],
                           rho_branch_upper=parents.BRANCHES[branch]["rho_hi"]) for i in range(100)]
            return dict(schema="SHARP25_" + branch.upper() + "_UNSEEDED_INITIAL_V1",
                        profile=parents.profile(branch), source_sha256=sources[kind],
                        predecessor_sha256=parents.PREDECESSOR_SHA256, maximum_covers=12,
                        stages=[dict(input_raw=None if i == 0 else "1", input_D=None if i == 0 else "1",
                                     cover=deepcopy(cover)) for i in range(12)],
                        export=dict(**cover, panels=panels), support=dict(q="5/16"),
                        final_invariants=dict(raw="1", D="1"))
        initial = root / names["initial_dir"]
        return dict(schema="EXACT_SHARP25_" + branch.upper() + "_GLOBAL_RESOURCES_V1",
                    profile=parents.profile(branch),
                    source_sha256=dict(sources[kind], **{"FROZEN_SOURCES.json": self.specs[branch]["resource_manifest"]}),
                    parent_proof_sha256=common.digest(initial / names["initial_proof"]),
                    parent_acceptance_sha256=common.digest(initial / names["initial_receipt"]),
                    parent_manifest_sha256=self.specs[branch]["initial_manifest"], parent_source_sha256=sources["initial"],
                    rows=[dict(index=i, result=dict(excluded=not 25 <= i <= 39, history=[])) for i in range(100)])

    def receipt(self, root, branch, kind, proof):
        names = parents.names(branch)
        directory = root / names[kind + "_dir"]
        receipt = dict(status=("PASS_FRESH_EXACT_INITIAL25_" + branch.upper() if kind == "initial" else
                               "PASS_FRESH_EXACT_SHARP25_" + branch.upper() + "_GLOBAL_RESOURCES"),
                       proof_sha256=common.digest(directory / names[kind + "_proof"]),
                       checker_sha256=common.digest(directory / names[kind + "_script"]),
                       profile=parents.profile(branch), source_sha256=proof["source_sha256"], probability_panels=100,
                       negative_controls=parents.INITIAL_CONTROLS if kind == "initial" else parents.RESOURCE_CONTROLS)
        if kind == "initial":
            receipt.update(signed_rectangles=239616, final_invariants=proof["final_invariants"])
        else:
            receipt.update(parent_proof_sha256=proof["parent_proof_sha256"],
                           parent_acceptance_sha256=proof["parent_acceptance_sha256"],
                           surviving_panels=list(range(25, 40)), excluded_panels=list(range(25)) + list(range(40, 100)),
                           signed_support_objects=0)
        return receipt

    def execute_fixture(self, argv, **options):
        """Simulate transport/guard metadata; never interpret any fixture source."""
        self.assertEqual(argv[1:3], ["-B", "-S"])
        self.assertEqual(options["mode"], "trusted_native")
        script = Path(argv[3])
        branch = "b3" if "b3" in script.name else "b4"
        kind = "initial" if script.name.startswith("initial") else "resource"
        action = argv[-1]
        root = Path(options["cwd"])
        names = parents.names(branch)
        if action == "construct":
            common.write(script.parent / names[kind + "_proof"], self.proof(root, branch, kind))
        else:
            proof = common.read(script.parent / names[kind + "_proof"])
            common.write(script.parent / names[kind + "_receipt"], self.receipt(root, branch, kind, proof))
        output = Path(options["output_dir"])
        output.mkdir()
        stdout, stderr = output / "stdout.txt", output / "stderr.txt"
        stdout.write_text(parents._marker(branch, kind + "-" + action) + "\n", encoding="utf-8")
        stderr.write_text("", encoding="utf-8")
        cpu = options["cpu_seconds"]
        controller_cpu = min(30, max(1, cpu // 10))
        return dict(status="completed", returncode=0, stdout_path=str(stdout), stderr_path=str(stderr),
                    stdout_sha256=common.digest(stdout), stderr_sha256=common.digest(stderr),
                    guard_scope=dict(kind="LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1", capability_established=True,
                                     native_python_execution=True, hard_sum_RLIMIT_AS_bytes=512*parents.MIB,
                                     worker_RLIMIT_AS_bytes=448*parents.MIB, supervisor_RLIMIT_AS_bytes=64*parents.MIB,
                                     hard_sum_RLIMIT_CPU_seconds=cpu, supervisor_RLIMIT_CPU_seconds=controller_cpu,
                                     worker_RLIMIT_CPU_seconds=cpu-controller_cpu, script_sha256=common.digest(script),
                                     supervisor_source_sha256=common.digest(Path(parents.__file__).with_name("linux_supervisor.py"))))

    def test_preparation_copies_complete_sources_without_historical_outputs(self):
        task = self.task()
        metadata = common.read(task / "TASK.json")
        self.assertFalse(metadata["stronger24_acquisition_verified"])
        self.assertFalse(metadata["count_interface_join_verified"])
        self.assertIn("not freshly acquired", metadata["conditional_premises"][0])
        for kind, count in (("initial", 30), ("resource", 32)):
            directory = task / "source" / parents.names("b3")[kind + "_dir"]
            self.assertEqual(len(list(directory.iterdir())), count+1)
            self.assertFalse(any("HISTORICAL" in p.name for p in directory.iterdir()))

    def test_source_tampering_fails_before_any_native_launch(self):
        task = self.task()
        script = task / "source" / parents.names("b3")["initial_dir"] / parents.names("b3")["initial_script"]
        script.write_text("corruption", encoding="utf-8")
        with patch.object(common, "supervise") as launch, self.assertRaisesRegex(ValueError, "Unchanged complete"):
            parents.run(task)
        launch.assert_not_called()

    def test_unbound_import_helper_or_injected_parent_output_is_rejected(self):
        task = self.task()
        directory = task / "source" / parents.names("b3")["initial_dir"]
        for name in ("unbound.py", parents.names("b3")["initial_receipt"]):
            path = directory / name
            path.write_text("unbound fixture", encoding="utf-8")
            with patch.object(common, "supervise") as launch, self.assertRaisesRegex(ValueError, "No unbound"):
                parents.run(task)
            launch.assert_not_called()
            path.unlink()

    def test_duplicate_archive_source_member_is_rejected(self):
        capsule = parents.names("b3")["initial_dir"]
        member = "cutoff25_20261011/new_root/" + capsule + "/" + parents.names("b3")["initial_script"]
        with zipfile.ZipFile(self.archive, "a") as archive:
            with self.assertWarns(UserWarning):
                archive.writestr(member, b"duplicate source")
        with self.assertRaisesRegex(ValueError, "One bounded exact source"):
            self.task()

    def test_four_real_action_commands_and_revalidated_stage_resume(self):
        for branch in ("b3", "b4"):
            with self.subTest(branch=branch):
                task = self.task(branch)
                with patch.object(common, "supervise", side_effect=self.execute_fixture) as launch:
                    result = parents.run(task)
                self.assertTrue(result["native_parent_chain_accepted"])
                self.assertFalse(result["stronger24_acquisition_verified"])
                self.assertFalse(result["count_interface_join_verified"])
                self.assertFalse(result["all_index_conclusion_verified"])
                self.assertEqual(launch.call_count, 4)
                self.assertEqual([call.args[0][-1] for call in launch.call_args_list], ["construct", "accept", "construct", "accept"])
                initial = result["stages"]["initial-accept"]["native_result"]
                self.assertEqual(initial["signed_rectangles"], 239616)
                self.assertEqual(initial["negative_controls"], 12)
                resource = result["stages"]["resource-accept"]["native_result"]
                self.assertEqual(resource["probability_panels"], 100)
                self.assertEqual(resource["negative_controls"], 12)
                with patch.object(common, "supervise") as launch_again:
                    repeated = parents.run(task)
                launch_again.assert_not_called()
                self.assertTrue(repeated["native_parent_chain_accepted"])
                root = task / result["stages"]["initial-construct"]["capsule_relative"]
                proof = root / parents.names(branch)["initial_dir"] / parents.names(branch)["initial_proof"]
                proof.write_text("{}\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Unchanged freshly observed"):
                    parents.run(task)

    def test_discovery_guard_cannot_accept_even_complete_fixture_outputs(self):
        task = self.task()
        def weakened(argv, **options):
            result = self.execute_fixture(argv, **options)
            result["guard_scope"]["kind"] = "UNTRUSTED_PROCESS_GROUP"
            return result
        with patch.object(common, "supervise", side_effect=weakened) as launch:
            result = parents.run(task)
        self.assertEqual(launch.call_count, 1)
        self.assertEqual(result["status"], "PARTIAL_NOT_ACCEPTED")
        self.assertFalse(result["native_parent_chain_accepted"])
        self.assertFalse((task / "initial-construct-COMPLETED.json").exists())

    def test_incomplete_execution_preserves_diagnostics_and_stops_chain(self):
        task = self.task()
        def stopped(argv, **options):
            result = self.execute_fixture(argv, **options)
            result.update(status="incomplete", returncode=-9)
            Path(result["stderr_path"]).write_text("fixture bounded timeout\n", encoding="utf-8")
            return result
        with patch.object(common, "supervise", side_effect=stopped) as launch:
            result = parents.run(task)
        self.assertEqual(launch.call_count, 1)
        self.assertEqual(result["failed_stage"], "initial-construct")
        self.assertIn("fixture bounded timeout", result["attempt"]["error"])
        self.assertTrue(list((task / "attempts").glob("*/RESULT.json")))

    def test_boolean_exit_code_and_changed_supervisor_log_capture_are_rejected(self):
        for mutation in (lambda x: x.update(returncode=False), lambda x: x.update(stdout_sha256="0"*64)):
            with self.subTest(mutation=mutation):
                task = self.root / ("mutated-task-" + str(len(list(self.root.glob("mutated-task-*")))))
                parents.prepare("b3", self.root / "archives", task)
                def changed(argv, **options):
                    observed = self.execute_fixture(argv, **options)
                    mutation(observed)
                    return observed
                with patch.object(common, "supervise", side_effect=changed):
                    result = parents.run(task)
                self.assertEqual(result["status"], "PARTIAL_NOT_ACCEPTED")
                self.assertFalse(result["native_parent_chain_accepted"])

    def test_native_initial_inventory_and_type_mutations_are_rejected(self):
        task = self.task()
        root = task / "source"
        directory = root / parents.names("b3")["initial_dir"]
        proof_path = directory / parents.names("b3")["initial_proof"]
        good = self.proof(root, "b3", "initial")
        mutations = [lambda x: x["profile"].update(n=True), lambda x: x["export"]["panels"].pop(),
                     lambda x: x["export"].update(total=True), lambda x: x.update(maximum_covers=True),
                     lambda x: x["stages"][0].update(input_raw="1"),
                     lambda x: x["source_sha256"].pop(next(iter(x["source_sha256"]))),
                     lambda x: x["export"]["panels"][1].update(pl="0")]
        for mutation in mutations:
            bad = deepcopy(good)
            mutation(bad)
            proof_path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaises(ValueError):
                parents.validate_native(root, "b3", "initial", accepted=False)

    def test_resource_acceptance_rejects_parent_rebinding_and_missing_controls(self):
        task = self.task()
        with patch.object(common, "supervise", side_effect=self.execute_fixture):
            result = parents.run(task)
        root = task / result["stages"]["resource-accept"]["capsule_relative"]
        directory = root / parents.names("b3")["resource_dir"]
        receipt_path = directory / parents.names("b3")["resource_receipt"]
        receipt = common.read(receipt_path)
        receipt["negative_controls"] = receipt["negative_controls"][:-1]
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "twelve named"):
            parents.validate_native(root, "b3", "resource", accepted=True)
        proof_path = directory / parents.names("b3")["resource_proof"]
        proof = common.read(proof_path)
        proof["parent_acceptance_sha256"] = "0" * 64
        proof_path.write_text(json.dumps(proof), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "this freshly acquired"):
            parents.validate_native(root, "b3", "resource", accepted=False)

    def test_explicit_stage_requires_previous_guarded_completion(self):
        task = self.task()
        with patch.object(common, "supervise") as launch, self.assertRaisesRegex(ValueError, "preceding native stage"):
            parents.run(task, stage="resource-construct")
        launch.assert_not_called()

    def test_colab_failure_still_exports_result_bundle(self):
        from be_replay import colab_batch
        with patch.object(parents, "prepare", side_effect=ValueError("fixture preparation failure")):
            result = parents.run_colab("b3", durable_root=self.root / "durable", work_root=self.root / "work",
                                       archives=self.root / "archives")
        self.assertEqual(result["status"]["state"], "PARTIAL_ERROR_NOT_ACCEPTED")
        self.assertFalse(result["status"]["native_parent_chain_accepted"])
        with zipfile.ZipFile(result["bundle"]) as bundle:
            names = bundle.namelist()
            self.assertTrue(any(n.endswith("SESSION_RESULT.json") for n in names))
            self.assertTrue(any(n.endswith("ERROR.txt") for n in names))


class PublishedParentPinsTests(unittest.TestCase):
    def test_distinct_exact_whole_parent_domains(self):
        self.assertEqual(parents.BRANCHES["b3"]["rho_lo"], "13/10")
        self.assertEqual(parents.BRANCHES["b3"]["rho_hi"], "7/5")
        self.assertEqual(parents.BRANCHES["b4"]["rho_lo"], "7/5")
        self.assertEqual(parents.BRANCHES["b4"]["rho_hi"], "3/2")
        self.assertEqual(len({spec[k] for spec in parents.BRANCHES.values()
                              for k in ("initial_manifest", "resource_manifest")}), 4)
        self.assertEqual(len(parents.INITIAL_CONTROLS), 12)
        self.assertEqual(len(parents.RESOURCE_CONTROLS), 12)


if __name__ == "__main__":
    unittest.main()
