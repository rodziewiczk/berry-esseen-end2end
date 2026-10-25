"""Exact optional acquired signed moments and alpha contraction; no acquisition."""
from probability_extrema import variance_extrema
from fractions import Fraction as F
import exact35_core as c
from optimized_arithmetic import cell35 as base_cell35

def moment_box(pl,pu,lo,hi,al,ah,n):
    # Literal same-orientation p in (0,1); pq extrema include the half seam.
    c.need(0<pl<=pu<1 and 0<=lo<=hi and 0<=al<=ah<=1,'signed moment box domain')
    vl,vh=variance_extrema(pl,pu)
    v=c.I(vl,vh);p=c.I(pl,pu);s=c.I(lo/n,hi/n);alpha=c.I(al,ah)
    beta=(v*(1-2*p)+s*(2*alpha-1))/(v+s)
    # v/sqrt(v+s) increases in v and decreases in s for v>0,s>=0.
    ml=vl/c.root(vl+s.h,10**12)[1]
    mh=vh/c.root(vh+s.l,10**12)[0]
    return beta,c.I(ml,mh)

def cell35(cfg,pl,pu,lo,hi,al,ah,k,ul,uh,a0l,a0h):
    c.validate_resources(cfg)
    n=cfg['n'];Lambda=F(cfg['Lambda']);d0=F(cfg['d0'])
    c.need(type(k)is int and 0<=k<=n,'actual count')
    c.need(all(type(x)is F for x in(pl,pu,lo,hi,al,ah,ul,uh,a0l,a0h)),'rational cell')
    c.need(F(cfg['p'][0])<=pl<=pu<=F(cfg['p'][1]) and 0<=lo<=hi<=Lambda and 0<=al<=ah<=1 and -F(1,2)<=ul<=uh<=F(1,2) and 0<=a0l<=a0h<=d0,'closed selected cell')
    for name in ('acquired_beta','acquired_mean'):
        c.need(type(cfg[name])is list and len(cfg[name])==2 and all(type(x)is str for x in cfg[name]),'explicit rational signed moment premise')
    bl,bh=map(F,cfg['acquired_beta']);ml,mh=map(F,cfg['acquired_mean'])
    c.need(-1<=bl<=bh<=1 and 0<=ml<=mh<=F(1,2),'ordered physical signed moment premises')
    beta,mean=moment_box(pl,pu,lo,hi,al,ah,n)
    if beta.h<bl or beta.l>bh:
        return dict(status='EMPTY_ACQUIRED_BETA',beta_lower=str(beta.l),beta_upper=str(beta.h))
    if mean.h<ml or mean.l>mh:
        return dict(status='EMPTY_ACQUIRED_MEAN',mean_lower=str(mean.l),mean_upper=str(mean.h))
    if lo>0:
        v=c.I(*variance_extrema(pl,pu));p=c.I(pl,pu);s=c.I(lo/n,hi/n)
        acquired=c.I(bl,bh)
        possible=(acquired*(v+s)-v*(1-2*p)+s)/(2*s)
        al=max(al,possible.l);ah=min(ah,possible.h)
        if al>ah:return dict(status='EMPTY_ACQUIRED_ALPHA',alpha_lower=str(al),alpha_upper=str(ah))
    return base_cell35(cfg,pl=pl,pu=pu,lo=lo,hi=hi,al=al,ah=ah,k=k,ul=ul,uh=uh,a0l=a0l,a0h=a0h)
