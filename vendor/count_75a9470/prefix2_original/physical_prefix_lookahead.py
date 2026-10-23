"""Discovery-only cut preference. Never used to emit a certified leaf."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from feasible_a0 import propose
from split_policy import choose as current_choose,rational

CORES={'f69e1b45e2c32ff163072ae1f9271fbe7114ee847ee8b457ec7a091d1a42d0e2',
       'a618867ae34841b2e3e1745e35142694142e08ca2d790b762870f50651e16d71'}
_active=False

def need(ok,message):
    if not ok:raise ValueError(message)

def probe(api,cfg,k,box):
    """Run the same native prefix, stopping at the first incoming-tail call.

    Single-threaded discovery only. All patches are restored even on errors.
    An EMPTY observation is only a heuristic; the forest still evaluates
    every selected child with the complete ordinary native evaluator.
    """
    global _active
    import exact35_core as core
    need(not _active,'no concurrent or nested physical probe')
    need(sha256(Path(core.__file__).read_bytes()).hexdigest()in CORES,'reviewed native prefix source')
    need(type(cfg['n'])is int and cfg['n']==25,'actual n25 prefix probe')
    original=core._cell35_engine
    class ReachedIncoming(Exception):pass
    def stop(*args,**kwargs):raise ReachedIncoming()
    def prefix(*args,**kwargs):
        # All selected source wrappers call the engine with13 positional
        # arguments:12 physical inputs and the last incoming evaluator.
        need(len(args)==13 and not kwargs,'selected engine positional interface')
        return original(*args[:-1],stop)
    _active=True;core._cell35_engine=prefix
    try:
        try:decision,result=api.evaluate(cfg,k,box)
        except ReachedIncoming:return dict(physical_empty=False,status='OPEN_AT_INCOMING_PREFIX')
        need(type(result)is dict and result.get('status')in api.EMPTY and
             decision==result['status'],'only native physical EMPTY may precede incoming')
        return dict(physical_empty=True,status=decision,result=result)
    finally:
        core._cell35_engine=original;_active=False

def choose(api,cfg,k,box,parent_result):
    """Prefer feasible-a0 only if it has more immediate physical-empty children."""
    old=current_choose(cfg,box,parent_result)
    if old['axis']is None:return dict(old,lookahead='no_strict_original_cut')
    try:
        proposal=propose(cfg['n'],box[0][0],box[1][0],box[2][1],rational(parent_result['outward0']),
                         *box[4],rational(parent_result['a0upper']))
    except(AssertionError,KeyError,TypeError,ValueError,ZeroDivisionError):
        return dict(old,lookahead='invalid_or_missing_a0_exports')
    if proposal['physical_empty']or proposal['cut']is None:
        return dict(old,lookahead='no_strict_feasible_a0_cut')
    cut=proposal['cut']
    if old['axis']==4 and old['cut']==cut:return dict(old,lookahead='already_same_a0_cut')
    trial=dict(axis=4,cut=cut,policy='physical_prefix_lookahead_a0',proposal=proposal)
    observations=[]
    for name,choice in(('current',old),('a0',trial)):
        children=api.children(box,choice['axis'],choice['cut'])
        items=[probe(api,cfg,k,child)for child in children]
        observations.append(dict(name=name,axis=choice['axis'],cut=str(choice['cut']),
            closed_children=sum(item['physical_empty']for item in items),children=items))
    selected=trial if observations[1]['closed_children']>observations[0]['closed_children']else old
    return dict(selected,lookahead='strictly_more_physical_empty_children',observations=observations)
