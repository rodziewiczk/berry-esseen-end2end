# Uniform confinement: antichains, centered deletion and one resource simplex

Date: 23 October 2026. This is a fallible internal AI source and hand-algebra
review, not external independent verification, formal verification or fresh
arithmetic acceptance. Cross-reads by other model agents are internal checks
by the same system. No archived mathematical module, constructor, acceptor,
concentration function or bound evaluator was imported or executed. The work
used original source bytes, text/AST comparisons and the derivations below.

## Bounded finding

This unit reads the full actual central and left Sperner proof texts and
their shared `sperner47_kernel.py`, together with the original confinement
proof/kernel differences. It follows the strict-gap antichain concentration,
actual deleted convolutions, signed phase slopes, endpoint intervals,
shared moment/leakage resource and exceptional-event tangent prices. No
unsound selected inequality was identified in this read. The conditional
same-law support implication has a coherent derivation, including atoms,
zero noise, both signs of H and the finite exterior ray allowed by the
already acquired strip.

This is not an acquisition of its weak input, strip, score/barrier/contact,
concentration or execution premises. The rational positivity gates still
require full replay. The standard finite Stirling inequalities are used
as a named analytical input: their substitutions and directions are checked
below, but no first-principles proof of Stirling's theorem is supplied here.
The later local Bernoulli comparison and global descent are separate.

The archive is `BE_cutoff49_20260930.zip`, SHA256
`ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e`.
Set `A=BE_cutoff49_20260930/` and
`B=A/baseline/certificates/work/below50_20260929/`. Paths below are relative
to B. The [new source map](code_uniform_confinement_source_map.json) records
all actual member hashes and original-manifest comparisons.

The central/left proofs have respective hashes
`517ed367bc961164cffccedb59d09f6cf5e3a339d387fb48bf6aa369dc521cb0`
and `668b87ac145a471e65c19f78e305cb35c93e1b4d8eef5ba7cb27c02d04d4e235`.
Their complete text difference is only the input/table scope, amplitude
schedule, 24 versus 16 noise subdivisions, and the correct cubic price
24 centrally versus 28 on the left. The shared kernel hash is
`21249fe117c6756a7a84af481dea2c5a490f9c66013c331cc998ab6828e1bb08`.
The original confinement kernel is the distinct
`59a601bf5615922e7ab1c71b22bdc25903e2f37c803eeb24d91919f370b6bfe7`.

## 1. Actual law, coordinate gap and contact

Let Y=B0+U, B0 Bernoulli(p), E[U|B0]=0, p in [l,u] subset (0,1/2),
X=ell(Y-p) variance one, theta=ell² E U² and lambda=n E U². The label-zero
support has largest endpoint a and label-one support smallest endpoint b,
where b-a=1-d, 0<=a<=d and 1-d<=b<=1. The acquired strip is
`support(Y) subset(-S,1+S)`, S=.55, and the selected d0<.025 is an upper
bound for d. These actual endpoints and this strip are essential premises,
not consequences of a proposed contraction amplitude.

The proof uses the contact majorant Q of the **closed** residual tail
`g(y)=nu([y,infinity))`, equal at actual support points. Its derivative is
the polynomial displayed in `sperner47_proof.tex:41–48`, with the same
actual C,rho,beta,H and law as the resource table. The score satisfies
.4<C<=.4253. The weak-input exact contact and positive leakage hypotheses
are inherited analytical obligations, not verified by a concentration bound.

The [local-join review](code_uniform_local_join_audit.md) traces the actual
strip/support/predecessor ordering. In particular the central strip comes
before confinement; LEFT270 and its separate strip precede left Sperner.
Neither a standardized radius alone nor a matching old JSON acquires them.

## 2. Simultaneous endpoint, variance and central-square prices

This proof needs the simultaneous inequality

`D>=c+ M+ +c- M- +b* theta+P`,

not separately valid bounds that each spend D. Here M+=p DeltaB,
M-=q DeltaA, with actual gap endpoints A=ell(p-a), B=ell(b-p).
Its derivation can be made explicit from the physical gap decomposition:

`D=mQ+(sigma-1)T+ +(sigma+1)T- +3(T-Jo)`,
`T-Jo>=2B R+ +2A R-`, `Q=(sqrt(sigma+1)A-sqrt(sigma-1)B)²`.

On the positive side, write bbar=m/p>=B. Conditional centering gives
`T+>=m DeltaB(bbar+B)+(B+2bbar)theta+` and
`R+=theta+ +m DeltaB`. Therefore

`(sigma-1)T+ +6B R+
 >=2(sigma+2)B² M+ +3(sigma+1)B theta+`.

The negative side similarly gives
`2(sigma+4)A² M- +3(sigma+3)A theta-`. These prices leave mQ available;
they are obtained in one expansion and may be added simultaneously.
Lower ell, p, 1-p and positive endpoints then give source c+/c- and b*.
The source constants 5.16,7.16,4.16,6.16 are lower bounds for the
corresponding sigma shifts.

For the central term, write c=sqrt(sigma+1), e=sqrt(sigma-1). Directly

`sqrt(Q)=ell*|(c+e)(p-p*)+e d-(c+e)a|`,

with p*=(4-sigma)/2. Since 0<=a<=d, the displacement term has magnitude
at most c d. The inequalities c+e>3.5, c<2.041 and
p* in [.41886,.41887] give precisely the source's positive-part square
P with lower m and lower ell². Thus its central loss is not a second use
of the displacement budget. Also
`d=(M+/p+M-/q)/ell`,
`epsilon=E|U|<=2(M++M-)/ell`; the latter follows signwise from centering
and the support lower endpoint of each conditional noise.

## 3. Strict-gap concentration, including collisions and endpoints

Independently sample each conditional noise pair (U0,U1), then an independent
Bernoulli label. This realizes the actual marginal Y; it does not replace
it by an extremizing or different marginal. Its random step is
`1+U1-U0>=b-a=1-d`.

After conditioning on all pairs, any subset of labels has a weighted sum
with all positive steps at least c=1-d. Subsets whose sums lie in an
interval of diameter strictly less than c form an antichain: comparable
distinct subsets differ by at least c. A random permutation chain contains
a fixed k-subset with probability 1/binom(j,k) and meets an antichain at
most once. Therefore the sum of these reciprocal level sizes is at most 1.
Multiplying by the largest biased binomial level mass gives the conditional
probability bound, and integrating gives it for the actual sum.

Independent additional noise only translates the interval after conditioning,
so it preserves the cap. Arbitrarily small atoms and exact subset-sum
collisions cause no problem. The strict diameter restriction is indispensable:
a closed interval [0,c] captures both atoms of a Bernoulli law on {0,c}.
The source's width gates apply to whole closed intervals and are strictly
positive; no density assumption or omission of boundary atoms is made.

## 4. The uniform binomial cap uses the correct remaining index

For j>=J0=N-2=45, a binomial mode k has
`(j+1)p-1<=k<=(j+1)p`. Hence k/j lies in
`[l-(1-l)/J0,u+u/J0]`. The source checks this interval lies inside (0,1),
so both factorial arguments are positive. Concavity of r(1-r) gives a
positive variance lower endpoint v*.

Applying the displayed finite Stirling inequalities to j!,k!,(j-k)!
places an upper exponential error only in the numerator. It gives
`sqrt(j)*mass <= exp(1/(12j)-j KL(r||p))/sqrt(2pi r(1-r))`.
KL>=0, `exp(x)<=1/(1-x)` on [0,1), phi(0)<.4 and j>=J0 then give the
strict cap M used by `sperner47_kernel.py:57–61`, with an outward upper
square root. This checks the use of Stirling, not a fresh proof of its
finite inequalities.

It covers n-1 full summands and **n-2** full summands after a mark/deletion.
The common fd bounds both `(n/(n-1))^(3/2)` and `sqrt(n/(n-2))`, uniformly
at N. The latter index is not upgraded to n-1. This distinction is needed
for centered noise, exceptional-pair error and the distance term, whose
normalizations differ.

## 5. Centered signed deletion and the strict exceptional pair event

Put m=n-1, Z=x-sum(Y_i), mu=x-mp, K=sum(B_i). Exchangeability gives
`mp*T1(I)=E[K 1_I(Z)]`, `mq*T0(I)=E[(m-K)1_I(Z)]`.
Since `mp-K=Z-mu+sum(U_i)`, this proves the two signed identities at
`sperner47_proof.tex:164–172`. The noises are not replaced by their
absolute values before summing.

For a full removed pair, the remaining conditional probability f(Y_i)
lies in [0,Q_{n-2}(w)]. Centering gives
`E[U_i f(Y_i)]<=Q_{n-2}(w)E(U_i)+=epsilon*Q_{n-2}(w)/2`.
It remains true for deterministic conditional laws. The source divides
the two directed terms by their actual p and q, then substitutes lower
p>=l and q>=1-u. Its factors and signs match these identities.

For independent conditional noises, Delta=U1-U0>=-d, E Delta=0 and
`Var(Delta)<=s/p`, because p<q and s=p Var(U1)+q Var(U0).
The map from the T1 point to the T0 point adds 1+Delta. On Delta<=tau this
maps I into `I+=I+1+[-d,tau]`. On the strict exceptional event Delta>tau,
conditioning on both noises leaves n-2 full summands, so the error is at
most their interval cap times P(Delta>tau).

Cantelli and Markov for Delta+d>=0 give respectively
`s/(s+p tau²)` and `d/(d+tau)`. Equality Delta=tau stays in the good event.
The source uses the minimum of two full valid bounds, not a sum. This
retains the actual common law, atoms and the correct deletion index.

## 6. Signed slope bounds and quantitative scalar hypotheses

The acquired strip and d<=d0<S imply |U0|,|U1|<S. Conditional expansion
therefore gives
`rho<=rhoB(p)+ell³*(3q+S)*s`.
The per-p-cell gate `third²*(l(1-l))³>(3(1-l)+S)²` licenses third=24
centrally or 28 on the left; s=lambda/n<=s_h/N gives the stored rho cap.
The signed second identity gives the source beta lower and upper endpoints.
Positive beta lower, positive Gaussian lower and the bound H<3 are actual
gates used in the slope algebra, not inferred from a name for a coefficient.

For H>=0 the upper H*phi is .4*h_h; for H<=0 it is
`-phi_lower*h_l`. Keeping that negative sign is necessary. On t<=0, the
contact derivative's polynomial is a positive quadratic. Its global lower
bound uses the upper nonnegative linear coefficient and denominator
12*.4. The `minimum_rho` gate ensures the coefficient is nonnegative before
it is squared. Negative corrections are multiplied by upper ell and 1/N;
the positive Gaussian term uses lower ell and lower density.

For t>=0, completing the downward square gives the positive half-line
upper slope. The central-gap lower slope instead uses rho>=1 and
`t(t-1)<=Bmax(Bmax-1)` on 1<=t<=Bmax, with its favorable sign on [0,1].
Here Bmax>=sqrt((1-l)/l)>1 bounds the positive conditional mean.

On the lower ray the whole contact interval has t<=tmax<0. The true
bracket is bounded below using
`B(t)=beta_lower+rho_upper*t+t²`,
`3C B(t)>=1.2 B(t)+3(C0-.4)min(0,B_min)`.
This explicitly separates the negative part before varying C. Adding the
adverse signed phase term leaves a convex quadratic minimized at its
clipped vertex on (-infinity,tmax]. This is the source's sharper lower
slope, including both H signs. No derivative bound is extrapolated from
a sampled t value.

## 7. Contact interval geometry and the finite exterior ray

For a lower support point y=a-r, r>=r0, take
`I=[a-r,a-d-tau_minus-eta]` and
`I+=[a-r+1-d,b-eta]`.
Contact at y and the majorant inequality at the other endpoint bound nu(I)
below by the integral of the lower slope. Closed tails give a half-open
difference interval; using its containing closed I is safe even with atoms.
The translate lies inside [a+g,b), g=1-S-2d0>0, so nu(I+)<=J/g.
Because actual support lies above -S, only r<=S+d0 is relevant.
Both widths are strictly below 1-d under the source gates, and the directed
distances depend on the upper endpoints, not on r. The two intervals are
disjoint throughout that actual finite ray.

For an upper support point y>=1+r0, take
`I=[a,a+tau_plus]`, `I+=[b,a+1+2tau_plus]`.
The buffer gates put I inside the central gap and I+ inside [b,y).
The contact identity between the support endpoints a,b gives
`sqrt(n)nu(I)>=L_gap(1-d)-sqrt(n)J/tau_plus`.
Contact at b,y gives the upper slope bound
`sqrt(n)nu(I+)<=U_plus(S+d)`. The atom at b is included by the closed-tail
convention. Their strict-width and disjointness gates are checked separately.

For the Sperner route all interval concentration caps and error terms are
independent of the lower-ray length r, while its contact lower bound grows
with strictly positive slope L. A strict contradiction at r0 therefore
covers every remaining support point up to S+d0. It makes no assertion
about an unacquired infinite exterior strip.

## 8. One strict budget and the zero-cap EMPTY boundary

The acquired strict budget is
`ne*rho+n phi(0)D/6+n^(3/2)L < min(T,max_j budget_quad_j(H))`.
Its strictness is traced in the local-join review: the exact Fourier ledger
uses 2/pi, whereas the selected rational source uses the strictly larger
16/25 or 212/333 with a positive enclosing Fourier expression. Finite corner
maxima, lower phase subtraction and outward targets preserve that strictness.
It does not arise merely from a non-strict JSON comparison.

On a closed H/lambda box, each concave phase quadratic is maximized at its
clipped vertex; the maximum of these full bounds is intersected with T.
With kappa=997/15000, lower noise s_l and lower ell E, this gives

`n c+M+ +n c-M- +n^(3/2)L/kappa < R-nP <=R-NP=:R0`,
`R=budget/kappa-b*E²*s_l`.

All resources are nonnegative. Thus R0<=0 excludes the box, **including
equality**, because the comparison is strict. Otherwise
`nd<R0/alpha=G`, `alpha=min(c+ l E,c-(1-u)E)>0`.
This supplies the Markov pair-event cap `G/(N tau+G)` independently of the
variance cap. It also explains why no one-sided n-to-N inequality is applied
to a negative resource.

## 9. Error allocation and the shared exceptional-event tangent

Contact and the two deletion identities leave the cost
`a_d*d+a_J*sqrt(n)J+a_e*epsilon + A/n+B*Pbad`.
On the lower side a_d=L, a_J=1/g; on the upper side a_d=L_gap+U_plus,
a_J=1/tau_plus. Substituting d,epsilon and J<=L/(1-Theta), the first three
terms are bounded by z times the **single** resource simplex, where

`z=max((a_d/l+2a_e)/(E c+),
       (a_d/(1-u)+2a_e)/(E c-), kappa*a_J/(1-Theta))`.

The source's older error is `(zR+A)/N-zP+B*bad`.
The inverse-index coefficient is checked positive before replacing n by N.
Both variance and Markov pair caps decrease when n is replaced adversely
by N. No independent full budget is then added for the pair event.

For the stronger bound set Dindex=nd. The function
`Dindex/(N*tau+Dindex)` is concave. Its tangent at t>=0 is
`N*tau*Dindex/(N*tau+t)²+t²/(N*tau+t)²`; subtracting the original function
leaves the nonnegative square stated in the source proof. The cost and
Dindex are simultaneous linear coordinates of the same three-resource
simplex. Their affine combination is maximized at a vertex. All vertex
cost/displacement coefficients are nonnegative, so the omitted zero-resource
origin cannot increase the maximum.

The kernel uses the maximum over those three vertices, then the minimum
over the older bound and eleven individually valid tangents. Every tangent
choice is safe; no minimizing derivative, convergence, independently chosen
resource extremizers or favorable piece of an invalid bound is used. This
checks the main resource-sharing step in `sperner47_kernel.py:120–135`.

## 10. The original confinement route's different concentration and ray

The original kernel uses the Berry--Esseen concentration bound
`sqrt(j) Q_j(w)<=ell*phi(0)*w+2*C0*rho` for j=n-1,n-2.
That is a separate hypothesis of its proof. A universal cap C_j<=.4253
at both deleted indices suffices: normal interval mass supplies the linear
term, and the two CDF errors supply the constant term, including atoms.
The earlier .7/j barrier with CE<.40974 supplies this cap for j>=45,
because `.40974+.7/45<.4253`. Acquiring that barrier is a separate prior
proof edge; the current witness's own score cap alone would not establish
a universal cap for the actual deleted convolutions.

The original centered error optionally uses the hull bound on two disjoint
intervals. Since p<q,
`fI/p+fJ/q<=min(QI/p+QJ/q,Qhull/q+(1/p-1/q)QI)`.
The reciprocal difference decreases in p; the code's lower-p and lower-q
substitutions enlarge it appropriately. This is an alternative complete
noise bound. The newer Sperner route deliberately uses separate caps and
does not need concentration of a wider hull.

Original concentration caps grow affinely with lower-ray length. Its
extra slope gate bounds their increments using the uncoupled price and
the independently valid cap `n*epsilon<2T/(kappa*E*min(c+,c-))`.
This can be justified for the same
physical resources before taking the resource/tangent maximum: both hull
and uncoupled affine noise prices have slope no larger than the uncoupled
one, and the exceptional probability is bounded by the unchanged bad cap.
Thus a better shared bound at r0 can be retained while paying the complete
uncoupled increment. This does not differentiate the minimum of tangent
bounds or assume a density for interval-probability increments.

Only the acquired finite ray r<=S+d0 is needed, where the intervals stay
disjoint. Loose wording about all r>=r0 must not be read as obtaining a
support theorem beyond its actual strip hypothesis. The original code's
strict ray-slope gate and the newer Sperner constant-error ray are different
valid sufficient strategies; neither may silently replace the other's gates.

## 11. Endpoint conclusion, execution boundary and remaining inputs

The strict lower/upper contradiction gates exclude support points
y<=a-r0 or y>=1+r0. Since a>=0, label-zero support<=a<=d0<r0 and label-one
support>=b>=1-d0>1-r0, both conditional noises satisfy |U|<r0. This includes
zero noise and does not require a minimum atom size. The positivity/width
gates cover complete closed H/noise rectangles, with both signs of H and
H=0. The full read-only acceptors still have to reconstruct every gate,
empty box, census and source-bound contract in actual execution.

The actual central, left and original acceptors were also source-read.
They reconstruct rather than trust stored minimum reserves, check each
gate has exact Fraction type and is strictly positive, and compare the
entire typed candidate object with the reconstructed result. The keys of
empty and feasible boxes must form the exact unique closed-grid index set
for every p/H-sign row. The selected full censuses are 45*2*16*24 centrally
and originally, and 38*2*16*16 on the left. These are source obligations,
not newly executed box evaluations. The same kernel argument applies to
the separately fixed profile schedules because their clipped closed noise
bands still have nonnegative lower endpoint and all the same gates; their
acceptors and different census remain separate fresh jobs.

The hand review therefore supplies a conditional derivation for this
confinement block. It leaves separate: finite Stirling as named analytical
input; unrestricted attainment/contact and exact identities; acquisition of
INITIAL, actual strip/support, barrier/decrement and strict resource tables;
fresh full rational arithmetic and transport/receipt acceptance; the later
TINY/MID/LOW comparison proofs, lambda=0 Bernoulli theorem and global descent.
The older dormant 29/5 bootstrap is still explicitly unreviewed. No completed
source review or historical PASS here is an unconditional all-index result.
