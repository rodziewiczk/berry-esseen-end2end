# Execution, scheduling and the CLI

Status: implementation contract, not a shipped runner. The mathematical Lean
modules remain unchanged. Protocol types and identity preimages are fixed in
[01-protocol-and-types.md](01-protocol-and-types.md); persistence and cloud
deployment are specified in [03](03-storage-and-recovery.md) and
[05](05-compute-and-deployment.md).

## 1. Concrete implementation boundary

Implement the orchestration and adapters in Python, preserving the existing
Python numerical kernels behind subprocess interfaces. The user's Java
analogy means explicit interfaces and invariants. It does not require a
second implementation language. Start with CPython 3.12 compatibility, then
freeze an exact patch/build, dependency lock and image digest in each
environment profile. No implicit interpreter upgrade is permitted.

Static inspection of the pinned research code found independent exact-rational
jobs, complete COUNT forests, source-bound native acceptors, PREFIX 2 discovery,
stage-level caches and Linux supervisors. Existing infrastructure reports
Windows/Python 3.12 fixtures; later code explicitly repairs Python 3.13 AST
descriptor differences. These observations are compatibility evidence, not a
benchmark or certification that every family runs on a newly built image.

The first implementation exposes these ports:

| Port | Required operations | Authority |
|---|---|---|
| `Planner` | validate/freeze project; detect cycles; expand exact jobs | immutable plan only |
| `Ledger` | transaction; reserve dispatch; claim; renew; checkpoint; complete; revoke | runtime authority |
| `ArtifactStore` | put-if-absent; read exact version; stat; verify bytes | immutable bytes only |
| `ComputeBackend` | submit; inspect; cancel; reconcile owned resources | runtime observations |
| `ProducerAdapter` | prepare; discover/replay; checkpoint; export candidate | no proof acceptance |
| `VerifierAdapter` | fresh complete replay; controls; source/context checks; export receipt | declared trust profile |
| `CoverageAssembler` | check exact claims, scopes, dependencies and covers | proof coverage only |

No port accepts an untyped dictionary as its mathematical contract. The
backend never interprets a numerical `PASS` or upgrades trust.

## 2. CLI behavior and stable campaign

The normal entry is `be run project.toml --resume`. First invocation freezes
the project, plan, source manifests, profiles and budget policy before any
paid submission. `--resume` finds the same frozen campaign and reconstructs
state; it does not follow a file called `latest` or silently replan edited
inputs. `be plan`, `be status`, `be stop`, `be verify` and `be export` expose
the same library; none runs a second scheduler implementation.

A `run_id` identifies a CLI invocation. A durable `campaign_id` anchors the
two phase budgets and the single main deadline across every invocation.
Creating a new run ID, retry, checkpoint migration or backend reconnect
cannot grant a new 550 PLN or another 12 hours. A new paid campaign requires a
new explicitly authorized budget policy. The live main campaign cannot
change its backend, trust policy or deadline by editing TOML.

Run exit meanings are fixed:

Public reproduction defaults to the local backend and requires no Google
Cloud account. `--fresh --empty-cache` creates a fresh mathematical execution
namespace and replays every required native/checker obligation; it cannot
reuse old acceptance. Immutable source bytes and published candidate
certificates may still be explicit, digest-checked inputs. `--offline` resolves
them only from a complete portable bundle and forbids network access. A
pinned public certificate never skips a producer required by the selected
full-recompute graph; bundle verification, full recompute and additional fresh
discovery are distinct reported modes. Missing
public/offline inputs produce `NO_PASS` with exact unresolved refs, not a
fallback to private GCS. Public recipes and lockfiles must build the pinned
runtime; a cloud-only image or private account permission cannot be a proof
dependency. See [07-reproducibility.md](07-reproducibility.md).

| Exit | Meaning |
|---|---|
| 0 | all requested obligations covered under the requested trust profile |
| 2 | valid plan; work remains, budget/deadline exhausted or stopped |
| 3 | input/schema/source/profile unsupported or invalid |
| 4 | verification rejection or conflicting deterministic receipts |
| 5 | unrecovered infrastructure/cleanup failure |

The normal full-proof command prints mathematical `PASS` or `NO_PASS`, plus
an independent cleanup status. Exit 0 also requires successful operational
closure. A cleanup failure changes the operational exit code, not the truth
of an already accepted mathematical receipt. Exit 0 is never inferred from empty queues, completed VMs or a green Lean
interface build. Full Lean compilation and numerical verification are
different receipts.

## 3. Three independent state machines

Runtime `JobState` is
`blocked | ready | dispatch_pending | dispatched | running | produced |
retry_wait | exhausted | cancelled`. A verification job also ends in
`produced`: its output is a receipt whose outcome is interpreted separately.

`AttemptState` is
`reserved | running | checkpointed | produced | failed | lost | cancelled |
superseded`. Only one attempt generation can commit authoritative completion
for a `(job_spec_id, task_kind)` pair. State events are append-only; the job
document is a transactional projection, not the sole audit history.

Receipt outcome is exactly the protocol's
`metadata_only | accepted_conditional | rejected | unsupported | inconclusive`.
Coverage is independently `uncovered | conditional | covered | conflict`.
`accepted_conditional` can cover an obligation only if the requested trust
profile, full scope and every exact dependency receipt are accepted. A
receipt for a proper subset does not close the whole obligation.

## 4. DAG readiness and dependency binding

Plan nodes have explicit task kind `produce | verify | assemble`, immutable
JobSpecs and typed dependency requirements. Readiness requires every selected
dependency claim and scope, not merely a producer's output file. An analytic
assumption is an explicit named premise; it is not scheduled as a fake
numerical job. Alternative methods are explicit OR routes whose selected
whole outputs meet the same requirement. Partial covers are AND joins.

The initial planner rejects cycles, unknown rules, missing frozen inputs,
unlicensed source epochs and unsupported producer/checker profiles. It
materializes the required mathematical DAG and a separate runtime DAG.
Producing a certificate permits a verifier job. Only a matching verification
receipt permits downstream semantic assembly. Producing parent data can
enable untrusted downstream search, but cannot satisfy its proof dependency.

Two different expansions are permitted. First, an approved typed semantic
adapter may instantiate a frozen mathematical template using exact accepted
dependency receipts (for example AB 24 quantitative U -> qR -> a new support
cap chain -> post-refinement COUNT). It publishes a new immutable graph
snapshot, newly materialized Statement/JobSpec IDs and exact provenance.
It cannot change the template, invent an edge or upgrade trust. Unresolved
templates are not executable jobs and do not count as covered obligations.

Second, a parent search
may issue immutable `SearchPartition` data naming parent context, root,
binary path, exact rational box and both child boxes. It must conserve the
whole root domain, including all closed faces, before children are admitted.
A failed or empty branch is not silently omitted. This expansion changes
runtime work, not the parent mathematical statement.

## 5. Legal splitting and aggregation

Prefer existing independent native units: exact forest/root, Fourier panel,
resource cell, fixed index or selected source action. A monolithic source
acceptor remains monolithic until an explicit checked aggregation contract
exists. Its logs cannot be concatenated into a substitute full receipt.

COUNT discovery can split at a verified existing internal tree node.
Each work item owns `(statement_digest, root_index, binary_path, box_digest)`.
The coordinator records both children before marking a split expanded.
Completed subtrees are immutable; merging reconstructs the canonical full
forest with every legal root and both children. It then invokes the original
complete acceptor. A subtree's acceptance does not substitute for that full
replay. General COUNT and AB quantitative caps retain their separate meanings;
an early search target need not be achieved to produce a valid quantitative
upper-bound candidate.

Fourier splitting requires the source integration/cover rule, weights,
endpoints and complete tails. Reductions use exact rationals or certified
enclosures in deterministic cell order. No nondeterministic floating-point
sum, coordinatewise mixture of alternative bounds, cropped phase domain or
omitted infinite ray is a scheduling optimization.

## 6. Dispatch, lease and fencing protocol

All time decisions use coordinator UTC; workers also maintain an elapsed
monotonic timer. A worker with clock discrepancy greater than 5 seconds fails
closed. Heartbeat period is 30 seconds, lease TTL 120 seconds. Renewal extends
only the same attempt/generation/token and never beyond the campaign fence.

Dispatch is deliberately distinct from claim:

1. In one ledger transaction, check ready dependencies, campaign admission,
   resource tokens and worst-case money reservation. Create a dispatch intent
   and outbox entry; set `dispatch_pending`. Perform no cloud call inside
   the transaction callback.
2. The backend submits a deterministic, immutable provider request from that
   outbox entry. Unknown responses are reconciled by provider ID; do not
   release reservations or submit a different request merely after timeout.
3. Queued jobs are `dispatched`, without an active computation lease.
   On actual worker start, `claim(dispatch_id, worker_identity)` checks the
   current dispatch, campaign/deadline, expected task kind and profile.
4. In the claim transaction increment the pair's monotone lease generation,
   create `attempt:<UUID>`, generate an unpredictable fencing token and
   mark the job running. A duplicate or obsolete worker fails the claim.
5. Completion first publishes immutable outputs, then performs the fenced
   ledger transaction described in 03. Only that transaction changes the
   authoritative completed output and enqueues its verifier.

Every mutable worker request carries campaign, run, job, task kind, attempt,
lease generation, token and idempotency key. `claim`, `renew`, `checkpoint`,
`complete`, `fail` and `stop_ack` return either the committed prior response
for an exact duplicate, or a typed conflict. Reusing one idempotency key with
different payload bytes is rejected. Provider task indices are locators,
never lease generations.

The controller scans expired leases. It increments/revokes the generation
before another dispatch becomes eligible. A late worker may leave immutable
candidate bytes, but cannot overwrite a newer checkpoint or completion.
Fencing protects the ledger; GCS generation preconditions protect individual
objects. Neither replaces the other. Execution is at least once, not exactly
once.

## 7. Retries, limits and stopping

Native provider retries are disabled. The controller permits at most 3
infrastructure retries after the first attempt, within the same campaign's
time, money and resource reservations. Backoff is 10, 30, 90 seconds plus a
deterministic per-job 0--5 second offset. Retries never reset native node,
precision or resource-policy limits. A planned bounded search slice may
checkpoint and continue as another attempt only while the original campaign
and cumulative work budget permit it.

| Condition | Action |
|---|---|
| preemption, temporary network/service failure | retain validated checkpoint; retry within policy |
| OOM, CPU/disk/log limit | exhausted; new explicit profile/JobSpec required |
| numerical guard failure or unfinished forest | incomplete; checkpoint; no certificate |
| native mathematical rejection | receipt rejected; no automatic precision escalation |
| unsupported environment or source mismatch | blocked; no fallback kernel |
| lease lost, revoked generation, inactive campaign | stop; retain orphan bytes only |
| deadline/cost admission fails | no new dispatch; checkpoint/stop existing work |

`be stop` closes admission transactionally, revokes leases, requests owned
process/backend cancellation, and waits for independent resource observations.
Disconnecting a notebook or closing the CLI is not cloud shutdown. A graceful
worker has at most 60 seconds to checkpoint; hard termination follows. The
global deadline, VM termination and independent watchdog remain effective
if the CLI/controller disappears, as specified in 05.

## 8. Reuse and observable progress

Reuse production only for identical JobSpec/input/profile bindings. Reuse a
verification only for its exact verification key, checker/environment, trust
profile and dependency receipts; it is not inherited from producer reuse.
Any policy requiring fresh execution still launches the prescribed replay.
Checkpoint compatibility is narrower and specified in 03.

Coalesce concurrent verifier requests for the same exact verification key
into one in-flight full replay and one compatible definitive anchor. Reuse
that anchor only when the requested freshness policy permits it. Inconclusive,
metadata-only and unsupported attempts are retained for audit but never
poison the accepted cache or prevent a later valid complete replay.

A public local reproduction uses its own explicit no-paid-activation
campaign policy and finite local CPU/memory/time limits, which may exceed
12 hours. It does not acquire or inherit this project's GCP budget or main
deadline. `--fresh`/`--empty-cache` within an active GCP campaign still cannot
reset its funds, T0 or deadline; a separate local reproduction campaign must
be named explicitly. No cloud credentials or price quote are required for
that local policy.

Expose queue/running/retry counts, validated checkpoint age, source/profile
blocks, producer bytes, verified claims, uncovered scopes and coverage
conflicts as separate metrics. Show exact accepted/required cell or root
counts where meaningful. No arbitrary percentage or ETA is fabricated from
visited nodes. Track compute/utilization, peak memory, checkpoint/upload
time, native replay time, retry waste, reserved money and deadline remaining.
Logs carry IDs and reason codes; full stdout/stderr remain bounded artifacts,
not proofs. A run report distinguishes runtime completion, mathematical
coverage, explicit analytic premises and shutdown confirmation.

## 9. Normative typed ports and transaction boundaries

These signatures are contracts, not runnable code. ID/ref types use the
strict protocol. `OperationKey` is scoped to campaign, authenticated
principal, operation name and key. Exact repeated request bytes return the
committed response; different bytes return `idempotency_conflict`.

```
Ledger.acquire_controller(campaign, holder_id, operation_key)
  -> ControllerFence | controller_busy | campaign_closed
Ledger.renew_controller(ControllerFence, operation_key)
  -> ControllerFence | controller_superseded | campaign_closed
Ledger.reserve_dispatch(ControllerFence, DispatchManifestRef,
  CostAdmissionRequest, operation_key)
  -> DispatchReservation | dependencies_unready | budget_denied |
     resources_denied | deadline_denied | quote_invalid | controller_superseded
Ledger.record_submission(ControllerFence, dispatch_id, ProviderObservation,
  operation_key)
  -> DispatchRecord | provider_spec_conflict | controller_superseded
Ledger.claim(dispatch_id, task_index, bundle_index, BootstrapGrant, ProviderWorkerIdentity,
  origin_run_id, operation_key)
  -> ClaimGranted<AttemptAdmission,PrivateWorkerFence> | dispatch_superseded | identity_denied |
     already_claimed | campaign_closed | deadline_denied
Ledger.renew(WorkerFence, operation_key)
  -> Lease | lease_expired | lease_superseded | campaign_closed
Ledger.checkpoint(WorkerFence, checkpoint_sequence, ManifestRef, operation_key)
  -> CheckpointRef | invalid_checkpoint | sequence_conflict | artifact_unsealed |
     lease_expired | lease_superseded | campaign_closed
Ledger.complete(WorkerFence, OutputManifestRef, operation_key)
  -> Completion | artifact_unsealed | output_contract_invalid |
     lease_expired | lease_superseded | campaign_closed
Ledger.fail(WorkerFence, FailureKind, DiagnosticsRef?, operation_key)
  -> FailureDecision | lease_superseded | campaign_closed
Ledger.revoke(ControllerFence, dispatch_or_attempt, Reason, operation_key)
  -> Revocation | controller_superseded | already_terminal
Ledger.reconcile(ControllerFence, dispatch_id, TrustedProviderObservationRef,
  operation_key)
  -> Reconciliation | ownership_conflict | observation_stale | controller_superseded

ComputeBackend.submit(ImmutableProviderRequestRef, provider_request_id)
  -> Submitted<ProviderRef> | AlreadyExists<ProviderRef> | Unknown | Rejected
ComputeBackend.inspect(ProviderRef)
  -> Queued | Provisioning | Running | Terminal | NotFound | Unknown
ComputeBackend.cancel(ProviderRef, cancellation_key)
  -> CancelRequested<OperationRef> | AlreadyTerminal | Unknown | Denied
ComputeBackend.list_owned(OwnershipScope, page_token?)
  -> Page<ProviderResourceObservation> | Unavailable | Denied
```

`DispatchReservation` owns one quoted physical dispatch-group liability and
an immutable task-index mapping. Its JobSpec IDs are a sorted unique set;
the array manifest maps every physical slot and ordered logical bundle index
explicitly. An unbundled slot has bundle_index0. It has no attempt or positive
worker lease generation yet. `AttemptAdmission`, created on actual claim,
binds reservation/dispatch/slot to an attempt and new lease generation.
Physical VM/group cost is reserved once, not once per logical job sharing
it. Each new physical retry has a new reservation while the old reservation
remains until reconciled.

Atomic read/write sets are normative:

| Operation | Read and recheck | Write together |
|---|---|---|
| reserve_dispatch | leader fence; campaign/time; phase money; resource tokens; jobs/dependencies; quote; operation key | reservation; dispatch; jobs dispatch_pending; submit outbox; event; response |
| record_submission | leader fence; dispatch/request digest; provider identity | provider ref/state; event; outbox result |
| claim | campaign/time; current dispatch/slot; grant/identity; job generation | consume grant; increment generation; attempt+AttemptAdmission; job running; event; response |
| renew | campaign fence; exact active token/generation; live lease | bounded expiry; heartbeat projection; response |
| checkpoint | worker checks; monotone sequence; sealed validated manifest | checkpoint event; latest pointer CAS; response |
| complete | worker checks; sealed output/format; exact dependency selection | job/attempt produced; output pointer; verifier/assembly outbox; event; response |
| fail/revoke | current authority; typed failure/retry policy | revoke/close attempt; fences; retry/cancel intent; event; response |
| reconcile | trusted observation; full ownership; unknown outcomes/liability | lifetime accounting; release only established liability; state/retry decision; event; response |

Prepare sealed refs and provider observations outside callbacks. Retried
transactions perform no external side effects. A concurrent stop wins if
its campaign generation/epoch changes before commit. Contention exhaustion
returns infrastructure failure rather than bypassing admission. `NotFound`
after an unknown create is insufficient alone to release money if an API
request can still be in flight; retain and reconcile that request's terminal
outcome/observation window.

## 10. Controller, invocation and worker authority

Control-loop leadership is a lease distinct from worker leases:
`(holder_id, controller_term, private_nonce, expires_at)`, TTL 60 seconds,
renewal 15 seconds while the bounded control request runs. Takeover after
expiry increments term and issues a fresh nonce. A stale instance cannot
adopt authority by merely reading a newer term; transactions match its
captured holder/term/nonce and expiry. Takeover reconciles unknown outbox
requests first. Campaign `control_generation` and `cancellation_epoch` are
policy fences, independent of leadership; none resets T0.

Cloud Run instances may concurrently serve authenticated worker calls.
Their transaction authority is the current campaign/worker fence, not a
fresh leadership lease granted to the worker. Provider actions require the
leader fence, an outbox send lease and an immediate campaign recheck. GCP
APIs do not accept our term: an already in-flight request can arrive late.
Immutable request IDs, worker admission refusal and watchdog reconciliation
contain the race; unknown cost remains reserved. External side effects are
not claimed exactly once.

`run_id` in an attempt is its origin/audit invocation. Resuming the same
campaign under a new CLI run ID does not revoke a healthy prior worker.
Mutations authenticate campaign, dispatch, attempt and fences, not equality
with the current CLI run ID. A stale controller cannot gain authority by
inventing a new run ID.

Each logical bundle entry receives an independent 256 bit bootstrap capability
scoped to exact dispatch/physical slot/bundle index/JobSpec, expected worker
SA, provider parent and expiry.
Only its hash is stored in the ledger. Workers cannot read the full array
assignment or other slots' capabilities. The trusted launch wrapper receives
its grant through per-task provider configuration; numerical children receive
no grant, lease token, cloud credentials or metadata-network access. Secrets
are never copied into logs/artifacts.

Claim verifies an audience-bound provider identity, the capability and
backend-observed parent/task/VM membership, binds the actual VM UID, and
consumes the grant atomically. A shared service-account name alone does not
identify a task. A startup isolation test must establish the trusted wrapper
boundary. If per-task grants cannot be isolated from other numerical
children, that deployment is unsupported. Later calls require WorkerFence.

Exportable Attempt/AttemptAdmission records contain `fencing_token_digest`,
never the raw secret. `PrivateWorkerFence` is returned only over the
authenticated claim response to the trusted wrapper. The ledger checks its
high-entropy token hash, generation and worker identity. A public digest
does not authorize any RPC; raw fence/bootstrap secrets are excluded from
ArtifactRefs, cache exports, logs and portable bundles.

## 11. Algorithmic and I/O bounds

The implementation baseline uses Kahn topological validation in O(V+E)
time and O(V+E) stored edges for each materialized graph snapshot. Maintain
a reverse-edge index and unmet-requirement count per node. A newly accepted
receipt updates only its dependents, O(outdegree), plus bounded indexed ready
queue insertions. It does not scan the whole graph or event history on every
worker heartbeat. Expanding a semantic template publishes a new checked
snapshot and its changed edges; it never mutates an old accepted graph.

Priority is deterministic: required critical dependencies first, then aged
ready work, then stable full JobSpec ID. A reverse-topological O(V+E) pass
computes estimated critical paths from the per-family cost table at snapshot
creation or a batched calibration update. These estimates guide runtime
ordering only. Unknown estimates are marked unknown, never used as a proof
criterion or a fabricated ETA. Indexed ready queries/pages are bounded 100;
local ready insertion/removal uses an O(log R) heap.

For small independent jobs, static longest-predicted-work-first assignment
to the least-loaded physical bundle costs O(K log K + K log P) for K selected
jobs and P bundles. Each bundle contains at most 32 logical jobs with one
homogeneous execution profile; its frozen mapping and each per-job grant
retain separate attempts and receipts. No dynamic cross-worker work stealing
is required in v1. Large unsplittable source units remain intact. Readiness
and money are checked for the full selected group before any submission.

Invalidation rules are explicit: mathematical/context/rule change creates a
new statement; producer/environment/resource/search-policy change creates a
new JobSpec; checker/trust/dependency-receipt change creates a new verification
key. Recompute affected semantic descendants through reverse edges, not all
unrelated families. Existing candidate bytes may still be explicit inputs to
a newly authorized verifier when its format/context contract permits it;
an old acceptance is never inherited by renaming an ID.

Stream hashes and parsers with bounded buffers; reject declared size/count
limits before allocation. Cache source capsules read-only per node by exact
digest, verify once on installation and when importing a new manifest, and
never rehash a whole 1GBclosure on each heartbeat. Process-local exact-function
memoization must include all relevant context/source/precision parameters and
has an explicit byte/entry ceiling. Discovery memoization remains discovery
only. Cache hits do not remove a source-required fresh complete native replay.

Do not rewrite Fraction kernels into floating point, change denominator
normalization or remove guards as a scheduler optimization. An arithmetic
implementation change requires a new producer/checker profile, reference
comparison and corresponding mathematical soundness contract. CPU, SMT,
memory, source-transfer and verification performance remain startup
measurements, not assumed wins from a language or VM family.
