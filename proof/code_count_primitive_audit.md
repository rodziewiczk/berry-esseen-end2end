# Selected count primitive code-to-rule audit

**Review status:** AI-generated internal source review. Cross-reads by
other model agents are internal checks by the same AI system. External
independent mathematical review and machine-checked formal verification
are not established here. This review may contain mistakes or omissions.
See the [evidence limits](CODE_INTERFACE_AUDIT.md#evidence-limits).

Date:23 October2026. Static algebra and source readback only; no archived
module or mathematical evaluator was run. The
[source map](code_count_primitive_source_map.json) checks all75 retained
B0--B2 capsules against their exact source-row hashes in catalog SHA256
`f055b5017d4e1fd14f2b48a6a95fef4a4c61a025dea6174c424cd5968de801f7`.
All75 use the same three files below; the selected function/class ASTs
also match the inspected portable p31 source.

| File | Actual SHA256 | Selected rules |
|---|---|---|
| `finite_gaussian.py` | `4f5b1a829df4c3c8c0e5467adb79f112984ee8eab8ba5f25b20fd7173b78a4a0` | Root, Machin constants, integrated Gaussian remainder and reflection |
| `exact_count_core_v5.py` | `0ffba7a5e1a91fc3c3c770f9d3bcb073a529fade3d622bc5615567153a4255a0` | Directed arithmetic, interval operations, exponentials, normal lower, binomial masses |
| `interval_scalar_fast.py` | `3eaa0d78eec8b8d5c2044eb020a406ec352ac5a99b30f9d2773694a4f9601512` | Exact scalar specialization of interval multiplication/addition |

The Gaussian module's entire AST outside the legacy `panel` function is
identical, including constants and import-time scalar checks, to the already
[reviewed parent Gaussian source](code_fourier_primitive_audit.md), SHA256
`939236711b080f9148ee3d3f7f6a0cd15b86cb24f3d2700f0e7127b2a345291f`.
The count copy disables that legacy panel entry point with an unconditional
exception; it does not substitute a partial old binomial table for a complete
count forest. Its actual positive CDF and root rules retain the reviewed
directed Taylor/Machin argument.

## Exact intervals and scalar optimization

`I.__add__/__neg__/__mul__` implement endpoint sums, reversed negation and
the extrema of all four products. Division first requires a strictly positive
denominator interval and multiplies by its reversed reciprocal endpoints.
An odd nonnegative integer power is monotone; an even power includes zero
exactly when the interval crosses zero. These are complete rational interval
enclosures, not sampled values.

`interval_scalar_fast` delegates a non-point interval multiplier to the
original four-corner method. For a scalar>=0 it keeps endpoint order; for
a negative scalar it reverses the endpoints. Its scalar addition translates
both endpoints. `__rmul__`/`__radd__` use the same commutative operations.
This specialization preserves exact endpoints under the sealed Fraction
runtime; it does not change the mathematical interval interpretation.

`up/down` use ceilings/floors on scale10^12, correctly for negative rational
values as well as positive ones. The containing original loaders reject
optimized Python so the Gaussian module's scalar assertions remain enabled.

## Exponential bounds, lines35--42

For x>=0 the positive partial series through degree48 is a lower bound for
exp(x). Downward rounding weakens that lower bound. For0<=x<50,
the omitted first term is x^49/49! and every subsequent ratio is at most
x/50<1. Hence

`exp(x) <= sum(x^i/i!,i=0..48)+(x^49/49!)/(1-x/50)`.

The upper primitive rounds this expression upward. The strict x<50 gate
and positivity gates are retained. A caller outside that domain is rejected;
this review does not silently extend the primitive. Later use of a
reciprocal must still respect the corresponding lower/upper direction.

## Normal lower bound, lines44--48

For den>0, let a<=sqrt(den)<=b be the directed positive root endpoints.
If num>=0, `num/b<=num/sqrt(den)`; flooring its argument to the Gaussian
grid and taking the CDF lower endpoint is therefore a valid lower bound.
If num<0, the positive magnitude `-num/a` bounds the exact magnitude above.
Ceiling it to the grid, taking the positive CDF upper and subtracting from1
again yields a lower bound. These directions retain the sign crossing and
num=0. The compact |z|<=5 grid gate remains explicit. A zero lower root
in a divisor would reject, not establish a false probability estimate.

## Whole-p binomial mass bounds, lines50--58

For0<pl<=p<=pu<1, each binomial mass
`b_j(p)=choose(n,j)*p^j*(1-p)^(n-j)` is positive and increases up to
p=j/n, then decreases. Its minimum on the closed interval is therefore
the smaller of its two endpoint values; its maximum is the larger endpoint
or the mode j/n when that mode lies in the interval. This includes j=0,n,
where the maximum is at an endpoint. The returned cumulative value is the
exact CDF at pl. The physical binomial CDF decreases with p, so it may be
used as the appropriate upper endpoint, with the jump-side convention
required by the caller.

In particular every returned lower own mass is nonnegative. This supplies
the explicit multiplication premise of [R1](logic_audit_repairs.md) for
these75 selected copies. It does not prove every caller's other
probability/score normalization or every distinct count engine.

## Remaining boundary

This review establishes the stated primitive interfaces under their exact
argument domains. Complete Gaussian/incoming derivative cancellation,
CGF/stop-loss/own-buffer strategy selection, outward algebra in other modules,
physical contract acquisition, full original roots and fresh arithmetic
acceptance remain the responsibilities of their named callers and audits.
No parent, full n25 or all-index flag is closed here.
