"""Linux-only launch setup, then exec the native command without changing PID.

Invoked by supervisor.py, never a mathematical checker.  A small pipe guardian
survives the exec so abrupt supervisor death also kills ordinary descendants
in the private process group. This is for reviewed source, not hostile code.
"""
from __future__ import annotations

import ctypes
import os
import resource
import signal
import sys
import time


def main() -> None:
    # Positional private protocol: parent, CPU, address space, control FD,
    # ready FD, then the original argv. No shell or Python preexec_fn.
    parent, cpu, memory, control, ready = map(int, sys.argv[1:6])
    wall_end, campaign_end = map(float, sys.argv[6:8])
    command = sys.argv[8:]
    if not command or sys.platform != "linux" or os.getpgrp() != os.getpid():
        raise RuntimeError("Expected Linux private-session launch")
    libc = ctypes.CDLL(None, use_errno=True)
    libc.prctl.argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong,
                           ctypes.c_ulong, ctypes.c_ulong]
    libc.prctl.restype = ctypes.c_int
    if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
        raise OSError(ctypes.get_errno(), "Cannot arm parent-death signal")
    if os.getppid() != parent:
        raise RuntimeError("Supervisor exited before launch was armed")
    resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
    resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    group = os.getpgrp()
    guardian = os.fork()
    if guardian == 0:
        # Only the supervisor owns the pipe writer. Close the output/ready FDs
        # so the guardian cannot keep log drains alive after native exit.
        for name in os.listdir("/proc/self/fd"):
            fd = int(name)
            if fd != control:
                try:
                    os.close(fd)
                except OSError:
                    pass
        try:
            while os.read(control, 1):
                pass
        finally:
            try:
                os.killpg(group, signal.SIGKILL)
            finally:
                os._exit(125)
    os.close(control)
    # CLOEXEC is explicit: the native program must not inherit these ports.
    os.set_inheritable(ready, False)
    if time.monotonic() >= wall_end or (campaign_end and time.time() >= campaign_end):
        raise RuntimeError("Native execution deadline closed during launch")
    os.write(ready, ("READY " + str(guardian) + "\n").encode("ascii"))
    os.execv(command[0], command)


if __name__ == "__main__":
    try:
        main()
    except BaseException as exc:
        os.write(2, ("exec_guard setup failed: " + str(exc)[:500] + "\n").encode("utf-8", "replace"))
        os._exit(125)
