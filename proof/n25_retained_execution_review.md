# Retained n25 B0–B2: source-only execution review

Reviewed on 2026-10-23. This review specifies a runnable next lane; it does not report a new native acceptance. No mathematical source was imported, no leaf was evaluated, and no constructor, search or acceptor was run.

## Selection and available bytes

Use exactly the 75 `jobs` in [the retained catalogue](n25_retained_b012_catalog.json), schema `N25_RETAINED_B012_SELECTED_COUNT_CATALOG_V1`, SHA-256 `f055b5017d4e1fd14f2b48a6a95fef4a4c61a025dea6174c424cd5968de801f7`. Its [companion inventory](n25_retained_b012_catalog.md) explains the historical selectors and supersessions. The catalogue is a selection/provenance input, not fresh arithmetic evidence.

All selected payloads belong to `cutoff25_20261011.zip`, expected size 514,958,998 bytes and SHA-256 `17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`. The later base13 archive supplies historical selection context; these 75 replays do not need its payloads. The source-preparation step must verify the complete public archive pin before extraction.

| Separate Colab job | Selected acceptors | Saved complete roots | Saved leaves | Saved forest bytes | Full frozen source rows |
|---|---:|---:|---:|---:|---:|
| B0 | 17 | 442 | 12,985 | 25,067,448 | 573 |
| B1 | 35 | 910 | 47,946 | 91,877,650 | 1,925 |
| B2 | 23 | 598 | 33,357 | 63,672,704 | 1,504 |
| Total | 75 | 1,950 | 94,288 | 180,617,802 | 4,002 |

Each complete saved forest has 26 ordered roots and zero pending nodes. The largest has 9,620 nodes; every original acceptor has `LIMIT=10000` and a maximum replay depth of 128. The largest observed saved depth is 24 and the largest candidate is 10,269,525 bytes. These are exact stored-object censuses, not fresh arithmetic results or runtime estimates. This lane needs no resource-limit source patch and no search or fresh forest construction.

## Exact closure and platform findings

This readback went beyond the catalogue's 3,826 runtime input rows: it opened every selected historical `FROZEN_DESIGN.json` and independently SHA-matched all 4,002 declared member rows against actual archive bytes. All matched. Full designs contain 27–76 files per job; copying only the 21–71 kernel-manifest entries would omit some sealed source-epoch material.

The additional frozen filenames, depending on the job, are `EXACT_GLOBAL_INTERFACE.json`, `SOURCE_PORT.json`, `SOURCE_TRANSFORMS.json`, `SPLIT_FIXTURE_SOURCE.json`, `THETA_ALLOCATION_PORT.json` and `construct_alpha4.py`. Preserve them unchanged when they occur in the actual design. Historical checked/review/interface JSON must be classified as conditional source/premise material. Their inclusion does not mean that their claims were acquired in this replay.

All 156 distinct Python source hashes in these full designs were parsed statically. Local imports resolve within their selected flat capsules; other imports are standard-library modules. No selected source imports subprocess, thread/process launchers, ctypes, resource, or Windows-specific modules. The only dynamic import found is the literal `__import__('math').factorial` in `finite_gaussian.py`, line 26. No source/platform blocker was found for the established single-process Python native guard. Actual guard capability, memory use, runtime and arithmetic completion still require Colab execution.

## Original action and receipt contract

For every job, invoke the unchanged script in a private flat capsule:

```text
python -B -S count_protocol.py accept
```

Use `sys.executable` and an absolute script path in the actual launch, with `cwd` equal to that capsule. Copy its exact full frozen inputs, unchanged `FROZEN_DESIGN.json`, and the SHA-pinned `COUNTINDEX_FOREST.json` candidate. The fresh capsule must initially contain no `COUNTINDEX_ACCEPTED.json`. That historical acceptance filename is catalogue selection/schema evidence and must not be extracted as fresh output.

Every original acceptor:

1. Rehashes its full declared kernel map and loads one literal n25 contract row.
2. Reconstructs all 26 original five-dimensional closed root boxes, including the signed coordinate `[-1/2,1/2]`; checks strict interior rational cuts and both closed children; and checks every stored leaf box against the reconstructed box.
3. Starts with an empty evaluation cache and recomputes the retained `cell35` decision/result for every original leaf. A leaf must close through an admitted named empty status or a strict score bound below the frozen `CE_LO`; its complete saved result must match.
4. Runs 24 corruption controls in an exact order, reusing the main replay's evaluation cache. That cache is keyed by the count and the complete reconstructed box; it does not import a historical arithmetic cache.
5. Rechecks source hashes, writes a fresh acceptance JSON only if the destination is absent, and prints that complete JSON.

All 75 supplied receipt schemas agree. The exact fields are:

```text
status, forest_sha256, contract_sha256, checker_sha256, kernel_sha256,
statistics, negative_controls, fresh_leaf_evaluations, seconds, scope
```

The original status is `PASS_FRESH_CONDITIONAL_EXACT_COUNTINDEX`. `statistics` contains exactly `nodes`, `leaves`, `closed_statuses`, `maximum_score` and `maximum_depth`. The 24 ordered control labels in every historical receipt match those extracted from its actual pinned checker AST. They cover type-sensitive n/index/count fields, target/contract/kernel/checker identity, missing/reordered roots, split children/axis/cut, leaf box/decision/result, unknown nodes and extra success claims.

Fresh output must bind the actual complete forest, contract, checker and kernel bytes; its statistics must equal the independently parsed complete candidate census, closed-status counts, rational maximum score and depth. Require `fresh_leaf_evaluations` to be a literal integer equal to the full leaf count and require all 24 labels exactly. Do not compare fresh elapsed seconds or the whole fresh receipt hash with historical elapsed seconds/receipt hashes: those are execution-specific.

## Initial design proposal, followed by the implemented interface

The following interface and two-hour example were the initial design proposal.
They are retained as review history, **not the implemented API or current
execution defaults**. The actual implementation is described immediately below.

```python
prepare(branch, archives, task, *, download=False)
run(task, *, wall_seconds=7260, cpu_seconds=7200,
    memory_bytes=2 * 1024**3, resume=True)
validate_completed(task, *, original_task_root=None)
run_colab(branch, *, durable_root,
          work_root="/content/berry-esseen-runs",
          archives="/content/berry-esseen-archives", resume=True)
```

The proposal required only `b0`, `b1` or `b2`, serial selected jobs within each branch and three independent branch notebooks. Its suggested resource values were a starting policy, not evidence that every action would finish within them.

The earlier proposal identified `aux24_sources.prepare` as a possible transport layer. The implemented lane instead uses its own retained-n25 source adapter and schemas; it does not relabel n25 arithmetic as an auxiliary24 acquisition.

### Implemented lane and reviewed execution boundary

The current [runner](../be_replay/retained_n25.py) exposes
`run_colab(branch, *, durable_root, work_root=..., archives=..., backup_interval=60)`.
It uses [the retained source adapter](../be_replay/retained_n25_sources.py), whose
interfaces are `prepare(branch, archive, output)`, `verify(task)`, `jobs(branch)`
and `census(job, capsule)`. The distinct
[evidence validator](../be_replay/retained_n25_evidence.py) provides
`validate_run(...)` and
`validate_stage(task, job, epoch, *, original_task_root=None)`.

Each complete native action now has an explicit **43,200-second CPU ceiling,
43,500-second wall ceiling and 2 GiB memory policy**. These are bounds, not
runtime forecasts. All original numerical sources, the original 10,000-node
limit and the selected candidate forests remain unchanged.

The source adapter binds the exact catalogue and the union of its actual runtime
rows and full historical frozen design, plus the design and candidate. It writes
deterministic retained-n25 manifests, verifies exact full closed geometry without
evaluating a numerical kernel, and excludes archived acceptance outputs.

Completed native stages are exported separately as append-only ZIP/SHA pairs
under each branch/job cache. The runner preflights the entire bounded ZIP before
extracting a member, preserves original capture/receipt bytes, and reuses a stage
only after full relocated evidence validation. Live backups copy logs and small
ledgers rather than repeatedly copying all immutable mathematical inputs. Final
result bundles preserve the full task evidence. The native record remains
conditional: parent acquisitions and the all-index conclusion stay false.

This source-only readback found no blocking issue in the current runner's
stage-cache preflight/export/import and fresh source/guard/capture/receipt
validation path. It did not run the mathematical acceptors or establish their
analytic premises. Synthetic orchestration fixtures and actual source-only
preparations remain distinct from Colab arithmetic.

For each job, derive the selection from the actual pinned full frozen design and verify it against its catalogue design hash. Include every frozen member plus the design and candidate; classify only the forest as a new untrusted candidate. Do not select every directory mentioned by historical source graphs. Bind exact selected job IDs/order, branch source manifest, catalogue hash, driver/supervisor/validator hashes, source archive pin, per-job contract/checker/design/forest hashes and the original conditional scope in the outer task record.

The existing stronger24 runner is an orchestration example, with BASIC supervision explicitly recorded. The retained lane can use the established `trusted_native` Python path and should validate its actual guard receipts accordingly. The seven-target `count_task` validators have fixed target assumptions and should not be applied to arbitrary retained catalogue rows without an explicit generic schema implementation.

## Resume only complete verified stages

Keep immutable prepared inputs separately from private per-attempt native capsules. Name each stage by its literal catalogue job ID; make a fresh attempt directory for an incomplete or rejected stage. The original acceptor has no partial replay checkpoint protocol, so an interrupted accept action must replay that whole job. Already completed jobs can be retained after full validation; there is no need to replay earlier valid jobs merely because a later action was interrupted.

A stage is reusable only after validating actual source/candidate bytes and the complete fresh acceptance chain: exact integer return code zero, completed native mode, explicit resource policy, worker/controller guard files, actual launch command/context, saved supervisor-result equality, both bounded capture hashes, empty stderr and complete stdout JSON equal to the fresh receipt. Keep `proof_accepted=false` at the supervisor layer. Recheck the sealed capsule after execution and allow only the designated fresh acceptance output beyond its inputs. A status string, file existence or historical acceptance is insufficient.

For restored bundles, use an explicit original-task-root mapping. Preserve original argv, capture paths, timestamps and receipt bytes; do not rewrite them to imitate execution at the restore location. A deterministic ledger should bind each accepted job's inputs, output receipt, native report and captures. Branch completion requires the exact selected set of 17/35/23 fully validated jobs and matching aggregate census, with no duplicate or substituted target. A branch packet can report fresh conditional native arithmetic while keeping resource acquisition, parent composition and global proof flags false.

Save durable stage start/end events and periodic wall/CPU/RSS heartbeat data. Report completed job and fully accepted leaf counts. The unchanged acceptor prints its full receipt at completion; the outer wrapper must not invent an in-flight leaf percentage or an ETA.

## Representative selection rows and remaining premises

All prefixes below are relative to `cutoff25_20261011/`; the complete exact hashes and closed p/rho domains are already in the pinned catalogue.

| Target | Selected capsule prefix | Forest leaves | Full frozen files | Selection implication |
|---|---|---:|---:|---|
| `b0-p37` | `new_low/count37_global_conditional_v2/` | 871 | 27 | Whole selected panel |
| `b1-p35-q0` | `new_root/local_theta_b1_p35_q0_v4/` | 1,240 | 42 | Requires the separately acquired B1 p35 local interface |
| `b1-p40-q0` | `new_root/global_tangent_b1_p40_q0_v1/` | 1,765 | 46 | Selected tangent quarter |
| `b1-p40-q2` | `new_root/global_joint_cubic_b1_p40_q2_v3/` | 2,797 | 52 | Superseding selected joint-cubic quarter |
| `b2-p31-q3` | `new_root/local_joint_cubic_b2_p31_q3_v5/` | 3,600 | 51 | Supersedes local-theta q3 v4; requires B2 p31 local interface |
| `b2-p33` | `new_root/global_alpha_stoploss2_b2_p33_v12/` | 1,475 | 76 | Selected whole-panel V12 route |

The native contract rows contain `K=0`, branch and p bounds, support/window and charge budgets, signed marginal assumptions, acquired beta/mean intervals, and in some routes an acquired theta cap. These inputs explicitly include `ASSUMED_ACQUIRED_FOR_CONDITIONAL_TEST`; the acceptor does not turn them into an acquired parent resource. B1 p35 and B2 p31 each additionally require the selected separate 16-cover local acquisition. The 83/89/89 resource-excluded panels in B0/B1/B2 are outside these 75 count replays.

No missing payload or execution-contract blocker was found in this source-only review. Fresh native arithmetic, source-algebra justification, same-witness parent/local resource acquisition and interfaces, the remaining n25 regions, stronger24 acquisition and the final n25/all-index joins remain separate work. This availability finding supports starting the conditional retained replay lane now; it does not require restarting the ongoing seven recovery searches or the B3/B4 parent jobs.
