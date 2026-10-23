# Finite-index, uniform-tail and global logical audit

Date: 23 October 2026. This is an independent mathematical read of the actual
supplied `berry_esseen_manuscript.tex`, SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
Line references below refer to those9252 source lines. The principal scope is
lines6624–9178, with the effective-tail statement282–363, attainment/contact
368–457, closed-CDF orientation4754–4761 and increasing induction4766–4813.
The source was read without modification. No numerical kernel, certificate
producer, leaf evaluator or fresh mathematical replay was executed.

**Finding:** the inspected scalar composition has an acyclic conditional
proof mechanism. In particular, the least-failure tail does not assume
monotonicity of `C_n`, an earlier cutoff, or its own conclusion. The detailed
local argument explicitly handles atoms and noise tending to zero. No
confirmed mathematical contradiction or missing implication was found in
this scoped read. This does **not** establish all shared analytic rules or
the truth/completeness of their finite witnesses. Those are separate
obligations, not silently accepted hypotheses.

## Definitions and the contrary witness

The manuscript defines `C_n(P)` as the absolute Kolmogorov error multiplied by
`sqrt(n)/rho(P)`, and `C_n` as its unrestricted supremum over standardized
laws with finite third absolute moment (lines282–290). The global target is
`C* = sup_n C_n = C_E`. Distinct indices may have different maximizing laws;
the tail induction uses only the scalar suprema (7458–7461).

The fixed-index attainment argument at368–399 applies also at equality
`C_n=C_E`. A maximizing sequence with score bounded away from zero has a
bounded third moment. This gives uniform integrability of the first two
moments, but does not initially give third-moment uniform integrability.
Closed-set Portmanteau at the limiting threshold gives a limiting positive
closed discrepancy at least `C_n b/sqrt(n)`, where `rho_j -> b` and
`rho(P)<=b`. Extremality then forces equality and `rho(P)=b`. This is a valid
way to obtain third-moment convergence as a conclusion. Compact support
comes later from the contact inequality; it is not assumed for the initial
maximizing sequence.

A negative closed discrepancy reflects into a positive **strict** discrepancy.
Approaching that threshold from below gives the same supremum with positive
closed discrepancies. The atom-preserving identity is written at4754–4758:

`Phi(x)-P(S_n<x) = P(-S_n<=-x)-Phi(-x)`.

Reflection changes the whole marginal and its signed moments. Handling both
signs of the threshold with the same marginal is not that reflection
(4760–4761). No step of the inspected global induction identifies `p` with
`1-p` merely to halve the witness domain.

The raw-contamination contact calculation at429–456 keeps the raw threshold
fixed before standardization; its raw closed CDF is a polynomial in the
contamination parameter. The finite second moment justifies differentiation
of the centered third absolute moment. The resulting influence is
nonpositive everywhere and has zero integral. Its upper semicontinuity
extends equality from almost every point to the full closed support. This
licenses later support-point arguments even at atoms of very small mass.

## Complete integer coverage

The following table gives the mathematical coverage required for a global
proof. It is not an execution or notebook census.

| Integers | Required implication | Actual proof boundary |
| --- | --- | --- |
|1| Published one-summand bound, cited at9149–9150. | Primary theorem proof/normalization remains a literature obligation. |
|2,3| Standalone unrestricted witness reductions and their complete finite inequalities. | Separate [small-index analytic review](small_indices_analytic_review.md); observed finite arithmetic alone is not the all-law conclusion. |
|4| The all-law `C_3<=59 sqrt(3)/250` input, then unrestricted localization/physical bridge and full ROOT4 inequality. | The explicit predecessor appears at5565–5568 and5595–5602; arbitrary laws are retained. See [analytic audit](analytic_audit.md). |
|5| Full signed moment cover, gap-free and gapped branches, with the same-law predecessor input. | `C_4<=C_E` permits zero predecessor allowance; independent own-score/resource premises remain. |
|6–30| One complete literal-index certificate per integer, increasing from sharp `C_5`. | Lines6632–6702. A success at one index, or n25 alone, cannot represent the other24 indices. |
|31| Complete eight-rho-band, all100-panel sharp cover and its own support/resources/counts. | Lines6792–6833; its predecessor can come from sharp30 or from the separate positive-budget ladder. |
|32–34| Three actual-index bridges in order31,32,33,34. | Lines7342–7374. Actual binomial counts, support and score caps are retained; these are not renamed31 proofs. |
|35–38| The specified finite exclusions with sharp predecessor and their own-score caps. | Lines7382–7387 and7431–7434. |
|39| Positive39 barrier followed by the sharp39 exclusion. | Lines7388–7392 and7436–7442. The positive barrier supplies the narrower own-score cap needed by the listed sharp contract. |
|40–41| Their actual-index contracts with two controlled deleted predecessors. | Lines7393–7395 and7442–7444. |
|42–48| The stated finite-band contracts, preserving weighted resources, signed phase and closed noise faces. | Lines7396–7413 and7445–7448. |
|49 onward| Independent finite-ceiling base at49 plus the uniform local exclusion and a least later failure. | Lines7458–7644; detailed local/confinement rules7647–8885. |

All finite score exclusions must include equality in the contrary branch
`C_n>=C_E` and end strictly below a rational lower enclosure of `C_E`
(6677–6681). A non-strict upper bound equal to `C_E` does not prove a strict
conclusion. Failed guards, missing count roots, unfinished trees and omitted
threshold tails close no domain.

## Increasing induction and the auxiliary24 route

For the same marginal, `R_(n-1)(P)<=C_(n-1)<=C_E<=C` implies
`q_n(P,C)=n(R_(n-1)(P)-C)_+=0` (4776–4788). Any stored nonnegative allowance
therefore remains valid. In the full increasing6–30 proof, sharp24 can
replace a coarse predecessor-only acquisition used to justify the n25
allowance `5/16`. It does not remove a current-law own-score, support,
Fourier, resource or count obligation (4807–4813).

The current auxiliary route acquiring `C24<C_E+1/80` is another acyclic way
to justify the same n25 allowance: `25/80=5/16`. It enables conditional n25
work before the complete sharp6–24 chain has been acquired. It is not a
logical prerequisite of the entire global proof if sharp24 is supplied by
that increasing chain. Conversely, proving the auxiliary bound alone does
not establish sharp24 or fill the other literal indices. Old source objects
whose hashes encode that auxiliary route still need an explicit semantic
replacement/interface; changing the proof graph is not permission to copy a
historical PASS or bypass a numerical acquisition.

The positive ceilings at27–30 (6736–6790) also form an independent acyclic
ladder. The seed uses only the universal `.469` cap at26; successive bounds
supply their listed contact allowances. This ladder is sufficient for the
standalone31 theorem. Once the full increasing proof has sharp30, these
positive ceilings are unnecessary as separate predecessor bounds: sharp30
implies the weaker needed ceiling and permits the same nonnegative
allowance. Any independent own-score or actual-index calculation used by a
31 certificate must still be retained.

## The independent49 base and least failure

The support-free smoothing lemma at7464–7506 is derived for every actual
mean-zero, variance-one law with finite third absolute moment, before taking
suprema. Conditioning controls the `(n-1)`-sum, a globally bounded third
Gaussian derivative controls the third-order moment remainder, and a heat
equation/variance Taylor step supplies the second remainder. The factor
`rho>=1` is used only in its valid adverse direction. It is uniform in the
law and every real threshold, including closed events and their left
limits. It is not a monotonicity theorem for the optimal constants.

The index dependency order at7513–7621 is:

1. A40 and P41, together with independent contact support, prove
   `a_j<1.5/j` for40–45 from the universal cap at39.
2. A45 and P46 improve this to `a_j<.7/j` for45–50. Each first failure has
   a previously established predecessor; smoothing supplies the `.432`
   own-score cap. P41's stated finite upper endpoint49 and P46's98 are used
   only through45 and50, respectively, at this step.
3. A46 and its independent support row sharpen46 to `a_46<.54/46`.
   The support edge uses the already proved finite ceilings, not the output
   of A46 itself (8082–8094).
4. If `a_49>=0`, all premises of the local proposition except its contact
   allowance already hold at49. Hence its contrapositive gives
   `a_48>a_49+.19/49>0`. Apply the same reasoning at48 and47; the accumulated
   loss exceeds `.54/46`, contradicting step3. No sharp47/48 conclusion was
   assumed to prove49.
5. If a failure occurs after49, choose its least index `n`. Then
   `delta_n=0`. Smoothing gives `0<=n a_n<.29`, and thus the local excess and
   own-score caps. Both deleted predecessors are below `.4253`; when
   `n=50`, the second predecessor48 uses the independently proved finite
   ceiling. For `n>=51`, minimality supplies both. The uniform local
   proposition contradicts the failure (7623–7644).

The decrease used in the smoothing bound concerns elementary bounding
expressions such as `s_n=sqrt(n/(n-1))` and
`n(s_n-1)=s_n^2/(s_n+1)`. It does not assert that `C_n` decreases.

## Uniform local exclusion, atoms and the zero-noise face

The local proposition's exact premises (7538–7545) are

`n>=47`, `0<=a_n<=.7/n`, `delta_n<=.19`,
`C_n<.4247`, `C_(n-1),C_(n-2)<.4253`.

Its conditional finite work must acquire support and all83 probability
panels covering `[.304,.47]`, with the same law's moments, signed thresholds,
gap and conditional variance. The finite row fields are hypotheses of the
local theorem, not consequences of its conclusion. The apparent98 endpoint
is explained at7564–7571: the actual application has `K=0`, so its only score
floor use is independent of98. Weighted quantities `nD` and
`lambda=n E U^2` are retained. A complete verifier still has to establish
that these are the quantities its actual source enclosures export.

The following analytic steps were read in detail:

- The antichain concentration proof requires interval diameter **strictly**
  below the acquired gap; the text explicitly shows why a closed interval
  of equal width fails for a Bernoulli atom (7740–7771). Its cap controls
  both actual deleted indices `n-1,n-2` and is preserved by adding an
  independent conditional noise.
- Signed deletion combines the noise terms before bounding them, treats
  the exceptional event strictly, and retains the good-event equality
  endpoint (7807–7852). The confinement slope and simplex bounds consume
  one common nonnegative resource. A newly proved amplitude is used only
  as a later support update (7647–7650,7971–8063). The explicit sign guard
  discussed in R3 below must accompany the displayed general formulas.
- The exact local master identity uses the actual `v+s`, actual `n`, one
  threshold phase and the same conditional laws (8228–8269). The count
  decomposition has strict outgoing events and closed incoming events
  (8305–8308), which are complementary with atoms.
- The finite Stirling/derivative, variance, mass-ratio and cubic-repair
  bounds have explicit denominator/sign/index gates (8315–8421). The
  bound replacing a binomial mass by its lower estimate uses a negative
  coefficient first; the bound replacing `n` by its floor uses a
  nonnegative inverse-index coefficient first (8310–8312).
- TINY does not substitute a positive lower noise endpoint into a cell
  touching zero. The rescaled quartic and per-noise Poisson/Bennett bounds
  apply to every `0<lambda<=U`, including a deterministic conditional
  component (8534–8590).
- The whole-count route uses a monotone coupled integer cutoff, a signed
  curvature estimate, marked crossing, and a fractional-part gain
  (8592–8807). Its elementary Poisson comparison is proved at8465–8485;
  the harmonic gain includes zero variances and integer collisions at
  8716–8759. The finite scalar inequalities, denominators, convexity signs
  and both noise-cell endpoints remain certificate obligations.
- The selected LOW/MID/TINY cover explicitly retains both threshold signs,
  nearest-count ties, row-ceiling singletons, positive noise tending to
  zero and the finite coefficient/coverage checks (8809–8873).

At `lambda=0`, conditional centering and `0<p,q<1` force both noises to
vanish almost surely. The law is exactly Bernoulli. At an attained positive
closed maximum the threshold is an atom; the preceding-atom argument does
not lose its included mass. Schulz's all-probability theorem supplies a
strict bound for both this case and the signed Bernoulli score in the
positive-noise comparison (8875–8885). No division by zero or varying-law
limit is used. The primary statement/normalization check is recorded in
[literature_inputs.md](literature_inputs.md); its published proof is a
separate literature input.

**R3: make the signed-moment multiplier gate explicit.** The general
confinement statement gives only `beta_-<=beta<=beta_+` (7662–7668).
The lower-slope substitutions in7881 and7887 use `3(.4)b_-<=3 C beta`;
the upper substitution in7890 uses `3 C beta<=3 C_0 b_+`. These directions
need `b_->=0` and `b_+>=0` (or sign-aware endpoint multipliers). State that
gate explicitly in the parameterized lemma; it does not follow merely from
`p<1/2` for an arbitrary admitted parameter table.

The actual selected-source audit resolves this concern for the inspected
rows, without evaluating a bound algorithm. In the original tail49 source,
`baseline/certificates/work/below50_20260929/local/confinement47_kernel.py`
(SHA-256 `59a601bf5615922e7ab1c71b22bdc25903e2f37c803eeb24d91919f370b6bfe7`)
line23 emits the `beta_domain` gate on `cfg['beta_lo']`; line50 sets
`blo=max(cfg['beta_lo'],...)`, and line51 checks `bhi-blo`. Static JSON
inspection found positive fraction/decimal strings for all45 `beta_lo`
entries in `entry/sperner_feedback47_table.json` (SHA-256
`4a1ea8a439e85e9f481bb6c6eb7a197ec4d35e53ceecf0ec92c3d4c96b9f618a`)
and all38 entries in `entry/left270_input47_table.json` (SHA-256
`4b7bb259e469ee57ca6a61d89fd0b3385443508129138899fe597fd82dc9521a`).
All45 original central entries in `local/conditional_input47.json` are also
positive (SHA-256
`b9d2aa15ad96181f5a8eb846e76ae296d2c2c8ed1a5975c6f389c2f7d14ff2b7`).
The source files were read as bytes/text from the inspected exported
tail49 capsule; no source was imported and no gate was numerically replayed.
This is **REQUIRES_EXPLICIT_SIGN_GATE_IN_GENERAL_STATEMENT**, with the
selected static fields satisfying the needed sign, not a confirmed failing
selected certificate.

## Actual-index bridges and the optional shorter global composition

The31–34 transfer preserves `mD_m<=31 d_stored` and the raw bound, not just
`D_m<=d_stored` (7348–7369). Actual-index support, score caps, resource
callbacks, binomial probabilities, threshold normalization and count
coverage are acquired separately. Finite band endpoints and a floor may
bound the corresponding formulas only under their stated gates. Signed
Gaussian/cubic repair retains adverse signs rather than multiplying a
negative coefficient by an index floor (7212–7340).

There are two possible acyclic global compositions of the supplied
implications:

- The manuscript's explicit independent49 route uses its own positive
  finite-ceiling base and uniform local exclusion; combine it with the
  separate sharp31–48 continuation.
- After a fully proved sharp31–46 continuation, choose a least failure at
  any `n>=47`. The smoothing estimate already derived for `n>=35`
  (7415–7429) gives `0<=n a_n<.30<.7`. It also gives the local own-score
  cap, while minimality supplies zero allowance and both sharp deleted
  predecessors, including45/46 when `n=47`. The uniform local proposition
  then excludes every such failure. This composition can cover47 onward
  without the separate positive49-base calculations.

The following makes the second alternative precise.

**Proposition (conditional first-failure composition from46).** Suppose the
support-free smoothing lemma holds, `C_E<.40974`, `C_j<=C_E` for every
`1<=j<=46`, and the complete uniform local exclusion at7538–7545 has been
established for every actual integer `n>=47`. Then `C_n<C_E` for every
`n>=47`.

**Proof.** If the conclusion fails, choose the least integer `n>=47` with
`C_n>=C_E`. Both `C_(n-1)` and `C_(n-2)` are at most `C_E`; for indices above46
minimality supplies strict bounds. Thus `delta_n=0`, and both deleted
predecessors are strictly below `.4253`. Smoothing gives

\[
 n(C_n-C_E)\le C_E n(s_n-1)+s_n^3
       \left(\frac1{15}+\frac{.08}{\sqrt{n-1}}\right),
 \qquad s_n=\sqrt{n/(n-1)}.
\]

For `n>=47`, squaring positive quantities gives `s_n<1.011`,
`n(s_n-1)<.51` and `sqrt(n-1)>6`. Therefore

\[
 0\le n(C_n-C_E)
 <.40974(.51)+(1.011)^3(1/15+.08/6)<.30<.7.
\]

Also `C_n<.40974+.30/47<.4247`. All hypotheses of the uniform local
exclusion hold at this same actual index, including equality in the
contrary branch, which is a contradiction. This also treats `n=47`: its
two deleted predecessors are46 and45, supplied by the finite hypothesis.
No supremum over a fixed law is exchanged with an infinite-index limit.

This is a valid new conditional composition of the stated lemmas. It is
not a claim that the sharp31–46 finite certificates have been verified, or
permission to remove branches from an existing replay. The current full
tail replay is a sufficient independent route and its fixed14/41 arithmetic
scope remains unchanged. In particular, the actual source kernels must
still be shown to implement the advertised uniform local proposition.
Shared formulas do not identify different literal-index/K/domain
certificates.

## The AND spine and the alternative routes

Every arrow below needs all of its named premises. The choices in the two
rows marked **OR** are alternatives, not additional mandatory conjunctions.

| Logical part | Required AND inputs or explicit OR choice |
| --- | --- |
| Small-index foundation | External1 **AND** separate all-law2 **AND**3 **AND**4 **AND** the complete5 cover. The all-law4 result is the predecessor input for5; sharp2 is not needed to prove3 merely because its index is smaller. |
| Finite induction spine | Sharp5 **AND** each literal complete6,7,...,30 certificate, in increasing order. All selected support/Fourier/resource/count premises at each step remain AND inputs. |
| Permissible n25 predecessor input | Sharp24 **OR** the weaker acquired auxiliary bound `C24<C_E+1/80`, either implying the stored allowance `5/16`. The unrestricted global theorem still needs sharp24 somewhere on its finite induction spine. |
|31 entry | Sharp30 **OR** the independent positive-budget27–30 ladder, together with the full literal31 cover and actual own-score/support premises. |
|32–46| Sharp31 **AND** actual32,33,34 **AND** the finite35–38, positive-and-sharp39, actual40/41 and42–46 contracts. |
| Infinite completion, routeA **OR** routeB | **A:** complete sharp47/48 finite implications **AND** the independent49 finite base **AND** uniform local exclusion/smoothing. **B:** sharp through46 **AND** uniform local exclusion/smoothing, by the proposition above. |
| Final equality | The chosen all-index upper-bound route **AND** Esseen's lower bound. |

The auxiliary21–24 notebooks remain useful for the currently parallel
conditional n25 acquisition. Their logical optionality on a future complete
sharp induction does not invalidate those jobs, require a restart, or
transform their historical input receipt into a fresh sharp24 result.

## Global theorem and remaining mathematical boundary

The global conclusion at9129–9165 is expressly certificate-conditional.
Finite DAG soundness at9076–9091 is an induction over rules whose analytic
hypotheses must actually have been established for the same law. It does not
prove termination of search, existence of a successful cover, or the
implementation-to-lemma correspondence. The source explicitly says the full
computational data are not included and independent end-to-end verification
has not been completed (4817–4820,8959–8965,9167–9178).

One editorial precision is needed in the high-level global theorem: item(d)
at9141–9142 should explicitly list sharp31–34, the chosen sharp35–48 finite
continuation and the49+ tail, or state the shorter alternative above with
its exact premises. The phrase “remaining indices ... effective tail
argument” is less explicit than the actual coverage in6729–6733 and
7342–7448. Reading item(d) as *only* the theorem `n>=49` would leave31–48
uncovered. The detailed manuscript has a separate conditional route for
them, so this is a hypothesis/statement clarification, not a demonstrated
counterexample to the expanded composition.

The remaining boundaries must be kept separate:

| Boundary | Current conclusion of this audit |
| --- | --- |
| Scalar induction, range transitions and least-failure mechanism | No blocking implication or circularity found in the inspected arguments under their explicit hypotheses. |
| Selected local comparison/confinement arguments | Detailed read found no blocking sign, atom, index-floor or zero-noise gap; all stated numerical gates remain conditional. |
| Complete shared support/Fourier/resource/kernel mathematics | Not fully independently verified by this scoped read. Earlier3000+ lines and each actual implementation still require their own rule-by-rule audit. |
| Every finite certificate, source closure, control census and source-to-lemma map | Not established by this mathematical read or by historical PASS metadata. |
| Primary literature | Shevtsova and Schulz selected statements have separate normalization notes. The exact He–Cheng Appendix A.1(70) input is now checked against its [primary source](https://arxiv.org/html/2609.06358v1) and given a direct short proof in [logic_gaussian_input_audit.md](logic_gaussian_input_audit.md); this does not import an eventual-cutoff theorem. The one-summand theorem and Esseen lower bound retain their separate review boundaries. |
| Unconditional all-index theorem | Not accepted or promoted. |

Thus the scoped result is **LIMITED_VALIDATED_LOGICAL_CHAIN**, with no
**CONFIRMED_GAP** established here. An open numerical certificate is a
missing premise of the conditional theorem. An unreviewed analytic rule is
an independent verification obligation. Neither should be relabeled as an
already proved theorem, and neither is by itself a mathematical refutation.
