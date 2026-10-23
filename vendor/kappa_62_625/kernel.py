"""Standalone exact scalar cosine certificate. No floats or imported kernels."""
from fractions import Fraction as F
from math import comb,factorial

KAPPA=F(62,625)
END=F(625,124)
DEGREE=13

def need(ok,message):
    if not ok:raise ValueError(message)

def exact(x):
    need(type(x)in(int,F),'literal rational required')
    return F(x)

def parsed(x):
    need(type(x)is str,'canonical fraction string required')
    q=F(x);need(str(q)==x,'canonical fraction required');return q

def coefficients():
    c=[F(0)]*14;c[0]=KAPPA
    for j in range(2,9):c[2*j-3]=F((-1)**(j+1),factorial(2*j))
    return c

def intervals():
    return [(F(i,16),F(i+1,16))for i in range(80)]+[(F(5),END)]

def shifted_power(c,a,b):
    c=[exact(z)for z in c];a,b=exact(a),exact(b)
    need(a<b,'strict cell endpoints');n=len(c)-1
    return [sum(c[k]*comb(k,j)*a**(k-j)*(b-a)**j for k in range(j,n+1))for j in range(n+1)]

def forward_bernstein(c,a,b):
    power=shifted_power(c,a,b);n=len(c)-1
    return [sum(power[j]*F(comb(i,j),comb(n,j))for j in range(i+1))for i in range(n+1)]

def inverse_bernstein(bs):
    n=len(bs)-1
    return [sum(bs[i]*comb(n,i)*comb(n-i,j-i)*(-1)**(j-i)for i in range(j+1))for j in range(n+1)]

def cosine_taylor(x,degree):
    need(type(degree)is int and degree>=0 and degree%2==0,'even Taylor degree')
    x=exact(x)
    return sum(F((-1)**j,factorial(2*j))*x**(2*j)for j in range(degree//2+1))

def sine_taylor(x,degree):
    need(type(degree)is int and degree>0 and degree%2==1,'odd Taylor degree')
    x=exact(x)
    return sum(F((-1)**j,factorial(2*j+1))*x**(2*j+1)for j in range((degree+1)//2))

def atan_inverse(k,n):
    need(type(k)is int and k>=2 and type(n)is int and n>=1,'atan parameters')
    z=sum(F((-1)**j,(2*j+1)*k**(2*j+1))for j in range(n))
    nxt=F((-1)**n,(2*n+1)*k**(2*n+1))
    return min(z,z+nxt),max(z,z+nxt)

def splice_certificate():
    clo=1-cosine_taylor(4,16);chi=1-cosine_taylor(4,18)
    slo=sine_taylor(4,15)
    a=F(1,2)-4*KAPPA
    join=258*slo+119*clo
    need(0<16*a<=clo<=chi<=2,'positive curved scale at most one')
    need(join>0,'strict upward derivative jump')
    al,ah=16*a/chi,16*a/clo
    x,y=atan_inverse(5,32);z,w=atan_inverse(239,10)
    pi_l,pi_h=16*x-4*w,16*y-4*z
    need(F(25,8)<pi_l<pi_h<F(22,7),'weak pi bounds')
    return dict(cosine_deficit=[str(clo),str(chi)],sine_lower=str(slo),
                scale_A=[str(al),str(ah)],join_numerator_lower=str(join),
                pi_bracket=[str(pi_l),str(pi_h)])

def construct():
    c=coefficients()
    return dict(version='KAPPA_62_625_SCALAR_V1',kappa=str(KAPPA),
                upper=str(END),degree=DEGREE,coefficients=[str(z)for z in c],
                cells=[dict(interval=[str(a),str(b)],bernstein=[str(z)for z in forward_bernstein(c,a,b)])for a,b in intervals()],
                splice=splice_certificate())

def validate(obj):
    need(type(obj)is dict and set(obj)=={'version','kappa','upper','degree','coefficients','cells','splice'},'exact certificate schema')
    need(obj['version']=='KAPPA_62_625_SCALAR_V1'and obj['kappa']==str(KAPPA)and obj['upper']==str(END),'fixed theorem and domain')
    need(type(obj['degree'])is int and obj['degree']==DEGREE,'fixed degree')
    c=coefficients()
    need(type(obj['coefficients'])is list and obj['coefficients']==[str(z)for z in c],'fixed scalar polynomial')
    need(type(obj['cells'])is list and len(obj['cells'])==81,'complete cell list')
    minima=[]
    for row,(a,b)in zip(obj['cells'],intervals()):
        need(type(row)is dict and set(row)=={'interval','bernstein'},'exact cell schema')
        need(row['interval']==[str(a),str(b)],'canonical complete ordered cover')
        need(type(row['bernstein'])is list and len(row['bernstein'])==14,'complete coefficients')
        bs=[parsed(z)for z in row['bernstein']]
        need(inverse_bernstein(bs)==shifted_power(c,a,b),'Bernstein inverse polynomial identity')
        need(min(bs)>0,'strict Bernstein positivity')
        minima.append(min(bs))
    need(obj['splice']==splice_certificate(),'exact splice arithmetic')
    return dict(cells=81,positive_coefficients=81*14,minimum_bernstein=str(min(minima)))
