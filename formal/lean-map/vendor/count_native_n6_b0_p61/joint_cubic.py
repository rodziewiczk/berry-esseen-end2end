"""Proposed exact common-rho cubic polytope. Diagnostic, not an accepted theorem.
All bounds concern one pair of conditional mean-zero residual marginals.
"""
from probability_extrema import variance_extrema
from exact_count_core_v5 import *

def cubic_interval(w,L,U):
 need(0<=w.l<=w.h and L>=0 and U>=0,'conditional cubic box domain')
 if L==0 or U==0:
  need(w.l==0,'zero support endpoint requires zero actual variance')
  return F(0),F(0)
 x=max(w.l,min(w.h,L*L/2));lower=x*x/L-L*x
 x=max(w.l,min(w.h,U*U/2));upper=U*x-x*x/U
 need(lower<=upper,'nonempty cubic moment interval')
 return lower,upper

def rectangle_strip_vertices(xlo,xhi,ylo,yhi,cx,cy,lo,hi):
 need(xlo<=xhi and ylo<=yhi and lo<=hi,'closed rectangle and strip')
 corners=[(xlo,ylo),(xhi,ylo),(xhi,yhi),(xlo,yhi)]
 def f(z):return cx*z[0]+cy*z[1]
 points=set(z for z in corners if lo<=f(z)<=hi)
 for a,b in zip(corners,corners[1:]+corners[:1]):
  fa,fb=f(a),f(b)
  if fa==fb:continue
  for bound in(lo,hi):
   t=(bound-fa)/(fb-fa)
   if 0<=t<=1:
    z=tuple(a[j]+t*(b[j]-a[j])for j in range(2))
    need(xlo<=z[0]<=xhi and ylo<=z[1]<=yhi and lo<=f(z)<=hi,'closed exact strip vertex')
    points.add(z)
 return sorted(points)

def moment_polytope(pl,pu,s,s0,s1,O0,O1,a0,a1,rhol,rhoh):
 need(0<pl<=pu<1 and 1<=rhol<=rhoh,'actual probability and rho scope')
 xl,xh=cubic_interval(s0,O0,a0);yl,yh=cubic_interval(s1,a1,O1)
 vl,vh=variance_extrema(pl,pu)
 h3l=root((vl+s.l)**3,10**15)[0];h3h=root((vh+s.h)**3,10**15)[1]
 base_l=vl*(1-2*vl);base_h=vh*(1-2*vh)
 tl=rhol*h3l-base_h-3*vh*(s0.h+s1.h)
 th=rhoh*h3h-base_l-3*vl*(s0.l+s1.l)
 mid=(pl+pu)/2;error=(pu-pl)/2*max(abs(xl+yl),abs(xh+yh))
 need(tl<=th,'actual signed cubic strip order')
 vertices=rectangle_strip_vertices(xl,xh,yl,yh,-(1-mid),mid,tl-error,th+error)
 return dict(vertices=vertices,cubic0=(xl,xh),cubic1=(yl,yh),strip=(tl-error,th+error),coefficients=(-(1-mid),mid),phase_free_error=error)

def own_phase_bound(k,n,t,s0,s1,O0,O1,a0,a1,V,intercept,drift,mass,multiplier,vertices):
 need(type(k)is int and 0<=k<=n and vertices and 0<=mass<=1 and multiplier>0,'joint quartic phase scope')
 V0=(n-k)*s0;V1=k*s1;V=intersect(V,V0+V1);J=(n-k)*s0**2+k*s1**2
 support_cost=(n-k)*O0*a0*s0+k*a1*O1*s1
 best=None
 for aa in(F(i,20)for i in range(2,25)):
  point=max(V.l,min(V.h,aa*aa/2))
  concave=I(min(3*aa*aa*x-3*x*x for x in(V.l,V.h)),3*aa*aa*point-3*point*point)
  cases=[]
  for m0,m1 in vertices:
   third=(n-k)*m0+k*m1
   co=[concave+3*J-support_cost-(n-k)*(a0-O0)*m0-k*(O1-a1)*m1,I(4*third-2*aa**3),3*aa*aa-6*V,I(0),I(-1)]
   score=[-mass*x/(K*aa**4)for x in co];score[0]=score[0]+intercept;score[1]=score[1]+drift
   cases.append(-bernstein_interval_min([-x for x in score],t.l,t.h))
  bound=max(cases);best=bound if best is None else min(best,bound)
  if up(multiplier*max(F(0),best))<CE_LO:return best
 return best
