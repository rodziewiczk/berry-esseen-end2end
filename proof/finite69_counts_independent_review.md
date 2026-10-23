# Finite6–9 selected counts: bounded internal peer read

Date: 23 October 2026. This is a fallible internal source/infrastructure review
by the same AI system, not external independent mathematical verification.
No original mathematical module, leaf evaluator or acceptor was imported or
executed locally. The separate actual-export readback of notebooks37/39 does
not constitute a Colab integration test of these new notebooks40–43.

## Exact reviewed version

| File | SHA-256 |
|---|---|
| `be_replay/finite69_sources.py` | `67e9e2bb1009d8a2c03c3b4d42480c7b06254998d70dd3f8c6bfbb63df2d3791` |
| `be_replay/finite69_counts.py` | `8b58244f0732c37f0bb9ef27d7e51d9bf91d5086e46153d7fa8d9b970b112652` |
| `be_replay/finite69_count_evidence.py` | `15c1a9a9ee4ac37672bd151c7bdcc1c5204afe2feb2425b9b0cb9d19ac3a4c33` |
| `tests/test_finite69_counts.py` | `6efffc1ce4d791c674aa7d75f284d4b897363bc6a793914dcfe1100ca134bbd2` |
| `tools/make_finite69_count_notebooks.py` | `9db8ae86d34bf7cc6c24df0b21da4dc5a43a7d7b076e1e251b74313115a96494` |
| `tests/test_finite69_count_notebooks.py` | `bf44af0e49e45a69f662699cf165f84fb531042e75334d5199dbce195751c753` |
| `proof/finite69_sources_catalog.json` | `2a0575f59f9d6c8e95c53f68767b1cbae28b1ed2f5cd72c27a240b50d1367232` |
| `proof/finite69_count_source_preparation.json` | `5c20642a96c0007180de6fedb7ab3e1a1ca5026915666029c0fad4c5a6fdf492` |

The detailed execution contract is
[finite69_count_execution.md](finite69_count_execution.md). The distinct parent
source-reconstruction boundary is
[finite69_source_reconstruction_review.md](finite69_source_reconstruction_review.md).
The count-only driver does not execute those parent rows or remove their
unresolved joins.

## Selected scope

| Notebook | n | Forests | Original roots | Nodes | Candidate leaves |
|---|---:|---:|---:|---:|---:|
| 40 | 6 | 90 | 630 | 330,158 | 165,394 |
| 41 | 7 | 72 | 576 | 95,502 | 48,039 |
| 42 | 8 | 64 | 576 | 58,726 | 29,651 |
| 43 | 9 | 58 | 580 | 27,430 | 14,005 |
| Total | 6–9 | 284 | 2,362 | 511,816 | 257,089 |

These are the fixed final selected forests. Each new native invocation runs the
unchanged `count_protocol.py accept`, all n+1 original roots, the full leaf
census and all 24 original named corruption controls. No search, truncated
forest or numerical source substitution is introduced. The native source's
own literal contract commitment and n/index/p/K/rho gates remain intact.
Historical acceptance outputs are excluded from all 284 selected input maps.

## Concrete defect found and corrected

The first evidence draft required `launch.wall_seconds` to be an integer.
The actual supervisor normalizes that field to a float in
`linux_supervisor._settings`, even when the caller supplies an integer. Its
successful real launch would therefore have failed the draft readback, while
the first mock preserved an integer and masked the mismatch.

The frozen version admits an exact integer/float wall value of 54,000, excludes
bool, and retains exact integer CPU/memory ceilings. The observed controller
budget remains an integer. The synthetic supervisor now reproduces the actual
normalized wall and heartbeat types. This is a repaired implementation
compatibility defect, not a failed inequality or a weakened numerical check.

No further material blocker was found in the inspected frozen source. This
conclusion does not guarantee successful actual Colab startup or completion.

## Source and import closure

The reviewer independently read the actual selected Python bytes from the
pinned cutoff6 and combined source ZIPs, checked their hashes and parsed their
ASTs: 7,360 Python-path occurrences reduce to 315 unique source hashes. Every
nonstdlib import resolves to a sealed sibling in each of the 284 selected
capsules. No subprocess, multiprocessing, threading, ctypes or Windows-specific
import/process call was found. The sole dynamic import is the literal
`__import__('math').factorial` in `finite_gaussian.py`; it is not an arbitrary
module loader.

A separate source-only LIMIT comparison found 23 unchanged checkers with a
10,000-node ceiling and 261 with a 50,000-node ceiling. Every selected catalog
census fits its original ceiling. Maximum selected node counts for n6/7/8/9
are 33,701/5,422/3,989/1,720. A new node-limit epoch is unnecessary for this
selection; the original resource limits remain unchanged.

The owner's pinned preparation report records source-only completion of all
four actual source caches and all 284 manifest/checker/contract/target/header
and structural-census checks. It reports no mathematical imports or arithmetic.
That report and its exact hash were read here; this review does not relabel
its metadata checks as native replay.

## Execution, evidence and cache boundary

The inspected runner/validator chain preserves the following checks:

- Exact selected source and candidate dictionaries, actual immutable bytes and
  one permitted fresh output. Unbound helpers, extra outputs and source changes
  reject. Each stage starts in its own source epoch.
- Actual original argv/cwd, one contained original task root, real supervisor
  launch/result, integer-zero exit, positive sample count and empty stderr.
  Captured stdout/stderr must match the stopped supervisor's SHA-256 values.
- Exact BASIC guard fields and documented per-forest 2 GiB, 43,200-second CPU and
  54,000-second wall budgets. These are per-process limits plus sampled live-group
  observations; cumulative whole-tree CPU and aggregate kernel memory enforcement
  are explicitly unclaimed.
- The entire terminal native stdout JSON equals the fresh receipt. Literal
  original status/scope/schema, n/index and full control labels are checked.
  Manifest, forest, contract, checker and every kernel hash are bound to the
  selected source catalog.
- Complete original roots, nodes, leaves, depth, saved decision census and
  maximum score are read from the unchanged candidate. The fresh evaluation
  count must equal the full leaf census. The large original n6 forest is read
  under the explicit 64 MiB metadata bound.
- Observed evidence starts with all acquisition/global flags false. Completed
  evidence is written only after validation and binds the entire source,
  candidate, capture, receipt and observed-record inventory.
- A completed ZIP needs a correct actual SHA sidecar, bounded ordinary members,
  no traversal/links/duplicates/case aliases and full relocated source/evidence
  validation before a native invocation is skipped. Corrupt advisory caches do
  not accept a partial stage. Interrupted native acceptance restarts completely.
  Later progress logging is outside the sealed completed-stage inventory.

The reviewer ran the frozen `test_finite69_count*.py` suite under `-B -S` with
repository-owned temporary storage: 19 tests passed in 6.490 seconds. These are
source/fake-process/notebook tests, not numerical replay. They cover the real
controller transition and relocated completed stage, failed/boolean exits,
nonempty or mismatched captures, source/control/status mutations, changed guard
and budget fields, forged completed exports, unsafe ZIPs, cache reuse and
failure export. Generated notebook execution cells were exercised only against
a fake module to verify their exact literal-index routing.

## Acceptance boundary

The standalone jobs can run in parallel because their result is conditional
count arithmetic. They do not acquire INITIAL/resource/support/Fourier facts,
same-law resource-to-contract joins, sequential sharp predecessor conclusions,
closed regional composition or a finite-index theorem. All corresponding
parent/global flags remain false, including native-platform acceptance.

The mathematical validity of every kernel identity, actual future process
execution and the final analytic/finite composition remain separate review and
evidence obligations. Source completeness and 19 passing infrastructure tests
do not close those obligations.
