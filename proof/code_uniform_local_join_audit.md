# Uniform local joins: signed resources, LEFT270, Sperner and closed coverage

Date: 23 October 2026. This is a fallible internal AI source and hand-algebra
review. It is not external independent verification, formal verification or
fresh arithmetic acceptance. Other model agents' cross-reads are internal
checks by the same system. No archived mathematical module, constructor,
bound evaluator, acceptor or coverage program was imported or executed.
Only original bytes, source/AST/JSON, simple rational metadata comparisons
and the derivations below were used. No runtime or global proof status was
changed.

## Bounded result and exact sources

This unit extends the [INITIAL review](code_uniform_initial_atlas_audit.md)
and [live geometry review](code_uniform_geometry_atlas_audit.md). It follows
the actual installed signed-variance and conditional-gamma improvements,
the Sperner feedback/LEFT270 resource callers, and the selected exact
local-coverage composition. No unsound direction was found in the reviewed
improvements or their literal domain mapping. The inspected acyclic route
preserves the original same-law weak input while adding stronger resources.

This is **not** a complete re-proof of the Sperner/confinement or local
comparison kernels, and it does not acquire any predecessor. The coverage
checker itself expressly leaves theorem validity and arithmetic acquisition
as dependencies. Those limitations matter even if every numerical gate in
its own geometric partition check passes.

The archive is `BE_cutoff49_20260930.zip`, 16,660,566 bytes, SHA256
`ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e`.
Set `A=BE_cutoff49_20260930/` and
`B=A/baseline/certificates/work/below50_20260929/`. References below are
relative to B. The [source map](code_uniform_local_join_source_map.json)
records exact member hashes and original-manifest comparisons, read ranges,
the relevant candidate table bindings and explicit conditional graph edges.
Manuscript identity remains
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
Its positive-measure, joint-resource and same-law arguments at 2431–2674,
and conditional gamma at 2735–2743 and 3942–3955, provide the corresponding
mathematical notation. A hash identifies the selected argument; it does not
prove that argument.

## 1. Two real installed improvements, not a different optimization law

`entry/sperner_panel_core.py:9–13` installs HIGH_WINDOW and
`paired_conditional_gamma47`; `entry/coupled_panel_core.py:9–15` additionally
installs `signed_variance_resource`. The latter wraps the original acquired
`general_cell`, returning immediately if that original cell is impossible.
The actual support radius and the same acquired p/moment/defect state are
retained. The rest of each local driver has the ordered raw/conserved and
weighted-export structure already reviewed in the geometry unit. There is
no change of physical marginal between a tighter moment and its Fourier
envelope.

For the gamma improvement, conditional centering gives exactly

`gamma=E[V³]+E[W²(X+2V)]`,

where V=E[X|sign], W=X-V. On p in [l,u] subset (0,1/2), the positive-class
residual is nonnegative. On the negative class,
`|V|<=sqrt(u/(1-u))`, so the residual is at least
`-(R+2sqrt(u/(1-u)))*theta`. The binary third moment is
`(1-theta)^(3/2)*(1-2p)/sqrt(p(1-p))`.
Both factors are nonnegative and decrease toward the adverse endpoints
Theta and u. This proves `conditional_gamma47_proof.tex:13–34`, including
zero conditional variance. The source at `paired_conditional_gamma47.py:15`
uses a lower square root for the positive term and an upper root for the
negative coefficient. Taking its maximum with zero and the older valid
gamma floor remains a lower bound **on the selected acquired states** for
the following additional reason. The mere condition p<1/2 does not force
the actual signed third moment to be nonnegative under arbitrary noise.

For every row in the weak central input (45), first feedback (45), left
input (39), Sperner feedback (45), signed resource (83) and LEFT270 (38),
the exact declared metadata satisfy
`SL²*rhoB(u)²>(3+D_row)²`, where
`rhoB(u)²=(1-2u(1-u))²/[u(1-u)]`. These 295 elementary rational sign
comparisons did not evaluate a mathematical kernel. The iterated d never
exceeds D_row. Whenever the paired reserve gate passes, it proves
`rho>=rhoB(u)` for that state, while the physical gap identity gives
`gamma>=sigma*rho-3-D_actual`. Consequently
`gamma>SL*rhoB(u)-3-D_row>0`. Thus zero is a valid lower bound here;
the signed conditional formula alone is not being asked to prove it.
This selected-data license must accompany any reuse of this helper. Its
displayed p/M/g domain alone is not a proof of nonnegative gamma for
arbitrary supplied inputs.

The enlarged floor is fixed **before** the paired Fourier rectangle.
All moment, denominator, signed coefficient and R>2g gates are checked
again. The outer caller's preliminary eligibility uses the older weaker
floor; if the stronger floor makes an internal gate fail, the call aborts.
No exception turns that failure into an accepted smaller bound. The same
installed paired function recomputes the selected floor and rmin at its
subsequent uses. The late phase formula may keep a weaker valid gamma floor;
using a weaker curvature does not invalidate the improved LOW estimate.

## 2. Signed variance pricing and the zero-variance limit

The resource is the one simultaneous inequality

`6m(A_l+B_l)(DeltaA+DeltaB)+K+ theta+ +K- theta- <= r`,

with r=d-binary>=0, `K+=3(sigma+1)B_l`, `K-=3(sigma+3)A_l`.
For j=3,4,5 the conditional Taylor identity gives

`E|X|^j <= (1-theta)^(j/2) B_j(p)
             +L_j(v+)theta+ +L_j(v-)theta-`.

On the selected left-half panel an upper binary moment B* is obtained at
l. Convexity of `(1-theta)^(j/2)` places it below its chord on [0,Theta]:
`(1-theta)^(j/2)<=1-k_j theta`. The exact chord slope is
`[1-(1-Theta)^(j/2)]/Theta`. A **lower** slope enlarges the bound, since
it is subtracted from both variance prices.

`signed_variance_resource.py:19–27` uses an upper root in the subtracted
power, giving just such a lower slope; it clips this to zero. For j=4,
2-Theta is the exact slope. At Theta=0 it uses j/2, and only theta=0 is
then physical. Thus the division by Theta is not attempted at zero. The
binary ceilings have positive numerators/denominators, with an upper root
or lower positive denominator in the appropriate direction.

The positive-resource simplex rule now gives

`E|X|^j <= B* + r*max(0,(L_j(v+)-k_j B*)/K+,
                         (L_j(v-)-k_j B*)/K-)`.

This is a maximum of competing prices, not their sum. It permits signed
negative moment increments because zero is also a possible maximum. The
code intersects the resulting rho, fourth and fifth ceilings with their
previous valid bounds and radial/Pearson bounds. It does not construct a
new hypothetical law attaining all those separate maxima.

The same resource also controls outer charge. Conditional cubic expansion
gives `T+<=2m v+ DeltaB+L3(v+)theta+`, and its reflected counterpart.
Therefore `Wouter=(sigma-1)T+ +(sigma+1)T-` is at most r times the maximum
of the four displacement/variance prices in
`signed_variance_resource47_proof.tex:63–85`. Source lines 34–35 use upper
SU in the positive numerator and lower SL in K+/K-, preserving their
**different** sign weights. The smaller outer ceiling replaces the old
negative J1 penalty in the lower U formula, and the upper U is recomputed
using the smaller M and outer ceiling. It is not valid to add this entire
new resource bound to another use of r; the actual code does not do so.

## 3. Sperner feedback has a weak-input premise independent of its conclusion

The strict common-budget hypothesis in the Sperner proof also has an actual
source license; it is not inferred from a non-strict target-field comparison.
The exact error ledger is `|E_n|<=2sqrt(n)(I_LOW+I_HIGH)/pi` at manuscript
1596–1605. The general source uses the strictly larger Fourier factor
16/25, and the paired source uses 212/333>2/pi since pi>333/106. Their
enclosing LOW+HIGH expression is strictly positive: in particular all six
installed HIGH pieces are positive. Thus the rational raw quadratic
strictly exceeds the physical remainder, even if its later outward
coefficient comparison is an equality. Subtracting an acquired lower
phase price preserves strictness for the conserved budget. Maximizing
over the finite score/rho corners and rounding coefficients outward also
preserve that strict inequality. The raw ceiling update is a minimum of
previous and new strict ceilings. Consequently the acquired budget is
strictly below both its T ceiling and the exported maximum of budget
quadratics. This is conditional on the earlier complete Fourier bounds,
not evidence that their numerical gates were rerun here. In particular it
licenses the later `cap<=0` exclusion, including the zero endpoint: a
nonnegative resource cannot be strictly below a nonpositive cap.

The selected weak central input is `local/conditional_input47.json`, hash
`b9d2aa15ad96181f5a8eb846e76ae296d2c2c8ed1a5975c6f389c2f7d14ff2b7`.
It covers 45 closed .002 panels [.38,.47]. Original confinement and the
stronger Sperner confinement both consume this same weak input.

`accept_sperner_feedback47.py:29–53` binds:

* the first, already acquired `confined_feedback47_table.json`;
* `sperner47_certificate.json`, whose contract names the original weak input;
* both confinement signs and the exact p/index/amplitude for each of the
  45 panels;
* an amplitude no larger than the first feedback amplitude, then the
  outward actual-radius formula proved in the geometry review.

Its subsequent stronger arithmetic consumes the first feedback scalar
resources and the independently obtained smaller support. It does not use
its own new table to establish the Sperner premise. Both old and stronger
resources hold for the same witness after the refinement; the original
weak input is not discarded.

An essential additional premise is the actual Bernoulli-coordinate strip
`support(Y) subset (-.55,1.55)`. It is explicitly assumed in both
`local/sperner47_proof.tex:21–86` and its left counterpart. A standardized
radius such as R=2.5 or R=2.7 does **not by itself** supply this strip.
The actual separate central job is `root/accept_panel_exterior47.py`.
Its named 47 hypothesis rows cover the weak central p range and include
the required moment/threshold caps, prior standardized support radius 2.5,
true contact, decrement<=.19 and the external `0<=a<=.7/n` excess ceiling.

As a source-only interface check, all 45 weak rows fit their corresponding
named strip row: 315 elementary rational comparisons checked p containment,
rho, theta, both H caps, beta upper and nonnegative beta lower. This checks
compatibility of stored **hypotheses**, not their arithmetic acquisition or
the correctness of the contact polynomial. The finite strip replay and its
contact argument remain separate requirements. In particular, strip must
precede original/Sperner confinement in an actual full proof join.

The original Sperner proof's strict-gap antichain/convolution/deletion
argument and its complete numerical kernel were not re-proved in this
unit. The inspected interface requires them as actual same-law conditional
theorems; the word "Sperner" or a matching certificate hash is insufficient.

## 4. The 84-to-83 signed resource join and LEFT270 support

`accept_signed_resource47.py:16–55` consumes 39 left rows and 45 central
Sperner-feedback rows, exactly 84 prior probability panels. It fully
processes all of them. The first left row [.302,.304] must be excluded;
the other 83 output rows cover [.304,.47]. Their p/index/source mapping
is literal, including the closed common endpoint .38. Each output radius
is exactly the acquired parent radius, not a freely proposed contraction.
The full four score/rho corners and both signed phase curvatures are checked.

The acquired signed table is
`entry/signed_resource47_table.json`, hash
`8ede412f88e5b0758dadf2590ca0f48f24b579cac22db6e4701cb6de532e6c39`.
Its 38 left rows are the input to the **separate** support theorem
`accept_left_radius270_47.py`. That wrapper's exact conditional statement is:
for n>=47, C>=CE, decrement<=.19, rho<=1.2563 and |beta|<=.3926, every
attained oriented witness has full actual support inside (-2.7,2.7),
uniformly in H. It uses the previously reviewed complete fifth-order heat
support theorem; no prior support radius is assumed by that heat argument.

`accept_left270_input47.py:29–44` checks all 38 selected rows have the
moment caps needed by that support theorem, including the absolute maximum
of both beta endpoints. A simple source-table comparison confirmed all 38
meet those declared caps. This does not evaluate the heat kernel. The
standalone support wrapper fixes the claimed caps; it does not acquire the
row table by itself. The dependency must be signed resource acquisition,
then the support theorem on its moments, then the new radius-2.7 refinement.

The new LEFT270 table has hash
`4b7bb259e469ee57ca6a61d89fd0b3385443508129138899fe597fd82dc9521a`.
Its 38 closed cells remain exactly `[ (152+j)/500,(153+j)/500 ]`,
j=0,...,37, covering [.304,.38]. The entry and local copies are byte-for-byte
equal. This identity is required before the local comparator lane reads it.

The left strip job `root/accept_left_strip47.py` then consumes this acquired
LEFT270 table, prior actual support 2.7, true positive closed contact,
decrement<=.19 and `0<=a<=.7/n`. It checks the whole finite standardized
exterior up to that prior radius and derives `support(Y) subset(-.55,1.55)`
on [.304,.38]. Its actual call explicitly enforces
`0<=beta_lo<=beta_hi<1` before using the signed polynomial. All 83 stored
signed resource rows have nonnegative beta lower metadata, but the
inequalities producing those rows still need full replay. No beta sign is
inferred just from a variable called beta_hi.

The left strip precedes left Sperner confinement and its noise-dependent
profile. Thus the sequence signed resource -> LEFT270 heat support ->
LEFT270 refinement -> left strip -> left Sperner is acyclic. It would be
invalid to acquire the initial left strip from a confinement conclusion
that itself assumes that strip.

## 5. Stronger resources and old amplitude theorems remain simultaneous

`local/final_review/check_local47_coverage.py:26–36` compares the central
Sperner-feedback scalar interface against the original weak central input.
Upper ceilings shrink, lower endpoints rise, and the acquired amplitude is
no larger than the old per-panel theorem. It also requires exact equality
of the two LEFT270 copies. These conditions mean the stronger state still
satisfies the weak hypotheses used to prove the older confinement/profile
theorems.

The new and old signed quadratic envelopes need not be componentwise
ordered. Both are valid for this same witness if both acyclic acquisitions
have been proved. One may use an old theorem under its old resources and
a newer comparator under newer resources without claiming coefficientwise
domination. A join must carry both source acquisitions, rather than selecting
the smaller coefficient from unrelated or unacquired envelopes.

The additional amplitude schedules are actual fixed conditional theorem
jobs, `accept_sperner47_profile.py` and `accept_left_sperner47_profile.py`.
For each panel they cover the closed noise bands [.05,.08], [.08,.10], and
[.10,Lambda], clipped to that input's acquired ceiling, and check both H
signs and the full 16x16 H/noise grid. Their output amplitudes are respectively
(.35,.30,.275) centrally and (.375,.325,.30) on the left, intersected later
with the base amplitude. The profile jobs require complete kernel gates;
they do not follow merely by rounding the base amplitude down.

The coverage check's amplitude license subdivides at all schedule boundaries
and checks endpoints and interval interiors. Its source tables have no
Lambda exactly equal to .05, .08 or .10, so no skipped zero-width profile
band is being used to obtain a stronger isolated-boundary amplitude. This
is a checked property of the fixed data; unrestricted changes to those
ceiling values would require reconsidering the zero-width boundary case.

## 6. Exact phase/noise union and what its finite representative test proves

The final cover uses 38 left plus 45 central closed probability cells and
explicitly checks their common .38 seam. On each it covers
`0<=lambda<=Lambda` and the full outer lattice phase `-.5<=u<=.5`.
This outer phase u is distinct from the sign of H. Both H signs are checked
by the LOW row/sign census even though only one duplicate geometric
rectangle per phase/noise domain is needed in the union.

The source's partition is:

| Noise band | Central phase union | Left phase union |
| --- | --- | --- |
| 0<lambda<=.05 | TINY covers the full [-.5,.5] | Same wide TINY domain |
| [.05,.06] | LOW [-.09,.09], MID complements | LOW [-.09,.09], MID complements |
| [.06,.08] | LOW [-.13,.13], MID complements | LOW [-.14,.14], MID complements |
| [.08,.10] | LOW [-.18,.18], MID complements | LOW [-.19,.19], MID complements |
| [.10,.12] | LOW [-.29,.29], MID complements | LOW [-.29,.29], negative MID [-.5,-.29], extra positive LOW [.29,.5] |
| lambda>.12 up to Lambda | Standard LOW covers [-.5,.5] | Standard left LOW covers [-.5,.5] |

Every row is clipped to the acquired Lambda; a nonexistent upper band adds
no obligation. Endpoints .05,.06,.08,.10,.12 and the phase seams are closed.
The extra positive-left family is essential: the selected left MID code
has only the negative-phase context in the [.10,.12] band. Omitting the
extra positive LOW would leave an actual phase-domain hole. The selected
coverage code includes it; this review found no such omission.

`prove_cover:38–52` collects all rectangle endpoints and one midpoint of
each adjacent interval on both axes, then checks their Cartesian product.
This finite test is exact for closed axis-aligned rectangles: membership
in every rectangle is constant on each open interval between consecutive
endpoints, while each endpoint is a separately tested face. The Cartesian
product therefore tests every 2D open cell, edge and vertex. It is not
sampling an arbitrary nonlinear feasible set. `license_amplitude` uses the
same valid finite-partition argument for a piecewise constant schedule.

`inspect_low_object:64–79` additionally requires the exact ordered p/H-sign
rows, expected finite box census, both noise endpoints, complete scalar
contract and absence of failed gates. A wholly budget-excluded row has no
score value; it is not assigned a fictitious strict score. This inspector
does not recompute the LOW inequalities. The corresponding full original
LOW acceptors, EMPTY-implication proofs and comparison theorem are separate
dependencies. The same is true of TINY and MID; a correct union cannot
turn their invalid or unacquired inputs into a proof.

The original frozen coverage JSON reports 83 probability panels, 585 scalar
monotonicity checks and 84,415 partition checks, plus LOW censuses of
74/66/54 signed rows. These are historical data read here, not rerun results.
This source review established the structure of the finite coverage test,
not those numerical outcomes.

## 7. Atoms, lambda=0 and the global boundary

The contact and support hypotheses are closed and actual. No positive
minimum atom size is inserted by these joins. Zero conditional variance
is included by the gamma and signed-resource arguments above. For the
local comparison itself, lambda=0 is a separate logical case: U=0 almost
surely and the witness is exactly the associated two-point law.

The coverage rectangle starts at lambda=0, but its own label says
"Bernoulli at0; TINY atpositive lambda", and the returned scope cites the
finite-n Bernoulli theorem separately. A strict comparison proportional
to lambda at lambda>0 cannot prove the lambda=0 boundary by setting
lambda=0. That named two-point theorem and its endpoint convention remain
required analytical input. This note has not newly verified that literature.

Likewise the local lemmas are conditional for n>=47. The original coverage
scope expressly separates the global descent over 47..98 and the prior
99 tail. Deriving the later all-index cutoff requires the actual slow-index
selection/smoothing recurrence, barrier and decrement hypotheses, finite
range joins and the relevant tail. No global cutoff follows solely from
an 83-panel local partition.

## 8. Explicit completion boundary

Completed in this bounded source read: the conditional-gamma derivation;
the signed positive-resource moment/outer directions and zero-variance
limit; the actual 84-to-83 and 38-row maps; the required strip/support
ordering and checked data compatibility; the four-phase-family closed
union, including the extra positive-left bridge; and the exact reason the
coverage representative test suffices for rectangles.

Still separate: fresh full arithmetic and execution/source/receipt acceptance;
actual support/strip/confinement and scalar predecessor acquisitions; the
full antichain/deletion/concentration-to-confinement proof and kernel;
TINY/MID/LOW analytic comparisons and all their primitive rules; the
lambda=0 Bernoulli theorem; and the unrestricted/global descent and
same-law final proof joins. The older 29/5 coarse bootstrap remains
explicitly unreviewed as stated in the geometry unit. No completed label
in this note promotes any of those boundaries to unconditional acceptance.
