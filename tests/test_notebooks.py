"""Notebook structure and source-pin checks; never start a Colab calculation."""
import importlib.util
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("notebook_builder", ROOT/"tools/make_notebooks.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class NotebookTests(unittest.TestCase):
    def test_each_count_notebook_has_fixed_distinct_job_and_pinned_code(self):
        pin = "a"*40
        targets = set()
        for stem, target in builder.TARGETS:
            doc = builder.make_count(pin, stem, target)
            targets.add(target)
            source = "\n".join("".join(c["source"]) for c in doc["cells"])
            self.assertIn('CODE_COMMIT = "'+pin+'"', source)
            self.assertIn('run_count("'+target+'"', source)
            self.assertIn("total_seconds=10800", source)
            self.assertIn("backup_interval=60", source)
            self.assertIn("test_linux_supervisor.py", source)
            ids = [c["id"] for c in doc["cells"]]
            self.assertEqual(len(ids), len(set(ids)))
            for cell in doc["cells"]:
                if cell["cell_type"] == "code":
                    compile("".join(cell["source"]), stem, "exec")
        self.assertEqual(len(targets), 7)

    def test_small_notebook_uses_real_runner_and_compiler_check(self):
        doc = builder.make_small("b"*40)
        source = "\n".join("".join(c["source"]) for c in doc["cells"])
        self.assertIn("from be_replay.small_indices import run_colab", source)
        self.assertIn("g++", source)
        self.assertIn("test_linux_supervisor.py", source)
        self.assertNotIn("run_reproduction.py --tiny", source)
        for cell in doc["cells"]:
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]), "small", "exec")

if __name__ == "__main__":
    unittest.main()
