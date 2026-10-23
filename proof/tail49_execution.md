# Original cutoff49 selected FULL arithmetic on Colab

The original portable arithmetic entry point is the byte-pinned capsule's `verify.py --output NEW_PATH`, without `--quick`. It runs 14 top-level jobs, the last of which runs all 41 retained components. A full computation is available through the new BASIC Colab wrapper:

```python
from be_replay.tail49 import run_colab
RESULT = run_colab(durable_root=DURABLE)
```

The wrapper downloads the public `cutoff49-sources-2026-10-22` release asset `BE_cutoff49_20260930.zip`, checks its exact 16,660,566-byte size and SHA-256 `ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e`, and extracts all 1,401 original files. The original manifest, mathematical sources, job lists, old provenance records, and `verify.py` remain unchanged. The `verify.py` SHA-256 is `766e9cee5d1cb8b173fd2db264cddbd227439e4e87fbcf3daec243ec2c9a1375`.

## Corrected memory budget after the observed interrupted run

The first notebook 12 run stopped at the wrapper's 512 MiB sampled process-group
RSS ceiling, after 13 top-level jobs and 28 retained components had completed.
The observed peak was 537,497,600 bytes, with reason
`Sampled group RSS limit exceeded`. See [the inspected result ZIP review](tail49_failed_run_review.md).
This was an incomplete resource-limited execution, not a reported failed inequality.

The replacement notebook uses an explicit 2 GiB BASIC budget. `run` and
`run_colab` accept `memory_bytes`, default 2,147,483,648, within 512–2048 MiB.
The same selected value supplies the per-process address-space ceiling and the
sampled group RSS threshold; it is not an aggregate kernel memory guarantee.
At that memory-only correction, CPU/wall/disk/log ceilings and every
mathematical source byte, target, required14/41 invocation and completion check
were unchanged. That profile recorded
`basic_memory_bytes` and `BASIC_FULL_SUITE_EXPLICIT_MEMORY_V2`.

This is a fresh full run. The original driver has no completed-stage resume;
the earlier ZIP is preserved as inspected incomplete evidence and its completed
work is not silently relabeled as a complete original run. A separately reviewed
composite continuation could retain suitable completed evidence in the future.

## Corrected wall allowance after the actual2GiB interruption

The actual corrected-run ZIP confirms `external_wall_timeout` after
7800.436257839001seconds, with return code-15. Its maximum sampled RSS was
101,392,384bytes, far below2GiB. The incomplete outputs contain13 successful
top-level rows and25 successful retained rows. See the
[actual wall-limit review](tail49_wall_limit_review.md).

The replacement defaults and notebook12 explicitly use64,800seconds
(18hours) of external wall time and64,800seconds (18hours) of per-process CPU
allowance, and2GiB of memory. BASIC group CPU/RSS observations cover sampled
live processes, not cumulative CPU across exited sequential subprocesses.
The outer wall watchdog is the actual whole-invocation elapsed-time ceiling.
These budgets do not guarantee completion or a Colab session of that length.

The result records all three selected budgets under a new explicit resource
profile. Source bytes, original `verify.py` invocation, every14/41 required
job, capture validation and disk/log caps are retained. There is no numerical
resume or hidden inner budget argument: the original driver and retained runner
have no CPU/wall option. This replacement starts a fresh full run in a separate
directory, preserving earlier ZIPs and live evidence.

## Actual execution and acceptance boundary

This is an execution route, not a claim that the calculation has already completed. The wrapper actually invokes the complete unchanged original driver in a fresh output epoch. It then requires all 14 top-level names and invocations in order, all 41 retained component names and invocations, successful integer exit codes, matching stdout/stderr hashes, empty successful stderr, unchanged sources, and no bytecode-cache prefix. Preparation, a quick run, a partial retained list, or an old capture cannot qualify.

The original strong adapter is `moment-defects/reproduction/uniform_tail/linux49_replay.py` in the research repository. It requires Python 3.12, a dedicated Docker init process, and an actual private cgroup-v2 with whole-container memory/CPU/PID accounting. Ordinary Colab does not provide that established contract. The new wrapper therefore does not call it with its checks removed, fabricate its receipt, or claim that per-process limits replace the cgroup.

The unchanged original full driver itself has no Python-3.12-only gate and uses POSIX-compatible paths. BASIC mode permits its real subprocess tree under the new external wall watchdog and process-group supervisor. Hard `RLIMIT_AS`/`RLIMIT_CPU` limits remain per process; group RSS/CPU and file quotas are sampled observations. Descendants changing sessions are outside that weaker containment guarantee. The wrapper records these limitations and always retains `native_arithmetic_accepted: false` and `all_index_conclusion_verified: false`.

The single-process seccomp contract used for eligible Python count workers cannot run this full driver: the original driver deliberately launches many subprocesses. Requesting `mode="native"` fails closed before the full computation starts. A stronger full-tree Colab acceptance contract remains a separate obligation.

## Complete top-level selection

The 14 required executions are `composition49`, `support46`, `independent_support46`, `independent_selectors`, `phase_product_controls`, `new_phase_controls`, `later_phase_domains`, `independent_phase_scope`, `corrected_legacy_acquisition`, `corrected_barrier46`, `finite_base`, `entry_schedule_mapping`, `local_formula_mapping`, and `retained_components`. The final execution must select all 41 entries of the original, separately pinned `retained_jobs.json`.

These checks reproduce the original selected arithmetic suite. Their success does not establish every analytic or literature premise, the cutoff31 continuation, the full n6–48 graph, or an all-index theorem. A composition job may check scalar implications and inherited hypotheses; its PASS must not be promoted to an independent proof of those hypotheses.

## Progress, evidence, and real command

The session displays original START/PASS lines, periodic counts read from the original live receipts, elapsed time, and the supervisor's resource observations. Logs and status files are backed up to the user-selected durable directory every 60 seconds. On completion or a handled failure it produces a results ZIP with the original capsule, fresh reports/captures, context, and failure diagnostics. Live backups and incomplete outputs are evidence to inspect, not accepted certificates. There is no partial-result resume that silently omits already recorded jobs: a complete run must execute the full original driver in a new epoch.

The equivalent Linux CLI is:

```console
python -B -S -m be_replay.tail49 --output work/new-tail49-epoch --archives archives --download --mode basic --wall-seconds 64800 --cpu-seconds 64800 --memory-mib 2048
```

The wall limit applies externally to the whole invocation. The CPU allowance and 2 GiB address-space cap are per-process limits under BASIC supervision, not the original adapter's aggregate cgroup budget. No mathematical kernel has been run locally while implementing this wrapper. Local tests use small schema, source-binding, negative-control, and failure-bundling fixtures only. The memory correction adds tests for actual budget forwarding, invalid-budget rejection before launch, unchanged full 14/41 requirements and preserved BASIC/global flags.
