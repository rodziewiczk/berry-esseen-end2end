# Berry–Esseen: clean end-to-end reproduction

Authors: Kacper Rodziewicz and Bartosz Kołodziejek.

Start with [the current status](STATUS.md) and [the mathematical audit and
high-level proof graphs](proof/LOGICAL_AUDIT.md). The present priority is to
verify the logical and source-specific implications before adding compute jobs.
The follow-up [implementation and certificate-link audit](proof/CODE_INTERFACE_AUDIT.md)
records exact component matches, remaining enabled paths and the collector23 repair.

This repository rebuilds the computational proof obligations for the sharp iid Berry–Esseen constant from pinned public sources. It is a **work in progress**, not a completed proof of the conjecture.

For centered unit-variance iid laws with \(\rho(P)=E|X|^3\), the target is
\[
C_n=\sup_P\frac{\sqrt n\,\Delta_n(P)}{\rho(P)},\qquad
C^*=\sup_{n\ge1}C_n=\frac{3+\sqrt{10}}{6\sqrt{2\pi}}.
\]

Heavy mathematical calculations run in **Google Colab CPU sessions**. Local checks are limited to small infrastructure fixtures and source inspection. Separate sessions receive separate task directories; no two processes write the same forest or checkpoint.

## Current boundary

- Historical PASS records provide provenance and candidate certificates. They do not count as fresh acceptance in this repository.
- Search is untrusted. Complete native leaf replay, negative controls, source binding, domain coverage and analytic implication checks remain separate obligations.
- The global theorem remains open until every required node and edge passes a fresh complete run.
- Notebook 08 completed all six supplied n2/n3 arithmetic stages. The [observed-run record](proof/observed_runs.md) preserves the exact scope and execution details. The [standalone analytic review](proof/small_indices_analytic_review.md) and [checker source review](proof/small_indices_checker_review.md) found no blocking gap in the reviewed reductions and selected acceptance paths.
- No source research archives are deleted or rewritten.

The initial executable task is the reconstruction of seven missing **n=25** count forests. Five preserve original V12 designs; two are explicitly new conditional V14 epochs. They are not seven missing components of cutoff49.

## Colab

The current n25 count set is `01_RESTART_...` through `07_RESTART_...` in
`colab/`, with the matching notebook24. Its restored PREFIX2 discovery strategy
preserves saved trees, uses original lookahead/cuts/accelerators, and records an
explicit lossless checkpoint migration. Source/JSON migration was checked on
actual saved exports for all seven targets; this is not fresh leaf acceptance
or a measured speedup. All mathematical checks and the existing bounded resource
policies remain in force. The old01–07 and the separate q2-only25 are in
`colab/archive/`. See the [current execution instructions](colab/README.md) and
[cache handoff inventory](proof/count_cache_handoff.md).

The first seven notebooks rebuild the missing n25 count forests. Notebook 08 checks n2/n3. Notebooks 09–12 rebuild n25 INITIAL/resource premises, the complete n4 root and the retained tail49 arithmetic. Queued notebook 13 checks the independent n5 gap-free corner, including both infinite phase rays. Notebooks 14–22 replay the auxiliary n21–24 arithmetic supplying the selected n25 predecessor bound; notebook 23 joins their finished evidence.

The numbered notebooks in `colab/` are preconfigured for separate CPU sessions. Notebooks 09–12 can run while 01–07 continue.
See [the English upload-and-run instructions](colab/README.md).

Queued notebook24 imports the finished 01–07 and 09/10 bundles and verifies
their [seven conditional resource-to-count interfaces](proof/n25_collect_execution.md).
It preserves original evidence and does not repeat their heavy mathematics.
The [remaining n25 scope](proof/n25_completion_scope.md) and
[selected regional input inventory](proof/n25_regional_selection.json) keep
the other n25 domains explicit.

Queued notebooks26–28 freshly replay75 already complete retained B0--B2 count
forests,94,288 leaves. Each batch saves and fully revalidates completed stages
across sessions. These are additional conditional count components, with
parent/local resources and analytic implications still separate. See the
[retained execution scope](proof/retained_n25_execution.md).

Notebook35 now packages the remaining selected n5 arithmetic:326jobs including
295complete count forests, with validated completed-job reuse. Its
[execution specification](proof/n5_remaining_execution.md) keeps support,
parent/count semantic joins and the separate notebook13 gap-free result
explicit. Infrastructure preparation does not establish fresh numerical
acceptance or the unrestricted n5 theorem.

Notebook 53 now packages the complete selected n26--30 COUNT lane. Run 64 to
completion with the same Drive, then Run all in
[53_n26_30_conditional_counts.ipynb](colab/53_n26_30_conditional_counts.ipynb).
It revalidates the exact recovered historical tree and runs the other 79 full
acceptors. All 80 forests and their original controls are required; parent
acquisition and the all-law theorem remain separate. See
[the execution scope](proof/finite2630_execution.md).

Notebook56A is the separately runnable original auxiliary9--14 Fourier part
of the larger parent package56. It runs the full original plan, construction,
replay and independent readback with unchanged sources and controls. Choose
Run all in [56A_n10_14_auxiliary_fourier.ipynb](colab/56A_n10_14_auxiliary_fourier.ipynb).
Support/HIGH, INITIAL/resources and the217count interfaces remain separate.
See [its exact execution scope](proof/finite1014_parent_auxiliary_execution.md)
and [the bounded infrastructure review](proof/finite1014_parent_auxiliary_root_review.md).

The separate [56B_n10_14_supported_fourier.ipynb](colab/56B_n10_14_supported_fourier.ipynb)
runs the unchanged supported two-band Fourier calculation. It preserves the
explicit |X|<=3 premise; support acquisition and complete56remain separate.
See [its scope](proof/finite1014_supported_execution.md) and
[the bounded source/infrastructure review](proof/finite1014_supported_root_review.md).

The separate [56C_n10_14_highrho_fourier.ipynb](colab/56C_n10_14_highrho_fourier.ipynb)
packages the original high-rho Fourier calculation for literal n10--14.
Its finite integration, selected published tail and conditional analytic
premises remain distinct from full56. See [scope](proof/finite1014_highrho_execution.md).

The fourth original Fourier family is
[56D_n10_14_corner_fourier.ipynb](colab/56D_n10_14_corner_fourier.ipynb).
It covers the closed rho interval[23/20,71/50] with the explicit support3
premise. It leaves support acquisition and the remaining56parents/interfaces
separate; see [scope](proof/finite1014_corner_execution.md).

The shared scalar certificate has its own full original execution in
[56K_kappa_62_625.ipynb](colab/56K_kappa_62_625.ipynb). It checks all 81 cells,
1134 positive coefficients and original controls without repeating any Fourier
integration. Run all with the same Drive; see [scope](proof/finite1014_kappa_execution.md).
The current [notebook completion queue](proof/notebook_completion_queue.md)
separates delivered files, running jobs and packages still being implemented.

The current12-hour settings in RESTART01–07 are budgets, not completion estimates.
A complete tree still requires a separate full acceptor run. An unfinished tree
is checkpointed for a compatible rerun.

Account authentication is performed by the user. VM-local work and durable checkpoint storage must use distinct paths. A timeout preserves an incomplete candidate; it never produces a certificate.

## Sources and provenance

The previous [research repository](https://github.com/rodziewiczk/berry-esseen-045-certificate) is an immutable source of selected code and archives, not the working tree of this rebuild. Initial code reference: `75a94708872e2bc053f42a279559b23ed91e4402`.

Earlier papers: [v1](https://hexagonmath.org/2610.00147v1), [v2](https://hexagonmath.org/2610.00147v2), [v3](https://hexagonmath.org/2610.00147v3). Their statements must be checked against the current analytic reductions. Earlier claims are not used as new all-index theorems.

Only necessary frozen code belongs under `vendor/`. Each imported byte is hash-bound and retains its original attribution. Archives, generated trees and runtime logs are excluded from Git; accepted reproducibility assets will be published separately.

## Proof and paper

The [remaining-work roadmap](proof/remaining_work_roadmap.md) distinguishes the
current notebook queue from the complete theorem. The total number of remaining
notebooks is not yet established; several finite-range and analytic obligations
still need an executable source/acquisition map.

`proof/obligations.json` records the proof graph and unresolved edges. `proof/analytic_audit.md` records the initial analytic review; [the small-index review](proof/small_indices_analytic_review.md), [primary-source statement checks](proof/literature_inputs.md), and [the direct pointwise Prawitz proof](proof/prawitz_majorant_review.md) add the subsequent findings. A new concise English paper will follow the verified minimal graph, with explicit literature inputs and no unsupported all-index completion claim.

ChatGPT and Codex assist with proofs, certificates and writing, using the user-identified GPT-5.6 Sol, GPT-6.1 Sol and GPT-6 Astra models. This is not a claim of full human review or whole-paper formal verification.

The next work is specified in [the n5 interface review](proof/n5_analytic_review.md), [the finite-range source inventory](proof/finite_range_replay_inventory.md), and [the stronger24 premise audit](proof/stronger24_replay_scope.md). The [auxiliary execution package](proof/aux24_execution.md) implements the queued numerical work. The auxiliary-premise audit does not invalidate or require restarting the running conditional n25 jobs. Their final all-law composition still needs a freshly acquired matching premise and the complete resource/count joins.

The [bounded n25 forest inventory](proof/n25_missing_forest_inventory.md) distinguishes the historical report claiming completion from the seven selected forest payloads that were not located in the inspected packages. The available partial checkpoints and newly prepared V14 alternatives are explicitly identified; a historical result hash does not supply its missing certificate bytes.
