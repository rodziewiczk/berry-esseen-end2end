"""Exact runtime special case for point/scalar interval operations."""
from fractions import Fraction as F
from exact_count_core_v5 import I
OLD_MUL=I.__mul__
def multiply(self,b):
 if isinstance(b,I):
  if b.l!=b.h:return OLD_MUL(self,b)
  scalar=b.l
 else:scalar=F(b)
 return I(self.l*scalar,self.h*scalar)if scalar>=0 else I(self.h*scalar,self.l*scalar)
def add(self,b):
 if isinstance(b,I):return I(self.l+b.l,self.h+b.h)
 scalar=F(b);return I(self.l+scalar,self.h+scalar)
def apply():
 I.__mul__=multiply;I.__rmul__=multiply;I.__add__=add;I.__radd__=add
