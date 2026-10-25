# Complete HIGH: WINDOW50 and supported compensated power

This document fixes the mathematical statements implemented by
[`BEMap/HighFamilies.lean`](../../BEMap/HighFamilies.lean). The analytic
inequalities and their uniformity are accepted theorem parameters. No full
Lean port of their calculus, product-measure proof or numerical evaluator is
claimed here. The contract specifies their exact frozen data, same-law
premises, complete expressions, applicability gates and output units.

Both families bound the **same actual compensated remainder**

```
V_n(t)=f_P(t)^n-exp(-n*t²/2)*(1-i*n*gamma*t³/6),
I_infinity=integral_[1/2,infinity) |V_n(t)|*t^-3 dt.
```

This is `highIntegral w halfFrequencySplit`, at the fixed split1/2, for the
law and actual n of the contact w. The bound is independent of the threshold,
but that does not permit substitution of another law, moment scope or index.
The full families return sqrt(n)*I_infinity bounds. `HighBound.value` instead
bounds the **unscaled** integral. The adapters make that conversion explicit.

## 1. Frozen WINDOW50 numerical data

`Window50Parameters` contains only rational numbers and finite choices:

| Field | Meaning and mandatory gate |
|---|---|
| `fourth` M | An acquired upper on E X⁴, M>=1 |
| `eventMass` a | Positive lower bound on the actual product-event probability, a<=1 |
| `distanceLower` d0 | Positive lower bound on abs(X-X') on the event |
| `eventSecond` M_E | Nonnegative upper on E[(X-X')² given E] |
| `radius` r | Window radius0<r<=1/4 |
| `gamma` g | A nonnegative separately licensed bound on the absolute signed third moment abs(E X³) |
| `gammaChoice` | Pearson sqrt(M-1), licensed g, or their minimum |
| `refinedFirst` | False uses the simple first term; true additionally requires s>0 |
| `refinedZero` | False uses the simple zero-cell term; true permits its minimum with Laguerre2 |

The number b is fixed to9/10. It is not the split of the final HIGH integral.
The exact rational auxiliary values are

```
h=333/106-(22/7)^3*r²/6 >0,
kappa=a*(23/48)²*d0²,
c=(1-max_{u in{1/4,81/100}}(1-u+(M+3)u²/12))/2 >0,
c0=1/8-(M+3)/384,
s=(1-(M+3)*53/600)/2.
```

These are `windowH`, `windowKappa`, `windowC`, `windowC0`, `windowSlope`.
The window theorem's c and its slope s are different quantities. s is not the
residual variance denoted s in COUNT. Their scopes are kept in separate types.

## 2. Actual event semantics: no artificial kernel

`Window50LawEvidence X parameters` is semantic evidence concerning one actual
standardized marginal. Its event is a measurable subset of R×R under

```
productLaw X = P_X × P_X.
```

It requires all of the following:

* Integrability of x⁴ under P_X and E X⁴<=M. A totalized integral alone does
  not establish the fourth-moment hypothesis.
* A bound on actual abs(gamma) by the selected `gammaEnvelope`.
* A measurable actual event E with (P_X×P_X)(E)>=a>0.
* d0<=abs(x-x') almost everywhere under the product measure restricted to E.
* Integrability of (x-x')² on E and
  `integral_E (x-x')² d(P_X×P_X) / (P_X×P_X)(E) <= M_E`.

`event_mass_positive` derives strict positivity of the normalization from
the supplied positive a. Thus a zero-probability event cannot be accepted
through totalized division. Atoms and discrete marginals are not excluded.

The event is a proof witness, not a numerical job input that asks a worker to
evaluate an unknown probability law. The numerical worker receives M,a,d0,
M_E,r and the choices; the accepted analytic/resource argument must license
those numbers uniformly for every law in the job's mathematical scope.

### 2.1. Source event recipes and their acquisition gates

The following are the three actual-event choices in
`rescore:fourier-events`. They are accepted analytic acquisitions of
`Window50LawEvidence`, rather than further production algorithms or new
arbitrary choices of a,d0,M_E.

1. **Fourth-moment recipe.** For the actual event
   `E={(x,x'):(x-x')²>=9/25}`, take
   `a=(2-9/25)²/(2M+6)`, d0=3/5 and M_E=2/a. Its hypotheses are the actual
   standardized law and acquired fourth-moment integrability and bound M.
   The source uses E[(X-X')²;E]>=2-9/25 and
   E[(X-X')⁴]=2*mu4+6 in the Cauchy bound.
2. **Small-defect sign-event recipe.** For the actual event E={XX'<0},
   `rescore:entry201-event` requires actual support abs(X)<=R<=6,
   rho<=37/20 and 0<=D<=d<2. With sigma=sqrt(10), define

   ```
   rStar=min(37/20,(3+d)/(sigma-1)),
   W=sqrt(37*d/10), cStar=sqrt(sigma+1), eStar=sqrt(sigma-1),
   CStar=cStar+eStar,
   hStar=CStar*sqrt(12+W²)/6+W/(3*CStar),
   LStar=max(hStar,((2*cStar-eStar)*hStar+3*W)/CStar).
   ```

   Its conclusions are rho<=rStar, A+B<=hStar and abs(2B-A)<=LStar.
   For the moment acquisition, additionally check alphaStar=LStar/6<=3;
   then

   ```
   abs(J1)<=alphaStar*(rho+1)+(3-alphaStar)*d/2,
   mu4<=hStar*rho+R*d/2,
   eta5<=hStar²*rho+R²*d/2.
   ```

   The event data are a=1/(2*rStar²), d0=sqrt(2-d),
   M_E=2/a=4*rStar². The selected event table uses the stronger d<=4/5;
   that gate belongs to the selected recipe even though the generic lemma
   is stated for d<2. For use of the selected table, check its moment
   acquisitions and the explicitly stated stronger alphaStar<3 gate;
   the generic lemma above itself permits alphaStar=3.
3. **Acquired-probability and gap recipe.** For the same actual event
   E={XX'<0}, assume 0<l<=p<=u<1, D<=d<2, and acquired actual central-gap
   endpoint lower bounds A>=A_l and B>=B_l. Take
   a=2*min(l*(1-l),u*(1-u)),
   d0=max(A_l+B_l,sqrt(2-d)), M_E=2/a. The defect gate licenses the genuine
   central gap and the equality P(XX'<0)=2*p*(1-p), including the absence
   of a zero atom needed for that equality. It is not a blanket assumption
   on all standardized laws. A probability cell crossing1/2 is allowed:
   the minimum of the endpoint products remains the lower bound.

The numerical fields remain rational. Outward acquisition rounds a and d0
downward and M_E and M upward while preserving their strict positivity
gates. For example, choose a rational rQ>=rStar and use
a=1/(2*rQ²), M_E=4*rQ² and a positive rational d0<=sqrt(2-d). Every such
rounded packet must still satisfy all `Window50Parameters` gates and the
actual-event evidence. A frequency-only rate or an invented distance
density does not supply `Window50LawEvidence`.

## 3. The exact complete six-term bound

Write

```
L(x)=(x+2)/(x²+4x+2),
S3=sum_(j=1)^20 j^-3 + 1/800,
S5=sum_(j=1)^20 (j-r)^-5 + 1/[4(20-r)^4],
x=n*kappa*b²,
g_eff=the explicitly selected and licensed gammaEnvelope.
```

The complete expression `window50ScaledUpper n parameters` is the sum of
the following **six** terms:

```
1. A_n,
2. M_E/[4*pi^(3/2)*h*sqrt(a)] * (S3+3*S5/[n*a*h²]),
3. M_E*sqrt(n)/(2*pi²) * exp(-n*a*h²*r²),
4. Z_n,
5. sqrt(n)/(2*b²) * exp(-n*a*(23/48)²),
6. sqrt(n)*exp(-n/8)*(2*L(n/8)+g_eff/3).
```

The default first term is `2*sqrt(n)*exp(-n*c)`. With s>0 it may be replaced
by the minimum of itself and

```
2*sqrt(n)*exp(-n*c0)*L(n*s/4).
```

The default zero-cell term is

```
exp(-x)/(2*b^4*kappa*sqrt(n)).
```

The pointwise refined option takes its minimum with

```
sqrt(n)*exp(-x)/(2*b²)*L(x).
```

At a single actual index this Laguerre option needs no uniform-floor
monotonicity gate beyond its positive arguments. Its additional gate is
required only when the expression is reused at a common floor.

The last comparator term covers its **entire** frequency halfline. It is not
discarded after bounding the characteristic-function part or the nonzero
event windows. The exact pi^(3/2) factor is represented as pi*sqrt(pi).

`Window50Theorem` states, for actual n>=5 and actual-event law evidence,
integrability on(1/2,infinity) and

```
sqrt(n)*highIntegral(w,1/2) <= window50ScaledUpper(n,parameters).
```

## 4. Uniform reuse at a common index floor

`Window50UniformInputs parameters` freezes a lower index N>=5 and checks

```
2*N*c' >1 for c' in{c, a*h²*r², a*(23/48)², 1/8}.
```

There are two **separate extra** gates:

* If `refinedFirst=true`, require2*N*c0>1 in addition to the pointwise s>0.
* If `refinedZero=true`, require N*kappa*b²>=1/4.

If an extra gate is unavailable, the corresponding parameter flag must be
false and the simpler complete expression retained. Failure of a refinement
gate is not an exclusion of the law. It does not authorize silently using
the refined term anyway.

`Window50UniformTheorem` states the exact scalar monotonicity

```
U(n)<=U(N) for every n>=N,
```

where U is that same six-term expression with those frozen parameters and
choices. This is a theorem about bounding expressions, so the marginal law
and its event may vary with n. No fixed-law limit or monotonicity of C_n is
assumed.

`window50_uniform_scaled` preserves the exact source strength

```
sqrt(actual n)*I_infinity(actual n) <= U(N).
```

The unscaled adapter `window50_uniform_high` uses
`ScaledHighRounding actual_n U(N)`, namely U(N)<=sqrt(actual n)*q. It returns
I_infinity(actual n)<=q and retains the sqrt(N)/sqrt(actual n) decay. It does
not silently weaken this to rounding by sqrt(N) alone.

The uniform theorem concerns the unmodified expressions. Clipping an
exponential, replacing a rate by a sampled rate, or retaining only favorable
terms requires a different proved implication; it is not a numerical
optimization licensed by the current uniformity theorem.

## 5. Supported compensated-power data and scope

`SupportedPowerParameters` freezes rational R,r,M4,M5,G,T with

```
R>0, r>0, M4>=0, M5>=0, G>=0, 1/2<T<pi.
```

The actual law evidence supplies

```
abs(X)<=R almost surely, rho<=r,
E X^4<=M4, E abs(X)^5<=M5, gamma²<=G,
```

together with explicit fourth/fifth integrability. The support is an acquired
hypothesis. This theorem does not acquire it, and requires no physical gap,
predecessor allowance or attained-contact identity.

`SupportedPowerPartition` is one finite **strict** rational sequence

```
1/2=t0<t1<...<ts=T, s>=1.
```

Every adjacent closed cell participates. For each cell j, the frozen table
has m_j>=0 and U_j>=0. `SupportedPowerLawEvidence.modulus` requires
`abs(characteristic(X,u))<=m_j` on that entire cell. The numerical
`SupportedPowerCells.whole_cell` requires U_j to bound the exact scalar
minimum below on the entire cell. Neither condition is midpoint sampling.

Any whole-cell modulus enclosure is allowed if it proves that exact
same-law inequality. There is no artificial Gaussian-frequency kernel in
place of the actual characteristic function.

## 6. Exact compensated-power and triangle expressions

For u in the finite cells, define

```
g=exp(-u²/2), b=sqrt(G)*u³/6, W=g*sqrt(1+b²),
d0=cos(u)-g, d1=d0+(r-1)*u³/6,
A=max(abs(d0),abs(d1)),
B=min(M4*u^4/24,M5*u^5/120)+b*(1-g),
Rf=sqrt(A²+B²),
C_n(u)=Rf*sum_(j=0)^(n-1) m_j^j*W^(n-1-j)
       +g^n*n*(n-1)*b²/2*(1+b²)^((n-2)/2),
T_n(u)=m_j^n+g^n*sqrt(1+n²*b²).
```

Here m_j denotes the fixed modulus cap of the current frequency cell; the
finite summation's exponent index is independent of that cell index. The
code names are `compensatedPower` and `trianglePower`.

The required scalar certificate is

```
min(C_n(u),T_n(u)) <= U_j for every u in[t_(j-1),t_j].
```

The finite telescoping sum uses no division by W-m and requires neither
W<=1 nor distinct roots. The real power exponent is(n-2)/2, with actual n>=2.
A valid interval or derivative enclosure may be used to prove the whole-cell
statement, but a sample of u values is not sufficient.

## 7. Complete infinite tail and integral weight

Each cell has the exact positive integration weight

```
integral_[a,b] u^-3 du=(a^-2-b^-2)/2.
```

Shared frequency endpoints have Lebesgue measure zero, even when the
underlying probability law has atoms. Their whole-cell enclosures still
include the endpoints.

The complete tail beyond T is

```
1/(2*T²)
+ exp(-n*T²/2)/(n*T)*(T^-3+n*sqrt(G)/6).
```

The first term is the characteristic contribution; the second is the
Gaussian comparator. Both are retained. `supportedPowerScaledUpper` is
sqrt(n) times the sum of all weighted finite-cell U_j and both tail terms.

`SupportedPowerTheorem` supplies integrability and that complete bound for
actual n>=2. `supported_power_high` uses explicit outward rounding to the
unscaled `HighBound w halfFrequencySplit`.

## 8. Rounding, alternatives and trust boundary

`ScaledHighRounding n expression` requires a rational q>=0 with

```
expression <= sqrt(actual n)*q.
```

Its q is the unscaled integral bound. A scalar Gaussian-tail certificate
from `FourierFamilies.laguerre2_gaussian_tail` cannot fill this type for an
actual complete HIGH without the other required contributions.

`min_complete_high` combines two complete HIGH bounds for the same contact,
actual index and half split. Repeated application permits a fixed finite
collection of licensed windows and/or the supported-power alternative.
Each input must have its own actual law evidence and all its own gates.

This is distinct from taking coordinatewise minima of LOW triples or
splicing favorable frequency pieces from different incomplete strategies.
Any such splice requires its own exact integral/cover theorem.

Numerical series/enclosure algorithms, floating-point acceleration and
production evaluator code remain implementation work. They must prove the
fixed scalar rounding and whole-cell statements above. The accepted
analytic theorem parameters do not imply that a historical numerical run
has passed or that its source/context bindings are correct.

## 9. Source pin

The source is the manuscript `berry_esseen_manuscript.tex`, SHA-256
`2b5c9419a5fc2363de21e02e200529b735c52e492f0d398aca6f42650c65eea1`:

* HIGH_LAGUERRE2 and complete high-frequency setup, approximately2055--2134.
* HIGH_WINDOW50, all six terms, actual event semantics and uniform gates,
  approximately2135--2280.
* `rescore:lem:compensated-high` and `rescore:eq:compensated-high`,
  approximately2282--2378.
* `rescore:entry201-event` / `rescore:mom-third`, the generic small-defect
  event and its moment acquisitions, approximately3229--3251.

The named accepted statements are `Window50Theorem`,
`Window50UniformTheorem` and `SupportedPowerTheorem`. Their exact Lean
signatures, actual-event evidence and symbolic formulas are part of this
contract. This closes the complete-HIGH **mathematical specification** for
these two source families; it does not claim a formal port of their analysis
or a completed production arithmetic evaluator.
