"""Local source-bound vertical slice; deliberately not the full proof runner."""
from __future__ import annotations

import hashlib
import importlib.metadata
import math
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time
import tomllib
import uuid

from .codec import bytes_digest, canonical_bytes, digest, load_json
from .errors import ProtocolError
from .ledger import SQLiteLedger
from .schema import ROOT
from .store import LocalCAS, ordinary_directory

PROTOCOL = "be.local-pilot/1"
KIND = "empty-joint-cubics-zero-noise"
DEFAULT_LIMITS = dict(wall_seconds=30, campaign_wall_seconds=300, cpu_seconds=30,
                      memory_bytes=512 * 1024 * 1024, output_bytes=1024 * 1024,
                      log_bytes=256 * 1024, lease_seconds=30, heartbeat_seconds=5,
                      maximum_attempts=3)
MAXIMUM_LIMITS = dict(wall_seconds=1200, campaign_wall_seconds=604800, cpu_seconds=1200,
                      memory_bytes=2 * 1024**3, output_bytes=4 * 1024 * 1024,
                      log_bytes=4 * 1024 * 1024, lease_seconds=300, heartbeat_seconds=60,
                      maximum_attempts=10)


def _file_digest(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ProtocolError("source_file_missing", "Required ordinary source/environment file is absent")
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return "sha256:" + hasher.hexdigest()


def environment_snapshot() -> dict:
    """Pin actual profile bytes, executable and installed locked dependencies."""
    if sys.version_info[:2] != (3, 12):
        raise ProtocolError("unsupported_python_version", "This explicit pilot profile requires CPython 3.12")
    if platform.python_implementation() != "CPython":
        raise ProtocolError("unsupported_python_implementation", "This profile requires the pinned CPython runtime")
    import fractions
    import json
    import decimal
    import _decimal
    source = {}
    for directory in (ROOT / "src/be", ROOT / "schemas/local-pilot"):
        for path in sorted(directory.rglob("*")):
            if path.is_file() and path.suffix in (".py", ".json") and "__pycache__" not in path.parts:
                source[path.relative_to(ROOT).as_posix()] = _file_digest(path)
    if not source:
        raise ProtocolError("missing_profile_sources", "Editable checkout with the public source/schema bundle is required")
    locks = {name: _file_digest(ROOT / name) for name in ("pyproject.toml", "tools/requirements-local-pilot.txt")}
    dependencies = {}
    for line in (ROOT / "tools/requirements-local-pilot.txt").read_text("utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line or line.startswith("-"):
            raise ProtocolError("unsupported_dependency_lock", "Only exact package pins are supported")
        name, required = line.split("==", 1)
        try:
            distribution = importlib.metadata.distribution(name)
        except importlib.metadata.PackageNotFoundError as exc:
            raise ProtocolError("dependency_missing", "Install the exact public local-pilot lock") from exc
        if distribution.version != required:
            raise ProtocolError("dependency_version_mismatch", "Installed package differs from the frozen lock: " + name)
        files = {}
        for entry in sorted(distribution.files or [], key=str):
            if "__pycache__" in entry.parts or str(entry).endswith(".pyc"):
                continue
            path = Path(distribution.locate_file(entry))
            if path.is_file():
                files[str(entry).replace("\\", "/")] = _file_digest(path)
        if not files:
            raise ProtocolError("dependency_inventory_missing", "Installed dependency lacks its file inventory")
        dependencies[name] = dict(version=required, files_digest=digest("dependency-files", files))
    stdlib = {}
    for module in (fractions, json, decimal, _decimal, math):
        if getattr(module, "__file__", None):
            stdlib[module.__name__] = _file_digest(Path(module.__file__))
    executable = Path(sys.executable).resolve()
    dlls = {path.name: _file_digest(path) for path in sorted(Path(sys.base_prefix).glob("python3*.dll"))}
    return dict(profile="pure-python-exact-local-pilot-v1", implementation=platform.python_implementation(),
                python_version=platform.python_version(), executable_digest=_file_digest(executable),
                platform=sys.platform, architecture=platform.machine(), optimization=str(sys.flags.optimize),
                profile_sources=source, locks=locks, dependencies=dependencies, core_stdlib=stdlib, runtime_libraries=dlls,
                enforcement=dict(wall=True, output_bytes=True, per_process_cpu=os.name == "posix",
                                 per_process_address_space=os.name == "posix", kernel_group_memory=False))


def load_project(path: Path | str, state_dir: Path | str | None = None) -> dict:
    path = Path(path).absolute()
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 65536:
        raise ProtocolError("invalid_project", "Expected a bounded ordinary TOML project")
    try:
        project = tomllib.loads(path.read_text("utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ProtocolError("invalid_project", "Invalid project TOML") from exc
    allowed = {"schema_version", "kind", "problem", "source_manifest", "trust_profile", "source_root", "state_dir", "limits"}
    if set(project) - allowed or project.get("schema_version") != PROTOCOL or project.get("kind") != KIND:
        raise ProtocolError("unsupported_project", "Only the explicit local pilot project is implemented")
    def local_path(key):
        value = project.get(key)
        if not isinstance(value, str) or not value or "\x00" in value:
            raise ProtocolError("invalid_project", "Missing project path: " + key)
        result = Path(value)
        return (result if result.is_absolute() else path.parent / result).absolute()
    limits = dict(DEFAULT_LIMITS)
    supplied = project.get("limits", {})
    if type(supplied) is not dict or set(supplied) - set(limits):
        raise ProtocolError("unsupported_resource_profile", "Unknown local pilot resource limit")
    for key, value in supplied.items():
        if isinstance(value, str) and value.isascii() and value.isdecimal() and (value == "0" or not value.startswith("0")):
            value = int(value)
        if type(value) is not int or not 1 <= value <= MAXIMUM_LIMITS[key]:
            raise ProtocolError("invalid_resource_limit", "Invalid bounded limit: " + key)
        limits[key] = value
    if 3 * limits["heartbeat_seconds"] >= limits["lease_seconds"]:
        raise ProtocolError("invalid_lease_policy", "Heartbeat must be shorter than one third of lease TTL")
    raw_state = state_dir if state_dir is not None else project.get("state_dir", ".be-local-pilot")
    if not isinstance(raw_state, (str, Path)) or not str(raw_state) or "\x00" in str(raw_state):
        raise ProtocolError("invalid_project", "State directory must be a nonempty local path")
    selected_state = Path(raw_state)
    if not selected_state.is_absolute():
        selected_state = path.parent / selected_state
    source_root = local_path("source_root") if "source_root" in project else ROOT
    return dict(path=path, state_dir=selected_state.absolute(), source_root=source_root,
                problem=local_path("problem"), source_manifest=local_path("source_manifest"),
                trust_profile=local_path("trust_profile"), limits=limits)


def _stop_process(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    else:
        process.terminate()
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        else:
            process.kill()
        process.wait(timeout=5)


def _posix_limits(limits):
    def apply():
        import resource
        resource.setrlimit(resource.RLIMIT_CPU, (limits["cpu_seconds"], limits["cpu_seconds"]))
        resource.setrlimit(resource.RLIMIT_AS, (limits["memory_bytes"], limits["memory_bytes"]))
        maximum = max(limits["output_bytes"], limits["log_bytes"])
        resource.setrlimit(resource.RLIMIT_FSIZE, (maximum, maximum))
    return apply


def run_worker(operation: str, request: dict, candidate: dict | None, *, directory: Path,
               limits: dict, deadline: float, ledger: SQLiteLedger, fence: dict) -> tuple[dict, dict]:
    if os.name == "posix":
        import threading
        if threading.active_count() != 1:
            raise ProtocolError("unsupported_threaded_launcher", "The POSIX rlimit subprocess launcher requires a single-threaded parent")
    directory = ordinary_directory(directory)
    request_path, output_path = directory / "request.json", directory / "output.json"
    if os.name == "nt" and any(len(str(directory / name)) >= 260 for name in
                              ("request.json", "candidate.json", "output.json", "stdout.log", "stderr.log")):
        raise ProtocolError("path_too_long", "This pilot Windows profile requires a shorter --state-dir")
    request_path.write_bytes(canonical_bytes(request))
    arguments = [sys.executable, "-m", "be.worker", operation, "--request", str(request_path), "--output", str(output_path)]
    if candidate is not None:
        candidate_path = directory / "candidate.json"
        candidate_path.write_bytes(canonical_bytes(candidate))
        arguments += ["--candidate", str(candidate_path)]
    environment = {k: v for k, v in os.environ.items() if k in
                   ("PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "HOME", "USERPROFILE", "LANG", "LC_ALL")}
    environment.update(PYTHONPATH=str(ROOT / "src"), PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1",
                       PYTHONHASHSEED="0", PYTHONSAFEPATH="1")
    stdout_path, stderr_path = directory / "stdout.log", directory / "stderr.log"
    now = time.time()
    allowed_wall = min(limits["wall_seconds"], deadline - now)
    if allowed_wall <= 0:
        raise ProtocolError("campaign_closed", "No worker may start after the campaign deadline")
    started = time.monotonic()
    next_heartbeat = started + limits["heartbeat_seconds"]
    process = None
    try:
        with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
            process = subprocess.Popen(arguments, cwd=directory, env=environment, stdin=subprocess.DEVNULL,
                                       stdout=stdout, stderr=stderr, shell=False,
                                       start_new_session=os.name == "posix",
                                       creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
                                       preexec_fn=_posix_limits(limits) if os.name == "posix" else None)
            while process.poll() is None:
                current = time.monotonic()
                if current - started >= allowed_wall or time.time() >= deadline:
                    raise ProtocolError("worker_timeout", "Bounded pilot worker reached its wall/deadline limit")
                if any(p.exists() and p.stat().st_size > limits["log_bytes"] for p in (stdout_path, stderr_path)):
                    raise ProtocolError("worker_log_limit")
                if output_path.exists() and output_path.stat().st_size > limits["output_bytes"]:
                    raise ProtocolError("worker_output_limit")
                if current >= next_heartbeat:
                    ledger.renew(fence, lease_seconds=limits["lease_seconds"])
                    next_heartbeat = current + limits["heartbeat_seconds"]
                time.sleep(0.02)
            code = process.wait()
        if any(p.stat().st_size > limits["log_bytes"] for p in (stdout_path, stderr_path)):
            raise ProtocolError("worker_log_limit")
        if code != 0:
            raise ProtocolError("worker_failed", "Fresh pilot worker failed with exit code " + str(code))
        if output_path.is_symlink() or not output_path.is_file() or output_path.stat().st_size > limits["output_bytes"]:
            raise ProtocolError("worker_output_invalid")
        output = load_json(output_path)
        return output, dict(operation=operation, returncode="0", wall_milliseconds=str(round((time.monotonic() - started) * 1000)),
                            stdout_digest=_file_digest(stdout_path), stderr_digest=_file_digest(stderr_path),
                            executable_digest=_file_digest(Path(sys.executable).resolve()))
    finally:
        if process is not None:
            _stop_process(process)


def run_project(path: Path | str, *, resume: bool = False, fresh: bool = False,
                state_dir: Path | str | None = None) -> tuple[dict, int]:
    from .semantic import authorized_readback, freeze_request, validate_source_files
    if sys.flags.optimize:
        raise ProtocolError("optimized_python_unsupported", "Pilot assertions/profile cannot be disabled")
    config = load_project(path, state_dir)
    problem, source, trust = (load_json(config[key]) for key in ("problem", "source_manifest", "trust_profile"))
    validate_source_files(source, config["source_root"])
    request = freeze_request(problem, source, trust)
    environment = environment_snapshot()
    frozen = dict(schema_version=PROTOCOL, artifact_kind="frozen_run_spec", kind=KIND,
                  request=request, environment=environment,
                  limits={k: str(v) for k, v in config["limits"].items()}, paid_activation=False,
                  full_proof_pass=False)
    frozen_digest = digest("frozen-run-spec", frozen)
    state = ordinary_directory(config["state_dir"])
    store = LocalCAS(state / "artifacts")
    frozen_ref = store.put_json(frozen, format_id="be.local-pilot/frozen-run-spec/1")
    ledger = SQLiteLedger(state / "ledger.sqlite3")
    # A state directory has one project head. TOML paths are locators, not
    # authorization to create a new campaign or reset its persisted deadline.
    project_key = "local-pilot-v1"
    campaign = ledger.campaign(project_key, frozen_digest, frozen_ref, resume=resume, fresh=fresh,
                               wall_seconds=config["limits"]["campaign_wall_seconds"])
    if campaign["frozen_ref"] != frozen_ref or store.read_json(campaign["frozen_ref"]) != frozen:
        raise ProtocolError("frozen_state_mismatch", "Ledger and immutable frozen inputs disagree")
    run_id = "run:" + str(uuid.uuid4())
    cache = {}
    refs = {}
    candidate = None
    receipt = None
    for operation in ("produce", "verify"):
        spec = dict(frozen_digest=frozen_digest, operation=operation)
        if operation == "verify":
            spec["candidate_ref"] = refs["produce"]
        job_id = ledger.ensure_job(campaign["campaign_id"], digest("job-spec", spec), operation)
        job = ledger.get_job(job_id)
        if job["state"] == "produced":
            metadata = job["completion_metadata"]
            if (type(metadata) is not dict or metadata.get("frozen_digest") != frozen_digest
                    or metadata.get("operation") != operation or metadata.get("returncode") != "0"):
                raise ProtocolError("unauthorized_cache_receipt", "Cached completion lacks its exact execution binding")
            for log in ("stdout_ref", "stderr_ref"):
                if log not in metadata:
                    raise ProtocolError("unauthorized_cache_receipt", "Cached completion lacks its immutable diagnostic binding")
                store.read_bytes(metadata[log])
            output = store.read_json(job["output_ref"])
            ref = job["output_ref"]
            cache[operation] = True
        else:
            fence = ledger.claim(job_id, run_id, lease_seconds=config["limits"]["lease_seconds"],
                                 maximum_attempts=config["limits"]["maximum_attempts"])
            attempt_dir = state / "attempts" / fence["attempt_id"].replace(":", "_")
            try:
                output, metadata = run_worker(operation, request, candidate, directory=attempt_dir,
                                              limits=config["limits"], deadline=campaign["deadline"], ledger=ledger, fence=fence)
                if environment_snapshot() != environment:
                    raise ProtocolError("environment_changed_during_execution")
                validate_source_files(source, config["source_root"])
                ref = store.put_json(output, format_id="be.local-pilot/" + operation + "/1")
                metadata.update(frozen_digest=frozen_digest)
                for log in ("stdout", "stderr"):
                    metadata[log + "_ref"] = store.put_bytes((attempt_dir / (log + ".log")).read_bytes(),
                        media_type="text/plain", format_id="be.local-pilot/worker-log/1")
                ledger.complete(fence, ref, operation_key="complete:" + fence["attempt_id"], metadata=metadata)
                cache[operation] = False
            except BaseException as exc:
                try:
                    ledger.fail(fence, getattr(exc, "code", "interrupted"))
                except ProtocolError:
                    pass  # An expired/superseded attempt cannot mutate newer state.
                raise
        refs[operation] = ref
        if operation == "produce":
            candidate = output
        else:
            receipt = output
    receipt = authorized_readback(request, candidate, receipt)
    outcome = receipt["core"]["outcome"]
    status, code = ("PILOT_PASS", 0) if outcome == "infeasible" else (("PILOT_NO_PASS", 2) if outcome == "no_contradiction" else ("PILOT_NO_PASS", 4))
    report = dict(schema_version=PROTOCOL, artifact_kind="run_report", status=status, outcome=outcome,
                  campaign_id=campaign["campaign_id"], run_id=run_id, frozen_digest=frozen_digest,
                  producer_cache_hit=cache["produce"], verifier_cache_hit=cache["verify"],
                  candidate_ref=refs["produce"], receipt_ref=refs["verify"],
                  request_id=request["request_id"], proof_scope=receipt["core"]["proof_scope"],
                  conditional=True, full_proof_pass=False, paid_activation=False,
                  authorized_readback=True, attempts_total=str(ledger.attempt_count(campaign["campaign_id"])))
    report_ref = store.put_json(report, format_id="be.local-pilot/run-report/1")
    ledger.finish_campaign(campaign["campaign_id"], report_ref)
    return report, code
