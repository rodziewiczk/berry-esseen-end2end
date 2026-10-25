"""Explicit conditional interface; validating fields is not resource acquisition."""
from fractions import Fraction as F
from variance_geometry import need

def validate_resources(cfg):
 n=cfg['n'];need(type(n)is int and n>=2,'integer count index')
 need(type(cfg['K'])is str and F(cfg['K'])>=0,'nonnegative fixed target offset')
 pl,pu=map(F,cfg['p']);d=F(cfg['d0'])
 need(0<pl<=pu<1,'literal same-orientation probability domain')
 need(d>0,'positive original affine inward intercept')
 need(type(cfg['acquired_inward_upper'])is str and 0<F(cfg['acquired_inward_upper'])<1,'separate independent inward cap below one')
 need(type(cfg['geometry_gap_lower'])is str and F(cfg['geometry_gap_lower'])>0,'positive acquired shared physical gap')
 need(type(cfg['acquired_gamma'])is list and len(cfg['acquired_gamma'])==2 and all(type(x)is str for x in cfg['acquired_gamma'])and F(cfg['acquired_gamma'][0])<=F(cfg['acquired_gamma'][1]),'same-law signed third-moment interval')
 need(0<F(cfg['acquired_mean'][1])<=F(1,2),'positive acquired mean upper')
 need(all(F(cfg[k])>0 for k in('outer0','outer1','Lambda','D','radius_minus','radius_plus','Hminus','Hplus')),'positive resources')
 need(cfg['quadratics'] and all(F(q['Qbudget'])>0 for q in cfg['quadratics']),'positive phase prices')
 need(F(cfg['binary_charge'])>=0 and F(cfg['gap_charge'])>0 and F(cfg['noise_charge'])>0,'same-law affine prices')
 need(1<=F(cfg['rho_lower'])<=F(cfg['rho_upper']),'acquired literal moment interval')
 need(F(1,4)+F(cfg['Lambda'])/n<1 and n*pl-F(cfg['Hminus'])>0 and n*pu+F(cfg['Hplus'])<n,'retained complete nearest-count coverage')
 sign=cfg['sign_premise']
 need(type(sign)is dict and set(sign)=={'schema','resource_status','conditional_means_zero','negative_endpoint_lower','positive_endpoint_lower'},'explicit sign premise fields')
 need(sign['schema']=='ACTUAL_SIGN_CONDITIONED_MARGINAL_V1' and sign['resource_status']=='ASSUMED_ACQUIRED_FOR_CONDITIONAL_TEST','conditional sign premise schema')
 need(sign['conditional_means_zero']is True,'actual centered conditional marginals')
 need(type(sign['negative_endpoint_lower'])is str and type(sign['positive_endpoint_lower'])is str,'rational physical endpoint floors')
 need(F(sign['negative_endpoint_lower'])>0 and F(sign['positive_endpoint_lower'])>0,'acquired positive central physical endpoints')

