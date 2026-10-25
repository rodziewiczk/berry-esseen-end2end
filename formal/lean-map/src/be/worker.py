"""One bounded producer or verifier operation in a fresh subprocess."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile

from .codec import canonical_bytes, load_json
from .errors import ProtocolError
from .producer import produce_request
from .semantic import verify_request


def _write_atomic(path: Path, value: dict) -> None:
    raw = canonical_bytes(value)
    if os.name == "nt" and len(str(path.absolute())) >= 260:
        raise ProtocolError("output_path_too_long", "Output path exceeds the enabled Windows pilot path profile")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        fd, name = tempfile.mkstemp(prefix=".o-", dir=path.parent)
        temporary = Path(name)
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except OSError as exc:
        if os.name == "nt" and getattr(exc, "winerror", None) == 206:
            raise ProtocolError("output_path_too_long", "Output path exceeds the enabled Windows pilot path profile") from exc
        raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m be.worker")
    sub = parser.add_subparsers(dest="operation", required=True)
    for name in ("produce", "verify"):
        child = sub.add_parser(name)
        child.add_argument("--request", type=Path, required=True)
        child.add_argument("--output", type=Path, required=True)
        if name == "verify":
            child.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args(argv)
    if sys.flags.optimize:
        sys.stderr.write("ProtocolError: optimized Python execution is not an enabled pilot profile\n")
        return 3
    try:
        request = load_json(args.request)
        result = produce_request(request) if args.operation == "produce" else verify_request(request, load_json(args.candidate))
        _write_atomic(args.output, result)
        summary = {"operation": args.operation, "status": "produced",
                   "full_proof_pass": False}
        if args.operation == "verify":
            summary["outcome"] = result["core"]["outcome"]
        sys.stdout.buffer.write(canonical_bytes(summary) + b"\n")
        return 0
    except ProtocolError as exc:
        sys.stderr.buffer.write(canonical_bytes({"error": exc.as_dict()}) + b"\n")
        return 3
    except (OSError, ValueError):
        sys.stderr.write("WorkerError: local input/output operation failed\n")
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
