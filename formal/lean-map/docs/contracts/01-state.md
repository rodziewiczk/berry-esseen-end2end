# 1. Concrete meaning of the mathematical state

This document specifies semantic types, not an executable representation of an
unknown extremizing distribution. It is based on the manuscript identified in
`provenance.json`. The Lean records make the same-law, same-index and
same-threshold dependencies explicit. Analytic theorems may be supplied as
named, source-bound inputs; their exact conclusions are fixed here.

## 1.1 Two levels which must not be confused

**Mathematical level.** A hypothetical probability law, its actual moments and
an attained contact are quantified in a theorem. A state contains proofs that
this one law satisfies the listed necessary bounds. A feasible numerical
moment vector is never presumed to be the moment vector of a law.

**Numerical level.** `CountTaskContext n` contains finite rational/natural data:
interval endpoints, support and resource caps, the original count domain, a
numerical target and source identities. The future checker receives this data
and a finite certificate. It does not receive a probability measure or an
unknown witness. `CountTaskContext.SatisfiedBy` interprets the frozen data for
every hypothetical contact to which it applies.

This is the mathematical analogue of a strongly typed interface: a producer
must satisfy the exact postcondition required by its consumer. A numerical
dictionary with similarly named entries is not a substitute for that proof.

## 1.2 Base law and the exact target

`StandardizedLaw` means a probability measure P on R with

```
EX = 0, EX² = 1, Integrable |X|³,
rho = E|X|³ >= 1, gamma = EX³, beta = E[X|X|].
```

`ProbabilityLaw.convolutionPow P n` is the law of the sum S_n.
`normalizedSum P n` is the law of S_n/sqrt(n). The CDF is closed: P(Y<=y).

```
Delta_n(P) = sup_y |P(S_n/sqrt(n) <= y) - Phi(y)|,
R_n(P)     = sqrt(n) Delta_n(P)/rho(P),
C_n        = sup_P R_n(P),
C_E        = (3+sqrt(10))/(6 sqrt(2 pi)).
```

The final upper result is C_n<=C_E for every integer n>=1. The sharp global
equality additionally needs the separate lower approximation. n=0 is only a
totalization of auxiliary definitions and is never an admissible final index.

## 1.3 Contact index, extraction floor and numerical output cap

`ContactAt n floor` contains the actual law, a normalized threshold z,
`floor <= R_n(P)`, `R_n(P)=C_n`, and the positive attained closed-CDF equality
`P(S_n/sqrt(n)<=z)-Phi(z)=Delta_n(P)`.

The extraction floor is a real parameter. The following are different types:

```
ContactAt 4 (4097/10000)       ROOT4's stronger target,
ContactAt 4 C_E               a weaker critical-C_E contact,
ContactAt 25 C_E              the n25 contrary contact.
```

No automatic conversion between them is used. In particular, extraction only
above C_E cannot prove the stronger bound C4<=4097/10000.

`FixedIndexExtraction n floor` extracts a contact from the strict violation
`floor<C_n`. The global strict failure is preserved through `w.optimal` when a
weak numerical bound `R_n(P)<=floor` is used to contradict it. Equality at the
target is not thereby excluded. `ClosedIndexExtraction` is a separate stronger
input for an argument which genuinely requires extraction at equality.

A numerical output cap such as a rational COUNT target is yet another role.
It can be below the extraction floor. `CountTaskContext.target` does not change
the type of the contact. `BoundRelation` records whether an output is weak or
strict; no unproved positive margin is invented.

## 1.4 Raw and normalized thresholds

`NormalizedThreshold` holds z. `RawThreshold` holds H. The designated conversion
for an n-contact is H=sqrt(n)z. Raw characteristic functions, contact
polynomials and predecessor CDFs use H, not z.

`ContactNormalizationEvidence w` supplies the exact normalization theorem

```
rawCDF(w) - Phi(z) = Delta_n(P),
rawCDF(w) = P(S_n <= H),       n>0.
```

The positive closed equality in `ContactAt` is initially in normalized
coordinates; it does not silently license the raw equality. The bridge is
required before COUNT normalizes a raw probability upper bound into a score.

Reflection, when used analytically, replaces the entire oriented law and its
threshold. Signed beta/gamma, positive probability, support, gap data and all
subsequent records refer to that one oriented law. A Fourier cancellation
which temporarily reflects both signs does not change the owner of the
physical contact or permit reflecting a predecessor half-line independently.

## 1.5 Three different defects

| Quantity | Exact meaning | Consumer |
|---|---|---|
| Matching moment defect | rho-(gamma²+2)/sqrt(gamma²+4) | Earlier two-point stability development |
| Physical gap defect D | (3+sqrt(10))rho-gamma-3J | Conserved contact identity and resource budget |
| ROOT4 excess eta | rho(P)-rho(Q3(P)) for the canonical three-atom reference | Physical ROOT4's common defect measure |

These are separate definitions, not aliases. A theorem about the earlier
matching moment defect is not automatically a theorem about D or eta.
`UnweightedDefectCap X d` means D<=d. `WeightedDefectCap X n N d` means
`nD<=N d`. The actual n and the floor N are separate natural parameters.

The checked conversion `weighted_to_unweighted` requires n>0, N<=n and d>=0.
It does not justify multiplying an unweighted conclusion by N to produce a
weighted export. The ROOT4 state and its common-measure semantics are specified
separately in `BEMap/Root4.lean`.

The exact native cap derived from nD<=N d is `(N*d)/n`. The helper
`derivedNativeDefectCap` computes this rational number, and
`weighted_to_native_defect_cap` proves its meaning. A frozen context stores
`nativeDefectCap` separately, with a proof `(N*d)/n<=nativeDefectCap`.
The numerical kernel's `cfg.D` is this unweighted native cap; it is not an
implicit alias for the weighted export parameter d. The signed quadratic's
factor15000/(997*n) always uses the actual index n.

## 1.6 Physical support gaps and canonical budget

A `SupportGap X` is a pair (a,b), with a<b, whose endpoints lie in the actual
closed support of P and whose open interior contains no support point. Thus
arbitrary subintervals of a gap cannot be counted as extra gaps.

Define tau(t)=E[X 1_{X>=t}]. `gapWeight` evaluates tau at (a+b)/2, an interior
point, to avoid accidentally including an atom at the left endpoint. The
canonical quantities sum over **all** such bounded gaps:

```
J  = sum tau_gap (b-a)²,
J1 = sum tau_gap integral_a^b (t-a)t dt,
J2 = sum tau_gap integral_a^b (t-a)t|t| dt,
L  = sum tau_gap integral_[a,b) (t-a) dLaw(H-S_(n-1))(t).
```

The half-open interval in L is part of its definition. `GapEvidence` requires
summability of all four families and proofs D>=0 and L>=0. Totalized integrals
or infinite sums are not numerical acceptance rules.

With s=sqrt(n), C=R_n(P), phi=phi(z), define

```
Kq = E|X|⁵/4 - rho EX⁴/2 - 3 beta gamma/2 + rho/2,
K1 = E[X|X|³] - 3 beta - 3 rho gamma/2,
U  = J1+(EX⁴-3)/6,
R  = C(3 beta J/2 + 3 rho J1 - 3J2 - Kq)
     + H(C K1 + phi U) - H²(C rho + gamma phi/2) + E_n.
```

`physicalError` is the canonical hinge error with factor -n sqrt(n)/2, not an
arbitrarily selected remainder. `ConservedIdentity` states exactly

```
R = n(C-C_E)rho + n C_E rho(1-exp(-H²/(2n)))
    + n phi(0)exp(-H²/(2n)) D/6 + n sqrt(n)L.
```

This is one budget. Two consequences charged to the same resource cannot be
added unless a simultaneous inequality explicitly licenses their sum.
The first term is nonnegative only under the additional gate C>=C_E; the
identity itself is defined at other positive extraction floors as well.

## 1.7 Binary coordinates and weighted noise

The exact sign convention is p=P(X>0), q=1-p, m=E max(X,0), v=pq and h=v/m.
Zero atoms belong to the nonpositive class. Define

```
I = 1_{X>0}, U = hX-I+p,
s = E U², lambda_n = n s, theta = s/h².
```

`BinaryModel X` binds the two conditional residual laws to the normalized
restrictions of this exact P to X<=0 and X>0, pushed forward by U. It includes
0<p<1, m>0, centering, integrability and the variance identity s=h²-v. Thus
`lambda_n`, s and theta have different meanings and different cap types.

For an acquired central gap(-A,B), the raw residual inner endpoints are

```
a0 = p-hA,        a1 = (1-p)-hB,
U0 in[-O0,a0],    U1 in[-a1,O1],
dY = a0+a1 = ((m/q-A)+(m/p-B))/(m/q+m/p).
```

The original five-coordinate COUNT point is **(p,lambda,alpha,u,a0)**.
Its fifth coordinate is `rawInward0`, not the sum dY. A separate total-inward
budget supplies dY<=d0. Consequently a0<=d0, but equality a1=d0-a0 is not
assumed. The actual a1 remains enclosed by the conditional support and the
joint resource. Confusing a0 with dY changes the numerical problem.

`ConditionalNoiseSplit` supplies alpha in[0,1] and the exact conditional
variance equalities

```
E U0²=s(1-alpha)/q,       E U1²=s alpha/p.
```

There is no division by s. At zero noise alpha may be any licensed value in
[0,1], with the zero conditional moments retained. `NoiseBranch` explicitly
separates zero and positive weighted noise. For the same X,
`lambda24=(24/25)lambda25` is proved algebraically; it does not transfer an
index25 contact equation to index24.

## 1.8 Joint resource versus marginal caps

`FrozenJointBudgetData` has two explicitly different branches. A zero joint
budget means dY=lambda=0, with no division. A positive budget stores d_star>0
and Lambda_joint>0 and means

```
dY/d_star + lambda/Lambda_joint <= 1.
```

The marginal lambda cap L may be contracted while this original plane stays
unchanged. It is invalid to replace Lambda_joint by L without a new proof.
For example dY=1/2,d_star=1,lambda=1,Lambda_joint=2 satisfies the plane and
lambda<=L=1. Substitution of L gives3/2>1. Types and frozen field names keep
these quantities separate.

`ResourceState.jointBudgets` is a catalog of licensed joint budgets tied to
their actual central gap and actual index. A resource refinement must retain
the catalog's earlier entries; a new entry needs its own proof.
`CountReadyState` selects a joint budget for its **same** central gap and
records its membership in that catalog. A scalar theta/lambda contraction
cannot rewrite a joint intercept.

The native scope additionally has a simultaneous affine lower price
`D>=binaryCharge+gapCharge*dY+noiseCharge*lambda` and a coherent signed
quadratic D upper envelope. They are separate acquired law inequalities,
not consequences of unrelated marginal caps.

## 1.9 Stages and their stored invariants

| Type | Required actual-law content |
|---|---|
| `PhysicalState w` | Raw normalization; contact majorant; acquired support; higher-moment evidence dependent on that support; gap sums; complete hinge Fourier bounds; exact conserved identity |
| `InitialState w` | Physical state; own-index cap; separately proved actual predecessor allowance; simultaneous moment intervals; raw-threshold interval |
| `ResourceState w` | INITIAL; exact binary model; asymmetric signed support; floor-index weighted D cap; raw remainder cap; theta cap below1; actual-index marginal noise cap; retained joint-budget catalog |
| `CentralGap X` | Positive endpoints A,B in the actual support, no support in(-A,B), and A<=m/q, B<=m/p |
| `CountReadyState w` | Resource state; acquired central gap; conditional noise split; joint/affine/signed budgets; closed count identity and comparison; actual(p,lambda,alpha,u,a0) realization; separate dY cap; complete count cover |

Support is acquired before fourth/fifth moments. An actual central gap is
acquired later; defining J over support gaps does not itself establish a gap
around zero. The support-free n5 corner uses a different state and does not
need to manufacture any of these support/gap records.

Every interval in `MomentBox` contains the actual rho, signed beta/gamma,
p, EX⁴ or E|X|⁵. Independently chosen extrema at incompatible moment corners
are not a state of one law. A resource refinement must preserve simultaneous
soundness and explicitly return any new endpoint floors, as specified next.

`GeneralCountRealization` is the separate numerical-law scope for an arbitrary
standardized law X, actual index m and raw H. It has the same native
resource/coordinate semantics and no `ContactAt`, extremality, attainment or
optimalConstant requirement. It bounds the signed positive-orientation point
score `sqrt(m)/rho*(P(S_m<=H)-Phi(H/sqrt(m)))`. This is the public semantic
route used for the same law at24 in AB. The ordinary attained-contact scope
converts into it using the exact raw normalization bridge.
