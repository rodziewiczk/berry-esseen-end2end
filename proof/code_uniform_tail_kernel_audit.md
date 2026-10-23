# Selected uniform-tail kernels: source-to-lemma audit

**Review status:** AI-generated internal source review. Cross-reads by
other model agents are internal checks by the same AI system. External
independent mathematical review and machine-checked formal verification
are not established here. This review may contain mistakes or omissions.
See the [evidence limits](CODE_INTERFACE_AUDIT.md#evidence-limits).

Date: 23 October 2026. This is a static mathematical/source read, continuing
[the global/tail logic audit](logic_global_tail_audit.md) and separating it
from [the execution-join audit](code_aux_tail_join_audit.md). No numerical
kernel, certificate reconstruction, bound evaluator, constructor, scalar
acceptor or mathematical test was imported or executed for this review.
The only executed checks read bytes/JSON, compare manifest hashes, and inspect
the signs of already stored rational fields.

**Scoped finding:** the inspected central confinement, weighted-resource,
normalization and LOW/MID/TINY formulas have the required conditional
source-to-lemma interpretation. No new confirmed mathematical gap was found
in that path. This is not a proof that their finite inequalities pass, that
all 83 rows have been acquired, or that the entire tail/global theorem has
been accepted. In particular, the left comparison kernels and the full
LOW/HIGH Fourier derivation remain outside this detailed implementation read.

## 1. Exact source and selected path

The supplied v4 `berry_esseen_manuscript.tex` has SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
Manuscript line references below refer to those 9,252 lines. Frozen source
references are from `BE_cutoff49_20260930.zip`, 16,660,566 bytes, recorded asset
SHA-256 `ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e`.
The actual exported `original-BE49/MANIFEST.json` read here has SHA-256
`58a770705c6e0bc500813ed37299753a16f6245ebea6ade238ad98078d7b4e26`.
All 36 source/proof files pinned in section10 matched that manifest byte for
byte. This is source-integrity evidence, not arithmetic acceptance.

Unless prefixed `A:`, frozen paths below are relative to
`baseline/certificates/work/below50_20260929/`. `A:` denotes a path relative
to the top of the original archive. These aliases avoid machine-specific
paths. The central path is the 45 closed probability rows covering
`[.38,.47]`; the other 38 rows cover `[.304,.38]`.

The actual selected central dependency direction is:

1. Separate all-threshold contact support and the INITIAL47 signed cover;
   the corrected broad PREP pass; then the radius 2.5 support implication.
2. Central INPUT47 and its original weak 45-row interface; the separately
   proved strip `supp(Y) subset (-.55,1.55)`.
3. Ordinary confinement, then confined feedback; independently licensed
   Sperner confinement, then Sperner feedback. A new amplitude is consumed
   only by a later resource pass.
4. Original weak-interface noise-dependent Sperner amplitudes, together
   with the refined central table; checked finite-binomial normalization;
   central LOW plus central MID and wide TINY.
5. A separate exact Bernoulli argument at zero noise, and the full selected
   coverage composition. The left38 rows require their own dependencies.

The old and refined resource bounds are simultaneous facts about the same
law. It is not necessary, and would be incorrect without another argument,
to infer componentwise domination of all old corner quadratics from a few
improved scalar fields. The coverage checker's resource note explicitly
retains that distinction (`local/final_review/check_local47_coverage.py`:127).

## 2. Phase curvature: distinguish the repair from its later license

The enabled route includes an actual repair, not unconditional use of the
old paired curvature. `A:legacy_phase/accept_phase_corrected_v3.py`:18–33
binds its source manifest, rechecks the ten PREP targets and 125 complement
cells, and compares every surviving complement resource in the required
direction. Its scope is not the later local comparison.

In `A:legacy_phase/corrected_phase_callback_v2.py`:15–25, put
`g0=3.16*rho-3-D` and `phi_low=PHI*(1-5*raw/(2N))`. The old expression is
`q=C*rho+phi_low*g0/2`. The new one is exactly

`q_corrected = C*rho + min(phi_low*g0, .4*g0)/2`.

This selects `.4*g0` when `g0<0`, in the correct adverse direction. The
callback checks the original formula, `0<=phi_low<=.4`, positive corrected
curvature and all four corners. The corrected curvature is concave in
`rho`; on a positive interval its reciprocal is convex. Thus the existing
endpoint reduction is not licensed merely by ignoring a negative `g0`.

Later source calls require a separate upstream lower-bound premise for
the actual marginal, conditional on its named certificate:

`gamma >= sqrt((1-Theta)^3*(1-2p)^2/(pq))
          -(R+2*sqrt(p/q))*Theta`.

`A:legacy_phase/check_later_phase_premises.py`:17–46,51–66 and
`A:audit/portable_audit_phase_scope.py`:41–48,64–96 bind 302 selected input
rows and require this lower bound to exceed `.096`, conservatively using
the common radius 3.84. These are arithmetic obligations here, not executed
results. Once established, the actual `gamma` remains positive throughout
each later refinement, because the acquired input facts remain true for
the same law. With `gamma>=g0` and `gamma>=0`,
`phi_actual*gamma >= phi_low*gamma >= phi_low*g0`; the old lower-density
choice is then valid even when the auxiliary `g0` happens to be negative.
No monotonicity of a rounded iteration's `theta` is required for this
argument. The broad corrected replay and the later 302-row license are
separate AND inputs.

## 3. Signed confinement and one resource

The direct mapping is:

| Mathematical step | Manuscript | Selected source |
| --- | --- | --- |
| Same marginal, signed contact derivative and deleted-law concentration |7652–7697,7807–7852| `local/confinement47_contract.py`:18–34; `local/confinement47_kernel.py`:18–39,71–108 |
| Outward scales, moment prices and binary penalty |7699–7737| confinement kernel40–51; Sperner kernel43–54 |
| Strict-gap antichain alternative at both deleted indices |7740–7806| `local/sperner47_kernel.py`:28–30,55–61,92,109–116 |
| Signed interval geometry and restricted negative slope |7854–7970| confinement kernel71–108; Sperner kernel81–112 |
| Four concave budget quadratics and closed-box exclusion |7985–7995| confinement kernel54–69; Sperner kernel63–77 |
| Single-budget error and eleven simplex tangent bounds |7997–8036| confinement kernel112–127; Sperner kernel120–135 |
| Strict margin and complete lower ray |8038–8063| confinement kernel128–134; Sperner kernel136–143 |

Both fixed contracts pass `Qbudget`, rather than `Qraw`, to the kernel.
The Gaussian phase price has already been added to `Qbudget`; the selected
additional `rebate` is zero. Maximizing each concave quadratic at its
clipped vertex, taking their maximum and then intersecting with `T`, is a
valid outward upper bound on the common budget. Four corner bounds must
remain four bounds; their maximum is not replaced by an unjustified minimum.

The multiplier sign missing from the general prose formulation is guarded
in the implementation. Confinement line23 and Sperner line24 emit the
strict `beta_domain` gate, and their cellwise `blo` is no smaller than that
input floor. Static JSON inspection here found positive stored `beta_lo`
in all 45 refined central and all 38 selected left rows. Their table hashes
are respectively
`4a1ea8a439e85e9f481bb6c6eb7a197ec4d35e53ceecf0ec92c3d4c96b9f618a`
and `4b7bb259e469ee57ca6a61d89fd0b3385443508129138899fe597fd82dc9521a`.
This supports the selected sign gate; it does not repair the general
parameterized manuscript statement automatically. The explicit R3 editorial
requirement in the global/tail audit remains.

The allocation uses one simultaneous inequality for the two moment
resources, variance and leakage. Its old error multiplier is positive
before the inverse-index relaxation. Every additional tangent is separately
an upper bound for the same pair-failure probability; taking their minimum
is valid. The kernels do not add separately optimized costs that each spend
the entire common residual. `cap<=0`, including equality, is a valid empty
closed box because the preceding budget inequality is strict.

The Sperner alternative requires interval width strictly below the acquired
gap. Its explicit width gates are material: a closed interval of exactly
one Bernoulli gap can contain both endpoint atoms. Both actual deleted
indices are bounded using `J=N-2` and the recorded mode interval; adding the
independent noise preserves this concentration bound. The ordinary branch
instead retains the actual deleted-law score concentration and the extra
uncoupled affine slope needed to cover the entire lower ray. The source
does not reflect the marginal when changing the sign of `H`.

## 4. Uniform index, weighted exports, and the inverse-index endpoint

The relevant invariant is

`raw_actual <= raw_stored`, and `n*D_actual <= N*D_stored`, with `n>=N=47`.

It is stronger than the unweighted statement `D_actual<=D_stored`.
`entry/local_signed_core.py`:123–141 and `entry/sperner_panel_core.py`:35–58
export the defect bound by dividing the conserved budget by
`kappa*N`, where `kappa=997/15000`. The interpretation is
`n*kappa*D_actual < budget_upper`; hence the new stored quantity satisfies
`n*D_actual <= N*D_stored`. Intersections and complete cell unions preserve
this interpretation. The detailed paper explanation is
`entry/initial47_panel_proof.tex`:13–42,91–153 and manuscript2535–2588,
7348–7369. This read maps the invariant; a full independent proof of every
Fourier envelope feeding that conserved budget is still required.

The final noise export is not `N` times an arbitrary variance bound.
`variance_resource`, `entry/sperner_panel_core.py`:18–26,59–63, derives
`D_actual >= b_* + K_var*theta`, with `b_*>=0`, `K_var>0`. Therefore

`n*K_var*theta <= N*D_stored - n*b_*
               <= N*(D_stored-b_*)`,

and

`lambda=n*pq*theta/(1-theta)
       <= N*pq_max*(D_stored-b_*)/[K_var*(1-Theta)]`.

The source implements exactly this residual and weighted ceiling. A
negative residual is an impossible cell, and positive divisors are checked.
The corresponding inward-gap export uses the same simultaneous inequality.
The noise price `K_var` is a minimum of two positive signed-variance prices;
it must not be confused with the signed moment named `beta`.

For central LOW, manuscript2514–2533 gives the stronger displacement price.
Writing the true inward distances as `a0,a1>=0`, `d=a0+a1<1`, one has
`A+B=ell*(1-d)` and `Delta_A+Delta_B=ell*d`. Its displacement term is
`6*m*ell^2*((1-d)*d+a0*a1)`. Dropping the nonnegative product proves

`D >= m*ell^2*((6+2*sqrt(10))*(p-p_*)^2+6*d*(1-d))
      + K_var*theta`.

This explains LOW lines72–77, including the unshifted binary penalty,
`alpha=6*m_lower*ell_lower^2*(1-d0)` and the two-sided minimum variance
price. With `theta=ell^2*lambda/n`, multiplying by `n` yields the source's
`nd<G` after subtracting `N*penalty` and the lower-noise variance charge.
No independently chosen law or duplicate resource is introduced.

To avoid a notation collision, write `t=1/n` for the index variable here;
the physical conditional noise is `s=E U^2`. The local normalizers and
confinement use sign-aware domination on `0<=t<=1/47`, not enumeration of
47, ..., 98. The positive terms in the contact callback are bounded at the
floor. In LOW, the coefficient multiplying `1/n` is checked positive before
using `1/n<=1/N`. Its continuous value at `t=0` is zero for that term;
the remaining constants and strict signs stay defined. There is no division
by `t` and no silently substituted finite upper index. This index endpoint
is distinct from `lambda=0`.

The initial source's `nmax=98` is used in `c0=.4095+K/nmax`; the selected
`K=0` removes that dependence (`entry/local_signed_core.py`:26–29).
`A:root/heat_support50.py`:55–66,97 likewise exports `[N,None]` when
`K=0`. Thus98 is not an upper endpoint of the selected uniform local lemma.

The HIGH source checks the exact analytic monotonicity gates, e.g.
`2*N*c>1` for `sqrt(n)*exp(-c*n)`
(`entry/high_window_core.py`:17–18,24,31). These license evaluation of an
outward upper bound at the floor. Do not infer that the executable rounded
helper is itself decreasing for unbounded integer arguments:
`entry/contracted_kernel.py`:27–31 caps its exponential-series argument at64.
The valid justification is monotonicity of the underlying exact analytic
quantity, followed by its outward floor evaluation. Completing the
LOW/HIGH proof beyond this monotonicity interface is outside this review.

## 5. Support callbacks and acyclic feedback

`root/panel_exterior.py`:38–62 applies the same actual contact expression
on both signs of `X`, with Bernstein bounds for its signed polynomials and
positive higher-order/remainder charges at `N=47`. Lines65–94 transform
the forbidden `Y` strip into conservative `X` endpoints using a positive
lower `ell`. They explicitly derive and require nonnegative `beta_lo`
before choosing the signed coefficient endpoints. Both exterior strip
boundaries and atoms remain included in the tested closed cells.
`root/panel_exterior_proof.tex`:7–60 explains why all discarded positive
index charges decrease with actual `n`.

`root/accept_support47.py`:15–38,44–56 binds ten broad radius rows and45
fine exterior rows. These are conditional implications. The source says
so explicitly at70–74. Their successful arithmetic cannot acquire their
own moment hypotheses or the initial radius 3.84. In the central chain,
PREP gives the broad moment/threshold rows before the radius 2.5 callback;
INPUT then uses that radius; the fine input precedes the strip callback.
The extra47-row exterior theorem is separately named and is not a
replacement for every support obligation merely because it has more rows.

`entry/accept_confined_feedback47.py`:29–56 binds the weak interface and
the separate confinement rows before computing the contracted actual
radius;58–78 checks upper fields upward and endpoint/curvature lower
fields downward. `entry/accept_sperner_feedback47.py` repeats that direction
with the preceding confined table and the separately required Sperner
amplitude premise, conditional on its named certificate.
In `entry/sperner_panel_core.py`:64–75, the export retains the
signed linear endpoints and uses `Qbudget=Qraw+extra`. The separate
`paired_conditional_gamma47` callback improves a conditional cubic lower
bound while retaining its explicit paired moment/radius gates. This
establishes an acyclic conditional interface; this note has not replayed
the moment-row inequalities or every support/composer binding in the full
archive DAG.

## 6. Normalization, Poisson tails, TINY and MID

The local identity uses the actual integer count, actual `n`, actual
variance `pq+s`, one nearest-count phase and the same two conditional laws
(manuscript8228–8269). The outgoing event is strict and the incoming event
closed (8305–8308). A sign branch for `H` is not a reflected law.

`root/low47_normalization.py`:33–77,80–139 matches the finite-Stirling
recipe at8315–8421: a positive outward scale, a shift ceiling containing
every mode, legal interior counts, a valid entropy segment, positive
binomial mass and derivative bounds, variance envelopes and legal count
ratios. Its repair checks a positive cubic bracket and handles the normal
variance correction with the adverse sign. The `pq+s` upper bound includes
`maxnoise/N`; it is not clipped to1/4. Every denominator/sign gate is a
finite obligation. These constants bound actual indices above 47 through
the floor inequalities, not by replacing their actual binomial law by
`Bin(47,p)`.

The continuous Poisson comparison is manuscript8444–8485, not an inference
from sample distributions. Its smoothed positive-cubic test has
nonnegative second, third and fourth derivatives; the centered-Poisson
semigroup Taylor remainder then permits successive replacements and an
increase to a variance upper envelope. In the code:

- LOW `poisson_numerator`24–38 uses the full cubic moment plus the finite
  nonnegative correction, with an upper bound for `exp(-mu)`. The cubic
  part can be negative; dropping the correction would be invalid.
- TINY16–32 and MID12–22 use the positive series through32 and a guarded
  geometric tail. Bennett uses a lower logarithmic/exponential series,
  producing an upper tail bound. Every anchor is constrained below the
  actual normalized threshold. The MID Bennett helper imported from
  `tiny47a_kernel.py`:25–32 is the same formula read in this audit; importing
  that helper does not license the unselected TINY-A theorem as a whole.
- All lower-tail uses are obtained by applying the one-sided theorem to
  the negative of the same centered noise, whose absolute support is
  bounded. Both closed and strict events are safely dominated.

Wide TINY's selected scope is every `0<lambda<=.05`, both phase signs,
`p in [.304,.47]`. `local/tiny47wide_kernel.py`:49–67 implements the
rescaling at8534–8565. After `r=z*t_k`, the quartic divided by `t_k` is
concave in `t_k` and extends to zero. Its value at zero is linear; at the
upper endpoint a lower quadratic is minimized at its endpoints and any
clipped vertex. Thus the `t_k=0` boundary used in the enclosure is real,
not an omitted positive-noise limit. Lines69–83 separately check
proportional-to-noise Poisson and Bennett gates for the near-zero phase
families; the other positive-phase families use an unscaled positive bound
and divide only after checking its bracket. A positive lower `lambda`
endpoint is never substituted into this TINY interval. Either conditional
variance may be zero.

Central MID uses four closed positive-noise/outer-phase regions
(`local/mid47a_kernel.py`:9,35–59). The shifted quartic is concave in the
actual variance; hence its two variance endpoints suffice. Each signed
phase monomial is bounded at its adverse endpoint, and any selected scale
is a valid witness. The Cantelli/normal alternatives are independently
valid. First incoming count plus the complete Bennett geometric remainder
retains all later legal counts, with harmless extra positive bounds for
illegal counts. The source requires all 2,620 phase rows and the full
comparison reserve, not merely a successful witness for some phases.

## 7. Whole-count LOW: marked crossing and fractional parts

`root/low47_kernel.py`:62–65,105–159 maps manuscript8594–8807 as follows:

| Source | Mathematical role and required sign |
| --- | --- |
|62–65,105–106| `c=1-d0>1/2`, positive inward resource/denominators, `G^2<c_v*N*L`, positive variance envelope. |
|111–127| First two marked pairs: projected positive distances; minimum of independent Cantelli/Poisson and common-background bounds on every closed phase subcell; maximum over the cover. |
|129–132| Fourth-moment midpoint integral for every remaining mark; fixed positive `z`, `eta=z*lambda<=1`. |
|135–145| Signed binomial curvature enclosure, including both positive-part kinks and a positive third-root upper bound. |
|146–150| Harmonic rate, increasing Taylor remainder frozen at `L`, and phase derivative error. |
|151–164| Both noise endpoints; event bracket negative, inverse-index coefficient positive, full strict score gate; exact feasible/empty cell census. |

The marked proof deletes the entire pair only after restricting to its
active event. Independence then factors the remaining sum from that pair;
it does not assert independence of the two deleted marginal sums.
The common-background bound preserves both marginals and uses disjoint
events of one centered background. The code's `t=ownhi*L` is the lower
endpoint of a chosen *variance upper envelope*, not a positive lower bound
for the actual deleted variance. The derivation at8662–8688, and
`structural/low47_new_lemmas.tex`:144–219, justify precisely that distinction.

The first-moment mark price follows from the centered one-sided quadratic
majorant under `G^2<c_v*N*L`. The source freezes the kernel, center, anchors,
resource cap and `z` before the final noise variable varies. Each such
rational choice is valid without proving it is globally optimal.

For the fractional-part reserve, the support span is `amplitude+d0<1/2`,
not merely the amplitude. Independence multiplies characteristic-function
moduli; the elementary scalar inequality
`1-cos(2*pi*x)<=(23/5)*x` on `[0,1]` converts this into the stated gain.
`baseline/structural/check_fractional_scalar.py`:13–47,51–68 specifies the
Machin enclosure and all 80 positive Bernstein coefficients over eight
closed intervals. This scalar program was read, not executed. It is an
actual whole-interval obligation, unlike the finite-distribution controls
in `structural/check_low47_new_lemmas_actual.py`.

With constants fixed on a positive closed noise cell, the final functions
have the form

`B(lambda)=z+a/(b*lambda+c)-h0+h1*lambda-g`,

`I(lambda)=I0+I1/lambda`, with `a,b,c,I1>=0`.

Thus `B` and `m*B+I/N` are convex, and `I` is decreasing. The source checks
`B<0` **before** using a binomial mass lower bound and `I>0` **before**
replacing `1/n` by `1/N`. Both endpoint strict inequalities then cover the
entire closed cell. The coarser central bound `|H|/ell` in the curvature
coefficient is an outward enlargement for either signed threshold, not a
change of law.

## 8. Closed cover, zero noise, and the 83-row boundary

The selected coverage source is
`local/final_review/check_local47_coverage.py`:26–127. It checks scalar
strengthening of the old central interface; licenses each applicable
amplitude on the entire closed noise band; retains TINY, LOW and the
appropriate MID rectangles; and tests every endpoint and open-cell
representative of their exact rectangular arrangement. Since membership
in closed axis-aligned rectangles is constant between their boundary
coordinates, those representatives suffice. The45 central and 38 left
rows share the closed `.38` seam. Row-ceiling singletons, `.05` and other
noise seams, `u=+/-1/2` nearest-count ties and both `H` signs are retained.
Its frozen LOW-object checks require both endpoints for every feasible
box and recognize an entirely budget-excluded row without inventing a
worst score.

At physical `lambda=0`, centering and `0<p,q<1` force both conditional
noises to vanish. The law is exactly Bernoulli; the positive closed maximum
is an atom. The separate Schulz theorem and the preceding-atom argument in
manuscript8875–8885 are required. A rectangle labelled “Bernoulli at0” in
coverage line91 is a dependency label, not a numerical proof of that
published theorem. No division by zero or limit through varying marginals
can replace this input. For positive noise, the local result gives
`rho_B*(C-C_B)<-.001*lambda`; `rho_B>0` and the Bernoulli upper theorem then
give the desired contradiction. The primary literature boundary is
recorded in [literature_inputs.md](literature_inputs.md).

The coverage program's historical text mentions descent47..98 and a99
tail (line127). Its geometric result is a conditional cover for `n>=47`.
The newer 49 least-failure composition is separately specified; the text
does not itself prove or invalidate that composition. This audit leaves
the original 14-production/41-retained replay unchanged.

## 9. What this read does not close

- The 38-row left acquisition and comparison path, including
  `left_sperner47_kernel.py`, `left_mid47b_kernel.py`,
  `phase_left_low47_kernel.py` and `positive_left_low47_kernel.py`, has not
  received the detailed line-by-line derivation above. Wide TINY's shared
  formula was read, and the geometric83-row composition was read; that
  does not prove every left rectangle's inequality.
- The universal signed-entry cover, support3.84 acquisition, general and
  paired LOW/HIGH Fourier bounds, HIGH-window refinements, Pearson/Mills
  coefficient enclosures and every corner-convexity derivation are not
  fully independently re-proved here. Their imported formulas and exact
  hypothesis gates remain explicit upstream obligations.
- The finite40–50 ceilings, corrected supported barrier46 and all their
  independent support callbacks are not replaced by this central local
  audit. The original 49 route and the conditional shorter 47+ proposition
  in the logical audit remain alternative compositions with their stated
  premises.
- Unselected earlier TINY variants, `left_binary47`, older95/99 kernels
  and discovery/optimization scripts are not silently covered by common
  filenames or helper imports.
- Stored positive gates, declared cell counts, source hashes and finite
  actual-law examples are not fresh arithmetic replay. An interruption or
  partial retained-component run cannot be promoted by this review.
- The general manuscript confinement statement should explicitly include
  the nonnegative signed-moment multiplier gate (R3). The selected sources
  enforce it; no selected failed certificate or new `CONFIRMED_GAP` is
  asserted here.

All native/global/theorem acceptance boundaries therefore remain separate.
No runtime code, frozen source, notebook, proof graph or publication pin
was changed by this audit.

## 10. Exact inspected source pins

These 36 byte hashes were checked against the actual exported original
manifest. Paths use the aliases defined in section1.

| File | SHA-256 |
| --- | --- |
| `local/confinement47_kernel.py` | `59a601bf5615922e7ab1c71b22bdc25903e2f37c803eeb24d91919f370b6bfe7` |
| `local/confinement47_contract.py` | `68977fb0cb98507f39ab1d55122efcecec5ad8d65c5c2e4f47cf260e66f813c7` |
| `local/sperner47_kernel.py` | `21249fe117c6756a7a84af481dea2c5a490f9c66013c331cc998ab6828e1bb08` |
| `local/sperner47_contract.py` | `f815e4d0b0124709f4f5922726cd20ef224d115dbd6251de6a633c955c60b8a2` |
| `local/accept_sperner47_profile.py` | `f57b691d5237b30b996440e83e4e639baded70767a7d9754868e3f2ce18a61dc` |
| `entry/local_signed_core.py` | `f0c2df790b794413e7fd08c4f3fc20f79c15c27a6456c8eae5013b96eb093c11` |
| `entry/local_panel_core.py` | `6e8c664e3870e1786ebd999f56c18e6319340602b0bcea7c5f18d0fc44f070ff` |
| `entry/contracted_kernel.py` | `0367aae733dfe2d6467188d941d6fc8ccd7bb6f4bf3aa4c98dca3c4781534d22` |
| `entry/high_window_core.py` | `53e181be63852e21abc3f44191cce7237c46d9e9d7868d3b6b94fccb606c7232` |
| `entry/paired_conditional_gamma47.py` | `2652ed1bfe72da2c802aceb06d280cb7f22abc70e8a608e866c53c9d30888e74` |
| `entry/sperner_panel_core.py` | `c1f6e77145ab1d7772e6c8fbb254655aa58e7e15941455e568955e8ae57620f7` |
| `entry/accept_confined_feedback47.py` | `0341dd3d29469c571f86862013902cbc1865fff2c24035d645bba302d8f63ddb` |
| `entry/accept_sperner_feedback47.py` | `e6e95ff4a329f4451967eb0d4f39d3f0d0884b8ebcc2177a6a7b28940eda3a3a` |
| `root/panel_exterior.py` | `4b2393ee11117a241eb035f2aa8d93b64128c79ab297305ccdc2677fa36b6092` |
| `root/gaussian_core.py` | `2d525417592046f615cf2b0ed9d72d80959609eba477f760cda192f9b535180d` |
| `root/accept_support47.py` | `58afe8959f004e568aa4bbe69de0c759670de3114d035e506ba978124bd39c91` |
| `root/low47_contract.py` | `3d7f378a975a9b46c54d1a32e90f80bf44ca8a2fb50a4fbe2c7195927fe0beb5` |
| `root/low47_normalization.py` | `3312a3cb096257afa6871c346b3f62e6c832516840aabe5146d5117574bedc1d` |
| `root/low47_kernel.py` | `176aa32731b414faeba5b8dffee0e30f7fc549577875fd438a8fba96c27bb37f` |
| `root/accept_low47.py` | `8a9606e7d843983421ca15d19d5ce909153963140fa8201765bde0af0bc61701` |
| `local/tiny47wide_normalization.py` | `f1e2606359e321d17db11c7240467a597f00094d1747d40ed4f69ceae18d4b71` |
| `local/tiny47wide_kernel.py` | `daa468b6b825dbb692c8a1930cc1cf94ffd9bd143c354fe22dde9575752b2626` |
| `local/mid47a_normalization.py` | `5652d64a77b58bf1b34b26e9d74712e1050235972a9fd68b6f095eec07eb2a04` |
| `local/mid47a_kernel.py` | `b2e514b3f9d7c3ac37cd04e670671d50d614df93e01e907c6aad04af91a9b1c4` |
| `local/tiny47a_kernel.py` | `38b58e946ee4e2dadad124e54cd65da688d44f519064e93c0918bc22755fbe82` |
| `local/final_review/check_local47_coverage.py` | `4e95ff6f5a14539edaf7d766eca13a70fb27db81d8e70d2d083d1fa25e8f3153` |
| `local/final_review/accept_local47_coverage.py` | `c12dcbeb47349266a178a465d8e6e6b6446d31086fcd3ce5c665c9176a73f996` |
| `baseline/structural/check_fractional_scalar.py` | `16e61bc2d61e826f2a437b3a62afdcf7380143ce51e362cd4edbb681aff5da7b` |
| `structural/low47_new_lemmas.tex` | `c5798455abd48aa363eab4dce7460489c414df8c019a91ac00a0ecfa56512a07` |
| `entry/initial47_panel_proof.tex` | `cff6a275ad9cdd3c6b347ea8fe34e548dc8deee0ce96299882cbe27b2f1cf142` |
| `root/panel_exterior_proof.tex` | `c836e9fbab9bb278aaf98b7e81037d2ddad4156ab34fc72955aa3a4f21d220a6` |
| `A:legacy_phase/accept_phase_corrected_v3.py` | `a2775c439b09c36c6130a49784403644019391f925184ee97feaff8e0a40c9dd` |
| `A:legacy_phase/corrected_phase_callback_v2.py` | `65b91b83fd888aea1b01bfe6f16040fc1b51b9ced1520a866aa82778bfd4a2d6` |
| `A:legacy_phase/check_later_phase_premises.py` | `80e435e338c52c0cbe9b60fe7f330a346f644086a643e9c7ca8c35873ce7fa42` |
| `A:audit/portable_audit_phase_scope.py` | `cdce2fe069fd6185a211baff7b0ed7748c256f92be6062db2a825c046b69fcec` |
| `A:root/heat_support50.py` | `650d7f3617775102fe92977605dfda5fb68a11e0ad738eb799aab77bc4a79e18` |
