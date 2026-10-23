# Literal n=9--14 Fourier algorithms: bounded source and algebra audit

Date: 2026-10-24. This is a fallible internal AI source/hand-algebra review, not external independent verification, a formal proof, or a fresh numerical acceptance. No original mathematical module was imported or evaluated. Only source text, ASTs, ZIP members, JSON, sizes and hashes were processed locally.

The selected algorithms are `auxiliary9_14_v1` and `supported9_14_v1`. Their active interval, second-derivative, fixed-branch quadrature and endpoint formulas were read in the actual archives. No concrete mathematical blocker was identified in this bounded review. Complete fresh integration, the standalone scalar kappa certificate, the named published large-rho input, and acquisition of the supported theorem's same-law support premise remain distinct obligations. A process wrapper or a retained PASS label supplies none of those mathematical implications by itself.

## 1. Actual source boundary

The accompanying [source map](code_finite1014_fourier_source_map.json) records every actual source-plan entry and all directly read members. All 75 auxiliary-plan entries and all 97 supported-plan entries matched their listed SHA256 and size in the corresponding archives. This check includes provenance files as provenance; it is not acceptance of their historical assertions. Nineteen mathematical source/proof members were directly read. The archive identities come from the selected plans; this unit did not repeat a whole-archive hash pass.

Within `cutoff5_10_15.zip`, abbreviate

`A = cutoff10_20261018/fourier/auxiliary9_14_v1/`

and `S = cutoff10_20261018/fourier/supported9_14_v1/`.

| Actual source | SHA256 | Scope read |
| --- | --- | --- |
| `A/kernel.py` | `a0c2c5f0aaa1c216ae2c9c796a1e17c88217049e4b30f844e9bb7979c0cb944e` | All 140 lines: interval arithmetic, elementary functions and scalar utilities |
| `A/jet.py` | `8decccac51b92cf58b3275e291b83e775da85cd9032f81501e9592d11d591329` | All 48 lines: values and two derivatives |
| `A/batch.py` | `7fb48e7dd00dbc7cb6a1d024694b38850fdea7742e7403dd26e3280c464a1b23` | All 131 lines: original upper-Darboux route and endpoint terms |
| `A/integrate.py` | `e4bda2d00d905bf0963ca6f48d62c7d52a831e14cc695a2bae18183239bb64fc` | All 151 lines: active midpoint route and fallback |
| `A/protocol.py` | `6c22f9ed340deb21a1cd4a1325f03a64f061b00e67c34c00c7b47218ab45d26e` | All 99 lines: literal indices, closed cover, exact normalization and scope |
| `S/protocol.py` | `338fcf3646eb115ac9d9ad1554fb8f460158e6779db067a503b482c2f6f47099` | All 100 lines: two supported bands, root directions and scope |

The four files `kernel.py`, `jet.py`, `batch.py` and `integrate.py` in S are **exact-byte identical** to those in A. The map records both members, sizes and hashes. Thus this reuse is an actual source identity, rather than an inference from similar filenames. Each protocol still needs its own scope proof. The floating planners and the operating-system execution wrappers were not treated as mathematical evidence.

Proof arguments were also read from the actual inherited Fourier reduction, sine-circle, universal-zeta, bounded-support-eta and scalar-splice texts. Their full archive members, pins and precise read boundaries are in the map. In particular, this unit does not endorse the separate larger-support perturbation discussion in `BOUNDED_ETA_SECOND_REVIEW.txt:19+`.

## 2. Same-law quantities and the two root directions

Throughout, X is one standardized real marginal, EX=0, EX^2=1, rho=E|X|^3, and X' is an independent copy of **that same X**. Atoms, including an atom at zero, are allowed. Set

\[
h=E|X|,\qquad \eta=\tfrac12E|X-X'|^3-\rho.
\]

The parameter called `eta` is this independent-copy excess. It is **not** h. The old `batch.py:129` display name `absmean_upper` and its header are loose terminology: an upper bound for h would suffice, but the improved supported route supplies a direct upper bound for eta. The active `integrate.py:150` uses the accurate label `eta_upper`.

The pointwise inequality

\[
|x-y|^3\le (x-y)^2(|x|+|y|)
\]

gives E|X-X'|^3 <= 2rho+2h after the mixed first moments vanish. Therefore eta <= h <= 1. This licenses the unconditional eta upper value 1, independently of support or attainment.

For the imaginary-coordinate improvement, write

\[
r=EX_+=EX_->0,\quad A=E(X_+)^2,\quad B=E(X_-)^2,
\quad A+B=1,\quad \zeta=2AB/r.
\]

One-sided Cauchy gives A^2 <= r E(X_+)^3 and B^2 <= r E(X_-)^3, hence rho+zeta >= 1/r. Also

\[
r^2/A+r^2/B\le P(X\ne0)\le1,
\]

so AB >= r^2 and zeta >= 2r=h. Consequently zeta(rho+zeta) >= 2. The positive root

\[
\beta(\rho)=\frac{\sqrt{\rho^2+8}-\rho}{2}
\]

is decreasing, and zeta >= beta(rho). This is a universal lower bound on zeta, distinct from an upper bound on eta.

For |X| <= M, the exact same-sign deficit identity is

\[
h-\eta=E[\min(|X|,|X'|)(X-X')^2\,1_{XX'>0}].
\]

Since min(a,b) >= ab/M on [0,M], its right side is at least

\[
\frac{h\rho-2+4AB}{M}
=\frac{h(\rho+\zeta)-2}{M}.
\]

Using zeta >= h yields eta <= h+(2-rho h-h^2)/M. Put b=beta(rho). If h<b, eta <= h<b. If h>=b, the difference between this last upper bound and b is

\[
\frac{(h-b)(M-\rho-h-b)}{M}\le0
\]

whenever M <= rho+2b=sqrt(rho^2+8). Thus support 3 and rho>=1 imply eta <= beta(rho), including equality endpoints. This checks the actual supported caller, not a general statement for a larger support radius.

Accordingly `S/protocol.py:75--77` uses an **upper** root bracket beta(lo) for eta and a **lower** root bracket beta(hi) for zeta on each closed rho strip [lo,hi]. Its exact guards eta^2+lo*eta>=2, zeta^2+hi*zeta<=2, positivity and `9<=lo*lo+8` have the correct directions. `A/protocol.py:72--75` uses eta=1 and the same lower zeta bracket. No independent law or unrelated acquired witness is substituted.

## 3. Coordinate envelopes and the zeta circle

The actual inherited reductions justify, for 0<=u<=pi,

\[
\cos u\le\Re f(u)\le\cos u+(\rho-1)u^3/6,
\qquad f(u)=Ee^{iuX}.
\]

For the lower bound, the supporting function cos(v)+a v^2 with a=sin(u)/(2u)>=0 has its minimum at u on v>=0. On [0,pi], this follows from the monotonicity of sinc; after pi, the bound cos(v)>=-1 and increasing a v^2 suffice. The expectation cancels the v^2 correction because EX^2=1. The u=0 case is a limit and is not divided by in the numerical low cells.

For the upper bound and the anchored imaginary estimate, let R=|X| and W=(R-1)^2(2R+1). The elementary integrated sine comparison bounds the real-coordinate remainder by u^3 W/12. Since EW=2(rho-1), it gives the displayed upper endpoint. For the imaginary coordinate, EX=0 and

\[
|\sin(uR)-R\sin u|\le u^3R|R^2-1|/6
\]

give a Cauchy product. The identity

\[
R^3+\frac{29R^2+1}{18}
-\frac{2R^2(R+1)^2}{2R+1}
=\frac{(R-1)^2(4R+1)}{18(2R+1)}\ge0
\]

then gives

\[
(\Im f(u))^2\le (\rho-1)(\rho+5/3)u^6/36.
\]

The independent zeta-circle proof is also relevant here. Decompose the nonzero part of the centered law into centered two-point laws on (a,-b), with weights b/(a+b), a/(a+b). The mixing measure

\[
d\nu(a,b)=(a+b)d\mu_+(a)d\mu_-(b)/r
\]

has total mass 1-P(X=0); the missing zero atom contributes nothing. For one component,

\[
\Im f_{a,b}(u)=\frac{ab u}{a+b}
[\operatorname{sinc}(au)-\operatorname{sinc}(bu)].
\]

The bound |sinc(v)-sinc(w)| <= |v^2-w^2|/6 implies that the two-dimensional vector with coordinates 2a^2b^2/(a+b) and 6 Im f_{a,b}(u)/|u|^3 has Euclidean norm at most ab(a^2+b^2)/(a+b). Integrating and applying the triangle inequality gives

\[
\zeta^2+36(\Im f(u))^2/u^6\le\rho^2.
\]

The zero-frequency statement follows by continuity. Thus the active coefficient in `integrate.py:121--123`,

`min((hi-1)*(hi+5/3), hi*hi-zeta*zeta)/36`,

uses two valid upper bounds on the same imaginary square. Increasing rho to hi and decreasing zeta to a certified lower bound are both conservative.

For a real coordinate in [a,b], its square is at most max(a^2,b^2), even when the interval crosses zero. `squared_choice` (`integrate.py:16--31`) uses b=a+increment, increment>=0, and the sign of 2a+increment to select an endpoint on the **whole closed cell**. Otherwise it uses disjoint squared intervals or a constant upper bound. The analogous low-error choice uses 2(cos(u)-exp(-u^2/2))/u^3+(hi-1)/6; only its sign is needed. No differentiation of an unresolved max is licensed or performed.

## 4. Kappa=62/625: analytic reduction and separate finite arithmetic

The active modulus bound uses kappa=62/625, not the weaker 1/10 utility still present in `kernel.py:131--140`. The standalone proof source is

`cutoff25_rethink_20261015/scale_analytic/kappa_62_625_v1/`

under the `cutoff5_20261020.zip` delivery extraction. Its exact source pins and preserved certificate/capture pins are recorded in the map.

The target scalar inequality is cos(x) <= 1-x^2/2+kappa|x|^3 for all real x. On x>=T=625/124, its right side is >=1. On [0,T], use the global cosine Taylor upper P16. The sixteenth derivative of cos-P16 is cos-1<=0 and the initial derivatives vanish. The resulting removable polynomial

\[
Q(x)=\frac{1-x^2/2+\kappa x^3-P_{16}(x)}{x^3},\qquad Q(0)=\kappa,
\]

has degree 13. The fixed certificate covers [0,T] with 80 closed cells [i/16,(i+1)/16], i=0,...,79, followed by [5,625/124]. `kernel.py:79--96` of the standalone directory checks the exact coefficient list, degree, all ordered cells, fourteen canonical rational Bernstein coefficients per cell, inverse-Bernstein equality to the independently shifted polynomial, and strict positivity of every coefficient. Nonnegative Bernstein basis functions summing to one prove positivity on each whole closed cell. This architecture proves the continuous statement if its exact arithmetic checks pass; sampling is not substituted for positivity.

For the convex modulus profile, set C=1-cos(4) and

\[
A_\kappa=(8-64\kappa)/C=(1032/625)/C,
\qquad
q(z)=\begin{cases}
1/2-\kappa z,&0\le z\le4,\\
A_\kappa(1-\cos z)/z^2,&4\le z\le2\pi,\\
0,&z\ge2\pi.
\end{cases}
\]

The scalar inequality at 4 gives 0<A_kappa<=1. The pieces agree. The necessary derivative jump at 4 is **258 sin(4)+119(1-cos(4))>=0**; the old 1/10 splice condition cannot replace it. The standalone checker obtains a strict rational lower bound using S15(4) and 1-P16(4), with P18 providing the opposite cosine bracket. The Taylor inequality directions follow by integrating derivatives 1-cos or cos-1 from zero, rather than assuming decreasing Taylor terms at x=4.

On the curved branch, q'' has the sign of B(z)=6+(z^2-6)cos(z)-4z sin(z). On [4,3pi/2], B'>=0 and B(4)>=4; on [3pi/2,2pi], B>=6. The derivative joins zero at 2pi. Together with the checked derivative jump, this proves that q is nonnegative, nonincreasing and convex on the **nonnegative** half-line. Convexity of its even extension on all real numbers is neither needed nor asserted.

Apply the profile to X-X'. The measure (X-X')^2 dP/2 is a probability measure. Its weighted mean of |u||X-X'| is |u|(rho+eta), bounded above by |u|D for D=hi+eta_upper. Convex Jensen followed by the decreasing direction of q gives

\[
1-|f(u)|^2\ge2u^2 q(D|u|).
\]

Thus the line radicand is 1-u^2+2kappa D|u|^3. On a whole cell satisfying 4<=D|u|<=2pi, the curved radicand is 1-2A_kappa(1-cos(Du))/D^2. `integrate.py:65--66` and `batch.py:61--64` require `z.lower>=4` and `z.upper<=2*PI.lower`; the latter is conservative. The constant 1 and the coordinate modulus supply additional valid upper bounds. The original active caller does not infer a stronger radicand by interchanging eta and zeta.

**Unresolved fresh arithmetic input:** these 56A/B protocols hash-bind the retained kappa source/certificate/provenance. They do not call the standalone `controls.py` again. This audit did not replay it either. Its historical CHECKED status is provenance, and cannot be described as fresh scalar acceptance in this epoch.

There is a concrete unchanged standalone replay route for a later shared dependency: place the pinned `kernel.py`, `controls.py` and `PROOF.txt` in a clean directory and invoke ordinary nonoptimized `python -B controls.py`. There is no operating-system guard, external package or child-process dependency in these sources. `controls.py:12--13` constructs and fully validates the certificate, then requires rejection of 21 malformed objects. Lines 40--49 add 324 exact power/Bernstein evaluations. It creates `CERTIFICATE.json` and `CHECKED.json` with exclusive `x`, so existing outputs must not be staged as writable output files. The terminal scalar status is `PASS_GLOBAL_COSINE_KAPPA_62_625_AND_CONVEX_SPLICE_V1`, with 81 cells and 1134 positive coefficients. A fresh execution must bind its actual captures and source bytes. The path keys in its fresh source map naturally differ from historical keys; an old receipt hash must not be imposed or fabricated. This is a proposed execution route identified by source reading, not a run performed here.

## 5. Prawitz normalization, recurrence and all endpoint pieces

The inherited argument uses the doubled Prawitz kernel

\[
K(t)=(1-t)+i[(1-t)\cot(\pi t)+1/\pi].
\]

With T=c sqrt(n), the characteristic function of the standardized n-sum at Tt is f(ct)^n. Its Gaussian comparison is g(ct)^n, g(u)=exp(-u^2/2). The four terms are the low-frequency integral of |K||f^n-g^n|, the high-frequency integral of |K||f|^n, the low normal correction with |K-i/(pi t)|g^n, and the Gaussian tail E1(nc^2 tau^2/2)/(2pi). This matches the four `terms` fields and the final normalization sqrt(n)/rho. The Prawitz majorant/closed-CDF theorem remains the named upstream input; see the separate [majorant review](prawitz_majorant_review.md) and [internal crosscheck](prawitz_majorant_crosscheck.md). This unit checks its actual Fourier substitution and estimates, not a new full proof of that upstream theorem.

For nonnegative modulus upper m and Gaussian g, telescoping gives

\[
|f^n-g^n|\le |f-g|\sum_{j=0}^{n-1}m^j g^{n-1-j}.
\]

`batch.py:26--31` and `integrate.py:95--98` compute this finite sum by recurrence. There is no division by m-g, so equality, zero and degenerate endpoints cause no missing case. The alternate triangle bound m^n+g^n is independently valid; integrating it separately and taking the smaller integral upper bound is valid. Every power is computed at the literal n, rather than inferred by sample-size monotonicity.

The integration interval is partitioned into [eps,tau] and [tau,1-eps], eps=1/1024. The rho-strips and quadrature cells use closed endpoints; shared seams do not lose a point. The admissible `0<c<PI.lower`, `0<tau<=3/10` imply u=c t<pi everywhere, and u<1 on the low interval. The exact parameter guards also require eps<tau<1-eps (`batch.py:99--104`).

For the small omitted t interval, the elementary Taylor estimate

\[
|f(u)-g(u)|\le\rho|u|^3/6+u^4/8
\]

and the geometric-sum upper n give precisely the positive `lowhead` in `integrate.py:145`. The kernel inequality |K(t)|<=1+1/(pi t) integrates these terms without a singular residue. No mean or atom at zero invalidates this finite-third-moment Taylor bound.

The identity delta(x)=1/x-cot(x)>=0 and

\[
\delta(x)\le\frac{x}{3(1-x^2/6)},\qquad0\le x\le1,
\]

follow from sin(x)-x cos(x)<=x^3/3 and sin(x)>=x-x^3/6. At the normal endpoint, |K-i/(pi t)|=(1-t)sqrt(1+delta(pi t)^2); this gives `normalhead=eps+PI.upper*eps^2/2`. At t near 1, write r=1-t: |K|=r sqrt(1+delta(pi r)^2). This gives `hightail=eps^2/2+PI.upper*eps^3/3`, using |f|<=1. These are upper reserves, not discarded intervals.

For a=nc^2 tau^2/2>0, E1(a)<=exp(-a)/a. Therefore the final upper tail is exp(-a)/(pi*n*(c*tau)^2), exactly `integrate.py:143--147`. No quadrature at infinity is needed and the direction of the denominator is conservative under interval division. Together the endpoint reserves, two closed finite pieces and Gaussian tail cover the whole smoothing expression.

## 6. Directed arithmetic, smooth selection and midpoint remainder

`kernel.py:12--65` uses exact integers/Fractions and a 10^-24 outward grid. Addition, subtraction and all four signed products enclose the result. Reciprocal is permitted only when the entire denominator excludes zero, with endpoints reversed. Squaring includes zero if the input crosses zero; odd integer powers are monotone and even powers use squaring. Square roots use integer floor/ceiling roots. Bool and float are not accepted as literal rational inputs.

The sine/cosine enclosures (`kernel.py:75--91`) use Taylor degrees 65/64 at the midpoint, the next zero coefficient and explicit global remainders 7^67/67! or 7^66/66!, plus the input radius from the unit Lipschitz bound. Their declared domain is [-7,7]. The active curve uses z<=2pi<7 and all other arguments are smaller. Clipping to [-1,1] is an intersection with a known true range.

For exp(-x), x in [0,7], divide by 16, use alternating polynomials of degree 33 below and 32 above on [0,7/16], intersect with [0,1], then raise the nonnegative interval to the sixteenth power. Monotonicity supplies the output endpoints for a nondegenerate input interval (`kernel.py:93--107`). The active one-step argument u^2/2 is <pi^2/2<7; the normal n-power is obtained by integer powers, not by submitting a larger argument to this exp routine. The declared pi bracket and Machin certificate are source-read; a fresh evaluation of its finite arithmetic remains part of the numerical source stack.

`jet.py:8--48` implements exact product, reciprocal, integer-power, sine, cosine, exponential and square-root differentiation with outward intervals. The reciprocal and smooth square-root guards exclude zero denominators and zero radicands. This is essential for the second derivative; a merely nonnegative radicand would not suffice.

For cos(u)-exp(-u^2/2) at low u, direct subtraction is replaced by the degree-20 even expansion u^4 P(u^2), terms k=2,...,10. For derivative order j=0,1,2 with respect to t, `integrate.py:43--57` adds the symmetric remainder

\[
\frac{2(22)_j}{2^{11}11!}\,u_{\rm upper}^{22-j}c^j.
\]

The omitted exponential-series coefficient dominates the difference coefficient; the successive derivative-tail ratios on 0<=u<=1 are below 1/2, so the factor 2 is conservative. The separate order-sign enclosure divides the symbolic u^4 factor before bounding the tail; it never divides an interval by a tiny or zero u. It is used only to select the correct squared endpoint on a whole cell.

`choose` first fixes one valid smooth modulus majorant: 1, a strictly positive line or curved square root, or the strictly positive coordinate square root. It also fixes the squared real/error branches. The same specification is then evaluated over the whole cell and at its midpoint (`integrate.py:72--117`). It never differentiates the pointwise minimum of these candidates. For t>=3/4, the cotangent-defect upper expression itself is chosen as a smooth pointwise kernel majorant; its derivatives are the derivatives of that majorant, which is sufficient for integration. Below that threshold the exact kernel expression has a checked positive sine denominator. The threshold need not be a grid seam: a cell crossing it conservatively uses the exact expression.

For any fixed C^2 majorant F on a closed cell of width w,

\[
\int F\le w\left(F(\text{mid})+\frac{w^2}{24}\max(0,\sup F'')\right),
\qquad \int F\le w\sup F.
\]

Taking the smaller of these two upper bounds is sound. Replacing a negative upper F'' by zero weakens the bound. `upper` (`integrate.py:101--104`) has exactly this form. All value and derivative remainder intervals are already included in the jets.

If this route raises ValueError, `calculate:131--137` invokes the original upper-Darboux formula on the **same entire closed cell**. That route uses the weaker anchored imaginary coefficient without zeta improvement, so it remains a valid upper enclosure. Its midpoint cos--Gaussian difference enclosure is licensed by the |d/du(cos u-exp(-u^2/2))| <= (2/3)u^3 bound on the selected low range. A derivative eligibility failure therefore does not become an accepted empty cell. If the fallback itself cannot satisfy its mathematical domain guards, the run fails; an unknown error does not create PASS.

## 7. What each complete protocol would establish

`A/protocol.py:22--35` requires exactly n=9,...,14, target 423/1000, full rho interval [1,19/10], canonical rationals, positive strip widths and ordered exact closed seams. All six literal rows are recomputed on each strip, at meshes 128, 256 or 512. Lines 78--80 independently compare the recorded exact normalization to sqrt(n).upper times the four exact term uppers divided by lo. Dividing by lo is conservative because rho>=lo>0. Float fields are finite discovery/display values, not target comparisons.

For rho>=19/10, this protocol uses the named published Shevtsova upper

\[
\frac{208}{625}\left(1+\frac{429/1000}{\rho}\right).
\]

It is decreasing in rho. Its exact value at 19/10 is compared with 423/1000, and the final maximum includes that value (`A/protocol.py:87--95`). The overlap at 19/10 is closed. This unit did not re-read the primary publication to independently license that theorem: it remains an explicit external mathematical input. Without it, the finite-rho numerical cover alone is not a global all-law auxiliary result.

`S/protocol.py:22--38` requires |X|<=3 and the exact two closed bands:

| Band | Closed rho interval | Strict normalized target |
| --- | --- | --- |
| B0 | [1,11/10] | 1049/2500 |
| BN | [11/10,23/20] | 52/125 |

Each strip uses the two separately directed beta roots proved above and all six literal indices, at meshes 128, 256, 512 or 1024. Both bands include 11/10. Lines 81--96 recompute exact normalization and all band/index maxima. No statement is supplied for rho>23/20 by this supported protocol, and no unrestricted statement follows merely because the support string is present in a plan. An acquired same-law support statement is still necessary wherever this conditional result is used downstream.

In both protocols, duplicate JSON keys and nonfinite JSON constants are rejected; literal index checks reject bools and altered index sets. The discovery value does not enter the exact comparison. If the complete rational upper bounds do not close, the original terminal statuses are `EXACT_AUXILIARY9_14_NOT_CLOSED` and `EXACT_SUPPORTED_SAME_LAW9_14_NOT_CLOSED`. The existence of construct/replay modes does not itself establish either PASS; both modes actually recompute the integrals, and this review executed neither.

## 8. Bounded conclusion and remaining obligations

The reviewed distinct arguments are: the independent-copy eta and zeta directions; support-3 eta improvement; real/imaginary coordinate envelopes; the changed 62/625 scalar/splice reduction; symmetrization and decreasing convex Jensen; literal-n Prawitz scaling; endpoint and infinite-tail reserves; directed elementary arithmetic; stable derivatives; whole-cell branch selection; midpoint remainder; conservative Darboux fallback; and exact closed-rho/index scope. No concrete sign, scaling, atom, zero-denominator or closed-seam error was found in those selected arguments.

The following are **not** concluded by this source review:

- Fresh acceptance of the 81-cell kappa certificate, its 21 controls or its 324 identity checks. The original standalone route is identified in section 4 and remains a separate fresh scalar arithmetic dependency.
- Fresh closure of every literal Fourier strip and its actual source/capture/readback evidence. Historical result JSON and process wrappers are not that computation.
- A newly primary-source-verified Shevtsova large-rho theorem or a new full Prawitz theorem proof. These inputs are named explicitly above.
- Acquisition of |X|<=3 for the same marginal used in a supported downstream proof, or any stronger attained/contact assumption beyond the algorithm's stated theorem.
- The sharp n=10--14 count theorems, all finite indices, n=25 completion, or the global Berry--Esseen conclusion. These Fourier auxiliary/support theorems are specific dependency edges, not substitutes for the remaining joins.

The source map preserves these boundaries with fresh arithmetic acceptance false. A later completed computation can discharge its finite arithmetic obligations only with its own fresh evidence; it cannot retroactively turn this internal review into external verification.
