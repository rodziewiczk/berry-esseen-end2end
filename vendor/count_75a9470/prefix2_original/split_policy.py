"""Pure discovery-only split choice; every returned split covers the raw box.

This helper neither changes a native result nor declares a leaf accepted/empty.
"""
from fractions import Fraction as F
from feasible_a0 import propose

SCALES=(F(1,1000),F(3,500),F(3,20),F(1,50),F(1))
A0_SCALE=F(1,50)

def rational(x):
    if type(x) not in (str,int,F):
        raise ValueError('exact rational required')
    return F(x)

def weighted_widths(cfg,box):
    if type(box) not in (list,tuple) or len(box)!=5:
        raise ValueError('five intervals required')
    if any(type(z) not in (list,tuple) or len(z)!=2 or
           any(type(x)is not F for x in z) or z[0]>z[1] for z in box):
        raise ValueError('ordered exact rational intervals required')
    limit=rational(cfg['Lambda'])
    if limit<=0:raise ValueError('positive Lambda required')
    widths=[(z[1]-z[0])/SCALES[i] for i,z in enumerate(box)]
    widths[2]*=16*max(box[1][1]/limit,F(1,10000))
    return widths

def original(cfg,box):
    widths=weighted_widths(cfg,box)
    axis=max(range(5),key=lambda i:widths[i])
    if box[axis][0]==box[axis][1]:
        return dict(axis=None,cut=None,policy='no_strict_raw_split',widths=widths)
    return dict(axis=axis,cut=sum(box[axis])/2,policy='original',widths=widths)

def choose(cfg,box,result):
    """Return a strict rational split, or explicit None for a singleton box.

    Missing/malformed native exports use the original policy. Valid feasibility
    data replaces the raw a0 score by its feasible width divided by 1/50.
    Ties prefer the other coordinates, with their original first-index rule.
    """
    old=original(cfg,box)
    if old['axis'] is None:return old
    try:
        if type(result)is not dict:raise ValueError('native result mapping required')
        proposal=propose(cfg['n'],box[0][0],box[1][0],box[2][1],
                         rational(result['outward0']),*box[4],
                         rational(result['a0upper']))
    except (AssertionError,KeyError,TypeError,ValueError,ZeroDivisionError):
        return dict(old,reason='invalid_or_missing_feasibility_exports')
    if proposal['physical_empty'] or proposal['cut'] is None:
        return dict(old,reason='no_strict_feasible_cut',proposal=proposal)
    feasible_score=(proposal['feasible'][1]-proposal['feasible'][0])/A0_SCALE
    other=max(range(4),key=lambda i:old['widths'][i])
    if feasible_score>old['widths'][other]:
        return dict(axis=4,cut=proposal['cut'],policy='feasible_a0',
                    widths=old['widths'],feasible_score=feasible_score,proposal=proposal)
    if box[other][0]<box[other][1]:
        return dict(axis=other,cut=sum(box[other])/2,policy='other_weighted_width',
                    widths=old['widths'],feasible_score=feasible_score,proposal=proposal)
    return dict(old,reason='zero_other_and_feasible_widths',
                feasible_score=feasible_score,proposal=proposal)
