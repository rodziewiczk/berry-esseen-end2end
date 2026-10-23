# Complete selected V12 count engine: conditional soundness readback

**Review status:** AI-generated internal source review. Cross-reads by
other model agents are internal checks by the same AI system. External
independent mathematical review and machine-checked formal verification
are not established here. This review may contain mistakes or omissions.
See the [evidence limits](CODE_INTERFACE_AUDIT.md#evidence-limits).

Date: 23 October 2026. This review follows the complete enabled native
V12 count path, rather than only selected helper components. It uses
source reading, exact source hashes, AST comparison and algebraic derivation
within the same AI-assisted workflow. The evidence limits in
[the audit index](CODE_INTERFACE_AUDIT.md#evidence-limits) apply. No archived
mathematical module, producer, evaluator, acceptor
or search was imported or run. No numerical result is acquired here.

## Result and precise scope

No concrete unsound exclusion, score substitution or counterexample was
found in the complete V12 engine path reviewed below. Every named EMPTY
return and every score strategy in the selected engine has a conditional
mathematical justification, with the domain and rounding qualifications
recorded here. The result is conditional on the actual same-law meaning
of the input contract and on the component inequalities identified below.
It does not establish those resource acquisitions, a successful fresh
replay, a complete regional composition or the manuscript's final theorem.

One important output distinction is essential: after Gaussian slope
cancellation, the first return value of an incoming evaluator need not
be a standalone upper bound for the incoming probability. It is valid
in the **combined difference with the Gaussian at the left endpoint**.
The inspected callers preserve that pairing. Reusing that scalar as a
free-standing probability upper bound would not follow from this audit.

The V14 contact/rho preprocessing is a separate layer, reviewed in
`code_v14_contact_audit.md`; it is not silently included by calling its
V12 fallback. The present file does not change any source or proof-graph
status.

## Exact inputs and actual call route

The supplied v4 manuscript has SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
The mathematical count interface is at lines 4050–4759.

The inspected current copies are in the sealed portable p31 source
preparation, whose V12 mathematical files are also used by p32, B3/p33
and the four B4/p29 quarters. The following SHA identities were read:

| File | SHA-256 |
|---|---|
| `exact35_core.py` | `a618867ae34841b2e3e1745e35142694142e08ca2d790b762870f50651e16d71` |
| `generalized_scope.py` | `0ca76c72ccf7f9243e1d9b7d68f814b84e160f7da11945a7842dff5b2abebc00` |
| `rho_signed_moment_tightener.py` | `f1650ff9ea811d66acf5f3529e0c0c462cc2d4747fbb42d147406714d0fc2be0` |
| `optimized_arithmetic.py` | `ab9bc728fbb7901f94323a384caf367eee2b2064e919dac27a01cabae743b765` |
| `exact_count_core_v5.py` | `0ffba7a5e1a91fc3c3c770f9d3bcb073a529fade3d622bc5615567153a4255a0` |
| `finite_gaussian.py` | `4f5b1a829df4c3c8c0e5467adb79f112984ee8eab8ba5f25b20fd7173b78a4a0` |
| `bernstein_fast.py` | `4983c9af05673775c3fd5b521e898a9c7f7fe5c9523a5009646872bf75adc607` |
| `interval_scalar_fast.py` | `3eaa0d78eec8b8d5c2044eb020a406ec352ac5a99b30f9d2773694a4f9601512` |

The actual native route is:

1. The pinned protocol reconstructs an original `(p,lambda,alpha,u,a0)`
   box and calls `rho_signed_moment_tightener.cell35`.
2. That wrapper imports `optimized_arithmetic.cell35`; this is the engine
   function imported from `exact35_core`, with its module globals retaining
   the installed exact Bernstein and scalar-interval optimizations.
3. `optimized_arithmetic.py` 7–10 installs those two optimizations,
   replaces the engine's Bernstein helper and sets its `joint` module to
   `joint_cubic_normalized_fast`.
4. The engine's `cell35` tries V11, V10 and finite-alpha refinements in its
   declared order. All retries start with the same wrapper-contracted
   necessary box and unchanged original configuration.

This is the native acceptance route. Search-only construction helpers and
historical accepted receipts are not part of this mathematical call route.
The complete original-root link is reviewed in `code_count_kernel_audit.md`.

## What the configuration must actually mean

Fix one actual oriented standardized iid marginal and one threshold.
Write `v=p(1-p)`, `s=lambda/n`, and
`sqrt(v+s)*X=I-p+U`, where `I=1_{X>0}` and
`E(U|I)=0`. A possible zero atom belongs to the nonpositive class.
The same law supplies all of the following hypotheses:

* acquired rho, signed beta, physical sign-mean and theta intervals;
* actual support `[-Rminus,Rplus]` and positive physical inner gap floors;
* centered conditional supports `U0 in [-O0,a0]`,
  `U1 in [-a1,O1]`, with `a0,a1>=0`;
* the original joint plane
  `(a0+a1)/d0 + lambda/Lambda <= 1`;
* `D>=binary_charge+gap_charge*(a0+a1)+noise_charge*lambda`;
* `D<=cfg.D`, the coherent signed quadratic upper envelope for that same
  physical D, and the actual raw threshold bounds `-Hminus<=H<=Hplus`.

The original box contains the actual five coordinates. The conditional
variances are `w0=s*(1-alpha)/(1-p)` and `w1=s*alpha/p`. At zero s both
conditional laws are zero and any allocation is harmless. At positive s,
the allocation belongs to `[0,1]`. All moments and both cubic coordinates
come from these same conditional laws.

`generalized_scope.validate_resources` checks the types and required
positive domains, including `d0<1/2`, positive joint/affine/phase prices,
and nearest-count coverage. It **does not prove the acquired inequalities**
from a law. The caller must supply their mathematical acquisition. The
native fixed-target loaders additionally bind n=25, K=0 and the literal
probability/rho domain. No claim for arbitrary unpinned dictionaries is
made here.

## Wrapper: every named exclusion

References in this table are to the 69-line theta-enabled
`rho_signed_moment_tightener.py` and its named helpers. Their exact helper
identities and derivations are in `code_count_kernel_audit.md`, section 1.

| EMPTY status | Return condition and justification |
|---|---|
| `EMPTY_ACQUIRED_THETA_VARIANCE` | 38–40: `lo` strictly exceeds `n*vmax*Theta/(1-Theta)` or the current hi. This is the exact theta identity, with the closed p=1/2 seam retained. |
| `EMPTY_SUPPORT_GAP_VARIANCE` | 41–43 or 66–68: the current lower lambda strictly exceeds the allocation/support cap derived from the original joint plane. The stored Lambda is unchanged. |
| `EMPTY_ACQUIRED_MEAN_VARIANCE` | 44–46: zero acquired upper sign-mean, or an empty necessary v/lambda interval from `lambda=n*(v^2/m^2-v)`. Equality survives. |
| `EMPTY_ACQUIRED_RHO_VARIANCE` | 47–49: a positive rho-floor numerator has nonpositive admissible coefficient, or its derived lower lambda strictly exceeds hi. The optional floor is omitted when its positive-numerator gate fails. |
| `EMPTY_ACQUIRED_BETA_VARIANCE` | 50–52: the strict signed-beta separation forces positive noise with an impossible coefficient or a floor above hi. Both low-beta and high-beta cases are handled. |
| `EMPTY_ACQUIRED_BETA` | 53–55: the necessary beta interval is strictly disjoint from the acquired interval. |
| `EMPTY_ACQUIRED_MEAN` | 53, 56–57: the physical mean interval `v/sqrt(v+s)` is strictly disjoint from the acquired interval. |
| `EMPTY_ACQUIRED_ALPHA` | 58–65: the solved necessary allocation interval has lower endpoint greater than upper endpoint. The solved division is attempted only if `lo>0`. |

The wrapper's beta formula uses interval arithmetic over the original
orientation and intersects only licensed corner refinements. Its sign-mean
lower and upper endpoints use monotonicity in v and s and directed
radicals. It forwards the **same configuration** to the base engine;
only necessary working coordinate intervals are contracted. In particular,
it does not replace the original joint-plane Lambda with an independent
lambda-domain cap.

## Engine: every named exclusion

All line references in this and subsequent engine sections are to the
596-line V12 `exact35_core.py` with SHA `a618867a...` above.

| EMPTY status | Source and conditional implication |
|---|---|
| `EMPTY_PHASE` | 426–428: the interval for `(k+u-np)/sqrt(v+s)` has empty intersection with the acquired raw H interval. |
| `EMPTY_NEGATIVE_BUDGET` | 429–430: the upper bound on the nonnegative physical D is negative. `quadratic_cap`, 24–32, maximizes each coherent concave signed corner on its clipped H interval, takes the corner maximum and intersects the scalar D cap. |
| `EMPTY_PHASE_RESOURCE` | 434–438: `Dcap-binary_charge-noise_charge*lo<0`, contradicting the simultaneous affine resource. |
| `EMPTY_SUPPORT_VARIANCE` | 443–446 or 488–490: the inward endpoint interval is empty or a variance lower bound exceeds `outward_cap*inward_cap`. The strict physical sign floors and both endpoints are retained. |
| `EMPTY_SHARP_BOX` | 447 or 472: a complete termwise lower enclosure of D is strictly above its acquired upper bound. A failed coefficient/domain gate returns `None` and cannot cause exclusion. |
| `EMPTY_SHARP_GAP` | 448–450: every full-domain derivative lower gate is positive and the resulting monotonic sharp-D lower bound strictly exceeds Dcap. Failure of the monotonicity gate does not imply emptiness. |
| `EMPTY_RHO_BRANCH` | 493–494 or 501: a valid rho lower bound is strictly above an acquired or independently valid rho upper bound. |
| `EMPTY_RHO_UPPER` | 495–500: a valid rho upper bound is strictly below the acquired lower bound. |
| `EMPTY_JOINT_CUBICS` | 502–503: the exact bounded closed moment polygon has no vertex. The rectangle/strip/halfplane construction retains every feasible pair and bounded nonempty degeneracies have vertices. |
| `EMPTY_VARIANCE_IDENTITY` | 505–507: the coupled formula for `V_k` and the sum `(n-k)w0+k*w1` have strictly disjoint intervals. |

No equality endpoint is an emptiness test in this list. A failed assertion,
zero divisor or rejected input is an execution failure; it is not returned
as one of these proved contradictions. The external replay requires a
completed valid result, so this distinction is material. This audit records
a source-level argument for conditional soundness of inspected completed
paths, without establishing totality or efficiency on
every relaxed infeasible box.

## Endpoint contraction and the physical D lower bounds

Lines 431–433 derive actual outward noise caps by subtracting the actual
conditional centers from the acquired signed support. Lines 441–443
retain the positive physical inner gap floors. Together with the joint
and affine resources, these yield the shared upper inward sum d.

`box_sharp_lower`, 70–81, uses manuscript 4286–4299. On an actual
`a0+a1<=d<1/2`, the function
`f(a0,a1)=a0+a1-a0^2-a1^2-a0*a1` increases in each coordinate.
Thus lower endpoint floors give a lower f. The linear variance prices
are lowered using upper inward endpoints and checked nonnegative before
lower variance substitution. The `w_i^2/a_i` terms use lower variances
and upper endpoints. The extra `3*pl>=u0` and `3*(1-pu)>=u1` gates make
the replacement of sqrt(10) by its lower enclosure safe in these prices.
A zero inward endpoint has zero actual conditional variance and is
handled before division.

When a sharp numerator lower bound is negative, clamping it to zero is
licensed by the independently nonnegative physical D. It does not require
the polynomial with a rounded lower sqrt(10) coefficient to be literally
a perfect square. Source comments alone would not supply that identity.

For the stronger monotonic inversion, differentiating the sharp D
numerator with respect to a0 gives

`6v*(1-2a0-a1)-q*(sigma+7)*w0-q*(sigma+1)*w0^2/a0^2`.

Since `w0/a0<=O0`, `a0+a1<=d`, and all variances are nonnegative,
`sharp_gates`, 34–37, is a lower bound for this derivative throughout the
consumed actual domain. The reflected derivative gives its second gate.
`effective`, 39–44, implements
`w^2/max(floor,w/O)=min(w^2/floor,O*w)`, with its zero-over-zero value
handled continuously. This expression increases in w.

In the finite searches at 454–484, an internal variable named `low` is
only a proposal cursor. A failed test does not export it as an actual
lower bound. Every change to the exported upper endpoint has its own
proof that the subcase `actual_endpoint>=mid` is impossible. The later
endpoint grid operation rounds **up** and intersects with prior valid
upper caps. No fixed-point or unproved bisection monotonicity is assumed.

The scalar rho bounds at 491–501 have the correct signed cubic directions:
the negative class contributes `-q*mu0`, the positive class `+p*mu1`.
Products with a negative cubic bound use the opposite probability endpoint.
The lower numerator divides by an upper positive cubic scale; a negative
lower numerator is harmless since rho is positive. The upper numerator
is clamped at zero before division by a positive lower scale. If its
upper value were negative, no actual positive absolute moment could be
present; the weaker zero clamp therefore cannot lose an actual witness.

## Own-count probability: strict events and all zero cases

The own-count routes at 95–138 and 511–515 all bound the same closed
own-count CDF, or equivalently its **strict** outgoing complement.

* For `uh<0`, Cantelli bounds `P(W_k<=u)` by the right-endpoint value
  with an upper V. Its complementary outgoing lower bound uses `>`.
  The exponential alternative applies to `-W_k` with upper conditional
  supports O0 and a1 and a common allocation.
* The quartic route uses the complete two-endpoint support bound for
  `E(U_i^4-4u U_i^3)`. The switches `(a0-O0)/4` and `(O1-a1)/4`
  have the correct direction. When the phase interval crosses a switch,
  both endpoint cases are retained and the final maximum/minimum is
  taken in the safe direction. The same applies at equality.
* For the additional class-one event, `b=uh+B+(k-1)*a1`.
  Any one class-one variable exceeding b forces that group's sum to
  exceed `uh+B`. The source treats `b<-a1` as certain, `b>=O1` as
  empty, and retains the strict event at both equality boundaries.
  The interior lower bound is
  `max(0,(w1_lower-a1*b)/((O1+a1)*(O1-b)))`.
  Independence gives `1-(1-r)^k`; k=0 skips this route.
* The other group is at least -B with lower probability
  `max(B^2/(V0_upper+B^2), B/(B+(n-k)*a0))` for B>0.
  The second term follows from its upper support and centering, using
  Markov on `(n-k)*a0-Y`. At B=0 the code uses one only if the variance
  upper bound is zero and otherwise zero. If k=n, the empty other group
  is deterministic and this convention is correct.

Zero lambda forces both actual conditional laws to zero. Allocation
endpoints force the corresponding conditional variance to zero. These
cases survive the wrapper's conditional division gate, moment identities,
quartics, binomial comparison laws and constant-one MGF factors. A zero
inward cap is coupled to zero conditional variance before division.
At u=0 the strict outgoing event excludes its atom; it is never replaced
by a closed outgoing event.

The source's own probability upper bound lies in `[0,1]`; the own binomial
mass lower bound is nonnegative. `masses()` in `exact_count_core_v5.py`
50–58 requires `0<pl<=pu<1` and computes exact positive endpoint values.
The interior maximum at j/n is included for incoming upper masses.
Thus a negative polynomial outgoing lower bound cannot reverse the mass
substitution used by manuscript 4681–4688.

For the base shape c=2, `exact_count_core_v5.py` 9–10 uses the exact
rational `K=9/(4*(4641/10000))`. It has `K>9/4`; the retained squared
comparison proves `K>9/4+3*sqrt(3)/2`, the global quartic maximum in
manuscript 4335. Thus its normalization is an upper bound in the required
direction. The selected native entry point requires unoptimized Python,
so this scalar check is not bypassed.

## Incoming lines and Gaussian cancellation: complete mapping

The four incoming evaluators are at 152–202, 204–257, 259–320 and
322–386. They differ only by the additional whole-phase stop-loss options.
For each incoming j, `d=j-k-u>=1/2` on the original phase domain.

Their enabled strategies are Cantelli; common-allocation Bennett;
independent sharp/cubic MGF bounds; common-allocation sharp-MGF tangent;
centered or shifted exponential excess; fixed cubic stop-loss; optimized
quadratic stop-loss with a matched chord; and the closed finite-alpha
cover. Each is applied to `-W_j`, hence bounds a **closed** incoming event.
The source identities and component derivations are pinned in
`code_count_kernel_audit.md`, sections 4–5.

For a frozen variance upper V, the maximum Cantelli phase derivative is
at an endpoint or `sqrt(V/3)`. The code's interior maximum is
`9/(8*sqrt(3V))`, using a lower radical in its denominator. If V=0
the line has zero slope. The exponential line's left value and uniform
derivative use the same rate and MGF upper bound. The centered/shifted
excess helper uses a positive lower denominator for `exp(x)-1-x`;
its reciprocal derivative is bounded at the smallest positive x.

Every selected pair `(left_value,slope)` is a complete upper line on the
whole phase interval. The source may choose a different whole line for
each incoming count, then adds them with nonnegative binomial mass upper
bounds. It never chooses unrelated left values and slopes. Stop-loss
endpoint optimization is done with a single scale for both endpoints of
each chord. Its finite-alpha endpoint maxima dominate a complete family
of such chords, not independently optimized values without a matching
whole-phase bound.

Write L and S for the summed left value and nonnegative upper slope.
The Gaussian derivative lower bound g comes from

`T=max(abs(k+ul-n*pu),abs(k+uh-n*pl))`,
`g <= phi(0)*exp(-T^2/(2*(n*vmin+lo)))/sqrt(n*vmax+hi)`.

The numerator maximum, denominator endpoints and density directions are
correct for both signs. If the optional compact exponential gate fails,
g is zero and no positive derivative cancellation is inferred.
For every actual law/parameter in the box,

`incoming(u)-Phi(z(u))
 <= L-Phi(z(ul))+(S-g)*(u-ul)`.

If `S<=g`, the right side is at most `L-Phi(z(ul))`.
This is why the evaluator can replace its first scalar by L. It is not
asserting `incoming(u)<=L`. The `finish` caller subtracts the Gaussian
at ul; its centered binomial/Gaussian alternative is also at ul.
The coherent caller at 528–530 uses the same L, S and g through
`drift=S-g`, `intercept=base+L-drift*ul`. The common-cubic callers remove
that complete old incoming line and retain the same Gaussian lower line
before adding their replacement. No caller in this inspected path uses
the first scalar alone as a probability bound.

Upward rounding of L and S preserves their line for `u-ul>=0`; downward
rounding of g preserves its lower line. The two endpoint dominance check
at 384–385 chooses between complete rounded lines and cannot splice them.

## Every score-return path and min/max order

At 521–527, `finish` combines two complete CDF-minus-Gaussian upper bounds,
subtracts the common nonnegative own loss, adds the paired incoming value,
takes the positive part, and only then multiplies by an upper sqrt(n)
and divides by a positive rho lower bound. Incoming probabilities are
nonnegative when binomial mass upper bounds are substituted.

The subsequent order is:

| Engine lines | Complete alternative |
|---|---|
| 528–533 | One common phase, variance-only outgoing quartic, all endpoint cases. |
| 534–538 | The same phase with a shared conditional-cubic polygon. |
| 539–549 | Both closed affine-rho normalization pieces, then convex common-cubic incoming and optional shifted-excess alternatives. |
| 550–554 | Complete own-count probability upper bound, retaining all prior complete score alternatives. |
| 555–559 | Complete exact SOS quartic strategy. |
| 560–563 | Complete fixed-peak quartic strategy. |

Each quartic scale/shape is fixed before maximizing over every Bernstein
control and every required moment-polygon vertex. Each common-cubic
rate/pivot/constant strategy is fixed for the whole polygon and phase
interval. Minima occur only between complete valid scalar bounds.
The affine-rho seam is explicitly split before the convex-numerator /
positive-affine-denominator vertex argument. Positive parts are taken
before the upper normalization factor.

The V10/V11/V12 dispatch at 565–593 does not introduce a new physical
domain. It reuses the complete engine with a different incoming evaluator,
retains an already closed result, and otherwise chooses a smaller complete
score upper bound. It checks that every physical output field agrees;
only status and score may differ. The fixed target K=0 in these selected
capsules makes `score<CE_LO` a strict exclusion below the true C_E.

## Arithmetic and the coupled binomial/Gaussian primitive

The separate internal [selected count primitive review](code_count_primitive_audit.md)
and [source map](code_count_primitive_source_map.json) check the three pinned
primitive files across all 75 retained capsules and their correspondence
with the portable p31 reference. That review supplies the interval,
exponential, radical, Gaussian and binomial primitive edges used here;
it does not replace the caller-specific analysis below.

The full module AST of count `finite_gaussian.py` **before its `panel`
function**, including imported constants, Machin setup, radical guards,
positive CDF, tail and endpoint functions, is identical to that prefix
of `local_contact_binomial.py`, SHA
`939236711b080f9148ee3d3f7f6a0cd15b86cb24f3d2700f0e7127b2a345291f`.
The latter primitive has a separate internal derivation in
`code_fourier_primitive_audit.md`. The count file's differing disabled
legacy panel is not used by this native engine. This is an explicit
source bridge, not an inference from similar filenames.

`exact_count_core_v5.py` 35–42 supplies another simple exponential pair:
the positive sum through degree 48 is a lower bound for exp(x), and for
`0<=x<50` the tail starting at degree 49 is at most
`x^49/49!/(1-x/50)`. Directed rounding retains both directions.
A completed path must satisfy every checked exponential domain; a rejected
domain aborts rather than returns a false score or EMPTY result.

`normal_lower`, 44–48, chooses the radical endpoint according to the
numerator sign, then rounds the absolute argument in the direction
required by Gaussian monotonicity/reflection. Its compact argument gate
must succeed in a completed replay; it is not an omitted threshold tail.
The actual nearest-count domain is acquired and checked separately.

For `centered_binomial_gaussian`, 111–129, at fixed p the maximum over
lambda is at a lambda endpoint because the Gaussian CDF is monotone in
variance for a fixed numerator. Both endpoints are tested. At each, the
source computes a midpoint upper value plus halfwidth times a whole-cell
absolute derivative bound. The derivative of
`F_Bin(n,p)(k)-Phi((k+ul-np)/sqrt(n*pq+lambda))` is

`-(n-k)*b_k/(1-p)
 +phi(z)*(n/sqrt(D)+(k+ul-np)*n*(1-2p)/(2*D^(3/2)))`,
`D=n*pq+lambda`.

This is the coded expression, including k=n and probability panels on
either side of 1/2. Full interval products retain both signs. A midpoint
sample alone is never the returned bound.

The scalar interval optimization retains negative multiplication endpoint
reversal, delegates non-point interval products to the original four-
corner implementation and changes no arithmetic meaning. The exact
Bernstein optimization uses the same positive elevation and signed
coefficient selection proved in `code_count_kernel_audit.md`.

## Retained-catalog source variants: exact comparison

The selected retained catalog SHA is
`f055b5017d4e1fd14f2b48a6a95fef4a4c61a025dea6174c424cd5968de801f7`.
Actual sources were read from pinned `cutoff25_20261011.zip`, SHA
`17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`.

| Core SHA-256 | Selected jobs | Representative archive-relative capsule |
|---|---:|---|
| `512c70ead43294a7f1d4e14922c9c3a55d3928c9555f4af1415cacf5ad6657bb` | 32 | `cutoff25_20261011/new_low/count37_global_conditional_v2/` |
| `67cb474849d0a2e68f5e00f04212ff1356ecb592312a64a04fb9386b0ac9bd57` | 2 | `cutoff25_20261011/new_root/global_tangent_b1_p40_q0_v1/` |
| `908c406f64298f5e8f111016a5cadac8c1597dd67b5c45e4cbf87f0be61d410b` | 7 | `cutoff25_20261011/new_root/global_joint_cubic_b1_p34_q0_v3/` |
| `660a83656239d197346392a053f021a07a8b121453e34c4771a56c893a2b903d` | 16 | `cutoff25_20261011/new_root/global_sos_quartic_b1_p36_q0_v8/` |
| `48cc8a17f64885be7ba36ea6d70d84eb349f06da71d64804e0e8956d65fae241` | 12 | `cutoff25_20261011/new_root/global_fixed_peak_b2_p29_q0_v9/` |
| `a618867ae34841b2e3e1745e35142694142e08ca2d790b762870f50651e16d71` | 6 | `cutoff25_20261011/new_root/global_alpha_stoploss2_b2_p33_v12/` |

All six have identical function ASTs for `quadratic_cap`, `sharp_gates`,
`effective`, `binary_lower`, `sharp_lower`, `box_sharp_lower`,
`bounded_cubic`, `cubic_upper`, `own_cdf`, `own_mgf_upper`,
`incoming_cantelli`, `own_phase_upper` and `optional_exceeds`.
The actual differences were read, not inferred solely from those hashes:

* The base incoming helper uses Bennett/Cantelli only. Tangent adds sharp
  and coupled-tangent MGF upper alternatives.
* The joint-cubic version adds the individual cubic lower bounds to
  incoming MGF options, moves the same valid polygon contradiction before
  the cheap score path, and adds a complete common-cubic score bound.
* The SOS version adds matched centered/shifted incoming lines, a complete
  shifted common-cubic strategy and the exact SOS outgoing strategy.
* Fixed-peak adds the complete fixed-peak strategy after retaining all
  earlier complete results.
* V12's `_cell35_engine` is exactly the fixed-peak `cell35` after renaming
  that function and replacing its incoming helper by an argument. V12
  adds the three declared complete incoming refinements and dispatch
  wrappers, reviewed above.

The 11 simple B0 capsules use wrapper SHA
`1fe8fefd93269e478be47077b3bf1c8d0cff9259de94824d55a66824b8052cdc`.
Its source diff from the theta-enabled wrapper only omits theta/mean/
allocation contractions and monotonicity corner shortcuts. It retains
the interval beta/mean checks, necessary rho/beta noise floors and the
`lo>0` solved-allocation gate. These omissions weaken necessary
contractions; they do not remove the original resource premises.

Some files inside larger sealed inventories are not enabled in this path:
the generic non-SOS `general_quartic_v2`/`general_quartic_bounds_v2`, legacy
`exact_count_core_v5.cell`, and legacy finite-Gaussian `panel` are not
called by the selected V12 native engine. Presence in a manifest is not
evidence that a strategy was used, and unused research alternatives are
not promoted into this conditional engine conclusion.

## Remaining boundaries

This source-level invariant argument is not machine-checked formalization.
It found no mathematical blocker in the complete selected V12 execution
path, including the listed retained variants, but supplies no numerical
acceptance. The named component proof notes remain explicit evidence;
their conclusions are not enlarged to other source hashes or callers.

Still separate are: actual contact/support/resource acquisition for the
same unrestricted attaining witness; complete region and reflected-law
coverage; fresh native execution under its precise source epoch; and the
other indices and external inputs of the manuscript. A protocol guard or
an immutable contract field does not establish those mathematical facts.
No runtime file, candidate, receipt, contract, notebook or graph was edited.
