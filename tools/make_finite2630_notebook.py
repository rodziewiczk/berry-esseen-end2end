"""Build notebook53: exact recovered64 evidence plus79 full original counts."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite2630_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='53_n26_30_conditional_counts'


def build(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('A nonplaceholder immutable full runtime commit is required')
    intro='''# Berry–Esseen: n26–30 — complete selected conditional counts

Complete notebook 64 with the **same Google Drive** first. Then select
**Runtime → Run all** here. CPU or GPU sessions work; arithmetic uses the CPU.
Sources are downloaded and SHA-checked automatically. Keep one active copy
of this numbered job. No path, source or parameter edits are required.

The complete batch has 80 forests, 2,316 roots, 150,296 nodes and 76,306 leaves.
One forest is imported from the complete two-action export of notebook 64. It must reproduce
the exact historical n27/p41 forest SHA, contract, checker and all 28 roots,
6,310 nodes and 3,169 leaves. Its new full acceptance and all 24 controls are
revalidated from actual original source/launch/guard/stopped captures. Its
fresh acceptance keeps its own hash; an old PASS receipt is not substituted.

The other 79 forests run their unchanged full native acceptors and all original
controls. The final 80-forest union recomputes the exact complete census and
checks the recovered identity edge. This selected COUNT calculation remains
conditional on its original same-law resources, physical/attainment and
predecessor premises. It does not establish a finite-index or all-index theorem.

If the complete pair from notebook 64 is missing or fails validation, this notebook records
WAITING before downloading sources or launching a numerical worker. Run 64
to completion on the same Drive, then run 53 again. It never silently constructs
a substitute p41 tree or modifies existing evidence from notebooks 50–55/64.

Only fully validated completed stages are reused from ZIPs with SHA sidecars.
Run all again with this same pinned notebook to restore them. Interrupted
native acceptance restarts fully; no partial numerical result is accepted.
Progress prints every 20 seconds, logs are backed up every 60 seconds, and the
final ZIP is saved on success or handled failure.

Each of the 79 native actions has a BASIC 2 GiB memory policy, a 43,200-second
per-process CPU ceiling and a 54,000-second external wall ceiling. Per-process
hard limits and sampled live-group CPU/RSS are not cumulative reaped-child
CPU or aggregate kernel memory quotas. These budgets do not estimate the
whole batch's runtime. Native-platform, parent-acquisition, all-law finite
and global theorem flags remain false.
'''
    fixtures='''print("Checking finite26–30 source, recovered64, full-stage cache and final80-forest join fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite2630.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite2630*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Finite26–30 infrastructure fixtures failed; mathematical execution will not start. Log: " + str(DRIVER_SELFTEST))
print("Finite26–30 infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite2630-counts'),
           base.cell('code',fixtures,'finite2630-fixtures'),
           base.cell('code','from be_replay.finite2630_counts import run_colab\n'
                     'RESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for cell in cells:
        if cell['cell_type']=='code':compile(''.join(cell['source']),NAME,'exec')
    return base.notebook(cells,NAME+'.ipynb')


def write(pin,output):
    doc=build(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    path=output/(NAME+'.ipynb');path.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode())
    return path


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--code-commit',required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'colab');args=parser.parse_args()
    print(write(args.code_commit,args.output))
