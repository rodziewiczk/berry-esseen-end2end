# Uniform local geometry: acquired state, conditional moments and signed exports

Date: 23 October 2026. This is a fallible internal AI source and hand-algebra
review, not external independent verification, formal verification, or a fresh
arithmetic replay. Other model agents' cross-reads are internal checks by the
same system. No archived mathematical module was imported or executed. Only
original bytes, text/AST/JSON and hand derivations were used. No runtime,
notebook, frozen source or global proof status was changed.

## Bounded finding and source instance

This unit follows the **live** uniform-tail `local_panel_core.cell` and
`contracted_panel_core.cell`, the complete `general_cell` formula atlas and
central Bernstein bound, the general/paired caller selection and signed
quadratic exports. It reads the actual central, complementary, left-input
and confined-feedback callers. The positive-measure and shared-gap-budget
arguments below give conditional directions for the inspected formulas.
No unsound selected inequality was identified in this block. This does not
acquire its INITIAL, support, confinement, score or fresh arithmetic premises,
nor exclude all probabilities or establish a cutoff theorem.

The archive is `BE_cutoff49_20260930.zip`, 16,660,566 bytes, SHA256
`ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e`.
Set `A=BE_cutoff49_20260930/` and
`B=A/baseline/certificates/work/below50_20260929/`. Source references below
are relative to B. Every listed archive member was compared with its actual
original `A/MANIFEST.json` SHA256. The new
[source map](code_uniform_geometry_atlas_source_map.json) records the pins,
function-level normalized-AST comparisons and line ranges.

The source files `entry/kernel.py` and `entry/contracted_kernel.py` have
respective hashes
`d71f58b7527c3cf6d2146d816e5d124f6f331d1b153e5aaedee5182707647f12`
and `0367aae733dfe2d6467188d941d6fc8ccd7bb6f4bf3aa4c98dca3c4781534d22`.
The latter is a separately named actual-radius extension, not an edit to the
former. Their `general_cell`, `central_bound`, `general_envelope`,
`late_envelope`, `quadratic_extrema` and `signed_k_error` function ASTs agree.
Their paired functions differ by the explicit contracted-radius gate R>2g.
The older source's R>=2.3 and paired g<=1 imply that gate automatically.

The source is related to, but not wholly identical with, the n25 resource
capsules. The n25 version adds an endpoint-empty exception, relaxes the rho
floor in its signed K error, changes the HIGH gap helper and phase-charge
piecewise score corners. These differences were text-compared. The
[n25 atlas review](code_general_cell_atlas_audit.md) is useful context but is
not a byte-identity shortcut for the present uniform callers.

Manuscript references are to the supplied `berry_esseen_manuscript.tex`,
SHA256 `2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
The relevant arguments are lines 2431–2674 (positive measure, simultaneous
gap budget and weighted exports), 2981–3037 (moment atlas and signed K),
3052–3155 (central/sign/outer charges), and 3196–3226 (rho and full signed
quadratic extrema). The original `entry/initial47_panel_proof.tex:91–190`,
`baseline/entry/entry95_proof.tex:21–80,217–299`, and
`entry/confined_feedback47_proof.tex:7–82` were also read as arguments,
rather than treating their historical PASS prose as acceptance evidence.

## 1. The state and the same-law obligation

At `entry/local_panel_core.py:24–31`, and the contracted copy at 25–32,
the acquired inputs concern a single attained oriented witness:

`n_actual>=N=47`, `|X|<=R`, `C<=cap`, `p=P(X>0) in [l,u] subset (0,1)`,
`Rraw<=r<.4N`, `n_actual D<=N d`, `0<d<2`, `theta<=Theta<1`,
with the exact contact/Fourier identity and nonnegative defect/leakage.

D<2 implies a true central gap (-A,B), A,B>0, hence no atom at zero.
Set q=1-p, m=EX+=EX-, conditional means `a_bar=m/q`, `b_bar=m/p`, and
`DeltaA=a_bar-A`, `DeltaB=b_bar-B`. They are nonnegative. The conditional
variance identity is `m²=(1-theta)pq`. Here n is the program's **floor N**,
not a substitution of the actual witness index throughout the theorem.

INITIAL provides the first valid state as reviewed in
[the signed INITIAL unit](code_uniform_initial_atlas_audit.md). Every later
support contraction must apply to this law on the same p interval. An old
resource JSON hash, a proposed radius, or an optimizer's compatible-looking
numbers cannot acquire that premise. The fixed callers explicitly describe
themselves as conditional; a full proof join must discharge those conditions.

## 2. Initialization and finite monotone geometry updates

The exact central-gap identity implies `A+B>=sqrt(2-D)` when D<2. Since
`m>=sqrt((1-Theta)*min_panel pq)`, dropping nonnegative terms from the
joint budget gives

`DeltaA+DeltaB <= d/[6 m_lower sqrt(2-d)]`.

The initial A/B lower formulas at `local_panel_core.py:28–30` subtract this
one shared displacement bound from lower conditional means. Both `lo` calls
are **lower square roots**, not floor-rounding of their arguments. Thus
`sqrt((1-Theta)l/(1-l))` and its reflected endpoint are lowered, while the
shift denominator is lowered to enlarge the shift. Nonpositive proposed
endpoints cause a failed initialization, not a successful empty-cell result.

For an acquired rectangle A>=al, B>=bl and variance cap Theta, the full
same-law budget gives

`D >= binary(p,theta) +6m(A+B)(DeltaA+DeltaB)
                      +3(sigma+1)B theta+ +3(sigma+3)A theta-`.

Dropping the additional nonnegative product `6m DeltaA DeltaB` weakens the
manuscript's exact lower estimate. Put

`b = (6+2SL)*sqrt_lower((1-Theta)^3)*dist(p*,[l,u])²/sqrt_upper(pq_max)`,
`K=min(3(SL+1)bl,3(SL+3)al)>0`.

The p* interval is `[(4-SU)/2,(4-SL)/2]`; using its distance from the panel
can only lower the true distance. Therefore residual=d-b is an upper
resource. A strictly negative residual excludes the entire closed panel;
equality is retained. Upper rounding of residual/K safely lowers Theta.
The residual computed before that variance improvement remains a weaker
valid upper resource after it; no claimed fixed-point equality is needed.

The two individual endpoint updates at `kernel.py:205` (contracted:207)
have another direct derivation. On the positive side, Y>=B gives
`T+>=2 B² M+` and `R+>=B M+`, where M+=p DeltaB. In the gap identity,
`T-Jo>=2 B R+ +2 A R-`. Consequently
`D>=2(sigma+2)B² M+`, with the reflected bound
`D>=2(sigma+4)A² M-`. Replacing these constants by 129/25 and 179/25,
using lower endpoints and lower class probabilities, enlarges the allowed
displacements and therefore lowers the updated A/B floors. Using d rather
than residual here is weaker, not an additional spending of residual.

The next common-shift update at `kernel.py:206–209` uses the single
`6m(A+B)(DeltaA+DeltaB)` term. Its denominator is lowered, each displacement
is at most their sum, and new endpoint floors are intersected with old ones.
The source performs a fixed 24 inner updates in the live local-panel caller;
each is ordinary induction on previously acquired inequalities. It never
asserts convergence or that an arbitrary numerical fixed point is physical.

## 3. Complete conditional moment atlas and zero-noise faces

For j>=2, conditional Taylor expansion gives

`E[h(|X|^j-|V|^j)]
   = E[h W² sum_{k=0}^{j-2}(k+1)|V|^k |X|^(j-2-k)]`,

where V=E[X|sign], W=X-V and h is constant on each sign class. The discarded
linear term has zero conditional expectation. For unsigned h the remainder
polynomials T3,T4,T5 are nonnegative. Their maxima on the actual support and
conditional-mean rectangle are L3,L4,L5 at `kernel.py:211–217`.

Let `smin=min(l(1-l),u(1-u))` and include 1/4 in `smax` precisely when
the closed panel crosses 1/2. The binary moments are
`rhoB=(1-2s)/sqrt(s)`, `M4B=1/s-3`,
`eta5B=(1-4s+2s²)/s^(3/2)`.
Each decreases toward p=1/2. The binary signed-third magnitude is bounded
at the p endpoints. Upper roots and positive factors enlarge these binary
ceilings. The exact variance factors are `(1-theta)^(3/2)`,
`(1-theta)^2`, `(1-theta)^(5/2)`; replacing the first by 1-theta and the
last by `(1-theta)^2` weakens upper bounds. Substitution theta<=Theta is
licensed by the **explicit** gates L3>rhoB,gammaB, L4>2M4B and L5>2eta5B.
These gates are mathematical hypotheses checked at each call, not mere
comments about likely parameter sizes.

The source intersects these ceilings with radial M4 and eta5 bounds and
Pearson `|gamma|<=sqrt(M4-1)`. Its Beta is an absolute-beta ceiling:
the conditional signed-second identity gives
`|beta|<=betaB+(1-betaB)Theta`. Later inherited `row['beta']` is required
to have this same absolute interpretation. Its signed lower export is
instead `beta>=1-2u-2(1-u)Theta`; both adverse endpoints follow because
the expression decreases in p and Theta for Theta<1.

The lower fourth/fifth moments at `kernel.py:239–240` use the opposite
endpoints: smax, upper Theta, lower roots in positive factors and upper
roots in positive denominators. No sign-dependent moment minimum is
silently used as a ceiling.

This block contains no division by theta. At theta=0 the exact conditional
variance measure vanishes; X=V almost surely and the signed error terms
become zero. All binary moment and geometric formulas still have the
required limit because 0<l<u<1 and positive A/B are retained. The separate
joint d_Y/lambda simplex needs its stated r=0 convention; no division by a
zero residual is made in the present local-panel exports.

## 4. Signed K1, the reserve gate and full quadratic extrema

For V, direct substitution gives

`K1(V)=-K(p,v)`,
`K(p,v)=(1-2p)*[(3v³/2-v²)/(pq)-3v³+v²+3v]`, `v=1-theta`.

For v>=2/3 the reciprocal coefficient is nonnegative, the remaining
bracket is positive and K decreases in p. The bracket's v derivative is
at least `9v²-6v+3>0`; hence its signed v monotonicity depends on 1-2p.
Both v endpoints are kept at both adverse p endpoints. This covers p=1/2
and panels on either side. If the v gate fails, the code uses the direct
triangle interval instead of extending this monotonicity claim.

The absolute error in `kernel.py:225` follows by bounding the signed fourth
and second residuals and using the exact factorization
`rho gamma-rhoV gammaV =rho(gamma-gammaV)+gammaV(rho-rhoV)`.
It is Theta times `L4+3+(3/2)L3(rho_upper+gammaB)`.

The signed improvement is used only on a left-half panel and when
`3 min(al,bl)>=(3/2)rhoB_upper`. Conditional cubic expansion then gives

`rho >= (1-theta)^(3/2)rhoB(p)+3min(A,B)theta >= rhoB(p)`.

That last implication uses `(1-theta)^(3/2)>=1-3theta/2` and the reserve
gate. Thus the uniform signed helper's unrelaxed rho floor is licensed.
It must not be copied into an arbitrary n25 caller without that gate;
the newer n25 helper has its separate relaxed floor.

For the exact signed Taylor error put
`F(x,a;t)=x²+2ax+3a²-3-(3/2)t(x+2a)`.
On the positive sign t=rho+gammaV; on the negative sign the error is
`-F(x,a;rho-gammaV)`. Since x+2a>0, F decreases in t. Its Hessian is
`[[2,2],[2,6]]>0`. Its maximum on a rectangle is at a corner; its minimum
is among corners, the four clipped edge vertices and the stationary point
`(3t/8,3t/8)` when inside. `quadratic_extrema` contains all those cases.
The negative class correctly reverses minima and maxima. Finally unknown
nonnegative theta gives `Theta*min(0,lower)` and `Theta*max(0,upper)`.
These are intersections of two complete valid intervals, not a favorable
combination of unrelated signs.

## 5. Outer resource, signed U and central Bernstein bound

The same residual controls both endpoint displacement and variance.
Conditional cubic expansion gives
`T+<=2m vstar DeltaB+L3 theta+`, with the reflected inequality. The simplex
rule for nonnegative resources therefore gives

`T++T- <= residual*max(vstar/[3(al+bl)], L3/K)`.

This is the maximum of prices, not their sum. Multiplication by sigma+1
and intersection with D<=d give the source's douter upper bound for
`(sigma-1)T++(sigma+1)T-`. It never creates another independent copy of
the residual. The outer signed integral satisfies
`-R*douter/[2(sigma+1)]<=J1_outer<=R*douter/4`, with SL used in the lower
denominator. The latter upper bound uses sigma-1>2.

The central polynomials are
`P1=B³/3+AB²/2-A³/6`, `P2=B⁴/4+AB³/3-A⁴/12`.
They increase in B, and their A derivative changes sign at A=B from
positive to negative. Their lower rectangle extrema are at lower B and an
A endpoint. A negative minimum is multiplied by upper m, a nonnegative
one by lower m. The central J1 upper is
`max(1/3,(2-3l)/(6l(1-l)))`: on p<=1/2 maximize at the conditional means
and use `(1-theta)^2<=1`; on p>=1/2 maximize first at A=B to obtain at
most `(2/3)(1-p)^2/p<=1/3`. The signed fourth lower/upper terms then yield
the U interval at `kernel.py:241–243`.

`central_bound:244–257` bounds `m*(rho P1-P2)` on the complete acquired
A/B rectangle. The power-to-tensor-Bernstein transform has degree four in
each variable. Its basis is nonnegative and sums to one on the normalized
closed unit square. Each coefficient z is multiplied by upper m if z>=0
and lower m otherwise, bounding every possible actual m. Thus the maximum
of these 25 values bounds the whole rectangle, including interior points,
without any stationary-point sampling. A coefficient is affine in rho;
its sign-aware endpoint product is convex in rho, and so is their maximum.
This last fact licenses the later rho endpoint cover.

## 6. General and paired envelopes, signed density and actual score

The full Fourier prerequisites remain those of the
[uniform acquisition review](code_uniform_tail_acquisition_audit.md).
The event is XX'<0 with probability 2pq, and its separation is at least
both A+B and sqrt(2-d). The HIGH caller uses their maximum and a lower
event probability; it retains the complete frequency bound installed by
`high_window_core.install`. The general LOW is always computed. Paired LOW
is an optional second valid upper estimate; failure of its eligibility
test does not exclude a law or silently return a smaller number.

The general constant at `kernel.py:267` has the signed coefficient bound
`rho M4/2-eta5/4+(3/2)beta gamma-rho/2`. Here rho>=1 makes the remaining
M4 coefficient rho/2-3/8 positive. The improvement
`max(0,eta5_lower-(3/2)M+.5)/4` is valid simultaneously with
`eta5>=(3/2)M4-.5`: before substituting M4<=M, the entire upper expression
is nondecreasing in M4. Consequently subtracting this improvement from
the common M expression is sound; it is not subtracting an independently
maximized loss from an unrelated maximum. Central and outer J costs use
the complete bounds from section 5 and the signed beta/gamma product is
upper bounded by Beta*g.

The general phase curvature uses a potentially negative gamma floor.
Since `gamma>=(79/25)rho-3-d` and rho>=1, its negative part is at most
`max(d-.16,0)`. For density in `[phi_lower,.4]` this gives the explicit
adverse term `-(.4-phi_lower)*max(d-.16,0)/2` at `kernel.py:268`.
It prevents multiplying a negative gamma by an unjustified lower density.
The paired branch instead explicitly proves gamma>=gl>=0, so that branch
does not need this coarse negative correction.

For every fixed nonnegative h=|H| the necessary envelope is convex
separately in C and rho. The signed linear rectangle is a maximum of
affine expressions in C, multiplied by h>=0. The central Bernstein maximum
and outer squared-price maximum are convex in rho; all remaining rho
terms and Q are affine. Positive C preserves that convexity. Thus four
C/rho corners cover the continuous rectangle before maximization in h.
The conserved-phase coefficient is added exactly once. Its positivity and
that of total Q are explicitly checked. Completing the square gives the
displayed raw or conserved bound; no score grid or omitted H tail is used.

The paired branch requires `u<1/2`, M<=2, g<=1, the reserve in section 4,
`0<=gl<=g`, `M-1-gl²>=0` and the actual-radius Pearson gate. Its rmin is
recomputed by the same paired function for the LOW coefficients, all four
corner rho values and final exports. The program does not substitute a
stronger rho floor only at the phase stage. The complete paired norm/Mills
derivation is in the preceding uniform review; it is not re-proved here.

## 7. Ordered local iteration and exports

At `local_panel_core.py:32–55`, each of the 24 or 32 outer iterations:

1. refines geometry using the acquired d and the same p panel;
2. intersects moment ceilings with inherited same-law rho and |beta| caps;
3. computes distinct raw and conserved upper envelopes, and optionally
   intersects them with complete paired estimates;
4. excludes only a strictly negative conserved upper budget, otherwise
   rounds new raw and stored d upward and intersects them with old bounds;
5. carries the newly valid A/B/Theta into the next finite step.

The moment rectangles computed before an inherited rho intersection remain
valid upper/lower rectangles afterward; retaining some weaker old eta or K
bounds is safe. The old raw ceiling supplies the density during the current
step. Its proposed improvement is not used to prove itself. The stored d
continues to mean `n_actual D<=N d` by the conserved-budget argument in
the INITIAL review, including the nonnegative-budget condition before any
floor substitution. One law cannot move to a different p panel mid-loop.

The final weighted theta, inward-coordinate and lambda exports recompute
the residual using the newly accepted d and final valid geometry. They
retain the N factor through `n_actual D<=N d`. The source's variable n=47
in `lambda_max=N*pq_max*theta_weighted/(1-Theta)` is therefore a floor;
it is not the unjustified claim `n_actual theta<=N Theta`.

Only a successfully checked paired context exports raw/budget quadratics.
For H>=0, `Fplus=max(C K1+phi U)+slope`; for H<=0,
`Fminus=-min(C K1+phi U)+slope`. They can be signed. The threshold-root
formula remains valid with a negative F because the exported constant A
is checked positive and Q>0. A positive root then bounds h>=0. The raw Q
and conserved Qbudget are different fields; Qbudget already includes the
phase price. A downstream comparator must not subtract that price again.

## 8. Literal covers and acyclic support changes in the inspected callers

These are source/candidate domain facts, not newly evaluated exclusions.
The original INITIAL candidate has 35 nonempty panels indexed 25–59,
covering [.25,.60]; the other 65 are marked empty. Interpreting that fact
requires the complete INITIAL replay and the arguments in the INITIAL note.

| Source caller | Literal domain and completed scope of this source read |
| --- | --- |
| `accept_central47.py:22–47` PREP | Ten closed .01 panels [.38,.48], each using its original INITIAL parent. The selected last panel [.47,.48] must be genuinely excluded; the first nine carry bounds. |
| `accept_central47.py:48–81` INPUT | Forty-five closed .002 panels [.38,.47], parent index `j//5`, actual support radius 2.5 required separately. It checks all four corner coefficients, both signed phase limits and independently weighted resources. |
| `accept_complement47.py:10–34` | Exactly indices 125–189 and 240–299, each `[i/500,(i+1)/500]`, covering [.25,.38] union [.48,.60]. Its permitted historical survivors have indices 145–189; its output is a resource table, not a local-domination conclusion. |
| `accept_left_input47.py:15–42` | Requires all 45 previous survivors 145–189 at actual support radius 3. Six left-edge panels 145–150 must be excluded; the 39 remaining target panels cover [.302,.38]. |
| `accept_confined_feedback47.py:29–78` | Forty-five original central p panels [.38,.47]. Both confinement signs, p/indices/amplitudes and the same weak input are bound before deriving a new radius and refining. |

These covers retain their shared endpoints. PREP's excluded [.47,.48]
connects central and complementary pieces; a union proof cannot simply
drop that closed strip. Similarly [.29,.302] requires the six explicit
left-input exclusions. Neither the central nor left code alone covers the
entire initial probability range. Subsequent local comparators, LEFT270,
Sperner feedback and the final union are separate source/certificate jobs.

For confined feedback, write `X=(B0+U-p)/sqrt(pq+s)`, s>=0. Acquired
`|U|<=a` gives
`|X|<=max(u+a,1-l+a)/sqrt(min_panel pq)`.
The denominator deliberately discards s>=0, so this includes zero noise.
The fixed caller rounds the radius upward, adds a positive grid margin,
and verifies both sign conclusions of the confinement certificate. The
new radius lies in a separately named 1<=R<=6 kernel domain. Radial
moment ratios are increasing for every R>=1; conditional Taylor and the
central rectangle require no old R>=2.3 lower bound. The only formerly
automatic paired gate R>2g is now explicit. This is a coherent **acyclic**
route: weak INPUT at R=2.5, independently proved confinement, contracted
actual support, then stronger feedback. Reusing its final feedback as the
premise for that same confinement would be circular and is not justified.

The standalone caller hashes identify candidate/predecessor files; they do
not themselves establish that those predecessors have been freshly acquired.
For example INPUT shape-checks PREP and reads its target values, while a
larger proof join must provide PREP's full arithmetic result and support
contraction. That is an explicit conditional boundary, not evidence that a
matching historical JSON is an unconditional theorem.

## 9. A dormant bootstrap is deliberately not covered

`kernel.general_geometry:179–193` is a **different** coarse bootstrap from
d alone. Among other quantities it uses `29/5*min((104/25)al,(54/25)bl)`
as a variance denominator. Its call sites found in this selected archive
are the older `entry/chain_core.py:45` and its propagation copy. They are
not in the 41 selected retained-job entry points; live local-panel calls
initialize from an acquired p/Theta row instead.

This note has not supplied the separate quantitative derivation of that
29/5 bootstrap, nor of every early `initial_cell`/old chain profile. The
shared simultaneous-budget coefficient in section 2 alone should not be
silently substituted for its stronger-looking denominator. This is an
**unreviewed distinct rule**, not a confirmed invalid inequality or a
counterexample. A later task that selects those older callers needs the
bootstrap argument and its full domain. AST equality with an unreviewed
n25 helper would not discharge it.

## 10. Remaining obligations and conclusion boundary

The inspected live formula atlas and finite update have coherent
conditional directions, including signed beta/gamma, closed p seams and
zero-noise faces. That result remains subject to the following obligations:

* fresh complete arithmetic and execution/source/evidence acceptance for
  each selected INITIAL/resource/support/confinement job;
* actual same-law predecessor acquisitions, unrestricted attainment/contact,
  exact oriented identities and named published analytical inputs;
* the separate support-ray/confinement proofs and their final joins (only
  their geometric **implication and acyclic ordering** were read here);
* later signed-resource, LEFT270/Sperner refinements and all local comparator
  coverage and supremum/asymptotic descent arguments;
* the dormant coarse-bootstrap/older-chain profiles in section 9 and any
  nonselected finite-index source variants.

No historical PASS, code identity, completed source review or coherent local
state is promoted to an unconditional all-index proof. The review records
specific algebra and domain coverage for outside checking, with the remaining
source and certificate boundaries explicit.
