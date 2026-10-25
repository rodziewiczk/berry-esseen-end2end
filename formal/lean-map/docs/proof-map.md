# The proof map linked to Lean declarations

![Berry--Esseen: checked Lean composition and open contracts](../assets/proof-map.svg)

[Open full SVG](../assets/proof-map.svg) · [PNG](../assets/proof-map.png) ·
[Machine-readable map](proof-map.json) · [Current plan](plan.md)

Green means **a proved implication with explicit inputs**. Amber means a
precisely stated analytic premise or numerical evidence still to supply. Blue
is the concrete probability model and its elementary proved API. The local
compiler report lists every checked source; it did not run the numerical
notebooks. Analytic correctness is accepted explicitly at this milestone.

![Five detailed mathematical interfaces](../assets/interface-map.svg)

[Full interface view](../assets/interface-map.svg) ·
[Source anchors](interface-map.json) · [Five-part specification](contracts/README.md)

This is a curated, grouped map of the Lean theorem interfaces, not an automatic
export of the kernel's proof-term graph. Where several assumptions are grouped
in one box, consult the theorem signature for their exact conjunction. The
additional predecessor bridge is displayed separately: its conclusion is one
of the possible licenses used by a future regional exclusion proof, rather
than an extra argument of `n25_cover`.

## Exact declarations behind the boxes

| Box | Lean declaration | Meaning at this checkpoint |
|---|---|---|
| Concrete model | [`normalizedScore_le_optimalConstant`](../BEMap/Foundations/OptimalConstant.lean) | Genuine law/CDF/supremum semantics, not an arbitrary score variable |
| Small/ROOT4/n5 providers | [`EndToEndProviders`](../BEMap/Assembly.lean), [`ConstantComparisons`](../BEMap/Global.lean) | Method-specific inputs and quantitative targets remain explicit |
| Ordinary finite methods | [`FixedIndexMethodProvider`](../BEMap/Assembly.lean), [`MethodEvidence`](../BEMap/TypedPipeline.lean) | Actual-index evidence has typed state and certificate semantics |
| Finite range | [`finite_composition`](../BEMap/Finite.lean) | Checked strong-induction composition for every 1<=n<=48 |
| n25 inputs | [`TwentyFiveProvider`](../BEMap/Assembly.lean), [`MiddleEnvelope25`, `HighEnvelope25`](../BEMap/Cover25.lean) | Extraction, signed-beta envelopes and all scoped regional methods |
| n25 closed cover | [`n25_cover`](../BEMap/Cover25.lean) | All 20 listed cells cover the feasible domain, assuming the envelopes |
| n25 conclusion | [`TwentyFiveProvider.upper`](../BEMap/Assembly.lean) | Complete same-witness regional methods imply C25<=C_E |
| Additional predecessor bridge | [`n25_allowance`](../BEMap/Finite.lean), [`same_law_n25_allowance`](../BEMap/Interfaces.lean) | Sharp24 OR auxiliary24 gives q25<=5/16 for the same law |
| Tail inputs | [`TailMethodProviders`](../BEMap/TailAssembly.lean) | Typed 83-panel comparison, auxiliary resource barriers and source smoothing construct `.contracts` |
| Smoothing | [`smoothing_first_failure`](../BEMap/TailAssembly.lean) | Exact source smoothing and explicit scalar brackets give the0.29 first-failure consequence |
| Base49 | [`tail_base49`](../BEMap/Tail.lean) | Three exact backward losses contradict the strong 46 cap |
| Infinite tail | [`tail_composition`](../BEMap/Tail.lean) | First-failure induction covers all n>=49 |
| Every index | [`all_indices_from_typed_providers`](../BEMap/Assembly.lean) | Constructed finite1--48 and independent49+ imply the upper bound |
| Lower approximation | [`LowerApproximation`](../BEMap/Global.lean) | Separate Bernoulli/lattice analytic premise |
| Sharp constant | [`sharp_from_typed_providers`](../BEMap/Assembly.lean) | Conditional equality of the concrete global supremum with C_E |

The source-linked JSON includes the exact line of every declaration anchor.
The finite and tail theorem records provide the detailed inputs behind grouped
boxes; their fields are not claims of completed numerical proofs.

## The n25 predecessor alternative

```mermaid
flowchart LR
  S["Sharp C24 <= C_E"]:::open --> OR{"Either license"}
  A["Complete auxiliary24: C24 < C_E + 1/80"]:::open --> OR
  OR --> Q["n25_allowance: q25 <= 5/16"]:::checked
  Q --> P["same_law_n25_allowance"]:::checked
  P -. "available to matching lower-rho exclusions" .-> R["Regional exclusion proofs"]:::open
  classDef checked fill:#effbf5,stroke:#0b805d,color:#173e30
  classDef open fill:#fff8e7,stroke:#b77721,color:#694314
```

The sharp route fits the sufficient finite induction. The auxiliary route is
an alternative, not a requirement to prove both. Either license bounds the
same law at 24; it never turns the index25 contact into an index24 contact.

## The tail's independence

`tail_composition` has `TailContracts C c` as its only proof-record input.
The entire finite 1--48 upper bound is not an argument. Its base 49 uses the
local exclusion at 49,48,47 and auxiliary bounds near46. For the later index50
step, the second deleted-index cap uses the auxiliary bound at 48. The
smoothing premise supplies the scaled0.29 estimate at any later first failure.

The canonical public route now constructs those scalar inputs through
`TailMethodProviders.contracts`. Its local comparison covers every actual
n>=47, all83 panels and positive/zero noise separately. The auxiliary
certificates are finite resource barriers ending in negative D, with A46's
paired signed corrections kept distinct. The support-free smoothing result
and pure-index brackets produce the scalar0.29 step. See
[uniform local comparison](contracts/UNIFORM-TAIL.md) and
[tail assembly](contracts/TAIL-ASSEMBLY.md).

This distinction is visible in the SVG: there is no arrow from the finite
composition to the tail composition. Both branches meet at the all-indices
theorem.

## Reproduce and inspect

```
python tools/render_proof_map.py
```

This standard-library script verifies the complete recorded Lean source set,
source hashes, declaration anchors, and acyclicity of the displayed grouped
edges. It writes
the SVG, Mermaid source and JSON map. These structural checks supplement the
actual Lean check; they do not prove a new analytic statement.

The check results and logical axiom lists are in
[`check-All.json`](../check-All.json) and [`check-All.log`](../check-All.log).
`Audit.lean` prints theorem signatures as well as axiom lists. Standard logical
axioms and undischarged theorem arguments are different things; inspect both.
