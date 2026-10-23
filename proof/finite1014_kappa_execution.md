# 56K: fresh full scalar kappa=62/625 certificate

This isolated notebook supplies one shared scalar arithmetic dependency for later Fourier joins. It does not execute a Fourier integration or acquire support, Prawitz smoothing, a parent theorem, complete package 56 or the all-index conclusion. Its result never rewrites the source manifests or historical inputs of 56A/B/C/D.

The mathematical reduction and its boundaries are in [the Fourier source/algebra audit](code_finite1014_fourier_audit.md), section 4. That audit is fallible internal AI review, not external independent verification. Neither that audit nor the source-preparation report claims a fresh scalar run. The first actual complete original calculation is to run in Colab.

## Unchanged original source and exact action

The [source plan](finite1014_kappa_source_plan.json) has SHA256 `3cfa73a7278e06b71c65cbb8726a500f2b6b3b6bd1524de852749f76544489bb`. The three original mathematical files, 12,771 bytes in total, are supplied in `vendor/kappa_62_625/`:

| Original file | Bytes | SHA256 |
| --- | ---: | --- |
| `kernel.py` | 4152 | `16170505dece7571725e4e601f1546989d546ed64685616f9d13283c59702b0a` |
| `controls.py` | 2951 | `331ee713e7950c9013d969b70de5809d4eb7e37ac34cd22a6184e0f8872fe4b5` |
| `PROOF.txt` | 5668 | `6645891bc75553f1a35faba00dd2a09e6b47c5fd374e637d83d62ec82069c162` |

These bytes were read directly from `cutoff5_20261020.zip`, archive SHA256 `8428002462d4e650613ea6e2ff673cb1e69c2079572cc40546d125349d582419`. The complete member prefix, public archive URL, attribution and license identity are in `vendor/kappa_62_625/PROVENANCE.json`. No original mathematical code is edited. The small vendor closure removes a large archive download from this notebook's startup. No historical CERTIFICATE, CHECKED or stdout/stderr files are supplied as task inputs.

`finite1014_kappa_sources.prepare` makes a new private capsule containing exactly those three files and writes `SOURCES.json`. Both original outputs must be absent. The only mathematical command is:

```
<current-python> -B -S <original-absolute-task>/capsule/controls.py
```

Its working directory is that capsule. Original `controls.py` requires ordinary nonoptimized Python with bytecode disabled. It has no Windows-only resource guard, subprocess launcher, external package dependency or numerical planner. The original full `controls.py` is called directly; it is not replaced by a wrapper's weaker certificate test.

## Complete scalar calculation

The original command constructs the degree-13 polynomial certificate and validates all 81 fixed closed cells: `[i/16,(i+1)/16]`, i=0,...,79, then `[5,625/124]`. It checks all 1134 strictly positive Bernstein coefficients and the inverse polynomial identities, the exact changed convex-splice margin, and the exact Machin pi bracket. It requires rejection of 21 malformed certificates and performs 324 additional exact power/Bernstein evaluations.

The scalar inequality extends by evenness and the elementary outer-domain argument to every real x:

`cos(x) <= 1 - x^2/2 + (62/625)*abs(x)^3`.

The associated nonnegative decreasing convex splice is on z>=0; convexity of its even extension on the whole real line is not asserted.

The original command exclusively creates `CERTIFICATE.json` and `CHECKED.json`, then prints the CHECKED object. Required terminal status is `PASS_GLOBAL_COSINE_KAPPA_62_625_AND_CONVEX_SPLICE_V1`. It is not compared to a historical receipt SHA. Its source-path map must refer to the actual originating capsule, the three actual unchanged sources and the newly constructed certificate. A relocated completed export preserves those original path strings and all receipt bytes, using contained readback mapping instead of rewriting them.

## Evidence and exact completion boundary

The wrapper records `OBSERVED_FINITE1014_KAPPA_V1` with scope `UNCHANGED_GLOBAL_SCALAR_KAPPA_62_625_BASIC_ONLY_V1`. The observed record initially has `scalar_certificate_arithmetic_completed=false`.

Pure readback checks the current implementation/source-plan pins, exact command and cwd, actual launch and supervisor-result files, typed zero exit, stopped successful BASIC scope, both bounded capture hashes, empty stderr, and whole stopped copies of both original outputs. It also checks the literal certificate polynomial/domain/ordered-cell census and positive recorded coefficients, all native receipt/control counts, actual source/certificate hashes and equality between the stdout JSON and CHECKED object. It does **not** import the original checker or run a second polynomial computation.

Only after those checks can `COMPLETED_FINITE1014_KAPPA_V1` set `scalar_certificate_arithmetic_completed=true`. It seals the observed record, summary and complete artifact inventory. `validate_completed(task)` revalidates all these files without numerical replay and returns `REVALIDATED_FINITE1014_KAPPA_V1`. False controls, missing cells, incomplete capture, source mutation, stale implementation, a changed receipt or a promoted unrelated proof flag cause rejection.

The following flags stay false in observed, completed, revalidated and session results:

- `native_arithmetic_accepted`
- `support_acquisition_verified`
- `prawitz_verified`
- `fourier_integrations_completed`
- `full_notebook56_completed`
- `parent_acquisitions_verified`
- `all_index_conclusion_verified`

The first flag describes the stronger native resource contract, not the content of the scalar calculation. A complete BASIC arithmetic result remains a specifically scoped scalar result; it does not become an unrelated theorem by aggregation.

## Colab, budgets and completed cache

The generator is `tools/make_finite1014_kappa_notebook.py`; after runtime review/publication it builds `56K_kappa_62_625.ipynb` with an immutable full runtime commit. No placeholder commit is a delivery. The notebook mounts the existing `MyDrive/Berry-Esseen-end2end` destination, checks the actual Linux supervisor and synthetic wrapper fixtures, then calls:

```python
from be_replay.finite1014_kappa import run_colab
RESULT = run_colab(durable_root=DURABLE, backup_interval=60)
```

The command uses the existing unchanged Linux BASIC process-group supervisor. Limits are 2 GiB per-process address space, 43,200 seconds per-process CPU, 54,000 seconds external wall time, 256 MiB sampled run-directory files and 16 MiB captured logs. Live process-group CPU/RSS are sampled. These are not aggregate kernel memory/CPU quotas, do not contain descendants that change session, and do not claim equivalence to a Windows Job or private cgroup. Budgets are ceilings, not a numerical runtime estimate.

Progress prints every 20 seconds. Live backups are attempted every 60 seconds, with a final session ZIP on success or handled failure. Live backups and incomplete outputs are not accepted certificates. There is no partial mathematical resume: an interrupted original call restarts in a new empty capsule.

Only an entirely completed transaction is cached, under `finite1014-kappa/completed/<source-plan-prefix>/`. Reuse requires the actual ZIP SHA sidecar, a bounded canonical inventory, safe contained extraction without links/duplicates/case aliases, and full current source/evidence revalidation. The cache holds exactly three sources, two original outputs, their two stopped copies, launch/captures/supervisor result and the three task ledgers. Old path strings and receipt bytes remain unchanged. Stale, partial, corrupt or incompatible caches are rejected, and retained exports are not deleted. A reused valid completed transaction skips the mathematical command entirely.

## Local validation scope

Local fixtures use a mocked supervisor and explicitly fabricated certificate data to test infrastructure. The fabricated data are not claimed to satisfy the original polynomial identities; only the full original controls call can check those. Tests cover source admission, exact command/budgets, all scope/control/domain fields, actual capture and stopped-copy bindings, empty stderr, relocation without mutation, complete-only cache, safe ZIP admission, failure export, notebook defaults and syntax. Source-plan/vendor checks only hash and parse original bytes. No original mathematical module is imported or executed by those fixtures.

Seventeen local infrastructure/notebook fixtures passed. The same seventeen fixtures also passed in a clean copy containing only seventeen publication dependency files, with zero ignored `work/` inputs. This copy included the three original vendor files, provenance/license, source plan, isolated driver/evidence/helper, shared supervisor/backup/environment files, generator/base and tests. Its source preparation and synthetic tests do not establish a numerical PASS. Final tracked-blob/runtime-commit publication checks and fresh Colab execution remain separate; downstream consumption of the exported scalar fact also needs an explicit semantic join.
