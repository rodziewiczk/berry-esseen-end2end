"""Build notebooks47/48 for the complete selected middle-n25 acquisitions."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('middle_n25_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
JOBS={'47_middle_n25_acquisition_b4':('b4',14,11,32),'48_middle_n25_acquisition_b5':('b5',12,9,33)}


def build(pin,name):
    if not re.fullmatch(r'[0-9a-f]{40}',pin)or name not in JOBS:raise ValueError('One immutable public commit and exact middle job')
    branch,actions,locals_,count_notebook=JOBS[name]
    intro=f'''# Berry–Esseen: middle n25 {branch.upper()} — full selected acquisitions

Choose a **CPU** runtime and **Runtime → Run all**. Authorize the Google Drive
used by the other proof jobs. No path or parameter edits are required.

This batch runs all{actions} selected full original actions: INITIAL acceptance,
fresh all100-panel global resource construction and separate full acceptance,
then all{locals_} selected local acceptances. The selected INITIAL and local
proof objects are untrusted candidates. Original mathematical sources, local
finite schedules and complete corruption controls remain unchanged.

The INITIAL receipt includes timing, so the archived global resource candidate
cannot substitute for a fresh parent edge. This batch constructs the global
candidate again under the actual new INITIAL receipt. For B4, the alternative
two-cycle local capsule receives identical freshly accepted canonical parents;
those parent bytes and their original captures are preserved. Each original
local exact-stage cache starts empty, and every mathematical call, miss and hit
is checked. No candidate result seeds the cache.

This is the rho `[33/20,7/4]` middle region, with a fixed signed-beta subdomain
for this branch and contact allowance `441991/2000000`. It uses the universal
same-law predecessor bound; a sharp global C24 premise is not required here.
The selected count forests are separate notebook{count_notebook}, and this batch
can run in parallel with them. It does not join or accept those forests.

Each original action has an18-hour CPU ceiling,18-hour wall ceiling and2GiB
memory policy. These are safety budgets, not runtime estimates. BASIC protection
means per-process limits and a sampled process-group watchdog, without a
cumulative whole-tree CPU or cgroup guarantee. Native acceptance remains false.

Every checked completed action is saved as a cumulative ZIP under
`MyDrive/Berry-Esseen-end2end/middle-n25-{branch}/completed/`. Reruns revalidate
the full source, actual commands/captures, parent edges and completed prefix
before reuse. An interrupted individual action restarts fully. Logs are backed
up every minute and progress is printed during each action.

Success records only conditional acquisition arithmetic. The source/analytic
same-witness argument, support/HIGH kernel premises, numeric resource-to-count
interfaces, full regional/n25 composition and all-index theorem remain separate.
'''
    fixture='''print("Checking middle acquisition infrastructure; no original mathematical kernel is run.", flush=True)
with SELFTEST.with_name(SELFTEST.stem + "-middle-n25.log").open("w", encoding="utf-8") as log:
    checked = subprocess.run([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_middle_n25_acquisition*.py", "-v"],
                             cwd=CODE, stdout=log, stderr=subprocess.STDOUT, text=True)
if checked.returncode:
    raise RuntimeError("Middle acquisition infrastructure fixtures failed; computation was not started.")
print("Middle acquisition infrastructure passed.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'middle-n25-'+branch),
        base.cell('code',fixture,'infrastructure'),base.cell('code',
            f'from be_replay.middle_n25_acquisition import run_colab\nRESULT = run_colab("{branch}", durable_root=DURABLE)\n','execute-task'),base.finish()]
    for cell in cells:
        if cell['cell_type']=='code':compile(''.join(cell['source']),name,'exec')
    return base.notebook(cells,name+'.ipynb')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True)
    p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    for name in JOBS:
        value=build(a.code_commit,name);path=a.output/(name+'.ipynb')
        path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(path)
