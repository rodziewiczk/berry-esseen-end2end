"""Build isolated57F/G complete conditional INITIAL/resource band notebooks."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1519_core_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
JOBS={'B0':'57F_n15_19_initial_resource_B0','BN':'57G_n15_19_initial_resource_BN'}


def build(pin,band):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('An immutable full reviewed runtime commit is required')
    if band not in JOBS:raise ValueError('One literal complete band: B0 or BN')
    intro=f'''# Berry--Esseen:57{'F'if band=='B0'else'G'} -- full n15--19 INITIAL/resources {band}

Select **Runtime -> Run all**, using your usual Google Drive. CPU or GPU sessions
work; the mathematics uses the CPU. No path, source or parameter edits are needed.
Keep one active copy of this numbered task in each session.

This notebook runs all five literal indices15,16,17,18,19 in band {band}.
Each case performs four full unchanged original calls: INITIAL construction,
full INITIAL replay, resource construction over all100 closed probability
panels, and full100-panel acceptance with every original control. There are20
original calls in this notebook,40 across57F/G. Every INITIAL constructor and
replay retains all nine complete2,592-cell signed covers and six support radii.

A complete compatible57E HIGH cache is required before a new core case starts.
The notebook automatically restores it from the same Drive and revalidates its
full sources, captures and original calculations. Both genuine47,474-byte
native RESULT files must have the exact required SHA. The HIGH calculation is
not repeated here. If that completed input is unavailable, this job stays
incomplete and preserves its logs; finish or restore57E, then rerun this notebook.
Do not replace the missing input with an old hash or a handwritten receipt.

Only source/capture metadata uses a new explicitly sealed epoch. Original
mathematical Python/control bytes, domains, panels, fixed HIGH values and
non-graph mathematical PREPARED fields remain unchanged. The n15 original
replay has a separate selected-candidate SHA field; this is rebound to the
genuine current constructor output after that constructor stops. Its original
SHA guard remains active. All other candidate metadata fields are preserved.
Old PREPARED files, candidates and all3,072 legacy commitments remain provenance.
Unavailable historical captures are labeled UNACQUIRED_NOT_STAGED; the genuine
current57E input and all four current own captures have separate typed bindings.

These are conditional core calculations.57D is coarse support and57E is
compensated HIGH. The Fourier/predecessor/same-law joins,147 resource-to-count
interfaces, full package57 and global theorem remain separate. All corresponding
proof flags stay false. Original constructors produce fresh candidates in empty
output paths, followed by complete original acceptors and controls.

Each n/band case is one four-call cache transaction. A completed compatible
case is revalidated and reused from Drive without mathematical reruns. An
interrupted case restarts its four calls; no genuine capture is rewritten to
resume a partial case. Other completed cases remain reusable. Progress prints
every20 seconds, logs are backed up every60 seconds, and a final ZIP is saved
on success or handled failure. Incomplete outputs are not accepted certificates.

Each original call has BASIC2 GiB per-process memory,82,800-second per-process
CPU and82,800-second external wall ceilings (23 hours),512 MiB sampled files
and16 MiB capture limits. There is no shorter explicit session ceiling here.
Live process-group CPU/RSS are sampled. These are not aggregate kernel quotas,
cumulative reaped-child CPU accounting or trusted native containment. Budgets
are ceilings, not expected durations or a guarantee that all20 calls finish
within one23-hour session. Complete cases remain reusable across sessions.
'''
    fixtures='''print("Checking source projection, genuine captures, completed-case cache and notebook fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-core.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite1519_core*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Full INITIAL/resource core infrastructure fixtures failed; mathematics will not start. Log: " + str(DRIVER_SELFTEST))
print("Full INITIAL/resource core infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite1519-core-'+band.lower()),
           base.cell('code',fixtures,'core-fixtures'),base.cell('code',
               'from be_replay.finite1519_core import run_colab\n'
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
