"""Independent attacks on local COUNT completion and authenticated resume.

One real construction/acceptance seeds the cache tests. No historical forest,
synthetic success receipt or mocked numerical verifier seeds that baseline.
The local HMAC is an execution trust boundary, never a Lean proof.
Operational/HMAC mutations reuse that actual runtime fingerprint to avoid
rehashing 1833 unchanged files per mutation; the clean resume also reads the
real runtime. These controls do not claim to test hostile runtime replacement.
"""
from __future__ import annotations

from contextlib import closing, nullcontext
import copy
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import unittest
from unittest import mock

from be import count_native as native
from be import count_runner as runner
from be.authority import LocalAuthority
from be.codec import digest
from be.errors import ProtocolError
from be.ledger import SQLiteLedger
from be.store import LocalCAS

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "examples/count-native/project.toml"
TMP = ROOT.parents[1] / "work" / "cra"


def job_record(state: Path, operation: str):
    with closing(sqlite3.connect(state / "ledger.sqlite3")) as connection:
        row = connection.execute("SELECT output_ref FROM jobs WHERE kind=?", (operation,)).fetchone()
    ref = json.loads(row[0])
    store = LocalCAS(state / "artifacts")
    return store, ref, store.read_json(ref)


def install_record(state: Path, operation: str, record: dict):
    store = LocalCAS(state / "artifacts")
    ref = store.put_json(record, format_id="be.count-native/authenticated-stage-receipt/1")
    with closing(sqlite3.connect(state / "ledger.sqlite3")) as connection:
        connection.execute("UPDATE jobs SET output_ref=? WHERE kind=?", (json.dumps(ref), operation))
        connection.commit()


class NativeCompletionPolicyTests(unittest.TestCase):
    """A zero process exit does not override a failed runtime policy."""

    @classmethod
    def setUpClass(cls):
        TMP.mkdir(parents=True, exist_ok=True)
        cls.runtime = native.runtime_profile()

    def exercise(self, metadata):
        with tempfile.TemporaryDirectory(prefix="p-", dir=TMP) as directory:
            state = Path(directory) / "s"

            def producer(capsule, workspace, *, timeout, supervisor):
                # Deliberately stop before numerical output. Only the operational
                # wrapper is tested: it must reject this metadata immediately.
                supervisor([str(Path(sys.executable)), "-V"],
                           workspace, workspace / "native.log", timeout)
                raise AssertionError("Non-completed execution reached the numerical adapter")

            with mock.patch.object(native, "construct", side_effect=producer), \
                    mock.patch("be.supervisor.supervise_native", return_value=metadata), \
                    mock.patch.object(native, "runtime_profile", return_value=self.runtime):
                with self.assertRaises(ProtocolError):
                    runner.run_project(PROJECT, state_dir=state)
            with closing(sqlite3.connect(state / "ledger.sqlite3")) as connection:
                self.assertEqual(connection.execute("SELECT count(*) FROM jobs WHERE state='produced'").fetchone()[0], 0)

    def test_zero_exit_with_noncompleted_reason_is_not_completion(self):
        for reason in ("wall_timeout", "campaign_deadline", "log_limit", "cpu_limit"):
            with self.subTest(reason=reason):
                self.exercise(dict(returncode=0, reason=reason, tree_cleanup_complete=True))

    def test_zero_exit_without_confirmed_cleanup_is_not_completion(self):
        for cleanup in (False, None):
            with self.subTest(cleanup=cleanup):
                metadata = dict(returncode=0, reason="completed")
                if cleanup is not None:
                    metadata["tree_cleanup_complete"] = cleanup
                self.exercise(metadata)


class CountResumeAdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TMP.mkdir(parents=True, exist_ok=True)
        cls.base = tempfile.TemporaryDirectory(prefix="b-", dir=TMP)
        cls.addClassCleanup(cls.base.cleanup)
        cls.state = Path(cls.base.name) / "s"
        cls.report, code = runner.run_project(PROJECT, state_dir=cls.state)
        if code != 0 or cls.report["status"] != "SCOPED_COUNT_PASS":
            raise RuntimeError("A real native construction and complete acceptance are required")
        if cls.report["full_proof_pass"] or cls.report["parent_acquisitions_verified"]:
            raise RuntimeError("Scoped fixture must not claim the final theorem or current parent facts")
        with closing(sqlite3.connect(cls.state / "ledger.sqlite3")) as connection:
            frozen_ref = json.loads(connection.execute("SELECT frozen_ref FROM campaigns").fetchone()[0])
        store = LocalCAS(cls.state / "artifacts")
        frozen = store.read_json(frozen_ref)
        cls.runtime = dict(profile=json.loads(store.read_bytes(frozen["native_runtime_ref"])),
                           digest=frozen["native_runtime_digest"])

    def setUp(self):
        self.case = tempfile.TemporaryDirectory(prefix="c-", dir=TMP)
        self.addCleanup(self.case.cleanup)
        self.current = Path(self.case.name) / "s"
        shutil.copytree(self.state, self.current)

    def resume_without_native_execution(self, *, state=None, project=PROJECT, real_runtime=False):
        profile = nullcontext() if real_runtime else mock.patch.object(native, "runtime_profile", return_value=self.runtime)
        with mock.patch.object(native, "construct", side_effect=AssertionError("Unexpected reconstruction")), \
                mock.patch.object(native, "accept", side_effect=AssertionError("Unexpected numerical replay")), profile:
            return runner.run_project(project, state_dir=state or self.current, resume=True)

    def assert_rejected_resume(self):
        with self.assertRaises(ProtocolError):
            self.resume_without_native_execution()

    def test_authenticated_resume_skips_both_expensive_native_stages(self):
        report, code = self.resume_without_native_execution(real_runtime=True)
        self.assertEqual(code, 0)
        self.assertTrue(report["producer_cache_hit"])
        self.assertTrue(report["verifier_cache_hit"])
        self.assertEqual(report["campaign_id"], self.report["campaign_id"])
        self.assertEqual(report["candidate_ref"], self.report["candidate_ref"])
        self.assertEqual(report["attempts_total"], "2")
        self.assertFalse(report["full_proof_pass"])

    def test_unsigned_sqlite_success_word_is_not_an_accepted_cache(self):
        install_record(self.current, "verify", dict(status="SCOPED_COUNT_PASS", full_proof_pass=False))
        self.assert_rejected_resume()

    def test_payload_changes_cannot_keep_the_old_seal(self):
        mutations = {
            "campaign_id": "campaign:borrowed",
            "statement_digest": "0" * 64,
            "source_epoch_digest": "1" * 64,
            "native_runtime_digest": "2" * 64,
            "trust_profile": "unreviewed-trust-upgrade",
            "full_proof_pass": True,
        }
        _, _, original = job_record(self.current, "verify")
        for field, value in mutations.items():
            with self.subTest(field=field):
                record = copy.deepcopy(original)
                record["payload"][field] = value
                install_record(self.current, "verify", record)
                self.assert_rejected_resume()

    def test_even_resigned_wrong_scope_is_rejected_by_context_binding(self):
        # Deliberately using the test-owned coordinator key checks that the
        # payload binder is still required in addition to cryptographic validity.
        _, _, original = job_record(self.current, "verify")
        for field, value in (("campaign_id", "campaign:other"),
                             ("statement_digest", "3" * 64),
                             ("trust_profile", "different-profile"),
                             ("full_proof_pass", True),
                             ("unexpected_claim", "not-a-supported-field")):
            with self.subTest(field=field):
                record = copy.deepcopy(original)
                record["payload"][field] = value
                record["seal"] = LocalAuthority(self.current).sign(record["payload"])
                install_record(self.current, "verify", record)
                self.assert_rejected_resume()

    def test_verifier_cannot_substitute_another_whole_candidate(self):
        store, _, record = job_record(self.current, "verify")
        raw = store.read_bytes(record["payload"]["candidate_ref"])
        # Harmless JSON whitespace preserves topology but changes whole bytes.
        record["payload"]["candidate_ref"] = store.put_bytes(raw + b"\n", format_id="be.count-native/whole-native-forest/1")
        record["seal"] = LocalAuthority(self.current).sign(record["payload"])
        install_record(self.current, "verify", record)
        self.assert_rejected_resume()

    def test_verification_key_cannot_be_replaced_even_with_a_valid_seal(self):
        _, _, record = job_record(self.current, "verify")
        record["payload"]["verification_key"] = "9" * 64
        record["seal"] = LocalAuthority(self.current).sign(record["payload"])
        install_record(self.current, "verify", record)
        self.assert_rejected_resume()

    def test_deleting_the_private_authority_cannot_reauthorize_old_results(self):
        (self.current / "authority.key").unlink()
        self.assert_rejected_resume()

    def test_new_campaign_cannot_borrow_old_authorized_receipts(self):
        ledger = SQLiteLedger(self.current / "ledger.sqlite3")
        with closing(sqlite3.connect(self.current / "ledger.sqlite3")) as connection:
            old = connection.execute("SELECT frozen_digest,frozen_ref FROM campaigns").fetchone()
        campaign = ledger.campaign("ordinary-count-native-v1", old[0], json.loads(old[1]),
                                   resume=False, fresh=True, wall_seconds=1800)
        producer_ref = self.report["producer_receipt_ref"]
        for operation, candidate_ref, ref in (("produce", None, producer_ref),
                                               ("verify", self.report["candidate_ref"], self.report["receipt_ref"])):
            spec = dict(frozen_digest=old[0], operation=operation, candidate_ref=candidate_ref)
            job = ledger.ensure_job(campaign["campaign_id"], digest("count-native-job-spec", spec), operation)
            with closing(sqlite3.connect(self.current / "ledger.sqlite3")) as connection:
                connection.execute("UPDATE jobs SET state='produced',output_ref=? WHERE job_id=?", (json.dumps(ref), job))
                connection.commit()
        self.assert_rejected_resume()

    def test_cache_artifact_bytes_are_rehashed_not_just_looked_up(self):
        for field in ("native_receipt_ref", "observation_ref", "log_ref"):
            with self.subTest(field=field):
                _, _, record = job_record(self.current, "verify")
                ref = record["payload"][field]
                hexdigest = ref["bytes_digest"].split(":", 1)[1]
                path = self.current / "artifacts/objects/sha256" / hexdigest[:2] / hexdigest
                original = path.read_bytes()
                path.write_bytes((b"x" if original[:1] != b"x" else b"y") + original[1:])
                try:
                    self.assert_rejected_resume()
                finally:
                    path.write_bytes(original)

    def test_changed_limits_do_not_reset_the_campaign_on_resume(self):
        project = Path(self.case.name) / "altered.toml"
        project.write_text(PROJECT.read_text(encoding="utf-8").replace("cpu_seconds = 300", "cpu_seconds = 299"), encoding="utf-8")
        with self.assertRaises(ProtocolError) as caught:
            self.resume_without_native_execution(project=project)
        self.assertEqual(caught.exception.code, "frozen_input_changed")


if __name__ == "__main__":
    unittest.main()
