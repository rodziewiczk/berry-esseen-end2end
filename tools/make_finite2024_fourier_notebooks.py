"""Build58D/E/F from exact original actual20 Fourier pipelines."""
from __future__ import annotations
import argparse,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite2024_fourier_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAMES={'auxiliary':'58D_n19_24_auxiliary_fourier','universal':'58E_n20_24_universal_highrho_fourier','supported':'58F_n20_24_supported_fourier'}
DETAILS={
'auxiliary':('58D','all literal indices 19–24 on rho [1,19/10], target 21/50, with the external tail from 19/10',
             'Its additional exact numeric interfaces require all n=20–24 bounds below 419/1000 and the n=20 predecessor allowance below 21/100. A 21/50 bound alone is insufficient. Index 19 is deliberately retained in the original full calculation.',51,48,468,24),
'universal':('58E','all literal indices 20–24 on rho [6/5,19/10], target 4097/10000, with the external tail from 19/10',
             'This is a support-free rho/H cover. It does not supply the lower-rho regions or the same-index attained-witness acquisition.',46,43,525,20),
'supported':('58F','all literal indices 20–24 on rho [9/8,6/5], target 4097/10000, assuming the same law has |X| at most 3',
             'The support radius of 3 remains an unacquired premise here. Its closed seams and all literal indices must pass the original exact coverage checks.',51,48,145,26)}

def build(pin,key):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:raise ValueError('An immutable full runtime commit is required')
    if type(key)is not str or key not in NAMES:raise ValueError('Literal auxiliary, universal or supported family required')
    label,scope,extra,inputs,manifest,oldrows,controls=DETAILS[key];name=NAMES[key]
    intro=f'''# Berry–Esseen: {label} — full original actual20 Fourier unit

Select **Runtime → Run all** with your usual Google Drive. CPU or GPU sessions
work; arithmetic uses the CPU. Sources are downloaded and hash-checked
automatically. Keep one active copy of this job. No parameter edits are needed.

This performs all four unchanged original actions: untrusted floating planning,
full exact construction, full exact replay, and the original independent
readback. All {inputs} original inputs and the original {manifest}-row manifest
remain unchanged. The planner uses NumPy; exact acceptance uses rational
arithmetic in the unchanged original programs. Every native control and all
{controls} original readback negative controls remain required.

The exact scope is {scope}.
{extra}

The old package used {oldrows} native rows. A fresh planner may divide cells
differently; every declared cell and literal index must be fully constructed,
replayed and checked, with the entire closed domain and all original bounded
mesh refinements preserved. No historical execution or result identity is
assigned to a new output. The readback request uses actual current source,
plan and capture hashes. It changes data only, not mathematical source code.

This is one Fourier unit of package 58. Prawitz/Fourier analytic estimates,
retained scalar inputs and any stated published tail theorem remain explicit
premises. The actual20 same-witness acquisition, sharp predecessor/induction,
INITIAL/resource/count joins and full58 conclusion remain separate. Existing
COUNT notebook 52 is not repeated here. No all-index theorem is asserted.

All four actions form one completed-cache transaction. Only a SHA-bound full
export is reused after complete source, launch, guard, child capture, output
and readback revalidation. Interrupted work restarts the unit; no partial
numerical result is resumed. Run all again in this same pinned notebook to
check for reusable completed evidence.

Progress prints every 20 seconds, log-only backups run every 60 seconds, and a final
ZIP is saved on success or handled failure. Each action has BASIC 2 GiB,
43,200-second per-process CPU and 54,000-second external wall ceilings. Sampled
live group CPU/RSS are not aggregate kernel quotas or cumulative reaped-child
CPU limits. Native resource, predecessor, support and full-theorem flags stay
false. Budgets are ceilings, not estimated durations.
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
print("Discovery uses one thread per numerical library; exact acceptance retains original arithmetic.", flush=True)
'''
    fixtures='''print("Checking actual20 Fourier source/capture/full-domain/complete-cache and notebook fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite2024-fourier.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite2024_fourier*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Actual20 Fourier infrastructure fixtures failed; mathematical execution will not start. Log: " + str(DRIVER_SELFTEST))
print("Actual20 Fourier infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite2024-fourier-'+key),base.cell('code',preflight,'planner-dependency'),
           base.cell('code',fixtures,'finite2024-fixtures'),base.cell('code','from be_replay.finite2024_fourier import run_colab\nRESULT = run_colab('+repr(key)+', durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),name,'exec')
    return base.notebook(cells,name+'.ipynb')

def build_all(pin):return {k:build(pin,k)for k in NAMES}
def write(pin,output):
    docs=build_all(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True);paths=[]
    for key,doc in docs.items():
        p=output/(NAMES[key]+'.ipynb');p.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode());paths.append(p)
    return paths
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True);p.add_argument('--output',type=Path,default=ROOT/'colab')
    a=p.parse_args();print('\n'.join(map(str,write(a.code_commit,a.output))))
