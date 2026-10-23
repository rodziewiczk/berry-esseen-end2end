"""Small source/geometry/supervisor fixtures; no mathematical evaluator or download."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch

from be_replay import count_task as count


class CountTaskTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.task = self.root / "task"
        self.capsule = self.task / "capsule"
        self.capsule.mkdir(parents=True)
        # This protocol is NEVER executed. It exists only for AST/source-binding fixtures.
        (self.capsule / "count_protocol.py").write_text(
            "def header(bound):return dict(schema='FIXTURE_FULL_ROOTS_V1',n=25,index=33)\n", encoding="utf-8")
        (self.capsule / "contract.json").write_text('{"rows": []}\n', encoding="utf-8")
        (self.capsule / "kernel.py").write_text("raise AssertionError('fixture must never execute')\n", encoding="utf-8")
        self.manifest = {"kernel.py": count.digest(self.capsule / "kernel.py")}
        count.write(self.capsule / "KERNEL_COPY_MANIFEST.json", {"files": self.manifest})
        files = {path.name: count.digest(path) for path in self.capsule.iterdir()}
        count.write(self.capsule / "FROZEN_DESIGN.json", {"files": files})
        self.pin = count.digest(self.capsule / "FROZEN_DESIGN.json")
        self.targets = dict(count.TARGETS, **{"b3-p33": ("original-v12", 33, self.pin)})
        self.target_patch = patch.object(count, "TARGETS", self.targets)
        self.target_patch.start()
        count.write(self.task / "TASK.json", dict(schema="COUNT_TASK_V1", target="b3-p33",
                                                   source_commit=count.COMMIT, design_sha256=self.pin))

    def tearDown(self):
        self.target_patch.stop()
        self.temporary.cleanup()

    def header(self):
        return count.native_header(self.capsule, "b3-p33")

    def checkpoint(self):
        return dict(schema="UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1", arithmetic_accepted=False,
                    binding=dict(design_sha256=self.pin, alpha_priority="4", native_header=self.header()),
                    roots=[dict(k=k, tree={"kind": "pending"}) for k in range(26)])

    def forest(self):
        return dict(**self.header(), roots=[dict(k=k, tree=dict(kind="leaf", box=[],
                                                               decision="FIXTURE_ONLY", result={})) for k in range(26)])

    def receipt(self, capsule):
        return dict(status="PASS_FRESH_CONDITIONAL_EXACT_COUNT33", fresh_leaf_evaluations=26,
                    negative_controls=["control-" + str(i) for i in range(24)],
                    statistics=dict(nodes=26, leaves=26),
                    forest_sha256=count.digest(capsule / "COUNT33_FOREST.json"),
                    contract_sha256=count.digest(capsule / "contract.json"),
                    checker_sha256=count.digest(capsule / "count_protocol.py"), kernel_sha256=self.manifest)

    def observed(self, output, packet=None, status="completed", returncode=0, native_script=None):
        output.mkdir(parents=True)
        stdout, stderr = output / "stdout.txt", output / "stderr.txt"
        stdout.write_text(json.dumps(packet or {}) + "\n", encoding="utf-8")
        stderr.write_text("", encoding="utf-8")
        guard = "TEST_FIXTURE_NO_MATH"
        if native_script is not None:
            guard = dict(kind="LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1", capability_established=True,
                         native_python_execution=True, hard_sum_RLIMIT_AS_bytes=512 * count.MIB,
                         worker_RLIMIT_AS_bytes=448 * count.MIB, supervisor_RLIMIT_AS_bytes=64 * count.MIB,
                         hard_sum_RLIMIT_CPU_seconds=7200, script_sha256=count.digest(native_script))
        return dict(status=status, returncode=returncode, stdout_path=str(stdout), stderr_path=str(stderr),
                    elapsed_seconds=0.001, guard_scope=guard)

    def test_exact_frozen_vendor_sources_are_present(self):
        result = count.verify_vendor()
        self.assertEqual(result["commit"], "75a94708872e2bc053f42a279559b23ed91e4402")
        self.assertEqual(len(result["files_sha256"]), 3)
        fake = self.root / "vendor"
        fake.mkdir()
        for name in count.VENDOR_PINS:
            (fake / name).write_text("corrupt", encoding="utf-8")
        with self.assertRaises(ValueError):
            count.verify_vendor(fake)

    def test_seven_targets_keep_distinct_original_and_new_conditional_epochs(self):
        self.assertEqual(len(count.TARGETS), 7)
        self.assertEqual(sum(row[0] == "original-v12" for row in count.TARGETS.values()), 5)
        self.assertEqual(sum(row[0] == "new-conditional-v14" for row in count.TARGETS.values()), 2)
        self.assertEqual(len({row[2] for row in count.TARGETS.values()}), 7)
        for target in count.TARGETS:
            command = count.preparation_command(target, Path("archives"), Path("new-capsule"))
            self.assertEqual(command[1:3], ["-B", "-S"])
            if target.endswith("-new"):
                self.assertEqual(Path(command[3]).name, "prepare_v14_portable.py")
                self.assertIn("--base13-archive", command)
                self.assertIn("NOT_HISTORICAL", count.scope(target))
            else:
                self.assertEqual(Path(command[3]).name, "prepare_missing_count.py")

    def test_duplicate_metadata_and_corrupt_asset_are_rejected(self):
        path = self.root / "bad.json"
        path.write_text('{"roots":[],"roots":[]}', encoding="utf-8")
        with self.assertRaises(ValueError):
            count.read(path)
        asset = dict(name="fixed.zip", bytes=3, sha256=hashlib.sha256(b"abc").hexdigest())
        path = self.root / "fixed.zip"
        path.write_bytes(b"abd")
        with self.assertRaises(ValueError):
            count.verify_asset(path, asset)

    def test_child_failure_displays_actual_stderr_and_exit_reason_without_acceptance(self):
        observed = self.observed(self.root / "failed-execution", status="incomplete", returncode=1)
        observed["reason"] = "nonzero_subprocess_exit"
        Path(observed["stderr_path"]).write_text("Missing case-sensitive input: ORIGINAL_V12_CONTRACT.json\n",
                                                 encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Missing case-sensitive input") as error:
            count.final_packet(observed)
        self.assertIn("nonzero_subprocess_exit", str(error.exception))
        self.assertIn('"returncode": 1', str(error.exception))
        self.assertIn("preserved output is not acceptance", str(error.exception))

    def test_child_failure_diagnostics_use_only_bounded_stderr_tail(self):
        observed = self.observed(self.root / "long-stderr", status="incomplete", returncode=-9)
        Path(observed["stderr_path"]).write_bytes(b"do-not-repeat-entire-log\n" + b"x" * 10000 + b"\nactual final failure")
        details = count.execution_diagnostics(observed)
        self.assertLessEqual(len(details["stderr_tail"]), 8192)
        self.assertTrue(details["stderr_tail"].endswith("actual final failure"))
        self.assertNotIn("do-not-repeat-entire-log", details["stderr_tail"])

    def test_child_failure_keeps_exit_reason_when_stderr_is_missing(self):
        observed = dict(status="incomplete", reason="external_wall_timeout", returncode=-9,
                        stderr_path=str(self.root / "missing-stderr.txt"))
        with self.assertRaisesRegex(ValueError, "external_wall_timeout"):
            count.final_packet(observed)

    def test_capsule_rehash_detects_native_or_contract_change(self):
        count.verify_capsule("b3-p33", self.capsule)
        with (self.capsule / "contract.json").open("a", encoding="utf-8") as stream:
            stream.write(" ")
        with self.assertRaises(ValueError):
            count.verify_capsule("b3-p33", self.capsule)

    def test_untrusted_checkpoint_requires_every_root_and_native_source_binding(self):
        value = self.checkpoint()
        count.check_checkpoint(value, "b3-p33", self.capsule)
        changes = [lambda x: x["roots"].pop(), lambda x: x["roots"][0].update(k=False),
                   lambda x: x.update(arithmetic_accepted=True),
                   lambda x: x["binding"].update(design_sha256="0" * 64),
                   lambda x: x["binding"]["native_header"].update(checker_sha256="0" * 64)]
        for change in changes:
            bad = deepcopy(value)
            change(bad)
            with self.subTest(change=change), self.assertRaises(ValueError):
                count.check_checkpoint(bad, "b3-p33", self.capsule)

    def test_copy_resume_preserves_primary_and_backup_bytes(self):
        source = self.root / "CHECKPOINT.json"
        backup = source.with_suffix(".backup.json")
        source.write_text("{broken write", encoding="utf-8")
        count.write(backup, self.checkpoint())
        destination = self.root / "resume"
        destination.mkdir()
        result = count.copy_resume(source, "b3-p33", self.capsule, destination)
        self.assertEqual(result.read_bytes(), source.read_bytes())
        self.assertEqual((destination / "resume.backup.json").read_bytes(), backup.read_bytes())

    def test_complete_candidate_remains_untrusted_until_canonical_accept(self):
        self.assertEqual(count.forest_census(self.forest(), "b3-p33", self.capsule), dict(nodes=26, leaves=26, roots=26))
        for change in (lambda x: x["roots"].pop(), lambda x: x["roots"][1].update(k=0),
                       lambda x: x["roots"][0].update(tree={"kind": "pending"})):
            bad = self.forest()
            change(bad)
            with self.assertRaises(ValueError):
                count.forest_census(bad, "b3-p33", self.capsule)

    def test_search_executes_only_frozen_discovery_and_never_promotes_complete_candidate(self):
        calls = []
        def fake(argv, **options):
            calls.append((argv, options))
            return self.observed(options["output_dir"], dict(status="CANDIDATE_COMPLETE_NOT_ACCEPTED",
                                 arithmetic_accepted=False, nodes=26, leaves=26, pending=0))
        with patch.object(count, "supervise", side_effect=fake):
            result = count.search(self.task, seconds=1, wall_seconds=2)
        self.assertFalse(result["arithmetic_accepted"])
        self.assertFalse(result["native_acceptance_run"])
        self.assertEqual(len(calls), 1)
        self.assertEqual(Path(calls[0][0][3]).name, "count_discovery.py")
        self.assertEqual(calls[0][1]["mode"], "untrusted_search")
        self.assertEqual(len(calls[0][1]["checkpoint_paths"]), 2)

    def test_search_cannot_return_native_accepted_status(self):
        def fake(argv, **options):
            return self.observed(options["output_dir"], dict(status="NATIVE_COUNT_ACCEPTED", arithmetic_accepted=True))
        with patch.object(count, "supervise", side_effect=fake), self.assertRaises(ValueError):
            count.search(self.task, seconds=1, wall_seconds=2)

    def test_portable_v14_starts_fresh_without_importing_incompatible_published_hints(self):
        calls = []
        def fake(argv, **options):
            calls.append(argv)
            return self.observed(options["output_dir"], dict(status="SEARCH_CHECKPOINTED_INCOMPLETE",
                                 arithmetic_accepted=False, nodes=26, leaves=0, pending=26))
        with patch.object(count, "load_task", return_value=(self.task, "b3-p31-v14-new")), \
             patch.object(count, "verify_capsule"), \
             patch.object(count, "supervise", side_effect=fake), \
             patch.object(count, "obtain_asset") as download, \
             patch.object(count, "extract_published_hint") as hints:
            result = count.search(self.task, seconds=1, wall_seconds=2,
                                  published_hints=True, archives=self.root / "unused-cache")
        download.assert_not_called()
        hints.assert_not_called()
        self.assertNotIn("--resume", calls[0])
        self.assertIn(count.TARGETS["b3-p31-v14-new"][2], calls[0])
        self.assertFalse(result["arithmetic_accepted"])

    def test_native_success_requires_separate_guarded_original_accept_and_full_receipt(self):
        candidate = self.root / "candidate.json"
        count.write(candidate, self.forest())
        calls = []
        def fake(argv, **options):
            calls.append((argv, options))
            capsule = Path(options["cwd"])
            count.write(capsule / "COUNT33_ACCEPTED.json", self.receipt(capsule))
            return self.observed(options["output_dir"], native_script=capsule / "count_protocol.py")
        with patch.object(count, "supervise", side_effect=fake):
            result = count.accept(self.task, candidate)
        self.assertTrue(result["arithmetic_accepted"])
        self.assertFalse(result["parent_acquisitions_verified"])
        self.assertFalse(result["all_index_conclusion_verified"])
        self.assertEqual(calls[0][0][-1], "accept")
        self.assertEqual(Path(calls[0][0][3]).name, "count_protocol.py")
        self.assertEqual(calls[0][1]["mode"], "trusted_native")
        self.assertFalse((self.capsule / "COUNT33_ACCEPTED.json").exists())

    def test_unsupported_native_guard_fails_closed_without_search_fallback(self):
        candidate = self.root / "candidate.json"
        count.write(candidate, self.forest())
        modes = []
        def fake(argv, **options):
            modes.append(options["mode"])
            return self.observed(options["output_dir"], status="unsupported", returncode=None)
        with patch.object(count, "supervise", side_effect=fake), self.assertRaises(ValueError):
            count.accept(self.task, candidate)
        self.assertEqual(modes, ["trusted_native"])
        self.assertEqual(list(self.task.glob("accept-*/NATIVE_ACCEPTED.json")), [])

    def test_completed_child_without_established_native_contract_is_not_accepted(self):
        candidate = self.root / "candidate.json"
        count.write(candidate, self.forest())
        def fake(argv, **options):
            capsule = Path(options["cwd"])
            count.write(capsule / "COUNT33_ACCEPTED.json", self.receipt(capsule))
            # Even a perfectly shaped receipt and exit0 cannot promote the
            # weaker discovery resource contract to native acceptance.
            return self.observed(options["output_dir"])
        with patch.object(count, "supervise", side_effect=fake), self.assertRaisesRegex(ValueError, "platform contract"):
            count.accept(self.task, candidate)
        self.assertEqual(list(self.task.glob("accept-*/NATIVE_ACCEPTED.json")), [])

    def test_rehashed_receipt_still_requires_all_controls_and_every_fresh_leaf(self):
        capsule = self.capsule
        count.write(capsule / "COUNT33_FOREST.json", self.forest())
        census = dict(nodes=26, leaves=26, roots=26)
        good = self.receipt(capsule)
        count.validate_native(good, "b3-p33", capsule, census)
        for change in (lambda x: x.update(fresh_leaf_evaluations=25),
                       lambda x: x.update(fresh_leaf_evaluations=True),
                       lambda x: x["negative_controls"].__setitem__(1, x["negative_controls"][0]),
                       lambda x: x.update(forest_sha256="0" * 64),
                       lambda x: x["statistics"].update(nodes=25),
                       lambda x: x.update(kernel_sha256={})):
            bad = deepcopy(good)
            change(bad)
            with self.subTest(change=change), self.assertRaises(ValueError):
                count.validate_native(bad, "b3-p33", capsule, census)

    def test_durable_progress_and_bundle_preserve_both_checkpoints_and_sources(self):
        candidate = self.task / "search-fixture" / "candidate"
        candidate.mkdir(parents=True)
        count.write(candidate / "CHECKPOINT.json", self.checkpoint())
        (candidate / "CHECKPOINT.backup.json").write_bytes((candidate / "CHECKPOINT.json").read_bytes())
        count.event(self.task, "fixture_partial", nodes=26, leaves=0, pending=26, arithmetic_accepted=False)
        value = json.loads((self.task / "progress.jsonl").read_text(encoding="utf-8"))
        self.assertEqual(value["pending"], 26)
        self.assertFalse(value["all_index_conclusion_verified"])
        exported = count.bundle_task(self.task)
        self.assertTrue(exported["transport_is_not_arithmetic_acceptance"])
        with zipfile.ZipFile(exported["path"]) as zipped:
            self.assertIn("task/search-fixture/candidate/CHECKPOINT.json", zipped.namelist())
            self.assertIn("task/search-fixture/candidate/CHECKPOINT.backup.json", zipped.namelist())
            self.assertIn("task/capsule/count_protocol.py", zipped.namelist())
            manifest = json.loads(zipped.read("BUNDLE_MANIFEST.json"))
            for row in manifest["files"]:
                self.assertEqual(hashlib.sha256(zipped.read(row["path"])).hexdigest(), row["sha256"])
            self.assertTrue(manifest["transport_is_not_arithmetic_acceptance"])


if __name__ == "__main__":
    unittest.main()
