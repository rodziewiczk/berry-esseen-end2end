# ROOT4 corrected CF, linked center and fresh quadrature intervals

24 October 2026. This is a fallible internal AI source and hand-algebra
review, not external independent mathematical verification or formal
verification. No original mathematical module, numerical kernel or test
was imported or executed. The checks below derive selected inequalities
from source formulas; they do not constitute a fresh mathematical replay.

The [source map](code_root4_linked_center_source_map.json), SHA256
`78f8260b1f368e8922017ae0ae6a3c4d118d783634d930dfd255614abf59ca79`,
records 79 selected functions in 16 exact source members, their SHA256
pins and AST-derived line ranges. Their selected function ASTs agree
between `vendor/root4_75a9470` and the actual notebook11 capsule. All
16 actual file hashes match the 70-pin actual completed receipt, SHA256
`571bc91b257ac53c640dd3bee91377565ff7c475091d39076295200209beeae1`.
These are source/evidence checks, rather than proofs by receipt or hash.

This follows the
[common-defect and interval-primitives review](code_root4_common_defect_interval_audit.md).
It addresses its previously open corrected-CF/linked-center and selected
quadrature-cache dependencies. It leaves the enabled refined five-budget
radius, two-disk lens, HIGH/Cantelli portfolio and all-law placement
separate. No runtime, frozen mathematical source or notebook was changed.

## 1. Correct reference and fixed-point exponential

For `0<w<=1`, `0<=beta<1`, let D=1-beta^2 and

    a=sqrt((1-beta)/(w(1+beta))),
    b=sqrt((1+beta)/(w(1-beta))).

The canonical probability Q has masses `w(1+beta)/2` at -a,
`w(1-beta)/2` at b and `1-w` at zero. Thus the corrected generic CF
uses the correct negative/positive weights and the conjugated negative
exponential. It retains the true, possibly irrational midpoint contacts
inside their outward root intervals. Rational upper root endpoints are
not substituted as the nominal CF baseline.

`generic_characteristic_correctly_scaled` computes the physical degree60
imaginary-exponential remainder `(qR)^61/61!`, then passes its integer
upper `ceil(scale*remainder)` into `outward_exponential`, whose input and
output endpoints are in fixed-point units. The latter routine encloses
each positive Taylor coefficient by floor/ceil recurrence, rotates it
with the correct four-cycle signs and adds the remainder to both real
and imaginary coordinates. The integral Taylor remainder has modulus
at most `(qR)^61/61!` on imaginary arguments. Positive q, positive contact
intervals and contact upper R=17/4 give its uniform domain. Multiplication
by nonnegative probability weights is signed-endpoint floor/ceil,
including negative rectangle coordinates.

This repairs the documented legacy unit error; it does not validate the
legacy generic-CF producer. In particular, the older reference-bridge
file also contains `nominal_rectangle` with a physical remainder passed
to the integer helper. The active corrected path uses only that file's
`geometry` and `reference_error`, not `nominal_rectangle` or its old
high-level center producer. Likewise the fixed-beta pilot in the integer
helper is not used as a generic-beta producer. A whole-file endorsement
of these imported legacy modules would be incorrect.

The independent unit-disk bound permits clipping a probability CF's
modulus by1. Coordinate intersection with [-1,1]^2 also preserves every
probability CF. That operation is not a claim that a general CF lies on
the unit circle, or that every point in its rectangle is a CF.

## 2. Whole-box geometry and three reference-error bounds

The box-root and reference-bridge functions enclose a,b,u,rho by their
exact monotone endpoint squares and outward integer square roots. The
nominal w,beta labels are the exact rational rectangle midpoint. For
beta>=0, a decreases with both coordinates; b decreases with w and
increases with beta; u increases with w and decreases with beta; rho
has the opposite monotonicity. Nominal intervals remain inside the
whole-box intervals. The source checks the full contact upper against R.

Let `dm,dp,dz` bound absolute mass changes, `da,db` the contact motion,
and pm,pp actual-mass uppers. Splitting mass change at nominal contact
and contact motion with actual mass gives the direct error

    dm+dp+dz+pm*q*da+pp*q*db.

Mass cancellation removes the constant exponential term and replaces
dm,dp by their products with `min(2,q*a0_hi)` and
`min(2,q*b0_hi)`. The zero atom disappears. Cancellation of total mass,
mean and variance instead uses
`R2(x)=exp(iqx)-1-iqx+q^2*x^2/2`, with
`|R2(x)|<=q^3|x|^3/6` and `|R2'(x)|<=q^3*x^2/2`.
This gives exactly the source's third bound

    q^3[(dm*a0_hi^3+dp*b0_hi^3)/6
        +(pm*amax^2*da+pp*bmax^2*db)/2].

All are nonnegative complete upper bounds. Their scalar minimum is safe.
The additional bound `q^3*(da+db)/6` follows from the contact derivative
bounds in the next section. Ceil converts the selected physical bound
to integer units. With nominal modulus upper a0 and error e, the actual
modulus cap `min(1,a0+e)` is valid. The source's fourth-power telescope
and endpoint bound each give a complete scalar bound for
`|g_actual^4-g_nominal^4|`; their minimum, then the nonnegative weighted
sum, supplies the raw center correction once.

## 3. Contact derivatives and the required paths

At positive contacts, put s=a+b, pm=1/(as), pp=1/(bs), p0=1-1/(ab).
The exact moment-preserving identity is

    g=1-q^2/2+[F_-(a)+F_+(b)]/s,
    F_sigma(c)=[exp(i sigma q c)-1-i sigma q c+q^2c^2/2]/c.

The source's R, R', R'' and quotient-rule formulas agree with this
identity, as do its ga,gb,gaa,gab,gbb. Their rational-contact evaluation
uses signed outward rectangle arithmetic and the correctly scaled
`exponential_exact_argument` helper. The first two derivatives of the
same exponential are used; no independently changed CF baseline enters.

Each of the three derivative-majorant families used in the scalar
minimum has a direct justification:

* The weight/exponential family bounds every absolute rational weight
  derivative at the positive lower contact endpoints. All denominators
  and sums have the stated monotonicity. The mixed second derivative has
  two first-order exponential-motion terms and no q^2 mixed term.
* The moment-preserving family writes F=c^2 K. The third divided
  difference gives `|K|<=q^3/6`, `|K'|<=q^4/24`,
  `|K''|<=q^5/60`; product and quotient rules give the source's bounds.
* Since `g=1+f[-a,0,b]`, repeated-node differentiation gives
  `|ga|,|gb|<=q^3/6`, `|gaa|,|gbb|<=q^4/12`,
  `|gab|<=q^4/24`. The signs of these derivatives do not affect these
  absolute estimates. The order/factor2 for a repeated same contact is
  essential and is present.

The probability contact domain `a,b>0`, `b>=a`, `ab>=1` is convex:
`b>=1/a` is an epigraph of a convex function, and `b>=a` a half-plane.
Adding a,b<=R preserves convexity. Nominal, actual and rational upper-
root references lie in this domain. Thus their required straight
segments consist of probabilities and support `|g|<=1` on those paths.
There is no assertion that all corners of an enclosing contact rectangle
are probability laws. The derivative bounds themselves are uniform on
the positive enclosing rectangle; the probability assertion is needed
when converting those bounds to powers of g.

For the raw finite center C with its factor2, the gradient is
`8 Re sum kappa*g^3*gi`. Its contact Hessian has bounds
`8 sum |kappa| (3|gi||gj|+|gij|)`. This matches the source.
For squared modulus, the corresponding factors are
`2 Re(conj(g)gi)` and `2(|gi||gj|+|gij|)`.
Signed frequency terms are summed before taking the upper endpoint.
For the reflected row the source conjugates g and both contact
derivatives, while retaining the canonical a,b order and the same H
phase. It does not swap derivative labels because the CF is reflected.

## 4. True nominal gradients, radial tightening and contact normalization

Derivative bundles are evaluated at rational upper endpoints of the
true nominal root brackets. Their gradients are shifted to the true
nominal pair by `Haa*ea+Hab*eb` and `Hab*ea+Hbb*eb`, each ceiled upward.
This uses the same contact Hessian valid on the nominal-to-bar segment.
The raw Taylor upper retains the true nominal raw center. Signed
gradient intervals multiply the whole actual-minus-nominal contact
intervals; the absolute Hessian supplies the quadratic remainder.

For radial tightening, the source starts with the true nominal squared-
modulus upper, shifts its gradient in the same way, and takes the scalar
minimum of complete squared bounds. Its rational square-root floor and
square comparison produce an outward integer modulus upper. A negative
whole-box squared upper is rejected rather than silently clipped. The
nominal point is inside the whole box, and the caller checks that its
retained nominal modulus cap is not lost.

The contact moment is `rho(a,b)=(a^2+b^2)/(a+b)`. Its Hessian is

    4/(a+b)^3 * [[b^2,-ab],[-ab,a^2]],

which is positive semidefinite. The supporting-plane residual at z is
`2*(z_b*a-z_a*b)^2/[(a+b)(z_a+z_b)^2]>=0`.
Consequently subtracting T>=0 times its supporting plane gives the
correct upper bound for C-T*rho. The source keeps the signed constant
shift from the true nominal point to the rational supporting point;
the gradient is `grad C(n)-T grad rho(z)`. Only the raw C Hessian
remainder is charged. No absolute moment-Hessian cost is necessary.

The separately available `C_whole_upper-T*rho_whole_lower` is also a
complete normalized upper. The source ceils the two complete bounds
separately and then intersects them as scalars. It does not independently
minimize their polynomial coefficients or relabel a normalized bound
as a raw center.

## 5. Linked w,beta normalization

Writing `rho=w^(-1/2)f(beta)`,
`f=(1+beta^2)/sqrt(1-beta^2)`, gives
`f'=beta*(3-beta^2)/D^(3/2)` and `f''=3*(1+beta^2)/D^(5/2)`.
The Hessian divided by rho has entries
`3/(4w^2), -k/(2w), 3/D^2`, where
`k=beta*(3-beta^2)/[(1+beta^2)D]`. Its determinant is

    [9+9beta^2+15beta^4-beta^6]
    /[4w^2(1+beta^2)^2 D^2] > 0.

Thus rho is jointly convex on w>0, |beta|<1. The source's rational
identity and positive numerator are correct. Its lower supporting plane
at the true midpoint justifies subtraction with no absolute rho-Hessian
reserve.

The linked raw gradients are
`C_w=-(a C_a+b C_b)/(2w)` and
`C_beta=(-a C_a+b C_b)/D`. The source's contact second derivatives
also agree with differentiation, including
`a_betabeta=a(1-2beta)/D^2` and
`b_betabeta=b(1+2beta)/D^2`.
In the mixed raw Hessian,
`a_w*b_beta+b_w*a_beta=0`, so the C_ab term cancels exactly.
The remaining terms are bounded using whole-box contact/Jacobian and
second-derivative envelopes plus contact-gradient drift from the true
nominal pair. Replacing the potentially signed second derivative by
its absolute envelope uses the maximum of |1-2beta| at both beta faces.

The linear increments are the linked w-w0,beta-beta0 intervals; the
moment and raw-center gradients remain signed until their interval
products. The raw-center Hessian remainder covers the entire rectangular
parameter segment. Root enclosures are checked by exact squared
inequalities and midpoint labels. This establishes the source's complete
linked normalized upper under the incoming true center/gradient/Hessian
premises. Its scalar intersection with the contact-normalized upper is
valid after separate upward rounding.

The actual fresh linked wrapper calls the corrected table and derivative
producers directly. It preserves the original nominal/raw center and CF
fields, adds normalized fields and refreshes worst-normalized metadata.
The later signed consumer uses M as a bound on C-T*rhoQ and subtracts
T*eta, rather than subtracting T*rhoQ a second time.

## 6. Selected cache interval arithmetic and scaling

The original and actual CPU cache builders use the same mathematical
operations. The CPU clone changes resource clocks and source integrity
bookkeeping. It preserves the original immutable cache class and pure
helpers; it does not supply saved numerical JSON as a proof input.

For pi, the alternating arctangent bounds at 1/5 and 1/239 have the
correct even/odd next-term directions. Machin's identity
`pi=16 atan(1/5)-4 atan(1/239)` follows from the tangent addition formula
and the principal-angle range. The lower/upper interval combination
uses opposite endpoints in the subtracted term. Positive square roots
and inverse endpoints then enclose `phi(0)=1/sqrt(2pi)` outward.

For |x|<=2, the exact integrated degree60 expansion of exp(-t^2/2)
has remainder bounded by
`|x|^123/[2^61*61!*123]`. The source uses this bound on both sides,
multiplies by the positive phi(0) enclosure, and reflects the integral
with the correct endpoint order for negative x. The checked target
and Gaussian-tail comparisons are separate integer inequalities; no
claim is made here that those comparisons were newly recomputed.

For 0<u<1, cotangent partial fractions give

    R(u)=(1-u)cot(pi u)+1/pi
        =[1/u-2u(1-u) sum_(j>=1) 1/(j^2-u^2)]/pi.

After j=M, the omitted sum lies between `1/(M+1)` and
`(2M+1)/[2M(M+1)]`. The lower bound follows by comparison with
the integral of x^-2 from M+1; the upper follows by the telescoping
sum of 1/(j^2-1). Their use has the correct reversed order in the
subtracted numerator. The division evaluates all endpoint pairs,
which is safe even when the enclosing numerator crosses zero.

The stored kernel is `((1-u)+i R(u))/N`, namely 2K(u)/N for the
half-scaled Prawitz K. The midpoint frequency is q=3u, the phase is
exp(-i q H), and the normal term is Phi(H/2). Thus the raw center
`1+2 Re sum kernel*phase*g^4-2 Phi(H/2)` has the correct factor2 for
the n=4 standardized one-sided discrepancy. This matches the later
factor8 contact gradient and factor4 A1 before the final raw factor2.

Phase0 and ratio are exp(-i3H/(2N)) and exp(-i3H/N). Their outward
recurrence therefore contains every midpoint phase; intersection with
[-1,1]^2 preserves the exact unit phase after each multiplication.
The cache builds all N256 frequencies, the complete exact H grid from
-4 through25/8, both sides' phase data through the consumers, and the
Gaussian endpoint witness. It shares only geometry-independent kernel,
phase and normal data; each geometry's CF and derivative bundles are
fresh. Data shape/type/hash validators alone are not proofs of these
inequalities: validity requires the actual direct builder path.

## 7. Limited outcome and next dependencies

No confirmed sign, scaling, path-quantifier or outward-rounding defect
was found in these selected functions. This unit supplies a conditional
source derivation for the corrected nominal CF, reference-error bounds,
contact and linked normalized centers, and selected shared cache
interval arithmetic. The prior report's open-cache/center boundary is
narrowed by this later source read; the earlier note remains a dated
record of its own smaller scope.

The enabled refined common-nu modulus-radius v3 and two-disk lens still
need their own proof from source. The HIGH Cantelli portfolio and its
physical signed tail routes also remain distinct. The all-law support,
attainment, closed-CDF majorant and first-critical predecessor
implications are upstream mathematical obligations. This report does
not promote a conditional arithmetic receipt to unrestricted C4, native
resource acceptance or an all-index theorem.
