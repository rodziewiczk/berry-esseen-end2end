"""One explicit local pilot command; unsupported full-proof modes fail closed."""
from __future__ import annotations

import argparse
from pathlib import Path
import sqlite3
import subprocess
import sys

from .codec import canonical_bytes
from .errors import ProtocolError
from .runner import run_project


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="be", description="Source-bound exact local pilot; not the full Berry--Esseen proof runner")
    subcommands = parser.add_subparsers(dest="command", required=True)
    run = subcommands.add_parser("run", help="Run the supported local pilot, with separately verified output")
    run.add_argument("project", type=Path)
    policy = run.add_mutually_exclusive_group()
    policy.add_argument("--resume", action="store_true")
    policy.add_argument("--fresh", action="store_true", help="Explicitly create a new no-paid local pilot campaign")
    run.add_argument("--state-dir", type=Path, help="Ordinary local durable state directory")
    args = parser.parse_args(argv)
    try:
        report, code = run_project(args.project, resume=args.resume, fresh=args.fresh, state_dir=args.state_dir)
    except ProtocolError as exc:
        incomplete = {"job_busy", "campaign_closed", "attempt_budget_exhausted", "worker_timeout"}
        code = 2 if exc.code in incomplete else (5 if exc.code in {"worker_failed", "cas_install_unsupported"} else 3)
        report = dict(schema_version="be.local-pilot/1", artifact_kind="run_error", status="PILOT_NO_PASS",
                      error=exc.as_dict(), full_proof_pass=False, paid_activation=False)
    except KeyboardInterrupt:
        code = 2
        report = dict(schema_version="be.local-pilot/1", artifact_kind="run_error", status="PILOT_NO_PASS",
                      error=dict(code="interrupted", message="Local pilot interrupted; committed stages remain resumable"),
                      full_proof_pass=False, paid_activation=False)
    except OSError:
        code = 5
        report = dict(schema_version="be.local-pilot/1", artifact_kind="run_error", status="PILOT_NO_PASS",
                      error=dict(code="local_io_failure", message="Local state or process operation failed"),
                      full_proof_pass=False, paid_activation=False)
    except (sqlite3.Error, subprocess.SubprocessError):
        code = 5
        report = dict(schema_version="be.local-pilot/1", artifact_kind="run_error", status="PILOT_NO_PASS",
                      error=dict(code="local_runtime_failure", message="Local ledger or process supervision failed"),
                      full_proof_pass=False, paid_activation=False)
    sys.stdout.buffer.write(canonical_bytes(report) + b"\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
