# Validation and implementation handoff

This is the acceptance plan for future implementation. The architecture
checkpoint validates specification artifacts; it does not run a cloud proof
or claim runtime fault-tolerance has been tested.

## 1. Architecture checkpoint

Required now:

* Every protocol reference resolves locally; schemas validate against their
  declared JSON Schema draft and all examples match their declared types.
* Canonical byte and digest fixtures are reproducible. Negative controls
  distinguish malformed input, a valid rejected candidate and an unsupported
  profile. No fixture invents a numerical PASS.
* Documents agree on identity, authority, final acceptance, campaign lifetime,
  phase budgets and ownership of every mutable operation.
* Every current Lean source still matches the source hash in the successful
  compiler report. Architecture-only changes do not assert a fresh Lean run.
* Graph links point to real contracts. Audit findings are either resolved or
  explicitly block the corresponding implementation/deployment stage.

The reference codec/fixture tooling supplied with the specification is for
format conformance. It is not the production runner, a numerical checker or
a proof of the semantics of a JSON object.

## 2. First local vertical slice

Implement canonical parsing and identity first, then immutable local storage,
transactional local ledger, producer isolation and receipt publication. Use
the small rational Farkas path with its exact necessary-row binding as the
first semantic exercise. A syntactically valid multiplier vector alone is
insufficient: bind the row meanings to the frozen mathematical context.

The same public CLI must execute the complete pilot graph. Capture the source
capsule, environment, frozen statement, candidate bytes, exact verification
key, receipt, selected dependencies, coverage result and final report. An
explicitly scoped pilot may pass that pilot; it cannot print the full theorem
PASS banner or claim that the other families are implemented.

Required controls include a wrong denominator, duplicate JSON key,
noncanonical rational, modified row, unsupported rule, changed strictness,
wrong statement ID, altered bytes after hashing and a dependency from another
scope. Each must fail in the responsible layer with the documented reason.

## 3. Implement proof families without inventing mathematics

| Slice | Required acceptance evidence |
|---|---|
| Ordinary COUNT | Full original root forest, both children, closed seams, exact a0 axis, quantitative returned bound and complete replay |
| Original selected count5 subtree | Exactly its licensed ancestor subtree; no invented full-forest obligation or reuse as full transferred AB24 |
| Transferred AB24 | All 25 original roots at actual n24, full new phase/threshold scope, same law, complete exterior tails |
| Mixed reference registry | Exact epoch/capsules, one enclosing scope, explicit admission versus selected uses, earlier-license acyclic dependencies |
| LOW/HIGH and Prawitz | Separate physical and score meanings, coherent triples, complete integrals/tails, all required window terms and gates |
| Small indices and ROOT4 | Distinct bases, chosen owner and common defect, weak ROOT4 target preserved |
| Uniform comparison | All 83 exact panels, actual support and zero-noise branch, source-bound numerical acquisition license |
| Auxiliary tail barriers | A40/P41/A45/P46/A46 finite resource passes ending in strict negative D, with their separate resource/correction rules |
| Final assembly | Literal finite indices and independent n49+ tail; lower approximation additionally required for sharpness |

For every slice, record the source contract and exact accepted conclusion.
Implementers may choose search algorithms and data structures. They must
raise a contract defect if acceptance requires an unstated mathematical fact.
Missing historical source capsules require an approved complete capsule or a
new explicit acquisition epoch, not a historical PASS imported as evidence.

## 4. Ledger and storage conformance

Run the same port-level scenarios against durable local and cloud adapters:

| Fault or race | Required observable result |
|---|---|
| Crash after artifact upload, before completion transaction | Orphan immutable bytes; obligation remains open; recovery can retry safely |
| Crash after completion commit, before acknowledgement | Exact duplicate returns committed response; no second authoritative completion |
| Lease expires; old worker finishes after replacement | Old generation cannot publish authoritative completion or checkpoint |
| Two duplicate workers claim one dispatch | At most one active authoritative generation |
| Provider create succeeds but response is lost | Reconcile deterministic provider identity; hold liability reservation |
| Checkpoint truncated or wrong environment | Reject continuation; preserve accepted independent subresults |
| Same verification key, divergent receipts | Quarantine conflict; no semantic reuse or final PASS |
| Object listing is delayed or partial | Read exact manifest references; listing is not completion evidence |
| Controller restarts or a second CLI resumes | Same campaign, phase ledgers, deadline and fenced coordinator policy |
| Parent cover has a missing root, seam or ray | Assembly rejects completeness even if every present child passed |

Do not simulate these only by mocking successful method returns. Exercise
the committed state before and after each interruption and verify immutable
bytes, generation checks, event history and reservations.

## 5. Paid startup gate: at most PLN75

Before the first paid test, supply exact source and environment capsules,
current region-specific prices and exchange-rate policy, quotas, scoped
identities, frozen resource inventory, stop manifest, logs/retention policy
and the maximum outstanding liability calculation. Startup shares the same
admission discipline as the main run and has its own PLN75 ceiling/reserve.

Use a bounded representative workload, not a full proof attempt. Measure
single-process arithmetic and memory, selected machine profiles, controlled
process scaling, replay bottlenecks, upload/checkpoint overhead and startup/
shutdown latency. Record warm/cold and SMT effects instead of assuming a
vCPU is one independently fast physical core. Choose the configuration that
maximizes verified useful work under the declared budget.

Required cloud safety trials: controller loss, local CLI disconnect, queued
job past cutoff, preempted worker, ambiguous create/cancel response, duplicate
watchdog invocation and independent stop with the primary ledger unavailable.
Record provider-observed resource cessation; a cancel request acknowledgement
does not settle the reservation. If these trials cannot fit the startup
allocation, reduce their scope or stop; do not spend the main allocation to
complete them automatically.

## 6. Main gate: PLN550 and one 12-hour window

Start only after startup evidence passes and the complete requested proof
graph has supported producers, verifiers and assembly. Validate the selected
price/profile bounds again and freeze the absolute main deadline before any
paid main activation. Reserve final verification, export and shutdown costs.

During execution, compare observed verified throughput and memory against
calibration. Adapt dispatch only within approved machine/concurrency/chunk
policy. Prioritize unfinished proof dependencies and drain verification
before the remaining window becomes too short. Never sacrifice a required
checker or coverage step to display a success before cutoff.

At the limit, close admission, stop/checkpoint running work and verify cleanup.
Persist reusable accepted results and a machine-readable remaining-obligation
report. The fixed budget/window does not guarantee that the full proof can
finish; unfinished coverage yields NO PASS and remains resumable only under
an explicitly authorized later campaign policy.

## 7. Definition of the implementation handoff

The [reproducibility contract](07-reproducibility.md) is a release gate:
third parties must have complete public/offline input and environment closure,
a clean local recomputation route and portable verification without the
author's cloud credentials. Cache-only readback does not satisfy this gate.

Each implementer receives a port, exact input/output types, authority limits,
state transitions, failure meanings, conformance cases and links to the
mathematical contract. A task is complete only with reproducible evidence
for its assigned acceptance cases. The auditor checks compatibility across
ports before a new family or deployment stage becomes available in the CLI.
