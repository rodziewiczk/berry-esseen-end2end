"""Validate the delivered queue without fetching sources or evaluating kernels."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("retained_builder_fixture", ROOT/"tools/make_retained_n25_notebooks.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class RetainedNotebooks(unittest.TestCase):
    def test_three_distinct_branches_with_pinned_code_and_empty_outputs(self):
        pin = "a"*40
        seen = set()
        for name, (branch, count, leaves) in builder.JOBS.items():
            doc = builder.build(pin, name)
            self.assertEqual(doc["nbformat"], 4)
            self.assertEqual(doc["metadata"]["colab"]["name"], name+".ipynb")
            cells = {cell["id"]: "".join(cell["source"]) for cell in doc["cells"]}
            self.assertIn('CODE_COMMIT = "'+pin+'"', cells["pinned-code"])
            self.assertIn('RESULT = run_colab("'+branch+'", durable_root=DURABLE)', cells["execute-task"])
            self.assertIn(f"all {leaves:,} selected leaves", cells["instructions"])
            self.assertIn(f"each of the {count} forests", cells["instructions"])
            self.assertIn("Global/local", cells["instructions"])
            self.assertIn("The global proof remains unverified.", cells["download-result"])
            for cell in doc["cells"]:
                if cell["cell_type"] == "code":
                    self.assertEqual(cell["outputs"], [])
                    self.assertIsNone(cell["execution_count"])
                    compile("".join(cell["source"]), name, "exec")
            seen.add(branch)
        self.assertEqual(seen, {"b0", "b1", "b2"})

    def test_mutable_or_invalid_commit_ref_is_rejected(self):
        for pin in ("main", "HEAD", "a"*39, "A"*40, "../main"):
            with self.subTest(pin=pin), self.assertRaises(ValueError):
                builder.build(pin, next(iter(builder.JOBS)))

    def test_complete_exact_queue_census(self):
        self.assertEqual(sum(row[1] for row in builder.JOBS.values()), 75)
        self.assertEqual(sum(row[2] for row in builder.JOBS.values()), 94288)


if __name__ == "__main__":
    unittest.main()
