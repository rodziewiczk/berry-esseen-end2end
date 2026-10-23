"""Unselected exact discovery memo after proven incoming-envelope cancellation."""
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import sys

CORE='a618867ae34841b2e3e1745e35142694142e08ca2d790b762870f50651e16d71'
PINS={
 'common_cubic_bound.py':'f62a02b6e081b377b584a100cf704ed0966589e1de80177b4a33002af665af1c',
 'common_shifted.py':'947ef9b4b43e265fc3250d2c43b69976f11ed7229387d9e0ab51673e683e35b6',
 'general_quartic_sos_bounds.py':'716eda950209111c78960e819e20d0e86b83cb51868a9eaa583b839dbe32c4b5',
 'fixed_peak_quartic_bounds.py':'26d5ec337ef7f0cab81f7c4ced7b4c208d810e5a2670c07d25041ff797e3e88e'}

def install():
    import exact35_core as c
    import common_cubic_bound as cubic
    import common_shifted as shifted
    import general_quartic_sos_bounds as sos
    import fixed_peak_quartic_bounds as fixed
    assert sha256(Path(c.__file__).read_bytes()).hexdigest()==CORE
    for module in(cubic,shifted,sos,fixed):
        p=Path(module.__file__);assert sha256(p.read_bytes()).hexdigest()==PINS[p.name]

    def freeze(value,seen=frozenset()):
        if type(value)is c.F:return('F',value)
        if type(value)is int:return('int',value)
        if type(value)is c.I:
            if type(value.l)is not c.F or type(value.h)is not c.F or value.l>value.h:raise TypeError('unsupported interval')
            return('I',value.l,value.h)
        if type(value)in(tuple,list):
            if id(value)in seen:raise TypeError('recursive cache container')
            return('tuple'if type(value)is tuple else'list',tuple(freeze(x,seen|{id(value)})for x in value))
        raise TypeError('unsupported cache type')

    def thaw(key):
        kind=key[0]
        if kind in('F','int'):return key[1]
        if kind=='I':return c.I(key[1],key[2])
        values=[thaw(x)for x in key[1]]
        return tuple(values)if kind=='tuple'else values

    targets=((cubic,'bound'),(shifted,'bound'),(sos,'common_cubic_gamma'),
             (sos,'common_shifted_gamma'),(fixed,'common_cubic_gamma'),(fixed,'common_shifted_gamma'))
    wrappers={}
    for module,name in targets:
        original=getattr(module,name)
        assert Path(original.__code__.co_filename).resolve()==Path(module.__file__).resolve()
        def build(original):
            @lru_cache(maxsize=2048)
            def cached(key):return original(*thaw(key))
            def wrapped(*args,**kwargs):
                if kwargs or len(args)!=15:return original(*args,**kwargs)
                try:
                    freeze(args)
                    k,n,t,s0,s1,O0,O1,a0,a1,V,intercept,drift,mass,vertices,context=args
                    incoming_args,values=context
                    nn,kk,pl,pu,lo,hi,al,ah,ul,uh,ss0,ss1,o0,aa1=incoming_args
                    incoming,left,lip,gaussian=values
                    # Preserve BOTH original preconditions before any lookup.
                    physical=(nn==n and kk==k and ul==t.l and uh==t.h and ss0.l==s0.l and ss0.h==s0.h and ss1.l==s1.l and ss1.h==s1.h and o0==O0 and aa1==a1)
                    if not physical or drift!=lip-gaussian:return original(*args)
                    # Only exact rational scalar envelope data are canonicalized.
                    if any(type(x)is not c.F for x in(intercept,drift,incoming,left,lip,gaussian,ul)):
                        return original(*args)
                    canonical=list(args)
                    canonical[10]=intercept-left+lip*ul
                    canonical[11]=-gaussian
                    canonical[14]=(incoming_args,(c.F(0),c.F(0),c.F(0),gaussian))
                    key=freeze(tuple(canonical))
                except (TypeError,ValueError,AttributeError,RecursionError):return original(*args)
                # Results include nested chosen-strategy lists/dictionaries.
                # A caller never receives the stored cache object itself.
                return deepcopy(cached(key))
            wrapped.cache_info=cached.cache_info;wrapped.original=original
            return wrapped
        wrapper=build(original)
        # Include imported aliases such as exact35_core.common_cubic_bound.
        for loaded in list(sys.modules.values()):
            if loaded is None:continue
            for attribute,value in list(vars(loaded).items()):
                if value is original:setattr(loaded,attribute,wrapper)
        wrappers[module.__name__+'.'+name]=wrapper
    return wrappers
