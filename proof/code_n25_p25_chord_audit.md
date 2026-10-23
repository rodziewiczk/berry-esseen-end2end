# n25 lower B5 p25: compatible moments, quadratic chord and finite contact feedback

Date: 24 October 2026. This is a fallible internal AI source and hand-algebra
review, not external independent verification or a machine-checked formal
proof. Other model agents provide internal checks by the same AI system.
No original mathematical module, scalar calculation, contact ray, count
leaf, producer or acceptor was imported or executed. Archived sources and
JSON were read only. There is no fresh arithmetic acceptance here.

## Scope and bounded result

This unit checks the distinct dynamic scalar/derived-native rules in the
selected p25 **coupled-chord ABCDF** forest. It covers the conserved-moment
elimination, continuous closed-law-box extension, quadratic chord and
reciprocal maximum, and the actual finite same-box support/contact caller.
The selected fresh acceptance implementation and its complete-cover
induction are also read. The AB/C/D/F registry consumers are distinguished
from the mathematical acquisition of their theorems.

No concrete algebraic, sign, zero-variance, closed-seam or circular
finite-feedback error was identified in this bounded unit. This is not a
complete p25 theorem: the separate AB/C/D/F acquisition arguments and their
actual applications remain to be reviewed, the selected original native
p25 capsule is not supplied at its canonical path, and no new computation
or final resource/regional composition has been accepted.

The [source map](code_n25_p25_chord_source_map.json) records 16 actual
source/proof members, all matching the historical final source selector,
and five exact contact-helper reuse edges. The helpers are supplied in the
base13 archive and match both the reviewed portable p31 design's actual
file pins and the original selected p25 source-hash references. This proves
an identity of these helper bytes; it neither reconstructs the absent p25
capsule nor establishes its original contract or entire kernel closure.

The selected domain is n=25, K=0, p in [1/4,13/50], rho in [3/2,33/20].
The original same unrestricted attained positive-closed contrary witness,
its stronger24/contact allowance 5/16 and its acquired INITIAL/global
resources remain necessary premises. A smaller dictionary of caps alone
does not establish any new physical bound.

## 1. Compatible cubic moments and the second denominator

Use q=1-p, v=pq, s=lambda/n and h squared=v+s. Put

    b=s*(1-alpha)=q*V0, c=s*alpha=p*V1,
    T=v*(1-2*v)+3*(p*b+q*c),
    l=-q*m0, r=p*m1, t=rho*h^3=T+l+r.

The same physical centered residuals have supports [-O0,a0] and [-a1,O1].
The before-cubic inequality, derived directly from the manuscript in the
[p24 unit](code_n25_p24_pointwise_audit.md), is

    (sigma+1)*t <= D*h^3+G0(a0,a1)+2*r,
    G0(a,z)=2*p*q^2*(1+2*p)
            -6*v*(a+z-a^2-z^2-a*z)+6*b*(a-p)+6*c*z,
    sigma=sqrt(10).

For a centered Y<=a with variance V and a>0, expanding
E[(a-Y)*(Y+V/a)^2]>=0 gives E[Y^3]<=V*(a-V/a). The reflected
lower-support inequality gives the opposite cubic bound. Consequently

    L0(a0)=b^2/(q*a0)-b*a0 <= l <= U0=b*O0-b^2/(q*O0),
    r <= U1=c*O1-c^2/(p*O1).

When a0=0, feasibility forces V0=b=0, and the residual and cubic moment
vanish. This is a physical zero-variance case, not evaluation of 0/0.
All statements hold for atoms and discrete laws.

Using r<=U1 gives the previous (sigma+1) ceiling. A second valid ceiling
comes from substituting r=t-T-l and then using l>=L0:

    (sigma-1)*t <= D*h^3+G0(a0,a1)-2*T-2*L0(a0).

The signs and denominator sigma-1 are therefore necessary. This step does
not choose independent maximizing moments for the two residual laws.
Together with the raw moment bound, the physical rho is bounded by

    min((T+U0+U1)/h^3,
        D/(sigma+1)+(G0+2*U1)/((sigma+1)*h^3),
        D/(sigma-1)+(G0-2*T-2*L0)/((sigma-1)*h^3)).

This elimination is the actual mathematics behind
`root/coupled_third_moment_boxes_v1/box_kernel.py:19-42`, not a theorem
inferred from an archived review label.

## 2. One retained inward coordinate and continuous law boxes

The original direct resource caller supplies caps O0,O1,d, with
a0+a1<=d<1/2. The uniform gates V0_upper<=p_lower*(1-2*d) and
V1_upper<=(1-p_upper)*(1-2*d) imply that G0 is nonincreasing in each
inward coordinate throughout the physical simplex. Lowering a1 to
z=V1/O1 remains valid in both compatible-moment ceilings, but a0 is retained
in its entire necessary interval

    V0/O0 <= a0 <= d-V1/O1.

The implemented enclosure takes the lower endpoint of V0/O0 for the left
endpoint, and d minus the lower endpoint of V1/O1 for the right endpoint
(`box_kernel.py:30-36`). Thus it includes every physical a0 for every
parameter in the original closed p/lambda/alpha box. Strict reversal of
this interval is an exclusion. Equality is retained, as are zero-width
subintervals.

The interval is partitioned into exactly `parts` closed cells, 32 in the
selected caller. The code checks the first and last endpoints and equality
of every adjacent seam. On [A,B], monotonicity makes G0(A,V1/O1) an upper
bound; replacing V1/O1 by its lower endpoint is also an upper bound.
The minimum of their two interval upper enclosures is valid. The retained
comparison points stay below the actual endpoints in the same simplex;
they need not describe a new realizable law.

For B>0 the lower enclosure

    L0 >= b_lower^2/(q_upper*B)-b_upper*B

has the correct directions for its positive reciprocal and negative linear
terms. It also works when A=0 because only B is in its denominator. If
B=0, a0=V0=b=0 is necessary and the code uses L0=0. The raw moment and old
pointwise-defect bounds remain as independent baseline upper bounds. A
failed inward gate keeps those baselines; it does not make the box empty.

For each cell the implementation takes the minimum of valid upper bounds,
and then the maximum across **all** cells. For the actual law, its actual
a0 belongs to a cell, and that cell's minimum still bounds its rho. This is
why the maximum of the cellwise minima is valid; a minimum across cells
would have been insufficient.

The generic `premises()` actually called from
`b5/actual26_pointwise_pilot_v1/application.py:30-47` accepts n>=2 and obtains
it from cfg. Its n26-only `extract()` is not called here and is not being
transferred to n25. This selected call passes n25 and the **original joint
Lambda** as `lambda_domain_upper`. The resource D, gap and noise prices
stay unchanged. The directed outer-cap, inward-budget and conditional
variance arguments are the same inequalities checked in the p24 unit;
the square-root upper is one 10^-15 grid unit above the integer floor, so
it is conservative even when the exact root lies on the grid.

## 3. The quadratic chord and signed reciprocal maximum

The sharper source `root/coupled_chord_v1/kernel.py` retains the dependence
of G0-2*T-2*L0 on a=a0. With z=V1/O1 its numerator is exactly

    C+K*a+Q*a^2-Brec/a,
    C=2*p*q^2*(1+2*p)-6*v*(z-z^2)+6*c*z-6*b*p-2*T,
    K=6*v*(z-1)+8*b, Q=6*v>0, Brec=2*b^2/q>=0.

The coefficient 8*b is 6*b from G0 plus 2*b from -2*L0. Missing the latter
would change the bound. This hand expansion matches source lines 21-23.

On a closed cell [A,Z], a^2<=(A+Z)*a-A*Z. Multiplication by positive Q
preserves the direction. Interval upper bounds for C-Q*A*Z and
K+Q*(A+Z), and a lower bound for Brec, therefore give

    numerator <= constant_upper+U*a-Bmin/a.

Here a>=0 is essential for replacing the linear coefficient by its upper
bound. If Bmin=0, the reciprocal term can be omitted, including at a=0;
the code uses the maximum of the remaining linear function. If Bmin>0,
every physically feasible a is positive. For U>=0, U*a-Bmin/a is
increasing. For U<0 it is strictly concave and has its maximum at
sqrt(Bmin/(-U)), unless that point lies beyond a closed endpoint. The
tests Bmin<=(-U)*A^2 and Bmin>=(-U)*Z^2 pick the correct endpoints,
including equality. In the interior case its maximum is
-2*sqrt((-U)*Bmin). Multiplying the outward **lower** square-root bound by
-2 gives an upper bound. These are precisely the cases in
`reciprocal_max():7-14`.

The resulting numerator may be negative. Source line 28 uses full signed
interval division by the strictly positive interval (sigma-1)*h^3, and
then takes its upper endpoint. It does not divide a negative upper
numerator by a lower denominator as though it were positive. The new cap
is intersected cellwise with the old valid cap, followed by the maximum
across all 32 cells. A strict cap<rho_lower excludes; equality survives.
If the old calculation gives an omission or a different established
contradiction before producing inward cells, the chord layer retains that
entire old result. It does not manufacture a chord success.

## 4. The actual five-cap caller is finite and remains on one box

`low/coupled_chord_discovery_v1/feedback.py:23-48` first validates the
**original** entire cfg and original five-coordinate count box. It computes
H and beta once from those original coordinates. In at most three rounds:

1. Valid current signed support radii give necessary positive outer caps.
2. The chord scalar is evaluated on the original p/lambda/alpha box, with
   the original joint Lambda retained. Its new rho upper is rounded
   upwards to the 10^-9 grid, then intersected with the previous cap.
3. The original H/beta enclosures and this valid rho upper feed the
   original full-ray contact helpers. Each selected signed radius has a
   strict negative contact bound, all six strict derivative gates, correct
   sign/reflection and q=5/16.

Only rho_upper, radius_minus, radius_plus, outer0 and outer1 may change.
`frame():3-8` checks exact equality of all other fields, including D,d0,
Lambda, signed planes, affine prices, acquired moments and the attained
premise. Each changed field must be positive and no larger than the prior
cap. These numerical monotonicity checks are insufficient alone, but the
preceding scalar/support derivations supply the necessary physical license
for each actual change. No cap is used to prove itself. Finite induction
establishes all caps for the same fixed original box and k.

The H/beta/contact/outer helper bytes, including their constant provider,
are identical to the ones actually reviewed in
[the V14 contact unit](code_v14_contact_audit.md), and their original p25
hash references agree. The [new source map](code_n25_p25_chord_source_map.json)
records this explicit identity edge. The existing full-ray proof therefore
applies under the same attained-witness/CE/stronger24 premises. This does
not acquire those premises anew. Failed contact candidates provide no
support contraction; finite candidate selection needs no monotonicity of
the search heuristic.

These derived caps may depend on k, u and the raw inward interval. Their
use in a scalar calculation omitting those coordinates is sound because
the caps hold uniformly for witnesses in **this same fixed box**. The
conclusion is not phase-free and cannot be transferred to another box or
count. A nonlocal/empty original state conservatively falls back to the
unchanged native cfg. A nonpositive outer proposal is omitted. After at
most three rounds a surviving case is evaluated by the unchanged native
evaluator under the fully derived necessary cfg and all original raw
coordinates. Soundness needs the actual witness to satisfy that cfg; it
does not require monotonicity of the evaluator's program score in its caps.

## 5. Actual acceptance versus candidates and acquired references

The acceptance implementation is separate from discovery. In
`low/coupled_chord_acceptance_v1/protocol.py:120-147`:

- Ordinary leaves always rerun the original evaluator under original cfg.
- Dynamic scalar or derived-native leaves always rerun their entire
  declared scalar/contact chain, even if a registry theorem would also
  cover the leaf. Full typed evidence must equal the candidate.
- Theorem-reference leaves check their declared family, whole original
  cfg, immutable acquired object/review and exact closed containment.
  They do not rerun the scalar/native acquisition of that theorem.

The session's source loader pins the chord and compatible-moment kernels
and the original contact helpers. The acceptance process disallows
discovery/installer modules, checks all actually loaded local module
origins against the source graph, and uses the stored candidate only as
untrusted geometry and output to be compared. The protocol reconstructs all
26 ordered roots and all strict rational closed splits, rejects unknown or
pending rules, and checks original resource boxes. It separates scalar,
derived-native, ordinary and theorem counts. Source, result and deliberate
corruption controls are additional safeguards; they are not substitutes for
the continuous inequalities above.

For a dynamic leaf, scalar exclusion has no invented native result.
A derived-native leaf must really call native evaluation once after its
fresh finite chain. An unresolved native result cannot become a successful
declared leaf. Every ordinary/derived native success requires a known EMPTY
or strict score<CE_LO and full typed result equality. The whole forest's
cover implication follows by structural induction over each closed binary
tree, not merely the nodes=2*leaves-26 census.

The selected historical forest has 2,166 nodes and 1,096 leaves: 759
ordinary, 112 scalar, 149 derived-native and 76 theorem references (AB 2,
D 18, F 56; no C references in this particular forest). Its archived
statistics report 908 native evaluations, 637 scalar calls and 6,700
contact attempts. These are recorded as historical data, not fresh work by
this audit. Its receipt correctly has `all_native_count_receipt=false`.
Neither the rule name ABCDF nor its historical PASS establishes a whole
p25/n25 theorem.

## Remaining distinct edges

This unit reduces the dynamic scalar and finite feedback mathematics to
explicit checked implications. It leaves the following concrete work:

1. Read the actual AB sparse, D saved-scalar and F grid-pointwise
   **acquisition** routes and prove their current selected scopes; C is
   admitted by the source epoch but unused by this selected forest. The
   registry consumers' exact cfg/containment checks are not such a proof.
2. Supply the selected original p25 V14 native capsule and full kernel
   closure, or define an explicit audited replacement source epoch. The
   five identical supplied contact helpers are insufficient by themselves.
3. Acquire the actual B5 INITIAL/global resources in the new execution
   epoch, map them to the exact original p25 cfg and retain the required
   attained-contact premises. Acquire theorem objects and rerun every
   dynamic/ordinary acceptance call with complete evidence.
4. Check the final p25 original-row/regional join and all remaining B5
   panels against the [outer n25 union](code_n25_global_union_audit.md).
   No full B5, n25, C4/C5 or eventual-cutoff conclusion follows here.
