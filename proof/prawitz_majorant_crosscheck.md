# Independent crosscheck of the closed half-line majorant

Review date: 23 October 2026. Status: **scoped adversarial analytic read; no blocking gap found in the derivation below**. This is a second AI-assisted derivation check, not independent human verification, formal verification, an audit of Prawitz's original paper, or proof acceptance.

The derivation under review is recorded in [the majorant review](prawitz_majorant_review.md). This crosscheck independently examines its partial fractions, real-series convergence, Abel limit, Fourier signs, frequency scaling and value at the included boundary. It does not change either the manuscript or the proof-obligation graph.

The complete majorant note was read after it was saved and reread after its source-provenance header was added. That reviewed version has SHA-256 `b10bdece328be148d25ccda8d1d0c8230c5d274fe9b60a516bc5328edc7402d2`. Removing only that added header reproduces the exact previously reviewed bytes; the mathematical body is unchanged. Its displayed formulas agree with the independently checked derivation below. This identifies the version reviewed, without treating its hash as proof.

## Exact manuscript target

The source is `berry_esseen_manuscript.tex` from the supplied `hexagon-2610.00147v4-source.zip`. Its SHA-256 is:

```text
2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1
```

The target is lines 195–278, especially `orig:lem:BPcardinal`, formulas (P0)–(P7). The manuscript uses, for \(0<t<1\),

\[
 K(t)=\frac{1-t}{2}+\frac{i}{2}R(t),
 \qquad R(t)=(1-t)\cot(\pi t)+\frac1\pi,
\]

\[
 M(x)=\frac12+2\lim_{\varepsilon\downarrow0}
 \operatorname{Re}\int_\varepsilon^1K(t)e^{2\pi itx}\,dt.
\]

The order of operations matters: this is the limit of the real part. A convergent complex improper integral is not required or asserted.

The original manuscript imports the key pointwise inequality from Prawitz at lines 245–251; its following argument checks the cardinal and integrability facts. The direct construction in the companion note supplies that exact missing justification. This crosscheck does not claim that the unchanged manuscript already contained the construction or proved the imported inequality itself.

## Real construction and the error inequality

Put \(W(x)=(\sin(\pi x)/(\pi x))^2\), extended by \(W(0)=1\), and define

\[
 H(x)=\sum_{m\ge1}\{W(x-m)-W(x+m)\}+2xW(x).
\]

The series is absolutely and locally uniformly convergent on the real line. For \(x\) in a fixed compact interval and large \(m\), both translates are bounded by a constant times \(m^{-2}\). This justifies the real-series limits used here; no conditional summation convention is hidden in the definition. Since \(W\) is even, \(H\) is odd.

For a positive noninteger \(y\), let

\[
 A=\left(\frac{\sin\pi y}{\pi}\right)^2,
 \qquad S(y)=\sum_{m\ge1}\frac1{(y+m)^2}.
\]

The partial-fraction identity needed in the derivation is

\[
 \sum_{m\in\mathbb Z}\frac1{(y-m)^2}
 =\pi^2\csc^2(\pi y)=\frac1A.
\]

It can be obtained without assuming the desired majorant. Integrate
\(\pi\cot(\pi z)/(z-y)^2\) around the square with real and imaginary coordinates \(\pm(N+1/2)\). On the vertical edges the cotangent is uniformly bounded; on the horizontal edges it is bounded uniformly in \(N\). The denominator is bounded below by a constant times \(N^2\), while the perimeter is of order \(N\). The integral tends to zero. The residue at an included integer \(m\) is \((m-y)^{-2}\); the residue at \(y\) is \(-\pi^2\csc^2(\pi y)\). The residue theorem and absolute convergence give the displayed identity. The contour avoids every integer and, for sufficiently large \(N\), encloses \(y\).

Substitution in the series for \(H\) gives exactly

\[
 H(y)-1=A\left(\frac2y-\frac1{y^2}-2S(y)\right).
\]

For the decreasing function \(s\mapsto s^{-2}\), comparison with its integral on \([y,\infty)\) gives

\[
 S(y)\le\frac1y,
 \qquad \frac1{y^2}+S(y)\ge\frac1y.
\]

Consequently the expression in parentheses lies between \(-y^{-2}\) and \(y^{-2}\). Hence

\[
 |H(y)-1|\le A/y^2=W(y).
\]

Oddness gives the corresponding bound for negative nonintegers. At nonzero integer \(j\), the cardinal values of \(W\) give \(H(j)=\operatorname{sgn}(j)\), and \(H(0)=0\). Thus, with \(\operatorname{sgn}(0)=0\),

\[
 |H(x)-\operatorname{sgn}(x)|\le W(x)
 \quad\text{for every real }x.
\]

Both integral comparisons, including the lower bound for \(0<y<1\), remain valid. No restriction keeping \(y\) away from an integer is needed after the integer values are treated separately.

## Fourier identity and the Abel limit

The elementary triangular Fourier transform gives

\[
 W(x)=2\int_0^1(1-t)\cos(2\pi tx)\,dt.
\]

For \(0<r<1\), absolute convergence permits interchanging the integral with the geometrically weighted translates. Their difference is

\[
 \sum_{m\ge1}r^m\{W(x-m)-W(x+m)\}
 =4\int_0^1(1-t)\sin(2\pi tx)
 \frac{r\sin(2\pi t)}{1-2r\cos(2\pi t)+r^2}\,dt.
\]

The sign is positive: the translation difference of the two cosines is \(2\sin(2\pi tx)\sin(2\pi tm)\). For \(0<t<1\), the bracket tends to \(\tfrac12\cot(\pi t)\). Its absolute value satisfies the uniform bound

\[
 \left|\frac{r\sin(2\pi t)}{1-2r\cos(2\pi t)+r^2}\right|
 \le\frac12|\cot(\pi t)|,
\]

because the denominator is \((1-r)^2+4r\sin^2(\pi t)\). After multiplication by \((1-t)\sin(2\pi tx)\), the right side is integrable: near zero the sine cancels the cotangent pole, and near one the factor \(1-t\) cancels the other pole. Dominated convergence is therefore justified for every fixed real \(x\). On the series side, absolute convergence also permits \(r\uparrow1\).

Finally,

\[
 2xW(x)=\frac2\pi\int_0^1\sin(2\pi tx)\,dt,
\]

including \(x=0\) by direct evaluation. Combining these identities yields

\[
 H(x)=2\int_0^1
 \left((1-t)\cot(\pi t)+\frac1\pi\right)
 \sin(2\pi tx)\,dt.
\]

This integral is ordinary and finite for fixed \(x\). The proof does not pass an unbounded cotangent factor through an integral without its cancelling sine and endpoint weight.

## Match to the manuscript and the closed boundary

Taking the real part with the manuscript's **positive** exponent gives

\[
 M(x)=\frac12+\int_0^1(1-t)\cos(2\pi tx)\,dt
       -\int_0^1R(t)\sin(2\pi tx)\,dt
 =\frac{1-H(x)+W(x)}2.
\]

The sign of the sine term and the factor of two both match the displayed \(K\). For \(x>0\), the error inequality gives \(0\le M(x)\le W(x)\). For \(x<0\), it gives \(1\le M(x)\le1+W(x)\). At zero,

\[
 M(0)=\frac{1-0+1}{2}=1.
\]

Therefore

\[
 M(x)\ge\mathbf1_{(-\infty,0]}(x),
 \qquad 1-M(-x)\le\mathbf1_{(-\infty,0)}(x).
\]

The second inequality has the strict half-line exactly as required: at zero its left side is zero. At integer nodes, \(M(j)=\mathbf1_{\{j\le0\}}\). The construction also gives \(0\le M\le2\), so its expectation exists for every probability law.

## Expectation compensation and physical scaling

For integrable \(U\),

\[
 M(U)=1+2\operatorname{Re}\int_0^1K(t)
                   \{e^{2\pi itU}-1\}\,dt.
\]

Near zero, \(K(t)=i/(2\pi t)+O(1)\), while
\(|e^{2\pi itU}-1|\le2\pi t|U|\). The expectation of the absolute compensated integrand is integrable. Fubini is consequently valid for this compensated expression. Adding back the real constant term recovers exactly manuscript (P4), with its real-part improper convention. Conjugation yields the displayed \(\overline K\) identity for \(1-M(-U)\). No complex improper integral of the uncompensated singular term is interchanged with expectation.

For a real integrable \(Y\), threshold \(a\), frequency \(T>0\), and characteristic function \(\chi_Y(s)=Ee^{isY}\), set \(U=T(Y-a)/(2\pi)\). The event \(U\le0\) is precisely \(Y\le a\), and

\[
 F_Y(a)\le\frac12+2\operatorname{Re}\int_0^1
 K(t)e^{-iTat}\chi_Y(Tt)\,dt.
\]

Thus there is no missing \(2\pi\) in the physical-frequency formula. In the manuscript's four-summand use at lines 5801–5817, \(Y=Z=(X_1+\cdots+X_4)/2\) and \(T=6\), so \(\chi_Z(6t)=\varphi_P(3t)^4\) and \(\widehat K=2K\). With \(D=a-Z\), the real integrand is \((1-t)E\cos(6Dt)+R(t)E\sin(6Dt)\), with a positive sine term, matching line 5817 after writing \(S(t)=tR(t)\). This checks that use's normalization and sign; it does not audit its later derivative or quadrature estimates.

## Scope of the result

The derivation supplies a direct analytic proof of the selected pointwise closed-half-line majorant, its cardinal values, the stated compensated expectation identity and the displayed scaling. The crosscheck found no blocking convergence, sign or atom-boundary gap in those steps.

The original Prawitz article was not independently audited here. This note does not verify every smoothing theorem attributed to it, every later Fourier/resource/contact interface, any finite certificate, a native execution contract, or the global proof. Independent human review and formal verification remain separate. No proof-obligation node is closed or promoted to accepted by this document.
