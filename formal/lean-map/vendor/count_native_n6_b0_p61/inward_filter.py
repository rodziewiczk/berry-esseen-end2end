"""One extra acquired noise cap; original affine Lambda and root stay fixed."""
from fractions import Fraction as F
from rho_signed_moment_tightener import cell35 as original_cell
from generalized_scope import validate_resources
from variance_geometry import need

def cell35(cfg,pl,pu,lo,hi,al,ah,k,ul,uh,a0l,a0h):
    validate_resources(cfg)
    n=cfg['n'];original_lambda=F(cfg['Lambda']);d=F(cfg['d0'])
    need(type(k)is int and 0<=k<=n,'actual count')
    need(all(type(x)is F for x in(pl,pu,lo,hi,al,ah,ul,uh,a0l,a0h)),'rational original cell')
    need(F(cfg['p'][0])<=pl<=pu<=F(cfg['p'][1])and 0<=lo<=hi<=original_lambda and 0<=al<=ah<=1 and -F(1,2)<=ul<=uh<=F(1,2)and 0<=a0l<=a0h<=d,'original closed cell')
    need(type(cfg['acquired_lambda_upper'])is str,'explicit rational independent noise cap')
    cap=F(cfg['acquired_lambda_upper']);need(0<=cap<=original_lambda,'independent cap within original Lambda')
    if lo>cap:return dict(status='EMPTY_ACQUIRED_INWARD_NOISE',lambda_lower=str(lo),acquired_lambda_upper=str(cap))
    return original_cell(cfg,pl=pl,pu=pu,lo=lo,hi=min(hi,cap),al=al,ah=ah,k=k,ul=ul,uh=uh,a0l=a0l,a0h=a0h)
