# Selected finite6–9 INITIAL and resource replay

This is an internal, fallible source/implementation review and a new Linux
execution protocol. It is not external independent verification or a locally
executed mathematical proof. All original numerical execution is reserved for
Colab.

## Two independent bounded lanes

Notebook 44 runs `finite69_parents.run_colab('n6', durable_root=...)`:

| Original action family | Jobs | Covers or resource rows | Original controls per job |
|---|---:|---|---:|
| Full INITIAL B0, BN, B2 and outer BN | 4 | 9,9,4,9 covers; 2592 cells per cover | 20 |
| Local INITIAL refinements | 17 | 6 covers each; 2592 cells per cover | 29 for 15 jobs; 27 for 2 |
| Full resource B0, BN, B2 | 3 | Every ordered 100 closed probability panels | 16 |
| Local resource refinements | 17 | Every selected original single-panel support plan | 15 |

This is 41 complete original replay actions, 133 INITIAL covers and 872 original
named controls. The local cases include B0 panel40 and the selected BN
refinements; the literal catalog records their exact base INITIAL dependencies,
candidate/source identities and CLI arguments. They are additional acquisitions,
not substitutes for the three full 100-panel resources.

Notebook 45 runs `finite69_parents.run_colab('initial7_9', durable_root=...)`:
all nine literal indices n=7,8,9 × B0,BN,B2 INITIAL actions, nine 2592-cell covers and
100 closed panel exports per action, with 27 controls each. Its total is 81
covers and 243 original controls. These are conditional computations with the
symbolic sharp immediate-predecessor/contact-zero premise. They may run before
the separate n6 proof has been globally composed; they do not establish that
predecessor theorem.

The fixed isolated catalog is `proof/finite69_parent_sources.json`, SHA-256
`9eef9a7c11abaa6a239fbcd0890acc32e420ac56bca1a09043e4a87187c244bf`.
It derives only these 50 source-available jobs from the frozen COUNT/source
catalog SHA-256
`2a0575f59f9d6c8e95c53f68767b1cbae28b1ed2f5cd72c27a240b50d1367232`.
The existing40–43 COUNT runtime, catalog and evidence files are unchanged.

## Source closure and unchanged CLI

Both lanes use the two original public archives described in
`proof/finite69_count_execution.md`, with exact byte-size/SHA verification.
The n6 cache has 1965 files / 157195394 bytes; the n7–9 cache has 125
files / 31612444 bytes. Their shared canonical union has 2076 files.
Every selected input, source and conditional reference was extracted and
SHA-matched in a source-only preparation. All 328 inspected JSON files have
portable source-graph paths; no embedded `files_sha256` or
`original_source_graph` path required a Windows-path rewrite.

The unchanged entry sources are:

| Archive-relative entry | SHA-256 |
|---|---|
| `cutoff6_20261018/root/initial6_accept_v1/replay.py` | `291f50234973e9d292b1df79b2264bfcf79920a9a8d82fd787d36b98fa84a053` |
| `cutoff6_20261018/root/initial6_outer_accept_v1/replay.py` | `60f9888f01ff23b13f0d83168da03e405065dc7508b617a39919b0cc30c12913` |
| `cutoff6_20261018/analytic/panel_accept_v1/replay.py` | `59ef28a84cef27e307bc136d3ccc48617e50e6111911075fbcde9399621cf9e1` |
| `cutoff6_20261018/root/resource6_accept_v1/replay.py` | `da99b82cb663ac0c0111e10be88c78924574f127eff1c272acf588e2b0c7c684` |
| `cutoff6_20261018/root/refined_resource6_accept_v2/replay.py` | `bd9e28b1bdeaffdfef41a737c05ce7732724d9a2b23d2c288064044f875b3ddd` |
| `cutoff6_20261020/root/BN_resource_accept_v1/replay.py` | `e7d514ab5069ab7f2d31aebc3d577170a69a11d86d2bcf3753d4680fd01ed96e` |
| `cutoff6_20261018/analytic/initial7_9_accept_v1/replay.py` | `dfd8d2b820f1e221eaed0e6b515649a9b15dc71e66af78f947330bb8129ad5ab` |

Each child runs `python -B -S <original-replay.py> <literal arguments>` from
that entry's original relative directory in a new private capsule. The original
deep directory structure is preserved, so `H.parents[3]` resolves to the private
capsule root. No original mathematical source or function is patched.

The n6 INITIAL acceptors start their complete schedules with `raw=D=None`,
recompute every stage, require the entire candidate cover/physical invariants
and licensed final gap to match, and execute their original corruption controls.
The full resource acceptor recomputes every ordered panel from the candidate's
final INITIAL cover, including every retained support-plan history, and compares
the complete result. Local INITIAL/resource acceptors retain their full selected
schedules and complete original controls. Their source-specific candidate and
result schemas are not replaced by a generic PASS/census check.

## Missing timed INITIAL metadata

Nine original `initial7_9_accept_v1/<case>/PREPARED.json` bytes are reconstructed
by the separately pinned stdlib-only `finite69_metadata.reconstruct_prepared`.
It preserves the original POSIX insertion order and serialization, and requires
the complete original 97-file preparation manifest, 54-file origin graph, actual
candidate/INPUT aliases and externally pinned PREPARED output hash. All nine
reconstructions match those original output hashes exactly. Neither a numerical
function nor a native acceptance is reconstructed. The missing old timed
`REPLAY_CHECKED.json` files are not fabricated.

Each of those nine expected native output packets is derived only as untimed
validation metadata from the fixed candidate/profile/final invariants and the
literal original result status/scope AST. This metadata cannot complete a job:
the unchanged original INITIAL arithmetic and all 27 controls must actually run
and write a fresh receipt, under the actual execution evidence below.

## Actual execution and full stopped-output binding

Each original replay has the same new BASIC policy as the COUNT lanes:
43,200 seconds per-process CPU, 54,000 seconds external wall, 2 GiB memory policy,
512 MiB sampled disk and 16 MiB log ceilings. Per-process hard AS/CPU limits,
external wall monitoring and sampled live process-group CPU/RSS are explicit.
Aggregate kernel memory enforcement, cumulative CPU for reaped descendants,
cgroup equivalence and original Windows-Job acceptance are not claimed.

The original scripts print progress and a terminal status rather than the whole
receipt. Therefore a terminal status alone never validates a stage. The
supervisor is requested to capture the complete newly generated
`<case>/REPLAY_CHECKED.json` after its owned process group has stopped. Readback
requires its exact original source path, captured path, byte length, SHA-256,
whole captured copy and current native output to agree. The source capsule is
checked before and after execution; the job's own historical output is excluded
from its prepared inputs, and only one fresh output is allowed.

`STAGE_OBSERVED.json` is written first with false completion/acceptance flags.
Validation requires the actual source-bound CLI/cwd/output directory, current
implementation pins, fixed normalized launch budgets, the stopped BASIC
supervisor result, exact integer return code 0, actual stdout/stderr hashes and
empty stderr. It then compares the whole native receipt against its candidate
metadata: every numeric result, profile, source graph, domain, selected index and
original control label must match; only the top elapsed duration is variable.
That duration must itself be an ordinary finite nonnegative number.

Only after this readback is a fully inventoried `STAGE_COMPLETED.json` written.
`finite69_parent_evidence.validate_completed` revalidates a relocated export
without importing or rerunning an original mathematical kernel. It maps
absolute recorded captures only under the single recorded originating task root.

## Fresh timed-parent joins

Unchanged n6 child replay scripts explicitly bind archived parent-receipt bytes
in their original source/candidate metadata. Those files are retained as frozen
conditional statements in each child capsule; they are not silently overwritten
by a new timestamped receipt and their old PASS words do not acquire a theorem.

The new controller orders the fresh parent actions before their children.
For every selected INITIAL/local-INITIAL receipt dependency, it revalidates the
complete fresh parent stage and compares the entire old conditional packet to
the actual fresh packet, excluding **only the top-level `seconds` field**.
Every mathematical, source, profile and nested field must still agree.
Nested durations or changed numerical facts are not ignored. Each interface
records both actual receipt hashes and the fresh completed-stage hash.

This joins the exact conditional numerical facts used by the unchanged child
computation. It does not assume byte equality of two elapsed timestamps, and
does not promote a historical receipt to fresh execution. It also does not
acquire the external HIGH/owncap/support/predecessor assumptions. Whole-lane
`fresh_parent_metadata_interfaces_verified=true` means only these explicit
old/fresh numerical-packet joins passed.

## Cache, scope and remaining work

Progress/actual stdout is forwarded every 20 seconds, with log and ledger backups every 60 seconds. A completed job is revalidated before its ZIP+SHA sidecar is
saved. Later RunAll reuses only fully restored/revalidated completed stages;
it recomputes the fresh parent metadata joins. No partial numerical resume is
implemented or accepted. Earlier complete stages remain reusable after a later
failure. A final results ZIP is saved on success or handled failure.

The only successful batch state is
`complete_selected_conditional_parent_arithmetic_basic`, after the literal
complete ordered job list and all relevant joins. Native acceptance, external
parent acquisition, full analytic-framework/fresh-parent-fact proof, unrestricted
finite6–9 conclusions and the all-index theorem remain false. The native
receipts' original status wording does not override these limits.

Fresh full n7–9 resources and their tighter owncaps/CAPS dependency are excluded
from 44/45. The separate missing old plan/capture ancestry and fresh Fourier/CAPS
epoch are described in `proof/finite69_source_reconstruction_review.md`.
The complete support/HIGH/Fourier and same-witness resource-to-count proofs,
global sequential predecessors and final regional composition also remain
separate. These two notebooks are useful complete conditional arithmetic lanes,
not a claim that every finite6–9 obligation has already been packaged or proved.

Synthetic infrastructure tests use mathematical import traps and a fake child;
they test whole stopped-output capture, strict receipt/control/source gates,
timed-parent comparison, completed-cache relocation/reuse, missing dependencies,
false-scope rejection and failure export. The real-source preparation and tests
execute no original mathematical function.

## Notebook44underscore routing repair

The supplied21:21UTC log completes and saves the four full n6INITIAL actions,
then fails before launching `n6.panel.b0_40`: the controller's safe identifier
pattern omitted ASCII underscore. The literal catalog legitimately contains
17such local INITIAL identifiers. Allowing underscore fixes routing; all50
actual44/45job identifiers retain unique unchanged slugs. Path separators,
drive names, whitespace and nonstring inputs remain rejected.

The mathematical source/preparer/catalog and numerical/control requirements
are unchanged. Completed-stage validation accepts either the exact new runtime
or one complete ten-field implementation table from the original published
runtime `a6f49554d4024df7cf4cc86e65cd63013a190873`. Every old table entry was
independently checked against that Git commit's actual blob bytes. Individual
mixed hashes, omitted/extra fields and mismatched observed/completed runtime
tables fail. No cached receipt is rewritten and no validation rule is omitted.

The replacement44notebook revalidates the four preserved old completed-stage
ZIPs and can reuse them before starting the fifth action. This behavior passes
a synthetic four-old-stage fixture; actual user exports are accepted only after
their own complete readback in Colab. Existing45runs retain their immutable
old source commit and do not require restarting for this44routing repair.
