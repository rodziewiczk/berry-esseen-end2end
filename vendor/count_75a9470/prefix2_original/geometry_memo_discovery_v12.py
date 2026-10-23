"""Discovery-only value memoization; ordinary acceptance source stays unchanged."""
from functools import lru_cache
from hashlib import sha256
from pathlib import Path

def install():
 import exact35_core as c
 assert sha256(Path(c.__file__).read_bytes()).hexdigest()=='a618867ae34841b2e3e1745e35142694142e08ca2d790b762870f50651e16d71'
 wrappers={}
 for name in('sharp_lower','box_sharp_lower'):
  original=getattr(c,name)
  def build(original):
   @lru_cache(maxsize=50000)
   def cached(key):
    args=[c.I(x[1],x[2])if x[0]=='interval'else x[1]for x in key]
    return original(*args)
   def wrapped(*args):
    if any(type(x)not in(c.I,c.F)or(type(x)is c.I and(type(x.l)is not c.F or type(x.h)is not c.F))for x in args):return original(*args)
    key=tuple(('interval',x.l,x.h)if type(x)is c.I else('scalar',x)for x in args)
    return cached(key)
   wrapped.cache_info=cached.cache_info
   return wrapped
  wrapped=build(original);setattr(c,name,wrapped);wrappers[name]=wrapped
 return wrappers
