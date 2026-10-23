# Portable V14 source preparation

The first Colab runs of notebooks 06 and 07 stopped during source preparation. Their saved child stderr identifies a missing `ORIGINAL_V12_CONTRACT.json`. The frozen preparer had emitted `ORIGINAL_V12_contract.json`; its native loader used the uppercase name. Case-insensitive Windows filesystems concealed this mismatch. Neither failed preparation reached count-forest evaluation.

`be_replay/prepare_v14_portable.py` verifies the original producer's SHA-256 and changes exactly one checked output-destination expression before executing it. The native protocol, contract, mathematical modules, proof text, limits, geometry checks and 24 native corruption controls retain their bytes. The correctly named contract is included in the producer's provenance, kernel manifest and frozen design. There is no filesystem alias or input outside that closure. The epoch's preparer hash binds the complete adapter.

| Input | SHA-256 |
|---|---|
| Frozen producer | `4116a054c2f725794d82cc4bd7b954023c9b8525d8f943c6cea2a8096aceb647` |
| Portable adapter | `b4896cae54058bb63f3c68a295131a83ceace34e71d180c0b228bd4a28ce44f6` |
| Portable p31 design | `bc699a2d539b4aafc193049c8074b02e0b77a38fb01b594c1ba3e2fde6b7b3ff` |
| Portable p32 design | `cfe934b1385f9a26f36b6bf94cda9e5caeb6593700a54eeac7e7b1638df61627` |

The two corrected epochs have new source designs and native kernel bindings. Historical V14 checkpoints are not silently rebound: these tasks start with all 26 original roots. Matching checkpoints produced by the corrected epochs can be resumed. The old published hint manifest retains its independent seven historical design pins, so the five unchanged V12 tasks can still use their own hints.

Validation on 23 October 2026 executed both complete source preparers against the original archives. Both produced the externally pinned 178-file designs, loaded the corrected contract and checked all 26 root geometries and premise rejection fixtures. Their mathematical evaluator tripwires remained in place; no leaf evaluation, count acceptance or parent acquisition was performed by these preparation checks. Linux execution and mathematical acceptance remain separate Colab obligations.

Infrastructure fixtures also compare the complete transformed producer AST, reject modified frozen code, and verify that failure messages retain the actual child exit reason and a bounded stderr tail. Notebook bootstrapping discards cached execution modules from an older code pin before importing the corrected checkout.
