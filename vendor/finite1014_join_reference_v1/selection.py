"""Exact selected whole-family epochs; never fall back from missing fine BN."""
import common as c
N,R=c.N,c.R
def selected(n,b):
    c.need(type(n)is int and 10<=n<=14 and b in c.BANDS,'literal selected index/band')
    fine=n==10 and b=='BN'
    return dict(fine=fine,
      initial=N/('analytic/initial10_BN_fine_v1/n10'if fine else f'analytic/initial10_14_v1/n{n}'),
      resource=N/('root/resource10_BN_fine_v1'if fine else f'root/resource{n}_v2'),
      count=N/('root/count10_BN_fine_v1'if fine else f'root/count{n}_v2'),
      initial_capture_prefix='initial10_BN_fine'if fine else f'initial{n}_{b}',
      resource_capture_prefix='resource10_BN_fine_v1_BN'if fine else f'resource{n}_v2_{b}',
      initial_status='COMPLETE_UNSEEDED_SIGNED_INITIAL10_BN_FINE_CONDITIONAL'if fine else'COMPLETE_UNSEEDED_SIGNED_INITIAL10_14_CONDITIONAL',
      initial_replay_status='PASS_FRESH_UNSEEDED_SIGNED_INITIAL10_BN_FINE_REPLAY_CONDITIONAL'if fine else'PASS_FRESH_UNSEEDED_SIGNED_INITIAL10_14_REPLAY_CONDITIONAL',
      grid=[12,24,12,3]if fine else[12,12,6,3],cells=10368 if fine else 2592,scope_controls=26 if fine else 24)
def inventory():
    return {f'{n}_{b}':{k:str(v.relative_to(R))if hasattr(v,'relative_to')else v for k,v in selected(n,b).items()}for n in range(10,15)for b in c.BANDS}
