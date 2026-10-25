# First local execution slice: zero-noise joint-cubic exclusion

This is the executable, deliberately scoped first slice of the
[architecture](../architecture/README.md). Its wire protocol is the separate
`be.local-pilot/1` extension; its identities use `BELOCALPILOT/1`. It does not
change the frozen `be.arch/1` formats or claim that all production ports and
numerical families have been implemented.

## Exact mathematical obligation

Freeze a point rational probability `0<p<=1/2`, an acquired closed rational
rho interval `1<=rhoLower<=rhoUpper`, and two zero conditional variances.
Here conditional variance means `E(U_i^2)` for a **centered** residual,
`E(U_i)=0`, in the standardized binary decomposition. It does not mean the
variance of an arbitrary noncentered random variable.

The accepted source premises are exactly:

* the standardized binary-decomposition interpretation of p and the residuals;
* zero conditional second moment forces each residual and its third moment
  to vanish almost surely;
* the same-law absolute-third-moment identity in
  [EMPTY_JOINT_CUBICS](../contracts/COUNT-RULES.md#empty_joint_cubics).

With `q=1-p`, `v=p*q`, `x=E(U_0^3)` and `y=E(U_1^3)`, this identity becomes

```text
rho * v^(3/2) = v*(1-2*v) - q*x + p*y,
x = 0, y = 0, rhoLower <= rho <= rhoUpper.
```

The requested pilot conclusion is that **no data satisfying these exact
premises and this point context exist**. Consequently a probability law
realizing the stated decomposition cannot lie in that context. It is not a
bound on a full probability panel, an original COUNT forest, an attained
contact or the Berry–Esseen constant. No arbitrary input matrix is allowed
to define the meaning of this conclusion.

The source manifest binds the public mathematical contract and the relevant
Lean binary/physical interfaces. Byte agreement establishes provenance;
correctness of the named analytic interpretation remains an explicit premise.
The existing Lean Farkas soundness theorem motivates the exact inference;
this pilot's Python checker is not a newly verified Lean decoder.

## Independently derived necessary system

For a declared bounded precision b, compute rational `rL,rH` using integer
square root, and check exactly

```text
0 <= rL <= rH, rL^2 <= v <= rH^2.
hL=v*rL, hH=v*rH, base=v*(1-2*v).
tL=rhoLower*hL-base, tH=rhoUpper*hH-base.
```

Positive rho and v justify the multiplication direction. Point p has no
midpoint-width error; the two noise-variance terms vanish. In this exact
order the necessary rows `A*(x,y)<=b` are:

| Row | Normal | Right side |
|---|---|---|
| 0 | (1,0) | 0 |
| 1 | (-1,0) | 0 |
| 2 | (0,1) | 0 |
| 3 | (0,-1) | 0 |
| 4 | (-q,p) | tH |
| 5 | (q,-p) | -tL |

The checker reconstructs all rows and the root enclosure from the frozen
request, before inspecting the candidate's witness. A candidate must bind
the exact request, context and complete derived-problem identity. It cannot
supply replacement planes, a square-root approximation or a truth flag.

For Farkas weights `w_i`, acceptance requires exact reduced rational values,
all weights nonnegative, `sum_i w_i*A_ij=0` for both columns, and
`sum_i w_i*b_i<0`. The strict negative sum proves a contradiction with the
necessary rows. Equality at zero never supplies an exclusion.

The producer is untrusted. It tries the two strip directions and constructs
a six-entry witness using the zero rectangle when strict separation exists.
If zero satisfies the complete necessary system, it returns that relaxed
feasible point. The checker reports `no_contradiction`; this is not a proof
that an actual probability law exists. A coarse enclosure may miss a true
exclusion, and never becomes acceptance by changing the precision silently.

Arithmetic verification is O(m*d) rational operations with m=6 and d=2.
Integer bit size and square-root precision are explicitly bounded. There
is no generic LP solver, exponential vertex enumeration or floating-point
comparison in this slice.

## Local workflow and authority

One CLI invocation loads and freezes the closed project and inputs, checks
the source/trust contract, and runs a producer followed by an independently
invoked verifier. Immutable bytes live in a local content-addressed store;
SQLite/WAL owns campaign deadlines, attempts, lease generations, events and
authoritative completion. Each worker has a private work directory and a
bounded subprocess profile. Source, environment and policies bind job/cache
identity. Unsupported full-proof requests fail closed.

Resume verifies exact artifacts and performs independent semantic readback
of the stored receipt. A filename, source hash or stored outcome string
alone never authorizes `PILOT_PASS`. The small readback is deliberately cheap
enough to repeat; native production-family replay remains outside this slice.
Stale attempts cannot publish authoritative completion, and retries do not
reset the campaign's time limit.

`PILOT_PASS` means this exact conditional local infeasibility has been
verified. `NO_PASS` includes a feasible necessary relaxation, missing/invalid
data, unsupported scope, exhausted resources and infrastructure failure.
Every report retains `full_proof_pass=false`. Mathematical results and
operational failures remain distinct.

## Scope of the local execution profile

This new profile runs pure Python integer/Fraction arithmetic and bounded
JSON through separate subprocesses. It records the actual Python build,
platform, dependencies, source and supported enforcement. It is not the
legacy Linux numerical-image profile and cannot be used to claim legacy
source replay compatibility.

Wall-clock, input/output and integer/precision limits are enforced. POSIX
may additionally provide OS CPU/address-space limits. Windows must not claim
a hard RAM cap from a sampled value or an unsupported resource API. Full
container isolation, all cloud backends and large numerical families remain
future architecture implementation gates.
