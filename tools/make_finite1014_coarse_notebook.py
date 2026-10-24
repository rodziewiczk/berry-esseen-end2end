"""Build 56F: two complete unchanged conditional coarse-support actions."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1014_coarse_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='56F_n10_14_coarse_support'


def build(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('An immutable full runtime commit is required')
    intro='''# Berry–Esseen: 56F — conditional coarse support10–14

Select **Runtime → Run all** with your usual Google Drive. CPU or GPU sessions
work; arithmetic uses the CPU. Exact sources are downloaded and hash-checked
automatically. Keep one active copy of this job. No parameter edits are needed.

This notebook performs two complete unchanged original actions: construction
and full exact replay, including all 20 malformed-scope and 2 parser controls.
All 81 original static inputs are preserved, including the exact recovered
foundation prose bytes. Ten literal index/band rows cover indices
10–14, both signed support rays, the full threshold line and infinite tails.

This is part 56F only. It computes a support-radius-3 implication conditional
on same-marginal all-threshold predecessor caps: 423/1000 on rho [1,7/5], and
209/500 on rho [7/5,71/50]. The allowance is n times (cap minus 4097/10000).
Those predecessor caps remain unacquired here. The localized premise needs a
separate fresh regional bound at predecessor indices 9–13 below 209/500; a
global 423/1000 bound alone cannot supply it. Historical source audit packets
are conditional inputs, not newly acquired conclusions. Attainment, positive
contact and support analytic premises also remain separate.

This result does not establish narrower radii 23/10 or 12/5 needed by 56E,
complete package 56, all 217 resource/count interfaces or any all-index theorem.

The original replay consumes a constructor capture. The notebook writes a new
explicit capture bridge from the actual stopped launch, streams and result,
binding the complete current input graph. No historical execution identity is
recreated. Both actions form one complete-cache transaction. Only a fully
validated complete export is reused after all sources, launches, captures and
outputs are checked again. Interrupted work restarts both actions; there is no
partial numerical resume. Run all again in this same pinned notebook to check
for reusable complete evidence.

Progress prints every 20 seconds, logs are backed up every 60 seconds, and a
final ZIP is saved on success or handled failure. Each action has BASIC 2 GiB,
43,200-second per-process CPU and 54,000-second external wall limits. Sampled
live group CPU/RSS are not aggregate kernel quotas or cumulative reaped-child
CPU limits. Native, predecessor, support and full-theorem acceptance stay false.
'''
    fixtures='''print("Checking coarse support source, truthful capture, full controls, completed-cache and notebook fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite1014-coarse.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite1014_coarse_*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Coarse support infrastructure fixtures failed; mathematical execution will not start. Log: " + str(DRIVER_SELFTEST))
print("Coarse support infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite1014-coarse-support'),
           base.cell('code',fixtures,'finite1014-fixtures'),
           base.cell('code','from be_replay.finite1014_coarse import run_colab\n'
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
