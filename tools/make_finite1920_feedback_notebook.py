"""Build notebook 58G: the conditional same-law19--20 Fourier sublane only."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1920_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='58G_n19_20_same_law_feedback_fourier'


def build(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('An immutable full runtime commit is required')
    intro='''# Berry–Esseen: 58G — conditional same-law19–20 Fourier calculation

Select **Runtime → Run all** with your usual Google Drive. CPU or GPU sessions
work; arithmetic uses the CPU. Sources are downloaded and hash-checked
automatically. Keep one active copy of this job. No parameter edits are needed.

This notebook performs four unchanged original actions: untrusted planning,
full exact construction, full exact replay, and complete independent readback.
It preserves all 74 original inputs and the original 71-row source manifest.
The planner uses NumPy. The exact mathematical acceptors retain their original
standard-library arithmetic and complete corruption/parser controls.

This is **part 58G**, a conditional supported Fourier sublane for literal indices
19–20. Its two closed bands are rho [1, 11/10] with ceiling 831/2000 and
rho [11/10, 9/8] with ceiling 103/250. The premise |X| ≤ 3 is explicit and is
not acquired here. This job does not prove support, a new contact allowance,
the remaining support/HIGH/INITIAL/resource stages, the 163 count interfaces,
complete package 58, or an all-index theorem.

All four actions form one completed-cache transaction because their original
captures bind the originating paths. Only a fully validated complete export
is reused. Interrupted work restarts the transaction; previous exports remain
preserved. Run all again in this same pinned notebook to check for reusable
complete evidence. Progress prints every 20 seconds and logs are backed up
every 60 seconds. A final ZIP is saved on success or handled failure.

Each action has BASIC 2 GiB, 43,200-second per-process CPU and 54,000-second
external wall limits. The supervisor also samples live process-group CPU/RSS;
these are not aggregate kernel quotas or cumulative reaped-child CPU limits.
The budgets are ceilings, not estimated durations. Native proof acceptance,
parent acquisition and full-package conclusions remain false.
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
    fixtures='''print("Checking selected supported source, capture, completed-cache and notebook fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite1920.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite1920_feedback*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Supported infrastructure fixtures failed; mathematical execution will not start. Log: " + str(DRIVER_SELFTEST))
print("Supported infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite1920-feedback'),
           base.cell('code',preflight,'planner-dependency'),base.cell('code',fixtures,'finite1920-fixtures'),
           base.cell('code','from be_replay.finite1920_feedback import run_colab\n'
                     'RESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),NAME,'exec')
    return base.notebook(cells,NAME+'.ipynb')


def write(pin,output):
    doc=build(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    path=output/(NAME+'.ipynb');path.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode())
    return path


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True)
    p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args();print(write(a.code_commit,a.output))
