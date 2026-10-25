# Architecture decisions and change control

These decisions record the user's requirements and the chosen implementation
boundary. They are not a claim of completed deployment or measured throughput.

## D01 — Keep the mathematical interface authoritative

The mathematical statements, typed provider scopes and coverage rules in
[contracts](../contracts/README.md) are the source of meaning. Runtime jobs
operate on finite frozen data. The unknown probability law remains in the
semantic quantifiers; it is not serialized as a runtime object. Scheduling
cannot change an index, units, signed coordinate, strictness, contact owner,
root scope, exterior tail or accepted analytic premise.

The existing Lean skeleton checks conditional assembly and structural
mathematics. Full formalization of the analytic proofs remains outside the
agreed scope. A checker profile must state its exact trusted implication;
receipt decoding does not automatically construct a Lean proof term.

## D02 — One product entry point

`be run project.toml --resume` owns the complete workflow, including eligible
cache reuse, missing work, verification, coverage, assembly, export and cleanup.
Optional inspection commands use the same library and state. A user does not
manually coordinate individual proof families or launch cloud workers.

The project declares the requested final theorem and trust policy before
execution. The upper bound and sharpness are distinct requests: the latter
also requires the separate lower approximation input. Full PASS is never
inferred from a partial family or a successful conditional Lean build.

## D03 — Python orchestration with isolated numerical adapters

Use Python for the initial CLI and orchestration to preserve the existing
numerical implementations. Typed domain objects and closed wire schemas
provide the rigor requested by the Java interface analogy. Numerical kernels
run in isolated subprocesses with frozen interpreter, dependencies, source
and environment. Exact patch versions and image digests are mandatory build
artifacts, not values guessed by an implementer from this document.

Optimize or replace a kernel only behind the same mathematical contract and
after conformance and performance measurements. Native or vectorized code
must retain the declared exact arithmetic or enclosure guarantees.

## D04 — Separate authority for bytes, execution and acceptance

An artifact store establishes immutable bytes. A transactional ledger controls
dispatch, leases, money reservations and authoritative runtime completion.
A verifier establishes only the claims allowed by its declared trust profile.
The coverage assembler establishes complete composition. No one of these
layers impersonates the others.

The local backend uses durable SQLite/WAL and a local content-addressed store.
The cloud backend uses Firestore Native as its transactional ledger and Cloud
Storage for immutable bytes. The precise adapter contracts are in
[storage and recovery](03-storage-and-recovery.md). Local execution does not
depend on an in-memory emulator for durability.

## D05 — Google Cloud is the scale backend

Use Batch CPU jobs for numerical work, a Cloud Run controller, Cloud Storage
and the transactional ledger. An independently invoked watchdog enforces
shutdown against a frozen inventory. Exact IAM, cancellation, resource
inventory and outage limitations belong to
[compute and deployment](05-compute-and-deployment.md).

This architecture phase creates no paid resources. The deployment must have
an exact approved region, frozen price quote, quotas and resource inventory
before any paid admission. These are measured deployment inputs, not changes
to the mathematical interface.

## D06 — Budget and time are campaign invariants

The user's allocation is PLN **75** for startup and tests, plus PLN **550**
for the main **12-hour** compute window: PLN **625** planned total. Store
money in minor units, with distinct phase ledgers; unused startup allowance
is not silently added to the main allowance.

The main window is one absolute 43,200-second campaign interval beginning
before the first paid main activation. Resume, retry, preemption, provisioning
delay and a new CLI invocation cannot restart it. Budget admission reserves
worst-case liabilities and includes supporting services and shutdown reserve,
not just CPU time. Persistent storage has an explicit retention and cleanup
policy because it can remain billable after compute ends.

Provider billing is delayed and infrastructure can fail. The system must
state what its own admission and stop mechanisms guarantee and where a
provider outage or already incurred liability can exceed an estimate. It
must never present an alert as an exact invoice ceiling.

## D07 — Maximize useful verified computation

The objective is accepted proof progress per available time and money,
including producer, verifier and assembly bottlenecks. CPU utilization alone
is insufficient. The controller schedules independent legal tasks, balances
long-running roots and protects verification capacity so that candidates do
not accumulate beyond the remaining verification window.

Startup measurements select among explicitly permitted machine profiles and
chunk sizes. Measure representative rational arithmetic, memory, replay,
checkpoint and storage costs. Do not assume that GPU support, more vCPUs,
simultaneous multithreading or more aggressive process nesting improve these
kernels. Avoid CPU/RAM oversubscription and pin native thread pools. The exact
scheduler/performance policy is part of [execution](02-execution.md) and
[compute](05-compute-and-deployment.md).

## D08 — Cache acceptance as carefully as computation

Reuse requires exact semantic, source, environment, checker, trust and
dependency bindings. Candidate cache, accepted verification cache and mutable
checkpoint continuation are different objects. A label, historical PASS,
filename, timestamp or matching source hash alone cannot close an obligation.
Conflicting deterministic receipts are quarantined. A cache object can save
compute without changing the requested theorem or weakening its trust policy.

## D09 — Freeze before dispatch; fail with a useful reason

Before paid work, the planner rejects unsupported profiles, cycles, missing
inputs, incompatible cache entries and incomplete declared cover strategies.
The final mathematical verdict is PASS or NO PASS; structured reason codes
distinguish unfinished work, rejection, invalid input and infrastructure
failure. Persist evidence and remaining obligations even if the CLI exits.

## D10 — How this specification changes

* A semantic change requires a new contract/schema version, source comparison,
  affected Lean interface review and explicit cache invalidation.
* A checker or trust change requires a new verification identity. Old receipts
  remain auditable but are reused only if the requested profile permits it.
* A backend optimization must preserve port invariants and pass local/cloud
  conformance and failure-injection scenarios.
* Machine choice, concurrency and chunk size may vary only within frozen
  campaign policy and reservations; they cannot enlarge money or time caps.
* Missing capsules, exact environment builds or price quotes are explicit
  implementation/deployment gates. They do not authorize fabricated defaults.
