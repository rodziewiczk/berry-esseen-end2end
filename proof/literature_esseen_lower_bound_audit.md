# Esseen lower-bound implication from a full primary lattice theorem

Review date: 24 October 2026. This is a fallible internal AI source and hand-algebra review, not external independent verification or a formal proof. No archived mathematical module was imported or executed. No all-index acceptance flag is changed.

## Result and exact boundary

The implication needed by the manuscript, \(C^*\ge C_E\), follows by the short derivation below from Esseen's fully located 1945 lattice expansion. The original 1956 article has **not** been read in full. This note supplies a different, explicitly identified primary-source route to that limited implication; it does not relabel the 1956 proof as checked.

The separate claimed one-summand input \(C_1\le0.3704\) of Bentkus--Kirsa (1989) remains without a full-primary-text proof read in this audit. Bibliographic matches and later quotations do not acquire that input.

The supplied v4 manuscript is `berry_esseen_manuscript.tex`, SHA256 `2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`. Its normalization is at lines 87--100; the lower-bound implication is used at lines 9122--9127 and 9164, while the one-summand input occurs at lines 9149--9150. Sources were not edited.

## Full primary source and what was read

C.-G. Esseen, *Fourier analysis of distribution functions. A mathematical study of the Laplace-Gaussian law*, Acta Mathematica **77** (1945), 1--125, DOI [10.1007/BF02392223](https://doi.org/10.1007/BF02392223). A complete original scan is available from [Tsinghua's institutional mathematical archive](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/5654-11511_2006_Article_BF02392223.pdf).

The downloaded PDF has 125 pages, 4,607,200 bytes, SHA256 `717a6db268c14e27c2351b7ba5eb9726e3e44162a1320474cc83841f813e2386`. Printed page numbers equal one-based PDF page numbers. The source was inspected as rendered page images as well as extracted text:

- Page 9: the distribution-function convention at a jump is the average of the two one-sided limits.
- Pages 53--55, equations (23), (26)--(31): maximal lattice span, lattice location, periodic correction and its value away from jumps.
- Page 56, Chapter IV, Theorem 3, equation (35): the first-order lattice expansion for independent identically distributed centered variables of positive finite variance and finite third absolute moment.
- Pages 57--59: the displayed proof of Theorem 3, including the frequency decomposition and the final smoothing estimate (47). Its bounds are independent of the evaluation point, licensing the moving midpoint used below.

This is a read of the selected theorem statement and its displayed proof, not a fresh audit of every earlier Fourier/smoothing lemma invoked by that proof. In particular Chapter II, Theorem 2b remains an explicitly imported analytic theorem here. No eventual Bernoulli optimality theorem is needed.

## Licensed analytic statement in current notation

Write \(\varphi(x)=e^{-x^2/2}/\sqrt{2\pi}\). For a centered lattice variable of variance \(\sigma^2>0\), third moment \(\alpha_3\), finite third absolute moment and maximal span \(d>0\), Esseen's selected expansion is

\[
 G_n(x)=\Phi(x)+\frac{\alpha_3}{6\sigma^3\sqrt n}(1-x^2)\varphi(x)
       +\frac d{\sigma\sqrt n}\psi_n(x)\varphi(x)+o(n^{-1/2}).
\]

Here \(G_n\) uses the source's midpoint convention, and the periodic correction has \(Q_1(u)=\tfrac12-u\) for \(0<u<1\), repeated with period one. If \(\xi_n\) is the least nonnegative lattice position of the standardized sum, then \(\psi_n(x)=Q_1((x-\xi_n)\sigma\sqrt n/d)\). Only its value \(Q_1(1/2)=0\), away from a jump, will be used. The remainder is uniform in the evaluation point; no uniformity in the underlying law is claimed or needed.

## Direct derivation of the required lower bound

Fix a rational \(p\in(0,1/2)\), put \(q=1-p\), and let

\[
 X=\frac{B-p}{\sqrt{pq}},\qquad P(B=1)=p,
 \qquad Z_n=\frac{X_1+\cdots+X_n}{\sqrt n}.
\]

These are admissible iid laws for the manuscript: \(EX=0\), \(EX^2=1\), and every absolute moment is finite. Direct two-point evaluation gives

\[
 \kappa_3=EX^3=\frac{q-p}{\sqrt{pq}},\qquad
 \rho=E|X|^3=\frac{p^2+q^2}{\sqrt{pq}},\qquad
 d=\frac1{\sqrt{pq}}.
\]

Take only positive integers \(n\) for which \(np\) is integral. There are infinitely many such integers because \(p\) is rational. The standardized binomial has a mean atom at zero, its next lattice point is \(d/\sqrt n\), and its least nonnegative lattice position is \(\xi_n=0\).

Set \(x_n=d/(2\sqrt n)\), the midpoint between those two points. This is not an atom. Consequently the source's \(G_n(x_n)\) equals the manuscript's **closed** probability \(P(Z_n\le0)\); the mean atom is included. Moreover \(\psi_n(x_n)=Q_1(1/2)=0\). The licensed expansion therefore gives

\[
 P(Z_n\le0)=\Phi(x_n)+\frac{\kappa_3}{6\sqrt n}(1-x_n^2)\varphi(x_n)
                  +o(n^{-1/2}),
\]

and elementary differentiation of \(\Phi\) at zero yields

\[
 \lim_{\substack{n\to\infty\\np\in\mathbb Z}}
 \sqrt n\bigl(P(Z_n\le0)-\tfrac12\bigr)
 =\varphi(0)\left(\frac d2+\frac{\kappa_3}6\right)
 =\frac{\varphi(0)}{\sqrt{pq}}
       \left(\frac12+\frac{q-p}6\right)>0.
\]

For this fixed law the absolute Kolmogorov discrepancy is at least its positive discrepancy at zero. By the manuscript's definitions \(C_n=\sup_P\sqrt n\Delta_n(P)/\rho(P)\) and \(C^*=\sup_n C_n\), it follows that

\[
 C^*\ge L(p):=
 \frac{\varphi(0)(3+q-p)}{6(p^2+q^2)}.
\]

Put \(v=q-p\in(0,1)\). Then

\[
 L(p)=\frac{\varphi(0)(3+v)}{3(1+v^2)},\qquad
 \frac{d}{dv}\frac{3+v}{1+v^2}
 =\frac{1-6v-v^2}{(1+v^2)^2}.
\]

The maximizer is \(v_* =\sqrt{10}-3\), corresponding to \(p_*=(4-\sqrt{10})/2\). Since rational \(p\)'s can approach this interior value and \(L\) is continuous,

\[
 C^*\ge \sup_{p\in\mathbb Q\cap(0,1/2)}L(p)
 =\frac{\varphi(0)}{6v_*}
 =\frac{3+\sqrt{10}}{6\sqrt{2\pi}}=C_E.
\]

For the middle equality use \(v_*^2+6v_*=1\), hence \(1+v_*^2=2v_*(v_*+3)\). The limit in \(n\) was taken separately for each fixed rational \(p\), followed by continuity in \(p\). There is no interchange of limits, triangular-array assumption, or irrational lattice-phase assertion.

This proves only the needed supremum lower bound. It does **not** assert \(C_n\ge C_E\) at a fixed index, attainment of \(C_E\) at a finite index, or any of the upper-bound certificate obligations. A separate internal AI reviewer checked the two-point moments, atom/midpoint identification and optimization algebra conditional on the stated lattice theorem; that reviewer did not review Esseen's proof.

## Atom convention and the still-open one-summand input

For any probability law and continuous comparison function, the supremum of the absolute discrepancy is the same whether one uses the closed CDF or its midpoint-at-jumps version. At an atom the midpoint discrepancy is an average of the two endpoint discrepancies; conversely each endpoint discrepancy is approached by values at nearby continuity points. This elementary observation can resolve that convention once a theorem is actually read. It does not establish an unread theorem's hypotheses or constant.

The original Russian Bentkus--Kirsa article has been identified as *Otsenki blizosti funktsii raspredeleniya k normal'nomu zakonu*, Lietuvos matematikos rinkinys **29** (1989), no. 4, 657--673; the English translation is *Estimates of the proximity of a distribution to the normal law*, Lithuanian Mathematical Journal **29** (1989), 321--332, DOI [10.1007/BF00971947](https://doi.org/10.1007/BF00971947). Its full proof remains unread here. In particular this audit does not certify an unrestricted all-law \(C_1\le0.3704\) from a two-point calculation alone.

The bounded additional retrieval attempts went beyond the previously unsuccessful publisher preview:

| Official or institutional route examined | Observed result | Consequence |
| --- | --- | --- |
| [Vilnius University LMJ archive](https://www.zurnalai.vu.lt/LMJ/issue/archive) and its `journals.vu.lt` counterpart | The exposed archive starts with volume 12 (1972) and earlier issues; no 1989 issue was located in the inspected archive. | Not evidence that no lawful copy exists elsewhere. No 1989 proof read. |
| [Bentkus's institutional biography](https://www.mii.lt/apie-instituta/istorija/izymus-darbuotojai/vidmantas-kastytis-bentkus), with targeted author/institution searches | The indexed publication route concerns later work; no target 1989 full text was located. | Author affiliation/publication metadata only. |
| Exact English/Russian title, author and original page-range searches, including institutional archive queries | Bibliographic references and later quotations were returned, without a located complete original target text. | These quotations were not substituted for the original proof. |
| Esseen 1956 original target, DOI [10.1080/03461238.1956.10414946](https://doi.org/10.1080/03461238.1956.10414946), plus institutional searches | No full original 1956 text was located in this bounded search. | The direct derivation above instead imports the explicitly located 1945 theorem. |

No paywall, authorization or access control was bypassed; no paid access was purchased. The open 1945 PDF is kept privately as a source copy, not added to the published repository. The one-summand literature obligation remains distinct from the now-specified lower-bound route and from the entire certificate-conditional upper-bound proof.
