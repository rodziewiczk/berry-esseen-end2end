# Original cutoff49 selected FULL arithmetic on Colab

The original portable arithmetic entry point is the byte-pinned capsule's `verify.py --output NEW_PATH`, without `--quick`. It runs 14 top-level jobs, the last of which runs all 41 retained components. A full computation is available through the new BASIC Colab wrapper:

```python
from be_replay.tail49 import run_colab
RESULT = run_colab(durable_root=DURABLE)
```

The wrapper downloads the public `cutoff49-sources-2026-10-22` release asset `BE_cutoff49_20260930.zip`, checks its exact 16,660,566-byte size and SHA-256 `ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e`, and extracts all 1,401 original files. The original manifest, mathematical sources, job lists, old provenance records, and `verify.py` remain unchanged. The `verify.py` SHA-256 is `766e9cee5d1cb8b173fd2db264cddbd227439e4e87fbcf3daec243ec2c9a1375`.

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
python -B -S -m be_replay.tail49 --output work/new-tail49-epoch --archives archives --download --mode basic --wall-seconds 7800 --cpu-seconds 7200
```

The wall limit applies externally to the whole invocation. The CPU allowance and 512 MiB address-space cap are per-process limits under BASIC supervision, not the original adapter's aggregate cgroup budget. No mathematical kernel has been run locally while implementing this wrapper. Local tests use small schema, source-binding, negative-control, and failure-bundling fixtures only.
