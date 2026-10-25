"""Exact conditional direct count score with common inward gap-D resource.
No acquisition. All bounds refer to the same oriented conditional marginal.
"""
from probability_extrema import variance_extrema
from exact_count_core_v5 import *
import joint_cubic_normalized as joint
from inward_triangle import minimum as inward_minimum
from signed_gamma import clip as signed_gamma_clip
SIG_LO,SIG_HI=root(F(10),10**20)
TARGET=CE_LO
from generalized_scope import validate_resources

def quadratic_cap(cfg,H):
 values=[]
 for qq in cfg['quadratics']:
  A,fp,fm,Q=(F(qq[x])for x in('A','Fplus','Fminus','Qbudget'))
  need(Q>0,'positive quadratic price')
  for l,h,f in ((max(F(0),H.l),H.h,fp),(max(F(0),-H.h),-H.l,fm)):
   if l>h:continue
   x=max(l,min(h,f/(2*Q)));values.append(A+f*x-Q*x*x)
 return min(F(cfg['D']),F(15000,997*int(cfg['n']))*max(values))

def sharp_gates(pl,pu,s0,s1,O0,O1,dmax):
 v=variance_extrema(pl,pu)[0]
 return (6*v*(1-2*dmax)-(1-pl)*(SIG_HI+7)*s0.h-(1-pl)*(SIG_HI+1)*O0**2,
         6*v*(1-2*dmax)-pu*(SIG_HI+5)*s1.h-pu*(SIG_HI-1)*O1**2)

def effective(si,floor,outer):
 a=I(max(floor,si.l/outer),max(floor,si.h/outer))
 # si^2/max(floor,si/outer)=min(si^2/floor,outer*si).
 # This is increasing in si. Zero/zero is its continuous value0.
 ratio=outer*si.l if floor==0 else min(si.l**2/floor,outer*si.l)
 return a,ratio

@lru_cache(None)
def binary_lower(pl,pu):
 ss=SIG_LO
 co=[I(0),I(ss-1),I(-3*ss-3),I(4*ss+10),I(-2*ss-6)]
 return bernstein_interval_min(co,pl,pu)

def sharp_lower(pl,pu,s,s0,s1,a0floor,a1floor,O0,O1):
 """Actual ai>=max(ai_floor,si/Oi); monotonicity is separately gated."""
 v,vh=variance_extrema(pl,pu)
 a0,r0=effective(s0,a0floor,O0);a1,r1=effective(s1,a1floor,O1)
 ss=SIG_LO
 binary=binary_lower(pl,pu)
 # f(a,b)=a+b-a²-b²-ab increases on the entire acquired dmax box.
 inward=a0.l+a1.l-a0.l*a0.l-a1.l*a1.l-a0.l*a1.l
 c1=3*(ss+1)*(1-pu)-(ss+5)*a1.h
 c0=3*(ss+3)*pl-(ss+7)*a0.h
 if not(inward>=0 and c0>0 and c1>0):return None
 raw=binary+6*v*inward+pl*(s1.l*c1+(ss-1)*r1)+(1-pu)*(s0.l*c0+(ss+1)*r0)
 # Actual F is nonnegative: binary square, positive inward term,
 # and the explicitly checked positive coefficients. Thus clamp
 # a negative interval lower endpoint before positive division.
 raw=max(F(0),raw)
 return down(raw/root((vh+s.h)**3,10**12)[1])

def box_sharp_lower(pl,pu,s,s0,s1,l0,u0,l1,u1,d):
 """Termwise actual-endpoint enclosure, independent of sharp monotonicity gates."""
 need(0<pl<=pu<1 and s.l>=0 and s0.l>=0 and s1.l>=0,'box p and variance domain')
 ss=SIG_LO;vl,vh=variance_extrema(pl,pu)
 need(0<=l0<=u0 and 0<=l1<=u1 and l0+l1<=d<1,'actual inward polygon below one')
 c0=3*(ss+3)*pl-(ss+7)*u0;c1=3*(ss+1)*(1-pu)-(ss+5)*u1
 if not(c0>=0 and c1>=0 and 3*pl>=u0 and 3*(1-pu)>=u1):return None
 need(u0>0 or s0.l==0,'zero inward variance0');need(u1>0 or s1.l==0,'zero inward variance1')
 r0=s0.l*s0.l/u0 if u0 else F(0);r1=s1.l*s1.l/u1 if u1 else F(0)
 f=inward_minimum(l0,u0,l1,u1,d)[0]
 raw=binary_lower(pl,pu)+6*vl*f+pl*(s1.l*c1+(ss-1)*r1)+(1-pu)*(s0.l*c0+(ss+1)*r0)
 return down(max(F(0),raw)/root((vh+s.h)**3,10**12)[1])

def bounded_cubic(si,a):
 if a==0:
  need(si.h==0,'zero inward cap forces zero variance');return F(0)
 x=max(si.l,min(si.h,a*a/2))
 return x*x/a-a*x

def cubic_upper(si,outer):
 """Exact maximum of outer*w-w^2/outer on a nonnegative variance interval."""
 need(si.l>=0 and outer>0,'cubic upper domain')
 x=max(si.l,min(si.h,outer*outer/2))
 return outer*x-x*x/outer

def own_cdf(k,n,t,s0,s1,O0,O1,a0,a1,V):
 V0=(n-k)*s0;V1=k*s1;V=intersect(V,V0+V1);J=(n-k)*s0**2+k*s1**2
 cut0=(a0-O0)/4;cut1=(O1-a1)/4
 xs0=(-O0,)if t.l>=cut0 else(a0,)if t.h<=cut0 else(-O0,a0)
 xs1=(-a1,)if t.l>=cut1 else(O1,)if t.h<=cut1 else(-a1,O1)
 best=F(0)
 for a in(F(i,20)for i in range(2,25)):
  low=None;vertex=max(V.l,min(V.h,a*a/2))
  concave=I(min(3*a*a*x-3*x*x for x in(V.l,V.h)),3*a*a*vertex-3*vertex*vertex)
  for x0 in xs0:
   for x1 in xs1:
    third=intersect(V0*x0+V1*x1,V*x1+V0*(x0-x1),V*x0+V1*(x1-x0),V*I(min(x0,x1),max(x0,x1)))
    cost=intersect(V0*x0*x0+V1*x1*x1,V*x1*x1+V0*(x0*x0-x1*x1),V*x0*x0+V1*(x1*x1-x0*x0),V*I(min(x0*x0,x1*x1),max(x0*x0,x1*x1)))
    co=[concave+3*J-cost,4*third-2*a**3,3*a*a-6*V,I(0),I(-1)]
    z=bernstein_interval_min(co,t.l,t.h)/(K*a**4);low=z if low is None else min(low,z)
  best=max(best,low)
 if t.h<0:best=max(best,t.h*t.h/(V.h+t.h*t.h))
 if k:
  for B in map(F,('0','.0025','.005','.01','.02','.03','.04','.05','.075','.1','.15','.2','.3','.5','1')):
   b=t.h+B+(k-1)*a1
   if b< -a1:prob=F(1)
   elif b>=O1:prob=F(0)
   else:prob=max(F(0),(s1.l-a1*b)/((O1+a1)*(O1-b)))
   need(0<=prob<=1,'single strict event probability')
   union=1-(1-prob)**k
   if B==0:buffer=F(1)if V0.h==0 else F(0)
   else:buffer=max(B*B/(V0.h+B*B),B/(B+(n-k)*a0))
   best=max(best,union*buffer)
 need(0<=best<=1,'own strict outgoing lower')
 return 1-best

@lru_cache(None)
def own_mgf_upper(n,k,pl,pu,hi,al,ah,O0,a1,uh):
 """Upper P(W_k<=u), for every u<=uh<0 and common actual alpha."""
 need(type(n)is int and type(k)is int and 0<=k<=n,'own MGF count')
 need(0<pl<=pu<1 and hi>=0 and 0<=al<=ah<=1 and O0>0 and a1>=0 and uh<0,'own MGF domain')
 bounds=[F(1)]
 for z in(F(2),F(4),F(6),F(8)):
  if max(z*O0,z*a1)>=50:continue
  r0=up(hi/(n*(1-pu)*O0**2)*(exp_upper(z*O0)-1-z*O0))
  r1=up(hi/(n*pl*a1**2)*(exp_upper(z*a1)-1-z*a1))if a1 else F(0)
  product=maximum_mgf(n,k,r0,r1,al,ah)
  bounds.append(up(product/exp_lower(-z*uh)))
 return min(bounds)

def incoming_cantelli(n,k,pl,pu,lo,hi,al,ah,uh,s0,s1):
 """Sum closed lower-tail Cantelli bounds at every incoming count."""
 need(type(n)is int and type(k)is int and 0<=k<=n and uh<=F(1,2),'incoming Cantelli count/phase')
 p=I(pl,pu);alpha=I(al,ah);vl,vh=variance_extrema(pl,pu);ms=masses(n,pl,pu);total=F(0)
 for j in range(k+1,n+1):
  direct=(n-j)*s0+j*s1
  coupled=I(lo,hi)*(1+(j-n*p)*(alpha-p)/I(n*vl,n*vh))
  variance=min(direct.h,coupled.h);distance=F(j-k)-uh
  need(variance>=0 and distance>0,'incoming Cantelli positive domains')
  total+=ms[j][1]*variance/(variance+distance*distance)
 return up(total)

def incoming_per_count(n,k,pl,pu,lo,hi,al,ah,ul,uh,s0,s1,O0,a1):
 """Per-count hybrid envelope, preserving phase when derivative gate passes.
 The returned value is combined only with the Gaussian at ul and with
 a constant, cell-wide own-count upper bound in cell35.finish.
 """
 need(type(n)is int and type(k)is int and 0<=k<=n and ul<=uh<=F(1,2),'incoming count/phase')
 p=I(pl,pu);alpha=I(al,ah);vl,vh=variance_extrema(pl,pu);ms=masses(n,pl,pu)
 total=left_total=derivative=F(0);products=[]
 def expo(x):return exp_upper(x)if x>=0 else 1/exp_lower(-x)
 for z in(F(2),F(3),F(4),F(6),F(8)):
  if max(z*O0,z*a1)>=50:continue
  r0=up(hi/(n*(1-pu)*O0**2)*(exp_upper(z*O0)-1-z*O0))
  r1=up(hi/(n*pl*a1**2)*(exp_upper(z*a1)-1-z*a1))if a1 else F(0)
  products.append((z,r0,r1,expo(z*ul),expo(z*uh)))
 for j in range(k+1,n+1):
  direct=(n-j)*s0+j*s1
  coupled=I(lo,hi)*(1+(j-n*p)*(alpha-p)/I(n*vl,n*vh))
  V=min(direct.h,coupled.h);dl=F(j-k)-uh;dh=F(j-k)-ul
  need(V>=0 and dl>0 and dl<=dh,'incoming positive domains')
  right=[V/(V+dl*dl)]
  if V==0:lip=F(0)
  elif V<=3*dl*dl:lip=2*V*dl/(V+dl*dl)**2
  elif V>=3*dh*dh:lip=2*V*dh/(V+dh*dh)**2
  else:lip=F(9,8)/root(3*V,10**15)[0]
  left=[(V/(V+dh*dh),lip)]
  for z,r0,r1,fl,fh in products:
   C=maximum_mgf(n,j,r0,r1,al,ah)/exp_lower(z*(j-k))
   right.append(C*fh);left.append((C*fl,z*C*fh))
  value,lip=min(left,key=lambda x:x[0])
  total+=ms[j][1]*min(right);left_total+=ms[j][1]*value;derivative+=ms[j][1]*lip
 # This differentiates only a frozen smooth upper envelope, not the CDF.
 # All actual p/lambda in this cell have this Gaussian derivative lower.
 T=max(abs(k+ul-n*pu),abs(k+uh-n*pl));exponent=T*T/(2*(n*vl+lo))
 gaussian=F(0)
 if exponent<10:
  gaussian=PHI_LO/(root(n*vh+hi,10**15)[1]*exp_upper(exponent))
  if derivative<=gaussian:total=min(total,left_total)
 # The affine envelope always remains valid, without a derivative-sign gate.
 return up(total),up(left_total),up(derivative),down(gaussian)

def own_phase_upper(k,n,t,s0,s1,O0,O1,a0,a1,V,intercept,drift,mass,multiplier,target=CE_LO):
 """Whole-cell quartic CDF-difference envelope at one common phase.
 Each endpoint case covers its appropriate phase subrange; the maximum
 over every listed case safely covers switch points. Negative quartic
 values remain safe because mass>=0 and outgoing loss>=mass*Q/(K*a^4).
 """
 need(0<=mass<=1 and multiplier>0,'phase mass and normalization')
 V0=(n-k)*s0;V1=k*s1;V=intersect(V,V0+V1);J=(n-k)*s0**2+k*s1**2
 cut0=(a0-O0)/4;cut1=(O1-a1)/4
 xs0=(-O0,)if t.l>=cut0 else(a0,)if t.h<=cut0 else(-O0,a0)
 xs1=(-a1,)if t.l>=cut1 else(O1,)if t.h<=cut1 else(-a1,O1)
 best=None
 for aa in(F(i,20)for i in range(2,25)):
  vertex=max(V.l,min(V.h,aa*aa/2))
  concave=I(min(3*aa*aa*x-3*x*x for x in(V.l,V.h)),3*aa*aa*vertex-3*vertex*vertex)
  cases=[]
  for x0 in xs0:
   for x1 in xs1:
    third=intersect(V0*x0+V1*x1,V*x1+V0*(x0-x1),V*x0+V1*(x1-x0),V*I(min(x0,x1),max(x0,x1)))
    cost=intersect(V0*x0*x0+V1*x1*x1,V*x1*x1+V0*(x0*x0-x1*x1),V*x0*x0+V1*(x1*x1-x0*x0),V*I(min(x0*x0,x1*x1),max(x0*x0,x1*x1)))
    co=[concave+3*J-cost,4*third-2*aa**3,3*aa*aa-6*V,I(0),I(-1)]
    score=[-mass*x/(K*aa**4)for x in co]
    score[0]=score[0]+intercept;score[1]=score[1]+drift
    cases.append(-bernstein_interval_min([-x for x in score],t.l,t.h))
  bound=max(cases);best=bound if best is None else min(best,bound)
  if up(multiplier*max(F(0),best))<target:return best
 return best

def optional_exceeds(lower,upper):
 return lower is not None and lower>upper

def cell35(cfg,pl,pu,lo,hi,al,ah,k,ul,uh,a0l,a0h):
 validate_resources(cfg)
 n=int(cfg['n']);TARGET=CE_LO+F(cfg['K'])/n;Lambda=F(cfg['Lambda']);d0=F(cfg['d0'])
 need(type(k)is int and 0<=k<=n,'actual count')
 need(all(type(x)is F for x in(pl,pu,lo,hi,al,ah,ul,uh,a0l,a0h)),'rational cell')
 need(F(cfg['p'][0])<=pl<=pu<=F(cfg['p'][1]) and 0<=lo<=hi<=Lambda and 0<=al<=ah<=1 and -F(1,2)<=ul<=uh<=F(1,2) and 0<=a0l<=a0h<=d0,'closed selected cell')
 vl,vh=variance_extrema(pl,pu);s=I(lo/n,hi/n);p=I(pl,pu);alpha=I(al,ah)
 sr=I(root(vl+s.l,10**12)[0],root(vh+s.h,10**12)[1]);H=(k+I(ul,uh)-n*p)/sr
 hl=max(H.l,-F(cfg['Hminus']));hh=min(H.h,F(cfg['Hplus']))
 if hl>hh:return dict(status='EMPTY_PHASE')
 H=I(hl,hh);Dcap=quadratic_cap(cfg,H)
 if Dcap<0:return dict(status='EMPTY_NEGATIVE_BUDGET')
 O0=min(F(cfg['outer0']),F(cfg['radius_minus'])*sr.h-pl)
 O1=min(F(cfg['outer1']),F(cfg['radius_plus'])*sr.h-(1-pu))
 need(O0>0 and O1>0,'positive outward caps')
 bcharge,gcharge,hcharge=(F(cfg[key])for key in('binary_charge','gap_charge','noise_charge'))
 need(bcharge>=0 and gcharge>0 and hcharge>0,'positive same-law phase charge')
 budget=Dcap-bcharge-hcharge*lo
 if budget<0:return dict(status='EMPTY_PHASE_RESOURCE')
 rl=F(cfg['rho_lower']);mu=F(cfg['acquired_mean'][1]);gh=F(cfg['acquired_gamma'][1])
 price=max((SIG_LO-1)*rl,SIG_LO*rl-gh)-Dcap
 square=max(F(0),2*rl-2*Dcap/(SIG_LO-1),2*price/(3*mu))
 gap=max(F(cfg['geometry_gap_lower']),root(square,10**12)[0])
 d=min(d0*(1-lo/Lambda),budget/gcharge,F(cfg['acquired_inward_upper']),1-gap*sr.l)
 if d<0:return dict(status='EMPTY_SUPPORT_VARIANCE')
 s0=s*(1-alpha)/(1-p);s1=s*alpha/p
 sign=cfg['sign_premise']
 sign0=pu-F(sign['negative_endpoint_lower'])*sr.l
 sign1=1-pl-F(sign['positive_endpoint_lower'])*sr.l
 a0l=max(a0l,s0.l/O0);a0h=min(a0h,d-s1.l/O1,sign0)
 if a0l>a0h or s1.l>O1*min(d-a0l,sign1):return dict(status='EMPTY_SUPPORT_VARIANCE')
 if s0.l>O0*a0h:return dict(status='EMPTY_SUPPORT_VARIANCE')
 s0=I(s0.l,min(s0.h,O0*a0h));s1=I(s1.l,min(s1.h,O1*(d-a0l)))
 if optional_exceeds(box_sharp_lower(pl,pu,s,s0,s1,a0l,a0h,s1.l/O1,min(d-a0l,sign1),d),Dcap):return dict(status='EMPTY_SHARP_BOX')
 gates=sharp_gates(pl,pu,s0,s1,O0,O1,d)
 if min(gates)>0:
  if optional_exceeds(sharp_lower(pl,pu,s,s0,s1,a0l,F(0),O0,O1),Dcap):return dict(status='EMPTY_SHARP_GAP')
  # Every replacement of upper by mid is separately licensed: sharp lower
  # at max(mid,si/Oi)>Dcap excludes all actual ai>=mid. Internal low need
  # not be a lower bound for the actual ai; only the upper is exported.
  low,upper=a0l,a0h
  for _ in range(12):
   mid=(low+upper)/2
   if optional_exceeds(sharp_lower(pl,pu,s,s0,s1,mid,F(0),O0,O1),Dcap):upper=mid
   else:low=mid
  a0=upper
  low,upper=s1.l/O1,min(d-a0l,sign1)
  for _ in range(12):
   mid=(low+upper)/2
   if optional_exceeds(sharp_lower(pl,pu,s,s0,s1,a0l,mid,O0,O1),Dcap):upper=mid
   else:low=mid
  a1=upper
 else:
  # No sharp-D monotonicity is claimed here. The common displacement
  # and support/variance gates already prove these actual endpoint caps.
  a0=a0h;a1=min(d-a0l,sign1)
 # Every endpoint replacement is licensed by a termwise box lower.
 for _round in range(2):
  if optional_exceeds(box_sharp_lower(pl,pu,s,s0,s1,a0l,a0,s1.l/O1,a1,d),Dcap):return dict(status='EMPTY_SHARP_BOX')
  low,upper=a0l,a0
  for _ in range(12):
   mid=(low+upper)/2
   if optional_exceeds(box_sharp_lower(pl,pu,s,s0,s1,mid,a0,s1.l/O1,a1,d),Dcap):upper=mid
   else:low=mid
  a0=upper
  low,upper=s1.l/O1,a1
  for _ in range(12):
   mid=(low+upper)/2
   if optional_exceeds(box_sharp_lower(pl,pu,s,s0,s1,a0l,a0,mid,a1,d),Dcap):upper=mid
   else:low=mid
  a1=upper
 # Enlarge only proved upper endpoints onto a fixed rational grid.
 # Every subsequent bound still concerns supports containing the actual law.
 def endpoint_up(x):return F(-((-x.numerator*10**6)//x.denominator),10**6)
 a0=min(a0h,d,endpoint_up(a0));a1=min(d-a0l,sign1,endpoint_up(a1))
 if s0.l>O0*a0 or s1.l>O1*a1:return dict(status='EMPTY_SUPPORT_VARIANCE')
 s0=I(s0.l,min(s0.h,O0*a0));s1=I(s1.l,min(s1.h,O1*a1))
 c0=bounded_cubic(s0,a0);c1=bounded_cubic(s1,a1)
 raw=vl*(1-2*vl)+3*vl*(s0.l+s1.l)+(1-pl if c0<0 else 1-pu)*c0+(pu if c1<0 else pl)*c1
 rho=max(F(cfg['rho_lower']),raw/root((vh+s.h)**3,10**12)[1])
 if rho>F(cfg['rho_upper']):return dict(status='EMPTY_RHO_BRANCH')
 c0u=cubic_upper(s0,O0);c1u=cubic_upper(s1,O1)
 rawhi=vh*(1-2*vh)+3*vh*(s0.h+s1.h)+(1-pu if c0u<0 else 1-pl)*c0u+(pl if c1u<0 else pu)*c1u
 # Actual absolute-moment numerator is nonnegative. Clamp its interval
 # upper to zero before division by the positive denominator lower.
 rho_law_upper=max(F(0),rawhi)/root((vl+s.l)**3,10**12)[0]
 if rho_law_upper<F(cfg['rho_lower']):return dict(status='EMPTY_RHO_UPPER')
 ms=masses(n,pl,pu);V=I(lo,hi)*(1+(k-n*p)*(alpha-p)/I(n*vl,n*vh));V=I(max(F(0),V.l),V.h)
 vsum=(n-k)*s0+k*s1
 if V.h<vsum.l or vsum.h<V.l:return dict(status='EMPTY_VARIANCE_IDENTITY')
 # First try only the cheap valid own-count upper bounds. A strict
 # score pass already proves the cell; otherwise use every old bound.
 # This changes evaluation order, never the target or covered domain.
 cheap=F(1)
 if uh<0:
  vmax=min(V.h,vsum.h)
  need(vmax>=0,'own cheap positive variance')
  cheap=min(vmax/(vmax+uh*uh),own_mgf_upper(n,k,pl,pu,hi,al,ah,O0,a1,uh))
 incoming,incoming_left,incoming_lip,gaussian_lip=incoming_per_count(n,k,pl,pu,lo,hi,al,ah,ul,uh,s0,s1,O0,a1)
 num=k+ul-n*pu;den=n*(vh if num>=0 else vl)+(hi if num>=0 else lo)
 normal=normal_lower(num,den)
 centered=centered_binomial_gaussian(n,k,pl,pu,ul,lo,hi)
 multiplier=root(F(n),10**12)[1]/rho
 def finish(upper):
  ownloss=ms[k][0]*(1-upper)
  difference=max(F(0),min(ms[k][2]-ownloss+incoming-normal,centered-ownloss+incoming))
  score=up(multiplier*difference)
  return dict(status='PASS'if score<TARGET else'UNRESOLVED',score_upper=str(score),rho_lower=str(rho),a0upper=str(a0),a1upper=str(a1),Dupper=str(Dcap),outward0=str(O0),outward1=str(O1))
 fast=finish(cheap)
 if fast['status']=='PASS':return fast
 drift=incoming_lip-gaussian_lip
 intercept=min(ms[k][2]-normal,centered)+incoming_left-drift*ul
 coherent=own_phase_upper(k,n,I(ul,uh),s0,s1,O0,O1,a0,a1,V,intercept,drift,ms[k][0],multiplier,target=TARGET)
 coherent_score=up(multiplier*max(F(0),coherent))
 if coherent_score<TARGET:
  fast['status']='PASS';fast['score_upper']=str(coherent_score);return fast
 if rho>min(F(cfg['rho_upper']),rho_law_upper):return dict(status='EMPTY_RHO_BRANCH')
 poly=joint.defect_polytope(pl,pu,s,s0,s1,O0,O1,a0,a1,rho,min(F(cfg['rho_upper']),rho_law_upper),a0l,d,Dcap)
 poly=signed_gamma_clip(poly,pl,pu,s,s0,s1,F(cfg['acquired_gamma'][0]),F(cfg['acquired_gamma'][1]))
 if not poly['vertices']:return dict(status='EMPTY_JOINT_CUBICS')
 coupled=joint.own_phase_bound(k,n,I(ul,uh),s0,s1,O0,O1,a0,a1,V,intercept,drift,ms[k][0],multiplier,poly['vertices'])
 coherent=min(coherent,coupled)
 coherent_score=up(multiplier*max(F(0),coherent))
 if coherent_score<TARGET:
  fast['status']='PASS';fast['score_upper']=str(coherent_score);return fast
 normalized_vertices=joint.normalized_polytope(poly,pl,pu,s,s0,s1,rho)
 need(normalized_vertices,'nonempty polygon split by denominator switch')
 normalized_score=joint.own_normalized_bound(k,n,I(ul,uh),s0,s1,O0,O1,a0,a1,V,intercept,drift,ms[k][0],normalized_vertices)
 coherent_score=min(coherent_score,normalized_score)
 if coherent_score<TARGET:
  fast['status']='PASS';fast['score_upper']=str(coherent_score);return fast
 upper=min(cheap,own_cdf(k,n,I(ul,uh),s0,s1,O0,O1,a0,a1,V))
 result=finish(upper)
 if coherent_score<F(result['score_upper']):result['score_upper']=str(coherent_score)
 return result
