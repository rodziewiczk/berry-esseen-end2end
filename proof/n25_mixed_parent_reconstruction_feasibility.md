# Mixed n25 B5 p24/p25 parent reconstruction feasibility

This is a bounded source-availability and interface-construction finding, not numerical acceptance or an independently verified proof. The inspection read archived bytes, JSON, and Python ASTs only. It did not import an original module, execute a mathematical producer/checker, run a corruption control, or acquire a theorem registry. The accompanying [machine-readable records](n25_mixed_parent_reconstruction_feasibility.json) have SHA-256 `47714ca3d22ede7463d632bdceeefed6d62205b876b453d7383c0c455ed1ef8b`.

The concrete finding is stronger than "the parent sources are missing": **all 93 expected native kernel files are supplied, both exact historical native checker bytes are reconstructible, and the exact historical kernel manifest is reconstructible.** The two physical resource rows are also supplied. The complete historical contract provenance bytes have not been recovered. An honest new source/contract epoch can therefore be constructed without inventing a numerical kernel, subject to explicit mixed-header and theorem-registry interface work and full fresh Colab replay.

## Supplied inputs and exact native identities

Only these two pinned source assets were used for the conclusions below:

| Asset key | Asset | Bytes | SHA-256 |
|---|---|---:|---|
| `old` | `cutoff25_20261011.zip` | 514958998 | `17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb` |
| `base13` | `cutoff25_20261013.zip` | 529557492 | `a97f3e6e50e428df0893304bcd2f746851c9fccef2079b1ec66be9ab909d7f2c` |

The supplied physical bases are:

- p24: `old:cutoff25_20261011/new_root/global_stoploss2_b5_p24_v11/contract.json`, SHA `4450c53323f528dff49cea469de0ca2ba6913cf94c519273f57a321594f61a07`.
- p25: `old:cutoff25_20261011/new_root/global_alpha_stoploss2_b5_p25_v12/contract.json`, SHA `055a5d07e72c14c264251d78aa24e6239f9fc4efd9da9a10153d345ad4eb6289`.

The supplied p24 V11 contract has exactly the contract SHA recorded for the later p24 V12 source in `base13:b5/local_contact_v14_producer_prefix_review_v1/NATIVE_PREFLIGHT.json`. This does **not** identify its V11 numerical kernel with V12. The correct common numerical donor for both reconstructed V14 parents is the supplied **p25 V12** capsule. Its `exact35_core.py` SHA is `a618867ae34841b2e3e1745e35142694142e08ca2d790b762870f50651e16d71`; the p24 V11 core has a different SHA and must not be substituted.

For each panel, the complete saved mixed receipt's `original_cfg` equals the complete supplied physical row after adding exactly:

```json
{
  "local_contact_allowance": "5/16",
  "local_contact_premise": {
    "schema": "ATTAINED_POSITIVE_CLOSED_CONTACT_V1",
    "sample_size": 25,
    "same_unrestricted_attained_witness": true,
    "positive_closed_threshold": true,
    "score_at_least_CE": true
  }
}
```

Every original guard, support endpoint, rounding value, quadratic budget, sign premise and acquired-moment field is retained in the machine-readable full rows. This is a whole-row identity finding, not a comparison of only p/rho endpoints.

| Panel | Expected historical V14 contract SHA, still unrecovered | Exact recovered checker SHA |
|---|---|---|
| p24 | `3214522020e35bdcf825ac1e6be12db5e8199e98df79c90bf55a199cef754323` | `daf6cd8b2a981faa925e8c07d18d8a42d2c504c8a8d5d13ea76af42e4a58c12a` |
| p25 | `07596e69651349238c487f39a2d86468b6e6b3fda2e5eabdd7ee83850c82f2f7` | `2b2d274490d9364516ec66f4de484821c89f4889123d09bbdf951ad7533da583` |

Both expect kernel manifest SHA `f73f0c6eed5a3ef0b74eb5242b30336ead091b0f7d3783de120c3ec56a32dac0` and the same 93-name `kernel_sha256` dictionary. Their full expected native headers are preserved in the JSON.

## Exact source reconstruction recipes

All 93 actual archive members were reread and checked against their expected SHA and byte length. There are 71 unchanged p25 V12 kernel/proof records and 22 combined-V14 records, including the additions manifest. The JSON gives an archive-relative alias for every file; there are no missing expected file bytes. Fifty files are Python sources. The static nonstdlib import names resolved to sealed sibling files. This is not an assertion that every dynamically enabled execution path or analytic inequality has been independently proved.

The combined helper prefix is `base13:cutoff25_20261013/b5/local_contact_v14_combined/`. Its `LOCAL_CONTACT_V14_ADDITIONS.json` SHA is `ba80569735e7042a588eba6c8219fbd68c4deae354c3983ea518dbbb2d9a8336`. It contains the exact 21 additions; the manifest itself is the 22nd copied file.

The exact p25 historical checker follows from the supplied source-only fixture `base13:cutoff25_20261013/b5/local_contact_regional_review_v1/private_source_fixture/count_protocol.py`, SHA `8d77de0e5e2d0bf17f1e1fb3fb5b1a4fd795d8c0f54713b437a1c3c5afba4544`, by the two literal substitutions recorded in the JSON: the V13 import becomes V14 and the V13 header label becomes V14. Fixed p24 index/p-domain/file/status substitutions then give the exact expected p24 checker SHA. These byte hashes were matched; no derived checker was imported or run.

The exact historical manifest follows by preserving every top-level field and insertion order of the supplied p25 V12 manifest, updating `files` with the ordered 21 additions, and appending the actual additions-manifest SHA. Serialize with `json.dumps(indent=2)` plus LF, without sorting keys. The resulting SHA is exactly `f73f0c6e...` above. A sorted-key serialization is a different identity.

The recovered historical native checkers retain `LIMIT=10000`, depth 128, all 26 closed count roots and all 24 original native corruption controls. This records the original interface; the mixed acceptors have their own additional full-result and structural controls.

## Historical contract provenance remains a separate boundary

The supplied producer source review explicitly models the following construction (`base13:cutoff25_20261013/b5/local_contact_v14_producer_prefix_review_v1/check.py`, lines 73--89): retain the old contract; add the exact two row fields; set status to `EXACT_GLOBAL_GUARDS_AND_LOCAL_CONTACT_RHO_FEEDBACK_CONDITIONAL_UNTIL_V8_COMPOSITION`; update `source_inputs_sha256` with ROOT-relative producer-required source entries and the producer gate.

The real gate commitment is `work/cutoff25_20261011/new_low/local_contact_v14_native_v1/ROOT_REVIEW.json`, SHA `212512410b597252f5f37bd08571ee0f48e4be739a7fe2bedddad1bc45f45470`. Its actual bytes and the original producer `prepare.py` bytes were not located by this inspection. The fixture's `'e'*64` gate is explicitly synthetic and must never be copied into a production parent.

The actual preflight records 104 required inputs per panel and a larger source-admission ancestry. A bounded 104-entry model (26 shared producer/helper entries, 74 panel capsule entries, four old source edges, then the real gate), as well as bounded larger-source-map serialization alternatives, did not recover any of the nine historical B5 p24--32 contract hashes. Those failed model hashes are recorded so they cannot be mistaken for recovered artifacts. No conclusion about global absence of the original bytes is made.

Consequently, the new assembler must issue an explicitly **new** contract/source design, with its own external pin and provenance. It must not label a mathematical-row match as an exact historical contract reconstruction. The old contracts, producer/gate SHA references and saved acceptances remain provenance commitments.

## The two mixed proof systems are not ordinary count jobs

The p24 acceptor is `base13:cutoff25_20261013/low/p24_mixed_acceptance_v1/accept.py`, through its `protocol.py` and `low/p24_static_pointwise_v1/mixed.py`. The p25 acceptor is `low/coupled_chord_acceptance_v1/accept.py`, through `protocol.py`, the coupled-chord candidate/feedback code and the mixed4/mixed3/mixed2/native chain. Exact inspected source SHA records are in the JSON; their presence is not a claim that the entire relocatable mixed execution closure is already implemented.

The original Session checks fixed native contract/checker/header hashes, source freezes and registry bindings. Therefore **the unchanged mixed acceptor does not directly admit a new whole-contract loader or a new native header**. A subsequent explicit adapter must bind the new source epoch, prove full original-row and 93-file identity, and restrict its metadata migration to the enumerated source/header/selection/registry fields. No old contract or gate hash may be impersonated.

The mathematical geometry must remain the same: all 26 roots, every split, closed box and leaf result payload. A migrated candidate is untrusted. Full fresh evaluator results must compare with full typed equality. If a new execution changes a result, the adapter must fail closed or produce a newly labeled candidate through legitimate Colab reconstruction; it cannot relax result equality.

The selected historical counters are metadata only:

| Panel | Nodes | Leaves | Required mixed work represented by the saved receipt |
|---|---:|---:|---|
| p24 | 8846 | 4436 | 4310 ordinary native leaves; 126 E theorem-reference leaves; depth 29 |
| p25 | 2166 | 1096 | 759 ordinary, 112 scalar, 149 derived-native and 76 theorem-reference leaves; depth 26 |

The p24 saved acceptor reports 19 structural controls and one additional genuinely fresh ordinary full-result corruption evaluation. The p25 saved acceptor reports 41 structural controls and one additional genuinely fresh original full-result corruption evaluation. The positive p25 replay reports 908 native calls, 637 scalar calls and 6700 finite contact attempts. These values are neither a fresh result nor an execution-time forecast.

The p24 E acquisition has eight statements; seven are used by the selected forest. Its registry binds `b5/p24_pointwise_acquisition_v1/ACQUIRED_POINTWISE_EXCLUSIONS.json` and the pointwise acquisition review. The p25 F registry contains 32 canonical statements, although only seven F claims appear in the selected forest. The ABCDF loader also retains its other registry gates, including C even where the selected forest has no C leaf. **A zero selected leaf count does not remove a registry gate checked during Session construction.** Full statement acquisition/source validation remains required; old registry names or old PASS receipts are not fresh proof.

## Required execution and joining work

A sound implementation still needs all of the following:

1. A sealed, externally pinned new source/contract epoch, with the supplied complete mathematical row, exact 93 kernel bytes and a reviewed native loader. The historical checker is retained as an exact reference.
2. An explicit source/header/registry migration adapter for the mixed loaders and selection/freezes. It must not alter mathematical domains, schedules, typed results or acceptance controls.
3. Genuine complete B5 INITIAL/resource acquisitions, or independently validated fresh exports, joined to these exact rows. The stronger24/contact and unrestricted attained positive-closed witness premises remain explicit; a conditional historical resource declaration does not acquire them.
4. Fresh complete E and ABCDF registry acquisitions and their original controls, or independently validated compatible completed exports. Their source/capture epochs must be genuine current executions.
5. Full Colab mixed acceptance of the selected candidates: all roots and ordinary/dynamic/theorem leaves; the complete structural lists; the explicit extra full-result negative control; before/after source checks; actual launch and stopped stdout/stderr/result bindings.
6. A new exact same-witness regional composition. Neither mixed receipt is an all-native `COUNT_ACCEPTED` receipt, and neither can silently enter the existing 01--07 ordinary validator.

The available bytes are sufficient to start this reconstruction without inventing an inequality or reusing an old successful capture as current. This note does not certify that the adapters, mathematical prerequisites or fresh replays have already been completed. Fresh arithmetic, native acceptance, parent/theorem acquisition and all-law/all-index flags remain false.
