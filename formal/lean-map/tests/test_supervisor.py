"""Real process/resource/cancellation tests; no fake proof verdicts."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

from be.errors import ProtocolError
from be.supervisor import supervise_native


SUPPORTED = os.name == "nt" or sys.platform == "linux"


def active(pid):
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel.WaitForSingleObject.restype = wintypes.DWORD
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x100000, False, pid)
        if not handle:
            if ctypes.get_last_error() == 87:  # Already reaped / invalid PID.
                return False
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            return kernel.WaitForSingleObject(handle, 0) == 0x102
        finally:
            kernel.CloseHandle(handle)
    try:
        # Zombies do not execute. Normal supervisor cleanup also reaps its
        # adopted group; after a killed parent, init owns the remaining wait.
        return Path(f"/proc/{pid}/stat").read_text().split(") ", 1)[1][0] != "Z"
    except FileNotFoundError:
        return False


@unittest.skipUnless(SUPPORTED, "No truthful native enforcement profile for this OS")
class SupervisorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_child(self, source, name="child", **kwargs):
        directory = self.root / name
        directory.mkdir()
        return supervise_native([sys.executable, "-c", source], directory,
                                directory / "combined.log", kwargs.pop("timeout", 8), **kwargs)

    def wait_gone(self, pids):
        until = time.monotonic() + 5
        while any(active(pid) for pid in pids) and time.monotonic() < until:
            time.sleep(0.02)
        self.assertFalse(any(active(pid) for pid in pids), "Owned process survived cleanup")

    def tree_source(self):
        return ("import os,sys,json,subprocess,time;from pathlib import Path;"
                "child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(120)']);"
                "Path('pids.json').write_text(json.dumps([os.getpid(),child.pid]));"
                "time.sleep(120)")

    def test_combined_log_and_normal_exit(self):
        result = self.run_child("import sys;print('out',flush=True);print('err',file=sys.stderr,flush=True)")
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["reason"], "completed")
        self.assertTrue(result["tree_cleanup_complete"])
        self.assertIn(b"out", (self.root / "child/combined.log").read_bytes())
        self.assertIn(b"err", (self.root / "child/combined.log").read_bytes())
        self.assertIs(type(result["returncode"]), int)

    def test_nonzero_is_not_success_or_a_cpu_diagnosis(self):
        result = self.run_child("raise SystemExit(17)")
        self.assertEqual(result["returncode"], 17)
        self.assertEqual(result["reason"], "nonzero_exit")

    def test_timeout_terminates_parent_and_grandchild(self):
        result = self.run_child(self.tree_source(), timeout=1)
        self.assertEqual(result["reason"], "wall_timeout")
        self.assertNotEqual(result["returncode"], 0)
        self.wait_gone(json.loads((self.root / "child/pids.json").read_text()))

    def test_heartbeat_renews_and_cancellation_kills_tree(self):
        calls = []
        class Cancelled(Exception):
            pass
        def beat():
            calls.append(time.monotonic())
            if len(calls) == 3:
                raise Cancelled("lease revoked")
        with self.assertRaisesRegex(Cancelled, "lease revoked"):
            self.run_child(self.tree_source(), heartbeat=beat)
        self.assertEqual(len(calls), 3)
        self.wait_gone(json.loads((self.root / "child/pids.json").read_text()))

    def test_deadline_is_absolute_and_closed_campaign_never_starts(self):
        result = self.run_child("import time;time.sleep(30)", campaign_deadline=time.time() + 0.4)
        self.assertEqual(result["reason"], "campaign_deadline")
        directory = self.root / "late"
        directory.mkdir()
        with self.assertRaises(ProtocolError) as caught:
            supervise_native([sys.executable, "-c", "print('must not run')"], directory,
                             directory / "combined.log", 5, campaign_deadline=time.time() - 1)
        self.assertEqual(caught.exception.code, "campaign_closed")
        self.assertFalse((directory / "combined.log").exists())

    def test_log_is_hard_capped_even_for_unlimited_output(self):
        result = self.run_child("import os\nwhile True: os.write(1,b'x'*65536)", log_bytes=1024)
        self.assertEqual(result["reason"], "log_limit")
        self.assertEqual(result["log_bytes"], 1024)
        self.assertEqual((self.root / "child/combined.log").stat().st_size, 1024)

    def test_cpu_limit_precedes_long_wall_limit(self):
        result = self.run_child("while True: pass", cpu_seconds=1, timeout=15)
        self.assertNotEqual(result["returncode"], 0)
        self.assertNotEqual(result["reason"], "wall_timeout")
        self.assertLess(result["duration_seconds"], 10)
        self.assertGreaterEqual(result["resource_usage"]["cpu_seconds"], 0.8)

    def test_memory_allocation_above_limit_is_refused(self):
        result = self.run_child("x=bytearray(512*1024*1024);print('unbounded allocation succeeded')",
                                memory_bytes=64 * 1024 * 1024)
        self.assertNotEqual(result["returncode"], 0)
        self.assertNotIn(b"unbounded allocation succeeded", (self.root / "child/combined.log").read_bytes())

    @unittest.skipUnless(os.name == "nt", "Windows aggregate committed-memory contract")
    def test_windows_memory_limit_covers_all_descendants(self):
        source = ("import subprocess,sys;"
                  "code='import time;x=bytearray(40*1024*1024);time.sleep(0.5)';"
                  "children=[subprocess.Popen([sys.executable,'-c',code]) for _ in range(2)];"
                  "codes=[p.wait() for p in children];sys.exit(21 if any(codes) else 0)")
        result = self.run_child(source, memory_bytes=64 * 1024 * 1024)
        self.assertNotEqual(result["returncode"], 0)
        self.assertEqual(result["returncode"], 21)
        self.assertIn(b"MemoryError", (self.root / "child/combined.log").read_bytes())
        # Each individual allocation is below the per-process limit. Refusing
        # their overlap therefore tests aggregate Job memory. Windows' reported
        # peak can include the rejected large request; it is not successful
        # allocated bytes and is deliberately not a <=limit acceptance test.

    def test_blocked_periodic_heartbeat_cannot_disable_timeout(self):
        calls = []
        def beat():
            calls.append(True)
            if len(calls) > 1:
                time.sleep(3)
        result = self.run_child("import time;time.sleep(30)", timeout=1, heartbeat=beat)
        self.assertEqual(result["reason"], "wall_timeout")
        self.assertLess(result["duration_seconds"], 2.5)

    def test_parallel_launches_work_with_threads_without_preexec(self):
        def operation(index):
            return self.run_child("import time;print('parallel');time.sleep(.2)", name=str(index))
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(operation, range(8)))
        self.assertEqual([r["returncode"] for r in results], [0] * 8)
        self.assertTrue(all(r["tree_cleanup_complete"] for r in results))

    def test_abrupt_supervisor_death_kills_owned_tree(self):
        directory = self.root / "hard-death"
        directory.mkdir()
        source = ("import sys;from pathlib import Path;from be.supervisor import supervise_native;"
                  "d=Path(sys.argv[1]);supervise_native([sys.executable,'-c',sys.argv[2]],"
                  "d,d/'combined.log',90)")
        kwargs = dict(creationflags=subprocess.CREATE_NO_WINDOW) if os.name == "nt" else {}
        controller = subprocess.Popen([sys.executable, "-c", source, str(directory), self.tree_source()],
                                      stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL, **kwargs)
        try:
            until = time.monotonic() + 8
            pids = directory / "pids.json"
            while not pids.exists() and time.monotonic() < until and controller.poll() is None:
                time.sleep(0.02)
            self.assertTrue(pids.exists(), "Native child did not reach the real process-tree fixture")
            owned = json.loads(pids.read_text())
            self.assertTrue(all(active(pid) for pid in owned))
            controller.kill()  # No Python finally/atexit runs in the supervisor.
            controller.wait(timeout=5)
            self.wait_gone(owned)
        finally:
            if controller.poll() is None:
                controller.kill()
                controller.wait(timeout=5)

    def test_log_publication_is_create_only(self):
        directory = self.root / "existing"
        directory.mkdir()
        log = directory / "combined.log"
        log.write_bytes(b"preserved")
        with self.assertRaises(ProtocolError) as caught:
            supervise_native([sys.executable, "-c", "print('replacement')"], directory, log, 3)
        self.assertEqual(caught.exception.code, "supervisor_io_failed")
        self.assertEqual(log.read_bytes(), b"preserved")


if __name__ == "__main__":
    unittest.main()
