# Conditional fresh auxiliary21--24 numerical chain

This collector implements a new evidence and finite-edge protocol. It does
not execute INITIAL, resource, Fourier or count kernels. All numerical
work for those components belongs to the nine independent Colab jobs.
Local fixtures use synthetic evidence and mock the scalar calculation;
neither the scalar certificate nor the archived mathematical kernels
were executed locally.

## Inputs and completion scope

The required completed jobs are auxiliary21, auxiliary22, auxiliary23,
and stronger24-b0 through stronger24-b5. Their conditional input and
execution scopes are documented in `proof/aux21_23_execution.md` and
`proof/strong24_branches_execution.md`. In particular, historical proof
objects may be untrusted candidates, whereas their old accepted receipts
are never promoted to fresh arithmetic evidence.

The target chain is:

```text
universal C20 <= 469/1000 (external premise)
 -> C21 < CE + 11/210
 -> C22 < CE + 9/220
 -> C23 < CE + 3/115
 -> C24 < CE + 1/80
 -> n25 contact allowance <= 5/16
```

The universal C20 theorem, retained attainment/contact/support/Fourier/
INITIAL/resource/count implications, the exact optimized-arithmetic
identities, and the published high-rho envelopes remain explicit
mathematical premises. The collector verifies that the newly replayed
finite objects fit those implications; it does not claim to acquire the
premises or the unrestricted auxiliary theorem.

Every imported auxiliary result must have the literal n, K and allowance,
the expected source-selection pin, current reviewed driver identity,
complete finite census and same-object semantic edges. Each branch must
have n24, K3/10, global predecessor allowance15/46, and the exact frozen
n23 statement identity
`8871835341669078aa1a25b62e95ad7e8342dffae794c8d0cd7faf8032d4d563`.

The six closed rho intervals are
[1,11/10], [11/10,6/5], [6/5,13/10], [13/10,7/5],
[7/5,3/2], [3/2,712569/449000]. Their exact endpoints match, with no
unaccounted open seam. The selected count scopes are:

| Source | Panels | Forests | Leaves |
| --- | --- | ---: | ---: |
| auxiliary22 | 31--39 | 9 | 258 |
| auxiliary23 | 24--44 | 21 | 18,377 |
| stronger24-b0 | 37--48 | 12 | 1,929 |
| stronger24-b1 | 32--40 | 9 | 9,803 |
| stronger24-b2 | 28--36, with the selected mean-floor patch | 9 | 26,625 |
| stronger24-b3 | 25--32, selected corrected composition | 8 | 12,484 |
| stronger24-b4 | 23--30 | 8 | 4,168 |
| stronger24-b5 | 21--27 | 7 | 2,444 |
| Total | | 83 | 76,088 |

Each branch's driver separately revalidates its full100 probability
panels, actual source/profile/INITIAL/resource edges, signed quadratic
implications, selected local refinements and every selected count leaf.
Those checks cannot be replaced by this table or a PASS word.

B4 and B5 legitimately strengthen their effective same-law support
allowances using the universal envelope. Their effective q values are
12351561/43750000 and746553/6250000. The collector requires those
source-validated values and verifies that they do not exceed15/46. It
retains15/46 as the global predecessor allowance; it does not incorrectly
require the effective support q to equal that global allowance.

## Exact high-rho scalar comparison

On Colab, `scalar_certificate()` uses exact rational arithmetic and checks
the following values. It never calls a numerical leaf evaluator.

At R =712569/449000 the minimum of
469/1000,
(1661/5000)(1+(429/1000)/R), and
(3031/10000)(1+(646/1000)/R)
is exactly211/500. Each expression is nonincreasing for positive rho,
so the same upper bound applies on the entire remaining ray rho >= R,
conditional on the external envelope theorems.

For the strict target comparison, the function bounds pi by
16 atan(1/5) -4 atan(1/239), using12 and4 alternating terms. For even n,
integration of the finite geometric expansion of1/(1+t^2) gives the
truncated sum as a lower bound for atan(x), and that sum plus the next
positive term as an upper bound. The minus4 coefficient is handled with
the opposite arctangent endpoint when forming the pi interval.

The Machin identity can be checked algebraically: tan(4 atan(1/5))
=120/119, hence tan(4 atan(1/5)-atan(1/239))=1. The latter angle lies in
(0,pi/2), so it equals pi/4. Thus the finite rational bounds do enclose pi.

The function checks exact squares for
r =3162277660168/10^12 < sqrt(10) and
s =2506628274632/10^12 > sqrt(2*pi), with s^2 greater than twice the
upper pi endpoint. It then checks

```text
(3+r)/(6s) > 40973218/10^8,
211/500 < 40973218/10^8 + 1/80.
```

Using the stated formula CE =(3+sqrt(10))/(6 sqrt(2*pi)), this supplies
the strict scalar margin below CE+1/80. The result records every rational
endpoint, series length, square-comparison input and the current source
hash. Exact rational identities also give the allowance sequence
53/210,15/44,15/46,5/16 at the subsequent target changes.

These operations are implemented for execution on Colab. Their successful
production is required by a completed collector run. The local test suite
mocks them and provides no claim of an actually observed scalar result.

## Bundle authenticity, relocation and waiting

The collector searches the selected durable directory for each job.
Auxiliary bundles use `auxiliaryNN/SESSION/bundles/ID/*-results.zip`;
branch bundles use `stronger24-bN/SESSION/*-results.zip`. It considers
newest files first and skips candidates that fail complete validation.
It does not accept a live snapshot as a completed job.

Every ZIP must be an ordinary bounded file with its actual `.zip.sha256`
sidecar, exact basename and matching SHA-256. Extraction rejects unsafe
paths, duplicate portable member names, links, encryption, unknown file
types, excessive individual members and excessive total expansion. The
whole ZIP hash is checked before and after extraction. Original receipt,
source and execution-record bytes are copied without rewriting.

The collector calls each driver's `validate_completed` in the new private
extraction. Those validators map preserved original execution paths to
the restored artifact locations while checking actual captures, guard
scope, source pins, controls, censuses and semantic edges. They import no
archived numerical module. The imported result is checked again against
the exact scope expected by this chain.

For each accepted import the collector records the source ZIP path/hash,
actual imported job-result hash, complete revalidated report/hash,
source-selection identity, current driver identity and contained restored
task location. A historical receipt cannot satisfy these new driver and
fresh-stage protocols merely by declaring PASS.

If any job is absent, incomplete or invalid, the result is
`WAITING_FOR_COMPLETED_JOBS`, with the missing job list and bounded
diagnostics. No scalar calculation or chain acceptance occurs. Rerun the
collector after the missing jobs finish; the original computation jobs
need not be restarted merely to scan their completed evidence.

## Public interface and output flags

```python
from be_replay.aux24_join import run_colab
result = run_colab(durable_root=DURABLE)
```

Optional defaults are `work_root='/content/berry-esseen-runs'` and
`backup_interval=60`. The return object contains `status`, `bundle` and
`work`. Progress identifies the job being searched, rejected incomplete
evidence, accepted source-bound imports and extraction progress; live
evidence backups run every60 seconds. A handled failure or a waiting
result still produces a final evidence ZIP and hash sidecar.

`CONDITIONAL_NUMERIC_CHAIN.json` has schema
`FRESH_CONDITIONAL_AUX24_NUMERIC_CHAIN_V1`. Only complete validation of
all nine jobs and the fresh exact scalar comparison can set
`conditional_fresh_numeric_chain_verified=True`. It then records the
83-forest/76,088-leaf census and the conditional target chain.

The flags `analytic_framework_verified`,
`universal_C20_acquisition_verified`, `full_auxiliary_bound_verified`,
`stronger24_acquisition_verified`, `all_index_conclusion_verified` and
whole-chain `native_arithmetic_accepted` remain false. The final flag
reflects the honestly mixed native/BASIC execution contracts; it does
not invalidate the independently classified arithmetic stages.
