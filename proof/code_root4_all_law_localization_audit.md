# ROOT4: from an unrestricted violating law to the bounded physical class

24 October 2026. This is a fallible internal AI source and hand-algebra
review, not external independent mathematical verification or formal
verification. No original mathematical module, numerical kernel or test
was imported or executed. The four preceding ROOT4 inner notes and maps
remain unchanged. This unit checks the preceding all-law implication,
rather than inferring it from kernel validity or a completed receipt.

The supplied v4 `berry_esseen_manuscript.tex` is384847 bytes, SHA256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
The [source map](code_root4_all_law_localization_source_map.json) records
the exact sections, labels, old analytic-note pin and current caller
contexts. It also distinguishes a current wrapper read from the earlier
actual11 export validation. No private absolute paths are recorded.

## 1. Precise conditional proposition

Put `K3=59 sqrt(3)/250`, `c0=256/625`, `T=4097/10000`.
The following three mathematical inputs suffice:

* G3: every standardized law with finite third absolute moment satisfies
  `Delta3(P)<=59 rho(P)/250`, equivalently `C3<=K3`.
* E: the selected iid structural bound
  `R_n(P)<=.3031*(1+.646/rho(P))` holds in the stated normalization.
* B4: the complete bounded-law inequalities establish the ROOT4 bound T
  for every standardized P with `|X|<=17/4`, `rho(P)<46/25`,
  `625/2116<=w<=1`, `|beta|<=13/20`, every real threshold and both
  genuine orientations.

Then `C4<=T<CE`. The argument below derives this implication. Acquiring
G3 and B4 requires their complete valid arithmetic and analytic checks;
their truth does not follow from a historical status, a source hash or
this note. E is an explicit external mathematical input; its located
primary statement and normalization are recorded in
[literature inputs](literature_inputs.md).

G3 is the manuscript's certificate-conditional Theorem `n3:thm:main`,
lines5128–5138. It is an all-law inequality, not an estimate for the
three-summand score of a selected discrete law. The earlier
[n2/n3 analytic review](small_indices_analytic_review.md) and separate
checker/observed08 records address its different obligations. This
four-summand implication needs G3 and does not require C2, any monotonicity
of C_n, or an assumption that the three-summand maximizer is P.

## 2. Why an unrestricted maximizing pair exists

At lines368–399, `cut49:global:attainment` applies to every fixed n>=1,
including equality at CE. Since rho>=1, `0<Cn<=sqrt(n)`; positivity
already follows from a symmetric binary law at the top sum atom.
Reflection and approximation from below identify the absolute-discrepancy
supremum with the positive closed-CDF supremum. No continuity or absence
of atoms in the sum is assumed.

For a positive maximizing sequence with scores at least c>0,
`rho_j<=sqrt(n)/c=:M`. The third-moment bound gives the uniform tails
`E[X^2;|X|>A]<=M/A` and `E[|X|;|X|>A]<=M/A^2`.
Tightness and these first/second-moment tails preserve mean0 and
variance1 under a weak subsequential limit P. After another subsequence,
rho_j converges to b, while lower semicontinuity initially gives only
`rho(P)<=b`. Uniform integrability of the third moments is not assumed.

For a negative threshold, Chebyshev bounds the positive discrepancy by
`n/H_j^2`; for a positive threshold the same bound follows from the
Gaussian upper tail. Thus `|H_j|<=n^(3/4)/sqrt(c)`, allowing a convergent
threshold subsequence. Fixed-n convolution preserves weak convergence.
Apply closed-set Portmanteau at H+epsilon and then let epsilon decrease
to0. Right continuity gives

    F_(n,P)(H)-Phi(H/sqrt(n)) >= Cn*b/sqrt(n).

The normalized score of P is therefore at least `Cn*b/rho(P)>=Cn`.
The definition of Cn forces equality and `rho(P)=b`. This proves a
positive CLOSED maximizing pair and third-moment convergence as a
conclusion of extremality. It also covers Cn=CE. A positive discrepancy
does not mean that H itself is positive.

## 3. Raw contamination and contact at every support point

For the actual attaining pair, perturb by
`P_epsilon=(1-epsilon)P+epsilon delta_y`, with raw H fixed. Its mean is
epsilon*y and variance is
`v_epsilon=1+epsilon(y^2-1)-epsilon^2*y^2`, positive for sufficiently
small nonnegative epsilon. Standardization changes the Gaussian
threshold to `(H-n epsilon*y)/sqrt(n*v_epsilon)` but leaves the raw sum
event exactly `sum X_i<=H`. Its CDF is a polynomial in epsilon, whose
derivative is `n(F_(n-1,P)(H-y)-F_(n,P)(H))`.

For the raw centered third absolute moment r_epsilon, dominated
differentiation needs only an integrable quadratic majorant and gives
`r'_0=|y|^3-rho-3 beta*y`, with `beta=E[X|X|]`, the signed second
moment, not E X^3. The variance-normalization derivative and Gaussian
derivative then give exactly the influence function at lines413–415.
There is no differentiation of a CDF across a moving atom.

Every contaminated standardized signed score is bounded by the same
fixed-index unrestricted Cn and equals it at epsilon0. Its right
derivative I(y) is nonpositive for every real y. Integration against
the SAME P gives zero by convolution and its actual moments. I is
integrable and upper semicontinuous: `y -> F_(n-1,P)(H-y)` is upper
semicontinuous for a closed CDF. Thus I=0 almost surely, and its closed
zero set contains the full closed support, including accumulation
points and arbitrarily small atoms.

The leading term of rho*I is `-Cn*|y|^3`; the remaining unbounded terms
are at most quadratic and the CDF term is bounded. Since Cn>0, contact
first gives qualitative compact support. This step needs no predecessor
bound, numerical radius, fourth moment, finite-support restriction or
Berry–Esseen constant monotonicity.

## 4. The exact C3 predecessor edge

For n4 write `C=C4`, `z=H/2`, `F=F_(4,P)(H)` and `G=F_(3,P)`.
Global maximality gives `F=Phi(z)+C*rho/2`. G3 applies to this SAME P:

    G(H-y) <= Phi((H-y)/sqrt(3))+K3*rho/sqrt(3).

Multiplication by8 and substitution into contact yield

    rho I(y) <= H4(z,y)+4rho(K3-C)+4rho(s-1)K3
                +C[-|y|^3+(3rho/2)y^2+3beta*y-rho/2],
    s=sqrt(4/3).

This is exactly `n4all:eq:predecessor`, lines5599–5602. It bounds the
same-law deleted sum by a universal C3 upper; it does not identify its
extremizer with P. The identity `c0^2-K3^2=1069/1562500>0` gives
`K3<c0<T`. Under the contrary hypothesis C4>T, the term
`4rho(K3-C)` is strictly negative. The scale term is positive and can
be enlarged by replacing K3 with C. This is the only predecessor use
in the quantitative support polynomial.

## 5. The special n4 Gaussian remainder

The manuscript's stronger localization does not merely reuse the old
finite Gaussian remainder1/2. Define u=z-y/2 and
`f(lambda)=Phi(u/sqrt(1-lambda))`. For lambda in[0,1/4],

    f''(lambda)=r(3-r^2)phi(r)/[4(1-lambda)^2],
    r=u/sqrt(1-lambda).

The bound `sup |r(3-r^2)phi(r)|<3/5` has the stated elementary proof.
For t=r^2 in[0,3], use the positive partial series for e^t and

    (9/4)(1+t+t^2/2+t^3/6)-t(3-t)^2
       >=(3/4)[7(t-9/14)^2+3/28]>0.

The lower quadratic follows by replacing `-(5/8)t^3` with
`-(15/8)t^2` on this interval. Multiplication by `phi(0)^2<4/25`
proves the required squared bound. For t>=3,
`|r(3-r^2)|phi(r)<=|r|^3 phi(r)<1/2`; the latter maximum follows
at t3 using pi>3 and e>8/3.

Consequently `|f''|<4/15`, and the Taylor remainder in
`8(f(1/4)-f(0))=u phi(u)+E` is `<1/15`.
The second-order translation of Phi(z-y/2) cancels the source's linear
and quadratic terms. Its remainder is at most `phi(0)|y|^3/6`.
What remains is `u phi(u)-z phi(z)`, bounded by
`phi(0)|y|/2<|y|/5`, because `sup|(x phi(x))'|=phi(0)`.
This proves the full stated uniform inequality

    |H4(z,y)| < phi(0)|y|^3/6+|y|/5+1/15

for all real z,y, before any threshold restriction or higher-moment
assumption. Its signs and factor8 agree with raw-sum scaling.
Another agent in this same AI team separately cross-read only
lines5603–5637 and the hand algebra above, finding no sign or constant
issue. In particular the gap in the displayed quadratic comparison is
exactly `(5/8)t^2(3-t)>=0`. This narrow internal cross-read is not an
external review of the full localization argument.

## 6. Moment and support localization above c0

Input E and C>c0 give
`rho<979013/532500<46/25`. The canonical Q reference has
`r=rho(Q)<=rho`, `0<w<=1`, and
`r^2=(1+beta^2)^2/[w(1-beta^2)]`. This identity is derived from tagged
first/second moments and the nonnegative defect W. It does not assume
the actual law has three support points. Its monotonicity gives
`|beta|<321/500` from the exact displayed comparison with `(46/25)^2`,
and `r^2>=1/w` subsequently gives `w>625/2116`.
For an additional small rational check of that beta gate, at
`z=4121/10000` the difference
`(1+z)^2-(2116/625)(1-z)` is `363217/100000000>0`.
The difference increases for z>=0, and `(321/500)^2>4121/10000`.

For `r_y=|y|>=4`, after dropping the strictly negative predecessor
difference and enlarging the positive scale term, its C bracket is
strictly below

    B(r_y)=-r_y^3+(69/25)r_y^2+(963/500)r_y+23/100.

Here `4(s-1)<5/8`, rho<46/25 and `3|beta|<963/500` were used with
the correct signs. B and its first two derivatives are negative at4,
and B'''=-6. Hence B<0 on the entire ray. ONLY after establishing
this negativity may C>c0 be substituted to enlarge C times the bracket.
The uniform Gaussian estimate gives

    rho I(y)<P(r_y),
    P(r)=-(643/1875)r^3+(17664/15625)r^2
          +(77257/78125)r+7541/46875.

The coefficient arithmetic agrees with `r^3/15+r/5+1/15+c0*B(r)`.
At101/25, P,P',P'',P''' have the four negative rational values shown
at lines5662–5663. Their derivative ordering makes P strictly negative
on the whole exterior ray. The support contact I=0 therefore excludes
EVERY support point with `|y|>=101/25`, including endpoints and
accumulation points. There is no finite grid or finite-support premise
in this argument.

The resulting class is strictly inside the numerical class:
`101/25<17/4`, `321/500<13/20`, and strict w lower bounds are contained
in the closed root. Positive and negative beta are both retained. Eta0
allows the reference's zero atom; it is not silently reduced to a
Bernoulli family. Bounded support now licenses later fourth moments
without introducing a new axiom.

## 7. The older17/4 note has a different threshold premise

The frozen `first_critical_support_17_4_2026_10_01.md`, SHA256
`2beabc365118ae67c6263580ec8ae9cc300a071681d8a7587c627ce5dfc40ca6`,
assumes `C_(m-1)<CE<=C_m`. It is a valid first-critical conditional
route with its stated inputs, but alone cannot prove the stronger
`C4<=T` because T<CE: a hypothetical C4 in(T,CE) would not satisfy its
premise. With a complete B4 bound it can instead exclude C4>=CE,
including equality, and prove the weaker strict statement C4<CE.

There is no such threshold gap in the v4 theorem as written: its
separate Lemma `n4all:lem:owner` uses C4>c0 and the quantitative G3
bound. That stronger implication must be the explicit source join for
the claim C4<=T. The old frozen note need not be edited or its premise
silently weakened.

## 8. Actual caller and final contradiction

The actual selected request builders use closed root rectangles, exact
rhoQ minima and their own eta cuts. Their bound formulas require an
arbitrary standardized law in the physical class, not an additional
hidden C4>=CE assumption. The earlier four inner source reviews
followed those formulas. The original driver's standing-premise text
correctly leaves all-law placement outside the program.

The actual receipt metadata records all260 parents closed with zero
unresolved classes. Its183 direct-parent route labels include54 empty
parents, corresponding to129 nonempty direct parents; the other43 and34
parent classes use the two four-child alternatives. This is metadata
from the previously revalidated actual export, not a new replay or
proof of the analytic implication. The wrapper still distinguishes
`conditional_physical_root_verified` from `all_law_C4_verified`; the
latter and the all-index flag remain false.

Given G3, E and B4, suppose C4>T. Attainment gives a positive closed
maximizing pair, and the stronger owner lemma places that actual law
inside B4's class. B4 bounds its score by T, contradicting its score
C4>T. Therefore C4<=T. For a general law the other discrepancy is
covered by
`Phi(x)-F_Z(x)<=Phi(x)-F_Z(x-)=F_(-Z)(-x)-Phi(-x)`, retaining the atom.
The selected exact Machin/sqrt10 comparison establishes T<CE. Equality
C4=T is not excluded and is not needed for the conclusion.

**Limited outcome:** no confirmed attainment, contact, localization,
predecessor, endpoint or atom-handling gap was found in this conditional
chain. The all-law implication is explicit and acyclic. Its acquisition
inputs remain separate: full valid G3, full valid bounded-law B4,
the selected iid structural theorem and the physical closed-CDF
majorant/numerical implications. This internal review does not
automatically promote any all-law or global proof-acceptance flag.
