# Review of the interrupted notebook12 tail49 run

Date: 23 October 2026. This review reads the actual user-generated result ZIP;
it imports no mathematical source and runs no mathematical checker.

The run stopped on its explicitly configured sampled process-group memory
limit. The saved evidence contains 13 completed top-level jobs and 28 completed
retained components. Their actual captures match the recorded hashes and all
their recorded exit codes are integer zero. The complete selected suite remains
unfinished; this failure is not evidence that a mathematical inequality failed.

## Evidence identity

| Item | Identity |
| --- | --- |
| Result ZIP | `20261023T115611Z-27dfd0a3-results.zip` |
| ZIP bytes | 16,883,307 |
| Actual ZIP SHA-256 | `86027e5f0e4d3670b3449116e9dfb2d5af9ee1cf67fcf9842cb5c4777c21db77` |
| Notebook code commit | `30ed60e64362ed5876daaf8ab01bbdf54c9d7d1c` |
| Original source-archive pin | `ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e` |
| Actual original manifest SHA-256 | `58a770705c6e0bc500813ed37299753a16f6245ebea6ade238ad98078d7b4e26` |
| Actual unchanged `verify.py` SHA-256 | `766e9cee5d1cb8b173fd2db264cddbd227439e4e87fbcf3daec243ec2c9a1375` |
| Actual invocation-adapter SHA-256 | `48208994de690d4caa0a3b5753171106e50beb528b5999c31fe3371473b09ccd` |
| Recorded supervisor SHA-256 | `61e71dd4a9653de2bbbee8c54928a1f5c5bffd0bf083dd324851716c3a1eaea2` |

The code-commit prefix in the actual traceback was resolved to the full local
Git commit above. The original manifest, driver and adapter hashes were checked
directly against their bytes inside this ZIP. The source-archive and supervisor
pins are recorded provenance; the result ZIP does not contain the original
source ZIP or a separate supervisor source copy for a new independent rehash.

All 1,400 original manifest entries match the actual saved source bytes. There
are exactly 1,401 files in `arithmetic/original-BE49`, including `MANIFEST.json`.
All 272 retained-runner input bindings also match the saved source bytes after
mapping their original recorded paths. No source mismatch was found.

## Completed and interrupted work

The original top-level `native-full/result.json` remains `RUNNING`, with
`quick=false`. Its 13 completed rows are:

`composition49`, `support46`, `independent_support46`,
`independent_selectors`, `phase_product_controls`, `new_phase_controls`,
`later_phase_domains`, `independent_phase_scope`,
`corrected_legacy_acquisition`, `corrected_barrier46`, `finite_base`,
`entry_schedule_mapping`, `local_formula_mapping`.

For every one of those 13 rows, this review checked:

- `type(returncode) is int` and `returncode == 0`;
- the actual stdout and stderr bytes against their recorded SHA-256 values;
- zero stderr bytes.

The fourteenth top-level action, `retained_components`, started but did not
complete. Its metadata has `selected_jobs=41`, `optimized=false` and 28 completed
job rows. Every one of those 28 rows independently passes the same integer-zero,
actual-capture-hash and empty-stderr checks. Its last completed component is
`certificate_low_normalization47`.

The next component is `certificate_central_low47`, running the original
`accept_low47.py`. Its stdout contains 21 partial signed-index PASS records:
both signs at indices 0–9 and the negative sign at index 10. Its stderr is empty,
but there is no completed job row, terminal acceptance or exit-zero receipt for
this component. These partial records do not accept the whole component.

The 13 components not yet recorded as completed, including the interrupted one,
are:

`certificate_central_low47`, `certificate_left_low47`,
`certificate_positive_left_low47`, `coverage_local47`,
`control_signed_regressions`, `control_gamma_actual`,
`control_phase_low_geometry`, `control_active_marks`,
`control_sperner_actual`, `control_shifted_quartic_actual`,
`control_left_mid_actual`, `control_low_lemmas_actual`,
`control_signed_resource_actual`.

Thus the observed completed prefix is 13/14 top-level actions and 28/41 retained
components. These are invocation censuses, not a runtime percentage or ETA.

## Actual stop condition

The outer execution records:

- status `incomplete`;
- reason `Sampled group RSS limit exceeded`;
- integer return code `-15` after group termination;
- elapsed wall time 3,908.972036937 seconds;
- maximum sampled process-group RSS 537,497,600 bytes against the configured
  536,870,912-byte limit;
- maximum sampled group CPU field 1,359.81 seconds. This is the recorded sampled
  maximum, not a separately established cumulative CPU total for every exited
  descendant over the whole run.

The contract is explicitly BASIC process-group supervision, with per-process
limits and sampled group observations. It does not claim private-cgroup or
Windows Job equivalence. The result correctly keeps full arithmetic completion,
trusted native acceptance and all-index acceptance false.

The preserved progress records contain aggregate RSS observations. They do not
provide a per-PID RSS census at the stopping sample, so this evidence does not
identify which interpreter or other descendant contributed the excess. The
interrupted entry source is Python and has no direct C++ compiler/subprocess
invocation; that source observation does not attribute the measured group peak
to an individual process. No mathematical rejection or failed inequality was
found in the captured completion prefix or interrupted stdout.

## Possible retention under a separate future protocol

The completed rows and captures are real evidence and need not be discarded.
A separately specified continuation/composition protocol could revalidate the
unchanged source and input bindings, commands, complete outcomes and actual
captures for each completed action, then execute and validate every remaining
required component under its explicitly recorded execution budget. It would
need to preserve the distinction between this incomplete original run and its
own completed composite evidence.

The original full verifier's unfinished result cannot simply be changed to PASS,
and the 21 partial records cannot be resumed as accepted component output.
The current original-verifier route does not thereby acquire an automatic
resume mechanism. A fresh full rerun with a larger, openly declared BASIC memory
budget is also a valid execution approach without changing mathematical source.
This review implements neither continuation nor rerun and makes no new theorem
claim.
