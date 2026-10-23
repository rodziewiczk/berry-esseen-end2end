"""Exact evidence compatibility fixtures; no original mathematics executes."""
from copy import deepcopy
import unittest
from unittest.mock import patch

from be_replay import count_implementation_history as history
from be_replay import n25_count_evidence as ordinary
from be_replay import count_recovery_evidence as recovery


class CountImplementationHistoryTests(unittest.TestCase):
    def record(self, value):
        return dict(deepcopy(value), python="fixture-python-no-math")

    def test_published_ordinary_pins_are_revalidated_after_discovery_upgrade(self):
        old = self.record(history.ordinary())
        current = self.record(history.ordinary())
        current["count_task_sha256"] = "a" * 64
        with patch.object(ordinary.count, "implementation", return_value=current):
            ordinary.implementation(old)
            ordinary.implementation(current)
            bad = deepcopy(old)
            bad["supervisor_sha256"] = "a" * 64
            with self.assertRaises(ValueError):
                ordinary.implementation(bad)

    def test_recovery_implementations_are_whole_tuples_without_mixed_epochs(self):
        old = self.record(history.recovery())
        current = deepcopy(old)
        current["count_task_sha256"] = "a" * 64
        current["count_recovery_sha256"] = "b" * 64
        current["count_limit_epoch_sha256"] = "c" * 64
        with patch.object(recovery.count, "implementation", return_value={
                k: v for k, v in current.items() if k not in history.MIDPOINT_RECOVERY_PAIR}), \
             patch.object(recovery.count, "digest", side_effect=lambda p:
                          current["count_recovery_sha256"] if str(p).endswith("count_recovery.py")
                          else current["count_limit_epoch_sha256"]):
            for target in recovery.limit.PROFILES:
                recovery.implementation(old, target)
                recovery.implementation(current, target)
                mixed = deepcopy(old)
                mixed["count_task_sha256"] = current["count_task_sha256"]
                with self.subTest(target=target), self.assertRaises(ValueError):
                    recovery.implementation(mixed, target)

    def test_legacy_q2_is_not_a_compatibility_gate_for_other_targets(self):
        old = self.record(history.recovery(legacy_q2=True))
        self.assertTrue(history.matches(old, history.recovery(legacy_q2=True)))
        self.assertFalse(history.matches(old, history.recovery()))
        recovery.implementation(old, "b4-q2")
        for target in recovery.limit.PROFILES:
            if target != "b4-q2":
                with self.subTest(target=target), self.assertRaises(ValueError):
                    recovery.implementation(old, target)

    def test_extra_pins_and_missing_context_are_not_accepted(self):
        for change in (lambda x: x.update(python=""), lambda x: x.update(extra=True),
                       lambda x: x["vendor"]["files_sha256"].update(unreviewed="f" * 64)):
            value = self.record(history.ordinary())
            change(value)
            self.assertFalse(history.matches(value, history.ordinary()))


if __name__ == "__main__":
    unittest.main()
