"""Record real local-pilot tests and CLI runs; never claim the full proof."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from be.codec import canonical_bytes, load_json
from be.runner import environment_snapshot
from be.semantic import derive_problem, freeze_request, authorized_readback


def main():
    started = time.monotonic()
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), PYTHONDONTWRITEBYTECODE="1")
    checks = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                            cwd=ROOT, env=env, capture_output=True, timeout=240)
    log = checks.stdout + checks.stderr
    (ROOT / "verification/local-pilot-check.log").write_bytes(log)
    if checks.returncode:
        sys.stdout.buffer.write(log[-16000:])
        raise SystemExit("Local-pilot suite failed; no successful report written")
    count = re.search(rb"Ran (\d+) tests", log)
    if count is None:
        raise SystemExit("Test count missing")
    print("Unit, adversarial and process-recovery tests passed", flush=True)
    cases = []
    with tempfile.TemporaryDirectory(prefix="be-") as temporary:
        folder = Path(temporary)
        for label, relative, state, expected in (
            ("cold", "project.toml", folder / "main", 0),
            ("resume", "project.toml", folder / "main", 0),
            ("feasible", "feasible/project.toml", folder / "feasible", 2),
            ("wide-rho", "wide-rho/project.toml", folder / "wide", 2),
        ):
            command = [sys.executable, "-m", "be", "run", str(ROOT / "examples/local-pilot" / relative),
                       "--resume", "--state-dir", str(state)]
            completed = subprocess.run(command, cwd=folder, env=env, capture_output=True, timeout=90)
            report = json.loads(completed.stdout)
            if completed.returncode != expected or report.get("full_proof_pass") is not False:
                raise SystemExit("Unexpected actual CLI outcome: " + label + " " + repr(report))
            cases.append({"case": label, "exit_code": completed.returncode, "report": report})
    a, b = cases[0]["report"], cases[1]["report"]
    if a["producer_cache_hit"] or a["verifier_cache_hit"] or not b["producer_cache_hit"] or not b["verifier_cache_hit"]:
        raise SystemExit("Cache execution controls failed")
    for field in ("campaign_id", "frozen_digest", "candidate_ref", "receipt_ref", "attempts_total"):
        if a[field] != b[field]:
            raise SystemExit("Resume binding changed: " + field)
    if a["run_id"] == b["run_id"] or a["attempts_total"] != "2":
        raise SystemExit("Expected distinct CLI invocations with two total attempts")
    examples = ROOT / "examples/local-pilot"
    request = freeze_request(*(load_json(examples / name) for name in (
        "problem.json", "source-manifest.json", "trust-profile.json")))
    from be.producer import produce_request
    from be.semantic import verify_request
    candidate = produce_request(request)
    receipt = verify_request(request, candidate)
    authorized_readback(request, candidate, receipt)
    evidence = ROOT / "verification/local-pilot-evidence"
    evidence.mkdir(exist_ok=True)
    for name, value in (("request.json", request), ("candidate.json", candidate),
                        ("receipt.json", receipt), ("derived-problem.json", derive_problem(request))):
        (evidence / name).write_bytes(canonical_bytes(value))
    from render_proof_map import load_checked_report
    lean = load_checked_report()
    inventory = [*ROOT.joinpath("src/be").glob("*.py"), *ROOT.joinpath("schemas/local-pilot").glob("*.json"),
                 *ROOT.joinpath("tests").glob("*.py"), ROOT / "pyproject.toml",
                 ROOT / "tools/requirements-local-pilot.txt", ROOT / "tools/requirements-local-pilot-build.txt"]
    report = dict(checked_at=datetime.now(timezone.utc).isoformat(),
                  scope="be.local-pilot/1 zero-noise joint-cubic exclusion only",
                  tests_passed=True, test_count=int(count[1]), cli_cases=cases,
                  full_proof_pass=False, paid_cloud_resources_created=False,
                  lean_recompiled=False, unchanged_lean_sources=len(lean["modules"]),
                  environment=environment_snapshot(),
                  clean_venv=sys.prefix != sys.base_prefix and
                    "include-system-site-packages = false" in (Path(sys.prefix) / "pyvenv.cfg").read_text(),
                  code_and_schema_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                         for p in sorted(inventory)},
                  total_seconds=round(time.monotonic()-started, 3))
    (ROOT / "verification/local-pilot-check.json").write_text(json.dumps(report, indent=2)+"\n",
                                                             encoding="utf-8", newline="\n")
    print(json.dumps({"tests_passed":True, "test_count":int(count[1]),
                      "cli_exit_codes":[c["exit_code"] for c in cases], "full_proof_pass":False}))


if __name__ == "__main__":
    main()
