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
- Notebook 08 completed all six supplied n2/n3 arithmetic stages. The [observed-run record](proof/observed_runs.md) preserves the exact scope and execution details; the [standalone analytic review](proof/small_indices_analytic_review.md) records the separate reduction to unrestricted laws.
- No source research archives are deleted or rewritten.

The initial executable task is the reconstruction of seven missing **n=25** count forests. Five preserve original V12 designs; two are explicitly new conditional V14 epochs. They are not seven missing components of cutoff49.

## Colab

The first seven notebooks rebuild the missing n25 count forests. Notebook 08 checks n2/n3. The next independent batch, notebooks 09–12, rebuilds n25 INITIAL/resource premises, the complete n4 root and the retained tail49 arithmetic.

The numbered notebooks in `colab/` are preconfigured for separate CPU sessions. Notebooks 09–12 can run while 01–07 continue.
See [the English upload-and-run instructions](colab/README.md).

Account authentication is performed by the user. VM-local work and durable checkpoint storage must use distinct paths. A timeout preserves an incomplete candidate; it never produces a certificate.

## Sources and provenance

The previous [research repository](https://github.com/rodziewiczk/berry-esseen-045-certificate) is an immutable source of selected code and archives, not the working tree of this rebuild. Initial code reference: `75a94708872e2bc053f42a279559b23ed91e4402`.

Earlier papers: [v1](https://hexagonmath.org/2610.00147v1), [v2](https://hexagonmath.org/2610.00147v2), [v3](https://hexagonmath.org/2610.00147v3). Their statements must be checked against the current analytic reductions. Earlier claims are not used as new all-index theorems.

Only necessary frozen code belongs under `vendor/`. Each imported byte is hash-bound and retains its original attribution. Archives, generated trees and runtime logs are excluded from Git; accepted reproducibility assets will be published separately.

## Proof and paper

`proof/obligations.json` records the proof graph and unresolved edges. `proof/analytic_audit.md` records the initial analytic review; [the small-index review](proof/small_indices_analytic_review.md) and [primary-source statement checks](proof/literature_inputs.md) add the subsequent findings. A new concise English paper will follow the verified minimal graph, with explicit literature inputs and no unsupported all-index completion claim.

ChatGPT and Codex assist with proofs, certificates and writing, using the user-identified GPT-5.6 Sol, GPT-6.1 Sol and GPT-6 Astra models. This is not a claim of full human review or whole-paper formal verification.
