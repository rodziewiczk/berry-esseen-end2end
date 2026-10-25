# 3. Complete covers and method-specific rules

This document specifies geometric coverage and method dispatch. The relevant
Lean declarations are in `BEMap/Covers.lean` and `BEMap/Certificates.lean`.
The statements are expressed over real parameters with exact rational cuts.
No floating-point grid or finite sample is a cover of a continuous domain.

Status terminology used here:

* **Structural theorem:** the stated coverage/composition is proved in Lean.
* **Accepted analytic premise:** a precise theorem from the mathematical
  argument, supplied at this formal interface; it is not reproved here.
* **Numerical evidence pending connection:** exact/interval evidence must be
  connected through the soundness interface described in part 4.
* **Specification gap / BLOCK:** a required mathematical statement or semantic
  connection is absent. It must be resolved before the affected computation
  can instantiate its intended conclusion. This label is not used merely
  because an accepted analytic theorem is a parameter rather than a Lean proof.

## 3.1 Semantic scope of a region

A region is a necessary parameter domain for one actual oriented law. Its
membership does not assert that every point in that domain is realizable by a
law. In the n5/n25 maps, `rho` means E|X|³ and `beta` means E[X|X|]. Neither
signed beta nor the actual law is silently reflected when a row changes.

The cover has the following logical form:

```
actual law satisfies the accepted moment envelope
    -> its actual parameters belong to at least one listed closed region
    -> the exclusion rule for that region applies to the same law/contact.
```

The last implication is a separate method-specific proof. A region count or a
successful domain-union proof does not provide that exclusion.

All shared endpoints are included in both adjacent closed pieces. An equality
case may be handled by either applicable proof, but must not be lost by both.

## 3.2 The complete n=5 domain

`BetaEnvelope5 rho beta` is the accepted analytic/scalar premise

```
rho <= 237/200 -> -b2 <= beta <= b2,
rho <= 6/5     -> -b3 <= beta <= b3,
b2 = 84729828287999/250000000000000,
b3 = 35139006743001/100000000000000.
```

The moment theorem is `rho >= (1+beta²)/sqrt(1-beta²)`, with |beta|<1.
Its endpoint specialization uses the outward scalar enclosures at 237/200
and 6/5. The exact positive polynomial tests are now proved by
`betaFive2_endpoint_certificate`, `betaFive3_endpoint_certificate` and
`betaFive_enclosures_positive`. The general moment theorem and its signed-beta
inference remain accepted analytic inputs. `BetaEnvelope5` states exactly the
consequences needed by the region union. It does not assert any signed
restriction in the first two rows.

| `LowRegion5` | Closed rho interval | Closed beta interval | Required method |
|---|---|---|---|
| `b0` | [1,11/10] | All necessary beta values | Resource acquisition / COUNT |
| `bn` | [11/10,23/20] | All necessary beta values | Resource acquisition / COUNT |
| `b2s0` | [23/20,467/400] | [-b2,1/5] | Resource acquisition / COUNT |
| `b2s1` | [23/20,467/400] | [1/5,b2] | Resource acquisition / COUNT |
| `b2s2` | [467/400,237/200] | [-b2,1/5] | Resource acquisition / COUNT |
| `b2s3` | [467/400,237/200] | [1/5,b2] | Resource acquisition / COUNT |
| `b3s0` | [237/200,477/400] | [-b3,1/5] | Resource acquisition / COUNT |
| `b3t0` | [237/200,477/400] | [1/5,3/10] | Resource acquisition / COUNT |
| `b3t1` | [237/200,477/400] | [3/10,b3] | Resource acquisition / COUNT |
| `b3s2` | [477/400,6/5] | [-b3,1/5] | Resource acquisition / COUNT |
| `b3t2` | [477/400,6/5] | [1/5,3/10] | Resource acquisition / COUNT |
| `b3lower` | [477/400,6/5] | [3/10,17/50] | Resource acquisition / COUNT |
| `corner` | [477/400,6/5] | [17/50,b3] | Separate support-free gap-free argument |

“Resource acquisition / COUNT” is a workflow name, not a premise that the law
already has a central support gap. A gap used by a later count rule must be
acquired for the same law. The `corner` method is deliberately distinct: its
initial assumptions do not include an acquired support radius or support gap.
The boundary beta=17/50 is present in both `b3lower` and `corner`.

The rest of the finite rho domain uses the following separate Fourier rules:

| `FourierBand5` | Closed rho interval | Required acquired support radius |
|---|---|---|
| `f0` | [6/5,5/4] | 13/5 |
| `f1` | [5/4,7/5] | 117/40 |
| `f2` | [7/5,3/2] | 25/8 |
| `f3` | [3/2,8/5] | 133/40 |
| `f4` | [8/5,17/10] | 7/2 |
| `f5` | [17/10,7361/4000] | 15/4 |

For each Fourier rule the support-acquisition implication is an incoming
obligation. The complete Fourier/smoothing bound must include its endpoint
pieces and infinite frequency tail, with the bound relation specified by the
selected source rule at 4097/10000. A finite
frequency-window estimate alone is not this rule.

The remaining `Region5.tail` is the inclusive domain rho>=7361/4000. The
accepted universal all-law theorem supplies

```
R_5(P) <= (3031/10000)(1 + (323/500)/rho).
```

`universalFiveTailEnvelope_antitone` and `n5_tail_envelope_bound` prove its
monotone endpoint bound by 819/2000 on the inclusive ray. The exact comparison
819/2000<4097/10000 is proved by `n5_tail_target_gap`; the C_E comparison belongs
to the constant interface. These are separate scalar/analytic obligations,
not outputs of the COUNT cover.

**Structural theorems:** `n5_cover`, `fourier5_cover`,
`n5_region_inventory`, `lowRegions5_complete`, `fourierBands5_complete`.
The inventory is 13 low + 6 Fourier + 1 tail = 20 pieces. `Region5.method` maps the
corner to its own constructor, and records the exact Fourier radius for every
Fourier band. `n5_resource_region_count` proves the 12 resource rows, and
`n5_corner_seam` explicitly retains beta=17/50 in both adjacent methods.
`n5_exclude_by_cover` composes all region rejections for the same witness.

## 3.3 Floor31 bands and actual-index transfer

`floor31_cover` proves the closed union with endpoints

```
1, 11/10, 6/5, 13/10, 7/5, 3/2, 33/20, 7/4, 7361/4000.
```

`floor31_band_count` proves that there are exactly 8 adjacent bands. The theorem
is a rho-domain cover, not a transfer theorem to indices 32,33,34.

An actual-index transfer must retain all of the following:

* the same oriented marginal law;
* actual index m in support, count probabilities and normalized thresholds;
* the weighted inequality mD<=31d, with physical D;
* actual m-weighted noise and the correct phase scaling;
* the entire resource transcript being exported.

It must not replace mD<=31d by D<=d and then manufacture a bound by multiplying
the latter by31. A contact at31 is not supplied to a transferred law at m, or
conversely, unless an independent contact theorem proves it.

## 3.4 The original COUNT products

`CountPoint n` has precisely the following scalar coordinates:

| Field | Intended meaning when realized by a physical state |
|---|---|
| `root : Fin(n+1)` | Original count k, including 0 and n |
| `p` | P(X>0), with a zero atom in the nonpositive class |
| `lambda` | n E U², not E U² |
| `alpha` | Conditional-variance allocation in [0,1] |
| `phase` | u=np+hH-k for the raw threshold H and inverse scale h |
| `rawInward0` | The raw nonpositive residual endpoint a0=p-hA; not the total d_Y=a0+a1 |

The last coordinate is **a0**, not d_Y. The acquired resource supplies
`a0+a1=d_Y<=d0`, so a0 lies in[0,d0] because a1>=0.
`OriginalCountDomain.totalInwardCap` names this total d0 cap; it does not
change the coordinate in the root product into a sum.

The geometric type intentionally allows relaxed points. A typed physical
realization must prove every coordinate equality before a numerical leaf
statement is applied to the law. Box membership alone supplies no such
realization and no new probability law.

`OriginalCountDomain n` requires a closed rational p interval inside [0,1],
Lambda>=0 and d0>=0. Its root product for **each** k=0,...,n is

```
[p_lower,p_upper] x [0,Lambda] x [0,1] x [-1/2,1/2] x [0,d0].
```

The five axes are `probability`, `weightedNoise`, `alpha`, `phase`, `rawInward0`.
The count index is a separate discrete field and does not get merged with an
axis. A `CountBox` includes its root; membership proves exact root equality.
Every necessary-condition contraction is justified inside these original
products. A certificate cannot silently substitute only a contracted domain
for the original root domain that its conclusion claims to cover.

## 3.5 Finite trees, zero faces and equality seams

`StrictBoxCut box axis` requires lower<cut<upper over exact rationals.
`CountTree.split` then requires **both** closed children as constructor
arguments. The left child ends at the cut; the right child begins there.
`CountBox.split_cover` and `CountTree.cover` prove the union inductively.

The consequences are fixed by the interface:

* A singleton coordinate interval is a valid leaf; it is not cut at an
  endpoint. A missing child is not a complete tree.
* Lambda=0, alpha=0/1, raw a0=0, closed phase endpoints and cut equality remain
  part of the geometric cover. Zero-variance methods need their deterministic
  probability rule rather than division by variance.
* A failed denominator or method guard cannot prune its cell. It returns no
  proof for that method, and another sound method or further split is needed.
* `CompleteCountForest.roots` is a function over `Fin(n+1)`, so every original
  root is mandatory. `toLeafCover` proves the complete original-product union.
* A geometric leaf is not an accepted numerical leaf. Acceptance additionally
  needs the applicable method's full mathematical bound or contradiction.

`CountLeafCover.conclude` composes any sound per-leaf mathematical statement
for the **same** point, after original-product membership is proved.

## 3.6 Nearest-count confinement and the exterior thresholds

Let z=np+hH. `PhaseConfinement n z` is the exact conjunction

```
-1/2 <= z <= n + 1/2.
```

`nearest_root_exists` proves that a confined z has some k in 0,...,n with
u=z-k in [-1/2,1/2]. The proof includes ties and all boundary points. It makes
no claim about thresholds outside that interval.

`ThresholdLocation` and `threshold_locations_complete` separate three cases:

1. Central confined threshold, handled by the original finite roots.
2. Strict left ray z<-1/2, requiring its separately stated tail rule.
3. Strict right ray z>n+1/2, requiring its separately stated tail rule.

An execution may omit the tail rules only if its acquired state proves
confinement for every allowed threshold. It may not infer confinement from
the use of nearest-count notation. Raw H, normalized H/sqrt(n), and u have
different meanings and must be connected through the explicit coordinate
equalities in the physical state.

## 3.7 Required separate argument families

| Family | Mandatory incoming semantic evidence | Output required |
|---|---|---|
| Ordinary COUNT | Same-law acquired support/resources, count-mixture identity, actual coordinate realization, complete original forest and valid leaf methods | The explicitly configured weak or strict numerical bound for the same positive closed discrepancy |
| Gap-free corner | Its signed-moment/rho domain and its own complete threshold/event comparison | Its stated bound without assuming an acquired support gap/radius |
| Supported Fourier | Exact band, independently acquired required radius, valid complete Fourier/smoothing evidence | Its stated bound with all frequency and threshold tails retained |
| Universal rho tail | All-law analytic inequality and exact endpoint/monotonic scalar proof | Its stated bound on the inclusive unbounded rho ray |
| Mixed predecessor | Same law at both indices, correct weighted transfers and complete phases at the transferred index | The stated inequality for the current-index law; no borrowed predecessor contact |
| Zero noise | Proven zero residual variance and deterministic/Bernoulli rule | Bound or exclusion covering that face |
| Positive noise | Strict positivity and all positivity gates required by the local comparison | The stated local inequality with its strict margin |

This table is a dispatch contract, not a statement that a single proof may be
substituted for all methods. The method-specific evidence records in the
state/transition layer must retain these distinct prerequisites.

Source: manuscript sections around labels `five:eq:benclosures`,
`countcore:representation`, `countcore:forest`, `rescore:re-exports` and the
floor31 finite-index reduction; manuscript and repository pins are recorded in
`provenance.json` and the main mathematical contract document.
