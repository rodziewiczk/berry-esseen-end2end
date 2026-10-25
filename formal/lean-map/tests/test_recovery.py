"""Real CLI process interruption and frozen-input recovery controls."""
from __future__ import annotations

from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

from be.codec import canonical_bytes, load_json

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/local-pilot"


class CLIRecoveryTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / ".test_tmp"
        parent.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.state = self.folder / "state"
        self.problem = self.folder / "problem.json"
        self.problem.write_bytes((EXAMPLE / "problem.json").read_bytes())
        self.project = self.folder / "project.toml"
        text = (EXAMPLE / "project.toml").read_text(encoding="utf-8")
        for key, path in (("problem", self.problem), ("source_manifest", EXAMPLE / "source-manifest.json"),
                          ("trust_profile", EXAMPLE / "trust-profile.json")):
            text = text.replace(f'{key} = "{path.name}"', f'{key} = "{path.as_posix()}"')
        text = text.replace('lease_seconds = "30"', 'lease_seconds = "4"')
        text = text.replace('heartbeat_seconds = "5"', 'heartbeat_seconds = "1"')
        self.project.write_text(text, encoding="utf-8", newline="\n")
        self.env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), PYTHONDONTWRITEBYTECODE="1")
        self.args = [sys.executable, "-m", "be", "run", str(self.project), "--resume", "--state-dir", str(self.state)]

    def run_cli(self):
        result = subprocess.run(self.args, cwd=self.folder, env=self.env, capture_output=True, timeout=60)
        return result.returncode, json.loads(result.stdout)

    def test_process_kill_retains_producer_and_fences_expired_verifier(self):
        process = subprocess.Popen(self.args, cwd=self.folder, env=self.env,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            deadline = time.monotonic() + 40
            interrupted = False
            while time.monotonic() < deadline and process.poll() is None:
                db = self.state / "ledger.sqlite3"
                if db.exists():
                    try:
                        with closing(sqlite3.connect(db, timeout=0.2)) as connection:
                            states = dict(connection.execute("SELECT kind,state FROM jobs"))
                        if states.get("produce") == "produced" and states.get("verify") == "running":
                            process.kill()
                            process.communicate(timeout=10)
                            interrupted = True
                            break
                    except sqlite3.OperationalError:
                        pass  # The initialization transaction may not yet expose jobs.
                time.sleep(0.01)
            self.assertTrue(interrupted, "Did not observe the durable producer / live verifier boundary")
            # The lost verifier has no coordinator to commit. Its lease and tiny
            # bounded worker expire before a replacement is permitted to claim.
            time.sleep(4.5)
            code, report = self.run_cli()
            self.assertEqual(code, 0, report)
            self.assertEqual(report["status"], "PILOT_PASS")
            self.assertTrue(report["producer_cache_hit"])
            self.assertFalse(report["verifier_cache_hit"])
            self.assertEqual(report["attempts_total"], "3")
            self.assertFalse(report["full_proof_pass"])
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate(timeout=10)

    def test_modified_context_cannot_inherit_an_existing_campaign(self):
        code, report = self.run_cli()
        self.assertEqual(code, 0, report)
        problem = load_json(self.problem)
        problem["context"]["p"] = {"num": "1", "den": "2"}
        self.problem.write_bytes(canonical_bytes(problem))
        code, changed = self.run_cli()
        self.assertEqual(code, 3, changed)
        self.assertEqual(changed["error"]["code"], "frozen_input_changed")
        self.assertFalse(changed["full_proof_pass"])

    def test_project_locator_change_does_not_reset_campaign(self):
        code, first = self.run_cli()
        self.assertEqual(code, 0, first)
        moved = self.folder / "relocated.toml"
        moved.write_bytes(self.project.read_bytes())
        self.args[4] = str(moved)
        code, second = self.run_cli()
        self.assertEqual(code, 0, second)
        self.assertEqual(second["campaign_id"], first["campaign_id"])
        self.assertEqual(second["frozen_digest"], first["frozen_digest"])
        self.assertEqual(second["attempts_total"], "2")
        self.assertTrue(second["producer_cache_hit"])
        self.assertTrue(second["verifier_cache_hit"])


if __name__ == "__main__":
    unittest.main()
