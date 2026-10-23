"""Restored discovery ledger and native-evidence fixtures; no math executes."""
from copy import deepcopy
import unittest

from be_replay import count_task as count, count_recovery_evidence as evidence
from be_replay import count_limit_epoch as epoch, count_implementation_history as history
import test_count_recovery_evidence as recovery_fixtures


class RestoredEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.fixture = recovery_fixtures.RecoveryEvidenceTests()
        self.fixture.RESTORED = True
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.task = self.fixture.task

    def test_complete_restored_fixture_and_relocated_evidence_are_read_back(self):
        report = evidence.validate_completed(self.task)
        self.assertTrue(report["native_arithmetic_accepted"])
        self.assertFalse(report["all_index_conclusion_verified"])
        task = count.read(self.task / "TASK.json")
        self.assertTrue(task["migration"]["roots_preserved"])
        self.assertEqual(task["migration"]["before_statistics"], task["migration"]["after_statistics"])
        self.fixture.test_relocation_preserves_original_paths_and_receipts()

    def test_each_lossless_migration_claim_is_recomputed(self):
        good = count.read(self.task / "TASK.json")
        files = epoch.verify(self.fixture.target, self.task / "capsule")
        changes = [
            lambda x: x["migration"].update(roots_preserved=False),
            lambda x: x["migration"]["before_statistics"].update(leaves=1),
            lambda x: x["migration"]["source_strategy"].update(alpha_priority="16"),
            lambda x: x["migration"]["target_strategy"].update(alpha_priority="4"),
            lambda x: x["migration"].update(execution_binding_sha256="0"*64),
            lambda x: x["migration"].update(input_checkpoint_sha256="0"*64),
            lambda x: x["migration"].update(migration_type="UNKNOWN_MIGRATION"),
            lambda x: x.update(implementation=dict(history.recovery(), python="fixture")),
        ]
        for change in changes:
            bad = deepcopy(good)
            change(bad)
            with self.subTest(change=change), self.assertRaises(ValueError):
                evidence.source_and_migration(self.task, bad, files)


if __name__ == "__main__":
    unittest.main()
