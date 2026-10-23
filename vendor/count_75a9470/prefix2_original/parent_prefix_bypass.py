"""Discovery-only parent-tail bypass; never returns a leaf or proof result."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import physical_prefix_lookahead as lookahead
from feasible_a0 import propose

def need(ok,message):
    if not ok:raise ValueError(message)

def capture(api,cfg,k,box):
    """Capture the exact outward0/a0upper passed to the first incoming call."""
    import exact35_core as core
    need(not lookahead._active,'no concurrent or nested prefix capture')
    need(sha256(Path(core.__file__).read_bytes()).hexdigest()in lookahead.CORES,'reviewed native prefix source')
    need(type(cfg['n'])is int and cfg['n']==25,'actual n25 prefix capture')
    original=core._cell35_engine;captured=[]
    class ReachedIncoming(Exception):pass
    def incoming(*args,**kwargs):
        need(len(args)==18 and not kwargs,'selected eighteen-argument incoming interface')
        n,j,pl,pu,lo,hi,al,ah,ul,uh,s0,s1,O0,a1,a0,O1,c0,c1=args
        need(type(n)is int and n==25 and type(j)is int and j==k and type(O0)is F and type(a0)is F,
             'exact native support exports')
        captured.append(dict(outward0=O0,a0upper=a0))
        raise ReachedIncoming()
    def prefix(*args,**kwargs):
        need(len(args)==13 and not kwargs,'selected engine positional interface')
        return original(*args[:-1],incoming)
    lookahead._active=True;core._cell35_engine=prefix
    try:
        try:decision,result=api.evaluate(cfg,k,box)
        except ReachedIncoming:
            need(len(captured)==1,'one captured incoming call')
            return dict(physical_empty=False,exports=captured[0])
        need(not captured and type(result)is dict and result.get('status')in api.EMPTY and
             decision==result['status'],'only native physical EMPTY may precede incoming')
        return dict(physical_empty=True,status=decision)
    finally:
        core._cell35_engine=original;lookahead._active=False

def propose_bypass(api,cfg,k,box):
    """At most three prefixes. Both children must be physically empty.

    A returned choice only licenses discovery to store a raw binary split with
    two pending children. Those children still require full native evaluation.
    """
    parent=capture(api,cfg,k,box)
    if parent['physical_empty']:return None
    exports=parent['exports']
    proposal=propose(cfg['n'],box[0][0],box[1][0],box[2][1],exports['outward0'],
                     *box[4],exports['a0upper'])
    if proposal['physical_empty']or proposal['cut']is None:return None
    need(type(proposal['cut'])is F,'rational candidate bypass cut')
    children=api.children(box,4,proposal['cut'])
    observations=[lookahead.probe(api,cfg,k,child)for child in children]
    if not all(item['physical_empty']for item in observations):return None
    return dict(axis=4,cut=proposal['cut'],policy='both_a0_children_physically_empty_parent_bypass')
