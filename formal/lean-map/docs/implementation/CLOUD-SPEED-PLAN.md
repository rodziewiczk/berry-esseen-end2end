# Cloud speed plan and bounded pilot

Observation: 25 October 2026, approximately 20:42–20:54 Europe/Warsaw.
No VM was started, created, stopped or deleted. No quota, API, IAM or billing
setting was changed during that inventory. Account identities and IP addresses
are excluded. The separately authorized single-VM activation below happened
later; the six-machine fleet has not been activated by this note.

This is a deployment proposal, not an implemented cloud runner or proof PASS.
The user's current allocation is at most **1000 PLN of existing eligible
promotional credits, with 0 PLN cash authorization**. The user explicitly
attested approximately 1000 PLN remains until January 2027 and authorized
autonomous CLI configuration/activation. Plan 300 PLN overnight, with a
separate 350 PLN ceiling covering setup, run and cleanup, leaving a large
margin against the declared balance. This is user-attested funding, not a
CLI-verified exact balance. The earlier 75/550 PLN examples are superseded;
see [credit policy](CLOUD-CREDIT-POLICY.md).

## 1. Limits and existing resources actually observed

The Cloud Quotas metric is `compute.googleapis.com/cpus_per_vm_family`,
quota ID `CPUS-PER-VM-FAMILY-per-project-region`; C4/C4D are dimensions of
this quota, rather than standalone legacy regional Compute quota fields.
The four relevant dimension values are:

| Region | C4D vCPU limit | C4 vCPU limit | Ordinary regional CPU limit | Spot CPU limit |
| --- | ---: | ---: | ---: | ---: |
| europe-west4 | 24 | 24 | 200 | 0 |
| europe-west1 | 24 | 24 | 200 | 0 |

The common `CPUS-ALL-REGIONS-per-project` limit is **100 vCPUs**. All observed
running CPU usage is zero. These limits apply together; regional limits cannot
be added to bypass the global limit. Readback and provenance are recorded in
[sanitized observations](../../verification/cloud-backend-readonly.json).
[Cloud Quotas inspection](https://docs.cloud.google.com/docs/quotas/gcloud-cli-examples).

The existing machine is a stopped, private `c4d-standard-16` in
`europe-west4-a`, without an external IPv4/IPv6 address. Its attached boot disk
is 250 GiB Hyperdisk Balanced, provisioned at 3000 IOPS and 140 MiB/s. Its
recorded source image is Ubuntu 24.04 amd64 from 24 October 2026. This is
image provenance, not evidence of the current guest's Python/runtime state.
`automaticRestart=false`; its existing absolute termination time is
`2026-10-26T13:00:51Z`, later than the manuscript target. It therefore needs
explicit campaign adoption and a suitable shutdown policy before reuse.

A router/Public NAT in `europe-west4`, automatic NAT address allocation and
an IAP TCP/22 ingress rule already exist. No west1 NAT was observed. The NAT
IPv4 count is not established by this check; do not infer zero networking
charges from the absence of separately reserved addresses. Existing disk
capacity alone is approximately 80.69 PLN per catalog month of 744 hours,
or 2.60 PLN per 24 hours, before any other retained resource.

## 2. Proposed allocation: 96 vCPUs, six machines

The machine-type catalog lists the following shapes in all three checked
zones of each region: west4-a/b/c and west1-b/c/d. A catalog entry and quota
are not a reservation or evidence of free physical capacity.
[Machine families](https://docs.cloud.google.com/compute/docs/general-purpose-machines).

| Per region | vCPUs | RAM | Count |
| --- | ---: | ---: | ---: |
| c4d-standard-16 | 16 | 62 GiB | 1 |
| c4d-standard-8 | 8 | 31 GiB | 1 |
| c4-standard-24 | 24 | 90 GiB | 1 |
| Total for both regions | **96** | **366 GiB** | **6** |

C4 supports a 24-vCPU shape, so using one C4-24 rather than C4-16 plus C4-8
per region reduces fleet size from eight to six at the same CPU/RAM price.
C4D fills each 24-vCPU bucket with 16+8. Reuse the existing C4D-16 only after
qualification. The remaining 4 global vCPUs are headroom, not an instruction
to launch another VM. Current Spot quota excludes a Spot-dependent plan.

This is the largest allocation using only these four verified 24-vCPU
buckets. It is not a claim that these CPUs are globally fastest, that 96
physical cores are available, or that more resources always improve useful
throughput. vCPUs are hardware threads; measure the actual process throughput
and SMT placement rather than assuming linear scaling.

If a zone lacks capacity, retry a catalogued zone in the same region using
the same family/shape and exact runtime profile. An unknown create response
retains the original resource/quota/cost reservation until reconciled; never
submit a second 24-vCPU allocation in that bucket on the assumption the first
failed. A different family or region requires its own inspected limits and
rate/profile binding. Do not silently request quota increases.

## 3. Current public prices, with their exact units

The Cloud Billing Catalog API was read through existing OAuth credentials,
without creating an API key or enabling a service. All seven catalog pages
were traversed. The extracted public SKU record is
[cloud-public-prices-pln.json](../../verification/cloud-public-prices-pln.json).
Prices have effective time `2026-10-25T07:00:00Z` and catalog USD conversion
rate `3.84255`. They are public list prices, not a negotiated account quote,
tax calculation or proof that a particular credit covers the charge.
[Catalog API units, pagination and currency conversion](https://docs.cloud.google.com/billing/docs/reference/rest/v1/services.skus/list).

| Region/family, 24 vCPUs | CPU PLN/vCPU h | RAM PLN/unit h | RAM unit | CPU+RAM PLN/h |
| --- | ---: | ---: | --- | ---: |
| west4 C4D, 93 GiB | 0.131948171 | 0.014103530 | GB | 4.57510626 |
| west4 C4, 90 GiB | 0.139801575 | 0.015888559 | GiB | 4.78520811 |
| west1 C4D, 93 GiB | 0.138369456 | 0.014789901 | GB | 4.79775672 |
| west1 C4, 90 GiB | 0.146605271 | 0.016661804 | GiB | 5.01808886 |
| Total | | | | **19.17615996** |

The C4D RAM SKU is `GBy.h`, while C4 is `GiBy.h`. For C4D, charge
`GiB × 2^30 / 10^9` GB; multiplying the decimal-GB price by the GiB count
would understate the result. CPU+RAM for 12 hours is about **230.11 PLN**.
The historical 17.91 PLN/h estimate is not the current quote.

For a concrete sizing illustration, reuse the 250 GiB disk and provision at
most one 64 GiB boot/work disk per other VM, provided measured source cache
and scratch bounds fit. That is 378 GiB in west4 and 192 GiB in west1.
Current non-confidential Hyperdisk capacity rates are respectively
0.3227742 and 0.3381444 PLN/GiB month. The catalog base-unit conversion is
744 hours for this price version, yielding approximately **0.25125 PLN/h**.
This illustration assumes no excess provisioned IOPS/throughput; they are
separate priced dimensions, not free capacity inferred from disk size.
[Hyperdisk pricing](https://cloud.google.com/compute/disks-image-pricing).

Public NAT's published rate is USD 0.0014 per assigned VM hour, USD 0.005 per
NAT external IPv4 hour, plus USD 0.045 per processed GiB. Six VMs and two
NAT IPv4 addresses would add about **0.07070 PLN/h** fixed charges when
converted using the observed catalog FX. The two-address assumption still
requires actual network sizing and a PLN SKU/account check.
[NAT and network rates](https://cloud.google.com/vpc/network-pricing).

Thus this particular fixed compute/disk/NAT illustration is approximately
**19.50 PLN/h**, or **233.98 PLN per 12 hours**. It is **not an all-in cap**.
A complete admission quote must additionally reserve bounded transfer/NAT
bytes, regional copies, storage operations, controller/watchdog, logging,
build/registry if used, provisioning/retries/overlap, cleanup, taxes if
applicable, credit exclusions and retention after compute stops. Avoid an
unbounded per-iteration remote log stream. A current quote must conservatively
cover every admitted liability horizon; freshness at submission alone is
insufficient. Rate/FX uncertainty needs a reserve, not an invented guarantee.

## 4. Dispatcher and asymmetric memory packing

Keep the source mathematical modules unchanged. A qualified producer or
verifier is a fresh single-process execution unit with exact source,
environment, inputs and policy bindings. Python Fraction work scales through
independent processes; do not multiply native thread/process counts inside
an already fully packed VM. Source assertions require unoptimized Python.

Reserve 1 vCPU and 2 GiB per node for its OS/agent. With the architecture's
128 MiB wrapper allowance, the admissible concurrent child count is:

```
min(vcpu - 1,
    floor((memory_gib - 2) / (child_memory_gib + 0.125)),
    floor(scratch_budget / child_scratch_limit))
```

This gives at most **90 child slots** across six machines, before memory and
I/O constraints. For 4 GiB children the memory limits reduce this to 84;
for 8 GiB children, to 40. These are admission examples, not measured family
requirements. Never use a fleet-average memory figure to place a job that
does not fit an 8-vCPU/31-GiB node. A shared immutable source cache is counted
once per node, while private work directories and concurrent charged memory
are counted per child. No swapping or RAM oversubscription is a speed policy.

Maintain a deterministic ready heap and reverse dependency index; update only
dependents when a matching accepted receipt arrives. Pop critical dependency
work first, then the longest predicted ready units. Assign each popped unit
to the feasible idle node with the smallest predicted verified finish time
using family-specific calibration. Do not give a permanent proof family to
one region while idle compatible slots exist elsewhere. Mathematical scope
or search splitting requires the existing typed rule; physical placement and
bundling do not change scope. A worker finishing a unit pulls another ready
unit, so unequal hard panels cannot strand the rest of the fleet.

Use the already specified 60–900 second chunk policy, initial target 300
seconds, only on licensed independent units or resumable search subtrees.
Retain both children of every mathematical split. Bundle short jobs without
merging receipt boundaries. A native complete forest remains complete: a
cutoff or partial replay cannot be relabeled accepted.

Producers and complete verifiers have separate queues and leases. Start with
roughly one verifier slot per four active slots, then allocate by measured
producer/replay cost; this is placement, not a trust shortcut. Keep at least
one verifier runnable. When unverified work exceeds twice the measured
15-minute verification capacity, shift slots toward verification and throttle
new production. Cache shared source/data by exact digest per node; stream
large transfers and hashes rather than loading every archive in every worker.
Checkpoints and candidates publish immutably before fenced ledger completion.

## 5. Qualification and the publication target

No guest has yet been started for these checks. Before scaling, run a bounded
single-node compatibility/recovery/throughput pilot after allocation and shutdown
gates pass. Check actual CPython 3.12, dependency/source hashes, assertion
behavior, all required native replay controls, charged peak memory and child
cleanup. Compare C4 and C4D using the same representative ready units. Test
one process, then physical-core and SMT concurrency; measure complete
freshly verified units/hour and useful critical-path progress, not merely
visited nodes or a producer's historical receipt.

Keep all ready work busy within the verified limits once this pilot passes;
do not reduce parallelism merely to minimize cost. Conversely, do not buy
idle capacity while required adapters/dependencies are absent. The existing
local Farkas pilot and one ordinary native COUNT adapter are not a full-proof
cloud dispatcher or complete root theorem implementation.

Freeze one absolute campaign deadline and earlier dispatch cutoff. Do not
reset either on CLI resume, retry or zone fallback. The desired publication
time is 26 October 2026 at 08:00 Europe/Warsaw; it is a target, not a claim
that unknown proof work will finish. Reserve time for complete verification,
artifact export and PDF compilation. Existing VM metadata is not an armed
campaign watchdog. Native absolute VM termination, an independently checked
cloud watchdog, safe early-stop signaling, ownership reconciliation and
cleanup receipts must work before scaling. Billing alerts are not that stop
mechanism. Pending creates, boot costs and retained disks remain liabilities.

The user's ordinary-compute authorization is already recorded; do not request
it again merely because this read-only note did not activate resources. The
next concrete gates are a synchronized source-bound runnable task set, a
conservative 350 PLN allocation and a tested bounded shutdown path. New
services with unknown credit coverage remain excluded. Publication must
distinguish accepted proof coverage from
runtime completion and from successful cleanup.

## 6. Bounded single-VM pilot, later on 25 October

After explicit authorization for a pilot with a 20 PLN liability reservation,
the existing C4D-16 was adopted and started at approximately 20:23 UTC. Its
absolute provider stop was frozen at **25 October 2026 21:04:16 UTC**, action
STOP, automatic restart disabled. Existing user data and the 250 GiB disk are
preserved. A guest systemd shutdown timer uses the same absolute time, and a
separate local watchdog reconciles/stops this exact adopted instance. No new
VM, disk, API or billing service was created for this pilot. Stopped disk
retention continues to cost about 2.60 PLN/day and remains an accounted item.

Actual guest: CPython 3.12.3, x86_64, 16 logical CPUs, approximately 60.8 GiB
RAM. The native supervisor passed all 12 applicable Linux process/resource
tests; its Windows-specific aggregate-memory test was skipped honestly.
The completed native n6 pilot used only copied source bytes, constructed a
new seven-root forest, replayed every leaf and ran all 24 corruption controls.
Its result is **conditional SCOPED_COUNT_PASS**, never a full-proof PASS.
The actual Linux runtime and source bytes matched before/after. See
[sanitized Linux evidence](../../verification/supervisor-linux-pilot.json).

An initial runtime inventory correctly refused Ubuntu's standard symlinks;
it produced no accepted result. The next isolated source bundle pinned link
chains and resolved target bytes and repeated the complete construction from
scratch. The final inventory additionally rejects linked parent directories;
all three related tests passed on Linux before the representative batch.

The representative measurement batch contains 15 fresh jobs: the middle panel
of each n6–n9/B0/BN/B2 group, plus three known short controls. It uses at most
15 direct native children, conservative 2 GiB native limits, separate wrapper
and coordinator parsing allowances, and a bounded coordinator address-space
limit. It shares one actual Linux runtime inventory before/after the batch,
not a Windows profile or an arbitrary digest label. Every result remains
provisional until complete child cleanup and runtime/source postchecks.
`LINUX_MEASUREMENT_SEALED` alone does not claim 15/15 success; completed and
unresolved counts must be reported separately. The pilot's deadline is not
extended by retries, later bundles or the batch.
