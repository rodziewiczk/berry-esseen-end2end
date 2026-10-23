# Source audit of the stronger24 premise used by n25

Audit date: 23 October 2026. This is a source and dependency audit. No mathematical producer, count acceptor or compositor was executed. Historical result files below identify the intended objects and census; their PASS labels are not fresh acceptance.

## What n25 actually imports

`be_replay/n25_parents.py` pins `STRONGER24_COMPLETE_JOINED.json` to SHA-256

```text
f3c6a95c5fa814cc024872c0b4212d7d5272d8b7696306dfc0f5a3b74d12167f
```

The exact 2,362,725-byte member is `cutoff25_20261011/continuation_20261011/STRONGER24_COMPLETE_JOINED.json` in `cutoff25_20261011.zip`. Copies in the n25 INITIAL capsules have the same digest. The consumed statement is **C24 < CE + 1/80**, with `n=24`, `K="3/10"` and status `PASS_FULL_STRONGER24_AUXILIARY_BOUND_IN_RETAINED_FRAMEWORK`. This is an auxiliary bound, not the sharp C24 bound and not a cutoff theorem.

The n25 INITIAL `fixed_support()` reads those statement fields and derives the next contact allowance `q25 = (25/24)(3/10) = 5/16`. It then performs its own support/own-score construction. The current n25 driver correctly retains `stronger24_acquisition_verified: false`: completing notebooks 09/10 does not acquire this imported premise or the later count interfaces.

The current notebook 01–07 count jobs and notebook 09/10 parent jobs remain valid conditional work and are needed by the selected n25 route. This finding does **not** require restarting them. Their source-bound outputs can be completed before the auxiliary fact is freshly acquired; the later proof join must connect that acquired fact to the exact frozen statement they consumed.

The archive pin declared in `be_replay/count_task.py` is:

```text
cutoff25_20261011.zip
bytes: 514958998
sha256: 17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb
```

It is available as the [original source asset](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/download/cutoff20-sources-2026-10-17/cutoff25_20261011.zip). Selected member digests were computed directly during this audit. The historical aggregate receipt binds 12,590 files, including earlier progress records and unrelated cutoff material; that broad provenance inventory must not be mistaken for the minimal logical prerequisite set.

## Smallest identified original acquisition chain

Let `X10` denote `cutoff25_20261011/continuation_20261010` and `X11` denote `cutoff25_20261011/continuation_20261011` inside a private extraction. The original logical route is:

```text
published universal C20 <= 469/1000
  -> auxiliary C21 < CE + 11/210
  -> auxiliary C22 < CE + 9/220
  -> auxiliary C23 < CE + 3/115
  -> six stronger24 rho branches + universal high-rho tail
  -> C24 < CE + 1/80
  -> the conditional n25 contact allowance 5/16
```

This route does not require sharp C20, sharp C21–24, the n5 theorem, or an already proved cutoff31. It does require the retained attainment, same-law contact/support, charged INITIAL, resource and count implications, plus the external envelopes actually used by these sources. This audit locates those dependencies; it does not verify all of those analytic implications.

| Stage | Exact target / contact allowance | Required original numerical scope |
|---|---|---|
| n21 | `K=11/10`, target `CE+11/210`, `q=299/2000` | Five complete INITIAL covers: 92,160 signed rectangles; final negative defect. No count forest at this stage. |
| n22 | `K=9/10`, target `CE+9/220`, `q=53/210` | Seven INITIAL covers: 129,024 rectangles; all 100 resource panels; nine count forests, panels 31–39, 258 leaves. |
| n23 | `K=3/5`, target `CE+3/115`, `q=15/44` | Nine INITIAL covers: 165,888 rectangles; all 100 resource panels; 21 optimized count forests, panels 24–44, 18,377 leaves. |
| stronger24 | `K=3/10`, target `CE+1/80`, predecessor `q=15/46` | The six complete branches below, including their global/local acquisitions, actual count premises and 57,453 count leaves. |

The allowances are explicit in the source, rather than an assumption of monotonicity in n. In particular the n21 source uses the universal `.469` bound and the retained lower bound `.4095 < CE`; it does not consume a freshly proved sharp n20 result. The relevant predecessor receipt identities are:

| Member relative to X10 | Historical SHA-256 |
|---|---|
| `toward25/exact21/EXACT21_CHECKED.json` | `59d35a34b3f15f8b07516e22d9a975cce2b19573ec08684e11eb51ade8113107` |
| `toward25/POSITIVE22_JOINED.json` | `1e3aca987d228f62e741398dabd7c479ee5bbc2fe9251c90d1c44a44c809a468` |
| `toward25/POSITIVE23_JOINED.json` | `8871835341669078aa1a25b62e95ad7e8342dffae794c8d0cd7faf8032d4d563` |

The original `toward25/join22.py` and `join23.py` explicitly describe their conclusions as conditional on the analytic framework. Their source hashes are respectively `af13425d197e05ef5bd973ed7985bc4412bdc2077c251e95eba8e913c477dad8` and `21a8630d6120e15a55fd09b0f8c0f808ba63597a19b9d0fab99cb7c0df602185`.

## Exact stronger24 branch selection

All six branches concern the same attained unrestricted contrary witness at actual index 24. Every branch must account for the full 100-panel probability partition and acquire each surviving count contract, including the signed quadratic premises. A conditional accepted count forest alone does not establish its resource assumptions.

| Branch | Closed rho interval | Selected count panels | Leaves | Selected source locations |
|---|---|---|---:|---|
| B0 | `[1,11/10]` | 37–48 | 1,929 | X10 `local24/exact_b0`, `resource_b0_fixedpoint_v1`, `count_b0`; `join_b0.py` |
| B1 | `[11/10,6/5]` | 32–40 | 9,803 | X10 `local24/exact_b1`, `resource_b1_fixedpoint_v1`, `count_b1`; `join_b1.py` |
| B2 | `[6/5,13/10]` | Old 28–32; mean-floor patch 33–36 | 26,625 | X10 `local24/exact_b2_common_v1`, `resource_b2_common_fixedpoint_v1`, `b2_meanfloor_local_exact_v1`, `resource_b2_meanfloor_patch_v1`, `count_b2`, `count_b2_meanfloor_patch_v1`; `join_b2_meanfloor_patch.py` |
| B3 | `[13/10,7/5]` | 25–32 | 12,484 | X11 `stronger24/b3_initial_exact_v1`, `b3_resource_exact_v1`, `b3_mixed_feedback_selected_exact_v1`, `b3_count_conditional_v1`, `b3_composition_selected_v2` |
| B4 | `[7/5,3/2]` | 23–30 | 4,168 | X11 `stronger24/b4_initial_exact_v1`, `b4_resource_exact_v1`, `b4_mixed_feedback_exact_v1`, `b4_count_wave1_conditional_v1`, `b4_composition_v1` |
| B5 | `[3/2,712569/449000]` | 21–27 | 2,444 | X11 corresponding `b5_*` directories |

For B2, the old forests 33–36 are not substitutes for the selected mean-floor patch. The selected patch contract SHA is `b0ce1a7c120de2f430bf9306d004f300a2d946d8fc5a0e0c7fd8b3bbbfb9b85a`; its four forests contain 7,963 of the B2 leaves. B0/B1/B2 also retain complete-object fixed-point validation records; these optimization-equivalence checks are part of the selected source route, not automatically discharged by a scalar result.

B3 uses the corrected `b3_composition_selected_v2`, not either superseded v1 compositor. Its local schedule is six covers for panels 25–29 and four for 30–35, with second cycles only for 29–33. The historical complete local census is 16 cycles and 1,400,832 rectangles. B4 and B5 perform one four-cover local cycle for each actual global survivor, respectively panels 22–36 and 21–34. Their combined local census is 2,138,112 rectangles. Only the remaining survivors go to the selected count panels.

The union has 53 selected n24 panel forests. With the nine n22 and 21 n23 forests, the identified original route contains **83 panel forests and 76,088 leaves**. These are historical replay censuses, not a runtime estimate or evidence that a new run has completed. Each acceptor must still reconstruct the complete original count-root partition and recompute every leaf.

The selected `contract.json` member hashes were checked directly in the archive:

```text
n22          ff586219ed2d49924b566a265bec49a0eb1b43705628f086f612c7f7273f8621
n23          076838cbfac8fc36aab4ff86d3ba8ae8153f8b0d2ad7f11bfda749813826c2a0
n24-B0       743dc16999e84c5473568d6c150792d2f0124c846e2eafd5a08fb8bd74412b36
n24-B1       1ff58ab4a456adb38fca1646339ae11c6930a4590eca248006aad916d9073759
n24-B2-old   deb00c596a775a4fac6504e1c46e49f07b90161e6954a073d3d49b6c7527da94
n24-B2-patch b0ce1a7c120de2f430bf9306d004f300a2d946d8fc5a0e0c7fd8b3bbbfb9b85a
n24-B3       f61e40293ec51e51614b283fd80786086856f2bdc9dfa74fcbbf7b8094987ad3
n24-B4       b3313b8cf8224903137d2ae16501cc60dc46e60d51aecde8d720533a94072b15
n24-B5       2454b8b052a652ba88c4b4bc2e885e5efbbb69763cdd8e3be51ec2b2bbf9f8f9
```

The remaining rho tail uses the monotone minimum of the three selected Shevtsova envelopes, at the exact endpoint `712569/449000`, where the recorded envelope is `211/500`, strictly below the target. This tail step requires its exact scalar comparison and the external estimate, not an additional high-rho count forest.

## Original commands and working directories

The table records native entry points, not a claim that a ready Colab driver already exists. Run each command in the named source directory, in a new output epoch, with assertions enabled. `python -B -u` denotes the selected interpreter with bytecode disabled; `-O` is invalid for these protocols. Preserve the required sibling layout and copy only source inputs and explicitly identified candidate/input objects. Accepted outputs must be produced in that epoch.

| Working directory | Original command / action |
|---|---|
| X10 `toward25/exact21` | `python -B -u check21.py` |
| X10 `toward25/exact22` | `python -B -u initial22.py construct`, then `accept` |
| X10 `toward25/resource22` | `python -B -u construct_resources22.py`, then `accept_resources22.py` |
| X10 `shared/exact23` | `python -B -u initial23.py construct`, then `accept` |
| X10 `toward25/resource23` | `python -B -u construct_resources23.py`, then `accept_resources23.py` |
| Each selected count directory | `python -B -u accept_strict.py INDEX`; `join_counts.py` is the original aggregation entry point |
| X10 `local24/exact_b0`, `exact_b1`, `exact_b2_common_v1` | `python -B -u initial24_bN.py construct`, then `accept`, with the matching N |
| Matching X10 fixed-point resource directory | `python -B -u construct_resources24_bN.py`, then `accept_resources24_bN.py` |
| X10 `local24/b2_meanfloor_local_exact_v1` | `python -B -u local_initial.py construct`, then `accept` |
| X10 `local24/resource_b2_meanfloor_patch_v1` | `python -B -u resource_patch.py construct`, then `accept` |
| X11 `stronger24/bN_initial_exact_v1`, N=3,4,5 | `python -B -u initial24_bN.py construct`, then `accept` |
| Matching X11 global resource directory | `python -B -u resources_bN.py construct`, then `accept` |
| X11 B3 selected local directory | `python -B -u mixed_b3_selected.py construct INDEX`, then `accept INDEX`, for all actual global survivors; finally `join_panels.py` |
| X11 B4/B5 local directory | `python -B -u mixed_bN.py construct INDEX`, then `accept INDEX`, for all actual global survivors; finally `join_panels.py` |

The resource protocols have their own fixed input names and source hashes. For example the n22/n23 resource folders consume the corresponding fresh INITIAL proof under their protocol's input filename. Preparing that input edge, including its source identity and accepted-parent receipt, is required; running a command in a folder containing old parent outputs does not establish a fresh edge.

Existing count forests can be treated as untrusted candidate data and freshly replayed by the unchanged complete acceptor. Repeating the search that originally found a forest is not needed to validate it. If a new forest is desired, the original search command is `python -B -u construct.py INDEX`; its output still needs complete fresh `accept_strict.py INDEX`. Never import an old `accepted_strict_INDEX.json` or count join as fresh acceptance.

The final historical command is, from X11 `composition_protocol_reviews`:

```text
python -B -u compose_stronger24_complete.py ../stronger24/reviews/FULL_STRONGER24_COMPOSITION_INDEPENDENT_REVIEW.json
```

Its source SHA is `c1f54ca9ca25190055df3c5187a743fe73a939374fa6b8e7c73cb036b8c7c43c`. It consumes the four-branch prefix and B4/B5 final reviews. The prefix source `compose_stronger24_b0_b3.py` has SHA `30aa1a28ba951051999d31712b49934bf7ec142907ad77681bcdc354a873b04a`. These original commands also consume historical review/progress identities; they are not yet a complete fresh-epoch composition protocol.

## Viable execution and the outstanding composition work

An unchanged full arithmetic replay in **BASIC** mode is viable in principle, with frozen sources, actual process/child census, captured logs, complete outputs and source/math review. The numerical drivers' use of subprocesses is an execution-contract issue, not an additional missing inequality or a failure of the analytic implication. As with notebook 08 and the tail49 BASIC route, its stronger native flag must remain false unless that stronger contract is actually established.

The current single-process `trusted_native` seccomp mode cannot run the selected B3/B4/B5 local drivers unchanged: `mixed_b3_selected.py` line 88 and `mixed_b4.py`/`mixed_b5.py` line 89 launch `resource_worker.py` with `subprocess.run`. The regional compositors also start separate interface checkers. A future stronger execution tag would require a reviewed compatible process-tree contract or a reviewed orchestration port with the exact numerical work preserved. This limitation does not prevent honest BASIC arithmetic evidence.

Fresh joins need explicit specification. The old `join23.py` pins the historical POSITIVE22 join and optimized COUNT23 join hashes; B0/B1 and other downstream components also pin historical predecessor/count artifacts. Yet the native n22 INITIAL receipt records `sys.version`, and the count acceptance receipts record `sys.executable` and `sys.version`. A Colab receipt can therefore have different bytes while certifying the same exact numerical object. Merely substituting old receipts to satisfy those hashes would not establish a fresh chain.

The smallest honest implementation work is a reviewed new-epoch composition layer that keeps the original numerical modules and contract/profile hashes, verifies actual fresh acceptances and parent edges, and reconstructs every scalar and signed quadratic resource-to-count implication. It must separate statement identity from historical receipt identity, preserve the exact closed seams and tail comparison, and issue a new receipt. The archived `f3c6...` file can remain a frozen statement/provenance input to n25; it must not be relabeled as freshly generated. A semantic join must bind an independently acquired matching auxiliary fact to the precise statement consumed there.

## Later sharp24 alternative and remaining limits

The separately supplied `cutoff5_10_15.zip` is 224,483,065 bytes, SHA-256 `268f71662171764d7ebe116910b5df82dfd58cadb2de2a7ef82db7da98b66dae`. It contains a later cutoff20 continuation under `cutoff15_20261017/supplied/continuation_cutoff20_20261016`. That later route claims conditional sharp bounds at 20–24. A genuinely acquired sharp C24 bound would mathematically imply this weaker auxiliary premise and could avoid duplicating its legacy replay.

The parallel inventory found no ready fresh standalone sharp24 acquisition. Its selected n20–24 count censuses are 87,986, 21,957, 14,442, 11,073 and 8,562 leaves, respectively, with predecessor/native/full-DAG joins still unresolved. The status points to `b0/sequential_synthesis_v8/CONDITIONAL_CUTOFF20_COMPOSED.json` (historical SHA `0247c2bbf7df6d101239818f097647e94f5f7a9fdef8ae49a60ebc71ed88ee08`), not an unconditional fresh C24 theorem. It is therefore an alternative to audit and compare, not an already acquired cheap replacement.

This note identifies a specific original route and its outstanding provenance/composition work. It does not prove that route is globally cheapest among all possible new arguments, audit every transitive import or mathematical kernel, establish its historical assumptions, certify a Colab resource contract, or promote stronger24/n25/global proof acceptance. Sources, runtime code and the proof graph were not changed.
