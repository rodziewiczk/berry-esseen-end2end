"""Synthetic orchestration/cache fixtures; no archived mathematical execution."""
from copy import deepcopy
import io
import json
from pathlib import Path
import shutil
import stat
import tempfile
from types import SimpleNamespace
import unittest
import warnings
import zipfile
import zlib
from unittest.mock import patch

from be_replay import retained_n25 as runner


class QuietBackups:
    def __init__(self, *unused, **options):
        self.active = None

    def start(self):
        pass

    def set_active(self, epoch):
        self.active = epoch

    def save(self):
        return 0

    def close(self):
        pass


class RetainedRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.task = self.root/"task"
        self.task.mkdir()
        self.job = self.job_for(37)
        self.cache = self.root/"cache"
        self.validations = []
        self.native_calls = []

    def tearDown(self):
        self.temporary.cleanup()

    def job_for(self, index):
        identity = "b0-p"+str(index)
        return dict(job_id=identity, target_id=identity, branch="b0", index=index,
                    leaf_count=26, capsule_relative="capsules/"+identity,
                    forest_filename=f"COUNT{index}_FOREST.json",
                    acceptance_filename=f"COUNT{index}_ACCEPTED.json")

    def source(self, task, job):
        capsule = Path(task)/job["capsule_relative"]
        capsule.mkdir(parents=True, exist_ok=True)
        payload = {"count_protocol.py": b"raise AssertionError('fixture native source must never execute')\n",
                   "contract.json": b'{"fixture":"conditional input"}\n',
                   job["forest_filename"]: b'{"fixture":"untrusted candidate"}\n'}
        for name, raw in payload.items():
            (capsule/name).write_bytes(raw)
        return capsule

    def manifest(self, task, jobs):
        rows = []
        for job in jobs:
            capsule = Path(task)/job["capsule_relative"]
            rows.append(dict(job_id=job["job_id"], files=[dict(filename=p.name,
                sha256=runner.common.digest(p), bytes=p.stat().st_size)
                for p in sorted(capsule.iterdir())]))
        return dict(branch="b0", jobs=rows)

    def make_epoch(self, task=None, job=None, name="accept-0123456789ab"):
        task, job = Path(task or self.task), job or self.job
        source = self.source(task, job)
        epoch = task/name
        shutil.copytree(source, epoch/"capsule")
        execution = epoch/"execution"
        execution.mkdir()
        receipt = epoch/"capsule"/job["acceptance_filename"]
        receipt.write_text(json.dumps(dict(status="MOCK_FRESH_SCOPED", job_id=job["job_id"]))+"\n")
        (execution/"stdout.txt").write_bytes(receipt.read_bytes())
        (execution/"stderr.txt").write_bytes(b"")
        observed = dict(status="completed", returncode=0, proof_accepted=False)
        runner.atomic_json(execution/"supervisor-result.json", observed)
        before = dict(job_id=job["job_id"], arithmetic_accepted=False, observed=observed,
                      parent_acquisitions_verified=False, all_index_conclusion_verified=False)
        runner.atomic_json(epoch/"NATIVE_OBSERVED.json", before)
        runner.atomic_json(epoch/"NATIVE_ACCEPTED.json", dict(before, arithmetic_accepted=True,
            native_receipt=str(receipt), native_receipt_sha256=runner.common.digest(receipt)))
        return epoch

    def validate(self, task, job, epoch):
        """A mock evidence boundary that actually checks preserved fixture bytes."""
        task, epoch = Path(task), Path(epoch)
        self.validations.append((task, job["job_id"], epoch))
        before = runner.common.read(epoch/"NATIVE_OBSERVED.json")
        after = runner.common.read(epoch/"NATIVE_ACCEPTED.json")
        runner.common.need(before["arithmetic_accepted"] is False and after["arithmetic_accepted"] is True,
                           "Mock validates the observed-to-accepted transition")
        runner.common.need(before["job_id"] == after["job_id"] == job["job_id"], "Mock exact job")
        receipt = epoch/"capsule"/job["acceptance_filename"]
        runner.common.need(after["native_receipt_sha256"] == runner.common.digest(receipt), "Mock receipt hash")
        runner.common.need((epoch/"execution/stdout.txt").read_bytes() == receipt.read_bytes()
                           and (epoch/"execution/stderr.txt").read_bytes() == b"", "Mock exact captures")
        for source in (task/job["capsule_relative"]).iterdir():
            runner.common.need((epoch/"capsule"/source.name).read_bytes() == source.read_bytes(),
                               "Mock full source and candidate clone")
        return dict(schema="MOCK_FULL_EVIDENCE_VALIDATOR_RESULT", job_id=job["job_id"],
                    native_arithmetic_accepted=True, parent_acquisitions_verified=False,
                    all_index_conclusion_verified=False)

    def zip_rows(self, names):
        output = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(output, "w") as zipped:
                for name in names:
                    zipped.writestr(name, b"{}\n")
        output.seek(0)
        return zipfile.ZipFile(output)

    def test_cache_preflight_rejects_traversal_duplicates_and_extra_paths(self):
        epoch = "accept-0123456789ab"
        good = [epoch+"/NATIVE_OBSERVED.json", epoch+"/NATIVE_ACCEPTED.json"]
        extras = [epoch+"/../../escape", "/absolute/file",
                  epoch+"/capsule/C:bad", epoch+"/capsule/../bad", epoch+"/other.json",
                  epoch+"/capsule/nested/bad", good[0], good[0].upper()]
        for extra in extras:
            with self.subTest(extra=extra), self.zip_rows(good+[extra]) as zipped:
                with self.assertRaises(ValueError):
                    runner._cache_members(zipped)
        # Windows ZipInfo construction normalizes backslashes before writing;
        # feed the actual untrusted central-directory name to the preflight.
        bad = zipfile.ZipInfo(epoch+"/capsule/x.py")
        bad.filename = epoch+"\\capsule\\x.py"
        bad.file_size = 1
        with self.assertRaises(ValueError):
            runner._cache_members(SimpleNamespace(infolist=lambda: [bad]))

    def test_cache_preflight_requires_both_ledgers_and_one_epoch(self):
        for names in (["accept-0123456789ab/capsule/file.py"],
                      ["accept-0123456789ab/NATIVE_ACCEPTED.json"],
                      ["accept-0123456789ab/NATIVE_OBSERVED.json", "accept-abcdefabcdef/NATIVE_ACCEPTED.json"]):
            with self.subTest(names=names), self.zip_rows(names) as zipped:
                with self.assertRaises(ValueError):
                    runner._cache_members(zipped)

    def test_cache_preflight_rejects_symlink_oversize_and_large_inventory(self):
        names = ["accept-0123456789ab/NATIVE_OBSERVED.json", "accept-0123456789ab/NATIVE_ACCEPTED.json"]
        with self.zip_rows(names) as zipped:
            rows = zipped.infolist()
        rows[0].external_attr = (stat.S_IFLNK | 0o777) << 16
        with self.assertRaises(ValueError):
            runner._cache_members(SimpleNamespace(infolist=lambda: rows))
        rows[0].external_attr = (stat.S_IFREG | 0o600) << 16
        rows[0].file_size = 128*runner.MIB+1
        with self.assertRaises(ValueError):
            runner._cache_members(SimpleNamespace(infolist=lambda: rows))
        rows[0].file_size = 3
        with patch.object(runner, "MAX_CACHE_BYTES", 5):
            with self.assertRaisesRegex(ValueError, "bounded complete"):
                runner._cache_members(SimpleNamespace(infolist=lambda: rows))
        with patch.object(runner, "MAX_CACHE_FILES", 1):
            with self.assertRaisesRegex(ValueError, "inventory"):
                runner._cache_members(SimpleNamespace(infolist=lambda: rows))

    def test_save_restore_revalidates_and_preserves_original_receipt_bytes(self):
        epoch = self.make_epoch()
        originals = {p.relative_to(epoch): p.read_bytes() for p in epoch.rglob("*") if p.is_file()}
        restored_task = self.root/"restored"
        self.source(restored_task, self.job)
        with patch.object(runner.evidence, "validate_stage", side_effect=self.validate) as checked:
            output = runner.save_stage(self.task, self.job, epoch, self.cache)
            self.assertEqual(output.with_suffix(".zip.sha256").read_text("ascii"),
                             runner.common.digest(output)+"  "+output.name+"\n")
            restored = runner.restore_stage(restored_task, self.job, self.cache)
            self.assertIsNotNone(restored)
            self.assertEqual(checked.call_count, 2)
            self.assertEqual(restored[1]["job_id"], self.job["job_id"])
        for relative, raw in originals.items():
            self.assertEqual((restored[0]/relative).read_bytes(), raw)

    def test_failed_validation_never_exports_stage(self):
        epoch = self.make_epoch()
        with patch.object(runner.evidence, "validate_stage", side_effect=ValueError("mock guard failure")):
            with self.assertRaisesRegex(ValueError, "guard failure"):
                runner.save_stage(self.task, self.job, epoch, self.cache)
        self.assertFalse(self.cache.exists())

    def test_wrong_zip_sha_cannot_reach_evidence_or_extraction(self):
        epoch = self.make_epoch()
        with patch.object(runner.evidence, "validate_stage", side_effect=self.validate):
            output = runner.save_stage(self.task, self.job, epoch, self.cache)
        output.with_suffix(".zip.sha256").write_text("0"*64+"  "+output.name+"\n")
        restored_task = self.root/"restored"
        self.source(restored_task, self.job)
        with patch.object(runner.evidence, "validate_stage") as checked:
            self.assertIsNone(runner.restore_stage(restored_task, self.job, self.cache))
            checked.assert_not_called()
        self.assertFalse((restored_task/epoch.name).exists())

    def test_resigned_zip_with_mutated_receipt_is_rejected_by_evidence(self):
        epoch = self.make_epoch()
        with patch.object(runner.evidence, "validate_stage", side_effect=self.validate):
            output = runner.save_stage(self.task, self.job, epoch, self.cache)
        with zipfile.ZipFile(output) as zipped:
            rows = [(i.filename, zipped.read(i)) for i in zipped.infolist()]
        with zipfile.ZipFile(output, "w") as zipped:
            for name, raw in rows:
                zipped.writestr(name, b'{"tampered":true}\n' if name.endswith(self.job["acceptance_filename"]) else raw)
        output.with_suffix(".zip.sha256").write_text(runner.common.digest(output)+"  "+output.name+"\n")
        restored_task = self.root/"restored"
        self.source(restored_task, self.job)
        with patch.object(runner.evidence, "validate_stage", side_effect=self.validate) as checked:
            self.assertIsNone(runner.restore_stage(restored_task, self.job, self.cache))
            self.assertEqual(checked.call_count, 1)

    def test_decompression_failure_rejects_cache_without_aborting_batch(self):
        epoch = self.make_epoch()
        with patch.object(runner.evidence, "validate_stage", side_effect=self.validate):
            runner.save_stage(self.task, self.job, epoch, self.cache)
        restored_task = self.root/"restored"
        self.source(restored_task, self.job)
        with patch.object(zipfile.ZipFile, "open", side_effect=zlib.error("synthetic malformed stream")), \
             patch.object(runner.evidence, "validate_stage") as checked:
            self.assertIsNone(runner.restore_stage(restored_task, self.job, self.cache))
            checked.assert_not_called()

    def test_unsafe_cache_is_preflighted_before_any_extraction(self):
        self.cache.mkdir()
        output = self.cache/"accept-0123456789ab-native.zip"
        with zipfile.ZipFile(output, "w") as zipped:
            zipped.writestr("accept-0123456789ab/NATIVE_OBSERVED.json", "{}")
            zipped.writestr("accept-0123456789ab/NATIVE_ACCEPTED.json", "{}")
            zipped.writestr("accept-0123456789ab/capsule/../../escape", "bad")
        output.with_suffix(".zip.sha256").write_text(runner.common.digest(output)+"  "+output.name+"\n")
        with patch.object(runner.evidence, "validate_stage") as checked:
            self.assertIsNone(runner.restore_stage(self.task, self.job, self.cache))
            checked.assert_not_called()
        self.assertEqual(list(self.task.iterdir()), [])

    def setup_batch(self, *, stop_on=None):
        jobs = [self.job_for(37), self.job_for(38)]
        def prepare(branch, archive, task):
            Path(task).mkdir(parents=True)
            for job in jobs:
                self.source(task, job)
            runner.atomic_json(Path(task)/"SOURCES.json", self.manifest(task, jobs))
            runner.atomic_json(Path(task)/"SOURCE_PREPARATION.json", {"fixture": True})
            return self.manifest(task, jobs)
        def supervise(argv, **options):
            self.native_calls.append((argv, options))
            self.assertEqual(options["mode"], "trusted_native")
            self.assertEqual(options["memory_bytes"], 2*1024**3)
            self.assertEqual(options["cpu_seconds"], 43200)
            capsule, execution = Path(argv[3]).parent, Path(options["output_dir"])
            execution.mkdir()
            if stop_on is not None and len(self.native_calls) == stop_on:
                (execution/"stdout.txt").write_text("")
                (execution/"stderr.txt").write_text("synthetic bounded stop\n")
                return dict(status="incomplete", returncode=1, proof_accepted=False)
            candidate = next(capsule.glob("COUNT*_FOREST.json"))
            receipt = capsule/candidate.name.replace("_FOREST", "_ACCEPTED")
            receipt.write_text(json.dumps(dict(status="MOCK_FRESH_SCOPED", index=int(candidate.name[5:7])))+"\n")
            (execution/"stdout.txt").write_bytes(receipt.read_bytes())
            (execution/"stderr.txt").write_bytes(b"")
            observed = dict(status="completed", returncode=0, proof_accepted=False)
            runner.atomic_json(execution/"supervisor-result.json", observed)
            return observed
        def validate_run(task, job, epoch, observed, census):
            before = runner.common.read(Path(epoch)/"NATIVE_OBSERVED.json")
            self.assertIs(before["arithmetic_accepted"], False)
            self.assertFalse((Path(epoch)/"NATIVE_ACCEPTED.json").exists())
            runner.common.need(observed["status"] == "completed" and type(observed["returncode"]) is int
                               and observed["returncode"] == 0, "Mock bounded native execution")
            runner.common.need((Path(epoch)/"capsule"/job["acceptance_filename"]).is_file(), "Mock fresh native receipt")
            receipt = runner.common.read(Path(epoch)/"capsule"/job["acceptance_filename"])
            runner.common.need(receipt["status"] == "MOCK_FRESH_SCOPED", "Mock complete fresh receipt")
        patches = [patch.object(runner.sources, "jobs", return_value=deepcopy(jobs)),
            patch.object(runner.sources, "prepare", side_effect=prepare),
            patch.object(runner.sources, "verify", side_effect=lambda task: self.manifest(task, jobs)),
            patch.object(runner.sources, "census", return_value=dict(roots=26, nodes=26, leaves=26)),
            patch.object(runner.common, "obtain_asset", return_value=self.root/"fixture-archive.zip"),
            patch.object(runner.common, "supervise", side_effect=supervise),
            patch.object(runner.evidence, "validate_run", side_effect=validate_run),
            patch.object(runner.evidence, "validate_stage", side_effect=self.validate),
            patch.object(runner.evidence, "implementation", return_value={"fixture": True}),
            patch.object(runner.evidence, "premises", return_value=["Explicit conditional fixture premise"]),
            patch.object(runner, "LogBackups", QuietBackups),
            patch("be_replay.environment.snapshot", return_value={"fixture": True}),
            patch("builtins.print")]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        return jobs

    def run_batch(self, folder):
        return runner.run_colab("b0", durable_root=self.root/"drive", work_root=self.root/folder,
                                archives=self.root/"archives")

    def test_two_job_batch_saves_each_stage_and_resume_calls_no_native(self):
        jobs = self.setup_batch()
        first = self.run_batch("first")
        self.assertEqual(first["status"]["state"], "selected_retained_count_arithmetic_accepted")
        self.assertEqual(first["status"]["completed_jobs"], 2)
        self.assertEqual(first["status"]["new_native_calls"], 2)
        self.assertEqual(len(self.native_calls), 2)
        for job in jobs:
            cache = self.root/"drive/n25-retained-b0/completed"/job["job_id"]
            self.assertEqual(len(list(cache.glob("*-native.zip"))), 1)
            self.assertEqual(len(list(cache.glob("*-native.zip.sha256"))), 1)
        second = self.run_batch("second")
        self.assertEqual(second["status"]["new_native_calls"], 0)
        self.assertEqual(second["status"]["reused_completed_stages"], 2)
        self.assertEqual(len(self.native_calls), 2)
        self.assertTrue(all(stage["reused"] for stage in second["status"]["stages"]))
        self.assertTrue(Path(second["bundle"]).is_file())
        for field in ("parent_acquisitions_verified", "full_n25_verified", "all_index_conclusion_verified"):
            self.assertIs(first["status"][field], False)
            self.assertIs(second["status"][field], False)

    def test_accept_writes_false_observation_before_validation_then_true_acceptance(self):
        jobs = self.setup_batch()
        for job in jobs:
            self.source(self.task, job)
        callbacks = []
        epoch, checked = runner.accept(self.task, jobs[0], on_epoch=callbacks.append)
        before = runner.common.read(epoch/"NATIVE_OBSERVED.json")
        after = runner.common.read(epoch/"NATIVE_ACCEPTED.json")
        self.assertIs(before["arithmetic_accepted"], False)
        self.assertIs(after["arithmetic_accepted"], True)
        self.assertEqual(callbacks, [epoch])
        self.assertEqual(checked["job_id"], jobs[0]["job_id"])
        self.assertEqual(len(self.native_calls), 1)
        self.assertEqual(after["native_receipt_sha256"], runner.common.digest(epoch/"capsule"/jobs[0]["acceptance_filename"]))

    def test_accept_native_failure_never_creates_accepted_ledger(self):
        jobs = self.setup_batch(stop_on=1)
        for job in jobs:
            self.source(self.task, job)
        with self.assertRaisesRegex(ValueError, "bounded native"):
            runner.accept(self.task, jobs[0])
        epochs = list(self.task.glob("accept-*"))
        self.assertEqual(len(epochs), 1)
        self.assertIs(runner.common.read(epochs[0]/"NATIVE_OBSERVED.json")["arithmetic_accepted"], False)
        self.assertFalse((epochs[0]/"NATIVE_ACCEPTED.json").exists())

    def test_accept_malformed_fresh_receipt_never_creates_accepted_ledger(self):
        jobs = self.setup_batch()
        for job in jobs:
            self.source(self.task, job)
        working_native = runner.common.supervise.side_effect
        def malformed(argv, **options):
            observed = working_native(argv, **options)
            capsule = Path(argv[3]).parent
            (capsule/jobs[0]["acceptance_filename"]).write_bytes(b"{malformed fresh receipt")
            return observed
        runner.common.supervise.side_effect = malformed
        with self.assertRaises(ValueError):
            runner.accept(self.task, jobs[0])
        epoch = next(self.task.glob("accept-*"))
        self.assertIs(runner.common.read(epoch/"NATIVE_OBSERVED.json")["arithmetic_accepted"], False)
        self.assertFalse((epoch/"NATIVE_ACCEPTED.json").exists())

    def test_incomplete_second_stage_preserves_first_cache_and_final_bundle(self):
        jobs = self.setup_batch(stop_on=2)
        result = self.run_batch("incomplete")
        status = result["status"]
        self.assertEqual(status["state"], "incomplete_error")
        self.assertEqual(status["completed_jobs"], 1)
        self.assertEqual(status["completed_leaves"], 26)
        self.assertEqual(len(status["stages"]), 1)
        self.assertEqual(status["stages"][0]["job_id"], jobs[0]["job_id"])
        cache_root = self.root/"drive/n25-retained-b0/completed"
        self.assertEqual(len(list((cache_root/jobs[0]["job_id"]).glob("*-native.zip"))), 1)
        self.assertFalse((cache_root/jobs[1]["job_id"]).exists())
        self.assertTrue(Path(result["bundle"]).is_file())
        with zipfile.ZipFile(result["bundle"]) as zipped:
            self.assertTrue(any(name.endswith("ERROR.txt") for name in zipped.namelist()))
        for field in ("native_arithmetic_accepted", "parent_acquisitions_verified", "full_n25_verified", "all_index_conclusion_verified"):
            self.assertIs(status[field], False)


if __name__ == "__main__":
    unittest.main()
