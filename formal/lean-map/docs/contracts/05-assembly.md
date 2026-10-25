# 5. Actual conditional assembly of the final proof

`BEMap/Assembly.lean` constructs the earlier coarse `FiniteContracts` from
source-specific analytic/numerical provider interfaces. It then invokes the
checked finite and independent-tail compositions. It does not take the
desired all-index theorem as one opaque input.

This is a precise conditional mathematical program. Its analytic theorems may
be assumed correct as explicit project inputs; numerical certificate meaning
and applicability still have to match their exact hypotheses. The assembly
does not claim that all providers have already been implemented or populated
by accepted arithmetic evidence.

## 5.1 Provider dependency table

| Provider | Exact input/output role |
|---|---|
| `ConstantComparisons` | The quantitative n2/n3/n4 constants compare with C_E |
| One-summand input | C1<=0.3704; the small comparison to4097/10000 and then C_E is handled in assembly |
| `SmallPolynomialProvider .tensorTwo` | Extraction at2sqrt(2)/7, acquired support[-6,6], finite rho<=2 polynomial portfolio and separate large-rho structural complement |
| `SmallPolynomialProvider .independenceNullThree` | Extraction at59sqrt(3)/250, acquired support[-6,6], finite rho<=15/8 null-polynomial portfolio and separate structural complement |
| `Root4Provider` | Strong n3 result -> one correctly localized canonical ROOT4 owner; weak certificate bound on that class -> C4<=4097/10000 |
| `FiveProvider` | Strong n4 input -> exact n5 envelopes and one method-specific result for every applicable closed region |
| `TwentyFiveProvider` | Earlier sharp inputs or an independently acquired alternative predecessor license; signed-beta envelopes; all20 scoped regional methods |
| Ordinary actual-index providers | Every literal n from6 to48 except25; each may consume earlier sharp bounds or use its own independently acquired route |
| `TailMethodProviders` | Typed uniform local-comparison data, auxiliary resource barriers and source smoothing; `.contracts` constructs the independent scalar tail input |
| `LowerApproximation` | Separate Bernoulli/lattice approximation to the global supremum |

For n3 the physical owner support(-6,6) lies inside the numerical majorant
cube[-7,7]^3. The number7 in that certificate is not an acquired support
radius for a different law. n2's tensor majorants use[-6,6]^2. The finite rho
domains differ:2 for n2 and15/8 for n3. Their large-rho structural inputs are
separate, rather than silently incorporated into a field called polynomial.

The canonical small-index constructors are
`SmallPolynomialProvider.tensorFromCertificate` and `.nullFromCertificate`.
They consume a concrete coefficient payload, its exact numerical meaning,
accepted `SmallCertificateImplications`, extraction/localization and a
separate large-rho result. The path is therefore

```
coefficient payload -> exact numerical certificate meaning
 -> accepted bounded-class analytic implication
 -> small-rho branch + separate large-rho branch -> quantitative bound.
```

The coefficient conventions differ: n2 sums15 symmetric tensor terms with
feature x²; n3 averages distinct permutations of59 triples and uses the
centered-null feature x²-1. The meaning types fix those conventions before
analytic consumption. A file label or array length is not a basis conversion.

## 5.2 Why the n4 target needs its own contact type

The assembly passes `FixedIndexBound 3 bound3` to `Root4Provider.upper`.
That provider localizes from `bound4<C4`, where bound4=4097/10000. Its contact
floor is bound4. Extraction at C_E would leave the entire possible interval
`4097/10000<C4<C_E` untreated.

The returned ROOT4 certificate may establish only `C4<=bound4`. The strict
global failure is preserved via `w.optimal` and contradicted by that weak cap.
There is no need to assert a uniform strict gap belowbound4.

## 5.3 n5: a genuine disjoint method interface over an overlapping cover

The geometric regions are closed and overlap on seams. The evidence type is
indexed by the selected `Region5`:

* A gapped/resource low row returns `SupportedCountEvidence` and has a proof
  that its row is not the corner.
* The corner returns `GapFreeEvidence`, with no support or central-gap input.
* A Fourier band returns complete four-term `PrawitzScoreEvidence` at that
  band's prescribed support radius and its source-level4097/10000 cap.
* The tail returns the n5 third structural estimate; the checked scalar tail
  comparison gives819/2000<=4097/10000<=C_E.

`n5_cover` chooses a region for the same actual rho and signed beta.
`FiveProvider.upper` retains a strict global violation while consuming that
region's weak score cap. Thus a closed cover does not accidentally identify
the gap-free and gapped methods or discard their shared endpoint.

## 5.4 n25: covers and predecessor alternatives

`TwentyFiveProvider` obtains a fixed-index extraction contract, the two
signed-beta envelopes, a predecessor license and a method for every eligible
`Region25`. `n25_cover` contains six lower-rho, seven middle-beta, six
high-beta regions and the inclusive universal rho tail.

The predecessor input is a sum type, not a conjunction:

```
Sharp24: C24<=C_E
    OR
Auxiliary24: C24<C_E+1/80.
```

`same_law_n25_allowance` converts either alternative to
`25 max(R24(P)-C_E,0)<=5/16` for the very same law P. The regional provider
receives this actual-law bound explicitly. The earlier sharp route is
sufficient for the mathematical induction. A numerical implementation using
the auxiliary route still needs its complete acquisition evidence; the OR
does not certify that evidence automatically.

Each regional evidence object concerns one contact. Selecting COUNT in one
region does not require a global COUNT provider on the corner or on every
other region. Source-specific mixed E/chord/AB steps are separate acquisition
and contradiction roles; see `MIXED.md`.


## 5.4a Numerical COUNT, source scope and the AB24 route

The fixed meaning of a numerical payload is in `BEMap/GeneralCount.lean`.
It quantifies every standardized law X and raw H realizing the frozen
context, without C_m optimality or attainment. Its conclusion concerns the
signed positive-orientation point score, not the absolute Kolmogorov supremum.

The ordinary path is

```
frozen context + finite payload + checker soundness + accepted computation
 -> CountCertificateMeaning for all hypothetical eligible laws
 -> GeneralCountRealization of the actual contact's law/raw H
 -> point-score bound
 -> explicit raw/normalized contact equality
 -> R_n(P) bound.
```

For AB the same law at24 uses a different path:

```
original n25 law resources
 -> transferred24 context: same X, new lambda/joint prices and full phase
 -> GeneralCountRealization (no24 contact)
 -> quantitative native24 bound U
 -> ABGeneralCountPort.toWindowPacket
 -> complete window + negative exterior tail + positive exterior tail
 -> closed-halfline upper
 -> constant predecessor allowance on a whole support ray
 -> licensed n25 support/resource update, then COUNT or contradiction.
```

`QuantitativeCountPayload` and `CountBoundCertificateMeaning` certify a valid
returned U independently of reaching a search early-exit target. U may lie
above that early target. Target-achievement uses the separate
`CountCertificateMeaning`/`BoundRelation.Transfers` condition. The early target
is never promoted to the returned numerical maximum.

The AB24 context's H interval is exactly one requested closed raw half-line
intersected with[-47/4,47/4]. A union uses separate scopes. An irrelevant
leaf proves no realization in that scope, not global impossibility of the
law. `ABEmptyCentralPort` handles an actually empty clip without an invalid
nonempty interval. Both exterior tails are still required by the half-line
aggregation. Closed cut/window seams remain active.

The original COUNT axis is raw a0=p-hA. The total dY=a0+a1, marginal lambda
cap and joint noise intercept remain separate. General native scope binds
all of: actual asymmetric support, conditional outer caps, rho/beta/gamma/
mean/fourth/fifth intervals, actual-coordinate realization, joint plane,
affine D lower price, coherent signed D quadratic upper and separately
licensed native unweighted D cap. A tuple of scalar caps alone cannot
instantiate this interface.

## 5.5 Every literal finite index

`EndToEndProviders.finite` constructs the seven fields of `FiniteContracts`:

```
one, two, three,
four(strong quantitative n3),
five(strong quantitative n4),
ordinary(actual n, earlier sharp bounds),
twentyFive(earlier sharp bounds).
```

The `ordinary` quantifier covers every integer6<=n<=48 with n!=25. The
already checked strong induction covers the rest exactly. A floor31 resource
transcript is not a proof at32,33,34 until the actual-index transfer contracts
are satisfied. Weighted D, support, binomial probabilities and phase
normalization use the actual index specified in those contracts.

The interface permits an independently licensed actual-index proof to ignore
the earlier-sharp argument. It does not force the selected notebook execution
graph to be one linear chain or import a historical global composer as a
finite theorem.

## 5.6 The independent tail and lower bound

The tail's public provider is `TailMethodProviders` from
[`TailAssembly.lean`](../../BEMap/TailAssembly.lean). Its `.contracts` constructs
`TailContracts optimalConstant C_E` from the detailed
[uniform local comparison](UNIFORM-TAIL.md), five auxiliary
[resource-barrier families](TAIL-ASSEMBLY.md) and source smoothing. The full
finite1--48 result is not an argument. Its base49 follows from three backward
losses at49,48,47 and the stronger46 cap. Later failures use the sharp
preceding index, zero drop and the0.29 smoothing consequence. At50, the
second deleted index48 uses its independent auxiliary ceiling.

`EndToEndProviders.tail` requires this typed provider. Both canonical final
theorems consume `.tail.contracts`; the new adapter is part of the actual
assembly rather than an optional unused constructor. The older scalar
`all_indices_upper` helper remains available with its coarse `TailContracts`
argument, with that boundary explicitly visible in its signature.

`LowerApproximation` remains separate: for every b<C_E there exists n>=1
with b<C_n. It comes from the fixed-law lattice expansion and subsequent
Bernoulli optimization/continuity. It does not assert attainment at a fixed
finite n, and no upper-bound provider substitutes for it.

## 5.7 Final exact statements

The checked assembly exports

```
all_indices_from_typed_providers:
  EndToEndProviders -> forall n>=1, C_n<=C_E,

sharp_from_typed_providers:
  EndToEndProviders -> LowerApproximation -> globalConstant=C_E.
```

`globalConstant` is the concrete supremum over positive-index optimal
constants from the probability-law model. Nonemptiness and boundedness of
the supremum sets are established before the conditional-supremum rules are
used. `BEMap.universal_iid_inequality` yields the actual law-level conclusion
`sqrt(n)Delta_n(P)<=C_E rho(P)` from the assembled upper bound.

`EndToEndProviders` contains only upper-bound inputs. The lower approximation
is a separate argument of the sharpness theorem, so constructing the upper
bound never requires supplying that independent lower-bound result.

## 5.8 What remains trusted, specified and implemented

Three statuses must stay separate:

1. **Specified analytic input:** an exact source-bound theorem statement is
   accepted as a mathematical premise at this stage. Its presence is not a
   specification gap or an instruction to prove all analysis during coding.
2. **Checked logical composition:** Lean checks that the specified inputs
   compose with their actual indices, laws, thresholds, normalizations and
   inequality relations.
3. **Implemented numerical evidence:** an actual parser/checker and data
   establish the fixed certificate meaning under the frozen context. Historical
   PASS strings or source labels alone do not provide this status.

A missing theorem statement, omitted applicability gate or unspecified source
recipe is a specification defect and must be resolved before handing that
component to an implementer. A fully stated trusted analytic theorem is an
explicit mathematical trust input. A precise but not-yet-coded checker is an
implementation task. These categories must not be merged into one green flag.
