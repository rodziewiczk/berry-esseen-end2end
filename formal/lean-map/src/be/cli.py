"""One command for explicitly typed, independently checked proof stages."""
from __future__ import annotations

import argparse
from pathlib import Path
import sqlite3
import subprocess
import sys
import tomllib

from .codec import canonical_bytes
from .errors import ProtocolError
from .runner import run_project as run_pilot


def project_header(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 65536:
        raise ProtocolError("invalid_project", "Expected a bounded ordinary TOML project")
    try:
        header = tomllib.loads(path.read_text("utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ProtocolError("invalid_project", "Invalid project TOML") from exc
    return header


def run_project(path, **options):
    header = project_header(path)
    if header.get("schema_version") == "be.count-native/1":
        from .count_runner import run_project as run_count
        return run_count(path, **options)
    return run_pilot(path, **options)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="be", description="Fresh construction and separate verification of explicitly supported proof stages")
    subcommands = parser.add_subparsers(dest="command", required=True)
    run = subcommands.add_parser("run", help="Run a typed project, with separately verified output")
    run.add_argument("project", type=Path)
    policy = run.add_mutually_exclusive_group()
    policy.add_argument("--resume", action="store_true")
    policy.add_argument("--fresh", action="store_true", help="Explicitly create a new no-paid local campaign")
    run.add_argument("--state-dir", type=Path, help="Ordinary local durable state directory")
    args = parser.parse_args(argv)
    protocol, failure_status = "be.local-pilot/1", "PILOT_NO_PASS"
    try:
        if project_header(args.project).get("schema_version") == "be.count-native/1":
            protocol, failure_status = "be.count-native/1", "COUNT_NO_PASS"
        report, code = run_project(args.project, resume=args.resume, fresh=args.fresh, state_dir=args.state_dir)
    except ProtocolError as exc:
        incomplete = {"job_busy", "campaign_closed", "attempt_budget_exhausted", "worker_timeout", "native_timeout"}
        code = 2 if exc.code in incomplete else (5 if exc.code in {"worker_failed", "cas_install_unsupported"} else 3)
        report = dict(schema_version=protocol, artifact_kind="run_error", status=failure_status,
                      error=exc.as_dict(), full_proof_pass=False, paid_activation=False)
    except KeyboardInterrupt:
        code = 2
        report = dict(schema_version=protocol, artifact_kind="run_error", status=failure_status,
                      error=dict(code="interrupted", message="Project interrupted; committed stages remain resumable"),
                      full_proof_pass=False, paid_activation=False)
    except OSError:
        code = 5
        report = dict(schema_version=protocol, artifact_kind="run_error", status=failure_status,
                      error=dict(code="local_io_failure", message="Local state or process operation failed"),
                      full_proof_pass=False, paid_activation=False)
    except (sqlite3.Error, subprocess.SubprocessError):
        code = 5
        report = dict(schema_version=protocol, artifact_kind="run_error", status=failure_status,
                      error=dict(code="local_runtime_failure", message="Local ledger or process supervision failed"),
                      full_proof_pass=False, paid_activation=False)
    sys.stdout.buffer.write(canonical_bytes(report) + b"\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
