"""Exact elementary conditional variance geometry. No acquisition occurs here."""
from fractions import Fraction as F

def need(x,m):
 if not x:raise ValueError(m)
def validate(n,p,A,d0,Lambda):
 raise RuntimeError('Legacy variance geometry is disabled in this capsule')
 need(type(n)is int and n>=2,'integer sample size')
 need(all(type(x)is F for x in(p,A,d0,Lambda)),'rational inputs')
 need(0<p<=F(1,2) and A>0 and d0>0 and Lambda>0,'positive geometry')
def ceiling(N,p,A,d0,Lambda):
 """Weighted premise (n/N)d/d0+lambda/Lambda<=1, n>=N."""
 validate(N,p,A,d0,Lambda)
 return 1/(1/Lambda+1/(N*A*(1-p)*d0))
def allocation_ceiling(N,p,A,d0,Lambda,alpha):
 validate(N,p,A,d0,Lambda);need(type(alpha)is F and 0<=alpha<=1,'allocation')
 return 1/(1/Lambda+((1-alpha)/(1-p)+alpha/p)/(N*A*d0))
def allocation_limit(N,p,A,d0,Lambda,lam):
 validate(N,p,A,d0,Lambda);need(type(lam)is F and 0<lam<=Lambda,'noise')
 if p==F(1,2):return F(1)if lam<=ceiling(N,p,A,d0,Lambda)else F(-1)
 return (N*A*d0*(1/lam-1/Lambda)-1/(1-p))/(1/p-1/(1-p))
def row_cap(row,N):
 pl,pu=map(F,row['p']);A=F(row['amplitude']);d0=F(row['d0']);lm=F(row['lambda_max'])
 need(pl<pu,'nonempty p interval')
 profiles=[(F(0),F('.05'),A),(F('.05'),F('.08'),min(A,F('.45'))),(F('.08'),F('.10'),min(A,F('.40'))),(F('.10'),F('.12'),min(A,F('.35'))),(F('.12'),F('.125'),min(A,F('.3125'))),(F('.125'),lm,min(A,F('.30')))]
 out=[]
 for lo,hi,a in profiles:
  hi=min(hi,lm)
  if hi<lo:continue
  cap=ceiling(N,pl,a,d0,lm)
  out.append(dict(lo=str(lo),hi=str(hi),amplitude=str(a),cap=str(cap),empty=cap<lo,feasible_upper=str(min(hi,cap))))
 return dict(index=row['index'],p=row['p'],original_ceiling=str(lm),new_ceiling=str(max(F(x['feasible_upper'])for x in out if not x['empty'])),bands=out)
