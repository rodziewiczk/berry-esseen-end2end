# Scoped analytic review of the two- and three-summand reductions

Review date: 23 October 2026. Status: **scoped read completed; no blocking gap found in the analytic chain described below**. This is an AI-assisted mathematical readback, not formal verification, an independent human verification, a complete checker implementation audit, or proof acceptance.

The subsequent [checker source review](small_indices_checker_review.md) records the separate readback of the selected acceptance implementations and its connection to the completed notebook 08 run. The implementation limitations below describe this analytic note's own scope; they are not a claim that the companion review was omitted.

## Source and scope

The reviewed source is the user-supplied `hexagon-2610.00147v4-source.zip`, file `berry_esseen_manuscript.tex`. The SHA-256 of the reviewed TeX file is:

```text
2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1
```

The archive entry is exactly `berry_esseen_manuscript.tex`, 384,847 bytes; its digest matches the reviewed copy. Line numbers below refer to those exact bytes. The source was read without modification. No mathematical producer or verifier was run as part of this review.

| Source location | Reviewed content |
|---|---|
| Lines 168–192, `orig:thm:defect` | Elementary factorization proving the necessary third-moment domain |
| Lines 4822–5109, `n2:section` | Two-summand attainment, contact, bounded support and finite-certificate implication |
| Lines 5112–5485, `n3:section` | Three-summand attainment, contact, bounded support, independence-null features and finite-certificate implication |
| Lines 42–45 | Definitions of `Lam = 59/250`, `rhoMax = 15/8`, 111 certificate cells and 6,549 coefficients |

The four-summand section begins at line 5488 and is outside this review. The conclusions below concern the logical reduction from the specified finite inequalities to the two stated unrestricted-law bounds. They do not assert that every implementation establishing those inequalities has been audited.

## Selected external structural input

For centered, unit-variance identically distributed summands, the reduction uses

\[
 C_n(P)=\frac{\sqrt n\,\Delta_n(P)}{\rho(P)}
 \le \frac{1661}{5000}\left(1+\frac{429}{1000\rho(P)}\right),
 \qquad \rho(P)=E|X|^3.
\]

The exact constants and normalization are stated in Shevtsova's own monograph, Theorem 2.7, equation (2.13), printed page 55 (PDF page 54): the selected term is \(0.3322(\rho+0.429)/\sqrt n\) in the bound for \(\Delta_n\). The primary-source statement and normalization check is recorded in [the literature-input note](literature_inputs.md), with the [author's source, arXiv:1912.06482v3](https://arxiv.org/pdf/1912.06482v3#page=54). That statement check does not independently reverify the external theorem's numerical proof.

For n2 the structural estimate excludes \(\rho\ge2\) from any violation of \(C_2\le2\sqrt2/7\). For n3 it excludes \(\rho\ge15/8\) from any violation of \(C_3\le59\sqrt3/250\). These comparisons are the manuscript's exact scalar obligations; locating the external theorem does not substitute for their certificate checks.

## Attainment and the treatment of atoms

The compactness arguments at lines 4863–4876 and 5156–5175 are valid for the stated bounded-third-moment classes. The second moment gives tightness. A uniform third-moment bound gives uniform integrability of the first and second moments, so weak limits retain mean zero and variance one. Lower semicontinuity retains the upper bound on the third absolute moment. The third moment need not be continuous.

Convolution preserves weak convergence. The Kolmogorov distance to the fixed continuous Gaussian CDF is continuous under weak convergence, even when the limiting sum has atoms. More explicitly, if the Levy inequalities hold with error \(\varepsilon\), comparison after shifting the threshold gives

\[
 |\Delta(F_j,\Phi)-\Delta(F,\Phi)|
 \le \varepsilon+\omega_\Phi(\varepsilon),
\]

where \(\omega_\Phi\) is the uniform modulus of continuity of \(\Phi\). Since \(\rho\ge1\) is lower semicontinuous and the numerator is nonnegative and continuous, \(\Delta_n/\rho\) is upper semicontinuous. It attains its maximum on the compact class. The strict structural comparison excludes the upper moment boundary for a violating maximizer.

The reflection step at lines 4879–4890 and 5176–5185 uses both signed discrepancies:

\[
 F(t)-\Phi(t/\sqrt n),\qquad
 \Phi(t/\sqrt n)-F(t-).
\]

Both are upper semicontinuous and vanish at infinity. The supremum of the negative closed-CDF discrepancy agrees with the supremum using the left limit. The exact reflection identity

\[
 F_{-S}(-t)=1-F_S(t-)
\]

therefore permits a finite threshold with positive closed-CDF discrepancy. No atom or exact collision is removed.

## Raw contamination and contact on the entire support

The contact derivations at lines 4905–4931 and 5202–5232 keep the raw event fixed. For a fixed real \(y\), put

\[
 R_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_y,
 \quad \mu_\varepsilon=\varepsilon y,
 \quad \sigma_\varepsilon^2=1+\varepsilon(y^2-1)-\varepsilon^2y^2,
 \quad x_\varepsilon=\frac{t-n\mu_\varepsilon}{\sqrt n\,\sigma_\varepsilon}.
\]

For sufficiently small nonnegative \(\varepsilon\), standardization is well-defined and the sum event remains exactly \(Y_1+\cdots+Y_n\le t\). Its probability is polynomial in \(\varepsilon\); the argument does not differentiate a CDF across a moving jump.

Writing \(F=P^{*n}(( -\infty,t])\), \(x=t/\sqrt n\), \(D=F-\Phi(x)>0\), \(\lambda=D/\rho\), \(m=E[X|X|]\), and \(G=P^{*(n-1)}\), direct differentiation gives

\[
 x'_0=-\sqrt n\,y-\frac{x}{2}(y^2-1),
 \quad \rho'_0=|y|^3-3my+\frac\rho2-\frac{3\rho}{2}y^2,
 \quad F'_0=n\{G(( -\infty,t-y])-F\}.
\]

The derivative of the shifted absolute third moment has an integrable quadratic majorant; no fourth moment is needed. Global maximality makes the right derivative of the selected normalized score nonpositive. The resulting inequality is

\[
 nG(( -\infty,t-y])\le Q(y),
\]

\[
 Q(y)=\lambda|y|^3-\frac{x\phi(x)+3D}{2}y^2
 -(\sqrt n\,\phi(x)+3\lambda m)y
 +nF+\frac{x\phi(x)+D}{2}.
\]

Both sides integrate to \(nF\) under \(P\). Their nonnegative gap is therefore zero almost surely. The CDF expression as a function of \(y\) is upper semicontinuous, and \(Q\) is continuous, so the gap is lower semicontinuous. A positive gap at any support point would give a neighborhood of positive measure with positive gap. Thus equality holds at every point of the closed support, including accumulation points.

## Bounded support and the moment domain

The support arguments at lines 4934–4955 and 5235–5267 use only the available third-moment information. The manuscript's coefficient bounds give the following lower polynomials, with \(r=|y|\):

\[
 P_2(r)=\frac27r^3-\frac{67}{56}r^2-\frac{23}{14}r-\frac18,
 \qquad
 P_3(r)=\frac8{35}r^3-\frac45r^2-\frac85r-\frac18.
\]

The displayed identities

\[
 P_2(6+u)-2
 =\frac27u^3+\frac{221}{56}u^2+\frac{104}{7}u+\frac{373}{56},
\]

\[
 P_3(6+u)-3
 =\frac8{35}u^3+\frac{116}{35}u^2+\frac{472}{35}u+\frac{2197}{280}
\]

have strictly positive coefficients for \(u\ge0\). They contradict contact, whose left side is at most \(n\), at every support point with \(|y|\ge6\). The hypothetical violating maximizer consequently has support in \((-6,6)\). This is an extremizer argument, not a truncation of an arbitrary law or a finite-atom assumption.

The factorization at lines 168–192 gives, without a further external theorem once that factorization is checked,

\[
 \rho\ge\frac{\gamma^2+2}{\sqrt{\gamma^2+4}},
 \qquad \gamma=EX^3.
\]

Its two nonnegative factors on the positive and negative half-lines and its expectation identity agree with the displayed coefficients. Squaring its positive sides gives

\[
 h(\gamma^2,\rho)
 =\rho^2(\gamma^2+4)-(\gamma^2+2)^2\ge0.
\]

Together with \(\rho\ge1\) and \(|\gamma|\le\rho\), this supplies the necessary outer moment domains used by both certificates. The proof does not require every point of either outer domain to be realizable. On the stated rectangles, \(h\) increases in \(\rho\ge0\) and decreases in \(\gamma^2\ge0\) when \(\rho\le2\); the described domain-discard test is therefore a valid sufficient test for being outside the domain.

## From complete finite inequalities to all-law bounds

For n2, independence makes the expectation of the tensor majorant in the five features \((1,y,y^2,y^3,|y|^3)\) exactly the stated polynomial \(q(\gamma,\rho)\). The 70 intervals cover \([-5/2,1]\). The pointwise inequality uses the upper endpoint of each threshold interval; the Gaussian scalar inequality uses its lower endpoint. Monotonicity therefore bounds every threshold in each interval. Cantelli's inequality handles the left tail, the stated rigorous Gaussian enclosure handles the right tail, and reflection handles the other signed discrepancy. This establishes the finite-certificate implication at lines 5009–5028 for arbitrary bounded laws, followed by the all-law contradiction at lines 5097–5109.

For n3, higher powers appear only after bounded support has been established. In the seven features \((1,y,y^2-1,y^3,|y|^3,y^4,y^5)\), every permitted product involving a fourth or fifth power has a zero-mean factor in another coordinate. Independence therefore eliminates it without prescribing a fourth or fifth moment. The 59 symmetrized features comprise 49 zero-expectation terms and 10 terms contributing the stated monomials in \((\gamma,\rho)\).

The n3 inequalities cover the complete cube \([-7,7]^3\), which contains the witness support, and the consecutive threshold range \([-7/2,3/2]\). The same endpoint monotonicity, Cantelli tail and Gaussian tail reasoning gives the contradiction at lines 5364–5387. It does not use the two-summand theorem.

The described continuous-domain methods are mathematically sufficient when implemented as stated: nonnegative Bernstein coefficients imply nonnegativity on a full cell; the n3 signed affine tests imply the required event and complement inequalities; unresolved cells must be rejected; and the included event plane must satisfy the majorant value at least one. Coordinate symmetry and the ordered-box discard condition do not omit ordered points. The complete \(6^3\) grid check proves each degree-five polynomial identity, as stated, but is not a second positivity verification. Complete parsing, coverage, exact arithmetic, Gaussian enclosures and fail-closed behavior of the actual programs remain separate implementation-review obligations.

## Editorial correction and dependency boundary

At lines 4880–4881, “positive maximizing point,” and at lines 5366–5367, “positive maximizing raw threshold,” should read **a maximizing threshold with positive discrepancy**. Reflection gives a positive discrepancy, not necessarily a positive threshold. The proof already covers all real thresholds and does not require \(t>0\), so this wording issue does not invalidate the chain reviewed here. The manuscript was not edited.

The logical inputs for these two standalone reductions are the selected structural estimate, the elementary moment-domain factorization and their respective attainment/contact/support/certificate arguments. Neither reduction needs Prawitz, the general Fourier/resource/count framework, or a dependency from n3 to n2. The proof graph records these as separate scoped analytic obligations; this note does not change that graph or close its nodes.

## Remaining verification boundary

The [observed notebook 08 record](observed_runs.md) documents actual completion of the six finite n2/n3 arithmetic stages in BASIC mode. This scoped analytic read is additional evidence about their mathematical implication. Neither record supplies trusted native execution acceptance or a complete source-level checker audit. An independent human review or formal verification remains distinct work.

No all-law theorem, literature-proof obligation or all-index conclusion is promoted to accepted by this note. C4 and later indices, the tail argument and the global proof composition are outside its conclusions.
