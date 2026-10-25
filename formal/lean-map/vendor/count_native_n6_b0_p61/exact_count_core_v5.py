"""Exact rational direct-count rectangle bounds; no floating arithmetic."""
from probability_extrema import variance_extrema
from fractions import Fraction as F
from functools import lru_cache
from math import comb,factorial
from finite_gaussian import root,positive_cdf,CE_LO,S,Z,PHI_LO,PHI_HI
from variance_geometry import need
SCALE=10**12
K=F(9)/(4*F('.4641'))
need((F(2,3)*(K-F(9,4)))**2>3,'quartic global maximum')
def up(x):return F(-((-x.numerator*SCALE)//x.denominator),SCALE)
def down(x):return F(x.numerator*SCALE//x.denominator,SCALE)
class I:
 def __init__(self,a,b=None):
  self.l=F(a);self.h=self.l if b is None else F(b);need(self.l<=self.h,'interval order')
 def __add__(self,b):
  b=cast(b);return I(self.l+b.l,self.h+b.h)
 __radd__=__add__
 def __neg__(self):return I(-self.h,-self.l)
 def __sub__(self,b):return self+-cast(b)
 def __rsub__(self,b):return cast(b)+-self
 def __mul__(self,b):
  b=cast(b);v=[x*y for x in(self.l,self.h)for y in(b.l,b.h)];return I(min(v),max(v))
 __rmul__=__mul__
 def __truediv__(self,b):
  b=cast(b);need(b.l>0,'positive interval denominator');return self*I(1/b.h,1/b.l)
 def __pow__(self,n):
  need(type(n)is int and n>=0,'integer power')
  if n==0:return I(1)
  if n%2==0:
   return I(0 if self.l<=0<=self.h else min(self.l**n,self.h**n),max(self.l**n,self.h**n))
  return I(self.l**n,self.h**n)
def cast(x):return x if isinstance(x,I)else I(x)
@lru_cache(None)
def exp_upper(x):
 need(x>=0 and x<50,'exp directed Taylor range below50')
 terms=[x**i/F(factorial(i))for i in range(49)];tail=x**49/F(factorial(49))/(1-x/50)
 return up(sum(terms,F(0))+tail)
@lru_cache(None)
def exp_lower(x):
 need(x>=0,'positive exponential argument')
 return down(sum((x**i/F(factorial(i))for i in range(49)),F(0)))
@lru_cache(None)
def normal_lower(num,den):
 need(den>0,'normal variance');a,b=root(den,10**15)
 if num>=0:
  z=num/b;t=z.numerator*Z//z.denominator;need(t<=5*Z,'normal compact range');return F(positive_cdf(t)[0],S)
 z=-num/a;t=-((-z.numerator*Z)//z.denominator);need(t<=5*Z,'normal compact range');return 1-F(positive_cdf(t)[1],S)
@lru_cache(None)
def masses(n,pl,pu):
 need(type(n)is int and n>=2 and 0<pl<=pu<1,'mass domain')
 out=[];cum=F(0)
 for j in range(n+1):
  def value(p):return F(comb(n,j))*p**j*(1-p)**(n-j)
  a=value(pl);b=value(pu);cum+=a;hi=max(a,b)
  if pl<=F(j,n)<=pu:hi=max(hi,value(F(j,n)))
  out.append((min(a,b),hi,cum))
 return out

def intersect(*vals):
 lo=max(x.l for x in vals);hi=min(x.h for x in vals)
 need(lo<=hi,'consistent simultaneous interval bounds')
 return I(lo,hi)

def bernstein_interval_min(co,lo,hi):
 width=hi-lo
 a=[sum((co[j]*F(comb(j,i))*lo**(j-i)*width**i for j in range(i,5)),I(0))for i in range(5)]
 return min(sum((a[j]*F(comb(i,j),comb(4,j))for j in range(i+1)),I(0)).l for i in range(5))

def probability_upper(j,n,t,s0,s1,A,d,V):
 V0=(n-j)*s0;V1=j*s1;V=intersect(V,V0+V1);J=(n-j)*s0**2+j*s1**2
 cut0=(d-A)/4;cut1=(A-d)/4
 xs0=(-A,)if t.l>=cut0 else(d,)if t.h<=cut0 else(-A,d)
 xs1=(-d,)if t.l>=cut1 else(A,)if t.h<=cut1 else(-d,A)
 best=F(0)
 for a in(F(i,20)for i in range(2,25)):
  low=None;vstar=max(V.l,min(V.h,a*a/2))
  concave=I(min(3*a*a*x-3*x*x for x in(V.l,V.h)),3*a*a*vstar-3*vstar*vstar)
  for x0 in xs0:
   for x1 in xs1:
    third=intersect(V0*x0+V1*x1,V*x1+V0*(x0-x1),V*x0+V1*(x1-x0),V*I(min(x0,x1),max(x0,x1)))
    cost=intersect(V0*x0*x0+V1*x1*x1,V*x1*x1+V0*(x0*x0-x1*x1),V*x0*x0+V1*(x1*x1-x0*x0),V*I(min(x0*x0,x1*x1),max(x0*x0,x1*x1)))
    co=[concave+3*J-cost,4*third-2*a**3,3*a*a-6*V,I(0),I(-1)]
    z=bernstein_interval_min(co,t.l,t.h)/(K*a**4);low=z if low is None else min(low,z)
  best=max(best,low)
 upper=min(F(1),1-best)
 if t.h<0:upper=min(upper,V.h/(V.h+t.h*t.h))
 need(upper>=0,'nonnegative CDF upper bound')
 return upper

@lru_cache(None)
def maximum_mgf(n,j,r0,r1,al,ah):
 need(r0>=0 and r1>=0 and 0<=al<=ah<=1,'MGF allocation domain')
 points=[al,ah]
 if r0*r1:
  point=(j*r1*(1+r0)-(n-j)*r0)/(n*r0*r1)
  if al<=point<=ah:points.append(point)
 return up(max((1+r0*(1-aa))**(n-j)*(1+r1*aa)**j for aa in points))

@lru_cache(None)
def incoming_constants(n,k,pl,pu,hi,al,ah,A,d):
 ms=masses(n,pl,pu);out=[]
 for z in(F(2),F(4),F(6),F(8)):
  r0=up(hi/(n*(1-pu)*A**2)*(exp_upper(z*A)-1-z*A))
  r1=up(hi/(n*pl*d**2)*(exp_upper(z*d)-1-z*d))if d else F(0)
  tail=sum((ms[j][1]*maximum_mgf(n,j,r0,r1,al,ah)/exp_lower(z*(j-k))for j in range(k+1,n+1)),F(0))
  out.append((z,up(tail)))
 return tuple(out)

@lru_cache(None)
def centered_binomial_gaussian(n,k,pl,pu,ul,lo,hi):
 """Upper F_k(p)-Phi((k+ul-np)/sqrt(npq+lambda)), preserving p.
 For each p, its maximum over lambda is at an endpoint.  On each
 endpoint slice use the exact midpoint value plus a derivative interval.
 """
 pm=(pl+pu)/2; width=(pu-pl)/2; pp=I(pl,pu)
 ms=masses(n,pl,pu); cdfmid=masses(n,pm,pm)[k][2]
 bd=-I((n-k)*ms[k][0],(n-k)*ms[k][1])/(1-pp)
 answers=[]
 for lam in sorted(set((lo,hi))):
  vl,vh=variance_extrema(pl,pu);den=I(n*vl+lam,n*vh+lam)
  sr=I(root(den.l,10**12)[0],root(den.h,10**12)[1])
  num=k+ul-n*pp; exponent=num**2/(2*den)
  phi=I(PHI_LO/exp_upper(up(exponent.h)),PHI_HI/exp_lower(down(exponent.l)))
  derivative=bd+phi*(I(n)/sr+num*n*(1-2*pp)/(2*den*sr))
  deviation=max(abs(derivative.l),abs(derivative.h))*width
  midpoint=cdfmid-normal_lower(k+ul-n*pm,n*pm*(1-pm)+lam)
  answers.append(up(midpoint+deviation))
 return max(answers)

def cell(n,pl,pu,lo,hi,al,ah,k,ul,uh,A,d0,Lambda,Hminus,Hplus):
 raise RuntimeError('Legacy cell is disabled; use the reviewed generalized cell35')
 need(type(n)is int and n>=2 and type(k)is int and 0<=k<=n,'integer count domain')
 need(all(type(x)is F for x in(pl,pu,lo,hi,al,ah,ul,uh,A,d0,Lambda,Hminus,Hplus)),'rational cell')
 need(0<pl<=pu<1 and 0<=lo<=hi<=Lambda and 0<=al<=ah<=1 and -F(1,2)<=ul<=uh<=F(1,2),'closed parameter cell')
 need(0<A<1 and 0<d0<pl and Lambda>0,'support/resource domain')
 d=d0*(1-lo/Lambda)
 alloclo=1/(1-pl)+al*(1/pu-1/(1-pu))
 if lo*alloclo>n*A*d:return dict(status='EMPTY_VARIANCE_GEOMETRY')
 vl,vh=variance_extrema(pl,pu)
 hrawroot=root(vh+hi/n,10**12)[1]
 if k+ul-n*pu>Hplus*hrawroot or k+uh-n*pl< -Hminus*hrawroot:return dict(status='EMPTY_COUNT_PHASE')
 s=I(lo/n,hi/n);p=I(pl,pu);alpha=I(al,ah);s0=s*(1-alpha)/(1-p);s1=s*alpha/p
 # Feasibility yields each individual variance<=A*d, in addition to allocation.
 if s0.l>A*d or s1.l>A*d:return dict(status='EMPTY_VARIANCE_GEOMETRY')
 s0=I(s0.l,min(s0.h,A*d));s1=I(s1.l,min(s1.h,A*d))
 numerator=vl*(1-2*vl)
 coeff=min(3*(pp+(1-2*pp)*aa)for pp in(pl,pu)for aa in(al,ah))-d*max(ah,1-al)
 need(coeff>0,'positive cubic coefficient')
 rholo=max(F(1),(numerator+lo*coeff/n)/root((vh+hi/n)**3,10**12)[1])
 ms=masses(n,pl,pu);cdf=ms[k][2]
 V=I(lo,hi)*(1+(k-n*p)*(alpha-p)/I(n*vl,n*vh))
 V=I(max(F(0),V.l),V.h)
 upper=probability_upper(k,n,I(ul,uh),s0,s1,A,d,V)
 ownloss=ms[k][0]*(1-upper)
 cdf-=ownloss
 tails=[]
 for z,constant in incoming_constants(n,k,pl,pu,hi,al,ah,A,d):
  factor=exp_upper(z*uh)if uh>=0 else 1/exp_lower(-z*uh)
  tails.append(constant*factor)
 incoming=min(tails)
 cdf+=incoming
 num=k+ul-n*pu;den=n*(vh if num>=0 else vl)+ (hi if num>=0 else lo)
 normal=normal_lower(num,den)
 coupled_difference=centered_binomial_gaussian(n,k,pl,pu,ul,lo,hi)-ownloss+incoming
 difference=max(F(0),min(cdf-normal,coupled_difference))
 score=up(root(F(n),10**12)[1]*difference/rholo)
 return dict(status='PASS'if score<CE_LO else'UNRESOLVED',score_upper=str(score),reserve=str(CE_LO-score),rho_lower=str(rholo),CDF_upper=str(up(cdf)),normal_lower=str(down(normal)))
