"""Build the ten queued auxiliary-bound Colab notebooks, numbered 14--23."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("aux24_private_phase2_builder", ROOT / "tools/make_phase2_notebooks.py")
phase2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase2)

PARALLEL = """This is a queued CPU job. Start it when a session is available.
Notebooks 14–22 may run in parallel: their arithmetic is conditional on explicitly
recorded predecessor and analytic premises, which are joined separately afterward.
Do not run concurrent copies of the same job. Existing notebooks 01–07 and 09/10
remain useful conditional computations and do not need restarting for this work.

Progress and elapsed time are shown automatically. Logs are preserved, with live
Google Drive copies every minute and a final results ZIP on completion or handled
failure. A partial computation remains incomplete; a budget is not a runtime estimate.
Each numerical action has a 7,200-second CPU ceiling and 7,260-second wall limit.
The whole job may contain several actions and can outlive a Colab allocation.
"""

JOBS = {
    "14_auxiliary21": dict(
        task="auxiliary21", tests="test_aux21_23.py",
        title="auxiliary21: the five complete INITIAL covers",
        scope=PARALLEL + """
This job replays all five original covers, totaling 92,160 signed rectangles,
under the universal C20 <= 469/1000 input. The auxiliary target is
C21 < CE + 11/210. It does not claim the sharp C21 bound.
Source identities and the selected execution contract are checked separately
from the arithmetic result. A completed calculation remains conditional evidence;
the final auxiliary theorem and the global proof are not accepted by this notebook.
""",
        execute="from be_replay.aux21_23 import run_colab\nRESULT = run_colab('21', durable_root=DURABLE)\n"),
    "15_auxiliary22": dict(
        task="auxiliary22", tests="test_aux21_23.py",
        title="auxiliary22: INITIAL, all resource panels and nine forests",
        scope=PARALLEL + """
The unchanged full acceptors recalculate seven INITIAL covers (129,024 signed
rectangles), all 100 resource panels and all nine selected count forests
(258 leaves). Archived proof objects are untrusted candidates, not imported
acceptances. The target C22 < CE + 9/220 retains its auxiliary21 predecessor
premise until the separate evidence join. It is not a sharp C22 or global result.
""",
        execute="from be_replay.aux21_23 import run_colab\nRESULT = run_colab('22', durable_root=DURABLE)\n"),
    "16_auxiliary23": dict(
        task="auxiliary23", tests="test_aux21_23.py",
        title="auxiliary23: INITIAL, all resource panels and 21 forests",
        scope=PARALLEL + """
The unchanged full acceptors recalculate nine INITIAL covers (165,888 signed
rectangles), all 100 resource panels and all 21 selected count forests
(18,377 leaves). The selected optimization comparison is a separate BASIC
subprocess stage, so the whole job does not claim trusted native acceptance.
The target C23 < CE + 3/115 retains its auxiliary22 predecessor premise.
Complete conditional arithmetic is distinct from an acquired auxiliary theorem.
""",
        execute="from be_replay.aux21_23 import run_colab\nRESULT = run_colab('23', durable_root=DURABLE)\n"),
}

BRANCHES = {
    "b0": ("[1,11/10]", "12 forests, 1,929 leaves", "both original resource implementations and their fixed-point comparison"),
    "b1": ("[11/10,6/5]", "nine forests, 9,803 leaves", "both original resource implementations and their fixed-point comparison"),
    "b2": ("[6/5,13/10]", "nine selected forests, 26,625 leaves", "the full mean-floor local and resource patch, plus the fixed-point comparison"),
    "b3": ("[13/10,7/5]", "eight forests, 12,484 leaves", "the selected six/four-cover local schedule, including its required second cycles"),
    "b4": ("[7/5,3/2]", "eight forests, 4,168 leaves", "the complete four-cover local acquisition for each actual global survivor"),
    "b5": ("[3/2,712569/449000]", "seven forests, 2,444 leaves", "the complete four-cover local acquisition for each actual global survivor"),
}

for number, (branch, (rho, count, local)) in enumerate(BRANCHES.items(), 17):
    JOBS[f"{number:02d}_stronger24_{branch}"] = dict(
        task="stronger24-" + branch, tests="test_strong24_branches.py",
        title=f"stronger24 {branch.upper()}: the complete rho branch {rho}",
        scope=PARALLEL + f"""
This job replays the complete original {branch.upper()} branch for the auxiliary target
C24 < CE + 1/80: global INITIAL, all 100 probability panels, {local},
and every selected surviving count forest ({count}). Resource-to-count numeric
interfaces are recorded afresh. The auxiliary23 and analytic premises remain
separate until the final join; this branch alone is not a complete C24 theorem.

The unchanged sources use BASIC process-tree supervision, including numerical
subprocesses where required. This job does not claim trusted native execution
acceptance. An interrupted action requires a new attempt; no partial prefix is
automatically accepted. Source and execution evidence keep that boundary explicit.
""",
        execute=f"from be_replay.strong24_branches import run_colab\nRESULT = run_colab('{branch}', durable_root=DURABLE)\n")

JOBS["23_auxiliary24_final_join"] = dict(
    task="auxiliary24-final-join", tests="test_aux24*.py",
    title="auxiliary24: final join of the nine completed evidence bundles",
    scope="""Run this notebook LAST, after notebooks 14–22 have finished successfully and
their results ZIPs have been saved on the same Google Drive. Those preceding
jobs may run in parallel; this final join depends on all nine completed bundles.
It does not require restarting notebooks 01–07 or 09/10.

The join discovers the completed auxiliary21–23 and stronger24 B0–B5 evidence
on Drive, then checks its precise source and receipt identities, complete stage
censuses, captured outcomes and mathematical interfaces. A filename or historical
PASS label does not establish a fresh computation. Missing, partial or incompatible
evidence cannot become a successful join.

This revision also checks the actual preserved launch, supervisor result,
native worker/controller guard receipts and captures for every stage. It
keeps BASIC stages explicitly conditional and does not rerun the numerical
jobs. Existing valid14--22 exports can be used without restarting them.

This notebook assembles recorded evidence rather than rerunning the heavy numerical
jobs. The stated auxiliary fact is C24 < CE + 1/80, not the sharp C24 bound.
Remaining analytic premises, execution-contract limitations and the global proof
remain explicit. The final scoped result and an evidence ZIP are saved to Drive.
""",
    execute="from be_replay.aux24_join import run_colab\nRESULT = run_colab(durable_root=DURABLE)\n")

# This is a private imported helper instance. Reusing its exact build/common/
# finish path changes no generator file and never touches notebooks 01--13.
phase2.JOBS = JOBS


def build(pin, name):
    if not isinstance(pin, str) or not re.fullmatch(r"[0-9a-f]{40}", pin):
        raise ValueError("Immutable full Git commit required")
    if name not in JOBS:
        raise ValueError("One of the ten queued auxiliary jobs is required")
    return phase2.build(pin, name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pin", "--code-commit", dest="code_commit", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "colab")
    parser.add_argument("--jobs", nargs="+", choices=tuple(JOBS), default=list(JOBS))
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.code_commit):
        raise ValueError("Immutable full Git commit required")
    args.output.mkdir(parents=True, exist_ok=True)
    for name in args.jobs:
        path = args.output / (name + ".ipynb")
        path.write_text(json.dumps(build(args.code_commit, name), ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")
        print(path)


if __name__ == "__main__":
    main()
