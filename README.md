# Berry–Esseen: clean end-to-end reproduction

Authors: Kacper Rodziewicz and Bartosz Kołodziejek.

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
`colab/`, with the current notebook24. It restores the seven inspected candidate
caches and uses explicit larger finite-tree/time/memory policies while preserving
all mathematical checks. The old01–07 and the separate q2-only25 are in
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

The three-hour setting in notebooks 01–07 is a search budget, not a completion estimate. A complete tree still requires a separate full acceptor run. An unfinished tree is checkpointed for a compatible rerun.

Account authentication is performed by the user. VM-local work and durable checkpoint storage must use distinct paths. A timeout preserves an incomplete candidate; it never produces a certificate.

## Sources and provenance

The previous [research repository](https://github.com/rodziewiczk/berry-esseen-045-certificate) is an immutable source of selected code and archives, not the working tree of this rebuild. Initial code reference: `75a94708872e2bc053f42a279559b23ed91e4402`.

Earlier papers: [v1](https://hexagonmath.org/2610.00147v1), [v2](https://hexagonmath.org/2610.00147v2), [v3](https://hexagonmath.org/2610.00147v3). Their statements must be checked against the current analytic reductions. Earlier claims are not used as new all-index theorems.

Only necessary frozen code belongs under `vendor/`. Each imported byte is hash-bound and retains its original attribution. Archives, generated trees and runtime logs are excluded from Git; accepted reproducibility assets will be published separately.

## Proof and paper

`proof/obligations.json` records the proof graph and unresolved edges. `proof/analytic_audit.md` records the initial analytic review; [the small-index review](proof/small_indices_analytic_review.md), [primary-source statement checks](proof/literature_inputs.md), and [the direct pointwise Prawitz proof](proof/prawitz_majorant_review.md) add the subsequent findings. A new concise English paper will follow the verified minimal graph, with explicit literature inputs and no unsupported all-index completion claim.

ChatGPT and Codex assist with proofs, certificates and writing, using the user-identified GPT-5.6 Sol, GPT-6.1 Sol and GPT-6 Astra models. This is not a claim of full human review or whole-paper formal verification.

The next work is specified in [the n5 interface review](proof/n5_analytic_review.md), [the finite-range source inventory](proof/finite_range_replay_inventory.md), and [the stronger24 premise audit](proof/stronger24_replay_scope.md). The [auxiliary execution package](proof/aux24_execution.md) implements the queued numerical work. The auxiliary-premise audit does not invalidate or require restarting the running conditional n25 jobs. Their final all-law composition still needs a freshly acquired matching premise and the complete resource/count joins.

The [bounded n25 forest inventory](proof/n25_missing_forest_inventory.md) distinguishes the historical report claiming completion from the seven selected forest payloads that were not located in the inspected packages. The available partial checkpoints and newly prepared V14 alternatives are explicitly identified; a historical result hash does not supply its missing certificate bytes.
