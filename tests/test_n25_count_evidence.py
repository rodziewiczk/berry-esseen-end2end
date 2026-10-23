"""Synthetic native-evidence fixtures; trap source code is never executed."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from be_replay import count_task as count, linux_supervisor as supervisor, n25_count_evidence as evidence


class N25CountEvidenceTests(unittest.TestCase):
    def setUp(self):
        parent = count.ROOT / "work" / "n25-count-evidence-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.task = self.root / "task"
        self.source = self.task / "capsule"
        self.source.mkdir(parents=True)
        labels = ["fixture-control-" + str(i) for i in range(24)]
        protocol = "raise AssertionError('No numerical source may execute in evidence fixtures')\n"
        protocol += "def header(bound):return dict(schema='TRAP_FOREST_V1',n=25,index=33)\n"
        protocol += "def accept():\n mutations = [" + ",".join("("+repr(s)+",lambda x: None)" for s in labels) + "]\n"
        (self.source / "count_protocol.py").write_text(protocol)
        (self.source / "kernel.py").write_text("raise AssertionError('Kernel import forbidden')\n")
        (self.source / "contract.json").write_text('{"fixture_only":true}\n')
        self.kernel = {"kernel.py": count.digest(self.source / "kernel.py")}
        count.write(self.source / "KERNEL_COPY_MANIFEST.json", dict(files=self.kernel))
        files = {p.name: count.digest(p) for p in self.source.iterdir()}
        count.write(self.source / "FROZEN_DESIGN.json", dict(files=files))
        self.pin = count.digest(self.source / "FROZEN_DESIGN.json")
        self.patch = patch.object(count, "TARGETS", dict(count.TARGETS, **{"b3-p33": ("original-v12", 33, self.pin)}))
        self.patch.start()
        self.addCleanup(self.patch.stop)
        count.write(self.task / "TASK.json", dict(schema="COUNT_TASK_V1", target="b3-p33", scope=count.scope("b3-p33"),
                    source_commit=count.COMMIT, design_sha256=self.pin, prepared_source_files=len(files),
                    source_archives=dict(old=count.ASSETS["old"]), preparation_result=dict(fixture=True),
                    implementation=count.implementation(), arithmetic_accepted=False,
                    parent_acquisitions_verified=False, all_index_conclusion_verified=False))
        self.epoch = self.task / "accept-0123456789ab"
        self.capsule = self.epoch / "capsule"
        shutil.copytree(self.source, self.capsule)
        forest = dict(**count.native_header(self.capsule, "b3-p33"), roots=[dict(k=k, tree=dict(kind="leaf", box=[], decision="EMPTY_FIXTURE", result={})) for k in range(26)])
        count.write(self.capsule / "COUNT33_FOREST.json", forest)
        receipt = dict(status="PASS_FRESH_CONDITIONAL_EXACT_COUNT33", fresh_leaf_evaluations=26,
                       negative_controls=labels, statistics=dict(nodes=26, leaves=26, closed_statuses=dict(EMPTY_FIXTURE=26), maximum_depth=0, maximum_score="0"),
                       forest_sha256=count.digest(self.capsule / "COUNT33_FOREST.json"), contract_sha256=count.digest(self.capsule / "contract.json"),
                       checker_sha256=count.digest(self.capsule / "count_protocol.py"), kernel_sha256=self.kernel)
        count.write(self.capsule / "COUNT33_ACCEPTED.json", receipt)
        self.execution = self.epoch / "execution"
        self.execution.mkdir()
        (self.execution / "stdout.txt").write_text(json.dumps(receipt, indent=2) + "\n")
        (self.execution / "stderr.txt").write_bytes(b"")
        launch = dict(argv=["/original/python", "-B", "-S", str(self.capsule / "count_protocol.py"), "accept"],
                      cwd=str(self.capsule), output_dir=str(self.execution), wall_seconds=7260.0, cpu_seconds=7200,
                      memory_bytes=512*count.MIB, checkpoint_paths=[], mode="trusted_native", sample_seconds=.2,
                      disk_bytes=256*count.MIB, log_bytes=16*count.MIB, heartbeat_seconds=20.0,
                      supervisor_memory_bytes=64*count.MIB, worker_memory_bytes=448*count.MIB,
                      supervisor_cpu_seconds=30, worker_cpu_seconds=7170)
        count.write(self.execution / "native-launch.json", launch)
        outer = dict(launch, argv=["/original/python", "-B", "-S", "/old/repo/be_replay/linux_supervisor.py", "--_native-controller", str(self.execution / "native-launch.json")])
        count.write(self.execution / "launch.json", outer)
        instructions, architecture, denied, prlimit = supervisor._filter_instructions("x86_64")
        base = dict(seccomp_mode=2, no_new_privileges=True, audit_architecture=architecture, machine="x86_64",
                    denied_syscalls=denied, prlimit64_query_only=prlimit, x32_or_unknown_syscall_ABI_killed=True,
                    filter_instructions_sha256=hashlib.sha256(json.dumps(instructions).encode()).hexdigest())
        worker = dict(base, address_space_bytes=448*count.MIB, cpu_seconds=7170, script_sha256=receipt["checker_sha256"], pid=200, birth_tick=100)
        controller = dict(base, address_space_bytes=64*count.MIB, cpu_seconds=30, pid=199, birth_tick=99)
        count.write(self.execution / "native-worker-guard.json", worker)
        count.write(self.execution / "native-controller-guard.json", controller)
        count.write(self.execution / "native-controller-result.json", dict(returncode=0, worker_pid=200, worker_source_sha256_after=receipt["checker_sha256"]))
        guard = dict(kind="LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1", capability_established=True, native_python_execution=True,
                     hard_sum_RLIMIT_AS_bytes=512*count.MIB, worker_RLIMIT_AS_bytes=448*count.MIB, supervisor_RLIMIT_AS_bytes=64*count.MIB,
                     hard_sum_RLIMIT_CPU_seconds=7200, worker_RLIMIT_CPU_seconds=7170, supervisor_RLIMIT_CPU_seconds=30,
                     script_sha256=receipt["checker_sha256"], supervisor_source_sha256=count.digest(Path(count.__file__).with_name("linux_supervisor.py")),
                     worker_guard=worker, supervisor_guard=controller)
        observed = dict(status="completed", returncode=0, mode="trusted_native", proof_accepted=False,
                        stdout_path=str(self.execution / "stdout.txt"), stderr_path=str(self.execution / "stderr.txt"),
                        stdout_sha256=count.digest(self.execution / "stdout.txt"), stderr_sha256=count.digest(self.execution / "stderr.txt"), guard_scope=guard)
        count.write(self.execution / "supervisor-result.json", observed)
        before = dict(schema="COUNT_NATIVE_EXECUTION_V1", target="b3-p33", scope=count.scope("b3-p33"), epoch=str(self.epoch),
                      observed=observed, census=dict(nodes=26, leaves=26, roots=26), implementation=count.implementation(),
                      arithmetic_accepted=False, parent_acquisitions_verified=False, all_index_conclusion_verified=False)
        count.write(self.epoch / "NATIVE_OBSERVED.json", before)
        accepted = dict(before, arithmetic_accepted=True, native_receipt=str(self.capsule / "COUNT33_ACCEPTED.json"),
                        native_receipt_sha256=count.digest(self.capsule / "COUNT33_ACCEPTED.json"), negative_controls=24,
                        conditional_premises=evidence.PREMISES)
        count.write(self.epoch / "NATIVE_ACCEPTED.json", accepted)

    def alter(self, path, change):
        obj = count.read(path)
        change(obj)
        path.unlink()
        count.write(path, obj)

    def rejection(self):
        with self.assertRaisesRegex(ValueError, "No fully revalidated"):
            evidence.validate_completed(self.task)

    def test_complete_fixture_revalidates_without_any_kernel_import_or_execution(self):
        with patch.object(count, "supervise", side_effect=AssertionError("Never execute")):
            result = evidence.validate_completed(self.task, expected_target="b3-p33")
        self.assertEqual(result["schema"], "REVALIDATED_N25_COUNT_V1")
        self.assertEqual((result["branch"], result["n"], result["index"]), ("b3", 25, 33))
        self.assertTrue(result["native_arithmetic_accepted"])
        self.assertFalse(result["parent_acquisitions_verified"])
        self.assertEqual(result["census"], dict(nodes=26, leaves=26, roots=26))
        self.assertEqual(result["accepted_capsule_relative"], "accept-0123456789ab/capsule")
        self.assertEqual(result["accepted_report_sha256"], count.digest(self.epoch / "NATIVE_ACCEPTED.json"))

    def test_relocation_preserves_original_receipt_and_launch_context(self):
        original = str(self.task)
        other = self.root / "restored" / "task"
        shutil.copytree(self.task, other)
        original_bytes = (self.epoch / "NATIVE_ACCEPTED.json").read_bytes()
        shutil.rmtree(self.task)
        result = evidence.validate_completed(other, original_task_root=original)
        self.assertEqual(result["original_task_root"], original)
        self.assertEqual((other / result["accepted_report_relative"]).read_bytes(), original_bytes)
        with self.assertRaises(ValueError):
            evidence.validate_completed(other, original_task_root="/another/original/task")

    def test_recorded_python_version_is_context_not_current_runtime_requirement(self):
        for path in (self.task / "TASK.json", self.epoch / "NATIVE_OBSERVED.json", self.epoch / "NATIVE_ACCEPTED.json"):
            self.alter(path, lambda x: x["implementation"].update(python="Original interpreter context, intentionally different"))
        self.assertTrue(evidence.validate_completed(self.task)["native_arithmetic_accepted"])

    def test_wrong_target_and_changed_driver_pin_are_rejected(self):
        with self.assertRaises(ValueError):
            evidence.validate_completed(self.task, expected_target="b4-q0")
        self.alter(self.task / "TASK.json", lambda x: x["implementation"].update(count_task_sha256="0"*64))
        with self.assertRaisesRegex(ValueError, "implementation pins"):
            evidence.validate_completed(self.task)

    def test_missing_unaccepted_observation_cannot_be_filled_by_an_accepted_receipt(self):
        (self.epoch / "NATIVE_OBSERVED.json").unlink()
        self.rejection()

    def test_modified_observed_to_accepted_transition_is_rejected(self):
        self.alter(self.epoch / "NATIVE_OBSERVED.json", lambda x: x.update(arithmetic_accepted=True))
        self.rejection()

    def test_false_returncode_and_missing_capability_fail_closed(self):
        for path in (self.epoch / "NATIVE_OBSERVED.json", self.epoch / "NATIVE_ACCEPTED.json"):
            self.alter(path, lambda x: x["observed"].update(returncode=False))
        self.alter(self.execution / "supervisor-result.json", lambda x: x.update(returncode=False))
        self.rejection()

    def test_empty_stderr_wrong_hash_is_rejected(self):
        for path in (self.epoch / "NATIVE_OBSERVED.json", self.epoch / "NATIVE_ACCEPTED.json"):
            self.alter(path, lambda x: x["observed"].update(stderr_sha256="0"*64))
        self.alter(self.execution / "supervisor-result.json", lambda x: x.update(stderr_sha256="0"*64))
        self.rejection()

    def test_nonempty_stderr_and_tampered_stdout_are_rejected(self):
        (self.execution / "stderr.txt").write_text("unexpected diagnostic")
        self.rejection()
        (self.execution / "stderr.txt").write_bytes(b"")
        (self.execution / "stdout.txt").write_text("{}\n")
        self.rejection()

    def test_missing_launch_or_changed_controller_command_is_rejected(self):
        self.alter(self.execution / "launch.json", lambda x: x["argv"].__setitem__(4, "--_exec-search"))
        self.rejection()
        (self.execution / "native-launch.json").unlink()
        self.rejection()

    def test_actual_guard_artifact_must_match_nested_observation(self):
        self.alter(self.execution / "native-worker-guard.json", lambda x: x.update(cpu_seconds=1))
        self.rejection()

    def test_incomplete_newer_acceptance_does_not_hide_older_complete_evidence(self):
        newer = self.task / "accept-fedcba987654"
        newer.mkdir()
        count.write(newer / "NATIVE_ACCEPTED.json", dict(status="not complete"))
        result = evidence.validate_completed(self.task)
        self.assertEqual(result["accepted_capsule_relative"], "accept-0123456789ab/capsule")

    def test_unlisted_capsule_output_and_changed_forest_are_rejected(self):
        (self.capsule / "extra-output.json").write_text("{}")
        self.rejection()
        (self.capsule / "extra-output.json").unlink()
        self.alter(self.capsule / "COUNT33_FOREST.json", lambda x: x["roots"].pop())
        self.rejection()

    def test_source_and_native_clone_must_both_match_original_sealed_design(self):
        with (self.source / "kernel.py").open("a") as out:
            out.write("\n")
        with self.assertRaises(ValueError):
            evidence.validate_completed(self.task)

    def test_control_labels_are_read_from_ast_without_evaluating_lambdas(self):
        labels = evidence.control_labels(self.capsule / "count_protocol.py")
        self.assertEqual(len(labels), 24)
        self.alter(self.capsule / "COUNT33_ACCEPTED.json", lambda x: x["negative_controls"].reverse())
        self.rejection()


if __name__ == "__main__":
    unittest.main()
