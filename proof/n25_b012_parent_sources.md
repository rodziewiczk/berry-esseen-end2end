# Exact INITIAL and global-resource parents for retained n25 B0–B2 counts

The minimal unchanged-source route is **six fresh acceptance actions**: one complete INITIAL accept and one complete global-resource accept for each of B0, B1 and B2. Construction is unnecessary when the archived proof objects are treated as untrusted candidates and the original acceptors replay them completely. This source/JSON audit establishes that route's byte-level compatibility; it does not execute those actions or acquire their mathematical premises.

The companion `n25_b012_parent_sources.json` pins every selected source file, proof candidate, historical receipt used only as metadata, source range, command and dependency edge. Inputs come from the existing pinned `cutoff25_20261011.zip` (514,958,998 bytes; SHA256 `17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`) and the frozen75-forest catalog SHA256 `f055b5017d4e1fd14f2b48a6a95fef4a4c61a025dea6174c424cd5968de801f7`. This pass read ZIP members and checked the selected source hashes. It did not rehash the whole transport, import an archived module or run a mathematical evaluator. All exported archive paths are normalized and contain no personal paths.

## Three independent global parent batches

| Branch | Closed rho band | Symmetric support radius | INITIAL covers / rectangles | Global resource rows | Count jobs ultimately fed |
| --- | --- | --- | --- | ---: | --- |
| B0 | [1,11/10] | 12/5 | 12feedback+1export;239,616 | 100 | 17global |
| B1 | [11/10,6/5] | 13/5 | 12feedback+1export;239,616 | 100 | 31global+4local |
| B2 | [6/5,13/10] | 29/10 | 12feedback+1export;239,616 | 100 | 19global+4local |

All profiles have actual n=25, K=0, owncap434477/1000000, grid[24,24,8,4], and contact allowance5/16. Every INITIAL signed cover has18,432 rectangles and the final export has all100 closed probability panels `[i/100,(i+1)/100]`, i=0,...,99. Every INITIAL and global-resource acceptor has12 original object-corruption controls. The JSON records their literal labels extracted from the checker AST and matched against the historical output metadata.

The six source/manifest identities are:

| Branch | Stage | Original directory | Checker SHA256 | FROZEN_SOURCES.json SHA256 |
| --- | --- | --- | --- | --- |
| B0 | INITIAL | `cutoff25_20261011/new_low/initial25_b0_v2` | `b1643148258ceadf312ebc67648e5d8aabbff51cf6547e9b1498117b4a9ad3b7` | `1963a9a8e34d1d789814026d9df247030f8b29229573e844bdd13886b0adbab5` |
| B0 | Global resources | `cutoff25_20261011/new_low/resource25_b0_v1` | `9260f957d362125749c053bcea9592fe714dcd4668d71b452fe70bdc3fa1e1b9` | `d12af679165d44e4e5b01965ca99b769b922306f9291998e42214bf6eb328644` |
| B1 | INITIAL | `cutoff25_20261011/new_root/initial25_b1_exact_v1` | `0166295959cba3ac6e50d79c5563bd0be8c3942c0fbc4b05ed211c90b30b69a7` | `b8915e0a7b2e51df6db0218c6a23365040ce3303cb2b4d7ab49c9db7d302c8b8` |
| B1 | Global resources | `cutoff25_20261011/new_root/resource25_b1_v1` | `212ec4eb417b05032a206210bdc9bf40bfa7a4ad045859cb8f165992d467711c` | `f352792aa7db4fd36bedc07773e090ae77668bf35e683b9773e36a85063cc2e5` |
| B2 | INITIAL | `cutoff25_20261011/new_root/initial25_b2_exact_v1` | `c5b3e684c60686666958006d3681922f19ec6869ab4fbd54f61fd813bc0e61ed` | `b6c07b868dc99414b124175a9c5863a8dc701248231ef02ea175b294a2a4bcfa` |
| B2 | Global resources | `cutoff25_20261011/new_root/resource25_b2_v1` | `211b96ca62c03c37db88f583b2eda17a83c59ab6c181078fd219b1f5301f9aec` | `96cf787e4db37a65d529d41d180737c2534dddbb7ac374be777d5b395f9abe7c` |

Each INITIAL manifest has30 declared source/premise files; each resource manifest has32. Every declared member is present and SHA-matched. The source manifests are direct filename-to-SHA dictionaries, rather than dictionaries nested under `files`. Keep their original bytes and directory names. Resource scripts resolve the sibling INITIAL directory by the original literal relative path.

Run the following two actions in each branch's own original directories, in this order:

1. `python -B -S initial25_bN.py accept`, with the retained `INITIAL25_BN_PROOF.json` present and the old `INITIAL25_BN_ACCEPTED.json` omitted.
2. `python -B -S resources_bN.py accept`, with the retained `RESOURCE_BN_GLOBAL_PROOF.json` present, the **newly generated and execution-validated** INITIAL receipt in its sibling directory, and the old resource receipt omitted.

Here N is the literal branch index0,1,2. The JSON contains six fully expanded commands, paths, output names and dependencies; this is not an arbitrary parameterized source selection. No historical acquired receipt should be supplied as a substitute for a successful fresh action.

## Why accept-only preserves the resource candidate binding

The INITIAL main recomputes `calculate(action)` before comparing the candidate. Its finite schedule starts from `raw=d=None`, runs12 full feedback covers, and performs a separate complete export cover (`initial25_b0.py:71–88`; B1/B2`:69–86`). Acceptance compares the entire recomputed proof object with the retained candidate, then executes all12 controls (B0`:95–103`; B1/B2`:93–101`). It emits a status marker after writing the receipt; stdout is not itself the receipt JSON.

A separate source-only byte witness was checked for all three branches. The literal output dictionary was reconstructed from the retained candidate's source/profile/final-invariant/scope fields, actual proof and checker hashes, the12 literal control labels from the source AST, and the literal239,616/100 census. The original field order and `json.dumps(out, indent=2) + '\n'` serialization reproduce the archived INITIAL acceptance **raw bytes exactly** in every branch. Neither elapsed time nor original filesystem paths occurs in that output dictionary. The witness's expected SHA and field order are stored in the JSON.

Consequently, if the unchanged INITIAL accept succeeds on that exact candidate and closure, its fresh output has the exact parent receipt SHA already bound in the retained resource candidate. The future runner must check that actual fresh receipt SHA before launching the resource acceptor. This avoids both repeating construction and changing the resource candidate header. The proof of compatibility is conditional on actual successful replay; reproducing an old receipt template locally is not mathematical acceptance.

Every resource `calculate(candidate)` iterates over all100 ordered INITIAL export rows. It validates the candidate's complete support plan, calls the original `resource25_core.resource` with that plan, checks the whole actual plan equals the supplied plan, and compares the entire recomputed resource object (`resources_bN.py:57–80`). The12 controls and complete survivor/exclusion classification follow (`:81–89`). No count contract is presumed by these global resource engines. Progress files (`PROGRESS_accept.json` for INITIAL and `PROGRESS.json` for resources) are partial diagnostics and do not resume an interrupted acceptance internally.

## Predecessor and execution contract remain explicit

Every INITIAL source hard-pins `STRONGER24_COMPLETE_JOINED.json` at SHA256 `f3c6a95c5fa814cc024872c0b4212d7d5272d8b7696306dfc0f5a3b74d12167f`, requiring the statement C24<CE+1/80 with n24/K3/10. The file is a retained **conditional statement input**, not a newly acquired theorem. `fixed_support` derives the5/16 contact allowance and checks its support consequences under the retained attainment/contact/smoothing framework (`initial25_bN.py:52–68`, B0 through70). The source-only inventory does not discharge that framework or turn an auxiliary numeric-chain report into this historical theorem.

The global INITIAL/resource import closures resolve to their own frozen pure Python files and the standard library. Static inspection found no unresolved import, child-process/thread creation module, ctypes, Windows-specific module or resource-limit mutation in these declared closures. The original scripts require ordinary unoptimized no-bytecode Python. They do not supply a new execution guard. A future Colab wrapper must establish and preserve the actual bounded Linux native contract, captures and complete fresh output chain. This audit does not claim that an old Windows execution receipt proves Linux guard capability.

The historical B0 composer used the separately reviewed `global_initial_cache_v1/accept_initial_memoized.py` route for its INITIAL acceptance (`compose_low_b0_complete_v3.py:223–227`). Its helper/review source pins are recorded as an optional accelerator. The direct original INITIAL accept remains the minimal semantic route; old cache or runtime files are not fresh numerical evidence.

## Eight local count contracts require two additional acquisitions

The six global accepts do not discharge the local B1p35 and B2p31 count contracts. The selected source routes are:

| Local panel | Source directory | Complete local replay | Selected count targets |
| --- | --- | --- | --- |
| B1p35 | `cutoff25_20261011/new_root/local25_b1_v2` | 4cycles×4covers=16covers;294,912rectangles;4isolated resource consequences;12controls | b1-p35-q0..q3 |
| B2p31 | `cutoff25_20261011/new_root/local25_b2_v2` | 4cycles×4covers=16covers;294,912rectangles;4isolated resource consequences;12controls | b2-p31-q0..q2 plus selected local-joint-cubic q3 |

The frozen `mixed_bN.py` driver calls `subprocess.run` for `resource_worker.py` (`:80–91`, spawn at89). Therefore its unchanged execution is **ineligible for the current single-process native guard**. It needs an honestly declared bounded process-tree/BASIC contract. The original memoized wrapper starts with a fresh empty complete-stage cache; it does not remove the resource child processes. Its sibling INITIAL/resource imports resolve to the complete source closures already recorded above.

There is also a real fresh-binding conflict. `parents()` hashes the actual global resource acceptance receipt into `parent_binding_sha256` (`mixed_bN.py:32–48`), while that receipt includes variable `seconds` (`resources_bN.py:88`). The local `calculate` returns this current binding and `accept` requires whole-object equality (`mixed_bN.py:93–141`). Thus an unchanged old local candidate cannot silently be combined with a new timing-bearing resource receipt.

The conservative unchanged-source route is four additional actions in total: B1 `mixed_b1.py construct 35`, then `accept 35`; B2 `mixed_b2.py construct 31`, then `accept 31`. Each construction and acceptance performs its own full local numerical work. An alternative can preserve the saved local support plans by an explicit, reviewed parent-binding-only candidate adapter followed by full unchanged acceptance, but that new protocol is not implemented or acquired by this inventory. No historic global receipt may be substituted to avoid the conflict.

## Resource-to-count joins still required

The source dependency split is67global count contracts and8local contracts. B0's contract has the older `conditional_predecessor`, `contact_allowance`, `owncap` and `rounding` fields; its schema differs from the B1/B2 global contracts. The local contracts are explicitly marked `UNACQUIRED_RATIONAL_GUARDS_ONLY` and refer to cycle4 resource/input/INITIAL design data; their theta and quarter premises must be acquired from the fresh same-law local output.

Fresh global resource receipts have timing-dependent hashes, so literal old receipt hashes in count-contract provenance are not a new interface proof. New joins must bind the actual fresh parent proof/receipt and count acceptance, then verify the simultaneous numerical guard implications, physical interval restrictions, moment floors, theta bounds and signed quadratic margins on the complete closed domains. Existing composer `physical` routines are at B0`:102–125` and B1/B2`:108–131`; their broader mains also pin historical executions and must not be mistaken for a fresh execution protocol.

This map leaves all fresh-arithmetic, parent-acquisition, full-n25 and all-index conclusion flags false. It provides the exact six global acceptance jobs and the separate local/semantic obligations for a compact future replay, rather than another set of proof claims based on historical PASS labels.
