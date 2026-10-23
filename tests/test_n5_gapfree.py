"""Preparation and mocked protocol fixtures; no frozen arithmetic executes."""
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

from be_replay import n5_gapfree as job


class N5GapfreeTests(unittest.TestCase):
    def setUp(self):
        parent = job.ROOT / "work" / "n5-gapfree-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def prepared(self):
        task = job.prepare(self.root / "task")
        return task, task / "arithmetic/private/capsule"

    def original(self, capsule):
        return dict(status="PASS_FRESH_C5_GAPFREE_INDEPENDENT_WHOLE_LINE", n=5,
                    rho=job.DOMAIN["rho"], beta=job.DOMAIN["beta"], target=job.DOMAIN["target"],
                    compact=dict(**job.CENSUS, independent_upper="2/5", stored_upper="409/1000"),
                    exteriors=dict(left_upper="33/100", right_upper="93/500", left_domain="z<=0", right_domain="z>=5"),
                    negative_controls=job.ORIGINAL_CONTROLS, inputs=job.inputs(job.verify_sources(job.VENDOR)),
                    adapter_sha256=job.digest(capsule / "c5_gapfree_worker.py"),
                    old_capture_metadata_used_as_a_mathematical_premise=False,
                    unrestricted_C5_or_all_indices_verified_by_this_stage=False)

    def packet(self, capsule, old):
        return dict(schema="FRESH_LINUX_N5_GAPFREE_WHOLE_LINE_RESULT_V1", status="NATIVE_WORKER_COMPLETED",
                    domain=job.DOMAIN, census=job.CENSUS, compact=old["compact"], exteriors=old["exteriors"],
                    original_controls=job.ORIGINAL_CONTROLS, added_controls=job.ADDED_CONTROLS, control_count=21,
                    manifest_sha256=job.MANIFEST_SHA256, driver_sha256=job.digest(job.__file__),
                    original_result_sha256=job.digest(capsule / job.OLD_RESULT),
                    inputs_sha256={name: job.digest(capsule / name) for name in sorted(job.SOURCE_NAMES)},
                    original_checker_main_called=False, historical_execution_used_as_a_premise=False,
                    full_n5_verified=False, all_index_conclusion_verified=False)

    def guard(self, capsule, cpu_seconds):
        controller = min(30, max(1, cpu_seconds // 10))
        return dict(kind="LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1", capability_established=True,
                    native_python_execution=True, hard_sum_RLIMIT_AS_bytes=512*job.MIB,
                    worker_RLIMIT_AS_bytes=448*job.MIB, supervisor_RLIMIT_AS_bytes=64*job.MIB,
                    hard_sum_RLIMIT_CPU_seconds=cpu_seconds, supervisor_RLIMIT_CPU_seconds=controller,
                    worker_RLIMIT_CPU_seconds=cpu_seconds-controller, script_sha256=job.digest(capsule / job.ENTRY),
                    supervisor_source_sha256=job.digest(Path(job.__file__).with_name("linux_supervisor.py")))

    def fake_native(self, *, mutate=None, unsupported=False):
        def observe(argv, **options):
            capsule = Path(options["cwd"])
            self.assertEqual(argv[1:3], ["-B", "-S"])
            self.assertEqual(argv[-1], "--_worker")
            self.assertEqual(Path(argv[3]), capsule / job.ENTRY)
            self.assertEqual(options["mode"], "trusted_native")
            self.assertEqual(options["memory_bytes"], 512*job.MIB)
            self.assertEqual(options["cpu_seconds"], 7200)
            self.assertEqual(options["wall_seconds"], 7260)
            output = Path(options["output_dir"])
            output.mkdir()
            stdout, stderr = output / "stdout.txt", output / "stderr.txt"
            old = self.original(capsule)
            job.write(capsule / job.OLD_RESULT, old)
            packet = self.packet(capsule, old)
            job.write(capsule / job.RESULT, packet)
            stdout.write_text(json.dumps(old) + "\n" + json.dumps(packet) + "\n", encoding="utf-8")
            stderr.write_bytes(b"")
            receipt = dict(status="unsupported" if unsupported else "completed", returncode=0,
                           stdout_path=str(stdout), stderr_path=str(stderr), stdout_sha256=job.digest(stdout),
                           stderr_sha256=job.digest(stderr), guard_scope=self.guard(capsule, options["cpu_seconds"]))
            if mutate:
                mutate(capsule, receipt)
            return receipt
        return observe

    def checked_run(self, task, **options):
        with patch("be_replay.count_task.supervise", self.fake_native(**options)), redirect_stdout(io.StringIO()):
            return job.run(task)

    def test_complete_frozen_closure_is_exact_and_preparation_does_not_import_it(self):
        with patch.object(job.runpy, "run_path", side_effect=AssertionError("No arithmetic in preparation")), \
             patch.object(job.importlib.util, "module_from_spec", side_effect=AssertionError("No mathematical import")):
            source = job.verify_sources(job.VENDOR)
            task, capsule = self.prepared()
        self.assertEqual(set(source["files"]), job.SOURCE_NAMES)
        self.assertEqual(job.census(capsule), dict(roots=60, nodes=1994, leaves=1027))
        self.assertGreaterEqual(len(capsule.parents), 4)
        self.assertEqual(job.verify_sources(capsule, capsule=True), source)
        self.assertFalse((capsule / job.OLD_RESULT).exists())
        self.assertFalse((capsule / job.RESULT).exists())
        self.assertEqual(job.read(task / "TASK.json")["native_arithmetic_accepted"], False)
        for name in job.SOURCE_NAMES:
            self.assertEqual((capsule / name).read_bytes(), (job.VENDOR / name).read_bytes())

    def test_vendor_tampering_and_extra_source_are_rejected(self):
        vendor = self.root / "vendor"
        shutil.copytree(job.VENDOR, vendor)
        (vendor / "LICENSE").write_bytes(b"different license")
        with self.assertRaisesRegex(ValueError, "Unchanged frozen source"):
            job.verify_sources(vendor)
        shutil.copyfile(job.VENDOR / "LICENSE", vendor / "LICENSE")
        (vendor / "old_receipt.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "historical output"):
            job.verify_sources(vendor)

    def test_no_historical_output_or_second_execution_can_be_reused(self):
        task, capsule = self.prepared()
        (capsule / job.OLD_RESULT).write_text("{}")
        with self.assertRaisesRegex(ValueError, "historical output"):
            job.run(task)
        with self.assertRaisesRegex(ValueError, "new private task"):
            job.prepare(task)

    def test_exact_full_guarded_fixture_is_accepted_only_for_scoped_rectangle(self):
        task, capsule = self.prepared()
        report = self.checked_run(task)
        self.assertEqual(report["status"], job.ACCEPTED)
        self.assertIs(report["native_arithmetic_accepted"], True)
        self.assertIs(report["full_n5_verified"], False)
        self.assertIs(report["all_index_conclusion_verified"], False)
        self.assertEqual(report["domain"]["cdf_orientation"], "POSITIVE_CLOSED")
        self.assertEqual(report["native_result"]["control_count"], 21)
        self.assertEqual(report["native_result"]["census"], job.CENSUS)
        with self.assertRaises(ValueError):
            job.run(task)

    def test_unsupported_native_guard_never_falls_back_to_search(self):
        task, _ = self.prepared()
        report = self.checked_run(task, unsupported=True)
        self.assertEqual(report["status"], "PARTIAL_NOT_ACCEPTED")
        self.assertIs(report["native_arithmetic_accepted"], False)

    def test_false_returncode_is_not_integer_zero(self):
        task, _ = self.prepared()
        report = self.checked_run(task, mutate=lambda c, r: r.update(returncode=False))
        self.assertIn("integer successful", report["error"])
        self.assertFalse(report["native_arithmetic_accepted"])

    def test_missing_capability_is_not_acceptance(self):
        task, _ = self.prepared()
        report = self.checked_run(task, mutate=lambda c, r: r["guard_scope"].update(capability_established=False))
        self.assertIn("native guard", report["error"])
        self.assertFalse(report["native_arithmetic_accepted"])

    def test_modified_actual_stdout_is_rejected_even_with_valid_terminal_file(self):
        task, _ = self.prepared()
        def mutate(capsule, receipt):
            with Path(receipt["stdout_path"]).open("a") as stream:
                stream.write("\n")
        report = self.checked_run(task, mutate=mutate)
        self.assertIn("supervisor capture", report["error"])
        self.assertFalse(report["native_arithmetic_accepted"])

    def test_nonempty_stderr_is_rejected_even_when_hash_is_rebound(self):
        task, _ = self.prepared()
        def mutate(capsule, receipt):
            path = Path(receipt["stderr_path"])
            path.write_text("unexpected diagnostic")
            receipt["stderr_sha256"] = job.digest(path)
        report = self.checked_run(task, mutate=mutate)
        self.assertIn("empty stderr", report["error"])

    def test_empty_stderr_with_wrong_supervisor_hash_is_rejected(self):
        task, _ = self.prepared()
        report = self.checked_run(task, mutate=lambda c, r: r.update(stderr_sha256="0"*64))
        self.assertIn("supervisor capture", report["error"])
        self.assertFalse(report["native_arithmetic_accepted"])

    def test_extra_file_after_worker_is_rejected(self):
        task, _ = self.prepared()
        def mutate(capsule, receipt):
            (capsule / "unexpected-receipt.json").write_text("{}")
        report = self.checked_run(task, mutate=mutate)
        self.assertIn("historical output", report["error"])
        self.assertFalse(report["native_arithmetic_accepted"])

    def test_source_change_after_worker_is_rejected(self):
        task, _ = self.prepared()
        def mutate(capsule, receipt):
            with (capsule / "FOREST.json").open("ab") as stream:
                stream.write(b" ")
        report = self.checked_run(task, mutate=mutate)
        self.assertIn("Unchanged frozen source", report["error"])

    def test_missing_control_in_result_and_terminal_packet_is_rejected(self):
        task, _ = self.prepared()
        def mutate(capsule, receipt):
            path = capsule / job.RESULT
            packet = job.read(path)
            packet["added_controls"].pop()
            path.unlink()
            job.write(path, packet)
            log = Path(receipt["stdout_path"])
            log.write_text(json.dumps(packet) + "\n")
            receipt["stdout_sha256"] = job.digest(log)
        report = self.checked_run(task, mutate=mutate)
        self.assertIn("Complete exact Linux", report["error"])

    def test_other_log_path_is_rejected_even_with_matching_bytes(self):
        task, _ = self.prepared()
        def mutate(capsule, receipt):
            other = task / "another-stdout.txt"
            shutil.copyfile(receipt["stdout_path"], other)
            receipt["stdout_path"] = str(other)
        report = self.checked_run(task, mutate=mutate)
        self.assertIn("Actual bounded log", report["error"])

    def test_five_controls_reach_original_validator_and_duplicate_parser(self):
        forest = dict(beta=["17/50", "x"], roots=[dict(tree=["S", 0, ["L", 1], ["L", 1]])])
        observed = []
        def reject(value):
            observed.append(value)
            raise ValueError("Fixture validator rejects malformed input")
        module = SimpleNamespace(validate=reject, unique=job.unique)
        self.assertEqual(job.additional_controls(module, forest), job.ADDED_CONTROLS)
        self.assertEqual(len(observed), 4)
        self.assertEqual(observed[0]["beta"][0], "347/1000")
        self.assertEqual(observed[1]["roots"][0]["tree"][1], 2)
        self.assertIs(observed[2]["roots"][0]["tree"][1], True)
        self.assertEqual(len(observed[3]["roots"][0]["tree"]), 3)
        self.assertEqual(forest["roots"][0]["tree"][1], 0)

    def test_control_that_is_not_rejected_fails_closed(self):
        forest = dict(beta=["17/50", "x"], roots=[dict(tree=["S", 0, ["L", 1], ["L", 1]])])
        with self.assertRaisesRegex(ValueError, "Corruption accepted"):
            job.additional_controls(SimpleNamespace(validate=lambda x: None, unique=job.unique), forest)

    def test_worker_dispatch_calls_unchanged_main_then_extra_controls_with_mocked_math(self):
        _, capsule = self.prepared()
        seen = []
        def main():
            seen.append("unchanged-worker-main")
            job.write(capsule / job.OLD_RESULT, self.original(capsule))
        loader = SimpleNamespace(exec_module=lambda m: seen.append("unchanged-checker-extra-controls"))
        def reject(value):
            raise ValueError("Malformed fixture rejected")
        module = SimpleNamespace(validate=reject, unique=job.unique)
        with patch.object(job, "__file__", str(capsule / job.ENTRY)), \
             patch.object(job.sys, "dont_write_bytecode", True), \
             patch.object(job.runpy, "run_path", return_value={"main": main}) as dispatch, \
             patch.object(job.importlib.util, "spec_from_file_location", return_value=SimpleNamespace(loader=loader)), \
             patch.object(job.importlib.util, "module_from_spec", return_value=module), redirect_stdout(io.StringIO()):
            job.worker()
        dispatch.assert_called_once_with(str(capsule / "c5_gapfree_worker.py"), run_name="frozen_independent_worker")
        self.assertEqual(seen, ["unchanged-worker-main", "unchanged-checker-extra-controls"])
        self.assertEqual(job.read(capsule / job.RESULT)["control_count"], 21)

    def test_invalid_budget_never_dispatches(self):
        with patch("be_replay.count_task.supervise", side_effect=AssertionError("No dispatch")):
            for values in (dict(cpu_seconds=7201), dict(wall_seconds=7261), dict(cpu_seconds=True)):
                with self.assertRaises(ValueError):
                    job.run(self.root, **values)

    def test_preparation_failure_still_creates_final_zip_and_false_scope_flags(self):
        from be_replay import colab_batch
        with patch.object(job, "prepare", side_effect=ValueError("fixture preparation failure")), \
             patch("be_replay.environment.snapshot", return_value={"fixture": True}), redirect_stdout(io.StringIO()):
            result = job.run_colab(durable_root=self.root / "durable", work_root=self.root / "work")
        self.assertEqual(result["status"]["state"], "PARTIAL_ERROR_NOT_ACCEPTED")
        self.assertFalse(result["status"]["native_arithmetic_accepted"])
        self.assertFalse(result["status"]["full_n5_verified"])
        bundle = Path(result["bundle"])
        self.assertTrue(bundle.is_file())
        self.assertTrue(bundle.with_suffix(".zip.sha256").is_file())
        with zipfile.ZipFile(bundle) as archive:
            status_name = next(name for name in archive.namelist() if name.endswith("/SESSION_RESULT.json"))
            status = json.loads(archive.read(status_name))
            self.assertFalse(status["all_index_conclusion_verified"])
            self.assertTrue(any(name.endswith("/ERROR.txt") for name in archive.namelist()))
        self.assertTrue((Path(result["work"]) / "PROGRESS.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
