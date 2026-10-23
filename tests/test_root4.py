"""ROOT4 resource-port and driver fixtures; no mathematical producer executes."""
from copy import deepcopy
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

from be_replay import root4


class Root4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = root4.verify_frozen()
        cls.derived, cls.epoch = root4.derive_sources(cls.original)

    def setUp(self):
        parent = root4.ROOT / "work" / "root4-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def capsule(self):
        capsule = self.root / "capsule"
        root4.prepare(capsule)
        return capsule

    def terminal(self, capsule, stage, *, pending=()):
        summary = dict(geometry_classes_total=260, closed_geometry_classes=260-len(pending),
                       unresolved_geometry_classes=len(pending), ALL_high_request_slots_accounted=1300,
                       fixed_geometry_max_depth=1,
                       entire_conditional_root_score_upper_exact="41/100" if pending else "409/1000")
        status = ("UNKNOWN_WITH_ENTIRE_ROOT_AND_ALL_PORTFOLIO_GAPS_RETAINED" if pending else
                  "EXACT_CONDITIONAL_ENTIRE_PHYSICAL_ROOT_PORTFOLIO")
        return dict(status=status if stage == "produce" else "READ_ONLY_REPLAY_ALL_NONRESOURCE_FIELDS_MATCH",
                    result=str(capsule / root4.OUTPUT_NAME), summary=summary,
                    unresolved_geometry_indices=list(pending),
                    resources=dict(budget_clock_basis="time.process_time", time_limit_seconds=43200,
                                   memory_limit_bytes=256*root4.MIB, actual_CLI_cpu_seconds=.01,
                                   actual_CLI_peak_working_set_bytes=20*root4.MIB,
                                   read_only_replay_wrote_any_checkpoint=False))

    def guard(self, capsule):
        return dict(kind="LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1", capability_established=True,
                    native_python_execution=True, proof_acceptance=False,
                    hard_sum_RLIMIT_AS_bytes=320*root4.MIB,
                    worker_RLIMIT_AS_bytes=256*root4.MIB,
                    supervisor_RLIMIT_AS_bytes=64*root4.MIB,
                    hard_sum_RLIMIT_CPU_seconds=43230, worker_RLIMIT_CPU_seconds=43200,
                    supervisor_RLIMIT_CPU_seconds=30,
                    script_sha256=root4.digest(capsule / root4.ENTRY),
                    supervisor_source_sha256=root4.digest(Path(root4.__file__).with_name("linux_supervisor.py")))

    def fake_native(self, *, pending=(), change_replay=False, weak_guard=False):
        """Fixture packets exercise orchestration only, never establish real math."""
        def observed(argv, **options):
            capsule = Path(options["cwd"])
            stage = "produce" if argv[-1] == "--produce" else "replay"
            self.assertEqual(options["mode"], "trusted_native")
            self.assertEqual(options["memory_bytes"], 320*root4.MIB)
            self.assertEqual(options["cpu_seconds"], 43230)
            self.assertEqual(Path(argv[3]).parent, capsule)
            self.assertEqual(argv[1:3], ["-B", "-S"])
            receipt = capsule / root4.OUTPUT_NAME
            if stage == "produce":
                receipt.write_text('{"fixture_only_not_mathematics":true}\n', encoding="utf-8")
            elif change_replay:
                with receipt.open("a", encoding="utf-8") as stream:
                    stream.write(" ")
            output = Path(options["output_dir"])
            output.mkdir()
            stdout, stderr = output / "stdout.txt", output / "stderr.txt"
            stdout.write_text(json.dumps(self.terminal(capsule, stage, pending=pending)) + "\n", encoding="utf-8")
            stderr.write_text("", encoding="utf-8")
            guard = self.guard(capsule)
            if weak_guard:
                guard["capability_established"] = False
            return dict(status="completed", returncode=0, stdout_path=str(stdout), stderr_path=str(stderr),
                        stdout_sha256=root4.digest(stdout), stderr_sha256=root4.digest(stderr), guard_scope=guard)
        return observed

    def test_original_closure_is_pinned_to_immutable_public_commit(self):
        self.assertEqual(len(self.original), 77)
        self.assertEqual(sum(name.endswith(".py") for name in self.original), 73)
        self.assertIn("LICENSE", self.original)
        self.assertFalse(any(name.endswith(".json") for name in self.original))
        self.assertEqual(root4.sha(self.original[root4.ENTRY]),
                         "82b62e0088cd0055b1bc4b33bf3ca92087cafc62ff6396c679a7baf013672c0e")

    def test_only_monitor_and_four_transitive_hash_callers_change(self):
        changed = {name for name in self.original if self.original[name] != self.derived[name]}
        self.assertEqual(changed, root4.EXPECTED_CHANGED)
        self.assertEqual(self.derived[root4.MONITOR], root4.LINUX_MONITOR)
        self.assertEqual(len(self.epoch["mathematical_ast_projections"]), 72)
        self.assertEqual(root4.sha(root4.canonical(self.epoch)), root4.EPOCH_SHA256)
        self.assertIs(self.epoch["mathematical_arithmetic_accepted"], False)
        self.assertIs(self.epoch["all_index_conclusion_verified"], False)

    def test_every_literal_pin_rebinds_to_actual_derived_source_bytes(self):
        graph, order = root4.pin_graph(self.original)
        self.assertEqual(sum(map(len, graph.values())), 125)
        self.assertEqual(len(order), 73)
        positions = {name: i for i, name in enumerate(order)}
        for name, dependencies in graph.items():
            for dependency in dependencies:
                self.assertLess(positions[dependency], positions[name])
        for name, changes in self.epoch["changes"].items():
            for dependency, pins in changes.get("literal_source_pin_rebindings", {}).items():
                self.assertEqual(pins["old_sha256"], root4.sha(self.original[dependency]))
                self.assertEqual(pins["new_sha256"], root4.sha(self.derived[dependency]))
                self.assertIn(pins["new_sha256"].encode("ascii"), self.derived[name])
                self.assertNotIn(pins["old_sha256"].encode("ascii"), self.derived[name])

    def test_derivation_is_deterministic_under_input_dictionary_reordering(self):
        sources, epoch = root4.derive_sources(dict(reversed(list(self.original.items()))))
        self.assertEqual(sources, self.derived)
        self.assertEqual(root4.canonical(epoch), root4.canonical(self.epoch))

    def test_source_projection_rejects_mathematical_change_but_normalizes_only_pins(self):
        original = b"SCALE=10**40\nPIN='" + b"a"*64 + b"'\n"
        rebound = original.replace(b"a"*64, b"b"*64)
        names = {"a"*64: "helper.py", "b"*64: "helper.py"}
        self.assertEqual(root4.ast_projection(original, names), root4.ast_projection(rebound, names))
        changed_math = rebound.replace(b"10**40", b"10**39")
        self.assertNotEqual(root4.ast_projection(original, names), root4.ast_projection(changed_math, names))

    def test_empty_python_minor_version_ast_fields_do_not_change_epoch(self):
        raw = b"def f(x):\n    return x\n"
        expected = root4.ast_projection(raw, {})
        parsed = root4.tree(raw)
        function = parsed.body[0]
        # CPython 3.11 lacks this field; 3.12+ includes it.  Simulate the other
        # shape while retaining exactly the same program semantics.
        if "type_params" in function._fields:
            function._fields = tuple(name for name in function._fields if name != "type_params")
        else:
            function._fields = function._fields + ("type_params",)
            function.type_params = []
        with patch.object(root4, "tree", return_value=parsed):
            self.assertEqual(root4.ast_projection(raw, {}), expected)

    def test_resource_helper_change_creates_a_different_unsealed_epoch(self):
        with patch.object(root4, "LINUX_MONITOR", root4.LINUX_MONITOR.replace(b"return value * 1024", b"return value")):
            with self.assertRaisesRegex(ValueError, "Exact sealed portable ROOT4 epoch"):
                root4.derive_sources(self.original)

    def test_foreign_literal_source_pin_is_rejected(self):
        sources = dict(self.original)
        old_pin = root4.sha(sources[root4.MONITOR]).encode("ascii")
        name = "n4_cpu_time_quadrature_cache_2026_10_09.py"
        sources[name] = sources[name].replace(old_pin, b"f"*64)
        with self.assertRaisesRegex(ValueError, "Every literal ROOT4 source pin resolves"):
            root4.pin_graph(sources)

    def test_corrupt_frozen_manifest_or_source_is_rejected_before_preparation(self):
        frozen = self.root / "vendor"
        shutil.copytree(root4.VENDOR, frozen)
        source = frozen / root4.ENTRY
        original = source.read_bytes()
        source.write_bytes(original + b"\n")
        with self.assertRaisesRegex(ValueError, "frozen source"):
            root4.prepare(self.root / "bad-capsule", vendor=frozen)
        self.assertFalse((self.root / "bad-capsule").exists())
        source.write_bytes(original)
        with (frozen / "MANIFEST.json").open("ab") as stream:
            stream.write(b" ")
        with self.assertRaisesRegex(ValueError, "Pinned ROOT4 source manifest"):
            root4.verify_frozen(frozen)

    def test_capsule_is_fresh_and_rechecks_every_source_byte(self):
        capsule = self.capsule()
        self.assertEqual(root4.verify_capsule(capsule), self.epoch)
        with self.assertRaisesRegex(ValueError, "no overwrite or resume"):
            root4.prepare(capsule)
        with (capsule / root4.ENTRY).open("ab") as stream:
            stream.write(b"\n")
        with self.assertRaisesRegex(ValueError, "source drift"):
            root4.verify_capsule(capsule)

    def test_unpinned_extra_executable_in_capsule_is_rejected(self):
        capsule = self.capsule()
        (capsule / "injected.py").write_text("raise RuntimeError('must never execute')\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "extra executable Python source"):
            root4.verify_capsule(capsule)

    def test_original_cli_has_exact_producer_then_full_read_only_replay(self):
        capsule = self.root / "ordinary"
        for stage, flag in (("produce", "--produce"), ("replay", "--replay-existing")):
            argv = root4.command(capsule, stage)
            self.assertEqual(argv[1:3], ["-B", "-S"])
            self.assertEqual(argv[-1], flag)
            self.assertEqual(Path(argv[3]), capsule.resolve() / root4.ENTRY)
        with self.assertRaises(ValueError):
            root4.command(capsule, "resume")

    def test_terminal_census_cannot_drop_parents_high_slots_or_unresolved_classes(self):
        capsule = self.root / "ordinary"
        packet = self.terminal(capsule, "produce")
        mutations = (
            lambda p: p["summary"].update(geometry_classes_total=259),
            lambda p: p["summary"].update(ALL_high_request_slots_accounted=1299),
            lambda p: p["summary"].update(closed_geometry_classes=True),
            lambda p: p.update(unresolved_geometry_indices=[0]),
            lambda p: p["summary"].update(entire_conditional_root_score_upper_exact=.4),
            lambda p: p.update(result=str(capsule / "foreign.json")),
            lambda p: p["resources"].update(memory_limit_bytes=512*root4.MIB),
            lambda p: p["resources"].update(actual_CLI_peak_working_set_bytes=None),
            lambda p: p["resources"].update(read_only_replay_wrote_any_checkpoint=True),
        )
        for change in mutations:
            malformed = deepcopy(packet)
            change(malformed)
            with self.subTest(change=change), self.assertRaises(ValueError):
                root4.validate_terminal(malformed, "produce", capsule)

    def test_native_guard_requires_capability_actual_hashes_and_original_worker_caps(self):
        capsule = self.capsule()
        observed = dict(guard_scope=self.guard(capsule))
        self.assertTrue(root4.guard_verified(observed, capsule))
        # proof_acceptance=False is deliberate supervisor scope, not a veto on
        # mathematics which only this caller can check after actual execution.
        self.assertIs(observed["guard_scope"]["proof_acceptance"], False)
        for key, value in (("capability_established", False), ("script_sha256", "0"*64),
                           ("worker_RLIMIT_AS_bytes", 448*root4.MIB),
                           ("worker_RLIMIT_CPU_seconds", 7200),
                           ("supervisor_source_sha256", "0"*64),
                           ("kind", "BASIC_PROCESS_GROUP")):
            changed = deepcopy(observed)
            changed["guard_scope"][key] = value
            with self.subTest(key=key):
                self.assertFalse(root4.guard_verified(changed, capsule))

    def test_actual_monitor_source_uses_kernel_peak_without_dropping_original_gates(self):
        self.assertIn(b"resource.getrusage(resource.RUSAGE_SELF).ru_maxrss", root4.LINUX_MONITOR)
        self.assertIn(b"return value * 1024", root4.LINUX_MONITOR)
        self.assertNotIn(b"return None", root4.LINUX_MONITOR)
        for name in (root4.ENTRY, "n4_cpu_time_high_preparation_2026_10_09.py"):
            self.assertIn(b"peak is not None and peak <=", self.derived[name])
        self.assertIn(b"HIGH_MEMORY_LIMIT = 256 * 1024 * 1024, 64 * 1024 * 1024", self.derived[root4.ENTRY])

    @unittest.skipUnless(sys.platform == "linux", "Actual Linux kernel resource fixture")
    def test_actual_linux_monitor_and_complete_source_closure_under_native_guard(self):
        # Hash/read-only closure checks; no geometry, HIGH, cache, CDF, or root
        # arithmetic producer is called by this tiny platform fixture.
        capsule = self.capsule()
        script = capsule / "source_closure_fixture.py"
        script.write_text(
            "import json\n"
            "import n4_cpu_time_entire_root_2026_10_09 as root\n"
            "root.source_drift_check()\n"
            "pins=root.dependency_pins()\n"
            "peak=root.resources.peak_bytes()\n"
            "current=root.resources.current_working_set_bytes()\n"
            "assert type(peak) is int and peak>0 and type(current) is int and current>0\n"
            "assert peak<=64*1024*1024\n"
            "print(json.dumps(dict(fixture='SOURCE_CLOSURE_ONLY_NO_MATH',sources=len(pins),"
            "peak=peak,current=current)))\n", encoding="utf-8")
        observed = root4.supervise([sys.executable, "-B", "-S", str(script)], cwd=capsule,
                                  output_dir=self.root / "actual-linux-closure", wall_seconds=60,
                                  cpu_seconds=60, memory_bytes=320*root4.MIB, mode="trusted_native")
        self.assertEqual(observed["status"], "completed", observed)
        self.assertEqual(observed["returncode"], 0, observed)
        self.assertIs(observed["guard_scope"].get("capability_established"), True)
        packet = json.loads(Path(observed["stdout_path"]).read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual(packet["fixture"], "SOURCE_CLOSURE_ONLY_NO_MATH")
        self.assertGreater(packet["sources"], 60)
        self.assertGreater(packet["peak"], 0)
        self.assertGreater(packet["current"], 0)

    def test_failed_native_process_exposes_actual_stderr_without_acceptance(self):
        stderr = self.root / "stderr.txt"
        stderr.write_bytes(b"not-the-whole-log\n" + b"x"*10000 + b"\nactual root import failure")
        observed = dict(status="incomplete", reason="nonzero_subprocess_exit", returncode=1,
                        stderr_path=str(stderr), stdout_path=str(self.root / "stdout.txt"))
        with self.assertRaisesRegex(ValueError, "actual root import failure") as caught:
            root4.terminal_packet(observed)
        self.assertIn("nonzero_subprocess_exit", str(caught.exception))
        self.assertNotIn("not-the-whole-log", str(caught.exception))

    def test_actual_capture_hashes_and_empty_stderr_are_required(self):
        stdout, stderr = self.root / "stdout.txt", self.root / "stderr.txt"
        raw = b'{"fixture_only":true}\n'
        stdout.write_bytes(raw)
        stderr.write_bytes(b"")
        observed = dict(status="completed", returncode=0, stdout_path=str(stdout), stderr_path=str(stderr),
                        stdout_sha256=root4.digest(stdout), stderr_sha256=root4.digest(stderr))
        self.assertEqual(root4.terminal_packet(observed), {"fixture_only": True})
        stdout.write_bytes(raw + b" ")
        with self.assertRaisesRegex(ValueError, "stdout capture matches"):
            root4.terminal_packet(observed)
        stdout.write_bytes(raw)
        stderr.write_bytes(b"actual stderr must not be ignored\n")
        with self.assertRaisesRegex(ValueError, "stderr capture matches"):
            root4.terminal_packet(observed)
        observed["stderr_sha256"] = root4.digest(stderr)
        with self.assertRaisesRegex(ValueError, "empty stderr"):
            root4.terminal_packet(observed)

    def test_warning_environment_is_narrow_and_restored(self):
        with patch.dict(os.environ, {"PYTHONWARNINGS": "error::RuntimeWarning"}):
            with root4.syntax_warning_policy():
                self.assertEqual(os.environ["PYTHONWARNINGS"],
                                 "error::RuntimeWarning,ignore:invalid escape sequence:SyntaxWarning")
            self.assertEqual(os.environ["PYTHONWARNINGS"], "error::RuntimeWarning")
        with patch.dict(os.environ, clear=True):
            with root4.syntax_warning_policy():
                self.assertEqual(os.environ["PYTHONWARNINGS"], "ignore:invalid escape sequence:SyntaxWarning")
            self.assertNotIn("PYTHONWARNINGS", os.environ)

    def test_two_full_modes_run_with_real_source_preparation_but_fixture_execution(self):
        # The source derivation itself is separately checked above. Reuse its
        # exact bytes for orchestration fixtures, retaining real file rehashes.
        with patch.object(root4, "derive_sources", return_value=(self.derived, self.epoch)), \
                patch.object(root4, "supervise", side_effect=self.fake_native()) as native, redirect_stdout(io.StringIO()):
            result = root4.run(self.root / "two-pass")
        self.assertEqual(native.call_count, 2)
        self.assertEqual([row["stage"] for row in result["stages"]], ["produce", "replay"])
        self.assertTrue(result["all_required_stages_computed"])
        self.assertTrue(result["native_arithmetic_accepted"])
        self.assertTrue(result["conditional_physical_root_verified"])
        self.assertFalse(result["all_law_C4_verified"])
        self.assertFalse(result["all_index_conclusion_verified"])

    def test_complete_unknown_two_pass_result_is_kept_without_acceptance(self):
        with patch.object(root4, "derive_sources", return_value=(self.derived, self.epoch)), \
                patch.object(root4, "supervise", side_effect=self.fake_native(pending=(17,))), redirect_stdout(io.StringIO()):
            result = root4.run(self.root / "unknown")
        self.assertTrue(result["all_required_stages_computed"])
        self.assertFalse(result["native_arithmetic_accepted"])
        self.assertEqual(result["stages"][1]["unresolved_geometry_indices"], [17])

    def test_changed_replay_receipt_is_rejected_and_observation_preserved(self):
        output = self.root / "changed"
        with patch.object(root4, "derive_sources", return_value=(self.derived, self.epoch)), \
                patch.object(root4, "supervise", side_effect=self.fake_native(change_replay=True)), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, "preserves every receipt byte"):
                root4.run(output)
        record = root4.read(output / "ROOT4_RESULT.json")
        self.assertFalse(record["native_arithmetic_accepted"])
        self.assertEqual(len(record["stages"]), 2)
        self.assertFalse(record["stages"][1]["completed"])

    def test_weak_guard_never_falls_back_or_accepts_terminal_marker(self):
        output = self.root / "weak"
        with patch.object(root4, "derive_sources", return_value=(self.derived, self.epoch)), \
                patch.object(root4, "supervise", side_effect=self.fake_native(weak_guard=True)) as native, redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, "no basic-guard acceptance"):
                root4.run(output)
        self.assertEqual(native.call_count, 1)
        self.assertFalse(root4.read(output / "ROOT4_RESULT.json")["native_arithmetic_accepted"])


if __name__ == "__main__":
    unittest.main()
