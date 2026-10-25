# Ordinary COUNT: semantic replay rules

This catalogue fixes the mathematical meaning of the six EMPTY tags reported
for the reviewer's selected ordinary COUNT forest, together with PASS_TARGET.
It is a specification of the numerical replay obligations, not a claim that
those numerical proofs have been ported into Lean. The six tags are not the
complete set of branches in the historical evaluator. An unsupported tag must
be rejected or reported as unsupported; it must never be interpreted as EMPTY.

These seven tags form the selected final-verifier rule catalogue. Broader
historical evaluators and mixed D/AB acquisitions have separately specified
rules in `MIXED-REGISTRY.md`; sharing a scalar numerator does not erase their
different gates or scopes. Ordinary global forests and AB's complete subtree
of one original count5 ancestor also have distinct coverage contracts.
The independent all-index local comparison in `UNIFORM-TAIL.md` is another
separate contract: its TINY/MID/LOW witnesses prove a noise-proportional
comparison with the same law's Bernoulli score, not an ordinary COUNT
scoreUpper. `TAIL-ASSEMBLY.md` likewise specifies auxiliary resource-pass
exports and their negative-D closure rather than reusing these score leaves.

## Two different certificate boundaries

The present public `CountCertificateMeaning` is a **mathematical replay
boundary**: the complete frozen task, original boxes, ordered leaf entries,
and uniform semantic validity of every claim are mandatory. A checker may
recompute the original exact evaluator and establish that meaning through an
explicit analytic/numerical soundness parameter. A status string, a digest,
or equality with a saved result does not by itself establish soundness.

A **self-contained arithmetic trace** would additionally carry the local
arithmetic witnesses listed below: outward enclosures, rational polynomial
coefficients and their positivity witnesses, selected bounds with their gates,
and a proof of each contradictory strict comparison. That trace format and its
verified arithmetic evaluator are not implemented by the current generic
`infeasible | scoreUpper` payload. This catalogue fixes what a future decoder
or evaluator must prove; it does not rename the current payload as such a trace.

The mathematical leaf meaning and required inequalities are specified. An
implementation may choose exact source-bound replay or a new self-contained
trace while preserving that meaning. This is an explicit engineering/trust
choice; no further mathematical interpretation of EMPTY or PASS is delegated
to that implementation.

## Shared state and arithmetic conventions

Every claim quantifies over **every unknown law** satisfying the same frozen
task and the same closed leaf. No law is serialized as a runtime input.
For one such law and leaf, use:

- integer index `n>0`, root `k∈{0,…,n}`;
- `p∈[pl,pu]⊂(0,1)`, `q=1-p`, `v=pq`;
- `lambda∈[lo,hi]`, `s=lambda/n=E(U²)≥0`;
- allocation `alpha∈[al,ah]⊂[0,1]` and phase `u∈[ul,uh]⊂[-1/2,1/2]`;
- conditional mean-zero residual laws `U0∈[-O0,a0]`,
  `U1∈[-a1,O1]`, with conditional variances `s0,s1`;
- `s0=s(1-alpha)/q`, `s1=s alpha/p`;
- actual inward distances `a0,a1≥0`, `dY=a0+a1≤d<1/2`;
- `D=(3+sqrt(10))*rho-gamma-3J`, with a proved upper cap `Dcap`;
- acquired bounds `rhoLo≤rho≤rhoHi`, raw threshold
  `H∈[-Hminus,Hplus]`, and physical variance `theta≤Theta` where needed.

The fifth leaf coordinate is **a0**, not dY. The conditional supports and all
moments belong to this same law. The original joint intercept Lambda in
`dY/d0+lambda/Lambda≤1` is distinct from an acquired marginal lambda cap.
The asymmetric support bounds Rminus/Rplus are distinct inputs.

Let `vL=min_{p∈[pl,pu]}p(1-p)` and `vH=max_{p∈[pl,pu]}p(1-p)`; the maximum
includes the half seam. Let `sigmaL≤sqrt(10)≤sigmaH`. All square-root and
division bounds are outward rational enclosures with explicitly positive
denominators. Each strict comparison uses the correct directed endpoints.
Failure of a gate or inability to establish an enclosure is **not** EMPTY.

Before the six rules below, the source evaluator may contract the cell using
acquired mean, signed beta, allocation, conditional support, phase-resource,
or joint-resource constraints. Each contraction must preserve every unknown
law in the original cell. Their updated bounds and supporting facts must be
included in a replay derivation; they cannot be inferred from the final tag.

## EMPTY_PHASE

**Inputs:** the original root/phase/probability/noise box and acquired raw
threshold interval. The exact representation is

`H=(k+u-n*p)/sqrt(p*q+s)`.

**Gates:** n>0; ordered closed input intervals; 0<pl≤pu<1; s≥0; denominator
lower bound strictly positive. The source forms an outward interval Hbox by
interval arithmetic, then intersects it with `[-Hminus,Hplus]`.

**Necessary inequality:** the same actual H lies in both closed intervals.

**Strict EMPTY condition:** `Hbox.upper < -Hminus` or
`Hplus < Hbox.lower`. Equality at either endpoint survives.

**Output:** no law/point can satisfy this original leaf and frozen task.

**Replay facts/witness:** exact original inputs, outward square-root/quotient
bounds, acquired threshold evidence, and one strict endpoint inequality.
Source: `exact35_core.py:425–428`.

## EMPTY_ACQUIRED_THETA_VARIANCE

**Inputs:** n, p interval, current `[lo,hi]`, and acquired physical
`theta≤Theta`.

**Gates:** n>0; 0<pl≤pu<1; 0≤lo≤hi; 0≤Theta<1. The exact bridge is
`theta=s/(p*q+s)`, equivalently
`lambda=n*p*q*theta/(1-theta)`.

**Necessary inequality:**

`lambda ≤ capTheta := n*vH*Theta/(1-Theta)`.

**Strict EMPTY condition:** `lo > min(hi,capTheta)`. If no contradiction is
obtained, replacing hi by that minimum is a valid contraction. Lambda and
all joint-plane prices remain unchanged.

**Output:** infeasibility, or a contained lambda interval preserving all laws.

**Replay facts/witness:** the theta acquisition proof, exact bridge,
vH extremum, positive denominator, rational cap and strict comparison.
Source: `theta_variance.py:7–16`; wrapper
`rho_signed_moment_tightener.py:38–40`.

## EMPTY_SHARP_BOX

This is the **termwise actual-endpoint** sharp lower bound. It does not
require the additional monotonicity gates of the different EMPTY_SHARP_GAP
branch.

**Inputs:** closed conditional variance enclosures `[s0L,s0H]`,
`[s1L,s1H]`, actual endpoint enclosures
`l0≤a0≤u0`, `l1≤a1≤u1`, total cap d, physical Dcap, and p/s intervals.

**Gates:** 0<pl≤pu<1; nonnegative variance lower bounds;
0≤l0≤u0, 0≤l1≤u1, l0+l1≤d<1/2; actual a0+a1≤d;

`c0=3*(sigmaL+3)*pl-(sigmaL+7)*u0 ≥0`,

`c1=3*(sigmaL+1)*(1-pu)-(sigmaL+5)*u1 ≥0`,

`3*pl≥u0`, `3*(1-pu)≥u1`.
If ui=0, the corresponding conditional variance must be zero; the ratio
`siL²/ui` then means its justified continuous value zero, never a default
totalized division. Otherwise ui>0.

Let bL be a certified lower bound over p∈[pl,pu] for

`(sigmaL-1)*p + (-3*sigmaL-3)*p²
 + (4*sigmaL+10)*p³ + (-2*sigmaL-6)*p⁴`.

Set

`f=l0+l1-l0²-l1²-l0*l1`,

`raw=bL+6*vL*f
 +pl*(s1L*c1+(sigmaL-1)*s1L²/u1)
 +(1-pu)*(s0L*c0+(sigmaL+1)*s0L²/u0)`.

For an outward upper bound `denH≥(vH+sH)^(3/2)>0`, let
`Lsharp≤max(0,raw)/denH` be the downward rounded result.

**Necessary inequality:** `D≥Lsharp`.

**Strict EMPTY condition:** `Lsharp>Dcap`. Equality survives.

**Output:** infeasibility. A midpoint exclusion may instead shrink an upper
endpoint, but its own lower-bound comparison and containment argument must be
retained. An unlicensed monotonicity assertion may not replace this rule.

**Replay facts/witness:** every endpoint/variance acquisition, all gates,
sigma enclosure, polynomial lower certificate (for example complete
Bernstein coefficients), denominator enclosure, and strict comparison.
Source: `exact35_core.py:46–50,70–81,443–448,470–490`.

## EMPTY_JOINT_CUBICS

**Inputs:** the same conditional supports/variances, acquired rho interval,
Dcap and endpoint box. Introduce the actual signed conditional third moments
`x=E(U0³)` and `y=E(U1³)`.

**Support rectangle:** for a mean-zero variable in [-L,U] with variance w,

`w²/L-L*w ≤ E(V³) ≤ U*w-w²/U`.

Minimize/maximize these quadratics over the closed variance enclosure, using
the clipped critical points L²/2 and U²/2. Zero support endpoint forces the
variance and third moment to zero. This produces `[xL,xH]×[yL,yH]` with
the source assignments `(L,U)=(O0,a0)` and `(a1,O1)`.

**Same-rho strip:** write `pm=(pl+pu)/2`, `pw=(pu-pl)/2` and
`cx=-(1-pm)`, `cy=pm`. Let h3L/h3H enclose `(v+s)^(3/2)`, and set

`tL=rhoLo*h3L-vH*(1-2*vH)-3*vH*(s0H+s1H)`,

`tH=rhoHi*h3H-vL*(1-2*vL)-3*vL*(s0L+s1L)`,

`e=pw*max(abs(xL+yL),abs(xH+yH))`.

The necessary strip is `tL-e≤cx*x+cy*y≤tH+e`.
This follows from the actual same-law identity
`rho*(v+s)^(3/2)=v*(1-2v)+3v*(s0+s1)-(1-p)*x+p*y`.

**Optional defect half-plane:** use `l0=max(a0floor,s0L/O0)`,
`l1=s1L/O1`; require l0≤a0, l1≤a1, l0+l1≤d<1/2.
Let b be max(0,bL) with the polynomial lower bound above;
`f=l0+l1-l0²-l1²-l0*l1`,
`c0=3*(sigmaL+3)*pl-6*a0`,
`c1=3*(sigmaL+1)*(1-pu)-6*a1`.
Only when f,c0,c1≥0 add this plane. Define

`base=b+6*vL*f+(1-pu)*s0L*c0+pl*s1L*c1`,

`ax=-(sigmaL+1)*(1-pm)`, `by=(sigmaL-1)*pm`,

`ex=(sigmaH-sigmaL)*(1-pl)+(sigmaL+1)*pw`,

`ey=(sigmaH-sigmaL)*pu+(sigmaL-1)*pw`,

`err=ex*max(abs(xL),abs(xH))+ey*max(abs(yL),abs(yH))`.

The additional necessary inequality is
`ax*x+by*y ≤ Dcap*h3H-base+err`.
If its gates fail, omit this plane and keep the valid rectangle/strip.

**Strict EMPTY condition:** the resulting closed rational half-plane system
is infeasible. A portable witness is rational nonnegative Farkas weights
whose weighted normals sum to zero and whose weighted right sides sum to
a strictly negative number. The historical code instead enumerates every
nonparallel pair intersection and checks all inequalities. For that method,
replay must establish boundedness from the support rectangle and completeness
of the enumeration, including degenerate feasible line segments and points.
An unexplained empty vertex list is not a witness.

**Output:** no common conditional moments, hence no law, can satisfy the leaf.

**Replay facts/witness:** all source half-planes and their sound derivations,
all rounding directions, and Farkas weights or a complete bounded-polytope
enumeration certificate. Source: `joint_cubic.py:7–44`,
`joint_cubic_defect.py:9–43`, `exact35_core.py:502–504`.

## EMPTY_RHO_UPPER

**Inputs:** p/s/conditional variance intervals, outward supports O0,O1>0,
and acquired rhoLo. For i=0,1 define

`zi=clip(Oi²/2,[siL,siH])`, `Ci=Oi*zi-zi²/Oi`.

These are upper bounds for the appropriately oriented conditional cubic
terms in the absolute-moment numerator. Let

`w0=1-pl if C0≥0 else 1-pu`,

`w1=pu if C1≥0 else pl`,

`rawHi=vH*(1-2*vH)+3*vH*(s0H+s1H)+w0*C0+w1*C1`.

For `denL≤(vL+sL)^(3/2)` with denL>0, compute an upward bound
`rhoU≥max(0,rawHi)/denL`.

**Gates:** same-law identities and valid supports/variances; 0<pl≤pu<1;
siL≥0; Oi>0; positive denominator enclosure. The coefficient choice must
depend on the sign of Ci as above.

**Necessary inequality:** `rho≤rhoU`.

**Strict EMPTY condition:** `rhoU<rhoLo`. Equality survives.

**Output:** infeasibility. A noncontradictory rhoU can tighten the rho cap.

**Replay facts/witness:** support/variance acquisitions, exact clipped
quadratic maxima, sign choices, root lower enclosure and strict comparison.
Source: `exact35_core.py:89–93,495–501`.

## EMPTY_ACQUIRED_RHO_VARIANCE

**Inputs:** acquired rhoLo>0, p/allocation/lambda box and O0,O1>0.
Choose rational `0≤t≤sqrt(vL)` and define

`A=rhoLo*vL*t-vL+2*vL²`,

`M=max_{p∈{pl,pu},a∈{al,ah}}
 ((3*p+O0)*(1-a)+(3*(1-p)+O1)*a)`,

`B=M-(3/2)*rhoLo*t`.

**Gates:** n>0; 0<pl≤pu<1; 0≤lo≤hi; 0≤al≤ah≤1;
rhoLo>0; O0,O1>0; certified t enclosure. For the nontrivial A>0 branch,
also establish `(3/2)*rhoLo*t-1+4*vL>0`, the source's explicit monotonicity
gate. The branch A≤0 supplies no new EMPTY conclusion.

**Necessary inequality:** `A≤B*s=B*lambda/n`. This uses the same-law
absolute third-moment numerator upper bound with coefficient M, the convex
tangent lower bound for `(v+s)^(3/2)`, and the monotonicity gate to replace
the actual v by vL.

**Strict EMPTY conditions:** A>0 and either B≤0 (since s≥0), or
B>0 and `n*A/B>hi`. Otherwise replace lo by max(lo,n*A/B).

**Output:** infeasibility or a necessary lambda lower bound preserving the
same law. The first branch is not licensed when A≤0.

**Replay facts/witness:** acquired rho lower proof; outer-support proofs;
vL extremum and square-root lower proof; four M corners; monotonicity gate;
sign of A/B and the final strict comparison.
Source: `rho_variance_floor.py:11–28`; wrapper
`rho_signed_moment_tightener.py:47–49`.

## PASS_TARGET / scoreUpper

**Inputs:** the full source-exact count identity, all n+1 root masses,
strict outgoing events and closed incoming events, Phi normalization,
positive rho lower and sqrt(n) upper enclosures. A selected native result
may instead bound the whole coherent binomial/Gaussian expression; it need
not expose an independent upper bound for each incoming probability.

**Necessary conclusion:** for every law/point in this closed leaf, its
positive closed-CDF score is ≤a stated rational cap. A direct source route is

`ownloss = bMassLower[k]*(1-ownCDFUpper)`,

`difference ≤ max(0,min(binCDFUpper-ownloss+incomingUpper-PhiLower,
                       centeredBinGaussianUpper-ownloss+incomingUpper))`,

`score ≤ roundUp(sqrtNUpper/rhoLower * differenceUpper)`.

The native coherent route combines the Gaussian slope with incoming and own
terms **before** maximizing over the common phase and conditional cubic
polygon. Its conclusion is a bound for that combined expression. A bound
computed with independent, incompatible choices of the common law's cubic
moments, Gaussian term, or denominator cannot be substituted silently.

**Gates:** every selected probability/kernel/stop-loss/quartic bound must
meet its own source hypotheses. If multiple sound strategies are available,
their complete upper bounds may be minimized. This does not license taking
the minimum of incomplete corner/parameter covers. Bernstein, MGF, support,
derivative and common-moment gates belong to replay facts, not to a status tag.

**Target relation:** the historical ordinary engine uses **strict**
`scoreUpper < target`; target is `CE_LO+K/n` for its frozen task, not a
universal replacement for the actual contact floor. The public typed payload
also supports closed targets: cap≤target suffices for a closed target;
for a strict target use cap<target or a strict source cap with cap≤target.
Weak ROOT4 is a different family and must not inherit the ordinary strict
test. Retain exact rational target and explicit relation in the task.

**Output:** uniform upper cap plus its closed/strict relation. Both the cap
and its semantics, not merely PASS_TARGET, are consumed by final assembly.

**Replay facts/witness:** chosen complete bounding strategy, its original
inputs and arithmetic enclosures, all needed gates, and the rational target
comparison. Source: `exact35_core.py:421,515–563`; its wrappers preserve
physical exports and only select a smaller **complete** score bound.

## Source pins

The immutable original archive is `cutoff25_20261011.zip`, SHA-256
`17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`.
All listed members have prefix
`cutoff25_20261011/new_audit/fixed_law24_b5_p24_eps01_v1/`.
The path component `p24` must not be interpreted as a proof of an extremizer
at index 24. The task's explicit n and the source's same-law scope govern.

| Member | SHA-256 |
|---|---|
| exact35_core.py | a618867ae34841b2e3e1745e35142694142e08ca2d790b762870f50651e16d71 |
| theta_variance.py | d33f4e4aced4a1a3887f16964b25a3d716df00702d5c12d3212403b4644831fd |
| rho_variance_floor.py | 615acbcb948d2ba5767082f0dd2a2ab6f1d3999ae0a8afac3fd4c1d73b3aab6b |
| rho_signed_moment_tightener.py | f1650ff9ea811d66acf5f3529e0c0c462cc2d4747fbb42d147406714d0fc2be0 |
| joint_cubic.py | d4adf6e9cfa430bbd7be7ffd90b994672d648d9886c42aa38e0a94b66eb55238 |
| joint_cubic_defect.py | 86874d28284f931b8907b573c118a9fb8191653a6569d903aed54c9f1974e970 |

The rule formulas above were read from these archive members without importing
or executing their code. Historical module docstrings such as "diagnostic"
do not themselves establish or refute a bound: the replay implication remains
an explicit mathematical trust premise until proved. The reviewer-reported
forest statistics are observations from its historical target, not newly
verified measurements for the present branch.
