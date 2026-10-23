# Exact closed-half-line Prawitz majorant

Review date: 23 October 2026.

Source checked: `berry_esseen_manuscript.tex` from the supplied v4 source
archive, SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
The principal target is lines 195–278; the ROOT4 use is at lines 5801–5817.

This note supplies a self-contained proof of the isolated analytic statement
`orig:lem:BPcardinal`, formulas (P1)–(P4), in the supplied v4 manuscript. In
particular, the pointwise inequality follows for the manuscript's exact
Fourier kernel, with the closed boundary and the positive imaginary sign.
It does not need to be inferred from a two-sided smoothing estimate or from
an unread statement in the original Prawitz article. No numerical producer
or historical acceptance receipt is used below.

The remaining proof graph, analytic reductions, derivative estimates and
computational implementations are separate review obligations.

## 1. A real-variable Beurling construction

Set

\[
 W(x)=\left(\frac{\sin\pi x}{\pi x}\right)^2\quad(x\ne0),
 \qquad W(0)=1,
\]

and define the continuous odd function

\[
 H_B(x)=\sum_{m=1}^{\infty}\{W(x-m)-W(x+m)\}+2xW(x).
 \tag{1}
\]

The series converges absolutely and locally uniformly on the real line:
for \(|x|\le R\) and \(m>2R+1\), each shifted term is bounded by a
constant times \(m^{-2}\). Thus the function and all the integer values in
what follows are unambiguous. In particular,

\[
 H_B(0)=0,\qquad H_B(j)=\operatorname{sgn}(j)
 \quad(j\in\mathbb Z\setminus\{0\}).                 \tag{2}
\]

Here \(\operatorname{sgn}(0)=0\). The corresponding classical Beurling
majorant is \(B=H_B+W\). For noninteger \(x\), its series is

\[
 B(x)=\left(\frac{\sin\pi x}{\pi}\right)^2
 \left\{\frac2x+\sum_{m=0}^{\infty}\frac1{(x-m)^2}
                    -\sum_{m=1}^{\infty}\frac1{(x+m)^2}\right\}.
 \tag{3}
\]

We prove the needed inequality directly, without importing an extremality
or Fourier-transform theorem about \(B\).

The elementary partial-fraction identity

\[
 \sum_{m\in\mathbb Z}\frac1{(y-m)^2}
       =\frac{\pi^2}{\sin^2\pi y},\qquad y\notin\mathbb Z,
 \tag{4}
\]

has the following short proof. Integrate
\(\pi\cot(\pi z)/(z-y)^2\) counterclockwise over the square with vertices
\(\pm(N+\tfrac12)\pm i(N+\tfrac12)\). The cotangent is uniformly bounded
on these edges: on the vertical edges it is a multiple of a hyperbolic
tangent, and on the horizontal edges its modulus is bounded by
\(\coth(\pi(N+\tfrac12))\). The denominator is of order \(N^2\) and the
perimeter of order \(N\), so the integral tends to zero. Its residues are
\((m-y)^{-2}\) at \(m=-N,\ldots,N\), and
\(-\pi^2\csc^2(\pi y)\) at \(y\). The residue theorem and absolute
convergence give (4).

For \(y>0\), \(y\notin\mathbb Z\), put

\[
 A(y)=\left(\frac{\sin\pi y}{\pi}\right)^2,
 \qquad S(y)=\sum_{m=1}^{\infty}(y+m)^{-2}.
\]

Subtracting (4) from (1) gives exactly

\[
 H_B(y)-1=A(y)\left\{\frac2y-\frac1{y^2}-2S(y)\right\}.
 \tag{5}
\]

The decreasing positive function \(s\mapsto(y+s)^{-2}\) satisfies

\[
 S(y)\le\int_0^\infty(y+s)^{-2}\,ds=\frac1y
       \le\frac1{y^2}+S(y).
 \tag{6}
\]

Consequently the expression in braces in (5) lies between
\(-y^{-2}\) and \(y^{-2}\). Hence

\[
 |H_B(y)-1|\le W(y)\quad(y>0).
\]

Positive integer points follow directly from (2). Oddness of \(H_B\) and
evenness of \(W\), together with their values at zero, now prove

\[
 |H_B(x)-\operatorname{sgn}(x)|\le W(x)
 \qquad(x\in\mathbb R).                              \tag{7}
\]

This is the required sign-function majorization, with its normalization
proved rather than assumed.

## 2. Recovering the exact Fourier kernel

Elementary integration gives, for every real \(x\),

\[
 W(x)=2\int_0^1(1-t)\cos(2\pi tx)\,dt.              \tag{8}
\]

For \(0<r<1\), insert (8) into the absolutely convergent Abel-weighted
series. Termwise integration is legitimate because
\(\sum_{m\ge1}r^m<\infty\). The cosine subtraction formula gives

\[
 \begin{aligned}
 \sum_{m\ge1}r^m\{W(x-m)-W(x+m)\}
   &=4\int_0^1(1-t)\sin(2\pi tx)
               \sum_{m\ge1}r^m\sin(2\pi mt)\,dt\\
   &=4\int_0^1(1-t)\sin(2\pi tx)
        \frac{r\sin(2\pi t)}{1-2r\cos(2\pi t)+r^2}\,dt.
 \end{aligned}                                                    \tag{9}
\]

For \(0<t<1\),

\[
 \left|\frac{r\sin(2\pi t)}{1-2r\cos(2\pi t)+r^2}\right|
 \le\frac12|\cot(\pi t)|,
 \tag{10}
\]

since the denominator is
\((1-r)^2+4r\sin^2(\pi t)\). The right side of (9), including its
remaining factors, is therefore dominated by

\[
 2(1-t)|\sin(2\pi tx)|\,|\cot(\pi t)|.
\]

This is integrable at both endpoints: the sine is \(O_x(t)\) at zero,
and \((1-t)\cot(\pi t)\) is bounded at one. Dominated convergence on
the integral side and absolute convergence on the series side allow
\(r\uparrow1\). The fraction in (9) tends to
\(\tfrac12\cot(\pi t)\). Also, direct integration gives

\[
 2xW(x)=\frac2\pi\int_0^1\sin(2\pi tx)\,dt,          \tag{11}
\]

including \(x=0\). Combining (1) and (9)–(11),

\[
 H_B(x)=2\int_0^1 R(t)\sin(2\pi tx)\,dt,
 \qquad R(t)=(1-t)\cot(\pi t)+\frac1\pi.
 \tag{12}
\]

Every integral in (12) is a convergent real integral. No principal-value
Fourier manipulation has been used.

Now take exactly the manuscript's kernel

\[
 K(t)=\frac{1-t}{2}+\frac i2 R(t),\qquad0<t<1.
 \tag{13}
\]

Equations (8) and (12) establish the exact identity

\[
 \boxed{\displaystyle
 M(x):=\frac12+2\lim_{\epsilon\downarrow0}\operatorname{Re}
       \int_\epsilon^1K(t)e^{2\pi itx}\,dt
       =\frac{1-H_B(x)+W(x)}2=\frac{1+B(-x)}2.}
 \tag{14}
\]

In particular, the exponent has the **positive** sign and the imaginary
part of \(K\) has the **positive** sign. The minus sign on \(H_B\) comes
from taking the real part of \(iR(t)e^{2\pi itx}\).

## 3. Closed boundary, cardinal values and the minorant

For \(x<0\), (7) gives \(M(x)\ge1\); for \(x>0\), it gives
\(M(x)\ge0\). At the boundary, (2) and \(W(0)=1\) give

\[
 M(0)=1.                                             \tag{15}
\]

Thus this majorizes the **closed** half-line, including a point mass at
zero, rather than merely the half-height convention for a jump:

\[
 M(x)\ge1_{(-\infty,0]}(x),\qquad
 1-M(-x)\le1_{(-\infty,0)}(x).
 \tag{16}
\]

The second inequality follows by subtracting the first inequality at
\(-x\) from one; its endpoint is open. Direct cardinal values are

\[
 M(j)=1_{\{j\le0\}},\qquad1-M(-j)=1_{\{j<0\}}
 \quad(j\in\mathbb Z).                              \tag{17}
\]

The proof also gives the useful global error bound

\[
 0\le M(x)-1_{(-\infty,0]}(x)\le W(x)
 \quad(x\in\mathbb R).                              \tag{18}
\]

At zero the left-hand error is exactly zero; it is not obtained by
assigning half of an atom to each side. In particular \(0\le M\le2\).

## 4. Expectations and the compensated identity

Suppose \(U\) is real and \(\mathbb E|U|<\infty\), and use the convention
\(\psi_U(t)=\mathbb E e^{2\pi itU}\). Since
\(2\int_0^1\operatorname{Re}K(t)\,dt=1/2\), (14) can be written

\[
 M(u)=1+2\operatorname{Re}\int_0^1
             K(t)\{e^{2\pi itu}-1\}\,dt.             \tag{19}
\]

The complex integral in (19) is absolutely convergent. Indeed,
\(K(t)=i/(2\pi t)+1/2+O(t)\) at zero, \(K\) is bounded near one,
and

\[
 \mathbb E|e^{2\pi itU}-1|\le2\pi t\,\mathbb E|U|.
\]

Consequently
\(\int_0^1|K(t)|\mathbb E|e^{2\pi itU}-1|\,dt<\infty\), so ordinary
absolute Fubini applies to (19). Restoring the constant real part gives

\[
 \mathbb EM(U)=\frac12+
     2\lim_{\epsilon\downarrow0}\operatorname{Re}
        \int_\epsilon^1K(t)\psi_U(t)\,dt.            \tag{20}
\]

Since \(\psi_{-U}=\overline{\psi_U}\), conjugation similarly yields

\[
 \mathbb E\{1-M(-U)\}=\frac12-
     2\lim_{\epsilon\downarrow0}\operatorname{Re}
        \int_\epsilon^1\overline{K(t)}\psi_U(t)\,dt.
 \tag{21}
\]

These are precisely the two identities (P4) under the real-part
improper convention (P0). All expectations are finite; (18) even gives
boundedness of the majorant without a moment assumption. The first
absolute moment is a sufficient hypothesis for the stated compensated
Fourier/Fubini argument. The uncompensated complex integral itself need
not converge.

## 5. Scale and sign in the physical ROOT4 formula

Let \(Y\) be integrable, let \(h\in\mathbb R\), and let \(T>0\). For
\(\chi_Y(s)=\mathbb E e^{isY}\), apply (16) and (20) to
\(U=T(Y-h)/(2\pi)\). The resulting exact normalization is

\[
 \mathbb P(Y\le h)\le\frac12+
  2\lim_{\epsilon\downarrow0}\operatorname{Re}
       \int_\epsilon^1K(t)e^{-iTth}\chi_Y(Tt)\,dt.
 \tag{22}
\]

For the v4 ROOT4 setting,
\(Z=(X_1+\cdots+X_4)/2\), \(\varphi_P(s)=\mathbb E e^{isX_1}\),
and iid summands, choose \(T=6\). Independence gives
\(\chi_Z(6t)=\varphi_P(3t)^4\). Thus (22) is exactly

\[
 F_Z(x)\le\frac12+\int_0^1\operatorname{Re}
   \{\widehat K(t)e^{-6itx}\varphi_P(3t)^4\}\,dt,
 \qquad \widehat K=2K,
 \tag{23}
\]

the manuscript's `n4all:eq:prawitz`. Writing \(D=x-Z\) and
\(S(t)=tR(t)\), its real integrand is exactly

\[
 (1-t)\mathbb E\cos(6Dt)+S(t)\mathbb E[6D\operatorname{sinc}(6Dt)],
 \qquad \operatorname{sinc}(v)=\sin(v)/v,
 \tag{24}
\]

with the continuous value at zero. This verifies both the factor six
and the sign of the sine term. No non-atomicity, finite-support, density,
or continuity-at-the-threshold assumption is needed. For (23), iid
independence and integrability are sufficient; the manuscript's bounded
support assumptions imply integrability.

## 6. Primary-source context and scope of the check

The construction is the classical Beurling sign majorant appearing in
the introduction of Graham and Vaaler's original 1981 paper. An
[author-uploaded copy](https://www.researchgate.net/publication/243079138_A_class_of_extremal_functions_for_the_Fourier_transform)
was consulted; its bibliographic identifier is
[10.1090/S0002-9947-1981-0607121-1](https://doi.org/10.1090/S0002-9947-1981-0607121-1).
The proof above independently establishes the properties used here.

[Vaaler's 1985 paper](https://doi.org/10.1090/S0273-0979-1985-15349-2)
is a relevant primary bibliographic reference. Its publisher PDF could
not be retrieved during this review, so no uninspected theorem or formula
from it is used as a proof premise. The later
[Carneiro–Vaaler primary paper](https://arxiv.org/pdf/0809.4050), introduction,
also describes the classical sign-majorant problem; its statements about
interval endpoints are not used to infer the closed-boundary value here.

The kernel in
[Shevtsova's primary paper, Lemma 4.1](https://ami.uni-eszterhazy.hu/uploads/papers/finalpdf/AMI_39_from241to307.pdf#page=23)
matches (13) on \(0<t<1\). That lemma's two-sided smoothing inequality is
not substituted for the pointwise assertion: (14)–(18) prove the latter
directly, including the atom convention.

The specific pointwise/Fourier/compensation gap identified in
`literature_inputs.md` therefore has an explicit analytic proof in this
note. This does not assert that Prawitz's entire original article, the
remaining literature inputs, the whole manuscript, any numerical
kernel implementation, or the all-index theorem has been verified.
