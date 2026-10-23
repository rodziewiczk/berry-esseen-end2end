# Explicit analytic repairs identified by the logic audit

Source: `berry_esseen_manuscript.tex`, SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
The supplied source is preserved unchanged. The amendments below are proposed
for the revised paper; an audit note does not edit or reissue that paper.

## R1: nonnegative own-mass lower bound

Location: `countcore:scoretheorem`, lines4653--4687.

The theorem calls `b_k^-` a lower bound for the own binomial mass. Its proof uses

\[
 b_k\Pr(W_k>u)\ge b_k^-\Pr(W_k>u)\ge b_k^-L_k(u,\mu).
\]

The second inequality requires `b_k^- >= 0`, especially because the theorem
explicitly allows its outgoing probability lower bound `L_k` to be negative.
A generic lower bound for a probability need not be nonnegative. For example,
`b_k^-=-1`, `Pr(W_k>u)=1/2`, and `L_k=-1` satisfy the lower-bound descriptions,
but the second asserted inequality would read `-1/2 >= 1`.

Amend the hypothesis to require, throughout the whole parameter box,

\[
 0\le b_k^-\le b_k(p).
\]

With that explicit premise the displayed multiplication chain is valid. An
implementation may replace any valid lower mass bound by its maximum with zero;
the new bound remains a valid lower bound. This note does not authorize changing
any frozen source, candidate or acceptance record.

Classification: a repairable omitted explicit hypothesis in the theorem
statement. It is not by itself a failed selected leaf or a counterexample to the
sharp-constant conjecture. The source-specific nonnegativity gate must still be
checked wherever this rule is instantiated. The companion resource/count audit
records the implementation readback separately.

## R2: enumerate the global integer-range premises

Location: `verify:thm:global`, item(d), lines9141--9143.

Replace the compressed description of the "remaining indices" by explicit
premises for the sharp finite base31--34, the supported finite bridge35--48,
and the uniform first-failure proof from49. The detailed refinement section
already names these obligations. The final theorem should name them as well,
so that a tail49 certificate cannot be read as a proof of the missing31--48
range. The positive-budget27--30 route may be retained as an alternative
predecessor acquisition; an already proved sharp result through30 is stronger.

Classification: an explicit dependency/completeness clarification, not a newly
found counterexample or a claim that the finite bridge has been verified.

## R3: retain the confinement multiplier sign gate

Location: confinement hypotheses/slopes, lines7651--7692 and7881--7897.
The substitutions using3(.4)b_- and3C_0 b_+ require nonnegative beta
endpoints, or sign-aware coefficient endpoints. State the sign condition
explicitly in the applied interface. A positive closed-CDF orientation alone
does not supply it.

The inspected frozen confinement kernel has an explicit `beta_domain` gate and
defines its improved lower beta bound by a maximum. All83 selected field rows
inspected in the tail audit have positive beta_lo. The actual inspected route
therefore supplies the premise; no failed selected certificate is demonstrated.
The source-to-lemma map must retain that gate. See exact source pins and line
references in [the global/tail audit](logic_global_tail_audit.md).

## R4: state the general signed LOW rectangle actually enabled

The selected B3/B4 resource entry points install
`general_paired_exact.py`, SHA256
`e383a78467c380ae55ef9ef32f296cb5813f837c8bcaf3003a113a04fb29fb96`.
The manuscript's displayed paired coefficient specialization at1927--1957
uses M<3,g^2<2,R>2g. The enabled source instead uses a piecewise Pearson
rectangle valid for R>=1, including a switch at |gamma|=R/2. A revised paper
must explicitly state and prove that broader rectangle before selecting it.

The [signed LOW implementation audit](code_signed_low_audit.md) supplies
the conditional coefficient formulas, their exact cubic Bernstein
enclosures, signed c endpoints, corner norm and Mills parity readback.
It found no invalid inequality in those operations. The same-law input
acquisition and resource context remain separate. Classification: a precise
paper-to-enabled-code documentation obligation with a reviewed derivation,
not a license to discard the old radius gate from its old formula.

## R5: describe the actual HIGH comparator upper bound

The HIGH_WINDOW50 discussion at the end of its proof says the selected
implementation uses min(1.85,sqrt(M-1)) in the comparator. The inspected
selected `high_window_common.py` instead uses a directed upper sqrt(M-1)
without that optional minimum. This is a weaker valid bound. Its complete
six-piece computation must still pass the final target; no result can be
inferred from the stronger unused description. Match the revised source
description to the actual expression. See the [HIGH implementation
audit](code_fourier_primitive_audit.md). No frozen source was changed.

## R6: include the actual n>=2 direct-Gaussian support lemma

The active B3/B4 n25 INITIAL/resource sources call
`direct_gaussian_support.target`, using the exact scale from
`small_index_support.constants`. They do not call the manuscript's
displayed n>=36 polynomial support recipe at714–788.

The revised paper should include the actual Gaussian support function,
its derivative-in-radius bound from Taylor plus heat interpolation, the
strict complete-ray gates, the closed threshold-cell curvature bound and
both infinite threshold tails. The [general-cell/direct-support review](code_general_cell_atlas_audit.md)
section7 records an internal derivation valid for n>=2 and the actual
directed roots/exponential/CDF interfaces. Same-law contact, beta/rho
bounds and predecessor allowance must remain explicit hypotheses.

Classification: a substantive paper-to-selected-source explanation is
required. No false selected inequality or completed proof acceptance is
claimed. The reviewed source and original manuscript remain unchanged.

## R7: preserve the already named scaled-phase bridge correction

The selected bridge36–39 frozen contract prose omitted the multiplier
`15000/(997*n)` in its phase bound on D. The original
`check_cutoff35.py` explicitly requires `BRIDGE_SCALED_PHASE_SCOPE_V2`:

`D <= (15000/(997*n))*max_j(A_j+Fsign_j*abs(H)-Qbudget_j*H^2)`.

The inspected quartic36 leaf already uses this factor. The source join
does not assert the literal unscaled wording. The revised exposition and
any fresh semantic join must consume this corrected same-witness premise.
See [the finite-index implementation review](code_finite_index_bridge_audit.md).

Classification: preserve an existing explicit scope repair. This is not
a newly observed arithmetic failure or a proof that every distinct older
bridge engine has been checked.
