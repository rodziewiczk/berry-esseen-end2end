# Bounded inventory of the seven selected n25 forests

Date: 23 October 2026. This is a source and JSON inventory, with no mathematical
module imported, no leaf evaluated and no replay performed.

The historical claim that the n25 finite union is complete **does exist**. The
supplied final-union record refers to seven completed historical forests, but
this bounded inspection did not locate those seven payloads. A recorded hash or
a historical final-union PASS is insufficient to reconstruct the missing bytes.
This finding does not establish that every possible alternative proof route is
unavailable.

## Historical claim and exact source identity

The principal record inspected is the member
`cutoff25_20261013/root/global25_final_v2/GLOBAL_C25_COMPLETE_JOINED_V1.json`
in `cutoff25_20261013.zip`:

- Member size: 7,781,950 bytes.
- Member SHA-256: `abae7a25b9b82d8b0dd0fc691d33944038d2ffc6707c6f387561f8f17437563d`.
- Status: `PASS_EXACT_GLOBAL_C25_CLOSED_UNION_UNDER_RETAINED_FRAMEWORK_V1`.
- Conclusion: `C25 < CE`, for the unrestricted attained positive closed witness
  under the stated retained framework.
- `new_native_calls = 0` and `new_resource_acquisitions = 0`.
- Its execution description expressly retains component native arithmetic and
  acquisitions rather than rerunning them.
- Its predecessor is the global auxiliary bound `C24 < CE + 1/80`;
  `sharp24_required = false`.

The adjacent unchanged `compose.py` reads the selected lower-region results,
upper/middle union, auxiliary24 and the final B5 union. It checks their source
identities and finite interfaces. It does not manufacture the component forest
bytes from the `source_sha256` map. Its `check.py` separately describes its own
scope checks as source-only, with no new native arithmetic or acquisitions.

The archive pin recorded by the selected downloader is:

| Archive | Bytes | SHA-256 |
| --- | ---: | --- |
| `cutoff25_20261011.zip` | 514,958,998 | `17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb` |
| `cutoff25_20261013.zip` | 529,557,492 | `a97f3e6e50e428df0893304bcd2f746851c9fccef2079b1ec66be9ab909d7f2c` |

These are the existing whole-archive provenance pins; this inspection read the
local ZIP directories and selected members and did not independently rehash both
large archives. The final-union member hash above was computed directly from its
actual ZIP member bytes during this inspection. The public source assets are
available under the [cutoff20 source release](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff20-sources-2026-10-17)
and [cutoff25 base-source release](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff25-base-sources-2026-10-22).

## Seven historical references

All paths in this table are relative to `cutoff25_20261011/new_root/`. The hashes
are the historical expectations in the actual final-union record, not hashes of
recovered or freshly accepted forests.

| Target | Historical forest path | Expected SHA-256 |
| --- | --- | --- |
| B4 q0 | `global_alpha_stoploss2_b4_p29_q0_v12/COUNT29_FOREST.json` | `29dce0656d1c81757d8ff1155f58d22b7c9f69a1e9a142682ebb819547644db5` |
| B4 q1 | `global_alpha_stoploss2_b4_p29_q1_v12/COUNT29_FOREST.json` | `db5b19c66bf9e2a3734cfc36a68306eb85b82f6795b41e96e98e9835c0fa924b` |
| B4 q2 | `global_alpha_stoploss2_b4_p29_q2_v12/COUNT29_FOREST.json` | `84bbf64689cced81b24a76128509d9f1fc7867404a777c6178524d1af712ba7d` |
| B4 q3 | `global_alpha_stoploss2_b4_p29_q3_v12/COUNT29_FOREST.json` | `addc7eeef85f126a65053dc53beb72240c45a260ae9cecff2dac371b6f420a2f` |
| B3 p33 | `global_alpha_stoploss2_b3_p33_v12/COUNT33_FOREST.json` | `6b97b42d8527f1941faebf870898a415af9ff1a3e0bf14611561bf508dfb2222` |
| Original B3 p31 V14 | `global_local_contact_b3_p31_v14/COUNT31_FOREST.json` | `4516ff02d27743b9c0b5fcf60903c44c85c07ce35696f2fbf9bee66d86dabae4` |
| Original B3 p32 V14 | `global_local_contact_b3_p32_v14/COUNT32_FOREST.json` | `5322e6c0d72f871017d4dcee5507a65fd47b3e2a032e8c65b84395364dc15aaf` |

The four B4 source capsules and B3 p33 source capsule are present in the
11 October archive, including their frozen designs. None contains its named
complete forest or accepted receipt. B3 p33 contains
`PREFIX2_CHECKPOINT_001.json` (2,567,382 bytes). That checkpoint is not the named
complete forest.

The original selected `global_local_contact_b3_p31_v14` and
`global_local_contact_b3_p32_v14` directories were absent from both principal
archives. The new Colab p31/p32 epochs are explicit conditional replacements;
their names, design hashes and native status identities do not claim recovery of
these historical V14 sources or forests.

## What the published hints actually contain

The inspected [search-hints asset](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/download/count-search-hints-2026-10-22/untrusted_count_search_hints_2026-10-22.zip)
is 161,372 bytes, with published SHA-256
`9e9e45befa5590d2166f4aa5c55edd6d2595b1eb6c4ac6adcd1fd24855aead2a`.
Its `RELEASE_NOTES.md` explicitly says these are partial, untrusted hints and not
the seven missing historical completed forests.

Reading each actual checkpoint JSON gives the following structural census.
Every checkpoint has 26 ordered roots and `arithmetic_accepted = false`.
The counts below are saved node kinds, not independently checked leaf results.

| Hint | Saved leaf nodes | Saved split nodes | Pending nodes |
| --- | ---: | ---: | ---: |
| `b4-q0` | 508 | 500 | 18 |
| `b4-q1` | 295 | 298 | 29 |
| `b4-q2` | 482 | 473 | 17 |
| `b4-q3` | 233 | 235 | 28 |
| `b3-p33` | 1,329 | 1,328 | 25 |
| `b3-p31-v14-new` | 43 | 33 | 16 |
| `b3-p32-v14-new` | 38 | 22 | 10 |

Thus none is even structurally a completed search checkpoint. Native acceptance
must reconstruct the full closed cover, recalculate every leaf and complete the
24 original corruption controls. The published p31/p32 hints also predate the
clean repository's portable V14 epoch; their design identities must not silently
be treated as matching that later epoch.

## Bounded alternatives examined

The following checks were performed without invoking an arithmetic evaluator:

1. ZIP directory inspection of `cutoff25_20261011.zip`,
   `cutoff25_20261013.zip`, `cutoff25_rethink_20261015.zip` and
   `cutoff25_continue_20261015.zip` for the exact selected historical capsule
   names, their forest/acceptance files and the original B3 V14 names. No complete
   matching target payload was located in those four archives.
2. Inspection of the final n25 union and its unchanged composer, including the
   seven historical forest references above. This is the known claimed complete
   n25 route; it still references these component forests rather than supplying a
   distinct complete replacement for them.
3. Inspection of the original B3 p31/p32 V12 alternatives. B3 p31 V12 contains
   `A0_SPLIT_CHECKPOINT_001.json` through `A0_SPLIT_CHECKPOINT_005.json`, but no
   complete named forest; B3 p32 V12 contains the frozen source design, but no
   complete named forest. These V12 alternatives are not the selected historical
   V14 identities.
4. A bounded filesystem-name search through the old workspace's `research`,
   `output`, `publication` and `tmp` trees. It located the source capsules and
   partial search evidence, but no complete forest under the seven target names.
   The earlier `CUTOFF20_ALL_ARCHIVE_AVAILABILITY.json` independently records the
   same expected historical forest paths as `NOT_LOCATED`; that report is
   corroborating inventory, not fresh arithmetic evidence.

Nearby complete forests do exist, including B4 p32/p33 and B3 p29 q2/q3. Their
branch or probability domains differ. Their presence cannot discharge B3 p33 or
B4 p29 q0–q3 merely because the file number or algorithm name resembles the
missing target. No full same-contract, same-domain alternative was identified by
this bounded inspection. Other sources or a separately proved alternative cover
could change that conclusion and require their own explicit acquisition and
composition audit.

The inspected old handoff already describes the seven selected missing forests
and distinguishes the five original V12 designs from two newly constructed V14
epochs. The historical claim and the missing-data finding therefore coexist;
neither should be erased in reporting the current proof status.

## Effect on current Colab work

This inventory does not require stopping or restarting notebooks 01–07 or 09/10.
Those computations remain useful conditional evidence for the selected fresh
route. Completing the current count searches and running the unchanged full
acceptors is a concrete way to replace the unavailable payloads, while preserving
the explicit distinction between recovered historical bytes and new conditional
p31/p32 epochs. Fresh auxiliary24 acquisition and the same-witness analytic and
semantic joins remain separate obligations. No n25 or all-index conclusion is
promoted by this inventory.
