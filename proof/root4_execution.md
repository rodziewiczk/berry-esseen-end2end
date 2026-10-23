# ROOT4 Linux resource epoch and actual full replay

The ROOT4 driver computes the original full producer and then its full read-only
replay. It does not accept a source manifest, old status, parent checkpoint,
geometry mask, or partial result as numerical evidence. Neither calculation has
been run for this port. Local checks used source hashing, AST comparisons, and
synthetic execution fixtures only.

The notebook interface is:

```python
from be_replay.root4 import run_colab
RESULT = run_colab(durable_root=DURABLE)
```

It returns `status`, an absolute results ZIP path in `bundle`, and an absolute
local `work` directory. Progress and backups are written every 60 seconds.

## Frozen sources and deterministic derivation

The 77 files in `vendor/root4_75a9470` were read from a Git archive of immutable
commit `75a94708872e2bc053f42a279559b23ed91e4402` and compared byte for byte with
the old publication tree. They comprise 73 Python sources, three analytic notes,
and the original license. No old numerical receipt is included.

The frozen manifest SHA-256 is
`eb3541112dd78d0bcef22ae8bb7fa4b307760199e478d43e35ad0c255b76053d`.
The original entry source is `n4_cpu_time_entire_root_2026_10_09.py`, SHA-256
`82b62e0088cd0055b1bc4b33bf3ca92087cafc62ff6396c679a7baf013672c0e`.

The original memory helper returns `None` outside Windows, while the ROOT and
HIGH coordinators require a positive measured peak. An external watchdog alone
therefore cannot run the unchanged producer on Linux.

A fresh private capsule replaces that helper with Linux
`resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024`. This is the kernel's
lifetime maximum process RSS in bytes. It is explicitly a different operating
system metric from Windows `PeakWorkingSetSize`; it does not claim API identity.
Missing measurements raise an error. The original strict 64 MiB HIGH and
256 MiB ROOT gates remain in place.

The original literal source-pin graph has 125 edges and is acyclic. The resource
change affects exactly five files:

- `n4_windows_resource_guard_2026_10_09.py`, the new resource helper;
- `n4_cpu_time_quadrature_cache_2026_10_09.py`, literal hash rebinding;
- `n4_cpu_time_cheap_linked_leaf_2026_10_09.py`, literal hash rebinding;
- `n4_cpu_time_geometry_join_2026_10_09.py`, literal hash rebinding;
- `n4_cpu_time_entire_root_2026_10_09.py`, literal hash rebinding.

All other Python source bytes remain unchanged. All 72 nonresource ASTs must
agree exactly after replacing recognized source-hash literals with their source
file names. No arithmetic constant, branch, bound, grid, timer, or validator is
excluded from this comparison. Empty `type_params` AST fields are normalized to
make the same source epoch usable across Python 3.11 and 3.12+.

The derived epoch SHA-256 is
`63f409204df8b1a786ce049dfdd1868f6b7fb736fc4053729b228f7675ce3a90`.
Every source byte and epoch record is rechecked before and after each full pass.
The original sources and their imported modules are never monkeypatched.

One pinned legacy Gamma compiler docstring contains an invalid escape sequence.
The launcher temporarily appends
`ignore:invalid escape sequence:SyntaxWarning` to `PYTHONWARNINGS` and restores
the prior environment afterward. Other warning settings remain. Exceptions,
other warnings, and any nonempty stderr fail the execution checks. Both captured
logs must match the hashes in the actual supervisor result.

## Full calculation and resource contract

Each pass invokes the original CLI, first `--produce`, then
`--replay-existing`. The replay freshly rebuilds all numerical data before
comparing every canonical nonresource receipt byte; it is a second calculation
through the same exact implementation, not an independent numerical algorithm.

Each pass includes all 260 original closed geometry parents, all 1300 HIGH
request slots before the shared cache, the complete-parent or all-four-children
portfolio, N=256, H spacing 1/8, all 16 closed eta cells, both orientations and
tails, and the original quadrature and threshold reserves. Complete UNKNOWN
results remain visible and never become an accepted target bound.

The native single-process Linux supervisor receives 320 MiB total hard
address-space allowance: 256 MiB for the numerical interpreter and 64 MiB for
its dedicated controller. The worker retains 43200 CPU seconds per pass; the
controller has a separate 30 CPU seconds. The original 60-second HIGH, cache,
and cheap stages, 180-second A1/Gamma phases, and 600-second optimized stages
remain unchanged. The default external wall watchdog is 54000 seconds per pass.
The wrapper also caps captured logs at 16 MiB and the private capsule disk tree
at 512 MiB; the original complete receipt cap remains 48 MiB.

These are limits, not runtime estimates. Two full passes can require more than
one ordinary Colab session permits. The current driver starts a fresh full pair
and does not resume numerical work from complete-parent checkpoint outputs.
Live backups retain complete checkpoints and any complete receipt as evidence;
they are not an accepted prefix or a claim that a disconnected session finished.

Native acceptance requires the actual established seccomp single-process
capability and its exact worker/controller caps and source hashes. An unavailable
capability, interrupted process, changed capture, stderr, changed source, changed
replay receipt, missing parent, or unresolved class leaves acceptance false.
There is no fallback through an untrusted discovery guard.

The selected producer uses standard-library exact integer/Fraction kernels.
Two imported historical floating probes attempt optional NumPy imports. `-S`
keeps site packages out of this worker, so NumPy is unavailable and no BLAS or
floating probe calculation is needed. No package installation or C++ compilation
is required for ROOT4.

## Remaining scope

A successful pair verifies the conditional bounded physical ROOT4 target
`U <= 4097/10000`, including its fresh comparison with `C_E`. It does not by
itself verify unrestricted all-law C4. The C3 input, attainment/contact,
localization, original-law physical Prawitz bridge, exact imported literature,
and final composition remain separate obligations in `obligations.json`.
The limited analytic review is recorded in `analytic_audit.md`.

The test suite includes a Linux-only source-closure and kernel RSS fixture under
the native supervisor. It calls no HIGH, quadrature, CDF, or ROOT producer. A
Windows test run skips this actual Linux capability check; it cannot establish
Linux execution readiness by itself. The full mathematical target remains open
until both full native passes actually finish and all classes close.
