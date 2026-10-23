# Selected INITIAL cover and finite-feedback code audit

**Review status:** AI-generated internal source review. Cross-reads by
other model agents are internal checks by the same AI system. External
independent mathematical review and machine-checked formal verification
are not established here. This review may contain mistakes or omissions.
See the [evidence limits](CODE_INTERFACE_AUDIT.md#evidence-limits).

Date:23 October2026. This note concerns the actual B3/B4 n25
`initial34_indexed.stage` and its `initial25_bB` driver, under the exact
source manifests in [the source map](code_fourier_source_map.json).
Source was read; no signed rectangle or numerical kernel was evaluated.

The finite iteration, original parameter cover, closed probability-panel
export and directions of the selected physical moment contractions below
were checked. This is not independent verification of every scalar/Fourier
coefficient or every EMPTY reason in the entire INITIAL engine. In particular
its quantitative moment envelopes and acquired global support remain inputs
to be matched to their exact analytic rules.

## Original parameter domain and counts

The driver fixes actual n25, a literal rho branch, acquired support radius,
own-score cap and grid[24,24,8,4]. `stage` covers rho, signed beta, signed
third moment and the common first moment. Each step subdivides a complete
closed interval into adjacent closed cells; degenerate endpoints survive.
Early exits account for the entire number of omitted inner cells, not a
sampled subset. `active+excluded=nr*nb*ng*nm=18,432` is checked. This
cardinality check is necessary but does not independently prove each
exclusion predicate sound.

The same original witness is restricted to the literal rho branch; this is
not attainment inside that branch. The support and predecessor/contact
premises enter through `fixed_support` before higher moment/Fourier use.
`c0=.4095+K/nmax` is only a lower bound for the actual contrary score;
the current literal profile has K=0 and n=nmax=25.

## Selected physical moment constraints

Write `beta=EX|X|`, `gamma=EX^3`, `rho=E|X|^3`,
`m=EX_+=EX_-`, and `a_plus/minus=(1+/-beta)/2`.
For the two sign classes, `b_plus/minus=(rho+/-gamma)/2`.
The source's interval versions retain all original signs.

- Signed Cauchy gives `m^2<=p*a_plus`,
  `m^2<=(1-p)*a_minus` and `m^2<=p*(1-p)`.
  The p-local upper bounds use upper p/beta endpoints and upward roots,
  including a v maximum at1/2 when appropriate.
- Cauchy on each positive sign magnitude gives
  `m>=a_plus^2/b_plus` and `m>=a_minus^2/b_minus`.
  The code uses nonnegative lower a endpoints and positive upper b endpoints.
  It excludes a nonpositive b upper endpoint only when the positive a
  moment makes it impossible. It also retains the lower bound
  `(1+beta_min_abs^2)/(2*rho_upper)`.
- With class support bound R, the sign-support deficit
  `Delta_s=E[T^2*(R-T)]` is nonnegative; it is distinct from physical defect D. Cauchy applied to
  `E[T*(R-T)]` gives the correction
  `mu4_sign <= R*b_sign-(R*a_sign-b_sign)^2/(R*m-a_sign)`
  when the denominator is positive. The source uses a nonnegative lower
  numerator and upper denominator to subtract a weaker correction. A zero
  denominator with a strictly positive numerator is a contradiction;
  a zero/zero optional correction is omitted.
- The analogous class-probability bound follows by Cauchy on
  `E[T*(R-T)]` and `E[R-T]`:
  `P(class)>=m/R+(R*m-a_sign)_+^2/(R*Delta_s)`.
  Replacing a by an upper bound and Delta_s by an upper bound weakens this lower
  bound in the coded direction. Summing both classes gives `fmean(m)<=1`.
  `fmean` is increasing on m>=0; its32-step bisection retains the upper
  side, then rounds outward before subdividing. No numerical equality
  root or assumed support saturation is used.

The signed gamma, projection/Pearson, fifth-moment, negative-gap and phase
coefficient rules used in other lines retain their own analytic obligations.
Reading these selected constraints is not a blanket approval of every
expression in `stage`.

## Continuous score, thresholds and finite feedback

The stage maximizes its score/budget expressions over the two C endpoints
and an interior `.40974+K/n` split when present. The split is required by
the charge `max(K,n*(C-.40974))`; on each piece the charge is affine.
The positive phase curvature and squared-linear/curvature terms need their
stated convexity/positivity premises. Full signed phase extrema and Fourier
coefficients remain separate source-to-rule checks.

The exported H root uses a nonnegative upper constant in its discriminant;
replacing a possibly negative constant by its positive part only weakens
the upper root of the downward quadratic. It does not silently omit an
H tail. Acquiring that original quadratic still requires the corresponding
same-law phase/Fourier argument.

`calculate` starts with raw=d=None. Each of12 complete stages obtains new
upper bounds by upward rounding plus a positive rational buffer, then
intersects them with earlier valid upper bounds. This is finite induction
on simultaneous invariants, not a fixed-point limit. A separate thirteenth
complete cover exports the final panel table. Acceptance recomputes the
entire object, compares it type-sensitively and retains all12 original
corruption controls. Saved partial progress alone cannot replace that replay.
The first Gaussian weight-removal license also consumes a valid raw enclosure
and the checked raw<2n/5 bound; a finite iteration count alone does not supply it.

## Complete closed p export

For an acquired p interval[l,u], the panel `[j/100,(j+1)/100]` intersects
it exactly when `j<=100*u` and `j>=100*l-1`. The selected loop therefore
uses `max(0,ceil(100*l)-1)` through `min(99,floor(100*u))`, inclusive,
and repeats the exact intersection test. Endpoint-only intersections stay.

For each intersecting panel, upper resources use a maximum over all
contributing rectangles; lower resources use a minimum. The fields are
necessary enclosures for whichever original witness has p in that panel,
not jointly attainable coordinates of a newly chosen extremizer. The
table retains all100 panels. Zero contributing cells has its explicit
exclusion interpretation in the subsequent resource driver; sentinel
upper/lower values are not an acquired nonempty contract.

The exported theta upper is `max(0,1-m_lower^2/v_upper)`, from
`theta=1-m^2/[p(1-p)]`. Its direction and the probability-panel seam rule
match the later [resource-to-contract mapper](code_n25_join_audit.md).

No numerical acceptance, full support acquisition, complete INITIAL rule
review or all-index theorem is asserted by this bounded source readback.
