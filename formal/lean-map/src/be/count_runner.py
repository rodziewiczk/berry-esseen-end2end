"""Durable fresh construction and source replay of an ordinary COUNT forest.

The local seal authenticates a completed checker execution within this campaign.
It is operational trust, not a proof of the analytic hypotheses or a Lean proof.
"""
from __future__ import annotations

from pathlib import Path
import sys
import threading
import time
import tomllib
import uuid

from . import count_native as native
from .authority import LocalAuthority
from .codec import canonical_bytes, digest
from .errors import ProtocolError
from .ledger import SQLiteLedger
from .runner import environment_snapshot
from .store import LocalCAS, ordinary_directory

PROTOCOL = "be.count-native/1"
KIND = "ordinary-count-source-replay"
DEFAULT_LIMITS = dict(wall_seconds=300, campaign_wall_seconds=1800, cpu_seconds=300,
                      memory_bytes=512 * 1024 * 1024, log_bytes=1024 * 1024,
                      lease_seconds=30, heartbeat_seconds=5, maximum_attempts=3)
MAXIMUM_LIMITS = dict(wall_seconds=600, campaign_wall_seconds=604800, cpu_seconds=600,
                      memory_bytes=2 * 1024**3, log_bytes=1024 * 1024,
                      lease_seconds=300, heartbeat_seconds=60, maximum_attempts=10)


class _LeaseHeartbeat:
    """Renew through parent-side hashing as well as through native execution."""
    def __init__(self, ledger, fence, limits):
        self.ledger, self.fence, self.limits = ledger, fence, limits
        self.finished = threading.Event()
        self.error = None
        self.thread = threading.Thread(target=self._renew, name="be-count-lease", daemon=True)

    def start(self):
        self.ledger.renew(self.fence, lease_seconds=self.limits["lease_seconds"])
        self.thread.start()

    def _renew(self):
        while not self.finished.wait(self.limits["heartbeat_seconds"]):
            try:
                self.ledger.renew(self.fence, lease_seconds=self.limits["lease_seconds"])
            except BaseException as exc:
                self.error = exc
                return

    def check(self):
        if self.error is not None:
            raise self.error

    def stop(self, *, check=True):
        self.finished.set()
        if self.thread.ident is not None:
            self.thread.join(timeout=12)
            if self.thread.is_alive():
                raise ProtocolError("heartbeat_cleanup_failed", "Lease authority operation did not finish")
        if check:
            self.check()


def load_project(path: Path | str, state_dir: Path | str | None) -> dict:
    path = Path(path).absolute()
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 65536:
        raise ProtocolError("invalid_project", "Expected a bounded ordinary TOML project")
    try:
        value = tomllib.loads(path.read_text("utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ProtocolError("invalid_project", "Invalid project TOML") from exc
    if (set(value) - {"schema_version", "kind", "capsule", "state_dir", "limits"}
            or value.get("schema_version") != PROTOCOL or value.get("kind") != KIND):
        raise ProtocolError("unsupported_project", "Unknown source-replay project")
    limits = dict(DEFAULT_LIMITS)
    supplied = value.get("limits", {})
    if type(supplied) is not dict or set(supplied) - set(limits):
        raise ProtocolError("unsupported_resource_profile", "Unknown source-replay resource limit")
    for key, item in supplied.items():
        if isinstance(item, str) and item.isascii() and item.isdecimal() and not item.startswith("0"):
            item = int(item)
        if type(item) is not int or not 1 <= item <= MAXIMUM_LIMITS[key]:
            raise ProtocolError("invalid_resource_limit", "Invalid bounded limit: " + key)
        limits[key] = item
    if 3 * limits["heartbeat_seconds"] >= limits["lease_seconds"]:
        raise ProtocolError("invalid_lease_policy", "Heartbeat must be shorter than one third of lease TTL")

    def locator(raw):
        if not isinstance(raw, (str, Path)) or not str(raw) or "\x00" in str(raw):
            raise ProtocolError("invalid_project", "Nonempty ordinary local path required")
        selected = Path(raw)
        return (selected if selected.is_absolute() else path.parent / selected).absolute()

    return dict(capsule=locator(value["capsule"]) if "capsule" in value else native.DEFAULT_CAPSULE,
                state_dir=locator(state_dir if state_dir is not None else value.get("state_dir", ".be-count-native")),
                limits=limits)


def _census(value: dict) -> dict:
    return {key: ({k: str(v) for k, v in item.items()} if isinstance(item, dict) else str(item))
            for key, item in value.items()}


def _authorized_stage(record, *, authority, common, operation, candidate_ref,
                      native_runtime_digest, capsule, store):
    if type(record) is not dict or set(record) != {"payload", "seal"} or type(record["payload"]) is not dict:
        raise ProtocolError("unauthorized_cache_receipt", "Closed signed source-checker receipt required")
    payload = record["payload"]
    authority.verify(payload, record["seal"])
    fields = set(common) | {"operation", "status", "candidate_ref", "census", "verification_key",
                            "native_receipt_ref", "observation_ref", "log_ref"}
    if set(payload) != fields or any(payload.get(k) != v for k, v in common.items()):
        raise ProtocolError("unauthorized_cache_receipt", "Exact campaign, source, runtime and conditional scope required")
    status = "CANDIDATE_PRODUCED" if operation == "produce" else "SCOPED_COUNT_PASS"
    if payload["operation"] != operation or payload["status"] != status:
        raise ProtocolError("unauthorized_cache_receipt", "Wrong authorized native operation")
    if candidate_ref is not None and candidate_ref != payload["candidate_ref"]:
        raise ProtocolError("unauthorized_cache_receipt", "Verifier must cover the whole produced candidate")
    raw = store.read_bytes(payload["candidate_ref"])
    if _census(native.precheck_forest(raw, capsule)) != payload["census"]:
        raise ProtocolError("unauthorized_cache_receipt", "Complete candidate topology differs from authenticated census")
    if native.cache_key(raw, capsule, native_runtime_digest) != payload["verification_key"]:
        raise ProtocolError("unauthorized_cache_receipt", "Complete verification key differs")
    if operation == "verify":
        store.read_bytes(payload["native_receipt_ref"])
    elif payload["native_receipt_ref"] is not None:
        raise ProtocolError("unauthorized_cache_receipt", "Producer cannot claim a native acceptance")
    # These exact bytes were bound by the trusted coordinator after source replay.
    # A worker-controlled success word or an unsigned SQLite row is insufficient.
    for key in ("observation_ref", "log_ref"):
        store.read_bytes(payload[key])
    return payload


def run_project(path: Path | str, *, resume=False, fresh=False, state_dir=None) -> tuple[dict, int]:
    from .supervisor import supervise_native

    if sys.flags.optimize:
        raise ProtocolError("optimized_python_unsupported", "Native source assertions must remain enabled")
    config = load_project(path, state_dir)
    limits, capsule = config["limits"], config["capsule"]
    try:
        statement = native.statement(capsule)
        runtime = native.runtime_profile()
        environment = environment_snapshot()
        state = ordinary_directory(config["state_dir"])
        authority = LocalAuthority(state)
        store = LocalCAS(state / "artifacts")
        runtime_ref = store.put_bytes(native.canonical(runtime["profile"]),
                                      format_id="be.count-native/native-runtime-profile/1")
        frozen = dict(schema_version=PROTOCOL, artifact_kind="frozen_run_spec", kind=KIND,
                      statement=statement, source_epoch_digest=native.source_epoch(),
                      native_runtime_digest=runtime["digest"], native_runtime_ref=runtime_ref,
                      execution_environment=environment, authority_id=authority.authority_id,
                      limits={k: str(v) for k, v in limits.items()},
                      freshness="construct-from-source-no-historical-candidate-or-acceptance",
                      full_proof_pass=False, paid_activation=False)
        frozen_digest = digest("count-native-frozen-run-spec", frozen)
        frozen_ref = store.put_json(frozen, format_id="be.count-native/frozen-run-spec/1")
        ledger = SQLiteLedger(state / "ledger.sqlite3")
        campaign = ledger.campaign("ordinary-count-native-v1", frozen_digest, frozen_ref,
                                   resume=resume, fresh=fresh, wall_seconds=limits["campaign_wall_seconds"])
        if campaign["frozen_ref"] != frozen_ref or store.read_json(campaign["frozen_ref"]) != frozen:
            raise ProtocolError("frozen_state_mismatch", "Ledger and immutable source-replay inputs disagree")
        common = dict(schema_version=PROTOCOL, artifact_kind="native_stage_receipt",
                      campaign_id=campaign["campaign_id"], frozen_digest=frozen_digest,
                      statement_digest=native.identity("statement", statement),
                      source_epoch_digest=native.source_epoch(), native_runtime_digest=runtime["digest"],
                      trust_profile=native.TRUST, parent_acquisitions_verified=False,
                      all_law_C6_verified=False, all_index_conclusion_verified=False,
                      full_proof_pass=False, paid_activation=False)
        run_id = "run:" + str(uuid.uuid4())
        refs, cache = {}, {}
        candidate_ref = None
        for operation in ("produce", "verify"):
            spec = dict(frozen_digest=frozen_digest, operation=operation, candidate_ref=candidate_ref)
            job_id = ledger.ensure_job(campaign["campaign_id"], digest("count-native-job-spec", spec), operation)
            job = ledger.get_job(job_id)
            if job["state"] == "produced":
                ref = job["output_ref"]
                record = store.read_json(ref)
                cache[operation] = True
            else:
                fence = ledger.claim(job_id, run_id, lease_seconds=limits["lease_seconds"],
                                     maximum_attempts=limits["maximum_attempts"])
                attempt_dir = ordinary_directory(state / "attempts" / fence["attempt_id"].replace(":", "_"))
                keeper = _LeaseHeartbeat(ledger, fence, limits)

                def supervised(command, cwd, log, timeout):
                    metadata = supervise_native(command, cwd, log, timeout, heartbeat=keeper.check,
                                                campaign_deadline=campaign["deadline"],
                                                cpu_seconds=limits["cpu_seconds"], memory_bytes=limits["memory_bytes"],
                                                log_bytes=limits["log_bytes"])
                    if (metadata.get("reason") != "completed" or metadata.get("returncode") != 0
                            or metadata.get("tree_cleanup_complete") is not True):
                        raise ProtocolError("native_execution_failed", "Native execution did not complete within its resource policy")
                    return metadata

                try:
                    keeper.start()
                    if operation == "produce":
                        observation = native.construct(capsule, attempt_dir, timeout=limits["wall_seconds"], supervisor=supervised)
                        raw = native.read_regular(Path(observation["candidate"]))
                        fresh_candidate_ref = store.put_bytes(raw, format_id="be.count-native/whole-native-forest/1")
                        receipt_ref = None
                    else:
                        raw = store.read_bytes(candidate_ref)
                        input_path = attempt_dir / "candidate.json"
                        with input_path.open("xb") as stream:
                            stream.write(raw)
                        observation = native.accept(capsule, input_path, attempt_dir,
                                                    timeout=limits["wall_seconds"], supervisor=supervised)
                        if observation["outcome"] != "SCOPED_COUNT_PASS" or observation["full_proof_pass"] is not False:
                            raise ProtocolError("native_scope_mismatch", "Only conditional native COUNT acceptance is supported")
                        fresh_candidate_ref = candidate_ref
                        receipt_ref = store.put_bytes(native.read_regular(Path(observation["native_receipt"])),
                                                      format_id="be.count-native/native-receipt/1")
                    if environment_snapshot() != environment or native.runtime_profile()["digest"] != runtime["digest"]:
                        raise ProtocolError("environment_changed_during_execution", "Source or runtime changed through native execution")
                    keeper.check()
                    log_path = Path(observation["process"]["execution_directory"]) / "native.log"
                    payload = dict(common, operation=operation,
                                   status="CANDIDATE_PRODUCED" if operation == "produce" else "SCOPED_COUNT_PASS",
                                   candidate_ref=fresh_candidate_ref, census=_census(native.precheck_forest(raw, capsule)),
                                   verification_key=native.cache_key(raw, capsule, runtime["digest"]),
                                   native_receipt_ref=receipt_ref,
                                   observation_ref=store.put_bytes(native.canonical(observation),
                                                                  format_id="be.count-native/opaque-native-observation/1"),
                                   log_ref=store.put_bytes(native.read_regular(log_path), media_type="text/plain",
                                                          format_id="be.count-native/native-log/1"))
                    record = dict(payload=payload, seal=authority.sign(payload))
                    ref = store.put_json(record, format_id="be.count-native/authenticated-stage-receipt/1")
                    _authorized_stage(record, authority=authority, common=common, operation=operation,
                                      candidate_ref=candidate_ref, native_runtime_digest=runtime["digest"],
                                      capsule=capsule, store=store)
                    keeper.stop()
                    ledger.complete(fence, ref, operation_key="complete:" + fence["attempt_id"],
                                    metadata=dict(frozen_digest=frozen_digest, operation=operation,
                                                  authority_id=authority.authority_id, returncode="0"))
                    cache[operation] = False
                except BaseException as exc:
                    keeper.stop(check=False)
                    try:
                        ledger.fail(fence, getattr(exc, "code", "interrupted"))
                    except ProtocolError:
                        pass  # Expired attempts cannot modify a newer generation.
                    raise
            payload = _authorized_stage(record, authority=authority, common=common, operation=operation,
                                        candidate_ref=candidate_ref, native_runtime_digest=runtime["digest"],
                                        capsule=capsule, store=store)
            candidate_ref = payload["candidate_ref"]
            refs[operation] = ref
        report = dict(common, artifact_kind="run_report", status="SCOPED_COUNT_PASS", run_id=run_id,
                      producer_cache_hit=cache["produce"], verifier_cache_hit=cache["verify"],
                      candidate_ref=candidate_ref, producer_receipt_ref=refs["produce"], receipt_ref=refs["verify"],
                      census=payload["census"], statement=statement, authorized_local_readback=True,
                      attempts_total=str(ledger.attempt_count(campaign["campaign_id"])))
        report_ref = store.put_json(report, format_id="be.count-native/run-report/1")
        ledger.finish_campaign(campaign["campaign_id"], report_ref)
        return report, 0
    except native.CountError as exc:
        raise ProtocolError("count_" + exc.code, "Native source-replay rejected: " + exc.code) from exc
