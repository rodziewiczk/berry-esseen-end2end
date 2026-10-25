# Mathematical interface specification

The agreed goal is a detailed, source-aligned mathematical specification and
a solid Lean skeleton **assuming the correctness of the explicitly stated
analytic theorems**. A full Lean formalization of those analytic proofs is
outside this stage. Exact types, domains, conclusions and assembly are not.

The specification has the five parts requested for the project:

1. [Concrete mathematical states](01-state.md): laws, indices, contact floors,
   raw/normalized thresholds, signed moments, asymmetric support, the three
   different defects, weighted resources, conditional noise and joint budgets.
2. [Exact transition contracts](02-transitions.md): required inputs, analytic
   premises, outputs, gates, units, outward rounding and finite refinement.
3. [Complete covers and separate methods](03-covers-and-methods.md): n5, n25,
   floor31, all count roots, closed seams, zero cases, finite trees and tails.
4. [Certificate semantics and trust](04-certificates-and-trust.md): frozen
   rational job context versus an unknown law in the theorem's quantifiers;
   payload meaning, decoding, soundness, and unresolved/invalid results.
5. [Actual final assembly](05-assembly.md): the small-index, regional, finite,
   independent-tail and lower-bound interfaces construct the final conditional
   theorem. A final all-index conclusion is not imported as its own premise.

## Source-specific supplements

* [Small indices n2/n3](SMALL-INDICES.md): different bases, normalizations,
  moment domains, exact row meanings and positivity geometries.
* [Physical ROOT4](ROOT4.md): correct weak target below C_E, chosen bounded
  owner, canonical Q3/eta, common defect measure and complete physical cover.
* [Fourier families](FOURIER-FAMILIES.md): coherent physical LOW/HIGH,
  finite-window coefficients, Laguerre pointwise/uniform gates and a distinct
  complete four-term Prawitz route.
* [Complete HIGH families](HIGH.md): all six WINDOW50 terms, actual product
  event recipes, exact uniformity gates, compensated-power cells and infinite
  tails, with explicit conversion from scaled to unscaled HIGH.
* [Mixed n25 rules](MIXED.md): pointwise E, compatible chord bounds, same-law
  AB24 acquisition, finite feedback, and their distinct numerical conclusions.
* [Mixed reference registry](MIXED-REGISTRY.md): C/D/F/AB scopes, one-entry
  containment, earlier-license dependencies, admission and selected uses.
* [Ordinary COUNT rule catalogue](COUNT-RULES.md): exact selected replay
  obligations and the extra witnesses needed for a self-contained arithmetic trace.
* [Uniform local comparison](UNIFORM-TAIL.md): all actual n>=47, 83 panels,
  exact Bernoulli comparison, TINY/MID/LOW and a separate zero-noise case.
* [Independent tail assembly](TAIL-ASSEMBLY.md): five auxiliary resource
  barrier families, signed paired enclosures, smoothing and construction of
  the scalar tail contracts from typed analytic/numerical inputs.
* [Existing Lean reuse](reuse-ledger.md): the580-file source inventory and
  precise compatibility boundaries. Similar theorem names are insufficient.

## Auditing rule

The [adversarial audit](AUDIT.md) and its
[source-alignment/question register](implementation-questions.json) compare
Lean interfaces with the exact mathematical source, not merely something
similar. The user-provided reviewer note is tracked observation by observation;
its reported experiments are not reported as fresh results of this project.

Use the following status distinctions:

| Status | Meaning |
|---|---|
| Checked structural result | Lean proves the coverage, algebra or composition from its stated inputs |
| Accepted analytic theorem | Exact sourced statement supplied as a parameter under the agreed analytic-correctness assumption |
| Numerical evidence not connected | The mathematical meaning is fixed; an implementation must still produce and validate an object with that meaning |
| Specification BLOCK | A formula, scope, gate or semantic connection is missing or mismatched; this must be fixed mathematically, not guessed while coding |

The practical handoff rule is: implementation may choose algorithms, search
heuristics, cuts and scheduling within the declared contracts. It must not
choose the meaning of a coordinate, a normalization, a theorem's domain, a
strictness convention, or what acceptance proves.

The [visible interface map](../../assets/interface-map.svg) links these five
views to concrete Lean declarations. The complete
[proof graph](../../assets/proof-map.svg) shows the conditional final assembly.
