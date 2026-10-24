"""Build two isolated original full n26--30 Fourier-cover notebooks59B/C."""
import argparse,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite2630_cover_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
PROFILES={
 'b2':dict(label='59B',name='59B_n26_30_absmean_b2',rows=115,strips=23,actions=14,
  statement='Closed rho [6/5,13/10], with the explicit additional premise E|X| <= 122/125. All 23 original strips and all five literal indices n = 26,...,30 are computed.'),
 'higher':dict(label='59C',name='59C_n26_30_higher_fourier',rows=215,strips=43,actions=16,
  statement='Closed rho [13/10,19/10]: 110 B3 rows, 30 B5 rows and 75 extension rows. All 43 original strips and all five literal indices n = 26,...,30 are computed.')}
def build(pin,name):
 if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:raise ValueError('Immutable full runtime commit required')
 if name not in PROFILES:raise ValueError('One fixed original full-cover lane required')
 p=PROFILES[name]
 intro=f'''# Berry--Esseen: {p['label']} - original full Fourier cover

Select **Runtime -> Run all** with your usual Google Drive. No parameter edits
are needed. CPU or GPU sessions work; exact arithmetic uses the CPU.

{p['statement']} The strict target is 4097/10000.
Every historical pilot is recomputed freshly in each pass; no old successful
pilot or control receipt is supplied as current arithmetic. Fixed rational
schedules require no NumPy or floating discovery.

This new execution protocol runs two genuine complete original pipelines:
construction and replay. Each pass executes all prerequisite original controls,
pilots and complete cover integrations. There are {p['actions']} native actions
in total ({p['actions']//2} per pass), and {p['rows']} exact rows per pass. Full current outputs and all original controls
are checked, including each closed seam and every explicit actual index.
Only exact approved source-check SHA literals receive current-receipt epochs;
original numerical kernels, schedules, targets and control lists stay unchanged.
Byte-inverse and whole-module AST checks constrain these metadata changes.

All 48 original source/provenance commitments and 34 active source files are
sealed. Historical output objects remain provenance only. Actual launches,
ordinary Python context, source maps, streams, stopped output copies and complete
native JSON objects are bound. Only explicitly enumerated execution timing
fields and the separately checked top-level source map are excluded from
mathematical-object equality; both fresh passes must reproduce all other fields.

Only a complete revalidated two-pass export skips execution. Interrupted work
is preserved and the transaction reruns; no partial numerical resume. Each
action has BASIC 2 GiB, 43,200-second per-process CPU and 54,000-second external
wall ceilings, with sampled live group RSS/CPU. These are not aggregate kernel
quotas or duration estimates. Progress streams every 20 seconds and logs back
up every 60 seconds. A final ZIP is saved on success or handled failure.

Fourier/contact analytic inputs and the remaining parent/count interfaces stay
explicit premises. Native acceptance, support/parent acquisition, full package 59,
full finite 26--30 and all-index theorem flags remain false. Existing 53/64
COUNT results and their caches are untouched.
'''
 fixtures='''print("Checking full-cover source/port/capture/cache fixtures only; no original mathematics.", flush=True)
COVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite2630-covers.log")
with COVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover", "-s", "tests", "-p", "test_finite2630_covers*.py", "-v"], cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True); log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Full-cover infrastructure fixtures failed; mathematical execution will not start. " + str(COVER_SELFTEST))
print("Full-cover infrastructure fixtures: PASS.", flush=True)
'''
 cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite2630-covers-'+name),base.cell('code',fixtures,'cover-fixtures'),
  base.cell('code',"from be_replay.finite2630_covers import run_colab\nRESULT = run_colab("+repr(name)+", durable_root=DURABLE, backup_interval=60)\n",'execute-task'),base.finish()]
 for c in cells:
  if c['cell_type']=='code':compile(''.join(c['source']),p['name'],'exec')
 return base.notebook(cells,p['name']+'.ipynb')
def build_all(pin):return{name:build(pin,name)for name in PROFILES}
def write(pin,output):
 docs=build_all(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True);result=[]
 for name,d in docs.items():
  p=output/(PROFILES[name]['name']+'.ipynb');p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode());result.append(p)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True);p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args()
 for p in write(a.code_commit,a.output):print(p)
