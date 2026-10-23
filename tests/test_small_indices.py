"""Driver/source/trust fixtures only. Never execute a mathematical checker."""
from copy import deepcopy
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import small_indices as small


def output_for(stage):
    lines = []
    if stage == "n2-primary":
        lines = [f"CHECKED {i} 1 1" for i in range(70)]
    elif stage == "n2-independent":
        lines = [f"INTEGER_CHECK {i:02d}: triangles=1, leaves=1, moment_boxes=1" for i in range(70)]
    elif stage == "n3-full":
        manifest = small.verify_vendor()
        hashes = [row["sha256"] for row in manifest["files"]
                  if row["path"].startswith("n3/certificate/")]
        lines = [f"CELL {i:03d} [0,1] nodes=1 leaves=1 depth=1 moment_boxes=1 sha256={digest}"
                 for i, digest in enumerate(hashes)]
    return "\n".join([*lines, small.STAGES[stage]["marker"]]) + "\n"


def weak_receipt():
    return {"status": "completed", "returncode": 0, "mode": "untrusted_search",
            "guard_scope": {"kind": "UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP",
                            "proof_acceptance": False}, "proof_accepted": False}


class SmallIndicesTests(unittest.TestCase):
    def setUp(self):
        fixture_parent = small.ROOT / "work/small-index-fixtures"
        fixture_parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=fixture_parent)
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.assertTrue(self.root.resolve().is_relative_to((small.ROOT / "work").resolve()))
        self.temp.cleanup()

    def test_frozen_complete_inventory_without_importing_kernels(self):
        data = small.verify_vendor()
        self.assertEqual(data["certificate_counts"], {"n2": 70, "n3": 111})
        self.assertEqual(len(data["files"]), 189)

    def test_source_byte_mutation_is_rejected(self):
        destination = self.root / "source"
        shutil.copytree(small.VENDOR, destination)
        with (destination / "n3/certificate/110.json").open("ab") as stream:
            stream.write(b" ")
        with self.assertRaisesRegex(ValueError, "Unchanged native source"):
            small.verify_vendor(destination)

    def test_manifest_mutation_is_rejected(self):
        destination = self.root / "source"
        shutil.copytree(small.VENDOR, destination)
        with (destination / "MANIFEST.json").open("ab") as stream:
            stream.write(b"\n")
        with self.assertRaisesRegex(ValueError, "manifest identity"):
            small.verify_vendor(destination)

    def test_extra_receipt_is_not_a_source(self):
        destination = self.root / "source"
        shutil.copytree(small.VENDOR, destination)
        (destination / "OLD_PASS.json").write_text('{"status":"PASS"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "extra source-tree"):
            small.verify_vendor(destination)

    def test_full_native_marker_requires_complete_n2_census(self):
        text = output_for("n2-primary").replace("CHECKED 69 1 1\n", "")
        with self.assertRaisesRegex(ValueError, "cell census"):
            small.validate_output("n2-primary", text)

    def test_duplicate_count_is_rejected(self):
        text = output_for("n2-independent").replace("INTEGER_CHECK 69:", "INTEGER_CHECK 68:")
        with self.assertRaisesRegex(ValueError, "cell census"):
            small.validate_output("n2-independent", text)

    def test_reordered_n3_cells_are_rejected(self):
        text = output_for("n3-full").splitlines()
        text[0], text[1] = text[1], text[0]
        with self.assertRaisesRegex(ValueError, "cell census"):
            small.validate_output("n3-full", "\n".join(text))

    def test_duplicate_acceptance_marker_is_rejected(self):
        marker = small.STAGES["n3-scalars"]["marker"]
        with self.assertRaisesRegex(ValueError, "One exact"):
            small.validate_output("n3-scalars", marker + "\n" + marker)

    def test_rejection_cannot_coexist_with_success(self):
        with self.assertRaisesRegex(ValueError, "rejection"):
            small.validate_output("n2-scalars", output_for("n2-scalars") + "REJECTED: fixture\n")

    def test_nonzero_exit_even_with_marker_is_incomplete(self):
        receipt = weak_receipt()
        receipt["returncode"] = 1
        with self.assertRaisesRegex(ValueError, "successful bounded"):
            small.classify("n3-scalars", receipt, output_for("n3-scalars"))

    def test_timeout_even_with_marker_is_incomplete(self):
        receipt = weak_receipt()
        receipt.update(status="incomplete", reason="external_wall_timeout")
        with self.assertRaises(ValueError):
            small.classify("n2-scalars", receipt, output_for("n2-scalars"))

    def test_basic_mode_never_accepts_math_certificate(self):
        result = small.classify("n3-full", weak_receipt(), output_for("n3-full"))
        self.assertFalse(result["native_arithmetic_accepted"])
        self.assertFalse(result["all_law_theorem_verified"])

    def test_native_guard_without_established_capability_is_not_accepted(self):
        receipt = weak_receipt()
        receipt.update(mode="trusted_native", guard_scope={
            "kind": "LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1",
            "contract_status": "experimental_platform_contract_requires_review",
            "native_python_execution": True, "proof_acceptance": False})
        self.assertFalse(small.classify("n2-scalars", receipt, output_for("n2-scalars"))[
            "native_arithmetic_accepted"])

    def established_guard(self):
        receipt = weak_receipt()
        receipt.update(mode="trusted_native", guard_scope={
            "kind": "LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1",
            "native_python_execution": True, "capability_established": True,
            "proof_acceptance": False, "hard_sum_RLIMIT_AS_bytes": 512*small.MIB,
            "worker_RLIMIT_AS_bytes": 448*small.MIB,
            "supervisor_RLIMIT_AS_bytes": 64*small.MIB,
            "hard_sum_RLIMIT_CPU_seconds": 7200,
            "worker_RLIMIT_CPU_seconds": 7170, "supervisor_RLIMIT_CPU_seconds": 30,
            "script_sha256": "a"*64, "supervisor_source_sha256": "b"*64})
        return receipt

    def test_established_native_resource_contract_is_not_a_supervisor_proof_boolean(self):
        result = small.classify("n2-scalars", self.established_guard(), output_for("n2-scalars"),
                                script_sha="a"*64, supervisor_sha="b"*64,
                                memory_bytes=512*small.MIB, cpu_seconds=7200)
        self.assertTrue(result["native_arithmetic_accepted"])
        self.assertFalse(result["all_law_theorem_verified"])

    def test_wrong_native_source_pin_and_caps_are_rejected(self):
        receipt = self.established_guard()
        receipt["guard_scope"]["script_sha256"] = "c"*64
        self.assertFalse(small.trusted_guard(receipt, script_sha="a"*64,
                                            supervisor_sha="b"*64,
                                            memory_bytes=512*small.MIB, cpu_seconds=7200))
        receipt = self.established_guard()
        receipt["guard_scope"]["worker_RLIMIT_AS_bytes"] = 512*small.MIB
        self.assertFalse(small.trusted_guard(receipt, script_sha="a"*64,
                                            supervisor_sha="b"*64,
                                            memory_bytes=512*small.MIB, cpu_seconds=7200))

    def test_cpp_cannot_use_python_single_process_contract(self):
        receipt = self.established_guard()
        self.assertFalse(small.classify("n3-full", receipt, output_for("n3-full"),
                                       script_sha="a"*64, supervisor_sha="b"*64,
                                       memory_bytes=512*small.MIB, cpu_seconds=7200)[
            "native_arithmetic_accepted"])

    def fake_supervisor(self, wrong_n3_digest=False, wrong_stdout_digest=False):
        """Controlled fixture writes; no child/native evaluator is ever launched."""
        def run(argv, **settings):
            self.assertTrue(Path(argv[3]).resolve().is_relative_to(Path(settings["cwd"]).resolve()))
            self.assertEqual(small.sha(argv[3]), small.sha(small.__file__))
            config = json.loads(Path(argv[-1]).read_text("utf-8"))
            stage = config["stage"]
            output = Path(settings["output_dir"])
            output.mkdir(parents=True)
            text = output_for(stage)
            if wrong_n3_digest and stage == "n3-full":
                text = re.sub(r"sha256=[0-9a-f]{64}", "sha256=" + "0"*64, text, count=1)
            stdout = output / "stdout.txt"
            stdout.write_text(text, encoding="utf-8")
            stderr = output / "stderr.txt"
            stderr.write_text("", encoding="utf-8")
            return dict(weak_receipt(), stdout_path=str(stdout), stderr_path=str(stderr),
                        stdout_sha256="0"*64 if wrong_stdout_digest else small.sha(stdout))
        return run

    def test_full_six_stage_orchestration_stays_untrusted(self):
        with patch("be_replay.linux_supervisor.run", side_effect=self.fake_supervisor()) as supervisor:
            with patch.object(small.shutil, "which", return_value=str(Path(small.sys.executable))):
                result = small.run(self.root / "run", heartbeat_seconds=1)
        self.assertEqual(supervisor.call_count, 6)
        self.assertTrue(result["all_selected_stages_computed"])
        self.assertTrue(result["all_required_stages_selected"])
        self.assertFalse(result["native_arithmetic_accepted"])
        self.assertEqual(result["status"], "COMPUTED_EXACT_OUTPUTS_UNTRUSTED_GUARD")
        self.assertTrue((self.root / "run/progress.jsonl").stat().st_size > 0)
        self.assertTrue((self.root / "run/SMALL_INDICES_RESULT.json").is_file())
        self.assertFalse(result["context"]["historical_receipts_used"])

    def test_partial_selection_does_not_claim_full_n2_n3(self):
        with patch("be_replay.linux_supervisor.run", side_effect=self.fake_supervisor()):
            result = small.run(self.root / "run", stages=["n2-scalars"], heartbeat_seconds=1)
        self.assertTrue(result["all_selected_stages_computed"])
        self.assertFalse(result["all_required_stages_selected"])
        self.assertFalse(result["native_arithmetic_accepted"])

    def test_fresh_output_is_exclusive(self):
        output = self.root / "run"
        output.mkdir()
        with self.assertRaisesRegex(ValueError, "Fresh exclusive"):
            small.run(output, stages=["n2-scalars"])

    def test_stdout_tampering_fails_closed(self):
        with patch("be_replay.linux_supervisor.run", side_effect=self.fake_supervisor(wrong_stdout_digest=True)):
            result = small.run(self.root / "run", stages=["n2-scalars"], heartbeat_seconds=1)
        self.assertFalse(result["all_selected_stages_computed"])
        self.assertFalse(result["native_arithmetic_accepted"])
        self.assertIn("stdout", result["rows"][0]["reason"])

    def test_n3_cell_digest_must_bind_its_actual_frozen_source(self):
        with patch("be_replay.linux_supervisor.run", side_effect=self.fake_supervisor(wrong_n3_digest=True)):
            with patch.object(small.shutil, "which", return_value=str(Path(small.sys.executable))):
                result = small.run(self.root / "run", stages=["n3-full"], heartbeat_seconds=1)
        self.assertFalse(result["all_selected_stages_computed"])
        self.assertIn("frozen certificate", result["rows"][0]["reason"])

    def test_native_cpp_stage_fails_closed_before_spawn(self):
        with patch("be_replay.linux_supervisor.run") as supervisor:
            result = small.run(self.root / "run", mode="native", stages=["n3-full"], heartbeat_seconds=1)
        supervisor.assert_not_called()
        self.assertFalse(result["all_selected_stages_computed"])
        self.assertEqual(result["rows"][0]["status"], "UNSUPPORTED_NATIVE_PROCESS_TREE_CONTRACT")

    def test_boolean_returncode_is_not_an_integer_success(self):
        receipt = weak_receipt()
        receipt["returncode"] = False
        with self.assertRaises(ValueError):
            small.classify("n2-scalars", receipt, output_for("n2-scalars"))

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate JSON"):
            json.loads('{"stage":"n2-scalars","stage":"n3-full"}', object_pairs_hook=small.unique)

    def test_colab_entrypoint_runs_work_and_bundles_explicit_untrusted_scope(self):
        result = {"all_selected_stages_computed": True, "all_required_stages_selected": True,
                  "native_arithmetic_accepted": False, "rows": [],
                  "status": "COMPUTED_EXACT_OUTPUTS_UNTRUSTED_GUARD"}
        with patch.object(small, "run", return_value=result) as actual_run:
            packet = small.run_colab(durable_root=self.root / "durable",
                                     work_root=self.root / "work", backup_interval=60)
        self.assertEqual(actual_run.call_count, 1)
        self.assertEqual(actual_run.call_args.kwargs["mode"], "basic")
        self.assertEqual(packet["status"]["state"], "exact_arithmetic_completed_untrusted_guard")
        self.assertFalse(packet["status"]["native_arithmetic_accepted"])
        self.assertFalse(packet["status"]["all_index_conclusion_verified"])
        self.assertTrue(Path(packet["bundle"]).is_absolute())
        with zipfile.ZipFile(packet["bundle"]) as archive:
            self.assertTrue(any(name.endswith("SESSION_RESULT.json") for name in archive.namelist()))

    def test_colab_failure_still_emits_durable_bundle(self):
        with patch.object(small, "run", side_effect=RuntimeError("fixture interrupted")):
            packet = small.run_colab(durable_root=self.root / "durable",
                                     work_root=self.root / "work", backup_interval=60)
        self.assertEqual(packet["status"]["state"], "incomplete_error")
        self.assertFalse(packet["status"]["native_arithmetic_accepted"])
        with zipfile.ZipFile(packet["bundle"]) as archive:
            self.assertTrue(any(name.endswith("ERROR.txt") for name in archive.namelist()))


if __name__ == "__main__":
    unittest.main()
