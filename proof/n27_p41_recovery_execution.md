# Notebook64: original n27/p41 construction and full conditional replay

This implements the source-only design in
`n27_p41_recovery_source_plan.json`, SHA-256
`94d5a0048c619a86666c94fc7ba93d7cb5bfee602c3e505e663d5ee2583fc814`.
That unchanged proposal describes the original algorithm and source provenance;
it is not an execution receipt. The new implementation has not run original
mathematics locally. Development uses source/AST/JSON reads and synthetic process
fixtures. This is fallible internal AI engineering/source review, without external
independent mathematical verification.

## API and exact original inputs

```python
from be_replay.n27_p41_recovery import run_colab
RESULT = run_colab(durable_root=DURABLE, backup_interval=60)
```

The result has `status`, `bundle` and `work`. Source preparation downloads the
public `cutoff25_20261011.zip`, 514,958,998 bytes, SHA-256
`17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`,
from the existing `cutoff20-sources-2026-10-17` GitHub release. Existing local
copies are verified by whole-file size/SHA. The exact selected directory is
`cutoff25_20261011/new_middle/actual27_30_b0_plan_v1/actual27_count41_prototype`.

The capsule contains exactly 43 unchanged source inputs, 160,351 bytes: all 39
kernel-manifest files, that manifest, the contract, checker and alpha4 constructor.
This family has no `FROZEN_DESIGN.json`; no alternative historical design seal is
invented. Its own old forest, construction receipt and acceptance are excluded.
Only the three explicit fresh output filenames may subsequently coexist with
the sealed inputs.

Actual source-only preparation was completed and recorded in
`n27_p41_recovery_source_preparation.json`. All 43 input hashes matched, and an
AST-only traversal found 22 reachable Python files, 36 sealed sibling-import
edges and no unresolved import. Its control-name list exactly matches all 24
original source mutations. No original module was imported or evaluated.

## Two required original actions

1. Execute unchanged `python -B -S construct_alpha4.py` in the new capsule.
   Its original alpha priority4, 10,000 global-node limit, depth128 limit and
   600-second elapsed check at node entry remain byte-identical. The time check
   does not interrupt an individual ongoing leaf evaluation. A larger external
   budget does not replace the original internal check.
2. After complete construction evidence passes, execute unchanged
   `python -B -S count_protocol.py accept` in that same capsule. It reconstructs
   all original closed boxes and freshly recomputes every leaf and all 24
   original corruption controls.

The constructor catches ordinary exceptions and can return code zero while
reporting `BOUNDED_CONSTRUCTION_NOT_COMPLETE`. Zero exit alone never starts the
acceptor. Construction requires its exact
`STORED_CONDITIONAL_FOREST_CONSTRUCTED_NOT_ACCEPTED` packet, unchanged input
hashes, newly written whole forest, exact native header and all 28 ordered roots.
The new outer reader independently reconstructs binary split geometry and exact
leaf boxes, counts every node/leaf, and requires the unchanged 10,000/128 bounds.
The original numerical evaluator is called only by the native Colab actions.

The exact target literal is
`76824784444199314310731654405729617052063596250011448874609/187500000000000000000000000000000000000000000000000000000000`.
It was read as metadata from the source-pinned n10/B0/p36 forest
`cutoff10_20261018/root/count10_v2/B0/capsule36/COUNT36_FOREST.json`, SHA-256
`e7b1033f33287215672fa0113ddb10c31958a64f118ee1a07eeb84d5da5cd4d8`,
which binds the identical `finite_gaussian.py` CE_LO definition. No Gaussian
constant was recomputed locally. The unchanged n27 checker also recomputes its
header target during fresh acceptance; this metadata comparison does not replace
that check.

Acceptance requires the complete
`PASS_FRESH_CONDITIONAL_ACTUAL27_EXACT_COUNT41` receipt: actual new forest SHA,
unchanged checker/contract/all39 kernel hashes, all24 named controls in original
order, complete fresh-leaf count and exact statistics reconstructed from the
whole closed forest. Only the receipt's finite nonnegative elapsed field is
variable. All other fields and the complete original scope text are required.
The actual terminal JSON must equal the freshly written whole receipt.

## Execution, transport and reuse

Each action has the explicit BASIC process-group policy: 2 GiB memory allowance,
7,200-second per-process CPU ceiling, 7,260-second external wall ceiling,
256 MiB sampled private-disk ceiling and 16 MiB logs. Per-process hard limits and
sampled live-group CPU/RSS do not provide cumulative CPU for reaped descendants,
aggregate kernel memory enforcement, cgroup/Windows-Job equivalence or containment
of descendants changing sessions. Native-platform acceptance remains false.

Both actions record actual launch/cwd/arguments, budgets, supervisor result,
guard scope and bounded stdout/stderr hashes. Successful stderr must be empty.
The entire constructor packet and forest, and later the entire acceptance, are
requested as stopped-supervisor captures. Native files, copied captures, original
paths, byte counts and hashes must match. The constructor forest cannot change
between construction and acceptance. Original sources are rechecked throughout.
Failure retains observed ledgers, captures, bounded diagnostics and a final ZIP.

Twenty-second supervisor heartbeats show actual process observations; sixty-second
backups contain logs and ledgers. Only a fully validated completed TWO-action pair
is exported as a reusable ZIP with its SHA sidecar. ZIP import rejects unbounded
inventories, traversal, links, encryption, duplicates/case collisions and missing
pair evidence before extraction, then revalidates the complete relocated pair.
Original launch, receipt and capture bytes are never rewritten. Interrupted or
partial numerical work restarts fully; no constructor checkpoint is invented.

`n27_p41_recovery_evidence.validate_completed(task)` is a pure metadata/source/
geometry readback API. It imports no original kernel and does not rerun a leaf.

## New evidence boundary

The fixed original contract remains n27, panel41, K=0, p in[41/100,21/50], rho
in[1,11/10]. It assumes the separately unacquired sharp global C26 predecessor
and same-witness resource/acquisition facts. A complete new forest may have
different topology, census and SHA from the missing historical forest. Its new
candidate and acceptance hashes are exported under a new explicit evidence epoch;
the missing old hashes remain provenance only.

Success records `new_candidate_full_conditional_count_computed_basic`. It never
rewrites the historical composer's old forest/acceptance pins or pretends that
the historical byte edge has been replayed. Notebook53 remains NOT_READY at79/80
until a separate source-bound same-contract semantic replacement join is reviewed
and implemented. This module does not modify that catalog or its readiness.
Parent acquisition, semantic replacement, native-platform acceptance, lane53
readiness and the all-index theorem remain false. No completion, timing or
historical-census reproduction is promised for the unchanged bounded constructor.
