"""Check next-stage notebook routing and immutable source selection; no math."""
import ast
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("phase2_builder", ROOT / "tools/make_phase2_notebooks.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class Phase2NotebookTests(unittest.TestCase):
    def test_distinct_jobs_are_pinned_and_executable_cells_compile(self):
        pin = "d" * 40
        tasks = set()
        for name, job in builder.JOBS.items():
            document = builder.build(pin, name)
            tasks.add(job["task"])
            source = "\n".join("".join(cell["source"]) for cell in document["cells"])
            self.assertIn('CODE_COMMIT = "' + pin + '"', source)
            self.assertIn("test_linux_supervisor.py", source)
            self.assertIn(job["tests"], source)
            self.assertIn("Driver", source.replace("driver", "Driver"))
            self.assertIn("RESULT[\"bundle\"]", source)
            self.assertIn("The global proof remains unverified.", source)
            self.assertEqual(len({cell["id"] for cell in document["cells"]}), len(document["cells"]))
            for cell in document["cells"]:
                if cell["cell_type"] == "code":
                    compile("".join(cell["source"]), name, "exec")
            self.assertNotRegex(source, r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]")
        self.assertEqual(len(tasks), 5)

    def test_notebooks_bind_exact_parent_branches_and_intended_runners(self):
        expected = {
            "09_n25_b3_initial_resources": ("be_replay.n25_parents", "b3"),
            "10_n25_b4_initial_resources": ("be_replay.n25_parents", "b4"),
            "11_n4_complete_root": ("be_replay.root4", None),
            "12_tail49_complete_arithmetic": ("be_replay.tail49", None),
            "13_n5_gapfree_whole_line": ("be_replay.n5_gapfree", None),
        }
        for name, (module, branch) in expected.items():
            doc = builder.build("e" * 40, name)
            source = "".join(next(cell for cell in doc["cells"] if cell["id"] == "execute-task")["source"])
            tree = ast.parse(source)
            self.assertEqual(tree.body[0].module, module)
            call = tree.body[1].value
            self.assertEqual(call.func.id, "run_colab")
            self.assertEqual([ast.literal_eval(arg) for arg in call.args], [branch] if branch else [])
            keywords = {item.arg: item.value for item in call.keywords}
            self.assertEqual(keywords["durable_root"].id, "DURABLE")
            if name == "12_tail49_complete_arithmetic":
                self.assertEqual(set(keywords), {"durable_root", "memory_bytes", "cpu_seconds", "wall_seconds"})
                self.assertEqual(ast.dump(keywords["memory_bytes"]), ast.dump(ast.parse("2048*1024**2", mode="eval").body))
                self.assertEqual(ast.literal_eval(keywords["cpu_seconds"]), 43200)
                self.assertEqual(ast.literal_eval(keywords["wall_seconds"]), 54000)
            else:
                self.assertEqual(set(keywords), {"durable_root"})

    def test_scope_keeps_untested_premises_and_distinct_platform_contracts_visible(self):
        parents = builder.JOBS["09_n25_b3_initial_resources"]["scope"]
        self.assertIn("STRONGER24", parents)
        self.assertIn("two-hour CPU ceiling", parents)
        root4 = builder.JOBS["11_n4_complete_root"]["scope"]
        self.assertIn("260", root4)
        self.assertIn("1,300", root4)
        self.assertIn("43,200", root4)
        self.assertIn("UNKNOWN", root4)
        tail = builder.JOBS["12_tail49_complete_arithmetic"]["scope"]
        self.assertIn("14", tail)
        self.assertIn("41", tail)
        self.assertIn("BASIC", tail)
        self.assertIn("cannot claim", tail)
        self.assertIn("2 GiB", tail)
        self.assertIn("512 MiB", tail)
        self.assertIn("54,000-second", tail)
        self.assertIn("43,200-second", tail)
        self.assertIn("not cumulative CPU accounting", tail)
        self.assertIn("no numerical resume", tail)
        n5 = builder.JOBS["13_n5_gapfree_whole_line"]["scope"]
        self.assertIn("positive closed-CDF", n5)
        self.assertIn("60-root", n5)
        self.assertIn("1,027", n5)
        self.assertIn("both infinite phase rays", n5)
        self.assertIn("one component of n5", n5)


if __name__ == "__main__":
    unittest.main()
