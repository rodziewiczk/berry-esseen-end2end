"""Exact necessary lambda floor from the same-law signed-beta identity."""
from probability_extrema import variance_extrema
from fractions import Fraction as F

def lower_lambda(n,pl,pu,lo,hi,al,ah,bl,bh):
    if not(type(n)is int and n>0 and all(type(x)is F for x in(pl,pu,lo,hi,al,ah,bl,bh))):
        raise ValueError('exact index and rational variance-floor premises')
    if not(0<pl<=pu<1 and 0<=lo<=hi and 0<=al<=ah<=1 and -1<=bl<=bh<=1):
        raise ValueError('ordered variance-floor premises')
    v=variance_extrema(pl,pu)[0];tmin=1-2*pu;tmax=1-2*pl
    cases=[]
    if bh<tmin:cases.append(('low_beta',v*(tmin-bh),bh+1-2*al))
    if bl>tmax:cases.append(('high_beta',v*(bl-tmax),2*ah-1-bl))
    for side,numerator,denominator in cases:
        if denominator<=0:return dict(empty=True,reason=side+'_nonpositive_denominator')
        lo=max(lo,n*numerator/denominator)
        if lo>hi:return dict(empty=True,reason=side+'_lambda_floor',lambda_lower=str(lo),lambda_upper=str(hi))
    return dict(empty=False,lo=lo)
