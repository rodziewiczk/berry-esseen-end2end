"""Build notebook49 for all selected high-beta3 parent acquisitions."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
NAME='49_high_beta3_acquisition'
spec=importlib.util.spec_from_file_location('high_beta3_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

def build(pin):
    if not re.fullmatch(r'[0-9a-f]{40}',pin):raise ValueError('One immutable public code commit')
    intro='''# Berry–Esseen: upper n25 high-beta3 — all selected acquisitions

Choose a **CPU** runtime and **Runtime → Run all**. Authorize the Google Drive
used by the other proof jobs. No path or parameter edits are required.

This batch runs **14 complete original actions**: INITIAL acceptance with
11 feedback covers and one export, fresh all100-panel global resource
construction and full acceptance, then all11 selected finite local acceptances
on panels16–26. Each complete signed cover has9216 rectangles. The selected
INITIAL and local proof objects are untrusted candidates, checked again by the
unchanged original numerical calculators and complete malformed controls.

The INITIAL receipt includes timing. Its actual fresh bytes are bound by the
new global construction and acceptance. The selected local path uses the
original calculator on17–21 and the original exact-stage cache wrapper on16
and22–26. Every cached action starts empty. Only identical complete input
arguments can reuse a full result computed in that action; resource/support
subprocesses remain unchanged.

The old broad cache manifest also bound unrelated historical results. This
batch preserves it as provenance, and creates an explicit, separately sealed
source-only transport epoch plus snapshots of the actual freshly accepted
parents. Original Python arithmetic, wrapper and cache-helper bytes remain
unchanged. No historical acceptance or fabricated historical execution enters
the fresh parent chain.

This is rho `[7/4,459061/250000]`, signed beta `[14/25,640471/1000000]`,
with contact allowance `1366497/14000000`. It uses the universal same-law
predecessor bound; no sharp global C24 premise is required. Notebook34's six
count forests are separate. This batch does not join or reaccept those counts.

Each original action has an18-hour CPU ceiling,18-hour wall ceiling and2GiB
memory policy. These are safety ceilings, not runtime predictions. BASIC means
per-process resource limits plus a sampled process-group watchdog, without
cumulative whole-tree CPU/cgroup guarantees. Native acceptance remains false.

Every validated completed action is saved as a cumulative ZIP under
`MyDrive/Berry-Esseen-end2end/high-beta3-acquisition/completed/`.
Reruns revalidate all sources, actual commands/captures, current timed parent
bindings, cache counters and the complete prefix before reuse. An interrupted
individual action restarts fully. Progress appears every20 seconds and logs
are copied to Drive every minute. A final result ZIP is saved on failure too.

Success records conditional acquisition arithmetic only. Numeric
resource-to-count implications, analytic same-witness/support/HIGH premises,
regional composition, the full n25 theorem and all-index conclusion remain
separate obligations.
'''
    fixture='''print("Checking high-beta3 infrastructure; no original mathematical kernel is run.", flush=True)
with SELFTEST.with_name(SELFTEST.stem + "-high-beta3.log").open("w", encoding="utf-8") as log:
    checked = subprocess.run([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_high_beta3_acquisition*.py", "-v"],
                             cwd=CODE, stdout=log, stderr=subprocess.STDOUT, text=True)
if checked.returncode:
    raise RuntimeError("High-beta3 infrastructure fixtures failed; computation was not started.")
print("High-beta3 infrastructure passed.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'high-beta3-acquisition'),
        base.cell('code',fixture,'infrastructure'),base.cell('code',
        'from be_replay.high_beta3_acquisition import run_colab\nRESULT = run_colab(durable_root=DURABLE)\n','execute-task'),base.finish()]
    for cell in cells:
        if cell['cell_type']=='code':compile(''.join(cell['source']),NAME,'exec')
    return base.notebook(cells,NAME+'.ipynb')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True)
    p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    path=a.output/(NAME+'.ipynb');path.write_text(json.dumps(build(a.code_commit),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(path)
