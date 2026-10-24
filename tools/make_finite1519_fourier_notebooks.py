"""Build the three originalFourier sublanes57A--57C."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1519_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
PROFILES={
    'auxiliary':dict(name='57A_n15_19_auxiliary_fourier',label='57A',files=63,manifest=60,
        statement='Auxiliary ceiling 21/50 on the closed finite rho interval [1,19/10], plus its original published tail. It does not assume support, an attained witness or a sharp predecessor.'),
    'supported':dict(name='57B_n15_19_supported_fourier',label='57B',files=85,manifest=82,
        statement='Three closed bands: [1,11/10] below 417/1000; [11/10,23/20] below 827/2000; [23/20,33/25] below 4097/10000. The premise |X| <=3 is explicit and is not acquired here.'),
    'highrho':dict(name='57C_n15_19_highrho_fourier',label='57C',files=73,manifest=70,
        statement='Score ceiling 4097/10000 for rho >=33/25: the finite closed interval [33/25,19/10] plus its original published tail. It does not assume support, an attained witness or a sharp predecessor.')}


def build(pin,kind):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('An immutable full runtime commit is required')
    if kind not in PROFILES:raise ValueError('One fixed originalFourier family is required')
    p=PROFILES[kind]
    intro=f'''# Berry--Esseen: {p['label']} - original {kind} Fourier sublane

Select **Runtime -> Run all** with your usual Google Drive. CPU or GPU sessions
work; arithmetic uses the CPU. Sources are downloaded and hash-checked
automatically. Keep one active copy of this job. No parameter edits are needed.

This is one sublane of parent package 57 for n15--19. The unchanged original
program intentionally computes all six literal indices 14--19, including its
n14 overlap. {p['statement']}

All four original actions are mandatory: untrusted planning, full exact
construction, full exact replay and independent readback. All {p['files']}
original inputs and the original {p['manifest']}-row manifest stay unchanged.
The NumPy planner cannot accept a mathematical row. Exact construction,
replay and readback retain their original arithmetic and complete controls.
Original Prawitz/kappa and any published-tail inputs remain explicit premises.

All four actions form one completed-cache transaction because their genuine
captures bind originating paths. Only a fully validated complete export is
reused. Interrupted work restarts this transaction; older exports are retained.
Run all again in this same pinned notebook to check for complete reusable work.
Progress streams every 20 seconds, logs are backed up every 60 seconds, and a
final ZIP is saved on success or handled failure.

Each action has BASIC 2 GiB, 43,200-second per-process CPU and 54,000-second wall
limits, with sampled live process-group CPU/RSS. These are not aggregate
kernel quotas or cumulative reaped-child CPU accounting. Limits are ceilings,
not duration estimates. Native, parent-acquisition, complete package 57, full finite
and all-index theorem flags remain false. The remaining support/HIGH,
INITIAL/resource and 147 count-interface joins are separate.
'''
    preflight='''import importlib.metadata, os
for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"
try:
    import numpy
except ImportError:
    print("Installing NumPy for the original untrusted planner.", flush=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "numpy"], check=True)
    import numpy
print("Planner NumPy distribution:", importlib.metadata.version("numpy"), flush=True)
print("Untrusted planner thread policy: one thread per numerical library.", flush=True)
print("Exact construction/replay/readback retain their original arithmetic.", flush=True)
'''
    fixtures='''print("Checking selected Fourier source, capture, completed-cache and notebook fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite1519.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite1519*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Fourier infrastructure fixtures failed; mathematical execution will not start. Log: " + str(DRIVER_SELFTEST))
print("Fourier infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite1519-'+kind),
           base.cell('code',preflight,'planner-dependency'),base.cell('code',fixtures,'finite1519-fixtures'),
           base.cell('code','from be_replay.finite1519_'+kind+' import run_colab\n'
                     'RESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),p['name'],'exec')
    return base.notebook(cells,p['name']+'.ipynb')


def build_all(pin):return {kind:build(pin,kind)for kind in PROFILES}


def write(pin,output):
    docs=build_all(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True);result=[]
    for kind,doc in docs.items():
        path=output/(PROFILES[kind]['name']+'.ipynb');path.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode());result.append(path)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True)
    p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args();[print(p)for p in write(a.code_commit,a.output)]
