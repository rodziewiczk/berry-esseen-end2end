"""Build the isolated57D original full-ray support notebook."""
import argparse,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('finite1519_support_notebook_base',ROOT/'tools/make_notebooks.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
NAME='57D_n15_19_full_ray_support'
def build(pin):
 if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None or pin=='0'*40:raise ValueError('Immutable full runtime commit required')
 intro='''# Berry--Esseen: 57D - full-ray support for n15--19

Select **Runtime -> Run all** with your usual Google Drive. No parameter edits
are needed. Arithmetic uses the CPU in either CPU or GPU sessions.

This isolated sublane executes the unchanged original support constructor and
full independent-driver replay for every literal n15,...,19, rho in the closed
interval [1,33/25], radius 3 and both complete support rays. All 26 exact input
files stay unchanged. The replay recomputes every full proof and all original
14 malformed-candidate and 2 parser controls. No old candidate or accepted
capture is supplied as fresh execution.

The conditional hypothesis remains explicit: an unrestricted attained
sharp-contrary witness at each actual index, with the stated same-law or
universal predecessor ceiling 21/50 and the analytic contact framework.
Successful arithmetic does not acquire this premise, the support theorem,
the full parent package 57, or the 147 resource-to-count joins.

A new capture epoch records the actual stopped constructor command, source
inputs, interpreter, stdout/stderr and candidate. The unchanged replay keeps
its original deterministic candidate SHA gate. Both actions form one atomic
completed-cache transaction: only a complete revalidated export skips them.
Interrupted transactions are preserved and rerun; no partial numerical resume.

Each action uses BASIC process-group supervision with 2 GiB memory,
43,200-second per-process CPU and 54,000-second wall limits, plus sampled live
group CPU/RSS. These are ceilings, not duration estimates or aggregate kernel
quotas. Progress streams every 20 seconds and log backups run every 60 seconds.
A final ZIP is saved on success or handled failure. All native, support/parent
acquisition, full-finite and all-index theorem flags remain false.
'''
 fixtures='''print("Checking source/capture/cache fixtures only; no original mathematics.", flush=True)
SUPPORT_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite1519-support.log")
with SUPPORT_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover", "-s", "tests", "-p", "test_finite1519_support*.py", "-v"], cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True); log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Support infrastructure fixtures failed; mathematical execution will not start. " + str(SUPPORT_SELFTEST))
print("Support infrastructure fixtures: PASS.", flush=True)
'''
 cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,'finite1519-support'),base.cell('code',fixtures,'support-fixtures'),
  base.cell('code','from be_replay.finite1519_support import run_colab\nRESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
 for c in cells:
  if c['cell_type']=='code':compile(''.join(c['source']),NAME,'exec')
 return base.notebook(cells,NAME+'.ipynb')
def write(pin,output):
 d=build(pin);output=Path(output);output.mkdir(parents=True,exist_ok=True);p=output/(NAME+'.ipynb')
 p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode());return p
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--code-commit',required=True);p.add_argument('--output',type=Path,default=ROOT/'colab');a=p.parse_args();print(write(a.code_commit,a.output))
