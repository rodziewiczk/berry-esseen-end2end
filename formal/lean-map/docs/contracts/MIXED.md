# Mixed lower-B5 rules: E, compatible chord, and AB same-law24

`BEMap/Mixed.lean` is the mathematical contract for three different operations.
It does not identify them with an ordinary COUNT leaf and does not assume
the final n25 score bound as an input.

| Operation | Output | What may consume it next |
|---|---|---|
| E pointwise scalar | A ceiling on the same law's rho | Strict rho contradiction, or a justified refinement |
| Compatible-moment/chord scalar | A ceiling on the same law's rho | Strict rho contradiction, or finite support/resource feedback |
| AB same-law24 | A quantitative positive closed predecessor-score bound on a requested raw halfline, hence a constant ray allowance | The ray contact/support theorem, followed by the applicable ordinary numerical argument |

**The name p24 E denotes the probability panel p in [0.24,0.25], not 24 summands.**
That E calculation is applied to the original n25 law. Only the AB argument
changes the sum index to 24, and it keeps the marginal law unchanged.

The analytic statements below are accepted mathematical inputs at this
project stage. Their exact meanings are formal records. They are not
reproved by the numerical code and are not inferred from historical PASS
strings or the titles of old audit files.

## 1. One physical frame and its units

For the same law X and its actual sign-conditioned centered residual laws,
write

```
p=P(X>0), q=1-p, v=pq, h=v/E X_+,
s=E U², lambda_n=n*s, h²=v+s,
V0=E U0²=s(1-alpha)/q, V1=E U1²=s*alpha/p,
m0=E U0³, m1=E U1³.
```

The zero atom is assigned to the nonpositive sign class. `EFrame X binary`
uses integrals of the actual conditional laws for V0,V1,m0,m1. They are not
four independent optimization variables. It includes square/cubic
integrability and the actual conditional support statements

```
U0 in [-O0,a0], U1 in [-a1,O1], O0,O1>0, a0,a1>=0.
```

When the acquired physical gap is(-A,B), the raw endpoints are
`a0=p-hA` and `a1=q-hB`. Their sum is the normalized inward displacement dY.
The last original COUNT coordinate is **a0**, not dY. The frame must be
connected to those actual endpoints, or supplied with the exact physical-D
halfplane license below. Merely choosing numbers satisfying support bounds
does not establish that halfplane.

The exact conserved cubic relation is

```
rho*h³ = v(1-2v)+3v(V0+V1)-q*m0+p*m1.
```

With sigma=sqrt(10), phi=a0+a1-a0²-a1²-a0*a1, the physical-D input is

```
D*h³ >= v[(sigma-1)+2p-(2sigma+6)v] + 6v*phi
        +q*V0[3p(sigma+3)-6a0] +p*V1[3q(sigma+1)-6a1]
        -(sigma+1)q*m0 +(sigma-1)p*m1.
```

D is the canonical physical defect, never the matching moment defect
rho-rho_two(gamma). `EFrame.physical_halfplane` is this exact input.
At a0=0, feasibility forces V0=m0=0; the explicit zero branch is part of
the frame, and no 0/0 expression is used to manufacture a moment bound.

## 2. E: exact scalar statement and frozen whole-box inputs

`FrozenEBox` contains closed rational intervals for p, s and alpha, fixed
positive O0,O1, total inward cap d in [0,1/2), upper bounds U0,U1 on a0,a1,
and the source pin. Here s is **unweighted** variance. In an n25 count box
it is obtained from lambda/25, not by reusing lambda as s.

The mandatory whole-path gates are

```
V0_upper <= p_lower(1-d-U0),
V1_upper <= (1-p_upper)(1-d-U1),
1-d-U0 >=0, 1-d-U1 >=0,
V0_upper = s_upper(1-alpha_lower)/(1-p_upper),
V1_upper = s_upper*alpha_upper/p_lower.
```

They license lowering the actual inward endpoints to V0/O0 and V1/O1 on the
entire path. If any gate fails, this E rule is inapplicable. It does not
exclude the cell and does not borrow a gate valid only at a midpoint.

The exact numerator encoded by `eNumerator` is

```
N=b(p)+s*M+s²*C,
b(p)=2p-6p³+4p⁴,
M=-6p(1-alpha)(1+1/O0)+alpha(2O1-6q/O1),
C=K0(1-alpha)²+K1*alpha²+K01*alpha(1-alpha),
K0=6(p+O0)/(q*O0²),
K1=(6q+4O1)/(p*O1²),
K01=6/(O0*O1).
```

The asymmetric 4O1 coefficient is intentional. The denominator of `eRatio`
is `(sqrt(pq+s))³`, with p strictly between 0 and 1 and s>=0. The source
analytic theorem `EPointwiseTheorem.necessary` states

```
(sigma+1)*rho <= D + N/(pq+s)^(3/2)
```

for the same frame realizing the entire frozen box. Zero s remains valid;
no division by s or a positive noise lower bound is introduced.

`ERatioBound` is the precise numerical obligation: the returned rational
upper U bounds that ratio for **every** p,s,alpha in the closed box.
If endpoint reduction is used, the signs of its derivative numerators
must hold on the entire current box. An uncertain sign retains the old
whole-box upper. At fixed p,s, the complete alpha interval is covered.

Signed division is mandatory: a nonnegative numerator upper is divided by
a positive denominator lower; a negative numerator upper is divided by a
denominator upper. A negative numerator does not license the former rule.

`eRhoCeiling` combines the analytic inequality, actual unweighted D cap,
uniform ratio bound and an outward rho rounding:

```
rho <= (Dcap+U)/(sigma+1) <= returned_rho_cap.
```

If Dcap+U<=0, this contradicts rho>=1. Otherwise the implementation follows
the source positive-denominator rounding and intersects the new cap with
the old cap. `RhoCeiling.excludes` requires cap<rho_lower. Equality retains
a valid ceiling; it is not EMPTY. No R25 score conclusion is returned here.

## 3. Directed physical acquisition for E and chord

The outer proposals preserve the two independently acquired support radii:

```
O0=min(acquired_outer0, Rminus*sqrt_upper-p_lower),
O1=min(acquired_outer1, Rplus*sqrt_upper-1+p_upper),
sqrt_upper >= sqrt(pq+s) throughout the same closed box.
```

These are `directedOuter0` and `directedOuter1`. Nonpositive proposals make
the cubic rule inapplicable. They do not authorize a division by that cap.

The total-inward proposal is the minimum of two separately valid bounds:

```
dY <= joint_d0*(1-lambda_lower/joint_Lambda),
dY <= (Dcap-binaryCharge-noiseCharge*lambda_lower)/gapCharge.
```

`directedInwardProposal` uses the **joint** intercept, not the marginal
lambda upper endpoint. The positive joint intercept and positive gap charge
are required. In the zero-joint-resource branch dY=lambda=0; there is no
division by the zero intercept. A negative residual budget excludes only
after the actual same-law resource license has been supplied.

`Dcap` here is the explicit native unweighted D cap. The weighted bound
nD<=N*d is converted first, through the visible N*d/n weakening proof.
The native D field is not silently filled with weighted d.

## 4. Compatible cubic ceilings and retained a0

Put b=s(1-alpha)=qV0, c=s*alpha=pV1, and

```
T=v(1-2v)+3(pb+qc),
U0=bO0-b²/(qO0), U1=cO1-c²/(pO1),
L0(a)=b²/(q*a)-b*a for a>0; L0(0)=0 only in the feasible b=0 case.
```

For z=V1/O1, the source uses the three compatible ceilings

```
raw:       rho <= (T+U0+U1)/h³,
plus:      (sigma+1)rho <= D+(G0(a0,z)+2U1)/h³,
minus:     (sigma-1)rho <= D+(G0(a0,z)-2T-2L0(a0))/h³,
G0(a,z)=2p*q²(1+2p)-6v(a+z-a²-z²-a*z)+6b(a-p)+6c*z.
```

All three refer to the same moments and the same physical frame. They do
not independently maximize m0 and m1. `CompatibleChordTheorem` supplies
these exact accepted analytic consequences and the necessary retained range.
`ChordPathGates` retains the source uniform conditions
`V0_upper<=p_lower(1-2d)` and `V1_upper<=q_lower(1-2d)`.

The actual a0 is retained in

```
V0/O0 <= a0 <= d-V1/O1.
```

The frozen outward lower and upper endpoints in `retainedLower/Upper`
include this interval for every p,s,alpha in the original box. Strict
reversal is a necessary-condition contradiction. Equality survives.
`ChordPartition` requires exactly 32 closed cells and their full union.
Every cell contributes to the final result, including zero-width cells.

`ChordFeasiblePoint` keeps the necessary variance lower bound, inward upper
bound, nonnegativity and the a0=0=>b=0 branch. A positive-reciprocal formula
is never applied at a0=0 solely because division is totalized in Lean.

## 5. Quadratic chord and signed reciprocal maximum

The minus numerator is encoded exactly as

```
C+K*a+Q*a²-Brec/a,
C=2p*q²(1+2p)-6v(z-z²)+6c*z-6bp-2T,
K=6v(z-1)+8b, Q=6v>0, Brec=2b²/q>=0.
```

The coefficient is 8b, including the2b from the L0 elimination. On[A,Z],
`a²<=(A+Z)a-AZ`. Upper bounds on C-QAZ and K+Q(A+Z), and a lower bound
Bmin for Brec, give a signed upper of the form

```
constant_upper + U*a - Bmin/a.
```

`reciprocalMaximum` fixes the complete case distinction:

* Bmin=0: maximize the linear term at both endpoints, including A=0.
* Bmin>0, U>=0: use the right endpoint, with Z>0.
* Bmin>0, U<0 and Bmin<=(-U)A²: use the left endpoint.
* Bmin>0, U<0 and Bmin>=(-U)Z²: use the right endpoint.
* Otherwise: the interior maximum is -2sqrt((-U)Bmin).

Endpoint equality belongs to the relevant closed case. In the interior
case an outward **lower** sqrt bound, multiplied by -2, gives an upper.
`ReciprocalMaximumTheorem` states this accepted scalar theorem with its
positive-domain/zero-reciprocal preconditions.

`ChordRatioBounds` supplies uniform numerical upper bounds for the three
ratios on every necessary feasible point of each closed cell. Negative
numerators retain signed interval division by the strictly positive
denominator. For each cell, take the minimum of its three valid ceilings;
then take an upper of those minima over **all 32 cells**. The rounding
field of `chordRhoCeiling` expresses precisely this maximum-of-minima rule.
A minimum across different cells is not a valid global ceiling.

The result is a `RhoCeiling`, not a direct score bound. A surviving ceiling
may feed finite same-box contact/support feedback. The original raw H,
signed beta, joint resource intercepts, moment/phase prices and all original
count coordinates remain fixed unless an explicit licensed transition
updates the named field. No numerical cap proves its own acquisition.

## 6. AB: the same marginal law at 24, with a new phase

AB is the only operation here that changes the summand count. It uses

```
lambda24=(24/25)lambda25,
joint_Lambda24=(24/25)joint_Lambda25,
noise_price24=(25/24)noise_price25.
```

Thus lambda_m/m is unchanged. `ab_noise_price_preserved` and the existing
same-law weighted-noise theorem record these identities. The affine
noise charge is preserved by `ab_affine_budget_preserved`. The joint
intercept is a different field from the marginal noise cap.

The standardized marginal, p, alpha, a0,a1, rho, signed beta, mean, support
and physical D remain the same. **No extremality, contact equation, n25
phase, or n25 threshold-dependent quadratic is supplied at 24.**

`transferredDomain24` has 25 roots k=0,...,24, full phase[-1/2,1/2] and the
same raw-a0 cap. Its lambda range extends to the transferred **joint** noise
intercept, not merely the current marginal lambda upper endpoint. The full
window gates use that joint scope. `joint_noise_upper` derives the actual
noise upper bound from the coupled budget and dY>=0.
`ABCountIdentity` is a conditional-count identity for every
raw24threshold, with no `ContactAt 24` parameter. `ABWindowCountPacket`
requires the entire root cover and a quantitative score upper at every
relevant semantic leaf, using actual returned numerical upper bounds.

The private early-exit target CE_LO+1/100 is not a returned upper bound.
Valid unresolved scores may contribute to a halfline maximum; an arbitrary
EMPTY/success label or the weak observation0<=CDF<=1 cannot replace the
required quantitative native bound.

## 7. AB window, weak D quadratic and exterior tails

The raw predecessor window is |z|<=Hstar=47/4. With eta=10^-12, use

```
A=(997*24/15000)Dcap+eta*Hstar²,
Fplus=Fminus=0, Qbudget=eta,
(15000/(997*24))(A-eta*z²)
  =Dcap+(15000*eta/(997*24))(Hstar²-z²) >=Dcap.
```

`abWeakBudget_valid` proves the weakening on this entire window. It is not
a new defect acquisition. The original n25 signed quadratic is discarded.

`ABWindowInput` freezes p and lambda scopes and requires the exact strict
squared window gates

```
Hstar²(vmax+lambda24_cap/24) < (24*p_lower)²,
Hstar²(vmax+lambda24_cap/24) < (24*(1-p_upper))².
```

The selected probability panels are below 1/2, so vmax uses the upper p
endpoint. The accepted `ABWindowScopeTheorem` gives 0<=24p+h*z<=24 on the
window. `nearest_root_exists` then licenses a closed nearest phase. The
Gaussian approximation's argument-domain and positivity gates must also
be checked by its pinned native arithmetic source; its source identity
alone does not establish those numerical gates.

`ABWindowCountPacket.window_bound` composes the new phase license, actual
same-law coordinates, all 25 root coverage and the quantitative per-leaf
meanings. It does not assume a uniform 24 extremal constant.

For each requested halfline the generic24checker context's raw threshold
scope is exactly that halfline intersected with[-Hstar,Hstar]. The helper
`clippedRawWindow` computes it by exact rational max/min. A strictly empty
intersection is a separate empty-central branch; equality gives a singleton.
A union of two requested halflines uses two scoped contexts. An irrelevant
leaf means no physical realization in **that scoped intersection**, not that
the marginal law is globally impossible.

The primary arbitrary-law `GeneralCountRealization` and the quantitative
certificate interface can instantiate these leaf meanings without a contact
at 24. `QuantitativeCountPayload`/`CountBoundCertificateMeaning` distinguish a
valid returned upper from achievement of the native early-exit target. The
returned upper may exceed that target while remaining useful for AB.

Both exterior tails are explicit. With rho>=rho_lower>0, X>=-Rminus,
t=1/3 and M=1+(exp(tRminus)-1-tRminus)/Rminus², the accepted exterior theorem
supplies the coded upper bounds

```
left:  (4.9/rho_lower) M^24 exp(-Hstar/3),
right: (4.9²/rho_lower)(2/(5Hstar)) exp(-Hstar²/48).
```

The factor4.9 exceeds sqrt(24). The left estimate is the centered bounded
MGF/Chernoff argument; the right is the Gaussian Mills bound. `ABTailNumericalBounds`
requires outward rational bounds on those actual transcendental expressions.
The source uses the degree40 positive exponential series and term41
geometric tail with ratio x/42; its argument domain is part of acceptance.

`ABWindowCountPacket.completeHalfline` combines the window and **both**
tails, with a maximum. Endpoint and window/tail equality are retained.

## 8. Raw halflines, support rays and the constant allowance

The predecessor threshold at a current n25 support point y is raw
`z=H25-y`. For a positive ray y>=R it lies in
`z<=H25_upper-R`. For a negative ray y<=-R it lies in
`z>=H25_lower+R`. These are closed half-lines for the **same unreflected**
positive predecessor CDF. The Gaussian contact expression's orientation
does not authorize reflection of the predecessor law.

`SupportRay.requiredHalfline` and `predecessor_inside` prove this raw
geometry. Broader acquired AB halflines can be reused only with an exact
containment proof. A boundary equal to a cut remains active.

If U is the quantitative positive closed24score upper on the entire required
halfline and CE_LO<=C_E<=C25, the derived allowance is

```
q_R = 25*max(U-CE_LO,0),
25*max(c24_positive_closed(H25-y)-C25,0) <= q_R
```

throughout that ray. This is `ab_predecessor_allowance`. It need not hold on
the central predecessor thresholds. q_R is frozen during the ray derivative
argument; no derivative of a changing piecewise allowance is taken.

The support-contact adapter reconstructs the exact affine expression with
the new q_R. It may not subtract a presumed improvement from an arbitrary
opaque old upper bound. The ray's full Gaussian/contact bound and all
strict derivative gates remain necessary. A resulting support refinement
can then feed the correctly scoped ordinary COUNT argument.

## 9. Source statement pins and acceptance boundary

The following are source identities, not claims of a new successful replay:

| Statement/component | Original member in cutoff25_20261013 | SHA-256 |
|---|---|---|
| E scalar | `low/pointwise_inward_defect_v2/pointwise_inward_v2.py` | `9c8b78578dcdef7863dc933bc142eb2c9b1b4f5e29fd49cca7497a2f4a4fbde3` |
| E interval arithmetic | `low/pointwise_inward_defect_v2/pointwise_interval_v2.py` | `aeb610b681466f6b2c729866462cb3a5767145614f5000509a992a5d0e5c41a5` |
| Physical E caller | `b5/coarse_pointwise_application_review_v1/application.py` | `400de430897cb50c748c2972808141aef65f089f4043937cd97de08d027aed89` |
| Compatible-moment cells | `root/coupled_third_moment_boxes_v1/box_kernel.py` | `81e3137085b2644da4eb5f0fcc04993a2b5935d24c75012082642a4068fad712` |
| Chord/reciprocal maximum | `root/coupled_chord_v1/kernel.py` | `cf36b3fc56b072047811fa47850b985efcb6b46bc097f7a36ba23e7d8e3a8431` |
| AB A full-window/halflines | `archive_audit/b5_sparse_halfline_review_v1/check24.py` | `2f69f53080e1a203eef30e4cc1f4b27cd497c3d210c416895af0cd94c620a8a5` |
| AB B full-window/halflines | `archive_audit/b5_sparse_next_pending_review_v1/check24_v2.py` | `00a11411033030077cdea88204969562e31fe32d49466dbcbcfdd83aeb26567f` |

Their tracked source maps are
`proof/code_n25_p24_pointwise_source_map.json`,
`proof/code_n25_p25_chord_source_map.json` and
`proof/code_n25_p25_references_source_map.json` in the research repository.
The corresponding internal audit notes are fallible reviews; the mathematical
contract is the explicit statement above tied to the pinned originals.
The manuscript physical-D halfplane/cubic identity is at lines 4216--4310
of the manuscript identified in `provenance.json`.

The p24 E registry requires containment in one acquired E rectangle; it
cannot stitch pieces of different rectangles into a new unproved theorem.
The dynamic p25 chord chain and AB/C/D/F reference families remain separate
acceptance rules, with their entire declared source/whole-box conditions.
This module gives the E/chord/AB interfaces and their derived output roles.
The separate [mixed registry contract](MIXED-REGISTRY.md) specifies C/D/F/AB
acquisition, their distinct source gates, exact single-scope lookup, finite
dependencies and original count5 subtree composition. Together they fix the
mathematical meanings of these selected families. They do not certify a
populated admission library or a complete B5 receipt. Missing canonical
capsule data and fresh arithmetic remain explicit source/evidence inputs,
rather than an “equivalent-looking” helper or a historical review label.

Pinned research context: [p24 E source map](https://github.com/rodziewiczk/berry-esseen-end2end/blob/6ca9730273c81447be4863824c0b7d012db0e8b8/proof/code_n25_p24_pointwise_source_map.json), [p25 chord source map](https://github.com/rodziewiczk/berry-esseen-end2end/blob/6ca9730273c81447be4863824c0b7d012db0e8b8/proof/code_n25_p25_chord_source_map.json), [AB/reference source map](https://github.com/rodziewiczk/berry-esseen-end2end/blob/6ca9730273c81447be4863824c0b7d012db0e8b8/proof/code_n25_p25_references_source_map.json).
