# Read-only validation of completed n25 count evidence

`be_replay/n25_count_evidence.py` adds a new evidence verifier around the
unchanged count driver. It does not modify `count_task.py`, any frozen
source, a currently running notebook, or a recorded receipt. It imports
no mathematical capsule and reruns no count leaf or discovery search.
Local tests use synthetic sources containing executable traps; those
sources must only be parsed and hashed, never imported.

## Public interface

```python
from be_replay.n25_count_evidence import validate_completed
report = validate_completed(EXTRACTED_TASK, expected_target='b3-p33')
```

The accepted target strings are the unchanged seven targets in
`count_task.TARGETS`: b4-q0, b4-q1, b4-q2, b4-q3, b3-p33,
b3-p31-v14-new and b3-p32-v14-new. Optional
`original_task_root=` asserts the recorded originating task context.

The verifier scans `accept-*/NATIVE_ACCEPTED.json` in newest-file order
and selects the first fully revalidated complete acceptance. A newer
partial, invalid or unsupported attempt cannot hide an older valid
acceptance. If no complete valid acceptance exists, it raises a bounded
diagnostic `ValueError`. An untrusted search checkpoint or candidate,
an isolated accepted receipt, or `NATIVE_OBSERVED.json` alone cannot
establish completion.

## Relocation and original context

The original absolute task root is derived from the preserved accepted
report's `epoch` and its exact `accept-ID` directory name. Every captured
path must belong to that one original task. Original native argv,
working/output directories, receipt path and log paths are compared to
the expected contained relative artifact locations under the restored
task. Receipt bytes and their recorded original interpreter context are
never rewritten. Traversal and paths outside the originating task are
rejected.

The outer controller's original supervisor script may be outside the
task, as in the original Colab checkout. Its exact role, argument shape,
reviewed supervisor source identity and bound native configuration are
verified. The original Python executable/version remain execution
context: an archived `implementation['python']` is deliberately not
compared with the verifier's current `sys.version` after restoration.
The source driver, supervisor and frozen vendor identities must match
the current unchanged reviewed implementation.

## Required evidence chain

The verifier checks the original source-task schema, literal target,
source commit, externally pinned design, complete source-file census,
archive identities and implementation pins. It reuses unchanged
`count_task.verify_capsule` for both the source capsule and the native
acceptance clone. Both must contain precisely the same sealed source
design. Unknown files or historical native outputs are rejected.

The portable V14 source capsule additionally retains its original
`SOURCE_PREPARATION_REPORT.json`, equal to the source task's recorded
preparation result. Its producer's current bytes must match the reviewed
portable producer pin. No filename alias or source migration is made.
The native clone contains only the sealed sources, frozen design, exact
native forest and newly produced native accepted receipt.

The original `NATIVE_OBSERVED.json` must have
`arithmetic_accepted=False`. `NATIVE_ACCEPTED.json` must preserve that
entire original observed record, change only the acceptance flag, and
add exactly the original native receipt/hash,24-control count and
explicit conditional premises. Parent-acquisition and all-index flags
remain false throughout. This original transition is verified rather
than reconstructed or relabeled by the new verifier.

The complete guard evidence is required:

- `execution/native-launch.json` binds the original `-B -S` native
  `count_protocol.py accept` command, capsule working directory and
  execution output directory. Its resource split is64 MiB controller
  plus448 MiB worker, with at most7,200 total hard CPU seconds and7,260
  wall seconds.
- `execution/launch.json` is the exact controller launch derived from
  that native configuration, using the original supervisor entry point.
- `execution/supervisor-result.json` must exactly equal the actually
  observed final native result, with completed status, exact integer
  return code zero, native mode and established reviewed capability.
- The actual worker/controller guard JSON files must equal the nested
  captured guards. Their seccomp mode, no-new-privileges flag, architecture,
  exact denied syscall/filter specification and hard CPU/address-space
  caps are verified against the reviewed supervisor's policy data.
- The actual controller-result file must bind successful worker
  completion, worker PID and unchanged native script after execution.
- Actual bounded stdout/stderr bytes must match their supervisor hashes
  and original contained paths. Stderr must be empty. The complete stdout
  JSON object must be the actual accepted native receipt.

Policy-data verification never installs a filter, starts a process, or
imports a mathematical evaluator. It is separate from the originally
observed native execution whose artifacts are being checked.

## Whole-forest and native receipt checks

The unchanged `forest_census` checks the literal source/header/contract/
kernel binding and all26 ordered nearest-count roots. Every branch must
be complete: no pending node, missing child or duplicate root is accepted.
The full binary census must agree with the recorded execution census.

The unchanged `validate_native` checks every fresh-leaf count, complete
native census,24 distinct controls and actual forest/contract/checker/
kernel hashes. The new verifier additionally reads the24 ordered control
labels directly from the pinned protocol's literal AST and requires
that exact ordered list. It reconstructs the stored leaf-decision
histogram, maximum depth and stored maximum score to compare the entire
native statistics object. These operations inspect candidate metadata;
the original guarded checker supplied the fresh mathematical evaluation.

The native accepted receipt's actual SHA-256 must equal the original
accepted report's hash. The complete preserved source/launch/guard/log
chain is required even if a receipt has an otherwise plausible PASS
status, count census and input hash map.

## Stable report

The return schema is `REVALIDATED_N25_COUNT_V1`. It includes target,
branch (`b3` or `b4`), n25, index, design/source-manifest/contract/forest/
receipt hashes, census, full statistics, driver/supervisor/verifier
identities, recorded implementation/premises and evidence-file hashes.
The following paths are relative to the supplied restored task:

```text
accepted_capsule_relative = accept-ID/capsule
accepted_report_relative = accept-ID/NATIVE_ACCEPTED.json
native_receipt_relative = accept-ID/capsule/COUNTINDEX_ACCEPTED.json
execution_relative = accept-ID/execution
```

`accepted_report_sha256` binds the actual original accepted execution
record; `receipt_sha256` binds the actual native accepted receipt.
`original_task_root` identifies the preserved original context.
`source_manifest_sha256` is the actual `KERNEL_COPY_MANIFEST.json` hash;
`contract_sha256` is the accepted capsule's actual `contract.json` hash.
A later resource-interface collector can read that precise contract and,
for the two new V14 tasks, its sealed `ORIGINAL_V12_CONTRACT.json`.

Only successful revalidation returns `native_arithmetic_accepted=True`.
`parent_acquisitions_verified` and `all_index_conclusion_verified` remain
false. This verifier supplies portable access to completed01--07
evidence; it does not establish the n25 parent or final all-law joins.
