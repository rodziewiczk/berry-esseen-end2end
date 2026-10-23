"""Transport/identity fixtures only; fixture mathematical scripts are never run."""
from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import test_n25_parents as fixtures
from be_replay import n25_parent_evidence as evidence
from be_replay import n25_parents as parents
from be_replay import count_task as common
from be_replay.linux_supervisor import _filter_instructions

ROOT = Path(__file__).resolve().parents[1]


class ParentEvidenceTests(unittest.TestCase):
    def setUp(self):
        work = ROOT / "work"
        work.mkdir(exist_ok=True)
        original_temporary = tempfile.TemporaryDirectory
        self.temp_patch = patch.object(fixtures.tempfile, "TemporaryDirectory",
                                      side_effect=lambda *a, **k: original_temporary(*a, dir=work, **k))
        self.temp_patch.start()
        self.fixture = fixtures.ParentTaskTests(methodName="test_preparation_copies_complete_sources_without_historical_outputs")
        self.fixture.setUp()

    def tearDown(self):
        self.fixture.tearDown()
        self.temp_patch.stop()

    def execute(self, argv, **options):
        observed = self.fixture.execute_fixture(argv, **options)
        output = Path(options["output_dir"])
        cpu = options["cpu_seconds"]
        controller = min(30, max(1, cpu//10))
        rows, architecture, denied, prlimit = _filter_instructions("x86_64")
        guard = dict(seccomp_mode=2, no_new_privileges=True, audit_architecture=architecture,
                     machine="x86_64", denied_syscalls=denied, prlimit64_query_only=prlimit,
                     x32_or_unknown_syscall_ABI_killed=True,
                     filter_instructions_sha256=hashlib.sha256(json.dumps(rows).encode()).hexdigest())
        worker = dict(guard, address_space_bytes=448*parents.MIB, cpu_seconds=cpu-controller,
                      script_sha256=common.digest(argv[3]), pid=1234, birth_tick=1000)
        controller_guard = dict(guard, address_space_bytes=64*parents.MIB, cpu_seconds=controller)
        observed.update(mode="trusted_native", reason=None, proof_accepted=False)
        observed["guard_scope"].update(worker_guard=worker, supervisor_guard=controller_guard)
        config = dict(argv=argv, cwd=str(options["cwd"]), output_dir=str(output),
                      wall_seconds=float(options["wall_seconds"]), cpu_seconds=cpu,
                      memory_bytes=512*parents.MIB, checkpoint_paths=[], mode="trusted_native",
                      sample_seconds=.1, disk_bytes=256*parents.MIB, log_bytes=16*parents.MIB,
                      worker_memory_bytes=448*parents.MIB, supervisor_memory_bytes=64*parents.MIB,
                      worker_cpu_seconds=cpu-controller, supervisor_cpu_seconds=controller)
        common.write(output / "native-launch.json", config)
        common.write(output / "launch.json", dict(config, argv=[argv[0], "-B", "-S",
                     str(Path(parents.__file__).with_name("linux_supervisor.py")), "--_native-controller",
                     str(output / "native-launch.json")]))
        common.write(output / "native-worker-guard.json", worker)
        common.write(output / "native-controller-guard.json", controller_guard)
        common.write(output / "native-controller-result.json", dict(returncode=0, worker_pid=1234,
                     worker_source_sha256_after=common.digest(argv[3])))
        common.write(output / "supervisor-result.json", observed)
        return observed

    def completed(self, branch="b3"):
        with redirect_stdout(io.StringIO()):
            task = self.fixture.task(branch)
            with patch.object(common, "supervise", side_effect=self.execute):
                result = parents.run(task)
        self.assertTrue(result["native_parent_chain_accepted"])
        return task

    def update_last(self, task, change):
        ledger = task / "resource-accept-COMPLETED.json"
        obj = common.read(ledger)
        change(obj)
        ledger.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
        attempt = task / Path(obj["capsule_relative"]).parent
        (attempt / "RESULT.json").write_bytes(ledger.read_bytes())

    def test_restored_both_branches_validate_without_launch_or_byte_changes(self):
        for branch in ("b3", "b4"):
            with self.subTest(branch=branch):
                original = self.completed(branch)
                restored = self.fixture.root / ("restored-" + branch)
                shutil.copytree(original, restored)
                shutil.rmtree(original)
                before = {p.relative_to(restored).as_posix(): common.digest(p) for p in restored.rglob("*") if p.is_file()}
                with patch.object(common, "supervise", side_effect=AssertionError("No numerical launch")):
                    result = evidence.validate_completed(restored, original_task_root=str(original), expected_branch=branch)
                    inferred = evidence.validate_completed(restored)
                self.assertEqual(result, inferred)
                self.assertEqual(result["schema"], "REVALIDATED_N25_PARENT_V1")
                self.assertEqual(result["contact_allowance"], "5/16")
                self.assertEqual(result["signed_rectangles"], 239616)
                self.assertEqual(len(result["stage_ledger_sha256"]), 4)
                self.assertTrue(result["native_arithmetic_accepted"])
                self.assertFalse(result["stronger24_acquisition_verified"])
                self.assertFalse(result["count_interface_join_verified"])
                self.assertFalse(result["all_index_conclusion_verified"])
                self.assertTrue((restored / result["resource_capsule_relative"] / parents.names(branch)["resource_dir"]).is_dir())
                self.assertEqual(before, {p.relative_to(restored).as_posix(): common.digest(p)
                                          for p in restored.rglob("*") if p.is_file()})

    def test_wrong_branch_or_original_prefix_is_rejected(self):
        task = self.completed()
        for options in ({"expected_branch": "b4"}, {"original_task_root": "/another/original/task"}):
            with self.subTest(options=options), self.assertRaises((ValueError, KeyError)):
                evidence.validate_completed(task, **options)

    def test_exact_task_premises_and_flags_are_required(self):
        task = self.completed()
        path = task / "TASK.json"
        saved = common.read(path)
        for mutate in (lambda o:o.update(stronger24_acquisition_verified=True),
                       lambda o:o.update(imported_stronger24_sha256="0"*64),
                       lambda o:o["conditional_premises"].pop(), lambda o:o.update(unbound=True)):
            value = deepcopy(saved); mutate(value)
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(ValueError):
                evidence.validate_completed(task)
        path.write_text(json.dumps(saved), encoding="utf-8")

    def test_missing_complete_stage_or_dependency_is_rejected(self):
        task = self.completed()
        self.update_last(task, lambda o:o["dependencies"].pop("initial-construct"))
        with self.assertRaisesRegex(ValueError, "dependency chain"):
            evidence.validate_completed(task)
        (task / "initial-accept-COMPLETED.json").unlink()
        with self.assertRaises(ValueError):
            evidence.validate_completed(task)

    def test_false_integer_returncode_and_weak_guard_are_rejected(self):
        task = self.completed()
        ledger = task / "resource-accept-COMPLETED.json"
        saved = common.read(ledger)
        for mutate in (lambda o:o["observed"].update(returncode=False),
                       lambda o:o["observed"]["guard_scope"].update(capability_established=False)):
            value = deepcopy(saved); mutate(value)
            self.update_last(task, lambda o:o.update(value))
            with self.assertRaises(ValueError):
                evidence.validate_completed(task)

    def test_empty_capture_with_wrong_hash_and_nonempty_stderr_are_rejected(self):
        task = self.completed()
        saved = common.read(task / "resource-accept-COMPLETED.json")
        self.update_last(task, lambda o:o["observed"].update(stderr_sha256="0"*64))
        with self.assertRaisesRegex(ValueError, "capture matches"):
            evidence.validate_completed(task)
        stderr = Path(saved["observed"]["stderr_path"])
        stderr.write_text("fixture diagnostic\n", encoding="utf-8")
        saved["stderr_sha256"] = common.digest(stderr)
        saved["observed"]["stderr_sha256"] = common.digest(stderr)
        self.update_last(task, lambda o:o.update(saved))
        with self.assertRaisesRegex(ValueError, "stderr is empty"):
            evidence.validate_completed(task)

    def test_actual_launch_cwd_and_supervisor_result_are_checked(self):
        task = self.completed()
        report = common.read(task / "resource-accept-COMPLETED.json")
        execution = task / Path(report["capsule_relative"]).parent / "execution"
        path = execution / "native-launch.json"
        original = path.read_bytes(); obj = common.read(path); obj["cwd"] = str(task / "source")
        path.write_text(json.dumps(obj), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "native launch"):
            evidence.validate_completed(task)
        path.write_bytes(original)
        path = execution / "supervisor-result.json"
        obj = common.read(path);obj["status"] = "incomplete";path.write_text(json.dumps(obj), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "supervisor-result"):
            evidence.validate_completed(task)

    def test_complete_artifact_set_and_traversal_are_rejected(self):
        task = self.completed()
        self.update_last(task, lambda o:o["artifact_sha256"].pop(parents.names("b3")["initial_dir"] + "/" + parents.names("b3")["initial_receipt"]))
        with self.assertRaisesRegex(ValueError, "artifact inventory"):
            evidence.validate_completed(task)
        self.update_last(task, lambda o:o.update(capsule_relative="attempts/../new_root"))
        with self.assertRaises(ValueError):
            evidence.validate_completed(task)

    def test_resource_copy_must_be_the_exact_earlier_fresh_initial_receipt(self):
        task = self.completed()
        ledger = common.read(task / "resource-accept-COMPLETED.json")
        root = task / ledger["capsule_relative"]
        names = parents.names("b3")
        initial_receipt = root / names["initial_dir"] / names["initial_receipt"]
        obj = common.read(initial_receipt); obj["unbound_transport_addition"] = True
        initial_receipt.write_text(json.dumps(obj), encoding="utf-8")
        for key in ("resource_proof", "resource_receipt"):
            path = root / names["resource_dir"] / names[key]
            obj = common.read(path); obj["parent_acceptance_sha256"] = common.digest(initial_receipt)
            if key == "resource_receipt":
                obj["proof_sha256"] = common.digest(root / names["resource_dir"] / names["resource_proof"])
            path.write_text(json.dumps(obj), encoding="utf-8")
        def rebind(report):
            report["artifact_sha256"] = {n:common.digest(root / n) for n in report["artifact_sha256"]}
            report["native_result"] = parents.validate_native(root, "b3", "resource", accepted=True)
        self.update_last(task, rebind)
        with self.assertRaisesRegex(ValueError, "exact fresh INITIAL acceptance"):
            evidence.validate_completed(task)

    def test_kernel_guard_sidecar_is_required_and_not_just_the_embedded_flag(self):
        task = self.completed()
        report = common.read(task / "resource-accept-COMPLETED.json")
        path = task / Path(report["capsule_relative"]).parent / "execution/native-worker-guard.json"
        obj = common.read(path);obj["seccomp_mode"] = 0;path.write_text(json.dumps(obj), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "kernel guard sidecar"):
            evidence.validate_completed(task)


if __name__ == "__main__":
    unittest.main()
