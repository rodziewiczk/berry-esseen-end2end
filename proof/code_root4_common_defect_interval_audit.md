# ROOT4 common-defect, signed ledger and interval primitives

24 October 2026. This is a fallible internal AI source and hand-algebra review,
not external independent mathematical verification or formal verification.
No original mathematical module, constructor, acceptor or numerical kernel was
imported or executed. The scope is conditional soundness of the selected
functions below, rather than a new ROOT4 computation or an all-law C4 theorem.

The [machine source map](code_root4_common_defect_interval_source_map.json)
has SHA256 `f23c1eee7be908c662bdaf1f5c090e69ad21ee76ea1be3e601c2ae486e5bfa3b`.
It records exact original and actual-capsule file hashes and AST-derived line
ranges for 64 selected functions in 18 members of `vendor/root4_75a9470`.
Each selected function has the same AST in the vendor source and the actual
notebook11 capsule. All 18 actual member hashes match the 70-source-pin map in
the actual completed receipt, SHA256
`571bc91b257ac53c640dd3bee91377565ff7c475091d39076295200209beeae1`.
Those checks bind the inspected implementation; hashes and output statuses do
not prove its inequalities. The separate
[closed-cover review](code_root4_closed_cover_audit.md) treats the outer cover.

## 1. Actual selected path and boundary

The actual CPU geometry join calls the fresh generic common-A1 table v2,
then computes its five-price Gamma table on that same in-memory table, then
calls the CPU signed-CDF consumer with the same rectangle, eta interval,
frequency list and H labels. The consumer enables `use_two_disk=True` and
`modulus_radius_mode="five_budget"`. It combines each fixed H/orientation's
center, Gamma, remainder and reserves before taking the worst H/orientation.
It does not select coefficients from different complete bounds.

The map gives the precise selected function ranges, including:

| Source member, abbreviated by its unique stem | Read role |
| --- | --- |
| `n4_cpu_time_geometry_join_2026_10_09` | Actual same-table A1/Gamma/consumer call |
| `n4_cpu_time_signed_CDF_consumer_2026_10_09` | Active CPU-clone consumer and complete-route selection |
| `n4_fresh_signed_common_nu_quartic_ledger_2026_10_09` | Shared measure, signed ledger, remainder and normalization |
| `n4_Q3_fresh_generic_common_A1_response_table{,_v2}_2026_10_09` | Fresh HG table, tail/mesh/geometry margins and RAW alias |
| `n4_Q3_exact_common_signed_response_table_2026_10_08` | Selected homogeneous/signed interval primitives only |
| `n4_Q3_first_critical_integer_response_radius_verifier_2026_10_08` | Selected integer rectangle and response primitives only |
| `n4_Q3_first_critical_integer_abs_Prawitz_gate_strict_v2_2026_10_08` | Rectangle complex multiplication |
| `n4_Q3_fresh_generic_A1_five_price_cell_suprema_2026_10_09` | Whole-cell cost lower bounds and equality-price optimization |
| `n4_Q3_three_budget_exact_affine_radius_verifier_2026_10_08` | Reciprocal-domain and concave quadratic optimization |
| `n4_fresh_signed_A1_CDF_cell_consumer{,_v3,_v4}_2026_10_09` | Input/label gates, signed remainder and complete-score helpers |
| `n4_local_physical_moment_quadrature_2026_10_09` | Physical moments and midpoint reserve |
| `n4_frequency_local_physical_H_curvature_2026_10_09` | Actual-law modulus fill and H interpolation reserve |
| `n4_Q3_H_curvature_low_eta_box_leaf_2026_10_09` | Curvature and frequency transfer interface |
| `n4_Q3_generic_low_eta_center_only_exact_box_leaf_2026_10_09` | Selected affine-radius/complete-ABS helper only |
| `n4_eta_affine_transfer_bernstein_2026_10_08` | Whole-cell absolute fourth-power transfer |

This is not a review of every function in those files. In particular, it does
not validate the old `generic_characteristic` in the exact-common-response
file, or the fixed-beta pilot `phi_q_modulus_upper` in the integer-response
file as a generic-beta producer. The active fresh A1 path reuses only the
listed pure primitives from those legacy files. The fixed-beta pilot uses
fixed weights 13/20 and 7/20. Its import does not license generic use.

## 2. One physical law, one tagged defect measure

Let P be standardized and centered. Write
`u=E X_+=E X_->0`, `v_s=E X_s^2`, `c_-=a=v_-/u`, `c_+=b=v_+/u`.
The canonical reference Q has masses `u/a`, `u/b` at `-a`, `b` and
`p0=1-u/a-u/b` at zero. On a sign tag and y>0 set

    W_s(y)=y(y-c_s)^2,  eta=E W=rho(P)-rho(Q).

For eta>0, `nu=W dP/eta` is ONE probability measure over both tags and
off-contact points. On that same measure the actual budgets are

    eta E_nu k0 = p0-P{X=0} <= p0,    k0=1/(c_s^2 y),
    eta E_nu,tag k2 <= u,             k2=1/(y-c_s)^2,
    E_nu,tag k1 = 0,                 k1=1/(y-c_s).

The first identity follows by expanding `(y-c)^2/c^2` on y>0 and summing
both tags. Thus actual zero atoms consume budget; they are not discarded.
For the second and third identities, multiply by W and use
`v_s-c_s u=0`. Cauchy with the finite k2 budget gives absolute integrability
of k1. Contact atoms have W=0. If eta=0, W=0 almost surely and the sign
means/second moments fix P=Q; every CF defect is zero. No artificial nu is
introduced at eta=0.

Quadratic Hermite interpolation of `f(y)=exp(i sigma q y)` at nodes
0,c,c gives `f(y)-h(y)=W_s(y) f[0,c,c,y]`. The moments of h under P equal
those under Q. Consequently `delta_q=phi_P(q)-g_Q(q)=eta E_nu r_q`,
with `r_q=f[0,c,c,y]`. This identity applies to arbitrary physical P with
the stated moments and support, including zero/contact atoms. It does not
assume a finite-support actual law.

## 3. Signed Gamma and whole-domain equality prices

For fixed H and orientation let
`A1_H=Re sum_q 4 kappa_H(q) g_Q(q)^3 r_q`. Choose ONE price tuple
`(lambda0,lambda+,lambda-,theta+,theta-)`, with the first three nonnegative
and the equality prices theta signed. A whole-domain bound

    S >= sup(A1_H-lambda0 k0-lambda_tag k2-theta_tag k1)

implies `eta E A1_H <= A+eta S`, where
`A=p0_hi lambda0+u_hi(lambda+ +lambda-)`. S and the resulting affine
Gamma may be negative. They cannot be clipped, treated as a modulus, or
used as an infeasibility test. A positive intercept is safe but loose at
eta=0; exact delta=0 remains a separate fact.

The source's k0 lower bound `1/(c_hi^2 y_hi)` is rounded downward, as is
its nonnegative lambda0 product; subtracting that lower cost enlarges the
response upper bound. The reciprocal image of `[y_lo-c_hi,y_hi-c_lo]`
is kept as its full interval, ray or TWO rays when it crosses zero. On
each component the function `-zeta z^2-theta z` has its exact clipped
vertex/end-point supremum. The zero-zeta finite case requires theta=0.
Signed suprema are rounded upward, including negative values.

For a fixed equality price the source takes the maximum over all 273 y
cells before minimizing over candidate prices. It does not choose theta
separately at each point. Each tag can use a different complete theta
model; both use the same lambda0. The combination is the maximum of the
two tag suprema because nu is one probability, rather than a sum of two
unit masses. Exact midpoint selection between finitely many complete
price models is sound: whichever model is selected still bounds the
whole eta cell and reference box.

Reflection swaps the plus/minus contacts a,b and conjugates the CF and
responses; it does not swap the physical ordering of the price tuple.
The same raw-H phase is retained.

## 4. HG enclosure and integer interval directions

The localized support premise is `|X|<=R=17/4`. The order-three divided
difference has a Hermite-Genocchi representation with prefactor
`(i sigma q)^3/6`. For normalized homogeneous coefficients,

    hhat_0=1,
    hhat_n=(y/R) hhat_(n-1)+(n+1)(c/R)^n,
    b_n=q^3(qR)^n/(n+3)!.

This matches the source recurrence `b_n=b_(n-1) qR/(n+3)`.
Its degree60 exponential remainder is bounded by
`q^3/6 * (qR)^61/61!`; an unnecessary real exponential-growth factor is
not required for the imaginary exponential. The simplex weights have
mean 1/4 for y and 1/2 for the two repeated c nodes, giving
`|r_y|<=q^4/24` and `|r_c|<=q^4/12`.

The closed nearest-node y cells use mesh 1/64, clipped at 0 and R. Their
half-width gives response fill `q^4 h/48`. The endpoints and contacts are
covered through continuous divided differences, without division by y
or y-c there.

At scale `10^40`, the selected primitives floor lower bounds and ceil
upper bounds for positive products/powers. Their three signed-times-
positive cases have the correct endpoint order. The four-corner complex
product, rectangle conjugation and outward integer square root have the
required enclosure directions. The `(i sigma)^(n+3)` rotation and
reflection conjugation agree. All signed frequency terms are summed
before the y supremum; integer dot products are in scale-squared units
and rounded only after summation. Shape gates in the current caller
require the complete N, degree61 and 273-node arrays, preventing silent
zip truncation.

The HG tail and mesh are first expressed as physical Fractions, then
multiplied by scale and ceiled. They are not passed as raw physical
Fractions into integer units. The nominal RAW response modulus includes
tail and mesh once. The v2 compatibility alias changes metadata only.

For the box correction let e bound `|g_actual-g_nominal|`, p bound the
actual modulus, and a0 bound the nominal modulus. Then
`D3=e(p^2+p a0+a0^2)` bounds the cubed-CF difference. The extra A1 margin
is the complete nonnegative sum

    4 sum_q |kappa| [D3 R0_cell+p^3 q^4 Delta_c/12].

Here `R0_cell=min(nominal RAW cell bound,q^3/6)` is a minimum of two
complete scalar bounds; the contact-motion term is added once. The
source's scale powers in these products agree with physical units.
This verifies the transfer algebra and interval directions conditional
on the incoming actual/nominal CF-error and kernel enclosures.

## 5. Fourth-power remainder and signed normalization

The exact identity is

    psi^4-g^4=4 g^3 delta+delta^2(psi^2+2 psi g+3g^2).

A1 already contains the coefficient4. Thus the raw signed transfer is
`2 Gamma_H+2 sum |kappa| R2`, with linear coefficient8, not16 or32.
For a complete nonnegative affine radius `e=A+B eta` on [L,U], freeze
`p_hi=min(1,a+max(e(L),e(U)))`. The primary remainder is the whole convex
quadratic `e^2(p_hi^2+2p_hi a+3a^2)`.

Independently, the integral Taylor formula and exact chord identity give

    |R2| <= s(4a^2+2-s),  s=|delta|^2.

Its maximum for `s<=e_hi^2` is the complete constant
`V(4a^2+2-V)`, `V=min(e_hi^2,2a^2+1)`. Choosing the whole primary
quadratic or whole disk constant is sound; minimizing coefficients is
not. The sharper enabled two-disk lens routine is not proved in this
unit. Upward rounding of polynomial coefficients enlarges their whole
value on eta>=0, including a negative middle coefficient. A kernel
modulus upper multiplies the complete nonnegative remainder function;
one must not apply coefficientwise monotonicity to signed coefficients.

For one fixed H/orientation the row is

    P_H(eta)=M_H+quad+Hreserve+2 Gamma_H+2 weighted_R2-T eta.

The source subtracts T eta once and adds each reserve once. Its quadratic
coefficient is nonnegative. The degree2 Bernstein middle coefficient
is `(P(L)+P(U))/2-c2(U-L)^2/2`; strict endpoint negativity is therefore
equivalent to negativity of all three Bernstein coefficients.

The quantitative score uses all four faces
`P(L)/cap`, `P(U)/cap`, `P(L)/(rhoQ_lo+L)`, `P(U)/(rhoQ_lo+U)`.
For the lower-denominator branch the derivative numerator N satisfies
`N'=P''(rhoQ_lo+eta)>=0`, so interior critical points can only be minima.
For the cap branch convexity gives endpoint maxima. Both denominator
faces are necessary when the numerator is negative. Taking
`max(0,T+max(faces))` is valid for the positive-part score.

The baseline ABS helper also selects whole nonnegative affine or
constant fourth-power bounds. V7 extracts its transfer coefficients;
it does not use the helper's dummy normalized score with raw constant0.
The later complete-ABS helper performs the sign-safe four-face
normalization. This observation does not validate every old score
producer for arbitrary negative centers.

## 6. Physical moments and midpoint reserve

The identities

    y^3=W+2cy^2-c^2y,
    y^4=(y+2c)W+3c^2y^2-2c^3y

give `kappa_P=(b-a)+E sigma W` and
`M4_P=(a^2-ab+b^2)+E[(y+2c)W]`. Hence the implemented upper bounds

    |kappa_P|<=min(rho_P,|b-a|+eta),
    M4_P<=min(R rho_P,M4_Q+(R+2 cmax)eta)

are valid for the same physical P. Whole-box maxima and `cmax<=R`
follow from the supplied support/reference premises; no extra fourth-
moment or finite-atom assumption is introduced.

For `Z=(X1+...+X4)/2`, `E Z^2=1`, `E Z^3=kappa_P/2`, and
`E Z^4=(M4_P+9)/4`. With D=x-Z,
`E D^2=x^2+1` and
`E D^4=x^4+6x^2-2x kappa_P+(M4_P+9)/4`.
The source bounds the signed cubic term by `2|x| |kappa_P|` and uses
Cauchy for `m1<=sqrt(E D^2)` and `m3<=sqrt(E D^2 E D^4)`.
Its square-root helper compares squares to round upward.

In the regular Prawitz integrand
`F(u)=(1-u) A(u)+S(u) L(u)`, with
`A=E cos(6Du)`, `L=E[6D sinc(6Du)]`, the bounds
`0<=S<=1/3`, `|S'|<2`, `|S''|<5` imply

    |F''| <= 42 m1+108 m2+24 m3.

The derivative estimates follow by the integral representation of sinc:
`|A'|<=6m1`, `|A''|<=36m2`, `|L|<=6m1`,
`|L'|<=18m2`, `|L''|<=72m3`. The raw reserve is `F2/(12N^2)`,
including the factor2 from Prawitz. The minimum with the separate old
uniform reserve is a minimum of complete bounds.

The original physical-bridge prose imports the S derivative estimates.
The following supplies an explicit justification in this review, rather
than claiming that the original source already proved them. From the
cotangent partial fractions, cancel the first pole and set

    pi S=A-2p Rtail,
    A=3-2u-2/(1+u),  p=u^2(1-u),
    Rtail=sum_(n>=2) 1/(n^2-u^2).

The tail and its first two derivatives converge uniformly on [0,1].
The telescoping sum at1 gives `Rtail<=3/4`; the denominators are at least3,
so `Rtail'<=1/2` and `Rtail''<=7/6`. Also
`p<=4/27`, `|p'|<=1`, `|p''|<=4`, `|A'|<=3/2`, `|A''|<=4`.
Thus `|S'|<=85/(27 pi)<2` and `|S''|<=1000/(81 pi)<5`, using pi>3.
Nonnegativity follows from cot>=0 on [0,1/2], and on its other half from
`tan(pi(1-u))>=pi(1-u)`. The cotangent series gives `S<=1/pi<1/3`.
The pole-cancelled formula also establishes endpoint regularity.

## 7. Physical H-curvature reserve

Variance1 makes the physical CF 1-Lipschitz. The half-frequency-cell fill
is consequently `3/(2N)` for the X-frequency used here. Each cell's
modulus bound is `p_j=min(1,a_j+e_j+3/(2N))`, rounded upward.
The full nonnegative affine radius is maximized at its eta endpoints.
Scalar minima over complete valid models are safe.

For the Prawitz kernel, the cotangent identity yields both
`0<=S<=1/pi<1/3` and
`S<=(1-u)(1+2u)/(pi(1+u))< (1-u)/2`.
Therefore `u^2 |K(u)|` is bounded by each of

    u^2(1-u)+u/3,      u^2(1-u)+u(1-u)/2.

Their cell integrals are exact; the total integrals are 1/4 and 1/6.
The source chooses the minimum of two complete cell-integral bounds,
then forms `B=36 sum_j d_j p_j^4`, an upper bound on `|J_P''|`.
This is a real regular integral, not an asserted absolute complex
improper integral. Since `sup |Phi''|=phi(1)<1/4`, the raw H interpolation
reserve for H-step h is `h^2(B+1/4)/16`. Both upward rounding stages
enlarge it. The B<=6 comparison licenses replacing the old larger H
reserve once; the reserves must not be added or subtracted twice.

The baseline cubic, mass and unit radius alternatives have the stated
conditional meaning. In particular the divided-difference identity
`r=(f[c,c,y]-f[0,c,c])/y` gives `|r|<=q^2/y`; the same k0 budget and
contact upper bound M yield the mass radius. This is not a use of signed
Gamma as an absolute CF radius.

## 8. Still open after this bounded unit

No confirmed algebraic or interval-direction defect was found in the
selected scope above. Full ROOT4 soundness still requires at least:

1. The corrected generic CF, linked w/beta normalized center and actual-
   versus-nominal CF-error bounds. The relevant generic center,
   fresh-cached center, fresh-linked normalized-center and linked H-
   curvature producers have not been completely derived in this unit.
2. The complete cotangent, phase, Gaussian/pi and quadrature-cache
   arithmetic. Selected integer primitives do not prove all incoming
   kernel and center rectangles.
3. The enabled refined common-nu five-budget modulus-radius v3 and the
   two-disk lens remainder. Primary/disk algebra does not by itself prove
   those sharper alternatives.
4. The selected HIGH Cantelli bounds and all physical H/sign tail routes.
5. The preceding all-law localization, support, attainment and closed-CDF
   Prawitz implications. These are separate from a completed finite run.

Every enabled bound that can win the minimum needs a sound justification;
the possibility that a weaker alternative might suffice is not an audit
of the actual selected route. The completed receipt provides arithmetic
and provenance evidence, rather than an automatic proof of these remaining
lemmas. This report does not promote native-resource acceptance, the
all-law C4 claim or an all-index conclusion.
