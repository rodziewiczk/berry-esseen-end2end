# Analytic audit and remaining proof obligations

Audit date: 2026-10-23, Europe/Warsaw.

This is a record of a limited read-only mathematical and source audit. It is not a native acceptance, a full referee review, a literature verification, or a proof of the sharp constant. No heavy mathematical job was run for this audit. Every obligation in `obligations.json` remains open in the clean reproduction epoch.

## Target and normalization

For a standardized real law P with E X = 0, E X² = 1 and rho = E|X|³ < infinity, the target uses

    C_n = sup_P [sqrt(n)/rho] sup_H |P(S_n <= H) - Phi(H/sqrt(n))|,
    C* = sup_{n >= 1} C_n,
    C_E = (3 + sqrt(10)) / (6 sqrt(2 pi)).

The desired conclusion is C_n <= C_E for every positive integer n, together with Esseen's lower bound C* >= C_E. A bounded-law result, a reference-law result, selected count panels, and an eventual tail each have a smaller scope.

## Material actually read

The audit read the supplied v4 TeX and, later, the corresponding current workspace draft:

- `manuscript/drafts/appendix_elementary_045.tex`;
- the C4 source closure under the publication repository's `moment-defects/code/n4/research/all_n/`, particularly:
  - `finite4_contact_derivation_2026_10_09.py`;
  - `n4_elementary_gaussian_1_15_owner_radius_101_25_2026_10_09.py`;
  - `n4_complete_root_all_law_reduction_2026_10_09.py`;
  - `n4_first_critical_physical_quadrature_bridge_2026_10_08.md`;
  - `n4_local_physical_moment_quadrature_2026_10_09.py`;
  - `n4_frequency_local_physical_H_curvature_2026_10_09.py`;
  - selected parts of `n4_cpu_time_entire_root_2026_10_09.py`;
- `moment-defects/reproduction/all_indices/coverage.py`, `finite.py`, and the entry point `moment-defects/reproduce.py`;
- the user handoff dated 2026-10-23;
- selected streams from the historical `cutoff6_20261020.zip`, including its final composer, preflight, composition argument and one native count capsule.

The old workspace and historical publication commit identify provenance. They are not runtime dependencies of this new repository and do not supply fresh acceptances. The full 79-file C4 source closure was not independently reviewed line by line.

## C4 finding

No confirmed missing analytic implication was found in the reviewed current chain

    all-law C3 bound
      -> unrestricted C4 attainment and contact
      -> support and moment localization
      -> original-law physical Prawitz / midpoint / threshold bridge
      -> COMPLETE_ROOT(U)
      -> C4 <= max(256/625, U).

The numerical premise COMPLETE_ROOT(U) remains open. The exact imported Prawitz theorem and the implementation-to-lemma correspondence also remain to be verified. The finding is therefore narrower than a statement that the complete proof is correct.

The canonical three-point Q is a reference determined by P's tagged first two moments. The reviewed C4 statements allow arbitrary bounded P, including infinitely many support points and an atom at zero. They do not assume P itself has three atoms.

### Attainment and full-support contact

Current draft lines 5571-5667 use the common attainment/contact arguments to obtain a positive CLOSED-CDF maximizing pair when C4 > 256/625.

The reviewed points are:

- bounded third moments in a maximizing sequence preserve the first two moments through weak convergence;
- third-moment convergence is concluded from extremality, rather than assumed as uniform integrability;
- the contamination keeps the raw threshold fixed and standardizes the actual contaminated law;
- differentiating the central third moment needs an integrable second-moment majorant;
- the contact function is nonpositive everywhere;
- integration gives zero almost surely, and upper semicontinuity extends equality to the full closed support, including accumulation points.

Reflection must retain atoms. The applicable identity uses a strict left limit:

    Phi(x) - F_Z(x) <= Phi(x) - F_Z(x-)
                    = F_{-Z}(-x) - Phi(-x).

A reflected CLOSED CDF is not the naive complement of the original CLOSED CDF at an atom.

### Localization

The current draft derives the moment cap from the published Shevtsova envelope before invoking bounded support or fourth moments.

The elementary Gaussian bound checked in the review is

    |H4(z,y)| < phi(0)|y|³/6 + |y|/5 + 1/15.

The argument uses a uniform scale second-derivative bound 4/15, a second-order translation remainder, and the exact cancellation of the scale and translation terms.

The contact bracket is first shown negative on |y| >= 4. Only after that sign proof is the lower score C > 256/625 substituted in an upper estimate. The resulting cubic and its first three derivatives are negative at 101/25. This excludes the whole two support rays and gives

    |X| < 101/25 < 17/4,
    rho < 46/25,
    625/2116 < w <= 1,
    |E[X|X|]| < 321/500 < 13/20.

These bounds place the same unrestricted maximizer in the full closed class accepted by ROOT4. The finite scalar checks of this cubic are useful checks of arithmetic; they do not establish attainment or contact by execution.

### Common physical defect

For the canonical reference contacts a,b, the reviewed identities use

    W = X_+(X_+-b)² + X_-(X_--a)²,
    eta = E W = rho(P) - rho(Q) >= 0.

At eta = 0 the law is Q; no division by eta is needed. For eta > 0, one measure nu = W dP / eta is retained at every frequency. The budget formulas correctly account for omitted mass at the contact points and for P{0}. This preserves the required cancellation between frequencies.

The complete response-series, whole-geometry correction, priced-supremum and fourth-power portfolios still require a full implementation audit. This review did not independently certify every disk/lens maximization and every selected portfolio branch.

### Physical Prawitz and midpoint reserve

Current draft lines 5801-5883 apply the one-sided majorant to the original physical law P, with Z = S4/2. For D = x-Z, the real regular integrand is

    F_x(u) = (1-u) E cos(6Du) + S(u) E[6D sinc(6Du)].

The reviewed derivative bound is

    |F_x''(u)| <= 42 E|D| + 108 E D² + 24 E|D|³.

The coefficients follow from the product rule, the sinc integral representation, and the stated bounds for S,S',S''. Support supplies the necessary fourth moment. Thus composite midpoint quadrature charges the raw numerator once:

    Q_H <= M_H / (12 N²).

The uniform version is 687/(8 N²). Local moment and uniform reserves may be intersected as two independently valid complete bounds. A separate reference, transfer and nonlinear-remainder quadrature reserve must not be added or silently removed.

The old bridge note has historical C4 >= C_E / He-Cheng headers. The reviewed physical moment, Prawitz, midpoint and threshold calculations themselves require only |X| <= 17/4 and rho < 46/25. The newer localization supplies these already for C4 > 256/625, so those historical headers do not by themselves create a new gap in the current implication.

### Threshold interpolation and tails

Current draft lines 5885-5928 interpolate the smooth physical majorant, rather than the discontinuous CDF or a minimum of computed bounds.

Whole continuous frequency cells are filled using E|X| <= 1. If B bounds |J_P''|, the raw-threshold reserve is

    E_H = h² (B + 1/4) / 16.

The factor includes the change x = H/2 and the factor two in the raw numerator. The threshold tails H <= -4 and H >= 25/8 have positive normalized score at most 2/5. Both actual reflected orientations remain necessary.

### The remaining C4 certificate

Current draft lines 6089-6167 state a conditional bounded-law implication. It requires:

- all 260 closed geometry parents;
- the complete parent or all-four-children route;
- all selected high-excess requests, 1300 slots in the original root protocol;
- all low-excess cells, including eta = 0 and their shared endpoints;
- all 58 central threshold nodes and 57 interpolation joins;
- both reflected orientations and both threshold tails;
- original-law normalization rho = rho_Q + eta.

The native adapter in `reproduction/all_indices/finite.py`, lines 104-134, requires two complete passes, `--produce` then `--replay-existing`, zero unresolved classes and the original target U <= 4097/10000. A replay through the same exact kernel is an independent recomputation in time, not a second independent numerical implementation.

A genuinely verified COMPLETE_ROOT(U) gives C4 <= max(256/625,U). Therefore a valid complete U above 4097/10000 but below C_E could still prove the sharp C4 inequality. It must receive an explicit reviewed composition; a failed target label may not simply be relabeled PASS.

The next falsifiable C4 target is a full fresh COMPLETE_ROOT(U), with the original two-pass protocol and all required domains. A missing class, unresolved HIGH request, failed exact inequality or incomplete native execution leaves this target open. No heavy C4 run was performed for this audit.

## Other common interface checks

The reviewed v4 interfaces distinguish an analytic schema from its finite certificates:

- support is acquired before higher moments are used;
- a LOW alternative is one whole triple; coordinatewise minima of triples are not justified;
- complete HIGH alternatives retain every frequency interval and infinite tail;
- Gaussian weight removal starts only after its required first raw pass;
- nD <= Nd and D <= d are different facts;
- a signed phase corner must be dominated on the full consumed phase interval;
- all n+1 original count roots and original five-dimensional boxes must remain covered;
- strict outgoing and closed incoming events retain the proper atoms;
- common cubic moments, noise allocation, marginal orientation and phase remain coupled;
- exact inward endpoints must not be replaced by arbitrary loose support caps inside identities;
- an unproved convergence or fixed point of resource iteration is not a certificate.

The current source text supplies mathematical rules for these checks. It does not itself show that every required source-specific instance has passed.

## Literature still unverified by this audit

No original external theorem was independently verified against its primary publication during this audit. The clean proof manifest therefore leaves all literature nodes open.

| Input | Required verification |
| --- | --- |
| Bentkus-Kirsa 1989 | Exact n=1 statement, normalization and unrestricted scope. |
| Esseen 1956 | The lower-bound construction and its equality with the manuscript's C_E. |
| Prawitz 1972 | Displayed complex kernel, Fourier convention, one-sided CLOSED-CDF majorant, frequency scaling and atoms. The manuscript imports the majorant itself. |
| Shevtsova 2012/2013/2014 | Each selected smoothing/envelope/moment theorem, exact constants, iid hypotheses and permitted moment range. Attribute the known sharp third-moment inequality correctly. |
| Schulz 2016 | The required all-n, all-p binomial comparison and discrepancy conventions. |
| He-Cheng 2026 | Only the specifically selected finite Gaussian estimate and its domain. No all-index or eventual-exactness result is accepted by association. |

The reviewed elementary C4 contact/Gaussian localization has its own argument; it does not require importing He-Cheng contact or an all-index conclusion.

## Global graph and execution boundary

The older `coverage.py` declares 45 nodes. Its n4 node depends on n3 but compresses localization, physical bridging and root arithmetic into one entry. Its `computational_scope(records)` accepts caller-supplied `fresh_arithmetic=True` records; that helper is not an executing validator of theorem domains, source captures or analytic edges.

The older `reproduce.py` registers eight component adapters and three explicitly arithmetic-only C5 substeps. Its `--all` fails closed and does not yet execute a complete proof. These are appropriate limitations. Tests of topology, source identity and adapter schemas do not close mathematical nodes.

The new `obligations.json` exposes the C4 analytic and arithmetic pieces separately, C5 acquisition joins separately from arithmetic, and each literal index 6-30 explicitly. It also records the seven pending n25 jobs, the incomplete 31-48 bridge, the full original BE49 requirement of 14 top-level executions / 41 retained components, and the uniform least-failure interface.

A conditional arithmetic job can run in parallel before its mathematical parents are discharged. Its final unrestricted conclusion cannot be composed until those parents and the exact same-law joins are proved.

## Historical data and the new epoch

Historical PASS files are candidate provenance, never fresh proof in this epoch.

The audited old cutoff6 final composer recorded 284 count forests, 2362 roots, 257089 leaves and 1200 probability panels at literal n=6,7,8,9. Its final numerical-oracle count was zero: it joined stored acceptances and reconstructed geometry. Selected native count capsules do contain true leaf-replay code, but that does not mean their replay has run here.

The cutoff6 archive did not contain its referenced earlier cutoff6_20261018 / cutoff10 / cutoff15 / cutoff20 source closures. Its final graph contained many such hash references. Hash references are not supplied dependencies, nor a fresh replay of n10-30 or the tail.

The handoff's previous n2, n3, C5 and CI results remain provenance. Timeouts, memory stops and orchestration errors remain incomplete executions. The seven n25 jobs are five original V12 cases and two new conditional V14 source epochs; search hints and checkpoints are untrusted candidate state until complete native acceptance.

## Acceptance in the clean repository

No component or analytic edge has been marked completed here. Closing a node requires the exact selected domain and target, source pins, a fresh native result when applicable, all required native controls, observed execution and an explicit mathematical join. All heavy execution belongs in the user's Colab sessions.

Colab compatibility is a separate open execution requirement. Some historical entry points enforce Windows resource guards. This audit did not test a Colab runtime or approve removal of those guards. A compatible runtime or an explicitly audited mathematics-preserving port must retain process-tree supervision, exact source identities and the original acceptance obligations.

A final proof requires both complete arithmetic and complete mathematical implications. Neither a new wrapper nor a single global success Boolean can replace either part.
