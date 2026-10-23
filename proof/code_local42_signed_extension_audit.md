# Distinct LOCAL42 extensions: signed Gaussian correction and joint-noise cells

Date: 23 October 2026. This is a fallible internal AI source and hand-algebra
review, not external independent verification, formal verification or fresh
arithmetic acceptance. No archived mathematical module, constructor,
normalizer, gate or acceptance routine was imported or executed. Only
source/AST/text/JSON/byte checks and the derivations below were used.

## Bounded source result

This unit inspects the distinct LOCAL42 changes relative to the previously
reviewed uniform47 comparison: joint-noise gap substitution, localized
binomial mass, harmonic constant 4.553, the new signed Gaussian upper
correction in LEFT42 LOW, the corresponding signed MID derivatives,
noise-endpoint convexity and the source's curvature cache. No invalid
inequality was identified in those inspected extensions. This is **not**
a full audit of every LOCAL42 normalization, count-event/Poisson/quartic
primitive, acquisition callback, scalar/decrement branch or final union.

The original source is in `closure31.zip`, whose previously verified
transport pin is 135,288,952 bytes, SHA256
`68eb555e08ee7509f9d136df6fae5e354aff816ec4f77cc8426698c479b205a0`.
This unit did not repeat that large transport hash. Its actual selected
member bytes were hashed afresh and compared with the historical final
`continuation_20261010/repair31/EVENTUAL_CUTOFF31_COMPOSED.json`
`files_sha256` map where supplied. That historical graph itself states
`fully_reproduced_historical_dependency_DAG=false`.

Set
`W=BE_cutoff35_release_20261007/work/cutoff40_release_20261007/work/toward40_20261007/`
and `B=W/audit43/capsule/work/below49_20261006/`.
All following paths are relative to B. The
[source map](code_local42_signed_extension_source_map.json) records actual
pins, ranges and map-match status. Source filenames containing LOW47 are
legacy names; the actual fixed contracts here set N=42.

The two selected whole-count kernels are genuinely different:

* `local/central42_v2/central42_kernel.py`, SHA256
  `9dc0754fe2dd4f2f7057247d3d62f3b71472c65a49d46f67d35fb0d66e3f8673`,
  keeps the earlier coarse Gaussian correction;
* `local/left42_final/central42_kernel.py`, SHA256
  `d025529aa2690c3cfc0f1c34a6af385d6fa69db8e069543057f29475cbb133c3`,
  uses the new signed correction below and includes the noise-band index
  in its phase cache key.

Their complete source difference was inspected. The mathematical extension
texts are `local42_improvements.tex` and `local42_signed_gaussian_v2.tex`.
The former's general Gaussian lemma alone does not describe the sharper
selected LEFT42 negative-phase implementation.

## 1. A joint physical input, not two unrelated ceilings

For the same actual law, let Y=B0+U, E[U|B0]=0, p in [l,u] subset (0,1/2),
v=p(1-p), s=E U², lambda=n s, and ell=(v+s)^(-1/2). Let d denote its
inward-coordinate gap. The source installs `joint_d0` and `joint_lambda`
from a proposed/acquired row. It requires the physical statement

`d/d_star+lambda/Lambda<=1`, with positive intercepts.

Separate upper bounds d<=d_star and lambda<=Lambda do not imply it.
On a closed noise band [L,U], the actual joint statement implies
`d<=d_L=d_star*(1-L/Lambda)`. Source LOW then recomputes c=1-d_L,
the displacement/variance prices, cubic correction and the conditional
characteristic-function span. MID recomputes its d at the same lower
noise endpoint. These operations are valid provided the row's **joint**
resource has actually been acquired for that same law.

Its derivation from a shared gap residual is available in manuscript
2591–2629 and the weighted-resource review: intercepts derived from the
same residual and coefficients satisfy the simplex inequality, and enlarging
either intercept outward is safe. This unit has not traced every actual42
acquisition row back to those common coefficients. A row name, or running
the two independent scalar bounds, must not substitute for that edge.

The whole-count displacement price follows from
`D>=m ell²[(6+2sigma)(p-p*)²+6d(1-d)]+beta_price*theta`.
Indeed the joint gap expansion has the displayed binary square and
`6m(A+B)(DeltaA+DeltaB)`; here A+B=ell(1-d) and the displacement sum is
ell*d. Dropping its extra nonnegative product weakens the bound. Thus
using d_L in `alpha=6*m_lower*ell_lower²*(1-d_L)` raises a necessary
positive price legitimately; it does not manufacture another residual.

## 2. The actual count stays fixed in the Gaussian integral

Let the actual threshold be x=np+h=k+u, where h=H/ell, k is a nearest
integer, |u|<=1/2 and delta=k-np=h-u. Define

`f(t)=[Phi((delta+t)/sqrt(n(v+s)))-Phi(delta/sqrt(n(v+s)))]/pi_k`.

When differentiating/integrating in t, the actual k and delta are fixed.
The whole-count identity needs the **upper signed** correction u-f(u),
not an absolute error and not the derivative obtained by changing k with t.
Assume the already proved global Stirling segment gives

`sqrt(n)pi_k=phi(0)/sqrt(v)*exp(-delta²/(2nv)+zeta)`,
`n|zeta|<=Z_N(D)`, |delta|<=D.

The actual kernel computes H/ell and delta corner intervals for the full
signed H and u cells. Division by a positive scale has its extrema at
corners. Its dd bounds |delta|; `dpositive` separately bounds delta_+.
These two quantities are not interchangeable in the signed cubic repair.
The global normalizer's count-segment gates, including delta_global>
H/elo+.5 and mode/count positivity, remain necessary even if local dd is
less than 1. The source's localized mass is not a new Stirling proof on
a too-short segment.

## 3. Positive phase: a lower derivative gives an upper signed correction

The exact logarithmic derivative is

`log f'(t)=-.5 log(1+s/v)+delta²/(2nv)
                         -(delta+t)²/(2n(v+s))-zeta`.

For 0<=t<=u, log(1+s/v)<=s/v gives
`log f'(t)>=-[lambda+2delta*t+t²]/(2nv)-zeta`.
The convex quadratic in t is maximized at 0 or u, while actual
delta=h-u is held fixed. Hence its maximum is
`max(0,2h*u-u²)`. On u in [a,b], h<=h_cap, its upper bound G+ is obtained
at the projection of h_cap onto [a,b], intersected with zero. Therefore

`u-f(u)<= b/n*[lambda/(2v_lower)+G+/(2v_lower)+Z_N(D)]`.

The source implements this at LEFT42 LOW lines 181–186 and the signed
positive MID branch. Both signs of H are covered without reflecting the
law. For negative H it is safe to weaken h_cap to zero. A negative
derivative improvement is not used: it must pass its positive domain gate
before being intersected with an older valid derivative bound.

## 4. Negative phase: variance cancellation is conditional and explicit

Write u=-r, 0<=r<=b. Then

`log f'(-t)=-.5log(1+s/v)+delta²*s/[2nv(v+s)]
                            +(2delta*t-t²)/[2n(v+s)]-zeta`.

Using log(1+x)>=x/(1+x), the first two terms are at most
`s/[2(v+s)]*(delta²/(nv)-1)`. They can be dropped for an **upper**
derivative bound only when D²<=N*v_lower. LEFT42 checks the stronger
strict gate `N*v_lower-dd²>0` before doing this. Omitting that gate would
leave a positive uncharged variance correction.

Since delta=h+r<=h_cap+b, the remaining numerator is at most
`G-=max_{0<=t<=b}(2(h_cap+b)t-t²)`.
Its maximizer is `clip(h_cap+b,0,b)`; G->=0. Put
`eta=G-/(2v_lower)+Z_N(D)`. For eta<N,

`f'(-t)-1 <= eta/[n(1-eta/N)]`,
`u-f(u)<=b*eta/[n(1-eta/N)]`.

The source checks eta<N and uses the clipped vertex even when h_cap<0;
replacing it blindly by the endpoint b would be unnecessarily weaker.
LEFT42 MID uses a valid coarser vertex with max(0,h_cap) and intersects
the improved upper derivative with its old upper bound. The sign in
`u-f(u)=integral_0^r(f'(-t)-1)dt` matches the code's upper derivative
for the negative-phase own-event minorant.

## 5. Noise endpoints, negative event bracket and all-index signs

After division by lambda>0, the new Gaussian correction has form
`A+B/lambda`, A,B>=0: on positive phase A=b/(2v_lower), while on negative
phase A=0. The source rejects a phase cell crossing zero and explicitly
rejects negative A or B. Zero itself is a shared closed phase endpoint.

Within a fixed full noise/phase/H box, the other selected resource and
kernel enclosures are frozen. The event bracket has a positive reciprocal
of an affine positive lambda denominator plus affine/constant terms, hence
is convex in lambda. Its negative endpoint gates imply it is negative on
the entire closed noise interval. Only **then** may a lower binomial mass
be used to form an upper score: multiplication by a negative bracket
reverses the favorable mass direction.

The complete inverse-index correction is K+A+B/lambda. It decreases with
lambda. Its positivity gates at both endpoints (in particular the upper
endpoint) license replacement 1/n<=1/N throughout the interval. Its sum
with the mass-weighted event bracket is convex in lambda; two strict score
endpoint gates therefore cover the whole interval. A negative correction
cannot simply be divided by N in the adverse direction. The source retains
that independent sign gate and also uses delta_+ for the signed repair.

This checks the new signed-Gaussian insertion and endpoint argument, not
the complete marked-event, common-background, quartic, Poisson or tail
comparison underlying the original event bracket.

## 6. Localized mass and the harmonic improvement

For a smaller phase cell with |delta|<=D, the same global Stirling formula
gives

`sqrt(n)pi_k >= (.39886/sqrt(v_upper))
               *(1-[D²/(2v_lower)+Z_N(D)]/N)`.

It follows from exp(-x)>=1-x, with nonnegative x. A negative right side is
still a lower bound; the source takes its maximum with a previously positive
mass bound and checks positivity. All entropy/log-variance/factorial
constants still come from the acquired **global** count segment. This is
why a cell-local D<1 causes no mode-coverage defect.

The stronger harmonic price uses `1-cos(2pi*x)<=4.553*x` for x>=0. For
x>=2/4.553, the bound 1-cos<=2 suffices. On the remaining interval the
degree-14 alternating polynomial is an upper bound; directed pi coefficients
enlarge it further. Positivity of the resulting degree-13 polynomial in
the Bernstein basis on all 64 closed subintervals proves the claim at every
point, including zero by continuity. It is not a collection of sampled
cosine values.

The proof names `check_harmonic4553.py`, which is absent by that filename
from the supplied closure. The actual supplied equivalent checker is
`entry/local_audit/check_harmonic_interpolation.py`, SHA256
`efe03f77beaa6af7897d14c2d583b0b7c5def96f8ae649a29c44f697f29acebf`.
It recovers all 896 Bernstein coefficients by exact interpolation with
14 rational nodes and Gaussian elimination, so it checks a whole degree-13
polynomial, not positivity at those nodes alone. Its pi/tail and false-slope
controls were source-read, not executed. This is a concrete source-reference
correction. A fresh acceptance needs that actual strict polynomial check
or an explicit equivalent derivation; historical minimum-coefficient prose
does not acquire it.

Replacing 5/23 and 5/46 by 1000/4553 and 500/4553 then follows from the same
characteristic-function/expected fractional-part argument. The retained
Taylor gain is evaluated at the lower noise endpoint only under the
`rate*high<3` gate: its derivative has the sign of
`240-90x+24x²-5x³`, which decreases and stays positive on [0,3]. Thus the
source's lower-endpoint gain remains a lower bound on the whole band.

## 7. Joint-gap characteristic rate and the actual cache difference

On each band the conditional noise support span is at most amplitude+d_L.
The sine lower polynomial with positive small argument gives a valid new
characteristic rate for this smaller span; the source recomputes it with
the same d_L and takes its maximum with the older complete valid rate.
The cubic repair and all c-dependent tail prices are recomputed too.

The central42 cache key omits the band index. This is conservative for
the actual ascending-noise traversal: d_L decreases and c=1-d_L increases.
The cached denominators `(c-u)^2` and `(c+min(u,c/3))^2` increase on the
checked positive domain. Their nonnegative numerators depend only on the
fixed p/H/phase key and are unchanged, so an earlier cached upper bound
remains an upper bound. All other c-dependent quantities are recomputed.
The selected LEFT42 implementation instead includes bi in its cache key;
it does not rely on reuse across changed c at all. These implementations
must not be conflated simply because their filenames match.

## 8. Actual selected phase domains and the remaining boundary

The fixed central resource contract has 47 closed p cells [.38,.474] and
LOW starts at lambda=.05. Its four MID complements have phase starts
.09,.14,.19,.29. The fixed LEFT42 contract has 45 p cells [.29,.38] and
LOW starts at .08. Its MID starts are **0,0,.19,.27** on the four noise
bands [.05,.06], [.06,.08], [.08,.10], [.10,.12]. Both phase signs are
checked on complete .001 subintervals, including zero in the first two
bands. The shifted-quartic own-event formulas contain no division by phase;
their sign witnesses and positive noise denominator gates remain required.
Thus this full-phase MID route can close [.05,.08] while LOW starts at .08;
it is different from the later tail47 positive-extra-LOW partition.

Zero noise remains the separate Bernoulli case. The full tiny/normalizer
implementation, all local comparison primitives, physical joint-resource
and amplitude acquisitions, exact scalar/index/decrement branch union,
fresh full arithmetic and global joins remain outside this bounded extension
review. The source's fixed resource filename `actual_float_targets.json`
does not by itself disprove its exact rational arithmetic, and does not
acquire those target hypotheses either. No unconditional finite42–48 or
all-index conclusion is established here.
