# B4 q2 checkpoint recovery in a declared resource epoch

This describes the first q2-only profile published with notebook25. The current
operational set is [unified RESTART01–07](count_restart_execution.md), whose04
supersedes25. The original profile and its records remain reproducible in Git.

Notebook 25 continues the actual saved candidate from the interrupted notebook 04.
The [inspected ZIP review](b4_q2_node_limit_review.md) establishes the failure:
the original global 10000-node ceiling, 4996 untrusted saved leaves and 17 pending
boxes. No completed native replay exists for that run.

The original checker also enforces 10000 nodes during acceptance. Increasing only
the search cap would therefore not solve the acceptance problem. The original
driver, checker, design, checkpoint ZIP and notebooks 01–07 retain their identities.

## Exact new source identity

The new profile uses a 100000-node global ceiling and the original depth128 cap.
The sole original-source byte replacement is `LIMIT=10000` to `LIMIT=100000`.
The source adapter verifies the entire AST, every function AST, both occurrences
of `visited <= LIMIT`, and that every other source byte is identical. No formula,
leaf criterion, kernel, contract, count root, target or corruption control changes.
This changes a finite resource restriction; the mathematical implication of a
fully replayed forest is preserved.

- Original design: `2517c1b8c79949bad93eecdcaa43e389344411fd4c71d5d516dde1e40b732e2a`.
- New externally pinned design: `866eec6360d31f80931ddd9edfb87c4218caa23c8f06346ba8362f093b110e6a`.
- New checker: `f535bae9054163b57206e2bdffe2afae96b5c0bfb28b3efa4533c88d037ca376`.
- Unchanged contract: `0576748a8e4deb2450fea8fc7b1b06898dd8bd3ae2d5fc3465163a123d9425c3`.

The new design seals the original design/checker copies, every original numerical
source and an explicit resource-epoch record. A new successful receipt belongs
to this new profile, even though the unchanged native accept function retains its
historical terminal status literal. The recovery wrapper and evidence validator
always expose the new scope and source pins.

## Resume and independent acceptance

Upload notebook 25 to Colab, select CPU and Run all, and authorize the same Drive.
The controller locates the original pinned source closure in the live backups.
It selects a compatible saved checkpoint and copies the old bytes separately.
Migration changes only the design and checker pins in a new checkpoint; every
saved tree, closed leaf payload and pending box is retained as untrusted data.
No compatible backup means a preserved incomplete error, never a silent restart.
Later invocations can also resume this profile's own compatible checkpoints.

Discovery uses the unchanged frozen search worker. When it finishes, a new private
acceptance capsule recomputes every leaf of all26 roots and all24 corruption
controls. The original strict Linux native guard, actual script/supervisor pins,
complete captures, full forest census and exact receipt checks remain required.
There is no fallback to BASIC arithmetic acceptance. The original 512MiB native
policy, two-hour CPU limit and bounded external wall policy remain unchanged.

Progress and one-minute Drive backups remain automatic, including on failure.
The three-hour search allocation is a budget, not an estimate or a promise that
100000 nodes suffice. Partial checkpoints remain useful candidates and cannot
establish arithmetic acceptance.

## Composition boundary

Use the updated notebook 24 after a successful recovery and completion of its
other count/parent inputs. Its narrow additional evidence route accepts the fixed
new resource epoch only for logical b4-q2 and preserves its exact identity in the
joined result. The unchanged original contract feeds the same resource interface.
No tenth logical count job is introduced, and other running jobs need no changes.

Fresh regional arithmetic remains conditional on the original parent acquisitions
and analytic/framework premises. Neither the resource port, migration, discovery,
native count acceptance nor the seven-interface join proves the full n25 theorem
or the all-index theorem. Local implementation checks parse sources and use
synthetic orchestration fixtures; no original numerical kernel is executed locally.
