"""Fixed scalar certificate and adversarial controls. No integration."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from copy import deepcopy
import json,sys
import kernel as k

H=Path(__file__).resolve().parent

def main():
    k.need(__debug__ and sys.flags.dont_write_bytecode and not sys.flags.optimize,'ordinary Python -B')
    obj=k.construct();receipt=k.validate(obj)
    bad=[]
    def mutate(fn):
        z=deepcopy(obj);fn(z);bad.append(z)
    mutate(lambda z:z.update(kappa='1/10'))
    mutate(lambda z:z.update(upper='5'))
    mutate(lambda z:z.update(degree=12))
    mutate(lambda z:z.update(degree=True))
    mutate(lambda z:z['coefficients'].__setitem__(0,'1/10'))
    mutate(lambda z:z['cells'].pop())
    mutate(lambda z:z['cells'].append(deepcopy(z['cells'][-1])))
    mutate(lambda z:z['cells'].__setitem__(1,deepcopy(z['cells'][0])))
    mutate(lambda z:z['cells'].reverse())
    mutate(lambda z:z['cells'][0]['interval'].reverse())
    mutate(lambda z:z['cells'][0]['bernstein'].__setitem__(0,'0'))
    mutate(lambda z:z['cells'][0]['bernstein'].__setitem__(0,'-1'))
    mutate(lambda z:z['cells'][0]['bernstein'].__setitem__(0,62/625))
    mutate(lambda z:z['cells'][0]['bernstein'].__setitem__(0,'124/1250'))
    mutate(lambda z:z['cells'][0]['bernstein'].__setitem__(0,'missing'))
    mutate(lambda z:z['cells'][0]['bernstein'].pop())
    mutate(lambda z:z['splice'].update(join_numerator_lower='1'))
    mutate(lambda z:z.update(unknown='extra'))
    bad.extend([None,[],{}])
    for z in bad:
        try:k.validate(z)
        except (ValueError,TypeError,KeyError,ZeroDivisionError):pass
        else:raise AssertionError('corrupted certificate accepted')
    # Additional exact endpoint evaluations through the Bernstein convex form.
    identity_checks=0
    for row in obj['cells']:
        a,b=map(F,row['interval']);bs=list(map(F,row['bernstein']))
        for t in (F(0),F(1,3),F(1,2),F(1)):
            x=a+(b-a)*t
            p=sum(c*x**j for j,c in enumerate(k.coefficients()))
            bern=sum(bs[i]*k.comb(13,i)*t**i*(1-t)**(13-i)for i in range(14))
            k.need(p==bern,'power/Bernstein evaluation identity')
            identity_checks+=1
    with(H/'CERTIFICATE.json').open('x')as stream:json.dump(obj,stream,indent=2);stream.write('\n')
    out=dict(status='PASS_GLOBAL_COSINE_KAPPA_62_625_AND_CONVEX_SPLICE_V1',
             mathematical_status='Exact scalar polynomial and splice certificate; no Fourier integration or cutoff claim',
             receipt=receipt,negative_controls=len(bad),additional_identity_checks=identity_checks,
             source_sha256={str(H/name):sha256((H/name).read_bytes()).hexdigest()for name in ('kernel.py','controls.py','PROOF.txt','CERTIFICATE.json')})
    with(H/'CHECKED.json').open('x')as stream:json.dump(out,stream,indent=2);stream.write('\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
