"""Build three lower-n25 parent and resource-interface Colab batches."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("n25_acquisition_notebook_base", ROOT/"tools/make_notebooks.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
JOBS = {"36_n25_parents_b0": ("b0", 2, 17), "37_n25_parents_b1": ("b1", 4, 35),
        "38_n25_parents_b2": ("b2", 4, 23)}


def build(pin, name):
    if not re.fullmatch(r"[0-9a-f]{40}", pin):
        raise ValueError("One full immutable public runtime commit is required")
    branch, actions, edges = JOBS[name]
    intro = f'''# Berry–Esseen: n25 {branch.upper()} — complete parent acquisitions

Choose a **CPU** runtime, then **Runtime → Run all**. Authorize the Google Drive
used for the other proof jobs. No path or parameter edits are required.
Use one session for this branch. Existing notebooks and computed forests remain
unchanged. This batch can run independently of count notebooks26–28.

The batch freshly runs {actions} full original actions: INITIAL acceptance,
all100 probability-panel global resource acceptance, and, for B1/B2, a new
local candidate construction followed by its separate complete acceptance.
Local construction is necessary because a freshly timed global resource
receipt has a different hash. Historical accepted receipts are never inputs.
The original mathematical source and the selected global candidates remain
byte-for-byte unchanged. The existing exact local memoization starts empty.

Afterwards it checks all {edges} exact rational resource-to-count interfaces,
including entire signed quadratic intervals, physical endpoint/beta/mean/theta
premises and the closed partition of every surviving probability panel.
The corresponding count forests are replayed separately by notebooks26–28.

Each original action has an18-hour CPU ceiling,18-hour wall ceiling and2GiB
memory policy. These are safety budgets, not runtime estimates. The subprocess
lane uses BASIC per-process limits and a sampled process-group watchdog; it
does not claim the stronger single-process native resource contract.

Every completed action is saved to a separate cumulative ZIP under
`MyDrive/Berry-Esseen-end2end/n25-parents-{branch}/completed/`. A rerun revalidates
the complete source, command, captures, outputs and parent chain before reuse.
Interrupted individual actions restart in full. Logs are backed up every minute.

Success verifies this branch's conditional parent arithmetic and its numeric
interfaces. It does not acquire the stronger24 premise, verify the analytic
same-witness reduction, accept count forests, or establish the all-index theorem.
'''
    fixture = '''print("Checking parent acquisition infrastructure; no original mathematical kernel is run.", flush=True)
with SELFTEST.with_name(SELFTEST.stem + "-n25-parents.log").open("w", encoding="utf-8") as log:
    checked = subprocess.run([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_n25_b012_acquisition*.py", "-v"],
                             cwd=CODE, stdout=log, stderr=subprocess.STDOUT, text=True)
if checked.returncode:
    raise RuntimeError("Parent acquisition infrastructure fixtures failed; computation was not started.")
print("Parent acquisition infrastructure passed.", flush=True)
'''
    cells = [base.cell("markdown", intro, "instructions"), *base.common(pin, "n25-parents-"+branch),
             base.cell("code", fixture, "infrastructure"),
             base.cell("code", f'from be_replay.n25_b012_acquisition import run_colab\nRESULT = run_colab("{branch}", durable_root=DURABLE)\n', "execute-task"),
             base.finish()]
    for cell in cells:
        if cell["cell_type"] == "code":
            compile("".join(cell["source"]), name, "exec")
    return base.notebook(cells, name+".ipynb")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, default=ROOT/"colab")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for name in JOBS:
        path = args.output/(name+".ipynb")
        path.write_text(json.dumps(build(args.code_commit, name), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
