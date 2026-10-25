# Berry–Esseen · the Lean proof map

**Mathematical contracts → checked Lean composition → remaining proof obligations.**

![Berry–Esseen proof map: green checked implications, amber open contracts, blue concrete probability model](assets/proof-map.svg)

[Open the full graph](assets/proof-map.svg) · [PNG version](assets/proof-map.png) ·
[Source-linked map](docs/proof-map.md) · [Current plan](docs/plan.md) ·
[Mathematical contracts](docs/mathematical-contracts.md)

This repository contains the first two stages of the project: mathematical
contracts and a thin Lean skeleton. Green boxes are **proved conditional
implications**. Amber inputs remain open in this formal development. The
concrete probability semantics use real measures, convolution sums, the
Gaussian CDF and actual suprema.

The complete local check passed for **8 Lean files**, without `sorry`, custom
`axiom` declarations or `native_decide`. The source-bound report records
**41 seconds for the logical core** and **2 minutes 51 seconds for the full
check**, using an existing compiled mathlib cache. These are local compiler
results, rather than a GitHub Actions run. Analytic and certificate assumptions
are still explicit theorem parameters.

## The current plan

| Stage | Status | What it provides |
|---|---|---|
| Mathematical inventory | Version 0.1 available | Exact target, normalizations, cases and open proof contracts |
| Conditional Lean map | Checked | Finite 1–48, all 20 n25 regions, independent 49+ tail and final composition |
| Discharge assumptions | Next | Reuse matching existing lemmas; prove covers, analytic interfaces and numerical soundness |
| Detailed execution architecture | Later | Design only after the mathematical interfaces stabilize |
| One CLI | Later | Implement resumable proof execution against those contracts |

The next concrete steps are to formalize the remaining n5 and floor31 covers,
replace abstract resource predicates with exact mathematical records, and
connect matching lemmas from the earlier Lean work. The separate lower-bound
approximation remains visible. See the [detailed plan](docs/plan.md).

## What the checked map contains

| Branch | Checked composition |
|---|---|
| Finite 1–48 | Strong induction, preserving the quantitative n3→n4 and n4→n5 inputs |
| n25 | 20 closed rational regions; signed-beta envelope inputs; same-witness exclusions |
| Predecessor alternatives | Sharp24 OR auxiliary24 implies the same-law q25≤5/16 allowance |
| Independent 49+ | Three backward losses give base 49; first-failure induction covers later indices |
| Final upper bound | Finite and tail branches cover every positive integer |
| Sharpness | The upper bound plus a separate lower approximation gives the exact global supremum |

There is **no finite 1–48 → tail49+ dependency**. The graph preserves this
independence. It also distinguishes the n25 alternative licenses rather than
requiring both.

## Source layout

| File | Role |
|---|---|
| [`BEMap/Finite.lean`](BEMap/Finite.lean) | Finite induction and predecessor alternatives |
| [`BEMap/Cover25.lean`](BEMap/Cover25.lean) | Exact rational region coverage |
| [`BEMap/Tail.lean`](BEMap/Tail.lean) | Independent scalar tail composition |
| [`BEMap/Foundations/`](BEMap/Foundations/) | Reused probability model and elementary bounds |
| [`BEMap/Interfaces.lean`](BEMap/Interfaces.lean) | Contacts, same-law pipelines and the n25 bridge |
| [`BEMap.lean`](BEMap.lean) | Concrete final upper and sharpness statements |
| [`Audit.lean`](Audit.lean) | Theorem signatures and logical axiom lists |

## Check using the existing local installation

Run from this folder in PowerShell:

```powershell
.\check.ps1 -Scope Core
.\check.ps1
```

The helper detects Lean on PATH, or the installed Lean 4.32.0 toolchain under
the current user profile. It defaults to the earlier mathlib cache at
`$env:USERPROFILE\Desktop\eventual_exactness_proof`. Override these with parameters
or the `BEMAP_MATHLIB_WORKSPACE` and `BEMAP_LEAN_EXE` environment variables:

```powershell
.\check.ps1 -MathlibWorkspace 'C:\path\to\existing-project' `
  -LeanExe 'C:\path\to\lean.exe'
```

The script verifies the toolchain and mathlib revision, then rechecks this
project's modules directly with Lean. It does not recompile the dependency
library or run numerical kernels. It writes measured times, source hashes and
compiler output to `check-All.json` and `check-All.log` (or `check-Core.*`).
This is a **direct compiler check**, not a claim that a fresh `lake build` was
executed. The supplied report describes the actual successful check.

Measured on the existing installation: the three core modules took about
41 seconds altogether; the full eight-module check, including the concrete
probability model and axiom audit, took 171.486 seconds (2 minutes 51 seconds).
These timings reuse compiled mathlib dependencies. The complete Lean source
is 856 lines, including 377 lines of reused probability foundations.

## Recreate a portable Lake project

The project pins Lean 4.32.0 and mathlib commit
`81a5d257c8e410db227a6665ed08f64fea08e997`. With Lean/Elan and Git available:

```text
lake update
lake exe cache get
lake build
lake env lean Audit.lean
```

On a new machine the first preparation includes fetching dependencies and
their compiled cache; its duration is distinct from checking the small map.
Do not change the pinned Lean version independently of mathlib. The optional
PowerShell helper needs an existing dependency cache; the standard Lake route
does not require the original author's filesystem paths.

## Regenerate the visible graph

```text
python tools/render_proof_map.py
```

The script uses the Python standard library. It validates the recorded Lean
source hashes, declaration anchors and acyclicity of the grouped diagram, then
writes the SVG, Mermaid source and JSON. The checked-in PNG is a rendered copy
of the SVG. The map is a curated view of the theorem interfaces, not an
export of internal kernel proof terms.

## Companion repositories and provenance

* [Original end-to-end research repository](https://github.com/rodziewiczk/berry-esseen-end2end)
* [The proof-map branch there](https://github.com/rodziewiczk/berry-esseen-end2end/tree/lean/proof-map)
* [Standalone Lean map](https://github.com/rodziewiczk/berry-esseen-lean-map)

The research baseline is commit `6ca9730273c81447be4863824c0b7d012db0e8b8`.
The original research work in progress was preserved. The two foundational
Lean modules are reused with namespace/import renaming; their hashes and
source identity are recorded in [`provenance.json`](provenance.json).
The original MIT notice is retained in [`LICENSE`](LICENSE).

The current scope is mathematical contracts and their Lean composition.
No numerical runner, cloud system or production CLI is implemented here.
