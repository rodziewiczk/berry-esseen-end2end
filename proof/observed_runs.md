# Observed Colab arithmetic runs

This document records a user-supplied notebook 08 result inspected on 23 October 2026. The inspection read the saved stage receipts and stdout/stderr captures; it did not rerun the mathematical calculations. Raw logs, account paths, and VM identifiers are not published here.

## Notebook 08: all six n2/n3 stages completed in BASIC mode

The results ZIP has SHA-256:

```text
77b7750b3e6cb124a0622f906034dca8dec500aed07c8a70596c747285736e2b
```

Its session receipt records `exact_arithmetic_completed_untrusted_guard`, with all six required stages selected and computed. The arithmetic receipt records `COMPUTED_EXACT_OUTPUTS_UNTRUSTED_GUARD`. Every stage has observed return code 0, supervisor status `completed`, a null failure reason, and an empty stderr capture.

The recorded UTC interval is 23 October 2026, 10:25:41.818717 to 10:27:20.921536. The arithmetic driver reports 99.013 seconds elapsed, including orchestration overhead. These measurements describe this run; they are not runtime guarantees for another Colab allocation.

| Stage | Observed complete scope or terminal marker | Reported elapsed seconds |
|---|---|---:|
| `n2-scalars` | Original `verify_reductions`; `FRESH_SCALARS_COMPLETED n2-scalars verify_reductions` | 0.529 |
| `n2-primary` | All 70 tensor cells; `ACCEPTED_ALL_70_TENSOR_CELLS 35878 134` | 12.209 |
| `n2-independent` | All 70 cells through the independent integer checker; `ACCEPTED_ALL_70_BY_INDEPENDENT_INTEGER_CHECK 35878 18426 134` | 46.488 |
| `n3-scalars` | Original `analytic_constants`; `FRESH_SCALARS_COMPLETED n3-scalars analytic_constants` | 0.523 |
| `n3-identities` | 111 cells, 444 sign orthants, 95,904 exact grid identities | 9.362 |
| `n3-full` | Full 111-cell verifier with fresh C++ compilation; `ACCEPTED_FULL_N3 111 501156 219860 349` | 29.307 |

The full n3 stage records maximum sampled process-group RSS of 387,592,192 bytes. This is a sampled observation, not an aggregate kernel memory guarantee. The receipts retain source-cell hashes and log hashes; the complete private ZIP is identified above rather than reproduced in this document.

## Source and code provenance

- Mathematical source reference: [`75a94708872e2bc053f42a279559b23ed91e4402`](https://github.com/rodziewiczk/berry-esseen-045-certificate/tree/75a94708872e2bc053f42a279559b23ed91e4402) in the original research repository.
- Mathematical source-manifest SHA-256 recorded by the run: `8ca0f5c30991b50c61fc998c7c873873c2ac7d2bde6611123ce74651e1a3c26b`.
- Published notebook execution-code pin: [`4b2c0e44ae0d7d0f7985e5b8c7714a03c4607bad`](https://github.com/rodziewiczk/berry-esseen-end2end/tree/4b2c0e44ae0d7d0f7985e5b8c7714a03c4607bad). The archived driver and supervisor hashes match the bytes of these files at that commit.
- Archived driver SHA-256: `06667714b4822639ea7301400c28e09e199e23ae7c11fb344a6af15d3013f8f2`.
- Archived supervisor SHA-256: `61e71dd4a9653de2bbbee8c54928a1f5c5bffd0bf083dd324851716c3a1eaea2`.
- The run context records Python 3.13.16 and a C++ compiler. It records `historical_receipts_used: false`.

The execution-code commit above is the notebook's declared pin, corroborated by the two archived code hashes. The result ZIP does not provide a separate Git HEAD attestation for the whole execution checkout. This provenance inspection is not a fresh replay of the mathematical source inventory or leaf inequalities.

## Acceptance boundary

The requested mode was **BASIC**, using `UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP`. It supplied an external wall watchdog, owned process-group cleanup, per-process `RLIMIT_AS`/`RLIMIT_CPU`, and sampled group/file observations. It did not establish an aggregate kernel CPU or charged-memory limit, containment of descendants changing sessions, or equivalence to a Windows Job/cgroup contract. Samples of process-group CPU also must not be treated as complete accounting of every short-lived compiler or child process.

Accordingly, the saved results explicitly retain:

```text
native_arithmetic_accepted: false
all_law_theorems_verified: false
all_index_conclusion_verified: false
```

The observed checker outputs concern the supplied finite n2/n3 arithmetic, conditional on the stated analytic reductions. They do not independently prove those reductions or the literature inputs. The six-stage completion is useful new computational evidence; it is not trusted native acceptance, a certificate for C4 or later indices, or an all-index PASS. See [the small-index execution contract](small_indices_execution.md) for the distinction between BASIC execution and stronger native execution.
