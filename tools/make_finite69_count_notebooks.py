"""Build only the four conditional finite6--9 count notebooks; LF output."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("finite69_count_notebook_base", ROOT / "tools/make_notebooks.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

JOBS = {
    6: dict(name="40_n6_conditional_counts", forests=90, roots=630, leaves=165394),
    7: dict(name="41_n7_conditional_counts", forests=72, roots=576, leaves=48039),
    8: dict(name="42_n8_conditional_counts", forests=64, roots=576, leaves=29651),
    9: dict(name="43_n9_conditional_counts", forests=58, roots=580, leaves=14005),
}


def validate_pin(pin):
    if type(pin) is not str or re.fullmatch(r"[0-9a-f]{40}", pin) is None or pin == "0" * 40:
        raise ValueError("A nonplaceholder immutable full runtime commit is required")


def build(pin, n):
    validate_pin(pin)
    if type(n) is not int or n not in JOBS:
        raise ValueError("One literal selected count index: 6, 7, 8 or 9")
    job = JOBS[n]
    intro = f"""# Berry–Esseen: n{n} — complete selected conditional count replay

Choose a **CPU** runtime, upload this notebook and select **Runtime → Run all**.
Authorize the Google Drive used by the other proof jobs. Source packages are
downloaded and hash-checked automatically. No path, source or parameter edits
are required. Keep only one running copy of this same numbered job.

This batch replays all {job['forests']} selected n{n} count forests, all
{job['roots']:,} roots and all {job['leaves']:,} candidate leaves. Each forest
receives its full original acceptance, all {n + 1} literal roots and all 24
original corruption controls. The selected mathematical checker, kernels,
contract and forest bytes remain unchanged. This batch does not search for
new trees or substitute a shorter forest.

Notebooks 40–43 are independent conditional count jobs and may run in parallel.
They do not acquire their parent INITIAL/resource/support/Fourier facts or the
sequential global predecessor conclusions. A checked forest remains conditional
on those exact premises and on the source-to-lemma argument.

Progress is printed at least every 20 seconds during a job. Logs are backed up
every 60 seconds. Each fully validated completed forest is exported as a ZIP
with its SHA-256 sidecar on Google Drive. Run all again with this same pinned
notebook to revalidate and reuse completed-stage exports. Interrupted native
acceptance restarts fully; partial numerical results are never accepted or
resumed. The final results ZIP is saved on success or handled failure.

Each forest has a 2 GiB memory policy, a 43,200-second per-process CPU ceiling
and a 54,000-second external wall ceiling. BASIC protection uses per-process
limits and sampled live process-group CPU/RSS observations. Cumulative
whole-tree CPU, aggregate kernel memory enforcement and cgroup/Windows-Job
equivalence are not claimed. These are budgets per forest, not a runtime
estimate for the complete batch.

Successful completion records selected conditional count arithmetic only.
Native-platform acceptance, fresh parent-fact joins, unrestricted finite6–9
conclusions and the all-index theorem remain unverified. Remaining acquisition,
support, Fourier, semantic-interface and regional-composition work is separate.
"""
    fixtures = '''print("Checking finite6–9 count source, complete-stage cache and evidence fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite69-counts.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite69_count*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Finite6–9 count infrastructure fixtures failed; computation will not start. Log: " + str(DRIVER_SELFTEST))
print("Finite6–9 count infrastructure fixtures: PASS.", flush=True)
'''
    cells = [base.cell("markdown", intro, "instructions"),
             *base.common(pin, f"finite69-counts-n{n}"),
             base.cell("code", fixtures, "finite69-count-fixtures"),
             base.cell("code", "from be_replay.finite69_counts import run_colab\n"
                       f"RESULT = run_colab({n}, durable_root=DURABLE, backup_interval=60)\n", "execute-task"),
             base.finish()]
    for item in cells:
        if item["cell_type"] == "code":
            compile("".join(item["source"]), job["name"], "exec")
    return base.notebook(cells, job["name"] + ".ipynb")


def build_all(pin):
    validate_pin(pin)
    return {job["name"]: build(pin, n) for n, job in JOBS.items()}


def write(pin, output):
    docs = build_all(pin)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, doc in docs.items():
        path = output / (name + ".ipynb")
        path.write_bytes((json.dumps(doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        paths.append(path)
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "colab")
    args = parser.parse_args()
    for path in write(args.code_commit, args.output):
        print(path)


if __name__ == "__main__":
    main()
