"""Exact same-law signed cubic strip; no independent resource acquisition."""
from fractions import Fraction as F
from math import isqrt
def need(ok,msg):
 if not ok:raise ValueError(msg)
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[1],-a[0])
def mul(a,b):
 v=[x*y for x in a for y in b];return(min(v),max(v))
def roots(x,scale=10**16):
 need(type(x)is F and x>0,'positive exact root');a=F(isqrt(x.numerator*scale*scale//x.denominator),scale);b=a+F(1,scale)
 need(a*a<=x<=b*b,'outward root bracket');return a,b
def strip(pl,pu,sl,sh,s0l,s0h,s1l,s1h,gl,gh,xl,xh,yl,yh):
 need(all(type(x)is F for x in(pl,pu,sl,sh,s0l,s0h,s1l,s1h,gl,gh,xl,xh,yl,yh)),'exact rational signed cubic arguments')
 need(0<pl<=pu<1 and 0<=sl<=sh and 0<=s0l<=s0h and 0<=s1l<=s1h and gl<=gh and xl<=xh and yl<=yh,'closed same-law signed cubic domain')
 vl=min(pl*(1-pl),pu*(1-pu));vh=F(1,4)if pl<=F(1,2)<=pu else max(pl*(1-pl),pu*(1-pu));v=(vl,vh)
 h3=(roots((vl+sl)**3)[0],roots((vh+sh)**3)[1])
 base=add(mul(v,(1-2*pu,1-2*pl)),mul((3*vl,3*vh),(s1l-s0h,s1h-s0l)))
 t=add(mul((gl,gh),h3),neg(base));pm=(pl+pu)/2;error=(pu-pl)/2*max(abs(yl-xh),abs(yh-xl))
 return dict(coefficients=(1-pm,pm),lower=t[0]-error,upper=t[1]+error,midpoint_error=error)
def clip(poly,pl,pu,s,s0,s1,gl,gh):
 from joint_cubic_defect import polygon_vertices
 xl,xh=poly['cubic0'];yl,yh=poly['cubic1']
 z=strip(pl,pu,s.l,s.h,s0.l,s0.h,s1.l,s1.h,gl,gh,xl,xh,yl,yh);cx,cy=z['coefficients']
 planes=list(poly['halfplanes'])+[(cx,cy,z['upper']),(-cx,-cy,-z['lower'])]
 result=dict(poly);result.update(halfplanes=planes,vertices=polygon_vertices(planes),signed_gamma_strip=z)
 return result
