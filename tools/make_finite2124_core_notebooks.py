"""Build58B/C: full conditional actual21--24 INITIAL and resource calls."""
from __future__ import annotations
import argparse,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite2124_core_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAMES={'B0':'58B_n21_24_B0_initial_resources','BN':'58C_n21_24_BN_initial_resources'}

def build(pin,band):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:raise ValueError('An immutable full runtime commit is required')
    if type(band)is not str or band not in NAMES:raise ValueError('Literal B0 or BN band required')
    name=NAMES[band];label='58B'if band=='B0'else'58C'
    rho,radius=('[1,11/10]','23/10')if band=='B0'else('[11/10,9/8]','12/5')
    intro=f'''# Berry–Esseen: {label} — actual21–24 {band} INITIAL and resources

Select **Runtime → Run all** with your usual Google Drive. CPU or GPU sessions
work; arithmetic uses the CPU. Original sources are downloaded and hash-checked
automatically. Keep one active copy of this job. No parameter edits are needed.

This notebook performs 16 full original calls: four actual indices 21–24, each
with INITIAL construction, full INITIAL acceptance, resource construction and
full resource acceptance. The other band has its own notebook. The two together
perform all 32 calls; neither requires the other notebook to begin.

This band is {band}, on the closed rho interval {rho}, with radius {radius}.
Every INITIAL call includes one full two-ray support computation, nine complete
signed covers of 2,592 cells and all 100 ordered probability panels. Both
INITIAL calls retain all 12 negative controls. Each resource call evaluates
all 100 original panels; resource acceptance retains all 12 negative controls
and completely replays the stored support plans. Failed resource criteria stay
explicit non-exclusions, not a proof that their panels were excluded.

All 193 original static inputs, both original frozen manifests, and the
hardcoded INITIAL source identity are preserved. The original resource review
binds an example historical INITIAL. A separate data-only review epoch replaces
exactly its eight example graph entries with this case's genuinely completed
INITIAL results and captures. Every other review field and all 190 static graph
entries remain unchanged. The old review is preserved separately. The original
mathematical programs execute unchanged; no historical result identity is
claimed for a new output.

The retained 419/1000 auxiliary Fourier ceiling and sharp predecessor/first
failure assumptions remain conditional. These computations do not freshly
acquire the historical Fourier input, C20, full package 58, the resource/count
join or any all-index theorem. The independent high-rho58A and other finite
acquisition/join obligations are separate.

Only a completely validated four-call case export is reused, after checking
all original sources, exact output bytes, actual launch/captures, guard scope,
fresh parent edges and the explicit review epoch. Interrupted cases restart
all four calls; already completed cases remain reusable. Run all again in this
same pinned notebook to check for reusable completed cases.

Progress prints every 20 seconds, log-only backups run every 60 seconds, and a
final ZIP is saved on success or handled failure. Each original call has BASIC
2 GiB, 43,200-second per-process CPU and 54,000-second external wall limits.
Live process-group CPU/RSS are sampled; these are not aggregate kernel quotas
or cumulative reaped-child CPU limits. Native and full-theorem flags stay false.
'''
    fixtures='''print("Checking actual21–24 source, fresh-parent review epoch, full captures, complete-case cache and notebook fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite2124-core.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite2124_core*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Actual21–24 INITIAL/resource infrastructure fixtures failed; mathematical execution will not start. Log: " + str(DRIVER_SELFTEST))
print("Actual21–24 INITIAL/resource infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite2124-core-'+band),base.cell('code',fixtures,'finite2124-fixtures'),
           base.cell('code','from be_replay.finite2124_core import run_colab\nRESULT = run_colab('+repr(band)+', durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),name,'exec')
    return base.notebook(cells,name+'.ipynb')

def build_all(pin):return {band:build(pin,band)for band in NAMES}

def write(pin,output):
    docs=build_all(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True);paths=[]
    for band,doc in docs.items():
        p=output/(NAMES[band]+'.ipynb');p.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+'\n').encode());paths.append(p)
    return paths

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True);p.add_argument('--output',type=Path,default=ROOT/'colab')
    a=p.parse_args();print('\n'.join(map(str,write(a.code_commit,a.output))))
