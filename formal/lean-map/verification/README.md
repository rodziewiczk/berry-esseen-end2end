# Compiler verification history

`check-baseline27.json` and its log record the fresh direct compiler pass of
the 27-source checkpoint on25October2026: **904.28 seconds**, with compiled
mathlib dependencies reused. Every selected project source was recompiled.
Later mathematical additions and consumer changes are checked separately;
the current authoritative source set is the root `check-All.json`.

The optional `check.ps1 -ReuseVerified` mode is a development compiler cache,
not a numerical-certificate cache. It accepts only a previous successful
compiler record with the same toolchain, mathlib revision and compiler
options. For every reused module it checks the source hash, the exact compiled
artifact hash, and that none of its project dependencies was rebuilt. A
changed source/artifact/dependency forces recompilation of that module and
its consumers. New modules always require compilation. A missing or mismatched
cache configuration fails closed. Sources and the full selected inventory
must remain stable during the check.

The cache is local under `.lake/` and is not shipped. It is written only after
a successful full check. In this session the fresh27-source checkpoint also
seeded that cache immediately after its successful compiler pass, binding its
artifacts to the checkpoint report. The current report explicitly distinguishes
`reused_artifact`, `verified_at` and `last_compile_seconds`; preserved compiler
output is attributed to the original check. Root module logs and axiom lists
are not described as a new compiler run when reused.

For an independent fresh project check, omit `-ReuseVerified`. The portable
Lake route is another option. Neither route reruns the numerical kernels or
discharges accepted analytic theorem arguments.
