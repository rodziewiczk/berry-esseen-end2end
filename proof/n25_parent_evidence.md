# Restored n25 parent-evidence validation

`be_replay.n25_parent_evidence.validate_completed(task,
original_task_root=None, expected_branch=None)` checks the actual four-stage
09/10 parent evidence after a result bundle is restored to another directory.
It does not import frozen mathematical modules, launch any numerical action or
rewrite any receipt, capture, command or source file.

The function reuses the unchanged `n25_parents._task`, `verify_sources` and
`validate_native` source/object checks. It requires the original driver identity,
the complete pinned initial/resource source manifests, the exact task schema and
the original explicit conditional premises. The imported stronger24 receipt
remains a premise; a source hash does not acquire its auxiliary theorem.

The four completed ledgers must exist in order, with exact preceding-ledger
hashes and matching original attempt-result bytes. Every action has a distinct
sealed source capsule. The validator checks the exact generated/input artifact
inventory and preserves the important cross-capsule edges:

- all four actions use the exact INITIAL proof produced by the fresh
  `initial-construct` action;
- both resource actions consume the exact receipt produced by the fresh
  `initial-accept` action;
- `resource-accept` consumes the exact complete proof produced by
  `resource-construct`.

The final resource-accept capsule contains both the INITIAL and resource
directories, so a later interface checker can inspect the actual accepted
proof pair without copying a historical source-era acceptance.

Absolute paths remain in their original recorded form. The validator infers one
original task prefix from the first capture path, or checks the explicitly
supplied prefix. Only contained paths with the exact original stage suffixes
map to the restored task. Traversal, symlinks/junctions, missing artifacts,
changed source or captured bytes and incompatible contexts fail validation.

For every stage the validator also checks:

- the original `-B -S` command/action and `new_root` working directory;
- the actual `native-launch.json`, outer `launch.json` and
  `supervisor-result.json`, including CPU/wall/memory and capture bindings;
- both actual kernel guard sidecars, their unchanged filter description and
  their exact copies embedded in the supervisor observation, plus the native
  controller completion/script identity;
- integer return code zero, successful bounded native status, stable stdout and
  stderr hashes, empty stderr and exactly one original completion marker;
- the unchanged native proof/receipt checks: all 239,616 INITIAL signed
  rectangles, the complete ordered 100-panel export, all 100 terminal resource
  rows and all 12 original controls in each acceptance action.

These checks validate preserved evidence of the separately documented Linux
single-process execution contract. They do not claim an aggregate cgroup
charged-memory guarantee, remote attestation, or independent mathematical
verification of the analytic framework.

The returned schema is `REVALIDATED_N25_PARENT_V1`. Its stable interface includes
`branch`, `n=25`, `contact_allowance='5/16'`, `resource_capsule_relative`, the
INITIAL/resource proof and receipt SHA-256 values, source-manifest pins,
stage-ledger/capture bindings, original task prefix and unchanged original
driver hash. `resource_capsule_relative` is relative to the supplied task and
names the final `new_root` containing the two original source directories.

Successful evidence validation sets `native_arithmetic_accepted=True` while
keeping `stronger24_acquisition_verified=False`,
`count_interface_join_verified=False` and
`all_index_conclusion_verified=False`. It neither repeats completed 09/10
arithmetic nor substitutes the global allowance for a count contract's
separately justified effective allowance. The subsequent resource-to-count
interface and fresh auxiliary-premise joins are distinct obligations.

The accompanying tests use synthetic source manifests, proof/receipt objects
and execution sidecars. Their fixture scripts explicitly raise if executed;
the numerical launcher is mocked. Tests cover relocation of both branches,
unchanged artifact bytes, wrong branch/context, task-premise changes, missing
dependencies/artifacts, malformed captures/guards/launches and a consistently
rebound local receipt that is nevertheless not the earlier fresh INITIAL
acceptance. Passing these fixtures is infrastructure validation only.
