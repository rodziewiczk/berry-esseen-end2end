"""Build only notebooks 50--55 for the fixed selected COUNT lanes; LF output."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("finite1039_notebook_base", ROOT/"tools/make_notebooks.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

JOBS = {
    "n10_14": dict(name="50_n10_14_conditional_counts", indices="10–14", forests=217, family="count_protocol"),
    "n15_19": dict(name="51_n15_19_conditional_counts", indices="15–19", forests=147, family="count_protocol"),
    "n20_24": dict(name="52_n20_24_conditional_counts", indices="20–24", forests=163, family="count_protocol"),
    "n26_30": dict(name="53_n26_30_conditional_counts", indices="26–30", forests=80, family="count_protocol"),
    "n31_34": dict(name="54_n31_34_conditional_counts", indices="31–34", forests=282, family="strict"),
    "n35_39": dict(name="55_n35_39_conditional_counts", indices="35–39", forests=120, family="strict"),
}


def validate_pin(pin):
    if type(pin) is not str or re.fullmatch(r"[0-9a-f]{40}", pin) is None or pin == "0"*40:
        raise ValueError("A nonplaceholder immutable full runtime commit is required")


def ready_lanes():
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from be_replay import finite1039_sources
    declaration = finite1039_sources.catalog()
    blocked = declaration.get("not_ready_lanes", {})
    readiness = declaration["lane_ready"]
    if (type(blocked) is not dict or not set(blocked) <= set(JOBS)
            or type(readiness) is not dict or set(readiness) != set(JOBS)
            or any(type(value) is not bool for value in readiness.values())
            or set(blocked) != {lane for lane, ready in readiness.items() if not ready}):
        raise ValueError("Exact catalog source-readiness declarations are required")
    return {lane for lane, ready in readiness.items() if ready}


def build(pin, lane):
    validate_pin(pin)
    if type(lane) is not str or lane not in JOBS:
        raise ValueError("One of the six fixed selected finite COUNT lanes is required")
    if lane not in ready_lanes():
        raise ValueError("This selected COUNT lane is not source-complete; no runnable notebook is generated: "+lane)
    job = JOBS[lane]
    if job["family"] == "count_protocol":
        protocol = """Each forest receives its full original `count_protocol.py accept`
execution, every literal count root and every original named corruption control.
The original nested-tree representation is retained. Selected subdivided panels
remain separate complete component forests; no easier whole-panel substitute
is selected.
"""
    else:
        protocol = """Each forest receives its full original `accept_strict.py` or
`accept_strict_v2.py` execution. These originals use a source-specific four- or
five-dimensional root box
and flat split/leaf paths for every literal count. The original representation,
all closed branches and each checker's own control count are retained; a
24-control schema is not imposed on a different checker family.
Retained auxiliary predecessor contracts keep their own literal allowance;
they are not relabelled as zero-allowance sharp contracts.
"""
    intro = f"""# Berry–Esseen: n{job['indices']} — complete selected conditional count replay

Choose a **CPU** runtime, upload this notebook and select **Runtime → Run all**.
Authorize the Google Drive used by the other proof jobs. Source packages are
downloaded and hash-checked automatically. No path, source or parameter edits
are required. Keep only one running copy of this same numbered job.

This batch replays all {job['forests']} selected forests in the n{job['indices']}
COUNT lane. The exact complete root/node/leaf census is bound by the frozen
catalog and printed at the start. Every selected candidate leaf is recomputed
by its original mathematical acceptor. Original mathematical sources, contracts
and candidate bytes remain unchanged. No new tree search is performed.

{protocol}
Each source-complete numbered conditional count batch may run in parallel with
the other available batches. A lane with a missing mandatory candidate is
withheld by the generator and rejected before computation. These count jobs do
not acquire the INITIAL/resource/support/Fourier facts,
sequential predecessor conclusions or same-witness interfaces that justify
their literal contracts. Historical selection receipts identify inputs only;
their old PASS fields do not replace a fresh acceptance.

The entire newly generated acceptance receipt is captured after the supervised
process group stops and is checked against the actual logs, source closure,
literal index, candidate, contract and full expected numerical/control fields.
Only each source family's explicitly declared execution metadata is variable.

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

Successful completion records the complete selected conditional count arithmetic
only. Native-platform acceptance, full parent-fact acquisition, unrestricted
finite-index conclusions and the all-index theorem remain unverified. Those
acceptance flags remain false. Acquisition, analytic/source-to-lemma and final
regional composition work remains separate.
"""
    fixtures = '''print("Checking selected finite10–39 source, count, complete-stage cache and evidence fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite1039-counts.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite1039*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Selected finite COUNT infrastructure fixtures failed; computation will not start. Log: " + str(DRIVER_SELFTEST))
print("Selected finite COUNT infrastructure fixtures: PASS.", flush=True)
'''
    cells = [base.cell("markdown", intro, "instructions"), *base.common(pin, "finite1039-counts-"+lane),
             base.cell("code", fixtures, "finite1039-count-fixtures"),
             base.cell("code", "from be_replay.finite1039_counts import run_colab\n"
                       f"RESULT = run_colab({lane!r}, durable_root=DURABLE, backup_interval=60)\n", "execute-task"),
             base.finish()]
    for item in cells:
        if item["cell_type"] == "code":
            compile("".join(item["source"]), job["name"], "exec")
    return base.notebook(cells, job["name"]+".ipynb")


def build_all(pin):
    validate_pin(pin)
    ready = ready_lanes()
    return {job["name"]: build(pin, lane) for lane, job in JOBS.items() if lane in ready}


def write(pin, output):
    docs = build_all(pin)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, doc in docs.items():
        path = output/(name+".ipynb")
        path.write_bytes((json.dumps(doc, ensure_ascii=False, indent=2)+"\n").encode("utf-8"))
        paths.append(path)
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, default=ROOT/"colab")
    args = parser.parse_args()
    for path in write(args.code_commit, args.output):
        print(path)


if __name__ == "__main__":
    main()
