"""Build notebook39 for the two lower-B5 global parent acceptances."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("b5_global_notebook_base", ROOT/"tools/make_notebooks.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
NAME = "39_n25_global_parents_b5"


def build(pin, name=NAME):
    if not re.fullmatch(r"[0-9a-f]{40}", pin) or name != NAME:
        raise ValueError("Exact notebook39 and one immutable public runtime commit")
    intro = '''# Berry–Esseen: n25 lower B5 — two complete global parent acceptances

Choose a **CPU** runtime, then **Runtime → Run all**. Authorize the Google Drive
used for the other proof jobs. No path or parameter edits are required.

This batch freshly runs two full, unchanged original acceptors: the unseeded
INITIAL (12 feedback covers plus the export cover, 239,616 signed rectangles)
and all100 probability-panel global resources. Both run all12 original
corruption controls. Complete historical proof objects are untrusted candidates;
historical accepted receipts are never execution inputs. The first fresh
receipt has a deterministic original serialization, allowing the second full
acceptor to consume its unchanged candidate with the exact fresh parent edge.

The exact lower-B5 domain is rho `[3/2,33/20]`, with contact allowance `5/16`.
The imported stronger24 statement remains a conditional premise until it is
freshly acquired and joined separately. This batch may run in parallel with
the count and auxiliary jobs. It neither repeats notebook31's retained forests
nor supplies the11 missing B5 count capsules or the two mixed proofs.

Each complete action has an18-hour CPU ceiling,18-hour wall ceiling and2GiB
memory policy. These are safety budgets, not runtime estimates. The BASIC
contract uses per-process limits and a sampled process-group watchdog; it
does not claim single-process native acceptance or cumulative whole-tree CPU.

Each completed stage is saved as a separate cumulative ZIP under
`MyDrive/Berry-Esseen-end2end/n25-global-parents-b5/completed/`. A rerun checks
the entire source, command, captures, outputs and parent chain before reuse.
An interrupted action restarts in full. Logs are backed up every minute.

Success records only conditional global parent arithmetic. Same-law analytic
premises, stronger24 acquisition, resource-to-count interfaces, local feedback,
full B5 composition and the all-index theorem remain separate obligations.
'''
    fixture = '''print("Checking B5 global-parent infrastructure; no original mathematical kernel is run.", flush=True)
with SELFTEST.with_name(SELFTEST.stem + "-b5-global.log").open("w", encoding="utf-8") as log:
    checked = subprocess.run([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_n25_b5_global*.py", "-v"],
                             cwd=CODE, stdout=log, stderr=subprocess.STDOUT, text=True)
if checked.returncode:
    raise RuntimeError("B5 global-parent infrastructure fixtures failed; computation was not started.")
print("B5 global-parent infrastructure passed.", flush=True)
'''
    cells = [base.cell("markdown", intro, "instructions"), *base.common(pin, "n25-global-parents-b5"),
        base.cell("code", fixture, "infrastructure"),
        base.cell("code", "from be_replay.n25_b5_global import run_colab\nRESULT = run_colab(durable_root=DURABLE)\n", "execute-task"),
        base.finish()]
    for cell in cells:
        if cell["cell_type"] == "code": compile("".join(cell["source"]), name, "exec")
    return base.notebook(cells, name+".ipynb")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, default=ROOT/"colab")
    args = parser.parse_args()
    value = build(args.code_commit)
    args.output.mkdir(parents=True, exist_ok=True)
    path = args.output/(NAME+".ipynb")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(path)
