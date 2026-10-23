# Middle n25 acquisition lanes: notebooks47 and48

This is a fallible internal source/infrastructure review by the same AI system,
not external independent mathematical verification. No original mathematical
kernel was imported or evaluated locally. No fresh Colab acquisition is claimed
for these newly prepared lanes.

The exact catalog is [middle_n25_acquisition_sources.json](middle_n25_acquisition_sources.json),
SHA-256 `8c2c518bd044dd53ca2d5974d06bfb3ed04b3b1fa641490a1533cdfb6042d278`.
Its inputs are members of `cutoff25_20261011.zip`, 514,958,998 bytes, SHA-256
`17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`.
The catalog builder reads and hashes source/JSON only and imports no original
module. Member paths below are relative to `cutoff25_20261011/`.

## Exact selected complete queues

| Notebook | Region | Complete actions | Selected local source |
|---|---|---:|---|
|47 | Middle B4: rho `[33/20,7/4]`, beta `[12/25,14/25]` |14 | `new_middle/b4_exact2_v1/` for18,19,20,21,23,26,27,28; `b4_exact_v1/` for22,24,25 |
|48 | Middle B5: rho `[33/20,7/4]`, beta `[14/25,307827/500000]` |12 | `new_middle/b5_exact_v1/` for18–26 |

Each queue begins with three complete original actions in its canonical
`new_middle/b4_exact_v1/` or `new_middle/b5_exact_v1/` directory:

```
python -B -S initial_middle.py accept
python -B -S global_resources.py construct
python -B -S global_resources.py accept
```

It then runs, from each exact selected local directory:

```
python -B -S acquire_panel_memoized.py accept INDEX
```

The actual notebook commands use absolute script paths and those same source
directories as cwd. All original mathematical modules, original local wrappers
and the fixed exact-stage cache helper remain unchanged.

The final selectors are `new_middle/B4_FINAL_V4_SELECTION.json`, SHA-256
`9697250ae08c7112580cb4adfc13a2682c708731e827aca81f1b8c1d71888e63`,
and `new_middle/B5_FINAL_V4_SELECTION.json`, SHA-256
`16f04e12eead996b7d31a44d2e2d8285b8500829195264047c00a8759a4b9aaf`.
These selectors specify all11 B4 and9 B5 local obligations, including local
exclusions that need no count forest. They are not replaced by every transitive
alternative in an old source graph.

## Why the fresh global constructor is required

Each INITIAL accepts an untrusted complete supplied proof candidate by
reconstructing all12 unseeded feedback covers and the export cover:13 covers
of9,216 signed rectangles,119,808 total, with all100 ordered probability panels
and all12 original corruption controls.

Its accepted receipt includes `seconds`. The archived global resource candidate
binds that historical timed receipt through `initial_acceptance_sha256`.
Consequently that candidate is not selected as an input for a direct fresh
global acceptance. The new protocol constructs all100 global resource rows
under the actual fresh INITIAL receipt, preserves the resulting candidate bytes,
and then runs the full original global acceptor again, including all12 controls.
No old timed receipt is substituted or rewritten.

Each selected local proof candidate instead binds the unchanged INITIAL proof
SHA and its entire selected local source map. The local algorithm recomputes
its own corresponding global resource row and every finite local feedback
cycle. Full unchanged local acceptance is therefore possible with the supplied
local candidates. It verifies complete object equality and all15 original
controls for these selected cases. The new outer readback also requires the
local recomputed global row to equal the row in the fresh complete global proof.

The B4 two-cycle variant has the same INITIAL proof and INITIAL source manifest
as the canonical B4 capsule, but a different local `acquire_panel.py` commitment
in its complete panel manifest. The global resource stage is executed once in
the canonical capsule. Only after its full acceptance are its actual INITIAL
receipt, global proof and global receipt copied byte-for-byte into the selected
two-cycle alias. Their hashes are bound in the stage ledger and rechecked on
restore. The canonical global stage is not rerun under a different local source
map. The old `TWO_CYCLE_PORT.json` remains an immutable historical description,
not fresh evidence for its old parent hashes.

## Scope of the original local arithmetic

| Selected local panel | Cycle limit | Candidate cycles | Complete cover calls | Candidate outcome |
|---|---:|---:|---:|---|
| B4:18,19,20,21,23 |2 |2 each |8 each |survivor |
| B4:22,24 |8 |8 each |32 each |survivor |
| B4:25 |8 |4 |16 |excluded |
| B4:26 |2 |2 |8 |excluded |
| B4:27,28 |2 |1 each |4 each |excluded |
| B5:18–24 |8 |8 each |32 each |survivor |
| B5:25 |8 |2 |8 |excluded |
| B5:26 |8 |1 |4 |excluded |

These are structural censuses read from the complete archived candidates,
not newly recomputed inequalities. B4 has136 and B5 has236 mathematical local
cover calls. Each call covers9,216 signed rectangles. The exact-stage cache
starts empty in every local acceptance, only memoizes identical complete
arguments, and never receives a serialized candidate result as a seed. The
new evidence validator reconstructs the typed argument multiplicities and
requires the exact reported calls, misses, hits, helper identity and output
hashes. Full original resource workers remain separate child processes.

## Source and process evidence

[The source module](../be_replay/middle_n25_acquisition_sources.py) selects169 B4
and89 B5 source/candidate files. This includes complete COPY/PANEL/resource
manifests, exact helper sources and selected local candidates. Static review
objects are explicitly conditional premises. Historical INITIAL/global/local
accepted outputs and archived global resource candidates are absent from the
execution inputs.

The deterministic selection SHA-256 values are:

- B4: `ae04f71430b83232a7df7f63745e8680df618920be6c4a148872259d600a2961`.
- B5: `694190b2024ae7dcd8f3d142e94ef7fe8c559a3da3e10837650959cda6e91154`.

[The runner](../be_replay/middle_n25_acquisition.py) uses the new BASIC Linux
process-group epoch, with CPU and wall ceilings each64,800 seconds per action,
a2GiB memory policy,512MiB sampled file limit and16MiB log limit. These are
safety budgets, not runtime estimates. Per-process limits and sampled live-group
RSS/CPU are not cumulative whole-tree CPU or aggregate cgroup guarantees.

[The evidence validator](../be_replay/middle_n25_acquisition_evidence.py) checks
actual commands/cwd, exact budgets/guard fields, integer-zero exits, stopped
supervisor receipts, full stdout hashes and empty stderr, exact original terminal
markers, immutable inputs, complete source dictionaries, all controls and parent
proof/receipt edges. Every ledger binds the entire preceding ledger prefix.
Completed-prefix ZIPs have safe bounded exact member sets, actual sidecar/member
hashes and full post-restore evidence validation. Recorded capture and receipt
bytes are never rewritten when interpreting their original task prefix.

Only checked completed stages are reused. An interrupted individual stage
restarts fully. Live backups contain logs/ledgers and do not constitute an
accepted partial calculation. Durable directories are
`MyDrive/Berry-Esseen-end2end/middle-n25-b4/` and `middle-n25-b5/`.

## Validation and remaining obligations

Actual source-only preparation and complete epoch verification passed for all
169/89 selected inputs. A separate readback of the actual archived JSON artifact
schemas passed all14 B4 and12 B5 planned stages, including cache counts, exact
source dictionaries, controls and candidate bindings. This metadata-only check
did not supply process observations and is not fresh acceptance. No original
mathematical module was imported.

The19 synthetic infrastructure fixtures passed in41.865 seconds (`-B -S`,
repository-owned temporary directory). They cover a full fake INITIAL/global
construct/global accept/local chain, fresh canonical parent aliases, restoration
of a constructed global prefix before acceptance, relocated captures, corruption
controls and rejection of stale parent/cache metadata. Fixture kernels contain
tripwires and are never executed.

The API is `middle_n25_acquisition.run_colab("b4" or "b5", durable_root=...)`.
[The generator](../tools/make_middle_n25_acquisition_notebooks.py) builds only
notebooks47/48 with a full immutable runtime commit pin. Existing notebook/runtime
pins remain unchanged.

These middle routes use the universal same-law predecessor and the literal
allowance `441991/2000000`; they do not require sharp global C24. Success records
conditional acquisition arithmetic only. Same-witness analytic reductions,
support/HIGH/kernel assumptions, full numeric resource-to-count interfaces,
regional seam/union composition and the n25/all-index theorem remain separate.
The retained forests are computed independently by notebooks32/33.
`native_arithmetic_accepted`, `resource_interfaces_verified`, count acceptance,
`full_n25_verified` and the all-index conclusion remain false.
