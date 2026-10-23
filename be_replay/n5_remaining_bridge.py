"""Explicit Linux resource-only bridge for the frozen C5 small supervisors.

Copied as run_reproduction.py in each private source epoch. The original
runner remains separately sealed. Exactly four checked literal substitutions
keep ordinary inner children in the outer BASIC process group, kill only the
owned PID on inner failure, and permit three original uppercase B3 log labels.
No mathematical source, assertion, numerical limit or invocation is changed.
The Linux64MiB self-check reads this exec image's approximate VmHWM instead
of getrusage's peak retained from pre-exec address spaces. Windows is unchanged.
"""
from pathlib import Path
import hashlib
import re

ORIGINAL_RUNNER_SHA256 = "795c673a5df57ac6619b66832957cbfa83f1f31e4e3a9a7e775c3c3c52307ed0"
RESOURCE_POLICY = "LINUX_CURRENT_EXEC_VM_HWM_64MIB_V2"
EDITS = (
    (b'options = {"start_new_session": True, "preexec_fn": limits}',
     b'options = {"start_new_session": False, "preexec_fn": limits}'),
    (b'os.killpg(process.pid, signal.SIGKILL)', b'process.kill()'),
    (b're.fullmatch(r"[a-z0-9-]+", label)',
     b're.fullmatch(r"[a-z0-9-]+|owncap-B3-ext-(?:construct|replay|accept)", label)'),
    (b'import resource\n    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024',
     b'return linux_peak_from_status(Path("/proc/self/status").read_text("ascii"))'),
)


def linux_peak_from_status(text):
    """Current exec-mm RSS high water; approximate observation, not a cgroup."""
    if type(text)is not str or len(text)>256*1024 or not text.isascii():
        raise RuntimeError("Bounded ASCII current-exec Linux memory status required")
    values={}
    for name in("VmHWM","VmRSS"):
        rows=[line for line in text.splitlines()if line.startswith(name+":")]
        match=re.fullmatch(name+r":\s+([1-9][0-9]*) kB",rows[0])if len(rows)==1 else None
        if match is None:raise RuntimeError("One positive current-exec "+name+" KiB counter required")
        value=int(match.group(1))
        if value>2**53:raise RuntimeError("Bounded current-exec RSS counter required")
        values[name]=value
    if values["VmRSS"]>values["VmHWM"]:
        raise RuntimeError("Current-exec VmRSS cannot exceed VmHWM")
    return values["VmHWM"]*1024


def derive(raw):
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_RUNNER_SHA256:
        raise ValueError("Exact original supervisory resource source")
    for old, new in EDITS:
        if raw.count(old) != 1: raise ValueError("Unique checked resource-only substitution")
        raw = raw.replace(old, new, 1)
    return raw


if Path(__file__).name == "run_reproduction.py":
    if __name__ == "__main__":
        raise SystemExit("The C5 resource bridge is an imported controller, not a mathematical CLI")
    # The supplied __file__ remains this private runner's path, preserving the
    # original BASE/code/work conventions. Imported original main is dormant.
    _original = Path(__file__).with_name("ORIGINAL_RUN_REPRODUCTION.py")
    exec(compile(derive(_original.read_bytes()), str(_original), "exec"), globals())
