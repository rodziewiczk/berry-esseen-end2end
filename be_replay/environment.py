"""Read the actual execution environment without running a mathematical task."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import sys

def read(path):
    try:
        return Path(path).read_text(encoding="utf-8").strip()
    except OSError:
        return None

def snapshot():
    mem = {}
    for line in (read("/proc/meminfo") or "").splitlines():
        key, _, val = line.partition(":")
        if key in ("MemTotal", "MemAvailable"):
            mem[key + "_bytes"] = int(val.split()[0]) * 1024
    return {
        "scope": "ENVIRONMENT_MEASUREMENT_ONLY",
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "logical_cpu_count": os.cpu_count(),
        "allowed_cpu_count": len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None,
        "cpu_max": read("/sys/fs/cgroup/cpu.max"),
        "memory_max": read("/sys/fs/cgroup/memory.max"),
        "memory": mem,
        "mathematical_acceptance": False,
        "all_index_conclusion_verified": False,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = snapshot()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as out:
            json.dump(result, out, indent=2)
            out.write("\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
