# LOCAL42 signed repair and common-background bound: scoped crosscheck

Date: 23 October 2026. This is a fallible internal source and hand-algebra
cross-read by the same AI system. It is not external independent mathematical
verification, formal verification or fresh arithmetic acceptance. No original
normalizer, probability kernel, constructor or acceptor was imported or executed.

The reviewed note is `code_local42_count_primitives_audit.md`, SHA-256
`06d4328db75a0901559f57917150cd89a83983b8ed491ff3f5d4185ba5ceea57`,
and its source map is `code_local42_count_primitives_source_map.json`, SHA-256
`fd2430c30500751bff5dd643911f0a306e8763d2ccd85a7a6c3dc04dbc2ec377`.
The scope below is sections 3 and 6 and their actual selected source paths.
It does not cross-review every argument in that note.

The reviewer read the actual supplied `closure31.zip` members and checked all
30 mapped member sizes and hashes. Each also matches its literal entry in the
actual 9,518-row `EVENTUAL_CUTOFF31_COMPOSED.json` source map, whose member hash
is `33c73b3bd4c8cb25cedb6c9c8ce3768608db18f1f65932a0fcd6bb468c2b51b9`.
The complete archive transport hash was not recomputed in this cross-read.

## Signed cubic repair

Actual selected sources include LEFT TINY's
`normalization_piecewise42_v2.py`, SHA-256
`acc4055234a2629298cb665b12474ba5a9f35ed979dd3d238fffe9afd4aa5708`,
and `accept_tiny42_actual.py`, SHA-256
`5ab060f4506fdb99b57e4948e4230626238c747b1a255fe2aeaa132cda70109b`.
The caller checks the distinct finite actual-source scope 42 through 48 and
carries the fixed upper score premise `.4226`. The normalizer checks that
literal input and the signed lower/upper multiplier gates. These are additional
input obligations, not a consequence of the lower score premise `.4` alone.

For `v=p(1-p)` and inward shifts totaling `d`, conditional centering and
`d<p<1/2` give

`E|B+U-p|^3 >= v(1-2v)+(3p-d)s`.

Indeed, the cubic contributions are at least `-q*a0*s0-p*a1*s1`, while
the two variance coefficients dominate `(3p-d)(q*s0+p*s1)`. Subtracting
the binomial third-moment normalization and using the upper Taylor bound for
`(1+s/v)^(3/2)` produces exactly

`s[6p-3p^2-3/2-d-3(1-2v)s/(8v)]`.

The lower bound on this bracket may be negative at the leftmost selected
probabilities. If `m_lower <= C/(v+s)^(3/2) <= m_upper`, with both bounds
positive, multiplication of that signed bracket is bounded below by
`min(m_lower*q_star,m_upper*q_star)`. This agrees with the actual code;
using only the lower multiplier when `q_star<0` would reverse the needed
inequality. The code retains the nonnegative repair clipping and its gate
before replacing division by n with division by 42. No sign defect was found.

## One background, an upper variance envelope, and the complete tail

The actual selected LOW sources are the distinct left and central
`central42_kernel.py` files, SHA-256 respectively
`d025529aa2690c3cfc0f1c34a6af385d6fa69db8e069543057f29475cbb133c3`
and `9dc0754fe2dd4f2f7057247d3d62f3b71472c65a49d46f67d35fb0d66e3f8673`.
Their signed distances and common-background implementation were read directly.

Deleting the marked pair leaves the two marginals represented using one
centered background Z. The forward event lies in `Z<=-alpha`, the backward
event in `Z>beta`, with the note's positive alpha and beta. Dropping the
nonnegative eta in the latter distance weakens the estimate safely. The two
events are disjoint. For a center inside `(-alpha,beta)`, the quadratic Markov
estimate bounds their sum using `Var(Z)+center^2` and the smaller squared
distance to the two endpoints. The source's clipped center is inside this
interval; its validity does not require proving it optimal.

Set `T(lambda)=ownhi*lambda` and `T_L=ownhi*lambda_low>0`. The needed facts
are `Var(Z)<=T(lambda)` and `T(lambda)>=T_L`. They imply

`Var(Z)+center^2 <= T(lambda)*(1+center^2/T_L)`.

Thus the normalization does not require a positive lower bound on the actual
variance. The same distinction licenses the separate Cantelli denominator
`b^2+T_L` and the positive-noise endpoint Poisson bound divided by `T_L`.

For the remaining marks, `d0<=A` permits the weaker two distances
`c*i-A-u` and `c*i-A+u`. The convex midpoint integral from 2.5 to infinity
gives the two cubic denominators used by the source. They correctly use
`outerh` and `-outerl`; using the same signed endpoint twice would not be
valid. Their positive-denominator gates remain required.

The first-moment cap gate uses a comparison with an upper variance envelope;
it does not assert an actual variance lower bound. The pathwise integer-mark
argument also requires `0<eta<=1`. Here `eta=z*lambda`, the selected mark has
`z<=.849`, and the selected source tables have `Lambda<1`, as recorded in the
author's source review. These selected-input licenses cannot be generalized to
arbitrary helper arguments. The physical same-law support/profile facts,
`d0<=A`, the parent resource inequalities and all positive replay gates remain
separate premises.

No invalid implication was identified in this limited signed repair and
common-background/tail read. No upstream premise, scalar certificate, LOCAL42
theorem or all-index conclusion is acquired by this crosscheck.
