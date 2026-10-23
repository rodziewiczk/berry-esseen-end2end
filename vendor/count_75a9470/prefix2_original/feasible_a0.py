from fractions import Fraction as F

def necessity_floor(n,pl,lo,ah,outward):
 assert type(n)is int and n>0
 assert all(type(x)is F for x in(pl,lo,ah,outward))
 assert 0<pl<1 and lo>=0 and 0<=ah<=1 and outward>=0
 v=lo*(1-ah)/(n*(1-pl))
 if outward==0:return dict(physical_empty=v>0,floor=F(0),variance_floor=v)
 return dict(physical_empty=False,floor=v/outward,variance_floor=v)

def propose(n,pl,lo,ah,outward,raw_lower,raw_upper,inward_upper):
 assert all(type(x)is F for x in(raw_lower,raw_upper,inward_upper))
 assert 0<=raw_lower<=raw_upper and inward_upper>=0
 result=necessity_floor(n,pl,lo,ah,outward)
 left=max(raw_lower,result['floor']);right=min(raw_upper,inward_upper)
 if result['physical_empty']or left>right:return dict(**result,feasible=(left,right),cut=None)
 cut=(left+right)/2
 return dict(**result,feasible=(left,right),cut=cut if raw_lower<cut<raw_upper else None)
