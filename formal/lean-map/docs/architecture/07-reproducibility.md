# Reproducibility: a release requirement for the public CLI

The user requires a third party to reproduce the complete computation and
verification from the published project, without the author's Google Cloud
account, private working directories or undocumented intervention. This is
an implementation release criterion, not a claim that the current architecture
branch already ships that runnable release.

## 1. Two reproducible workflows

The normal entry remains one `be run` command. Exact options and FrozenProject
mapping are specified in [protocol](01-protocol-and-types.md) and
[execution](02-execution.md). The release must support both workflows:

| Workflow | Meaning | Required inputs |
|---|---|---|
| Full recomputation | Start in an empty isolated local state/store; execute the required numerical producers, independent checkers, covers and final assembly | Complete frozen input/source closure and reproducible environment |
| Verification of an exported result | Read a portable proof bundle; verify exact bytes, trust/authority, all required numerical evidence, coverage and assembly | Bundle plus the declared checker/source environment; no private service dependency |

A verified cache hit may accelerate normal resume, but cannot be reported as
a fresh recomputation. A byte-integrity check of a bundle cannot be reported
as a fresh mathematical verification. The report records which work was
executed, which authorized acceptance was reused, and which assumptions remain.

An exported trusted-replay receipt may be authenticated using its approved
issuer policy; a third party can instead rerun the checker from the frozen
sources under their own declared authority. If the resulting receipt bytes
contain different operational metadata, the newly assembled report binds
those exact receipts. It does not silently relabel them as the original ones.

## 2. Complete input closure

The published distribution contains, or resolves by digest from documented
public mirrors/offline bundles, every required input:

* Frozen mathematical project, requested top theorem, obligation/template
  manifest, accepted analytic bundle, rules, covers and parameter capsules.
* All native numerical source capsules, source-preparation rules and selected
  historical acquisition/reference inputs, with exact epochs and whole scopes.
* Producer/checker/issuer/trust manifests, schemas, codec versions, environment
  and dependency locks, image digest and the source recipe used to build it.
* Lean sources, pinned toolchain/mathlib, bridge-generation recipe and exact
  expected conditional theorem/parameter mapping.
* Any data required by a selected route, including full admitted mixed
  reference manifests as distinct from the final used subset.

A private bucket URL, an author's Desktop path or a digest with no retrievable
bytes fails this requirement. Mirrors and local paths are locators; they do
not change the ArtifactRef or statement identity. Downloads verify length
and digest before use and support explicit offline installation. Large data
need not live inside Git, but their complete manifests and durable retrieval
or generation instructions must be published.

The known missing canonical selected p25 capsule is a reproduction blocker
for that historical epoch. Resolve it with the exact approved capsule or a
new explicitly acquired epoch satisfying the same mathematical contracts.
Historical PASS text cannot fill that gap. The release input-closure check
must identify every such missing artifact before paid dispatch.

## 3. Environment and platform contract

The first numerical execution target is the frozen Linux x86-64 image.
Linux may run it directly; other host systems require the documented
compatible Linux container/VM setup. Do not claim arbitrary platform
portability from Python source alone. The local backend uses the same
mathematical adapters and verification rules as cloud execution.

Publish both an immutable retrievable image and its reviewable build recipe,
base image/dependency pins, licenses and source capsule hashes. The image is
not allowed to depend on a private registry or hidden credentials. Distinguish
a semantically reproducible rebuild from a bit-identical OCI image rebuild:
the latter needs a deterministic build process and separate evidence. A
different rebuilt image digest requires an approved environment profile;
similar version strings do not authorize reuse.

Initial setup may install the documented CLI and container prerequisites.
The single proof command then prepares validated inputs, schedules work,
checks, assembles and exports the result. Publish the setup steps and minimum
RAM/disk/CPU requirements as measured release metadata. A small local machine
can take substantially longer than the cloud allocation; a 12-hour cloud
policy is not a local runtime guarantee.

Clean local reproduction is a separate explicit local campaign with no paid
cloud activation and its own declared CPU/RAM/disk/time limits. It may allow
a longer local window. It cannot inherit the original campaign's spending
authority, reopen its admission or reset its absolute cloud deadline.
Resuming the original cloud campaign still obeys its frozen75/550PLN and
43,200-second policy. Importing its immutable evidence does not transfer its
control authority. The typed policy variants and project mapping must make
this distinction explicit before implementation.

## 4. Identity and deterministic meaning

Exact canonical data have deterministic bytes and domain-separated digests.
Accepted arithmetic, bounds, complete scopes and the requested theorem must
retain their specified meaning across local and cloud adapters. Exact
reductions have a fixed ordering, and any permitted adaptive search policy
and seed are recorded.

Different valid search trees, processor timing, scheduling, timestamps,
provider IDs, logs and receipt metadata need not be byte-identical. A fresh
run may discover another valid certificate. Acceptance must establish the
same frozen requested conclusion under the same declared trust semantics;
it must not promise that wall time or every candidate byte will match.

The bundle manifest distinguishes deterministic semantic artifacts from
operational observations. Each is hashed as its own actual bytes. Export
preserves original bytes and exact references rather than pretty-printing
them into a different evidence object.

## 5. Portable bundle and security boundary

`be export` packages the complete selected proof closure, analytic/trust
policies, source/environment manifests, checker recipes, coverage/assembly
reports and the exact referenced artifacts. Its immutable bundle manifest
lists every member, length, digest and format; consumers reject undeclared
missing members. Additional historical candidates may be omitted when they
are outside the declared required proof/input closure.

No private access token, service-account key, billing account or author's
cloud authorization is necessary to verify the bundle. A third party who
chooses cloud recomputation supplies their own project and budget; that is
deployment configuration, not a mathematical premise. Publishing a result
does not grant access to the original campaign's control or finances.

Preserve redistribution notices for original code, manuscript material,
dependencies and source capsules. A necessary input that cannot be legally
redistributed or publicly regenerated is an explicit release blocker for
the claim that anyone can reproduce the full workflow.

## 6. Release evidence

Before advertising the complete CLI as reproducible, demonstrate:

1. A clean checkout/install on a second environment without the author's
   home directories, local caches, cloud credentials or private mirrors.
2. Successful full local execution of the declared conformance slice, then
   of the complete requested proof when all production families are enabled.
   A pilot result is labelled with its exact scope.
3. Offline bundle verification with network disabled and an explicit trust
   policy. Removing one required member produces a precise missing-input
   result, rather than accidental access to the original cloud store.
4. Local/cloud port agreement on frozen statements, arithmetic/scopes,
   rejection controls, coverage and final conditional conclusions.
5. A reproducibility report recording environment/inputs, fresh versus reused
   work, time/resource needs, final trust assumptions and remaining limits.

These tests are future implementation acceptance gates. The architecture
validator checks schemas and fixture identities; it does not satisfy them.
