"""Build the isolated57E original compensated-HIGH notebook."""
import argparse,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1519_high_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='57E_n15_19_compensated_high'
def build(pin):
 if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:raise ValueError('Immutable full runtime commit required')
 intro='''# Berry--Esseen: 57E - supported compensated HIGH for n15--19

Select **Runtime -> Run all** with your usual Google Drive. No parameter edits
are needed. Arithmetic uses the CPU in either CPU or GPU sessions.

This isolated sublane performs two complete unchanged native compensated-HIGH
runs and the full original independent readback for every literal n15,...,19.
The three bands use rho caps 11/10,23/20,33/25 and strict targets 2/5,43/100,3/5.
All 74 original inputs and the exact original 71-row native manifest stay
unchanged. The infinite characteristic and comparator tails are included.
Native runs retain all 8 domain controls; readback retains all 34 corruption
and parser controls. No old successful native proof or capture is execution input.

Actual support radius <=3 and the pointwise Fourier/contact framework remain
explicit premises. This notebook does not acquire the support premise, the
full parent package 57, or the 147 resource-to-count joins.

A pinned standard-library worker starts genuine bound.py children at their
original working directory and records their actual command, complete local
inputs, interpreter and streams. A new explicit current-capture epoch changes
only the top-level CAPTURE_SHA dictionary in derived FRESH_CHECK.py. Exact
byte-inverse and full AST checks retain every mathematical function, original
result/manifest hash gate, domain and control. Sealed original check.py stays
unchanged. Every saved output is copied after the whole owned group stops.

Only a complete three-action revalidated export skips execution. Interrupted
transactions are retained and rerun; no partial numerical resume. Each action
uses BASIC 2 GiB,43,200-second per-process CPU and54,000-second external wall
limits, plus sampled live group CPU/RSS. These are ceilings, not duration
estimates or aggregate kernel quotas. Progress streams every 20 seconds,
logs back up every 60 seconds, and a final ZIP is saved on success or handled
failure. All native, support/parent acquisition, complete package57, full finite
and all-index theorem flags remain false.
'''
 fixtures='''print("Checking HIGH source/capture/port/cache fixtures only; no original mathematics.", flush=True)
HIGH_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite1519-high.log")
with HIGH_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover", "-s", "tests", "-p", "test_finite1519_high_*.py", "-v"], cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True); log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("HIGH infrastructure fixtures failed; mathematical execution will not start. " + str(HIGH_SELFTEST))
print("HIGH infrastructure fixtures: PASS.", flush=True)
'''
 cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite1519-high'),base.cell('code',fixtures,'high-fixtures'),
  base.cell('code','from be_replay.finite1519_high import run_colab\nRESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
 for c in cells:
  if c['cell_type']=='code':compile(''.join(c['source']),NAME,'exec')
 return base.notebook(cells,NAME+'.ipynb')
def write(pin,output):
 d=build(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True);p=output/(NAME+'.ipynb')
 p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode());return p
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True);p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args();print(write(a.code_commit,a.output))
