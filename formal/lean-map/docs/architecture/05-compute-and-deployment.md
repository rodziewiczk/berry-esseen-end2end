# Local and Google Cloud deployment, throughput and cost controls

This is the selected implementation baseline, checked against official
documentation on 25 October 2026. No cloud resources, images, paid pilot or
numerical calculations were created during architecture work.

## 1. One CLI, two deployments

`be run project.toml --resume` plans, runs, verifies and assembles the entire
requested proof. The user does not launch notebook families manually.
It reports mathematical `PASS` or `NO_PASS` under the frozen trust profile,
and independently reports shutdown/cleanup status. Exit 0 requires the
requested coverage and successful operational closure; cleanup failure
does not invalidate a previously established mathematical receipt.

The 75/550 PLN and 12 hour policy below is the specifically authorized GCP
campaign policy. Public local reproduction uses a distinct no-paid-activation
policy with explicit local resource/time limits; it may run longer than
12 hours and needs no GCP account. It never reopens an expired cloud campaign
or copies its spending authorization.

| Component | Local | Selected Google Cloud baseline |
|---|---|---|
| controller/scheduler | one Python process | one authenticated Cloud Run service |
| authoritative ledger | SQLite/WAL, one local host | Firestore Native, server transactions |
| immutable artifacts | ordinary local content-addressed files | regional GCS |
| numerical producers/verifiers | bounded Linux subprocess/container workers | Google Batch CPU tasks, digest-pinned containers |
| independent deadline enforcement | external supervisor plus monotonic deadline | separate watchdog Cloud Run service +Cloud Scheduler +absolute VM termination |
| monitoring | CLI/events/artifact logs | same events plus bounded Cloud Logging/Monitoring |

There is no Cloud SQL fixed-instance baseline, Kubernetes cluster, Pub/Sub
broker, Workflows DAG engine or numeric Cloud Run Jobs layer. Firestore is
the single cloud database. Its serializable transactions implement the same
Ledger invariants as the durable local adapter. The emulator is only an
integration-test dependency. [Transactions](https://firebase.google.com/docs/firestore/transaction-data-contention),
[emulator limits](https://docs.cloud.google.com/firestore/native/docs/emulator).

Cloud Run executes short control requests and bounded streaming artifact
sealing; it does not run forest discovery. Baseline limits are min instances 0,
max instances 2 for the controller, request concurrency 8, 1 vCPU/1 GiB and a
300 second request timeout. The watchdog has a separate identity/service,
max instances 1 and a300 second request timeout. No long-running background
scheduler is assumed to survive an HTTP request. The scheduled tick and
worker events each run bounded idempotent reconciliation.

Project ID, billing account/currency, region, allowed zones, Firestore
database location, bucket names and service-account identities are required
deployment configuration. They are not inferred from a folder name. Use
one supported region for data and workers; verify locations/quotas before
activation. Unknown values block paid dispatch, not local schema validation.

## 2. Runtime compatibility and reuse

Images are pinned by OCI digest and platform `linux/amd64`. Each numerical
profile freezes exact CPython build, source bytes, dependency lock, native
assertion policy, argv/cwd conventions, supported output/checkpoint formats
and supervisor behavior. CPython 3.12 is the initial compatibility line, based
on existing research fixtures; the exact patch/build is recorded at packaging.
Python 3.13 AST differences require the existing explicit adapter or a distinct
profile. `python -O`, `PYTHONOPTIMIZE`, implicit package upgrades and fallback
to another source kernel are prohibited.

Reuse existing `be_replay` source preparation, evidence readers, transport,
completed-stage validation and supervised native execution where their exact
contracts fit. `prefix2_runtime.py` is discovery-only; it never supplies
native acceptance. `runtime_origin.py` reconstructs a sealed historical
namespace; it must remain isolated and cannot replace an unrelated folder.

Existing `linux_supervisor.py` distinguishes per-process RLIMIT_AS/CPU and
sampled group observations from kernel cgroup limits. The new outer worker
uses Linux cgroup/container CPU, charged-memory, PID and filesystem quotas
where available, while preserving the inner source profile. It must record
which enforcement actually exists. Missing required seccomp/cgroup features
fail closed; Windows fixtures do not establish Linux enforcement. Local
numerical execution therefore uses the same Linux image, not a silent
Windows-native substitute.

## 3. Batch request and immutable dispatch mapping

Group only homogeneous image/profile/resource tasks in one Batch array.
The immutable array manifest maps task index and logical bundle index to full
dispatch ID, JobSpec, task kind and output namespace. A physical task may
execute at most 32 independent ready logical jobs sequentially, each retaining
its own claim/attempt/receipt. Default array cap 64 physical tasks; the parallelism
limit is the smaller of admitted slots, verified quota and resource tokens.
The plan can contain thousands of jobs without thousands of simultaneously
provisioned machines.

Set native `maxRetryCount=0`; the application owns retries and accounting.
Set explicit task/runnable timeouts and limits. Provider scheduling and
queued time are not an application lease. On actual start the worker must
claim its exact current dispatch and pass the campaign/deadline fence before
loading numerical code. A stale queued task exits without a claim; its boot
cost still belongs to the reservation. Batch retries/timeouts do not enforce
one global 12 hour campaign. [Job execution](https://docs.cloud.google.com/batch/docs/create-run-job),
[retries](https://docs.cloud.google.com/batch/docs/automate-task-retries),
[timeouts](https://docs.cloud.google.com/batch/docs/set-timeouts).

Provider IDs are deterministic from the immutable dispatch-group ID; a
create timeout is reconciled with GET before retry. A409existing response
must match the exact request digest. The ledger outbox, not a Firestore
transaction callback, performs provider calls. Unknown creation retains all
money/resource liability until a terminal observation establishes what ran.

## 4. CPU packing and verified throughput

The inspected workloads primarily use exact rational Python computation,
independent forests/panels and native full replay. Add CPU capacity by
process-level parallelism. No GPU is assumed to accelerate Fraction arithmetic
or proof checking. One CPU-bound Python child receives one logical vCPU
unless its frozen profile explicitly permits additional processes/threads.

Initial machine candidates include x86 N2 high-CPU/standard reference shapes
and C4D, C4 and C3D where region, quota, price and the runtime profile permit.
N2 is not presumed fastest. Candidates are selected
from a current region-specific allowlist and price quote. The startup pilot
compares their **verified work per PLN and elapsed hour**. A machine SKU,
zone or physical packing choice is attempt/deployment metadata; it does not
change a mathematical statement. It can vary within a frozen profile only
if image architecture, logical caps, arithmetic environment and source policy
remain identical. Otherwise a new JobSpec is required.

For every node, reserve 1 vCPU and 2 GiB for OS/agent/shared services. A task's
wrapper allowance is 128 MiB in addition to its enforced child-memory cap.
Admit no more than

```
min(floor((node_vcpu-1)/task_vcpu),
    floor((node_memory-2 GiB)/(task_memory+128 MiB)),
    floor(node_scratch_budget/task_scratch_limit))
```

concurrent tasks. The scheduler also enforces campaign-wide CPU, RAM, disk,
provider-slot and money tokens. Sum reservations before dispatch, including
queued instances that may boot concurrently. Do not allocate a native
multi-process profile as though it were single-process. Use an outer charged
memory ceiling, not sampled RSS, for admission safety.

Default source/transport bounds are 1 GiB per blob and 16 MiB per manifest, with
any stricter native bound taking precedence. Node boot disk is sized from
OS+image+one shared immutable source cache+all simultaneous scratch budgets;
64 GiB is the first quoted candidate, not an unmeasured assurance that every
family fits. Boot disks use auto-delete. Source bundles are downloaded once
per digest per node, verified fully, then exposed read-only. Every attempt
has private mutable work/checkpoint/output paths.

## 5. Calibration and adaptive work sizing

The 75 PLN startup phase funds only bounded compatibility, recovery and
calibration work plus its control/storage/cleanup charges. First pass:
one representative admitted job from each of discovery, native replay,
Fourier/resource evaluation and transport-heavy readback. Start at one
worker, then 2, 4 and 8 only if memory, CPU, storage and verification results remain
within budget and the planned sample limit. Do not spend the main budget to
discover whether the runtime is compatible.

Record p50/p95 wall and CPU time, charged memory, output/checkpoint bytes,
upload/seal time, complete native replay time and rejected/incomplete work.
The objective is complete freshly verified cells/forests/scopes per elapsed
hour and per PLN. Raw visited nodes, producer-only speed and a historical
PASS are diagnostic counters, not the performance objective.

The adaptive policy is frozen by digest before execution:

* Target 300 seconds of useful producer work per chunk; permitted range 60--900.
  Bundle tiny independent native jobs to amortize process/source overhead,
  without changing any individual full acceptor or receipt boundary.
* Every 60 seconds update an EWMA with weight 1/4 for completed comparable units.
  Choose the next bundle as the largest integer number of those units whose
  predicted work is at most the target, subject to count/byte/memory caps.
  Tie-break by sorted JobSpec/root/path identity.
* Split an eligible untrusted search subtree when its estimated remaining
  work exceeds twice the target and a licensed strict interior split exists.
  Retain both child boxes. Otherwise leave the native unit intact.
* Choose target within the permitted range so checkpoint+transport overhead
  is at most 5 percent when possible. If that is impossible, record the
  overhead and keep the bounded target; do not invent a faster proof rule.
* On preemption/lost work reduce target by half, floor 60 seconds. After four
  consecutive successful chunks with overhead above 5 percent, double target,
  cap 900 seconds. Never extend beyond remaining global time minus shutdown
  and publication reserves.

Physical batching and telemetry choices do not change the frozen mathematical
scope. Search cuts, node limits, precision and algorithm families must remain
within the frozen search/execution policy; adaptation cannot raise native
`LIMIT` or introduce an unlicensed lemma. Profiles that only support completed
stages cannot pretend to checkpoint arbitrary partial numerical state.

Schedule ready critical dependencies first, then keep all admitted CPU slots
busy with independent work. Reserve at least one verifier slot, and grow the
verifier share when produced-but-unverified work exceeds twice its measured
15 minute replay capacity. Throttle producers before the verifier queue grows
past the remaining deadline. Permit no CPU/RAM oversubscription to make an
attractive worker count. A larger allocation is useful only if verified
throughput increases. At the end of the campaign prioritize completing and
verifying existing candidates over starting long new forests.

Spot is allowed for checkpointable untrusted discovery after its recovery
pilot passes and a separately confirmed nonzero Spot quota exists. The current
read-only preflight has zero such quota, so the initial activation is standard
VMs only. Full native replay and nonresumable units initially use standard
VMs. Preemption/retry waste, boot, queued-late boot and lost work are charged
to the same campaign. Switching procurement does not grant extra time.

## 6. Two separate planned budgets

The authorized policy is exact integer grosz:

| Ledger | Limit | Scope |
|---|---:|---|
| startup |7500 (75 PLN) | setup/tests/calibration and their overhead |
| main |55000 (550 PLN) | one 43200 second window plus reserved closure/retention |
| combined |62500 (625 PLN) | sum, never an additional allowance |

Unused startup money is not silently added to main. Resuming does not reset
either ledger. The main all-in average ceiling is 550/12=45.833333...PLN/hour;
it is not a VM price quote or permission to spend that amount on VMs alone.

Read-only account preflight is recorded, with identifiers redacted, in
[`verification/cloud-preflight.json`](../../verification/cloud-preflight.json).
It observed SDK 590.0.1, billing enabled, global CPU quota 100 with usage 0,
regional N2/CPU quota 200 in europe-west 4 and 100 in europe-central 2, and
PREEMPTIBLE_CPUS quota 0 in both. Thus Spot is disabled in the initial plan;
it cannot be used in a price/capacity forecast without a separately acquired
quota change. Global 100 is the current upper limit, not a capacity promise.
Batch, Cloud Run, Firestore, Scheduler and Artifact Registry APIs were not
enabled. No services or VMs were changed. A pre-existing terminated VM was
observed; its identity and disks are outside campaign ownership and its
residual storage cost has not been audited. Revalidate this snapshot at
activation; it is not a price quote or permission to use that VM.

Before paid admission, freeze a `CostQuote` with exact SKU IDs, region,
procurement, effective/expiry times, billing units/rounding, currency,
account/list-price basis, outward currency/tax factor and artifact limits.
Prefer actual PLN account prices. If converting USD, use the account's
published pricing conversion, round upward and include an uncertainty
reserve; an internet spot FX rate does not establish the billed PLN rate.
Account prices and tax treatment are explicit inputs, never guessed.
[Pricing APIs](https://docs.cloud.google.com/billing/docs/how-to/get-pricing-information-api),
[catalog fields](https://docs.cloud.google.com/billing/v1/how-tos/catalog-api),
[billing currencies](https://docs.cloud.google.com/billing/docs/resources/currency).

No machine-count promise or fabricated current PLN SKU rate is included in
this specification: the account/region quote has not been acquired. An expired,
missing or unsupported quote blocks paid dispatch. The startup plan must
reserve its own worst-case total before it runs. Quotes may be refreshed
within the same campaign, but cannot increase the authorized budgets.

Each quoted conservative rate bound must cover its CostLine's entire
liability horizon, including reserved cleanup and retention. A current price
fetched just before submission does not alone bound a longer lifetime. If
the horizon is unsupported, shorten admission or acquire an explicit bounded
quote first. Refreshing prices never releases an unknown liability or assumes
favorable future FX. Provider price/outage uncertainty remains an explicit
planning reserve, not an invoice guarantee.

Reserve every cost class: VM CPU/RAM/provisioning minimums, boot/scratch disks,
Spot/standard retries, image build/storage/download, GCS data/operations and
retention/soft-delete, network/egress, Firestore reads/writes/indexes/storage,
Cloud Run requests/CPU/memory, Scheduler, logs/monitoring and teardown. Batch
does not add a separate service charge, but its underlying resources and
ancillary services do. [Batch pricing](https://cloud.google.com/batch/pricing),
[Firestore billing](https://firebase.google.com/docs/firestore/pricing).

Admission is one atomic money/resource reservation:

```
observed_charged_upper + all_unreleased_reservations
  + new_request_worst_case + still_required_closure_reserve <= phase_limit;
startup_total_upper + main_total_upper <=62500.
```

The upper includes the full permitted lifetime of a dispatch plus boot,
retry policy, artifacts and cleanup. Never deduct expected discounts/free
tier/credits unless their availability is itself frozen and conservatively
bounded. Unknown create/cancel/charge outcomes retain their full reservation.
Release liability only against reconciled actual resource lifetimes and
conservative metered bounds, not a delayed billing dashboard. Ancillary
service operation counters have their own quotas and reservations.

The controller optimizes concurrency to use the available compute envelope;
it does not deliberately leave affordable ready CPU idle. Keep a nonzero
quoted teardown/unknown-outcome reserve and reserve the selected retention
horizon before dispatch. The policy must contain actual amounts rather than
an unspecified percentage. The fixture project is intentionally unarmed
until those quote-backed values are supplied.

Billing alerts are secondary monitoring. Current Google spend-cap budgets
cover selected API services, and the published list does not currently cover
Compute Engine/Batch. Enforcement also has delay and billable overages.
Do not claim that the 625 PLN operational policy is an absolute invoice cap
under provider outages, tax/FX changes or unrelated project spending.
[Budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets),
[current spend-cap scope](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps).

Use a dedicated project/campaign resource scope and inventory pre-existing
paid resources. The policy governs resources admitted by this system; it
cannot control an unrelated administrator's spending. Retained cloud proof
data still costs money after VMs stop. The quote and shutdown report state
the funded retention horizon, byte cap, export destination and residual
liability; longer retention requires a separate explicit allowance.

## 7. One absolute 12 hour deadline and independent shutdown

Startup is independently bounded too. Its phase control has one immutable
`startup_t0`, `startup_deadline=startup_t0+7200s`, phase namespace `startup`
and its own 7500 grosz ledger. Set this activation before the first paid setup
operation; `main_t0` may still be null. Setup/API/image operations have
explicit bounded counts, byte caps, 300 second request timeouts and reserved
liability; serverless services have min instances 0. Creating the watchdog
itself cannot logically depend on an already running copy of itself, so
this bounded bootstrap is distinguished from numerical VM provisioning.

Before the first paid startup pilot VM, the startup stop manifest must be
durable, the independent watchdog armed and tested, and the phase-specific
absolute VM template installed. Use startup dispatch cutoff at−300 seconds,
checkpoint/hard-stop/VM termination at−180/−120/−90 seconds relative to its
own deadline. Queued/provisioning pilots and boot costs are included. No
retry or new CLI invocation extends startup. If watchdog arming fails, no
pilot VM is submitted. The 7200 seconds is a maximum bootstrap allowance,
not a completion estimate or a second main window.

Startup must reach verified no-active-compute closure before main activation.
Reuse compatible pinned service/image artifacts, not startup leases or money.
Each stop manifest/ownership predicate includes the phase, so an old startup
watchdog cannot delete a later main resource. Persistent control/storage costs
are accounted across the phase boundary; they are not dropped or double
credited. Only a successful explicit main activation grants its one 12 hour
window. The watchdog and cleanup protocol below applies to both phases.

Main activation order is mandatory:

1. Validate startup gates, quote, IAM, quota and cleanup capabilities.
2. CAS the campaign from planned to arming with main T0=coordinator UTC and
   deadline=T0+43200 seconds, before the first paid main resource is created.
3. Create an immutable GCS stop manifest with `ifGenerationMatch=0`, containing
   full campaign/project IDs, T0/deadline, controller generation, exact region/
   zone allowlist, resource-name prefix, provisioning identities and cleanup
   rules. Read back and pin its generation/digest. A crash never resets T0.
4. Arm and verify the independent watchdog schedule and campaign-owned fixed
   VM template. Only then set admission active. If arming fails, remain
   stopped; elapsed time and any cost are not refunded by a fresh deadline.

Set `dispatch_cutoff=deadline-900s`, `worker_checkpoint_at=deadline-180s`,
`worker_hard_stop_at=deadline-120s`, and the VM absolute termination timestamp
to `deadline-90s`. These margins are policy values, not extra computation
after 12 hours. Worker startup checks the current campaign and absolute time;
timeouts are additionally clamped to the remaining permitted lifetime.

Use a campaign-owned immutable Compute Engine instance template with
`properties.scheduling.terminationTime` and
`instanceTerminationAction=DELETE`; auto-delete its boot disk. Batch refers
to this template through its documented `instanceTemplate` field. Do not
invent `Batch.InstancePolicy.scheduling`. Template and Batch service-account
settings must match. The startup pilot inspects actual VMs to confirm the
absolute setting. [Batch VM templates](https://docs.cloud.google.com/batch/docs/create-run-job-vm-template),
[template schema](https://docs.cloud.google.com/compute/docs/reference/rest/v1/instanceTemplates/insert).

An absolute timestamp is used because `maxRunDuration` restarts its clock
when a VM is restarted/replaced. Provider automatic termination may begin
after the configured timestamp, so it supplements rather than replaces
the earlier worker stop and watchdog. [VM run-time limits](https://docs.cloud.google.com/compute/docs/instances/limit-vm-runtime).

The watchdog runs every minute with a separate service account, service,
scheduled trigger and frozen stop-manifest ref. It does not depend on the
CLI, controller availability or Firestore. Its deployment config includes
the exact project/region/resource scope and deadline as a read-only fallback
if GCS is unavailable. A missing/unverifiable manifest fails closed: no new
admission; owned resources are reconciled using the previously pinned scope.

At `dispatch_cutoff` close new dispatch, while already running work may
continue toward checkpoint/hard-stop times. At `worker_checkpoint_at` request
the final checkpoint; at `worker_hard_stop_at` kill remaining numerical work.
An early manual/budget stop begins this drain immediately, bounded by 60 seconds
and the earlier absolute deadline. It does not cancel healthy work 15 minutes
early merely because new-dispatch admission closed.

An early stop is also written independently as an authorized immutable GCS
cancellation record under the campaign's stop prefix, including epoch,
reason, actor and initial stop-manifest digest. Only controller/operator
stop identities can create these records. Immediately invoke the watchdog;
its next scheduled tick also scans this prefix. If Firestore is down, the
stop record still closes watchdog-side admission and initiates cleanup.
If both control stores are unavailable, the worker lease expiry and frozen
absolute VM deadline remain the fallback; report the unconfirmed stop.

On early stop or the final hard-stop stage, controller and watchdog:

1. close admission, increment cancellation epoch and stop creating dispatches;
2. request checkpoint/termination and cancel every owned queued/running Batch
   job, including provisioning jobs whose numerical task never started;
3. repeatedly inspect Batch jobs, their actual MIG/VM UIDs and boot disks;
   wait for cancellation operations, then delete residual owned resources
   according to the exact manifest scope;
4. reconcile unknown create/cancel requests until platform observations show
   no active/provisioning compute or chargeable orphan disks;
5. publish a shutdown receipt distinguishing request sent, platform confirmed,
   verified no active compute, and cleanup failure. Preserve logs/results.

The initial stop manifest cannot contain future VM UIDs. It freezes a full
campaign ownership predicate: dedicated project/allowed zones, immutable
template identity, campaign provisioning service accounts, deterministic
parent Batch job/request namespace and full campaign metadata. The watchdog
lists provider jobs and their derived MIG/VM relationships, checks this
predicate and records actual resource UIDs before deleting them. It works
even when create succeeded without a ledger acknowledgement. New observed
resources extend its immutable observation inventory, not the initial scope.

Labels are search hints. GCP label values cannot hold arbitrary full IDs;
if a shortened digest is used, deletion additionally checks full ownership
metadata, immutable manifest membership and actual resource UID. Never delete
another campaign by matching a truncated label alone. Cancellation is not
proof of deletion, and stopping a VM leaves disk/storage liability.
[Cancel Batch jobs](https://docs.cloud.google.com/batch/docs/cancel-job),
[delete Batch jobs](https://docs.cloud.google.com/batch/docs/delete-job).

After the deadline, no paid numerical retry or verifier can start. Already
committed receipts may be assembled locally/read-only, and existing candidate
bytes may be imported for a future explicitly funded verification campaign.
Budgeted cleanup/export/control requests can continue within the reserved
closure allowance; they never reopen numerical admission. A late worker
cannot regain completion authority. Provider-control outages may delay
cleanup and cause billed overrun; report `cleanup_failed` and unreleased
liability rather than falsely asserting shutdown or a guaranteed invoice cap.

## 8. Operational IAM matrix

Use separate user-managed accounts and short-lived credentials; no service
account JSON keys in artifacts or worker images. The following is the minimum
functional matrix, implemented with resource-scoped roles/custom permissions:

| Principal | Allowed | Explicitly denied by design |
|---|---|---|
| operator/deployer | freeze/activate authorized campaign; deploy pinned images/IAM | no automatic new paid campaign |
| controller | Firestore ledger transactions; read/verify artifacts; create/cancel/read owned Batch jobs; act as selected worker SAs; write catalog/stop manifests | arbitrary project administration; implicit trust upgrades |
| producer worker | invoke producer claim/heartbeat/complete endpoints; read selected source/input artifacts; create candidate/checkpoint objects | Firestore access; receipt sealing; overwrite/delete; verifier role |
| verifier worker | invoke verifier endpoints; read exact candidates/sources/dependency receipts; create verifier-output objects | producer mutation; direct coverage acceptance; arbitrary database writes |
| watchdog | read pinned stop manifest; inspect/cancel owned Batch; inspect/delete owned residual MIG/VM/disks; emit shutdown receipt | numerical dispatch; mathematical verification; Firestore dependency |
| scheduler invocation SA | invoke only scheduled controller/watchdog routes | access to numerical artifacts or ledger |
| archive/GC maintainer | generation-checked export/retention operations under policy | arbitrary live/sole-copy deletion |

Cloud Run invocations use audience-bound Google ID tokens and
`roles/run.invoker` on the receiving service. Application handlers separately
authorize principal, task kind, campaign and dispatch; service-level invocation
is not permission to call every admin route. Firestore access is limited to
the controller (`roles/datastore.user` or a narrower reviewed custom role);
workers have no database credentials. [Service authentication](https://docs.cloud.google.com/run/docs/authenticating/service-to-service),
[Firestore roles](https://docs.cloud.google.com/iam/docs/roles-permissions/firestore),
[Scheduler authentication](https://docs.cloud.google.com/scheduler/docs/http-target-auth).

Batch permissions such as job creation/cancellation are project-scoped
authority; an application prefix check is not an IAM restriction. Do not
assume Batch or MIG IAM conditions support the same resource attributes as
Compute instances. Dedicated-project isolation plus the application ownership
predicate limits the operational scope. Validate only actually supported
conditions. [Supported IAM resource attributes](https://docs.cloud.google.com/iam/docs/conditions-resource-attributes).

GCS sources, candidates, verifier outputs and catalog/stop manifests use
separate buckets or enforceable IAM conditions. Producer upload permission is
create-only; controller catalog writes use generation CAS. Exact custom
Batch/Compute cleanup permissions and IAM conditions are validated in startup
negative controls. A leaked verifier identity still cannot convert an
unsupported claim into an allowed trust-profile receipt.

## 9. Deployment acceptance gates

Before main activation, the startup allowance must establish: exact image and
source compatibility; unoptimized Python guard; complete native controls;
filesystem isolation; actual cgroup/timeout enforcement; same ledger
interleavings as local; no duplicate lease publication; checkpoint recovery
after forced worker loss; GCS generation races; unknown-create reconciliation;
independent watchdog with controller/Firestore unavailable; queued-late
startup refusal; absolute VM deletion; and no active compute/orphan disk
after a deliberately stopped bounded pilot.

These are planned tests, not completed claims. Failure closes admission.
The pilot uses its startup ledger and cannot borrow the 550 PLN main allowance.
No full-proof completion time, speedup, specific worker count or final PASS
is promised before measured verified throughput and the remaining workload
are known.
