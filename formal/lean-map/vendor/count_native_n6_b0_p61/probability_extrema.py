"""Exact variance range of a literal Bernoulli probability interval; no reflection."""
from fractions import Fraction as F

def variance_extrema(pl,pu):
    if not(type(pl)is F and type(pu)is F and 0<pl<=pu<1):
        raise ValueError('exact ordered literal probability interval inside (0,1)')
    left,right=pl*(1-pl),pu*(1-pu)
    lower=min(left,right)
    upper=F(1,4) if pl<=F(1,2)<=pu else max(left,right)
    return lower,upper
