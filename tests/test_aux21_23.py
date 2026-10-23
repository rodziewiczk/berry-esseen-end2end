"""Synthetic source/candidate and observed-execution fixtures; no kernels run."""
from contextlib import redirect_stdout, nullcontext
from copy import deepcopy
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import aux21_23 as job, aux24_sources as sources


class Aux21to23Tests(unittest.TestCase):
    def setUp(self):
        parent = job.ROOT / "work" / "aux21_23-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.pins = dict(job.EPOCH_PINS)
        self.pin_patch = patch.dict(job.EPOCH_PINS, self.pins)
        self.pin_patch.start()
        self.addCleanup(self.pin_patch.stop)

    def fixture(self, value, output=None):
        """A deliberately synthetic archive selection, never a certificate."""
        task = output or self.root / ("task" + value)
        task.mkdir(parents=True)
        selection = job.members(value)
        for name in selection:
            path = task / "source" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"{}\n" if path.suffix == ".json" else b"# synthetic source: never executed\n")
        if value != "21":
            spec = job.SPECS[value]
            root = sources.source_root(task) / "continuation_20261010"
            initial, resource, count = (root / spec[k] for k in ("initial", "resource", "count"))
            profile = dict(n=spec["n"], nmax=spec["n"], barrier=spec["K"], radius="13/5" if value == "22" else "3", cap="469/1000" if value == "22" else "464661/1000000", grid=[24, 24, 8, 4])
            proof = dict(profile=profile, predecessor_allowance=spec["allowance"])
            raw = (json.dumps(proof) + "\n").encode()
            (initial / f"POSITIVE{value}_INITIAL_PROOF.json").write_bytes(raw)
            (resource / f"initial{value}_proof.json").write_bytes(raw)
            contract = dict(n=spec["n"], K=spec["K"], rows=[dict(index=i) for i in spec["indices"]])
            raw = (json.dumps(contract) + "\n").encode()
            (count / "contract.json").write_bytes(raw)
            (resource / f"contract{value}.json").write_bytes(raw)
            names = job.RESOURCE_COMMON + [f"resource{value}_core.py", f"protocol{value}.py", f"initial{value}_proof.json", f"contract{value}.json"]
            if value == "23":
                names += ["integer_exphi.py", "INTEGER_EXPHI_PROOF.txt"]
            bindings = {name: job.digest(resource / name) for name in names}
            r = dict(profile=profile, theorem=dict(n=spec["n"], K=spec["K"], contact_allowance=spec["allowance"]),
                     input_sha256=bindings, rows=[dict(index=i, result=dict(excluded=i not in spec["indices"])) for i in range(100)])
            (resource / f"resources{value}_proof.json").write_text(json.dumps(r) + "\n")
            each, rest = divmod(spec["leaves"], len(spec["indices"]))
            for position, index in enumerate(spec["indices"]):
                c = dict(index=index, contract_sha256=job.digest(count / "contract.json"),
                         leaves=[dict(status="fixture") for _ in range(each+(position < rest))], maximum_score="2/5")
                (count / f"candidate_{index}.json").write_text(json.dumps(c) + "\n")
        files = {name: dict(kind=kind, bytes=(task / "source" / name).stat().st_size,
                           sha256=job.digest(task / "source" / name)) for name, kind in sorted(selection.items())}
        manifest = dict(schema=sources.SCHEMA, archive=sources.ARCHIVE, files=files,
                        mathematical_code_executed=False, historical_acceptances_imported=0,
                        premises_acquired=False, all_index_conclusion_verified=False)
        sources._write(task / sources.MANIFEST, manifest)
        pin = job.digest(task / sources.MANIFEST)
        job.EPOCH_PINS[value] = pin
        sources._write(task / sources.TASK, dict(schema="AUX21_24_SOURCE_TASK_V1", manifest_sha256=pin,
                       preparer_sha256=job.digest(sources.__file__), selected_files=len(files),
                       native_arithmetic_accepted=False, premises_acquired=False, all_index_conclusion_verified=False))
        job.write(task / "JOB.json", dict(schema="FRESH_AUX21_23_JOB_V1", target=value, manifest_sha256=pin,
                  driver_sha256=job.digest(job.__file__), premises=job.PREMISES[value], predecessor_acquisition_verified=False,
                  full_auxiliary_bound_verified=False, stronger24_acquisition_verified=False, all_index_conclusion_verified=False))
        job._job(task)
        return task

    def bindings(self, directory, names):
        return {name: job.digest(directory / name) for name in names}

    def receipt(self, task, value, stage):
        spec = job.SPECS[value]
        d = sources.source_root(task) / stage["directory"]
        name = stage["name"]
        if value == "21":
            return dict(status="EXACT_FINITE_COVER_PASS_CONDITIONAL_ANALYTIC_INTERFACES", profile=dict(n=21),
                        predecessor_allowance="299/2000", signed_rectangles=92160,
                        stages=[dict(total=18432, active=1, excluded=18431, D="-1/25") for _ in range(5)],
                        source_sha256=self.bindings(d, job.INITIAL_COMMON), checker_sha256=job.digest(d / stage["script"]))
        if name == "initial":
            proof = job.read(d / f"POSITIVE{value}_INITIAL_PROOF.json")
            names = ["initial34.py", "kernel.py", "high_window_core.py"] if value == "22" else job.INITIAL_COMMON + ["integer_exphi.py", "INTEGER_EXPHI_PROOF.txt"]
            r = dict(status="FRESH_EXACT_CONDITIONAL_POSITIVE22_INITIAL_PASS" if value == "22" else "PASS_FRESH_CONDITIONAL_POSITIVE23_INITIAL",
                     profile=proof["profile"], signed_rectangles=spec["rectangles"], probability_panels=100,
                     proof_sha256=job.digest(d / f"POSITIVE{value}_INITIAL_PROOF.json"), checker_sha256=job.digest(d / stage["script"]),
                     source_sha256=self.bindings(d, names))
            r["fixed_expected_object_controls" if value == "22" else "negative_controls"] = job.INITIAL22_CONTROLS if value == "22" else job.INITIAL23_CONTROLS
            return r
        if name == "resource":
            proof = job.read(d / f"resources{value}_proof.json")
            return dict(status=f"PASS_POSITIVE{value}_RESOURCES", probability_panels=100, profile=proof["profile"],
                        theorem=proof["theorem"], negative_controls=job.RESOURCE_CONTROLS, resource_sha256=job.digest(d / f"resources{value}_proof.json"),
                        acceptor_sha256=job.digest(d / stage["script"]), input_sha256=proof["input_sha256"],
                        surviving_panels=spec["indices"], excluded_panels=[i for i in range(100) if i not in spec["indices"]])
        if name == "optimization":
            return dict(status="PASS_EXACT_OUTPUT_EQUIVALENCE_COUNT23", complete_cell_dicts=70, random_quartics=1000,
                        source_sha256=self.bindings(d, ["exact35_core.py", "optimized_arithmetic.py", "bernstein_fast.py", "interval_scalar_fast.py", "joint_cubic_normalized_fast.py", "check_optimization.py"]))
        if name == "count-join":
            return dict(status="PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES", n=spec["n"], K=spec["K"], indices=spec["indices"],
                        all_closed_leaves=spec["leaves"], contract_sha256=job.digest(d / "contract.json"), maximum_score="2/5", target_lower="41/100", strict_margin="1/100",
                        source_sha256=self.bindings(d, job.COUNT_COMMON + (job.COUNT_FAST if value == "23" else [])),
                        rows=[dict(index=i, candidate_sha256=job.digest(d / f"candidate_{i}.json"), receipt_sha256=job.digest(d / f"accepted_strict_{i}.json")) for i in spec["indices"]])
        index = int(name.split("-")[1])
        candidate = job.read(d / f"candidate_{index}.json")
        nleaves = len(candidate["leaves"])
        return dict(status="PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES", n=spec["n"], K=spec["K"], index=index,
                    candidate_sha256=job.digest(d / f"candidate_{index}.json"), contract_sha256=job.digest(d / "contract.json"),
                    negative_controls=24, all_closed_leaves=nleaves, passed_cells=1, empty_cells=nleaves-1,
                    maximum_score="2/5", target_lower="41/100",
                    source_sha256=self.bindings(d, job.COUNT_COMMON + (job.COUNT_FAST if value == "23" else [])))

    def fake_native(self, task, value, *, mutate=None):
        calls = []
        def observe(argv, **options):
            stage = next(s for s in job.stages(value) if Path(argv[3]).name == s["script"] and argv[4:] == s["args"])
            calls.append(stage["name"])
            self.assertEqual(options["mode"], stage["mode"])
            self.assertEqual(options["memory_bytes"], 512*job.MIB)
            r = self.receipt(task, value, stage)
            receipt_path = Path(options["cwd"]) / stage["output"]
            job.write(receipt_path, r)
            r = job.read(receipt_path)
            if value == "21":
                stdout = "EXACT21_STAGE fixture\nEXACT21_PASS\n"
            elif stage["name"].startswith("count-") and stage["name"] != "count-join":
                prefix = "ACCEPTED_CONDITIONAL_COUNT22_K090_COUNT" if value == "22" else "ACCEPTED_CONDITIONAL_COUNT23_K060_OPTIMIZED_V1_COUNT"
                stdout = f"{prefix} {r['index']} {r['passed_cells']} {r['empty_cells']} {r['all_closed_leaves']} 24 fixture\n"
            elif stage["name"] == "count-join":
                stdout = json.dumps({k: r[k] for k in ("status", "n", "K", "all_closed_leaves", "maximum_score", "target_lower", "strict_margin")}, indent=2)+"\n"
            else:
                stdout = json.dumps(r, indent=2 if stage["name"] == "optimization" or value == "22" and stage["name"] == "initial" else None)+"\n"
            output = Path(options["output_dir"])
            output.mkdir()
            (output / "stdout.txt").write_text(stdout, encoding="utf-8")
            (output / "stderr.txt").write_bytes(b"")
            cpu = options["cpu_seconds"]
            controller = min(30, max(1, cpu//10))
            guard = dict(kind="LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1", capability_established=True,
                         native_python_execution=True, hard_sum_RLIMIT_AS_bytes=512*job.MIB,
                         worker_RLIMIT_AS_bytes=448*job.MIB, supervisor_RLIMIT_AS_bytes=64*job.MIB,
                         hard_sum_RLIMIT_CPU_seconds=cpu, supervisor_RLIMIT_CPU_seconds=controller,
                         worker_RLIMIT_CPU_seconds=cpu-controller, script_sha256=job.digest(argv[3]),
                         supervisor_source_sha256=job.digest(Path(job.__file__).with_name("linux_supervisor.py")))
            if stage["mode"] != "trusted_native":
                guard = dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP", proof_acceptance=False)
            observed = dict(status="completed", returncode=0, mode=stage["mode"], guard_scope=guard,
                            stdout_path=str(output / "stdout.txt"), stderr_path=str(output / "stderr.txt"),
                            stdout_sha256=job.digest(output / "stdout.txt"), stderr_sha256=job.digest(output / "stderr.txt"))
            if mutate:
                mutate(stage, receipt_path, observed)
            return observed
        return observe, calls

    def mocked_run(self, task, value, **options):
        native, calls = self.fake_native(task, value, **options)
        # Source-copy integrity has its own real fixtures. Cache this already
        # verified synthetic inventory while exercising all dispatch stages.
        manifest = sources.verify_prepared(task, job.EPOCH_PINS[value], outputs=job.allowed_outputs(value))
        with patch("be_replay.count_task.supervise", native), \
             patch.object(sources, "verify_prepared", return_value=manifest), \
             patch("be_replay.small_indices.FollowOutput", side_effect=lambda *args: nullcontext()), redirect_stdout(io.StringIO()):
            result = job.run(task)
        return result, calls

    def test_selections_have_exact_census_and_no_historical_acceptance_inputs(self):
        self.assertEqual({v: len(job.members(v)) for v in job.SPECS}, {"21": 8, "22": 55, "23": 103})
        for value in job.SPECS:
            for name, kind in job.members(value).items():
                sources._kind(name, kind)
                self.assertNotIn("ACCEPTED", name.upper())
                self.assertNotEqual(Path(name).name, "OPTIMIZATION_EQUIVALENCE.json")
        self.assertEqual(sum(s["name"].startswith("count-") and s["name"] != "count-join" for s in job.stages("22")), 9)
        self.assertEqual(sum(s["name"].startswith("count-") and s["name"] != "count-join" for s in job.stages("23")), 21)

    def test_complete_initial21_fixture_and_stage_resume_without_math(self):
        task = self.fixture("21")
        result, calls = self.mocked_run(task, "21")
        self.assertEqual(calls, ["initial"])
        self.assertTrue(result["conditional_arithmetic_replayed"])
        self.assertTrue(result["semantics_verified"])
        self.assertFalse(result["full_auxiliary_bound_verified"])
        with patch("be_replay.count_task.supervise", side_effect=AssertionError("No repeated arithmetic")), redirect_stdout(io.StringIO()):
            self.assertEqual(job.run(task), result)

    def test_complete22_fixture_binds_initial_resource_and_all_count_contracts(self):
        task = self.fixture("22")
        result, calls = self.mocked_run(task, "22")
        self.assertEqual(calls, [s["name"] for s in job.stages("22")])
        edges = result["semantic_edges"]
        self.assertEqual(edges["count_leaves"], 258)
        self.assertEqual(edges["probability_panels"], 100)
        self.assertEqual(edges["count_indices"], list(range(31, 40)))
        self.assertEqual(edges["allowance"], "53/210")
        self.assertTrue(result["native_arithmetic_accepted"])
        self.assertFalse(result["stronger24_acquisition_verified"])

    def test_complete23_fixture_preserves_basic_optimization_and_native_counts(self):
        task = self.fixture("23")
        result, calls = self.mocked_run(task, "23")
        self.assertEqual(calls, [s["name"] for s in job.stages("23")])
        self.assertTrue(result["conditional_arithmetic_replayed"])
        self.assertFalse(result["native_arithmetic_accepted"])
        self.assertEqual(result["semantic_edges"]["count_leaves"], 18377)
        optimization = job.read(task / "optimization-COMPLETED.json")
        self.assertFalse(optimization["native_arithmetic_accepted"])
        self.assertTrue(job.read(task / "count-31-COMPLETED.json")["native_arithmetic_accepted"])

    def test_relocated_completed_capsule_uses_original_context_without_rewriting_receipts(self):
        task = self.fixture("22")
        expected, _ = self.mocked_run(task, "22")
        relocated = self.root / "another-private-location" / "task"
        shutil.copytree(task, relocated)
        shutil.rmtree(task)
        with patch("be_replay.count_task.supervise", side_effect=AssertionError("No arithmetic on validation")):
            self.assertEqual(job.validate_completed(relocated, original_task_root=str(task)), expected)
        with self.assertRaises(ValueError):
            job.validate_completed(relocated, original_task_root="/somewhere/else")

    def test_changed_candidate_after_completed_run_is_rejected(self):
        task = self.fixture("22")
        self.mocked_run(task, "22")
        path = sources.source_root(task) / "continuation_20261010/count22/candidate_31.json"
        with path.open("a") as out:
            out.write(" ")
        with self.assertRaisesRegex(ValueError, "Unchanged exact selected input"):
            job.validate_completed(task)

    def test_boolean_returncode_is_not_integer_zero(self):
        task = self.fixture("21")
        result, _ = self.mocked_run(task, "21", mutate=lambda s, p, r: r.update(returncode=False))
        self.assertEqual(result["status"], "PARTIAL_NOT_ACCEPTED")
        self.assertIn("integer successful", result["attempt"]["error"])

    def test_empty_stderr_with_wrong_supervisor_capture_hash_fails(self):
        task = self.fixture("21")
        result, _ = self.mocked_run(task, "21", mutate=lambda s, p, r: r.update(stderr_sha256="0"*64))
        self.assertIn("Actual capture", result["attempt"]["error"])

    def test_missing_native_guard_is_not_acceptance(self):
        task = self.fixture("21")
        result, _ = self.mocked_run(task, "21", mutate=lambda s, p, r: r["guard_scope"].update(capability_established=False))
        self.assertFalse(result["conditional_arithmetic_replayed"])

    def test_missing_original_resource_control_is_rejected(self):
        task = self.fixture("22")
        def mutate(stage, path, observed):
            if stage["name"] == "resource":
                obj = job.read(path)
                obj["negative_controls"].pop()
                path.unlink()
                job.write(path, obj)
        result, _ = self.mocked_run(task, "22", mutate=mutate)
        self.assertEqual(result["failed_stage"], "resource")
        self.assertIn("all20", result["attempt"]["error"])

    def test_missing_native_source_binding_is_rejected(self):
        task = self.fixture("21")
        def mutate(stage, path, observed):
            obj = job.read(path)
            obj["source_sha256"].pop("kernel.py")
            path.unlink()
            job.write(path, obj)
        result, _ = self.mocked_run(task, "21", mutate=mutate)
        self.assertIn("binding inventory", result["attempt"]["error"])

    def test_tampered_stored_semantic_edges_are_rejected(self):
        task = self.fixture("22")
        self.mocked_run(task, "22")
        path = task / "SEMANTIC_EDGES.json"
        obj = job.read(path)
        obj["allowance"] = "0"
        path.unlink()
        job.write(path, obj)
        with self.assertRaisesRegex(ValueError, "semantic edge packet"):
            job.validate_completed(task)

    def test_semantic_join_rejects_other_initial_object_and_uncovered_survivor(self):
        task = self.fixture("22")
        self.mocked_run(task, "22")
        spec = job.SPECS["22"]
        path = sources.source_root(task) / "continuation_20261010" / spec["resource"] / "RESOURCES22_ACCEPTED.json"
        saved = job.read(path)
        bad = deepcopy(saved)
        bad["input_sha256"]["initial22_proof.json"] = "0"*64
        path.unlink(); job.write(path, bad)
        reports = {s["name"]: job.read(job._ledger_path(task, s)) for s in job.stages("22")}
        with self.assertRaisesRegex(ValueError, "fully replayed INITIAL"):
            job.semantic_edges(task, "22", reports)
        path.unlink(); job.write(path, saved)
        bad = deepcopy(saved); bad["surviving_panels"].append(70)
        path.unlink(); job.write(path, bad)
        with self.assertRaisesRegex(ValueError, "Every surviving closed panel"):
            job.semantic_edges(task, "22", reports)

    def test_parser_and_recorded_path_traversal_are_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"n":21,"n":22}', object_pairs_hook=job.unique)
        with self.assertRaises(ValueError):
            job.recorded_relative("/tmp/original/../stdout.txt", "/tmp/original")
        self.assertEqual(job.recorded_relative("/old/task/attempts/a/stdout.txt", "/old/task").as_posix(), "attempts/a/stdout.txt")
        self.assertEqual(job.recorded_relative("C:\\old\\task\\a\\stdout.txt", "C:\\old\\task").as_posix(), "a/stdout.txt")

    def test_error_still_preserves_final_zip_with_false_global_flags(self):
        with patch.object(job, "prepare", side_effect=ValueError("fixture source failure")), \
             patch("be_replay.environment.snapshot", return_value={"fixture": True}), redirect_stdout(io.StringIO()):
            result = job.run_colab("21", durable_root=self.root / "durable", work_root=self.root / "work", resume=False)
        self.assertEqual(result["status"]["state"], "PARTIAL_ERROR_NOT_ACCEPTED")
        with zipfile.ZipFile(result["bundle"]) as archive:
            name = next(n for n in archive.namelist() if n.endswith("/SESSION_RESULT.json"))
            packet = json.loads(archive.read(name))
            self.assertFalse(packet["conditional_arithmetic_replayed"])
            self.assertFalse(packet["full_auxiliary_bound_verified"])
            self.assertFalse(packet["all_index_conclusion_verified"])
            self.assertTrue(any(n.endswith("/ERROR.txt") for n in archive.namelist()))


if __name__ == "__main__":
    unittest.main()
