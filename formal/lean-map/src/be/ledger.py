"""Single-host SQLite authority for the explicitly bounded local pilot."""
from __future__ import annotations

from contextlib import closing, contextmanager
import hashlib
import os
from pathlib import Path
import secrets
import sqlite3
import time
import uuid

from .codec import canonical_bytes, digest, loads
from .errors import ProtocolError
from .store import ordinary_directory, validate_ref


def _encode(value) -> str:
    return canonical_bytes(value).decode("ascii")


def _decode(value):
    return None if value is None else loads(value.encode("ascii"), require_canonical=True)


def _token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("ascii")).hexdigest()


class SQLiteLedger:
    def __init__(self, path: Path | str, *, clock=time.time):
        self.path = Path(os.path.abspath(path))
        ordinary_directory(self.path.parent)
        if any(p.is_symlink() for p in (self.path, Path(str(self.path) + "-wal"), Path(str(self.path) + "-shm"))):
            raise ProtocolError("linked_ledger", "Ledger files must not be links")
        self.clock = clock
        with closing(self._connect()) as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS campaigns (
                  campaign_id TEXT PRIMARY KEY, project_key TEXT NOT NULL,
                  frozen_digest TEXT NOT NULL, frozen_ref TEXT NOT NULL,
                  created_at REAL NOT NULL, deadline REAL NOT NULL,
                  state TEXT NOT NULL, report_ref TEXT);
                CREATE TABLE IF NOT EXISTS project_heads (
                  project_key TEXT PRIMARY KEY, campaign_id TEXT NOT NULL REFERENCES campaigns);
                CREATE TABLE IF NOT EXISTS jobs (
                  job_id TEXT PRIMARY KEY, campaign_id TEXT NOT NULL REFERENCES campaigns,
                  job_spec_digest TEXT NOT NULL, kind TEXT NOT NULL,
                  state TEXT NOT NULL, generation INTEGER NOT NULL DEFAULT 0,
                  active_attempt TEXT, output_ref TEXT, completion_metadata TEXT,
                  UNIQUE(campaign_id,job_spec_digest,kind));
                CREATE TABLE IF NOT EXISTS attempts (
                  attempt_id TEXT PRIMARY KEY, job_id TEXT NOT NULL REFERENCES jobs,
                  generation INTEGER NOT NULL, token_digest TEXT NOT NULL,
                  origin_run_id TEXT NOT NULL, state TEXT NOT NULL,
                  lease_expires REAL NOT NULL, checkpoint_sequence INTEGER NOT NULL DEFAULT 0,
                  checkpoint_ref TEXT, failure_code TEXT, created_at REAL NOT NULL,
                  UNIQUE(job_id,generation));
                CREATE TABLE IF NOT EXISTS operations (
                  job_id TEXT NOT NULL, operation_key TEXT NOT NULL,
                  request_digest TEXT NOT NULL, response TEXT NOT NULL,
                  PRIMARY KEY(job_id,operation_key));
                CREATE TABLE IF NOT EXISTS events (
                  sequence INTEGER PRIMARY KEY AUTOINCREMENT, campaign_id TEXT NOT NULL,
                  job_id TEXT, event_kind TEXT NOT NULL, body TEXT NOT NULL);
            """)
        if os.name == "posix":
            os.chmod(self.path, 0o600)

    def _connect(self):
        connection = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA synchronous=FULL")
        connection.execute("PRAGMA busy_timeout=10000")
        return connection

    @contextmanager
    def _transaction(self):
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def _event(connection, campaign, job, kind, body):
        connection.execute("INSERT INTO events(campaign_id,job_id,event_kind,body) VALUES(?,?,?,?)",
                           (campaign, job, kind, _encode(body)))

    def campaign(self, project_key: str, frozen_digest: str, frozen_ref: dict, *,
                 resume: bool, fresh: bool = False, wall_seconds: int = 120) -> dict:
        validate_ref(frozen_ref)
        if not 1 <= wall_seconds <= 604800:
            raise ProtocolError("invalid_campaign_limit", "Finite local campaign limit required")
        with self._transaction() as connection:
            old = connection.execute("SELECT c.* FROM project_heads h JOIN campaigns c USING(campaign_id) "
                                     "WHERE h.project_key=?", (project_key,)).fetchone()
            if old is None and not fresh and connection.execute("SELECT 1 FROM project_heads LIMIT 1").fetchone():
                raise ProtocolError("incompatible_state", "State uses an older or different project head; explicit --fresh is required")
            if old is not None and not fresh:
                if old["frozen_digest"] != frozen_digest:
                    raise ProtocolError("frozen_input_changed", "Inputs, source, environment or limits changed; use an explicit fresh local campaign")
                if not resume:
                    raise ProtocolError("resume_required", "Existing campaign requires --resume or explicit --fresh")
                result = dict(old)
                result["frozen_ref"] = _decode(result["frozen_ref"])
                return result
            campaign_id = "campaign:" + str(uuid.uuid4())
            now = self.clock()
            connection.execute("INSERT INTO campaigns VALUES(?,?,?,?,?,?,?,NULL)",
                               (campaign_id, project_key, frozen_digest, _encode(frozen_ref),
                                now, now + wall_seconds, "active"))
            connection.execute("INSERT INTO project_heads VALUES(?,?) ON CONFLICT(project_key) "
                               "DO UPDATE SET campaign_id=excluded.campaign_id", (project_key, campaign_id))
            self._event(connection, campaign_id, None, "campaign_created", dict(frozen_digest=frozen_digest))
            return dict(campaign_id=campaign_id, project_key=project_key, frozen_digest=frozen_digest,
                        frozen_ref=frozen_ref, created_at=now, deadline=now + wall_seconds,
                        state="active", report_ref=None)

    def ensure_job(self, campaign_id: str, job_spec_digest: str, kind: str) -> str:
        if kind not in ("produce", "verify"):
            raise ProtocolError("unsupported_task_kind", "Only pilot producer and verifier jobs are supported")
        job_id = digest("job-instance", dict(campaign_id=campaign_id, job_spec_digest=job_spec_digest, kind=kind))
        with self._transaction() as connection:
            connection.execute("INSERT OR IGNORE INTO jobs(job_id,campaign_id,job_spec_digest,kind,state) "
                               "VALUES(?,?,?,?,?)", (job_id, campaign_id, job_spec_digest, kind, "ready"))
        return job_id

    def get_job(self, job_id: str) -> dict:
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
        if row is None:
            raise ProtocolError("job_missing", "Unknown local job")
        result = dict(row)
        for key in ("output_ref", "completion_metadata"):
            result[key] = _decode(result[key])
        return result

    def _active(self, connection, fence):
        now = self.clock()
        row = connection.execute("SELECT a.*, j.active_attempt, j.state AS job_state, j.campaign_id, "
                                 "c.state AS campaign_state,c.deadline FROM attempts a JOIN jobs j USING(job_id) "
                                 "JOIN campaigns c USING(campaign_id) WHERE a.attempt_id=?",
                                 (fence["attempt_id"],)).fetchone()
        if (row is None or row["job_id"] != fence["job_id"] or row["generation"] != fence["generation"]
                or row["active_attempt"] != fence["attempt_id"]
                or not secrets.compare_digest(row["token_digest"], _token_digest(fence["token"]))
                or row["state"] != "running" or row["job_state"] != "running"):
            raise ProtocolError("lease_superseded", "Attempt no longer owns this job")
        if row["campaign_state"] != "active" or now >= row["deadline"]:
            raise ProtocolError("campaign_closed", "Local campaign is inactive or past its immutable deadline")
        if now >= row["lease_expires"]:
            raise ProtocolError("lease_expired", "Attempt lease expired")
        return row

    def claim(self, job_id: str, origin_run_id: str, *, lease_seconds: int = 30,
              maximum_attempts: int = 3) -> dict:
        if not 1 <= lease_seconds <= 300 or not 1 <= maximum_attempts <= 10:
            raise ProtocolError("invalid_lease_policy", "Invalid bounded lease/retry policy")
        with self._transaction() as connection:
            row = connection.execute("SELECT j.*,c.state AS campaign_state,c.deadline FROM jobs j "
                                     "JOIN campaigns c USING(campaign_id) WHERE job_id=?", (job_id,)).fetchone()
            if row is None:
                raise ProtocolError("job_missing")
            now = self.clock()
            if row["state"] == "produced":
                raise ProtocolError("job_already_produced")
            if row["campaign_state"] != "active" or now >= row["deadline"]:
                raise ProtocolError("campaign_closed")
            old = connection.execute("SELECT * FROM attempts WHERE attempt_id=?", (row["active_attempt"],)).fetchone()
            if old and old["state"] == "running" and old["lease_expires"] > now:
                raise ProtocolError("job_busy", "Another live attempt owns this job")
            if row["generation"] >= maximum_attempts:
                raise ProtocolError("attempt_budget_exhausted")
            if old:
                connection.execute("UPDATE attempts SET state='lost' WHERE attempt_id=? AND state='running'", (old["attempt_id"],))
            generation = row["generation"] + 1
            attempt_id = "attempt:" + str(uuid.uuid4())
            token = secrets.token_urlsafe(32)
            expires = min(now + lease_seconds, row["deadline"])
            connection.execute("INSERT INTO attempts(attempt_id,job_id,generation,token_digest,origin_run_id,state,lease_expires,created_at) "
                               "VALUES(?,?,?,?,?,?,?,?)", (attempt_id, job_id, generation, _token_digest(token),
                                                          origin_run_id, "running", expires, now))
            connection.execute("UPDATE jobs SET state='running',generation=?,active_attempt=? WHERE job_id=?",
                               (generation, attempt_id, job_id))
            self._event(connection, row["campaign_id"], job_id, "claimed", dict(attempt_id=attempt_id, generation=str(generation)))
            return dict(job_id=job_id, attempt_id=attempt_id, generation=generation, token=token, lease_expires=expires)

    def renew(self, fence: dict, *, lease_seconds: int = 30) -> float:
        if not 1 <= lease_seconds <= 300:
            raise ProtocolError("invalid_lease_policy")
        with self._transaction() as connection:
            row = self._active(connection, fence)
            expires = min(self.clock() + lease_seconds, row["deadline"])
            connection.execute("UPDATE attempts SET lease_expires=? WHERE attempt_id=?", (expires, fence["attempt_id"]))
            return expires

    def checkpoint(self, fence: dict, sequence: int, checkpoint_ref: dict) -> None:
        validate_ref(checkpoint_ref)
        with self._transaction() as connection:
            row = self._active(connection, fence)
            if type(sequence) is not int or sequence <= row["checkpoint_sequence"]:
                raise ProtocolError("checkpoint_sequence_conflict")
            connection.execute("UPDATE attempts SET checkpoint_sequence=?,checkpoint_ref=? WHERE attempt_id=?",
                               (sequence, _encode(checkpoint_ref), fence["attempt_id"]))
            self._event(connection, row["campaign_id"], row["job_id"], "checkpointed", dict(sequence=str(sequence), artifact=checkpoint_ref))

    def complete(self, fence: dict, output_ref: dict, *, operation_key: str, metadata: dict | None = None) -> dict:
        validate_ref(output_ref)
        if not isinstance(operation_key, str) or not 1 <= len(operation_key) <= 256:
            raise ProtocolError("invalid_operation_key")
        metadata = metadata or {}
        request = dict(attempt_id=fence["attempt_id"], generation=str(fence["generation"]),
                       output_ref=output_ref, metadata=metadata)
        request_digest = digest("completion-request", request)
        with self._transaction() as connection:
            authenticated = connection.execute("SELECT * FROM attempts WHERE attempt_id=?", (fence["attempt_id"],)).fetchone()
            if (authenticated is None or authenticated["job_id"] != fence["job_id"]
                    or authenticated["generation"] != fence["generation"]
                    or not secrets.compare_digest(authenticated["token_digest"], _token_digest(fence["token"]))):
                raise ProtocolError("lease_superseded", "Completion caller does not own this fence")
            previous = connection.execute("SELECT * FROM operations WHERE job_id=? AND operation_key=?",
                                          (fence["job_id"], operation_key)).fetchone()
            if previous:
                if previous["request_digest"] != request_digest:
                    raise ProtocolError("idempotency_conflict")
                return _decode(previous["response"])
            row = self._active(connection, fence)
            response = dict(job_id=row["job_id"], attempt_id=row["attempt_id"],
                            lease_generation=str(row["generation"]), output_ref=output_ref)
            connection.execute("UPDATE attempts SET state='produced' WHERE attempt_id=?", (row["attempt_id"],))
            connection.execute("UPDATE jobs SET state='produced',output_ref=?,completion_metadata=? WHERE job_id=?",
                               (_encode(output_ref), _encode(metadata), row["job_id"]))
            connection.execute("INSERT INTO operations VALUES(?,?,?,?)",
                               (row["job_id"], operation_key, request_digest, _encode(response)))
            self._event(connection, row["campaign_id"], row["job_id"], "produced", response)
            return response

    def fail(self, fence: dict, code: str) -> None:
        with self._transaction() as connection:
            row = self._active(connection, fence)
            connection.execute("UPDATE attempts SET state='failed',failure_code=? WHERE attempt_id=?", (code, row["attempt_id"]))
            connection.execute("UPDATE jobs SET state='failed' WHERE job_id=?", (row["job_id"],))
            self._event(connection, row["campaign_id"], row["job_id"], "failed", dict(code=code))

    def finish_campaign(self, campaign_id: str, report_ref: dict) -> None:
        validate_ref(report_ref)
        with self._transaction() as connection:
            pending = connection.execute("SELECT count(*) FROM jobs WHERE campaign_id=? AND state!='produced'", (campaign_id,)).fetchone()[0]
            if pending:
                raise ProtocolError("campaign_incomplete")
            connection.execute("UPDATE campaigns SET state='completed',report_ref=? WHERE campaign_id=?", (_encode(report_ref), campaign_id))

    def attempt_count(self, campaign_id: str) -> int:
        with closing(self._connect()) as connection:
            return connection.execute("SELECT count(*) FROM attempts a JOIN jobs j USING(job_id) WHERE campaign_id=?", (campaign_id,)).fetchone()[0]


Ledger = SQLiteLedger
