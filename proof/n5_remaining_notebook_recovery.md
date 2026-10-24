# Notebook35: preserve completed work after notebook-parent bytecode failure

The actual wrapper-failed run20261023T194522Z-6560588f completed support, both
HIGH protocols and the long owncaps stage, then completed INITIAL.B0 at
00:46:09UTC on24October. The subsequent repeated source-inventory check failed
with `No unbound supervisory import/helper`. Both INITIAL stage ledgers and
all native result/source/capture files were already written in its final ZIP.

The metadata reader imported pinned standard-library-only adapters inside the
notebook parent. That parent normally lacks `-B`; assigning
`sys.dont_write_bytecode=True` inside an imported adapter happens after its
loader can create a `.pyc`. The corrected reader sets this flag before import
and restores the prior parent flag/path even on failure. Strict immutable
source inventories are preserved: extra helpers and bytecode are still rejected.
No original numerical program, selected input, source catalog, resource budget,
native control, result assertion or mathematical premise changes.

Only the exact preceding metadata-reader SHA
`c18d64bbd0691d90c7a89e359e659e2cbb6cc8d856149ce038cae37b5cf655b5`
is additionally admitted in old stage implementation maps. Every other
controller/source/snapshot/guard/catalog/resource-policy pin must equal the
current fixed one, and observed/completed implementation maps must agree.
Old artifacts are not rewritten; every full source/capture/native result and
control is revalidated by the current reader. Thus the earlier support/HIGH/
owncaps completed cache remains reusable without repeating its mathematics.

Before the normal326-job runner, the corrected notebook's recovery helper
looks for the actual saved wrapper-failed bundle under the usual Drive root.
The entire ZIP is pinned to5098913bytes and SHA256
`77fdf3b9cc40070ad3350250960e0896efc91df713debda79222e227938f40c4`.
It extracts only the named complete INITIAL.B0 subtree, with bounded ordinary
member/path/link/duplicate checks, then requires full `validate_completed`.
Only after that check does it save a normal complete-stage ZIP in the existing
INITIAL.B0 cache namespace. A valid existing cache skips this recovery. If the
known source bundle is absent, the regular full INITIAL run is still required;
an incomplete stage is never promoted. Native/global flags remain false.

The actual downloaded INITIAL export passed pure full readback: nine complete
2592-cell covers,100panels and27native controls. The complete helper was also
run on those actual saved bytes, then its new cache was restored and fully
revalidated without any mathematical execution. The sanitized
[readback result](n5_remaining_initial_recovery_readback.json) records those
identities and counts. This is source/result/capture validation, not a new
local numerical replay or a full C5 proof.

All36 source/synthetic/notebook fixtures pass from a clean351-public-file
checkout without ignored work; one actual-Linux exec probe is skipped on this
Windows host and remains mandatory in Colab. New regressions cover a parent
with bytecode writing enabled, failed-import restoration, exact old-reader
compatibility, unsafe recovery archives, missing bundles and complete cache
reuse. A local overly long Windows test path was shortened for actual cache
transport validation; deployed Colab paths and numerical code were unchanged.

Open the new pinned notebook35 and use Run all on the same Drive. It should
revalidate/reuse the three existing component caches and the recovered INITIAL,
then continue the remaining selected jobs. Preserve the earlier final ZIP.
