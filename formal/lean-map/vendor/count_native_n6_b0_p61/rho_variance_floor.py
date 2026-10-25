"""Exact necessary lambda lower bound from rho and outward conditional caps."""
from probability_extrema import variance_extrema
from fractions import Fraction as F
from math import isqrt

def root_lower(x,grid=10**18):
    if type(x)is not F or x<0 or type(grid)is not int or grid<=0:
        raise ValueError('nonnegative exact square root and positive grid')
    return F(isqrt(x.numerator*grid*grid//x.denominator),grid)

def lower_lambda(n,pl,pu,lo,hi,al,ah,rho_lower,outer0,outer1):
    xs=(pl,pu,lo,hi,al,ah,rho_lower,outer0,outer1)
    if type(n)is not int or n<=0 or not all(type(x)is F for x in xs):
        raise ValueError('exact index and rational noise-floor premises')
    if not(0<pl<=pu<1 and 0<=lo<=hi and 0<=al<=ah<=1
           and rho_lower>0 and outer0>0 and outer1>0):
        raise ValueError('ordered probability/noise/moment premises')
    v=variance_extrema(pl,pu)[0];t=root_lower(v)
    A=rho_lower*v*t-v+2*v*v
    if A<=0:return dict(empty=False,lo=lo)
    assert F(3,2)*rho_lower*t-1+4*v>0
    M=max((3*p+outer0)*(1-a)+(3*(1-p)+outer1)*a
          for p in(pl,pu)for a in(al,ah))
    B=M-F(3,2)*rho_lower*t
    if B<=0:return dict(empty=True,reason='rho_floor_nonpositive_coefficient')
    floor=n*A/B;lo=max(lo,floor)
    if lo>hi:return dict(empty=True,reason='rho_floor_above_noise_upper',lambda_lower=str(lo),lambda_upper=str(hi))
    return dict(empty=False,lo=lo)
