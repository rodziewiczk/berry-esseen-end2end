# Uniform-tail acquisition: heat support and complete Fourier inputs

Date: 23 October 2026. This is a fallible internal AI source and hand-algebra
review, not external independent verification, formal verification, or fresh
arithmetic acceptance. Other model agents' cross-reads are checks within the
same system. No archived module, kernel, bound evaluator, constructor or
acceptor was imported or executed. Only source/AST/JSON/byte checks were run.
Original source comments and archived PASS descriptions are material being
examined, not authority for the conclusions here.

## Bounded finding

The actual selected all-H heat-support route has a coherent conditional
derivation, including the signed fifth derivative, finite integer bands,
the infinite band and exclusion of both exterior support rays. The complete
HIGH frequency partition and the triangle LOW transfer below also retain
their terms and the necessary directions for a floor N. The selected paired
LOW's coefficient, Mills and orientation rules have the same conditional
interpretation described below. No invalid inequality was identified within
these inspected arguments.

This does **not** say that all uniform-tail resources have been acquired.
The finite rational sign gates still require full replay; the signed INITIAL
and later resource atlases still require every necessary-predicate and
same-witness implication, with their actual dependency order. The published
finite caps and far-ray Gaussian estimate remain named imported inputs. The
remaining boundaries are listed at the end. In particular this note supplies
neither an unrestricted local exclusion by itself nor a global conclusion.

## 1. Actual selected bytes and notation

The source archive is `BE_cutoff49_20260930.zip`, 16,660,566 bytes, SHA-256
`ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e`.
The supplied v4 manuscript has SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
References use its 9,252 source lines. In the archive, define

- `A = BE_cutoff49_20260930/`;
- `B = A/baseline/certificates/work/below50_20260929/`.

The [new source map](code_uniform_tail_acquisition_source_map.json) records
actual member hashes and the precise reviewed ranges. The selected entry
paths come from `A/retained_jobs.json`, not from a guessed earlier script
with a similar name. The selected unrestricted support entry is
`B/structural/accept_unrestricted_cover50.py`; the HIGH algebra entries are
`B/entry/accept_high_tail.py` and `accept_high_window50.py`; the INITIAL entry
is `B/entry/accept_initial47.py`.

All following moment bounds refer to the **same** mean-zero, variance-one
law X. Write rho=E|X|^3, beta=E[X|X|], gamma=EX^3, mu_j=EX^j and
eta_5=E|X|^5. H is the raw threshold of the unrestricted attained positive
closed maximizing pair. The support radius R and a Fourier coefficient
radius R0 are different quantities; R0 may be enlarged to max(R,2g).
The integer n varies through n>=N. It is neither the conditional noise nor
the Bernoulli parameter p.

## 2. Contact gives a support test before bounded-support Fourier is used

Manuscript401–457 proves I<=0 everywhere and I=0 on the entire closed support
of the attaining law. Using the deleted-law positive CDF bound in the
displayed contact formula gives manuscript731–750:

`rho*I(t) <= H_n(H,t) + C*(-|t|^3+3*rho*t^2/2+3*beta*t+rho*e_n)
                 +rho*s_n*d`,

where s_n=sqrt(n/(n-1)), e_n=n(s_n-1)-1/2 and
d=n(C_(n-1)-C_n)_+. Replacing the actual deleted score by the global
predecessor score only enlarges this upper bound; replacing a negative
predecessor difference by its positive part does likewise. It does not
replace the attaining law or optimize under a rho restriction.

Consequently a strict negative upper bound for this expression at a point
t contradicts support there, even for an arbitrarily small atom or a support
accumulation point. A weakly negative bound would not suffice to exclude a
boundary point. The acquired decrement must belong to this same current
index and attaining pair. It is not a generic monotonicity assertion for C_n.

The scale calculation at manuscript467–482 and
`B/structural/heat_support50.py:48–53` uses c=48/125. For x=1/n,

`(1-x)*(1+x/2+c*x^2)^2-1
 = x^2*((2c-3/4)-(c+1/4)*x+(c^2-c)*x^2-c^2*x^3)`.

The bracket decreases for x>=0 because 0<c<1. Its positive N-endpoint
gate licenses e_n<c/n for all n>=N>=36. This is not extension of the older
coefficient .38 to an unsupported floor. The positive lower e_n bound follows
from the analogous polynomial for 1+x/2.

## 3. Fifth-order heat identity and the all-H envelope

The entire `B/structural/support50_proof.tex:44–159` argument was read against
manuscript604–712. The actual code is `fifth_heat50.py:11–28`.
Put v=n-1, s=sqrt(n/v), u=|t|, z=H/sqrt(v), and

`A=(u^3-3u)/6`, `B4=(u^4-6u^2+3)/(24*sqrt(v))`,
`D5=(u^5-15u)/(120*v)`.

Expanding F_v(H-t) to degree5 and expanding F_(v+1), its first derivative
and its second derivative in the heat-time variable cancels the coefficients
of F_v,F_v',F_v''. The remaining coefficients are exactly

`(t/2-t^3/6)*F_v'''`,
`(t^4-6t^2+3)*F_v''''/24`,
`(t/8-t^5/120)*F_v'''''`.

Thus, after division by s^3, the retained expression is
`+/-A*(1-z^2)*phi(z)+B4*phi'''(z)-/+D5*phi''''(z)`.
The heat-time remainders have coefficients 1/48, u/48 and (u^2-1)/16;
the spatial remainder contributes u^6/720. The Gaussian Fourier integral
gives sup|phi^(5)|<=8/pi<51/20 and sup|phi^(6)|<=15*phi(0)<6.
Multiplication by v^(3/2) yields exactly

`E5 = 51*u^6/(14400*v^(3/2))
      +51*(3*u^2-2)/(960*v^(3/2)) +u/(8*v^2)`.

These are uniform derivative norms. No compact H interval was assumed or
silently substituted for the all-real-H claim.

The tangent `phi''''(z)>=phi(0)*(3-15*z^2/2)` follows from cos(w)>=1-w^2/2
under its positive Gaussian Fourier integral. For positive t and |z|<=1,
the retained terms are at most

`phi(0)*(A-3*D5-(A-15*D5/2)*z^2+3*B4*|z|)`.

When A,B4,D5>=0 and W=A-15*D5/2>0, completing that square gives
`T=A-3*D5+9*B4^2/(4*W)`. For positive t and |z|>=1 the first term is
nonpositive; the other terms are bounded by phi(0)*(2*B4+3*D5).
For negative t the first term has global upper bound
`2*exp(-3/2)*A*phi(0)<A*phi(0)/2`. The gate
`T>=A/2+2*B4+3*D5` therefore covers both signs and every z. This is why
the outer-domination gate is indispensable rather than optional metadata.

## 4. Simultaneous band endpoints, rays and literal integer coverage

For N<=n<=L, favorable -3D5 uses its **lower** value at L, adverse D5 and
B4 use their upper values at N, and W uses its positive lower value W_*.
For an infinite band the favorable lower D5 is zero. This is termwise
domination of the signed expression, not a claim that every signed coefficient
or a rounded executable helper is monotone in n.

`fifth_heat50.data:15–27` matches this directly. In particular
`B2=H4^2/(256*(N-1))` is exactly 9*B4_+^2/4. The inverse square-root in
the adverse remainder and in 2*B4_+ uses the lower rational root ell;
the multiplier s_n uses its upper rational root S. W_*>0 is established
before clearing it. The domination gate makes T_* positive before replacing
phi(0) by2/5 and s_n by S.

The signed contact coefficient Q(u) is bounded above using the same acquired
rho<=r, |beta|<=b and e_n<.384/N. `target:35–37` requires Q<0 **before**
using the lower current score c=.4095+K/L. K=0 gives c=.4095 without an
upper index. The source's rho/beta cap construction checks its positive
denominators and the strict squared sign-moment inequality; it does not
acquire those caps from unrelated laws.

The seven polynomial sign families are tested on every adjacent closed
radial cell from R through4.5. The exact Bernstein transformation in
`heat_support50.bern:33–36` is a change to the nonnegative Bernstein basis,
so strictly positive coefficients prove the sign on the entire closed cell.
Both exterior rays u>=4.5 are different inputs: they use the named imported
He--Cheng bound `|H_n(H,t)|<=u^3/15+u/5+1/2`. The resulting cubic Q and
contact cubic have their value and first three derivatives strictly negative
at4.5. Their exact Taylor expansion there then excludes every point of the
ray. This neither samples H nor truncates the support to a numerical box.
The primary source/scope of that imported Gaussian estimate has not been
independently rechecked by this source-only unit.

The selected unrestricted acceptor has literal bands

`[36,39],[40,44],[45,49],[50,59],[60,89],[90,134],[135,199],[200,infinity)`.

It checks every adjacent integer endpoint and the infinite terminal row.
The q=.19 cover starts at36; q=.20 starts at40. The all-index local route
uses their restriction to n>=47. No step ends at98: `last=0` deliberately
exports an infinite band and sets favorable D5_-=0. Removing or reordering
a band fails the structural checker. All strict polynomial signs remain
full arithmetic obligations, not observations of this review.

The left radius3 support is a separately named conditional callback.
`B/entry/accept_left_support47.py:14–20` temporarily substitutes already
acquired rho<=1.390, |beta|<=.430 into the same all-H kernel, then restores
the original constants even on failure. It calls `target(47,0,0,3,.19)`;
it does not assume an upper H bound or a prior radius3 support. Those actual
moment caps must first be obtained by PREP47_COMPLEMENT. The callback itself
cannot supply its own moment premise.

## 5. The complete HIGH integral and the actual product-law event

The full source proof `B/entry/high_window50_proof.tex:68–159` and actual
`high_window_core.py:9–38` were read, not only its algebra-acceptance status.
The event E is under the product of the same marginal law, with
P(E)>=a>0, distance |X-X'|>=d0>0 on E, and conditional second moment <=m.
Symmetrization gives `|f(t)|^n<=exp(-n*E sin^2(t*(X-X')/2))`.
The event restriction, positive a and convex Jensen then bound this by the
conditional expectation of `exp(-n*a*sin^2(t*d/2))`. Positive Tonelli permits
a separate frequency partition for each actual distance d; no new optimizing
law is chosen by that partition.

All six contributions are present:

1. On [1/2,9/10], the fourth-moment cosine polynomial gives a positive
   rate. Its concavity in t^2 licenses endpoint testing, and its chord on
   [1/4,81/100] yields the optional sharper first term. The chord residual
   has the correct nonnegative sign throughout that interval.
2. Nonzero peak cores use `|sin(pi*v)|>=h*|v|`. The symmetric t^-3 factor
   is bounded by `j^-3+6*(j-w)^-5*v^2`; its Gaussian zeroth/second moments
   give the exact two series terms. Their tails after20 are bounded by
   decreasing integrals, not discarded. The Jacobian contributes d^2,
   which is averaged using the actual conditional m bound.
3. Peak wings have damping h*w and their total positive weight is bounded
   by d^2/(2*pi^2). Enlarging a core or wing below9/10 only adds a positive
   integral, and cannot remove part of the original integral.
4. The zero cell with t*d/2<=1/2 uses sin(u)>=23u/24 and the positive
   Gaussian tail with rate kappa=a*(23/48)^2*d0^2.
5. The remaining zero-cell part uses sin(u)>=23/48 and total weight
   1/(2*(9/10)^2). Shared integration endpoints have measure zero even
   when the conditional distance distribution has atoms.
6. The Gaussian comparator is retained on the **entire** [1/2,infinity)
   half-line. Pearson gives |gamma|<=sqrt(M-1) for its cubic term.

The optional rational tail is not a heuristic Mills fit.
`high_tail_proof.tex:19–51` uses the positive integral
`integral u/(x+u)*exp(-u) du`. For P(u)=u^2-4u+2 and D(x)=P(-x)>0,
the exact square remainder in the polynomial division is nonnegative.
Integrating its polynomial quotient gives the upper fraction
`L(x)=(x+2)/(x^2+4x+2)`. Multiplication by x has the direction needed
for that upper bound. The derivative numerator of sqrt(x)*exp(-x)*L(x)
is `4-10x-22x^2-13x^3-2x^4`; its strict negativity on x>=1/4 licenses
the optional zero-cell floor substitution. The fixed algebra checker
reconstructs these identities and the shifted negative coefficients;
it does not by itself establish an actual-event hypothesis.

For all-index evaluation, sqrt(n)*exp(-c*n) decreases only after 2*N*c>1.
Every such rate has its explicit gate. L is positive and decreasing; the
optional first term has its additional positive slope and damping gate;
the rational zero-cell term has N*kappa*b^2>=1/4. The comparator's n>=5
gate is also present. The exact analytic quantities are compared at N and
only then rounded outward. Capping the executable exponential-series input
at64 is a weaker upper enclosure, not a proof that its rounded output is
decreasing on an unbounded sequence.

Every window candidate includes all six contributions. The minimum is
taken only after a complete bound, and an unavailable optional gate rejects
that candidate rather than proving an EMPTY law. The concrete actual-event
and moment acquisition at each caller is still required.

## 6. Triangle LOW transfer, including the actual-radius Pearson branch

The actual early routine is `B/entry/kernel.py:63–83`, with the same
`sixth` body in `entry/contracted_kernel.py:65–85`. The complete proof
`B/baseline/diagnostics/resource_calculus/fourier_replacement.tex:11–154`
was read against manuscript1708–1815,1877–1925. This is not an extension
of an index95-only certificate merely by changing its number.

For h(t)=exp(-t^2/2-i*gamma*t^3/6), Taylor gives
`f-h=-a*t^4-i*z*t^5+r6`, with a=(3-mu4)/24,
z=(10*gamma-EX^5)/120 and |r6|<=E6*t^6. The modulus of the exponential's
argument is bounded by `t^2*(1/2+g^2/144)<1/6` on [0,1/2]; the two Taylor
remainders give exactly the source's E6. B6=a_*+Z/2+E6/4 controls the full
f-h difference there, with mu6<=R*eta5 supplied by actual bounded support.

Symmetrization gives the damping `(45-M)/96`; convexity of the complex
disc bounds every point on the segment from f to h. The polynomial power
Taylor remainder is at most `n^2*B6^2*t^8*exp(-b0*n*t^2)/2`. Its full
divided integral and the r6 integral are at most
`(E6/(2*a0^2)+B6^2/(2*b0^3))/n`. Thus the finite L2 term is retained,
including at the smallest allowed N>2.

For the remaining leading terms, global sine/cosine bounds and Gaussian
moments give coefficients lambda_N and lambda_N/2, where
`lambda_N=sqrt(pi/2)*(N/(N-1))^(3/2)`.
The code's c0 is an upper enclosure of that value and c1=c0/2. The comparator
remainder supplies exactly `251*g^3/17280` and `251*g^2/4800*|H|`.
Every real H is covered by the linear |H| term. No H-grid or missing H tail
is hidden in this transfer.

For the coefficient Z, put Q=X^2-gamma*X-1. Direct expansion gives

`E Q^2=mu4-1-gamma^2`,
`EX^5=gamma^3+2*gamma+E[Q^2*(X+2*gamma)]`.

For |gamma|=t<=g and an enclosing R0>=max(R,2g), the two possible signs
of EX^5-10*gamma are bounded by

`P_R0(t)=R0*(M-1)+(10-2*M)*t-R0*t^2+t^3`,
`Q_R0(t)=R0*(M-1)+(2*M-10)*t-R0*t^2-t^3`.

The condition R0>=2g licenses replacement of the true mu4 by its upper
bound in the first polynomial as well as the second. For M<=5 the first
polynomial dominates; at R0=6 its second derivative is negative on g<2.
The derivative gate either licenses its upper endpoint or the code uses
the safe quadratic obtained from t^3<=g*t^2. For M>5, the first polynomial
is at most R0*(M-1), while dropping the negative cubic from the second
gives the displayed clipped quadratic maximum. The actual-radius variant
uses **R0=max(R,2g)** and R0>g before dividing by R0-g. It never substitutes
the smaller physical radius into a coefficient whose sign would reverse.
The radius-six, actual-radius and eta5+10g alternatives each bound the same
absolute coefficient, so their minimum is valid.

The resulting complete triple `(L0,LH,L2)` has the source's meaning
`I0(H)<=(L0+LH*|H|)/sqrt(n)+L2/n`. All floors/positive damping checks are
performed before returning it. Passing this rule still requires the actual
mu4, |gamma| and eta5 enclosures from the same law.

## 7. Paired LOW, finite Mills and the signed-phase boundary

`B/entry/contracted_kernel.py:277–308` is read under its narrower actual
gates M<=2, g<=1, R>2g and M-1-gl^2>=0. These gates suffice for its older
`b0=43*(1-2/N)/96`; that damping must not be exported to a larger M domain.
The containing coefficient rectangle has
`zl<=z<=Z` and `(3-M)*gl/144<=c<=(2-gl^2)*g/144`, with the extra increasing
2*gamma-gamma^3 bound used only when 3*g^2<=2. The lower z polynomial is
increasing for gamma>=0 under these gates. Pearson's sixth-moment identity
gives the recorded minimum of R*eta5 and its shared residual bound.

The exact Gaussian cancellation norm J(z,c) is convex and invariant under
simultaneous sign reversal. At positive corners, its exact split at
sqrt(z/c) has the signed Gaussian constant term plus a positive exponential
factor. The finite continued fraction at depth11 is a lower Mills bound
when z/c>=3, where its multiplier is negative; depth12 is an upper bound
when z/c<3, where its multiplier is positive. Positivity of the remaining
exponential factor is checked. A negative constant Gaussian coefficient
uses the lower root for sqrt(pi/2), and a nonnegative one the upper root.
At c=0 or z<=0 the explicit nondividing branch is retained. Convexity is
used for the **exact norm**, not assumed for either upper-bound formula.

These facts match the explicit finite positive-integral proof at
manuscript1817–1875. No convergence of an infinite continued fraction is
needed. The subsequent remainder, phase-LH and L2 terms are still present;
the cornerwise minimum is of two bounds for the same norm.

Clipping a signed lower bound at zero licenses a lower bound for |gamma|
only for this auxiliary Fourier norm. If gamma<0, reflect X and H **only
inside the unsigned Fourier calculation** and reflect both odd coefficients
together. `B/entry/paired_fourier_orientation47.tex` states this explicitly.
The original contact law's beta, gamma, p, K1 and signed phase coefficients
remain unchanged. In particular, a lower bound for |gamma| does not license
a later uncorrected signed-phase curvature. The selected broad corrected
PREP replay and its separate later positive-signed-gamma license remain
AND inputs, as detailed in
[code_uniform_tail_kernel_audit.md](code_uniform_tail_kernel_audit.md).

## 8. Acquisition order and remaining source boundary

The meaningful conditional order is:

1. Unrestricted attained contact and actual predecessor decrement, plus
   named finite caps and the all-H Gaussian estimate, imply radius3.84.
   Bounded-support Fourier is not used to establish that initial radius.
2. Radius3.84 and actual moment bounds license complete LOW/HIGH at every H.
   INITIAL starts without assuming an already small gap defect. The first
   accepted raw target is below .4*N **before** removing the Gaussian weight
   to acquire an unweighted defect. Every subsequent pass consumes only
   already accepted raw/defect bounds.
3. The final gap test precedes interpretation of sign probability and
   zero-atom exclusion. The actual all100 closed p panels and singleton
   incidences are exported; H bounds come from the positive root of a
   necessary conserved-budget quadratic. They are conclusions of an all-H
   bound, rather than hypotheses used to cut off an untested H region.
4. PREP/complement precedes their smaller support callbacks. Contracted
   support precedes INPUT. Each subsequent confinement or feedback resource
   pass consumes only previously acquired facts for that same law.

The literal source routes for this ordering were read in
`local_signed_core.py:19–29,123–153`, `accept_initial47.py:46–62`,
`local_panel_core.py:24–73`, the support callbacks and their original proof
notes. This records the ordering and the displayed bound meanings. It is
not a completed derivation of every predicate in those large atlases.

Still open after this unit:

- Full term-by-term mathematical review of the signed INITIAL moment atlas,
  all its support-deficit/PSD and integral-cost exclusions, and every
  later general/paired geometry and conditional callback variant. Earlier
  n25 reads and common helper names are not blanket coverage of these
  distinct uniform source bodies.
- The original signed remainder/inversion and every acquired p/rho/mean/
  moment/endpoint table must be bound at the exact selected uniform scope.
  Source formulas with named conditional premises do not themselves prove
  that the actual extremizer belongs to those premises.
- The original broad-phase repair, subsequent signed-gamma license,
  central/left PREP complement, support contractions and every final
  local closed union require their full evidence joins. A reflected
  Fourier norm cannot silently reflect the contact witness in such a join.
- The published finite caps, Bernoulli strict theorem and He--Cheng far-ray
  Gaussian bound have the separate primary-literature boundary recorded in
  [literature_inputs.md](literature_inputs.md). No external verification of
  those sources is claimed by this unit.
- Every selected strict finite sign, complete arithmetic pass, uniform local
  exclusion, finite base and global least-failure composition remain distinct
  requirements. This review acquires none by a historical PASS or by source
  identity, and changes no execution or proof-graph flag.

A remaining unreviewed implication is not called a disproof. Conversely,
the absence of a found counterexample here does not establish the unreviewed
atlases or the entire theorem.
