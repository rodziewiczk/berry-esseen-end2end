# Notebook 08: actual n2/n3 computation, explicit trust boundary

`from be_replay.small_indices import run_colab; run_colab(durable_root=DURABLE)` executes six stages from the byte-pinned sources at commit `75a94708872e2bc053f42a279559b23ed91e4402`:

1. The original n2 exact scalar/reduction checks (`verify_reductions`).
2. All 70 cells through the native rational tensor checker.
3. All 70 cells through the independent integer checker.
4. The original n3 exact scalar/reduction checks (`analytic_constants`).
5. All 111 initial polynomial identities on all four sign orthants.
6. Fresh compilation of `check_cube.cpp`, followed by the complete original n3 verifier: 111 cells, exact C++ cube positivity, moment-domain checks and the final full-native marker.

The scalar stages are the original standard-library rational checks. They are not a claim to run the optional SymPy symbolic audits. Notebook setup must provide `g++` and Boost.Multiprecision headers before this run; the driver does not silently download mathematical inputs or substitute a prebuilt binary.

The vendored inventory has 189 files, including all 70+111 certificate shards and the original license. `MANIFEST.json` is pinned by SHA-256 `8ca0f5c30991b50c61fc998c7c873873c2ac7d2bde6611123ce74651e1a3c26b`. Every source byte is checked before and after execution. No historical acceptance receipt is an input.

## Why notebook 08 reports untrusted guard

The default Colab entry point computes all six stages in basic mode. This is a real native arithmetic run, with fresh inputs and fresh output logs. Basic mode supplies an external wall watchdog, POSIX process-group cleanup, per-process limits and sampled group observations. It does not establish the stronger native process-tree resource contract.

The unchanged n3 verifier launches the compiler and C++ workers. It cannot be accepted under a Python-only single-process seccomp contract. The driver does not remove guards, monkeypatch the original checker, or label basic C++ execution as trusted native acceptance.

A complete basic run therefore reports `exact_arithmetic_completed_untrusted_guard`, with `native_arithmetic_accepted: false` and `all_index_conclusion_verified: false`. The exact markers, complete cell census, certificate hashes, logs and environment are evidence for a later accepted replay; they do not close proof obligations on the strength of this weaker resource contract.

The separate `--mode native` CLI can run eligible single-process Python stages only when the supervisor establishes its actual capability. It checks the exact RAM/CPU caps and driver/supervisor source identities. The full compile/spawn n3 stage fails closed as unsupported in that mode. Even accepted scoped arithmetic remains conditional on the analytic reductions and literature.

## Visible progress and preserved evidence

Each stage emits a start event, actual new native stdout lines, periodic heartbeat and a final scoped status. Logs are saved under `arithmetic/stages/`; run context, individual stage reports and `SMALL_INDICES_RESULT.json` retain exact bounds and trust fields. Live backups are saved to the durable destination every 60 seconds. The session produces a final results ZIP and SHA file even after a handled interruption or failed stage.

No native mathematical kernel was executed locally while implementing this notebook driver. The local tests use source-integrity checks and controlled driver/supervisor fixtures only. They test missing/reordered cells, changed sources and logs, nonzero exits, timeouts, guard classification, exclusive fresh output directories and final bundle preservation.
