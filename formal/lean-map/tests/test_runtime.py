"""Failure/interleaving tests for the local CAS and fenced durable ledger."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from be.codec import digest
from be.errors import ProtocolError
from be.ledger import SQLiteLedger
from be.runner import load_project
from be.store import LocalCAS


class LocalRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = LocalCAS(self.root / "cas")
        self.clock = [1000.0]
        self.ledger = SQLiteLedger(self.root / "ledger.sqlite3", clock=lambda: self.clock[0])
        self.frozen = self.store.put_json({"fixture": "frozen"})
        self.campaign = self.ledger.campaign("project", digest("test-spec", {"fixture": "one"}),
                                            self.frozen, resume=True, wall_seconds=100)
        self.job = self.ledger.ensure_job(self.campaign["campaign_id"], digest("test-job", {}), "produce")

    def assert_code(self, code, operation):
        with self.assertRaises(ProtocolError) as caught:
            operation()
        self.assertEqual(caught.exception.code, code)

    def test_create_only_cas_and_corruption_detection(self):
        ref = self.store.put_bytes(b"original", media_type="application/octet-stream")
        self.assertEqual(ref, self.store.put_bytes(b"original", media_type="application/octet-stream"))
        self.store._path(ref).write_bytes(b"tampered")
        self.assert_code("artifact_digest_mismatch", lambda: self.store.read_bytes(ref))
        self.assert_code("artifact_digest_mismatch", lambda: self.store.put_bytes(b"original", media_type="application/octet-stream"))

    def test_size_rejected_before_hash(self):
        small = LocalCAS(self.root / "small", max_blob_bytes=4)
        with patch("be.store.bytes_digest", side_effect=AssertionError("must not hash oversized input")):
            self.assert_code("artifact_size_limit", lambda: small.put_bytes(b"12345"))

    def test_ref_cannot_escape_store(self):
        ref = dict(self.frozen)
        ref["bytes_digest"] = "../../outside"
        self.assert_code("invalid_artifact_ref", lambda: self.store.read_bytes(ref))

    def test_simultaneous_claim_has_one_winner(self):
        def attempt(label):
            try:
                return self.ledger.claim(self.job, label, lease_seconds=3)
            except ProtocolError as exc:
                return exc.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, ("run:first", "run:second")))
        self.assertEqual(sum(isinstance(item, dict) for item in results), 1)
        self.assertIn("job_busy", results)
        self.assertEqual(self.ledger.attempt_count(self.campaign["campaign_id"]), 1)

    def test_stale_worker_cannot_complete_or_checkpoint(self):
        first = self.ledger.claim(self.job, "run:first", lease_seconds=3)
        self.clock[0] += 4
        second = self.ledger.claim(self.job, "run:resumed", lease_seconds=3)
        self.assertEqual(second["generation"], first["generation"] + 1)
        self.assert_code("lease_superseded", lambda: self.ledger.complete(first, self.frozen, operation_key="old"))
        self.assert_code("lease_superseded", lambda: self.ledger.checkpoint(first, 1, self.frozen))
        self.ledger.complete(second, self.frozen, operation_key="current")
        self.assertEqual(self.ledger.get_job(self.job)["output_ref"], self.frozen)

    def test_idempotent_completion_and_payload_conflict(self):
        fence = self.ledger.claim(self.job, "run:first", lease_seconds=3)
        first = self.ledger.complete(fence, self.frozen, operation_key="complete-once", metadata={"fixture": True})
        self.assertEqual(first, self.ledger.complete(fence, self.frozen, operation_key="complete-once", metadata={"fixture": True}))
        self.assert_code("idempotency_conflict", lambda: self.ledger.complete(
            fence, self.frozen, operation_key="complete-once", metadata={"fixture": False}))
        fake = dict(fence, token="not-the-secret")
        self.assert_code("lease_superseded", lambda: self.ledger.complete(
            fake, self.frozen, operation_key="complete-once", metadata={"fixture": True}))

    def test_resume_retains_original_deadline_and_rejects_drift(self):
        self.clock[0] += 10
        resumed = self.ledger.campaign("project", self.campaign["frozen_digest"], self.frozen,
                                       resume=True, wall_seconds=1000)
        self.assertEqual(resumed["deadline"], self.campaign["deadline"])
        self.assert_code("frozen_input_changed", lambda: self.ledger.campaign(
            "project", digest("test-spec", {"fixture": "changed"}), self.frozen, resume=True))

    def test_expired_campaign_cannot_start_worker(self):
        self.clock[0] = self.campaign["deadline"]
        self.assert_code("campaign_closed", lambda: self.ledger.claim(self.job, "run:late"))

    def test_legacy_head_does_not_silently_create_new_campaign(self):
        self.clock[0] += 10
        self.assert_code("incompatible_state", lambda: self.ledger.campaign(
            "local-pilot-v1", self.campaign["frozen_digest"], self.frozen,
            resume=True, wall_seconds=1000))
        original = self.ledger.campaign("project", self.campaign["frozen_digest"], self.frozen,
                                        resume=True, wall_seconds=1000)
        self.assertEqual(original["campaign_id"], self.campaign["campaign_id"])
        self.assertEqual(original["deadline"], self.campaign["deadline"])
        explicit = self.ledger.campaign("local-pilot-v1", self.campaign["frozen_digest"], self.frozen,
                                        resume=False, fresh=True, wall_seconds=100)
        self.assertNotEqual(explicit["campaign_id"], original["campaign_id"])

    def test_checkpoint_is_monotone(self):
        fence = self.ledger.claim(self.job, "run:one", lease_seconds=3)
        self.ledger.checkpoint(fence, 1, self.frozen)
        self.assert_code("checkpoint_sequence_conflict", lambda: self.ledger.checkpoint(fence, 1, self.frozen))

    def test_project_rejects_unknown_runtime_and_invalid_lease(self):
        project = self.root / "project.toml"
        base = ('schema_version="be.local-pilot/1"\nkind="empty-joint-cubics-zero-noise"\n'
                'problem="problem.json"\nsource_manifest="source.json"\ntrust_profile="trust.json"\n')
        project.write_text(base + '[limits]\nunknown="2"\n', encoding="utf-8")
        self.assert_code("unsupported_resource_profile", lambda: load_project(project))
        project.write_text(base + '[limits]\nheartbeat_seconds="10"\nlease_seconds="30"\n', encoding="utf-8")
        self.assert_code("invalid_lease_policy", lambda: load_project(project))


if __name__ == "__main__":
    unittest.main()
