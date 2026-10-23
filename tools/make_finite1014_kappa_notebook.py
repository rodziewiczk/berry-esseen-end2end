"""Build56K against an immutable reviewed runtime commit; no scalar execution."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1014_kappa_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='56K_kappa_62_625'


def build(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('An immutable full reviewed runtime commit is required')
    intro='''# Berry--Esseen: 56K -- complete scalar kappa=62/625 certificate

Select **Runtime -> Run all** with your usual Google Drive. CPU or GPU sessions
work; this arithmetic uses the CPU. Keep one active copy of this task. No
parameter edits or archive uploads are needed: the pinned repository contains
the three tiny unchanged original source files, their provenance and license.

This notebook performs **one full original controls.py call** in a fresh source
capsule. It constructs and verifies the complete degree-13 certificate on
81 closed intervals, checks all 1134 positive Bernstein coefficients, rejects
21 malformed certificates, and runs 324 exact power/Bernstein identity checks.
The changed convex-splice test and exact Machin pi bracket are also retained.
Historical CERTIFICATE/CHECKED files or captures are not staged as fresh outputs.

Success acquires this scalar certificate calculation only. Support acquisition,
Prawitz smoothing, the Fourier integrations in56A/B/C/D, full package56, all
parent acquisitions and the all-index theorem remain separate. Nothing in this
notebook rewrites the original56A/B/C/D source manifests.

Only a fully completed, currently revalidated transaction is reused from Drive.
Interrupted or incompatible work restarts the one original call; old exports
remain preserved. Rerun this same pinned notebook to reuse a complete cache.
Progress is printed every20 seconds, live files are backed up every60 seconds,
and a final ZIP is saved on success or handled failure.

The BASIC supervisor has2 GiB per-process address-space,43,200-second
per-process CPU,54,000-second external wall,256 MiB run-directory and16 MiB
capture limits. It samples live process-group CPU/RSS. These are not aggregate
kernel quotas or a trusted native containment contract. Native/global proof
flags stay false. Budgets are ceilings, not expected runtimes.
'''
    fixtures='''print("Checking scalar source, stopped-capture, relocation and complete-cache fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-kappa.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite1014_kappa*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Scalar certificate infrastructure fixtures failed; mathematics will not start. Log: " + str(DRIVER_SELFTEST))
print("Scalar certificate infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite1014-kappa'),
           base.cell('code',fixtures,'kappa-fixtures'),
           base.cell('code','from be_replay.finite1014_kappa import run_colab\n'
                     'RESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),NAME,'exec')
    return base.notebook(cells,NAME+'.ipynb')


def write(pin,output):
    doc=build(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    path=output/(NAME+'.ipynb');path.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    return path


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True)
    p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args();print(write(a.code_commit,a.output))
