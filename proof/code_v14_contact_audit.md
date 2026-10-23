# Code-to-lemma audit: the selected V14 local contact/rho wrapper

**Review status:** AI-generated internal source review. Cross-reads by
other model agents are internal checks by the same AI system. External
independent mathematical review and machine-checked formal verification
are not established here. This review may contain mistakes or omissions.
See the [evidence limits](CODE_INTERFACE_AUDIT.md#evidence-limits).

Date:23 October2026. Scope: portable p31/p32 epochs used by notebooks06/07.
The [source map](code_v14_contact_source_map.json) binds their exact178-file
designs and the inspected functions. All declared hashes matched; no archived
module, Gaussian evaluator or count leaf was executed. This note supplements
the separate [count-component review](code_count_kernel_audit.md) and
[resource-to-contract review](code_n25_join_audit.md).

No unsound mathematical step was identified in the original-box contact,
outer-cap/rho-upper formulas and finite three-step wrapper reviewed below,
conditional on the stated global attained witness and prior resources.
This does not close every V12 fallback kernel, full LOW/phase acquisition or
fresh numerical replay. It cannot turn a parameter-restricted optimizer into
the unrestricted witness required by contact.

The consumed `local_contact_scale.constants` interface must supply
c<=actual C, Sup>=sqrt(25/24), e_upper>=25*(Sup-1)-1/2 and the licensed
published rho cap. The radical directions and literal definitions were read;
source identity alone does not prove those structural or external premises.

## Sources and contract

The source map records these shared exact files:

| File | SHA256 |
|---|---|
| `local_contact_v14.py` | `78ee48726397e1a6185aa02584ffd21d4eb87ff69e9685807a13b5f9edf09a7c` |
| `local_contact_outer_v14.py` | `a30217eb6cdc16a3bec77d1ddf6e3a492b22fc30a9eb4e893ebe649ad49779f7` |
| `local_contact_support.py` | `f0881cee379d3bd2ff293751f4c802eabd91b2c28c76a1c0984701ce9c4db680` |
| `local_contact_gaussian.py` | `c0ca6ae03a2aa4e635e41bd2a5ba8fb02a8b060b3c89313860208b2ac548a3be` |
| `local_rho_upper_v14.py` | `ffa7e725310f18122abfb5883e780328de0156ef4efe4f099ddb86609588f41e` |

The contract loader compares the whole original V12 dictionary with the V14
dictionary, permitting exactly the explicit q=5/16 and attained-positive-closed
premise fields. It keeps n25/K0, the original p/rho panel, resources, target,
all26 count roots and original five coordinates. The underlying contact rule
is the supplied manuscript's same-law full-support contact inequality; the
localization and finite feedback are additional derived implementations
described in the source's `INDEPENDENT_LOCAL_CONTACT_PROOF.txt`,
`LOCAL_RHO_UPPER_PROOF.txt` and `INDEPENDENT_FINITE_FEEDBACK_PROOF.txt`.
These local derivations should be included or explicitly mapped in a revised
paper; a source pin alone is not such a mapping.

## 1. Original H/beta enclosures

Let `s=lambda/n`, `v=p(1-p)`, and
`X=(B-p+U)/sqrt(v+s)` with the licensed centered sign-conditioned components.
The original count box implies

`H=(k+u-n*p)/sqrt(v+s)`,
`beta=[v*(1-2*p)+s*(2*alpha-1)]/(v+s)`.

`original_box_state` computes exact extrema of v, interval products using
all four corners, positive root/divisor enclosures and intersections with
the OLD acquired H/beta intervals. This retains negative and zero-crossing
thresholds and s=0. No division by s occurs here. An empty interval or
non-strict beta endpoint conservatively omits the optional contact path;
it is not clamped into a new witness. Physical sign-mean is
v/sqrt(v+s), not sqrt(v+s).

## 2. Both full support rays

For radius R>=1 and ray sign sigma, set B=beta_upper on the positive ray
and B=-beta_lower on the negative ray. With r an acquired rho upper bound,
the cubic coefficient upper bound is

`Q(t)=-t^3+(3/2)*r*t^2+3*B*t+r*e_upper`.

`ray` requires Q(R),Q'(R),Q''(R)<0. Since Q'''=-6, Q stays negative
on the entire ray. Thus multiplying by the positive score lower bound c
is in the correct upper direction in the contact inequality.

For the known Gaussian function G(H,y), symmetry gives
`G(H,-t)=-G(-H,t)`. `restricted_line` reflects the entire H interval for
the negative ray and negates the lower G endpoint. It does not reflect beta
a second time or change the original one-sided predecessor premise.

The uniform derivative gate is

`|G_y(H,y)| <= phi(0)*(y^2/2+n*(sqrt(n/(n-1))-1))`.

To verify it directly, put z=H/sqrt(n), w=z-y/sqrt(n), S=sqrt(n/(n-1)).
Differentiate G to obtain
`G_y=(n+H*y)*phi(z)-n*S*phi(S*w)`.
Taylor's theorem bounds `(n+H*y)*phi(z)-n*phi(w)` by
phi(0)*y^2/2. The derivative of `s*phi(s*w)` is
`(1-s^2*w^2)*phi(s*w)`, whose absolute value is at most phi(0).
This gives the remaining n*(S-1) term. Using phi(0)<2/5 and the upper
e and S constants yields exactly the quadratic L in the code. Its
negative value, negative derivative at R and negative leading coefficient
prove strict decrease beyond R. A strict negative contact value at R
therefore excludes every support point on the closed ray, not just R.

At a fixed R, direct differentiation gives the source's G and G_H
formulas. A second derivative bound uses
`|z*phi(z)|<1/4`, `|(z^2-1)*phi(z)|<=phi(0)<2/5`, and
`|(z^3-3*z)*phi(z)|<=2*phi(0)<4/5`.
For the last bound, writing w=z^2, split w<=3, where
sqrt(w)*(3-w)<=2, and w>=3, where
w^(3/2)*exp(-w/2)<=3*sqrt(3)*exp(-3/2)<2.
The resulting curvature is the coded
`sqrt(n)_upper*(n/(n-1)+1)/4+(2/5)*R+(2/5)*|R^2-1|/sqrt(n)_lower`.
Midpoint Taylor with a derivative interval and M*halfwidth^2/2 bounds
each whole closed H cell. Adjacent cells and degenerate intervals retain
all endpoints. The512-cell work guard returns omission, not a false ray.

The Gaussian CDF backend is byte-identical to the
[reviewed finite Gaussian primitive](code_fourier_primitive_audit.md).
The density exponential uses an odd degree23 alternating truncation after
halving q into[0,1], adds term24 only to the upper endpoint, then squares
the nonnegative interval with directed integer rounding. G and G_H use
full interval products, preserving signs of CDF differences and coefficients.
The global Gaussian-tail helper is not called by the restricted local line;
this note does not certify every other use of that global helper.

## 3. Outer caps and a direct rho upper bound

Support `[-Rminus,Rplus]` and the original box give valid conditional caps

`O0_new=min(old_O0,Rminus*sqrt(v_upper+s_upper)_upper-p_lower)`,
`O1_new=min(old_O1,Rplus*sqrt(v_upper+s_upper)_upper-(1-p_upper))`.

Here O0/O1 denote upper caps on the respective one-sided centered noises;
the displayed minimum is a newly valid upper bound, not an assertion that
the physical cap equals that number. If a proposed cap is nonpositive,
the implementation omits the optional improvement conservatively.

For a centered W>=-A with variance t, expanding
`E[(W+A)*(W-t/A)^2]>=0` gives `-EW^3<=A*t-t^2/A`.
The reflected upper-support version gives the corresponding upper EW^3
bound. Apply these to both sign components with allocations1-alpha,alpha.
The raw absolute third moment is bounded by

`v*(1-2*v)+M(p,alpha)*s-C(p,alpha)*s^2`,
`M=(3*p+O0)*(1-alpha)+(3*(1-p)+O1)*alpha`,
`C=(1-alpha)^2/((1-p)*O0)+alpha^2/(p*O1)`.

The code maximizes the bilinear M at corners. It bounds C below by both
the clipped convex alpha minimum after replacing denominators by upper
endpoints and the Cauchy bound `1/max_p((1-p)*O0+p*O1)`. Their maximum
is still a lower bound. Since v(1-2v) increases on[0,1/4], its v_upper
value is an upper bound. The resulting concave quadratic in s is maximized
at its clipped vertex on the ORIGINAL s interval.

A nonpositive numerator excludes a variance-one law because its true
absolute third moment is positive. Otherwise divide by the positive lower
bound `(v_lower+s_lower)*sqrt(v_lower+s_lower)_lower`, round the resulting
rho upper bound UP, and intersect with the old cap. A zero lower root omits
the update. Empty rho means strictly new_upper<acquired_lower; equality
survives. These directions match `local_rho_upper_v14.upper_cap`.

## 4. Finite feedback and fallback link

`local_contact_v14.cell35` first validates all ORIGINAL resources and raw
coordinates. It then performs at most three explicit stages:
old support -> positive outer caps -> rho upper -> independently certified
contact rays. The original H and beta enclosures remain fixed and valid for
the same witness. No convergence, fixed point or monotonicity of the search
heuristic is assumed. Bisection chooses proposed radii; every exported radius
has its own complete strict full-ray certificate.

The candidate changes only acquired rho/support/outer upper caps; it retains
all prior resource inequalities and their original intercepts. Every V12
retry receives ALL ORIGINAL raw coordinates, not an already contracted box.
An independently justified necessary-condition contradiction may exclude the
box; otherwise the wrapper keeps the better of two conditional upper bounds
and retains the old fallback. These are legitimate finite implications for
one original unrestricted attained witness.

The remaining V12 kernel alternatives and full resource/contact acquisition
are separate. This review neither guarantees termination of candidate
discovery nor supplies a runtime estimate, a fresh forest acceptance or a
global n25 conclusion. All such flags remain false in the source map.
