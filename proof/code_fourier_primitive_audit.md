# Code-to-lemma audit: selected exact primitives and complete HIGH

**Review status:** AI-generated internal source review. Cross-reads by
other model agents are internal checks by the same AI system. External
independent mathematical review and machine-checked formal verification
are not established here. This review may contain mistakes or omissions.
See the [evidence limits](CODE_INTERFACE_AUDIT.md#evidence-limits).

Date: 23 October 2026. Scope: the pinned B3/B4 n25 INITIAL and global
resource capsules used by notebooks09/10. This is an internal source and
algebra readback, not a numerical replay or a claim that their mathematical
inputs have been acquired. No archived mathematical module was imported.
The supplied manuscript is unchanged, SHA256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.

[The source map](code_fourier_source_map.json) records four exact source
manifests, all declared-file SHA comparisons and function line locations.
Paths are members of `cutoff25_20261011.zip`, SHA256
`17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`.
The two INITIAL and two resource manifests have30/32 declared files each.
Every declared byte pin matched. Historical review text inside the capsules
was treated as material to check, not as authorization or fresh acceptance.

## Bounded result

No unsound inequality was found in the selected square-root, exponential,
Gaussian enclosure, complete HIGH six-term formula, Cantelli event or upward
moment-substitution rules below. Their mathematical directions match the
manuscript's respective statements. The source interfaces remain conditional
on genuine simultaneous moments and actual product-law events. This does not
review every LOW coefficient, phase callback, support ray or INITIAL rectangle.

| Actual source | Reviewed operation | Mathematical reference |
|---|---|---|
| `kernel.py:19--28`, and the identical primitive functions in resource `contracted_kernel.py` | Directed rounding, square roots, positive-series exponential upper bound | Manuscript exact-arithmetic rules, lines8980--9016 |
| `integer_exphi.py:12--24` | Integer Horner evaluation of the same finite exponential polynomial | Same rule; `INTEGER_EXPHI_PROOF.txt`, reviewed below |
| `finite_binomial_core.py:9--59` and byte-identical `finite_gaussian.py` | Machin constants, integrated Gaussian Taylor enclosure and tails | Manuscript lines8999--9016 |
| `finite_binomial_core.py:61--96` | Literal binomial probabilities, both jump sides, endpoint enclosure on the left half | Monotonicity argument below; not a proof of a selected complete table |
| `high_window_common.py:11--69` | Every HIGH frequency piece, optional improvements, complete-window minimum | HIGH_WINDOW50 statement/proof, lines2102--2268 |
| INITIAL `cantelli_high.py:9--49` | Additional actual-event candidate, without replacing the original bound | Same-law event premise of HIGH_WINDOW50 |
| INITIAL `high_grid.py:5--22` | Replace a moment upper bound by a larger one, rechecking all gates | Substitution of a weaker hypothesis, not monotonicity of the formula |

The active common HIGH file is SHA256
`2be56942b240633e9665c6da74c504da835d8d49a8aaefdd893e9dd14304671f`
in all four capsules. The kernel file is
`d71f58b7527c3cf6d2146d816e5d124f6f331d1b153e5aaedee5182707647f12`;
the resource caller actually uses `contracted_kernel.py`, SHA256
`bae2588aecc0dd07ca37fe38214ddff72aaabb1b02ca4afca03120a77570d0b0`.
Its `down/up/roots/exphi` function ASTs are identical to those of `kernel.py`;
their separate support/LOW domains are not equated by that observation.
the integer exponential file is
`5bf8e305e46d577314ee78220bd4185a162d6a9ba3cdcf0c4e4b0791cf41bd03`;
both Gaussian filenames have SHA256
`939236711b080f9148ee3d3f7f6a0cd15b86cb24f3d2700f0e7127b2a345291f`.
Two different retained `high_window_core.py` byte identities exist; their
inline and constant-extraction expressions have the same six terms. The
INITIAL Cantelli helper obtains its one-window function from that INITIAL
core and restores the previously installed `high` function immediately.

## 1. Directed arithmetic and exponential upper enclosure

For a positive integer scale S, integer floor gives
`down(x,S) <= x <= up(x,S)`, also for negative rational x. In `roots`,
`isqrt(floor(x*S^2))` equals `floor(S*sqrt(x))`; the adjacent grid points
therefore enclose the nonnegative root. The explicit squared comparison is
retained. Selected calls use fixed positive integer scales. A zero lower
root used as a divisor would reject execution, not prove an inequality.

The exponential primitive sets

`y=floor(10^6*min(x,64))/10^6`, `T=sum(y^j/j!,j=0..64)`.

For x>=0, `0<=y<=x`, and the positive exponential series gives
`T<=exp(y)<=exp(x)`. Thus the upward-rounded reciprocal is an **upper**
bound on exp(-x). Capping the argument at64 only weakens this upper bound;
it never cuts an infinite-frequency tail out of the integral.

For y=a/b with b=10^6, the Horner loop returns

`D=64!*b^64`,
`P=sum((64!/j!)*a^j*b^(64-j),j=0..64)`.

Starting P=d=1, each decreasing index j updates `d=d*b*j` and
`P=P*a+d`, producing exactly those coefficients. Hence P/D=T; the last
integer ceiling is exactly the original rational reciprocal and upward
rounding. No approximate transcendental library or changed truncation degree
enters the replacement.

## 2. Gaussian and literal binomial enclosures

The alternating arctangent series at1/5 and1/239 supplies directed Machin
endpoints; reciprocal and square-root directions are correct for
`1/sqrt(2*pi)`. Machin's identity has the branch
`4*atan(1/5)-atan(1/239)=pi/4`: the tangent identity gives1 and the angle
lies strictly between0 andpi/2. The kernel's short lower Machin bound and
positive-integral upper pi bound are consistent with these constants.

For z=t/Z in[0,5], the Gaussian routine integrates the terms

`T_k=z^(2k+1)/(2^k*k!*(2k+1))`.

Its recurrence multiplies by
`t^2*(2k+1)/(2*(k+1)*(2k+3)*Z^2)`, exactly T_(k+1)/T_k.
Each term has lower/upper integer bounds at scale S. Alternating addition
subtracts the upper endpoint for a negative term and the lower endpoint for
a positive lower sum. After terms0..79, the upper enclosure of term80 is
subtracted/added as an absolute remainder. This is valid even when the
initial terms grow: Taylor's remainder for exp(-u), u>=0, is bounded by
u^80/80!, and integration gives precisely T_80. No assumption of decreasing
terms from k=0 is used. Nonnegative lower sum is checked before multiplication
by the lower density constant.

The tail branch uses Mills at5 and a finite positive exponential lower
sum. Its strict rational tail comparison is explicitly checked at runtime.
The absolute Gaussian argument is enclosed by adjacent integer-square-root
endpoints before monotonicity and reflection. If the upper grid endpoint
exceeds5 while the exact argument is below5, substituting Phi(5) remains a
valid upper bound; the exact-tail branch handles arguments at or above5.

`endpoint` computes exact binomial masses by an integer recurrence, checks
division is exact, and checks the total is1. Its rows retain both cumulative
values before and after each atom. For j=0..n,

`z_j(p)=(j-n*p)/sqrt(n*p*(1-p))`

is decreasing: the sign of its derivative is minus the sign of
`j*(1-p)+(n-j)*p`, a nonnegative quantity. Each binomial CDF is also decreasing
in p, by coupling Bernoulli variables with common uniforms. Consequently a
closed cell uses the upper CDF from its left endpoint and the lower Gaussian
CDF from its right endpoint for the positive discrepancy; the opposite
discrepancy uses the left Gaussian upper and right pre-jump CDF lower.
Both jump sides and j=0,n are retained.

The score multiplier is
`sqrt(n*v)/(1-2*v)` with v=p(1-p). On the selected left-half panels, v and
this positive multiplier increase with p. Its right-endpoint v and upward
square root are therefore upper bounds. This argument is restricted to the
literal `panel` domain `0<idx<250`, including an upper endpoint at1/2.
It does not authorize applying the same right-endpoint rule to a right-half
panel or infer that an entire later table was evaluated.

## 3. Complete HIGH: expression-by-expression match

Write `p0=333/106<pi`, `sp0=4431/2500<sqrt(pi)`, `b=9/10`,
`h=p0-(22/7)^3*w^2/6`, `kap=a*(23/48)^2*d0^2`, and let `nl,nu`
enclose sqrt(n). The common helper returns all six positive terms:

| Frequency contribution | Code enclosure and direction |
|---|---|
| [1/2,b] | `2*nu*exphi(n*rate)`, optionally minimized with the chord/rational-tail bound at `cquarter` |
| Every nonzero peak core | `m*(s3+3*s5/(n*a*h*h))/(4*p0*sp0*h*roots(a)[0])`; denominator constants and roots are lower bounds |
| Every nonzero-cell wing | `m*nu*exphi(n*a*h*h*w*w)/(2*p0*p0)` |
| Zero cell, small sine argument | `exphi(n*kap*b*b)/(2*b^4*kap*nl)`, optionally minimized with the rational-tail bound when `n*kap*b*b>=1/4` |
| Zero cell, remaining argument | `nu*exphi(n*a*(23/48)^2)/(2*b*b)` |
| Comparator on the entire HIGH half-line | `nu*exphi(n/8)*(2*L(n/8)+roots(M-1)[1]/3)` |

Here `L(x)=(x+2)/(x*x+4*x+2)`. The rate obtained by testing t=1/2,b is
the manuscript's concave fourth-moment polynomial tested at u=1/4,81/100.
The chord slope53/600, intercept `(1/8)-(M+3)/384`, S3/S5 tails, sine
slope and both zero-cell options match the displayed formulas. All-index
gates are present for every exponential rate; the extra first-term and
zero-cell gates are retained. The final n>=5 gate covers the comparator.
The first-term gate is stricter than necessary for a literal-index call if
the optional candidate is inadmissible; rejection cannot produce false PASS.

The implementation uses the valid Pearson bound sqrt(M-1) in its comparator,
without the optional1.85 minimum mentioned in the manuscript. This is a
weaker valid upper bound, not an unjustified gain. The revised source map
should describe the actually executed expression rather than claim that
optional tightening was used.

Every finite-window candidate includes the entire sum. Taking the minimum
of complete bounds is valid; taking separate favorable frequency fragments
without their original hypotheses would not follow from this review.
The common caches depend only on explicit typed arguments and the fixed
arithmetic helpers. They do not depend on mutable radius/K4/K5 values. The
installed identity guard and call-site ordering retain those dependencies.

## 4. Cantelli candidate and moment grid

For Y=(X-X')^2, EY=2 and Var(Y)<=V=2M+2. For the selected fixed rational
d in{1/2,11/20,3/5,13/20,7/10}, h=2-d^2 is positive. Cantelli applied
to Y-2 gives, for the actual event E={Y>=d^2},

`P(E)>=a=h^2/(V+h^2)`.

Cauchy on Cov(Y,1_E) gives
`E[Y|E]<=2+sqrt(V*(1-P(E))/P(E))<=2+V/h=m`.
These are the directions required by HIGH_WINDOW50, including the event
boundary and P(E)=1. `admissible` checks each HIGH gate before adding a
candidate. `previous(n,M)` remains in the finite minimum. The product law
and genuine fourth moment upper bound must still come from the same witness.

`high_grid` sets U=ceil(1000*M)/1000>=M, unless U would exceed111/10,
when it keeps M. Every universal candidate is then computed from U, with its
original gates. Since EX^4<=M implies EX^4<=U, this is substitution of a
weaker moment hypothesis. It requires no monotonicity of the complete HIGH
formula as a function of M. Other moment/phase calculations keep their
original finer bounds.

## Remaining proof-to-code work

The B3/B4 INITIAL call sites install the integer exponential, common HIGH,
Cantelli candidates and moment grid at `initial25_bB.py:17--23`.
The resource call sites install the common HIGH after their signed-paired
and phase extensions at `resource25_core.py:15--23`. Thus this review is
attached to actual selected dependencies, not merely a similarly named
unused helper. It does not verify the callers' entire mathematical logic.

Still separate: every selected LOW transfer/remainder and signed Mills
variant; phase compensation and charged quadratics; both support rays and
all threshold tails; every INITIAL signed-rectangle exclusion; all same-law
resource updates; exact resource-to-count implications; and fresh complete
execution evidence. The source map marks these boundaries and all acceptance
flags false. No running capsule, candidate or acceptance hash was changed.
