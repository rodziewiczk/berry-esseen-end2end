"""Check auxiliary notebook routing and publication boundaries without mathematics."""
import ast
from contextlib import redirect_stdout
import hashlib
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
spec = importlib.util.spec_from_file_location("aux24_notebook_fixture_builder", ROOT / "tools/make_aux24_notebooks.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

EXPECTED = {
    "14_auxiliary21": ("be_replay.aux21_23", "21", "test_aux21_23.py"),
    "15_auxiliary22": ("be_replay.aux21_23", "22", "test_aux21_23.py"),
    "16_auxiliary23": ("be_replay.aux21_23", "23", "test_aux21_23.py"),
    **{f"{17 + i:02d}_stronger24_b{i}": ("be_replay.strong24_branches", f"b{i}", "test_strong24_branches.py")
       for i in range(6)},
    "23_auxiliary24_final_join": ("be_replay.aux24_join", None, "test_aux24_join.py"),
}


def cell_source(document, cell_id):
    return "".join(next(cell for cell in document["cells"] if cell["id"] == cell_id)["source"])


class AuxiliaryNotebookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = ROOT / "work"
        cls.work.mkdir(exist_ok=True)

    def test_all_ten_jobs_pin_source_and_compile_without_running_it(self):
        self.assertEqual(tuple(builder.JOBS), tuple(EXPECTED))
        self.assertEqual(len({job["task"] for job in builder.JOBS.values()}), 10)
        pin = "d" * 40
        for name, (_, _, fixtures) in EXPECTED.items():
            with self.subTest(job=name):
                document = builder.build(pin, name)
                source = "\n".join("".join(cell["source"]) for cell in document["cells"])
                self.assertIn('CODE_COMMIT = "' + pin + '"', source)
                self.assertIn('TASK = "' + builder.JOBS[name]["task"] + '"', source)
                self.assertIn("test_linux_supervisor.py", source)
                self.assertIn(fixtures, cell_source(document, "driver-fixtures"))
                self.assertIn('RESULT["bundle"]', source)
                self.assertIn("The global proof remains unverified.", source)
                self.assertEqual(len({cell["id"] for cell in document["cells"]}), len(document["cells"]))
                self.assertNotRegex(source, r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]")
                for cell in document["cells"]:
                    if cell["cell_type"] == "code":
                        compile("".join(cell["source"]), name, "exec")

    def test_each_execute_cell_routes_only_to_its_mocked_runner(self):
        durable = object()
        for name, (module_name, target, _) in EXPECTED.items():
            with self.subTest(job=name):
                source = cell_source(builder.build("e" * 40, name), "execute-task")
                tree = ast.parse(source)
                self.assertEqual(len(tree.body), 2)
                self.assertEqual(tree.body[0].module, module_name)
                call = tree.body[1].value
                self.assertEqual(call.func.id, "run_colab")
                expected_args = (target,) if target is not None else ()
                self.assertEqual(tuple(ast.literal_eval(arg) for arg in call.args), expected_args)
                self.assertEqual([(item.arg, item.value.id) for item in call.keywords], [("durable_root", "DURABLE")])
                calls = []
                result = {"status": {"state": "fixture"}, "bundle": "fixture.zip", "work": "fixture-work"}
                fake = types.ModuleType(module_name)

                def run_colab(*args, **kwargs):
                    calls.append((args, kwargs))
                    return result

                fake.run_colab = run_colab
                namespace = {"DURABLE": durable}
                with patch.dict(sys.modules, {module_name: fake}):
                    exec(compile(source, name, "exec"), namespace)
                self.assertEqual(calls, [(expected_args, {"durable_root": durable})])
                self.assertIs(namespace["RESULT"], result)

    def test_dependencies_censuses_and_execution_limits_are_visible(self):
        for name in tuple(EXPECTED)[:-1]:
            with self.subTest(job=name):
                scope = builder.JOBS[name]["scope"]
                self.assertIn("14–22 may run in parallel", scope)
                self.assertIn("do not need restarting", scope)
                self.assertIn("7,200-second CPU", scope)
                self.assertIn("7,260-second wall", scope)
                self.assertIn("conditional", scope)
                self.assertIn("incomplete", scope)
        for name, counts in {
            "14_auxiliary21": ("92,160", "11/210", "469/1000"),
            "15_auxiliary22": ("129,024", "100", "258", "9/220"),
            "16_auxiliary23": ("165,888", "100", "18,377", "3/115", "BASIC"),
        }.items():
            for count in counts:
                self.assertIn(count, builder.JOBS[name]["scope"])
        for name in tuple(EXPECTED)[3:-1]:
            scope = builder.JOBS[name]["scope"]
            self.assertIn("all 100 probability panels", scope)
            self.assertIn("BASIC", scope)
            self.assertIn("does not claim trusted native", scope)
            self.assertIn("not a complete C24 theorem", scope)
        final = builder.JOBS["23_auxiliary24_final_join"]["scope"]
        for text in ("LAST", "14–22 have finished successfully", "all nine completed bundles",
                     "Missing, partial or incompatible", "rather than rerunning", "1/80", "not the sharp C24"):
            self.assertIn(text, final)

    def test_invalid_selection_is_rejected_before_creating_output(self):
        for pin in ("main", "d" * 39, "D" * 40, "d" * 41, None):
            with self.subTest(pin=pin), self.assertRaises(ValueError):
                builder.build(pin, "14_auxiliary21")
        with self.assertRaises(ValueError):
            builder.build("d" * 40, "09_n25_b3_initial_resources")
        with tempfile.TemporaryDirectory(prefix="aux24-notebook-invalid-", dir=self.work) as temporary:
            output = Path(temporary) / "not-created"
            with patch.object(sys, "argv", ["make_aux24_notebooks.py", "--pin=main", "--output", str(output)]):
                with self.assertRaises(ValueError):
                    builder.main()
            self.assertFalse(output.exists())

    def test_cli_writes_ten_new_notebooks_and_preserves_earlier_files(self):
        old_generators = [ROOT / "tools/make_notebooks.py", ROOT / "tools/make_phase2_notebooks.py"]
        old_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in old_generators]
        with tempfile.TemporaryDirectory(prefix="aux24-notebook-fixture-", dir=self.work) as temporary:
            output = Path(temporary)
            old = {output / f"{number:02d}_existing.ipynb": f"earlier notebook {number}\n".encode()
                   for number in range(1, 14)}
            for path, content in old.items():
                path.write_bytes(content)
            with patch.object(sys, "argv", ["make_aux24_notebooks.py", "--pin", "f" * 40,
                                             "--output", str(output)]), redirect_stdout(io.StringIO()):
                builder.main()
            self.assertEqual({path.name for path in output.glob("*.ipynb")},
                             {path.name for path in old} | {name + ".ipynb" for name in EXPECTED})
            for path, content in old.items():
                self.assertEqual(path.read_bytes(), content)
            for name in EXPECTED:
                document = json.loads((output / (name + ".ipynb")).read_text(encoding="utf-8"))
                self.assertIn('CODE_COMMIT = "' + "f" * 40 + '"', cell_source(document, "pinned-code"))
        self.assertEqual([hashlib.sha256(path.read_bytes()).hexdigest() for path in old_generators], old_hashes)
        independent_spec = importlib.util.spec_from_file_location("independent_phase2_fixture", old_generators[1])
        independent = importlib.util.module_from_spec(independent_spec)
        independent_spec.loader.exec_module(independent)
        self.assertEqual(len(independent.JOBS), 5)
        self.assertNotIn("14_auxiliary21", independent.JOBS)

    def test_cli_can_generate_one_queued_job_with_the_existing_pin_alias(self):
        with tempfile.TemporaryDirectory(prefix="aux24-notebook-selected-", dir=self.work) as temporary:
            selected = "23_auxiliary24_final_join"
            with patch.object(sys, "argv", ["make_aux24_notebooks.py", "--code-commit", "a" * 40,
                                             "--output", temporary, "--jobs", selected]), redirect_stdout(io.StringIO()):
                builder.main()
            self.assertEqual([path.name for path in Path(temporary).iterdir()], [selected + ".ipynb"])


if __name__ == "__main__":
    unittest.main()
