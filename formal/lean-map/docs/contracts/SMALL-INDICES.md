# Small-index polynomial families: exact certificate meanings

The n2 and n3 families share an overall majorant argument, but do not share
the same feature basis, coefficient normalization, moment cap, positivity
geometry or threshold data. A common implementation must preserve these
differences explicitly.

Lean: [`SmallIndices.lean`](../../BEMap/SmallIndices.lean).
Sources: manuscript `n2:eq:tensor`, `n2:eq:expect`, `n2:eq:C1`, `n2:eq:C2`,
`n3:eq:features`, `n3:eq:majorant`, `n3:eq:expect`, `n3:prop:certificate`.

## 1. N2 tensor family

The five single-coordinate features and their actual means are

```
v=(1,y,y²,y³,|y|³), mu=(1,0,1,gamma,rho).
```

For each sorted pair0<=i<=j<=4, a diagonal basis term is v_i(u)v_i(v).
An off-diagonal term is the **sum**
`v_i(u)v_j(v)+v_j(u)v_i(v)`, without averaging. Therefore its expectation
is2 mu_i mu_j. There are exactly15 coefficients per row,1050 in70 rows.
The certificate model fixes the pointwise majorant and expectation polynomial
from these definitions; a supplied power expansion is not the semantic target.

The row j=0,...,69 has the derived raw threshold endpoints
`a_j=-5/2+j/20`, `b_j=a_j+1/20`. Its obligations are

```
M_j(u,v) >=1_{u+v<=b_j}                  on [-6,6]²,
q_j(gamma,rho) <=Phi(a_j/sqrt(2))+2rho/7  on D2,
D2: |gamma|<=2, 1<=rho<=2,
    rho²(gamma²+4)-(gamma²+2)²>=0.
```

The complete70-row grid covers[-5/2,1]. The analytic certificate implication
also uses the two exterior raw-threshold tails and whole-law reflection.
The small-rho bounded-law conclusion is R2(P)<=2sqrt(2)/7. The large-rho
structural complement and unrestricted-witness localization are separate
analytic inputs; the polynomial checker alone is not an all-law theorem.

The pointwise checker splits four sign quadrants and both **closed** event
half-planes, triangulates each resulting rational polygon, and checks the
degree6 triangular Bernstein expansion. All28 basis coefficients on a
triangle must be nonnegative, or the complete subdivision must certify it.
The event plane belongs to the included side; testing a finite point sample
is insufficient. The scalar moment-domain checker uses degree2 tensor
Bernstein on(gamma,rho) rectangles. A rectangle is omitted only by the
strict, proved outside-domain inequality in the source, never by uncertainty.

## 2. N3 independence-null family

The seven single-coordinate features are

```
v=(1,y,y²-1,y³,|y|³,y⁴,y⁵).
```

Admissible triples0<=i<=j<=k<=6 either have k<5 or contain at least one1
or2. There are exactly59. For each triple, the basis is the **average over
distinct permutations**, with divisor1,3 or6 according to multiplicity.
It is not the unnormalized sum used by n2 off-diagonal pairs.

Features1 and2 have mean zero. Independence kills any admissible term
containing them, including all terms with features5 or6. Only the ten
triples using0,3,4 survive in the expectation. This does **not** assert
EX⁴=0 or EX⁵=0. The source's49 null terms reshape the pointwise polynomial
without introducing unknown fourth/fifth-moment parameters into q(gamma,rho).

The payload has111 threshold intervals and59 coefficients per interval.
The intervals are explicit data with ordered endpoints, first endpoint-7/2,
last endpoint3/2 and exact equality at every adjacent seam. Do not impose
the n2 uniform-grid formula on them. The semantic obligations are

```
M_j(u,v,w) >=1_{u+v+w<=b_j}                  on [-7,7]³,
q_j(gamma,rho) <=Phi(a_j/sqrt(3))+(59/250)rho on D3,
D3: |gamma|<=15/8, 1<=rho<=15/8,
    rho²(gamma²+4)-(gamma²+2)²>=0.
```

The certificate cube is[-7,7]³, deliberately larger than the localized
witness support(-6,6). The accepted analytic implication includes the two
exterior threshold tails and whole-law reflection. Its output is the weak
quantitative bound R3(P)<=59sqrt(3)/250 for the bounded small-rho class.
Large rho has its separate structural rule.

On a sign box, the polynomial has degree at most5 in each coordinate.
The tensor Bernstein array therefore has6³=216 coefficients. Symmetry may
restrict to the ordered chamber u<=v<=w, but a box is discarded for ordering
only when a strict endpoint reversal proves that chamber empty. A half-space
test uses the source's signed affine slope: ell<=0 on the included side,
ell>=0 on the other side. At a zero half-space coefficient the base target
must be met directly. Every unresolved box is fully subdivided or rejected.
The scalar moment-domain checker uses degree3 tensor Bernstein.

## 3. Decoder and arithmetic obligations

The source vectors are indexed in **lexicographic order of the sorted
tuples**, not by the incidental enumeration of a Lean Fintype. The explicit
`tensorCoefficientKeys2` and `nullCoefficientKeys3` lists fix this mapping;
their lengths15 and59 are kernel-checked. A decoder binds slot k to the kth
canonical tuple, checks exact lengths and rejects malformed rational input.
Equivalent explicit key maps are acceptable only when they prove the same
coefficient function. Silently using a different tuple order changes M and q.

Rational Gaussian lower bounds must enclose the actual CDF in each moment
inequality. The two source series have different normalizations:

```
Phi(t/sqrt(2))=1/2+[1/(2sqrt(pi))]
              sum_k (-1)^k t^(2k+1)/[4^k k!(2k+1)],
Phi(t/sqrt(3))=1/2+[1/sqrt(6pi)]
              sum_k (-1)^k t^(2k+1)/[6^k k!(2k+1)].
```

Their chosen truncations, argument domains, positive radical bounds and
outward directions belong to the selected exact evaluator. A floating CDF
call, a positive value at the midpoint or a historical PASS is not the
semantic inequality. Geometry and coefficients alone also do not certify
every subdivision the source checker may perform.

## 4. Boundary of this skeleton

`TensorCertificateMeaning2` and `NullCertificateMeaning3` give exact
mathematical output predicates. `SmallCertificateImplications` records the
accepted analytic majorant-to-probability implications. The constructors
in `Assembly.SmallPolynomialProvider` consume these objects together with
source-exact localization and large-rho inputs.

No full Bernstein evaluator, Gaussian arithmetic implementation or replay
of the70/111 archived certificates is claimed here. This is an implementation
contract with concrete algebraic meaning, not an announcement of fresh
numerical acceptance or a full Lean formalization of the analytic proof.
