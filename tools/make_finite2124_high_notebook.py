"""Build58A with an immutable full reviewed runtime pin; no original math."""
from __future__ import annotations
import argparse,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite2124_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='58A_n21_24_highrho_support'

def build(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:
        raise ValueError('An immutable full runtime commit is required')
    intro='''# Berry--Esseen: 58A -- original actual21--24 high-rho support passes

Select **Runtime -> Run all** with your usual Google Drive. CPU or GPU sessions
work; arithmetic uses the CPU. Sources are downloaded and checked automatically.
Keep one active copy of this task. No parameters or uploads are needed.

This notebook runs both complete original actions: construction and full
acceptance. Each recomputes support for all four literal indices21--24 and
both complete signed rays, with all10original malformed-input controls.
Every original source, manifest and source-review byte is preserved.

The selected high-rho exclusion covers the closed seam rho=9/8 through infinity
under its stated sharp-predecessor and retained Fourier premises. This task
does NOT rerun those historical Fourier integrations or prove actual20--24.
Its exported scope is the fresh conditional support calculation only.

Only a completely validated two-action transaction is reused. An interrupted
pair restarts in a fresh capsule; old exports remain preserved. Progress is
printed every20seconds, live backups are attempted every60seconds, and a
final ZIP is saved on success or handled failure.

Each action has BASIC2GiB address-space,43200CPU-second and54000wall-second
ceilings, with sampled process-group limits. These are not aggregate kernel
quotas or a native proof-acceptance contract. Budgets are not runtime estimates.
'''
    fixtures='''print("Checking original-source admission, complete captures and completed-cache fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-actual2124-high.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite2124_high*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Support infrastructure fixtures failed; mathematics will not start. Log: " + str(DRIVER_SELFTEST))
print("Support infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'actual2124-high'),
        base.cell('code',fixtures,'support-fixtures'),base.cell('code',
        'from be_replay.finite2124_high import run_colab\nRESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for cell in cells:
        if cell['cell_type']=='code':compile(''.join(cell['source']),NAME,'exec')
    return base.notebook(cells,NAME+'.ipynb')

def write(pin,output):
    doc=build(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True);path=output/(NAME+'.ipynb')
    path.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode('utf-8'));return path

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True)
    p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args();print(write(a.code_commit,a.output))
