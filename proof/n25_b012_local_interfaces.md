# Selected B1 panel35 and B2 panel31 local acquisitions

Date:23 October2026. This bounded audit read archive source, ASTs, JSON and
hashes only. It did not import an archived module, evaluate a numerical kernel
or accept any historical receipt. The machine-readable source map is
[`n25_b012_local_interfaces.json`](n25_b012_local_interfaces.json). Its recorded
arithmetic and interface objects are historical input/provenance, with every
fresh acquisition flag false.

All paths below are members of `cutoff25_20261011.zip`, relative to its
`cutoff25_20261011/` root. The archive is514,958,998 bytes, SHA-256
`17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb`.

## Exact selected jobs and source availability

| Local target | Closed p domain | Closed rho domain | Selected local count capsules |
| --- | --- | --- | --- |
| B1 panel35 | `[7/20,9/25]` | `[11/10,6/5]` | `new_root/local_theta_b1_p35_q0..q3_v4` |
| B2 panel31 | `[31/100,8/25]` | `[6/5,13/10]` | `new_root/local_theta_b2_p31_q0..q2_v4`, then `new_root/local_joint_cubic_b2_p31_q3_v5` |

The literal selections are `new_audit/LOWER_B1_COMPLETE_SELECTION_V1.json`
and `new_audit/LOWER_B2_COMPLETE_SELECTION_V2.json`. Their exact pins and the
eight selected contract hashes/rows are retained in this JSON and in the
75-job retained catalog. The parent checker/candidate locations are:

| Target | Local source directory | Local candidate | Frozen local manifest SHA-256 |
| --- | --- | --- | --- |
| B1p35 | `new_root/local25_b1_v2/` | `PANEL_35_PROOF.json` | `b64fb9fc11febd10b6421af2d13281071345a62ff0c1fe8d80cdeb0889b649eb` |
| B2p31 | `new_root/local25_b2_v2/` | `PANEL_31_PROOF.json` | `448f299188f05fd9c41f9531298732612de97091f41693ea0ceb40dbe4e0c2a6` |

Each local manifest has7 entries. Each imports the sibling
`initial25_bB_exact_v1/` manifest with30 entries and
`resource25_bB_v1/` manifest with32 entries. Every declared file in these six
manifests was present and matched its actual SHA-256. The supplied local
candidates are approximately3.5MiB each. This is source/input availability,
not fresh acceptance. The JSON records every source row and candidate pin.

The B1 INITIAL/resource manifest pins are respectively
`b8915e0a7b2e51df6db0218c6a23365040ce3303cb2b4d7ab49c9db7d302c8b8`
and `f352792aa7db4fd36bedc07773e090ae77668bf35e683b9773e36a85063cc2e5`.
The B2 pins are
`b6c07b868dc99414b124175a9c5863a8dc701248231ef02ea175b294a2a4bcfa`
and `96cf787e4db37a65d529d41d180737c2534dddbb7ac374be777d5b395f9abe7c`.

## Finite work and the fresh-parent binding constraint

The selected original commands, from the corresponding local directory, are:

```text
python -B mixed_b1_memoized.py construct 35
python -B mixed_b1_memoized.py accept 35
python -B mixed_b2_memoized.py construct 31
python -B mixed_b2_memoized.py accept 31
```

These are four full local protocol actions. **Each** selected construction or
acceptance computes four cycles with four complete signed INITIAL covers per
cycle:16 mathematical covers, each accounting for18,432 signed rectangles,
and four isolated `resource_worker.py` invocations. Acceptance recomputes the
whole result, compares the complete candidate, and performs12 strict
full-object mutation controls. It does not merely hash the constructed proof.

The recorded resource replay-plan lengths per cycle are `[11,10,9,7]` for B1
and `[12,9,7,6]` for B2. Each resource invocation has one base `retained_cell`
call and then one call per selected plan step. The selected histories contain
no newly contracted support-ray certificates: their `support` lists are
empty; the acquired parent supports are retained. These counts do not replace
the Gaussian/HIGH/resource arithmetic inside a complete cover or resource
call. A constructor may discover its finite plan afresh; the acceptance binds
and replays that plan.

The existing exact cache starts empty for each action and keys the complete
typed `(profile,raw,D)` tuple. Historical acceptance sidecars record16 misses
and0 hits for B1, and14 misses plus2 hits for B2. Those are historical runtime
observations, not a promised fresh runtime. A cache hit returns a deep copy
and repeats the permitted initializer. The helper/source proof is
`exact_stage_cache.py`, SHA-256
`95c9b510c8a40e3e73e782c67d98ce0f29ea09ce689f4f3e993ad3580ca5d15d`.

Both local protocols require their respective whole global INITIAL and global
resource parents. `mixed_bB.parents()` checks their full source maps, profiles,
proof/receipt/checker edges and all100 resource rows. The local candidate's
`parent_binding_sha256` includes the **actual parent acceptance receipt bytes**.
Fresh timed receipts will normally change those hashes. The supported next
route is fresh construction followed by full acceptance against the fresh
parents, preserving the old source. Do not copy an old accepted receipt,
rename a fresh receipt to an old hash, or declare an unchanged historical
local candidate accepted under a different parent context. Any optimized
metadata-only candidate migration would need its own explicit reviewed rule;
it is not supplied by this audit.

At queue level, the B0–B2 parent lane comprises six global physical native
calls: three full INITIAL acceptances and three whole global-resource
acceptances. The INITIAL receipts have deterministic untimed bytes: the
separate parent-source audit confirmed that their freshly serialized form
matches the archived receipts for all three branches. The archived global
resource candidates can therefore remain valid under those fresh INITIAL
acceptances; extra global construction commands are unnecessary. Add the four
local construction/acceptance actions above, giving **10 future full actions**.
The timed global resource receipts require the local construction step.
The75 resource-to-count edges (67 global and8 local) are additional semantic
work. Their75 count replays are already the retained batch and must not be
counted again as new forests.

## The guards are hypotheses chosen before exact acquisition

`new_root/prepare_lower_count.py`, SHA-256
`808c7fadd6daad24b369d233ee30176f02a90ce28f6f70b89e7fef4f9bc1de75`,
explicitly takes floating-point pilot JSON as **design input**. With grid
`g=10^5`, it makes upper guards `ceil(g*x)/g+1/1000` and lower guards
`floor(g*x)/g-1/1000`, retaining nonnegative binary price and physical beta/mean
clamps. The same directions apply to upper `A,Fplus,Fminus` and lower
`Qbudget` in its six quadratic planes. These literal rationals are not exact
resources acquired from a physical law merely because they are outward
roundings of pilot numbers.

`prepare_theta_count_pilots.py` adds a separate theta hypothesis using
`ceil(10^8*theta)/10^8+1/10000`; it leaves all original row values unchanged.
`prepare_local_theta_quarters.py` changes only the probability interval into
four ordered closed quarters and adds the reviewed allocation contraction.
Thus the original `Lambda`, `d0`, coupled prices and phase planes remain
literal contract values. The final exact interface needs **domination** by
fresh exact resources; it should not demand equality with the pilot JSON or
reapply this design rounding to fresh values and silently change a contract.
Historical `source_inputs_sha256`/`theta_design_source_sha256` retain their
design provenance; they are not fresh acquisition receipt pins.

## Complete resource-to-eight-contract implication

The source rule is `new_audit/compose_lower25_complete_v1.py`, SHA-256
`483198e77dd3ce5fb0103e744dfe87448bab8788f11a13bdc0731d4f632f1347`.
Its `next_profile` and `merge` routines at lines64–89 intersect the previous
resource, acquired INITIAL export and new resource **for the same law and p**.
Its local loop at lines157–189 checks four ordered cycles, cover inputs,
complete signed accounting, nested supports, the mean floor, merged resource
inputs and complete plan histories. `physical` at lines108–131 and the
resource map below then establish the count hypotheses.

The scalar/phase routine is
`new_audit/compose_middle_b5_exact_v2.py:155–171`, SHA-256
`a4dcf781b400bce7fadfa93523bdd0db8a6fe1b3678fd1c19c2b94391b70dcbc`.
For **each** of the eight fixed contract rows, a new semantic join must check:

- n25, K0, exact selected p-quarter containment in its parent panel, and
  containment of the acquired rho interval in the contract rho interval;
- acquired upper bounds `D,d0,lambda_max,H_minus,H_plus,radius_minus,
  radius_plus,outer0,outer1` no larger than contract fields
  `D,d0,Lambda,Hminus,Hplus,radius_minus,radius_plus,outer0,outer1`;
- acquired prices `charge_b,charge_g,charge_h` no smaller than the nonnegative
  contract `binary_charge,gap_charge,noise_charge`;
- full signed quadratic-envelope domination, not just coefficient hashes or
  the scalar defect cap;
- actual centered sign-conditioned marginals, both endpoint lower bounds,
  signed beta interval containment, mean interval containment, and the
  separately acquired `raw_row.theta <= acquired_theta_upper < 1`.

For the quadratic step, on each sign's closed interval `0<=h<=Hsign`, an
acquired plane `q` must be bounded by at least one target plane `t`. Its
difference is
`(t.A-q.A)+(t.Fsign-q.Fsign)h+(q.Qbudget-t.Qbudget)h^2`.
The exact minimum is attained at an endpoint or, for positive quadratic
coefficient and a vertex strictly inside the interval, at that vertex.
Nonnegative minimum for a chosen target plane proves domination on the whole
interval. The source checks all six acquired planes on both signs, giving12
dominations per contract and96 for these eight semantic edges. The old JSON
selects target indices2/3 alternately; those old margins are provenance until
recomputed from the actual fresh resource object.

The sign endpoints are bounded below by the maximum of the current raw and
resource-seed `A/B` bounds. The beta interval intersects the final profile,
raw row and seed; its upper end uses the **signed** raw beta cap. The mean
lower bound intersects retained bounds with a downward square root on grid
`10^12` of `(1-theta)*min(p_l(1-p_l),p_u(1-p_u))`; its upper end intersects
all relevant same-law upper bounds. The count sign/mean/beta intervals must
enclose these entire acquired intervals, including equality points.

Theta has a distinct physical meaning. For `v=p(1-p)`, sign-conditioned
decomposition and variance1 give `theta=s/(v+s)` and
`lambda=n*v*theta/(1-theta)`. A bound `theta<=T<1` therefore contracts the
current lambda coordinate by `n*vmax*T/(1-T)`. It does **not** replace the
original coupled-plane `Lambda`. This elementary monotonicity implication is
spelled out in `new_root/THETA_VARIANCE_PROOF.txt`, SHA-256
`5092342a816ae4c92173e1112031e19fa450f8abc8eb9041a2b8ba3566e582e8`.
It remains conditional on the same physical decomposition and acquisition.

## Existing interface tests and the selected B2q3 detail

`new_root/check_lower_local_interfaces_v1.py`, SHA-256
`910a3fc4054dae33e2061683a0c9477cfdd5bcdf28a41df682b92d2873295a5d`,
calls that physical map for each closed quarter and tests eight corruptions:
theta too small, beta upper too small, mean lower too large, either endpoint
floor too large, defect cap too small, gap price too large, and p outside the
acquired panel. Its two historical interface JSON files are present; their
pins and the exact archived scalar/contract rows are in the machine-readable
map. These are existing tests and recorded assertions, not freshly run checks.

That helper names the old B2q3 theta capsule, whereas the regional selector
uses the joint-cubic v5 capsule. Direct byte comparison found their contract
JSON identical, SHA-256
`bc48aab017e9d291efd9abd81ee80ee9d4d9685a592daf31dd814f966b32bb90`.
Consequently a correct numerical resource-to-contract implication transfers
by exact contract identity. The final join must still bind the actual selected
joint-cubic checker, forest and kernel; the old helper's directory name does
not establish that selection. The other seven selected contracts use v4.

## Portability and obligations that remain open

The local source is not a single-process native stage: `mixed_bB.py` launches
`resource_worker.py` once per cycle. Its imported INITIAL/resource closures
contain no `ctypes`, `resource`, multiprocessing or threading imports in this
static audit. Their source is supplied, but successful Linux execution remains
unobserved here. The existing trusted single-process guard deliberately denies
the worker spawn. An unchanged subprocess route therefore needs the honest
BASIC process-tree execution classification, or a separately reviewed execution
contract/explicit new orchestration. Do not weaken the single-process guard
or label a BASIC run trusted native. This execution distinction does not undo
the exact arithmetic that a completed full replay can calculate.

The INITIAL source consumes the frozen stronger24 statement, SHA-256
`f3c6a95c5fa814cc024872c0b4212d7d5272d8b7696306dfc0f5a3b74d12167f`,
with conclusion `C24 < CE + 1/80`, yielding contact allowance `25/80=5/16`
and owncap `434477/1000000` here. A fresh stronger24 acquisition must be
joined semantically to that precise premise. The stored statement's PASS
label is not that fresh acquisition.

The remaining analytic obligations are the same-witness attainment/contact
reduction, sign-conditioned physical interpretation, soundness of each
INITIAL/resource necessity and signed-cover exclusion rule, and the count
kernel lemmas identified in the retained analytic review. JSON equality,
`INDEPENDENT_REVIEW`/`CHECKED` objects and passing corruptions establish source
or interface consistency, not those analytic theorems by themselves. No
counterexample or sign error was established in this bounded audit. The next
concrete work is the six global acquisition stages and four local full actions
with explicit fresh parent bindings, followed by all75 resource-to-count
edges, including the eight local edges specified above. No complete B0–B2,
n25 or all-index conclusion is claimed.
