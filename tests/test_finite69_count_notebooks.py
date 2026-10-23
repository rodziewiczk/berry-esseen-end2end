"""Notebook generation/routing only; no mathematical engine is imported."""
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
spec = importlib.util.spec_from_file_location("finite69_count_builder", ROOT / "tools/make_finite69_count_notebooks.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
PIN = "a" * 40
EXPECTED = {6: (40, 90, 630, 165394), 7: (41, 72, 576, 48039),
            8: (42, 64, 576, 29651), 9: (43, 58, 580, 14005)}


def cell(doc, identifier):
    return "".join(next(item["source"] for item in doc["cells"] if item["id"] == identifier))


class Finite69CountNotebooks(unittest.TestCase):
    def test_four_exact_jobs_census_scope_and_syntax(self):
        docs = builder.build_all(PIN)
        self.assertEqual(len(docs), 4)
        for n, (number, forests, roots, leaves) in EXPECTED.items():
            name = f"{number}_n{n}_conditional_counts"
            doc = docs[name]
            self.assertEqual(doc["metadata"]["colab"]["name"], name + ".ipynb")
            prose = cell(doc, "instructions")
            for expected in (f"all {forests}", f"{roots:,} roots", f"{leaves:,} candidate leaves",
                             f"all {n + 1} literal roots", "all 24", "2 GiB", "43,200", "54,000",
                             "every 20 seconds", "every 60 seconds", "BASIC", "partial numerical",
                             "parent INITIAL/resource/support/Fourier", "all-index theorem remain unverified"):
                self.assertIn(expected, prose)
            self.assertIn('CODE_COMMIT = "' + PIN + '"', cell(doc, "pinned-code"))
            self.assertIn("test_linux_supervisor.py", cell(doc, "actual-linux-guard-tests"))
            self.assertIn("test_finite69_count*.py", cell(doc, "finite69-count-fixtures"))
            self.assertIn(f"run_colab({n}, durable_root=DURABLE, backup_interval=60)", cell(doc, "execute-task"))
            self.assertIn("files.download", cell(doc, "download-result"))
            for item in doc["cells"]:
                if item["cell_type"] == "code":
                    compile("".join(item["source"]), name, "exec")

    def test_execution_cells_route_only_their_selected_index(self):
        calls = []
        module = types.ModuleType("be_replay.finite69_counts")
        def fake(n, **options):
            calls.append((n, options))
            return dict(status=dict(state="synthetic_complete"), bundle="synthetic.zip", work="synthetic")
        module.run_colab = fake
        with patch.dict(sys.modules, {module.__name__: module}):
            for n in EXPECTED:
                namespace = dict(DURABLE=Path("/synthetic/durable"))
                exec(compile(cell(builder.build(PIN, n), "execute-task"), "fake-route", "exec"), namespace)
                self.assertEqual(namespace["RESULT"]["status"]["state"], "synthetic_complete")
        self.assertEqual(calls, [(n, dict(durable_root=Path("/synthetic/durable"), backup_interval=60)) for n in EXPECTED])

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
                exec(compile(cell(builder.build(PIN, 6), "finite69-count-fixtures"), "fake-fixture", "exec"), namespace)
            self.assertNotIn("RESULT", namespace)
            self.assertEqual(log.with_name("fixture-finite69-counts.log").read_text(), "synthetic fixture failed\n")

    def test_pin_and_index_fail_before_output_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "must-not-exist"
            for pin in (None, "main", "0" * 40, "A" * 40, "a" * 39, "a" * 41):
                with self.subTest(pin=pin), self.assertRaises(ValueError):
                    builder.write(pin, destination)
                self.assertFalse(destination.exists())
        for n in (True, False, "6", 5, 10, None):
            with self.subTest(n=n), self.assertRaises(ValueError):
                builder.build(PIN, n)

    def test_writer_only_creates_four_expected_lf_notebooks(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "generated"
            paths = builder.write(PIN, destination)
            self.assertEqual({p.name for p in paths}, {f"{number}_n{n}_conditional_counts.ipynb"
                             for n, (number, *_) in EXPECTED.items()})
            self.assertEqual(len(list(destination.iterdir())), 4)
            for path in paths:
                data = path.read_bytes()
                self.assertNotIn(b"\r\n", data)
                self.assertTrue(data.endswith(b"\n"))
                self.assertEqual(json.loads(data)["metadata"]["colab"]["name"], path.name)


if __name__ == "__main__":
    unittest.main()
