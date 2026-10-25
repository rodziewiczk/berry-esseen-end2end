# Acquired mixed references: exact scopes, lookup and composition

`BEMap/MixedRegistry.lean` specifies the C/D/F/AB reference library used by
the selected lower-B5 argument. It extends [the E/chord/AB contracts](MIXED.md)
with the mathematical meaning of an acquired reference, its permitted scope,
its source-bound inputs and its use by a later COUNT leaf. It does not run
the historical receipt scripts or claim fresh arithmetic evidence.

The module imports only `TypedPipeline`, `Mixed` and `GeneralCount`. It does
not import the public `BEMap` entrypoint, `Global` or `Assembly`.

## 1. Objects and units

The original owner is `w : ContraryContact 25`. Its distribution, actual raw
threshold and normalized positive closed contact remain fixed. A transferred
24-sum numerical calculation instead uses `GeneralCountRealization` for the
same law, with its new raw threshold and phase. It has no attainment or
optimality hypothesis at index24.

For an original COUNT point, the five real coordinates are

```
(p, lambda25, alpha, u, a0),
lambda25=25*s,  s=E U^2,  u=25*p+h*H-k,
h=p*(1-p)/E X_+ = sqrt(p*(1-p)+s),
a0=p-h*A, a1=(1-p)-h*B, dY=a0+a1.
```

`a0` is the fifth coordinate. Total inward displacement `dY` remains a
separate resource. The C/F scalar uses unweighted `s=lambda25/25`; its
weighted-noise box cannot be passed unchanged as an `s` box.

`p24`, `p25`, `p26` in `ProbabilityPanel` are probability-panel names. They
do not change the summand count25. Only AB creates a same-law24 numerical
problem.

`FrozenReference` records its full original `CountTaskContext 25`, exact ID,
panel, acquired scope, whole-cfg identity, source epoch and source pin.
Its epoch must agree with both the original context and reference source.
These labels select a statement; they do not prove it. The theorem is the
corresponding `ReferenceAcquisition` object.

## 2. Two distinct scope types and one-region containment

| Scope | Frozen coordinates | Coordinates universally covered |
|---|---|---|
| `ReferenceScope.phaseFree` | A closed `(p,lambda25,alpha)` law box | Every root count and every phase/raw-a0 allowed by the original context |
| `ReferenceScope.fullBox` | One exact root and all five closed intervals | Every point of that one closed five-dimensional box |

`ReferenceUse` requires equality of the **whole original context**, exact
cfg/source-epoch identity and containment in one acquired scope. In the
full-box case the root must be equal and each of the five caller intervals
must refine the corresponding acquired interval. In the phase-free case
all three projected intervals must refine the same law box.

The checked `ReferenceScope.contains_of_covers` and `ReferenceUse.excludes`
lemmas transfer the same actual point into that one acquired theorem. They
do not combine partial overlaps of several references. Several smaller
acquired regions require an explicit closed partition with a theorem for
each child; a list of overlapping labels is insufficient.

## 3. C and F: phase-free E contradictions

`PhaseFreeEAcquisition` uses the unchanged necessary E inequality on its own
law box. With `v=p(1-p)` and the functions defined in `Mixed.lean`,

```
Eratio = [b(p)+s*M(O0,O1,p,alpha)+s^2*C(O0,O1,p,alpha)]/(v+s)^(3/2),
b(p)=2p-6p^3+4p^4,
(sqrt(10)+1)*rho(X) <= D(X)+Eratio.
```

The packet supplies the exact frozen E gates, an actual physical frame,
a whole-box upper `ratioUpper`, an actual physical-defect cap and an outward
rational bound

```
(Dcap+ratioUpper)/(sqrt(10)+1) <= rhoUpper < original.rho.lower.
```

The derived `EArguments.excludes` proves the contradiction with the same
law's acquired lower rho bound. The whole-box bound is universal in
`p,s,alpha`; checking a center or optimizer sample does not inhabit it.

The source admission includes two C and32 F statements. The selected final
forest uses no C and seven distinct F statements in56 leaf occurrences.
C is nevertheless required by the frozen admission epoch. A future reduced
library must declare a replacement manifest/epoch rather than silently
dropping required entries.

## 4. D: three different mathematical reasons

The admitted D library has92 statements across probability panels,45 in
p25. The selected18 p25 references are seventeen `EMPTY_PHASE` full raw
boxes at root counts9..25 and one `POINTWISE_EMPTY` full box at count5.
`SelectedDShape` represents these facts separately from occurrence counts.
Neither kind is promoted to a phase-free theorem.

### 4.1 EMPTY_PHASE

`nativeRawThreshold` is the exact source expression

```
H=(k+u-25*p)/sqrt(p*(1-p)+lambda25/25).
```

`NativePhaseNormalization` is the explicitly accepted binary normalization
statement relating this expression to the actual raw threshold.
`EmptyPhasePacket.enclosure` must enclose it over the entire acquired
`p/lambda/u` intervals, with `0<p<1` and `lambda>=0`. The resulting raw
interval must be **strictly** disjoint from the original closed H interval.
Equality at a seam is retained. `EmptyPhasePacket.excludes` checks the
contradiction from actual interval membership. No scalar moment calculation
is needed for these seventeen selected references.

### 4.2 Saved finite prefix and the finished pointwise scalar

`FinitePrefixLicense` starts at the original cfg. Its finite chain has at
most preflight plus three further steps. Its only changing upper caps are

```
rhoUpper, Rminus, Rplus, O0, O1.
```

Every step has a named source recipe/pin, a proved refinement and an exact
accepted consequence `before.Valid(actual law) -> after.Valid(actual law)`
on the same original owner and full box. The H/beta/resource domain is not
replaced. `final_valid` composes these consequences by finite induction.
It does not infer a fixed point or a stronger predecessor theorem.

The source recipes are preflight, fixed-outer normalized ratio,
variable-support coupled ratio and full-ray contact. Their numerical
acceptors may omit an uncertain contraction and retain the previous caps.
The variable-support route uses
`O0=Rminus*sqrt(v+s)-p`, `O1=Rplus*sqrt(v+s)-(1-p)` and differentiates these
square roots when using its p/s derivative gates. Treating O0/O1 as constants
in that route would be a different rule. A source callback's successful
result, with its entire input and side conditions, must supply `step_sound`;
the recipe enum or a saved status cannot supply that proof.

The native prefix export finishes before COUNT/Gaussian evaluation. Its
additional scalar inputs are represented by `FinishedScalarData`: acquired
rho interval, p/s/alpha intervals, positive O0/O1, coherent V0/V1 intervals,
a0 floor, inward upper endpoints U0/U1 and total inward cap d. In particular,

```
L0=max(a0Floor,V0.lower/O0), L1=V1.lower/O1,
0<=L0<=U0, 0<=L1<=U1, L0+L1<=d<1/2,
t0=1-d-U0>=0, t1=1-d-U1>=0,
V0.upper<=p.lower*t0, V1.upper<=(1-p.upper)*t1.
```

`FinishedScalarRealization` binds these to actual conditional variances,
actual inward endpoints and the same physical frame. The **upper** variance
endpoints occur in the path gates. They need not equal the less precise
independent p/s/alpha variance estimates in a phase-free E box.

`AcceptedFinishedPointwiseTheorem` states the exact E-ratio necessary
inequality under these gates. L0/L1 are validated physical input bounds;
they do not occur in the final E numerator. A universal scalar upper and
outward rational rounding produce a rho ceiling strictly below the
**acquired prefix rho lower endpoint**. The acquired interval refines the
original interval and `FinishedScalarRealization.rho` proves actual rho
membership. No equality of the two lower endpoints is assumed.

The strict rho contradiction remains local to this root/full box. It is
not fed into its own prefix prerequisites.

### 4.3 Admitted unused normalized-defect rule

This is distinct from the finished E numerator. `normalizedDefectNumerator`
defines exactly

```
phi(L0,L1)=L0+L1-L0^2-L1^2-L0*L1,
N=b(p)-6*v*phi(L0,L1)
  +s*[6*(U0-p)*(1-alpha)+(6*U1+2*O1)*alpha]
  -2*s^2*alpha^2/(p*O1),
ratio=N/(v+s)^(3/2).
```

`NormalizedScalarData` requires positive p below1, nonnegative s, alpha in
[0,1], O1>0, ordered nonnegative inward lower bounds, and
`L0+L1<=d<1/2`. `NormalizedScalarRealization` relates all bounds to the
actual frame and acquired rho interval. The accepted necessary inequality
is `(sqrt(10)+1)*rho<=D+ratio`. `NormalizedAcquisition` requires a **uniform**
closed-box ratio bound before deriving its strict acquired-rho contradiction.

An optimized evaluator may reduce p/s only after the complete derivative
gates hold. At fixed p,s the alpha quadratic is concave, so it checks the
clipped vertex as well as endpoints; s=0 is handled as a linear/constant
branch. A negative numerator divides by a denominator upper bound. Whole-box
fallback remains permitted. These are implementation recipes for proving
the stated universal bound, not permission to return a point sample.
No selected D leaf uses this normalized rule, but an admitted manifest may
still require its proofs.

## 5. AB: final original count5 exclusion

An AB halfline allowance is an intermediate object. The acquired registry
theorem is a completed exclusion of one exact original count5 ancestor.
`CompletedABAcquisition` therefore requires this sequence:

1. Three old-q source-licensed support/moment stages from the original
   context. Their old `5/16` predecessor allowance must already be licensed
   by the retained stronger24 premise; AB does not create that initial
   premise.
2. Same-law24 quantitative bounds on each requested **entire closed raw
   halfline**, using the old-stage resources. The 24-sum scope discards25
   phase/contact fields, creates its own phase and all25 roots, and preserves
   the appropriate joint resource intercept. The central clipped-window
   checker and both exterior tails are specified in `ABGeneralCountPort`,
   `ABEmptyCentralPort` and `Mixed.ABWindowCountPacket.completeHalfline`.
3. Three new-q support/moment stages. `ABNewAllowanceLicense` starts at the
   exact old-stage cap packet. Its chronological `step_sound` takes the
   same-law24 bounds and the previous stage's actual-law cap evidence.
   `final_valid` consumes these inputs at every stage. No future improved
   radius is used to justify an earlier24 calculation.
4. A post-context whose initial cap packet equals the final new-q packet,
   with a source-licensed `refinement` proving all its original-contact
   hypotheses. This includes the full retained resource/cfg statements,
   not only a list of improved radii.
5. A checked ordinary25 **complete closed subtree of that ancestor**, with
   output below C_E. `ScopedCountPayload` contains both children of each
   strict split and entries exactly matching all leaves. Its fixed
   `ScopedCountMeaning` quantifies arbitrary laws and signed point scores
   under the frozen post-context. A checked payload plus the original
   contact equality yields `scoped_count_score_bound`; the actual critical
   lower bound gives the exclusion.

The final step needs the complete count5 subtree, not an unrelated theorem
on the full26-root original domain. For source A, three direct descendants
and two complete subtrees cover the original ancestor (15 terminal cells).
For B, the source uses a different original ancestor and a44-split,
45-terminal tree with89 direct ordinary25 calls. These action counts do not
replace the full tree/leaf meaning, and A's acquired cap is not a premise
of B.

For a ray radius R, the required predecessor halfline is

```
y>=R:  H25-y <= original.H.upper-R,
y<=-R: H25-y >= original.H.lower+R.
```

If U bounds the positive closed24 point score on that entire halfline, then

```
q_R=25*max(U-CE_LO,0),
25*max(c24_positive_closed(H25-y)-C25,0)<=q_R.
```

`ABNewAllowanceLicense.ray_allowance` derives this from actual H membership,
the ray and `CE_LO<=C_E<=C25`. U is the **returned quantitative upper**,
including both exterior tails; it may exceed a native early-exit target.
The allowance is constant during the ray derivative argument.

The source contact replacement has the explicit affine form

```
old=lineUpper+cubicTerm+rhoScale*(5/16),
new=lineUpper+cubicTerm+rhoScale*q_R
   =old+rhoScale*(q_R-5/16).
```

`ray_contact_replacement` proves this identity. Source ray-contraction
rules retain the whole Gaussian/contact upper and their six strict
derivative/contact gates; one cannot subtract an improvement from an opaque
upper without its affine decomposition. The accepted new-stage source
consequences must supply the actual `step_sound` evidence.

## 6. Finite reference dependencies and exact admission

`SemanticRegistry` has finitely many indexed entries, unique reference IDs,
an explicit premise list and a proof that every premise has smaller rank.
Its `acquire` builder takes the semantic acquisitions of those earlier
premises. `SemanticRegistry.acquired` constructs each acquisition by
well-founded recursion. A cyclic declared dependency is unrepresentable.

Lean does not infer a source program's omitted dependencies. Completeness
of the source-to-manifest mapping is an explicit accepted source-traceability
obligation. `SourceManifest` freezes every complete reference specification,
the exact ID dependency lists and the mathematical rule kind. Given that
approved manifest, `OriginalP25Admission` requires a bijection of entries,
equality of every entire specification, exact dependency lists and matching
rule kinds. Thus equal family counts alone are not admission.

`OriginalP25Cardinalities` separately records the historical sanity checks:
A1/B1/C2/D92/F32 and45 p25 D entries (128 admitted statements). Every admitted
entry, used or unused, must have a semantic acquisition through the builder.
`SelectedUse`, `OriginalP25SelectedUsage` and `SelectedDShape` separately
describe the chosen76 leaf-reference occurrences: A1/B1/C0/D18/F56, with
seven distinct F references. They do not shrink the admitted library.

## 7. Source pins, trust and remaining evidence

The source-scoped statements were read from the tracked research audit and
its pinned originals. The audit is a fallible internal review; the exact
accepted mathematical rules are the records above and the corresponding
source definitions. Useful source anchors include:

| Component | Original member under `cutoff25_20261013/` | SHA-256 |
|---|---|---|
| Exact original-cfg/count/full-box matching | `root/sparse_local_acquisition_v1/matching.py` | `5ffd5aa4f52cb7772b59d9d77376e80747e04bb8eca0bf53c35d2865e5c7d278` |
| E / finished-prefix scalar | `low/pointwise_inward_defect_v2/pointwise_inward_v2.py` | `9c8b78578dcdef7863dc933bc142eb2c9b1b4f5e29fd49cca7497a2f4a4fbde3` |
| Finished-prefix exact export mapping | `archive_audit/pointwise_finished_prefix_v1/interface.py` | `4db0d6809f4f474a74003a57c43711dd206c311a784c08c8383c6dc6ccd5b0ad` |
| Native prefix projection | `archive_audit/normalized_defect_frontier_v1/prefix_project.py` | `81d9fd91592c2ffd524bbef49a58153b832d4c242d8e52d7cf177d9f70225153` |
| A old/new-q scalar induction | `archive_audit/b5_sparse_halfline_review_v1/check_scalar_v2.py` | `b48c21f1e988b2df51909818dfbf4a8d2bc130d07d37cc6cdb6eb8b42852e7bf` |

The archive SHA-256 is
`a97f3e6e50e428df0893304bcd2f746851c9fccef2079b1ec66be9ab909d7f2c`.
The complete source map records the other C/D/F, A/B24 and ordinary25 members.
See the pinned [reference audit](https://github.com/rodziewiczk/berry-esseen-end2end/blob/6ca9730273c81447be4863824c0b7d012db0e8b8/proof/code_n25_p25_references_audit.md)
and [source map](https://github.com/rodziewiczk/berry-esseen-end2end/blob/6ca9730273c81447be4863824c0b7d012db0e8b8/proof/code_n25_p25_references_source_map.json).

At this milestone the analytic/source implications are explicit accepted
inputs. Numerical checker soundness, complete leaf arithmetic and exact
approved manifest data must still be supplied. A canonical selected native
capsule is missing from the available original source material; its byte
content, full numeric manifest and fresh arithmetic cannot be reconstructed
from receipt counts, capture hashes or saved PASS strings. No populated
`OriginalP25Admission` or unconditional B5 result is claimed here.

This remaining source/evidence frontier is distinct from the now specified
mathematical lookup contract. An implementation can decode frozen contexts,
preserve the two scope kinds, build finite licensed refinements, verify whole
closed numerical leaves and produce exactly the rule-specific acquisition
objects. It does not have to decide whether C/F are phase-free, whether D
keeps its root/phase, whether AB is merely a ray allowance, or whether a
partial overlap suffices: those choices are fixed by the types and rules.
