"""ZIP, scope, wait and failure fixtures; the scalar proof is always mocked."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import aux24_join as join, aux21_23, strong24_branches, aux24_evidence


class AuxiliaryJoinTests(unittest.TestCase):
    def setUp(self):
        parent = join.ROOT / "work" / "aux24-join-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.work = self.root / "work"
        self.work.mkdir()
        self.durable = self.root / "durable"
        self.scalar = dict(schema="MOCK_SCALAR_ONLY_NOT_MATHEMATICS", rho_tail_start=join.RHO[-1],
                           tail_upper="211/500", strict_tail_comparison=True)

    def packet(self, key):
        if key.startswith("auxiliary"):
            value = key[len("auxiliary"):]
            spec = aux21_23.SPECS[value]
            edges = dict(signed_rectangles=92160, allowance="299/2000") if value == "21" else dict(
                initial_signed_rectangles=spec["rectangles"], probability_panels=100,
                count_indices=spec["indices"], count_leaves=spec["leaves"])
            return dict(schema="FRESH_AUX21_23_JOB_RESULT_V1", target=value, n=spec["n"], K=spec["K"],
                        allowance=spec["allowance"], conditional_arithmetic_replayed=True, semantics_verified=True,
                        source_manifest_sha256=aux21_23.EPOCH_PINS[value], driver_sha256=join.digest(aux21_23.__file__),
                        semantic_edges=edges, predecessor_acquisition_verified=False, full_auxiliary_bound_verified=False,
                        stronger24_acquisition_verified=False, all_index_conclusion_verified=False)
        branch = key[len("stronger24-"):]
        index = int(branch[1:])
        indices, leaves = join.BRANCHES[branch]
        return dict(schema="REVALIDATED_CONDITIONAL_STRONG24_BRANCH_V1", branch=branch, n=24, K="3/10",
                    rho_interval=join.RHO[index:index+2], contact_allowance="15/46",
                    effective_contact_allowance=strong24_branches.EFFECTIVE_Q[branch],
                    predecessor_statement_sha256=join.PREDECESSOR_SHA, driver_sha256=join.digest(strong24_branches.__file__),
                    source_manifest_sha256=strong24_branches.SELECTION_SHA[branch], probability_panels=100,
                    count_indices=indices, count_forests=len(indices), count_leaves=leaves,
                    numeric_resource_to_count_interfaces_verified=True, arithmetic_computed=True,
                    native_arithmetic_accepted=False, branch_theorem_acquired=False,
                    stronger24_acquisition_verified=False, all_index_conclusion_verified=False)

    def archive(self, key, *, stamp="20261023T120000Z-a", path=None):
        folder = self.durable / key / stamp
        if key.startswith("auxiliary"):
            folder /= "bundles/abcd"
        folder.mkdir(parents=True, exist_ok=True)
        output = path or folder / (stamp + "-results.zip")
        packet = self.packet(key)
        with zipfile.ZipFile(output, "x") as z:
            z.writestr(stamp + "/task/FIXTURE_JOB.json", json.dumps(dict(key=key, validated=packet)))
            result = "JOB_RESULT.json" if key.startswith("auxiliary") else "RESULT.json"
            z.writestr(stamp + "/task/" + result, json.dumps(dict(fixture_only=True, key=key)))
        output.with_suffix(".zip.sha256").write_text(join.digest(output) + "  " + output.name + "\n", encoding="ascii")
        return output

    def validator(self, task):
        data = json.loads((Path(task) / "FIXTURE_JOB.json").read_text())
        packet = data["validated"]
        if not data["key"].startswith("auxiliary"):
            packet["result_sha256"] = join.digest(Path(task) / "RESULT.json")
        return packet

    def run_mocked(self):
        with patch.object(aux21_23, "validate_completed", side_effect=self.validator), \
             patch.object(strong24_branches, "validate_completed", side_effect=self.validator), \
             patch.object(aux24_evidence, "validate_task_transport", side_effect=lambda task, key:
                          dict(job=key, execution_transport_revalidated=True, fixture_only=True)), \
             patch.object(join, "scalar_certificate", return_value=self.scalar) as scalar, redirect_stdout(io.StringIO()):
            result = join.run(self.durable, self.work)
        return result, scalar.call_count

    def test_missing_jobs_wait_without_running_scalar_or_kernels(self):
        result, scalar_calls = self.run_mocked()
        self.assertEqual(result["status"], "WAITING_FOR_COMPLETED_JOBS")
        self.assertEqual(len(result["missing_jobs"]), 9)
        self.assertFalse(result["conditional_fresh_numeric_chain_verified"])
        self.assertEqual(scalar_calls, 0)

    def test_all_nine_complete_reports_form_only_conditional_chain(self):
        for key in join.JOBS:
            self.archive(key)
        result, scalar_calls = self.run_mocked()
        self.assertEqual(scalar_calls, 1)
        self.assertEqual(result["status"], "CONDITIONAL_FRESH_NUMERIC_CHAIN_VERIFIED")
        self.assertTrue(result["conditional_fresh_numeric_chain_verified"])
        self.assertEqual((result["count_forests"], result["count_leaves"]), (83, 76088))
        self.assertEqual(result["n25_contact_allowance"], "5/16")
        self.assertEqual(len(result["imports"]), 9)
        self.assertTrue(all(result[k] is False for k in join.FALSE_FLAGS))
        for key, row in result["imports"].items():
            self.assertEqual(row["zip_sha256"], join.digest(row["zip_path"]))
            self.assertEqual(row["validated_report_sha256"], join.digest(self.work / row["validated_report_relative"]))

    def test_newer_incomplete_zip_is_skipped_in_favour_of_valid_old_complete_evidence(self):
        old = self.archive("auxiliary21", stamp="20261023T110000Z-a")
        bad = self.archive("auxiliary21", stamp="20261023T120000Z-a")
        bad.with_suffix(".zip.sha256").write_text("0"*64 + "  " + bad.name + "\n")
        result, _ = self.run_mocked()
        self.assertEqual(result["imports"]["auxiliary21"]["zip_sha256"], join.digest(old))
        self.assertEqual(len(result["missing_jobs"]), 8)

    def test_wrong_zip_sidecar_is_rejected_before_extraction(self):
        path = self.archive("auxiliary21")
        path.with_suffix(".zip.sha256").write_text("0"*64 + "  " + path.name + "\n")
        target = self.root / "extract"
        with self.assertRaisesRegex(ValueError, "match sidecar"):
            join.extract(path, target)
        self.assertFalse(target.exists())

    def test_arithmetic_packet_without_actual_transport_cannot_enter_chain(self):
        self.archive("auxiliary21")
        with patch.object(aux21_23, "validate_completed", side_effect=self.validator), \
             patch.object(aux24_evidence, "validate_task_transport", side_effect=ValueError("Missing actual guard artifact")), \
             patch.object(join, "scalar_certificate", side_effect=AssertionError("No scalar for rejected evidence")), redirect_stdout(io.StringIO()):
            result = join.run(self.durable, self.work)
        self.assertFalse(result["conditional_fresh_numeric_chain_verified"])
        self.assertFalse(result["imports"])
        self.assertEqual(len(result["missing_jobs"]), 9)
        reasons = result["missing_jobs"][0]["reasons"]
        self.assertIn("Missing actual guard artifact", reasons[0]["reason"])

    def test_missing_sidecar_and_wrong_basename_are_not_complete_evidence(self):
        path = self.archive("auxiliary21")
        sidecar = path.with_suffix(".zip.sha256")
        sidecar.unlink()
        with self.assertRaises(ValueError):
            join.verified_zip(path)
        sidecar.write_text(join.digest(path) + "  other-results.zip\n")
        with self.assertRaisesRegex(ValueError, "basename"):
            join.verified_zip(path)

    def test_zip_path_traversal_symlink_and_duplicate_member_are_rejected(self):
        for label in ("traversal", "symlink", "duplicate"):
            with self.subTest(label=label):
                path = self.root / (label + ".zip")
                with zipfile.ZipFile(path, "x") as z:
                    if label == "traversal":
                        z.writestr("root/../outside.json", "{}")
                    elif label == "symlink":
                        info = zipfile.ZipInfo("root/task/link")
                        info.create_system = 3
                        info.external_attr = 0o120777 << 16
                        z.writestr(info, "../../elsewhere")
                    else:
                        z.writestr("root/task/A.json", "{}")
                        z.writestr("root/task/a.json", "{}")
                path.with_suffix(".zip.sha256").write_text(join.digest(path) + "  " + path.name + "\n")
                with self.assertRaises(ValueError):
                    join.extract(path, self.root / (label + "-out"))

    def test_receipt_bytes_survive_extraction_unchanged(self):
        path = self.archive("auxiliary22")
        with zipfile.ZipFile(path) as z:
            name = next(n for n in z.namelist() if n.endswith("/JOB_RESULT.json"))
            original = z.read(name)
        task, _ = join.extract(path, self.root / "restored")
        self.assertEqual((task / "JOB_RESULT.json").read_bytes(), original)

    def test_wrong_branch_rho_and_forest_census_are_rejected(self):
        packet = self.packet("stronger24-b2")
        packet["rho_interval"] = ["6/5", "7/5"]
        with self.assertRaisesRegex(ValueError, "branch, predecessor"):
            join.validate_scope("stronger24-b2", packet)
        packet = self.packet("stronger24-b2")
        packet["count_leaves"] -= 1
        with self.assertRaisesRegex(ValueError, "Every branch"):
            join.validate_scope("stronger24-b2", packet)

    def test_b4_b5_stronger_effective_allowances_keep_global_predecessor(self):
        for branch in ("b4", "b5"):
            packet = self.packet("stronger24-" + branch)
            self.assertEqual(join.validate_scope("stronger24-" + branch, packet), packet)
            self.assertNotEqual(packet["effective_contact_allowance"], packet["contact_allowance"])
            packet["contact_allowance"] = packet["effective_contact_allowance"]
            with self.assertRaises(ValueError):
                join.validate_scope("stronger24-" + branch, packet)

    def test_wrong_auxiliary_target_source_or_promotion_is_rejected(self):
        for field, value in (("allowance", "0"), ("source_manifest_sha256", "0"*64), ("full_auxiliary_bound_verified", True)):
            with self.subTest(field=field):
                packet = self.packet("auxiliary22")
                packet[field] = value
                with self.assertRaises(ValueError):
                    join.validate_scope("auxiliary22", packet)

    def test_bad_fresh_scalar_comparison_cannot_complete_chain(self):
        for key in join.JOBS:
            self.archive(key)
        self.scalar["strict_tail_comparison"] = False
        with self.assertRaisesRegex(ValueError, "tail comparison"):
            self.run_mocked()

    def test_final_bundle_exists_when_join_is_waiting(self):
        with patch.object(join, "scalar_certificate", side_effect=AssertionError("No scalar while waiting")), redirect_stdout(io.StringIO()):
            result = join.run_colab(durable_root=self.durable, work_root=self.root / "colab")
        self.assertEqual(result["status"]["state"], "WAITING_FOR_COMPLETED_JOBS")
        self.assertTrue(Path(result["bundle"]).is_file())

    def test_join_error_still_writes_error_bundle_and_false_acquisition_flags(self):
        with patch.object(join, "run", side_effect=ValueError("fixture failure")), redirect_stdout(io.StringIO()):
            result = join.run_colab(durable_root=self.durable, work_root=self.root / "colab")
        self.assertEqual(result["status"]["state"], "PARTIAL_ERROR_NOT_ACCEPTED")
        self.assertFalse(result["status"]["stronger24_acquisition_verified"])
        with zipfile.ZipFile(result["bundle"]) as z:
            self.assertTrue(any(n.endswith("/ERROR.txt") for n in z.namelist()))


if __name__ == "__main__":
    unittest.main()
