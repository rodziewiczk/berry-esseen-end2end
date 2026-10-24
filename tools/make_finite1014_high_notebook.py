"""Build 56E: the complete three-action conditional supported HIGH10--14 unit."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1014_high_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='56E_n10_14_supported_high'


def build(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('An immutable full runtime commit is required')
    intro='''# Berry–Esseen: 56E — conditional supported HIGH10–14

Select **Runtime → Run all** with your usual Google Drive. CPU or GPU sessions
work; arithmetic uses the CPU. Exact sources are downloaded and hash-checked
automatically. Keep one active copy of this job. No parameter edits are needed.

This notebook performs all three original actions: complete construction,
complete replay, and the original independent check. All 98 static inputs and
the original 95-row manifest are preserved. Both 512- and 1024-cell meshes run
for both bands and all literal indices 10–14: 20 native rows and 10 selected
1024-cell rows. The original bounded controls remain required.

This is part 56E only. Its HIGH bounds assume the same marginal has support
|X| at most 23/10 when rho is at most 11/10, or support |X| at most 12/5 when
rho is at most 23/20. These support assumptions remain unacquired here.
A support radius of 3 alone does not supply them. The retained universal
characteristic-function and supported-HIGH analytic lemmas are also premises.
This does not establish complete package 56, its 217 count interfaces, or any
all-index theorem.

The unchanged original check consumes capture metadata. This notebook creates
an explicit new capture bridge from the actual stopped supervisor launch,
streams and result, binding the entire current input graph. It never recreates
or claims a historical execution identity.

All three actions form one completed-cache transaction. Only a fully validated
complete export is reused after all sources, captures and outputs are checked
again. Interrupted work restarts the transaction. Run all again in this same
pinned notebook to check for reusable complete evidence. Progress prints every
20 seconds; logs are backed up every 60 seconds. A final ZIP is saved on success
or handled failure. Partial numerical work is not resumed.

Each action has BASIC 2 GiB, 43,200-second per-process CPU and 54,000-second
external wall limits. Live process-group CPU/RSS are sampled; these are not
aggregate kernel quotas or cumulative reaped-child CPU limits. Native resource
acceptance, support acquisition and full-theorem flags remain false.
'''
    fixtures='''print("Checking supported HIGH source, truthful capture, completed-cache and notebook fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite1014-high.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite1014_high_*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Supported HIGH infrastructure fixtures failed; mathematical execution will not start. Log: " + str(DRIVER_SELFTEST))
print("Supported HIGH infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite1014-supported-high'),
           base.cell('code',fixtures,'finite1014-fixtures'),
           base.cell('code','from be_replay.finite1014_high import run_colab\n'
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
