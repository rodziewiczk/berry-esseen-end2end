"""Build notebook64 for the unchanged original n27/p41 new-candidate protocol."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('n27_p41_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='64_n27_p41_new_candidate'


def build(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('A nonplaceholder immutable full runtime commit is required')
    intro='''# Berry–Esseen: n27/p41 — new conditional candidate and full replay

Choose a **CPU** runtime, upload this notebook and select **Runtime → Run all**.
Authorize the same Google Drive used by the other proof jobs. Exact original
sources are downloaded and SHA-checked automatically. No source or parameter
edits are required. Keep only one running copy of this numbered job.

The selected historical n27/p41 forest payload is absent from the supplied
archives. This job creates a new candidate with the unchanged original
`construct_alpha4.py`, then executes unchanged `count_protocol.py accept` in
the same fresh sealed capsule. It never copies an old accepted result or
pretends the new forest has the missing historical hash or leaf count.

The original constructor keeps alpha priority4, its global 10,000-node bound,
depth128 bound and 600-second elapsed check at each visited node. It catches
ordinary failures and may return exit code zero even when incomplete. Success
therefore requires its exact complete-construction packet, the whole newly
written forest and all 28 original count roots with full closed geometry.
If its unchanged internal budget is exhausted, this notebook exports an
incomplete diagnostic bundle. Completion or runtime is not promised.

The second process freshly recomputes every leaf and all 24 original corruption
controls. Both whole native outputs, original sources, actual launch/guard/log
receipts and stopped output captures are checked. The original fixed contract
remains n27, panel41, K=0, p in[41/100,21/50] and rho in[1,11/10]. Its C26
predecessor and same-witness resource acquisition remain unverified premises.

Each action has a BASIC 2 GiB memory policy, 7,200-second per-process CPU ceiling
and 7,260-second external wall ceiling. These external limits do not extend the
constructor's original internal budget. The supervisor uses per-process hard
limits and sampled live process-group CPU/RSS; cumulative reaped-child CPU,
kernel aggregate memory enforcement and cgroup/Windows-Job equivalence are not
claimed. Progress is printed every20 seconds and logs are backed up every60.

Only a fully revalidated completed TWO-action pair is reused from its ZIP plus
SHA-256 sidecar. Run all again to check and reuse that complete pair. Interrupted
or partial construction/acceptance reruns fully from a fresh source capsule.
The final result ZIP is saved on success or handled failure.

This is a new conditional evidence epoch. A successful result does not rewrite
the original composer's old byte pins or close its missing selected edge.
Notebook53 remains NOT_READY until a separate same-contract semantic replacement
join is reviewed and implemented. Native-platform acceptance, parent acquisition,
semantic replacement, lane53 readiness and the all-index theorem remain false.
'''
    fixtures='''print("Checking n27/p41 source, complete geometry, fresh output and full-pair cache fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-n27-p41-recovery.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_n27_p41_recovery*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("N27/p41 infrastructure fixtures failed; mathematical execution will not start. Log: " + str(DRIVER_SELFTEST))
print("N27/p41 infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'n27-p41-recovery'),
           base.cell('code',fixtures,'n27-p41-recovery-fixtures'),
           base.cell('code','from be_replay.n27_p41_recovery import run_colab\n'
                     'RESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),NAME,'exec')
    return base.notebook(cells,NAME+'.ipynb')


def write(pin,output):
    doc=build(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True);path=output/(NAME+'.ipynb')
    path.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode());return path


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--code-commit',required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'colab');args=parser.parse_args();print(write(args.code_commit,args.output))
