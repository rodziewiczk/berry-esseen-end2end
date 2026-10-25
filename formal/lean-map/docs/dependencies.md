# Conditional dependency map

Solid dependencies below describe the mathematical contracts in this package.
Exact analytic leaf statements are accepted parameters at this milestone;
numerical semantic evidence remains to be supplied by its producers/checkers.
No numerical notebook was executed for this skeleton. The detailed interfaces
are in [the five-part specification](contracts/README.md).

```mermaid
flowchart TD
  C[Exact probability model and explicit constant comparisons]
  N1[All-law n1]
  N2[All-law quantitative n2]
  N3[All-law quantitative n3]
  N4[Unrestricted n4 localization and physical exclusion]
  N5[Complete n5: low cover, corner, Fourier, tail]
  F[Literal finite exclusions n6 to 48 except 25]
  S24[Sharp24]
  A24[Complete auxiliary24 acquisition]
  OR24{Either predecessor license}
  Q25[Same-law q25 at most5/16]
  R25[All 20 n25 domains and matching exclusions]
  N25[All-law n25]
  FIN[Finite composition n1 to 48]
  AUX[Independent auxiliary ceilings45 to 50 and strong 46]
  LOC[Uniform local exclusion n at least 47]
  SM[Smoothing first-failure consequence]
  B49[Three backward losses: base 49]
  TAIL[Strong induction: all n at least 49]
  U[All positive indices: upper bound]
  LOW[Separate Bernoulli lattice lower approximation]
  EQ[Global optimal constant equals C_E]
  N3 --> N4 --> N5
  S24 --> OR24
  A24 --> OR24
  OR24 --> Q25 --> R25 --> N25
  N1 --> FIN
  N2 --> FIN
  N3 --> FIN
  N4 --> FIN
  N5 --> FIN
  F --> FIN
  N25 --> FIN
  AUX --> B49
  LOC --> B49
  B49 --> TAIL
  AUX --> TAIL
  LOC --> TAIL
  SM --> TAIL
  FIN --> U
  TAIL --> U
  C --> U
  U --> EQ
  LOW --> EQ
```

`FiniteContracts.ordinary` also admits a sufficient sequential proof using
earlier sharp bounds. An independently licensed actual-index proof may ignore
that argument. There is no FIN -> TAIL arrow. The displayed sharp24 route is
compatible with the sequential finite proof; the auxiliary24 route is an
alternative and must include its full acquisition proof.

Checked glue:

| Lean theorem | Checked implication |
|---|---|
| `finite_composition` | The finite contracts cover every integer1 through 48 |
| `n25_allowance` | Either predecessor license gives the rational allowance |
| `same_law_n25_allowance` | The allowance applies to the same law at 24 |
| `ClosedChain.cover`, `n25_cover` | Closed rational cuts leave no n25 gap, assuming the stated envelopes |
| `n25_exclude_by_cover`, `n25_upper_of_regions` | Complete same-witness regional exclusions imply the n25 upper bound |
| `ContactPipeline.score_bound` | All typed pipeline transitions at the same n and contact give the weak score cap |
| `CountTree.cover` | Both children, closed seams and every original count root remain covered |
| `n5_cover`, `floor31_cover` | The listed closed rational domains cover their full stated ranges |
| `Root4Provider.upper` | A chosen localized owner with the weak ROOT4 cap excludes strict global failure |
| `tail_base49` | Auxiliary and local contracts imply the base 49 bound |
| `tail_composition` | Base49 and first-failure contracts cover the infinite tail |
| `UniformTail.UniformLocalProvider.reject` | Complete 83-panel numerical meaning and analytic probability kernels exclude positive noise; the zero-noise Bernoulli argument is separate |
| `barrier_resource_reject` | Finite auxiliary resource passes preserve the same owner and end in a strict negative bound for nonnegative D |
| `TailMethodProviders.contracts` | Typed local comparison, auxiliary barriers and smoothing construct the independent scalar tail inputs |
| `all_indices_upper` | Finite and independent tail bounds cover all n >= 1 |
| `sharp_global_constant` | Upper bound and separate lower approximation give the exact supremum |
| `EndToEndProviders.finite` | Typed small-index, ROOT4, n5, ordinary and n25 methods construct the finite contracts |
| `all_indices_from_typed_providers`, `sharp_from_typed_providers` | Those constructed finite contracts and independent tail give the final statements |

The [detailed interface graph](../assets/interface-map.svg) expands the state,
transition, cover, certificate and assembly layers. Their definitions fix the
mathematics consumed by a future implementation; production LOW/HIGH/ROOT4/COUNT
evaluators, resource search and byte decoding are subsequent work.
