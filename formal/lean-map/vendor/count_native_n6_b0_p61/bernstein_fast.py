"""Exact scalar implementation of the existing degree-four interval transform."""
from fractions import Fraction as F
from functools import lru_cache
from math import comb
from exact_count_core_v5 import I,need
@lru_cache(None)
def weights(lo,hi):
 need(lo<=hi,'ordered phase interval')
 width=hi-lo
 return tuple(tuple(F(comb(j,i))*lo**(j-i)*width**i for j in range(i,5))for i in range(5))
ELEVATE=tuple(tuple(F(comb(i,j),comb(4,j)) for j in range(i+1))for i in range(5))
def vector(co,lo,hi,upper):
 need(len(co)==5 and all(isinstance(c,I)for c in co),'fixed quartic interval coefficients')
 a=[]
 for i,row in enumerate(weights(lo,hi)):
  a.append(sum(((co[j].h if (w>=0)==upper else co[j].l)*w for j,w in enumerate(row,i)),F(0)))
 return [sum((a[j]*w for j,w in enumerate(row)),F(0))for row in ELEVATE]
def bernstein_interval_min(co,lo,hi):return min(vector(co,lo,hi,False))
def bernstein_upper_vector(co,lo,hi):return vector(co,lo,hi,True)
def apply():
 import sys
 for name in ['exact_count_core_v5','joint_cubic','joint_cubic_defect','joint_cubic_normalized','joint_cubic_normalized_fast','exact35_joint_normalized_fast','discovery_fast_core']:
  m=sys.modules.get(name)
  if m is not None and hasattr(m,'bernstein_interval_min'):m.bernstein_interval_min=bernstein_interval_min
 m=sys.modules.get('joint_cubic_normalized_fast')
 if m is not None:m.bernstein_upper_vector=bernstein_upper_vector
