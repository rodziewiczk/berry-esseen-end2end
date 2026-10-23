# B4 q2: observed node-budget stop

Date: 23 October 2026. This review reads source bytes, JSON, captures and saved
tree geometry only. No mathematical source was imported, no leaf result was
evaluated and no search or native acceptor was run locally.

The actual run exhausted its original 10,000-node discovery budget. Its saved
checkpoint remains incomplete: 4,996 leaves and 17 pending regions. This is not
a recorded mathematical rejection or a completed count certificate.

## Actual bundle and source identity

| Item | Value |
| --- | --- |
| Result ZIP | `20261023T102233Z-af459eba-results.zip` |
| Actual ZIP bytes | 1,913,858 |
| Actual ZIP SHA-256 | `84a5272daa9858e66c369f18365bf5f17568dd912e9901cfc0c5c1859a9972f0` |
| Target | `b4-q2`, original V12 conditional n25 count |
| Original source commit | `75a94708872e2bc053f42a279559b23ed91e4402` |
| Actual frozen-design SHA-256 | `2517c1b8c79949bad93eecdcaa43e389344411fd4c71d5d516dde1e40b732e2a` |
| Actual count-protocol SHA-256 | `5cd4f1a59ba1dbd10ae0455cde3731e03b236b0e1572dda78734dce5142e7f96` |
| Actual contract SHA-256 | `0576748a8e4deb2450fea8fc7b1b06898dd8bd3ae2d5fc3465163a123d9425c3` |
| Actual final checkpoint SHA-256 | `c08d59310fad35069c8d368629cdb0e2a902c39fff0deab9696f4b22bdc609e1` |

All 76 source/input file hashes in the actual `FROZEN_DESIGN.json` match the
saved capsule bytes. The capsule has exactly those 76 files plus the design
manifest, with no extra file. The kernel map agrees with the checkpoint's native
header. The fixed domain is n25, probability `[59/200,119/400]`, rho `[7/5,3/2]`,
with 26 ordered count roots, k=0 through 25.

The recorded discovery implementation hash is
`3b239119082d0d5275446beb2d38878c9a7c7988c655da6e52fd34023e485eb4`.
The task records its count driver hash as
`3ff711aa9271e1f277800b11e9db8241d3e532af9f271d9f797c678580aa37d1`
and supervisor hash as
`61e71dd4a9653de2bbbee8c54928a1f5c5bffd0bf083dd324851716c3a1eaea2`.
These are recorded execution provenance; source hashes alone do not validate
saved mathematical leaf decisions.

## Stop and saved progress

The final stderr contains exactly:

```text
DISCOVERY_INCOMPLETE_NO_ACCEPTANCE: Original split depth/node budget exhausted
```

The seventh slice returned integer code 1. Its supervisor classified the result
as `incomplete`, with reason `nonzero_subprocess_exit`. Its own wall duration was
1,388.526 seconds. The entire session lasted 10,515.953257 seconds, or about
2 hours 55 minutes 16 seconds, from its recorded start to finish. Slice elapsed
time must not be confused with the whole-session duration.

| Slice | Saved nodes | Saved leaves | Saved split nodes | Pending regions |
| --- | ---: | ---: | ---: | ---: |
| 1 | 1,030 | 511 | 502 | 17 |
| 2 | 2,760 | 1,375 | 1,367 | 18 |
| 3 | 4,426 | 2,206 | 2,200 | 20 |
| 4 | 6,144 | 3,072 | 3,059 | 13 |
| 5 | 7,614 | 3,802 | 3,794 | 18 |
| 6 | 8,920 | 4,455 | 4,447 | 18 |
| 7 | 10,000 | 4,996 | 4,987 | 17 |

Every saved checkpoint has maximum depth 20. Thus the actual final node census
reaches the 10,000-node ceiling while remaining below the unchanged depth 128
ceiling. Pending-region counts vary with subdivision; they are not a completion
percentage and do not support an ETA.

The maximum sampled process-group RSS among the saved slice summaries is
286,662,656 bytes, below the configured 536,870,912-byte limit. The final stop is
the explicit discovery node-budget exception, not a recorded memory-limit stop.

## Checkpoint and capture checks

For each of the seven saved checkpoints, this review checked:

- exact design, checker, contract, kernel-map, discovery implementation,
  alpha-priority and traversal bindings;
- all 26 roots in their original order;
- each stored split's integer axis, strict interior rational cut and both
  closed child boxes reconstructed from the original five-dimensional root;
- exact agreement of every saved leaf's box with that reconstructed geometry;
- the pending-node schema, which records an unresolved region without a saved
  accepted leaf result;
- unchanged prior splits and complete prior leaf payloads across slices, with
  only pending regions expanded;
- byte identity between each later slice's `resume.json` and the preceding
  completed slice's checkpoint;
- identical main and backup checkpoint bytes in every saved slice;
- actual stdout/stderr hashes, agreement of the stage observation with its
  supervisor result, and hash agreement of the supervisor-captured checkpoint
  copies with the actual candidates.

No source-binding, topology-transport or saved geometry mismatch was found.
These checks preserve the search work as untrusted topology; they do not
recompute or accept any saved arithmetic result.

## Acceptance boundary and proposed continuation

All seven search reports have `native_acceptance_run=false` and
`arithmetic_accepted=false`. The final session also keeps native arithmetic,
parent acquisition and all-index acceptance false. The bundle contains no
native count acceptance action or accepted count receipt. Its last search has
no complete candidate result packet.

An unchanged resume of the saved 10,000-node checkpoint still faces the original
node ceiling when another split is required. A useful continuation therefore
needs an explicitly identified new execution epoch or a separately justified
alternative search/cover strategy; it must not silently weaken or overwrite the
original 10,000-node source identity.

The proposed 100,000-node resource-only epoch can preserve the same numerical
leaf criteria while changing the declared resource budget and execution/header
identity. Its source transformation, sealed source closure and checkpoint
migration require separate review. Migrated topology must remain untrusted,
retain all roots and closed splits, and require full fresh evaluation of every
leaf and all original corruption controls before any scoped acceptance. A new
budget does not promise that discovery will finish or that the resulting forest
will pass. Parent acquisitions and mathematical composition remain separate.

## Independent review of the explicit larger-node source epoch

The reviewed `be_replay/count_limit_epoch.py` version has SHA-256
`9dc980c2e23580feb9402f9f15c533cc76582808656cc7c23b1b3fc37b5082dc`.
Using the actual original checker and design bytes from this failed ZIP, a
source-only derivation independently confirmed:

- new checker SHA-256
  `f535bae9054163b57206e2bdffe2afae96b5c0bfb28b3efa4533c88d037ca376`;
- new design SHA-256
  `866eec6360d31f80931ddd9edfb87c4218caa23c8f06346ba8362f093b110e6a`;
- exact checker byte equivalence except the single assignment
  `LIMIT=10000` becoming `LIMIT=100000`;
- no change to the AST of any original function;
- both original uses of `LIMIT` remain the `visited<=LIMIT` resource guards;
- original source/design bytes are retained separately and bound in a
  deterministic, path-independent 79-file new manifest, plus its design file;
- the source verifier rejects unbound helpers and directories, while permitting
  only the explicitly named forest/acceptance JSON outputs in addition to the
  sealed source inventory.

The constructor, leaf evaluator, canonical replay, exact target, contract,
kernels, closed roots/splits, depth 128 limit and all 24 controls retain their
original functions. The new checker hash and declared epoch identify the new
finite resource profile. Its output must not be relabeled as acceptance by the
original 10,000-node checker merely because some native status strings remain
the inherited original strings.

A separate source/JSON-only probe built the new capsule from the failed ZIP,
migrated the actual final checkpoint and passed the recovery driver's corrected
checkpoint check. The original packet and every root/tree/leaf payload remained
unchanged. Only the declared design/checker identity pins changed in the new
untrusted packet. The resulting census remained exactly 10,000 nodes, 4,996
leaves, 17 pending regions and maximum depth 20. No frozen mathematical module was
imported by that probe, and no search/acceptance call was made.

The review found and reported two implementation issues before that successful
probe: the source verifier initially lacked an exact extra-file inventory check,
and the recovery runner compared its literal header subset with the entire real
checkpoint header, inadvertently rejecting the dynamic `target` field. Both
were corrected. The reviewed recovery acceptance path was also tightened to
require exact integer completion, actual supervisor and kernel-guard sidecars,
actual capture hashes, complete forest statistics, ordered original controls
and equality of the captured terminal JSON with the fresh receipt. Final
execution-context checks belong to the recovery runner's own reviewed version.

These source and transport results establish a concrete eligible continuation
input, not successful recovery or a mathematical certificate. The new search
can still stop on resources or unresolved cells, and any later complete forest
must pass full fresh native replay before its scoped arithmetic is accepted.
