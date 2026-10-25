# Plan at the mathematical-interface checkpoint

Checkpoint: 25 October 2026, version 0.2. The agreed order is:

```
precise mathematical contracts -> solid conditional Lean skeleton
                              -> execution design -> implementation
```

Correctness of the precisely stated analytic results is an explicit assumption
at this milestone. Full formalization of their proofs is not a prerequisite
for designing the implementation. Exact theorem scope, all side conditions,
certificate meaning and actual conditional assembly are prerequisites.

## Current handoff

The [five-part specification](contracts/README.md) defines actual-law states,
transition contracts, complete covers, certificate semantics and final
composition. Dedicated contracts describe the two small-index polynomial
families, physical ROOT4, physical LOW/HIGH, four-term Prawitz, ordinary COUNT
and the mixed25/24 routes. The [adversarial audit](contracts/AUDIT.md) records
source comparisons and dispositions of the independent review.

The independent tail also has explicit contracts: the
[83-panel uniform comparison](contracts/UNIFORM-TAIL.md) and
[five auxiliary resource-barrier families](contracts/TAIL-ASSEMBLY.md).
Their typed provider constructs the scalar tail premises used by the public
final theorem. Uniform numerical goals are not relabelled as pure analysis.

The Lean layer now proves structural coverage and algebra and constructs the
final finite contracts from typed method providers. It preserves same-law
ownership, actual-index normalization, signed data, coherent joint budgets,
all roots and exterior tails. It keeps analytic assumptions visible in
signatures. [InterfaceChecks](../BEMap/InterfaceChecks.lean) includes negative
controls against common invalid substitutions.

## 1. Freeze the semantic handoff

Read each source-alignment row in the
[question register](contracts/implementation-questions.json). A mathematical
specification BLOCK must be resolved before its corresponding implementation
is designed. A named, exactly sourced analytic parameter is an accepted
premise under the agreed scope, rather than a request to port its whole proof.

Freeze the following for each implemented method:

* The actual law/index, owner scope, thresholds, coordinate meanings and units.
* Every analytic gate and the weak/strict conclusion it licenses.
* Complete root, interval, exterior and zero-case coverage.
* Frozen rational task data, payload meaning and the theorem supplied by a pass.
* Admission manifests versus the subset of acquired references used in a proof;
  lookup uses one enclosing scope and only earlier licenses.

Algorithm choices, search heuristics, cuts and parallel scheduling may remain
implementation choices. A change to mathematical meaning requires an explicit
contract revision and renewed source comparison.

## 2. Validate one small certificate path

Use a small real certificate to exercise candidate bytes -> typed payload ->
complete coverage -> semantic checker conclusion. The rational Farkas checker
already has a proved local soundness theorem; its rows still need the declared
binding to the actual necessary inequalities. The small inequality example
suggested by the independent review is suitable for this boundary exercise.

For this pilot, specify canonical rational encoding, malformed/unresolved
outcomes and outward rounding against the existing mathematical contracts.
Do not treat hash agreement or replay of an external implementation as a
replacement for the advertised semantic implication. A production checker may
initially have an explicitly trusted soundness implementation, but that trust
must be named and its precise statement must match the contract.

Acceptance: the small path supplies the exact typed conclusion required by a
consumer, with no new mathematical interpretation invented in the decoder.

## 3. Design the execution system against the contracts

Choose task/certificate serialization, a source-bound cache key, storage,
resumability and scheduling. Derive supported method tags from the completed
rule catalogue; unsupported tags return unresolved rather than PASS.
Document the chosen trust boundary for analytic results, arithmetic evaluation,
decoding, external replay and Lean assembly separately.

Use one ordinary COUNT case and one mixed24/25 case to check that the design
can represent a quantitative returned bound, all original count roots, exact
phase ownership, complete tails and finite reference dependencies.

## 4. Implement a vertical slice, then scale

Implement one complete producer/checker/assembly slice before widening to all
families. The numerical engine may search aggressively; acceptance must prove
the frozen statement. Then implement the remaining declared arithmetic rules,
resource acquisitions, certificate families and reference admission checks.

Only after this path is reproducible should heavy compute be distributed.
Cloud resources accelerate candidate production and exact checking; they do
not resolve a missing mathematical gate or an ambiguous acceptance condition.

The eventual CLI should run the frozen project, resume completed tasks and
report separately: checked structural Lean results, accepted analytic premises,
validated numerical evidence, and unresolved tasks. No production runner or
cloud CLI is implemented at this checkpoint.

## Reading the green graph

A green box is a checked implication from its stated inputs. The amber boxes
include accepted analytic statements and numerical evidence still to supply.
Neither color asserts that the original analytic mathematics has been proved
again inside Lean. The [source-bound compiler report](../check-All.json) and
[axiom/signature log](../check-All.log) document the actual local check.
