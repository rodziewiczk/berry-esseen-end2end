"""Discovery-only loop-invariant hoisting; the acceptance kernel is untouched.

The quartic parameter does not occur in the third-moment or cost intervals.
Compute those exact interval expressions once for each endpoint pair, rather
than 23 times. Preserve endpoint and parameter order, all arithmetic and all
early-return comparisons. Fresh ordinary acceptance must still recompute
every stored leaf using the frozen original source.
"""
from hashlib import sha256
from pathlib import Path
import inspect

CORE_SHA = 'a618867ae34841b2e3e1745e35142694142e08ca2d790b762870f50651e16d71'
THIRD = '    third=intersect(V0*x0+V1*x1,V*x1+V0*(x0-x1),V*x0+V1*(x1-x0),V*I(min(x0,x1),max(x0,x1)))'
COST = '    cost=intersect(V0*x0*x0+V1*x1*x1,V*x1*x1+V0*(x0*x0-x1*x1),V*x0*x0+V1*(x1*x1-x0*x0),V*I(min(x0*x0,x1*x1),max(x0*x0,x1*x1)))'

def install():
    import exact35_core as core
    assert sha256(Path(core.__file__).read_bytes()).hexdigest() == CORE_SHA
    changes = {}
    for name, variable in [('own_cdf', 'a'), ('own_phase_upper', 'aa')]:
        original = getattr(core, name)
        source = inspect.getsource(original)
        loop = f' for {variable} in(F(i,20)for i in range(2,25)):\n'
        assert source.count(loop) == 1
        old = '  for x0 in xs0:\n   for x1 in xs1:\n'+THIRD+'\n'+COST+'\n'
        assert source.count(old) == 1
        # Retain the original body indentation under two one-pass loops.
        # This avoids modifying the arithmetic expression strings at all.
        new = '  for third,cost in frozen_pairs:\n   if True:\n'
        pre = (' frozen_pairs=[]\n'
               ' for x0 in xs0:\n'
               '  for x1 in xs1:\n'
               +THIRD[1:]+'\n'+COST[1:]+'\n'
               '   frozen_pairs.append((third,cost))\n')
        transformed = source.replace(old, new).replace(loop, pre+loop)
        namespace = dict(vars(core))
        exec(compile(transformed, f'<discovery-hoist:{name}>', 'exec'), namespace)
        setattr(core, name, namespace[name])
        changes[name] = dict(original=original, transformed=namespace[name], source=transformed)
    return changes
