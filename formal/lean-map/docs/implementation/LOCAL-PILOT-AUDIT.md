# Local pilot: adversarial audit

Verdict: **accepted for the declared conditional local pilot scope**. No known unresolved implementation blocker remains in that scope. The original independent 23-test suite passed, followed by the new campaign-head regression and an independently executed real CLI relocation regression. The adversarial test file now contains 24 tests. This is not a production full-proof PASS, a complete COUNT forest or a certificate that a proposed law exists.

## Exact mathematical scope

The frozen context has one rational probability `0 < p <= 1/2`, q=1-p, v=pq, a closed interval `1 <= rhoLower <= rhoUpper` and both centered conditional second moments exactly zero: E(U_i)=0 and E(U_i^2)=0. A zero variance of an arbitrary noncentered variable would not justify cubic zero. The source conventions are conditional mean-zero residuals U0/U1 with x=E(U0^3), y=E(U1^3), and the same-law absolute-third-moment identity

`rho*(v+s)^(3/2) = v*(1-2v)+3v*(s0+s1)-q*x+p*y`.

Independently, zero centered residuals give the standardized two-point variable X=(B-p)/sqrt(v). Its absolute third moment is (q*p^3+p*q^3)/v^(3/2)=v*(1-2*v)/v^(3/2), confirming this specialization directly.

Accepted analytic premises supply the precise source identity and the zero-variance implication x=y=0. The implementation must state these premises in its trust profile rather than pretending to construct their Lean proof from a Boolean. This scope does not need the optional physical-D plane.

At s=s0=s1=0 and point p, the phase-free probability-width error is zero. Let hL<=v*sqrt(v)<=hH be an exact outward enclosure and b=v*(1-2v). Then tL=rhoLower*hL-b and tH=rhoUpper*hH-b. The exact ordered system is

```text
 x <= 0
-x <= 0
 y <= 0
-y <= 0
-q*x+p*y <= tH
 q*x-p*y <= -tL
```

All 6 rows are reconstructed by the independent checker. A producer-provided matrix or unrelated true contradiction is insufficient. If tH<0, weights(q,0,0,p,1,0) have zero weighted normal and strictly negative right side. If tL>0, weights(0,q,p,0,0,1) give the analogous contradiction. Equality does not prove EMPTY.

For p=1/4, rho=1, h^2=27/4096 while b^2=225/16384, hence h<b; a sufficiently sharp outward enclosure gives a genuine contradiction. For p=1/2, rho=1, h=b=1/8 and (x,y)=(0,0) satisfies every row. The negative control must never yield PILOT_PASS. An enclosure too coarse to separate a context remains inconclusive, not falsely infeasible.

## Source comparison

The source archive is cutoff25_20261011.zip, SHA-256 `17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`. The independently read member is `cutoff25_20261011/new_audit/fixed_law24_b5_p24_eps01_v1/joint_cubic.py`, SHA-256 `d4adf6e9cfa430bbd7be7ffd90b994672d648d9886c42aa38e0a94b66eb55238`. Both hashes were rechecked during this pilot audit; the source was read without importing/executing it.

Source anchors: cubic_interval lines 7–15; moment_polytope lines 33–44. In particular line 34 requires `1 <= rhoLower <= rhoUpper`. The pilot narrows its probability interval to a point and to p<=1/2. It changes the historical vertex-enumeration witness to the independently checked Farkas alternative already specified in [COUNT-RULES](../contracts/COUNT-RULES.md#empty_joint_cubics).

## Adversarial acceptance plan

* Correct inconsistent point produces only a scoped PILOT_PASS, with exact premise/source/environment/trust bindings.
* The Bernoulli equality point, a broad rho interval containing its feasible value and an unresolved coarse enclosure produce no PASS.
* Duplicate keys, JSON numbers, unreduced rationals, malformed intervals, unsupported versions, invalid probability/variance/rho and excessive input limits fail closed.
* Altered candidate weights, matrix, source pin, statement, certificate bytes, checker environment or cached receipt are rejected.
* Fresh execution and cache reuse are separately recorded. No source/profile drift inherits acceptance.
* Old lease/attempt cannot publish a current result. Partial bytes and interrupted subprocesses cannot establish acceptance.
* Exact arithmetic and square-root enclosures use bounded integer/rational operations, with no binary64 conversions.

The independent tests exercised the actual local CLI and durable ledger. The [finding register](local-pilot-findings.json) contains exact dispositions and reviewed source hashes.

## Executed adversarial evidence

`tests/test_adversarial.py` passed 23 tests in 31.186 seconds in the locked clean CPython 3.12 virtual environment on Windows. This elapsed value describes the test suite, not a numerical speedup or a prediction for the complete proof.

The real CLI controls established:

* The inconsistent point yields `PILOT_PASS`, explicitly conditional and `full_proof_pass=false`.
* A second CLI process resumes the same campaign with both cache hits, unchanged frozen digest and unchanged attempt count. Independent authorized readback still reconstructs the mathematical system and arithmetic.
* Bernoulli equality and the broad rho interval return `PILOT_NO_PASS`, never false infeasibility.
* Corrupting the stored receipt bytes makes resume fail closed. Modifying an actual copied pinned source file also prevents reuse.
* An unsupported full-proof kind and optimized Python execution are rejected.

Real SQLite/CAS tests additionally established one winner under simultaneous claims, rejection of old lease completion/checkpoint/renewal after replacement, exact duplicate completion, conflict on changed completion bytes, immutable campaign deadline on resume and corruption detection independent of filenames. Semantic controls covered both strict strip directions, rational-square equality, coarse enclosures, changed precision identities, unrelated problem binding, negative/zero/unreduced/wrong-size Farkas weights and altered receipt outcomes.

## Defects corrected during review

| Finding | Observed defect and correction |
|---|---|
| LP06 | Windows denied the original hard-link CAS install; create-only Windows rename now works. SQLite read/constructor handles are explicitly closed. |
| LP07 | A long outputbasename+UUID temporary file exceeded the Windows path limit despite an ordinary work directory. Short independent temporary names and explicit profile limits fixed actual CLI failures. |
| LP08 | The unsigned integer parser allowed one extra digit. Both sign variants now respect the declared digit count. |
| LP09 | Oversized CAS/source inputs could be hashed/read before the bound. Length checks and a fixed three-file, 1 MiB-per-file source inventory bound the work first. |

The source's rhoLower>=1 gate was also preserved after direct source comparison; the pilot does not silently widen it to mere positivity. All findings and the exact 23-test scope are recorded in the companion JSON.

## Algorithmic review

| Decision | Cost and correctness boundary |
|---|---|
| Fixed 6-row/2-variable system | O(m*d) rational operations to validate the witness; no generic LP solver or vertex enumeration. Bit complexity remains relevant and bounded by input/precision policies. |
| Two direct producer witnesses | Constant-size search over the two strip directions. Producer failure to separate is no contradiction; it does not justify another mathematical strategy. |
| Integer square root | Exact rational square checks validate enclosures. Perfect rational squares retain equality exactly; no float conversion or hidden precision upgrade. |
| Bounded parsing and source IO | Byte/depth/node/string/integer/parameter/precision caps precede acceptance. Source files have a fixed inventory and bounded read; CAS rejects oversize before SHA. |
| Content-addressed immutable output plus fenced SQL | Digest verification and exact frozen environment/policy bindings prevent stale reuse; transactions serialize authoritative completion without exactly-once claims. |
| Small semantic readback on cache reuse | Rechecking twelve coefficient products and strict rhs is intentionally simpler than trusting a stored PASS flag. It preserves authority while production large-family replay remains a separate contract. |

## Remaining boundaries

The [pilot specification](LOCAL-PILOT-SPEC.md) matches the implemented signs, normalization, ordered rows, accepted premises and result levels. Python/Fraction correctness and the explicitly accepted analytic interpretation remain trusted inputs. No Lean numeric decoder or unconditional theorem was constructed.

The Windows process profile truthfully records wall/output enforcement and its absence of hard OS RAM/cgroup enforcement. A fresh subprocess with controlled inputs is not advertised as a container security sandbox. Cloud execution, all production mathematical families, full root/phase/tail coverage and a whole-proof final PASS remain future work under the [architecture release gates](../architecture/06-validation-and-rollout.md). Public clean-copy installation/reproduction is a separate root-coordinated integration check; these tests do not pre-claim its result.

## Post-freeze correction: campaign authority is independent of TOML location

Root subsequently found that hashing the absolute TOML path as project_key let an identical relocated TOML select a new head in the same state directory, implicitly granting a new campaign/deadline. The audit was reopened for this concrete issue.

LP10 is now fixed: the runner selects one constant local-pilot head per state directory. The frozen content/environment/policy digest still detects actual drift. An existing different or legacy head is rejected as incompatible_state unless the caller explicitly requests a fresh no-paid local campaign; it cannot be mistaken for an empty ledger.

The new independent ledger regression passed in 0.103 seconds. It rejects an alternate head without fresh and permits the explicit fresh branch. The real CLI relocated-TOML regression was also independently executed and passed in 6.513 seconds: campaign and frozen digest stayed identical, both cache hits were true and attempt count remained 2. Resume does not update the original deadline. These are targeted follow-up runs; the earlier 31.186 seconds remains the duration of the original 23-test run.

The root-coordinated final full suite subsequently passed 58 tests after the stable-head and legacy guard changes, including the 24-test independent adversarial module. Its additional real CLI matrix returned exits 0,0,2,2 for positive, resume, equality and wide-rho cases. Public installation from a clean Git copy remains a separately reported next check.
