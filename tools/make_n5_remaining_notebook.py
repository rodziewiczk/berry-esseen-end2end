"""Build notebook35 only, from an immutable public runtime commit; LF output."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
NAME="35_n5_complete_remaining"
spec=importlib.util.spec_from_file_location("n5_base_notebooks",ROOT/"tools/make_notebooks.py")
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)


def build(pin):
    if not re.fullmatch(r"[0-9a-f]{40}",pin)or pin=="0"*40:
        raise ValueError("A nonplaceholder immutable full runtime commit is required")
    intro="""# Berry–Esseen: n5 — complete selected remaining arithmetic

Select **Runtime -> Run all** and authorize Google Drive when requested.
Keep one running copy of this notebook. The original source archive is downloaded
and verified automatically (about141 MB); its selected local source cache is
about475 MB. No source or parameter edits are required.

This batch runs all326 selected jobs: the three support protocols, both HIGH
protocols, global coarse and selected supported owncaps, all12 INITIAL jobs,
all15 resource jobs (1,200 panel obligations), all295 count forests (1,770 roots,
148,586 nodes and75,178 leaves), and both complete complement integrations
(41 strips,42 attempts). It preserves the original numerical algorithms,
complete selected domains and original negative controls.

Progress appears at least every20 seconds. Logs are backed up every60 seconds.
Every completed job is separately validated, saved as a ZIP with its SHA256,
and revalidated before reuse on the next Run all. A partial numerical job is
run again; completed jobs are skipped only after full evidence validation.
The final ZIP is saved on success or handled failure.

This is an explicit new Linux BASIC process-group execution protocol. Each
outer job has a43,200-second per-process CPU budget, a54,000-second external
wall budget and2 GiB memory allowance. Group CPU/RSS observations are sampled
over live processes; cumulative process-tree CPU and cgroup equivalence are
not claimed. Original inner64/512 MiB and7,200-second gates remain in force.
This resource epoch keeps the64 MiB self-cap but measures the current Linux
exec image's approximate VmHWM, excluding the pre-exec notebook image retained
by getrusage. A tiny Linux fixture verifies both the pre-exec distinction and
rejection of real96 MiB growth after exec before any mathematical job starts.
These are resource limits per job, not a completion-time estimate for the batch.

Completion establishes selected conditional arithmetic only. The separate
notebook13 gap-free result, unrestricted C4 premise, support/HIGH/owncap-to-INITIAL,
INITIAL-to-resource and resource-to-count semantic joins and final regional
composition remain separate obligations. The independent complement Fourier
readback runs its16 Fourier/JSON controls; three separate support-corruption
controls are explicitly not claimed. No full n5 or all-index theorem is acquired.
"""
    tests='''print("Checking source binding, completed-stage reuse and failure-export fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-n5-remaining.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_n5_remaining*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("The n5 infrastructure fixtures failed; computation will not start. Log: " + str(DRIVER_SELFTEST))
print("Selected n5 infrastructure fixtures: PASS.", flush=True)
'''
    cells=[base.cell("markdown",intro,"instructions"),*base.common(pin,"n5-remaining")]
    cells.append(base.cell("code",tests,"n5-driver-fixtures"))
    cells.append(base.cell("code",'''from be_replay.n5_remaining import run_colab
RESULT = run_colab(durable_root=DURABLE, backup_interval=60)
''',"execute-task"))
    cells.append(base.finish());doc=base.notebook(cells,NAME+".ipynb")
    for cell in doc["cells"]:
        if cell["cell_type"]=="code":compile("".join(cell["source"]),NAME,"exec")
    return doc


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--code-commit",required=True)
    p.add_argument("--output",type=Path,default=ROOT/"colab");a=p.parse_args()
    doc=build(a.code_commit);a.output.mkdir(parents=True,exist_ok=True);path=a.output/(NAME+".ipynb")
    path.write_bytes((json.dumps(doc,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    print(path)


if __name__=="__main__":main()
