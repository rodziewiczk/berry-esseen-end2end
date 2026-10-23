# Historical resource acceptance timings for notebooks36--39

These numbers were read from the actual archived acceptance JSON bytes on
23 October2026. No mathematical code was imported or run. The selected member
identities are pinned in [the B012 catalog](n25_b012_parent_sources.json) and
[the B5 catalog](n25_b5_global_sources.json), from `cutoff25_20261011.zip`,
SHA256 `17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`.

| Notebook | Exact historical resource acceptance member | Recorded seconds |
|---|---|---:|
|36|`cutoff25_20261011/new_low/resource25_b0_v1/RESOURCE_B0_GLOBAL_ACCEPTED.json`|407.76591181755066|
|37|`cutoff25_20261011/new_root/resource25_b1_v1/RESOURCE_B1_GLOBAL_ACCEPTED.json`|392.96161103248596|
|38|`cutoff25_20261011/new_root/resource25_b2_v1/RESOURCE_B2_GLOBAL_ACCEPTED.json`|418.276731967926|
|39|`cutoff25_20261011/new_root/resource25_b5_v1/RESOURCE_B5_GLOBAL_ACCEPTED.json`|982.0885858535767|

Each is the native resource acceptor's `seconds` field, not the whole notebook
wall time. None of the four selected INITIAL proof/acceptance objects contains
a timing field; no adjacent capsule stdout/timing logs were present. Notebooks
37/38 additionally construct and accept one local panel. This bounded check
does not establish those local durations, the original machine's speed or a
Colab speed ratio. The full notebook time therefore cannot be inferred by
reporting these component durations as a whole-run estimate. These parent
jobs replay supplied complete candidates; they do not search a count tree.

Historical timing/acceptance records are observations, never fresh proof inputs.
The new jobs require actual fresh arithmetic and validated captures under their
documented execution contracts.
