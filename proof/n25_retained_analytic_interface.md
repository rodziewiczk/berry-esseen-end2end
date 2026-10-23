# Conditional analytic interface of the retained n25 B0–B2 counts

This is a source-level review, dated 23 October 2026. No archived Python module
was imported, no numerical kernel was evaluated, and no historical receipt is
new evidence. The selected inputs are the 75 jobs in
[`n25_retained_b012_catalog.json`](n25_retained_b012_catalog.json), SHA-256
`f055b5017d4e1fd14f2b48a6a95fef4a4c61a025dea6174c424cd5968de801f7`.
They have 1,950 ordered count roots and 94,288 saved leaves. Source availability,
selection and saved-tree counts are documented in the accompanying catalog.

## The theorem interface that a full replay can establish

Fix one selected job, its literal rational contract, its frozen kernel closure,
and one physical law satisfying **all** that contract's simultaneous same-law
premises. These include its original INITIAL/resource acquisition, signed
conditional marginal interpretation, support and endpoint bounds, quadratic
resource inequalities, and any beta/mean/theta/allocation or local cover used
by that particular kernel. Also assume the analytic soundness of each enabled
cell enclosure and infeasibility rule described below.

The conditional cell lemma required of `cell35` is:

1. For a closed box and count `k`, every admissible physical configuration in
   the box is retained by its internal interval contractions.
2. Each named `EMPTY_*` result proves that no such configuration exists.
3. Every other accepted result provides a rational `score_upper` that bounds
   the physical normalized one-sided quantity for every retained configuration.

Subject to this lemma, successful full native replay proves the strict target
bound on the union of that job's 26 original closed root boxes. It does not
establish the premise that the law satisfies the contract. In particular, a
literal `resource_status: ASSUMED_ACQUIRED_FOR_CONDITIONAL_TEST` validates an
input convention; it is not a resource acquisition theorem.

The selected B0, B1 and B2 rho bands are respectively `[1,11/10]`,
`[11/10,6/5]` and `[6/5,13/10]`. Combining their 75 counts would still require
the original global exclusions for the other 83/89/89 probability panels,
respectively, and correct resource-to-count maps for the selected panels.
B1 panel35 and B2 panel31 additionally require their respective 16-cover local
resource acquisitions. Four accepted closed quarters cover their original
panel only after the exact quarter endpoints and these shared premises have
been checked. These requirements are not consequences of count acceptance.

## Closed coverage and the native proof rule

The representative source is archive member
`cutoff25_20261011/new_low/count37_global_conditional_v2/count_protocol.py`,
SHA-256 `bb2bd2d650a2e003bbbd695f25982351833775717037c1fb3d86cd809c9722ef`.
Its `evaluate` function is at lines48–54 and `replay` at lines71–95.
An AST comparison of all 75 selected protocols found identical `evaluate`
and `replay` functions, including their type checks and cache key. Their AST
SHA-256 values, using `ast.dump(..., include_attributes=False)`, are
`3f48f9eb2502fda0a1494dec4b12d75d793253da43071affe782ae743b29c9a7`
and `bb5b2d40f1caebcdc321315dbc90d26481feaa0edabf05e4e0554e6722c1ccb9`.

Each original root is
`[p_l,p_u] × [0,Lambda] × [0,1] × [-1/2,1/2] × [0,d0]`, with the
literal count `k` ranging in order from0 to25. Each split uses an integer axis
from0 through4 and an exact textual rational cut strictly inside that axis.
Both children are closed and meet at the cut. Induction on the finite binary
tree therefore proves coverage of every root, including its boundary and all
split seams. A leaf must reproduce the entire reconstructed original closed
box, the freshly computed decision and the complete computed result.
Unknown node kinds, missing children, extra success fields, pending leaves,
wrong root order and boolean substitutes for integer coordinates are rejected.

`evaluate` supplies all five original box coordinates to `cell35`; it does not
trust a stored contracted box. Only a named member of the protocol's fixed
EMPTY set or an exact rational `score_upper < CE_LO` closes a leaf. A cell's
own `PASS` label is insufficient without this strict comparison. Equality is
not accepted. Exceptions and unknown statuses fail the replay.

The target `CE_LO` is a pinned rational scalar lower bound. To infer the final
comparison with the intended Berry–Esseen constant, its scalar lower-bound
lemma and the definition of the normalized physical quantity must also be
retained. Replaying the leaves does not independently prove those scalar or
probabilistic identifications.

## Cache and resource independence

Native `accept` initializes `cache={}`, replays the complete candidate, and
then runs 24 corruption controls. A memoization key contains `k` and every
endpoint of the complete reconstructed five-dimensional box. Distinct leaves
of a strictly split root have disjoint interiors; because the original widths
are positive and every cut is interior, two different leaves cannot have the
same complete nondegenerate box. Different roots have different `k`. Thus
every main leaf is freshly evaluated once. Reuse during the subsequent
corruption controls is reuse of these same freshly computed cell values;
it is not reuse of the historical candidate's arithmetic or a cross-run cache.

The source-level argument establishes that successful verification of a fixed
forest is independent of discovery heuristics and elapsed-time cutoffs.
Increasing an external CPU or memory allowance changes whether verification
can finish, not which exact result or strict inequality is required. It does
not license changing the tree, mathematical kernel or literal contract. All
75 unchanged protocols retain their node limit10000 and depth limit128; the
largest selected saved forest has9620 nodes. An interrupted or killed run has
not verified a partial mathematical substitute for the full forest.

## Algebra actually traced, and its limits

For the representative closure, the review traced
`rho_signed_moment_tightener.py` (SHA-256
`1fe8fefd93269e478be47077b3bf1c8d0cff9259de94824d55a66824b8052cdc`),
`exact35_core.py` (SHA-256
`512c70ead43294a7f1d4e14922c9c3a55d3928c9555f4af1415cacf5ad6657bb`),
and `RIGHT_HALF_COUNT_PROOF.txt` (SHA-256
`a73a4f6abf8796e6e20ab161922f33a075c972953e1f6ee545709c51566a355b`).
The paths have the same capsule prefix as the representative protocol.

The traced wrapper uses the literal probability orientation on both sides of
one half. In particular, for `v=p(1-p)` and `s=lambda/n`, it uses
`beta=[v(1-2p)+s(2alpha-1)]/(v+s)` and
`mean=v/sqrt(v+s)`. The variance lower bounds, acquired beta/mean exclusions
and beta-to-alpha contraction are necessary conditions in this orientation.
The source uses strict disjointness for exclusion, retaining equality points.
Its rho variance-floor proof uses convexity of `(v+s)^(3/2)` and positive
denominator gates; a nonpositive preliminary lower bound yields no floor.
The right-half text's binomial mass/CDF extrema use literal `p` and `k`, and
do not silently reflect `p`, the count or signed beta.

The traced core combines outward rational interval bounds, optional necessary
resource/variance/support restrictions, Gaussian/binomial bounds and bounds
on the own-count conditional probability. Its concluding form subtracts an
own-count loss and bounds the remaining difference by the minimum of two
independently valid upper bounds. The positive multiplier uses an upper bound
for `sqrt(n)` divided by a positive lower bound for rho. Optional sharp lower
bounds are used for exclusion only when their hypotheses hold and their
comparison is strict. A failed optional hypothesis falls back to a weaker
bound rather than declaring an empty cell.

Some elementary signs and coverage implications above were independently
checked algebraically. This is **not** a complete independent proof of all
kernel variants used by the 75 jobs. The selected B1/B2 refinements also use
joint cubic, quartic/SOS, fixed-peak, tangent-MGF and alpha/stop-loss bounds.
Their frozen source/proof files, including `GENERAL_QUARTIC_SOS_PROOF.txt`,
`FIXED_PEAK_QUARTIC_PROOF.txt`, `TANGENT_MGF_PROOF_V1.txt`,
`COUPLED_ALPHA_STOPLOSS_PROOF.txt`, `THETA_VARIANCE_PROOF.txt` and
`ALLOCATION_VARIANCE_PROOF_v2.txt`, are exact identities in the catalog's
per-job source maps. Each enabled inequality and its implementation link
requires a separate soundness argument. Source identity ensures that the
executed function is the reviewed function; it cannot replace that argument.
No concrete sign error or counterexample was established by this bounded
review, and an unfinished independent verification is not such a discovery.

## Required fresh execution evidence

The unchanged native status is `PASS_FRESH_CONDITIONAL_EXACT_COUNTINDEX`.
Its exact receipt fields are `status`, `forest_sha256`, `contract_sha256`,
`checker_sha256`, `kernel_sha256`, `statistics`, `negative_controls`,
`fresh_leaf_evaluations`, `seconds` and `scope`. Statistics bind `nodes`,
`leaves`, `closed_statuses`, `maximum_score` and `maximum_depth`.
`fresh_leaf_evaluations` must equal the complete selected leaf census.
Every actual source/kernel/forest hash, full terminal JSON capture, empty
stderr hash and completed native guard/launch chain must be checked against
the new execution, not copied from a historical accepted receipt.

The controls have this exact order: wrong n; boolean n; wrong index; boolean
index; wrong target; wrong contract; missing kernel source; wrong checker;
missing count; reordered counts; wrong count; boolean count; missing child;
invalid axis; boolean axis; outside cut; nontext cut; changed leaf box; false
decision; false leaf arithmetic; missing result; unknown node; extra success
claim; extra leaf claim. AST comparison found the `accept` bodies identical
across the 75 jobs after replacing only literal `COUNT`-index strings. Split
controls additionally require the intended structural rejection before any
synthetic children can be treated as arithmetic evidence.

## Remaining acquisitions and the next falsifiable composition check

Fresh all75 replay would acquire conditional fixed-contract count arithmetic.
It would leave the B0/B1/B2 INITIAL/global-resource acquisitions, the two local
16-covers, exact outward resource-to-contract mappings, uncounted panel
exclusions, and their closed-domain union to be acquired and composed. The
literal contracts retain a stronger24 predecessor/contact allowance; the
same-law attainment/contact/localization and physical count interpretation
must apply to the very same witness. Stored checked/interface/source-review
JSON in a kernel manifest is an explicit premise or source artifact until its
underlying acquisition has been independently established.

The next concrete composition check is to reconstruct each selected contract
from the relevant freshly accepted resource object, including every signed
quadratic plane, endpoint floor, beta/mean/theta bound, rho cap and exact closed
p subdomain, then prove that a physical witness satisfying that resource
object lies in the original root family. A mismatch in any literal outward
rounding or domain endpoint falsifies that interface before the counts can
be joined. The historical selection/composer sources
`new_audit/compose_low_b0_complete_v3.py` and
`new_audit/compose_lower25_complete_v1.py` identify the original dependencies;
their receipt pins must not be replaced by invented fresh receipts. A new
semantic join must bind actual fresh objects and verify their implications.

All parent-acquisition, complete-n25 and all-index conclusions remain open in
this note. No execution label or source hash is promoted to those conclusions.
