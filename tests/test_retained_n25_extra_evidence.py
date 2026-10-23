"""Synthetic capture/guard fixtures; archived numerical code cannot execute."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from be_replay import (count_task as common, linux_supervisor as supervisor,
                       retained_n25_extra_evidence as evidence)


class RetainedEvidenceTests(unittest.TestCase):
    def setUp(self):
        parent = common.ROOT/"work"/"retained-evidence-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.task = self.root/"task"
        self.job = dict(job_id="b0-p37", target_id="b0-p37", branch="b0", index=37,
            capsule_relative="capsules/b0-p37", forest_filename="COUNT37_FOREST.json",
            acceptance_filename="COUNT37_ACCEPTED.json", manifest_filename="KERNEL_COPY_MANIFEST.json")
        self.source = self.task/self.job["capsule_relative"]
        self.source.mkdir(parents=True)
        self.labels = ["fixture-control-"+str(i) for i in range(24)]
        self.scope = "Conditional fixture count only; original parent acquisition remains open."
        protocol = "raise AssertionError('No archived code may be executed')\n"
        protocol += "def accept():\n mutations=["+",".join("("+repr(s)+",lambda x:None)" for s in self.labels)+"]\n"
        protocol += " out=dict(status='PASS_FRESH_CONDITIONAL_EXACT_COUNT37',scope="+repr(self.scope)+")\n"
        (self.source/"count_protocol.py").write_text(protocol, encoding="utf-8")
        (self.source/"kernel.py").write_text("raise AssertionError('No numerical kernel import')\n", encoding="utf-8")
        common.write(self.source/"contract.json", dict(fixture_only=True))
        kernel = {"kernel.py": common.digest(self.source/"kernel.py")}
        common.write(self.source/"KERNEL_COPY_MANIFEST.json", dict(files=kernel))
        common.write(self.source/"EXTRA_SOURCE_EPOCH.json", dict(files={p.name:common.digest(p) for p in self.source.iterdir()}))
        common.write(self.source/"COUNT37_FOREST.json", dict(roots=[dict(k=k, tree=dict(kind="leaf")) for k in range(26)]))
        self.files = [dict(filename=p.name, bytes=p.stat().st_size, sha256=common.digest(p), role="source")
                      for p in sorted(self.source.iterdir())]
        self.manifest = dict(branch="b0", jobs=[dict(job_id="b0-p37", files=self.files)])
        common.write(self.task/"SOURCES.json", self.manifest)
        self.census = dict(nodes=26, leaves=26, roots=26, splits=0, maximum_depth=0,
                           closed_statuses=dict(EMPTY_FIXTURE=26), maximum_score="0")
        self.patches = [patch.object(evidence.sources, "verify", return_value=self.manifest),
                        patch.object(evidence.sources, "jobs", return_value=[self.job]),
                        patch.object(evidence.sources, "census", return_value=self.census),
                        patch.object(evidence, "implementation", return_value={
                            "retained_n25_sha256":"1"*64, "source_adapter_sha256":"2"*64,
                            "catalog_sha256":"3"*64, "supervisor_sha256":common.digest(supervisor.__file__),
                            "native_guard_verifier_sha256":"4"*64, "native_evidence_helpers_sha256":"5"*64,
                            "retained_evidence_sha256":"6"*64, "python":"fixture interpreter"})]
        for item in self.patches:
            item.start(); self.addCleanup(item.stop)
        self.epoch = self.task/"accept-0123456789ab"
        self.capsule = self.epoch/"capsule"
        shutil.copytree(self.source, self.capsule)
        self.execution = self.epoch/"execution"
        self.execution.mkdir()
        stats = {k:self.census[k] for k in ("nodes", "leaves", "closed_statuses", "maximum_score", "maximum_depth")}
        self.receipt = dict(status="PASS_FRESH_CONDITIONAL_EXACT_COUNT37", forest_sha256=common.digest(self.capsule/"COUNT37_FOREST.json"),
            contract_sha256=common.digest(self.capsule/"contract.json"), checker_sha256=common.digest(self.capsule/"count_protocol.py"),
            kernel_sha256=kernel, statistics=stats, negative_controls=self.labels, fresh_leaf_evaluations=26,
            seconds=1.25, scope=self.scope)
        common.write(self.capsule/"COUNT37_ACCEPTED.json", self.receipt)
        (self.execution/"stdout.txt").write_text(json.dumps(self.receipt, indent=2)+"\n", encoding="utf-8")
        (self.execution/"stderr.txt").write_bytes(b"")
        launch = dict(argv=["/original/python", "-B", "-S", str(self.capsule/"count_protocol.py"), "accept"],
            cwd=str(self.capsule), output_dir=str(self.execution), wall_seconds=43500, cpu_seconds=43200,
            memory_bytes=evidence.MEMORY, checkpoint_paths=[], mode="trusted_native", sample_seconds=.2,
            disk_bytes=256*common.MIB, log_bytes=16*common.MIB, heartbeat_seconds=20.0,
            supervisor_memory_bytes=64*common.MIB, worker_memory_bytes=evidence.MEMORY-64*common.MIB,
            supervisor_cpu_seconds=30, worker_cpu_seconds=43170)
        common.write(self.execution/"native-launch.json", launch)
        common.write(self.execution/"launch.json", dict(launch, argv=["/original/python", "-B", "-S",
            "/original/repo/be_replay/linux_supervisor.py", "--_native-controller", str(self.execution/"native-launch.json")]))
        instructions, architecture, denied, prlimit = supervisor._filter_instructions("x86_64")
        base = dict(seccomp_mode=2, no_new_privileges=True, audit_architecture=architecture, machine="x86_64",
            denied_syscalls=denied, prlimit64_query_only=prlimit, x32_or_unknown_syscall_ABI_killed=True,
            filter_instructions_sha256=hashlib.sha256(json.dumps(instructions).encode()).hexdigest())
        worker = dict(base, address_space_bytes=evidence.MEMORY-64*common.MIB, cpu_seconds=43170,
                      script_sha256=self.receipt["checker_sha256"], pid=200, birth_tick=100)
        controller = dict(base, address_space_bytes=64*common.MIB, cpu_seconds=30, pid=199, birth_tick=99)
        common.write(self.execution/"native-worker-guard.json", worker)
        common.write(self.execution/"native-controller-guard.json", controller)
        common.write(self.execution/"native-controller-result.json", dict(returncode=0, worker_pid=200,
                      worker_source_sha256_after=self.receipt["checker_sha256"]))
        guard = dict(kind="LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1", capability_established=True, native_python_execution=True,
            hard_sum_RLIMIT_AS_bytes=evidence.MEMORY, worker_RLIMIT_AS_bytes=evidence.MEMORY-64*common.MIB,
            supervisor_RLIMIT_AS_bytes=64*common.MIB, hard_sum_RLIMIT_CPU_seconds=43200,
            supervisor_RLIMIT_CPU_seconds=30, worker_RLIMIT_CPU_seconds=43170,
            script_sha256=self.receipt["checker_sha256"], supervisor_source_sha256=common.digest(supervisor.__file__),
            worker_guard=worker, supervisor_guard=controller)
        self.observed = dict(status="completed", returncode=0, mode="trusted_native", proof_accepted=False,
            stdout_path=str(self.execution/"stdout.txt"), stderr_path=str(self.execution/"stderr.txt"),
            stdout_sha256=common.digest(self.execution/"stdout.txt"), stderr_sha256=common.digest(self.execution/"stderr.txt"),
            guard_scope=guard)
        common.write(self.execution/"supervisor-result.json", self.observed)
        before = dict(schema=evidence.SCHEMA, job_id=self.job["job_id"], branch="b0", index=37,
            scope=evidence.SCOPE, epoch=str(self.epoch), observed=self.observed, census=self.census,
            implementation=evidence.implementation(), arithmetic_accepted=False,
            parent_acquisitions_verified=False, all_index_conclusion_verified=False)
        common.write(self.epoch/"NATIVE_OBSERVED.json", before)
        common.write(self.epoch/"NATIVE_ACCEPTED.json", dict(before, arithmetic_accepted=True,
            native_receipt=str(self.capsule/"COUNT37_ACCEPTED.json"),
            native_receipt_sha256=common.digest(self.capsule/"COUNT37_ACCEPTED.json"),
            negative_controls=24, conditional_premises=evidence.premises(self.job)))

    def alter(self, path, change):
        value = common.read(path)
        change(value)
        path.unlink(); common.write(path, value)

    def validate(self):
        return evidence.validate_stage(self.task, self.job, self.epoch)

    def reject(self):
        with self.assertRaises((ValueError, KeyError, FileNotFoundError)):
            self.validate()

    def synchronize_receipt(self, change):
        self.alter(self.capsule/"COUNT37_ACCEPTED.json", change)
        self.receipt = common.read(self.capsule/"COUNT37_ACCEPTED.json")
        (self.execution/"stdout.txt").write_text(json.dumps(self.receipt)+"\n", encoding="utf-8")
        self.alter(self.execution/"supervisor-result.json", lambda x:x.update(stdout_sha256=common.digest(self.execution/"stdout.txt")))
        for path in (self.epoch/"NATIVE_OBSERVED.json", self.epoch/"NATIVE_ACCEPTED.json"):
            self.alter(path, lambda x:x["observed"].update(stdout_sha256=common.digest(self.execution/"stdout.txt")))
        self.alter(self.epoch/"NATIVE_ACCEPTED.json", lambda x:x.update(native_receipt_sha256=common.digest(self.capsule/"COUNT37_ACCEPTED.json")))

    def test_complete_stage_and_preledger_validation_do_not_execute_trap_source(self):
        result = self.validate()
        self.assertEqual(result["schema"], "REVALIDATED_RETAINED_N25_EXTRA_STAGE_V1")
        self.assertTrue(result["native_arithmetic_accepted"])
        self.assertFalse(result["parent_acquisitions_verified"])
        self.assertEqual(result["census"]["leaves"], 26)
        (self.epoch/"NATIVE_ACCEPTED.json").unlink()
        self.assertEqual(evidence.validate_run(self.task, self.job, self.epoch, self.observed, self.census), self.receipt)

    def test_relocation_preserves_exact_recorded_receipt_bytes(self):
        old = str(self.task)
        raw = (self.epoch/"NATIVE_ACCEPTED.json").read_bytes()
        other = self.root/"restored"/"task"
        shutil.copytree(self.task, other)
        shutil.rmtree(self.task)
        result = evidence.validate_stage(other, self.job, other/self.epoch.name, original_task_root=old)
        self.assertEqual(result["original_task_root"], old)
        self.assertEqual((other/self.epoch.name/"NATIVE_ACCEPTED.json").read_bytes(), raw)
        with self.assertRaises(ValueError):
            evidence.validate_stage(other, self.job, other/self.epoch.name, original_task_root="/foreign/task")

    def test_original_source_or_clone_changes_and_extra_outputs_fail(self):
        (self.capsule/"unknown.json").write_text("{}")
        self.reject(); (self.capsule/"unknown.json").unlink()
        (self.source/"COUNT37_ACCEPTED.json").write_text("{}")
        self.reject(); (self.source/"COUNT37_ACCEPTED.json").unlink()
        with (self.capsule/"kernel.py").open("a") as out: out.write("\n")
        self.reject()

    def test_exact_receipt_schema_scope_elapsed_and_full_leaf_evaluations(self):
        for change in (lambda x:x.update(seconds=True), lambda x:x.update(scope="another scope"),
                       lambda x:x.update(fresh_leaf_evaluations=25), lambda x:x.update(extra_success=True)):
            before = deepcopy(self.receipt)
            self.synchronize_receipt(change); self.reject()
            self.synchronize_receipt(lambda x:(x.clear(), x.update(before)))

    def test_ordered_controls_statistics_and_kernel_pins_are_required(self):
        for change in (lambda x:x["negative_controls"].reverse(),
                       lambda x:x["statistics"].update(maximum_depth=True),
                       lambda x:x["kernel_sha256"].update(**{"kernel.py":"0"*64})):
            before = deepcopy(self.receipt)
            self.synchronize_receipt(change); self.reject()
            self.synchronize_receipt(lambda x:(x.clear(), x.update(before)))

    def test_capture_hashes_bind_even_empty_stderr(self):
        for name in ("stdout.txt", "stderr.txt"):
            path = self.execution/name
            raw = path.read_bytes(); path.write_bytes(raw+b" ")
            self.reject(); path.write_bytes(raw)
        for path in (self.execution/"supervisor-result.json", self.epoch/"NATIVE_OBSERVED.json", self.epoch/"NATIVE_ACCEPTED.json"):
            self.alter(path, lambda x:(x.get("observed", x)).update(stderr_sha256="0"*64))
        self.reject()

    def test_no_partial_or_false_transition_and_wrong_implementation(self):
        self.alter(self.epoch/"NATIVE_OBSERVED.json", lambda x:x.update(arithmetic_accepted=True)); self.reject()
        self.alter(self.epoch/"NATIVE_OBSERVED.json", lambda x:x.update(arithmetic_accepted=False))
        self.alter(self.epoch/"NATIVE_ACCEPTED.json", lambda x:x.update(parent_acquisitions_verified=True)); self.reject()
        self.alter(self.epoch/"NATIVE_ACCEPTED.json", lambda x:x.update(parent_acquisitions_verified=False))
        for path in (self.epoch/"NATIVE_OBSERVED.json", self.epoch/"NATIVE_ACCEPTED.json"):
            self.alter(path, lambda x:x["implementation"].update(source_adapter_sha256="0"*64))
        self.reject()

    def test_census_mismatch_boolean_completion_and_missing_capability_reject(self):
        for path in (self.epoch/"NATIVE_OBSERVED.json", self.epoch/"NATIVE_ACCEPTED.json"):
            self.alter(path, lambda x:x["census"].update(roots=25))
        self.reject()

    def test_boolean_returncode_and_missing_native_capability_fail_closed(self):
        for change, undo in ((lambda x:x.update(returncode=False), lambda x:x.update(returncode=0)),
                             (lambda x:x["guard_scope"].update(capability_established=False),
                              lambda x:x["guard_scope"].update(capability_established=True))):
            for path in (self.execution/"supervisor-result.json", self.epoch/"NATIVE_OBSERVED.json", self.epoch/"NATIVE_ACCEPTED.json"):
                self.alter(path, lambda x:change(x.get("observed", x)))
            self.reject()
            for path in (self.execution/"supervisor-result.json", self.epoch/"NATIVE_OBSERVED.json", self.epoch/"NATIVE_ACCEPTED.json"):
                self.alter(path, lambda x:undo(x.get("observed", x)))

    def test_nonempty_stderr_rejects_even_if_all_capture_hashes_are_updated(self):
        (self.execution/"stderr.txt").write_bytes(b"unexpected diagnostic\n")
        pin = common.digest(self.execution/"stderr.txt")
        for path in (self.execution/"supervisor-result.json", self.epoch/"NATIVE_OBSERVED.json", self.epoch/"NATIVE_ACCEPTED.json"):
            self.alter(path, lambda x:x.get("observed", x).update(stderr_sha256=pin))
        self.reject()

    def test_captured_terminal_json_cannot_be_a_different_receipt_with_bound_hash(self):
        (self.execution/"stdout.txt").write_text('{}\n', encoding="utf-8")
        pin = common.digest(self.execution/"stdout.txt")
        for path in (self.execution/"supervisor-result.json", self.epoch/"NATIVE_OBSERVED.json", self.epoch/"NATIVE_ACCEPTED.json"):
            self.alter(path, lambda x:x.get("observed", x).update(stdout_sha256=pin))
        self.reject()

    def test_missing_unaccepted_observation_and_partial_guard_records_reject(self):
        raw = (self.epoch/"NATIVE_OBSERVED.json").read_bytes()
        (self.epoch/"NATIVE_OBSERVED.json").unlink(); self.reject()
        (self.epoch/"NATIVE_OBSERVED.json").write_bytes(raw)
        (self.execution/"native-controller-result.json").unlink(); self.reject()

    def test_wrong_command_budget_controller_or_actual_guard_rejects(self):
        original = common.read(self.execution/"native-launch.json")
        for change in (lambda x:x.update(memory_bytes=512*common.MIB), lambda x:x.update(cpu_seconds=43201),
                       lambda x:x.update(wall_seconds=43501), lambda x:x["argv"].__setitem__(-1,"construct")):
            self.alter(self.execution/"native-launch.json", change); self.reject()
            self.alter(self.execution/"native-launch.json", lambda x:(x.clear(), x.update(deepcopy(original))))
        self.alter(self.execution/"launch.json", lambda x:x["argv"].__setitem__(4, "--_exec-search")); self.reject()

    def test_nested_capability_and_actual_guard_and_worker_source_are_required(self):
        self.alter(self.execution/"native-worker-guard.json", lambda x:x.update(cpu_seconds=1)); self.reject()

    def test_literal_domain_and_supplemental_s1_premises_are_explicit(self):
        row = dict(self.job, branch='b3', index=30, target_id='b3-p30')
        self.assertEqual(len(evidence.premises(row)), len(evidence.PREMISES)+2)
        self.assertIn('supplemental S1', evidence.premises(row)[-1])
        self.assertEqual(len(evidence.premises(self.job)), len(evidence.PREMISES)+1)
        self.assertIn(self.job['target_id'], evidence.premises(self.job)[-1])


if __name__ == "__main__":
    unittest.main()
