# Notebook35 V2: current-exec memory-counter readback

Date: 23 October 2026. This is a fallible internal source/infrastructure review
by the same AI system, not external independent mathematical verification.
No original mathematical kernel, search or numerical acceptor was imported or
executed locally. The earlier
[V1 review](n5_remaining_independent_review.md) remains a historical review of
its exact source version; it did not establish successful Colab startup.

## Actual failed export

The supplied export `20261023T192537Z-01dab922-results.zip` is 950,667 bytes and
has SHA-256
`2162466f17ce25936c1487def793b283f9f9de6ae23aaac987fcff345bf26a82`.
Its first selected job, `support`, returned integer 1 after 0.533955318000011
seconds. The outer reason was `nonzero_subprocess_exit`. Its stdout is empty
(SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)
and its 59-byte stderr says:

> C5_SUPPORT_INCOMPLETE: Runner itself exceeds64MiB peak RSS

The stderr SHA-256 is
`fb3c3785e13383206927ee89067386681f7785335dc129a5b208a3ad248b6f2e`.
The original support wrapper calls `parent_guard()` before source-cache
validation and prints `fresh_support_start` before launching any support
producer (`vendor/n5_remaining_snapshot_v1/reproduction/all_indices/c5_support_one.py:23–25,48–60`).
The empty stdout and this guard error therefore show a pre-producer failure.
No completed support arithmetic was exported; the session has an empty job
list and `incomplete_selected_arithmetic`, with native/full-n5 flags false.

The outer sampler observed a maximum live-group RSS of 4,194,304 bytes. That is
a sampled observation, not the actual process peak, and cannot demonstrate
compliance with the 64 MiB self-check. The export does not record the failing
`ru_maxrss` value or its pre-exec history. The mechanism below is supported by
Linux semantics; its precise numerical contribution in this VM is not measured
by this export. This failure is an infrastructure interruption, not a numerical
counterexample or an acquired inequality.

## Exact reviewed V2 sources

| File | SHA-256 |
|---|---|
| `be_replay/n5_remaining_bridge.py` | `f0459a0570ca9a4fc11e507f25474e67bf5e3e958a60513bb7be364d707a069a` |
| `be_replay/n5_remaining.py` | `4c23c8f353f9a5301821089aec417087dc9972839c58953e7d02abad8e39d7ff` |
| `be_replay/n5_remaining_evidence.py` | `c18d64bbd0691d90c7a89e359e659e2cbb6cc8d856149ce038cae37b5cf655b5` |
| `be_replay/n5_remaining_sources.py` | `17f8d9b3bcdce510574901be83684a630d54cc8d2f6251856b7737bbd85aaaab` |
| `tests/test_n5_remaining.py` | `70a494de540457b06790712f3c404334cea873de75834ee31246459f67e4eab7` |
| `tests/test_n5_remaining_bridge.py` | `a8bd49f4b233ee2b5ec0216f40d8be4985816d407c4ce45a28681c1b44c2d0a7` |
| `tests/test_n5_remaining_notebook.py` | `e57f2beeaa27c064e087ba56bedd96b36f596973d00c50b27e53473b0d065f0c` |
| `tools/make_n5_remaining_notebook.py` | `7f14a86a62f6ee5312df54bb5c73dff541cc7a6ba2218dcdee81b16ef96e8733` |

The source catalog remains
`29cd3d9f8c30d8391b19792d5197a5a9d6b26b67e294500f53b2827441553ca3`;
the unchanged vendor snapshot manifest remains
`53257e64c0712ea4b8ceac81472b57f6623754f55636fc56f29586670e330f8d`.
The bridge still requires exact original runner SHA-256
`795c673a5df57ac6619b66832957cbfa83f1f31e4e3a9a7e775c3c3c52307ed0`.

## Counter semantics and explicit policy change

Linux `getrusage` preserves resource metrics across `execve`; its maximum RSS
can consequently include a previous executable image. This differs from a
check of the newly started controller's address space. See the primary
[`getrusage(2)` description](https://man7.org/linux/man-pages/man2/getrusage.2.html).

The distinction is visible in a fixed Linux source version: during exec,
[`fs/exec.c` in Linux v6.12](https://github.com/torvalds/linux/blob/v6.12/fs/exec.c#L929-L956)
replaces the task's memory map and preserves the old map's high-water RSS in
`signal->maxrss`;
[`kernel/sys.c`](https://github.com/torvalds/linux/blob/v6.12/kernel/sys.c#L1733-L1773)
includes that stored maximum in `RUSAGE_SELF`. By contrast,
[`fs/proc/task_mmu.c`](https://github.com/torvalds/linux/blob/v6.12/fs/proc/task_mmu.c#L31-L62)
formats `VmHWM` from the current memory map's RSS/high-water counters. These
source links explain the semantics; they do not identify the actual Colab
kernel build.

V2 explicitly names the new policy
`LINUX_CURRENT_EXEC_VM_HWM_64MIB_V2`
(`be_replay/n5_remaining_bridge.py:16–42`). It uses uniquely present positive
`VmHWM` and `VmRSS` counters from `/proc/self/status`, requires KiB units and
`VmRSS<=VmHWM`, then converts the high-water counter to bytes. Missing,
duplicate, malformed, non-ASCII, excessive or inconsistent inputs fail closed;
there is no fallback to a zero counter. The original guard still compares that
result to exactly 64 MiB. The Windows `NATIVE.peak()` branch is unchanged.

This is an explicit resource-policy revision, not byte identity with the old
Linux counter. Both
[`VmHWM` and `VmRSS` are documented approximate observations](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html).
The change does not create exact RSS enforcement or cgroup/Windows-Job
equivalence. The outer BASIC process-group observations and per-process limits
retain their stated limitations.

## Source/evidence and regression checks

`derive()` now performs exactly four unique literal substitutions after checking
the entire original runner hash (`be_replay/n5_remaining_bridge.py:17–51`). The
AST comparison permits changes only to `own_peak` and the previously reviewed
`run_child`. Original numerical expressions, selected protocols, controls and
the literal 64 MiB comparison remain unchanged. The V2 policy is recorded in the
source request and checked by `verify_job`
(`be_replay/n5_remaining_sources.py:184–223`), and is included in the exact
implementation dictionary and V2 evidence scope
(`be_replay/n5_remaining_evidence.py:14,52–56`). Old V1 completion evidence is
not silently accepted as current V2 evidence.

The runner additionally exports bounded actual stdout/stderr tails and their
hash comparison on failure (`be_replay/n5_remaining.py:85–122`). Those diagnostic
bytes cannot accept a stage. The metadata-only adapter loader also removes a
previously loaded adapter closure from another checkout before importing the
pinned local copy; a synthetic stale-module fixture covers this case.

The reviewer run completed 27 source/fake/notebook fixtures in 42.964 seconds:
26 passed and one actual-Linux fixture was skipped on this Windows host.
No mathematical kernel was called. The new memory tests compile only the
original infrastructure guard functions from their ASTs. They check exact
64 MiB acceptance versus 64 MiB + 1 KiB rejection, malformed/duplicate counters and
the unchanged Windows branch. The Linux-only fixture allocates 96 MiB before an
exec, then separately after an exec: it requires the former to leave a small
current-exec counter and the latter to trip the original guard. That live Linux
distinction is not locally acquired by the skipped Windows run; notebook35's
fixture cell must execute it in Colab before numerical work.

No material source/fixture blocker was found in this narrow V2 review. A fresh
actual Colab startup and the selected 326-job arithmetic remain uncompleted by
this review. Successful startup would not by itself establish support rows,
all selected jobs, fresh theorem-level joins, full C5 or the all-index theorem.
All existing conditional-arithmetic and false native/global flags remain
required.
