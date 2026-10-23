# CPU notebooks: upload and run all

Each notebook is preconfigured for a separate task. In Colab, select **Runtime → Run all**. You do not need to enter commands or change parameters.

Google may first ask you to authorize backups to your Drive. Results are saved under `MyDrive/Berry-Esseen-end2end/`, in separate directories named after the task and its start time.

| Notebook | Task |
|---|---|
| 01 | n25, original B3 p33 |
| 02–05 | n25, original B4 q0–q3 |
| 06–07 | n25, new conditional B3 V14 p31 and p32 |
| 08 | Full n2 and n3 arithmetic, with a separate platform and trust status |

In notebooks 01–07, the first short run measures the resources actually allocated. Subsequent slices use up to three hours of the allocated search budget. A complete candidate tree triggers a separate native acceptor. An incomplete result preserves its checkpoints. Rerunning the same notebook finds the latest valid Drive backup and rechecks its compatibility with the pinned sources before resuming.

Each notebook displays progress: the current stage, elapsed time, resources, counters available in the checkpoints, and the result status. Full logs are also saved to files, with a Drive backup every minute. The final ZIP contains the task capsule's sources, primary and backup checkpoints when produced, reports, and logs. The notebook displays a ZIP link and attempts to download it.

Run multiple notebooks in separate CPU sessions. Each uses its own directories. The available concurrency depends on the actual Colab allocation; several browser tabs do not automatically mean several machines.

**Scope:** these are specific reproduction tasks, not a completed certificate of the whole proof. Notebooks 01–07 alone do not verify every parent resource acquisition, n4, the complete n6–48 continuation, or the tail. Missing acceptance or interrupted execution never produces a global PASS.

Notebook 08 runs the full six-stage n2/n3 arithmetic sequence. Its default compile-and-spawn C++ run uses basic resource supervision and explicitly reports an untrusted guard; successful computation is not promoted to trusted native acceptance. See [the small-index execution scope](../proof/small_indices_execution.md).

The notebook code is pinned to a specific commit of the new public repository. Mathematical sources and resume hints have separate SHA-256 pins. Hints assist discovery; every leaf of a complete tree still requires fresh verification.
