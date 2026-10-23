"""Build independent next-stage Colab jobs, pinned to an immutable commit."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("phase1_notebook_builder", ROOT / "tools/make_notebooks.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

JOBS = {
    "09_n25_b3_initial_resources": {
        "task": "n25-b3-parents", "tests": "test_n25_parents.py",
        "title": "n25 B3: fresh INITIAL and all 100 resource panels",
        "scope": """This notebook recomputes the full B3 INITIAL proof and resource acquisition,
then runs both unchanged native acceptors, including their corruption controls.
It does not wait for the missing count trees. These computations can run in parallel.
The imported STRONGER24 bound, analytic same-law implications and final count join
remain separate premises. A fresh regional result is not a global theorem.

Each of the four stages has its own two-hour CPU ceiling and external wall limit.
Live evidence is backed up every minute. Interrupted internal computations are not
automatically treated as accepted prefixes.
""",
        "execute": "from be_replay.n25_parents import run_colab\nRESULT = run_colab('b3', durable_root=DURABLE)\n",
    },
    "10_n25_b4_initial_resources": {
        "task": "n25-b4-parents", "tests": "test_n25_parents.py",
        "title": "n25 B4: fresh INITIAL and all 100 resource panels",
        "scope": """This notebook recomputes the full B4 INITIAL proof and resource acquisition,
then runs both unchanged native acceptors, including their corruption controls.
It does not wait for the four missing B4 count trees. These computations can run in parallel.
The imported STRONGER24 bound, analytic same-law implications and final count join
remain separate premises. A fresh regional result is not a global theorem.

Each of the four stages has its own two-hour CPU ceiling and external wall limit.
Live evidence is backed up every minute. Interrupted internal computations are not
automatically treated as accepted prefixes.
""",
        "execute": "from be_replay.n25_parents import run_colab\nRESULT = run_colab('b4', durable_root=DURABLE)\n",
    },
    "11_n4_complete_root": {
        "task": "n4-complete-root", "tests": "test_root4.py",
        "title": "C4: complete ROOT4 production and fresh replay",
        "scope": """This notebook uses an explicitly derived and sealed Linux resource-only source epoch.
All mathematical functions, original closed domains and numerical targets are retained.
It attempts the complete producer and then a complete fresh replay: all 260 geometry
classes and all 1,300 HIGH request slots are required. UNKNOWN does not count as success.
The unrestricted C4 conclusion still requires the separate analytic reductions.

Each full pass retains the original 43,200-second CPU budget, the 256 MiB worker
allowance and the internal 64 MiB HIGH gates. This is a long computation; it may
outlive an allocated Colab session. Live backups preserve evidence, but the original
producer does not consume incomplete parent ledgers as an accepted resume input.
""",
        "execute": "from be_replay.root4 import run_colab\nRESULT = run_colab(durable_root=DURABLE)\n",
    },
    "12_tail49_complete_arithmetic": {
        "task": "tail49-complete-arithmetic", "tests": "test_tail49.py",
        "title": "Tail49: complete retained arithmetic replay",
        "scope": """This notebook executes the unchanged finite tail verifier, with all 14 required
top-level runs and all 41 retained component replays. It does not use a quick mode.
The final result is checked against the complete required invocation census.

This replacement uses a 64,800-second (18-hour) external wall allowance and a
64,800-second (18-hour) per-process CPU allowance, with 2 GiB BASIC memory.
These are budgets, not a completion-time estimate. The earlier 512 MiB run
stopped on memory; the corrected 2 GiB run stopped at the 7,800-second wall limit.
All mathematical source bytes, 14/41 jobs, exact targets and completion checks
are unchanged. This is a fresh full run; preserve both earlier incomplete ZIPs.
The original driver has no numerical resume, so all required jobs run again.

This portable route uses BASIC process-group supervision. It cannot claim the
original Docker/private-cgroup contract or trusted native arithmetic acceptance.
CPU/RSS group observations are sampled over live processes; the CPU allowance
is not cumulative CPU accounting for the entire sequential subprocess suite.
Completed arithmetic is reported with that explicit limitation, and the all-index
proof remains unverified. An interrupted or partial run is preserved as incomplete.
""",
        "execute": "from be_replay.tail49 import run_colab\nRESULT = run_colab(durable_root=DURABLE, memory_bytes=2048*1024**2,\n                   cpu_seconds=64800, wall_seconds=64800)\n",
    },
    "13_n5_gapfree_whole_line": {
        "task": "n5-gapfree-whole-line", "tests": "test_n5_gapfree.py",
        "title": "n5: complete gap-free corner, compact forest and both phase rays",
        "scope": """This queued task is independent of the ongoing n25 and n4 calculations.
Run it when a CPU session is available. It verifies the original 60-root forest,
all 1,994 nodes and 1,027 leaves, and both infinite phase rays through the exact
selected arithmetic functions. It does not use historical execution captures.

The result concerns the positive closed-CDF discrepancy at every real threshold
on the stated rho/beta rectangle. It is one component of n5, with no predecessor,
bounded-support, contact or physical-gap premise. The absolute all-law n5 theorem
still requires the other signed domains and the remaining n5 branches.

The notebook uses a separately documented Linux execution protocol and corruption
controls. Progress, logs and one-minute Drive backups are automatic. The whole
run has a two-hour total CPU ceiling; this is a budget, not a runtime estimate.
An interrupted computation is saved as incomplete and has no internal resume.
""",
        "execute": "from be_replay.n5_gapfree import run_colab\nRESULT = run_colab(durable_root=DURABLE)\n",
    },
}


def build(pin, name):
    job = JOBS[name]
    intro = "# Berry–Esseen: " + job["title"] + "\n\n"
    intro += "Select **Runtime -> Run all**. No command or parameter edits are required.\n"
    intro += "Authorize Google Drive when requested. Keep one session per selected task.\n\n"
    intro += job["scope"]
    cells = [base.cell("markdown", intro, "instructions"), *base.common(pin, job["task"])]
    tests = f'''print("Checking this job's orchestration and source-binding fixtures. No mathematics is executed by these tests.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-driver.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    result = subprocess.run([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                             "-s", "tests", "-p", "{job['tests']}", "-v"],
                            cwd=CODE, stdout=log, stderr=subprocess.STDOUT, text=True)
fixture_lines = DRIVER_SELFTEST.read_text(encoding="utf-8").splitlines()
if result.returncode == 0:
    summary = next((line for line in reversed(fixture_lines) if line.startswith("Ran ")), "All selected fixtures completed.")
    print("Driver infrastructure fixtures: PASS.", summary, flush=True)
else:
    print("\\n".join(fixture_lines), flush=True)
print("Infrastructure fixture log:", DRIVER_SELFTEST, flush=True)
if result.returncode != 0:
    raise RuntimeError("The selected driver failed its infrastructure fixtures; computation will not start.")
'''
    cells.append(base.cell("code", tests, "driver-fixtures"))
    cells.append(base.cell("code", job["execute"], "execute-task"))
    cells.append(base.finish())
    document = base.notebook(cells, name + ".ipynb")
    for cell in document["cells"]:
        if cell["cell_type"] == "code":
            compile("".join(cell["source"]), name, "exec")
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "colab")
    parser.add_argument("--jobs", nargs="+", choices=tuple(JOBS), default=list(JOBS))
    args = parser.parse_args()
    if not re.fullmatch("[0-9a-f]{40}", args.code_commit):
        raise ValueError("Immutable full Git commit required")
    args.output.mkdir(parents=True, exist_ok=True)
    for name in args.jobs:
        path = args.output / (name + ".ipynb")
        path.write_text(json.dumps(build(args.code_commit, name), ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")
        print(path)


if __name__ == "__main__":
    main()
