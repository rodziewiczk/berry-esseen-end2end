# Protocol, exact types and identities

Status: normative implementation contract. The 29 Lean source modules at the
mathematical checkpoint remain unchanged. These formats describe their future
runtime inputs, proof artifacts and independently checked outputs. A valid
JSON document is not an accepted mathematical certificate.

## 1. Protocol layer and exact codec

The protocol version is `be.arch/1`; the canonical instance codec is
`RJSON-BE/1`. Schemas use the explicitly selected [JSON Schema 2020-12
core](https://json-schema.org/draft/2020-12/json-schema-core) and
[validation vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation).
`protocol.schema.json` contains the closed type definitions; the other schema
files are typed entrypoints. Their `https://be-arch.invalid/v1/` IDs are
logical identifiers resolved from an offline registry. They are not hosted
services and must never trigger a network fetch.

Canonical instance bytes are defined as follows:

1. Decode strict UTF-8 without a BOM. Reject duplicate object keys before
   constructing a dictionary; reject JSON numeric tokens, NaN/Infinity and
   trailing data. Only objects, arrays, strings, booleans and null are allowed.
2. Keys and string values contain only printable ASCII U+0020..U+007E.
   Non-ASCII strings are rejected, rather than normalized. Human translated
   display text belongs in the UI or a separately referenced text artifact.
3. Validate the exact versioned schema with unknown fields rejected. Check
   the semantic type invariants below before sealing an object.
4. Sort object keys by ascending ASCII byte value. Preserve array order.
   Emit no whitespace, indentation, terminal newline or BOM. Emit strings
   with `"` and `\` escaped; emit every other allowed character literally,
   including `/`. Emit booleans/null as their lower-case JSON literals.
5. Persist only these canonical bytes. For sealed input, re-encoding must
   reproduce the input byte for byte. A separate interactive import may
   canonicalize transport JSON before sealing; it must not silently alter an
   already content-addressed artifact.

This restricted codec is intentionally narrower than
[RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785). It does not adopt
ECMAScript floating-point serialization or accept arbitrary Unicode.
Arrays representing sets must additionally follow the schema's specified
sort order and contain no duplicates. Absent and null are different: null is
allowed only by an explicit nullable field; required fields cannot be omitted.

JSON Schema documents themselves use ordinary JSON keywords/numbers. The
no-number codec restriction applies to protocol **instances**, not schema
source files.

## 2. Primitive mathematical and runtime types

| Type | Canonical instance | Additional semantic check |
|---|---|---|
| Natural | `"0"` or `[1-9][0-9]*` | Parse into arbitrary-precision integer; apply declared size limits |
| Positive natural | `[1-9][0-9]*` | Greater than zero |
| Integer | `"0"` or optional minus followed by nonzero decimal digits | No plus sign, `-0`, whitespace or leading zeros |
| Rational | `{"den":"1000","num":"409"}` | den>0, gcd(abs(num),den)=1; zero is exactly 0/1 |
| Closed interval | `{"lower":rational,"upper":rational}` | lower<=upper using exact cross-products |
| Bound | relation `le` or `lt`, rational value | Relation is part of the claim; equality survives a strict failure test |
| Digest | `sha256:` followed by 64 lower-case hex digits | Recompute using the correct identity domain |
| Timestamp | UTC `YYYY-MM-DDTHH:MM:SSZ` | Real calendar value, no offset/leap-second alias; compare as UTC instants |
| Attempt/run/campaign ID | Typed prefix and lower-case UUID | Opaque identity; never a proof or a sortable clock |
| Money | currency `PLN`, integer `minor_units` | Grosz, with outward rounding before admission |

Regex/schema validity cannot establish rational reduction, interval order,
calendar correctness, digest correctness, forest coverage or mathematical
truth. The decoder's semantic validation phase must establish these explicitly.
No binary64 conversion is permitted in mathematical comparisons, identities,
cost reservations or FX/outward-price arithmetic.

Every implementation has explicit limits for input bytes, nesting, integer
digits, cells, coefficients and recursion depth. Exceeding a limit produces
`unsupported` or `inconclusive`, never EMPTY or acceptance. Limits that can
change discovery results belong in the producer execution/precision policy;
verifier limits belong in the checker environment/manifest.

## 3. Bytes, artifact references and hash domains

`ArtifactRef` is exactly

```
{bytes_digest, size_bytes, media_type, format_id}
```

`bytes_digest=sha256(raw stored bytes)`; `size_bytes` is the exact byte count.
For an RJSON artifact those bytes must be canonical. Binary traces and native
logs have their own pinned format; they are hashed as raw bytes. A cloud URI,
filesystem path, bucket generation and download URL are operational locators,
stored separately. Moving identical bytes between local disk and GCS does not
change an artifact or mathematical identity.

Define the domain-separated identity function

```
D(kind,value) = "sha256:" + lowerhex(SHA256(
  ASCII("BEARCH/1\n" + kind + "\n") || RJSON_BE_1(value)))
```

`kind` is the exact literal from the following table, not user-selected text.
All fields of the named preimage are included. Self-ID fields are outside
their own preimages, avoiding a circular hash equation.

| Identity | `kind` | Exact preimage |
|---|---|---|
| statement_digest | `statement` | Statement.core |
| job_spec_id | `job-spec` | JobSpec.core |
| scope_digest | `scope` | Decoded canonical scope object |
| claim_digest | `claim` | Decoded canonical typed claim, including statement/scope and conclusion |
| verification_id | `verification-key` | VerificationReceipt.key |
| graph_digest | `task-graph` | TaskGraph without graph_digest |
| quote_id | `cost-quote` | CostQuote without quote_id |
| project_id | `frozen-project` | FrozenProject.core |
| schema bundle digest | `schema-bundle` | Root schema ID plus its complete sorted offline schema-resource manifest |
| Candidate/certificate/receipt identity | none | ArtifactRef raw bytes_digest |

An obligation label is a human lookup label outside Statement.core. Renaming
it changes the envelope bytes, not the mathematical statement digest.
The core includes all frozen mathematical context/scope references, exact
claim type and relation, source epoch, analytic rules and mathematical
dependency requirements. A source/kernel/semantic revision therefore cannot
reuse the old statement merely because the requested number is unchanged.

A schema digest binds the **complete referenced resource closure**, not just
a wrapper containing `$ref`. The schema-bundle manifest records the root
schema ID and every referenced resource ID, exact raw-byte digest/length and
format. A changed `protocol.schema.json` therefore changes the bundle digest
even when the small entrypoint wrapper is unchanged.

Canonical set-array order and uniqueness are fixed:

| Field | Ascending order | Uniqueness |
|---|---|---|
| analytic_rule_digests | ASCII digest | Digest |
| NamedArtifact arrays (inputs/source/environment/execution profiles) | ASCII role | Role |
| Statement/Job dependency requirements | ASCII tuple(statement_digest,scope_digest,claim_digest) | That tuple; one authorized trust requirement per tuple |
| Actual verification dependencies | ASCII tuple(statement_digest,scope_digest,claim_digest,trust_profile_digest,verification_id,receipt.bytes_digest) | Mathematical statement/scope/claim tuple |
| Accepted claims | ASCII tuple(scope_digest,claim_digest) | That tuple |
| Claim/assembly receipt-ref sets | ASCII bytes_digest | bytes_digest |
| DomainCover children | ASCII coverage_role | coverage_role; root/side/region roles are explicit labels |
| TaskGraph runtime nodes | ASCII job_spec_id | job_spec_id |
| Runtime edges | ASCII tuple(prerequisite_job_spec_id,dependent_job_spec_id,required_artifact_role) | Full tuple |
| Mathematical obligations | ASCII statement_digest | statement_digest |
| Schema resources | ASCII resource_id | resource_id |
| Dispatch job_spec_ids | ASCII digest | Digest |
| Dispatch slots | Numeric tuple(task_index,bundle_index) | That tuple; contiguous task indices and contiguous bundle indices within each task |
| Lean parameter bindings | ASCII lean_parameter | lean_parameter |
| Cost quote lines | ASCII line_id | line_id |

Do not sort mathematical vectors, polynomial controls, selected source
scripts, Fourier pieces or coverage trees as sets. Their order is the exact
source/format order. COUNT roots are numeric 0..n and leaves are DFS-left-first;
`"10"` does not precede `"2"` in this numeric root order. Farkas variables,
matrix rows and multiplier positions share the one source-derived ordering.

## 4. Statement, job and attempt are different objects

`Statement` states what every unknown law in a frozen scope must satisfy.
It contains no serialized unknown distribution, contact, measured moment or
Lean proof object. `CountContext` records rational acquired bounds; actual
moments appear only under the universal mathematical realization predicate.

`JobSpec.core` freezes the statement digest, task kind, exact producer recipe,
environment, logical execution profile, precision/search policy, immutable
inputs and dependency requirements. `task_kind` is `produce`, `verify` or
`assemble`. Changing arithmetic precision, stop policy or a kernel changes
the job ID. Physical VM packing/zone/SKU does not change it when the exact
architecture/image, logical per-task CPU/RAM/CPU-time limits, arithmetic and
adaptive policy remain unchanged; placement is recorded on the attempt.

An `Attempt` identifies one execution under a job ID and a lease generation.
Its worker, campaign admission, timestamps, fencing token and output refs are
operational evidence. Native exit0 or attempt state `produced` means bytes
were produced; it is not a mathematical verdict. The latest attempt cannot
replace an earlier certificate merely by finishing later.

Before a cloud submission there is no worker attempt or lease generation.
`Admission` reserves the **physical dispatch group's** liability, keyed by
dispatch_id and an immutable DispatchManifest with sorted job IDs/task slots.
The first actual worker claim atomically emits `AttemptAdmission`, binding
that reservation/slot to attempt_id, lease_generation, fencing token and
the current campaign control generation. Attempt.admission references this
claim binding. Queueing or an unknown create result can thus retain a valid
reservation without inventing an already running attempt. Several logical
jobs sharing one physical group do not reserve the same VM liability twice.

A physical task may contain an ordered bundle of independent logical jobs.
DispatchManifest binds `(task_index,bundle_index)` to one exact JobSpec and
bootstrap grant ID;0 is the unbundled index. Each logical claim still gets
its own attempt/lease/receipt. Public Attempt and AttemptAdmission contain
only `fencing_token_digest`. The raw high-entropy fence token is returned in
a private authenticated WorkerFence response, never serialized into an
ArtifactRef, public log or reproducibility bundle. Possession of its public
digest cannot authorize a ledger mutation.

`Candidate` binds producer output to its statement/job/attempt. Its native
status string and suggested scope are untrusted. `Certificate` adds the
versioned family kernel/schema, exact payload, output claim/scope and actual
dependency receipts. It is still untrusted until verified. A certificate
from another producer job may be reused for the **same mathematical
statement** under an authorized checker; job identity does not define truth.

## 5. COUNT scope and data contracts

The CountContext schema maps to the existing Lean `CountTaskContext` fields,
with target/search policy separated into the typed Statement/job records.
Decoder checks include n>=2; domain.actual_n=actual_n;0<N<=n; positive rho/m
lower bounds and support/gap floors; nonnegative caps;0<=theta<1; ordered
moment/H intervals; asymmetric radii<=convenience radius; and
`N*defect_cap/n<=native_defect_cap`.

The fifth box coordinate is **raw_inward0=a0**, not dY=a0+a1. Marginal
lambda_cap is not the joint noise intercept. `JointBudget.zero` means both
dY=lambda=0; `positive` requires strictly positive independent intercepts and
the actual coupled plane. Never replace an original joint intercept after
a marginal lambda contraction. The affine D lower plane and the coherent
signed-quadratic **maximum over the whole corner family** are frozen inputs.
Different independent complete families may be intersected; individual corner
coefficients may not be minimized separately.

The four COUNT coverage roles are distinct:

| Role | Required geometry and output |
|---|---|
| ordinary full forest | Exactly n+1 increasing roots 0..n; each root covers its original closed product; target-bound signed point score |
| general quantitative | Same arbitrary-law realization, without extremality; a declared valid U may exceed the producer early-exit target |
| original count5 ancestor | One exact original five-dimensional ancestor; complete closed subtree; no claim covering other roots or the whole panel |
| AB24 halfline | Same marginal at actual 24, fresh phase and 25 roots; requested closed halfline intersected with the central window, plus **both** exterior tails |

Every split has a strict interior rational cut, both closed children and
unchanged root/other coordinates. Both children retain the cut. Tree leaves
must match the serialized conclusions exactly in increasing-root,
left-first depth-first order. A missing root/child, duplicate root, switched
coordinate, one-sided split or promoted descendant bound is rejection.

An empty AB central clip is represented by `clip=null` and an explicit strict
disjointness proof. It is not an invented nonempty interval. A nonempty clip
requires its exact closed intersection and no empty-clip proof. Both exterior
tail bounds remain required in either case. Native early-exit search cap is
job search policy; accepted quantitative U is the actual certificate output.
An ordinary target check separately verifies the relation-transfer rule.

## 6. Covers and two DAGs

`DomainCover` names its parent statement/scope, exact child claims/scopes,
the accepted coverage rule and a coverage witness. A set of overlapping
rectangles does not prove a union covers the parent. Mixed references require
whole-cfg/source identity and containment inside one acquired reference;
partial overlaps from several references cannot be stitched implicitly.

The mathematical DAG has statements and rule premises. The runtime DAG has
producer/verification/assembly jobs and artifact prerequisites. These graphs
are not interchangeable: a successful runtime edge does not discharge a
mathematical premise. Validate both DAGs for cycles and exact dependency
identity; keep finite/tail and lower-bound prerequisites separate.

Some downstream contexts depend on an actual quantitative upstream U. Such
a mathematical port exists in the frozen rule/template manifest, but its
executable Statement/JobSpec is materialized only after the accepted typed
upstream claim is known. The accepted analytic adapter determines the new
context (for example U -> q_R -> licensed support refinement). Then freeze
its complete statement and dependency receipt before dispatch. Do not guess
a future claim digest or mutate an already frozen job. TaskGraph is a
content-addressed materialized snapshot; expansion events link snapshots
to the same immutable mathematical template manifest.

## 7. Receipt identity, authority and trust

`verification_id` is a deterministic **verification request key** binding the
statement, exact certificate bytes, checker build/environment, trust profile
and exact dependency receipts. It excludes worker/job/attempt/time metadata.
The receipt itself has a separate raw-byte digest. Definitive
`accepted_conditional` versus definitive `rejected` under one key is a
conflict to quarantine. Different accepted claim/scope/conclusion bytes under
one key are also a conflict. Different diagnostics or times alone are not.
`metadata_only`, `unsupported` and `inconclusive` carry no mathematical claim;
they are non-definitive attempt evidence and do not poison a later complete
retry's acceptance. The first authenticated definitive receipt is the stable
authority pointer; further compatible observations cannot silently replace
its bytes. A conflict blocks coverage until explicitly resolved. A required
fresh replay still executes, but an identical semantic result preserves this
anchor and records a new replay observation, avoiding dependency invalidation
solely from a changed completed_at/run_id. A changed verification key gets a
new anchor.

Receipt outcomes are `metadata_only`, `accepted_conditional`, `rejected`,
`unsupported` and `inconclusive`. Only `accepted_conditional` carries accepted
claims, and only after [the checker/authority contract](04-checkers-and-lean.md)
has been met. The checker must be authorized for the profile by a separately
approved manifest/policy. A receipt's self-declared profile, a copied
signature string or a source hash does not authorize a stronger trust claim.

Runtime publication requires an authenticated authority event or detached
seal over the exact receipt bytes/key. Producer credentials cannot mint
trusted receipts or coverage. `ReceiptSeal` references that separate evidence;
offline import without an authorized seal requires re-verification. A seal
proves issuer/binding, not numerical correctness beyond the named profile.

## 8. Campaign budget and absolute clock

`campaign_id` survives every CLI invocation; `run_id` identifies one invocation.
BudgetPolicy fixes startup 7500 PLN minor units, main 55000, total 62500, and
main runtime 43200 seconds. T0/deadline are persisted once before the first paid
main create. A retry, resume, new run ID, queue wait or backend reconnect cannot
reset either the clock or phase ledger. A new paid campaign requires fresh
explicit authorization. Deadline/cancellation state is monotonic.

RunControl stores campaign/control generation, cancellation epoch, immutable
T0/deadline/cutoff, phase ledgers, unreconciled liability and independent
watchdog manifest. Admission reserves a quoted worst-case liability **before**
create and binds the dispatch group/manifest/profile/quote/campaign/control
snapshot. Actual attempt/lease binding is created later by AttemptAdmission.
Unknown create outcome holds its reservation until definitive reconciliation.
No reservation is released merely because a client timed out.

CostQuote uses exact price/FX/tax/reserve arithmetic and an explicit liability
horizon for boot, queued resources, retries, verification, network, logging,
metadata, GCS operations/storage, watchdog, cancellation, retained storage and
cleanup. Prices and FX require a dated current quote before paid activation.
No machine-price or historical free-tier assumption is encoded in these
illustrative schemas. An outward modeled admission limit is not a guaranteed
invoice cap; `invoice_cap_guaranteed` is false.

ShutdownReceipt distinguishes requested, dispatched, platform-confirmed,
independently verified no-active-compute and cleanup failure. It retains
chargeable-resource inventory and unreconciled liability. Billing alerts do
not enforce a hard limit. Worker completion must still pass the live lease,
campaign cancellation and deadline CAS; it cannot override an expired budget
or restart a drained campaign. Cloud/local transaction mappings are in
[03](03-storage-and-recovery.md) and [05](05-compute-and-deployment.md).

## 9. Versioning and example status

A schema/meaning/codec change gets a new version/digest. Unknown versions,
families, rule tags or proof formats are unsupported. No permissive fallback
may interpret an unknown EMPTY tag as infeasibility. Migration reads old bytes,
validates old meanings and emits new immutable artifacts with explicit links;
it does not edit old digests in place.

`examples/architecture/fixture-index.json` lists exact structural and semantic
expectations. Examples are illustrative; none declares mathematical acceptance
or a completed proof. In particular, the Farkas example has correct arithmetic
for an unrelated inconsistent system and is rejected because its problem is
not bound to the statement's actual derived planes. This distinguishes
well-shaped bytes and a true small calculation from the required theorem.

## 10. Exact TOML compilation and resume compatibility

`FrozenProject` is the canonical compiled configuration, with
`project_id=D("frozen-project",core)`. TOML is only its editable frontend.
The compiler accepts exactly `schema_version="be.arch/1"` and the versioned
keys in the architecture example. Unknown sections/keys are rejected.
Numerical settings are canonical decimal/rational strings; TOML floating
point, dates used as implicit timestamps and environment-variable expansion
inside mathematical inputs are rejected.

| TOML field | FrozenProject.core field / normalization |
|---|---|
| requested_theorem | Exact enum: iid_upper_all_positive_indices or sharp_global_constant |
| top_template, obligation_manifest, issuer_policy, adaptive_policy | Resolve path from the TOML directory; decode/validate/seal; replace by exact ArtifactRef |
| allowed_trust_profiles | Resolve every profile; sort by bytes_digest; reject duplicates |
| source_capsules/environment_profiles/execution_profiles `{name,path}` | `name` becomes unique ASCII role; path resolves to ArtifactRef; sort by role |
| backend, campaign_id | Exact backend enum and stable campaign identity |
| budget_policy, campaign_control | Resolve selected policy and optional initial campaign snapshot; preserve the stable campaign/control relationship |
| artifacts resolver/allow_private_inputs | Freeze the normalized resolution-policy digest; private-only required inputs are forbidden for public replication |
| local/gcp/performance/budget_constraints | Compile closed versioned operational-profile capsules; logical caps/policies also bind execution profiles where they affect producer behavior |
| reproducibility manifest | Resolve the complete required-asset/build/license manifest supplied by the top template or explicit project input |

Physical mirror URLs, credentials, local store/ledger paths and cache
locations are resolver/invocation data, not ArtifactRef identities. Changing
the transport location of identical bytes changes neither statement nor job
identity. Every required source/kernel/certificate and public environment
build recipe must be obtainable from a public mirror or the portable offline
bundle without the original user's GCP account. A missing canonical p25
capsule or incomplete production manifest is a release/plan blocker, not a
private reference to be fetched after paid activation.

`--resume` resolves and compares this same frozen project, source/profile
closure and campaign policy. It reads live control by campaign_id, not by
following an arbitrary mutable latest file. An optional campaign_control ref
is the immutable initial/attached snapshot, not a file rewritten whenever
control_generation advances. Edited theorem/source/trust/precision/profile
inputs require an explicitly new frozen plan; no silent replan or new paid
campaign is inferred. Fresh execution ignores accepted-result caches as
specified in 02/07 while preserving source identities and the active campaign's
clock/ledger. It cannot mint another cloud budget.

## 11. Local and cloud phase policies

BudgetPolicy is a tagged union. `gcp_user_campaign` retains the exact user's
7500/55000/62500 PLN-minor-unit limits and 43200-second main window.
`gcp_authorized_campaign` supports another explicitly authorized campaign's
own exact caps; it cannot replace or extend this live user campaign.
`local_reproduction` has `no_paid_activation=true`, its own explicit local
CPU/RAM/time limit and `cloud_campaign_resume_allowed=false`. The example
local time window is 604800 seconds, not the cloud 12 hours. A fresh public local
reproduction uses a separate local campaign; it does not reset, continue or
inherit a cloud campaign's money or clock.

Paid startup has its own bounded window. The example cloud policy fixes
startup_runtime_seconds=7200. RunControl persists startup_t0,
startup_deadline and startup_admission_cutoff once before the first paid
pilot, plus its independent startup_stop_manifest. This watchdog/absolute
stop path must be armed before that pilot. Main activation requires confirmed
closure of startup compute, then sets the separate immutable main anchor.
Admission carries the active phase deadline/cutoff and must match live
control. Queueing, delayed boot, retries and setup cannot evade either window.
Local control instead uses local_t0/local_deadline; its cloud anchors and
charge ledgers remain unused. The planned examples have no active anchors
and no deployed resources.
