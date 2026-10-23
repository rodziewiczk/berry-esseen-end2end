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

In notebooks 01–07, the first short run measures the resources actually allocated. Subsequent slices use up to three hours of the allocated search budget. A complete candidate tree triggers a separate native acceptor. An incomplete result preserves its checkpoints. Rerunning the same notebook finds the latest valid Drive backup and rechecks its compatibility with the pinned sources before resuming.

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

These jobs do not complete n5, all remaining finite indices, the stronger24 acquisition, or the final analytic composition. Their results are concrete inputs for those next steps. Always retain the final ZIP, including when the run is interrupted or reports an unresolved case.

## Queued task 13: an independent n5 component

Notebook 13 can wait until a CPU session is available. It uses the same upload-and-run workflow and does not require interrupting any ongoing task.

It checks all 60 compact roots, 1,994 nodes and 1,027 leaves, plus both infinite phase rays for the stated n5 gap-free corner. The selected arithmetic functions are unchanged. The new Linux protocol records its exact source pins and corruption controls; historical execution captures are not proof premises.

This component bounds the **positive closed-CDF discrepancy at every real threshold**, on its specified rho/beta rectangle. Its analytic reduction requires no predecessor estimate, bounded support, contact or physical gap. It does not alone establish the absolute Kolmogorov bound on that signed rectangle or the unrestricted n5 theorem. Other orientations and branches require the final n5 composition.

The default total CPU ceiling is two hours, with a 121-minute external wall ceiling. These are limits, not a measured runtime estimate. Logs, current-stage progress, one-minute Drive backups and a final results ZIP are automatic. An interrupted run has no internal numerical resume. See [the n5 gap-free execution scope](../proof/n5_gapfree_execution.md).

## Corrected notebooks 06 and 07

The original V14 preparations stopped before mathematical evaluation because a contract filename differed in letter case. The corrected notebooks use a newly sealed portable source epoch. Upload the replacement notebooks and select **Run all**. Existing archive downloads can be reused after their hashes are checked.

The corrected V14 tasks start from all 26 original roots. Historical V14 hint/checkpoint bindings do not match the new closure; later checkpoints from the corrected epoch can be resumed. See [the portability derivation](../proof/v14_portability.md). Running notebooks 01–05 do not need to be interrupted for this repair. Notebook 08's observed six-stage completion is recorded [with its explicit trust limits](../proof/observed_runs.md).
