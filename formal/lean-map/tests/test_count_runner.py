"""Real supervised construction, separate acceptance, and durable scoped resume."""
from pathlib import Path
import os
import tempfile
import unittest
from unittest.mock import patch

from be import count_native
from be.count_runner import load_project, run_project
from be.errors import ProtocolError
from be.ledger import SQLiteLedger
from be.schema import ROOT
from be.store import LocalCAS


class CountRunnerTests(unittest.TestCase):
    def test_actual_fresh_pipeline_and_authenticated_resume(self):
        # A short external state locator also exercises Windows' explicit path profile.
        with tempfile.TemporaryDirectory(prefix="cn-") as folder:
            state = Path(folder)
            project = ROOT / "examples/count-native/project.toml"
            cold, code = run_project(project, state_dir=state, resume=True)
            self.assertEqual(code, 0)
            self.assertEqual(cold["status"], "SCOPED_COUNT_PASS")
            self.assertFalse(cold["full_proof_pass"])
            self.assertFalse(cold["parent_acquisitions_verified"])
            self.assertFalse(cold["producer_cache_hit"])
            self.assertFalse(cold["verifier_cache_hit"])
            self.assertEqual(cold["attempts_total"], "2")
            store = LocalCAS(state / "artifacts")
            producer = store.read_json(cold["producer_receipt_ref"])["payload"]
            verifier = store.read_json(cold["receipt_ref"])["payload"]
            construct_observation = count_native.native_json(store.read_bytes(producer["observation_ref"]))
            accept_observation = count_native.native_json(store.read_bytes(verifier["observation_ref"]))
            self.assertNotEqual(construct_observation["process"]["execution_directory"],
                                accept_observation["process"]["execution_directory"])
            self.assertNotEqual(construct_observation["process"]["supervisor_metadata"]["pid"],
                                accept_observation["process"]["supervisor_metadata"]["pid"])
            self.assertEqual(verifier["candidate_ref"], producer["candidate_ref"])
            for observation in (construct_observation, accept_observation):
                self.assertEqual(observation["process"]["supervisor_metadata"]["reason"], "completed")
            with patch.object(count_native, "construct", side_effect=AssertionError("cache must not reconstruct")), \
                 patch.object(count_native, "accept", side_effect=AssertionError("cache must not rerun native acceptance")):
                resumed, code = run_project(project, state_dir=state, resume=True)
            self.assertEqual(code, 0)
            self.assertTrue(resumed["producer_cache_hit"])
            self.assertTrue(resumed["verifier_cache_hit"])
            for field in ("campaign_id", "frozen_digest", "candidate_ref", "receipt_ref", "attempts_total"):
                self.assertEqual(resumed[field], cold[field])
            self.assertNotEqual(resumed["run_id"], cold["run_id"])
            # Losing the operational authority cannot silently mint cache trust.
            (state / "authority.key").unlink()
            with self.assertRaises(ProtocolError) as caught:
                run_project(project, state_dir=state, resume=True)
            self.assertEqual(caught.exception.code, "frozen_input_changed")

    def test_unknown_inputs_and_invalid_lease_policy_fail_before_native(self):
        with tempfile.TemporaryDirectory(prefix="cp-") as folder:
            project = Path(folder) / "project.toml"
            project.write_text('schema_version="be.count-native/1"\nkind="ordinary-count-source-replay"\nallow_old_pass=true\n')
            with self.assertRaises(ProtocolError) as caught:
                load_project(project, None)
            self.assertEqual(caught.exception.code, "unsupported_project")
            project.write_text('schema_version="be.count-native/1"\nkind="ordinary-count-source-replay"\n[limits]\nlease_seconds=15\nheartbeat_seconds=5\n')
            with self.assertRaises(ProtocolError) as caught:
                load_project(project, None)
            self.assertEqual(caught.exception.code, "invalid_lease_policy")


if __name__ == "__main__":
    unittest.main()
