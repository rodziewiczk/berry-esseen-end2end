# Observed Colab arithmetic runs

This document records user-supplied Colab evidence inspected on 23 October 2026. Notebook 08 was inspected through its saved stage receipts and stdout/stderr captures; notebooks 09, 10, 13 and 14 are presently recorded from their displayed progress logs only. No mathematical calculations were rerun locally. Raw logs, account paths, and VM identifiers are not published here.

## Notebook 08: all six n2/n3 stages completed in BASIC mode

The results ZIP has SHA-256:

```text
77b7750b3e6cb124a0622f906034dca8dec500aed07c8a70596c747285736e2b
```

Its session receipt records `exact_arithmetic_completed_untrusted_guard`, with all six required stages selected and computed. The arithmetic receipt records `COMPUTED_EXACT_OUTPUTS_UNTRUSTED_GUARD`. Every stage has observed return code 0, supervisor status `completed`, a null failure reason, and an empty stderr capture.

The recorded UTC interval is 23 October 2026, 10:25:41.818717 to 10:27:20.921536. The arithmetic driver reports 99.013 seconds elapsed, including orchestration overhead. These measurements describe this run; they are not runtime guarantees for another Colab allocation.

| Stage | Observed complete scope or terminal marker | Reported elapsed seconds |
|---|---|---:|
| `n2-scalars` | Original `verify_reductions`; `FRESH_SCALARS_COMPLETED n2-scalars verify_reductions` | 0.529 |
| `n2-primary` | All 70 tensor cells; `ACCEPTED_ALL_70_TENSOR_CELLS 35878 134` | 12.209 |
| `n2-independent` | All 70 cells through the independent integer checker; `ACCEPTED_ALL_70_BY_INDEPENDENT_INTEGER_CHECK 35878 18426 134` | 46.488 |
| `n3-scalars` | Original `analytic_constants`; `FRESH_SCALARS_COMPLETED n3-scalars analytic_constants` | 0.523 |
| `n3-identities` | 111 cells, 444 sign orthants, 95,904 exact grid identities | 9.362 |
| `n3-full` | Full 111-cell verifier with fresh C++ compilation; `ACCEPTED_FULL_N3 111 501156 219860 349` | 29.307 |

The full n3 stage records maximum sampled process-group RSS of 387,592,192 bytes. This is a sampled observation, not an aggregate kernel memory guarantee. The receipts retain source-cell hashes and log hashes; the complete private ZIP is identified above rather than reproduced in this document.

## Source and code provenance

- Mathematical source reference: [`75a94708872e2bc053f42a279559b23ed91e4402`](https://github.com/rodziewiczk/berry-esseen-045-certificate/tree/75a94708872e2bc053f42a279559b23ed91e4402) in the original research repository.
- Mathematical source-manifest SHA-256 recorded by the run: `8ca0f5c30991b50c61fc998c7c873873c2ac7d2bde6611123ce74651e1a3c26b`.
- Published notebook execution-code pin: [`4b2c0e44ae0d7d0f7985e5b8c7714a03c4607bad`](https://github.com/rodziewiczk/berry-esseen-end2end/tree/4b2c0e44ae0d7d0f7985e5b8c7714a03c4607bad). The archived driver and supervisor hashes match the bytes of these files at that commit.
- Archived driver SHA-256: `06667714b4822639ea7301400c28e09e199e23ae7c11fb344a6af15d3013f8f2`.
- Archived supervisor SHA-256: `61e71dd4a9653de2bbbee8c54928a1f5c5bffd0bf083dd324851716c3a1eaea2`.
- The run context records Python 3.13.16 and a C++ compiler. It records `historical_receipts_used: false`.

The execution-code commit above is the notebook's declared pin, corroborated by the two archived code hashes. The result ZIP does not provide a separate Git HEAD attestation for the whole execution checkout. This provenance inspection is not a fresh replay of the mathematical source inventory or leaf inequalities.

## Acceptance boundary

The requested mode was **BASIC**, using `UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP`. It supplied an external wall watchdog, owned process-group cleanup, per-process `RLIMIT_AS`/`RLIMIT_CPU`, and sampled group/file observations. It did not establish an aggregate kernel CPU or charged-memory limit, containment of descendants changing sessions, or equivalence to a Windows Job/cgroup contract. Samples of process-group CPU also must not be treated as complete accounting of every short-lived compiler or child process.

Accordingly, the saved results explicitly retain:

```text
native_arithmetic_accepted: false
all_law_theorems_verified: false
all_index_conclusion_verified: false
```

The observed checker outputs concern the supplied finite n2/n3 arithmetic, conditional on the stated analytic reductions. They do not independently prove those reductions or the literature inputs. The six-stage completion is useful new computational evidence; it is not trusted native acceptance, a certificate for C4 or later indices, or an all-index PASS. See [the small-index execution contract](small_indices_execution.md) for the distinction between BASIC execution and stronger native execution.

## Subsequent mathematical and checker reviews

The [standalone analytic reduction review](small_indices_analytic_review.md) checked attainment, reflection at atoms, full-support contact, support acquisition, moment domains and the finite-certificate implication. The [source-level checker review](small_indices_checker_review.md) checked both selected n2 acceptance paths and the n3 Python/C++ and identity-audit paths against the same source inventory. Neither review found a blocking gap within its stated scope.

Together with the observed full calculation, these reviews supply the selected finite inequalities and their reduction to the stated n2/n3 bounds under the reviewed external structural theorem and ordinary faithful execution assumptions. The BASIC fields remain a record of the execution contract; they do not indicate a failed inequality. No rerun of notebook 08 is warranted merely to change those labels. Compiler/runtime formal verification, a second full n3 implementation, later indices and the global composition are outside these scoped conclusions.

## Notebook 09: displayed log reports the complete conditional n25 B3 parent chain

The user-supplied progress log reports all four selected stages completed: INITIAL construction, INITIAL acceptance, resource construction and resource acceptance. The final stage completed at approximately 11:52:30 UTC on 23 October 2026. The displayed terminal marker is `PASS_FRESH_EXACT_SHARP25_B3_GLOBAL_RESOURCES`; the session state is `CONDITIONAL_FRESH_PARENT_CHAIN_ACCEPTED`. The log reports no errors and a saved final results ZIP.

This is useful evidence that the four-stage calculation finished. The ZIP, actual output receipts, supervisor results and captures have **not yet been independently inspected** for this record, so its contents and archive hash are not asserted here. The proof graph remains open. Completing this job also does not by itself acquire the imported stronger24 mathematical premise, complete the B3 count forests, or prove the final same-law n25 composition.

## Notebook 10: displayed log reports the complete conditional n25 B4 parent chain

The later user-supplied progress log reports the B4 resource acceptor completed successfully at 12:20:29 UTC on 23 October 2026, following the selected INITIAL construction/acceptance and resource construction. Its terminal marker is `PASS_FRESH_EXACT_SHARP25_B4_GLOBAL_RESOURCES`. The final session state is `CONDITIONAL_FRESH_PARENT_CHAIN_ACCEPTED`, and the log reports a saved results ZIP without an error.

As for notebook 09, this observation is currently based on the displayed log. It is not an independent inspection of the exported ZIP, actual acceptance objects and captures. The completed B3 and B4 parent calculations can be joined to later count evidence; they do not remove the selected stronger24 predecessor or complete the unrestricted n25 theorem by themselves.

## Notebook 13: displayed log reports accepted complete n5 gap-free component

The user-supplied log shows the full n5 gap-free worker launched at 12:33:33 UTC on 23 October 2026 and the guarded execution finished at 12:33:48 UTC. Its final state is `FRESH_LINUX_POSITIVE_CLOSED_N5_GAPFREE_RECTANGLE_ACCEPTED`, with `native_arithmetic_accepted=true`; the final ZIP was reported saved immediately afterward. The log contains both the original result and the new complete Linux protocol packet, without a reported error.

The reported complete scope is 60 roots, 1,994 nodes, 1,027 leaves, the two infinite exterior rays and all 21 original/added controls. Its actual n5 domain is rho `[477/400,6/5]`, beta `[17/50,35139006743001/100000000000000]`, the positive closed-CDF orientation and every real threshold. The recorded target is `4097/10000`. These are the selected component's domains, not an unrestricted absolute C5 theorem.

The logged source-manifest SHA-256 is `3f38d156e97f82132772b6c21aeffe4f6ad6ca254417882331fe8a9738617a40`; the driver SHA-256 is `b3efe30d0b67e0b172367e55a387515c3a2d2655ade1a44fd07749ca6d89a484`. The receipt explicitly retains `full_n5_verified=false` and `all_index_conclusion_verified=false`.

This records the displayed full-run evidence. The final ZIP, actual supervisor result and saved capture files have not yet been separately inspected for this record; no archive digest or newly closed proof-graph node is asserted. No repeat computation is requested merely to change these bookkeeping details. See [the execution contract](n5_gapfree_execution.md) and [the n5 analytic review](n5_analytic_review.md) for the component's implication and the remaining n5 domains.

## Notebook14: displayed log reports all five auxiliary21 covers completed

The user-supplied log reports `EXACT21_STAGE`1 through5, followed by the actual
`EXACT21_PASS` marker and guarded stage status `completed`, with
`native_arithmetic_accepted=true`. Stage5 reports a negative final defect. The
native output reports approximately632.779 seconds elapsed. The final saved
session state is `FRESH_CONDITIONAL_ARITHMETIC_REPLAY_COMPLETED`; the results ZIP
was reported saved on23 October2026 at12:50:42 UTC.

This is the selected five-cover,92,160-rectangle auxiliary21 calculation. The
source/transport contract and retained predecessor/analytic premises are
documented in [the auxiliary21–23 execution scope](aux21_23_execution.md).
`full_auxiliary_bound_verified` and `all_index_conclusion_verified` remain false
in the displayed result. The log reports complete scoped arithmetic; the actual
ZIP and saved native capture/guard artifacts have not yet been independently
inspected for this record. No full auxiliary theorem or sharp C21 conclusion is
promoted by this observation.

## Notebook 12: actual exported ZIP inspected after a memory-limit stop

The actual 16,883,307-byte result ZIP has SHA-256
`86027e5f0e4d3670b3449116e9dfb2d5af9ee1cf67fcf9842cb5c4777c21db77`.
Its saved result is `INCOMPLETE_NO_ACCEPTANCE`, with supervisor reason
`Sampled group RSS limit exceeded`: 537,497,600 sampled bytes against the
configured 536,870,912-byte ceiling after approximately 3908.972 seconds.

The [detailed source/capture inspection](tail49_failed_run_review.md) verified
all 1400 manifested source files, the manifest itself and 272 retained-input
bindings. All 13 completed top-level jobs and 28 completed retained components
have integer-zero recorded exits, matching actual stdout/stderr hashes and
empty stderr. Component 29, `certificate_central_low47`, was in progress. Its
partial signed-index messages are not a completed acceptance.

The full 14/41 suite remains unfinished. The corrected notebook 12 uses an
explicit 2 GiB BASIC memory budget, with unchanged mathematical sources and full
completion checks. No native/all-index acceptance or failed inequality is
inferred from this resource stop, and no completed prefix is silently substituted
for a full original run.

## Notebook 04: actual q2 result ZIP and separate q1/q3 time stops

The actual 1,913,858-byte q2 ZIP has SHA-256
`84a5272daa9858e66c369f18365bf5f17568dd912e9901cfc0c5c1859a9972f0`.
Its final stderr is `DISCOVERY_INCOMPLETE_NO_ACCEPTANCE: Original split depth/node budget exhausted`.
The final checkpoint contains 10000 nodes, 4996 untrusted closed leaves and
17 pending boxes at maximum depth20. All76 sealed source files and seven
checkpoint transitions were inspected without numerical replay. No native count
acceptance action occurred. See [the detailed review](b4_q2_node_limit_review.md).

The separate pasted q1 and q3 logs end `candidate_incomplete_budget_exhausted`:
q1 has 5858 nodes, 2920 leaves and22 pending boxes; q3 has 6828 nodes, 3404 leaves
and23 pending boxes. Those logs establish exhaustion of the search-time allocation,
not the q2 node-cap exception. Their actual result ZIPs were not inspected here.
The existing driver can resume compatible saved candidates for another time
allocation. All scoped/native/global acceptance flags remain false.

Notebook25 is an explicitly new q2 resource epoch with a100000-node ceiling and
preserved candidate topology. The unchanged numerical functions still require
full fresh native replay of all26 roots and24controls. Local verification passed
55 count/recovery infrastructure fixtures and65 n25 evidence/interface regression
fixtures. A source-only preparation using the actual failed q2 ZIP preserved its
exact checkpoint bytes and complete roots. None of these local checks evaluated
an original mathematical kernel or completed the proof.

## Unified restart handoff and auxiliary22 completion

All seven original count sessions have ended. The [cache handoff inventory](count_cache_handoff.md)
checks every actual final ZIP, full frozen source inventory and checkpoint binding.
The current RESTART01–07 set preserves those untrusted candidates and declares
100000 nodes,2GiB memory and separate12-hour search/native CPU ceilings. It
supersedes the old numbered count set and the q2-only notebook25. Fresh complete
native leaf replay and analytic/parent acquisition remain separate requirements.

The separate pasted notebook15 log ends
`FRESH_CONDITIONAL_ARITHMETIC_REPLAY_COMPLETED` for target22. Its final count join
reports all258 closed leaves, a strict positive margin and
`PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES`; the stage records native arithmetic
acceptance. The complete auxiliary-bound and all-index flags remain false.
This records the inspected log, without claiming independent inspection of its
actual exported ZIP or acquiring its conditional premises.

## Notebook 16: auxiliary23 complete arithmetic log

The supplied complete log has SHA-256
`00909a45c8908e76da3069bb0bca5324a51ee207ab4ed5d47a2464975b5bdecb`.
It records all 25 stages finishing: INITIAL, all 100 resource panels,
optimization, the 21 count acceptors for panels 24--44, and the count join.
INITIAL/resource/count/join stages report native arithmetic acceptance;
optimization finishes under its explicitly separate BASIC execution contract.
No stronger execution label is inferred for that stage.

The count join reports 18,377 closed leaves, maximum score
`435818419209/1000000000000`, and the strictly positive exact margin
`3109377771729146828051331781192197462713750263324116007/4312500000000000000000000000000000000000000000000000000000000`.
Its native conclusion remains `PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES`.
The final batch state is `FRESH_CONDITIONAL_ARITHMETIC_REPLAY_COMPLETED`, with
the completed results ZIP reported saved at 16:51:08 Europe/Warsaw on 23 October 2026.

This is complete conditional auxiliary23 arithmetic as reported by the inspected
log. The actual exported ZIP, full guard/capture chain and semantic resource
interfaces have not yet been independently revalidated for this record.
`full_auxiliary_bound_verified` and `all_index_conclusion_verified` remain false.
The remaining auxiliary24 branches and final notebook23 join stay separate work;
this result does not establish sharp all-law n23 or n24.

## Notebook 17: complete stronger24 B0 arithmetic log

The supplied log has SHA-256
`08574b10b1aafbaf760261b282d34f5759868c4b860854b4c1ab2ab746f469aa`.
It records all 16 selected stages finishing, with 1,929 closed count leaves,
maximum score `422231556519/1000000000000` and a positive exact final margin.
The completed results ZIP is reported saved at 17:15:59 Europe/Warsaw on
23 October 2026; the final state is `complete_conditional_arithmetic_basic`.

This task uses its explicit BASIC process-tree execution contract. Its
`native_arithmetic_accepted` flags remain false; the completed arithmetic is not
relabelled as the stronger single-process native contract. The original
conditional count join reports `PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES`.
The other five stronger24 branches, full auxiliary join and analytic premises
remain separate. This record inspects the full supplied log, not the actual
ZIP or its complete preserved capture/source chain.

## Notebook 12: corrected2GiB run stops incomplete near its wall ceiling

The supplied log has SHA-256
`176139033a7fc798c25b28b5bb7bd4dbb0111a96ac8ab6b0bcf199bf54c90143`.
It starts with2GiB, BASIC supervision and `quick_mode=false`. Its final state
is `INCOMPLETE_NO_ACCEPTANCE`, with `all_required_jobs_computed=false`.
The last heartbeat has13 main and25 retained execution records, against the
required14/41. These are recorded executions, not independent proof of every
record's successful completion.

The last elapsed heartbeat is7791.5seconds and the stop is reported at about
7802seconds, alongside a7800-second configured wall ceiling. This strongly
suggests a wall-limit stop; the exact `execution.reason`, native stderr and
actual final exported bundle have not been inspected for this record. The
supplied log does not display a failed mathematical inequality or a memory-limit
exception. No completion, native acceptance or uniform tail theorem is inferred.
