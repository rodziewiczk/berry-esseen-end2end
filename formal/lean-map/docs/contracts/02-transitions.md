# 2. Exact contracts for transitions and separate arguments

This chapter fixes the mathematical operation contracts. Their named analytic
statements may be trusted as project inputs at this stage; reproducing all
their analytic proofs in Lean is not required to specify an implementation.
An implementation must nevertheless consume the listed hypotheses and return
exactly the stated conclusion. An unresolved mathematical bridge is not a
choice delegated to a programmer.

## 2.1 Operation table

| Operation | Input | Output | Source / required restriction |
|---|---|---|---|
| Extract a contact | Fixed n>=1, extraction floor b, strict failure b<C_n | One `ContactAt n b` with R_n(P)=C_n | Attainment/orientation at **b**; extraction only at C_E does not service ROOT4's smaller b |
| Raw normalization | Same contact; n>0; H=sqrt(n)z | P(S_n<=H)-Phi(z)=Delta_n(P) | Exact pushforward/CDF theorem, closed event on both sides |
| Contact majorant | Unrestricted attained positive closed contact, n>=2 and C>0 | The explicit polynomial dominates h(y) everywhere and touches on support | `afcore:eq:contact-input`, `afcore:eq:contact-polynomial` |
| Qualitative then quantitative support | Contact majorant; every radius/cap/predecessor gate used by the selected support argument | `SupportedContact w` for the selected rational R>0 | Support callback is a distinct theorem, not a Fourier output |
| Higher moments | Previously acquired support for this law | Integrability of X⁴, |X|⁵ and X|X|³ | `HigherMomentEvidence support`; no higher-moment use before support |
| Gap and conserved budget | Same contact/support/moments, complete gap sums and hinge inversion | D>=0, L>=0 and exact budget equality | `afcore:eq:gap-definitions`, `afcore:prop:conserved` |
| Hinge LOW/HIGH | Same law, raw H, actual n and one positive split b | One coherent LOW triple, complete HIGH integral, integrability and error bound | `rescore:eq:finite-low-triple` and full-high lemmas; high interval extends to infinity |
| INITIAL | Acquired physical state, own cap, predecessor allowance, all moment and phase bounds | A simultaneous `InitialState w` | A predecessor license alone is insufficient |
| Resource update | Earlier actual-law state and applicable atlas/geometry gates | Tightened actual-law state and separately licensed endpoint floors | Finite schedule; no fixed-point hypothesis |
| COUNT readiness | Binary conditional laws; acquired central gap; actual root realization; original product membership; complete cover | `CountReadyState w` | All n+1 roots; a central-phase gate or separate tail argument |
| COUNT bound | One coherent outgoing/incoming envelope plus normalization and cover | A weak or strict score cap with its declared endpoint relation | `countcore:countineq`, `countcore:scorebound`, `countcore:forest` |

## 2.2 The contact polynomial and predecessor allowance

For the actual C=R_n(P), s=sqrt(n), H=sz and F=P(S_n<=H), the polynomial is

```
n Q_H(y) = nF + (H phi(z)+C rho)/(2s)
           -(s phi(z)+3C beta/s)y
           -(H phi(z)+3C rho)y²/(2s) + (C/s)|y|³.
```

`ContactMajorant w` asserts h(y)=P(S_(n-1)<=H-y)<=Q_H(y) for every real y,
with equality on the actual closed support. The support premise is not a
restriction to a two/three-atom reference family.

`actualPredecessorAllowance w` is
`n max(R_(n-1)(P)-R_n(P),0)`. Its index is n, and its reference score is the
current contact score. The earlier n25 bridge uses the sufficient bound
`25 max(R24(P)-C_E,0)<=5/16`. Since C>=C_E, that bounds the actual allowance
as well. Changing the reference from C to C_E requires this monotonicity gate.

## 2.3 Exact geometric resource update

The following formulas are frozen by `GeometryInput`, `GeometryRule` and
`RoundedGeometry`. Source: `rescore:re-residual`, `rescore:re-geometry`,
`rescore:re-exports` and `rescore:joint-resource`.

Input data are an existing `ResourceState w`, an actual `CentralGap X`,
a closed I=[l,u] with 0<l<=u<1 containing p, a ceiling0<=Theta<1 for theta,
positive endpoint floors A_l<=A, B_l<=B, and the **weighted** nD<=N d with
0<N<=n and d>=0. Define

```
sigma = sqrt(10), p_star=(4-sqrt(10))/2,
s_minus=min(l(1-l),u(1-u)),
s_plus=1/4 if l<=1/2<=u, otherwise max(l(1-l),u(1-u)),
b_I=(6+2sigma)(1-Theta)^(3/2) dist(p_star,I)^2 / sqrt(s_plus),
r_I=d-b_I,
K_plus =3(sigma+1)B_l, K_minus=3(sigma+3)A_l,
K=min(K_plus,K_minus), m_l=sqrt((1-Theta)s_minus).
```

The positivity gates imply K>0 and m_l>0. The simultaneous residual theorem
uses the actual inward displacements Delta_A=m/q-A and Delta_B=m/p-B:

```
6m(A_l+B_l)(Delta_A+Delta_B)+K_plus theta_plus+K_minus theta_minus <= r_I.
```

The deterministic output formulas are

```
theta_formula=min(Theta,r_I/K),
A_formula=max(A_l, sqrt((1-Theta)l/(1-l)) - r_I/(6m_l(A_l+B_l))),
B_formula=max(B_l, sqrt((1-Theta)(1-u)/u) - r_I/(6m_l(A_l+B_l))),
n theta <= N r_I/K,
n d_Y   <= N r_I/(6(1-Theta)(A_l+B_l)),
lambda_n<= N s_plus r_I/((1-Theta)K).
```

Here d_Y=(Delta_A+Delta_B)/(m/q+m/p), exactly the `CentralGap.inward` value.
`GeometryConsequences` states all six conclusions simultaneously. The source
theorem is a declared analytic input, not something inferred from an output
dictionary. The weighted exports are **not** N times an unweighted variance
or theta cap.

The stronger joint theorem has a separate `JointPriceInput`: a simultaneous
necessary inequality

```
D >= b + 6m S_star(Delta_A+Delta_B) + K theta,
b>=0, S_star>0, K>0, pq<=v_star, nD<=N d.
```

For r=d-b>0 its exact positive intercepts are

```
d_star = r/(6(1-Theta)S_star),
Lambda_joint = N v_star r/(K(1-Theta)),
dY/d_star + lambda_n/Lambda_joint <= 1.
```

`JointResourceTheorem` states this exact source theorem, together with the
r<0 contradiction and the separate r=0 conclusion dY=lambda=0. Its intercept
formulas are rational definitions when the priced inputs are rational.
`acquireJointBudget` appends a newly proved budget to the state's catalog.
It does not overwrite a joint intercept with a tightened marginal lambda cap.

The required branch rules are fixed:

* r_I<0: the necessary residual inequality contradicts feasibility.
* r_I=0: retain the zero-noise/zero-inward case; lambda_n=d_Y=0.
* r_I>0: use the positive-intercept formulas with their positivity gates.
* A failed endpoint or denominator gate: no new update. It is not an
  emptiness certificate. The earlier sound state remains available.

Rounding directions are explicit proofs:

```
theta_formula <= theta_ceiling,
A_floor <= A_formula, B_floor <= B_formula,
weighted_lambda_formula <= lambda_ceiling.
```

`geometryTransition` returns **both** a resource refinement and an
`AcquiredGapFloors` packet. The resource component intersects old/new theta
and lambda caps by min. The endpoint packet intersects the old/new floors by
max. A next geometry input uses that packet's numerical floors together with
their bound proofs. It must not reconstruct positive endpoint floors from
an unlicensed number or silently forget an exported endpoint.

## 2.4 Finite resource schedules

`ResourceSchedule` has only `stop` and `step edge rest` constructors. Every
edge contains an actual after-state, the same floor index and nonincreasing
defect/raw/theta/lambda caps. All semantic fields of the after-state are
proved again for the same w. `ResourceSchedule.output` is finite recursion;
`lambda_tightens` is proved by finite induction.

A support or phase callback consumes only bounds acquired earlier in that
schedule. Its theorem must list its positive denominator, signed orientation,
all exterior-ray gates and source-index scope. A callback's failure preserves
the previous state. No convergence, eventual regime or unproved fixed point
can be used to justify a finite export.

The refinement type also requires nonworsening own/predecessor caps, all six
moment intervals, raw-threshold interval, both signed support radii, and
retention of every earlier joint-budget entry. A tighter bound for one
coordinate cannot silently discard another acquired hypothesis.

## 2.4a Native frozen scope beyond scalar caps

The native input includes both signed support radii Rminus/Rplus and both
conditional outer residual caps O0/O1. A larger symmetric radius can lose a
tighter regional kernel's hypotheses. `GeneralCountRealization` binds the
asymmetric radii and conditional supports to the same actual law.

It also consumes two different simultaneous D inequalities:

```
D >= binaryCharge + gapCharge*(a0+a1) + noiseCharge*lambda,
D <= (15000/(997*n)) * max_j(A_j+F_j,sign(H)*|H|-Q_j*H²), Q_j>0.
```

The first has binaryCharge>=0, gapCharge>0 and noiseCharge>0. The second
retains one coherent nonempty family of signed quadratics and uses actual n.
Take the maximum across all corners in that family, including both clipped
sign segments where the H interval crosses zero. A minimum of independently
chosen corner coordinates is invalid. A minimum with a separately proved
scalar D cap is valid.

`ctx.defectCap` means the floor-weighted nD<=N d export. `nativeDefectCap`
is separately frozen and licensed by N*d/n<=nativeDefectCap. The kernel's
`cfg.D` means the latter. An adapter must not silently identify these caps.

## 2.5 COUNT arithmetic and normalization

For a fixed root k in Fin(n+1), write u=np+hH-k and
W_j=the convolution of n-j copies of U0 with j copies of U1. Define

```
b_j=choose(n,j)p^j(1-p)^(n-j),
F_Bin(k)=sum_(j<=k)b_j,
P_out=P(W_k>u)=1-P(W_k<=u),
P_in,j=P(W_j<=u+k-j).
```

`CountComparisonRule` is the exact analytic inequality

```
P(S_n<=H) <= F_Bin(k)-b_k P_out+sum_(j>k)b_j P_in,j.
```

It accompanies `CountIdentity`'s exact conditional mixture. A `CountEnvelope`
provides B>=F_Bin(k), b_minus<=b_k with b_minus>=0, L<=P_out, and
nonnegative B_j>=b_j and A_j>=P_in,j. Then the checked algebra gives

```
Q = B-b_minus L+sum_(j>k)B_j A_j >= P(S_n<=H).
```

L may be negative; the two-stage outgoing substitution still uses the
nonnegative true probability and the nonnegative b_minus. A negative own-mass
lower bound is not licensed. Incoming bounds are nonnegative so that replacing
their mass coefficients by upper bounds preserves the inequality direction.

The normalization packet supplies N<=Phi(z), sqrt(n)<=n_plus, and
0<rho_lower<=rho. With the exact raw normalization bridge, Lean proves

```
R_n(P) <= (n_plus/rho_lower) max(0,Q-N).
```

The positive part is taken before enlarging the upper factor. rho_lower is
the **lower**, not upper, rho bound. The whole coherent envelope is consumed
together. Choosing coordinatewise best entries from unrelated strategies is
not justified by this theorem.

There is a second, separately typed COUNT portfolio.
`CoherentCountNormalEnvelope` bounds the whole expression

```
F_Bin(k)-b_k P_out+sum_(j>k)b_j P_in,j-Phi(z) <= errorUpper.
```

Native Gaussian-slope cancellation can produce controls valid only in this
combined difference. They are not standalone incoming CDF uppers. This
portfolio retains the same phase and compatible cubic moments through its
whole-box Bernstein control. `score_le_combined_count_upper` normalizes its
coherent error upper with the positive-part/rho-lower discipline.
`CountLeafEvidence.combined` and `.bounded` are distinct constructors.

`SupportedCountEvidence w` concerns this one contact and its applicable
regional state. It does not require a global COUNT provider for every contact
at that n. The optional global `ContactPipeline n floor` is only a convenience
when an actual global provider is available.

## 2.6 Separate mathematical methods

### Supported four-term Prawitz

The n5 Fourier complement uses `PrawitzScoreEvidence`, not the compensated
hinge LOW/HIGH ledger. The former has the kernel

```
K(t)=(1-t)+i((1-t)cot(pi t)+1/pi), 0<t<1,
g(ct)^n=exp(-n c²t²/2), c>0, 0<tau<1.
```

Its four terms are exactly

```
int_0^tau |K(t)| |f(ct)^n-g(ct)^n| dt,
int_tau^1 |K(t)| |f(ct)|^n dt,
int_0^tau |K(t)-i/(pi t)| g(ct)^n dt,
(1/pi)int_tau^infinity g(ct)^n/t dt.
```

The analytic smoothing theorem bounds Delta_n by their sum. The record
requires integrability and a rational upper bound for every term. Endpoint
pieces and the infinite normal tail remain present. Normalization again uses
sqrt(n) upper and rho lower. Source: `afcore:eq:prawitz` (the four-term
Shevtsova/Prawitz normalization). A valid hinge remainder bound is not a
substitute for any of these four numerical inequalities.

### Support-free n5 corner

`GapFreeEvidence w` needs raw normalization, a probability upper, a Gaussian
lower and the normalized cap. Its type contains no acquired support radius,
central gap or higher moments. The finite corner cover includes both infinite
phase rays; see `five:eq:lefttail`, `five:eq:righttail` and the exact corner
source. Merely covering the compact phase intervals[0,1],...,[4,5] is
insufficient. The provider is universally quantified over all eligible corner
contacts, including any contact on those exterior rays.

### Universal rho tail

`UniversalRhoEvidence` uses the published structural envelope

```
T(rho)=min(0.469,0.3322(1+0.429/rho),0.3031(1+0.646/rho)).
```

Its inputs are a positive cutoff, actual rho>=cutoff, the structural bound,
the monotone specialization and an exact comparison T(cutoff)<=target.
For n5, the source uses only the third structural bound at rho>=7361/4000;
the typed n5 provider uses that separate `FiveTailEvidence`, rather than
requiring all three published bounds unnecessarily.

### ROOT4

ROOT4 is a separate canonical-Q3 family with excess eta, common defect
measure, thresholds and noise classes. The ordinary physical D/resource state
does not substitute for it. The localization interface returns one numerical
owner of `Root4PhysicalClass` under a strict violation at4097/10000. The
certificate bounds that bounded physical class weakly by4097/10000; equality
at the target is retained. Strong quantitative n3 is the input.

### Mixed E, compatible chord and AB

See [the source-specific mixed contracts](MIXED.md). The labels “p24 E” and
“p25 ABCDF” denote probability panels; E still concerns the original n=25
law. Only the AB reference argument transfers the same law to the actual
24-sum. These are separate operations:

* E and the compatible chord produce a necessary **rho ceiling**, or refine
  the same-law state. They do not directly assert an R25 target bound.
* The chord retains compatible cubic moments, the coefficient8b, signed
  reciprocal arithmetic, and all32 closed retained-inward cells.
* AB transfers lambda24 and the joint Lambda by24/25 and the noise price by
  25/24; the intrinsic law properties remain unchanged. It discards the
  n25 contact/phase fields and obtains a new complete24-sum half-line bound,
  with all25 roots, its full phase and exterior tails.
* A uniform half-line upper U gives the constant ray allowance
  q_R=25 max(U-CElo,0), with CElo<=C_E. This licenses a later support callback on that
  whole closed ray; it does not itself prove the final regional score bound.

The mixed scalar, reference and support steps feed ordinary COUNT or a
specific necessary-condition contradiction. A direct assumed target bound
with an index24 label is not the mixed mathematical interface.

### General24 numerical bridge and quantitative outcomes

`GeneralCountRealization ctx X H point` contains no attained contact or C24
optimality. Its output concerns the signed positive-orientation point score
`sqrt(m)/rho*(P(S_m<=H)-Phi(H/sqrt(m)))`. This is the correct native meaning
for the same X at24. Ordinary contact scope specializes this type, using the
exact normalization theorem to identify that point score with attained R_n(P).

`CountCertificateMeaning` checks achievement of a declared output target.
`CountBoundCertificateMeaning` and `QuantitativeCountPayload` separately
certify valid returned bounds, including bounds above a native early-exit
search target. AB may consume a valid returned U; the search target is never
substituted for U. These are different numerical output roles.

`ABGeneralCountPort` fixes a new24-sum context, transferred original domain,
source identity and an exact raw-H interval equal to the requested closed
half-line intersected with[-47/4,47/4]. It supplies the general-law realization
for every eligible raw H and nearest root, then applies the quantitative
checker theorem to construct `Mixed.ABWindowCountPacket`.

Each requested half-line gets its own scope; a union requires all scopes.
An irrelevant leaf proves no realization in this clipped scope, rather than
global impossibility of the law. If the intersection is empty,
`ABEmptyCentralPort` supplies an explicit emptiness proof and vacuous central
bound, without inventing a nonempty `ClosedInterval`. Equality at a cut or
window seam is retained. Both exterior tails remain mandatory in the later
`completeHalfline` operation.

## 2.7 Strong and weak conclusion relations

The default global proof starts from a **strict violation** b<C_n and obtains
a weak local cap R_n(P)<=b. That is enough for contradiction. It does not
prove C_n<b or exclude equality at b. A strict conclusion is available only
from an explicit strict numerical/analytic relation or an exact gap between
the output cap and the requested target.

`BoundRelation.Transfers` records the alternatives. This distinction matters
for ROOT4, closed seams, zero-noise cases and any checker which accepts
`upper<=TARGET`. A closed domain cover alone creates no strictness.
