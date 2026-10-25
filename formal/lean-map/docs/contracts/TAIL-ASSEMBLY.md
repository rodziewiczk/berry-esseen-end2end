# Independent49+ tail: typed local comparison and resource barriers

`BEMap/TailAssembly.lean` constructs the scalar `TailContracts` consumed by
the checked first-failure argument in `Tail.lean`. Its public input is
`TailMethodProviders`, and `.contracts` constructs every scalar field.
`independent_tail_from_methods` consequently proves the conditional upper
bound for every actual integer n>=49.

The inputs include neither `FiniteContracts` nor sharp results for1..48.
The tail has its own auxiliary **excess** ceilings, obtained from separate
supported resource calculations at40..50. Those auxiliary estimates are not
the finite proof's sharp C_n<=C_E results.

## 1. Scalar symbols, owner and units

Throughout the tail,

```
C_n=optimalConstant n, a_n=C_n-C_E,
delta_n=n*max(C_(n-1)-C_n,0),
q_actual=n*max(R_(n-1)(X)-C_n,0),
s=E U^2, lambda=n*s, theta=s/(p*(1-p)+s).
```

Each n may have a different maximizing law. For a particular owner
`w : ContraryContact n`, `w.optimal` identifies its score with C_n. The
deleted sums use this **same marginal law**. The checked
`same_law_predecessor_drop` proves `q_actual<=delta_n` using the all-law
optimal-constant bound. `same_law_deleted_caps` similarly supplies the
same law's n-1 and n-2 score caps. No contact or optimality is created at
either deleted index.

Raw H is `sqrt(n)*z` from the original normalized contact. All binomial
counts, phases, moment weights, Fourier powers and probability laws use
the actual n. A calculation floor N licenses specified uniform coefficients
and weighted exports `nD<N*d`; it does not replace actual n by N in lambda,
threshold normalization or convolution powers.

## 2. Closed extraction is an explicit analytic input

The scalar local contract permits a_n=0. Auxiliary barrier failures also
permit `C_n=C_E+K/n`. Strict-only extraction is insufficient for either
interface. `TailMethodProviders.extraction` therefore supplies

```
ClosedIndexExtraction n C_E      for actual n>=40
```

at the only required extraction floor. An auxiliary failure at the higher
barrier C_E+K/n also implies C_n>=C_E, so the same port suffices. No arbitrary
floor extraction or index1 premise is required. The accepted attained-maximum
source statement at manuscript368--398 explicitly includes C_n=C_E and
retains an attained positive closed maximum after orientation. Extraction
does not assume the law has finitely many atoms.

When the scalar local hypotheses hold, `.contracts.local_exclusion` extracts
the actual owner at floor C_E, rewrites the own-score hypotheses through
`w.optimal`, and calls the derived `UniformLocalProvider.reject`. Its result
is not supplied as a primitive scalar `False` field.

## 3. The uniform local input is a numerical comparison construction

The exact local entry hypotheses are

```
n>=47,
0<=a_n<=.7/n, delta_n<=.19,
C_n<.4247, C_(n-1)<.4253, C_(n-2)<.4253.
```

The provider in [UNIFORM-TAIL.md](UNIFORM-TAIL.md) acquires the actual
all-threshold support3.84, the83 closed probability panels covering
[.304,.47], their same-law moments/signed thresholds/conditional supports
and their coupled weighted resources. Its acquisition license contains
**analytic plus numerical resource/enclosure/confinement evidence**. The
concrete panel caps do not follow from an analytic theorem or metadata alone.

For the uniform support acquisition the source index bands are

```
[45,49], [50,59], [60,89], [90,134], [135,199], [200,infinity).
```

Only actual n>=47 are used. Every row checks both signs, the closed radial
cells of width.05 through4.5 and both complete exterior rays. The final
infinite index band uses its zero adverse endpoint; omitting it would leave
the tail uncovered. A finite P46 row ending at98 is not this uniform license.

The local certificate covers all positive noise regimes, including
arbitrarily small positive lambda and both threshold signs. At an actual
nearest integer count, it proves

```
rho_B*(C-C_B_positive_closed)<-lambda/1000.
```

The actual Bernoulli comparison score is strictly below C_E by the accepted
published all-parameter theorem. Since rho_B>0 and C>=C_E, the comparison
inequality is contradictory. For lambda=0, the exact conditional residuals
vanish and the law is Bernoulli; the whole-score Bernoulli theorem applies
directly. That branch divides by neither lambda nor a noise-dependent
quantity. These are the two branches of the checked `.reject` proof.

## 4. Five independent auxiliary support/resource rows

`TailAuxiliaryRow` freezes the original wider certificate scopes:

| Row | Actual indices | Support radius R | Own-score cap | Barrier n*a_n>=K | Support drop cap q | Resource passes |
|---|---|---|---|---|---|---|
| A40 |40 |3.3 |.469 |1.5 |.88 |5,64 closed cells each |
| P41 |41..49 |2.9 |.469 |1.5 |1.5/40 |6,64 cells each |
| A45 |45 |3.5 |.4431 |.7 |.8341 |12,18432 cells each |
| P46 |46..98 |3.5 |.432 |.7 |.7/45 |13,18432 cells each |
| A46 |46 |3.4 |.42496 |.54 |79/450 |4 signed passes of18432 cells, then3 probability passes of96 cells |

The scalar auxiliary argument uses P41 only through45 and P46 only through50.
The wider upper endpoints are retained as certificate scopes, not promoted
to an infinite uniform theorem.

`AuxiliarySupportImplication` is separate from the resource exclusion.
It consumes the original K/drop/index hypotheses and licenses the entire
actual support, including possible exterior atoms and accumulation points.
Only then can `BarrierScope` be supplied to the supported resource job.
The support implication's numeric radial/ray inequalities remain licensed
evidence, not a consequence of Fourier integration.

`BarrierResourceJob` fixes every finite pass, its complete closed
moment/mean/raw-H cells, source identity and strict target caps. Its checker
has the fixed meaning `BarrierResourceMeaning`:

* the same original supported contact has a `PhysicalState`, including
  actual moments, contact, gap summability/nonnegativity, coherent complete
  LOW/HIGH and conserved identity;
* every actual owner remains in at least one original closed cell at each
  pass, before a necessary-condition exclusion is used;
* a pass consumes only the immediately preceding accepted strict raw and
  weighted-defect exports, plus the original scope;
* each cell supplies a licensed general resource output or a paired
  coefficient/envelope output with the explicit rounding described below.

The result is `BarrierExport w N r d`:

```
rawRemainder(w)<r, actual_n*D(X)<N*d.
```

These are resource outputs, not closed-CDF score leaves. The final d is
strictly negative. `barrier_resource_reject` composes the finite passes and
contradicts D>=0. It never constructs a `ResourceState` with a negative
live defect cap: the terminal contradiction is a separate output type.

## 5. A46 warm start, phase correction and paired portfolio

Before weight removal, a prior strict raw bound must satisfy

```
rawRemainder<r<.4*n,
phi_minus=(997/2500)*(1-5*r/(2*n)),
n*a_n*rho+(997/15000)*n*D<=B(H).
```

`BarrierBudgetEvidence` carries this exact license and the actual density
floor. The first A46 raw result is below18.4 before any defect result is
used. Subsequent passes consume their accepted predecessors.

The extra coherent curvature is

```
e_rho=(1-5*r/(2*n))/2*(.4095*rho-d/15)>0.
```

On the barrier branch, K*rho is subtracted **only** in the resource bound.
The next stage's raw remainder bound retains the original raw quantity.

`PairedBarrierGates` requires

```
0<l<u<1/2, 1<=M<=2, 0<=g<=1, R>2*g,
3*min(innerMinus,innerPlus)>=1.5*max_(p in[l,u])rho_B(p),
paired absolute-skewness lower endpoint>=0.
```

The LOW data additionally freeze the entire actual coefficient rectangle
for `a=(3-mu4)/24`, `z=(10*gamma-E X^5)/120`, `c=a*gamma/6`, sixth-moment
and |a|/|z| bounds, the positive damping and the outward I/F/J coefficients.
`BarrierPairedLowData` defines the source complete triple L0,LH,L2 exactly.
Its Gaussian rectangle price is

```
U(z,c)=I*(|z|+3|c|)                                  if z*c<=0,
U(z,c)=I*abs(|z|-3|c|)+6*sqrt(abs(z*c))*exp(-|z|/(2*|c|)) otherwise.
```

All four rectangle corners are bounded before constructing the triple;
the source integral is convex. The source ordering gates include
`I>=sqrt(pi/2)`, `F>=(N/(N-1))^(3/2)` and the admissible positive damping.
`PairedEnvelopeMeaning` binds the actual moments/rectangle, integrability,
the complete coherent LOW price and the complete infinite HIGH bound to
the same owner. Reflection of the auxiliary Fourier integral does not
change the actual signed contact or its phase.

The signed phase repair is

```
eps_gamma=(.4-phi_minus)/2*max(d-.16,0),
q_tilde=q-eps_gamma>0.
```

The packet retains all four score/rho corners, with C at.4095/.42496 and
rho at rho_B(u)/rho_upper. The latter lower corner is a defined real radical,
not a falsely exact rational input. Positive corrected divisors and positive
extra curvature are mandatory. At fixed H, take the complete corner maximum
first. Then square completion gives

```
R_pair=max_corners(A+f^2/(4*q_tilde)),
B_pair=max_corners(A+f^2/(4*(q_tilde+e_rho))-K*rho).
```

`PairedEnvelopeMeaning` states weak whole-cell source coefficient upper
bounds for actual raw remainder and resource. The numerical outward
comparisons are strict: `maxRaw<rOut` and
`maxResource<(997/15000)*N*dOut`. Thus strictness is supplied by the verified
finite arithmetic, rather than invented in the analytic corner envelope.
`paired_envelope_export` derives the weighted resource export in Lean using
`quadratic_square_upper`; a paired packet is therefore consumed by the
pass rather than stored as decorative metadata.

The complete general and complete paired portfolios may be intersected.
Their coefficients may not be mixed coordinate by coordinate. If a paired
premise is unavailable, a valid general enclosure must remain for that cell.

The A46 fixed targets, all strict exact rational bounds, are:

| Pass | Cover | Raw remainder | D |
|---|---|---|---|
|1 |signed |5.8415 |1.6324 |
|2 |signed |2.8322 |.6195 |
|3 |signed |1.8719 |.3550 |
|4 |signed |1.4410 |.2371 |
|5 |probability |.9953 |.1077 |
|6 |probability |.7416 |.0379 |
|7 |probability |.5840 |-.0046 |

The source uses paired bounds on83/95/96 cells in the last three passes.
These counts describe that original numeric job; counts alone do not prove
its per-cell coefficient meanings or arithmetic. The final negative export
is the contradiction with D>=0.

## 6. Auxiliary scalar reduction is a stated analytic premise

`AuxiliaryScalarReduction` is the explicit accepted scalar implication from
the five actual supported exclusions, their separate support licenses,
closed attainment, the published C_n<=.469 bound and support-free smoothing.
Its inputs are not naked auxiliary targets. Its output is exactly

```
a_j<1.5/j for40..45 (intermediate source step),
a_j<.7/j for45..50,
a_46<.54/46.
```

The formal output retains only the last two inequalities needed by
`TailContracts`. This milestone accepts the elementary finite first-failure
reduction as a source theorem; it does not claim its full auxiliary
induction has been ported into Lean. The five resource-job arithmetic
meanings remain separate numerical premises and cannot be inferred from
that analytic reduction.

The source dependency order is A40 -> P41 through45 -> A45 -> P46 through50
-> A46. At a first failure, the previous auxiliary ceiling controls the
drop. Smoothing supplies the own .432 cap for the P46 application. The
A46 support bound uses `46*.7/45-.54=79/450` after the finite .7 ceiling,
and does not depend on its future stronger .54 result.

## 7. Support-free smoothing and the derived .29 bound

`SupportFreeSmoothing` is the exact published/source analytic inequality,
algebraically scaled by n. With `s_n=sqrt(n/(n-1))`,

```
n*C_n<=n*s_n*C_(n-1)+s_n^3*(1/15+.08/sqrt(n-1)).
```

It quantifies unrestricted centered variance-one laws with finite third
absolute moment, every raw threshold, closed CDFs and their left limits
before taking suprema. It uses no support or maximizing-law hypothesis.

`SmoothingIndexBrackets` supplies explicit scalar square-root brackets,
with no C_n conclusion inside them. For n>=50,

```
n*(s_n-1)<=25/49,
scaledRemainder<= (50/49)*(1011/1000)/15
                  +.08*(50/49)*(1011/1000)/7.
```

Together with C_E<=.409733 and C_(n-1)<=C_E, the checked
`smoothing_first_failure` derives

```
n*(C_n-C_E)
 <= .409733*(25/49)+(50/49)*(1011/1000)/15
                     +.08*(50/49)*(1011/1000)/7
 < .29.
```

The final rational comparison is proved by exact arithmetic. The source
square-root/index brackets and smoothing inequality are explicit accepted
analytic inputs; the target .29 conclusion is not an input field.

## 8. Base49 and the actual infinite first failure

The already checked `tail_base49` applies the constructed local exclusion
at49,48,47. A contrary C49>=C_E would force three backward losses,

```
a46>.19*(1/47+1/48+1/49)>.54/46,
```

contradicting the independently acquired A46 ceiling. It uses no sharp
finite theorem at47 or48.

For n>=50, `tail_composition` uses strong induction, equivalent to choosing
the least failure. The previous index is sharp, the drop is zero and the
derived smoothing bound gives `0<=a_n<.29/n<.7/n`. The second predecessor
is sharp too, except at n=50 where its index48 is bounded by the independent
auxiliary .7/48 ceiling. The own/deleted caps then match the typed uniform
local comparison, which rejects the failure.

## 9. Source pins and evidence frontier

The source is the pinned manuscript
`berry_esseen_manuscript.tex`, SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`.
Relevant source ranges are: closed attainment368--398; all-threshold support
rows790--814; support-free smoothing7463--7510; five auxiliary/local
contracts7513--7571; scalar auxiliary/base49/first-failure7574--7649;
A46 resource/paired correction8065--8215; complete local comparison8217--8868.

This module contains a checked conditional assembly and exact fixed meanings
for numerical resource exports. It does not contain populated successful
barrier jobs, accepted entry/confinement receipts, all83 panel data or a
production certificate checker. Source pins and historical target tables
cannot supply these proofs. Accepted analytic implications, licensed
numerical meanings and actually derived composition are separate fields,
so an implementation has a defined mathematical input/output boundary
instead of a hidden scalar impossibility premise.
