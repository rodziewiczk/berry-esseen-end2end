# Completed59B/C reader compatibility

On25October2026 the full pure current reader accepted the actual completed
59Bexport`20261024T023936Z-e903a551-results.zip`, SHA256
`b42cb262d1c8289e2fae214626c143e7bc83aee3550d71263e33991ac6173bb1`.
No original numerical programs were executed. All source/capture/result bytes
were unchanged before and after readback.

The original implementation source is available at commit
`ffa28f377f9745bea1fde57c5632f3f408af270b`; its source-adapter hash is
`0a03ca05ae2788118ea7c7c55e16d6b37443a222c0e21b9ee14f30fd267d167a`.
Commit`99d4a016bbfe7399639b49cf131ccbae2f103f0f` changed only the AST formatting
comparison to preserve full Python3.12 fields on Python3.13; adapter hash
`35213d6c838122bdd3df92b9f89c9097ef4c2d4f2f4eb8ef4211372c0b3f380b`.
The whole module/capture/evidence/source-plan maps for those two published
epochs are explicitly enumerated in`finite2630_covers_evidence.py`.

The reader permits either exact historical map, not an arbitrary adapter
hash. The observed and completed maps must agree. All current-source graph,
raw provenance, byte-inverse receipt literal ports, complete two-pass native
outputs, stopped checkpoints/streams, guards, exact mathematical projections,
115/215-row covers and mutation controls remain required. A completed ledger
alone is insufficient. New preparation and execution use the current source
hash; historical source admission is an explicit completed-readback path.

Tests cover unknown helper/other-file hashes, extra implementation entries,
mixed observed/completed epochs and rejection of old source hashes in new
execution. Existing full two-lane stopped/cache/relocation fixtures also pass.

For the real59Bexport the full reader verified two complete115-row passes,
14native actions,93controls per pass and all closed seams. This closes its
reader compatibility issue. Full support, resource-to-COUNT interfaces,
finite26–30 acquisition and the global theorem remain separate obligations.
