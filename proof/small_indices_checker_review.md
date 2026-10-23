# Source review of the completed n2/n3 finite checkers

Review date: 23 October 2026.

**Scoped conclusion:** no blocking mathematical or implementation defect was
identified in the reviewed acceptance paths for the n2 and n3 finite
certificates. Their parser, polynomial construction, continuous-domain
positivity tests, endpoint conventions, and exact scalar enclosures implement
the finite obligations stated in the reviewed manuscript. This conclusion is a
source-level mathematical review under ordinary faithful Python, compiler,
Boost-integer, operating-system, and hardware execution assumptions. It is not
formal verification or an independent implementation of the full n3 checker.

The review read the complete five checker sources below, the execution wrapper,
the manuscript's finite-certificate definitions, the scoped analytic review,
and the observed notebook08 record. It reran only the source-inventory hash
check. It did not rerun scalar, polynomial, C++, or full-certificate producers,
modify the sources, or change the proof graph.

## Exact reviewed source epoch

The original source commit is
`75a94708872e2bc053f42a279559b23ed91e4402`. All 189 manifested files in
`vendor/n2_n3_75a9470`, including all 70 n2 and 111 n3 certificate cells,
passed the existing inventory check during this review. The inventory itself
has SHA-256
`8ca0f5c30991b50c61fc998c7c873873c2ac7d2bde6611123ce74651e1a3c26b`.

| Source beneath `vendor/n2_n3_75a9470` | SHA-256 |
| --- | --- |
| `n2/tensor_certificate.py` | `f94746d16bb004da27778a51343dfc8b72e6d505a1fb2f9150e0f6391b7dbfc8` |
| `n2/independent_integer_check.py` | `5f109259f9ade7ac18576bab7f15075ed367c004f1fad732dd4b43eb2ce7f7f0` |
| `n3/verify.py` | `73002b7630faf496df86cfacb74c9c9b35a2db801dd40cbc8df8de0dd3725cef` |
| `n3/check_cube.cpp` | `ce5e57927f97ae1142410e933c7f2133a30938a96496beaeb8e48c1b29b973cb` |
| `n3/audit_initial_polynomials.py` | `9d5e767f1522dd42d4f07e96b5b4e3879daae28cc3fc6e23cdcab3b6727c3c5b` |

The manuscript reference is `berry_esseen_manuscript.tex`, SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
Its n2 formulas and checker description are at lines 4956–5109; the corresponding
n3 material is at lines 5269–5485. The analytic passage to these finite
obligations is reviewed separately in
[small_indices_analytic_review.md](small_indices_analytic_review.md).

## n2: parser, basis, and full threshold coverage

Both n2 parsers require the exact schema, format, integer cell index, prescribed
threshold endpoints, and 15 canonical rational strings. Duplicate JSON keys and
nonfinite JSON constants are rejected. The complete acceptance path requires
exactly `000.json` through `069.json`. The primary checker's global command
rejects a partial range; the independent checker labels a requested partial
range `PARTIAL_INTEGER_CHECK_ONLY`.

The native n2 parsers do not themselves bind every input file to a hash or reject
every possible file symlink. For this observed source epoch, the outer inventory
check supplies that binding: it rejects symlinks and missing/extra files, hashes
every source and cell, and runs before and after each selected stage. This is a
reviewed division of responsibility, not an omitted mathematical inequality.

`tensor_poly` and the independent `polynomial` implement the manuscript's
lexicographic pairs in the five features `(1,y,y²,y³,|y|³)`. Off-diagonal terms
are sums of two products, not averages. Their expectation routines accordingly
use means `(1,0,1,gamma,rho)` and multiply off-diagonal contributions by two.
On a sign quadrant, `|y|³ = sign(y)y³`; the resulting polynomial has degree at
most three in either variable and total degree at most six.

The 70 prescribed intervals are
`[-5/2+j/20, -5/2+(j+1)/20]`. Each pointwise check uses the upper endpoint,
while each Gaussian/moment check uses the lower endpoint. Thus their monotone
threshold implication covers every threshold in `[-5/2,1]`, including shared
endpoints. The exact scalar checks supply Cantelli's `8/33 < 2/7` left tail and
`Phi(1/sqrt(2)) > 5/7` right tail. Reflection is the analytic closed-CDF/left-limit
argument already recorded in the analytic review; the code assumes no generic
absence of atoms or sum collisions.

## n2: complete pointwise positivity

The primary code's `clip` and `triangles` (lines 61–87) intersect all four closed
quadrants with both closed event half-planes. Nondegenerate convex pieces are
covered by a fan of triangles. On the included side the polynomial is `M-1`;
on the other side it is `M`. Checking the included side on its closure enforces
the event-plane value at least one.

Zero-area triangles are omitted. This does not remove an event-plane exception:
every selected upper threshold lies strictly between the global square extrema
`-12` and `12`. The included half-space therefore has interior, and every point
of its intersection with the square is a limit of such points. The piecewise
polynomial is continuous across the sign axes. Any isolated or lower-dimensional
quadrant intersection, including the origin at threshold zero, inherits the
required bound from adjacent nondegenerate included pieces.

For the primary triangle conversion (lines 89–97), a transformed monomial
`s^a t^b` contributes to the barycentric degree-six coefficient with indices
`(k,i,j)` by

```text
binom(i,a) binom(j,b) / [binom(6,a+b) binom(a+b,a)].
```

This is the correct degree elevation factor. Nonnegative coefficients imply
nonnegativity throughout the closed triangle. The index permutation and the
two sums in `tri_split` are the exact midpoint de Casteljau identities for
vertices `(a, midpoint, c)` and `(midpoint, b, c)`. Both children are retained.
The longest-edge choice changes efficiency, not coverage. A negative vertex or
an unresolved depth/node limit rejects; a finite sample never accepts a cell.

The second checker independently rebuilds the polynomial on every child
triangle (lines 39–117). If `D_c` clears coefficient denominators and `D_v`
clears vertex denominators, it expands the homogeneous degree-six integer form

```text
sum (D_c c_ab) D_v^(6-a-b) U^a V^b (lambda0+lambda1+lambda2)^(6-a-b).
```

All discarded denominator and multinomial factors are positive. Consequently
its nonnegative homogeneous coefficients give the same valid positivity
criterion without using the first checker's subdivision formula. The exponent
ranges cover every possible term. Integer conversion is exact because the
denominators were cleared by least common multiples. It independently clips
both closed half-planes and retains both child triangles.

## Moment-domain and Gaussian checks

For both indices the scalar expectation is reconstructed from the feature
coefficients. No supplied expectation expansion is trusted. The n2 scalar has
degree at most two; n3 has degree at most three. Their rectangle conversions use
the corresponding exact tensor Bernstein bases. Acceptance occurs only when
all resulting lower-bound coefficients are nonnegative.

For `z = gamma²` write `h(z,rho) = rho²(z+4)-(z+2)²`. On the checked rectangles,
`rho <= 2`, so

```text
partial h / partial z = rho² - 2z - 4 <= 0,
partial h / partial rho = 2rho(z+4) > 0.
```

The rectangle discard value at its smallest possible `gamma²` and largest
`rho` is therefore a genuine maximum. Only a strictly negative maximum causes
discard; the admissible `h=0` boundary remains covered. The rectangles are outer
domains, so not using the additional restriction `|gamma|<=rho` only enlarges
the required check. Failed Bernstein tests subdivide both closed children.
All unresolved limits reject. The primary n2 checker's sampled feasible points
are used only to find a rejecting counterexample, never to accept positivity.

The Gaussian routines use Machin's arctangent identity, alternating rational
series, and integer-square-root brackets. The n2 factor is `1/(2sqrt(pi))` and
the integrand series is for `exp(-u²/4)`; the n3 factor is `1/sqrt(6pi)` and its
series is for `exp(-u²/6)`. These agree with the required normalizations.
All acceptance callers are within the declared ranges: `|t|<=5/2` for n2 and
`|t|<=4` for n3. The integral terms decrease in these ranges, so the selected
odd/even truncations bound the integral. Negative arguments use the correct
reversed bounds after reflection around `1/2`.

The independent n2 checker uses independently enclosed rational prefactors and
different truncation orders. The scalar support-polynomial shifts, structural
comparisons, tail comparisons, and strict target-versus-Esseen comparisons
match the analytic obligations and use exact rational arithmetic. No library
Gaussian CDF or floating-point decision enters any acceptance path. The n2
NumPy/SciPy code belongs solely to the untrusted `generate` branch.

## n3: feature reconstruction and coverage

The Python front end (lines 13–78) constructs exactly the 59 permitted
nondecreasing feature triples and averages over their distinct permutations.
The centered feature is `y²-1`, and indices 5 and 6 correctly represent `y⁴`
and `y⁵`. Every allowed higher-feature term also has a mean-zero factor in
another coordinate. After the independently established bounded-support
reduction, integrability is automatic; independence removes these terms.
`expectation` retains precisely the triples using only indices 0, 3, and 4,
with no spurious permutation multiplicity.

`load_records` (lines 145–159) rejects duplicate keys, unexpected schema fields,
noncanonical rationals, symlinks and non-JSON entries. It sorts strictly
nonempty intervals and requires consecutive coverage from `-7/2` to `3/2`.
That parser can mathematically accept another complete valid partition; it
does not itself require the historical filenames or exactly 111 records.
For notebook08, the frozen inventory and complete output census additionally
bind exactly the supplied 111 cells and their individual raw SHA-256 values.

The power-to-Bernstein transform is exact for degree five in each coordinate
on the four declared sign boxes. Its conversion denominator divides ten on
each axis; multiplying all three axes by ten explains the exported common
factor 1000. The index order agrees with C++ `id(i,j,k)=36i+6j+k`. Each C++
binary is compiled afresh and receives a freshly exported input per cell.

## n3: affine event-plane test and integer kernel

The C++ checker covers the four sign patterns of an ordered triple. Full
coordinate symmetry of the reconstructed majorant and of the sum event makes
this sufficient. Its discard condition uses strict `lower[i] > upper[j]` for
some `i<j`; such a box contains no ordered point. Equality and all shared faces
remain. All accepted bounds apply to the entire remaining box, a safe
enlargement of its ordered portion.

Let `s` be the Bernstein controls of `x1+x2+x3-t`, up to a positive common
scale. `affine_test` (C++ lines 48–75) intersects the exact constraints
`b_i-target >= slope*s_i`. A negative `s_i` gives a lower slope bound, a positive
one gives an upper bound, and zero requires the target directly. Its sign
restriction is correct:

- `slope<=0`, `target=1` proves `M>=1` on the included half-space;
- `slope>=0`, `target=0` proves `M>=0` on the other closed half-space.

The code accepts a whole included box only when `sum_upper<=t`, and accepts a
whole outside box only when `sum_lower>t`. Otherwise both required half-space
bounds must hold. Thus a face with `sum_lower=t` cannot be accidentally treated
as wholly outside, and the included event plane is always charged at least one.

`divide` (lines 79–105) implements the degree-five midpoint identities and
multiplies the common denominator by 32. Dyadic coordinates follow the same
closed child boxes. All coefficient arithmetic and rational comparisons use
Boost `cpp_int`. The remaining native integer coordinates are safely bounded:
before coordinate arithmetic the maximum level is at most 35, each coordinate
endpoint has magnitude at most `7*2^35`, and even a loose bound for the
intermediate five-times-sum expression is below `2^43`. These are far below
signed 64-bit overflow. Threshold products use arbitrary-size integers; slope
coordinates are range-checked before conversion, excluding `LLONG_MIN` before
its negation. The small binomial/shift factors are also within native range.
Depth, node, dyadic-level, malformed-input and extra-data errors reject.

The additional identity audit independently evaluates the original features at
the complete six-by-six-by-six tensor grid in each sign box. Its integer
scalings agree with the Bernstein evaluation: three feature denominators
`5^5` give `5^15`, and the coefficient common denominator is multiplied by six
to clear all distinct-permutation averages. Equality at these nodes proves a
polynomial identity because the separate degree is at most five. It does not
independently recheck positivity or constitute a second full n3 implementation.

## Connection to the actual notebook08 run

[observed_runs.md](observed_runs.md) identifies the inspected result ZIP by
SHA-256 `77b7750b3e6cb124a0622f906034dca8dec500aed07c8a70596c747285736e2b`.
It records all six stages completed, including both full n2 checkers, the
95,904 n3 identity checks, and fresh compilation plus the full 111-cell n3 run.
The recorded source-inventory pin is the same pin reviewed here. The complete
markers and ordered cell census agree with the selected finite obligations.

This source review supplies the previously separate implementation readback;
the observed run supplies the computation, which was not repeated here. BASIC
execution labels describe the available containment contract. They are not a
counterexample to any of the exact mathematical checks reviewed above, and this
review finds no reason to rerun notebook08 solely to change those labels.
The saved native/global acceptance fields remain unchanged.

## Remaining boundary

The review did not formally verify Python/Fraction, Boost, the C++ compiler, or
the machine execution. It did not independently re-execute every leaf, audit
untrusted candidate construction, or supply a second full n3 implementation.
Its analytic input is the separate scoped reduction review; the external
structural theorem and any final all-law composition retain their own stated
review scope. It makes no claim about n4 or later indices.

Under the reviewed finite-certificate implications and ordinary faithful
execution assumptions, the observed complete calculations provide the required
finite inequalities for the stated n2 and n3 bounds. No additional mathematical
or implementation blocker was found in these acceptance paths. This note
records that scoped result; it does not create a new run or alter graph status.
