"""Exact necessary rho quadratic retaining a common inward budget."""
from fractions import Fraction as F
from math import isqrt
def need(x,m):
    if not x:raise ValueError(m)
def roots(x):
    need(type(x)is F and x>0,'positive exact root')
    g=10**12;a=F(isqrt(x.numerator*g*g//x.denominator),g)
    b=a if a*a==x else a+F(1,g)
    need(0<a and a*a<=x<=b*b,'root bracket');return a,b
def minimum(c0,c1,c2,l,u):
    values=[c0+c1*l+c2*l*l,c0+c1*u+c2*u*u]
    if c2>0 and l<-c1/(2*c2)<u:values.append(c0-c1*c1/(4*c2))
    return min(values)
def test(pl,pu,al,ah,sl,sh,d,R):
    need(all(type(x)is F for x in(pl,pu,al,ah,sl,sh,d,R)),'rational box')
    need(0<pl<=pu<1 and 0<=al<=ah<=1 and 0<=sl<=sh and d>0 and R>0,'moment box domain')
    vl=min(pl*(1-pl),pu*(1-pu));vh=F(1,4)if pl<=F(1,2)<=pu else max(pl*(1-pl),pu*(1-pu))
    B=min(3*p*(1-a)+3*(1-p)*a-d*max(a,1-a)for p in(pl,pu)for a in(al,ah))
    r0=1/roots(1-pl)[1];r1=1/roots(pu)[1]
    H=min((1-a)*r0+a*r1 for a in(al,ah))**2
    t,T=roots(vh);c0=vl*(1-2*vl)-R*vh*T;c1=B-F(3,2)*R*T;c2=H/d-F(3,8)*R/t
    m=minimum(c0,c1,c2,sl,sh)
    return dict(empty=m>0,minimum=m,coefficients=[c0,c1,c2],B_lower=B,H_lower=H,inward_upper=d)
def cell(cfg,pl,pu,lo,hi,al,ah):
    n=cfg['n'];need(type(n)is int and n>=2,'actual integer n')
    L=F(cfg['Lambda']);d0=F(cfg['d0']);D=F(cfg['D'])
    b,g,h=map(F,[cfg[k]for k in('binary_charge','gap_charge','noise_charge')])
    need(L>0 and d0>0 and g>0 and b>=0 and h>=0 and 0<=lo<=hi<=L,'original resource domain')
    d=min(d0*(1-lo/L),(D-b-h*lo)/g)
    if d<=0:return dict(empty=False,reason='defer_zero_inward_endpoint_to_original_kernel')
    return test(pl,pu,al,ah,lo/n,hi/n,d,F(cfg['rho_upper']))
