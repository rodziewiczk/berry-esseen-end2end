"""Diagnostic: common cubic moments also constrain the positive score denominator.
Requires same-law polygon from joint_cubic_defect; no acceptance use yet.
"""
from probability_extrema import variance_extrema
from joint_cubic_defect import *

def normalized_polytope(poly,pl,pu,s,s0,s1,rhol):
 need(rhol>0 and 0<pl<=pu<1,'positive normalization scope')
 vl,vh=variance_extrema(pl,pu)
 base=vl*(1-2*vl)+3*vl*(s0.l+s1.l)
 h3=root((vh+s.h)**3,10**15)[1]
 need(h3>0,'positive denominator upper')
 cx,cy=poly['coefficients'];offset=base-poly['phase_free_error']
 switch=h3*rhol-offset
 planes=poly['halfplanes']
 vertices=sorted(set(polygon_vertices(planes+[(cx,cy,switch)])+polygon_vertices(planes+[(-cx,-cy,-switch)])))
 out=[]
 for x,y in vertices:
  lower=max(rhol,(offset+cx*x+cy*y)/h3)
  need(lower>0,'positive affine denominator on both pieces')
  out.append((x,y,lower))
 return out

def own_normalized_bound(k,n,t,s0,s1,O0,O1,a0,a1,V,intercept,drift,mass,vertices):
 need(type(k)is int and 0<=k<=n and vertices and 0<=mass<=1,'normalized quartic scope')
 V0=(n-k)*s0;V1=k*s1;V=intersect(V,V0+V1);J=(n-k)*s0**2+k*s1**2
 support_cost=(n-k)*O0*a0*s0+k*a1*O1*s1
 sn=root(F(n),10**12)[1];best=None
 for aa in(F(i,20)for i in range(2,25)):
  point=max(V.l,min(V.h,aa*aa/2))
  concave=I(min(3*aa*aa*x-3*x*x for x in(V.l,V.h)),3*aa*aa*point-3*point*point)
  cases=[]
  for m0,m1,rho in vertices:
   third=(n-k)*m0+k*m1
   co=[concave+3*J-support_cost-(n-k)*(a0-O0)*m0-k*(O1-a1)*m1,I(4*third-2*aa**3),3*aa*aa-6*V,I(0),I(-1)]
   score=[-mass*x/(K*aa**4)for x in co];score[0]=score[0]+intercept;score[1]=score[1]+drift
   numerator=-bernstein_interval_min([-x for x in score],t.l,t.h)
   cases.append(up(sn*max(F(0),numerator)/rho))
  bound=max(cases);best=bound if best is None else min(best,bound)
  if best<CE_LO:return best
 return best
