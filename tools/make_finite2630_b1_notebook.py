"""Build59A with an immutable runtime pin; no original numerical execution."""
from __future__ import annotations
import argparse,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('b1_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='59A_n26_30_b1_sine_fourier'
def build(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('An immutable full runtime commit is required')
    intro='''# Berry--Esseen:59A -- complete original n26--30 B1 sine Fourier

Select **Runtime -> Run all** with the same Google Drive. CPU or GPU sessions
work; arithmetic uses the CPU. Sources are downloaded automatically. No source,
parameter or path edits are required. Keep one active copy of this task.

This notebook executes both full original actions: construction and complete
acceptance. Each evaluates all23 closed rho strips over[11/10,6/5] at all five
actual indices26--30,115 exact Fourier rows per pass. The original256/512/1024
first-success mesh rule, all finite terms and full tails remain intact.
Acceptance recomputes the full candidate and retains all18 original controls.
The original exact adapter also validates all55 selected resource inputs in
each pass. Historical adapter corruption controls are not claimed freshly run.

All83 original inputs are pinned. Only two JSON source-location records are
derived:12 original absolute input paths are relocated to this exact capsule,
and the native manifest updates only that record's SHA. Every mathematical
program, numerical field, domain and other source commitment is unchanged.
Both original metadata files remain preserved as provenance.

This is conditional B1 Fourier arithmetic. Its55 resource/predecessor/kappa/
support premises remain explicit until separately joined to fresh evidence.
It does not repeat completed53/64 COUNT forests, prove all n26--30, finish
package59 or establish a global theorem. All corresponding flags stay false.

Only a fully revalidated two-pass transaction is cached on Drive. A completed
transaction is reused on rerun; an interrupted pair restarts both full passes.
Sources are cached outside the session export. Progress prints every20seconds,
live backups run every60seconds, and a final ZIP is saved on success or handled
failure. Each action has BASIC2GiB per-process memory,43200per-process CPU and
54000external wall-second ceilings, plus sampled live group limits. These are
ceilings, not time estimates, aggregate kernel quotas or native acceptance.
'''
    fixtures='''print("Checking original-source relocation, complete captures and cache fixtures; no original mathematics.", flush=True)
B1_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-b1.log")
with B1_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover", "-s", "tests", "-p", "test_finite2630_b1*.py", "-v"], cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True); log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("B1 infrastructure fixtures failed; mathematics will not start. " + str(B1_SELFTEST))
print("B1 infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite2630-b1'),base.cell('code',fixtures,'b1-fixtures'),
           base.cell('code','from be_replay.finite2630_b1 import run_colab\nRESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for cell in cells:
        if cell['cell_type']=='code':compile(''.join(cell['source']),NAME,'exec')
    return base.notebook(cells,NAME+'.ipynb')
def write(pin,output):
    doc=build(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True);p=output/(NAME+'.ipynb')
    p.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode('utf-8'));return p
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True);p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args();print(write(a.code_commit,a.output))
