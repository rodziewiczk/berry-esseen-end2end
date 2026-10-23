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

## Notebook 12: corrected 2 GiB run confirmed to hit its wall ceiling

The supplied log has SHA-256
`176139033a7fc798c25b28b5bb7bd4dbb0111a96ac8ab6b0bcf199bf54c90143`.
It starts with2GiB, BASIC supervision and `quick_mode=false`. Its final state
is `INCOMPLETE_NO_ACCEPTANCE`, with `all_required_jobs_computed=false`.
The last heartbeat has13 main and25 retained execution records, against the
required14/41. These are recorded executions, not independent proof of every
record's successful completion.

The actual corrected ZIP was subsequently inspected. Its SHA-256 is
`98ebb6e9a77f2576d3eb5ff4b4127d298246567c417f0ef05c17c045310c7f9a`.
The real supervisor record confirms `external_wall_timeout` at
7800.436257839001 seconds, with return code `-15`; stderr is empty.
All 13 + 25 completed rows have integer zero exit and their 76 actual captures
match the recorded hashes. This is a wall-limit stop, distinct from the earlier
512 MiB memory failure. It is not full-suite acceptance or evidence of a failed
mathematical inequality. See [the actual corrected-ZIP review](tail49_wall_limit_review.md).

## Notebook18: complete stronger24 B1 arithmetic log

The supplied log SHA256 is
`63877cb1974056d2602ae7e902c8e309de38c5fdb62f10187c1b28d58b308a88`.
All13 selected stages completed. The final join reports9,803 closed leaves,
maximum score `10555781431/25000000000` and a strictly positive exact margin.
The ZIP is reported saved at17:50:35 Europe/Warsaw on23 October2026 with state
`complete_conditional_arithmetic_basic`. The complete branch's
`native_arithmetic_accepted` remains false, as required by its BASIC policy.
This is log evidence, not an independent readback of that B1 export. Other
branches and the final conditional collector23 remain separate obligations.

## Notebook07 RESTART: supplied progress through17:49 Europe/Warsaw

The user supplied the recovery log directly in chat. It migrates an untrusted
checkpoint with1,469 closed leaves, then advances to1,898 leaves/3,798 nodes
in the last sampled line. The completed30-minute chunks report1,613,
1,756 and1,894 leaves, preserving progress between search attempts. The
active count is still k=7. Repeated`SEARCH_CHECKPOINTED_INCOMPLETE` is the
chunk boundary, not a full proof acceptance or a demonstrated kernel failure.
The pending frontier fluctuates as fields split and close; it gives no
remaining-leaf total or percentage/ETA. The100,000-node ceiling is a guard,
not a required final tree size. Every full candidate still needs all26 roots
and the separate complete acceptance. No final run status is inferred here.

## Additional actual execution-file readback during the code audit

The [auxiliary implementation audit](code_aux_tail_join_audit.md) now records
strict transport-only readback of54 preserved stages from actual auxiliary21,
22,23 and stronger24 B0 ZIPs. All passed the newly added launch/supervisor/
native-guard/capture checks. This supplements the earlier log-only records
above; it does not re-evaluate omitted full candidate payloads or acquire
the mathematical framework. The actual four ZIP hashes and native/BASIC
stage distinctions are retained in that audit. B1's new log is not included
in that four-export readback.

## Notebook07 RESTART: later supplied progress through18:22 Europe/Warsaw

The later supplied log has SHA-256
`4fe501b217ee928bd64b3fe5c6bc4b18a756783d6acdc523aead5774ceb17b69`.
The four full approximately30-minute chunks close138,143,138 and135 further
candidate leaves. The last sample has2,039 closed candidate leaves,
4,092 nodes and20 pending fields, still at k=7. Relative to the migrated
checkpoint,1,144 new nodes correspond to572 binary splits;570 additional
closed fields leave the pending count only two higher (18 to20).

This demonstrates continuing candidate-search work at a similar observed
chunk rate. It supplies neither a bound on descendants of the20 pending
fields nor a guarantee that the12-hour allowance suffices. Search arithmetic
and proof acceptance remain false in this log. No restart is indicated by
the stable pending count alone.

## Notebook19: stronger24 B2 completed scoped BASIC log

The later supplied B2 log has SHA-256
`87f28e02c14cfa9d3e899fa2f7d8ceb97daeb55f0524a6a37456c392dd470690`.
All15 selected stages complete, followed by a saved results ZIP at18:36:54
Europe/Warsaw on23 October2026. Its final state is
`complete_conditional_arithmetic_basic`; native acceptance remains false.

The nine original acceptors report closed-leaf totals
`740,1442,3248,6130,7102,3174,3067,1455,267`, summing to26,625.
The last printed count join reports7,963 because it covers only the four
mean-floor-patched indices33–36. `strong24_branches.count_jobs` selects
five original and four patched rows; its stage construction deliberately
skips the old full B2 join, which would include superseded panels. The
complete branch validator/final auxiliary collector must retain all nine
selected rows. A partial join total is not the full branch census.

The log reports a positive exact comparison margin for that last group.
This is completed scoped execution evidence from a supplied log, not a
fresh independent readback of the saved ZIP, acquisition of its resources
or a new global mathematical acceptance. No B3/B4/B5 completion is inferred.

## Notebook 20: stronger24 B3 completed scoped BASIC log

The supplied log has SHA-256
`f230d5210cd625ef7a68490d001af030ab29acc6ae2dd1f357a28064158a174f`.
It records all 24 selected stages completing. The final B3 count join reports
12,484 closed leaves, maximum score `422231693773/1000000000000`, a positive
exact comparison margin and `PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES`.
The terminal batch state is `complete_conditional_arithmetic_basic`.

The log reports `20261023T155406Z-eeee0789-results.zip` saved at
`2026-10-23T18:08:15.764033+00:00`, which is 20:08:15.764033
Europe/Warsaw on 23 October 2026 (UTC+2). This timestamp is the reported
bundle save, not an additional mathematical acceptance event.

This is supplied-log evidence only. The actual B3 ZIP, full original captures,
source bindings, execution sidecars and semantic interfaces have not been
revalidated for this record. The BASIC `native_arithmetic_accepted` flags remain
false, and the resource/analytic premises and final auxiliary join remain
separate. It does not establish sharp all-law n24, full n25 or the global
theorem; no B4/B5 branch completion is inferred.

## Notebook21: stronger24 B4 completed scoped BASIC log

The next supplied B4 log records all28 stages completing. Its eight selected
count acceptors cover panels23--30 with leaf counts164,256,433,693,791,724,598,
509, summing to4168. The final join reports the same total and
`PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES`, maximum score
`84445826977/200000000000` and a positive exact margin.

The bundle `20261023T163842Z-8f5bb9d0-results.zip` is reported saved at
`2026-10-23T18:15:30.451697+00:00` (20:15:30 Europe/Warsaw). The terminal state
is `complete_conditional_arithmetic_basic`. This is supplied-log evidence;
actual ZIP/sidecar/capture/source readback remains separate. BASIC native
acceptance stays false. The user is starting22; no B5 completion is inferred.

## New PREFIX2 final logs:03 B4q1 and05 B4q3

The supplied03 log has SHA-256
`b0acba714f52190b3913f21aab3ee668118de91656d4ef00f84fcea937d2d222`.
Search finishes with6304leaves,12582nodes and no pending field at
18:08:35UTC. Separate trusted-native replay ends in
`regional_count_arithmetic_accepted` at18:43:15UTC. The reported bundle is
`b4-q1/20261023T173630Z-c08f3ca5/20261023T173630Z-c08f3ca5-results.zip`.

The supplied05 log has SHA-256
`51f6d50c9200a09a259447ad951762d40c6ad257d0d02ad465cd86989a84aa92`.
Search finishes with7291leaves,14556nodes and no pending field at
17:59:12UTC. Separate full replay ends in scoped arithmetic acceptance at
18:45:38UTC. The reported bundle is
`b4-q3/20261023T173915Z-989ca66d/20261023T173915Z-989ca66d-results.zip`.

These are completed scoped native acceptance reports in supplied logs. Actual
ZIP/guard/capture/source readback remains separate. Their final scope is
`NEW_RESOURCE_LIMIT_EPOCH_CONDITIONAL_COUNT_ONLY`; parent acquisitions and
the all-index conclusion remain false. Other target completions are not
inferred from these two logs.

## ROOT4 second full pass and06/07 continuing search

The later ROOT4 log, SHA-256
`6a2d339173e4e763033ba0244970a79d4971b899a0ad58f2c1f4fe05abdaac2a`,
records production finishing at15:55:43UTC with all260classes, all1300HIGHslots
accounted and zero unresolved geometry classes. The exact conditional root
upper bound is4097/10000. A new complete replay starts at15:55:47UTC; the last
supplied progress has228closed classes/currentgrid228. This is32remaining
classes, not32fixed-duration jobs or a remaining-time percentage. No replay
completion is present.

The new06/07 logs preserve migration counts2208/2354 and progress to2652/2738
closed leaves. Both advance from k7 to k8 with continuing split/leaf decisions,
last pending16/14. Pending-frontier size does not bound future descendants.
No error/guard stop or complete candidate/native acceptance appears in these
supplied lines. Approximately400--450new closed leaves/hour describes those
intervals only, not a completion estimate.

## New PREFIX2 final logs:02 B4q0 and04 B4q2

The later02 log has SHA-256
`cf222324bac7602d7b1fd912398d29596549e9e6d76780750b51383d4757d6b2`.
Search completes6966leaves/13906nodes/pending0 at18:17:48UTC; separate native
replay reports `regional_count_arithmetic_accepted` at18:54:43UTC. The saved
bundle is `b4-q0/20261023T173533Z-3c55a3cd/20261023T173533Z-3c55a3cd-results.zip`.

The later04 log has SHA-256
`5e40041a0fd9f789f33f70717a046da2e91c64f7f46c31f3aaf1a72d5c94d8f6`.
Search completes8780leaves/17534nodes/pending0 at17:58:57UTC; separate native
replay reports scoped arithmetic acceptance at18:59:12UTC. The bundle is
`b4-q2/20261023T173624Z-bc1358b0/20261023T173624Z-bc1358b0-results.zip`.

Together with the03/05 logs, this reports all four B4 quarters accepted,
29341closed leaves in total. These remain supplied-log observations. The
actual four exports must still be revalidated and joined to their fresh
parent/resources by collector24. No B3, full n25 or all-index result is inferred.

## Notebook06: complete discovery, full native replay started

The next supplied log has SHA256
`30074e6f4a66cd2df11d2614f70b4e88cc83919e462a69e42fef81f3b71182e1`.
Target `b3-p31-v14-new` finishes discovery at19:12:09UTC
(21:12:09 Europe/Warsaw) with2819leaves,5612nodes and pending0. Its status is
`CANDIDATE_COMPLETE_NOT_ACCEPTED`. A separate `new_epoch_native_replay_started`
event selects all26roots immediately afterwards. The last supplied native
progress reaches100.676seconds without an error or guard stop, with sampled
RSS178847744bytes below the2GiB budget.

This is a transition to full replay, not final acceptance. The observed
`proof_accepted=false` is consistent with the ongoing stage. No completed
native receipt, final result ZIP or full n25 conclusion is inferred.

## Notebook35 first actual launch: runner memory gate, zero completed jobs

The actual user-downloaded `20261023T192537Z-01dab922-results.zip` is950667bytes,
SHA256 `2162466f17ce25936c1487def793b283f9f9de6ae23aaac987fcff345bf26a82`.
Its launch uses runtime7655cd1 and the complete326-job selection. The141304365B
source archive passes its pinned hash and source-cache preparation completes.
The first `support` subprocess then exits1 after0.533955318seconds, with reason
`nonzero_subprocess_exit` and actual stderr:

```
C5_SUPPORT_INCOMPLETE: Runner itself exceeds64MiB peak RSS
```

The native stdout is empty, `SESSION_RESULT.jobs=[]`, and no mathematical
stage is accepted. All n5/native/theorem flags remain false. The sampled outer
group peak4MiB reflects only its two samples; it is not the actual complete
process peak and cannot disprove the inner gate's observation.

The existing infrastructure/source-only fixtures did not exercise this real
Colab memory-counter startup. A separately reviewed Linux resource epoch is
being prepared; the original failed export, original supervisor and mathematical
sources remain preserved. No numerical success is inferred from the download
or from the earlier fixture passes.

## Notebook01: full scoped native acceptance reported

The next supplied log has SHA256
`0c404efc6b5b1b301f70f7ed90601fd32ceed1d09f6299bb289e134d9931e12d`.
Target `b3-p33` completes discovery at18:40:02UTC with10462leaves,
20898nodes and pending0. Separate full26-root native replay reports
`regional_count_arithmetic_accepted` at19:36:29UTC (21:36:29 Europe/Warsaw).
The reported bundle is
`b3-p33/20261023T173523Z-dd027bd6/20261023T173523Z-dd027bd6-results.zip`.

This completes the supplied-log acceptance observations for01--05. Actual
export/guard/capture/source readback and collector24's parent/interface joins
remain separate. The report preserves conditional-count-only scope and false
parent/full-theorem flags. No06/07 acceptance is inferred.

## Notebook06 accepted;07 entered complete native replay

The new06 log has SHA256
`853caa6649c7bfc0a255893502f653749e1e59ba39e9ab06d4c8a9d11e9b2bc8`.
The2819-leaf/5612-node candidate is followed by full26-root native replay,
`regional_count_arithmetic_accepted` at19:44:20UTC, and a saved bundle at
19:45:39UTC: `b3-p31-v14-new/20261023T173705Z-95cdbaee/20261023T173705Z-95cdbaee-results.zip`.
The scope remains `NEW_RESOURCE_LIMIT_EPOCH_CONDITIONAL_COUNT_ONLY`, with
parent acquisitions and all-index conclusion explicitly false. This completes
supplied-log acceptance observations for01--06; export readback remains separate.

The later07 log has SHA256
`a951557c67b9a8e4bab230d7b8f7326ab2d57f3a8079f8034e73b64dd04e9912`.
Discovery completes3134leaves/6242nodes/pending0 at19:47:39UTC, immediately
followed by native replay of all26roots. Its last observation is161.28seconds
into `trusted_native`, still `proof_accepted=false`. This is an ongoing full
replay, not final acceptance or an error. No07 result bundle is inferred.

## Notebook22: stronger24 B5 completed scoped BASIC log

The supplied log has SHA256
`2a0e46bc3a43329e829895bc390f421b3db7472d28641ef439964ec2ca43690c`.
All26stages complete; the final count join reports2444leaves, maximum score
`52778505603/125000000000` and a positive exact comparison margin. The final
state is `complete_conditional_arithmetic_basic`, with native acceptance false.
The reported bundle is `stronger24-b5/20261023T181807Z-d1c20667/20261023T181807Z-d1c20667-results.zip`,
saved at19:47:00UTC. All14--22 completion logs are now present. The actual
nine-export conditional evidence join by collector23 remains separate.

## Notebook36: actual completed B0 export and17interfaces read back

The supplied log has SHA256
`72bbd3dc587a2802c01629877472f67b54ccbd75bce21135dd27f4d9d10ae5bf`.
Both actions complete, followed by the bundle at19:43:57UTC, with state
`conditional_parent_acquisition_and_interfaces_complete`. The run begins
at19:16:07UTC; its observed full elapsed time is about28minutes. This is
an observation of this run, not a general Colab timing guarantee.

The actual downloaded `20261023T191607Z-38dfc33f-results.zip` is3639389bytes,
SHA256 `bbc929c336a1084c75d09433333d0eb93b640ddb9176913d53eaf2d84df15ce3`,
matching its actual private Drive sidecar. All189task members were transported
unchanged into a new bounded extraction and checked by the full current
`validate_prefix(...,"b0",2)` metadata validator. The root-level uppercase
and lowercase progress logs were kept in the original ZIP rather than
collapsed on Windows; neither is a task evidence input.

The actual INITIAL and global-resource receipts, source epoch, original
commands/working directories, preceding ledger hashes, captured successful
stdout/empty stderr and BASIC supervisor records pass. The exact resource
interface join reconstructs all17edges, proves the literal complete survivor
probability partition, and equals the saved `RESOURCE_INTERFACES.json`.
No mathematical kernel was imported or executed during this local readback.
This establishes preserved conditional computation evidence and exact
interfaces, not independent arithmetic repetition, count acceptance,
stronger24 acquisition or an unconditional all-law n25 result.

## Notebook39: lower-B5 global parent pair completed in supplied log

The supplied log has SHA256
`b073c5f3ca7b9091b7701d51ecf295f535e1a7693689d43181f63519f29848ab`.
The complete INITIAL/resource pair finishes2/2actions. Its resource terminal
marker is `PASS_FRESH_EXACT_SHARP25_B5_GLOBAL_RESOURCES`, with reported
resource-stage time1518.1538789272308seconds. The final state is
`conditional_global_parent_arithmetic_complete`; the bundle is saved at
19:55:14UTC as `n25-global-parents-b5/runs/20261023T191911Z-1f5e4d3b/20261023T191911Z-1f5e4d3b-results.zip`.

This is supplied-log evidence. Actual final export/sidecar/source/capture
readback and the separate local, mixed and count joins are still required.
No full n25 or all-index conclusion is inferred from the two global parents.

## Notebook37: B1 four-action parent/interface log completed

The supplied log has SHA256
`64cb4aaa5bb64becc7fd700a178df687e807d6809096ef4658bd4d9b3b564f0e`.
The last local accept completes4/4actions at20:02:10UTC and the final
`conditional_parent_acquisition_and_interfaces_complete` export is saved
at20:02:12UTC as `n25-parents-b1/runs/20261023T194405Z-8666b9c3/20261023T194405Z-8666b9c3-results.zip`.
This log reports the full selected B1 parent lane and interface assembly.
Actual export/sidecar/source/capture readback is a separate check; no B2,
count, unconditional n25 or all-index acceptance is inferred.

## Notebook33: seven middle-B5 count acceptors completed

The supplied log has SHA256
`3aeab2f141cdb25fc7bdbba8126224319eb3c9707133da33ba29243422ccf3db`.
It records all7selected full count acceptors,2446leaves, with24negative
controls for the final job and `reused=false`. The final state is
`selected_retained_count_arithmetic_accepted`. The bundle is saved at
20:03:30UTC as `n25-retained-extra-middle-b5/runs/20261023T200243Z-ea27e752/20261023T200243Z-ea27e752-results.zip`.
The actual export/native guards/captures/source readback remains separate;
parent acquisitions and the global conclusion are explicitly false.

Saved Drive output for29also contains ongoing trusted-native progress,
last sampled at20:02:36UTC in the inspected copy. Its code cells equal the
published notebook's cells. No completion is inferred from that progress.

## Corrected35: actual Linux startup regression fixture passed

The actual saved Drive fixture log `selftest-n5-remaining-20261023T194510Z-n5-remaining.log`
reports27tests, all passing in2.165seconds. In particular the previously
Windows-skipped `test_linux_preexec_peak_is_separate_and_postexec_growth_rejected`
ran and passed on Colab. This is an actual Linux infrastructure test result,
not a completed support calculation or acceptance of any of the326n5jobs.
No corrected35batch completion is inferred.

## Notebooks37and39: actual exported evidence read back

The actual37bundle `20261023T194405Z-8666b9c3-results.zip` is3366094bytes,
SHA256 `7cb3fd59ec7858f237022f05beace33463227c4eaa95fb622f7acb51fc2364d7`.
The actual39bundle `20261023T191911Z-1f5e4d3b-results.zip` is5498528bytes,
SHA256 `40040efb622ad76305ae2ae940263ef943177291ef1524485b8a350929ed6f94`.
Both match their actual downloaded private Drive sidecars. New bounded
task-only extractions preserve251/155members and30918702/85785440bytes
respectively; the original archives remain unchanged.

For37, `validate_prefix(...,"b1",4)` accepts the complete stage chain and
`n25_b012_interfaces.join` reconstructs35exact resource-to-contract edges
with complete closed survivor coverage, identical to the saved interface
object. The session reused three previously validated completed stages and
then completed the fourth; this is valid complete-prefix reuse, not partial
numerical resume. The prior completed-stage execution records are retained.

For39, `n25_b5_global_evidence.validate_completed` accepts both global stages,
their immutable source selection, full actual captures/commands/guards,
the deterministic INITIAL receipt and fresh timed resource receipt. The
INITIAL receipt retains SHA256
`5868ad7714c986a56405e596eb9c75bbface5a9321d5e82b4d23aa5290c8bac5`.
Its allowance is5/16; no stronger24 or local/mixed/count acquisition is inferred.

These checks execute only metadata, hash/JSON and exact rational interface
helpers. They do not import or run mathematical kernels. BASIC native flags,
analytic same-witness/full-n25/all-index conclusions remain false. This is
an internal same-system evidence readback, not external independent proof.

## Notebook34: six upper-beta3 count acceptors completed

The supplied log has SHA256
`10ea4b29f66ad869fa610c82ec280a1a4a6d1b279047ecfc616c0cc286feea70`.
All6selected acceptors finish4246leaves; the final job reports24negative
controls and `reused=false`. The state is
`selected_retained_count_arithmetic_accepted`; the export is saved at
20:07:51UTC as `n25-retained-extra-upper-high-beta3/runs/20261023T200609Z-98f2ca63/20261023T200609Z-98f2ca63-results.zip`.
This remains supplied-log evidence with separate export/source/guard readback,
parent acquisition and regional composition requirements.

## Notebook07: full scoped native acceptance reported

The final07log has SHA256
`c5b771de506940f5ad3064882de2ae05299dcd1aa50d5fca3c69b8a2933547b6`.
Following3134closed candidate leaves, the full26-root replay reports
`regional_count_arithmetic_accepted` at20:07:14UTC. The final export is saved
at20:08:33UTC as `b3-p32-v14-new/20261023T173850Z-ca51d9e6/20261023T173850Z-ca51d9e6-results.zip`.
All01--07nowhave supplied-log scoped native acceptance. The seven actual
exports and their09/10parent interfaces still require collector24. The
reported `NEW_RESOURCE_LIMIT_EPOCH_CONDITIONAL_COUNT_ONLY` scope preserves
false parent and global flags; it is not the complete n25 proof.

## Collectors23and24: final scoped joins reported

The user's inline23log records revalidation of all9selected exports14--22,
then `CONDITIONAL_FRESH_NUMERIC_CHAIN_VERIFIED`,83forests/76088leaves.
The final bundle was saved at20:17:29UTC as
`auxiliary24-join/20261023T201315Z-c98176d8/20261023T201315Z-c98176d8-results.zip`.
No attachment digest is assigned to that inline message. Universal C20,
stronger24 acquisition, analytic framework, full auxiliary and all-index
flags remain false. Actual final collector-bundle readback remains separate.

The24attachment has SHA256
`3a13065b286130f8fc92f3ca566b290c07487a7a515d9c0c8d273f43e1eab869`.
It records all9actual input exports revalidated:09/10and all seven fresh
01--07count exports. All7resource-to-count interfaces pass, followed by
`CONDITIONAL_SEVEN_N25_COUNT_INTERFACES_VERIFIED`. The bundle was saved at
20:23:04UTC as `n25-seven-interfaces/20261023T201326Z-b9ba9687/20261023T201326Z-b9ba9687-results.zip`.
This establishes the collector's reported scoped join, not full n25 regional
coverage, attained-contact/analytic premises, native promotion or all-index
acceptance. Actual final collector ZIP readback is a separate check.

## Notebooks26and32: completed retained count logs

The26attachment has SHA256
`7afd2608f7717d46c906b084baeee09d145029d35be1d513dcac3e307785ee44`.
It records17/17forests and12985leaves, with24controls and no reuse in the
last job. The final scoped native result is
`selected_retained_count_arithmetic_accepted`; the bundle was saved at
20:12:57UTC as `n25-retained-b0/runs/20261023T200813Z-281116a3/20261023T200813Z-281116a3-results.zip`.

The32attachment has SHA256
`f51638a55d952352130f60f5307d200e609d8694ec3169f8ba6bb2eed5a1634c`.
It records16/16forests,25257leaves and the same scoped status; its bundle
was saved at20:16:27UTC as
`n25-retained-extra-middle-b4/runs/20261023T200121Z-b9243cbe/20261023T200121Z-b9243cbe-results.zip`.
Both remain supplied-log observations with a separate actual final
export/source/guard readback boundary; no full regional theorem is inferred.

## Notebook38: actual B2 export and23interfaces read back

The completed38log has SHA256
`3a91df261a91baed04112e4ca812ae9a7abcbd52382421fe7c59f7467f92126b`.
The actual downloaded `20261023T191804Z-4ec6934d-results.zip` is4227973bytes,
SHA256 `7cc61bff1cf2a342f3ec104541fcddd241f9149edc9bca1e09f477296008c413`,
matching the actual104-byte private Drive sidecar. A new bounded task-only
extraction preserves238files/41318538bytes. All4fresh actions pass
`validate_prefix(...,"b2",4)`. The exact rational interface join reconstructs
all23edges with typed equality to saved `RESOURCE_INTERFACES.json`.
Together with actual36/37this covers17+35+23=75B012parent/interface edges.
These local checks read metadata/hashes/JSON and rational contracts only;
no numerical module is imported. Native/all-law/all-index flags stay false.

## Corrected35: support andHIGH completed, remaining batch ongoing

The actual saved corrected notebook code cells match the published V2.
Run `20261023T194522Z-6560588f` completes support at19:46:34UTC
(3protocols/19rows), then both selected HIGH protocols at19:58:25UTC.
Owncaps started at19:58:27UTC and was still running in the inspected
20:12UTC output. This supersedes the earlier fixture-only observation, but
does not establish completion of the326-job n5batch.

## Notebook11: both complete native ROOT4 passes and export revalidated

The final supplied log has SHA256
`9caabdb379d7e78e00b18e59c8b61f4db41f1f3edf3b3286c883b6f6a67b8c66`.
It records `conditional_physical_root_verified` and the final bundle at
20:27:38UTC. The actual `20261023T112903Z-63d200d0-results.zip` is12745098bytes,
SHA256 `5139f88952c3f989c6a5298a50293af70898658a075be3088347173590dffcb3`,
matching its actual104-byte private Drive sidecar. Bounded extraction
preserves363selected files/77645813bytes without modifying original captures.

The unchanged ROOT4metadata validators and actual launch/context/capture,
worker/controller filter, native guard and supervisor sidecars pass for both
full invocations. All70actual source commitments match. Production takes
15986.22723185seconds and independent full replay16295.686280629seconds;
both report260closed geometry classes, zero unresolved and1300HIGH slots,
with exact bound4097/10000. Both bind the same complete36903389-byte receipt,
SHA256 `571bc91b257ac53c640dd3bee91377565ff7c475091d39076295200209beeae1`.
Original absolute execution context is mapped in memory only, not rewritten.

The actual final report marks scoped native conditional physical ROOT4
arithmetic accepted. `all_law_C4_verified` and all-index remain false.
This same-system evidence readback runs no mathematical kernel and is not
an external independent mathematical proof.

## Notebooks41and43: complete selected finite count logs

The43attachment has SHA256
`4fbe926a734570a59f688ddcfb23c1939c70306c0ca16ed517b0a9bb7ff7ff78`.
It completes58/58forests with final status
`complete_selected_conditional_count_arithmetic_basic` and bundle
`finite9-counts/20261023T202945Z-e6e9d8aa/20261023T202945Z-e6e9d8aa-results.zip`.
Its final completed-stage export is saved at20:33:57UTC, about4min12s after
batch start. The supplied41log similarly completes72/72forests, with final
stage export at20:36:58UTC and bundle
`finite7-counts/20261023T202610Z-a536a0cc/20261023T202610Z-a536a0cc-results.zip`.
These are full conditional selected count batches, preserving false native,
parent acquisition, full finite69and all-index flags. Actual final ZIP
readback and source-to-parent semantic joins remain separate.

## Corrected12: current full tail replay still progresses

The current18-hour-run attachment has SHA256
`e34a69abe4b262e6ecfc7ca9675ac1016a6308d02c61f054b5b6bda2dab4c9e6`.
At20:35UTC it reports13/14top-level executions and25/41retained executions,
with elapsed time about7794seconds. Retained records increase20to25in the
last inspected interval. This is ongoing progress, not final arithmetic
acceptance. The original full driver has no completed-stage resume; changing
runtime starts its whole14/41invocation again. The18-hour ceiling is not an ETA.
