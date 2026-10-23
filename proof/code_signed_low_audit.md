# Code-to-lemma audit: selected signed LOW coefficients and cancellation

**Review status:** AI-generated internal source review. Cross-reads by
other model agents are internal checks by the same AI system. External
independent mathematical review and machine-checked formal verification
are not established here. This review may contain mistakes or omissions.
See the [evidence limits](CODE_INTERFACE_AUDIT.md#evidence-limits).

Date: 23 October 2026. This note checks the actual
`resource25_b3_v1/general_paired_exact.py` and B4 copy, SHA256
`e383a78467c380ae55ef9ef32f296cb5813f837c8bcaf3003a113a04fb29fb96`,
in the archive/source identities of [the source map](code_fourier_source_map.json).
The resource entry points install this function at `resource25_core.py:15`,
before their phase callbacks. No mathematical function was executed locally.

The signed transfer and finite Mills lemmas are in the supplied manuscript,
lines1708--1874. The more general piecewise coefficient rectangle below is
documented inside the archive's `GENERAL_PAIRED_PROOF.txt` and its older
review; it is broader than the manuscript's displayed specialized rectangle
with M<3, g^2<2, R>2g at lines1927--1957. We internally reviewed the
extension's algebra below. A revised paper must include this extension if
it uses these selected general resource implementations.

## Conditional result and boundary

Given genuine same-law inputs

`EX=0`, `EX^2=1`, `|X|<=R`, `EX^4<=M<=11.1`,
`0<=gl<=|EX^3|<=g<=1.85`, `E|X|^5<=eta`, `M>=1+gl^2`,
and literal integer n>2,

the inspected coefficient enclosure, signed norm, finite Mills parity and
literal-index transfer formulas match valid extensions/specializations of
the displayed transfer lemma. No unsound sign, missing R>2g gate or wrong
damping coefficient was found in those operations. This is not a review
of the entire `context/eligible` acquisition of gl/rmin, nor the complete
resource callback or its export; those remain explicit dependencies. Directed
root endpoints, a nonnegative exponential upper bound, and
333/106<pi<22/7 are consumed here as the separately reviewed
[primitive interfaces](code_fourier_primitive_audit.md).

## 1. Piecewise Pearson enclosure, lines10--36

Reflect only this auxiliary Fourier norm so t=|EX^3|>=0. Put
`Q=X^2-t*X-1` and `v=EQ^2=mu4-1-t^2>=0`. Exact expansion gives

`mu5=t^3+2*t+E[Q^2*(X+2*t)]`,
`mu6=1+3*t^2+t^4+E[Q^2*((X+t)^2+2*t^2+2)]`.

Hence, for `z=(10*t-mu5)/120`,

`L(t)=8*t-t^3-(R+2*t)*(M-1-t^2) <= 120*z`,
`120*z <= U(t)=8*t-t^3+max(R-2*t,0)*(M-1-t^2)`.

For the lower bound, X+2t<=R+2t and v<=M-1-t^2. For the upper
bound, X+2t>=-R+2t: if R-2t>=0, substitute the upper bound on v;
if R-2t<0, use v>=0. This sign split is necessary. It is exactly why
merely removing R>2g from the older rectangle would be unjustified.

The coded polynomials are therefore:

- `L=-R*(M-1)+(10-2*M)*t+R*t^2+t^3`;
- on t<=R/2, `U=R*(M-1)+(10-2*M)*t-R*t^2+t^3`;
- on t>=R/2, `U=8*t-t^3`.

`cubic_range` substitutes t=a+(b-a)x into each cubic. Its power
coefficient for x^h is
`sum(co[j]*choose(j,h)*a^(j-h)*(b-a)^h,j=h..3)`.
The conversion
`x^h=sum(choose(i,h)/choose(3,h)*B_i^3(x),i=h..3)`
is exact. Bernstein basis functions are nonnegative and sum to1; minimum
and maximum coefficients enclose the polynomial on the whole closed cell.
The32 cells and the two pieces at R/2 retain every endpoint, also when
gl=g. Enclosing infeasible t with t^2>M-1 is conservative: the inequalities
are applied to actual feasible t and the extrema are taken on a superset.

The eta cap supplies `|120*z|<=eta+10*g`. The remaining fields are

`a_star=max(|3-M|,|2-gl^2|)/24`,
`c_lower=(3-M)*(gl if M<=3 else g)/144`.

These use the entire interval `1+gl^2<=mu4<=M` with its actual signs.
The upper c endpoint maximizes `(2*t-t^3)/144`: the three exact cases
compare3g^2 and3gl^2 with2, using an upper sqrt(2/3)/108 at the interior
maximum. Negative c intervals are retained rather than clipped to zero.

## 2. Norm, signs and finite Mills parity, lines57--68

The exact norm is
`J(z,c)=integral_0^infinity exp(-x^2/2)*|z*x^2-c*x^4| dx`.
It is jointly convex. A rectangle maximum of the exact norm is therefore
bounded by the largest of its four corner values. The code uses an upper
bound at each corner; it does not assume the minimum of its two upper-bound
formulas is itself convex.

If z*c<=0, J=sqrt(pi/2)(|z|+3|c|). Otherwise simultaneous replacement
of (z,c) by (|z|,|c|) preserves the norm. Replacing just one sign would
not. For positive z,c, with x=z/c and r=sqrt(x), splitting at r and
integrating by parts gives exactly

`J=sqrt(pi/2)*(z-3*c)+sqrt(z*c)*exp(-x/2)*(6+2*(3-x)*r*Mills(r)/x)`.

To see the continued-fraction direction without assuming convergence, put
`I_j(r)=integral_0^infinity t^j*exp(-r*t-t^2/2) dt`.
Integration by parts gives `I_0=1/(r+I_1/I_0)` and
`I_j/I_(j-1)=j/(r+I_(j+1)/I_j)`. Every remainder is positive.
Replacing the last remainder by0 reverses order once per substitution:
odd depth11 gives a lower Mills bound and even depth12 gives an upper.
The multiplier3-x is nonpositive for x>=3 and positive for x<3,
exactly matching the code's depth choice.

The Gaussian constant multiplying z-3c is an upper endpoint when that
coefficient is nonnegative, a lower endpoint otherwise. The remaining
Mills multiplier is explicitly checked positive before multiplying root
and exponential upper endpoints. The simpler upper bound uses
`I*|z-3*c|+6*sqrt(z*c)*exp(-x/2)` and the minimum is safe at each corner.
For x<3 its validity also follows from
`exp(-x/2)*Mills(sqrt(x))<=sqrt(pi/2)`; for x>=3 the omitted Mills
correction is nonpositive.

## 3. Literal-index transfer, lines69--75

The factor `n/(n-1)*roots(n/(n-1))[1]` encloses
`(n/(n-1))^(3/2)`. The coded L0 and LH include the entire cancellation
triple from the manuscript: the35/48 and35/24 corrections, the LH
5/2 factor, and the251 Gaussian-comparator terms. None is dropped when
the signed norm is improved.

The sixth-moment enclosure follows from the Pearson identity above:

`M6=min(R*eta, 1+3*g^2+g^4+(R^2+2*R*g+3*g^2+2)*(M-1-gl^2))`.

Every replaced factor is nonnegative; no R>2g assumption enters it.
Then `E6=M6/720+g^2/72+(1/2+g^2/144)^3/5`,
`B6=a_star+Z/2+E6/4`, `a0=(n-1)/(2*n)`, and
`b0=(45-M)*(1-2/n)/96` are exactly the stated transfer parameters.
The L2 formula retains both terms and both positive damping gates.
In particular the obsolete43/96 value is not substituted on M>2.

## Open joins and scope retained

The following are not established by checking the coefficient/norm algebra:

- the actual same-law lower rho/gamma bounds returned by `context`;
- physical acquisition of R,M,g,eta,theta,endpoints and support;
- selection of this paired path versus each fallback at every call site;
- consistency of rmin between LOW, phase corners and resource exports;
- complete signed phase/charged-envelope and support-row coverage;
- any numerical acceptance or completed n25/global theorem.

The broader piecewise extension is a specific paper-to-code documentation
obligation, not evidence that the numerical inequality is false. The source
map keeps full LOW/callback acceptance flags false and pins the actual code.
