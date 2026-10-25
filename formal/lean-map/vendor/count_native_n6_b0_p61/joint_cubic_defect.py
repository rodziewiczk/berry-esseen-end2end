"""Proposed exact common-rho and defect-constrained cubic polytope.
Diagnostic composition only. The defect edge is a lower inequality, not identity.
"""
from probability_extrema import variance_extrema
from joint_cubic import *
from itertools import combinations
from inward_triangle import minimum as inward_minimum
SIG_LO,SIG_HI=root(F(10),10**20)

def polygon_vertices(planes):
 need(len(planes)>=4,'bounded polygon includes support rectangle')
 points=set()
 for (a,b,c),(d,e,f) in combinations(planes,2):
  det=a*e-b*d
  if det==0:continue
  x=(c*e-b*f)/det;y=(a*f-c*d)/det
  if all(A*x+B*y<=C for A,B,C in planes):points.add((x,y))
 return sorted(points)

def defect_polytope(pl,pu,s,s0,s1,O0,O1,a0,a1,rhol,rhoh,a0floor,d,Dcap):
 poly=moment_polytope(pl,pu,s,s0,s1,O0,O1,a0,a1,rhol,rhoh)
 xl,xh=poly['cubic0'];yl,yh=poly['cubic1'];rl,rh=poly['strip'];cx,cy=poly['coefficients']
 need(0<=Dcap and 0<=a0floor<=a0 and 0<=a1 and 0<=d<1,'actual defect and inward interval below one')
 l0=max(a0floor,s0.l/O0);l1=s1.l/O1
 need(l0<=a0 and l1<=a1 and l0+l1<=d,'consistent actual inward floors')
 vl,vh=variance_extrema(pl,pu);mid=(pl+pu)/2;width=(pu-pl)/2
 ss=SIG_LO
 co=[I(0),I(ss-1),I(-3*ss-3),I(4*ss+10),I(-2*ss-6)]
 binary=max(F(0),bernstein_interval_min(co,pl,pu))
 inward=inward_minimum(l0,a0,l1,a1,d)[0]
 c0=3*(ss+3)*pl-6*a0;c1=3*(ss+1)*(1-pu)-6*a1
 if not(inward>=0 and c0>=0 and c1>=0):
  planes=[(F(-1),F(0),-xl),(F(1),F(0),xh),(F(0),F(-1),-yl),(F(0),F(1),yh),(-cx,-cy,-rl),(cx,cy,rh)]
  poly.update(vertices=polygon_vertices(planes),halfplanes=planes)
  return poly
 base=binary+6*vl*inward+(1-pu)*s0.l*c0+pl*s1.l*c1
 ax=-(ss+1)*(1-mid);by=(ss-1)*mid
 ex=(SIG_HI-SIG_LO)*(1-pl)+(ss+1)*width
 ey=(SIG_HI-SIG_LO)*pu+(ss-1)*width
 error=ex*max(abs(xl),abs(xh))+ey*max(abs(yl),abs(yh))
 upper=Dcap*root((vh+s.h)**3,10**15)[1]-base+error
 planes=[(F(-1),F(0),-xl),(F(1),F(0),xh),(F(0),F(-1),-yl),(F(0),F(1),yh),(-cx,-cy,-rl),(cx,cy,rh),(ax,by,upper)]
 poly.update(vertices=polygon_vertices(planes),halfplanes=planes,defect_base_lower=base,defect_coefficient_error=error)
 return poly
