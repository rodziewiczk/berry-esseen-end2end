"""Build only the two conditional finite6--9 parent notebooks; LF output."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("finite69_parent_notebook_base", ROOT / "tools/make_notebooks.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

JOBS = {
    "n6": dict(name="44_n6_conditional_parents", actions=41, covers=133, controls=872),
    "initial7_9": dict(name="45_n7_9_conditional_initial", actions=9, covers=81, controls=243),
}


def validate_pin(pin):
    if type(pin) is not str or re.fullmatch(r"[0-9a-f]{40}", pin) is None or pin == "0" * 40:
        raise ValueError("A nonplaceholder immutable full runtime commit is required")


def build(pin, lane):
    validate_pin(pin)
    if type(lane) is not str or lane not in JOBS:
        raise ValueError("One literal selected parent lane: n6 or initial7_9")
    job = JOBS[lane]
    if lane == "n6":
        title = "n6 — complete selected conditional parent arithmetic"
        selection = """This batch runs all 41 selected n6 parent actions: four full INITIAL
acceptances, 17 local INITIAL acceptances, three full 100-panel resource
acceptances and 17 local resource acceptances. The INITIAL stages cover all
133 selected covers, with 2,592 cells per cover. Every original control is
required: 872 named controls across the complete batch. Four full INITIAL
jobs use 20 controls each; 15 local INITIAL jobs use 29 and two use 27; the
three full resource jobs use 16 each and 17 local resource jobs use 15 each.

The exact selected source, candidate and conditional parent-input bytes are
sealed. Fresh parent evidence is checked along the selected job dependencies;
the metadata comparison permits only the original top-level elapsed time to
differ. It does not acquire an omitted analytic or Fourier premise.
"""
    else:
        title = "n7–9 — complete selected conditional INITIAL arithmetic"
        selection = """This batch runs all 9 selected n7–9 INITIAL acceptances: three
literal bands for each of n7, n8 and n9. Each job checks all nine covers, with
2,592 cells per cover, all 100 panels and all 27 original controls. The batch
therefore requires all 81 selected covers and all 243 named controls.

Missing original preparation metadata is reconstructed only when the result
matches its externally pinned historical bytes. Missing historical timed
acceptance receipts are not fabricated. Each selected INITIAL acceptance is
performed freshly with the original mathematical sources and candidate bytes.
The n7–9 resource/CAPS acquisition and its fresh interfaces remain separate.
"""
    intro = f"""# Berry–Esseen: {title}

Choose a **CPU** runtime, upload this notebook and select **Runtime → Run all**.
Authorize the Google Drive used by the other proof jobs. Source packages are
downloaded and hash-checked automatically. No path, source or parameter edits
are required. Keep only one running copy of this same numbered job.

{selection}
Notebooks 44 and 45 are separate conditional parent jobs and may run in
parallel with the conditional count notebooks 40–43. They do not replace those
count replays. Parent facts, the complete support/Fourier and predecessor
premises, the source-to-lemma arguments and the finite6–9 theorem joins remain
separate proof obligations.

Progress is printed at least every 20 seconds during a job. Logs are backed up
every 60 seconds. Each fully validated completed action is exported as a ZIP
with its SHA-256 sidecar on Google Drive. Run all again with this same pinned
notebook to revalidate and reuse completed-stage exports. Interrupted native
acceptance restarts fully; partial numerical results are never accepted or
resumed. The final results ZIP is saved on success or handled failure.

Each action has a 2 GiB memory policy, a 43,200-second per-process CPU ceiling
and a 54,000-second external wall ceiling. BASIC protection uses per-process
limits and sampled live process-group CPU/RSS observations. Cumulative
whole-tree CPU, aggregate kernel memory enforcement and cgroup/Windows-Job
equivalence are not claimed. These are budgets per action, not a runtime
estimate for the complete batch.

Successful completion records selected conditional parent arithmetic and
checked fresh metadata interfaces only. Native-platform acceptance, full
parent-fact acquisition, the unrestricted finite6–9 conclusions and the
all-index theorem remain unverified. The corresponding acceptance flags
remain false.
"""
    fixtures = '''print("Checking finite6–9 parent source, complete-stage cache and evidence fixtures. No original mathematics is evaluated.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite69-parents.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_finite69_parent*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Finite6–9 parent infrastructure fixtures failed; computation will not start. Log: " + str(DRIVER_SELFTEST))
print("Finite6–9 parent infrastructure fixtures: PASS.", flush=True)
'''
    cells = [base.cell("markdown", intro, "instructions"),
             *base.common(pin, "finite69-parents-" + lane),
             base.cell("code", fixtures, "finite69-parent-fixtures"),
             base.cell("code", "from be_replay.finite69_parents import run_colab\n"
                       f"RESULT = run_colab({lane!r}, durable_root=DURABLE, backup_interval=60)\n", "execute-task"),
             base.finish()]
    for item in cells:
        if item["cell_type"] == "code":
            compile("".join(item["source"]), job["name"], "exec")
    return base.notebook(cells, job["name"] + ".ipynb")


def build_all(pin):
    validate_pin(pin)
    return {job["name"]: build(pin, lane) for lane, job in JOBS.items()}


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
