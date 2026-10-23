# The exact finite Gaussian input

Audit date: 23 October 2026. This note checks one analytic input, not the full
tail theorem. It uses no numerical producer, integration or certificate replay.

The manuscript's selected He--Cheng input is Appendix A.1, equation (70), in
[the original v1 paper](https://arxiv.org/html/2609.06358v1). In their
notation, for every integer n >= 2 and all real z,y,

\[
 |H_n(z,y)|\le \phi(0)|y|^3/6+|y|/5+1/2.
\]

Their equation (47) defines the same function as the manuscript's
`mathcal H_n(H,t)` after the substitution z=H/sqrt(n), y=t. This is a
finite Gaussian estimate. Its use does not import their eventual sharpness
theorem or its threshold. Both the stated domain and normalization agree.

## Direct check of the selected estimate

Write u=z-y/sqrt(n) and f(lambda)=Phi(u/sqrt(1-lambda)). Taylor expansion
of Phi at z through order two leaves a translation remainder bounded by
phi(0)|y|^3/6 after multiplication by n^(3/2), since
`sup |phi''| = phi(0)`.

Taylor expansion of f at zero gives the remaining main term
sqrt(n)[u phi(u)-z phi(z)]/2. Its absolute value is at most
phi(0)|y|/2 < |y|/5 because `(x phi(x))'=-phi''(x)`.

For 0 <= lambda <= 1/2, putting r=u/sqrt(1-lambda),

\[
 f''(\lambda)=\frac{r(3-r^2)\phi(r)}{4(1-\lambda)^2}.
\]

The bounds `sup |r| phi(r)<1/4` and `sup |r|^3 phi(r)<1/2` imply
`sup |f''|<5/4`. Thus the multiplied scale remainder is less than
5/(8 sqrt(n)) <= 5/(8 sqrt(2)) < 1/2. Summing these three bounds proves
the displayed estimate on the full stated domain.

This discharges the identified statement/normalization concern for this input.
It does not validate support-row arithmetic, the later compensated Fourier
inequalities, the uniform local comparison, or their implementations.
