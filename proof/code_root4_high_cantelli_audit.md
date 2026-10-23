# ROOT4 sign-count Cantelli, closed high cuts and the cheap LOW leaf

24 October 2026. This is a fallible internal AI source and hand-algebra
review, not external independent mathematical verification or formal
verification. No original mathematical module, numerical kernel or test
was imported or executed. The [source map](code_root4_high_cantelli_source_map.json),
SHA256 `c6dfcaed46902cfe810b77b4db8cbe4f32933d73189dbdd1ae09473202c82251`,
records 32 selected functions in ten members. Their selected function
ASTs agree between vendor and actual notebook11 sources. All ten actual
hashes match the 70-source-pin completed receipt, SHA256
`571bc91b257ac53c640dd3bee91377565ff7c475091d39076295200209beeae1`.
Hashes bind the inspected sources and do not prove their inequalities.

This unit complements the [outer closed cover](code_root4_closed_cover_audit.md),
[common-defect ledger](code_root4_common_defect_interval_audit.md),
[linked center and interval cache](code_root4_linked_center_audit.md),
and [radius/lens](code_root4_radius_two_disk_audit.md) reviews. It does
not declare unrestricted C4 or an all-index conclusion.

## 1. Actual sign convention and conditional moments

For any standardized centered iid law P put
`u=E X_+=E X_->0`, `v+=(1+beta)/2`, `v-=(1-beta)/2`.
The backend's p is `P(X>=0)`, including all zero mass, and q=1-p is
`P(X<0)`. Both are strictly between0 and1. Cauchy implies

    w(1-beta)/2 <= p <= 1-w(1+beta)/2,
    u^2=w(1-beta^2)/4.

Given J=j nonnegative sign labels, the sum has the distribution of j
independent nonnegative conditional draws and 4-j negative draws.
Exchangeability removes the irrelevant ordering of labels. For
`Z=(X1+...+X4)/2` its conditional mean and variance are

    mu_j=u(j-4p)/(2pq),
    V_j=[j(v+/p-u^2/p^2)+(4-j)(v-/q-u^2/q^2)]/4.

These are the source formulas. No atom-count, support or extra fourth-
moment assumption is needed for this HIGH backend. Under reflection
beta changes sign and p is recomputed for the reflected law. In general
`P(-X>=0)` is not1-p when zero has mass; the code does not use that false
identity.

For a conditional variable of mean mu and variance V, Cantelli's closed
lower-tail bound for H<mu is `V/[V+(mu-H)^2]`. For V>0 it follows by
Markov applied to `(Y-mu-V/(mu-H))^2`; V=0 is deterministic. At H>=mu
the safe bound is1, including the equality atom. These are exactly the
source's two branches and its separate V=0 case.

## 2. Necessary cuts and whole-cell moment bounds

For a closed p cell [pL,pU] and original w lower wl, the two Cauchy
inequalities imply

    beta >= 1-2pU/wl,
    beta <= 2(1-pL)/wl-1.

Intersecting with the original signed-beta interval gives blo,bhi.
Those inequalities also imply
`w<=min(wh,2pU/(1-bhi),2(1-pL)/(1+blo))`.
All denominators are positive. Strictly reversed intervals or an upper
w bound strictly below wl prove emptiness. Equality and shared faces
remain. These are necessary outer cuts, not corner-feasibility claims.

The local u interval comes from monotone exact squares. The local rhoQ
lower uses the upper w face and minimum absolute beta, including beta0
if its signed interval crosses zero. Its lower root is rounded downward
and may be intersected with the independent rhoQ>=1 fact.

For fixed u, mu_j decreases in p. Its derivative numerator is
`j(1-2p)+4p^2=4(p-j/4)^2+j(4-j)/4>=0` for j=0,...,4.
The whole-cell lower therefore uses pU and the u lower or upper endpoint
according to the sign of j-4pU, then floors it.

For fixed p,beta, V_j decreases in w. At w=wl it is convex in beta,
with nonnegative quadratic coefficient
`wl*[j/p^2+(4-j)/q^2]/16`. Its maximum over beta is at one of its
two faces. For fixed v,u^2 the sign variance
`v/r-u^2/r^2` has its maximum at r=clamp(2u^2/v), since its derivative
has sign `2u^2-vr`. The source applies these two separate p/q interval
maxima at the SAME beta endpoint, forms the weighted V_j upper there,
then takes MAX over the two beta endpoints. This is conservative even
though the independent maximizing p and q need not occur together.
It does not mix opposite-sign maxima from different beta endpoints.

If any resulting V_j upper is strictly negative, the entire cell has
no actual law: all five conditional variances must be nonnegative, and
every J=j has positive probability for0<p<1. This emptiness argument
does not assume the numerical corner parameters are laws. Otherwise
the upper variances are ceiled. With means in scale units and variances
also in scale units, the integer fraction
`ceil(V_int*scale^2/[V_int*scale+gap_int^2])` has the correct units and
outward direction.

## 3. Joint probabilities and closed threshold coverage

The five Cantelli bounds Aj are fixed nonnegative constants on a whole
p/H cell. Write p=pL+t(pU-pL). Realize each of the four Bernoulli trials
by independently choosing its success probability pU with chance t,
and pL otherwise. Conditional on exactly r upper-probability choices,
the distribution of J is the source's mixed Bernoulli convolution.
Therefore the binomial expectation is a degree4 Bernstein combination
of the five mixed expectations. Its maximum is bounded by their MAX.
This proves the source's joint envelope without assuming monotonicity
in j or separately maximizing each binomial mass.

The 25 mixed masses are exact nonnegative Fractions and are ceiled
once. Positive Aj multiplication and the final ceiling preserve the
upper bound; the independent CDF<=1 cap is valid. For H in a closed
cell [HL,HU], the upper CDF uses HU and the Gaussian lower uses HL.
Monotonicity covers both endpoints and the interior with no H
interpolation reserve. The integer Gaussian recurrence encloses every
integrated Taylor term by floor/ceil, alternates endpoint signs and
adds the61st integrated term as a symmetric remainder. For |H|<=2 the
exact integrated terms decrease; their consecutive ratio is at most
2/3. The negative-H reflection has the correct endpoint order.

The raw maximum is initialized at0, so every retained raw_i is
nonnegative. Dividing by the local lower `rhoQ_i_lower+eta_lower` is
therefore safe. This differs from signed LOW numerators, for which the
separate four-denominator-face argument was required.

For H<=-2, global Cantelli and mean0/variance1 give
`2(F_Z(H)-Phi(H))<=2/(1+H^2)<=2/5`.
For H>=25/16, `F_Z<=1` and the Gaussian witness
`Phi(25/16)>4/5` give raw<2/5. Both signed-beta boxes are covered with
their own p intervals. The atom-safe identity

    Phi(H)-F_Z(H) <= F_(-Z)(-H)-Phi(-H)

then bounds the other discrepancy; it uses `F_Z(H-)<=F_Z(H)` rather
than assuming a continuous CDF. The conditional count method thus
retains zero atoms and closed-CDF equality correctly.

## 4. Root pruning and the two complete HIGH alternatives

The CPU backend directly recomputes all required signed-p/H rows and
explicit empties. The frontier checks every orientation/index exactly
once before pruning. From each row's necessary local w/beta rectangle
it computes the exact rhoQ minimum SQUARED. Only
`rhoQ_min_square>=(46/25)^2` proves that class impossible for every
eta>=0 under the strict physical `rhoQ+eta<46/25` premise. Equality is
also impossible. Rounded rho lower bounds, difficult raw estimates and
backend UNKNOWN status do not justify a deletion. The global tail's
denominator is not replaced by a denominator from retained p classes.

At a fresh backend call with eta_lower0, raw_i and the Cauchy cuts do
not depend on eta. Hence for each retained class,
`R4<=raw_i/(rhoQ_i_lower+eta)` at all feasible eta>=0. Taking the maximum
of `raw_i/T-rhoQ_i_lower`, the analogous global-tail expression and0
gives a sufficient non-strict cut. The source rounds that cut upward
to its exact rational grid and adds1/10000, which makes the complete
Cantelli route strictly<T on and above its recorded closed cut.

The independent SV route imports the separately reviewed iid envelope
`R4<=.3031*(1+.646/rho)`; see [literature inputs](literature_inputs.md).
This unit does not reacquire that external theorem. Its exact threshold
is `rhoSV=.3031*.646/(T-.3031)` and its cut is
`max(0,rhoSV-rhoQ_box_lower)`. At the closed boundary the route gives
<=T, sufficient because the separate exact target certificate has
T=4097/10000<CE. No artificial reserve is needed for that route.

Selecting the lesser of the two COMPLETE cuts is valid. It does not
combine p/H contributions from Cantelli with contributions from SV.
The HIGH proof covers eta on and above the selected cut. The LOW request
retains [0,cut], including the shared face. If the cut is0, HIGH already
covers eta0 and every actual eta>=0; skipping the LOW producer is valid.
The original backend's older target only affects its diagnostic status,
not its valid raw rows; the frontier uses those rows at its own exact T.

## 5. Actual cheap LOW route

The actual CPU cheap producer directly invokes the corrected linked
center reviewed in the previous unit. It keeps the whole-box maximum
of normalized centers over every H and both reflections. Complete ABS
transfer and the continuous-frequency H reserve are independent of H,
so taking that maximum before adding these bounds is conservative.
It uses the separate uniform physical quadrature reserve.

On each of the16 adjacent closed eta cells the affine target polynomial
is `M+quad+Hreserve+2C+(2D-T)*eta`. M already bounds C_Q-T*rhoQ, so
T*rhoQ is not subtracted again. The complete transfer is nonnegative on
both faces. Strict degree1 Bernstein negativity equals endpoint
negativity; the sign-safe four-denominator-face score covers either
numerator sign. The source ignores the old dummy ABS acceptance/score
and uses only its proved transfer coefficients.

The pure postconsumer rederives the complete transfer, curvature,
normalized polynomial, endpoints, Bernstein coefficients and score for
all16 cells after the actual direct producer. It preserves every failed
cell. Its explicit cut override changes a local interval-label slot
only; it does not establish any above-cut theorem. That theorem comes
from the separately checked HIGH record. The outer parent-or-all-four-
children composition is treated in the closed-cover review.

## 6. Limited outcome

No confirmed sign, zero-atom, units, pruning, endpoint or quantifier
defect was found in this selected HIGH/cheap-LOW scope. The imported
binary certificate's Gaussian helper was read; its unrelated binary
producer was not inferred sound from being imported. Old timed full-
root/frontier producers are not the active CPU path reviewed here.

Together with the earlier inner units, this supplies a bounded
conditional source derivation for the actual selected LOW signed and
cheap routes and HIGH count/frontier arithmetic. A completed finite
receipt alone does not establish the all-law first-critical localization,
support and attainment, the external iid envelope or the closed-CDF
majorant. Those upstream implications and the outer whole-root joins
remain separately identified proof obligations. No original mathematics
was rerun locally and no native-resource, all-law C4 or all-index flag
is promoted by this review.
