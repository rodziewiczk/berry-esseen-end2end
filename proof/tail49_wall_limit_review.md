# Corrected notebook 12: confirmed wall-limit stop

Date: 23 October 2026. This is a read-only inspection of the actual corrected
result ZIP, its JSON records and captured bytes. No mathematical source was
imported, no kernel was evaluated and no certificate was replayed.

## Exact evidence

| Item | Observed value |
| --- | --- |
| Result ZIP | `20261023T131818Z-a090e039-results.zip` |
| ZIP bytes | 16,885,095 |
| Actual ZIP SHA-256 | `98ebb6e9a77f2576d3eb5ff4b4127d298246567c417f0ef05c17c045310c7f9a` |
| Supervisor reason | `external_wall_timeout` |
| Supervisor status / return code | `incomplete` / integer `-15` |
| Supervisor elapsed time | 7,800.436257839001 seconds |
| Configured wall / CPU ceilings | 7,800 / 7,200 seconds |
| Configured BASIC memory | 2,147,483,648 bytes |
| Maximum sampled group RSS | 101,392,384 bytes |
| Maximum sampled group CPU observation | 2,607.14 seconds |

The paths below are relative to the ZIP's single run directory. The actual
`arithmetic/supervision/supervisor-result.json` records the wall-time reason;
`arithmetic/supervision/launch.json` confirms the requested budgets. The same
execution object appears in `arithmetic/TAIL49_RESULT.json` and
`SESSION_RESULT.json`. The wrapper's overall elapsed time is
7,802.250129599999 seconds. Its `ERROR.txt` rejects a subprocess that did not
finish successfully; it does not report a failed mathematical inequality.

The wrapper stdout is 689 bytes and stderr is empty. Both actual capture
digests match the supervisor record. The CPU/RSS fields are sampled BASIC
observations, not audited aggregate kernel accounting of every descendant
over its complete lifetime. They do not establish a stronger native contract.

This is distinct from the earlier 512 MiB memory stop in
`20261023T115611Z-27dfd0a3-results.zip`, documented in
[the first failed-run review](tail49_failed_run_review.md). Both old ZIPs
remain preserved evidence.

## Completed work and its boundary

`arithmetic/native-full/result.json` remains `RUNNING`, with `quick=false`
and 13 completed top-level rows. Its last completed row is
`local_formula_mapping`; the wrapper stdout then says
`START retained_components` without a corresponding PASS.

`arithmetic/native-full/components/metadata.json` also remains `RUNNING`.
It selects 41 components and contains 25 completed rows. The last is
`certificate_tiny_wide47`, finished at
`2026-10-23T15:26:36.954117+00:00`. Empty capture files exist for
`certificate_central_mid47`, consistent with an interrupted subsequent
stage; they are not a completed execution record.

All 13 + 25 recorded completed rows have integer return code zero. The
actual stdout and stderr bytes match all 76 recorded capture digests.
These capture checks do not establish mathematical soundness. A separate
byte-level check also matched all1400 original manifest entries: the capsule
contains exactly1401files including its pinned manifest, with no missing or
extra source files and33,252,205 expanded bytes. The manifest, `verify.py`,
`new_jobs.json` and `retained_jobs.json` match the wrapper's existing pins.
No original source was executed during that check. The suite is still incomplete:
14 top-level executions and all 41 components are required.
`all_required_jobs_computed`, `native_arithmetic_accepted` and the all-index
conclusion remain false.

## Replacement execution policy

The authorized replacement sets both the wrapper's wall ceiling and BASIC
per-process CPU ceiling to64,800seconds (18hours), retaining2GiB memory.
The CPU/address-space limits remain per process; group CPU/RSS checks remain
sampled BASIC supervision. This is not a Docker/private-cgroup or trusted
single-process native acceptance claim.

No original mathematical source, grid, target, selected job list or full
14/41 completion condition changes. No quick mode or completed-stage resume
is introduced. It is a fresh full run, preserving these incomplete exports.
The larger ceilings do not guarantee completion or predict the next runtime.
The complete uniform analytic implication and other global proof obligations
remain separate even after a successful full arithmetic run.

The replacement passed18 synthetic tail49 fixtures and3 notebook-generator
fixtures. These cover default/custom budget forwarding through the Colab and
CLI layers, invalid budgets before source access, timeout/exit rejection,
incomplete-result export, and the unchanged full14/41 requirements. They do
not replay mathematical certificates.

## Historical runtime context

The pinned original archive also contains recorded macOS ARM/Python3.12
component timings in `baseline/evidence/suite_group{0,1,2}_01/metadata.json`.
All41 current retained names match those historical records. Their elapsed-time
sum is1850.157731seconds (30minutes50seconds); the historical groups actually
ran in parallel, so this sum is not a measured whole-suite wall time.
No single completed historical run of the current full14/41 invocation was
located in this bounded check.

For the same first25 retained names, the historical sum is936.8949seconds,
versus6438.4702seconds in the corrected Colab run. The current first13 top-level
jobs took1256.7828seconds; `certificate_initial47` alone took3372.902seconds.
The remaining16 historical components sum to about913seconds. If they had
the same aggregate slowdown as the first25, a fresh whole run would take
roughly4hours. That is a conditional extrapolation across different hardware
and stage mixtures, not a benchmark guarantee or completion deadline.

Source review found existing in-process exact caches and no duplicate complete
invocation in the selected10new+41retained jobs. `optimized=false` denotes
enabled Python assertions, not an absent algorithmic optimization switch.
The replacement changes execution budgets and diagnostics, not numerical
algorithms. Stage reuse or parallelism needs a separate explicitly reviewed
execution/composition protocol; neither is silently enabled here.
