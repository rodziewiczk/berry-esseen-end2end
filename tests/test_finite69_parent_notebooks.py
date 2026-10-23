"""Notebook generation and fake routing only; no numerical source is imported."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("finite69_parent_builder", ROOT / "tools/make_finite69_parent_notebooks.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
PIN = "a" * 40
EXPECTED = {"n6": ("44_n6_conditional_parents", 41, 133, 872),
            "initial7_9": ("45_n7_9_conditional_initial", 9, 81, 243)}
FALSE_FLAGS = ("native_arithmetic_accepted", "parent_acquisitions_verified",
               "fresh_parent_fact_joins_verified", "full_finite69_verified", "all_index_conclusion_verified")


def cell(doc, identifier):
    return "".join(next(item["source"] for item in doc["cells"] if item["id"] == identifier))


class Finite69ParentNotebooks(unittest.TestCase):
    def test_exact_two_jobs_census_scope_and_syntax(self):
        docs = builder.build_all(PIN)
        self.assertEqual(set(docs), {r[0] for r in EXPECTED.values()})
        for lane, (name, actions, covers, controls) in EXPECTED.items():
            doc = docs[name]
            self.assertEqual(doc["metadata"]["colab"]["name"], name + ".ipynb")
            prose = " ".join(cell(doc, "instructions").split())
            for expected in (f"all {actions}", f"all {covers}", f"all {controls}" if lane == "initial7_9" else "872 named controls",
                             "2,592 cells per cover", "2 GiB", "43,200", "54,000", "BASIC",
                             "every 20 seconds", "every 60 seconds", "partial numerical",
                             "parent-fact acquisition", "all-index theorem remain unverified", "remain false"):
                self.assertIn(expected, prose)
            self.assertIn('CODE_COMMIT = "' + PIN + '"', cell(doc, "pinned-code"))
            self.assertIn("test_linux_supervisor.py", cell(doc, "actual-linux-guard-tests"))
            self.assertIn("test_finite69_parent*.py", cell(doc, "finite69-parent-fixtures"))
            self.assertIn(f"run_colab({lane!r}, durable_root=DURABLE, backup_interval=60)", cell(doc, "execute-task"))
            self.assertIn("files.download", cell(doc, "download-result"))
            for item in doc["cells"]:
                if item["cell_type"] == "code":
                    compile("".join(item["source"]), name, "exec")
        self.assertIn("four full INITIAL", cell(docs[EXPECTED['n6'][0]], "instructions"))
        self.assertIn("17 local INITIAL", cell(docs[EXPECTED['n6'][0]], "instructions"))
        self.assertIn("three full 100-panel", cell(docs[EXPECTED['n6'][0]], "instructions"))
        self.assertIn("Missing historical timed", cell(docs[EXPECTED['initial7_9'][0]], "instructions"))

    def test_exact_catalog_action_and_control_census(self):
        catalog = json.loads((ROOT / "proof/finite69_parent_sources.json").read_bytes())
        for lane, (_, actions, _, controls) in EXPECTED.items():
            rows = [r for r in catalog["jobs"] if r["lane"] == lane]
            self.assertEqual(len(rows), actions)
            self.assertEqual(sum(len(r["native_controls"]) for r in rows), controls)
            self.assertTrue(all(r["parent_acquisitions_verified"] is False and
                                r["all_index_conclusion_verified"] is False for r in rows))

    def test_execution_routes_only_the_selected_lane_and_preserves_false_flags(self):
        calls = []
        module = types.ModuleType("be_replay.finite69_parents")
        def fake(lane, **options):
            calls.append((lane, options))
            return dict(status=dict(state="complete_selected_conditional_parent_arithmetic_basic",
                                    **{flag: False for flag in FALSE_FLAGS}),
                        bundle="synthetic.zip", work="synthetic")
        module.run_colab = fake
        with patch.dict(sys.modules, {module.__name__: module}):
            for lane in EXPECTED:
                namespace = dict(DURABLE=Path("/synthetic/durable"))
                exec(compile(cell(builder.build(PIN, lane), "execute-task"), "fake-route", "exec"), namespace)
                self.assertTrue(all(namespace["RESULT"]["status"][flag] is False for flag in FALSE_FLAGS))
        self.assertEqual(calls, [(lane, dict(durable_root=Path("/synthetic/durable"), backup_interval=60))
                                 for lane in EXPECTED])

    def test_infrastructure_failure_stops_before_any_numeric_call(self):
        class Child:
            stdout = ["synthetic fixture failed\n"]
            def wait(self):
                return 1
        with tempfile.TemporaryDirectory() as temporary:
            log = Path(temporary) / "fixture.log"
            process = types.SimpleNamespace(PIPE=object(), STDOUT=object(), Popen=lambda *a, **k: Child())
            namespace = dict(SELFTEST=log, subprocess=process, sys=sys, CODE=Path(temporary))
            with redirect_stdout(io.StringIO()), self.assertRaisesRegex(RuntimeError, "computation will not start"):
                exec(compile(cell(builder.build(PIN, "n6"), "finite69-parent-fixtures"), "fake-fixture", "exec"), namespace)
            self.assertNotIn("RESULT", namespace)
            self.assertEqual(log.with_name("fixture-finite69-parents.log").read_text(), "synthetic fixture failed\n")

    def test_pin_and_lane_reject_before_output_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "must-not-exist"
            for pin in (None, "main", "0" * 40, "A" * 40, "a" * 39, "a" * 41):
                with self.subTest(pin=pin), self.assertRaises(ValueError):
                    builder.write(pin, destination)
                self.assertFalse(destination.exists())
        for lane in (True, False, 6, "n7", "INITIAL7_9", None):
            with self.subTest(lane=lane), self.assertRaises(ValueError):
                builder.build(PIN, lane)

    def test_writer_creates_only_two_expected_lf_notebooks(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "generated"
            paths = builder.write(PIN, destination)
            self.assertEqual({p.name for p in paths}, {row[0] + ".ipynb" for row in EXPECTED.values()})
            self.assertEqual(len(list(destination.iterdir())), 2)
            for path in paths:
                data = path.read_bytes()
                self.assertNotIn(b"\r\n", data)
                self.assertTrue(data.endswith(b"\n"))
                self.assertEqual(json.loads(data)["metadata"]["colab"]["name"], path.name)


if __name__ == "__main__":
    unittest.main()
