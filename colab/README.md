# CPU notebooks: upload and run all

Each notebook is preconfigured for a separate task. In Colab, select **Runtime → Run all**. You do not need to enter commands or change parameters.

Google may first ask you to authorize backups to your Drive. Results are saved under `MyDrive/Berry-Esseen-end2end/`, in separate directories named after the task and its start time.

| Notebook | Task |
|---|---|
| 01 | n25, original B3 p33 |
| 02–05 | n25, original B4 q0–q3 |
| 06–07 | n25, new conditional B3 V14 p31 and p32 |
| 08 | Full n2 and n3 arithmetic, with a separate platform and trust status |
| 09 | n25 B3: fresh INITIAL and all 100 resource panels, with both acceptors |
| 10 | n25 B4: fresh INITIAL and all 100 resource panels, with both acceptors |
| 11 | n4: full ROOT4 producer followed by a fresh complete replay |
| 12 | Tail from n49: all 14 top-level jobs and all 41 retained component replays |
| 13 | n5 gap-free corner: complete compact forest and both infinite phase rays |
| 14 | Auxiliary n21: all five INITIAL covers, 92,160 signed rectangles |
| 15 | Auxiliary n22: full INITIAL/resources and nine count forests, 258 leaves |
| 16 | Auxiliary n23: full INITIAL/resources and 21 count forests, 18,377 leaves |
| 17–22 | Stronger24 branches B0–B5: full global/local resources and 53 forests, 57,453 leaves |
| 23 | Import and revalidate all nine completed auxiliary jobs, then check the conditional numerical chain |
| 24 | Revalidate completed 01–07 and 09/10 exports and their seven conditional n25 resource-to-count interfaces |

In notebooks 01–07, the first short run measures the resources actually allocated. Subsequent slices use up to three hours of the allocated search budget. A complete candidate tree triggers a separate native acceptor. An incomplete result preserves its checkpoints. Rerunning the same notebook finds the latest valid Drive backup and rechecks its compatibility with the pinned sources before resuming.

Three hours is a search limit, not a promise of completion. Final acceptance takes additional time after a complete candidate is found; an unfinished search can require further resumed runs.

Each notebook displays progress: the current stage, elapsed time, resources, counters available in the checkpoints, and the result status. Full logs are also saved to files, with a Drive backup every minute. The final ZIP contains the task capsule's sources, primary and backup checkpoints when produced, reports, and logs. The notebook displays a ZIP link and attempts to download it.

Run multiple notebooks in separate CPU sessions. Each uses its own directories. Notebooks 09–12 are independent of the ongoing searches in 01–07 and can start immediately.

**Scope:** these are specific reproduction tasks, not a completed certificate of the whole proof. Notebooks 01–07 alone do not verify every parent resource acquisition, n4, the complete n6–48 continuation, or the tail. Missing acceptance or interrupted execution never produces a global PASS.

Notebook 08 runs the full six-stage n2/n3 arithmetic sequence. One complete Colab run has already been inspected; it does not need to be repeated merely to change resource-supervision metadata. See [the observed result](../proof/observed_runs.md) and [the execution scope](../proof/small_indices_execution.md).

The notebook code is pinned to a specific commit of the new public repository. Mathematical sources and resume hints have separate SHA-256 pins. Hints assist discovery; every leaf of a complete tree still requires fresh verification.

## Independent batch 09–12

Upload the selected notebook, choose a CPU runtime, and select **Runtime → Run all**. Source retrieval, lightweight runtime checks, actual calculation, progress logging, one-minute Drive backups and the final results ZIP are automatic. Do not interrupt running notebooks 01–07 to install this batch.

Start 09 and 10 in separate sessions to acquire the INITIAL and resource premises needed for the n25 join. Each performs four full stages, with a two-hour CPU ceiling per stage. The imported stronger24 input and the final join to the count forests remain separate work. See [the n25 execution scope](../proof/n25_parents_execution.md).

Notebook 11 is the longest task: one complete n4 production and one fresh full replay, each covering all 260 geometry classes and 1,300 HIGH request slots. Each pass has a 12-hour worker CPU ceiling and a 15-hour wall ceiling. These are limits, not measured runtime estimates. The original producer does not resume an interrupted full pass; backups preserve its evidence. The two passes may exceed one allocated Colab session. See [the ROOT4 execution scope](../proof/root4_execution.md).

Notebook 12 runs the unchanged full tail49 verifier with no quick mode. Its default wall ceiling is 130 minutes. This portable arithmetic run preserves the original exact sources and invocation census; the original Docker/cgroup execution contract and the uniform analytic implication remain separate. See [the tail49 execution scope](../proof/tail49_execution.md).

Use the corrected notebook 12 published after the inspected memory stop. It
sets a 2 GiB BASIC memory budget, replacing the original
512 MiB wrapper budget. Upload the replacement and choose Run all; no edits are
needed. Preserve the earlier incomplete result ZIP. The unchanged original
driver starts a fresh full run and has no internal stage resume. Other running
notebooks need no changes. [The failed-run review](../proof/tail49_failed_run_review.md)
records 13 completed top-level jobs and 28 completed retained components before
the sampled memory threshold stopped the next component.

These jobs do not complete n5, all remaining finite indices, the stronger24 acquisition, or the final analytic composition. Their results are concrete inputs for those next steps. Always retain the final ZIP, including when the run is interrupted or reports an unresolved case.

## Recovery after the notebook 04 node-limit stop

Notebook `25_n25_b4_q2_checkpoint_recovery.ipynb` continues the compatible q2
checkpoint from the same Drive. Upload it and choose CPU / Run all. It preserves
the original 4996 untrusted saved leaves and pending boxes, and uses a separately
sealed 100000-node resource epoch. Every mathematical source, contract, root and
leaf criterion remains unchanged; fresh independent replay of all 26 roots and
24 controls is still required. The old checker and original evidence are retained.

Use the updated `24_n25_seven_count_interfaces.ipynb` for the eventual evidence
join; the earlier pinned notebook 24 cannot recognize this new source identity.
Other current notebooks need no changes. See the [recovery execution scope](../proof/b4_q2_recovery_execution.md)
and [actual failed-run review](../proof/b4_q2_node_limit_review.md).

For `candidate_incomplete_budget_exhausted`, the original count notebook can be
run again: it automatically finds a compatible Drive checkpoint and allocates
another search period. This is the observed q1/q3 time stop and differs from
the fixed q2 node-limit stop. Do not interpret either partial status as acceptance.

## Queued task 13: an independent n5 component

Notebook 13 can wait until a CPU session is available. It uses the same upload-and-run workflow and does not require interrupting any ongoing task.

It checks all 60 compact roots, 1,994 nodes and 1,027 leaves, plus both infinite phase rays for the stated n5 gap-free corner. The selected arithmetic functions are unchanged. The new Linux protocol records its exact source pins and corruption controls; historical execution captures are not proof premises.

This component bounds the **positive closed-CDF discrepancy at every real threshold**, on its specified rho/beta rectangle. Its analytic reduction requires no predecessor estimate, bounded support, contact or physical gap. It does not alone establish the absolute Kolmogorov bound on that signed rectangle or the unrestricted n5 theorem. Other orientations and branches require the final n5 composition.

The default total CPU ceiling is two hours, with a 121-minute external wall ceiling. These are limits, not a measured runtime estimate. Logs, current-stage progress, one-minute Drive backups and a final results ZIP are automatic. An interrupted run has no internal numerical resume. See [the n5 gap-free execution scope](../proof/n5_gapfree_execution.md).

## Queued auxiliary-bound batch 14–23

Use the same workflow: upload one notebook, select a CPU runtime, and choose **Run all**. No parameter or command edits are required. Source downloads, selected infrastructure checks, progress output, one-minute Drive copies and final ZIP/SHA files are automatic. All sessions must save to the same Google Drive account so notebook 23 can find their results.

Notebooks 14–16 replay the coarse auxiliary chain at n21, n22 and n23. Notebooks 17–22 cover the six closed rho branches at n24, B0 through B5. These **nine numerical jobs may run independently in parallel**: their predecessor statements are explicit conditional inputs. Start them as sessions become available; running 01–07, 11 and 12 need no changes. The selected full route contains 83 count forests and 76,088 leaves, plus its INITIAL/resource/local covers. These counts are not a runtime estimate.

Run **23 last**, after all nine jobs have completed and saved their final ZIPs. It discovers their bundles automatically, verifies the archive hashes and complete exported execution evidence, and checks the exact auxiliary allowances and high-rho tail. Missing or incompatible results produce `WAITING_FOR_COMPLETED_JOBS`; rerun 23 after the missing work finishes. It does not rerun the expensive leaf calculations.

Each numerical action has a two-hour CPU ceiling and a 121-minute wall ceiling. A job contains several such actions and may outlive a session. In 14–16, compatible completed stage evidence is revalidated before reuse; an interrupted stage restarts in full. In this first version of 17–22, a new Run all starts a new branch epoch, preserving earlier evidence but **without automatic completed-stage reuse**. Their interrupted native actions have no internal checkpoint.

The numerical target is the auxiliary statement **C24 < CE + 1/80**, supplying the selected n25 contact allowance 5/16. These notebooks do not claim sharp C24 or the global theorem. The final numerical chain still requires the stated external estimates and retained same-law analytic implications. See [the auxiliary execution scope](../proof/aux24_execution.md), [n21–23 details](../proof/aux21_23_execution.md), and [the six n24 branches](../proof/strong24_branches_execution.md).

## Queued evidence join24

Run24 after notebooks01–07 and09/10 have saved their successful final ZIPs on
the same Google Drive. Upload and choose Run all; it discovers those results
automatically. It does not require23 to have finished to check the conditional
numeric interfaces. The auxiliary24 acquisition and analytic premises remain
separate requirements of the eventual theorem.

Missing or incompatible inputs produce `WAITING_FOR_N25_EVIDENCE`; rerun after
they finish. Available individual interfaces can be checked while others remain
pending. No search, native leaf replay, INITIAL cover or resource computation
is repeated merely to validate the preserved exports at their new paths.

The successful selected-interface state concerns exactly seven count targets,
including all four closed B4 p29 quarters and the two new conditional V14
contracts. It does not complete the other n25 branches or the all-index proof.
Keep the final evidence ZIP. Progress and one-minute Drive copies are automatic.
See [the exact execution scope](../proof/n25_collect_execution.md).

## Corrected notebooks 06 and 07

The original V14 preparations stopped before mathematical evaluation because a contract filename differed in letter case. The corrected notebooks use a newly sealed portable source epoch. Upload the replacement notebooks and select **Run all**. Existing archive downloads can be reused after their hashes are checked.

The corrected V14 tasks start from all 26 original roots. Historical V14 hint/checkpoint bindings do not match the new closure; later checkpoints from the corrected epoch can be resumed. See [the portability derivation](../proof/v14_portability.md). Running notebooks 01–05 do not need to be interrupted for this repair. Notebook 08's observed six-stage completion is recorded [with its explicit trust limits](../proof/observed_runs.md).
