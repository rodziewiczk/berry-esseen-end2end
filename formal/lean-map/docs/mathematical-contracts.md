# Mathematical contracts for the iid Berry--Esseen proof

Version 0.1, 25 October 2026. **This is a conditional specification and a checked
logical skeleton, not a completed formal proof of the numerical theorem.**
The scope is mathematical contracts followed by Lean composition. Execution
architecture, cloud scheduling, certificate serialization and a production CLI
are outside this stage.

## 1. Exact final statement and semantic model

Let P be any probability law on the real line with EX = 0, EX² = 1 and
rho(P) = E|X|³ < infinity. For iid variables with common law P, set

```
S_n = X_1 + ... + X_n,                         n an integer >= 1,
Delta_n(P) = sup_y |P(S_n / sqrt(n) <= y) - Phi(y)|,
R_n(P) = sqrt(n) Delta_n(P) / rho(P),
C_n = sup_P R_n(P),
C_E = (3 + sqrt(10)) / (6 sqrt(2 pi)),
C_* = sup_{n >= 1} C_n.
```

The upper-bound target is `C_n <= C_E` for **every** positive integer n and
**every** such law P. Equivalently,
`sqrt(n) Delta_n(P) <= C_E rho(P)`. The final sharpness target is `C_* = C_E`.
It additionally requires a separate lower approximation: for every `b < C_E`
there is a positive n with `b < C_n`. No assertion of equality or attainment
at a particular finite n is needed for this lower bound.

`StandardizedLaw` and `optimalConstant` in Lean have this concrete meaning:
normalized sums are constructed by convolution of probability measures; the
CDF and the Gaussian are mathlib definitions. The original, already checked
foundational modules are reused with their namespace/import paths changed.
They prove rho >= 1, positivity of rho, CDF bounds, and boundedness and
nonemptiness of the sets used for the conditional suprema. Thus the supremum
manipulations in the final theorem carry their required hypotheses.

The index zero occurs only in total auxiliary definitions. Every final theorem
requires n >= 1. A threshold y for a normalized sum corresponds to
H = sqrt(n)y for the unnormalized sum. All discrepancy events here use `<=`.

Lean: `BEMap/Foundations/*`, `BEMap.lean` (`all_indices_upper`,
`universal_iid_inequality`, `sharp_global_constant`).

## 2. Variables and invariants that must not be identified

| Symbol | Meaning and required convention |
|---|---|
| rho | E|X|³, at least one |
| gamma | EX³, a signed third moment |
| beta | E[X|X|], a signed second moment; not gamma |
| p | P(X > 0); any atom at zero is in the nonpositive class |
| C | The score of the particular contact, not automatically a global upper cap |
| q_n(P,c) | n max(R_(n-1)(P) - c, 0), for the same law P |
| R | An almost-sure support radius, separately proved for the current contact |
| D | The unweighted physical defect, defined below |
| nD | A weighted defect; not interchangeable with D |
| lambda | n E U² in the normalized binary decomposition; not E U² |

Reflection, if needed to obtain a positive discrepancy, replaces the whole law
by its reflection. Its signed moments, probabilities, threshold and subsequent
resource state must all refer to that reflected law. A sign change in beta
alone is not a permitted operation.

## 3. Extraction of an unrestricted attained contact

For fixed n >= 2, the contact route must justify the following analytic
implication, not merely optimize within a convenient family of measures:

```
C_n >= C_E
    -> an unrestricted maximizing law P and a threshold H
    -> a positive, attained CLOSED-CDF discrepancy at H
    -> the first-variation contact majorant for that same law and threshold.
```

In particular P is not assumed to have two or three atoms. Equality at C_E is
included in the contact domains. The Lean `ContactExtraction` parameter states
the attainment and orientation part explicitly; it is not proved in this
package. `ContraryContact n` stores the actual law, threshold, score equality
and positive closed discrepancy. It does not silently provide the contact
polynomial or compact support.

More precisely, put s = sqrt(n), z = H/s, F = P(S_n <= H),
phi = the standard Gaussian density at z, and C = s(F-Phi(z))/rho > 0.
The analytic first-variation obligation is

```
h(y) = P(S_(n-1) <= H-y) <= Q_H(y) for all real y,
h(y) = Q_H(y) on supp(P),
n Q_H(y) = n F + (H phi + C rho)/(2s)
           - (s phi + 3 C beta/s)y
           - (H phi + 3 C rho)y²/(2s) + (C/s)|y|³.
```

Since C > 0 and 0 <= h <= 1, this implies qualitative compact support.
**Only afterwards** may fourth and fifth moments be introduced. A subsequent
quantitative radius is another implication with its own assumptions.

Lean: `BEMap/Interfaces.lean`. `ContactPipeline` is an abstract interface for
these implications. Its predicates still need their detailed analytic
instantiations; it is not a certificate checker.

## 4. One conserved budget and the resource pipeline

For the oriented, compactly supported law define
`tau(t) = E[X 1_{X >= t}]`, and let (a,b) range over the bounded complementary
intervals of the closed support. Write tau_(a,b) for the constant value of tau
inside that gap and let nu be the law of H-S_(n-1). The physical quantities are

```
J   = sum tau_(a,b) (b-a)²,
J1  = sum tau_(a,b) integral_a^b (t-a)t dt,
J2  = sum tau_(a,b) integral_a^b (t-a)t|t| dt,
L   = sum tau_(a,b) integral_[a,b) (t-a) dnu(t),
D   = (3+sqrt(10))rho - gamma - 3J >= 0.
```

The half-open interval in L is part of the definition. Absolute convergence
and D >= 0 are analytic obligations. The two expressions for contact slack
and compensated full inversion must give **one conserved budget for this
contact**. Adding two deductions which spend the same budget is invalid.

The ordinary exclusion route is

```
contact -> qualitative compact support -> quantitative support
        -> HIGH -> own-index cap -> INITIAL
        -> a finite sequence of resource intersections -> COUNT contradiction.
```

Each resource update must prove containment of the same actual law in the
new state. Exported floor bounds require the entire stated finite transcript.
No convergence or unproved fixed-point assumption is available. The bounds
are simultaneous: common first moments, a single defect measure, signed
moments and phase information cannot be chosen independently at each use.

A sharp predecessor gives q_n(P,C_E)=0, because R_(n-1)(P) <= C_(n-1).
It supplies neither a support radius nor an own-index cap nor a resource
transcript for the current n.

Lean checks that every stage in `ContactPipeline.reject` concerns the same
`ContraryContact n`, and that all declared transitions are consumed. The
conserved identity, inequalities and their numerical verification remain
explicitly unimplemented analytic obligations at this stage.

## 5. Exact coverage of the finite indices

| Indices | Required mathematical result / incoming information |
|---|---|
| 1 | All-law bound C_1 <= 0.3704 and comparison with C_E |
| 2 | All-law C_2 <= 2 sqrt(2)/7; unrestricted localization and rational tensor majorants |
| 3 | All-law C_3 <= 59 sqrt(3)/250; null-polynomial majorants |
| 4 | The **quantitative** C_3 bound, unrestricted localization, a complete physical ROOT4 exclusion; output C_4 <= 4097/10000 |
| 5 | Quantitative C_4 input; complete low-domain COUNT/gap-free cover, Fourier complement and universal rho tail |
| 6--9 | Every actual n separately; selected execution may use the independent auxiliary C_5 < 0.429 |
| 10--14 | Every actual n separately; selected execution may use independent auxiliary/supported n=9 licenses |
| 15--19 | Actual-index exclusions and their preceding n=14 license |
| 20--24 | Actual-index exclusions and their preceding n=19 license |
| 25 | All 20 domains in section 6; a licensed predecessor allowance and the appropriate ordinary or mixed exclusion for each domain |
| 26--30 | Full floor25 transcripts plus actual-index support, probabilities and transfer rules |
| 31--34 | Eight floor31 bands and correctly rescaled actual-index transfers |
| 35--39 | Separate retained signed/phase contracts |
| 40--42 | Complete literal exclusions; independent scalar/retained routes are available |
| 43--48 | Complete literal exclusions; independent barrier/retained routes are available |

The ROOT4 reference Q3 is not a restriction of P to three atoms. One common
defect measure must serve all its frequency evaluations. The complete stated
root, threshold, noise-bin and orientation cover is required.

For n=5 the low-domain inventory consists of 12 gapped rows plus one gap-free
corner. The corner is separate and support-free. The remaining rho range is
covered by six supported Fourier bands, with endpoints
`6/5, 5/4, 7/5, 3/2, 8/5, 17/10, 7361/4000`, followed by an inclusive universal
tail. A result on the 12 gapped rows alone is not an all-law n=5 result.

Here the exact low-domain list uses
`b2=84729828287999/250000000000000` and
`b3=35139006743001/100000000000000`. The scalar proof must first establish
that these enclose the beta moment envelopes at 237/200 and 6/5 respectively.
“Full” below means the necessary signed-beta range given by the moment
inequality, not a restriction to beta>=0.

| Row | Closed rho interval | Closed beta interval | Method |
|---|---|---|---|
| B0 | [1,11/10] | Full | Resources/COUNT |
| BN | [11/10,23/20] | Full | Resources/COUNT |
| B2 S0 | [23/20,467/400] | [-b2,1/5] | Resources/COUNT |
| B2 S1 | [23/20,467/400] | [1/5,b2] | Resources/COUNT |
| B2 S2 | [467/400,237/200] | [-b2,1/5] | Resources/COUNT |
| B2 S3 | [467/400,237/200] | [1/5,b2] | Resources/COUNT |
| B3 S0 | [237/200,477/400] | [-b3,1/5] | Resources/COUNT |
| B3 T0 | [237/200,477/400] | [1/5,3/10] | Resources/COUNT |
| B3 T1 | [237/200,477/400] | [3/10,b3] | Resources/COUNT |
| B3 S2 | [477/400,6/5] | [-b3,1/5] | Resources/COUNT |
| B3 T2 | [477/400,6/5] | [1/5,3/10] | Resources/COUNT |
| B3 lower | [477/400,6/5] | [3/10,17/50] | Resources/COUNT |
| B3 corner | [477/400,6/5] | [17/50,b3] | Separate gap-free exclusion |

Each gapped row still needs a complete p cover, its resource acquisition and
all six original n=5 count roots. The acquired Fourier radii, in the order of
the six bands above, are `13/5,117/40,25/8,133/40,7/2,15/4`. The universal
tail at rho>=7361/4000 has the stated 0.4095 target. The six support
acquisitions and this tail bound remain separate mathematical obligations.

The floor31 rho endpoints are
`1, 11/10, 6/5, 13/10, 7/5, 3/2, 33/20, 7/4, 7361/4000`.
For actual m=32,33,34, the imported defect bound has the stated mD <= 31d
normalization, while support, binomial probabilities and phase scaling use m.
A proof at index31 alone does not prove these three cases.

`FiniteContracts` deliberately exposes the stronger C_3 -> C_4 and
C_4 -> C_5 interfaces. Its remaining `ordinary` steps accept earlier sharp
bounds as a sufficient mathematical route. They may ignore those bounds when
using an independent acquired license. This interface is **not** a claim that
the selected notebook execution graph is a single linear chain.
`finite_composition` proves by strong induction that these contracts suffice
for every literal index 1 through 48. The finite numerical contracts themselves
remain premises. The detailed n=5 and floor31 domain covers are inventoried
here but are not formalized in this first skeleton.

## 6. The n=25 cover: exact cuts, signed beta and predecessor alternatives

All intervals below are closed. Their overlap on seams is intentional.

| Family | rho domain | Subdivision | Count |
|---|---|---|---:|
| Lower | 1 to 33/20 | rho cuts: 1,11/10,6/5,13/10,7/5,3/2,33/20; beta unrestricted | 6 |
| Middle | [33/20,7/4] | beta cuts: -13/20,0,4/25,321/1000,2/5,12/25,14/25,307827/500000 | 7 |
| High | [7/4,459061/250000] | beta cuts: -640471/1000000,0,321/1000,2/5,12/25,14/25,640471/1000000 | 6 |
| Tail | rho >=459061/250000 | Universal rho bound, including its left endpoint | 1 |

The signed-beta envelope follows analytically from
`rho >= (1+beta²)/sqrt(1-beta²)`, with |beta| < 1. The two endpoint
envelopes are explicit assumptions of `n25_cover` and `n25_upper_of_regions`;
the general moment inequality is not asserted as a proved Lean theorem here.
Under these assumptions, Lean proves that all feasible (rho,beta) belong to
at least one of exactly these 20 listed cells. All cuts are rational.

For the lower six regions the allowance q_25 <= 5/16 has two sufficient inputs:

```
C_24 <= C_E                         (sharp route), OR
C_24 < C_E + 1/80                   (complete auxiliary24 route).
```

Lean proves the implication from either alternative to the allowance, including
its same-law version. This does not assert that both routes are implemented by
the currently selected numerical notebooks. Middle/high own-caps can instead
be obtained from the universal T(rho) at the lower rho endpoint, with the
corresponding nonzero allowance.

The universal bound used in these contracts is
`T(rho) = min(0.469, 0.3322(1+0.429/rho), 0.3031(1+0.646/rho))`.
Its applicability, monotonic use and comparison with C_E require analytic and
exact/interval proofs; this package does not assert their numerical completion.

The lower-region mixed B5 exclusions include the p24 E family and the p25
ABCDF family. These are distinct from ordinary COUNT. AB transfers the **same
law** to index24: for example lambda_24=(24/25)lambda_25. Every required
index24 phase must be covered. The transferred law need not maximize C_24,
and the index25 contact equation may not be borrowed as an index24 contact.

Lean: `BEMap/Cover25.lean`, `same_law_n25_allowance`, `n25_upper_of_regions`.

## 7. COUNT and numerical-certificate meaning

This is a mathematical acceptance contract, not a serialization format.
For a particular law and admissible cell, an accepted exclusion must establish
an actual contradiction under all its stated hypotheses. Required invariants:

1. With I=1_{X>0}, use the stated hX=I-p+U representation and E(U|I)=0.
   lambda=n E U² uses the actual n. K=sum I has its actual binomial law.
2. Every original root k=0,...,n is covered, including k=0,n. Every split
   retains both children; all closed seams, zero variance, zero noise and
   equality cases remain covered. Threshold endpoints and infinite normal
   tails require their separate proofs.
3. Outgoing count probabilities use the strict event P(W_k > u); incoming
   events use the closed convention prescribed by the bound. An atom on a
   threshold cannot be discarded by changing this convention.
4. Every LOW triple and HIGH sum must be a coherent bound for the same state.
   One may select the best of complete valid strategies. One may not take
   coordinatewise minima of unrelated LOW triples or mix signed planes.
5. A failed applicability guard produces an unresolved cell, not an empty
   cell. Dividing by an unproved positive quantity is invalid. A zero
   denominator requires a separate valid branch. An own-mass lower bound
   used as nonnegative must actually be nonnegative.
6. Cached mathematical evidence is usable only for the identical semantic
   assumptions, index, law orientation and normalization. Resource exports
   are valid only after the entire required preceding finite transcript.

No numerical certificate parser, interval arithmetic soundness theorem or
checker implementation is included. The `reject` and pipeline proof fields
must eventually be filled by those results; no Boolean `accepted=true` is
trusted in the current Lean development.

## 8. Independent n>=49 tail: the exact conditional scalar proof

Set `a_n=C_n-C_E` and `delta_n=n max(C_(n-1)-C_n,0)`.
`TailContracts C C_E` has the following explicit inputs:

* C_E <=409733/1000000 (a deliberately coarse rational upper bracket).
* a_n <(7/10)/n for 45<=n<=50.
* a_46 <(54/100)/46.
* For n>=50, C_(n-1)<=C_E implies n a_n <29/100.
* For n>=47, the conjunction
  `0<=a_n<=(7/10)/n`, `delta_n<=19/100`, `C_n<4247/10000`,
  `C_(n-1)<4253/10000`, `C_(n-2)<4253/10000` is impossible.

The fourth input is the quantitative first-failure consequence to be derived
from the analytic smoothing inequality

```
C_n <= sqrt(n/(n-1)) C_(n-1)
       + sqrt(n)/(15 (n-1)^(3/2)) + 0.08 sqrt(n)/(n-1)^2.
```

This derivation is an open analytic obligation in the skeleton. The final
local-exclusion input includes the supported confinement, all p panels and
positive-noise local comparison, and the separate zero-noise Bernoulli case.
It is not supplied by scalar arithmetic alone.

The auxiliary acquisition schedule is also open: A40/P41 give the 1.5/n
ceilings, A45/P46 give the 0.7/n ceilings, and A46 gives the stronger 46 ceiling.
`TailContracts` starts at the exported ceilings rather than pretending that
these numerical acquisitions have already been checked.

What Lean proves from these inputs:

* A contrary index49 forces three backward losses at 49,48,47. Their sum is
  greater than (54/100)/46, contradicting the stronger 46 ceiling. The exact
  rational margin is 35419/254251200.
* Strong induction rules out every later failure. The preceding sharp bound
  makes delta_n=0 and smoothing gives n a_n<0.29<0.7. At n=50, the second
  deleted-index cap uses the auxiliary bound at 48; afterwards earlier sharp
  bounds suffice. All absolute caps are proved using the displayed rational
  thresholds.

This tail proof takes **no** sharp bound for the entire range 1,...,48 as an
argument. This removes an unnecessary dependency in an overstrong coarse graph.

Lean: `BEMap/Tail.lean` (`tail_base49`, `tail_composition`).

## 9. Separate lower bound and current proof boundary

The lower-bound route requires a justified Esseen lattice expansion for each
fixed admissible rational Bernoulli parameter, a compatible subsequence of n,
and then continuity/optimization in that parameter. It must supply
`LowerApproximation`. Neither the expansion nor this approximation is proved
in this package. Given it and the upper-bound contracts, Lean proves
`globalConstant = esseenConstant` with the concrete supremum definition.

The package contains no `sorry`, no project-declared `axiom`, and no
`native_decide`. That means the **conditional implications** are checked, not
that their premises have been discharged. Standard mathlib logical axioms in
the audit are distinct from the still-open theorem arguments. Always inspect
both theorem signatures and the printed axiom lists.

## 10. Source baseline and traceability

The specification is based on the conversation titled “Przelicz end-to-end
dowód”, the local manuscript and the repository at commit
`6ca9730273c81447be4863824c0b7d012db0e8b8`. The conversation is context, not
mathematical evidence. Its discussion was checked against the source inventory.

* [Repository proof graph](https://github.com/rodziewiczk/berry-esseen-end2end/blob/6ca9730273c81447be4863824c0b7d012db0e8b8/proof/proof_graph.md)
* [Historical obligation graph](https://github.com/rodziewiczk/berry-esseen-end2end/blob/6ca9730273c81447be4863824c0b7d012db0e8b8/proof/obligations.json)
* [Logic-audit repairs](https://github.com/rodziewiczk/berry-esseen-end2end/blob/6ca9730273c81447be4863824c0b7d012db0e8b8/proof/logic_audit_repairs.md)

The manuscript baseline is `berry_esseen_manuscript.tex`,9252 lines,
SHA-256 `2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
Useful source anchors are sections `afcore:sec:conserved`,
`afcore:eq:contact-input`, `afcore:eq:contact-polynomial`,
`afcore:eq:gap-definitions`, `rescore:re-enclosure` and `rescore:re-atlas`.
Machine-readable local provenance and checked file hashes accompany the project.

The historical 97-node, 157-edge graph is a sufficient abstract graph, not a
complete enumeration of present numerical instances. This skeleton records
the n25 predecessor alternative, keeps the independent tail independent, and
does not mistake a historical global composer for a finite conditional export.
Local work in progress in the source repository has not been changed or
certified as part of this delivery.
