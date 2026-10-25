"""Bound a reviewed native child; no shell and no mathematical acceptance.

Windows uses a private non-breakaway Job Object, assigned before first resume.
Linux execs the child in the guard's PID, with per-process CPU/address-space
rlimits and private-group cleanup. Linux limits are NOT aggregate cgroup/RSS
limits; the returned profile says so. Neither profile is a hostile-code sandbox.
"""
from __future__ import annotations

import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time
from typing import Callable

from .errors import ProtocolError


POLL_SECONDS = 0.02
HEARTBEAT_SECONDS = 0.25


class _LogDrain:
    def __init__(self, source, target, limit: int):
        self.source, self.target, self.limit = source, target, limit
        self.size = 0
        self.exceeded = threading.Event()
        self.error: BaseException | None = None
        self.thread = threading.Thread(target=self._read, name="be-native-log", daemon=True)
        self.thread.start()

    def _read(self):
        try:
            while data := self.source.read(65536):
                remaining = self.limit - self.size
                retained = data[:remaining]
                if retained:
                    self.target.write(retained)
                    self.size += len(retained)
                if len(data) > remaining:
                    self.exceeded.set()
        except BaseException as exc:
            self.error = exc

    def finish(self):
        self.thread.join(timeout=5)
        if self.thread.is_alive():
            raise ProtocolError("supervisor_cleanup_failed", "Native output pipe did not close after tree termination")
        self.source.close()
        if self.error:
            raise ProtocolError("supervisor_log_failed", "Bounded diagnostic drain failed") from self.error


class _Heartbeat:
    """One renewal in flight; a blocked database callback cannot disable wall kill."""
    def __init__(self, callback):
        self.callback = callback
        self.thread = None
        self.error = None

    def check(self):
        if self.error is not None:
            raise self.error

    def pending(self):
        return self.thread is not None and self.thread.is_alive()

    def start(self):
        self.check()
        if self.callback is None or self.pending():
            return
        def renew():
            try:
                self.callback()
            except BaseException as exc:
                self.error = exc
        self.thread = threading.Thread(target=renew, name="be-native-renew", daemon=True)
        self.thread.start()


class _LinuxProcess:
    profile = dict(name="linux-exec-rlimit-v1", cpu="per-process RLIMIT_CPU seconds; hard",
                   memory="per-process RLIMIT_AS bytes; hard; not aggregate/RSS",
                   wall="supervisor monotonic timer and campaign wall clock",
                   log="combined pipe retained bytes; hard",
                   tree="private process group and parent-death/pipe guardian; no setsid escape allowed")

    def __init__(self, command, cwd, cpu, memory, wall_end, campaign_end):
        import select
        import ctypes
        # Adopt and reap this launch's orphaned descendants. Reaping is always
        # by private process group, never wait(-1), so parallel launches do not
        # consume one another's exit statuses.
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
            raise ProtocolError("supervisor_setup_failed", "Linux subreaper is unavailable")
        self.select = select.select
        self.process = None
        self.control = self.ready = None
        control_read, self.control = os.pipe()
        self.ready, ready_write = os.pipe()
        self.ready_data = b""
        self.armed = False
        self.stats = {}
        try:
            argv = [sys.executable, str(Path(__file__).with_name("exec_guard.py")),
                    str(os.getpid()), str(cpu), str(memory), str(control_read),
                    str(ready_write), repr(wall_end), repr(campaign_end or 0), *command]
            self.process = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0,
                close_fds=True, pass_fds=(control_read, ready_write), start_new_session=True)
            self.pid, self.stdout = self.process.pid, self.process.stdout
        except BaseException:
            self.close()
            raise
        finally:
            os.close(control_read)
            os.close(ready_write)

    def poll(self):
        # WNOWAIT holds the leader's PID until group cleanup, avoiding a
        # killpg-after-reap PID reuse race in a concurrent launcher.
        value = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
        if value is None:
            return None
        return value.si_status if value.si_code == os.CLD_EXITED else -value.si_status

    def ready_now(self):
        if self.armed:
            return True
        if self.select([self.ready], [], [], 0)[0]:
            data = os.read(self.ready, 128)
            self.ready_data += data
            if b"\n" in self.ready_data:
                try:
                    prefix, guardian = self.ready_data.decode("ascii").strip().split(" ")
                    self.armed = prefix == "READY" and int(guardian) > 0
                except (ValueError, UnicodeError):
                    pass
                if not self.armed:
                    raise ProtocolError("supervisor_guard_setup_failed", "Malformed Linux limit acknowledgement")
            elif not data:
                raise ProtocolError("supervisor_guard_setup_failed", "Linux guard could not arm its limits")
        return self.armed

    def cpu_used(self):
        return None  # RLIMIT_CPU is kernel-enforced, not a global rusage delta.

    def stop_and_wait(self):
        try:
            os.killpg(self.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        until = time.monotonic() + 5
        while True:
            child, status, usage = os.wait4(self.pid, os.WNOHANG)
            if child:
                self.process.returncode = os.waitstatus_to_exitcode(status)
                self.stats = dict(cpu_seconds=usage.ru_utime + usage.ru_stime,
                                  peak_process_rss_bytes=usage.ru_maxrss * 1024)
                break
            if time.monotonic() >= until:
                raise ProtocolError("supervisor_cleanup_failed", "Native child did not terminate after SIGKILL")
            time.sleep(POLL_SECONDS)
        while True:
            try:
                adopted, _ = os.waitpid(-self.pid, os.WNOHANG)
                if adopted:
                    continue
            except ChildProcessError:
                pass
            try:
                os.killpg(self.pid, 0)
            except ProcessLookupError:
                return self.process.returncode
            if time.monotonic() >= until:
                raise ProtocolError("supervisor_cleanup_failed", "Native process group did not finish and reap")
            time.sleep(POLL_SECONDS)

    def close(self):
        for name in ("control", "ready"):
            value = getattr(self, name, None)
            if value is not None:
                os.close(value)
                setattr(self, name, None)


if os.name == "nt":
    import ctypes
    from ctypes import wintypes as W
    import msvcrt

    _K = ctypes.WinDLL("kernel32", use_last_error=True)
    _SIZE = ctypes.c_size_t

    class _BasicLimits(ctypes.Structure):
        _fields_ = [("process_time", ctypes.c_int64), ("job_time", ctypes.c_int64),
                    ("flags", W.DWORD), ("min_ws", _SIZE), ("max_ws", _SIZE),
                    ("active_limit", W.DWORD), ("affinity", _SIZE),
                    ("priority", W.DWORD), ("scheduling", W.DWORD)]

    class _IO(ctypes.Structure):
        _fields_ = [(name, ctypes.c_uint64) for name in
                    ("read_ops", "write_ops", "other_ops", "read_bytes", "write_bytes", "other_bytes")]

    class _Limits(ctypes.Structure):
        _fields_ = [("basic", _BasicLimits), ("io", _IO),
                    ("process_memory", _SIZE), ("job_memory", _SIZE),
                    ("peak_process_memory", _SIZE), ("peak_job_memory", _SIZE)]

    class _Accounting(ctypes.Structure):
        _fields_ = [(name, ctypes.c_int64) for name in
                    ("user", "kernel", "period_user", "period_kernel")]
        _fields_ += [(name, W.DWORD) for name in ("faults", "processes", "active", "terminated")]

    class _Security(ctypes.Structure):
        _fields_ = [("length", W.DWORD), ("descriptor", W.LPVOID), ("inherit", W.BOOL)]

    class _Startup(ctypes.Structure):
        _fields_ = [("cb", W.DWORD), ("reserved", W.LPWSTR), ("desktop", W.LPWSTR),
                    ("title", W.LPWSTR), ("x", W.DWORD), ("y", W.DWORD),
                    ("x_size", W.DWORD), ("y_size", W.DWORD), ("x_chars", W.DWORD),
                    ("y_chars", W.DWORD), ("fill", W.DWORD), ("flags", W.DWORD),
                    ("show", W.WORD), ("reserved_count", W.WORD), ("reserved_ptr", W.LPVOID),
                    ("stdin", W.HANDLE), ("stdout", W.HANDLE), ("stderr", W.HANDLE)]

    class _ProcessInfo(ctypes.Structure):
        _fields_ = [("process", W.HANDLE), ("thread", W.HANDLE), ("pid", W.DWORD), ("tid", W.DWORD)]

    class _StartupEx(ctypes.Structure):
        _fields_ = [("startup", _Startup), ("attributes", W.LPVOID)]

    def _api(name, result, args):
        function = getattr(_K, name)
        function.restype, function.argtypes = result, args
        return function

    _create_job = _api("CreateJobObjectW", W.HANDLE, [W.LPVOID, W.LPCWSTR])
    _set_job = _api("SetInformationJobObject", W.BOOL, [W.HANDLE, ctypes.c_int, W.LPVOID, W.DWORD])
    _query_job = _api("QueryInformationJobObject", W.BOOL, [W.HANDLE, ctypes.c_int, W.LPVOID, W.DWORD, W.LPVOID])
    _assign = _api("AssignProcessToJobObject", W.BOOL, [W.HANDLE, W.HANDLE])
    _terminate_job = _api("TerminateJobObject", W.BOOL, [W.HANDLE, W.UINT])
    _terminate_process = _api("TerminateProcess", W.BOOL, [W.HANDLE, W.UINT])
    _close = _api("CloseHandle", W.BOOL, [W.HANDLE])
    _pipe = _api("CreatePipe", W.BOOL, [ctypes.POINTER(W.HANDLE), ctypes.POINTER(W.HANDLE), ctypes.POINTER(_Security), W.DWORD])
    _handle_info = _api("SetHandleInformation", W.BOOL, [W.HANDLE, W.DWORD, W.DWORD])
    _create_file = _api("CreateFileW", W.HANDLE, [W.LPCWSTR, W.DWORD, W.DWORD, ctypes.POINTER(_Security), W.DWORD, W.DWORD, W.HANDLE])
    _create_process = _api("CreateProcessW", W.BOOL, [W.LPCWSTR, W.LPWSTR, W.LPVOID, W.LPVOID, W.BOOL,
                          W.DWORD, W.LPVOID, W.LPCWSTR, ctypes.POINTER(_Startup), ctypes.POINTER(_ProcessInfo)])
    _resume = _api("ResumeThread", W.DWORD, [W.HANDLE])
    _wait = _api("WaitForSingleObject", W.DWORD, [W.HANDLE, W.DWORD])
    _exit_code = _api("GetExitCodeProcess", W.BOOL, [W.HANDLE, ctypes.POINTER(W.DWORD)])
    _init_attributes = _api("InitializeProcThreadAttributeList", W.BOOL, [W.LPVOID, W.DWORD, W.DWORD, ctypes.POINTER(_SIZE)])
    _update_attribute = _api("UpdateProcThreadAttribute", W.BOOL, [W.LPVOID, W.DWORD, _SIZE, W.LPVOID, _SIZE, W.LPVOID, W.LPVOID])
    _delete_attributes = _api("DeleteProcThreadAttributeList", None, [W.LPVOID])

    def _wincheck(ok, stage):
        if not ok:
            raise ProtocolError("supervisor_setup_failed", stage + ": " + str(ctypes.WinError(ctypes.get_last_error())))

    class _WindowsProcess:
        profile = dict(name="windows-private-job-v1", cpu="job user CPU seconds hard; user+kernel monitored",
                       memory="aggregate job committed bytes hard; not RSS",
                       wall="supervisor monotonic timer and campaign wall clock",
                       log="combined pipe retained bytes; hard",
                       tree="private non-breakaway JobObject; KILL_ON_JOB_CLOSE")

        def __init__(self, command, cwd, cpu, memory, wall_end, campaign_end):
            self.job = self.handle = None
            self.stdout = None
            self.stats = {}
            reader = writer = null = thread = attributes = None
            attributes_ready = False
            assigned = False
            try:
                self.job = _create_job(None, None)
                _wincheck(self.job, "CreateJobObject")
                limits = _Limits()
                # JOB_TIME | PROCESS_MEMORY | JOB_MEMORY | KILL_ON_JOB_CLOSE.
                # No BREAKAWAY or SILENT_BREAKAWAY flags are enabled.
                limits.basic.flags = 0x4 | 0x100 | 0x200 | 0x2000
                limits.basic.job_time = cpu * 10_000_000
                limits.job_memory = limits.process_memory = memory
                _wincheck(_set_job(self.job, 9, ctypes.byref(limits), ctypes.sizeof(limits)), "SetInformationJobObject")
                actual = _Limits()
                _wincheck(_query_job(self.job, 9, ctypes.byref(actual), ctypes.sizeof(actual), None), "Read back job limits")
                _wincheck(actual.basic.flags & limits.basic.flags == limits.basic.flags and
                          actual.basic.job_time == limits.basic.job_time and
                          actual.job_memory == memory and actual.process_memory == memory,
                          "Job limit readback mismatch")
                security = _Security(ctypes.sizeof(_Security), None, True)
                read_handle, write_handle = W.HANDLE(), W.HANDLE()
                _wincheck(_pipe(ctypes.byref(read_handle), ctypes.byref(write_handle), ctypes.byref(security), 65536), "CreatePipe")
                reader, writer = read_handle.value, write_handle.value
                _wincheck(_handle_info(reader, 1, 0), "SetHandleInformation")
                null = _create_file("NUL", 0x80000000, 3, ctypes.byref(security), 3, 0, None)
                _wincheck(null != ctypes.c_void_p(-1).value, "Open NUL")
                startup = _StartupEx()
                startup.startup.cb, startup.startup.flags = ctypes.sizeof(startup), 0x100
                startup.startup.stdin, startup.startup.stdout, startup.startup.stderr = null, writer, writer
                size = _SIZE()
                _init_attributes(None, 2, 0, ctypes.byref(size))
                _wincheck(size.value > 0, "Size handle-list attributes")
                storage = ctypes.create_string_buffer(size.value)
                attributes = ctypes.cast(storage, W.LPVOID)
                _wincheck(_init_attributes(attributes, 2, 0, ctypes.byref(size)), "Initialize launch attributes")
                attributes_ready = True
                handles = (W.HANDLE * 2)(null, writer)
                _wincheck(_update_attribute(attributes, 0, 0x20002, ctypes.byref(handles),
                          ctypes.sizeof(handles), None, None), "Set explicit inherited handle list")
                jobs = (W.HANDLE * 1)(self.job)
                # Win10+: job assignment belongs to process creation itself;
                # a hard supervisor kill cannot leave a suspended unowned child.
                _wincheck(_update_attribute(attributes, 0, 0x2000D, ctypes.byref(jobs),
                          ctypes.sizeof(jobs), None, None), "Set atomic job assignment")
                startup.attributes = attributes
                info = _ProcessInfo()
                argv = ctypes.create_unicode_buffer(subprocess.list2cmdline(command))
                # CREATE_SUSPENDED | CREATE_NO_WINDOW: assign before any source runs.
                _wincheck(_create_process(command[0], argv, None, None, True, 0x4 | 0x08000000 | 0x80000,
                          None, str(cwd), ctypes.cast(ctypes.byref(startup), ctypes.POINTER(_Startup)),
                          ctypes.byref(info)), "CreateProcess suspended")
                self.handle, thread, self.pid = info.process, info.thread, info.pid
                assigned = True
                if campaign_end is not None and time.time() >= campaign_end:
                    raise ProtocolError("campaign_closed", "Campaign closed during native process setup")
                if time.monotonic() >= wall_end:
                    raise ProtocolError("supervisor_launch_timeout")
                _wincheck(_resume(thread) != 0xFFFFFFFF, "ResumeThread")
                fd = msvcrt.open_osfhandle(reader, os.O_RDONLY | os.O_BINARY)
                reader = None  # The file now owns this handle.
                self.stdout = os.fdopen(fd, "rb", buffering=0)
            except BaseException:
                if self.handle:
                    if assigned:
                        _terminate_job(self.job, 125)
                    else:
                        _terminate_process(self.handle, 125)
                    _wait(self.handle, 5000)
                self.close()
                raise
            finally:
                if attributes_ready:
                    _delete_attributes(attributes)
                for value in (reader, writer, null, thread):
                    if value and value != ctypes.c_void_p(-1).value:
                        _close(value)

        def ready_now(self):
            return True

        def poll(self):
            state = _wait(self.handle, 0)
            if state == 0x102:
                return None
            _wincheck(state == 0, "WaitForSingleObject")
            code = W.DWORD()
            _wincheck(_exit_code(self.handle, ctypes.byref(code)), "GetExitCodeProcess")
            return ctypes.c_int32(code.value).value

        def _account(self):
            account = _Accounting()
            _wincheck(_query_job(self.job, 1, ctypes.byref(account), ctypes.sizeof(account), None), "Query job accounting")
            return account

        def cpu_used(self):
            account = self._account()
            return (account.user + account.kernel) / 10_000_000

        def stop_and_wait(self):
            _wincheck(_terminate_job(self.job, 125), "TerminateJobObject")
            _wincheck(_wait(self.handle, 5000) == 0, "Wait after job termination")
            until = time.monotonic() + 5
            while True:
                account = self._account()
                if account.active == 0:
                    break
                if time.monotonic() >= until:
                    raise ProtocolError("supervisor_cleanup_failed", "Job retains active processes after termination")
                time.sleep(POLL_SECONDS)
            limits = _Limits()
            _wincheck(_query_job(self.job, 9, ctypes.byref(limits), ctypes.sizeof(limits), None), "Query job memory")
            self.stats = dict(cpu_seconds=(account.user + account.kernel) / 10_000_000,
                              windows_reported_peak_job_bytes=limits.peak_job_memory,
                              peak_process_committed_bytes=limits.peak_process_memory,
                              active_processes_after_cleanup=account.active)
            return self.poll()

        def close(self):
            for name in ("job", "handle"):
                value = getattr(self, name, None)
                if value:
                    _close(value)
                    setattr(self, name, None)


def supervise_native(command: list[str], cwd: Path, log: Path, timeout: int, *,
                     heartbeat: Callable[[], None] | None = None,
                     campaign_deadline: float | None = None,
                     cpu_seconds: int = 300, memory_bytes: int = 536870912,
                     log_bytes: int = 1048576) -> dict:
    """Execute one reviewed command; always kill/wait its owned tree before return.

    campaign_deadline is an absolute Unix wall-clock timestamp. Callback errors
    (including lease rejection and cancellation) are re-raised after cleanup.
    Initial authorization is synchronous, before launch. Periodic callbacks
    run serially on a daemon thread so blocked renewal cannot defeat wall kill.
    A pending callback may finish after cancellation; the ledger must fence it.
    Runtime limit exits return a non-success reason and returncode; callers must
    check both and then validate native proof outputs independently.
    """
    if (type(command) is not list or not command or
            any(type(part) is not str or not part or "\0" in part for part in command)):
        raise ProtocolError("invalid_native_command", "Expected a nonempty argv list without shell interpretation")
    if not Path(command[0]).is_absolute() or not Path(command[0]).is_file():
        raise ProtocolError("invalid_native_command", "Native executable must be an existing absolute path")
    if any(type(value) is not int or value <= 0 for value in (timeout, cpu_seconds, memory_bytes, log_bytes)):
        raise ProtocolError("invalid_supervisor_limit", "Positive integer limits required")
    if memory_bytes < 32 * 1024 * 1024:
        raise ProtocolError("invalid_supervisor_limit", "This runtime profile requires at least 32 MiB")
    if campaign_deadline is not None and (type(campaign_deadline) not in (int, float) or not math.isfinite(campaign_deadline)):
        raise ProtocolError("invalid_supervisor_deadline")
    if heartbeat is not None and not callable(heartbeat):
        raise ProtocolError("invalid_supervisor_heartbeat")
    if sys.platform != "linux" and os.name != "nt":
        raise ProtocolError("unsupported_supervisor_platform", "Only Windows Job Objects and Linux exec/rlimits are implemented")
    cwd, log = Path(cwd).absolute(), Path(log).absolute()
    if not cwd.is_dir() or cwd.is_symlink() or not log.parent.is_dir() or log.is_symlink():
        raise ProtocolError("invalid_supervisor_path", "Ordinary existing work/log directories required")
    if os.name == "nt" and (len(str(cwd)) >= 248 or len(str(log)) >= 260):
        raise ProtocolError("path_too_long", "Use a shorter native work/state directory on this Windows profile")
    if campaign_deadline is not None and time.time() >= campaign_deadline:
        raise ProtocolError("campaign_closed", "No native process may start after the campaign deadline")
    if heartbeat is not None:
        heartbeat()  # Claim/lease authorization before any source can run.
    if campaign_deadline is not None and time.time() >= campaign_deadline:
        raise ProtocolError("campaign_closed", "Campaign closed during prelaunch authorization")
    started = time.monotonic()
    process = drain = None
    reason = "completed"
    returncode = None
    renew = _Heartbeat(heartbeat)
    try:
        with log.open("xb", buffering=0) as output:
            try:
                process = (_WindowsProcess(command, cwd, cpu_seconds, memory_bytes, started + timeout,
                                           campaign_deadline) if os.name == "nt" else
                           _LinuxProcess(command, cwd, cpu_seconds, memory_bytes, started + timeout,
                                         campaign_deadline))
                drain = _LogDrain(process.stdout, output, log_bytes)
                next_heartbeat = started + HEARTBEAT_SECONDS
                while True:
                    now = time.monotonic()
                    if campaign_deadline is not None and time.time() >= campaign_deadline:
                        reason = "campaign_deadline"
                        break
                    if now - started >= timeout:
                        reason = "wall_timeout"
                        break
                    if drain.exceeded.is_set():
                        reason = "log_limit"
                        break
                    if drain.error:
                        raise ProtocolError("supervisor_log_failed") from drain.error
                    renew.check()
                    ready = process.ready_now()
                    if not ready and now - started > 5:
                        raise ProtocolError("supervisor_guard_setup_failed", "Linux launch guard did not acknowledge limits")
                    observed_cpu = process.cpu_used()
                    if observed_cpu is not None and observed_cpu >= cpu_seconds:
                        reason = "cpu_limit"
                        break
                    returncode = process.poll()
                    if returncode is not None:
                        if not ready:
                            raise ProtocolError("supervisor_guard_setup_failed")
                        if not renew.pending():
                            renew.check()
                            reason = "completed" if returncode == 0 else "nonzero_exit"
                            break
                    if heartbeat is not None and now >= next_heartbeat:
                        if returncode is None:
                            renew.start()
                        next_heartbeat = time.monotonic() + HEARTBEAT_SECONDS
                    time.sleep(POLL_SECONDS)
            finally:
                # This also runs after KeyboardInterrupt, a rejected lease,
                # source failure, log I/O error and constructor-independent errors.
                try:
                    if process is not None:
                        try:
                            final_code = process.stop_and_wait()
                            if returncode is None:
                                returncode = final_code
                        finally:
                            process.close()  # KILL_ON_JOB_CLOSE is a final backstop.
                finally:
                    if drain is not None:
                        drain.finish()
    except OSError as exc:
        raise ProtocolError("supervisor_io_failed", str(exc)) from exc
    if drain.exceeded.is_set():
        reason = "log_limit"
    if reason == "nonzero_exit" and sys.platform == "linux" and returncode in (-signal.SIGKILL, -signal.SIGXCPU):
        # SIGKILL is also possible for an external kill/OOM. Do not assert a
        # specific CPU or RAM diagnosis unless accounting actually establishes it.
        reason = "resource_or_signal_exit"
    return dict(returncode=int(returncode), reason=reason, pid=process.pid,
                duration_seconds=round(time.monotonic() - started, 6),
                log_bytes=drain.size, enforcement=dict(process.profile),
                resource_usage=process.stats, tree_cleanup_complete=True)
