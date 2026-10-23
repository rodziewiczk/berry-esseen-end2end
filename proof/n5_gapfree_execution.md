# Independent Linux execution of the n5 gap-free rectangle

This module implements a new bounded Linux replay protocol. No mathematical
checker, leaf evaluator or Gaussian calculation was executed locally while
preparing it. Preparation and mocked execution fixtures do not establish
native acceptance. A real Colab run and its preserved guard, source and log
evidence are required.

## Exact scope

The mathematical target is the **positive closed CDF discrepancy** for
standardized iid marginals at n = 5, rho in [477/400, 6/5], beta in
[17/50, 35139006743001/100000000000000], and every real threshold. Its strict
normalized upper target is 4097/10000. This is one signed rectangle. It does
not establish the opposite discrepancy, a reflected rectangle, unrestricted
C5, any other fifth-index atlas row, or an all-index conclusion.

The unchanged checker reconstructs the 12 beta cells and five phase cells,
all 60 compact roots, 1,994 binary-tree nodes and 1,027 leaves. Every leaf's
rational Gaussian bound is evaluated afresh and compared with its stored
outward integer upper bound and the strict target. Separately, `exterior`
reconstructs the same-law conditional variance bounds and the complete
rays z <= 0 and z >= 5. Their respective candidate upper bounds must be
strictly below 331/1000 and 187/1000, hence below the target. Neither an old
receipt's status nor its execution metadata is a mathematical premise.

The self-contained analytic reduction and remaining n5 interfaces are
reviewed in `proof/n5_analytic_review.md`. In particular, the reduction does
not require contact, bounded support, a physical gap or C4. Acceptance of
this finite job supplies only its stated positive closed rectangle.

## Frozen closure

`vendor/n5_gapfree_75a9470/MANIFEST.json` has SHA-256
`3f38d156e97f82132772b6c21aeffe4f6ad6ca254417882331fe8a9738617a40`.
The selected files are byte-identical to their sources:

| File | SHA-256 |
| --- | --- |
| check.py | 56fdf5d1bd98e07f6c1244997778d881e339de7945deb9738f0c27060ab87f3b |
| FOREST.json | 8603a74e850b5570b8c8e64b59113b2ad2510174a3fdeb278e83451467335e47 |
| EXTERIOR.json | 383ccfa6e3b068743c7ba882e6f166ef5f1a61a1229d7ca46b008dc8af771c5f |
| c5_gapfree_worker.py | 9e00ef595f600dc57d919803ca8848f14c85d606a81d1d589665c3b28a0d7754 |
| LICENSE | cd780a1d309ec3d7adf42b87b75430b8231e8c42161fc5cb3452188b2af4bd80 |

The first three files come from `cutoff5_20261020.zip`, 141,304,365 bytes,
SHA-256 `8428002462d4e650613ea6e2ff673cb1e69c2079572cc40546d125349d582419`.
Their full literal archive member names are recorded in the manifest. The
checker is `audit/gapfree5_readback_v1/check.py`, the forest is
`root/gapfree5_exact_v1/FOREST.json`, and the exterior candidate is
`high/gap_free_count_review_v2/CHECKED.json`, all under the archive's
`cutoff5_20261020/root/delivery_extract_v1/work/cutoff5_20261020/` prefix.
The complete supplied archive hash and selected member bytes were checked.

The independent worker is
`moment-defects/reproduction/all_indices/c5_gapfree_worker.py` and the MIT
license is `LICENSE`, both fetched at commit
`75a94708872e2bc053f42a279559b23ed91e4402` of
`rodziewiczk/berry-esseen-045-certificate`. No frozen algorithm or source
path expression has been edited. All selected source bytes and the exact
inventory are checked before and after execution.

## Executed protocol

`prepare` only checks source identities, traverses JSON structure, and
copies a new deep private capsule. It imports no mathematical checker.
Its depth preserves the original checker's unused `H.parents[3]`
expression on Linux. The capsule initially contains exactly the selected
five files, the pinned manifest, this adapter, and two new input/request
files. No historical acceptance output is copied. A previous attempt is
never resumed or accepted as an input.

Inside the guarded child, the adapter invokes the unchanged independent
worker's `main()` once through `runpy`. That worker calls unchanged
`validate(forest)` and `exterior(exterior)` and performs its sixteen
corruption controls. The original checker's `main()` is never invoked:
that historical entry point reads old absolute-path execution captures.
The selected arithmetic functions do not use those captures.

The sixteen unchanged controls reject: missing, duplicate and reordered
roots; wrong rho and target; Boolean root and phase indices; a root-domain
gap; a missing tree; a false leaf and Boolean leaf; an extra forest field;
and four false exterior inputs (n, left upper, right upper and beta).
This new adapter then imports the unchanged checker and tests five
additional cases: wrong compact beta, split axis 2, Boolean split axis,
missing split child, and a duplicate JSON key through the original parser.
All 21 ordered control labels must be present. A corruption accepted by
the checker aborts the job.

The original worker writes `FRESH_GAPFREE_RESULT.json`. The adapter writes
a distinct `LINUX_GAPFREE_RESULT.json` only after the arithmetic, original
controls, extra controls and post-run source checks complete. The new
packet binds the original result hash, all five source hashes, manifest,
adapter source, exact domain, census, both rays and ordered controls. The
parent requires this exact packet as the actual final stdout line.

## Guard and evidence

The actual command is ordinary unoptimized Python with `-B -S`, executing
the copied adapter with `--_worker`. It runs only in `trusted_native` mode.
The required Linux capability is the reviewed single-process seccomp
protocol, with 64 MiB supervisor plus 448 MiB worker hard address-space
caps. It denies child process creation and execution. The total hard CPU
budget is 7,200 seconds: 30 supervisor and 7,170 worker seconds. The outer
wall deadline is 7,260 seconds. An unavailable guard, timeout, incomplete
run or failure is `PARTIAL_NOT_ACCEPTED`; there is no discovery fallback.

The selected checker and independent worker contain no inherited 480- or
360-second internal timer, memory guard, subprocess or thread launcher.
They are preserved byte-for-byte; this new outer Linux guard supplies the
execution limits. Its successful establishment is checked independently
of mathematical output.

Acceptance requires exact integer return code zero (Boolean false is
rejected), the same adapter and supervisor source hashes, the actual
guard's bound script identity and resource contract, empty stderr, and
actual stdout/stderr hashes matching the supervisor's captured hashes.
Logs must be the bounded ordinary files in this attempt's execution
directory. Complete sealed source inventory, fresh result files and the
60/1,994/1,027 structural census are checked again after execution.

`FollowOutput` relays new worker lines and a heartbeat every 20 seconds.
The native supervisor additionally records its durable progress and
resource observations. Live evidence backups run every 60 seconds by
default; they are copies of an in-progress attempt, not checkpoints for
acceptance. On completion or a handled error the session state is written
and an evidence ZIP plus SHA-256 sidecar is created. No portable search
checkpoint or partial leaf resume is available for this finite replay.

## Colab interface and limitations

```python
from be_replay.n5_gapfree import run_colab
result = run_colab(durable_root=DURABLE)
```

The optional defaults are `work_root='/content/berry-esseen-runs'`,
`backup_interval=60`, `wall_seconds=7260`, and `cpu_seconds=7200`.
The returned object contains `status`, `bundle` and `work`. Source files
are already vendored, so the job does not require an archive download.
The caller chooses a writable durable location; authentication and Drive
mounting remain notebook concerns. A writable work and bundle location is
required to preserve evidence.

Only an actually observed complete native run can set
`native_arithmetic_accepted=True`, with state
`FRESH_LINUX_POSITIVE_CLOSED_N5_GAPFREE_RECTANGLE_ACCEPTED`.
`full_n5_verified` and `all_index_conclusion_verified` remain false in all
cases. Lightweight local tests exercise source preparation, dispatch with
mocked arithmetic, malformed-input controls, guard/capture negatives and
the error bundle path. Their fixture PASS results are not certificate
acceptance.
