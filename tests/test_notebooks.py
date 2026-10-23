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

    def test_generated_instructions_progress_and_error_messages_are_english(self):
        pin = "c"*40
        documents = [builder.make_count(pin, stem, target) for stem, target in builder.TARGETS]
        documents.append(builder.make_small(pin))
        for document in documents:
            source = "\n".join("".join(item["source"]) for item in document["cells"])
            self.assertNotRegex(source, r"[\u0105\u0107\u0119\u0142\u0144\u00f3\u015b\u017a\u017c\u0104\u0106\u0118\u0141\u0143\u00d3\u015a\u0179\u017b]")
            for message in ("Source commit mismatch", "Supervisor self-tests failed; computation will not start.",
                            "Logs and checkpoints:", "Execution status:", "Results ZIP on Google Drive:",
                            "The global proof remains unverified."):
                self.assertIn(message, source)
        count_intro = "".join(documents[0]["cells"][0]["source"])
        self.assertIn("one conditional n25 count forest", count_intro)
        self.assertIn("external wall-clock limit", count_intro)
        self.assertIn("both checkpoint copies", count_intro)
        small_intro = "".join(documents[-1]["cells"][0]["source"])
        self.assertIn("complete supplied n2 and n3 finite certificates", small_intro)
        self.assertIn("does not establish C4 or the all-index theorem", small_intro)

if __name__ == "__main__":
    unittest.main()
