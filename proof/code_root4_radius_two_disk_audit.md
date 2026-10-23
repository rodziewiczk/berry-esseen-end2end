# ROOT4 physical norm radii and the two-disk quartic remainder

24 October 2026. This is a fallible internal AI source and hand-algebra
review, not external independent mathematical verification or formal
verification. No original mathematical module, numerical kernel or test
was imported or executed. It examines the enabled refined-radius and
two-disk parts left open by the earlier
[common-defect](code_root4_common_defect_interval_audit.md) and
[linked-center](code_root4_linked_center_audit.md) units.

The [source map](code_root4_radius_two_disk_source_map.json), SHA256
`4b2d4266b4be076fbfa11f4fa816146039af048a0d7e9661d0741b3c513d63af`,
records 31 selected functions in eight exact members. Their selected
ASTs are identical in vendor and actual notebook11 sources. All eight
actual hashes match the 70-pin actual completed receipt, SHA256
`571bc91b257ac53c640dd3bee91377565ff7c475091d39076295200209beeae1`.
This binds the reviewed formulas; neither pins nor receipt status prove
the mathematical input premises.

## 1. Same measure, response norms and units

Use the same physical law, tagged defect measure nu and k0,k1,k2 budgets
derived in the common-defect unit. For eta>0,
`delta_q=eta E_nu r_q` implies `|delta_q|<=eta E_nu |r_q|`.
An H-summed signed Gamma is not a CF modulus radius.

The original A1v2 RAW arrays enclose `scale*|r_nominal|` on all273 closed
y cells, already including HG tail and half-cell mesh. For each actual
contact displacement Delta the source forms the complete actual bound

    min(q^3/6, RAW_nominal/scale+q^4*Delta/12).

The q^4/12 contact derivative was derived in the earlier HG unit. The
source ceils the physical contact movement once, intersects with an
outward cubic cap, and adds neither another HG tail nor another mesh.
It takes maxima over all273 cells and both physical contacts for the
zero-price norm slope. Conjugation preserves response norm, so those
two contact columns cover both signs and reflections; reflected physical
tag price pairs must be exchanged. This argument does not identify
the reflected signed A1 curves with the unreflected ones.

For the five-price compiler, division by positive exact q^3 occurs only
after the RAW actual response enclosure. `ceil(RAW_int/q^3)` has the
correct fixed-point units for `|r_actual|/q^3`. The same full-contact
k0 lower floors and signed concave two-ray pole suprema used by Gamma
give a bound S on the normalized norm minus one complete price tuple.
The first three prices are nonnegative; the equality prices remain
signed. Each fixed equality price takes MAX over all cells before MIN
over equality-price choices. The tags share one inverse-size price and
one probability nu; their signed suprema combine by MAX, not by SUM.

Thus the normalized model is `q^3*(A_normal+eta*S_normal)`. The source
emits physical Fractions `A=q^3*A_normal`, `S=q^3*S_normal`, and prices
multiplied by the same q^3. Its exact physical budget intercept is
recomputed from those prices. The optional physical integer
`S_upper_int` is only an extra outward alias; the consumer uses the
physical Fraction S. There is no extra q^3 divisor, guessed scale or
replacement of actual-reference modulus by a nominal one.

The independent cubic, mass and unit models remain present. At eta0
the physical defect is exactly zero without defining nu; their bounds
are still safe. A negative signed affine norm upper is not clipped to
zero. To use a model in a remainder, both closed-cell endpoint values
must be nonnegative. A one-face negative value is not whole-cell
emptiness. Strict negativity at both faces would exclude that cell for
that conditional model, but the actual CDF consumer does not use these
diagnostic signals to silently delete geometry classes.

## 2. Exact selection and actual enabled call path

The v2 compiler replaces repeated Fraction comparisons by one positive
common denominator D divisible by scale and every intercept denominator:

    Ai=D*A_normal, Si=(D/scale)*S_normal_int,
    A_normal+eta*S_normal_int/scale
      =(Ai*eta.denominator+eta.numerator*Si)/(D*eta.denominator).

Eligibility and sign tests therefore have exactly the same signs as
their integer numerators. The same denominator applies to all candidates
at a given midpoint, so the strict ordered midpoint comparison preserves
the first tie. Complete price tuples are deduplicated; A from one tuple
is never combined with S from another. Safe selected tuples and the
zero-price fallback are retained as whole-fiber bounds. Midpoint
selection is an efficiency choice and does not establish validity only
at the midpoint.

The v3 wrapper directly calls this v2 production compiler and changes
top-level source metadata only. Its replacement dormant tests are not
invoked by the actual producer. No old v1 compiler or old failing dormant
test suite is required for the enabled production path.

The actual CPU consumer requests `five_budget`, validates the same
literal rectangle, nominal roots, N256 q/H labels and closed eta cells,
and augments only each frequency's delta-radius model list. It preserves
the actual-reference modulus, kernel weight and every old radius model.
The chosen complete radius is nonnegative on both eta faces. Its maximum
endpoint value freezes the whole-cell scalar E passed to the lens bound.

The optional `compact_refined_H_curvature` is read as a conditional
monotone helper but is not enabled by the actual CPU consumer. That
consumer deliberately retains the old baseline physical H reserve.
Likewise the new radius models are not supplied to the old complete
ABS routine. Three complete per-H row scores are compared only after
each row has its own center, Gamma, remainder and reserves. The consumer
selects one entire score, then takes MAX over H/reflections. There is
no coefficientwise route minimum or mixing of endpoint pieces.

## 3. Exact two-disk reduction

Rotate so g=a>=0, put `delta=x+iy`, `r=|delta|`, `s=r^2`, and assume
`a<=A<=1`, `|psi|<=1`, `r<=E`. The exact quartic remainder satisfies

    R2=delta^2*(6a^2+4a delta+delta^2),
    |R2|^2=s^2 F(a,s,x),
    F=36a^4+4a^2s+s^2+8ax(6a^2+s)+24a^2x^2.

Expanding the real and imaginary parts verifies this identity. For a,r>0,
the full feasible x interval is
`[-r,min(r,(1-a^2-s)/(2a))]`, with r<=1+a. Since F is convex in x,
the maximum is at a negative collinear endpoint, a positive collinear
endpoint, or the unit-circle boundary. The case a=0 is direct and is
covered by the same final envelopes.

At the positive collinear endpoint, `a<=min(A,1-r)` and r<=1. The
remainder increases with a. Its maximum increases with r on both pieces:
the first has positive coefficients, and the second has derivative
`12r(1-r)^2`. It is therefore enough to evaluate at `r=min(E,1)`.

At the negative collinear endpoint, `max(0,r-1)<=a<=A`. The nonnegative
factor `6a^2-4ar+r^2` is convex in a. The a=A endpoint increases in r
because its derivative is `4r(r^2-3Ar+3A^2)>=0`. The lower-a branch is
r^4 below1 and `r^2(3r^2-8r+6)` above1, whose derivative is
`12r(r-1)^2`. Evaluating both at `r=min(E,1+A)` therefore bounds the
whole negative branch, even when E exceeds the feasible radius.

On the unit circle, substitution yields

    F=18a^4+12a^2+6-(12a^2+8)s+3s^2.

For fixed r this is convex in a^2 on `|1-r|<=a<=A`. Its lower-a
endpoint is already one of the collinear cases. At a=A the remaining
squared norm is

    Q_A(s)=s^2[C-Ds+3s^2],
    C=18A^4+12A^2+6, D=12A^2+8,
    (1-A)^2<=s<=min(E^2,(1+A)^2).

For A>0 its only interior local maximum is
`s_-=(3A^2+2-A*sqrt(4-3A^2))/2`; the other stationary point is a
local minimum. Endpoints and s_- suffice. At A=0 the interval is
degenerate. The source brackets the radical by an exact isqrt/square
comparison, intersects its s_- interval with the feasible s interval,
and bounds Q there by `C*s_hi^2-D*s_lo^3+3*s_hi^4`.
All signs in this interval upper are correct because C,D and the
clipped s endpoints are nonnegative. A final outward rational square
root converts the squared norm bound. No grid, floating optimizer or
sampled maximum supplies the continuum claim.

The final scalar minimum with the separately valid primary and old
integral-disk caps is sound. In the actual consumer, this is a whole-
cell constant candidate against a complete primary quadratic and a
complete old-disk constant. Its nonnegative kernel-weighted sum is
rounded upward coefficientwise on eta>=0, preserving the whole
polynomial even if its linear coefficient is negative.

## 4. Outcome and remaining portfolio

No confirmed algebraic, scaling, sign or enclosure defect was found in
this selected radius/lens path. This source read derives the sharper
enabled alternatives rather than assuming that a weaker fallback would
have sufficed. The optional full-ABS lens helper is a scalar triangle
intersection; it is not the signed A1 transfer and is not enabled in the
actual CPU path. Its exact scalar sharpness examples do not assert
joint realizability by one standardized law across frequencies.

Together, these three inner units narrow the source-to-lemma boundary
for the active LOW signed A1/Gamma/V7 path. They do not yet derive the
HIGH Cantelli portfolio, all alternate cheap-leaf mechanisms or the
all-law first-critical placement from their implementations. The outer
closed cover, preceding support/attainment, closed-CDF majorant and
predecessor facts remain separate joins. No all-law C4, all-index theorem
or new native-resource acceptance is declared here.
