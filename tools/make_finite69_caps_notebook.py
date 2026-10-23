"""Build only notebook46 for fresh n7--9 CAPS and resource acquisition."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite69_caps_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='46_n7_9_conditional_caps_resources'


def build(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('A nonplaceholder immutable full runtime commit is required')
    intro='''# Berry–Esseen: n7–9 — fresh CAPS and conditional resources

Select **Runtime → Run all** and authorize the same Google Drive used by the
other proof jobs. CPU or GPU sessions can be used; the mathematical work uses
the CPU. Source archives are downloaded and SHA-checked automatically. Keep
only one running copy of this numbered job. No source or parameter edits are
required.

This batch has19complete cache stages: nine selected INITIAL acceptances for
n7–9, one complete five-process CAPS pipeline, then nine full100-panel resource
acceptances. Exact compatible completed45INITIAL exports are revalidated and
reused; missing ones are computed freshly. This does not replace counts40–43.

The CAPS pipeline plans, constructs, replays, reads back and checks the fresh
86-strip certificate as one atomic stage. NumPy is required by the unchanged
discovery planner; the exact acceptance stages validate its candidate. Its
installed version is recorded before numerical work. If the new planner does
not produce the original required86strips, the stage fails and saves diagnostics.
No successful completion or whole-batch runtime is promised.

Fresh INITIAL and CAPS outputs form an explicit new evidence epoch. Historical
timed receipts and CAPS remain provenance and are not reused as fresh outputs.
The nine resource jobs consume the fresh checked graph, with their original
exact mathematical checks and controls preserved. Only the documented path
rebinding sends preparation/source-result outputs to new explicit filenames.

Only complete stages with a validated ZIP and SHA sidecar are reused. Run all
again with this same pinned notebook to restore them. Interrupted CAPS work
restarts its whole five-process stage; partial numerical work is not accepted.
Progress is printed every20seconds, logs are backed up every60seconds, and a
final results ZIP is saved on success or handled failure.

Each stage has a BASIC2GiB memory policy,43,200-second per-process CPU ceiling
and54,000-second external wall ceiling. Sampled live-group CPU/RSS and per-process
hard limits do not provide cumulative reaped-child CPU, aggregate kernel memory
enforcement or cgroup/Windows-Job equivalence. These budgets are not timing
estimates. Native-platform acceptance, full finite6–9 conclusions and the
all-index theorem remain false. Support/Fourier, predecessor, physical and
final semantic joins remain separate mathematical obligations.
'''
    fixtures='''print("Checking finite6–9 CAPS source, fresh epoch, complete-stage cache and evidence fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite69-caps.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite69_cap*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Finite6–9 CAPS infrastructure fixtures failed; mathematical execution will not start. Log: " + str(DRIVER_SELFTEST))
print("Finite6–9 CAPS infrastructure fixtures: PASS.", flush=True)
'''
    preflight='''import numpy
print("Discovery planner NumPy version:", numpy.__version__, flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite69-caps'),
           base.cell('code',fixtures,'finite69-caps-fixtures'),
           base.cell('code',preflight,'numpy-discovery-preflight'),
           base.cell('code','from be_replay.finite69_caps import run_colab\n'
                     'RESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for cell in cells:
        if cell['cell_type']=='code':compile(''.join(cell['source']),NAME,'exec')
    return base.notebook(cells,NAME+'.ipynb')


def write(pin,output):
    doc=build(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    path=output/(NAME+'.ipynb')
    path.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode())
    return path


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--code-commit',required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'colab');args=parser.parse_args()
    print(write(args.code_commit,args.output))
