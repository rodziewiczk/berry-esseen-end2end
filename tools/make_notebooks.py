"""Build preconfigured Colab notebooks against an immutable code commit."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ("01_n25_b3_p33", "b3-p33"),
    ("02_n25_b4_q0", "b4-q0"),
    ("03_n25_b4_q1", "b4-q1"),
    ("04_n25_b4_q2", "b4-q2"),
    ("05_n25_b4_q3", "b4-q3"),
    ("06_n25_b3_p31_v14", "b3-p31-v14-new"),
    ("07_n25_b3_p32_v14", "b3-p32-v14-new"),
]

def cell(kind, text, label):
    row = {"cell_type": kind, "id":label, "metadata":{"id":label}, "source":text.splitlines(keepends=True)}
    if kind == "code":
        row.update(execution_count=None, outputs=[])
    return row

def common(pin, task):
    code = f'''from pathlib import Path
import subprocess, sys, json, os, time
sys.dont_write_bytecode = True
CODE_COMMIT = "{pin}"
TASK = "{task}"
REPOSITORY = "https://github.com/rodziewiczk/berry-esseen-end2end.git"
CODE = Path("/content") / ("berry-esseen-code-" + CODE_COMMIT[:12])
print("Fetching the pinned source commit:", CODE_COMMIT, flush=True)
if not CODE.exists():
    subprocess.run(["git", "clone", "--quiet", "--no-checkout", REPOSITORY, str(CODE)], check=True)
    subprocess.run(["git", "-C", str(CODE), "checkout", "--quiet", "--detach", CODE_COMMIT], check=True)
observed = subprocess.check_output(["git", "-C", str(CODE), "rev-parse", "HEAD"], text=True).strip()
if observed != CODE_COMMIT:
    raise RuntimeError("Source commit mismatch")
subprocess.run(["git", "-C", str(CODE), "diff", "--exit-code", "HEAD", "--"], check=True)
(CODE / "work").mkdir(exist_ok=True)
# A rerun in an existing Colab kernel must not reuse modules from an older pin.
for module_name in tuple(sys.modules):
    if module_name == "be_replay" or module_name.startswith("be_replay."):
        del sys.modules[module_name]
sys.path.insert(0, str(CODE))
from be_replay.environment import snapshot
if not Path(sys.modules["be_replay"].__file__).resolve().is_relative_to(CODE.resolve()):
    raise RuntimeError("Imported execution code does not belong to the pinned checkout")
print(json.dumps(snapshot(), indent=2), flush=True)
print("Source code and environment recorded. Mathematical acceptance has not yet been established.", flush=True)
'''
    drive = '''from google.colab import drive
drive.mount("/content/drive")
BERRY_ESSEEN_DRIVE_MOUNTED = True
DURABLE = Path("/content/drive/MyDrive/Berry-Esseen-end2end")
DURABLE.mkdir(parents=True, exist_ok=True)
print("Logs and checkpoints:", DURABLE, flush=True)
'''
    tests = '''from datetime import datetime, timezone
SELFTEST = DURABLE / ("selftest-" + TASK + "-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".log")
print("Testing the supervisor on the actual Linux runtime. These lightweight fixtures do not verify the mathematics.", flush=True)
with SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_linux_supervisor.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Supervisor self-tests failed; computation will not start. Log: " + str(SELFTEST))
print("Supervisor self-tests passed. Starting the selected calculation.", flush=True)
'''
    return [
        cell("code", code, "pinned-code"),
        cell("code", drive, "durable-drive"),
        cell("code", tests, "actual-linux-guard-tests"),
    ]

def finish():
    return cell("code", '''from IPython.display import display, FileLink
from google.colab import files
print("Execution status:", RESULT["status"]["state"], flush=True)
print("The global proof remains unverified.", flush=True)
packet = RESULT["bundle"]
bundle_path = packet["path"] if isinstance(packet, dict) else packet
print("Results ZIP on Google Drive:", bundle_path, flush=True)
display(FileLink(bundle_path))
try:
    files.download(bundle_path)
except Exception as error:
    print("Download the ZIP from the Google Drive path shown above:", error, flush=True)
''', "download-result")

def shutdown():
    """Return a self-contained final cell; no change to the pinned runtime code."""
    return cell("code", '''# FINAL CELL: flush saved Drive results and release the Colab runtime.
# Runs after the final results ZIP is saved, including WAITING/INCOMPLETE.
# Do not run this cell manually while calculations or result writes are active.
# A synchronization error stops this cell BEFORE the runtime is released.
import os as _shutdown_os
import sys as _shutdown_sys

_managed_colab = (globals().get("BERRY_ESSEEN_DRIVE_MOUNTED") is True
                  or bool(_shutdown_os.environ.get("TBE_RUNTIME_ADDR")))
if not _managed_colab:
    print("Outside a managed Colab runtime; skipping shutdown.", flush=True)
else:
    from google.colab import drive as _shutdown_drive
    from google.colab import runtime as _shutdown_runtime

    print("Flushing saved results to Google Drive...", flush=True)
    _shutdown_sys.stdout.flush()
    _shutdown_sys.stderr.flush()
    _shutdown_os.sync()
    _shutdown_drive.flush_and_unmount(timeout_ms=300_000)
    print("Drive synchronization finished. Releasing the Colab runtime.", flush=True)
    _shutdown_runtime.unassign()
''', "shutdown-runtime")


def with_shutdown(cells):
    """Keep one canonical shutdown cell at the end, without mutating input cells."""
    return [c for c in cells if c.get("id") != "shutdown-runtime"] + [shutdown()]


def notebook(cells, title):
    return {"nbformat":4, "nbformat_minor":5,
            "metadata":{"colab":{"name":title,"provenance":[]},
                        "kernelspec":{"name":"python3","display_name":"Python 3"},
                        "language_info":{"name":"python"}},
            "cells":with_shutdown(cells)}

def make_count(pin, stem, target):
    intro = f'''# Berry–Esseen: {target} — CPU computation, logs and checkpoints

Select **Runtime → Run all**. This notebook is preconfigured for the selected task.
Google may request Drive authorization so that checkpoints survive a disconnected session.
Keep the code unchanged and do not run concurrent copies of the same task.

A short benchmark precedes up to 3 hours of allocated search, divided into bounded slices.
Each slice has an external wall-clock limit. A complete candidate forest is submitted to a separate native checker.
Progress is displayed in the cell and recorded in files. Partial results retain both checkpoint copies.
This notebook concerns one conditional n25 count forest; it does not establish the all-index theorem.
'''
    if target.endswith("-v14-new"):
        intro += "\nThis version fixes the Linux contract filename and pins a new sealed source epoch.\n"
        intro += "Old published V14 checkpoints are incompatible; discovery starts from all 26 original roots.\n"
        intro += "Later runs can resume checkpoints created with this corrected source epoch.\n"
    cells = [cell("markdown", intro, "instructions"), *common(pin, target)]
    cells.append(cell("code", f'''from be_replay.colab_batch import run_count
RESULT = run_count("{target}", durable_root=DURABLE,
                   total_seconds=10800, slice_seconds=1800, backup_interval=60)
''', "execute-task"))
    cells.append(finish())
    return notebook(cells, stem+".ipynb")

def make_small(pin):
    title = "08_n2_n3_cpu"
    cells = [cell("markdown", """# Berry–Esseen: n2 and n3 — complete finite CPU calculations

Select **Run all**. This notebook verifies the complete supplied n2 and n3 finite certificates,
compiles the C++ kernel from source and records progress.
The original Windows resource contract and the Linux execution contract are reported separately.
This calculation does not establish C4 or the all-index theorem.
""", "instructions"), *common(pin, "n2-n3")]
    cells.append(cell("code", '''import shutil
if shutil.which("g++") is None or not Path("/usr/include/boost/multiprecision/cpp_int.hpp").exists():
    print("Installing the compiler and Boost headers from Colab's system package repositories.", flush=True)
    subprocess.run(["apt-get", "update", "-qq"], check=True)
    subprocess.run(["apt-get", "install", "-y", "-qq", "g++", "libboost-dev"], check=True)
print("Compiler:", subprocess.check_output(["g++", "--version"], text=True).splitlines()[0], flush=True)
from be_replay.small_indices import run_colab
RESULT = run_colab(durable_root=DURABLE)
''', "execute-small"))
    cells.append(finish())
    return notebook(cells, title+".ipynb")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, default=ROOT/"colab")
    args = parser.parse_args()
    if not re.fullmatch("[0-9a-f]{40}", args.code_commit):
        raise ValueError("Immutable full Git commit required")
    args.output.mkdir(parents=True, exist_ok=True)
    docs = [(stem, make_count(args.code_commit, stem, target)) for stem,target in TARGETS]
    docs.append(("08_n2_n3_cpu", make_small(args.code_commit)))
    for stem, doc in docs:
        for item in doc["cells"]:
            if item["cell_type"] == "code":
                compile("".join(item["source"]), stem, "exec")
        path = args.output/(stem+".ipynb")
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(path)
    # The repository landing page links this preconfigured first task.
    (args.output/"count_cpu.ipynb").write_text(
        json.dumps(docs[0][1], ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
