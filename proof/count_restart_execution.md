# Seven PREFIX2 resume notebooks

The numbered `01_RESTART_...` through `07_RESTART_...` notebooks resume the
seven existing conditional n25 count jobs. The discovery policy is
`RESTORED_PREFIX2_V1`, with alpha 16 and depth-first traversal. The 100,000-node
native source epoch, 2 GiB memory policy and 12-hour budgets remain in force.
The strategy change affects how unfinished regions are explored; it does not
change the mathematical contract or turn a saved search decision into proof.

The restored policy uses the original feasible-prefix cuts, factor-16 weighted
widths and strict physical-prefix lookahead, together with the selected original
accelerators. Its eight retained helper files have a separate provenance
manifest under `vendor/count_75a9470/prefix2_original/`. The canonical-checkpoint
transport and source-admission adapter is new; this is not a claim that the
entire original constructor is copied byte for byte. The frozen native checker
remains the separate arithmetic acceptance route.

This document describes execution and evidence transport. Source review and
small synthetic infrastructure fixtures are fallible internal AI checks, not
external verification. No mathematical search or leaf replay is run locally as
part of preparing these notebooks. Actual arithmetic acceptance requires the
recorded Colab execution described below.

The prepared notebook set selects runtime commit
`3ed14a94abe5dbd9f0c111fc85db79c353e7d2ba`. The matching notebook24 includes
the new migration readback and the exact previous implementation tuples;
completed compatible earlier exports remain eligible for full validation.

Preparation validation on23 October2026 covered162 infrastructure cases, with
zero failures/errors and one intentionally inapplicable legacy-q2 case skipped.
The final seven notebooks and notebook24 match their generators, have clean
outputs, compile as Python, and bind that full immutable runtime commit. The
14 vendored discovery/preparation files and six runner/evidence files were
also compared with the actual Git commit blobs, preserving byte pins on Linux.

The [actual seven-export migration record](count_prefix2_migration_sourcecheck.json)
checks original checkpoint bytes, every root/split/leaf payload, strict closed
geometry, identical before/after censuses, idempotent remigration and source
compatibility with all original accelerators. Those inputs are the earlier
exported snapshots:4500/2865/2920/4996/3404/1322/1469 leaves. They are neither
the latest live counts nor a forced resume point; a compatible later descendant
must be selected at execution. These checks import no mathematical kernel and
perform no numerical search, leaf acceptance or timing benchmark.

## Moving an existing session

1. Keep the earlier notebook, logs, result ZIPs, SHA-256 sidecars and live Drive
   folders. Do not delete or rename the target's backup directory.
2. In the old running session, wait for a recent `backup_saved` message. Backups
   normally run every 60 seconds. Then stop that numbered job. Do not run two
   sessions for the same target at once.
3. Open the new corresponding number, select CPU, choose **Run all**, and
   authorize the same Google Drive. A new published copy is used so that saved
   outputs in the old notebook are not overwritten.
4. Before the first search slice, read the selected checkpoint path and hash and
   the restored node, leaf and pending counts. These must identify the work being
   resumed. If selection fails, keep the diagnostic ZIP; do not clear the cache
   or substitute an empty search.

No ordinary path or parameter edit is required. The durable root remains
`/content/drive/MyDrive/Berry-Esseen-end2end`. Each target keeps its existing
subdirectory, for example `b4-q2/`, and each new session writes a separate run
folder underneath it. The seven different targets may run in separate CPU
sessions. Each session uses one discovery worker.

The controller reads compatible saved checkpoints from the live backups and
verified result archives. It validates source/header bindings and full closed
tree geometry before migration. It selects a unique maximal descendant by tree
ancestry. A later timestamp, a larger leaf count or a lexicographically larger
filename is not enough to decide between different lineages. Identical backup
copies may be deduplicated. If two valid maximal candidates are incomparable,
selection stops with their paths and counts instead of silently choosing one.
A missing or incompatible cache also stops explicitly. There is no fallback to
new empty roots.

## What migration preserves

The exact selected incoming bytes are retained as `SOURCE_CHECKPOINT.json`.
The separately recorded input binds those trees to the current source and
discovery strategy. Every existing tree, leaf payload and pending region is
preserved; only the explicit source/strategy header fields may be migrated.
Before/after counts and a digest of the root data record this preservation.
The checkpoint remains `arithmetic_accepted=false`.

The selected source, restored counts and strategy are printed before search.
A typical log has the following meaning; values come from the selected cache,
and the example counts are illustrative rather than a required final census:

```json
{
  "event": "untrusted_checkpoint_migrated",
  "source_checkpoint": ".../b4-q2/<saved-run>/live/task/.../CHECKPOINT.json",
  "source_checkpoint_sha256": "<64 hexadecimal characters>",
  "before_statistics": {"nodes": 10000, "leaves": 4996, "pending": 17, "maximum_depth": 20},
  "after_statistics": {"nodes": 10000, "leaves": 4996, "pending": 17, "maximum_depth": 20},
  "roots_preserved": true,
  "arithmetic_accepted": false
}
```

The event also includes `source_strategy`, `target_strategy`, `roots_sha256`
and `rejected_checkpoints`. The target strategy records
`discovery_strategy=RESTORED_PREFIX2_V1`, `alpha_priority="16"` and
`traversal="depth"`, together with its bound source digests. The same migration
ledger is saved as `SESSION_RESULT.json.checkpoint_migration`. The actual event
contains additional fields; the excerpt above is not a native acceptance
receipt. The original
seven-cache inventory is preserved in [the handoff note](count_cache_handoff.md).
Those earlier counts are a historical floor, not an instruction to choose an
older checkpoint over a validated descendant from a later session.

## Resource limits and interruptions

The explicit source profiles retain the resource-only native checker change
from `LIMIT=10000` to `LIMIT=100000`. Mathematical kernels, exact contracts,
all 26 ordered closed roots, strict split geometry, depth 128, strict leaf tests
and all 24 original corruption controls keep their sealed identities. The
separately identified discovery strategy must not be confused with a claim that
every orchestration source byte is unchanged.

Search uses BASIC supervision with a 2 GiB budget and up to 43,200 seconds of
search allocation, normally divided into 1,800-second slices. Native replay has
its own ceiling of 43,200 CPU seconds and 43,500 wall seconds. Its 2 GiB total
memory budget is split into a 1,984 MiB worker and a 64 MiB controller under the
existing strict Linux native guard. These are finite limits, not an ETA, a
promise that Colab will keep a session alive, or a guarantee of convergence.

The node ceiling is not the only bound. JSON/checkpoint inputs and individual
live-backup files retain a 128 MiB cap. Discovery retains the 256 MiB sampled
run-directory disk quota, which includes its copied resume input and checkpoint
copies. A quota stop is incomplete, not an accepted result. Later selection
uses the last compatible saved checkpoint that actually exists. Live backups
can omit files above their size cap: `LIVE_SNAPSHOT.json.skipped` records the
omissions. A `backup_saved` message records a backup cycle and does not assert
that an oversized file was copied. No oversized-checkpoint preservation is
promised by these notebooks.

Progress and backups are written throughout the run. On an ordinary controlled
stop the result ZIP and SHA-256 sidecar are saved to Drive; a sudden runtime loss
may leave only the most recent live backup. Rerunning the same new notebook
selects the compatible saved descendant rather than discarding those trees.
An already accepted export may be reused only after full source, capture,
guard and receipt revalidation; its saved status label is insufficient.

The narrowly recognized first q2 recovery implementation remains a historical
512 MiB, 7,200/7,260-second execution policy. It is not the policy for a new run
of these notebooks and does not authorize arbitrary old adapters.

## Acceptance and the remaining proof

A completed discovery candidate is not accepted arithmetic. A fresh native
checker must recompute every leaf of all 26 roots and perform all 24 corruption
controls, with its actual command, context, guard sidecars, source hashes,
captures, census and terminal receipt agreeing. Preserved numerical leaf values
cannot replace that replay. Reusing a previously completed native export is a
separate transport/evidence validation, not a new arithmetic computation.

The matching notebook 24 validates the seven count exports and the resource-to-
contract interfaces using the two parent exports from 09/10. It records the
source/resource epoch used for each target. The original same-law framework,
matching parent acquisitions and, for portable V14 jobs 06/07, the auxiliary C24
and attained positive-closed contact premises remain explicit. These seven jobs,
their cache preservation and their interface join do not close the global n25
region or the all-index theorem. Notebook 25 is superseded by this set's 04.
