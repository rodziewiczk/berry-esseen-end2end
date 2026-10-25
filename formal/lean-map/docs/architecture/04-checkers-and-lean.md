# Checkers, trust profiles and Lean integration

Status: implementation specification. The existing Lean modules provide a
compiled **conditional mathematical composition**. This architecture does
not convert a JSON result, a native PASS string or a successful build into an
unconditional Lean proof of the numerical inequalities.

## 1. Authority and the four checks

A producer searches for or replays candidate data. An independently invoked
verifier checks those data. A coverage assembler checks complete statements,
scopes and dependencies. A Lean bridge checks the declared correspondence
with the conditional theorem and its parameters. These are distinct roles.

The verifier pipeline is ordered:

1. **Decode:** enforce the codec, exact versioned schemas, primitive semantic
   invariants, byte digests, lengths and bounded resource limits. Reject
   unknown fields, unsupported kernels and noncanonical rational aliases.
2. **Bind:** load the frozen mathematical statement, source/analytic rules,
   context, scope and exact prerequisite claims. Verify the certificate's
   complete identities and the approved checker/profile/issuer policy.
3. **Check:** execute the named source-bound replay or trace checker with
   whole-domain gates, exact arithmetic/outward bounds and complete geometry.
   An unsupported branch is not EMPTY. A failed numerical check is not a
   resource-acquisition result.
4. **Assemble:** emit authenticated conditional claims, then check their
   use by the exact cover/rule and final obligation manifest. Preserve all
   unresolved analytic or external numerical assumptions in the report.

Schema validation and source/provenance validation stop before step3. They
cannot establish that a bound is true. Cached verifier acceptance is reusable
only under the same verification key or an explicitly approved compatibility
rule; the existence of an artifact under a digest is not acceptance.

## 2. Trust profiles are pinned policies, not a label ladder

`TrustProfile` binds its accepted analytic bundle, numerical backend,
checker/environment manifests, dependency policy, Lean contracts and scope
policy. All profiles at this milestone retain explicit accepted analytic
inputs. Three backend roles are distinguished:

| Backend | Numerical trust boundary | Permitted report |
|---|---|---|
| `trusted_source_replay` | The approved source-bound evaluator, adapter and its exact dependency/runtime stack are trusted to establish the specified meaning | Conditional composition with trusted external numerical meanings |
| `self_trace_external_checker` | A producer supplies a self-contained trace; a separately approved smaller external checker validates arithmetic and scope | Conditional composition with that external trace checker in the trusted base |
| `lean_kernel_trace` | A sound Lean decoder/checker and kernel-checked proof term establish the exact numeric meaning | Kernel-checked numerical trace, still conditional on the named analytic inputs |

These are format/capability slots, not claims that all backends are implemented.
In particular, this branch does not ship a verified Lean trace evaluator.
Selecting that backend before its approved decoder/checker exists returns
`unsupported_trace_profile`. It must never fall back to trusted replay while
retaining the stronger profile ID.

There is no implicit ordering of profiles by their names or digest values.
The approved dependency policy explicitly lists compatible profiles and
meaning-preserving transfers. Changing the profile/checker digest cannot
upgrade an old receipt. The actual registered build, environment and issuer
authorization must match; an untrusted worker cannot self-assert a stronger
checker or reuse a signed weaker result under another key.

Producers may upload candidates; they cannot publish trusted verification
receipts or mark mathematical obligations covered. The authority validates
the authenticated verifier identity and configured checker manifest, records
the exact request and seals its receipt. A detached seal authenticates its
issuer and exact bytes; it does not remove the numerical/analytic trust
assumptions. Offline unsealed receipts require re-verification or an explicit
separately authorized trust decision.

## 3. Fixed semantic ports

The implementation uses typed ports with explicit failure variants:

```
decode(family_schema, bytes) -> FrozenPayload | DecodeFailure
bind(statement, payload, prerequisites, policy) -> BoundTask | BindingFailure
verify(BoundTask, checker_manifest) -> VerificationReceipt
assemble(manifest, accepted_receipts, covers, policy) -> AssemblyResult
bridge(AssemblyResult, lean_contracts) -> LeanBridgeReport
```

`BindingFailure` includes wrong statement/scope/source epoch, missing exact
dependency, unbound local arithmetic problem, wrong normalization/index or
unapproved profile. Numeric failure includes incorrect outward enclosure,
unproved strictness, invalid strategy gates and incomplete covers. Resource
exhaustion returns `inconclusive`; unimplemented families/rules return
`unsupported`. None supplies a mathematical premise.

The principal numerical meaning remains universal:

```
for every unknown law X, actual index, raw threshold and realized point
satisfying the frozen context and selected closed scope,
the claimed bound/export/comparison holds.
```

The law, its actual integrals and `ContactAt` are proof quantifiers. They are
not runtime job input and are not approximated by a supplied sample law.

The generic COUNT score is the signed positive closed discrepancy

```
sqrt(n)/rho(X) * (CDF_(X^*n)(H)-Phi(H/sqrt(n))).
```

It is not an absolute Kolmogorov score at an arbitrary point. The ordinary
attained-contact adapter separately supplies equality with that owner's
normalized score. AB24 uses the general signed point meaning and never
fabricates an attained/optimal contact at24.

The positive-noise local comparison claim is exactly
`rho_B(p)*(score_n(X)-ownBernoulliScore_n(p,k,delta)) < -epsilon*lambda`,
where `lambda=n*noiseVariance(X)>0` and the nearest count/phase belong to
that same law and raw threshold. The claim schema pins both the rho_B
factor and negative sign. `zero_noise_bernoulli` is a different claim: the
same law is Bernoulli and its whole score is strictly below C_E. At lambda=0
the positive-noise strict comparison is not applied.

## 4. Family dispatch and required certificate content

Every enabled `(family_kernel_id, family_schema_digest, source_epoch)` has
exactly one registered decoder/checker and one semantic port. Its immutable
parameter capsule is referenced by the Statement and validated against that
family schema. Hashing an opaque capsule without an approved family decoder
returns unsupported; it is not a generic proof method.

The common schemas provide transport, COUNT contexts/trees and the Farkas
trace slice. Other families retain their existing precise Lean/mathematical
contracts; their production parameter/trace decoders must be registered
before enabling them. The table below is the required content contract,
not permission to replace a family by an unexplained final scalar bound.

| Family / semantic port | Frozen inputs and certificate obligation |
|---|---|
| Ordinary COUNT -> `CountCertificateMeaning` | Full CountContext; all n+1 original root products; complete closed binary trees; ordered leaf entries; exact rule witnesses and target relation transfer |
| General quantitative COUNT -> `QuantitativeCountMeaning` | Same general-law realization without extremality; whole-root/window coverage; actual returned upper U dominating every score leaf; U may exceed search target |
| Count5 ancestor -> `ScopedCountMeaning` | Exact original ancestor/root5 and whole-cfg identity; complete closed subtree; no promotion to all roots/phases/panels |
| AB24 -> `ABGeneralCountPort` / empty-central port | Same-law24 transfer, fresh phase/all 25 roots, exact requested closed halfline/window clip, quantitative U, both exterior tails; correct lambda/joint intercept/noise-price scaling |
| n2 tensor -> `TensorCertificate2` meaning | SUM majorant on the specified cube, exact 15 feature-pair controls, canonical scalar/moment domain, all derived thresholds and tails |
| n3 null polynomial -> `NullCertificate3` meaning | Distinct-permutation AVERAGE majorant,59 triple/null controls, cube[-7,7]^3 enclosing acquired support6, rho<=15/8 plus separate large-rho complement |
| ROOT4 -> `Root4Provider` source class | Correct canonical Q3/excess-eta owner, its source localization/support/own caps, exact weak score cap. It is not generic physicalD COUNT |
| Prawitz -> four-term score evidence | c/tau/index gates, all four smoothing terms including endpoint pieces and infinite normal tail, integrability and outward integral bounds |
| LOW -> coherent `LowBound` | One complete constant/threshold/secondary triple from an enabled source family; actual moments/phase; whole-cell gates and integrability |
| Complete HIGH -> `HighBound` | Complete selected finite pieces plus infinite/compensation tails with their source gates; actual n/floor and n*theta/lambda units; theta=0 handled explicitly |
| Resource barrier -> `BarrierResourceMeaning` | Exact K/R/own/index row; all closed moment cells; chronological strict rawR and nD<N*d exports; coherent LOW/HIGH; warm-start gates and separate negative-D terminal |
| Mixed E / chord | Same-law physical frame; own closed p/lambda/alpha or compatible inward cells; necessary ratio/chord inequalities and all derivative/path gates; output rho ceiling, not a final COUNT score |
| Mixed C/F/D/AB registry | Source/cfg identity; containment in one acquired scope; phase-free versus full5D distinctions; finite earlier licenses; complete admitted manifest and used subset separately |
| Uniform tail acquisition | All six support index bands including200..infinity;83 probability rows; source-bound entry/resource/confinement licenses with actual same-law moments, phase, support and coupled resources |
| Uniform local comparison | Complete TINY/MID/LOW positive-noise cells, nearest or whole-count witnesses with full gates, rho_B(C-C_B)<-epsilon*lambda; separate zero-noise Bernoulli input |
| Analytic export | Exact named source statement/version and complete scope; authorization from the accepted analytic bundle, not a numeric PASS or arbitrary predicate |
| Final assembly | Exact expected top theorem and obligation manifest, all required accepted claims/covers/dependencies, source/contract/Lean bindings and declared residual assumptions |

The implementation does not infer old source rule semantics from similarly
named helpers. A finite P46 certificate ending at98 is not a uniform all-n
resource certificate; n=24 transfer is not probability panel p24; ROOT4 eta
is neither physicalD nor the older matching-moment defect.

## 5. Ordinary selected COUNT rule catalogue

The selected ordinary final-verifier branches are frozen in
[COUNT-RULES.md](../contracts/COUNT-RULES.md). Required witness content is:

| Tag | Required check |
|---|---|
| EMPTY_PHASE | Positive normalization denominator; outward H enclosure over the whole original box; strict disjointness of closed raw-threshold intervals |
| EMPTY_ACQUIRED_THETA_VARIANCE | Exact theta/lambda bridge, correct v maximum,0<=theta<1, positive division; lambda lower endpoint strictly above the necessary upper cap |
| EMPTY_SHARP_BOX | Actual endpoint/conditional-variance bounds, all coefficient gates, zero-endpoint branch, polynomial lower witness and outward denominator; sharp D lower bound strictly above available D cap |
| EMPTY_JOINT_CUBICS | Complete same-law cubic rectangle/strip and licensed optional D plane, with every source derivation; bound Farkas infeasibility or complete degenerate-safe bounded-polytope enumeration |
| EMPTY_RHO_UPPER | Exact clipped conditional-cubic maxima and coefficient sign choices, positive denominator; derived rho upper strictly below acquired rho lower |
| EMPTY_ACQUIRED_RHO_VARIANCE | Source tangent/monotonicity gates, four M corners, signs of A/B and nonnegative noise; exact strict comparison or valid preserving contraction |
| scoreUpper / PASS_TARGET | Source count identity and every required probability/stop-loss/quartic/Gaussian bound; coherent whole combined expression or valid direct probability envelope; upward normalized score cap |

Other historical tags, source branches and new local-comparison witnesses
need their own registered rule contracts. They cannot be decoded as a generic
`infeasible` leaf. In particular, a failed positivity/derivative gate means
omission/fallback or unsupported, not EMPTY. Equality at a strict comparison
survives. Independent strategy **whole bounds** may be minimized; incompatible
partial coefficients/common-law cubic choices may not be combined.

## 6. Farkas trace binding, not just arithmetic

For a rational system A*x<=b, a portable contradiction is a rational vector
y>=0 with y^T*A=0 and y^T*b<0. The checker performs all operations exactly
and checks dimensions, signs and strict negativity.

That computation is valid only after binding the exact ordered system to
the frozen statement/scope and source derivation. Reconstruct every required
support rectangle and same-rho strip; include an optional D half-plane only
when its gates were proved. Hash the canonical generated problem and compare
the trace's problem reference with that expected problem. The producer may
not substitute an unrelated inconsistent system or choose its own source
plane interpretation.

The illustrative fixture uses x<=0 and -x<=-1 with weights1,1. Its arithmetic
contradiction is correct. It is rejected as `unbound_farkas_problem` because
that system is not the statement's expected derived system. A vertex-list
alternative additionally proves boundedness/completeness and retains feasible
segments/points; an empty list alone is insufficient.

## 7. Quantitative outputs, target failures and cache

For ordinary target-checked COUNT, the certificate proves the requested
relation at the frozen target, including correct strict/closed transfer.
For quantitative AB24, the certificate instead proves its returned U. Missing
the producer early-exit target is not mathematical invalidity. The halfline
adapter computes its actual q_R from U and includes both exterior tails.

The transport CountContext omits an output target because the typed Statement
owns the required bound. The ordinary Lean adapter sets `target` and relation
from that statement. A general quantitative adapter uses the designated
erased target metadata value1/1, relation le, in the current Lean
`CountTaskContext`: `CountBoundCertificateMeaning` does not consume that field.
The bridge must prove this exact projection preserves the general meaning;
it does not copy a native search target into a mathematical assumption.

Cache rules follow the verification key. A certificate can be valid with a
larger quantitative U and still fail a separate downstream required cap.
Neither outcome overwrites the valid numerical claim. A changed analytic
bundle, context/scope, checker/environment, trust policy or prerequisite
receipt requires its own verification key. A cache hit may save replay only
when the authority already holds the exact permitted acceptance and seal.

## 8. Lean bridge: the actual story

The existing declarations include `CountCertificateMeaning`,
`GeneralCountRealization`, `ScopedCountMeaning`, `Root4Provider`,
`UniformLocalProvider`, `TailMethodProviders.contracts` and
`sharp_from_typed_providers`. They describe precise Props/typed providers.
A runtime receipt has no constructor that turns a Boolean into these Props.

The specified bridge produces a `LeanBridgeReport` binding every theorem
parameter to an exact statement/claim/scope, realization mapping, analytic
version and authorized receipt. Its three parameter roles are:

* an accepted analytic theorem parameter, with its complete source scope;
* a trusted external numerical meaning parameter, checked under the chosen
  external profile and explicitly retained as an assumption in Lean;
* an actual kernel-checked numerical proof term, only when a verified
  decoder/checker and corresponding proof construction exist.

The first delivery may compile a generated conditional theorem with numerical
meanings as explicit parameters. It must report that status as conditional
composition with external numeric meanings. There are no `sorry`/new axioms,
`of_decide_eq_true` applied to an unproved external function, unsafe native
evaluation pretending to be a kernel proof, or an axiom per receipt disguised
as a certificate import. The exact source theorem and proof-parameter list
remain reviewable.

The future stronger route is a proved decoder plus a proved Lean arithmetic
checker soundness theorem, so a checked trace yields the exact Meaning Prop.
The theorem then constructs the corresponding providers and uses the existing
assembly. Even that route retains the explicitly accepted analytic parameters
unless they are separately proved. Selecting a profile is never a claim that
this later implementation already exists.

Compiling all 29 mathematical modules checks the skeleton/type composition.
It does not discharge its external inputs. The bridge's build status and
claim level are separate fields; no build success alone gives full proof PASS.

## 9. Exact full-proof PASS predicate

One `be run project.toml --resume` plans and executes the entire requested
proof, with cached accepted artifacts reused and independent jobs scheduled
in parallel under the fixed resource/budget policy. It prints final PASS and
establishes mathematical PASS only when **all** of these conditions hold:

1. The frozen project selects the exact top statement: all-positive-index
   iid upper bound, or sharp global constant equality. The sharp request also
   requires the separate lower-approximation input; upper-bound coverage alone
   does not satisfy it.
2. Every mandatory mathematical obligation has a matching accepted claim
   under the requested authorized trust/dependency policy. Finite 1..48,
   independent 49+, constants, attainment/analytic interfaces and the requested
   lower-bound path are complete. Source-required admitted mixed statements
   remain required even when not selected by a final leaf.
3. Every parent cover/composition has been checked against the original
   domain, all seams/tails/index ranges and exact child claims. No missing,
   unsupported, stale, conflicting, unsealed or partial-scope receipt is used.
4. A final `FinalAssemblyPayload` names the exact top claim, complete
   obligation/coverage manifests, actual dependency receipts and a matching
   LeanBridgeReport. The assembler independently computes zero unresolved
   obligations; it does not trust a producer's empty list.
5. The authorized final verification receipt accepts that exact final
   assembly under the requested profile and source/contract snapshot. Its
   report states the conditional analytic/numerical trust assumptions and
   does not claim a stronger Lean proof level than was built.

A completed VM, runtime-produced verification job, empty queue, cache hit,
all local COUNT leaves passing, or a green interface build cannot substitute
for this predicate. Otherwise the CLI emits NO_PASS with typed unresolved,
unsupported, rejection, stop or infrastructure reasons. It may report a valid
partial numerical upper separately without marking the entire proof complete.

Compute shutdown is a distinct operational obligation. Normal full PASS
initiates the same owned-resource shutdown/reconciliation path; a mathematical
acceptance does not assert that chargeable resources stopped. The top-level
report separately shows mathematical assembly and shutdown/remaining-liability
status. Expired/cancelled lease or campaign state cannot be overridden by a
late successful worker. Cloud billing alerts are not a proof or a hard cap.

Exit 0 additionally requires successful operational closure/reconciliation.
If mathematical PASS has already been accepted but cleanup fails, preserve
that immutable mathematical result, report the operational failure and
return exit 5. Never rewrite the accepted proof receipt as a mathematical
rejection to hide a cleanup problem.

## 10. What is deliberately not claimed as delivered code

This branch supplies typed architecture, closed structural schemas,
illustrative fixtures and the previously compiled mathematical contracts.
It does not ship a production runner, cloud resources, approved family
replay containers, a complete self-contained trace language for every
numerical strategy, or the Lean numeric decoder/checker proof. Unsupported
portfolios remain explicit before paid execution. The first implementation
must register one audited vertical slice, prove/test its exact projection and
negative controls, then enable further source-specific families without
changing these mathematical meanings.

## 11. Closed LeanBridgeReport and AssemblyResult records

The files `lean-bridge-report.schema.json`, `final-assembly-payload.schema.json`
and `assembly-result.schema.json` are closed records, not untyped report blobs.
The report contains exact contract-source/toolchain manifests and one allowed
target declaration: `BEMap.sharp_from_typed_providers`,
`BEMap.all_indices_from_typed_providers` or `BEMap.universal_iid_inequality`.
The selected declaration must match the frozen project's requested theorem;
listing an allowed name is not itself evidence that its premises are filled.

Each unique parameter binding supplies the Lean parameter/Meaning declaration,
statement/claim/scope digests, exact receipt, full source pin, realization
mapping artifact and one of the three proof roles from section8. Bindings
are sorted by parameter name. The bridge compares them against the exact
required parameter inventory, not a producer-provided subset. Missing or
duplicate mappings are explicit unresolved_mappings. Build status
(`not_run`, `interface_build_passed`, `proof_term_build_passed`, `build_failed`)
is distinct from the report's conditional claim level. Residual assumptions
are listed explicitly and checked against the authorized analytic/external
meaning policy; an unapproved assumption is unresolved rather than hidden
behind a successful build.

FinalAssemblyPayload binds project plan, top statement/claim, trust profile,
complete obligation/coverage manifests, actual dependency receipts, Lean
sources/report and unresolved-obligation list. AssemblyResult records the
requested theorem, mathematical verdict, accepted final receipt/payload or
their absence, independently computed unresolved set, operational status,
shutdown receipt and process exit code. An accepted final result requires
the complete predicate in section9; it cannot be produced from a partial
forest or an arbitrary top claim reference.

For one verification key, non-definitive metadata/unsupported/inconclusive
observations carry no claims and remain retryable. The first authorized
definitive receipt is the stable dependency anchor. Identical semantic replay
records fresh execution evidence without replacing that anchor. An accepted
versus rejected definitive result, or different accepted claim/scope/conclusion
bytes, quarantines the key. Differences only in diagnostics, timestamps or
invocation IDs are not mathematical conflicts.

The exact final status combinations are: mathematical PASS with successful
operational closure -> exit0; mathematical PASS with cleanup failure -> exit 5
while preserving the accepted proof receipt; incomplete/stopped work ->
NO_PASS/exit2; unsupported input/profile -> exit3; mathematical rejection or
definitive conflict -> exit4; other unrecovered infrastructure failure ->
exit 5. The process cannot report exit0 while resources/financial liabilities
remain unreconciled merely because its mathematical receipt was accepted.
