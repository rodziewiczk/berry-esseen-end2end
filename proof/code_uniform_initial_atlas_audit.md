# Uniform INITIAL: signed moment atlas and ordered feedback

Date: 23 October 2026. This is a fallible internal AI source and hand-algebra
review. Cross-reads by other model agents are checks within the same system,
not external independent verification or formal verification. No archived
module, mathematical evaluator, constructor, forest or acceptor was imported
or executed. The work used original bytes, text/AST/JSON checks and symbolic
arguments written below. Archived statements that a replay passed are inputs
to this review, not fresh arithmetic acceptance.

## Scope and bounded finding

This note follows the complete selected 153-line `entry/local_signed_core.py`
INITIAL stage, its fixed `accept_initial47.py`, and their original proof text.
It extends the [uniform heat/Fourier review](code_uniform_tail_acquisition_audit.md)
with the signed moment necessary predicates, the passage to a true central
gap, continuous score maximization, ordered raw/defect feedback, and the final
closed probability export. No unsound inequality or missing part of that
specific continuous cover was identified in this read. This is a conditional
code-to-lemma conclusion; it is not a certificate replay or an acquisition of
INITIAL47, support, the score cap, or a cutoff theorem.

The subsequent `local_panel_core.cell` and the full general-geometry resource
atlas are a separate unit. Their weighted-resource formula is traced in
section 9, but this note does not claim that every later geometry update or
its support-contraction join has been checked here. The n25 INITIAL source is
a different source instance, already treated in
[the B3/B4 atlas note](code_general_cell_atlas_audit.md); the stage counts and
normalization in this note must not be substituted into that lane.

## 1. Exact source instance and conditional statement

The archive is `BE_cutoff49_20260930.zip`, 16,660,566 bytes, SHA256
`ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e`.
Set `A = BE_cutoff49_20260930/` and
`B = A/baseline/certificates/work/below50_20260929/`. Paths in this note
are relative to B. The [source map](code_uniform_initial_atlas_source_map.json)
records actual member hashes, line ranges, the original manifest comparison,
and the manuscript identity. The source does not get its mathematical
authority from those hashes.

The selected fixed call is `entry/accept_initial47.py:12,46–62`:

* floor N=47, actual support `|X|<=3.84`, score `CE<=C<=.4247`;
* an attained oriented witness with mean zero, variance one, and finite third
  moment, carrying the same law, threshold and contact identity throughout;
* nonnegative defect D and leakage from the prior analytical identities;
* the published score caps, previously justified LOW/HIGH kernels and the
  support premise, all of which are external to this INITIAL stage.

The fixed profile has `barrier=0`, `nmax=98`. Here nmax occurs in the score
floor `.4095+barrier/nmax`; it does not impose `n<=98` on the physical witness.
The computation parameter n is the floor N. Using it for an arbitrary actual
index n>=N requires the all-index kernel damping and weighted feedback
arguments, not merely the parameter name. The selected profile's lower score
floor `.4095` is below CE, and its upper caps apply to the same witness.

Write sigma=sqrt(10), rho=E|X|^3, beta=EX|X|, gamma=EX^3,
M4=EX^4, eta5=E|X|^5, m=EX+=EX-, and
`a±=(1±beta)/2`, `b±=(rho±gamma)/2`. Initially an atom at zero is allowed.
Mean zero and variance one still force both sign classes to have positive
moments. Every local rectangle is an enclosure of these quantities for the
same law, not independently realizable moments from different laws.

## 2. Outer moment cover and support-localizing matrices

`local_signed_core.py:29,36–46` bounds rho using the two published score caps
and divides `[1,rhomax]` into 24 closed intervals. For Y=|X| the positive
measure `(Y-1)^2(Y+1/2)dP` has mass rho-1. The ratios giving M4-1 and eta5-1
are respectively `(Y+1)^2/(Y+1/2)` and
`(Y^3+2Y^2+3Y+3/2)/(Y+1/2)`. Both are increasing for Y>=0: after clearing
positive denominators their derivatives have numerators `Y(Y+1)` and
`Y(2Y^2+(7/2)Y+2)`. Consequently the displayed K4/K5 upper bounds are valid.
The further bounds M4<=R rho and eta5<=R M4 use actual support. The bound
M4<=11.1 uses R<=6 and rho<=1.85; the fixed profile satisfies this domain.

Cauchy gives `m^2<=a+a-` and `m b±>=a±^2`. Eliminating m gives
`rho >= (1+beta^2)/sqrt(1-beta^2)` and the two signed gamma constraints in
`signed_entry50_proof.tex:39–57`. The inverse beta radius at source line 39
uses upper square-root endpoints; `0<ba<1` is checked before any division by
1±beta. The gamma lower bound increases with beta, so bl is the correct
endpoint at line 44; the upper bound likewise uses bu. The common lower m is
`max((1+bmin^2)/(2 rh), a_lower^2/b_upper)`; signed third upper bounds that
are nonpositive are impossible, rather than harmless singular divisions.

The other m upper bound at line 43 follows by integrating
`(Y-a)^2(R-Y)>=0`. It yields
`2m <= (R-rho+2a+R a^2)/(a(2R+a))` for every a>0. Taking the minimum of
eleven valid choices a=.2,...,1.2 is legitimate. It is not a numerical search
for a necessary optimum. The Cauchy upper m and this polynomial bound are
intersected, with square roots rounded upward.

For each sign, put `Dsign=R a-b>=0`. The positive semidefinite matrices of
`(R-Y)(1,Y)(1,Y)^T`, then of Y times that matrix, give

`2m + sum((Rm-a)^2/Dsign) <= R`,

`c4sign <= R b - Dsign^2/(Rm-a)`.

An additional factor Y gives
`c5sign <= R c4sign - (R b-c4sign)^2/Dsign`.
These are actual support inequalities; they do not assume absence of a zero
atom. At lines 57–75, DU is an upper bound for Dsign, DL is a lower bound,
and denm is an upper bound for Rm-a. Nonnegative corrections use the
positive part of a lower numerator and an upper positive denominator.
Zero denominators contribute zero unless a strictly positive necessary
numerator contradicts them. A negative upper denominator is itself a
contradiction. Omitting a singular nonnegative correction weakens the bound;
it does not exclude a potentially singular law.

The function at line 59 is a lower bound for the required probability sum.
It uses upper a, upper DU and positive parts, hence is nondecreasing in m>=0.
If it exceeds R at the lower m, the rectangle is impossible. Otherwise each
of the 32 bisections preserves an upper feasible m; the moving lower search
endpoint is not asserted to be a physical lower m. Downward mlo and upward
mhi then cover the retained interval. The comparison here is to R; the n25
varying-radius source's separately normalized comparison to 1 is different.

## 3. Projection, signed fourth and explicit EMPTY rules

Projection of X|X| onto X and |X|, whose Gram matrix is
`[[1,beta],[beta,1]]`, gives

`M4 >= rho^2 + (gamma-rho beta)^2/(1-beta^2)`.

At lines 50–51 the residual's full multi-affine rectangle is enclosed by its
corners. `dist` is the minimum possible absolute residual. The denominator
`1-bmin^2` is an upper denominator, so the resulting expression is a lower
M4 bound. It is tested with strict `>` against M and later Mc. No equality
case is discarded. `M4>=1` and `eta5>=1` are variance-one moment inequalities.
Lines 71–76 combine these with the PSD upper bounds, using outward rounding.

The signed fourth interval is for
`K1 = E[X|X|^3]-3 beta-(3/2)rho gamma`. Source lines 93–98 first enclose the
signed fourth moment using `c4sign>=b_sign^2/a_sign` and `c4sign<=R b_sign`,
then intersect it with the sharper PSD sign bounds. Both maximum and minimum
of rho*gamma use signed corner products. The direction of the gamma-dependent
cross term is reversed in the lower K1 bound. The entire beta sign interval
is retained; beta is not silently replaced by its absolute value.

The EMPTY paths before the central-gap branch are therefore: inconsistent
gamma interval; projection lower M4 above its upper; nonpositive sign-third
upper; inconsistent common m; negative support deficit; excessive minimum
probability; contradictory first support deficit; impossible fourth/fifth
moment; compulsory D above its acquired upper; inconsistent J or K1. Later
EMPTY paths are inconsistent p, endpoint, asymmetry, U or score intervals.
Each is a strict contradiction of a necessary condition. Runtime `need`
failures instead fail the stage; they are not silently counted as exclusions.
The source cardinality check counts every dropped child multiplicity as well
as every active final child. It does not by itself prove the inequalities.

## 4. The central-gap switch and the genuine opposite-sign event

The initial pass does not assume a central gap. From
`D>=(sigma rho-gamma-6m)` one obtains the compulsory lower D at lines 45,
77–78. If zero is in the support, the earlier gap integral gives J<=rho and
therefore `D>=(sigma-1)rho`. Only the strict acquired condition
`d<(SL-1)rl` at line 80 licenses an actual gap (-A,B), A,B>0, and absence of
a zero atom. It is stronger than merely assigning two sign probabilities.

On this branch Cauchy on both sign classes gives
`p>=2 ml^2/(1+bu)` and `p<=1-2 ml^2/(1-bl)`; these bounds are checked in
(0,1). For two independent copies of the same law the event XX'<0 has
probability 2p(1-p). Its second-moment identity is

`E[(X-X')^2 | XX'<0] = (1+4m^2+beta)/(2p)
                           +(1+4m^2-beta)/(2(1-p))`.

Its coefficients are positive; it is convex in p and affine in beta.
Thus the source's endpoint maximum with upper m is an upper bound. The
alternative 2/event is also an upper bound, so their minimum remains valid.
The event lower bound combines the minimum of 2p(1-p) on the p interval
with `(1+bmin^2)^2/(2 rh^2)`, derived from common-m Cauchy. A lower event
bound, upper conditional second moment and lower gap distance are the
directions required by the previously reviewed HIGH estimate. The gap
distance follows from
`(A+B)^2 >= (rho-D/(sigma-1))/m`; its source numerator is lowered and its
denominator raised. This is not an event assembled from different marginals.

## 5. Signed constant losses, endpoints and one shared outer budget

The nonnegative loss at line 99 is the maximum of two separately valid
deductions, not their sum. First, `M4^2<=rho eta5` and the projection give

`rho M4/2-eta5/4 <= rho^3/4
                 -(gamma-rho beta)^4/(4rho(1-beta^2)^2)`.

Second, applying `c4>=b^2/a`, `c5>=c4^2/b` sign by sign and completing a
square gives the two signed positive-part losses displayed at
`signed_entry50_proof.tex:86–102`. The code lowers their numerators, raises
their denominators, and clips a possible negative lower b to zero. The
manuscript has an additional weighted loss at lines 2822–2835; this source
uses only the two weaker valid strategies. It must not be described as
computing that extra loss.

The earlier charge at line 100 uses the negative-gap function bound at
`kernel.py:88–99`: a concave quadratic is maximized at its clipped vertex
on each of 64 closed subintervals, and its positive inverse-square term is
bounded at the left endpoint. The maximum is also intersected with the
proved global 5/2 bound for `1<=rho_lower<=R<=6`. This is a finite upper
bound, not a sampled value of the function. Multiplication by upper
rho-gamma and upper J is justified by their nonnegativity.

With a true central gap the exact decomposition is

`D = m Q +(sigma-1)T+ +(sigma+1)T- +3(T-Jo)`,

`Q=(sqrt(sigma+1)A-sqrt(sigma-1)B)^2`,
`T+=b+-mB^2`, `T-=b--mA^2`, with all displayed summands nonnegative.
The positive-side endpoint inequality is

`D >= (sigma-1)b+ +6a+B -(sigma+5)mB^2`.

When its constant lower bound exceeds d, the downward quadratic forces B
above its positive root. Lines 103–107 lower positive terms, raise the
negative quadratic coefficient and use a lower square root. The reflected
formula uses sigma+1 and sigma+7. If the constant does not exceed d, the
source keeps endpoint lower zero instead of excluding the law. Upper
endpoints a-/m and a+/m follow from the same sign moments.

Line 109 is a lower squared distance between two positive intervals; hence
`m Q>=ml*qm`. Subtracting it gives one common residual `dout=d-ml*qm`.
The two outer T bounds and the max-price bound at lines 114–115 each use
that same residual. Their minimum is legitimate; no two full charges from
the same budget are added. A negative residual is a contradiction.

For the central integral, `G(A,B;rho)=rho P1-P2` increases in B up to rho
and decreases after it. At B=rho it is increasing in A and convex in rho:
`dG/dA=(rho-A)^2(rho+2A)/6`, `d²G/drho²=rho²+rho A`.
It is nonnegative there, so upper m, upper A and both rho endpoints are
correct at line 113. For P1 itself the minimum is at lower B and an A
endpoint, while the maximum is at upper B and A clipped to B. Multiplying
by m uses opposite endpoints for negative bounds, as lines 117–118 do.
Combining outer `-R T-/2<=J1_outer<=R T+/2` with the fourth moment interval
gives U=`J1+(M4-3)/6` without losing its sign.

The two complete constant upper strategies at line 122 may be intersected.
In particular their minimum need not be positive. Later replacing this
constant by its positive part for a threshold root only weakens exclusion.

## 6. Continuous score, signed phase and order of induction

The exact contact identity and the prior heat/Fourier argument give a
necessary upper envelope `A_C+F_C |H|-Q_C H^2`, with Q_C>0. Lines 131–138
use the full signed rectangle `C K1+phi U`, with
`phi in [PHI*(1-5 raw/(2N)), .4]` after an acquired raw ceiling; the first
pass uses lower phi=0. The adverse gamma endpoint in Q is signed. At line
133 the minimum over the two density endpoints is needed even when l<0;
simply multiplying a density lower bound by negative gamma would be wrong.

For a fixed |H|, this upper expression is convex in C: the constant and
quadratic coefficients are affine, and the linear coefficient is a maximum
of absolute affine expressions. A score interval is therefore covered by
its two endpoints. Maximizing in H gives a quadratic perspective
`F_C^2/(4Q_C)`; the same endpoint rule follows from convexity, with positive
Q checked explicitly. The source does not optimize C and H independently
in a way that loses this premise. The H root at line 138 uses a nonnegative
linear coefficient and the positive part of the constant. Every real H is
covered; no separate unexamined H tail is discarded.

The own-score improvement at lines 125–129 uses only the preceding accepted
raw bound. Nonnegative excess score, D and leakage first give a lower
Gaussian weight `E_H>=1-5raw/(2N)`. If this cell also forces D>=dlower,

`C <= .40974 + [raw/N-PHI*(1-5raw/(2N))*dlower/6]/rl`.

A negative numerator contradicts C>=CE; otherwise division by lower rho is
safe. The numerator increases with 1/n, so the floor N is adverse. This is
not a same-pass self-improvement: the fixed acceptor passes old raw,d into
the next stage and assigns new values only after both comparisons pass.

## 7. Removing the Gaussian weight and retaining nD

This ordering deserves an explicit analytical argument. Write e=C-CE>=0
and E_H=exp(-H²/(2n)). The nonnegative exact identity has the form

`Rraw/n = e rho + CE rho(1-E_H) + phi0 D E_H/6 + sqrt(n) L`.

If an accepted raw target T is less than .4N<=.4n, then Rraw/n<CE rho.
Consequently `CE rho-phi0 D/6>0`; otherwise the identity would give
Rraw/n>=CE rho. Rewriting it now gives

`Rraw/n >= e rho + phi0 D/6 + sqrt(n)L`.

This licenses the first unweighted defect conclusion **after** the raw
ceiling is validated. `accept_initial47.py:29,49–53` checks the strict raw
ceiling before the strict defect ceiling; its target shape enforces
T<.4*47. The first stage's raw envelope uses neither an old D nor an old
raw bound. Thus this ordered logical use is not circular even though one
completed cover supplies both numerical comparisons.

For later passes the conserved budget subtracts
`n(CE rho-phi0 D/6)(1-E_H)` from the raw remainder. It is at least
`(997/15000)nD` plus nonnegative excess/leakage. The acquired raw,D bounds
give the positive extra quadratic coefficient at line 136, once only.
The budget maximum is converted using `15000/(997*N)` in the stored d.
The stronger interpretation is `nD<=N*d`, not merely D<=d. A negative
cell budget excludes an actual witness because this conserved quantity is
nonnegative; it cannot justify multiplying a negative bound by a one-sided
index estimate. The INITIAL core still includes such a rectangle in its
active bookkeeping; that is harmless only with this vacuity interpretation.

For a nonzero barrier K the analogous subtraction K*rho requires the
separate premise `C-CE>=K/n`; the selected INITIAL47 profile here has K=0.
This note does not independently acquire the anchor45/prop46 barrier jobs.

## 8. Closed cover, singular faces and final export

The four nested partitions have sizes 24,24,8,4. Each is a closed interval
cover of the preceding admissible range, including zero-width retained
intersections; shared boundary overlap is permitted. Strict contradiction
tests discard no feasible equality face. Every discarded parent contributes
its exact child multiplicity to `excluded`. The final equality
`active+excluded=18432` checks cardinality, while the loop construction
supplies the actual coverage argument.

The original candidate JSON has 13 ordered feedback rows and 100 probability
panels. The final export is a fourteenth pass, so the selected transcript
describes 258,048 signed-cell incidences. These are source/candidate census
facts, not newly evaluated inequalities. They must not be confused with
the n25 12+1-stage transcript. The fixed checker accepts a finite ordered
list of 2–24 rows, enforces strict progress in at least one coordinate and
recomputes every recorded active/excluded count. Its 16 negative controls
include schema, ordering, census, duplicate-key and false-arithmetic cases.
Their existence does not replace the proof of each necessary predicate.

Before the final probability interpretation, line 56 checks `d<SL-1`.
Since rho>=1, every physical final witness has the required true central
gap. Lines 144–150 intersect its Cauchy p interval with all 100 closed
`[j/100,(j+1)/100]` cells. They skip only `ll>uu`; a singleton intersection
is retained. On each intersection the variance identity is
`theta=1-m²/(p(1-p))`. The maximum of p(1-p) is at an endpoint or at 1/2
when present, so using lower m and upper p(1-p) gives an upper theta.
The source exports coordinate-wise maxima over every contributing signed
rectangle, including H, rho and |beta|. Such a maximum table covers each
same-law witness; it does not assert that its maxima are simultaneously
attained. A zero incidence count and the sentinel values exclude a panel
only after these domain and inequality arguments and a full fresh replay.

## 9. Boundary to weighted local resources

`initial47_panel_proof.tex:93–153` and `local_panel_core.py:15–23,56–60`
explicitly distinguish the initial **unweighted** theta bound from a weighted
n theta bound. With acquired `nD<=N d`, positive lower endpoints A_l,B_l,
theta<=Theta<1 and a fixed p interval, the central-gap expansion gives

`D>=b_*+K theta`,
`b_*=(6+2sigma)(1-Theta)^(3/2) dist(p*,[l,u])²/sqrt(pq_max)`,
`K=min(3(sigma+1)B_l,3(sigma+3)A_l)>0`.

Here p*=(4-sigma)/2. The code lowers the positive numerator and raises its
denominator. Since b_*>=0 and n>=N,
`n theta<=(N d-n b_*)/K<=N(d-b_*)/K`.
Thus `lambda=n pq theta/(1-theta)` is bounded by
`N*pq_max*(d-b_*)/[K(1-Theta)]`. It would be invalid simply to multiply the
initial unweighted theta by N. The strengthened shared-shift expansion
similarly gives the inward-coordinate bound with denominator
`6(1-Theta)(A_l+B_l)`.

This algebra justifies the *meaning and directions* of the final weighted
export if its acquired inputs are valid. The actual finite geometry updates,
the alternate paired LOW eligibility checks and the later support-contraction
receipt joins require their own complete source-level and fresh arithmetic
checks. They are not acquired by the INITIAL table alone.

## 10. What remains open

1. Fresh complete INITIAL replay, all sidecar/source/capture checks, and its
   actual support/score predecessor acquisitions are separate work. No old
   JSON PASS is promoted here.
2. The full later uniform `general_geometry`, `general_cell`, central
   Bernstein bound and local-panel iteration/caller atlas remain a separate
   source-audit unit. Section 9 checks only their weighted interface formula.
3. Unrestricted attainment/contact, the exact oriented identity, global
   same-law joins and published literature inputs remain the explicitly
   named analytical dependencies. This review is not a substitute for them.
4. The anchor45/prop46 profiles, their source-specific finite barriers, and
   other n25/finite-index atlas variants are outside this INITIAL47 scope.
5. Every outward rounding and rational sign gate still has to be satisfied
   by complete execution. Reading the rational program is not that execution.

The useful result is a concrete, bounded derivation of this selected INITIAL
stage's domain predicates, induction and closed export, available for outside
checking. It supplies no unconditional all-index conclusion.
