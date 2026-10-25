# Distinct Fourier families, exact gates and output units

Accepted analytic theorems are explicit parameters. Their source statements
are fixed here; full Lean proofs of their analytic derivations are outside
this skeleton's scope. Numerical evaluation must establish the stated rational
enclosures over whole cells.

## A. Physical compensated-hinge ledger

For one actual contact w with raw H, actual n and marginal characteristic
function f(t), define

```
V_n(t)=f(t)^n-exp(-nt²/2)(1-i n gamma t³/6),
I_low(b)=integral_0^b |Im(exp(-itH)V_n(t))|/t³ dt,
I_high(b)=integral_b^infinity |V_n(t)|/t³ dt.
```

The positive rational split b is part of the type of **both** results. Their
integrability is required explicitly. The canonical hinge error is defined
from the actual normalized-sum and Gaussian integrals; it is not a free error
variable chosen by a checker. The analytic inversion bound is
`|E_n| <=2sqrt(n)(I_low+I_high)/pi`.

`LowBound w b` contains one coherent triple satisfying
`I_low <=(L0+LH|H|)/sqrt(n)+L2/n`. `HighBound w b` contains an unscaled
upper bound for the **entire** I_high. Every coefficient refers to the same
law, signed moments, frequency split and raw threshold. No componentwise
minimum of different triples is allowed.

Source: `afcore:eq:epsilon`, `afcore:eq:error-ledger`.
Lean: [`Fourier.lean`](../../BEMap/Fourier.lean).

## B. Finite-window LOW constructor

Source: `rescore:lem:finite-low`, `rescore:eq:finite-low-triple`.
Lean: [`FiniteWindowLowInputs`](../../BEMap/FourierFamilies.lean).

The constructor is licensed only at b=1/2 and actual integer n>2, with acquired
support1<=R<=6. Its inputs must prove

```
mu4<=M<=111/10, |gamma|<=g<=37/20, eta5<=E5,
0<=g_l<=|gamma|, g_l²<=M-1,
A>=|(3-mu4)/24|, Z>=|(10gamma-E X^5)/120|.
```

All upper coefficients are nonnegative; eta5 is E|X|^5 whereas EX^5 is signed.
The support token precedes the higher-moment evidence in the types.

Set

```
M6=min(RE5, 1+3g²+g⁴+(R²+2Rg+3g²+2)(M-1-g_l²)),
E=M6/720+g²/72+(1/2+g²/144)^3/5,
B=A+Z/2+E/4,
a_n=(n-1)/2, b_n=(n-2)(45-M)/96,
I_j(A)=integral_0^(1/2) t^j exp(-A t²) dt.

L0=sqrt(n)[nZ I2(a_n)+n(n-1)Ag I4(a_n)/6+n³g³ I6(n/2)/1296],
LH=sqrt(n)[nA I2(a_n)+n²g² I4(n/2)/72],
L2=n[nE I3(a_n)+n(n-1)B² I5(b_n)/2].
```

The three Lean definitions L0,LH,L2 are these exact real expressions. A
`FiniteWindowLowRounding` provides one outward rational enclosure of all
three. The accepted `FiniteWindowLowTheorem` and this rounding construct an
actual `LowBound w halfFrequencySplit`. There is no formula silently freezing
n at a band endpoint or replacing n(n-1) by n².

The restricted rational finite-Gaussian evaluator, if selected, additionally
checks0<=A<=8 and0<=j<=16. Its whole-domain Taylor bounds are

```
P_(m,j)(A)=sum_(k=0)^m (-A)^k/[k!(j+2k+1)2^(j+2k+1)],
max(0,P_(21,j)(A))<=I_j(A)<=P_(20,j)(A).
```

The finite-window theorem does not require that particular evaluator. An
out-of-range call to that evaluator is an unresolved request, not an empty
mathematical cell.

## C. HIGH_LAGUERRE2 is a Gaussian-tail component

For actual n>0, b>0, kappa>0, put x=n kappa b². The source theorem gives

```
sqrt(n) integral_b^infinity exp(-n kappa t²)/t³ dt
 <= sqrt(n) exp(-x)/(2b²) * (x+2)/(x²+4x+2).
```

The corresponding `GaussianTailEvidence` carries all three positive gates
and integrability. The analytic theorem plus a checked rational enclosure of
the displayed upper expression constructs this evidence. Uniform reuse over
n>=N additionally requires N>0 and N kappa b²>=1/4. This extra monotonicity
gate is recorded by `Laguerre2UniformInputs`; pointwise validity is not enough.

This Gaussian-tail component is **not** a `HighBound` for V_n. A complete
HIGH portfolio also covers the actual-law contribution, finite windows and
the normal/compensation terms of its selected source formula. No coercion
from `GaussianTailEvidence` to `HighBound` exists.

## D. Four-term Prawitz smoothing gives a score bound

This is a separate numerical route, used in the supported-Fourier complement
of n5. Source: `afcore:eq:prawitz`, citing Shevtsova2012, Lemma4.1, p262.
Lean: [`Prawitz.lean`](../../BEMap/Prawitz.lean).

With c>0,0<tau<1, n>=1, define

```
Khat(t)=(1-t)+i[(1-t)cot(pi t)+1/pi],
g_n(t)=exp(-n(ct)²/2).
```

The analytic inequality bounds Delta_n by the sum of **four** nonnegative
terms:

```
integral_0^tau |Khat(t)| |f(ct)^n-g_n(t)| dt,
integral_tau^1 |Khat(t)| |f(ct)|^n dt,
integral_0^tau |Khat(t)-i/(pi t)| g_n(t) dt,
integral_tau^infinity g_n(t)/(pi t) dt.
```

Each has its own integrability and whole-integral rational upper bound in
`PrawitzScoreEvidence`. The endpoint pieces and the infinite Gaussian tail
are included, not discarded because the central quadrature succeeded.
The output score uses an upper bound for sqrt(n) and a strictly positive
**lower** bound for rho. A complete numeric comparison yields the weak target
bound; a strict margin is used only when the selected argument establishes it.

Within a finite integration cell, select one entire proved majorant. A
midpoint value needs its source C² reserve, or a separately valid Darboux
upper, on the whole cell. Selecting different favorable formulas only at
sample points does not satisfy the whole-integral contract.

## Implementation rule

The [complete HIGH supplement](HIGH.md) specifies both full source families,
including all WINDOW50 terms, actual product-event recipes and uniformity
gates, and compensated-power cells with their infinite tails. It supplies
the full `HighBound` adapters; the Gaussian component alone does not.

Every numerical family chooses exactly one declared source constructor and
supplies that constructor's inputs and gates. A common semantic output type
allows later composition; it does not license a different numerical formula.
In particular Prawitz score evidence does not require a compensated-hinge
certificate, and a hinge-error bound alone is not a Prawitz score conclusion.
