# Current plan: mathematical contracts -> Lean -> execution system

Checkpoint: 25 October 2026. The present milestone is a checked conditional
map with concrete probability semantics. The theorem inputs are visible, and
their analytic and numerical proofs remain separate work.

The [visible proof map](../assets/proof-map.svg) and
[declaration-by-declaration guide](proof-map.md) show this boundary.

## What is already available

* The exact probability-law model, normalized iid sums, rho positivity and the
  elementary supremum API are reused from the earlier Lean development.
* The finite 1--48 induction preserves the strong n3 input needed by n4 and the
  quantitative n4 input needed by n5.
* The n25 map includes20 closed rational regions, both predecessor-license
  alternatives and their same-law allowance implication.
* The scalar tail proves the base 49 and every later index from explicit tail
  contracts. It does not take the entire finite theorem as an input.
* The final upper-bound and exact-supremum implications compile. All 8 checked
  source files are bound by SHA-256 in the verification report.

These are checked implications. They do not establish the missing analytic
lemmas or soundness of the external numerical certificates.

## 1. Finish the mathematical interfaces

First close the specification gaps which can change downstream theorem types:

1. Formalize the complete n5 low-domain/corner/Fourier/tail cover and the eight
   floor31 bands, including all shared endpoints. These covers are currently
   inventoried in the specification, rather than proved in Lean.
2. Turn the generic `High`, `OwnCap`, `Initial` and `Resources` predicates into
   explicit mathematical records with units and side conditions. Retain the
   same law, contact threshold, signed beta, physical D, weighted nD and lambda.
3. State each actual-index transfer, including the n25->24 mixed argument and
   the floor25/floor31 transfers, with the exact target-index normalization.
4. Give every numerical family a semantic conclusion and a complete domain.
   Specify failed guards, zero denominators, zero noise, all original count
   roots, strict outgoing events and closed incoming events.

Acceptance criterion: every external computation has one unambiguous theorem
to provide, with all incoming assumptions listed. No parser or cloud design is
needed to settle these mathematical statements.

## 2. Reuse the existing Lean proofs before writing replacements

Audit the earlier formal development lemma by lemma. For a reusable lemma,
record its declaration, assumptions, normalization, imported axioms and
connection to this source baseline. Import or adapt only matching statements.
Do not import an older all-index conclusion as a premise for the new final
theorem, and do not import a global composer to stand in for a finite export.

Start with the small, local obligations: exact constant comparisons,
signed-beta envelopes, closed covers, same-law predecessor implications and
support/moment side conditions. Then connect contact extraction, unrestricted
localization and the first-variation majorant.

Acceptance criterion: each replaced assumption becomes a named proved lemma;
the final theorem signature visibly loses that assumption or obtains it from
an explicit proved construction.

## 3. Connect the conserved identity and resource deductions

Prove the qualitative-support-before-higher-moments order, the nonnegative
physical defect and the conserved identity for one contact. Build finite
resource intersection theorems which preserve simultaneous bounds for that
same contact. Preserve common moments and defect measures across frequencies.

Acceptance criterion: instantiate `ContactPipeline` with actual inequalities,
with no untyped acceptance flags and no unsupported fixed-point step.

## 4. Discharge numerical soundness and branch contracts

Connect exact/interval numerical proofs to the mathematical records. Search
outputs remain candidate evidence until a sound checker proves the stated
leaf obligations and complete domain coverage. Existing computation results
must be connected to their exact sources and assumptions; a historical PASS
does not automatically instantiate a Lean proof field.

The first targets are the strong n3->n4 interface, complete n5, the 20 n25
regions and their ordinary/mixed distinctions, actual-index finite exports,
and the independently acquired tail ceilings. Derive the first-failure0.29
consequence from the actual smoothing theorem, and connect both positive-noise
and zero-noise cases of the uniform local exclusion.

Acceptance criterion: construct concrete `FiniteContracts` and `TailContracts`
objects from the proved analytic and numerical results, rather than leave
those objects as assumptions of the final theorem.

## 5. Supply the separate lower approximation

Connect the rational Bernoulli lattice expansion, compatible index subsequences
and continuity/optimization argument to `LowerApproximation`. It requires
arbitrarily good values below C_E, not attainment at one fixed finite index.

Acceptance criterion: instantiate `sharp_global_constant` with all its inputs
proved. The conditional map alone is not this milestone.

## 6. Only then specify the execution system

Once the mathematical contract types are stable, design task and certificate
formats, source-bound cache keys, checker boundaries, resumability, storage
and cloud execution. Then implement the single user-facing CLI.

The intended order remains:

```
mathematical contracts -> Lean interfaces and proofs
                      -> detailed system architecture -> one CLI
```

No runtime architecture or cloud runner is being implemented in this repository
at this checkpoint. Its current purpose is to make the proof obligations and
their composition precise enough to guide that later design.

## Keeping the map honest

* A green node means a checked conditional implication or an elementary proved
  foundation, not completion of all its incoming assumptions.
* An amber node is open **in this Lean project**; this does not adjudicate all
  proofs or computations elsewhere in the research repository.
* The local report records 171.486 seconds for all 8 files using an existing
  compiled mathlib cache. It is not a GitHub Actions run.
* Regenerate the diagram after interface changes and recheck any changed Lean
  source. `tools/render_proof_map.py` rejects stale recorded source hashes and
  missing declaration anchors.
