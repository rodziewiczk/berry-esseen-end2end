# Selected retained n25 B0–B2 count forests

Date: 23 October 2026. The machine-readable inventory is
[`n25_retained_b012_catalog.json`](n25_retained_b012_catalog.json), SHA-256
`f055b5017d4e1fd14f2b48a6a95fef4a4c61a025dea6174c424cd5968de801f7`.

This is a complete count-job selection catalog for the three supplied historical
lower-rho B0/B1/B2 regional receipts identified in
[`n25_regional_selection.json`](n25_regional_selection.json). It is not a catalog
of their complete INITIAL/resource/local acquisitions, the other n25 regions,
or a fresh n25 theorem. No mathematical source was imported and no leaf was
evaluated. Only source bytes, JSON identities, selectors and saved-tree
censuses were inspected.

## Actual selection and census

| Branch | Closed rho domain | Selected probability panels | Count jobs | Saved leaves |
| --- | --- | --- | ---: | ---: |
| B0 | `[1,11/10]` | 37–53 | 17 | 12,985 |
| B1 | `[11/10,6/5]` | 32–42 | 35 | 47,946 |
| B2 | `[6/5,13/10]` | 28–38 | 23 | 33,357 |
| Total | Three adjacent closed bands | 39 original panels | 75 | 94,288 |

Every selected forest has all 26 ordered count roots, giving 1,950 roots in
total. Direct traversal of the saved JSON trees gives 186,626 nodes, including
92,338 split nodes and 94,288 leaf nodes, with zero pending nodes. Each saved
forest's leaf census agrees with its selected regional outcome, historical
strict receipt and `fresh_leaf_evaluations` field. Every historical receipt has
24 distinct original controls. These are verified metadata identities and
saved-node counts, not independently replayed leaf results.

The remaining 83/89/89 probability panels in B0/B1/B2 are classified by their
regional receipts as global resource exclusions. Their resource arithmetic is
outside this count-only catalog.

## Source and selector identity

All 75 selected count capsules are supplied by `cutoff25_20261011.zip`,
514,958,998 bytes, with archive pin
`17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`.
The [public source release](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff20-sources-2026-10-17)
provides this asset. The later `cutoff25_20261013.zip` supplies the historical
final-union selection context; none of these 75 payloads requires a substitute
from that archive.

The exact selection members, relative to `cutoff25_20261011/`, are:

| Branch | Selection member | SHA-256 |
| --- | --- | --- |
| B0 | `new_low/B0_SELECTED_PATHS_FINAL.json` | `57a3199cfa72839209609315f11d4fb338977d170357e0adcf25421355379e5d` |
| B1 | `new_audit/LOWER_B1_COMPLETE_SELECTION_V1.json` | `5edd835d43a9c7bf54d01142ac4030e2df9bdff0b597704ca306b3c021a04cec` |
| B2 | `new_audit/LOWER_B2_COMPLETE_SELECTION_V2.json` | `036896bcb8bf925168610074271ee11b808e815135e5ced7cbd60ed97a670816` |

The B0 receipt is assembled by `new_audit/compose_low_b0_complete_v3.py`.
B1/B2 use `new_audit/compose_lower25_complete_v1.py` with their distinct literal
selections. The catalog records the actual composer hashes, regional receipt
hashes and each selected outcome/selection pointer. Each candidate forest hash
also matches its reference in the corresponding regional receipt's source map.
The method follows the literal `panels` selections and final `selected_counts`
outcomes; it does not collect every forest mentioned by an inherited source
dependency graph.

## Partition and supersession details

B0 selects one whole-panel forest for every panel 37–53. Its selected paths are
the `new_low/countINDEX_global_conditional_v2` capsules, except panels 38–42 and
44, which select `countINDEX_global_theta_v1`.

B1 selects whole-panel `global_count_b1_pINDEX_v2` capsules for panels 32, 41 and
42. Its other eight selected panels are divided into four closed probability
quarters:

- panel33: `global_theta_b1_p33_q0..q3_v3`;
- panel34: `global_joint_cubic_b1_p34_q0..q3_v3`;
- panel35: `local_theta_b1_p35_q0..q3_v4`, under the separately acquired local
  resource route;
- panels36–39: `global_sos_quartic_b1_pINDEX_q0..q3_v8`;
- panel40: `global_tangent_b1_p40_q0_v1` and `q1_v1`, followed by
  `global_joint_cubic_b1_p40_q2_v3` and `q3_v3`.

B2 selects whole-panel `global_count_b2_p28_v2` and
`global_alpha_stoploss2_b2_pINDEX_v12` for panels 33–38. Its quarter partitions
are:

- panels29,30,32: `global_fixed_peak_b2_pINDEX_q0..q3_v9`;
- panel31: `local_theta_b2_p31_q0..q2_v4`, followed by
  `local_joint_cubic_b2_p31_q3_v5`, under the separately acquired local route.

In particular, the old local-theta B2 p31 q3 v4 capsule is not selected. Neither
are superseded whole-panel or alternative quarter forests that remain in source
graphs. For every selected panel, the catalog checks that its exact closed
quarter endpoints meet, preserve both original outer endpoints and sum to the
regional selected leaf count. The B1 p35 and B2 p31 outcomes each require their
separate 16-cover local acquisition in addition to the global parent; native
count acceptance alone does not acquire those interfaces.

## Inputs for a generic unchanged full acceptor

Each catalog job records its exact archive-relative capsule prefix, forest and
acceptance filenames, protocol/contract/kernel-manifest hashes, complete runtime
source-file rows, closed p/rho domain, forest schema and node/root/leaf census.
`manifest_filename` is `KERNEL_COPY_MANIFEST.json`; the separately recorded
`FROZEN_DESIGN.json` identifies the historical source epoch and has no mismatch
with the runtime inputs shared between them.

All selected forest, receipt, protocol, contract and manifest bytes were hashed
directly. All 3,826 runtime-source rows were independently checked against their
declared hashes and were present. Static parsing found no unresolved local
import, Windows-only import, subprocess/thread launcher, `ctypes` or `resource`
import in these selected runtime source closures. This is source compatibility
evidence; actual Linux capability, resource consumption and successful replay
still require execution in the intended environment.

The common original invocation is:

```text
python -B -S count_protocol.py accept
```

Run it in a fresh copy of the individual flat capsule. Its complete candidate is
`COUNTINDEX_FOREST.json`; the fresh output must be
`COUNTINDEX_ACCEPTED.json`, with status
`PASS_FRESH_CONDITIONAL_EXACT_COUNTINDEX`. The original acceptor prints its full
JSON receipt and must recompute all closed roots/leaves and all 24 controls.
Copy the immutable runtime inputs and forest candidate, and exclude the
historical accepted receipt from the fresh destination. The catalog's historical
receipt is selection/schema evidence, not an accepted input for a new run.

Kernel manifests include fixed implementation proof/review and checked JSON
inputs. Their supplied hashes establish source identity; they do not reclassify
those historical implementation reviews as newly executed mathematical checks.
The conditional kernel algebra, actual parent/local acquisition and
resource-to-count interfaces remain explicit review/composition obligations.

No selected payload or source was missing and no source/metadata issue was found
within this B0–B2 count catalog. This availability finding does not close B0–B2
parent/resource obligations, other n25 regions, stronger24 acquisition, the full
n25 theorem or the all-index proof. All corresponding fresh-proof flags remain
false in the JSON.
