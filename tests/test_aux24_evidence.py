"""Transport fixtures only: no mathematical source or guarded child is executed."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from be_replay import aux24_evidence as evidence, aux21_23, strong24_branches, linux_supervisor


class AuxiliaryEvidenceTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1] / "work/aux24-evidence-fixtures"
        root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=root)
        self.addCleanup(self.temp.cleanup)
        self.task = Path(self.temp.name) / "task"
        self.task.mkdir()
        self.original = "/original/unchanged-task"

    def write(self, relative, packet):
        path = self.task / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(packet, indent=2)+"\n", encoding="utf-8")
        return path

    def load(self, relative):
        return json.loads((self.task / relative).read_text("utf-8"))

    def context(self, relative):
        return self.original + "/" + relative

    def transport(self, *, native=True, execution="attempts/initial-000000000000/execution",
                  cwd="source/cutoff25_20261011/continuation_20261010/toward25/exact21",
                  script="check21.py", args=(), disk_bytes=256*evidence.MIB):
        directory = self.task / cwd
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / script
        source.write_text("raise AssertionError('Never execute numerical fixture')\n", encoding="utf-8")
        output = self.task / execution
        output.mkdir(parents=True)
        (output / "stdout.txt").write_bytes(b"synthetic complete marker\n")
        (output / "stderr.txt").write_bytes(b"")
        mode = "trusted_native" if native else "untrusted_search"
        command = ["/usr/bin/python3", "-B", "-S" if native else "-u", self.context(cwd+"/"+script), *args]
        launch = dict(argv=command, cwd=self.context(cwd), output_dir=self.context(execution),
                      wall_seconds=7260., cpu_seconds=7200, memory_bytes=512*evidence.MIB,
                      checkpoint_paths=[], mode=mode, sample_seconds=.2, disk_bytes=disk_bytes,
                      log_bytes=16*evidence.MIB, heartbeat_seconds=20.)
        group = dict(kind="UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP", proof_acceptance=False,
                     external_wall_seconds=7260., per_process_RLIMIT_AS_bytes=512*evidence.MIB,
                     per_process_RLIMIT_CPU_seconds=7200, aggregate_kernel_memory_limit=False,
                     aggregate_kernel_cpu_limit=False, sampled_group_RSS_limit_bytes=512*evidence.MIB,
                     sampled_group_CPU_limit_seconds=7200, sampled_file_limit_bytes=disk_bytes,
                     sampled_log_limit_bytes=16*evidence.MIB, descendants_changing_session_are_contained=False,
                     equivalent_to_Windows_Job_or_cgroup=False)
        scope = group
        if native:
            launch.update(worker_memory_bytes=448*evidence.MIB, supervisor_memory_bytes=64*evidence.MIB,
                          worker_cpu_seconds=7170, supervisor_cpu_seconds=30)
            instructions, architecture, denied, prlimit = linux_supervisor._filter_instructions("x86_64")
            guard = dict(seccomp_mode=2, no_new_privileges=True, audit_architecture=architecture,
                         machine="x86_64", denied_syscalls=denied, prlimit64_query_only=prlimit,
                         x32_or_unknown_syscall_ABI_killed=True,
                         filter_instructions_sha256=hashlib.sha256(json.dumps(instructions).encode()).hexdigest())
            worker = dict(guard, address_space_bytes=448*evidence.MIB, cpu_seconds=7170,
                          script_sha256=evidence.digest(source), pid=102, birth_tick=201)
            controller = dict(guard, address_space_bytes=64*evidence.MIB, cpu_seconds=30, pid=101, birth_tick=200)
            scope = dict(kind="LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1", capability_established=True,
                         native_python_execution=True, proof_acceptance=False,
                         hard_sum_RLIMIT_AS_bytes=512*evidence.MIB, worker_RLIMIT_AS_bytes=448*evidence.MIB,
                         supervisor_RLIMIT_AS_bytes=64*evidence.MIB, hard_sum_RLIMIT_CPU_seconds=7200,
                         worker_RLIMIT_CPU_seconds=7170, supervisor_RLIMIT_CPU_seconds=30,
                         script_sha256=evidence.digest(source), supervisor_source_sha256=evidence.digest(linux_supervisor.__file__),
                         worker_guard=worker, supervisor_guard=controller, external_group_watchdog=group)
            self.write(execution+"/native-worker-guard.json", worker)
            self.write(execution+"/native-controller-guard.json", controller)
            self.write(execution+"/native-controller-result.json", dict(returncode=0, worker_pid=102,
                       worker_source_sha256_after=evidence.digest(source)))
            self.write(execution+"/native-launch.json", launch)
            outer = dict(launch, argv=[*command[:3], "/original/repository/be_replay/linux_supervisor.py",
                                      "--_native-controller", self.context(execution+"/native-launch.json")])
            self.write(execution+"/launch.json", outer)
        else:
            self.write(execution+"/launch.json", launch)
        observed = dict(status="completed", returncode=0, reason=None, proof_accepted=False,
                        sample_count=1, mode=mode, guard_scope=scope,
                        stdout_path=self.context(execution+"/stdout.txt"), stderr_path=self.context(execution+"/stderr.txt"),
                        stdout_sha256=evidence.digest(output/"stdout.txt"), stderr_sha256=evidence.digest(output/"stderr.txt"))
        self.write(execution+"/supervisor-result.json", observed)
        return dict(execution=execution, cwd=cwd, command=command, mode=mode,
                    observed=observed, disk_bytes=disk_bytes)

    def validate(self, fixture):
        return evidence.validate_execution(self.task, self.original, **fixture)

    def test_native_complete_actual_guard_artifacts_and_relocation_pass_without_execution(self):
        fixture = self.transport()
        result = self.validate(fixture)
        self.assertTrue(result["native_platform_contract_revalidated"])
        self.assertFalse(result["native_arithmetic_accepted"])
        self.assertEqual(len(result["artifact_sha256"]), 8)
        before = {p.relative_to(self.task):p.read_bytes() for p in self.task.rglob("*") if p.is_file()}
        restored = self.task.parent / "restored"
        shutil.copytree(self.task, restored)
        self.assertEqual(evidence.validate_execution(restored, self.original, **fixture), result)
        self.assertEqual(before, {p.relative_to(restored):p.read_bytes() for p in restored.rglob("*") if p.is_file()})

    def test_missing_actual_launch_or_guard_file_rejects_embedded_native_claim(self):
        fixture = self.transport()
        (self.task/fixture["execution"]/"native-worker-guard.json").unlink()
        with self.assertRaisesRegex(ValueError, "Existing ordinary"):
            self.validate(fixture)

    def test_changed_actual_launch_cwd_is_rejected(self):
        fixture = self.transport()
        filename = fixture["execution"]+"/native-launch.json"
        launch = self.load(filename)
        launch["cwd"] = self.original+"/different-directory"
        self.write(filename, launch)
        with self.assertRaisesRegex(ValueError, "command, cwd"):
            self.validate(fixture)

    def test_changed_supervisor_result_is_rejected(self):
        fixture = self.transport()
        packet = deepcopy(fixture["observed"])
        packet["returncode"] = 17
        self.write(fixture["execution"]+"/supervisor-result.json", packet)
        with self.assertRaisesRegex(ValueError, "supervisor result"):
            self.validate(fixture)

    def test_changed_worker_guard_or_policy_is_rejected(self):
        fixture = self.transport()
        filename = fixture["execution"]+"/native-worker-guard.json"
        packet = self.load(filename)
        packet["cpu_seconds"] = 7200
        self.write(filename, packet)
        with self.assertRaisesRegex(ValueError, "kernel guard receipt"):
            self.validate(fixture)

    def test_matching_embedded_but_invalid_seccomp_policy_is_rejected(self):
        fixture = self.transport()
        packet = self.load(fixture["execution"]+"/native-worker-guard.json")
        packet["seccomp_mode"] = 1
        self.write(fixture["execution"]+"/native-worker-guard.json", packet)
        fixture["observed"]["guard_scope"]["worker_guard"] = packet
        self.write(fixture["execution"]+"/supervisor-result.json", fixture["observed"])
        with self.assertRaisesRegex(ValueError, "kernel guard receipt"):
            self.validate(fixture)

    def test_changed_native_controller_result_is_rejected(self):
        fixture = self.transport()
        filename = fixture["execution"]+"/native-controller-result.json"
        packet = self.load(filename)
        packet["worker_pid"] = 103
        self.write(filename, packet)
        with self.assertRaisesRegex(ValueError, "completed native worker"):
            self.validate(fixture)

    def test_actual_empty_stderr_hash_mismatch_is_rejected(self):
        fixture = self.transport()
        fixture["observed"]["stderr_sha256"] = "0"*64
        self.write(fixture["execution"]+"/supervisor-result.json", fixture["observed"])
        with self.assertRaisesRegex(ValueError, "captured bytes: stderr"):
            self.validate(fixture)

    def test_boolean_returncode_cannot_equal_success(self):
        fixture = self.transport()
        fixture["observed"]["returncode"] = False
        self.write(fixture["execution"]+"/supervisor-result.json", fixture["observed"])
        with self.assertRaisesRegex(ValueError, "complete sampled execution"):
            self.validate(fixture)

    def test_basic_complete_artifacts_remain_conditional_without_native_guards(self):
        fixture = self.transport(native=False, disk_bytes=1024*evidence.MIB)
        result = self.validate(fixture)
        self.assertFalse(result["native_platform_contract_revalidated"])
        self.assertFalse(result["native_arithmetic_accepted"])
        fixture["observed"]["guard_scope"]["aggregate_kernel_memory_limit"] = True
        self.write(fixture["execution"]+"/supervisor-result.json", fixture["observed"])
        with self.assertRaisesRegex(ValueError, "BASIC sampled"):
            self.validate(fixture)

    def test_task_native_stage_chain_checks_every_recorded_stage(self):
        stage = aux21_23.stages("21")[0]
        fixture = self.transport()
        packet = dict(schema="FRESH_AUX21_23_STAGE_V1", target="21", stage="initial", status="completed",
                      mode="trusted_native", original_task_root=self.original,
                      driver_sha256=evidence.digest(aux21_23.__file__), source_manifest_sha256=aux21_23.EPOCH_PINS["21"],
                      supervisor_sha256=evidence.digest(linux_supervisor.__file__), dependencies={},
                      execution_relative=fixture["execution"], command=fixture["command"], observed=fixture["observed"],
                      cpu_seconds=7200, wall_seconds=7260)
        self.write("initial-COMPLETED.json", packet)
        result = evidence.validate_task_transport(self.task, "auxiliary21")
        self.assertEqual(list(result["stages"]), ["initial"])
        self.assertTrue(result["execution_transport_revalidated"])
        with self.assertRaises(ValueError):
            evidence.validate_task_transport(self.task, "auxiliary21", original_task_root="/different")

    def test_full_basic_branch_transport_checks_all_expected_stages(self):
        previous = {}
        self.write("RESULT.json", dict(original_task_root=self.original))
        for stage in strong24_branches.stages("b0"):
            name = stage["name"]
            cwd = "execution-epoch/cutoff25_20261011/"+stage["folder"]
            fixture = self.transport(native=False, execution="captures/"+name, cwd=cwd,
                                     script=stage["script"], args=stage["args"], disk_bytes=1024*evidence.MIB)
            packet = dict(schema="OBSERVED_STRONG24_BRANCH_STAGE_V1", branch="b0", stage=stage,
                          original_task_root=self.original, preceding_stage_sha256=deepcopy(previous),
                          native_arithmetic_accepted=False, command=fixture["command"], observed=fixture["observed"],
                          supervisor_sha256=evidence.digest(linux_supervisor.__file__),
                          launch_sha256=evidence.digest(self.task/fixture["execution"]/"launch.json"),
                          supervisor_result_sha256=evidence.digest(self.task/fixture["execution"]/"supervisor-result.json"))
            ledger = self.write(name+"-COMPLETED.json", packet)
            previous[name] = evidence.digest(ledger)
        result = evidence.validate_task_transport(self.task, "stronger24-b0")
        self.assertEqual(len(result["stages"]), len(strong24_branches.stages("b0")))
        self.assertTrue(all(not r["native_platform_contract_revalidated"] for r in result["stages"].values()))


if __name__ == "__main__":
    unittest.main()
