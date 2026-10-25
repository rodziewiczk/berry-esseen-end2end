"""Build full67 against an actual checksum-bound local source ZIP."""
from __future__ import annotations
import argparse,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

base=module('n5_full_notebook_base',ROOT/'tools/make_notebooks.py')
runtime=module('n5_full_notebook_runtime',ROOT/'tools/local_notebook_runtime.py')
NAME='67_n5_full_evidence_and_proof_join.ipynb'

def build_local(source_name,source_sha256):
    intro='''# Berry–Esseen:67 — complete n2/n3/C4 foundation and n5 finite chain

Select **Runtime → Run all** using the same Google Drive as08,11,13 and35.
Upload the accompanying exact local source ZIP when requested. CPU or GPU
sessions are supported; the original arithmetic runs on the CPU.

This one notebook contains the complete assigned67 workload: fourteen full
original bounded-control programs, four support construct/replay actions,
and two complete41-strip complement integrations followed by the full original
acceptor and independent19-control readback. It then revalidates the complete
08/11/13/35 exports and checks all twelve current resource regions, all twelve
COUNT interfaces and the final closed signed-beta/rho/p/threshold composition.
All1,200 panel obligations,295 forests,1,770 roots and75,178 leaves from35
are retained. The corner has both infinite phase rays. ROOT4 uses the strong
quantitative **C3≤59√3/250**, before the all-law C4→C5 inference.

Completed atomic stages alone resume. The eight support/complement calls share
one physical atomic epoch because unchanged native programs require their real
captured cwd. An interrupted epoch restarts those eight calls; the other fourteen
complete controls stay cached. Existing08/11/13/35 results are never recomputed.
Missing complete upstream exports give WAITING and a final ZIP; Run all again
after those prerequisites finish. Historical PASS receipts remain provenance.

Every major original action has BASIC2GiB and82,800-second CPU/wall limits
(23hours **per action**, not an estimate for the whole batch). Progress prints
every20seconds; logs back up every60seconds; each fully checked atomic stage
gets a separate durable ZIP/SHA sidecar. A final ZIP is saved on success,
WAITING or a handled failure. Never run two copies of this job simultaneously.

A complete output is a source/capture-bound **conditional finite chain**.
Unrestricted analytic reductions, contact/localization, code-to-lemma validity
and cited smoothing/tail theorems remain explicitly named mathematical inputs.
Neither uploaded JSON nor source hashes establish those lemmas. This notebook
never declares the full n5 theorem or global proof verified. Final cells show
the result, synchronize Drive and release the runtime; a sync error blocks
shutdown.
'''
    fixtures='''print("Testing67 source, full capture, cache, semantic and notebook fixtures. No original numerical kernel is executed.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-n5-full-join.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_n5_full_join*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True); log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("67 infrastructure fixtures failed; mathematical execution will not start. Log: " + str(DRIVER_SELFTEST))
print("67 infrastructure fixtures passed.", flush=True)
'''
    cells=[base.cell('markdown',intro,'instructions'),*runtime.common(source_name,source_sha256,'n5-full-join'),
        base.cell('code',fixtures,'full67-fixtures'),base.cell('code','from be_replay.n5_full_join import run_colab\nRESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
    doc=base.notebook(cells,NAME)
    for c in doc['cells']:
        if c['cell_type']=='code':compile(''.join(c['source']),NAME,'exec')
    return doc

def write_local(source_name,source_sha256,output):
    doc=build_local(source_name,source_sha256);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    path=output/NAME;path.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');return path

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-name',required=True);p.add_argument('--source-sha256',required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(write_local(a.source_name,a.source_sha256,a.output))
