"""Synthetic source/transport fixtures; no proof kernel or native worker runs."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from be_replay import (count_recovery as runner, count_recovery_evidence as evidence,
    count_limit_epoch as limit, count_task as count, linux_supervisor as supervisor,
    n25_collect as collector)


class RecoveryEvidenceTests(unittest.TestCase):
    def setUp(self):
        parent = count.ROOT / "work/count-recovery-evidence-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = self.root / "backup/capsule"
        source.mkdir(parents=True)
        self.labels = ["fixture-control-" + str(i) for i in range(24)]
        protocol = "raise AssertionError('Synthetic protocol must never execute')\nLIMIT=10000\n"
        protocol += "def header(bound):return dict(schema='SYNTHETIC_FOREST_V1',n=25,index=29)\n"
        protocol += "def construct():\n visited=1\n need(visited<=LIMIT,'resource')\n"
        protocol += "def replay():\n visited=1\n need(visited<=LIMIT,'resource')\n"
        protocol += "def accept():\n mutations=[" + ",".join("("+repr(s)+",lambda x: None)" for s in self.labels) + "]\n"
        payload = {"count_protocol.py": protocol.encode(), "kernel.py": b"raise AssertionError('No kernel import')\n",
                   "contract.json": b'{"synthetic_only":true}\n'}
        self.kernel = {"kernel.py": limit.sha(payload["kernel.py"])}
        payload["KERNEL_COPY_MANIFEST.json"] = limit.encoded(dict(files=self.kernel))
        design = limit.encoded(dict(files={k: limit.sha(v) for k, v in payload.items()}))
        payload["FROZEN_DESIGN.json"] = design
        for name, raw in payload.items():
            (source / name).write_bytes(raw)
        for name, value in (("ORIGINAL_DESIGN_SHA256", limit.sha(design)),
                            ("ORIGINAL_CHECKER_SHA256", limit.sha(payload["count_protocol.py"]))):
            p = patch.object(limit, name, value); p.start(); self.addCleanup(p.stop)
        p = patch.object(count, "TARGETS", dict(count.TARGETS,
            **{"b4-q2": ("original-v12", 29, limit.ORIGINAL_DESIGN_SHA256)}))
        p.start(); self.addCleanup(p.stop)
        files, derived, checker, _ = limit._derive(design, payload["count_protocol.py"])
        for name, value in (("NEW_DESIGN_SHA256", limit.sha(derived)), ("DESIGN_SHA256", limit.sha(derived)),
                            ("CHECKER_SHA256", limit.sha(checker)), ("CONTRACT_SHA256", files["contract.json"])):
            p = patch.object(limit, name, value); p.start(); self.addCleanup(p.stop)
        checkpoint = dict(schema="UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1", arithmetic_accepted=False,
            binding=dict(design_sha256=limit.ORIGINAL_DESIGN_SHA256, alpha_priority="4", traversal="root-first",
                         native_header=dict(count.native_header(source, "b4-q2"), target="synthetic strict target")),
            roots=[dict(k=k, tree=dict(kind="pending")) for k in range(26)])
        count.write(source.parent / "CHECKPOINT.json", checkpoint)
        self.task = self.root / "task"
        runner.prepare(self.task, [source.parent])
        self.epoch = self.task / "accept-0123456789ab"
        self.capsule = self.epoch / "capsule"
        shutil.copytree(self.task / "capsule", self.capsule)
        forest = dict(**count.native_header(self.capsule, "b4-q2"),
            roots=[dict(k=k, tree=dict(kind="leaf", box=[], decision="EMPTY_SYNTHETIC", result={})) for k in range(26)])
        count.write(self.capsule / "COUNT29_FOREST.json", forest)
        self.save_native(forest)

    def save_native(self, forest):
        def write(path, value):
            path.write_text(json.dumps(value, indent=2)+"\n", encoding="utf-8")
        write(self.capsule / "COUNT29_FOREST.json", forest)
        census = limit.forest_census(forest, "b4-q2", self.capsule)
        receipt = dict(status="PASS_FRESH_CONDITIONAL_EXACT_COUNT29", fresh_leaf_evaluations=census["leaves"],
            negative_controls=self.labels, statistics=dict(**census, **evidence.full_statistics(forest)),
            forest_sha256=count.digest(self.capsule / "COUNT29_FOREST.json"),
            contract_sha256=count.digest(self.capsule / "contract.json"),
            checker_sha256=count.digest(self.capsule / "count_protocol.py"), kernel_sha256=self.kernel)
        receipt["statistics"].pop("roots")
        write(self.capsule / "COUNT29_ACCEPTED.json", receipt)
        self.execution = self.epoch / "execution"
        self.execution.mkdir(exist_ok=True)
        (self.execution / "stdout.txt").write_text(json.dumps(receipt, indent=2)+"\n")
        (self.execution / "stderr.txt").write_bytes(b"")
        native = dict(argv=["/original/python", "-B", "-S", str(self.capsule / "count_protocol.py"), "accept"],
            cwd=str(self.capsule), output_dir=str(self.execution), wall_seconds=7260.0, cpu_seconds=7200,
            memory_bytes=512*count.MIB, checkpoint_paths=[], mode="trusted_native", sample_seconds=.2,
            disk_bytes=256*count.MIB, log_bytes=16*count.MIB, heartbeat_seconds=20.0,
            supervisor_memory_bytes=64*count.MIB, worker_memory_bytes=448*count.MIB,
            supervisor_cpu_seconds=30, worker_cpu_seconds=7170)
        write(self.execution / "native-launch.json", native)
        write(self.execution / "launch.json", dict(native, argv=["/original/python", "-B", "-S",
            "/old/repo/be_replay/linux_supervisor.py", "--_native-controller", str(self.execution / "native-launch.json")]))
        instructions, architecture, denied, prlimit = supervisor._filter_instructions("x86_64")
        base = dict(seccomp_mode=2, no_new_privileges=True, audit_architecture=architecture, machine="x86_64",
            denied_syscalls=denied, prlimit64_query_only=prlimit, x32_or_unknown_syscall_ABI_killed=True,
            filter_instructions_sha256=hashlib.sha256(json.dumps(instructions).encode()).hexdigest())
        worker = dict(base, address_space_bytes=448*count.MIB, cpu_seconds=7170,
                      script_sha256=receipt["checker_sha256"], pid=200, birth_tick=100)
        controller = dict(base, address_space_bytes=64*count.MIB, cpu_seconds=30, pid=199, birth_tick=99)
        write(self.execution / "native-worker-guard.json", worker)
        write(self.execution / "native-controller-guard.json", controller)
        write(self.execution / "native-controller-result.json", dict(returncode=0, worker_pid=200,
            worker_source_sha256_after=receipt["checker_sha256"]))
        guard = dict(kind="LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1", capability_established=True, native_python_execution=True,
            hard_sum_RLIMIT_AS_bytes=512*count.MIB, worker_RLIMIT_AS_bytes=448*count.MIB, supervisor_RLIMIT_AS_bytes=64*count.MIB,
            hard_sum_RLIMIT_CPU_seconds=7200, worker_RLIMIT_CPU_seconds=7170, supervisor_RLIMIT_CPU_seconds=30,
            script_sha256=receipt["checker_sha256"], supervisor_source_sha256=count.digest(supervisor.__file__),
            worker_guard=worker, supervisor_guard=controller)
        observed = dict(status="completed", returncode=0, mode="trusted_native", proof_accepted=False,
            stdout_path=str(self.execution / "stdout.txt"), stderr_path=str(self.execution / "stderr.txt"),
            stdout_sha256=count.digest(self.execution / "stdout.txt"), stderr_sha256=count.digest(self.execution / "stderr.txt"), guard_scope=guard)
        write(self.execution / "supervisor-result.json", observed)
        before = dict(schema="COUNT_LIMIT_RECOVERY_EXECUTION_V1", target="b4-q2", scope=evidence.SCOPE,
            epoch=str(self.epoch), observed=observed, census=census, implementation=runner.implementation(),
            arithmetic_accepted=False, parent_acquisitions_verified=False, all_index_conclusion_verified=False)
        write(self.epoch / "NATIVE_OBSERVED.json", before)
        write(self.epoch / "NATIVE_ACCEPTED.json", dict(before, arithmetic_accepted=True,
            native_receipt=str(self.capsule / "COUNT29_ACCEPTED.json"), native_receipt_sha256=count.digest(self.capsule / "COUNT29_ACCEPTED.json"),
            negative_controls=24, conditional_premises=evidence.PREMISES))

    def alter(self, path, action):
        value = count.read(path); action(value)
        path.write_text(json.dumps(value, indent=2)+"\n", encoding="utf-8")

    def reject(self):
        with self.assertRaises((ValueError, KeyError)):
            evidence.validate_completed(self.task, expected_target="b4-q2")

    def test_complete_recovery_export_revalidates_without_execution(self):
        before = {p.relative_to(self.task).as_posix(): count.digest(p) for p in self.task.rglob("*") if p.is_file()}
        with patch.object(count, "supervise", side_effect=AssertionError("No native run")):
            result = evidence.validate_export(self.task, expected_target="b4-q2")
        self.assertEqual(result["resource_epoch"]["node_limit"], 100000)
        self.assertEqual(result["original_design_sha256"], limit.ORIGINAL_DESIGN_SHA256)
        self.assertEqual(result["new_design_sha256"], limit.NEW_DESIGN_SHA256)
        self.assertTrue(result["native_arithmetic_accepted"])
        self.assertFalse(result["parent_acquisitions_verified"])
        self.assertEqual(before, {p.relative_to(self.task).as_posix(): count.digest(p) for p in self.task.rglob("*") if p.is_file()})

    def test_relocation_preserves_original_paths_and_receipts(self):
        old = self.task
        self.task = self.root / "restored"
        shutil.copytree(old, self.task); shutil.rmtree(old)
        result = evidence.validate_completed(self.task, original_task_root=old)
        self.assertEqual(result["original_task_root"], str(old))
        self.assertEqual(result["census"]["roots"], 26)

    def test_old_epoch_schema_or_unrelated_target_rejected(self):
        self.alter(self.task / "TASK.json", lambda x: x.update(schema="COUNT_TASK_V1"))
        self.reject()
        with self.assertRaises(ValueError):
            evidence.validate_completed(self.task, expected_target="b4-q1")

    def test_captures_and_guard_sidecars_fail_closed(self):
        (self.execution / "stderr.txt").write_bytes(b"warning")
        self.reject()
        (self.execution / "stderr.txt").write_bytes(b"")
        (self.execution / "native-worker-guard.json").unlink()
        self.reject()

    def test_source_and_checkpoint_migration_are_revalidated(self):
        self.alter(self.task / "INPUT_CHECKPOINT.json", lambda x: x["roots"].pop())
        self.reject()

    def test_all_controls_and_current_implementation_are_required(self):
        self.alter(self.epoch / "NATIVE_ACCEPTED.json", lambda x: x["implementation"].update(count_recovery_sha256="0"*64))
        self.reject()

    def test_changed_control_order_rejected_with_other_bindings_refreshed(self):
        self.labels.reverse()
        self.save_native(count.read(self.capsule / "COUNT29_FOREST.json"))
        self.reject()

    def test_empty_capture_wrong_hash_and_changed_native_cwd_rejected(self):
        self.alter(self.epoch / "NATIVE_ACCEPTED.json",
            lambda x: x["observed"].update(stderr_sha256="0"*64))
        self.reject()
        self.save_native(count.read(self.capsule / "COUNT29_FOREST.json"))
        self.alter(self.execution / "native-launch.json", lambda x: x.update(cwd="/outside"))
        self.reject()

    def test_source_design_or_limit_cannot_be_relabeled(self):
        self.alter(self.task / "TASK.json", lambda x: x.update(node_limit=True))
        self.reject()

    def test_full_census_accepts_only_explicit_larger_cap(self):
        forest = count.read(self.capsule / "COUNT29_FOREST.json")
        def balanced(leaves):
            if leaves == 1:
                return dict(kind="leaf", box=[], decision="EMPTY_SYNTHETIC", result={})
            a = leaves//2
            return dict(kind="split", axis=0, cut="1/2", left=balanced(a), right=balanced(leaves-a))
        forest["roots"][0]["tree"] = balanced(5001)
        self.save_native(forest)
        result = evidence.validate_completed(self.task)
        self.assertGreater(result["census"]["nodes"], 10000)
        self.assertLessEqual(result["census"]["nodes"], 100000)

    def test_collector_only_dispatches_q2_new_task_schema(self):
        ordinary = SimpleNamespace(validate_completed=lambda *a, **k: (_ for _ in ()).throw(AssertionError("No old validator")))
        packet, validator = collector.validate_count_export(self.task, "b4-q2", ordinary)
        self.assertIs(validator, evidence)
        collector.validate_scope("b4-q2", packet)
        with self.assertRaises(ValueError):
            collector.validate_count_export(self.task, "b4-q1", ordinary)
        packet["resource_epoch"]["node_limit"] = 1000000
        with self.assertRaises(ValueError):
            collector.validate_scope("b4-q2", packet)

    def test_ordinary_dispatch_still_delegates_to_existing_validator(self):
        directory = self.root / "ordinary"
        directory.mkdir()
        expected = dict(marker="synthetic ordinary validator")
        ordinary = SimpleNamespace(validate_completed=lambda *a, **k: expected)
        packet, validator = collector.validate_count_export(directory, "b3-p33", ordinary)
        self.assertIs(packet, expected)
        self.assertIs(validator, ordinary)


if __name__ == "__main__":
    unittest.main()
