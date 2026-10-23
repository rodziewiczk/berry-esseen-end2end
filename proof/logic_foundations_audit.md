# Foundational logic audit: attainment, contact and the conserved identity

Audit date: 23 October 2026. The source actually read is
`berry_esseen_manuscript.tex`, lines159–1650, SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
Line references below refer to that exact supplied v4 source, not a generated
PDF. The audit read the mathematical arguments, independently followed their
principal algebra and limiting steps, and crossread the existing direct
Prawitz proof. No numerical kernel, integration job or certificate replay ran.

**Finding:** no confirmed mathematical gap was identified in the foundational
arguments checked below. This does not establish the numerical support rows,
LOW/HIGH estimates, resource acquisitions, count interfaces, finite-index
certificates or global theorem. Several explicit finite claims and later
implementation links remain unreviewed here. An incomplete review is not a
disproof, and a stored PASS is not a substitute for a mathematical implication.

## Classification and the directed proof graph

`ARGUMENT_CHECKED` means that this audit followed the stated analytic argument,
with its explicit hypotheses. It is a scoped mathematical review, not formal
verification or independent human refereeing. `CERTIFICATE_ONLY` identifies
finite exact inequalities whose checking rule is specified but whose values
were not recomputed here. `UNREVIEWED` means an argument, external proof or
implementation correspondence was outside this review. `CONFIRMED_GAP` would
require an actual counterexample or failed logical implication; none was found
in this slice.

The foundational graph is:

```text
centered variance1 law, finite third absolute moment
  -> moment inequalities and characteristic-function bounds

fixed-index maximizing sequence
  -> unrestricted positive CLOSED-CDF attainment, including Cn=CE
  -> pointwise contact inequality, equality on the FULL closed support
  -> qualitative compact support, using only C>0
  -> legitimate fourth/fifth moments, gap sums and zero-bias identities
  -> nonnegative physical defect + two evaluations of ONE contact slack
  -> compensated hinge inversion -> exact conserved identity

contact + actual predecessor allowance + acquired moment bounds
  + finite support inequalities -> QUANTITATIVE support radius
```

The conserved identity does **not** require a numerical support-radius
certificate, a predecessor estimate, Prawitz smoothing, or a LOW/HIGH bound.
It uses the qualitative compactness already implied by contact. Prawitz is a
separate smoothing/physical-majorant input. This separation prevents adding
unnecessary circular edges to the graph.

| Source result | Status here | Exact boundary |
| --- | --- | --- |
| `orig:thm:defect`,168–193 | ARGUMENT_CHECKED | Factorization and moment substitution give the sharp rho/gamma domain. |
| `orig:lem:BPcardinal`,219–278 | ARGUMENT_CHECKED with the separate direct proof | The manuscript itself imports the majorant; the repository's direct proof supplies precisely that pointwise statement. |
| `cut49:global:attainment`,368–399 | ARGUMENT_CHECKED | Fixed n, unrestricted standardized laws, positive closed discrepancy; no strict gap above CE is required. |
| `cut49:global:contact`,410–456 | ARGUMENT_CHECKED | One actual attaining pair; finite third moment; C>0. |
| `cut31:support:direct`,492–553 | ARGUMENT_CHECKED conditionally | Actual same-law predecessor allowance and every displayed strict ray/endpoint gate are hypotheses. |
| Fifth-order Gaussian identity/envelope,609–712 | ARGUMENT_CHECKED conditionally | u>sqrt3, A/B/D nonnegative, positive denominator W and domination gate. |
| Numerical support rows,585–605 and790–816; strip rows,926–946 | CERTIFICATE_ONLY | The quoted finite signs/cell maxima were not recomputed here. |
| Anchored coordinates and sine circle,962–1092 | ARGUMENT_CHECKED | Only mean0, variance1 and finite third absolute moment. Atoms at zero are included. |
| Scalar cosine certificate,1099–1178 | Rule ARGUMENT_CHECKED; finite minimum CERTIFICATE_ONLY | Its1134 exact Bernstein coefficients and asserted minimum were not evaluated here. |
| Compatible profile,1180–1238; modulus,1240–1269 | ARGUMENT_CHECKED conditionally on scalar certificate | Profile joins/convexity and independent-copy Jensen argument; D is an independent-copy upper bound. |
| Rectangle gate,1273–1301 | ARGUMENT_CHECKED | Both gates must hold on the whole consumed frequency cell. |
| Four-term smoothing,1322–1355 | Explicit external statement dependency | Existing primary-statement check is recorded separately; this audit does not reprove that entire external theorem. |
| Physical defect and same-slack identities,1395–1516 | ARGUMENT_CHECKED | Actual support gaps of the same marginal; the half-open measure convention is essential. |
| Hinge inversion,1520–1577 | ARGUMENT_CHECKED | Signed measure with zero mass/first moment and finite absolute second moment; full infinite integral. |
| Conserved identity/ledger,1581–1644 | ARGUMENT_CHECKED | Identity for C>0 with explicit contact; nonnegative left terms additionally require C>=CE. |

## Moment domain and the exact Prawitz boundary

For the sharp third-moment inequality, set
`s=sqrt(gamma^2+4)`, `a=(s-gamma)/2`, `b=(s+gamma)/2`. Then `a,b>0`,
`ab=1` and `a+b=s`. The two displayed factorizations of `w_gamma` have
positive coefficients and squares. Their constants and leading terms agree
with the displayed polynomial. Averaging uses only EX=0, EX²=1 and the
finite third moments; the resulting expression is
`rho-(gamma^2+2)/s`. No support or extremal assumption enters.

The signed-second-moment inequality used later for support also has an
elementary same-law derivation. Write `A=E X_+²`, `B=E X_-²` and
`m=E X_+=E X_->0`. Then `A+B=1`, `beta=A-B`,
`rho>=(A²+B²)/m` and `m²<=AB`. Consequently
`rho>=(1+beta²)/sqrt(1-beta²)`, with `|beta|<1`. The beta in this
statement is EX|X|, not gamma or the third absolute moment called beta in
some external notation.

The manuscript defines its singular kernel by the limit of **real parts**,
not by an assumed convergent complex improper integral. Subtracting1 in
`exp(2pi i tU)-1` cancels its t^-1 singularity under E|U|<infinity.
This justifies the expectation identities by absolute Fubini on the
compensated integrand. The integer-node calculation also has the correct
orientation: the majorant is1 at zero and majorizes the closed negative
half-line; its reflected minorant uses the open half-line.

The missing derivation in the manuscript's own proof is an explicitly cited
input, not a derivation from its cardinal identities. The separate
[`prawitz_majorant_review.md`](prawitz_majorant_review.md), crosschecked in
[`prawitz_majorant_crosscheck.md`](prawitz_majorant_crosscheck.md), supplies it
directly. This audit followed its partial-fraction argument, absolutely
convergent real series, dominated Abel limit and Fourier signs. In its
notation `M=(1-H_B+W)/2` and `|H_B-sign|<=W`; hence M(0)=1 and the stated
closed/open conventions follow. That isolated proof does not automatically
validate every later physical quadrature or the four-term smoothing theorem.

## Attainment: the critical equality case really is included

At lines368–399, reflection of a negative **closed** discrepancy first gives
a positive **strict** discrepancy. Approaching that reflected threshold from
below recovers the same supremum with closed CDFs. This avoids the false
closed-CDF complement identity at an atom.

For a maximizing sequence with positive score at least c>0, rho is bounded
by `sqrt(n)/c`. Its third-moment bound gives uniform integrability of the
first two moments, by the displayed tail estimates. Weak limits therefore
retain mean0 and variance1. One may extract `rho_j -> b`, while lower
semicontinuity yields only `rho(P)<=b` initially. That is sufficient.

The threshold bound follows from Chebyshev for negative thresholds and the
normal upper tail for positive thresholds; a positive discrepancy is bounded
by the appropriate tail. Thus one can also extract `H_j -> H`. Closed-set
Portmanteau at `H+epsilon`, then epsilon down to0, gives a discrepancy at
least `Cn*b/sqrt(n)`. Dividing by the limit law's rho gives a score at least
`Cn*b/rho(P)>=Cn`. The definition of Cn forces equality and rho(P)=b.
Third-moment convergence is thus a **conclusion of extremality**. The argument
never assumes uniform integrability of |X|³ and never requires Cn>CE.

## Contact, atoms and compact support before higher moments

The contamination proof fixes the **raw threshold H**. Standardization moves
the corresponding standardized threshold, but the raw CDF under contamination
is a polynomial in epsilon. Its derivative is
`n(F_{n-1,P}(H-y)-F)`, including all atoms. Differentiation of the centered
third absolute moment gives
`|y|³-rho-3 beta*y`; a finite second-moment dominating function suffices for
this derivative. The variance derivative contributes the displayed quadratic
term. Substitution gives exactly the stated influence function.

Every contaminated standardized signed score is at most the same fixed-index
global supremum C. Thus I(y)<=0 for every real y. Integration against **that
same P** gives zero, using convolution and its actual first three moments.
The closed CDF is upper semicontinuous, so I is upper semicontinuous and
its zero set is closed. Its full-measure zero set contains the entire closed
support, including accumulation points and arbitrarily small atoms.

The leading term is `-C|y|³`, while all other unbounded terms are at most
quadratic. C>0 therefore excludes both sufficiently distant support rays.
Equivalently the contact majorant tends to positive infinity and equals a
number in[0,1] at support points. This qualitative compactness licenses M4
and M5. No quantitative radius, predecessor theorem or bounded-law
certificate was smuggled into this step.

## Quantitative localization: what the proof proves conditionally

In the direct support lemma the actual predecessor quantity is
`A=sqrt(n-1)*Delta_{n-1}(P)/rho`, with `d_P=n(A-C)`. The algebra
`n(s*A-C)=s*d_P+n(s-1)*C` leaves the exact correction
`e=n(s-1)-1/2`; there is no discarded constant. The supremum bound
`A<=C_{n-1}` may weaken this same-law quantity, but does not identify its
extremizer with P or assume monotonicity of Cn.

The derivative bound for the Gaussian contact term follows by Taylor
expansion of phi and `d_s[s phi(sy)]=-phi''(sy)`. First the gates show
`Q(v)<0` on the entire ray. Only then is its multiplier C replaced by
a lower bound c. The envelope derivative is bounded by L(v); its negative
second derivative and two negative initial gates prove strict decrease.
Both signs and the whole threshold line must pass. An endpoint upper bound
without these ray gates is insufficient.

The fifth-order heat calculation at609–667 has the displayed cancellations:
the retained third/fourth/fifth derivative coefficients and powers of n/v
give the stated A,B,D. Its absolute remainder uses positive coefficients
under u>sqrt3. The signed envelope additionally needs B,D>=0 and W>0;
these hypotheses must be retained when applying the later cleared
polynomials. The favorable negative D term is frozen at the upper index
endpoint, adverse terms at the lower endpoint. This is a valid simultaneous
band bound, rather than an unjustified monotonicity claim about a signed sum.

The finite-series generating function at839–865 gives the displayed P_j
coefficients by coefficient extraction. Its absolute coefficient majorant at
z=1/4 and discarded degree>=7 yield the stated O(n^-6) bound after division
by z. This checks the mechanism and uniform domain, not every later tensor
Bernstein maximum or quoted strip margin. The selected large-ray Gaussian
input has a separate finite-n derivation in
[`logic_gaussian_input_audit.md`](logic_gaussian_input_audit.md); it requires
neither an eventual theorem nor a prior cutoff. Replacing phi(0)/6 by1/15
uses phi(0)<2/5 in the correct direction.

Numerical radius/strip conclusions remain conditional on their actual input
rows. A beta interval with nonnegative lower endpoint, a threshold bound or
a sharper moment cap may be used only after it has been acquired for this
same witness. Positive closed discrepancy alone does not make beta positive.
No quoted cell count or negative maximum was recomputed here.

## Characteristic bounds: checked analytic rules versus finite values

The anchor proof uses `W(R)=(R-1)²(2R+1)` and
`E W(R)=2(rho-1)`. The sinc bounds, integrated tangent correction and
Cauchy factorization give the stated real/imaginary bounds using only third
moments. The sharper lower real bound is global: its tilted cosine is
minimized at u on[0,pi], and its value at pi also bounds the remainder of
the positive ray.

For the sine circle, the positive measure mixing centered two-point laws has
mass P(X!=0); retaining the original zero atom recovers P. Integrating the
two-dimensional vector bound gives the claimed circle. Signwise Cauchy then
gives `zeta(rho+zeta)>=2`. Zero atoms contribute zero to the vector and do not
invalidate this argument. Dominated convergence at u=0 gives the gamma
version with the stated normalization.

The scalar cosine proof correctly reduces a global inequality to a degree13
polynomial on81 adjacent closed cells. Bernstein nonnegativity fills the
whole cells. Its asserted exact minimum is nevertheless a finite arithmetic
claim, not a theorem inferred merely from listing code. That claim and the
small rational trigonometric-join comparisons were not executed in this
audit. Conditional on them, the compatible profile's continuity, convexity,
decreasing derivative and cosine-defect domination follow as written.

The independent-copy modulus uses the probability measure
`(X-X')² dP/2`; convexity and monotonicity of the profile give Jensen and
the allowed replacement by a larger D. The universal estimate D=rho+1
follows from centering and E|X|<=1. This D is **not** the later physical
gap defect with the same letter. Substituting that different quantity here
would require a new proof.

In the rectangle gate the first condition bounds the argument of z^(n-2)
by3/2<pi/2. The second condition makes the x second derivative nonnegative;
the y second derivative is then also nonnegative. Separate convexity proves
the corner bound, including n=2 and equality in the gates. Without both
whole-cell gates the finite telescoper remains valid. A branch true only at
an integration midpoint is not a valid frequency-cell enclosure.

The four-term smoothing inequality is explicitly external at1322–1344.
Its factor2 kernel convention and all four nonnegative terms, including the
infinite Gaussian tail, are recorded in the primary statement check
[`literature_inputs.md`](literature_inputs.md). This audit checked the
manuscript's subsequent normalization rule `sqrt(n)/rho_lower`, and the
whole-cell quadrature logic; it did not independently reprove that external
smoothing theorem. The same literature note records the exact all-law
Shevtsova cap needed before quantitative moment localization. A located
primary statement is distinct from a review of its original proof.

## The conserved identity: same slack, exact compensation and signs

At1395–1456, tau is a nonnegative probability density by signwise Fubini.
Compact support makes every gap sum absolutely convergent. If zero is in
the support, the outer-gap estimate bounds J by rho. Otherwise the actual
central gap(-A,B) has both endpoints positive. The displayed expansion of D
has a squared term, nonnegative positive/negative third-moment remainders,
and a nonnegative outer-gap remainder. The coefficients use
`sqrt(sigma+1)*sqrt(sigma-1)=3`. Hence D>=0 for the **actual** support gaps;
arbitrary loose endpoint caps cannot replace A/B inside this identity.

The contact slack `Acal=integral tau(Q_H-h)` is evaluated twice. On a gap,
`h(a)-h(b)=nu([a,b))`; Fubini therefore produces exactly the half-open L
term. The endpoint b is excluded and a has zero weight. This is the correct
closed-CDF convention, not a negligible-atom assumption.

The second evaluation uses the zero-bias density tau. The identities
`E g'(X*)=E[Xg(X)]`, `E X*=gamma/2`, `E(X*)²=M4/3` and
`E|X*|³=M5/4` follow from signwise integration. Independence of X* from
S_{n-1}, and the actual iid summands, give the zero-bias law for S_n/sqrt(n).
Its CDF expression is insensitive to endpoint atoms because the displayed
polynomial vanishes at its endpoint. Direct substitution recovers both
`first-slack`, `second-slack` and the truncated-first-moment equality with
the written coefficients.

The hinge inversion at1520–1555 is absolutely convergent under its stated
signed-measure assumptions. The compensated scalar kernel has absolute
integral `pi*y²/4`; Fubini against the total-variation measure is therefore
legitimate using a second moment alone. Zero mass and first moment remove
the linear term. This avoids a CDF jump inversion or formal low-frequency
Taylor cancellation.

The Gaussian signed density has transform
`exp(-n*t²/2)*(1-i*n*gamma*t³/6)`: the minus imaginary sign matches the
positive Fourier convention. The third distributional derivative of
`(x-z)|x-z|` is4delta_z, giving the hinge correction
`2gamma*phi(z)/(3sqrt(n))`. The scale identity contributes the factor1/n
in epsilon. Consequently `E_n=-n^(3/2)*epsilon/2` has the error coefficient
`2sqrt(n)/pi`. The infinite high-frequency integral remains present.

Finally, substituting the two slack expressions gives the conserved identity
with `U=J1+(M4-3)/6`. Its algebra is valid under the explicit contact input
for C>0. Only the claim that **each** left-hand term is nonnegative needs
C>=CE: e=C-CE>=0, the phase loss is nonnegative, D>=0 and L>=0.
No division by e, D or a gap length is used; the equality boundaries remain
included. Strict exclusion requires a later strict upper bound or separate
boundary argument, not nonnegativity alone.

## Graph obligations and circularity risks to preserve

1. Global attainment/contact must precede a bounded-support certificate's
   application to an unrestricted contrary law. The reviewed proof supplies
   this order; assuming a finite atomic maximizer would be an unnecessary
   and unjustified shortcut.
2. A numerical radius must be acquired from a predecessor allowance and
   already valid moment bounds. A resource row obtained only after that same
   radius cannot justify its first acquisition unless a separate weaker
   input radius/row starts the chain.
3. All moment, support, phase, slack, LOW/HIGH and count quantities must refer
   to one law and threshold. Intersecting bounds from independent optimizing
   laws is not licensed by these identities.
4. C>=CE and the sign of every coefficient replaced by a lower or upper
   scalar must remain explicit. In particular the support proof checks a
   negative bracket before replacing C by its lower bound.
5. The equality case Cn=CE and all atoms must remain covered. Strict outgoing
   events, closed incoming events and half-open gap measures cannot be
   replaced by one uniform CDF convention.
6. The identity/error ledger does not establish the hypotheses of the
   quantitative LOW/HIGH bounds or the simultaneous resource enclosure.
   Those are later mathematical edges, and their actual finite inequalities
   are further certificate edges. Both remain outside this foundational
   conclusion.

No new compute queue or notebook is proposed by this note. The next logic
review should inspect those later LOW/HIGH, resource and count implications
against these explicit hypotheses, then test the global composition for an
acyclic same-witness acquisition order. The checked foundation does not by
itself close that high-level proof graph.
