"""Exact concave inward polynomial minimum on a clipped closed rectangle."""
from fractions import Fraction as F

def need(ok,message):
    if not ok: raise ValueError(message)

def polynomial(a,b):
    return a+b-a*a-b*b-a*b

def minimum(l0,u0,l1,u1,d):
    need(all(type(x)is F for x in(l0,u0,l1,u1,d)), 'exact rational inward endpoints')
    need(0<=l0<=u0 and 0<=l1<=u1 and l0+l1<=d<1, 'nonempty inward polygon with d<1')
    candidates={(a,b)for a in(l0,u0)for b in(l1,u1)}
    candidates.update((a,d-a)for a in(l0,u0))
    candidates.update((d-b,b)for b in(l1,u1))
    vertices=sorted((a,b)for a,b in candidates if l0<=a<=u0 and l1<=b<=u1 and a+b<=d)
    need(vertices, 'nonempty closed polygon vertex list')
    value=min(polynomial(a,b)for a,b in vertices)
    need(value>=0, 'nonnegative inward term on d<1')
    return value,vertices
