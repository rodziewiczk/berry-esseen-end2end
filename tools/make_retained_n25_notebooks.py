"""Build three automatic B0--B2 retained-count Colab batches."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("retained_notebook_base", ROOT/"tools/make_notebooks.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
JOBS = {
    "26_n25_retained_b0": ("b0", 17, 12985),
    "27_n25_retained_b1": ("b1", 35, 47946),
    "28_n25_retained_b2": ("b2", 23, 33357),
}


def build(pin, name):
    if not re.fullmatch(r"[0-9a-f]{40}", pin):
        raise ValueError("One full immutable public code commit is required")
    branch, count, leaves = JOBS[name]
    intro = f'''# Berry–Esseen: n25 {branch.upper()} — {count} retained count forests

Choose a **CPU** runtime and **Runtime → Run all**. Authorize the same Google
Drive used by the other jobs. No parameter or path edits are required.
Run this queued job when a session becomes available; ongoing jobs need no changes.
Use one session per branch, with no concurrent copies of this same notebook.

The original complete candidates already exist. This batch freshly evaluates
all {leaves:,} selected leaves and runs all 24 original corruption controls for
each of the {count} forests. Historical PASS records are not acceptance inputs.
The mathematical source, contracts and candidates remain byte-for-byte unchanged.

Progress is displayed by forest and by the native supervisor. Logs are backed
up every minute. Each completed native acceptance is immediately saved as a
separate ZIP in `MyDrive/Berry-Esseen-end2end/n25-retained-{branch}/completed/`.
Rerunning this same notebook revalidates those complete stage ZIPs before
reusing them. An interrupted individual forest restarts its full acceptance;
it is never treated as a partly accepted proof.

Each forest has a 2 GiB process-group memory cap and a 12-hour native CPU ceiling.
These are finite safety budgets, not measured runtime estimates. The full batch
may span multiple sessions; keep the same Drive and the same pinned notebook.

Success verifies the selected conditional count arithmetic only. Global/local
resource acquisitions, analytic kernel soundness, the other n25 regions and
the all-index theorem remain separate obligations. No global PASS is claimed.
'''
    fixtures = '''print("Checking retained-count source, evidence and resume infrastructure. No mathematical kernel is executed by these fixtures.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-retained.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    result = subprocess.run([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                             "-s", "tests", "-p", "test_retained_n25_*.py", "-v"],
                            cwd=CODE, stdout=log, stderr=subprocess.STDOUT, text=True)
lines = DRIVER_SELFTEST.read_text("utf-8").splitlines()
if result.returncode != 0:
    print("\\n".join(lines), flush=True)
    raise RuntimeError("Retained-count infrastructure fixtures failed; computation will not start.")
print(next((line for line in reversed(lines) if line.startswith("Ran ")), "Fixtures passed."), flush=True)
print("Infrastructure fixture log:", DRIVER_SELFTEST, flush=True)
'''
    cells = [base.cell("markdown", intro, "instructions"), *base.common(pin, "n25-retained-"+branch),
             base.cell("code", fixtures, "retained-infrastructure"),
             base.cell("code", f'from be_replay.retained_n25 import run_colab\nRESULT = run_colab("{branch}", durable_root=DURABLE)\n', "execute-task"),
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
