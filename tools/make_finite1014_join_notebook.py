"""Build the complete finite10--14 controls/interface notebook56I."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1014_join_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='56I_n10_14_finite_join'


def build(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('An immutable full runtime commit is required')
    intro='''# Berry--Esseen: 56I -- finite n10--14 controls and complete interface join

Select **Runtime -> Run all** with the same Google Drive used for notebook50
and 56A--H/K. CPU or GPU sessions work; arithmetic uses the CPU. Keep one
active copy of this job. No parameter edits or NumPy dependency are needed.

This notebook executes ten complete original bounded-control invocations
covering seven retained review scopes. It then revalidates 234 complete
exports: 217 native count acceptances, ten four-action INITIAL/resource
transactions and seven Fourier/support/HIGH/kappa transactions. It checks
all 1,000 closed probability-panel dispositions, 202 simultaneous parent
contracts and twenty restrictions of five composite panels. The full finite
induction is n10 -> n11 -> n12 -> n13 -> n14.

The base uses the actual regional and same-law supported n9 ceilings. It
does not assume sharp global n9 or eventual n15. General analytic implications
remain explicitly stated premises. Global, all-law, parent-acquisition,
native-guard and complete-package56 acceptance flags remain false.

Original mathematical/control Python sources stay byte-identical. A declared
data-only source-graph epoch preserves all mathematical fixture fields and
records thirty unavailable historical run inputs as unacquired provenance.
No historical successful capture or accepted theorem is fabricated.

Only a fully validated completed stage is reused. Interrupted original actions
restart that action; earlier complete exports remain preserved. Missing
upstream complete exports produce WAITING and a final ZIP. Run all again in
this same pinned notebook after its required jobs finish. Progress prints
every twenty seconds, logs are backed up every sixty seconds and completed
stages receive separate ZIPs with SHA sidecars. A final ZIP is saved on
success or handled failure.

Each original action has BASIC 2 GiB, 82,800-second per-process CPU and external
wall ceilings (23 hours). These are per-action limits, not an estimate that
the entire batch fits one Colab session. The supervisor samples live process
group CPU/RSS; these are not aggregate kernel quotas or cumulative CPU limits
for already reaped children. The exact policy is recorded in every export.
'''
    fixtures='''print("Checking finite-join source, capture, cache, interface and notebook fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite1014-join.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite1014_join*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Finite-join infrastructure fixtures failed; original execution will not start. Log: " + str(DRIVER_SELFTEST))
print("Finite-join infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite1014-join'),
           base.cell('code',fixtures,'finite1014-join-fixtures'),
           base.cell('code','from be_replay.finite1014_join import run_colab\n'
                     'RESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),NAME,'exec')
    return base.notebook(cells,NAME+'.ipynb')


def write(pin,output):
    doc=build(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    path=output/(NAME+'.ipynb');path.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    return path


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--code-commit',required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'colab');args=parser.parse_args();print(write(args.code_commit,args.output))
