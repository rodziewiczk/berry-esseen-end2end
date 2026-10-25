# Adversarial architecture audit

Verdict: **the documented implementation handoff has no known unresolved specification blocker in the reviewed scope**. All20 findings are `contract_resolved`. This means their mathematical/protocol rules are now explicit and cross-checked; it does not mean an implementation, numerical replay, cloud safety trial or performance claim has passed.

This review covers `architecture/execution-v1`, documents00–07, closed protocol schemas and illustrative fixtures, the execution graph, and their agreement with the [mathematical contracts](../contracts/README.md). The earlier [mathematical audit](../contracts/AUDIT.md) remains separate. Exact source-bound analytic theorem parameters are intentional accepted premises; no missing numerical license is reclassified as analysis.

The specification is suitable for starting implementation in the declared vertical slices. An implementer may choose data structures/search details within the frozen policies, but should not have to invent normalization, mathematical scope, certificate meaning, trust level, dispatch/claim order, money/deadline authority or final acceptance. A discovered source mismatch must be raised as a contract defect rather than patched with an undocumented premise.

## Resolved findings

The [machine-readable register](architecture-findings.json) records each original defect, concrete resolution, acceptance cases, reviewed file hashes and remaining release gates. `contract_resolved` is a specification status; none of the future implementation/cloud trials is claimed as executed by this audit.

| ID | Severity | Issue | Status |
|---|---|---|---|
| IT01 | P1 | Admission precedes attempt creation | contract_resolved |
| IT02 | P1 | No partial or stale-cache final PASS | contract_resolved |
| IT03 | P1 | JSON acceptance is not a Lean proof | contract_resolved |
| IT04 | P1 | Absolute campaign deadline and independent resource shutdown | contract_resolved |
| IT05 | P1 | Two atomic liability ledgers with honest billing limits | contract_resolved |
| IT06 | P2 | Post-deadline evidence handling needs one rule | contract_resolved |
| IT07 | P1 | At-least-once execution with fenced completion | contract_resolved |
| IT08 | P1 | Parallelism preserves legal mathematical decomposition | contract_resolved |
| IT09 | P1 | Port names need executable transition signatures | contract_resolved |
| IT10 | P1 | Frozen templates and quantitative materialization conflict | contract_resolved |
| IT11 | P1 | Controller leadership and resume authority must be fenced | contract_resolved |
| IT12 | P1 | One CLI needs a frozen ProjectConfig contract | contract_resolved |
| IT13 | P1 | Early stop and future-resource ownership need an independent protocol | contract_resolved |
| IT14 | P2 | Mathematical verdict and process exit policy disagree | contract_resolved |
| IT15 | P2 | IAM conditions must not promise unsupported Batch prefix isolation | contract_resolved |
| IT16 | P1 | Inconclusive retry must not poison deterministic verification cache | contract_resolved |
| IT17 | P1 | Reproducibility requires complete accessible input closure | contract_resolved |
| IT18 | P2 | Algorithmic baseline must avoid accidental global work | contract_resolved |
| IT19 | P1 | Paid startup also needs its own absolute stop window | contract_resolved |
| IT20 | P1 | Published attempt records must not contain live fencing secrets | contract_resolved |

## Non-negotiable final acceptance checks

One CLI invocation must either establish the exact complete requested theorem under its frozen analytic and checker trust profile, or report NO PASS with remaining obligations. Empty queues, successful Batch jobs, produced candidates, partial covers, historical PASS strings and a green conditional Lean build are insufficient. A scoped pilot may accept its own scope but cannot display the full theorem PASS.

The ordinary COUNT path must preserve the complete original root forest, both children and closed seams. The quantitative AB24 window retains actual index24, the same unknown law, all25 roots, a returned upper bound that may miss a search target, and both quantitative exterior tails. Its eventual ordinary selected count5 ancestor is a different scope. Unknown laws remain semantic quantifiers, not serialized runtime values. Uniform comparison covers every actual index in its stated infinite range through the source-bound uniform rules, not finite iteration to a computational helper bound.

Canonical encoding must reject duplicate keys before dictionary parsing, noncanonical integers/rationals, malformed timestamps and unsupported tags. Schema validity is only structural. Statement, JobSpec, artifact bytes, verification key, attempt lease and campaign identities have different preimages and authority. Exact dependency receipt, scope and trust bindings must survive import/cache/resume.

## Budget and shutdown criterion

The fixed ledgers are startup7500 and main55000 PLN minor units, with total62500. The main deadline is one T0+43200 seconds anchor persisted before the first paid main activation. Retry, queue, preemption, resume and a second CLI invocation cannot reset it. Reservations cover maximum admitted outstanding liability, including unknown creates, boot, storage, operations, metadata, logs, network, FX/tax and cleanup/retention. Cancellation acknowledgement does not release liability.

The specification must use an independent stop mechanism and absolute VM termination, not just task execution timeout or laptop disconnection. It must distinguish its admission invariant and configured shutdown controls from provider billing certainty. Alerts and delayed billing do not guarantee an exact invoice cap.

## Evidence boundary

Architecture checks can establish structural schema consistency, canonical fixture identities and documented port agreement. Future local interleaving tests, actual cloud preconditions/IAM/shutdown trials, price quotes, performance calibration and complete numerical replay are release gates, not results of this audit.

## Algorithmic decisions and evidence

These are correctness-preserving implementation decisions or proposed baseline choices, not measured speedups. A numerical kernel change still needs a new pinned recipe/profile and conformance evidence.

| Decision | Rationale and asymptotic/resource cost | Required evidence |
|---|---|---|
| Topological validation once per immutable graph snapshot; reverse dependency index | Kahn/DFS is O(V+E). A receipt updates only actual outgoing dependencies; a heap adds O(log V) per ready change. Avoid O(V) full scans on every heartbeat. | Synthetic DAG/cycle/diamond fixtures; exact edge activation under receipt replacement/conflict |
| Bounded deterministic ready queue and resource tokens | Keep scheduler memory and Firestore transaction/read sets bounded. Deterministic IDs resolve priority ties without changing mathematical meaning. | Large queue/page tests; no starvation of required verification/assembly |
| Single-flight verification by exact verification key | At-least-once retries remain safe, but duplicate simultaneous native replay wastes budget. One authoritative definitive result per exact key; no skipped replay when policy mandates freshness. | Two identical submissions, lost lease and fresh-execution cases |
| Stable authorized definitive receipt anchor | Receipt timestamps and run IDs can differ without a new mathematical claim. Keep the first matching definitive anchor and append observations, avoiding a cascade across exact dependency-byte bindings. | Same-key/same-claim fresh replay does not re-materialize descendants; conflict still quarantines |
| Stream large artifacts; validate immutable cache once per trusted store/version | Hashing is linear in bytes; streaming bounds memory independently of archive size. Pin exact immutable generation/source bytes before reuse. Heartbeats must not repeatedly decode/hash full forests. | Peak memory/read amplification measurements, corrupted-object and changed-generation controls |
| Share only read-only source/input caches across local tasks on a node | One verified copy per digest reduces repeated download/decompression. Private mutable attempt paths preserve isolation. Costs scale with distinct source bytes plus task scratch. | Concurrent cache publication, permissions/isolation, disk-cap measurements |
| Chunk only legal original units; preserve the full native acceptor | Scheduling can reduce stragglers but cannot replace full forest/tail/geometry replay. Checkpoint and merge overhead must remain bounded; no per-leaf database object explosion. | Heavy-tail workload calibration and full-cover negative controls |
| Reserve verifier capacity and bound candidate backlog | Producer utilization is not useful proof throughput if the remaining verification queue cannot finish. Backpressure trades some producer CPU for completed accepted work. | Measured producer/replay cost ratios, end-of-window drain behavior |
| Observe exact-integer/rational growth before optimization | Fraction operation count alone misses numerator/denominator bit length and GCD cost. Cache pure common subexpressions only under complete context keys; never mix incompatible source bounds. | Profile actual bit lengths, arithmetic/memory hotspots and context-key controls; compare any new kernel against the same exact contract |
| Simple baseline before extra infrastructure | SQLite locally, one Firestore authority and immutable GCS avoid a second database/broker. Add an optimization only for an observed bottleneck without changing port semantics. | Calibration evidence, bounded operational cost, fault/conformance tests |

## Cross-contract conclusions

| Boundary | Audited result |
|---|---|
| Mathematical states and numerical scopes | Ordinary full forests, quantitative AB24 all25 roots/window plus both tails, selected original count5 ancestor, weak ROOT4 cap, same-law transfers and uniform actual-index ranges remain distinct. Positive-noise local comparison retains the rho_B factor and negative epsilon*lambda sign; zero noise has its separate Bernoulli rule. |
| Final acceptance | One CLI establishes PASS only for the exact complete requested theorem under its authorized profile, with full dependency/cover closure. Sharpness additionally requires the separate lower approximation. Unfinished, unsupported, stale, unsealed or conflicting evidence cannot close an obligation. |
| Lean trust | JSON, foreign exit0, a signature or a hash is not a Meaning proof. The bridge records source/scope/parameter inventory and residual assumptions; source replay, external self-trace and kernel trace are separate capabilities. |
| Runtime authority | Pre-submit physical dispatch reservation precedes actual attempt claim. Separate controller/worker fences, per-slot private grants, exact idempotency, outbox and blob-first publication handle retries and ambiguous outcomes without exactly-once promises. |
| Cache and invalidation | Inconclusive attempts remain retryable. Contradictory definitive claims quarantine a key. Identical fresh replay preserves the first authorized definitive dependency anchor, avoiding timestamp-only invalidation. |
| Money and time | Startup7500 and main55000 grosz remain independent, total62500. Startup has its own7200-second window; main has exactly one43200-second anchor. Absolute VM deadlines and independent scoped cleanup supplement live lease fencing. Reservations persist through unknown outcomes. |
| Shutdown and verdict | Mathematical PASS remains valid if later cleanup fails, but process exit5 and outstanding liability remain visible. Exit0 requires operational closure as well as accepted complete mathematics. |
| Public replication | A separate no-paid local policy can use a longer window without reopening cloud authority. Complete public/offline source/environment/license closure, fresh recomputation and exported-bundle verification are separate explicit release requirements. |

## Checked artifacts versus future evidence

The final architecture validation report records29 structural schemas,466 offline-resolved schema references,49 fixture/assets, canonical/identity controls, local document links and29 preserved Lean source hashes. The independently inspected fixture includes a true rational contradiction for the wrong Farkas system and correctly rejects its statement binding. No fixture invents a numerical acceptance receipt. See the [format report](../../verification/architecture-check.json). This is format/control evidence, not a production numerical checker.

The sanitized [read-only cloud preflight](../../verification/cloud-preflight.json) reports current quota/API observations, including a global100-vCPU ceiling and zero Spot quota. It explicitly does not establish regional capacity, prices, a benchmark, live Batch allocation, watchdog behavior or zero residual cost from unrelated stopped resources.

The following remain future release gates, rather than unresolved mathematical/protocol choices:

* Production ports/codecs/backends and their local/cloud fault-interleaving tests.
* Complete accessible source/build/license closure, including the missing canonical selected p25 capsule for its historical epoch or a compliant explicitly acquired replacement epoch.
* Real registered numerical family adapters/checkers and their pinned Linux environment; whole numerical replay, authenticated receipts and final coverage.
* Quote-backed funded admission, actual IAM/resource ownership checks, independent startup/main watchdog and absolute-termination trials, plus measured CPU/memory/replay/transfer performance.
* A clean second-machine recomputation and offline result-bundle verification.

The stronger Lean-kernel trace route is optional for a declared trusted-source profile and remains unsupported until its verified bridge exists. The specification does not promise that all proof work will finish within the fixed main budget/window, a measured speedup, or an absolute provider invoice ceiling. It specifies what can be admitted and accepted, and how unfinished work yields NO PASS with durable reusable evidence.
