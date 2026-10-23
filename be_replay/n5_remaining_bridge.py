"""Explicit Linux resource-only bridge for the frozen C5 small supervisors.

Copied as run_reproduction.py in each private source epoch. The original
runner remains separately sealed. Exactly three checked literal substitutions
keep ordinary inner children in the outer BASIC process group, kill only the
owned PID on inner failure, and permit three original uppercase B3 log labels.
No mathematical source, assertion, numerical limit or invocation is changed.
"""
from pathlib import Path
import hashlib

ORIGINAL_RUNNER_SHA256 = "795c673a5df57ac6619b66832957cbfa83f1f31e4e3a9a7e775c3c3c52307ed0"
EDITS = (
    (b'options = {"start_new_session": True, "preexec_fn": limits}',
     b'options = {"start_new_session": False, "preexec_fn": limits}'),
    (b'os.killpg(process.pid, signal.SIGKILL)', b'process.kill()'),
    (b're.fullmatch(r"[a-z0-9-]+", label)',
     b're.fullmatch(r"[a-z0-9-]+|owncap-B3-ext-(?:construct|replay|accept)", label)'),
)


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
