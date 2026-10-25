"""Topology adversaries and real source replay, with no synthetic PASS."""
from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import unittest

from be import count_native as count

HERE = Path(__file__).resolve().parent
CAPSULE = Path(os.environ.get("BE_COUNT_CAPSULE", str(count.DEFAULT_CAPSULE))).resolve()
TMP = HERE.parent / ".test_tmp" / "count_native"


class CountNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        count.verify_capsule(CAPSULE)
        cls.raw = count.read_regular(HERE / "fixtures" / "count_native" / "n6_B0_p61.untrusted-original-forest.json")
        if count.sha(cls.raw) != count.manifest()["files"][count.FOREST_NAME]["sha256"]:
            raise RuntimeError("Pinned untrusted parser fixture changed")
        cls.candidate = count.native_json(cls.raw)
        TMP.mkdir(parents=True, exist_ok=True)

    def assert_bad(self, mutation, code):
        value = deepcopy(self.candidate)
        mutation(value)
        with self.assertRaises(count.CountError) as caught:
            count.precheck_forest(count.canonical(value), CAPSULE)
        self.assertEqual(caught.exception.code, code)

    def test_real_complete_forest_and_literal_right_half(self):
        result = count.precheck_forest(self.raw, CAPSULE)
        self.assertEqual(result, {"roots": 7, "nodes": 11, "leaves": 9, "maximum_depth": 1,
                                  "closed_statuses": {"EMPTY_PHASE": 6, "PASS_TARGET": 3}})
        statement = count.statement(CAPSULE)
        self.assertEqual(statement["probability"], ["61/100", "31/50"])
        self.assertEqual(statement["orientation"], "literal-positive-class-no-reflection")
        self.assertEqual(statement["axes"][-1], "a0")
        self.assertFalse(statement["all_law_C6"])

    def test_missing_root(self):
        self.assert_bad(lambda value: value["roots"].pop(), "all_roots")

    def test_root_bool_is_not_count(self):
        self.assert_bad(lambda value: value["roots"][0].update(k=False), "root_order")

    def test_reordered_roots(self):
        self.assert_bad(lambda value: value["roots"].reverse(), "root_order")

    def test_missing_closed_child(self):
        self.assert_bad(lambda value: value["roots"][3]["tree"].pop("right"), "complete_children")

    def test_outside_cut(self):
        self.assert_bad(lambda value: value["roots"][3]["tree"].update(cut="1/2"), "strict_cut")

    def test_boolean_axis(self):
        self.assert_bad(lambda value: value["roots"][3]["tree"].update(axis=True), "split_axis")

    def test_changed_leaf_box(self):
        self.assert_bad(lambda value: value["roots"][0]["tree"]["box"][0].__setitem__(0, "0"), "leaf_box")

    def test_duplicate_native_key(self):
        with self.assertRaises(count.CountError) as caught:
            count.native_json(b'{"n":6,"n":6}')
        self.assertEqual(caught.exception.code, "duplicate_key")

    def test_cache_binds_entire_candidate_source_runtime(self):
        first = count.cache_key(self.raw, CAPSULE, "a" * 64)
        self.assertNotEqual(first, count.cache_key(self.raw + b"\n", CAPSULE, "a" * 64))
        self.assertNotEqual(first, count.cache_key(self.raw, CAPSULE, "b" * 64))
        with tempfile.TemporaryDirectory(prefix="s-", dir=TMP) as folder:
            target = Path(folder)
            for name, raw in count.verify_capsule(CAPSULE).items():
                (target / name).write_bytes(raw)
            (target / count.SOURCE_NAME).write_bytes(b"print('fake success')\n")
            with self.assertRaises(count.CountError) as caught:
                count.cache_key(self.raw, target, "a" * 64)
            self.assertEqual(caught.exception.code, "source_pin")

    def test_fresh_real_construct_and_accept(self):
        with tempfile.TemporaryDirectory(prefix="r-", dir=TMP) as folder:
            root = Path(folder)
            self.assertFalse((CAPSULE / count.FOREST_NAME).exists())
            self.assertFalse((CAPSULE / count.RECEIPT_NAME).exists())
            produced = count.construct(CAPSULE, root)
            self.assertFalse(produced["mathematically_accepted"])
            calls = []

            def supervisor(command, cwd, log, timeout):
                calls.append((command[:], cwd, log, timeout))
                self.assertEqual(command[-1], "accept")
                self.assertEqual(command[1:4], ["-E", "-B", "-S"])
                self.assertFalse(log.exists())
                self.assertFalse((cwd / count.RECEIPT_NAME).exists())
                metadata = count._default_supervisor(command, cwd, log, timeout)
                return dict(metadata, delegated=True)

            accepted = count.accept(CAPSULE, Path(produced["candidate"]), root,
                                    supervisor=supervisor)
            self.assertEqual(accepted["outcome"], "SCOPED_COUNT_PASS")
            self.assertEqual(accepted["native_statistics"]["leaves"], 9)
            self.assertEqual(len(accepted["negative_controls"]), 24)
            self.assertEqual(accepted["trust_profile"], count.TRUST)
            self.assertFalse(accepted["full_proof_pass"])
            self.assertFalse(accepted["all_law_C6_verified"])
            self.assertNotEqual(Path(accepted["native_receipt"]).parent, Path(produced["candidate"]).parent)
            self.assertEqual(len(calls), 1)
            self.assertTrue(accepted["process"]["supervisor_metadata"]["delegated"])

    def test_construct_forwards_supervisor_without_nested_launch(self):
        with tempfile.TemporaryDirectory(prefix="p-", dir=TMP) as folder:
            calls = []

            def supervisor(command, cwd, log, timeout):
                calls.append(command)
                self.assertEqual(command[-1], "construct")
                self.assertFalse((cwd / count.FOREST_NAME).exists())
                return count._default_supervisor(command, cwd, log, timeout)

            result = count.construct(CAPSULE, Path(folder), supervisor=supervisor)
            self.assertEqual(len(calls), 1)
            self.assertEqual(result["census"]["roots"], 7)

    def test_supervisor_false_success_cannot_replace_candidate(self):
        with tempfile.TemporaryDirectory(prefix="f-", dir=TMP) as folder:
            def supervisor(command, cwd, log, timeout):
                log.write_bytes(b"fake success\n")
                return {"returncode": 0}

            with self.assertRaises(count.CountError) as caught:
                count.construct(CAPSULE, Path(folder), supervisor=supervisor)
            self.assertEqual(caught.exception.code, "regular_file")


if __name__ == "__main__":
    unittest.main()
