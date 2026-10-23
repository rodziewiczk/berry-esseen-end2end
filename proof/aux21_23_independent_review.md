# Independent source review of the auxiliary21–23 runner

Date: 23 October 2026. Reviewed driver:
[`be_replay/aux21_23.py`](../be_replay/aux21_23.py), SHA-256
`8945bc48e7cbcda958e9ec10679375f24d3007f8513afab4e7fb206785e68bb1`.
The common source preparer at this readback had SHA-256
`746eb0eea0d18297041130b390ecb7e4571e6ae666711076e4d1c706623ff87c`.

No runnable schema, source-closure or output-name blocker was found in this
scoped review. This is a static source and JSON comparison against the real
selected archive, not a fresh execution result. No mathematical module was
imported, no mathematical producer or acceptor was invoked, and no inequality
was independently recalculated.

## Source binding

The source is `cutoff25_20261011.zip`, 514,958,998 bytes, with the existing
archive pin
`17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`,
published in the [cutoff20 source release](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff20-sources-2026-10-17).
This review read the local ZIP directory and selected member bytes; it did not
rehash the entire large archive.

Every selected file in the three prepared inventories was compared both with
its manifest digest and with its actual ZIP member. All matched. The resulting
manifest identities agree with the runner's literal epoch pins:

| Job | Selected files | `SOURCES.json` SHA-256 |
| --- | ---: | --- |
| auxiliary21 | 8 | `ae5f29977948bbfb1e439fdf58f38fee449b7d7bb636d51aad4afa065f00491c` |
| auxiliary22 | 55 | `d0a35f509e75282a4887c6e1048a0852496873318c5f50498798ee47edec37d9` |
| auxiliary23 | 103 | `69fc6eed8940a7b5f4b447ad79c375d16a5b27c40ee9baeaddd817030ddef7a8` |

Static import inspection found the required local Python modules in their flat
capsules. The count capsules include their local `profile.py`; the fresh native
worker places the script's directory first on the import path. Remaining
imports are from the Python standard library. Literal dynamic imports found in
the selected arithmetic sources load `math`. No Windows-only import or hidden
process launcher was identified in the selected native entry closures.

The one process launcher is the explicitly selected auxiliary23
`count23/optimized_v1/check_optimization.py`. Its unchanged slow comparison runs
in the sibling `count23` directory. That original slow closure and its five
candidate inputs are included. The runner assigns this action BASIC supervision
and does not claim whole-job native acceptance for auxiliary23. This is a
separate execution contract, not a reason to discard the mathematical comparison.

## Original outputs and stdout contracts

The following expectations were checked against the unchanged statements that
produce the files and print the terminal output, as well as the real archived
receipt schemas. Archived receipts were inspected for compatibility only; they
are excluded from the new selected runtime input inventories.

| Action | Original output | Actual original completion form |
| --- | --- | --- |
| auxiliary21 INITIAL | `EXACT21_CHECKED.json` | Exactly one `EXACT21_PASS` line after five stage reports |
| auxiliary22 INITIAL accept | `POSITIVE22_INITIAL_ACCEPTED.json` | Complete indented JSON terminal object after stage/export messages |
| auxiliary23 INITIAL accept | `POSITIVE23_INITIAL_ACCEPTED.json` | Complete compact JSON object on the last line |
| resource22/23 accept | `RESOURCES22_ACCEPTED.json` / `RESOURCES23_ACCEPTED.json` | 100 panel reports followed by a compact JSON object |
| each strict count | `accepted_strict_INDEX.json` | The exact branch-specific count marker, index, passed/empty/total counts and control count |
| count22 join | `COUNT22_CONDITIONAL_JOINED.json` | JSON containing the seven selected aggregate summary fields |
| optimized count23 join | `COUNT23_OPTIMIZED_CONDITIONAL_JOINED.json` | The corresponding seven-field aggregate JSON |
| auxiliary23 optimization comparison | `OPTIMIZATION_EQUIVALENCE.json` | Complete indented JSON output with 70 complete-cell comparisons and 1,000 quartics |

The original statuses and original control labels match the runner's expected
forms: auxiliary22 INITIAL has 18 fixed-object/parser controls, auxiliary23
INITIAL has eight fixed-object controls, each resource acceptor has 20 controls,
and every selected strict count receipt has 24 controls. Auxiliary21 has no
additional corruption-control stage in its original checker; this review does
not invent one.

The native source-binding inventories also match the actual originals: seven
entries for auxiliary21 INITIAL, three for auxiliary22 INITIAL, nine for
auxiliary23 INITIAL, 16/18 for resource22/23, and 17/22 for count22/optimized
count23. The outer source manifest additionally binds the other selected source
and review files even when an original receipt has a narrower source map.

The declared generated files cover the paths used by these invocations. In
particular, auxiliary21 writes `EXACT21_PROGRESS.json` and auxiliary23 INITIAL
writes `PROGRESS.json`. Auxiliary22 writes `CONSTRUCTION_PROGRESS.json` only in
its unselected construction action; the chosen `accept` action calls
`calculate(progress=False)`. The commands use `-B -S`; the optimization child
also uses `-B`. Thus the selected calls do not require allowing generated
`__pycache__` files. No additional selected acceptor output was identified.

## Complete candidate and resource-to-count edges

For auxiliary22 and auxiliary23, the INITIAL proof candidate and the resource
capsule's `initialN_proof.json` are byte-identical. The original INITIAL acceptor
recalculates the complete object and checks that candidate, rather than trusting
its historical origin. The new semantic edge then binds the resource input hash
to this freshly replayed INITIAL proof hash.

The selected INITIAL objects have six/eight guarded feedback stages and their
complete final 100-panel export. Including the export, the original arithmetic
censuses are seven covers / 129,024 rectangles for auxiliary22 and nine covers /
165,888 rectangles for auxiliary23. Auxiliary21 separately runs five complete
covers / 92,160 rectangles.

Both resource candidates have exactly 100 ordered rows. Their complete 16/18
input bindings match the actual selected sources and candidate bytes. The
resource contract and the count capsule's `contract.json` are byte-identical.
The unchanged resource protocol fully recalculates all 100 rows, consumes each
entire declared refinement plan and checks the exact signed count interfaces
for every survivor. The protocol also explicitly reconciles the INITIAL
global-predecessor support schema with the resource same-law support schema by
comparing all numerical fields while permitting only the named scope/schema
labels to differ.

The saved candidate classifications are:

- auxiliary22: surviving panels 31–39, all covered by its nine selected forests,
  totaling 258 leaves.
- auxiliary23: surviving panels 25–44, all covered by its selected count panels
  24–44, totaling 18,377 leaves. The additional panel24 count is harmless extra
  coverage; no surviving panel is omitted.

The original strict count acceptors recalculate every selected candidate leaf.
Their joins reconstruct coverage and bind each candidate to its actual newly
written strict receipt. The outer runner additionally requires the full ordered
stage ledger, complete stdout/stderr hashes, empty stderr and the selected
execution guard. A false/partial return or malformed terminal object cannot
become a completed stage through the normal driver path. Restored evidence is
validated through contained relative paths while preserving the original
recorded receipt bytes and their execution context.

## Historical data and remaining premises

The driver does not use a pinned historical accepted-receipt hash as proof of a
new execution. Fixed hashes bind source modules, immutable proof candidates and
the simultaneous resource/count contracts. New receipt hashes are computed from
the actual new outputs and threaded through the new stage ledger. Runtime and
timing fields in newly generated receipts are not required to equal historical
timing-dependent hashes. The optimization receipt is newly generated too; its
archived version is not copied as an acquired fact.

The separate semantic interface is still conditional on its stated predecessor
and analytic framework. In particular, source matching does not independently
prove attainment/contact/support, the charged INITIAL implications or optimized
interval-arithmetic algebra. The 70-cell/1,000-quartic comparison is useful fresh
corroboration of the selected implementation, not a substitute for the retained
algebraic argument.

No Colab resource use, elapsed time, successful arithmetic replay, native
capability or theorem acceptance was established by this review. The driver
keeps predecessor acquisition, full auxiliary bounds, stronger24 acquisition
and the all-index conclusion false. A successful future run must retain these
boundaries until the corresponding independent premises and final joins are
actually discharged.
