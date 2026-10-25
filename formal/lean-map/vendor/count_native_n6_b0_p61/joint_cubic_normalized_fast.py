"""Exact runtime optimization: transform the interval base once per quartic.
Exact affine cubic translations commute with the interval Bernstein transform.
No target, vertex, halfplane or admissible parameter is changed.
"""
from joint_cubic_normalized import *

def bernstein_upper_vector(co,lo,hi):
 width=hi-lo
 power=[sum((co[j]*F(comb(j,i))*lo**(j-i)*width**i for j in range(i,5)),I(0))for i in range(5)]
 return [sum((power[j]*F(comb(i,j),comb(4,j))for j in range(i+1)),I(0)).h for i in range(5)]

def score_forms(k,n,t,s0,s1,O0,O1,a0,a1,V,intercept,drift,mass,aa):
 V0=(n-k)*s0;V1=k*s1;V=intersect(V,V0+V1);J=(n-k)*s0**2+k*s1**2
 cost=(n-k)*O0*a0*s0+k*a1*O1*s1
 point=max(V.l,min(V.h,aa*aa/2))
 concave=I(min(3*aa*aa*x-3*x*x for x in(V.l,V.h)),3*aa*aa*point-3*point*point)
 co=[concave+3*J-cost,I(-2*aa**3),3*aa*aa-6*V,I(0),I(-1)]
 score=[-mass*x/(K*aa**4)for x in co];score[0]=score[0]+intercept;score[1]=score[1]+drift
 base=bernstein_upper_vector(score,t.l,t.h)
 out=[]
 for i,B in enumerate(base):
  phase=t.l+F(i,4)*(t.h-t.l)
  out.append((B,mass*(n-k)*(a0-O0-4*phase)/(K*aa**4),mass*k*(O1-a1-4*phase)/(K*aa**4)))
 return out

def own_phase_bound(k,n,t,s0,s1,O0,O1,a0,a1,V,intercept,drift,mass,multiplier,vertices):
 need(type(k)is int and 0<=k<=n and vertices and 0<=mass<=1 and multiplier>0,'joint quartic phase scope')
 best=None
 for aa in(F(i,20)for i in range(2,25)):
  forms=score_forms(k,n,t,s0,s1,O0,O1,a0,a1,V,intercept,drift,mass,aa)
  bound=max(B+cx*x+cy*y for x,y in vertices for B,cx,cy in forms)
  best=bound if best is None else min(best,bound)
  if up(multiplier*max(F(0),best))<CE_LO:return best
 return best

def own_normalized_bound(k,n,t,s0,s1,O0,O1,a0,a1,V,intercept,drift,mass,vertices):
 need(type(k)is int and 0<=k<=n and vertices and 0<=mass<=1,'normalized quartic scope')
 sn=root(F(n),10**12)[1];best=None
 for aa in(F(i,20)for i in range(2,25)):
  forms=score_forms(k,n,t,s0,s1,O0,O1,a0,a1,V,intercept,drift,mass,aa)
  bound=max(up(sn*max(F(0),max(B+cx*x+cy*y for B,cx,cy in forms))/rho)for x,y,rho in vertices)
  best=bound if best is None else min(best,bound)
  if best<CE_LO:return best
 return best
