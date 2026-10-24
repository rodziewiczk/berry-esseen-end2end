"""Build isolated56G/H complete conditional INITIAL/resource band notebooks."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1014_core_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
JOBS={'B0':'56G_n10_14_initial_resource_B0','BN':'56H_n10_14_initial_resource_BN'}


def build(pin,band):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('An immutable full reviewed runtime commit is required')
    if band not in JOBS:raise ValueError('One literal complete band: B0 or BN')
    fine='The n10/BN case retains all nine fine10,368-cell covers; the other four retain2,592 cells per cover.'if band=='BN'else'All five cases retain nine complete2,592-cell signed covers.'
    intro=f'''# Berry--Esseen:56{'G'if band=='B0'else'H'} -- full n10--14 INITIAL/resource {band}

Select **Runtime -> Run all** using your usual Google Drive. CPU or GPU sessions
work; mathematics uses the CPU. No path, source, archive or parameter edits are
needed. Keep one active copy of this numbered task in each session.

This notebook runs all five literal indices10,11,12,13,14 in band{band}. Each
case performs four full unchanged original calls: INITIAL construction,
full INITIAL replay, resource construction over all100 original probability
panels, and full100-panel resource acceptance with every original control.
There are20 original calls in this notebook,40 across56G/H. {fine}

Only source/capture metadata uses a new explicitly sealed epoch. All original
mathematical Python/control bytes, domains, panel data, fixed HIGH values and
non-graph PREPARED fields are preserved. Both original PREPARED files and all
3,072 legacy commitments are retained as provenance. Unavailable historical
upstream captures are labeled UNACQUIRED_NOT_STAGED. They are never fabricated
or reported as freshly executed. Old candidates remain provenance; constructors
produce new candidates in empty output paths, followed by full original checks.

These are conditional core calculations, so56G/H can run in parallel with
56A/B/C/D/E/F/K. Fresh support, HIGH, Fourier and predecessor joins remain
separate. In particular56E is the selected HIGH lane and56F is coarse support.
Successful core arithmetic does not establish complete package56, complete
parent acquisitions, the217 resource-to-count implications or a global theorem.
All corresponding proof flags stay false.

Each n/band case is one four-call cache transaction. A fully completed case
is revalidated and reused from Drive. An interrupted case restarts all four
calls because the original INITIAL checker binds the constructor's absolute
current cwd; no old receipt or capture is rewritten to resume a partial case.
Other completed cases remain reusable. Rerun this same pinned notebook to
find complete compatible case exports. Progress prints every20 seconds and
logs are backed up every60 seconds. A final ZIP is saved on success or handled
failure. Live files and incomplete cases are not accepted certificates.

Each original call has BASIC2 GiB per-process memory,43,200-second per-process
CPU,54,000-second external wall,512 MiB sampled work/output files and16 MiB
capture limits. Live process-group CPU/RSS are sampled. These are not aggregate
kernel quotas, cumulative reaped-child CPU accounting, or a trusted native
containment contract. Budgets are ceilings, not expected durations.
'''
    fixtures='''print("Checking source projection, genuine captures, completed-case cache and notebook fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-core.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite1014_core*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Full INITIAL/resource core infrastructure fixtures failed; mathematics will not start. Log: " + str(DRIVER_SELFTEST))
print("Full INITIAL/resource core infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite1014-core-'+band.lower()),
           base.cell('code',fixtures,'core-fixtures'),base.cell('code',
               'from be_replay.finite1014_core import run_colab\n'
               f'RESULT = run_colab({band!r}, durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),JOBS[band],'exec')
    return base.notebook(cells,JOBS[band]+'.ipynb')


def write(pin,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True);paths=[]
    for band,name in JOBS.items():
        p=output/(name+'.ipynb');p.write_bytes((json.dumps(build(pin,band),ensure_ascii=False,indent=2)+'\n').encode('utf-8'));paths.append(p)
    return paths


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True)
    p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args()
    for file in write(a.code_commit,a.output):print(file)
