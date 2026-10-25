# ROOT4: canonical physical state and exact numerical obligations

This is the source-specific refinement of the small-index contract, not a
restriction to three-point laws. The actual P is an unrestricted standardized
law. The analytic results stated below are accepted theorem inputs in this
skeleton. Their full proofs are not being re-formalized here.

Source: the pinned manuscript, labels `n4all:eq:reference`, `n4all:lem:excess`,
`n4all:lem:owner`, `n4all:lem:common-measure`, `n4all:eq:response-series`,
`n4all:prop:certificate`. The native acceptance boundary is
`be_replay/root4.py:validate_terminal` at the research baseline: a complete
result is accepted with `upper <= TARGET`, not a strict margin below TARGET.

## 1. Target, contrary hypothesis and localization

Set T=4097/10000 and K3=59 sqrt(3)/250. ROOT4 consumes the **quantitative**
all-law bound C3<=K3. Its contrary hypothesis is T<C4. A contact restricted
to scores at least C_E is insufficient when T<C4<C_E.

`ContactAt 4 bound4` therefore has T as a type parameter. Localization returns
one such contact together with `Root4PhysicalClass` for that chosen owner:

* The actual P has acquired support |X|<=17/4. The source owner lemma gives
  the stronger open radius101/25, which safely implies this bound.
* rho(P)<46/25 is strict.
*625/2116<=w<=1 and |beta|<=13/20 are closed necessary geometry bounds.
* Its reference/excess data have the canonical meaning below.

The final bounded-law certificate is weak: actual score<=T. Combined with
the retained strict contrary hypothesis and the contact's global optimality,
this contradicts T<C4. Equality C4=T is **not** excluded.

Lean: [`Root4Provider`, `Root4Provider.upper`](../../BEMap/Root4.lean).
The provider localizer returns `Nonempty (Sigma w, Root4PhysicalClass w)`;
it does not silently demand localization of every unprepared contact.

## 2. Three distinct defects

Write u=E X_+, beta=E[X|X|], and

```
a=(1-beta)/(2u), b=(1+beta)/(2u), w=4u²/(1-beta²),
Q3=(u/a) delta(-a)+(1-w) delta(0)+(u/b) delta(b),
r=rho(Q3)=(1+beta²)/sqrt(w(1-beta²)),
eta=rho(P)-r,
W(x)=x_+(x_+-b)²+x_-(x_--a)².
```

The analytic canonical-reference theorem requires u>0, |beta|<1,
0<w<=1 and proves that Q3 is a centered variance-one probability law,
eta=E W>=0, and eta=0 iff P=Q3. The actual law P remains unrestricted.

These quantities are not interchangeable:

| Name | Definition | Source role |
|---|---|---|
| ROOT4 excess eta | rho(P)-rho(Q3) | Physical fourth-index comparison, allowing a zero atom |
| Matching moment defect | rho-(gamma²+2)/sqrt(gamma²+4) | Earlier two-point stability theory |
| Gap defect D | (3+sqrt(10))rho-gamma-3J | Conserved identity and later resource/count arguments |

Lean defines all three by separate named expressions. In particular,
`Root4CanonicalEvidence` states the exact probability/moment/zero-excess
identities, and `Root4PhysicalClass` does not accept a matching-defect cap
in place of eta.

## 3. The same defect measure at every frequency

When eta>0, define the **single** probability measure nu=W dP/eta. It can be
viewed as a measure on tagged nonzero points: sigma=sign(x), y=|x|,
c_+=b, c_-=a. The tagged version and the real-line version in Lean are the
same weighted law under this identification. Zero and the contacts have zero
nu mass.

```
r_q(sigma,y) = exp(i sigma q .)[0,c_sigma,c_sigma,y],
k0 = 1/(c_sigma² y), k2 = 1/(y-c_sigma)², k1=1/(y-c_sigma).
```

Singular costs are used only off their contacts; the Lean definitions set
their irrelevant nu-null contact values to zero. The analytic theorem proves
integrability and the exact simultaneous identities

```
phi_P(q)-phi_Q3(q) = eta integral r_q dnu,                 for every q,
eta integral k0 dnu = (1-w)-P{0} <=1-w,
eta integral_on_tag k2 dnu = u-c_sigma P{sigma c_sigma} <=u,
integral_on_tag k1 dnu = 0,
|r_q| <= |q|³/6.
```

The same nu appears for all frequencies. Replacing it by a separately
optimized nu_q changes the theorem and loses cancellation. At eta=0 use
P=Q3 directly; no normalized nu is required or inferred at zero excess.

Lean's entire response is defined by its everywhere-convergent series

```
sum_{k>=0} (i sigma q)^(k+3)/(k+3)!
           * sum_{j=0}^k (j+1)c^j y^(k-j).
```

The representation contract explicitly includes summability, integrability
and the common-measure budgets. A totalized divergent integral or sum cannot
serve as an accepted analytic input.

## 4. Frozen numerical geometry and complete domains

The numerical task has fixed rational data and a finite geometry. The unknown
P and nu occur only in the **meaning** of its output; they are not numerical
runtime inputs. The full family must cover all of the following:

*20 equal closed w-bands from625/2116 to1 and13 closed |beta|-bands of width
  1/20 from0 to13/20: exactly260 parents.
* Each parent has its own sufficient large-excess cutoff c_B>=0. A parent
  may be handled directly or by **all four** closed children from bisecting
  both geometry coordinates. Each child has its own cutoff and evidence.
* The large-excess branch covers eta>=c_B. If c_B>0, the low-excess branch
  covers all16 equal closed bins in[0,c_B]. If c_B=0, the large branch
  already covers eta>=0. The shared endpoint is included in both branches.
* N=256 midpoint frequencies u_j=(j+1/2)/N, q_j=3u_j, j=0,...,255.
*58 raw thresholds H_l=-4+l/8, l=0,...,57, their57 complete joins,
  and two exterior threshold tails H<=-4 and H>=25/8.
* Both actual reflected orientations. Reflect the entire marginal and
  threshold; changing only the beta sign or only signed moments is invalid.

`Root4Parent`, `Root4ThresholdJoin`, `Root4ExcessBin` and `Root4Child` provide
the finite index types. `root4_parent_count` checks the260-parent cardinality.
These indices alone are not a proof that a numerical payload covers every
required branch. Its semantic acceptance must establish the complete domain
conclusion of `Root4Provider.certificate_bound`.

A parent is empty from the strict physical rho cap only if its minimum
r² is at least(46/25)². An unresolved guard is not an empty parent. The
historical output's distribution among empty/direct/child portfolio classes
is provenance; coverage and the weak target bound are the acceptance criteria.

## 5. Priced response and coherent alternatives

For fixed H define

```
kappa_j(H)=Khat(u_j) exp(-i q_j H)/N,
A_H(sigma,y)=Re sum_j 4 kappa_j(H) g(q_j)^3 r_(q_j)(sigma,y),
g=phi_Q3.
```

Choose fixed nonnegative prices lambda0,lambda+,lambda- and signed prices
theta+,theta-. A whole tagged-domain supremum

```
S_H >= sup(A_H-lambda0 k0-lambda_sigma k2-theta_sigma k1)
```

implies the linear response upper bound
`eta integral A_H dnu <= (1-w)lambda0+u(lambda++lambda-)+S_H eta`.
S_H and this final expression may be negative. The signed equality prices
must retain their signs. Prices are fixed before the supremum is taken.

The source price sets are

```
lambda0: 0,1/1000,1/400,1/200,1/100,1/50,1/25,2/25,4/25,8/25,16/25;
lambda+,lambda-: 0,1/2000,1/1000,1/400,1/200,1/100,1/50;
theta+,theta-: 0, +/-1/200, +/-1/100, +/-1/50.
```

When lambda_sigma=0 only theta_sigma=0 is allowed. All273 nearest-node
closed y-cells on each tag, clipped to[0,17/4], enter the supremum.
If a cell crosses a contact, both reciprocal rays enter the cost supremum.
The response itself is evaluated through the entire series, not divided
quotients. Its degree60 truncation, factorial remainder and half-cell
derivative reserve are exactly `n4all:eq:response-series`; whole-rectangle
corrections must also cover the actual reference g and c throughout the cell.

For psi=g+delta, the complete fourth-power decomposition is
`psi^4-g^4=4g^3 delta+delta²(psi²+2psi g+3g²)`. The basic disk, lens,
absolute and priced linear-plus-remainder portfolios are complete alternatives.
Taking the best of whole valid alternatives is allowed. Taking minima of
unrelated coefficients is not.

## 6. Quadrature, joins, tails and normalization

There is one midpoint reserve for the **original law**, not separate copies
for the reference, linear transfer and remainder. With x=H/2,

```
D2=x²+1,
D4=x⁴+6x²+2|x| kappaUpper+(M4Upper+9)/4,
Q_H=min(687/(8N²), [42sqrt(D2)+108D2+24sqrt(D2D4)]/(12N²)).
```

The moment caps are the actual whole-cell source bounds

```
|gamma|<=min(rho, |b-a|+eta),
M4<=min((17/4)rho, a²-ab+b²+[(17/4)+2max(a,b)]eta).
```

The single physical threshold-interpolation reserve is
`E_H=h²(B+1/4)/16`, h=1/8, with B the complete source curvature sum over
all frequency cells. It interpolates the smooth physical Prawitz majorant,
**not the discontinuous CDF** and not a minimum selected differently at each
threshold. Both exterior tails have their separate bound at most2/5.

The final normalization uses the actual rho=r+eta. Both denominator faces
are retained when a numerator can be negative. Assemble each complete row
before maximizing over H. Retain the zero-excess case and all closed seams.

## Handoff status

Canonical states, the distinct excess, the common-measure analytic interface,
source domain and weak final composition are specified in Lean. The source
equations and finite numerical obligations above fix the intended physical
portfolio. A production parser/evaluator and its connection to these semantic
proof objects are not implemented at this checkpoint. Their implementation
may not change these constants, domains or acceptance meaning silently.
