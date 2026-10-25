# 4. Mathematical certificate semantics and the trust boundary

This part fixes what acceptance means. It does not prescribe a production
file format, parser, cache implementation or cloud scheduler. Those choices
must implement this meaning without changing it.

## 4.1 Frozen numerical input versus the unknown law

An extremizing law is an unknown object universally quantified in a theorem.
It is **not** input to a numerical job. A checker must never be asked to
evaluate an integral of that unknown law or receive a `ContactAt` object as
runtime data. Such contacts occur only in the semantic proof.

`CountTaskContext n` is the frozen finite mathematical input to a COUNT job:

| Fields | Exact interpretation |
|---|---|
| Actual n, with n>=2 | The integer used in binomial probabilities, normalizations and weighted noise |
| `target`, `targetRelation` | Rational output cap and explicit relation (`<=` or `<`); distinct from the contact extraction floor |
| `sourcePin` | Manuscript digest, analytic-interface revision, numerical-kernel revision and source epoch; provenance metadata |
| `domain` | All original n+1 products, including p range, Lambda and the total d0 cap (the final root axis is raw a0) |
| `rho`, `beta`, `gamma`, `fourth`, `fifth`, `mean` | Closed rational intervals for the actual moments and m=E X_+; positive lower rho and m bounds |
| `rawThreshold` | Closed rational interval for raw H, not H/sqrt(n) or count phase u |
| `supportRadius` | Positive rational R for the acquired bound abs(X)<=R |
| `negativeRadius`, `positiveRadius` | Separately acquired asymmetric radii Rminus,Rplus, both bounded above by the convenience R |
| `conditionalOuter0`, `conditionalOuter1` | Nonnegative caps for the two sign-conditioned residual outer supports |
| `jointBudget` | Separate zero-resource branch, or positive intercepts with dY/d0+lambda/Lambda<=1; Lambda is not the marginal lambda cap |
| `affineBudget` | Nonnegative binary charge and positive gap/noise prices for binaryCharge+gapCharge*dY+noiseCharge*lambda<=D |
| `signedEnvelope` | A nonempty coherent family of signed threshold quadratics, maximized over its complete corner family |
| `ownCap`, `predecessorCap` | Own-index score cap and nonnegative allowance for the same law at the previous index |
| `floorIndex`, `defectCap` | Positive N<=n and d>=0 for nD<=Nd, with the physical defect |
| `nativeDefectCap` | The unweighted native D cap, with the explicit weakening N*d/n<=nativeDefectCap |
| `rawRCap` | Signed upper bound for the canonical raw remainder |
| `thetaCap` | Rational 0<=Theta<1 for the original-scale variance fraction |
| `negativeGapFloor`, `positiveGapFloor` | Positive rational floors for the two acquired physical gap endpoints |

All numerical fields are rational or natural. The simple index/ordering proof
fields validate finite decidable input conditions. None is a measured unknown
moment or a serialized probability law.

`GeneralCountRealization` fixes which arbitrary law, raw threshold and actual
coordinate realizations satisfy the frozen numerical context. It has no
extremality or contact premise, so it also applies to the same-law AB transfer
at24. `CountTaskContext.SatisfiedBy` in the ordinary physical-state interface
adds the owner-contact acquisition statements. The primary count meaning is
then **fixed**, not selected by an implementer:

```
CountCertificateMeaning ctx payload:
  every declared leaf conclusion is valid
  for every actual law, raw threshold and realized point
  satisfying ctx's concrete physical scope and that leaf's closed box.
```

Every p, lambda, alpha, phase and raw-a0 coordinate is tied to the same law.
The generic score is the signed positive closed discrepancy at the specified
raw threshold, not an absolute value or an assumed attained supremum. The
ordinary contact adapter proves equality with that contact's normalized score.
The mathematical proof uses its count-mixture/normalization/conditional-moment
identities. The numerical checker instead proves uniform whole-cell
inequalities in the frozen parameters, using the accepted analytic rules.
Every method gate must hold uniformly on its stated applicability domain;
checking only a midpoint or a sampled favorable point is insufficient.

The candidate `CountCertificatePayload ctx` contains a complete forest and
an aligned finite list of leaf conclusions. Entries are ordered exactly by
increasing count root and left-first depth-first traversal. `boxes_match`
requires exact equality with the geometric forest leaves. `entry_cover`
proves that every original-domain point reaches one of those same entries.

The signed native envelope is
`D <= (15000/(997*n))*max_j(A_j+F_(j,sign(H))*abs(H)-Q_j*H²)`, with Q_j>0.
The maximum keeps every coherent score/moment corner. It is not a separate
upper bound for each quadratic, and it cannot be replaced by a minimum of
their coefficients. A minimum is legitimate only between independently valid
complete envelopes, or with an independently valid scalar D cap.

## 4.2 The three things which must remain separate

1. A **candidate payload** is untrusted data: a search tree, interval table,
   polynomial witness, resource transcript or downloaded historical result.
2. A **checker implementation** examines that payload and returns a result.
3. A **soundness theorem** proves that the accepted result entails the exact
   mathematical proposition claimed for the payload and its fixed context.

The Lean interface is

```
CertificateChecker Payload Meaning
  check : Payload -> CheckResult
  sound : forall payload, check payload = accepted -> Meaning payload

CheckedCertificate checker
  payload : Payload
  accepted : checker.check payload = accepted

CheckedCertificate.meaning : Meaning certificate.payload
```

`Meaning` is a proposition over the actual mathematical problem. It includes
the declared index, law orientation, normalization, original domain, target,
analytic theorem assumptions, coverage and leaf implications. It is not the
proposition “the checker returned accepted”. The theorem `meaning` uses the
soundness field; executing a program or presenting a Boolean alone is not a
replacement for it.

The analytic theorems accepted for this construction remain explicit proof
parameters of this soundness/meaning layer. They need not be reproved in
Lean at this project stage. Their exact statement, assumptions and source
must nevertheless be identified, and a numerical checker must prove the
conclusion of that statement under exactly those assumptions.

## 4.3 Weak and strict numerical conclusions

`BoundRelation.closed` means value<=cap; `BoundRelation.strict` means
value<cap. A leaf conclusion is either `scoreUpper cap relation` or
`infeasible`. Both the leaf relation and context target relation are explicit.
Closed domain coverage never supplies strictness by itself.

`BoundRelation.Transfers` fixes when a leaf cap entails the configured target:

| Requested context target | Required cap comparison |
|---|---|
| Weak score<=target | cap<=target; either weak or strict source relation is usable |
| Strict score<target | cap<target, or cap<=target together with a strict source relation |

`BoundRelation.transfer` proves this rule. In particular, a weak numerical
bound at a rational job target below C_E remains usable in the final sharp
argument. It is not required to manufacture another strict gap below the
job's own cap. Conversely, a source family which requires strict acceptance
must configure that relation explicitly.

The quantitative native return has a separate interface:
`QuantitativeCountPayload`, `CountBoundCertificateMeaning`,
`QuantitativeCountChecker` and `checked_quantitative_count_point_bound`.
It proves a returned rational upper even when the native early-exit target
was not achieved. A target-achievement receipt is a stronger/different claim.
AB uses the actual returned upper, including a valid unresolved upper; it
never substitutes the private early-exit target for that numerical result.

The numerical output target, the contact extraction floor, and the final C_E
are distinct roles. A valid adapter proves the necessary comparison between
them. ROOT4 may use 4097/10000 while a later global argument uses C_E.

## 4.4 Result semantics

`CheckResult` has `accepted` or `failure reason`. Reasons are fixed constructors:

| Result | Mathematical effect |
|---|---|
| `accepted` with the soundness theorem | Provides the full declared `Meaning` |
| `malformed` | Payload could not be interpreted; supplies no proof |
| `unsupported` | Required operation/domain is not implemented; supplies no proof |
| `guardFailed` | This rule's applicability was not established; supplies no proof |
| `incomplete` | Cover/transcript/required evidence is missing; supplies no proof |
| `rejected` | The acceptance condition did not pass; supplies no claimed exclusion |

`failure_is_not_acceptance` proves the constructor separation. A failed guard
is not a semantic contradiction. A timeout is incomplete data, rather than
evidence that the mathematical cell is empty. A lower bound equal to an upper
bound is a singleton intersection and remains in scope.

## 4.5 Required mathematical meaning by certificate family

### Rational interval or polynomial leaf

The payload must establish its inequality on every real point of the declared
closed rational domain. Outward lower/upper arithmetic must agree with the
direction of each use. Divisions require a proven denominator sign. A radical
comparison requires nonnegativity of the quantities being squared. A finite
series requires a proved remainder with its required sign or absolute bound.

The structural interval type records lower<=upper. No rounding algorithm is
trusted by virtue of producing two rationals. Each arithmetic operation needs
a sound enclosure theorem. All constants used in one numerical expression
remain frozen at the stated endpoints before any convex/corner maximization.

### Resource transcript

The meaning is finite, ordered preservation of the same actual law/contact.
Each step must consume only previously established inequalities, preserve
normalizations, and intersect a simultaneous state with a valid consequence.
The final export is valid only after all preceding required steps.

Weighted nD, physical D, n E U² and E U² are separate quantities. A numerical
bound on a different defect notion is not imported under a shared variable
name. A failed positivity gate supplies no resource contradiction. A strictly
negative upper bound for an independently proved nonnegative resource can
supply a contradiction; equality cannot.

### LOW/HIGH integration

The meaning includes the exact remainder function, same threshold and split,
integrability, every interval piece and the infinite tail. It retains one
complete coherent LOW triple and a compatible HIGH bound. Coordinatewise
minima across different strategies are not valid without a new joint theorem.

A finite-window integral bound is not a full half-line bound. Totalized Lean
integrals are not evidence of integrability; the corresponding proof fields
are mandatory in the Fourier interface.

### COUNT forest

The meaning includes **all** of the following conjunction:

* The original n+1 count roots and their full product domains.
* A complete finite tree for each root, with strict interior cuts and both
  closed children; or another representation with a proved equivalent
  `CountLeafCover` of the same original products.
* For each leaf, one applicable valid method whose entire inequality concerns
  the same point and physical realization.
* Exact conditional-probability conventions: outgoing P(W>u), incoming
  P(W<=threshold), so atoms at the threshold are preserved.
* The same coherent moment/phase choice and nonnegative own-mass lower bounds
  wherever their direction requires nonnegativity.
* Positive normalization lower bounds on every normalization piece, with all
  pieces and all score/moment corners retained before taking maxima.
* The exact configured weak/strict score relation at the declared numerical
  target, or an actual necessary-condition contradiction. Any stricter final
  comparison is supplied separately, with `BoundRelation.Transfers`.
* Confinement or separately certified exterior threshold tails.

`CountTree.cover` proves only the geometric union. A tree with valid geometry
but an unproved leaf is incomplete mathematical evidence.

## 4.6 Original domain, physical realization and leaf assertions

The numerical relaxation may contain points that correspond to no actual
law. Its domain must still contain every actual law covered by the theorem.
Necessary conditions may prove that a portion of the relaxation is empty of
physical realizations. A method must not infer realizability merely because a
relaxed box is nonempty.

For an actual physical state, the realization proof binds p, lambda, alpha,
phase and raw a0=p-hA to its coordinates. The same realized point is
passed through the original-domain membership proof, geometric cover and
semantic leaf theorem. `CountLeafCover.conclude` preserves this identity.
An index25 extremizer is not replaced with an unrelated extremizer at24.

For zero noise, the variance allocation alpha may be chosen in [0,1] without
division by zero; its conditional-moment equations still have to hold. For
positive noise, the chosen alpha must satisfy the exact allocation formula.

## 4.7 Source binding and reusable evidence

Source hashes identify provenance, not mathematical truth. Reusing accepted
evidence requires equality of the complete semantic statement, including:

```
source epoch / analytic-rule version
actual index and any distinct floor/transfer index
law orientation and threshold normalization
original domain and all closed endpoint conventions
target and strict/non-strict conclusion
resource/LOW/HIGH/moment/phase assumptions and their units
method family and every required control/leaf/corner
```

A cache key can later encode these data, but a matching byte string cannot
stand in for the proof that these are the intended problem. A cached search
candidate must be replayed or used through a verified reuse theorem. A local
report from a historical run contributes only its documented scope; it does
not automatically discharge a new semantic contract.

## 4.8 The boundary accepted at this checkpoint

**Accepted mathematical inputs:** the precise analytic theorem interfaces
and their sources, supplied as parameters rather than global custom axioms.

**Lean-checked structure:** actual mathematical definitions, identity of the
indexed objects, finite cover composition and the final conditional assembly.

**Still to implement/connect:** payload representations, exact numerical
acceptors and their soundness proofs, parsers, source-binding validation and
connection of historical/new numerical evidence to the semantic records.

**Specification BLOCK:** any particular numerical family for which the exact
statement, assumptions, original cover or connection to a transition remains
undetermined. Such a family must not be advertised as implementation-ready
until its missing contract is completed. An accepted analytic theorem which
is merely supplied as a parameter is not a specification BLOCK.

No checker implementation or serialization layout is claimed here. The
contract is intentionally independent of Python/Java/cloud tooling: those
implementations must preserve the same mathematical acceptance criterion.
