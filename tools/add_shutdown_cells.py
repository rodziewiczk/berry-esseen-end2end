"""Append/update the final Colab shutdown cell without changing earlier cells.

Run from the repository root:
    python -B tools/add_shutdown_cells.py
    python -B tools/add_shutdown_cells.py --check
Optional paths may name individual notebooks or directories, including local handoffs.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import os
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("shutdown_notebook_builder", ROOT / "tools/make_notebooks.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def update_notebook(path: Path, *, check: bool = False) -> bool:
    """Return whether a change is needed. Never execute notebook code."""
    if path.is_symlink() or not path.is_file() or path.suffix != ".ipynb":
        raise ValueError(f"Expected a regular .ipynb file: {path}")
    raw = path.read_text(encoding="utf-8")
    doc = json.loads(raw)
    if doc.get("nbformat") != 4 or not isinstance(doc.get("cells"), list):
        raise ValueError(f"Expected notebook format 4 and a cell list: {path}")
    cells = builder.with_shutdown(doc["cells"])
    if cells == doc["cells"]:
        return False
    if check:
        return True
    doc["cells"] = cells
    serialized = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    # Atomic replacement: interrupted maintenance cannot leave half a JSON file.
    fd, name = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as output:
            output.write(serialized)
            output.flush()
            os.fsync(output.fileno())
        os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, default=[ROOT / "colab"])
    parser.add_argument("--check", action="store_true", help="Do not write; fail when a notebook needs an update.")
    args = parser.parse_args()
    selected = set()
    for path in args.paths:
        if path.is_symlink():
            raise ValueError(f"Refusing a symbolic link: {path}")
        if path.is_dir():
            selected.update(path.rglob("*.ipynb"))
        elif path.is_file() and path.suffix == ".ipynb":
            selected.add(path)
        else:
            raise ValueError(f"Not a notebook or directory: {path}")
    if not selected:
        raise ValueError("No notebooks found")
    changed = 0
    for path in sorted(selected):
        if update_notebook(path, check=args.check):
            changed += 1
            print(("NEEDS UPDATE " if args.check else "UPDATED ") + str(path))
    print(f"Checked {len(selected)} notebooks; {'needing update' if args.check else 'updated'}: {changed}.")
    return int(args.check and changed > 0)


if __name__ == "__main__":
    raise SystemExit(main())
