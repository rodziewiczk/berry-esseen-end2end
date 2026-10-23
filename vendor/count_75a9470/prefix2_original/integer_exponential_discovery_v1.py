"""Exact integer evaluation of existing Taylor polynomials, discovery only.

For x=p/q, P_m=m!*q**m*sum(x**i/i!,i=0..m) satisfies
P_0=1 and P_m=m*q*P_(m-1)+p**m. No rounding occurs in this recurrence.
The upper remainder x**49/(49!*(1-x/50)) equals
50*p**49/(49*D_48*(50*q-p)). The final floor/ceiling is unchanged.
Acceptance is intentionally left on its original frozen implementation.
"""
from fractions import Fraction as F
from functools import lru_cache

def polynomial(x):
    x=F(x);p,q=x.numerator,x.denominator
    P=D=power=1
    for i in range(1,49):
        power*=p;P=i*q*P+power;D*=i*q
    return P,D,p,q,power*p

@lru_cache(None)
def exp_lower(x):
    from exact_count_core_v5 import need,SCALE
    need(x>=0,'positive exponential argument')
    P,D,_,_,_=polynomial(x)
    return F(P*SCALE//D,SCALE)

@lru_cache(None)
def exp_upper(x):
    from exact_count_core_v5 import need,SCALE
    need(x>=0 and x<50,'exp directed Taylor range below50')
    P,D,p,q,p49=polynomial(x)
    factor=49*(50*q-p)
    N=factor*P+50*p49;den=factor*D
    return F(-(-N*SCALE//den),SCALE)

def install():
    import sys
    import exact_count_core_v5 as base
    old_lower,old_upper=base.exp_lower,base.exp_upper
    changed=[]
    for name,module in list(sys.modules.items()):
        if module is None:continue
        for key,old,new in [('exp_lower',old_lower,exp_lower),('exp_upper',old_upper,exp_upper)]:
            if getattr(module,key,None) is old:
                setattr(module,key,new);changed.append((name,key))
    return old_lower,old_upper,changed
