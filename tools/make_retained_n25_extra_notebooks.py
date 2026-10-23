"""Build six extra retained-count notebooks29--34; no numerical work."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('extra_retained_notebook_base', ROOT/'tools/make_notebooks.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
JOBS = {
    '29_n25_retained_extra_b3': ('b3', 17, 37128),
    '30_n25_retained_extra_b4': ('b4', 30, 60270),
    '31_n25_retained_extra_lower_b5': ('lower-b5', 39, 48947),
    '32_n25_retained_extra_middle_b4': ('middle-b4', 16, 25257),
    '33_n25_retained_extra_middle_b5': ('middle-b5', 7, 2446),
    '34_n25_retained_extra_upper_beta3': ('upper-high-beta3', 6, 4246),
}


def build(pin, name):
    if not re.fullmatch('[0-9a-f]{40}', pin):
        raise ValueError('One full immutable public code commit is required')
    branch, count, leaves = JOBS[name]
    intro = f'''# Berry–Esseen: {branch} — {count} additional retained n25 forests

Choose a **CPU** runtime and **Runtime → Run all**. Authorize the same Google
Drive used by the other jobs. No command, path or parameter edits are required.
Use one session for this batch; other numbered jobs remain independent.

This batch replays {count} established selected forests, all {leaves:,} leaves,
all 26 original count roots and all 24 original corruption controls per forest.
It does not search for new trees. Numerical checker, kernel, contract and
candidate bytes are unchanged. A new explicit Linux source seal binds their
actual selected bytes. Historical FROZEN_DESIGN files, where present, are
unchanged provenance; stale or missing historical designs are never relabelled
as an original-design acceptance.

Progress is displayed by forest and by the native supervisor. Logs are copied
every minute. Each completed stage is immediately exported to its own ZIP/SHA
under `MyDrive/Berry-Esseen-end2end/n25-retained-extra-{branch}/completed/`.
Run all again with this same pinned notebook to revalidate and reuse complete
stage exports. An interrupted forest restarts its full acceptance.

Each forest has a 2 GiB native memory budget, a 12-hour native CPU ceiling and
a 12-hour5-minute wall ceiling. These are budgets, not runtime estimates.
The complete batch may span multiple Colab sessions.

Provisional B3p34, eleven missing lower-B5 capsules, two mixed-theorem jobs and
ten unresolved upper selections are explicitly excluded in NOT_READY.json.
The seven separate missing-forest reconstruction jobs are not repeated here.
The lower-B5 batch covers its 39 supplied forests; it does not complete that
whole region. Successful arithmetic remains conditional on its exact parent
resources and analytic implications. Full n25 and the all-index theorem stay
unverified.
'''
    fixtures = '''print("Checking extra retained-count source, evidence and cache infrastructure. No numerical kernel runs in these fixtures.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-retained-extra.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    result = subprocess.run([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                             "-s", "tests", "-p", "test_retained_n25_extra*.py", "-v"],
                            cwd=CODE, stdout=log, stderr=subprocess.STDOUT, text=True)
lines = DRIVER_SELFTEST.read_text("utf-8").splitlines()
if result.returncode != 0:
    print("\\n".join(lines), flush=True)
    raise RuntimeError("Extra retained-count infrastructure fixtures failed; computation will not start.")
print(next((line for line in reversed(lines) if line.startswith("Ran ")), "Fixtures passed."), flush=True)
print("Infrastructure fixture log:", DRIVER_SELFTEST, flush=True)
'''
    cells = [base.cell('markdown', intro, 'instructions'),
             *base.common(pin, 'n25-retained-extra-'+branch),
             base.cell('code', fixtures, 'retained-extra-infrastructure'),
             base.cell('code', 'from be_replay.retained_n25_extra import run_colab\n'
                       f'RESULT = run_colab("{branch}", durable_root=DURABLE)\n', 'execute-task'),
             base.finish()]
    for cell in cells:
        if cell['cell_type'] == 'code':
            compile(''.join(cell['source']), name, 'exec')
    return base.notebook(cells, name+'.ipynb')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'colab')
    args = parser.parse_args()
    # Validate before creating any directory or writing any notebook.
    if not re.fullmatch('[0-9a-f]{40}', args.code_commit):
        parser.error('One full immutable public code commit is required')
    args.output.mkdir(parents=True, exist_ok=True)
    for name in JOBS:
        path = args.output/(name+'.ipynb')
        path.write_text(json.dumps(build(args.code_commit, name), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(path)


if __name__ == '__main__':
    main()
