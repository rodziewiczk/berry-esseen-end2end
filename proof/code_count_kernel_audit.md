# Selected n25 count kernels: source-to-lemma audit

Date: 23 October 2026. Method: read source bytes, manifests, contracts,
JSON and ASTs, and independently derive the formulas described below.
No archived module was imported or executed. No leaf, producer, native
acceptor, numerical integration or mathematical search was run locally.

## Bounded verdict

No concrete counterexample or numerical-soundness defect was found in the
bounded families reviewed here. A small family can now be identified
precisely: the shared theta/mean/allocation domain contractions and their
monotonicity-gated beta/allocation corners were checked against the
manuscript formulas, including their wrapper's zero-noise routing and
retention of the original joint-plane intercept.

The review also checked the outgoing quartic coefficient generator,
its SOS and fixed-peak normalizations, the directed Bernstein transform,
the common-cubic polygon/normalization construction, and the principal
common-cubic/AM--GM and finite-allocation stop-loss assembly. These are
conditional component conclusions, not a declaration that every complete
count kernel or source-specific wrapper is mathematically verified.

The enabled paths not exhaustively reviewed are listed at the end.
In particular, the V14 local contact/support/rho preprocessing cannot be
certified merely because its final call uses the reviewed V12 count
components. Fresh numerical completion, parent acquisition and final
theorem composition remain separate obligations.

## Inputs and selected families

The manuscript is supplied v4 `berry_esseen_manuscript.tex`, SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
Its count lemmas are at lines 4050–4759. This audit uses the notation of
those exact bytes; a source variable named `gamma` in a quartic generator
is the **quartic shape parameter**, not the marginal's signed third moment.

The selected retained inventory is
`proof/n25_retained_b012_catalog.json`, SHA-256
`f055b5017d4e1fd14f2b48a6a95fef4a4c61a025dea6174c424cd5968de801f7`:
17 B0, 35 B1 and 23 B2 forests, 75 in total. The pinned original archive is
`cutoff25_20261011.zip`, SHA-256
`17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`.
Archive-relative paths below contain no dependence on a local directory.

For compact source references define these prefixes:

* **A**: `cutoff25_20261011/new_root/global_sos_quartic_b1_p36_q0_v8/`.
* **B**: `cutoff25_20261011/new_root/global_alpha_stoploss2_b4_p29_q2_v12/`.
* **C**: `cutoff25_20261011/new_low/count37_global_conditional_v2/`.

The source line numbers in each section refer to the named file under
these prefixes. Shared files were identified by SHA, not by filename.

The current seven targets consist of four B4/p29 quarters, B3/p33, and
new conditional V14 B3/p31 and p32. The seven original V12 source designs
under `new_root/global_alpha_stoploss2_*_v12/` have identical mathematical
Python-file pins after excluding their target-specific `count_protocol.py`
and construction helper. The V12 engine is `exact35_core.py` with SHA
`a618867ae34841b2e3e1745e35142694142e08ca2d790b762870f50651e16d71`.
The observed portable V14 designs were also read as sealed source data:

| Target | Original portable design SHA-256 |
|---|---|
| `b3-p31-v14-new` | `bc699a2d539b4aafc193049c8074b02e0b77a38fb01b594c1ba3e2fde6b7b3ff` |
| `b3-p32-v14-new` | `cfe934b1385f9a26f36b6bf94cda9e5caeb6593700a54eeac7e7b1638df61627` |

Each V14 design retains the same V12 count files and adds contact/rho
preprocessing and explicit parent/provenance inputs. Their resource-only
100000-node epochs change the literal checker budget, not these kernel
bytes. This audit did not treat an old exported execution result as a
fresh acceptance.

Retained source families include ordinary conditional count, theta,
tangent, joint-cubic, SOS-quartic, fixed-peak and alpha-stoploss2 variants.
The 75 capsules contain six distinct `exact35_core.py` byte versions;
reading one does not automatically review all six.

## 1. Fully checked small family: domain contractions

These four files occur byte-identically in 64 retained B0–B2 capsules
and in the V12 base of the current seven targets:

| File | SHA-256 | Relevant lines |
|---|---|---|
| `theta_variance.py` | `d33f4e4aced4a1a3887f16964b25a3d716df00702d5c12d3212403b4644831fd` | 7–16 |
| `mean_variance.py` | `c2fe5362f74792879998e23dbb37090cbce6898dad94acbb01b646c1fc7ad50f` | 7–33 |
| `allocation_variance.py` | `3d4d42bdc3cbaa1f578a83f1691c32cb33599a417989a274d21ec42e66671973` | 7–21 |
| `moment_corners.py` | `c95f84ade3b01ad498b46d33066257623f06c363ec3cb72764126a999fa44241` | 5–20 |

The representative copies are under A.

**Theta.** Manuscript 4179–4185 gives
`lambda = n*pq*theta/(1-theta)`. The implementation requires exact ordered
rational inputs, `0<=theta_upper<1`, and uses the maximum of `pq` over
the closed probability interval, including `1/4` when it crosses `1/2`.
It intersects the current upper lambda bound and excludes only `lo>hi`.
At `theta_upper=0`, a zero-noise singleton survives.

**Mean.** Manuscript 4170–4178 gives
`lambda/n = v^2/m^2-v`, `v=pq`, and `v>=m_lower^2`.
The code first intersects that necessary variance domain, minimizes the
convex quadratic with denominator `m_upper^2` at its endpoints and clipped
stationary point, and maximizes the quadratic with denominator
`m_lower^2` at endpoints when the lower mean is positive. A zero lower
mean omits that upper contraction. A zero upper mean excludes because
the original centered variance-one law has strictly positive sign mean.

**Allocation.** Manuscript 4193–4207 follows from
`a0>=s0/O0`, `a1>=s1/O1` and the unchanged joint plane. For fixed
allocation its coefficient is `A/(1-p)+B/p`, `A,B>=0`.
The source endpoint tests are exactly the derivative signs at the two
probability endpoints. Otherwise the minimum is
`A+B+2*sqrt(A*B)`. Integer square rooting rounds the radical **down**,
so the resulting lambda cap is weakened upward. The minimum over
allocation occurs at an allocation endpoint: the infimum over p of
functions affine in allocation is concave. The code changes only the
working lambda interval, not the joint-plane `Lambda` or `d0`.

**Moment corners.** For beta the source uses
`[v(1-2p)+s(2alpha-1)]/(v+s)` from manuscript 4161–4163.
Its global upper bound on the p derivative numerator is
`(1-2pl)*sh*max(0,1-2pl-(2al-1))-2*vl*(vl+sl)`.
If that bound is positive the shortcut returns `None`; it does not
exclude. If nonpositive, p endpoints suffice. For fixed other variables
the s dependence is monotone or constant and the alpha dependence is
increasing, so the remaining corners suffice.
The solved alpha identity is handled analogously: the p derivative
lower gate is a valid outward lower bound, and division is permitted
only for strictly positive s. These shortcuts are gated to `pu<1/2`;
the surrounding interval formula remains available elsewhere.

**Wrapper.** A/`rho_signed_moment_tightener.py`, SHA
`f1650ff9ea811d66acf5f3529e0c0c462cc2d4747fbb42d147406714d0fc2be0`,
lines 26–69, validates the original closed box before contraction.
The solved-alpha division occurs only at `lo>0` (58–65). The unchanged
configuration is passed to the base engine (69), retaining the original
joint intercept. The helper does not silently re-label a contracted
lambda cap as the acquired `Lambda`.

The adjacent source floors also match manuscript 4211–4242:
`signed_beta_variance_floor.py` SHA
`c4208b88510735d0e808b947ec624ce785de42ef4c9fe3217505ebbef2c823c6`,
lines 10–18, checks both low-beta and high-beta cases and divides only by
a strictly positive coefficient. `rho_variance_floor.py` SHA
`615acbcb948d2ba5767082f0dd2a2ab6f1d3999ae0a8afac3fd4c1d73b3aab6b`,
lines 18–28, uses a downward radical, a strictly positive numerator gate,
the four bilinear coefficient corners and strict contradiction for an
empty noise interval.

## 2. Outgoing quartic and exact Bernstein coefficients

The component sources under A or B are:

| File | SHA-256 |
|---|---|
| `general_quartic_sos.py` | `e8159858cafb60c2f469479367a73946688757ebb097be213fcf1ddb8a00ebec` |
| `fixed_peak_quartic.py` | `58fb848383db6f5b9f5b28232b666e94472b22f9f10a83b21ce71f6de4d4e8f7` |
| `bernstein_fast.py` | `4983c9af05673775c3fd5b521e898a9c7f7fe5c9523a5009646872bf75adc607` |
| `joint_cubic_normalized_fast.py` | `7d72ff8ec7cfc2ad59e45d26fcccd6998ef01abe24cb54653ba18b05f2bbf347` |

The SOS shape uses `c=3/2`, `K=2`, exactly the global polynomial identity
at manuscript 4335–4350. The fixed peak is `t_*=9/20`, which gives
`c=171/235` and `K=1975509/7520000` by the same displayed identity.
These constants are global majorant normalizations, not sampled extrema.

For scale a and shape c, let
`B=(c-2)a`, `C=(2c-1)a^2`, `D=c*a^3`, and
`J=(n-k)s0^2+k*s1^2`. After using the fourth-moment support bound,
the source's non-cubic coefficient polynomial is

`(C V-3V^2+3J-support_cost)
 +(-3B V-D)u +(C-6V)u^2 -B u^3-u^4`.

The separately retained cubic coefficients in the **score upper** bound
are

`mass*(n-k)*(a0-O0-B-4u)/(K*a^4)` and
`mass*k*(O1-a1-B-4u)/(K*a^4)`.

This agrees term by term with manuscript 4319–4322 and 4355–4362.
In particular, it has the correct sign after negating the outgoing loss.
The concave term `C V-3V^2` is enclosed at its endpoints and its clipped
vertex `C/6`, not merely at endpoints. The scale a is strictly positive,
mass is required in `[0,1]`, and the conditional support endpoints remain
separate on both signs.

`bernstein_fast.py` 7–19 first performs the exact affine phase substitution
and then the positive degree-four elevation. For each signed scalar
weight it selects the appropriate interval endpoint; the elevation
weights are nonnegative. Thus the resulting upper vector encloses every
coefficient. It does not depend on numerical sampling or on an interval
having positive width. The cubic coefficient is affine in u, so its
Bernstein coefficient is its value at `ul+i*(uh-ul)/4`, exactly as used
by the generators.

The SOS generator is a valid strict outgoing minorant: the polynomial
vanishes at the event boundary and is nonpositive on the closed negative
half-line. It therefore retains atoms correctly. No replacement by a
closed outgoing event is made. Using a negative polynomial lower bound
is safe only because the mass multiplying it is nonnegative; the inspected
`masses()` computes positive exact endpoint binomial masses. The small
literal theorem-hypothesis clarification is recorded separately in
`logic_resource_count_audit.md`.

## 3. Common cubics, defect halfplane and normalization

The common files, present in all 75 retained capsules, are:

| File | SHA-256 | Relevant lines |
|---|---|---|
| `joint_cubic.py` | `d4adf6e9cfa430bbd7be7ffd90b994672d648d9886c42aa38e0a94b66eb55238` | 7–44 |
| `joint_cubic_defect.py` | `86874d28284f931b8907b573c118a9fb8191653a6569d903aed54c9f1974e970` | 9–43 |
| `joint_cubic_normalized.py` | `1403856612e213b9a14118a5a4098b7f470ce890499811dd1ad53c808904e2f6` | 7–22 |

The conditional cubic extrema minimize `w^2/L-L*w` and maximize
`U*w-w^2/U` at their clipped vertices. A zero support endpoint forces
the actual centered conditional law to zero; it is treated before
division. The rho strip preserves the sign `-q*mu0+p*mu1`. Its midpoint
coefficient error bounds `abs(mu0+mu1)` on the complete cubic rectangle,
as required by manuscript 4605–4609.

The defect halfplane matches manuscript 4274–4291. Its binary polynomial
is expanded as coefficients
`[0, sigma-1, -3sigma-3, 4sigma+10, -2sigma-6]`.
The source uses the lower sigma endpoint for the nonnegative base and
keeps separate midpoint coefficient errors for the two cubic terms.
It uses lower variance substitution only when both displayed linear
coefficients are nonnegative. If that gate fails, it retains the rectangle
and rho strip and omits the optional defect halfplane. This weakens the
relaxation; it is not an emptiness conclusion.

`polygon_vertices()` solves every pair of nonparallel boundary lines
over exact rationals and retains only points satisfying all closed
halfplanes. The support rectangle makes the intersection bounded.
The pair enumeration also covers degenerate bounded segments and points.
The normalization helper splits this polygon at the affine rho-floor
switch and recomputes vertices on **both** closed pieces. Its denominator
is `max(acquired_rho_floor, affine_rho_floor)`, with a positive acquired
floor. This matches manuscript 4625–4640. No independent pair of cubic
extrema replaces the shared polygon.

## 4. Convex incoming assembly and strategy order

The reviewed common assembly sources include:

| File | SHA-256 |
|---|---|
| `cubic_mgf.py` | `d360be74b191529b2a7e76d03feb3db7c9e303fc5b05be4fb403eb342aa5168e` |
| `common_cubic_bound.py` | `f62a02b6e081b377b584a100cf704ed0966589e1de80177b4a33002af665af1c` |
| `common_shifted.py` | `947ef9b4b43e265fc3250d2c43b69976f11ed7229387d9e0ab51673e683e35b6` |
| `general_quartic_sos_bounds.py` | `716eda950209111c78960e819e20d0e86b83cb51868a9eaa583b839dbe32c4b5` |
| `fixed_peak_quartic_bounds.py` | `26d5ec337ef7f0cab81f7c4ced7b4c208d810e5a2670c07d25041ff797e3e88e` |

The directed cubic coefficients correspond to the chord of
`r_t(x)=(exp(tx)-1-tx)/x^2` at `[-L,B]` (manuscript 4550–4573).
The negative endpoint exponential is bounded by reciprocal positive
exponentials; when its upper-series domain would fail, zero remains a
valid lower bound for that negative exponential. The source uses a
coefficient midpoint plus `coefficient_halfwidth*max_abs_moment` to form
an affine upper MGF. The bound on moment magnitude is valid on the whole
polygon because a coordinate absolute value is maximized at its vertices.
For `-U_i` the cubic sign is reversed, as the source's `A-D*mu_i` requires.

The assembly uses positive fixed pivots and weighted AM--GM with weights
`(n-j)/n` and `j/n`, precisely manuscript 4575–4586. The positive clamp
`max(1, affine_upper)` is also convex and remains a valid MGF upper bound.
Rate, pivot and Cantelli/exponential strategy choices are made once per
incoming count and then retained for **all** vertices and phase controls.
They are not chosen independently at each vertex. The quartic scale/shape
menu is minimized only after the full vertex and Bernstein-control maximum.

For shifted excess, `reciprocal_chord()` requires a strictly positive
shifted distance. Its denominator lower bound is the larger of two valid
lower bounds for `exp(x)-1-x`, including `x^2/2`. Positive endpoint upper
values define a valid upper chord of the convex reciprocal-excess factor
from manuscript 4591–4598. The nonnegative convex numerator is retained
before the vertex argument. This is different from clipping a convex
incoming probability upper bound pointwise by one.

The common-assembly context guards require the same n, k, phase interval,
conditional variance intervals, outward ceiling, inward cap and matched
incoming/Gaussian slope. The old incoming line is removed algebraically
before a new common-cubic line is added. For example A/
`general_quartic_sos_bounds.py` 26–32 uses
`base_intercept=intercept-left+lip*ul` and `base_drift=-gaussian`.
This retains the original Gaussian lower envelope; it does not charge the
old incoming line a second time.

The use of `up()` at vertex evaluations does not require the rounded
function itself to be convex: the underlying unrounded convex numerator
has its ratio bounded at the vertices, and rounding those finitely many
upper values upward preserves that bound.

## 5. Finite-allocation stop-loss route

The V12/current-seven and six retained B2/p33–38 capsules share:

| File | SHA-256 |
|---|---|
| `coupled_alpha_stoploss.py` | `9b2808677ab3ec1f38973a82fd7a6df081314144548c05dbe86fd4b8204a0074` |
| `integer_stoploss.py` | `e8178e82421b7b58de948abf94a65f9eb517e4a54f65e43bddbfd76f3ed9a9ab` |
| `quadratic_stoploss.py` | `bbf1ae7a745ad5c0798ee4a009bc6e96b2ae12983198cebc35605745cef1cf88` |
| `stoploss3_fixed.py` | `04ddcd5e351c0d6a01f7b1c7a39e41f6cec6d77052a8d3ca5393f7390c706366` |

The comparison law is exactly the convolution of the two centered
two-point laws in manuscript 4474–4517. For upper ceiling B and variance
v its atoms are `-v/B,B`, with positive mass `v/(B^2+v)` at B. Integer
common denominators preserve these rational atoms and weights; zero
variance, zero ceiling and zero multiplicity contribute a unit atom at
zero. Repeated atoms may remain repeated with positive weights, which
does not change their expectation.

The quadratic optimizer scans the ordered negative-offset breakpoints,
removing a term only when its positive part has reached zero. On each
active interval it uses the stationary point of the exact quadratic.
The initial derivative is negative because the comparison sum is centered
and the distance positive. A final constant interval is handled. The
returned scale is then fixed for both phase endpoints of that chord.
The cubic alternative likewise fixes its rational scale for the whole
chord. These are whole-phase upper envelopes for closed incoming events.

`coupled_alpha_stoploss.py` 18–38 covers the entire closed allocation
interval with four parts. On each part it uses the valid separate
variance ceilings from manuscript 4536–4546. For each selected scale it
evaluates **both** endpoints of a complete chord. Taking the maxima of
left and right values over those complete chords yields one line
dominating every chord throughout the phase interval. Thus the source
does not join unrelated optimized endpoint values without a common
whole-phase witness. Its zero-width phase case is evaluated directly.

## 6. Certificate link and original roots

The topology/parser part has a stronger source inventory result than one
representative read: all 75 retained protocols have identical ASTs for
`same`, `unique`, `rootbox`, `children`, `evaluate` and `replay`.
Their common `replay` function AST SHA-256, with source positions omitted,
is `bb5b2d40f1caebcdc321315dbc90d26481feaa0edabf05e4e0554e6722c1ccb9`.
This AST comparison ran no protocol code.

Representative B/`count_protocol.py`, SHA-256
`5cd4f1a59ba1dbd10ae0455cde3731e03b236b0e1572dda78734dce5142e7f96`,
lines 33–55 and 71–126, binds the contract, checker and kernel manifest;
reconstructs all 26 original boxes; requires ordered integer counts,
strict interior rational cuts and both closed children; reconstructs
each leaf box; recomputes each leaf and requires whole result equality.
The cache key includes k and every reconstructed box endpoint. A claimed
score is not accepted as arithmetic evidence by itself.

The root coordinates are `(p,lambda,alpha,u,a0)`. In B/
`exact35_core.py` 443–490, the other inward endpoint remains enclosed
by the residual budget and physical sign cap. It is not assumed to
saturate the budget. Equality in interval tests survives; empty cases
use strict contradiction. All 24 original corruption controls remain
part of the acceptor. Their execution is a separate fresh-run obligation.

`generalized_scope.py`, SHA
`0ca76c72ccf7f9243e1d9b7d68f814b84e160f7da11945a7842dff5b2abebc00`,
15, imposes stronger-than-needed nearest-count coverage: h<1 follows
from `1/4+Lambda/n<1`, and `n*pl-Hminus>0`,
`n*pu+Hplus<n` put all allowed thresholds inside the nearest-count union.
These are conditional acquired H bounds. Merely validating their fields
does not acquire them for an actual law.

The portable V14 protocol has the same topology logic, checks the exact
original V12 contract plus explicit contact fields (p31 source 40–47),
and calls `local_contact_v14.cell35`. Its final V12 call receives every
original raw coordinate, not a saved contracted box. The V14 helper SHA
is `78ee48726397e1a6185aa02584ffd21d4eb87ff69e9685807a13b5f9edf09a7c`;
lines 21–50 show three finite preprocessing steps followed by the V12
call. This establishes the code route, not the soundness of those
additional support/contact implications.

The current node-limit adapter preserves every original function AST and
changes only `LIMIT=10000` to `LIMIT=100000`. That gives a new checker/design
epoch. It does not weaken the strict leaf target, original roots,
corruption controls, contract or mathematical component pins. Acceptance
must still use the exact new profile and must not be presented as the old
checker identity.

## Explicit remaining enabled paths and review limits

This audit does **not** certify any complete one of the 82 selected jobs.
The checked small contraction family and component matches above should
be retained as scoped proof-to-code evidence. Remaining work includes:

1. **V14 preprocessing:** `local_contact_v13.py`,
   `local_contact_support.py`, `local_contact_outer_v14.py`,
   `local_rho_upper_v14.py` and their support/Gaussian/scale/binomial/heat
   helpers. The finite ordering and original-box call were read, but the
   entire chain's quantitative derivative/ray gates were not independently
   rederived here. This is required for both new V14 targets.
2. **Complete engine routes:** all six retained `exact35_core.py` versions,
   every optional sharp-D endpoint inversion and every status returned by
   its complete call chain. The V12 source was read, but this note does
   not claim an exhaustive branch-by-branch proof of its whole engine.
   The older no-theta wrapper variant in the 11 simple B0 capsules is a
   separate source version from the reviewed theta wrapper.
3. **Primitive enclosure proof:** a complete standalone review of
   `finite_gaussian.py`, the Machin/pi/radical constants, directed CDF
   evaluation, `normal_lower`, centered binomial/Gaussian derivative
   cancellation and all enabled optimized interval operations. Relevant
   source was read; these primitives were not executed or exhaustively
   independently verified in this pass.
4. **Additional incoming/own strategies:** the full paired left-value/
   slope selection and Gaussian derivative cancellation in each engine
   version, all own-count buffer/union paths, and every tangent/sharp MGF
   call's feasible-domain routing. Some component formulas were checked;
   complete caller coverage remains distinct.
5. **Actual acquisition joins:** prove that the current physical law
   satisfies every support, signed moment, theta, phase, affine and joint
   premise consumed by each exact contract, including local B1/p35 and
   B2/p31 acquisitions. Neither a manifest, source hash, stored accepted
   object nor a completed conditional count run supplies this implication.
6. **Fresh execution and final scope:** complete the numerical replay on
   Colab with its exact source/profile and controls, then verify complete
   region and discrepancy-orientation coverage. The seven reconstructed
   jobs and the retained B0–B2 jobs do not by themselves cover every n25
   region, let alone every index of the manuscript.

No runtime, frozen source, contract, forest, graph or notebook was changed
by this audit, and no global or parent-acquisition flag is asserted.
