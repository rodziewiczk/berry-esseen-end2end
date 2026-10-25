"""Exact finite-binomial Berry--Esseen upper envelopes. No floating arithmetic.
Monotone endpoint enclosure in p; finite Gaussian integral Taylor enclosure.
"""
from fractions import Fraction as F
from math import isqrt,comb
S=10**30
Z=10**12

def ceildiv(a,b):return -((-a)//b)
def root(x,scale=S):
 assert x>=0
 k=isqrt(x.numerator*scale*scale//x.denominator)
 assert F(k,scale)**2<=x<F(k+1,scale)**2
 return F(k,scale),F(k+1,scale)
def atan_interval(q,m):
 # First2m terms undershoot; the next positive term bounds the remainder.
 a=sum((F((-1)**k,(2*k+1)*q**(2*k+1))for k in range(2*m)),F(0))
 return a,a+F(1,(4*m+1)*q**(4*m+1))
a,b=atan_interval(5,24);c,d=atan_interval(239,8)
PI_LO,PI_HI=16*a-4*d,16*b-4*c
PHI_LO=root(1/(2*PI_HI))[0];PHI_HI=root(1/(2*PI_LO))[1]
CE_LO=(3+root(F(10))[0])*PHI_LO/6
assert F('.398942280401432677939946059934')<=PHI_LO<PHI_HI<=F('.398942280401432677939946059935')
TAIL=F(3,10**7)
# Mills at5: tail<phi(0)*exp(-25/2)/5<3e-7.
EXP_LO=sum((F(25,2)**k/__import__('math').factorial(k)for k in range(61)),F(0))
assert PHI_HI/(5*EXP_LO)<TAIL

def positive_cdf(t):
 """t is an exact nonnegative multiple of1/Z; lower/upper on scaleS."""
 assert type(t)is int and 0<=t<=5*Z
 if t==0:return S//2,S//2
 # Integrate the degree159 alternating Taylor polynomial for exp(-x*x/2).
 # Term80 gives a rigorous absolute remainder bound, for all t in[0,5].
 lo=t*S//Z;hi=ceildiv(t*S,Z);sl=sh=0
 for k in range(80):
  if k%2:sl-=hi;sh-=lo
  else:sl+=lo;sh+=hi
  den=2*(k+1)*(2*k+3)*Z*Z
  mul=t*t*(2*k+1)
  lo=lo*mul//den;hi=ceildiv(hi*mul,den)
 sl-=hi;sh+=hi
 assert sl>=0
 low=S//2+(sl*PHI_LO.numerator)//PHI_LO.denominator
 high=S//2+ceildiv(sh*PHI_HI.numerator,PHI_HI.denominator)
 return max(0,low),min(S,high)

def cdf_at(n,j,pnum,M):
 """Enclose Phi((j-np)/sqrt(npq)) in integers overS."""
 a=j*M-n*pnum;D=n*pnum*(M-pnum)
 assert D>0
 if a*a>=25*D:
  tail=ceildiv(TAIL.numerator*S,TAIL.denominator)
  return (S-tail,S)if a>=0 else(0,tail)
 rr=isqrt(D*Z*Z)
 # Absolute z endpoints on grid1/Z, with exact directed rational rounding.
 l=abs(a)*Z*Z//(rr+1);u=ceildiv(abs(a)*Z*Z,rr)
 lo=positive_cdf(l)[0];hi=positive_cdf(min(5*Z,u))[1]
 return (lo,hi)if a>=0 else(S-hi,S-lo)

def endpoint(n,pnum,M):
 assert 0<pnum<M
 den=M**n;b=(M-pnum)**n;cum=0;rows=[]
 for j in range(n+1):
  prev=cum;cum+=b;phlo,phhi=cdf_at(n,j,pnum,M)
  rows.append((prev*S//den,ceildiv(prev*S,den),cum*S//den,ceildiv(cum*S,den),phlo,phhi))
  if j<n:
   num=b*(n-j)*pnum;div=(j+1)*(M-pnum)
   assert num%div==0
   b=num//div
 assert cum==den
 return rows

def panel(n,idx,subdiv):
 raise RuntimeError('Legacy finite Gaussian panel API is disabled in this capsule')
 assert type(n)is int and n>=1 and type(idx)is int and 0<idx<250
 assert type(subdiv)is int and subdiv>0
 M=500*subdiv;first=idx*subdiv;last=(idx+1)*subdiv
 left=endpoint(n,first,M);best=F(-1);where=None
 for a in range(first,last):
  right=endpoint(n,a+1,M)
  v=F((a+1)*(M-a-1),M*M)
  factor=root(n*v)[1]/(1-2*v)
  for j in range(n+1):
   # F_j decreases withp, as doesz_j. Both closed jump sides included.
   positive=F(max(0,left[j][3]-right[j][4]),S)*factor
   negative=F(max(0,left[j][5]-right[j][0]),S)*factor
   for sign,x in (('+',positive),('-',negative)):
    if x>best:best=x;where=[a,j,sign]
  left=right
 cap=F(ceildiv(best.numerator*10**9,best.denominator),10**9)
 epsilon=F((CE_LO-cap).numerator*10**9//(CE_LO-cap).denominator,10**9)
 assert epsilon>0
 return dict(n=n,index=idx,p=[str(F(idx,500)),str(F(idx+1,500))],subdivisions=subdiv,score_cap=str(cap),epsilon=str(epsilon),maximizing_box=where,closed_boxes=subdiv*(n+1)*2)
