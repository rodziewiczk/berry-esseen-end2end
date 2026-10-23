# Primary literature inputs: statement and normalization checks

Review date: 23 October 2026. This note distinguishes a located theorem statement from a review of its proof. It does not certify every literature node in the proof graph.

## Structural estimate used by n2 and n3

The exact constants used in the manuscript are present in Shevtsova's own monograph, Theorem 2.7, equation (2.13), printed page 55 (PDF page 54): for the identically distributed case,

\[
\Delta_n\le\frac1{\sqrt n}\min\{0.469\rho,\;0.3322(\rho+0.429),\;0.3031(\rho+0.646)\}.
\]

Here the standardized third absolute moment is \(\rho=E|X|^3/(EX^2)^{3/2}\) for centered summands. Thus unit variance gives the manuscript's input \(\sqrt n\Delta_n/\rho\le(1661/5000)(1+(429/1000)/\rho)\). This checks the exact statement and normalization of this selected input; it does not audit the monograph's numerical proof. [Author's primary source, arXiv:1912.06482v3](https://arxiv.org/pdf/1912.06482v3#page=54).

The manuscript's original 2013 Math-Net citation was not accessible through the retrieval service during this review. The author's later explicit theorem supplies a primary-source statement of the same selected bound. [Original bibliographic entry](https://www.mathnet.ru/eng/ia252).

## Prawitz kernel

Shevtsova's 2012 paper, Lemma 4.1, printed page 263 (PDF page 23), gives the four-term smoothing estimate and the kernel

\[
K(t)=\tfrac12(1-|t|)+\tfrac i2\bigl((1-|t|)\cot(\pi t)+\operatorname{sign}(t)/\pi\bigr).
\]

For \(0<t<1\), this is exactly the manuscript's displayed kernel, including the sign of its singular imaginary term. The lemma includes the Gaussian comparison and infinite-frequency remainder. [Primary paper](https://ami.uni-eszterhazy.hu/uploads/papers/finalpdf/AMI_39_from241to307.pdf#page=23).

This statement does **not by itself** discharge the manuscript's stronger pointwise closed-half-line majorant, its atom convention or its compensated-expectation identity. The original Prawitz 1972 article's full text was not available to this review; its bibliographic record and abstract were located. [Original article](https://doi.org/10.1080/03461238.1972.10404645).

A subsequent [self-contained derivation](prawitz_majorant_review.md) supplies the exact selected pointwise statement directly. It proves the Beurling sign error bound, derives the manuscript's Fourier kernel by an explicitly dominated Abel limit, checks the included atom at zero, and justifies the compensated expectation identity. The [separate analytic crosscheck](prawitz_majorant_crosscheck.md) found no blocking sign, scaling, endpoint or convergence gap. This avoids relying on an unread original statement for that isolated lemma. It does not audit every later use of the kernel, derivative estimate or numerical implementation.

## Binomial input

Schulz's dissertation, Theorem 1 on printed page 1 (PDF page 11), treats every \(n\in\mathbb N\) and \(0<p<1\), with \(q=1-p\), and gives a strict bound

\[
\sup_x|F_{n,p}(x)-\Phi((x-np)/\sqrt{npq})|
< C_E\frac{p^2+q^2}{\sqrt{npq}}.
\]

The standardized Bernoulli law has \(\rho_B=(p^2+q^2)/\sqrt{pq}\), so this is exactly \(\sqrt n\Delta_n/\rho_B<C_E\). The statement uses a distribution function and a supremum of the absolute discrepancy, covering both orientations. Deterministic limits require their separate treatment; they are not additional cases of the positive-variance hypothesis. [Primary dissertation](https://d-nb.info/1197702695/34#page=11).

## Inputs still requiring direct verification

The original Bentkus–Kirsa one-summand theorem and Esseen's original lower-bound construction have not been checked from their full primary texts here. The exact He–Cheng estimate selected by the tail likewise remains open. The pointwise Prawitz statement now has the direct proof above; this is not a verification of Prawitz's whole original paper. No all-index theorem is imported from a title, abstract, historical PASS, or secondary summary.
