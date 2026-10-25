# Reuse of the earlier Lean development

This is a compatibility inventory, not a claim that all earlier proofs have
been imported or rechecked in this repository. The current skeleton assumes
source-exact analytic theorems explicitly; their full formal reproving is
outside the agreed scope. Existing formal lemmas are reusable evidence only
when their exact statement and assumptions match.

The read-only inventory scanned580 Lean source files under the earlier
`finite_cutoff_49/EventualExactness` tree. Its relative source names, SHA-256
hashes, import graph and declaration counts are in
[`reuse-inventory.json`](reuse-inventory.json). The scanner is reproducible:

```
python tools/inventory_existing_lean.py --source-root PATH_TO_EventualExactness
```

Import-graph reachability of a custom axiom is a conservative warning only;
actual logical dependence requires inspecting the theorem and `#print axioms`.
The scanner is not a replacement for a Lean parser or kernel audit.

| Earlier source | Current role / reuse decision | Compatibility boundary |
|---|---|---|
| `Foundations/ProbabilityLaw.lean` | Already reused, namespace/import rename | Concrete laws, convolution, normalized sums, rho/gamma and fixed-index supremum |
| `Foundations/OptimalConstant.lean` | Already reused, namespace/import rename | rho>=1, positive denominator, bounded/nonempty score sets, valid supremum API |
| `Foundations/Reflection.lean` | Candidate source for a future analytic orientation provider | Reflect the whole law; closed/open CDF handling and atoms must be retained |
| `TwoPoint/Constants.lean` | Candidate scalar lemmas with explicit normalization conversion | Earlier C_E writes sqrt(10)+3; current definition writes3+sqrt(10); prove the equality when adapting |
| `Defect/Algebra.lean`, `Defect/Exact.lean` | Correct source for the **matching moment defect** | rho-(gamma²+2)/sqrt(gamma²+4), not physical gap D and not ROOT4 eta |
| `Defect/BernoulliRepresentation.lean` | Candidate for its own matching-defect Fourier route | Its weighted measure uses the earlier matching defect; it is not automatically the ROOT4 common measure |
| `Defect/SmoothingScale.lean` | Matching-two-point smoothing-scale theorem | Do not substitute its defect parameter into a gap-resource price |
| `Shape/RationalInterval.lean` | Candidate verified arithmetic backend | `ClosedInterval` is the current semantic contract view, not a competing production arithmetic implementation |
| `Shape/Constants.lean` | Candidate outward radical/pi enclosures | Exact rational endpoints and soundness lemmas; no floating-point acceptance |
| `Outer/MomentCap.lean` | Candidate for its stated Shevtsova-derived rho cap | Bound/normalization differ from some stronger finite-index caps; check exact domain |
| `Prawitz/*` | Candidate source for a matching smoothing normalization | Current four-term Prawitz and compensated-hinge routes remain separate; kernel normalization factors must match |
| `Axioms.lean` | Trust-boundary reference, not imported wholesale | Three custom declarations: structural Shevtsova, Schulz binomial localization, lattice Edgeworth |
| Earlier `Main.lean` / eventual-theorem composers | Not used to prove the new all-index theorem | Avoid introducing a circular final-theorem assumption or a later tail into a finite export |

## Why similar names are insufficient

The older development contains names such as `physicalDefectTailCoefficient`.
That name alone does not identify the conserved-gap defect used in this
manuscript. Compatibility is decided by equations and quantifiers, not by a
shared English word. Three different excess/defect expressions are now named
separately in `Physical.lean` and `Root4.lean`.

The same rule applies to a bound at C_E versus a bound at4097/10000, a
weak<=target conclusion versus a strict margin, a finite index versus an
eventual statement, and one supported class versus all standardized laws.

## What an adapter must record

For every imported/adapted lemma, record its exact source declaration/hash,
domain, positive-denominator and integrability hypotheses, output inequality,
normalization conversion and the intended current contract. A source-exact
analytic theorem may remain an explicit trusted parameter in this skeleton.
A different statement needs a documented mathematical bridge; it is not an
implementation detail to be filled in later.
