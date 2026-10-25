# Storage, publication and recovery

This document fixes the `Ledger` and `ArtifactStore` ports from
[02-execution.md](02-execution.md). The cloud implementation uses Firestore
Native mode and GCS. The local implementation uses a single-controller
SQLite/WAL database and ordinary local files. They implement one transition
contract; SQLite is not presented as an emulator of Firestore.

## 1. Identities and locators

The protocol's `ArtifactRef` is exactly bytes digest, byte length, media type
and format ID. Location is separate. A cloud locator contains project,
bucket, object name and exact generation; a local locator contains the
registered store ID and ordinary relative path. Moving an identical artifact
does not change its mathematical identity. Changing one byte does.

Objects use `objects/sha256/<first-two-hex>/<full-lower-hex>` inside each
role-specific bucket/store. Their application identity includes the entire
digest. Short aliases used for provider labels never replace full IDs.
Multi-file certificates are manifests naming every ordered member ArtifactRef;
archives preserve original bytes as separate imported artifacts. Neither ZIP
container order nor a pretty-printed JSON copy silently changes the byte pin.

Candidate, native certificate, checkpoint, verification receipt, source
manifest and coverage result are different artifact formats. Typed canonical
records use the RJSON-BE/1 encoding from 01. Original native JSON stays as
original bytes and is interpreted by its explicitly versioned adapter.

## 2. Durable ledger records

Cloud collections are `campaigns`, `jobs`, `attempts`, `dispatches`,
`outbox`, `idempotency`, `verifications`, `coverage`, `artifact_locations`
and `events`. Documents use safe encodings of full IDs, not a human label.
Small bounded records and ArtifactRefs belong in the ledger; forests, logs
and source inventories belong in the artifact store. No document stores a
whole forest or unbounded event array.

The campaign owns immutable main T0/deadline, current control generation,
cancellation epoch, phase budgets and outstanding reservations. Job records
own current state, active dispatch/attempt, monotone lease generation and
committed output refs. Attempt records preserve every actual worker outcome.
Events have deterministic IDs derived from the operation idempotency key.
Events, projections and outbox entries are written in the same transaction.

The scheduler queries a bounded ready index, then transactionally rechecks
the candidate document, campaign, current dependency receipt refs and
resource reservation. The index is a scheduling hint, not readiness proof.
Do not scan every historical event on each heartbeat. Default pages are 100
records, bounded by a frozen API limit.

Firestore transactions are serializable and server SDK callbacks can retry.
All reads precede writes; callbacks contain only ledger reads/computation and
writes. GCS upload, provider submit/cancel, HTTP and process launch occur
after commit through the outbox. [Firestore transaction isolation](https://firebase.google.com/docs/firestore/transaction-data-contention).

Local SQLite uses WAL, `synchronous=FULL`, foreign keys, a busy timeout and
short `BEGIN IMMEDIATE` transactions. Only the local coordinator writes it;
workers use the coordinator API. Its directory must be on one local durable
filesystem, outside Drive synchronization, SMB/NFS and object mounts. WAL's
shared-memory model requires same-host clients. [SQLite WAL](https://www.sqlite.org/wal.html).

The Firestore emulator is for integration fixtures only. It is not the
durable local ledger; official documentation describes its data as
in-memory and nonpersistent across runs. [Firestore emulator](https://docs.cloud.google.com/firestore/native/docs/emulator).

## 3. Blob-first publication

Every publication follows this order:

1. Worker writes into its private attempt directory and closes the file.
   It fsyncs durable local files before advertising a checkpoint, hashes all
   bytes and enforces the declared size/format bounds.
2. Publish each immutable blob. Locally, write an exclusive temporary file
   on the same filesystem, flush/fsync it, then install without overwriting
   an existing digest path. An existing path must independently match size
   and digest; otherwise quarantine the store. Never use an overwrite rename
   as `put-if-absent`.
3. On GCS use `ifGenerationMatch=0`. If another writer wins, read/stat the
   existing live generation and verify the complete bytes/length. Record
   the successful generation. A412 is a race result to reconcile, not a
   reason to overwrite. Every later read pins that generation.
4. Publish the package manifest last, also immutably. The controller verifies
   all refs exist at their recorded versions and checks their bytes. Large
   streamed objects are hashed while reading; provider checksum metadata
   supplements rather than replaces the SHA-256 check.
5. In one fenced ledger transaction, bind the completed output manifest,
   record the operation result and enqueue verification. Commit only if the
   current dispatch/attempt/token/generation matches, the lease is live and
   the campaign fence permits the operation.

GCS has individual-object atomic publication and strongly consistent object
reads. It does not give a transaction over all certificate files and the
ledger. The manifest plus blob-first/ledger-last rule supplies that
application boundary. [Consistency](https://docs.cloud.google.com/storage/docs/consistency),
[request preconditions](https://docs.cloud.google.com/storage/docs/request-preconditions).

GCS generation identifies a specific object version; it is neither the
SHA-256 digest nor the attempt lease generation. Mutable operational pointers,
if needed, use CAS against their exact prior object generation, paired with
the correct metadata generation when metadata is changed. The authoritative
job pointer remains in the ledger. No workflow depends on cloud atomic rename.

## 4. Completion transaction and conflicts

Completion request preconditions are all mandatory:

```
campaign_id/control_generation/cancellation_epoch match current policy;
campaign admission remains active and controller time is before its fence;
job_spec_id/task_kind/current_dispatch_id match;
attempt_id/lease_generation/fencing_token match the active lease;
lease_expires_at > controller_now;
all output ArtifactRefs and generation-pinned locators were verified;
operation idempotency key is unused or has this identical request digest.
```

Success records output refs, the attempt's `produced` state, job projection
and verifier outbox entry atomically. A lost response is retried with the
same operation key and receives the exact committed response. A stale
completion receives `lease_superseded` or `campaign_closed`. Its blobs may
remain recoverable candidates but cannot become the job's current result.

Verifier jobs have their own identity, queue, lease, resource reservation and
completion transaction. Only the verifier's sealed receipt reaches coverage
evaluation. A timeout/preemption/inconclusive or unsupported attempt followed
by a valid complete replay is not a mathematical conflict. These operational
outcomes remain attempt evidence and never populate an accepted cache entry.
For one verification key, contradictory definitive mathematical accept/reject
outcomes, or incompatible accepted claim/scope/conclusion bytes, are quarantined
as `verification_conflict`; no winner is chosen by timestamp. Different log,
duration or attempt bytes alone are not contradictory. Exact dependency receipts and requested trust policy
are checked at coverage publication. Coverage itself is an immutable report
plus a CAS ledger pointer, never a worker-written boolean.

## 5. Checkpoint contract

Exportable records carry only `fencing_token_digest`. Private authenticated
claim-response/idempotency storage may retain the raw WorkerFence for exact
retry of a lost response; it is access-restricted, expires after the lease
and recovery grace, and is excluded from every public artifact/export.
Private disaster-recovery backups require the controller trust boundary;
restoring one revokes its old leases before dispatch. Published ledger/event
exports never include raw bootstrap, worker or controller fence secrets.

Checkpoint manifests contain the exact JobSpec/statement, producer and
checkpoint-format versions, source/environment/profile pins, deterministic
search-policy/seed, completed subtrees or stages, pending frontier, counters,
cumulative resource spend and parent checkpoint ref. They declare
`mathematical_acceptance=false`. Progress is a manifest of work retained,
not evidence that leaves passed.

Each root/path appears exactly once as completed or pending. The loader
checks full geometry, both children, all roots, strict interior cuts and
closed boundary conventions before resuming. It re-hashes source and payload
bytes, rejects duplicate keys, extra paths and unsupported encodings, and
reconstructs executable state from data. Pickle or executable checkpoint
deserialization is forbidden.

Default publication is every 60 seconds of changed state or at a completed
subtree/stage boundary, whichever is earlier and safe. Only the current lease
can CAS the latest validated checkpoint pointer. A newer wall timestamp does
not supersede a different source epoch. Search adapters without checkpoint
support declare that capability false and restart the complete bounded unit.
Completed-stage caching is allowed only under that family's full validation;
an older runtime review explicitly disallows partial numerical resume for
some source families.

Migrations are explicit immutable transformations with old/new format and
profile IDs, input/output digests, losslessness checks and a migration receipt.
They create a new candidate namespace; they do not rewrite originals or
transfer native acceptance. A higher native `LIMIT`, changed precision,
different checker, new resource epoch or new mathematical context requires
the corresponding new JobSpec and fresh acceptance. An untrusted discovery
cache can be imported only under a declared compatibility adapter.

## 6. Recovery matrix

| Crash/race point | Recovery |
|---|---|
| temporary local file or interrupted upload | no committed ref; ignore partial; remove after grace period |
| blobs present, manifest absent | orphan bytes; no job completion |
| manifest present, completion transaction absent | retry exact fenced completion; if lease lost, import only as candidate |
| ledger commit succeeded, response lost | exact idempotency-key retry returns committed result |
| dispatch intent committed, provider create response unknown | reconcile deterministic provider ID; hold reservation |
| provider started, controller restarted | recover dispatch/attempt; require same generation and heartbeat |
| worker continues after revoked lease | quarantine late completion; current state untouched |
| verifier crashed mid replay | retain bounded diagnostics; no receipt acceptance; rerun complete required stage |
| receipt exists, coverage transaction absent | repeat deterministic coverage check with exact dependency refs |
| ledger unavailable | stop new claims/renewals; worker stops by lease/deadline; watchdog uses independent stop manifest |
| restored stale ledger backup | enter recovery mode; revoke all leases, reconcile resources, replay durable events/refs before any dispatch |

`--resume` verifies the frozen project/plan/policy pins, recovers committed
state, checks source and environment compatibility, and reconciles unknown
dispatches. It never marks missing blobs complete from a historical log.
Restoring a database must not restore expired authorization or reset a budget.
The immutable stop manifest's earlier T0/deadline is an independent lower
bound on any reconstructed campaign control.

## 7. Integrity, retention and backups

Local snapshots use SQLite's consistent backup API or a controlled quiescent
backup, not a copy of a live `.db` without its WAL. Cloud snapshots export
bounded immutable ledger/event batches and their digests; recovery verifies
all referenced artifacts. A snapshot is not a numerical acceptance receipt.

GC is mark-and-sweep from frozen projects, committed results/receipts,
coverage reports and retained validated checkpoints. A pending upload or
completion has a protected upload-session record. Default orphan grace is
24 hours; GC rechecks reachability and exact generation before deletion.
Do not race GC with a live lease or unknown provider outcome. GCS soft-delete,
version retention and lifecycle costs belong to the price quote.

Ephemeral scratch/boot disks are deleted at shutdown. Proof artifacts and
last usable checkpoints are retained according to a frozen retention/export
policy, with bytes and retention cost reserved in advance. Deletion of a
canonical accepted artifact requires verified export and the configured
retention rule; cleanup must never erase the only valid copy to manufacture
a zero residual bill. Any retained cloud data incurs continuing cost after
compute stops; the shutdown report states inventory and the funded horizon.

## 8. Required storage/ledger conformance fixtures

Normative store signatures are:

```
ArtifactStore.put_if_absent(expected_ArtifactRef, byte_stream, upload_session)
  -> Stored<ExactVersionLocator> | ExistingIdentical<ExactVersionLocator> |
     digest_mismatch | size_limit | existing_conflict | unknown_upload
ArtifactStore.stat(ExactVersionLocator)
  -> ObjectMetadata<size,generation> | not_found | unavailable
ArtifactStore.get(expected_ArtifactRef, ExactVersionLocator, byte_range?)
  -> VerifiedByteStream | digest_mismatch | size_mismatch | not_found | unavailable
ArtifactStore.seal(PackageManifestRef, exact_member_locators, operation_key)
  -> SealedManifestRef | incomplete_package | invalid_format | artifact_conflict
```

`get` verifies complete bytes before returning a whole artifact as verified.
A range is unverified transport data unless its format supplies a validated
chunk proof; it cannot independently establish the full SHA-256. Unknown
upload is resolved by the exact object name/version and full verification,
not by allocating a new mutable name. Local and GCS versions have the same
immutable semantics, with different version-locator encodings.

Both local and cloud adapters must pass the same interleavings: simultaneous
claim; duplicate completion; stale generation; lease expiry/renew race;
cancel/complete race; ambiguous submit; upload-before-commit crash; commit
with lost response; missing or corrupt blob; checkpoint pointer conflict;
receipt-key conflict; stale backup; and budget reservation contention.
Cloud pilot tests additionally exercise actual GCS generation preconditions,
Firestore transaction retry and API outages. Passing emulator fixtures alone
does not establish production durability or IAM enforcement. These tests are
implementation acceptance criteria, not tests performed during architecture.
