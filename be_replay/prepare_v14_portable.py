"""Prepare a sealed, portable V14 source epoch without modifying the vendor.

The frozen producer writes ORIGINAL_V12_contract.json but its unchanged native
loader reads ORIGINAL_V12_CONTRACT.json. Case-insensitive filesystems hide this
producer defect. This adapter changes exactly that output destination, before
the producer builds its provenance, kernel manifest and source design.

No mathematical source, contract, native evaluator, native acceptor, guard or
finite proof is changed. The mathematical proof text retains its original
bytes. The resulting source designs are new, externally pinned epochs; old
checkpoint bindings are not valid for them. The producer's preparer_sha256
binds this complete adapter, whose source determines the one checked edit.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FROZEN_SOURCE = ROOT / "vendor/count_75a9470/prepare_b3_v14_epoch_2026_10_22.py"
FROZEN_SHA256 = "4116a054c2f725794d82cc4bd7b954023c9b8525d8f943c6cea2a8096aceb647"
OLD_DESTINATION = "add('ORIGINAL_V12_'+name, original[name], Path(old.filename).name, pre+name,"
NEW_DESTINATION = (
    "add('ORIGINAL_V12_'+('CONTRACT.json' if name == 'contract.json' else name), "
    "original[name], Path(old.filename).name, pre+name,"
)


def transformed_source(path=None):
    """Return exactly the reviewed one-destination source transform."""
    source_path = Path(path) if path is not None else FROZEN_SOURCE
    if not source_path.is_file() or source_path.is_symlink():
        raise ValueError("The frozen V14 producer must be a regular source file")
    raw = source_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != FROZEN_SHA256:
        raise ValueError("Frozen V14 producer SHA-256 mismatch")
    source = raw.decode("utf-8")
    if source.count(OLD_DESTINATION) != 1 or NEW_DESTINATION in source:
        raise ValueError("The reviewed V14 output-destination edit must occur exactly once")
    return source.replace(OLD_DESTINATION, NEW_DESTINATION, 1)


def main():
    adapter = str(Path(__file__).resolve())
    source = transformed_source()
    # Keeping __file__ at this adapter is intentional: the unchanged producer
    # hashes it into the sealed source epoch. No runtime alias is introduced.
    namespace = {"__name__": "__main__", "__file__": adapter, "__package__": None}
    exec(compile(source, adapter, "exec"), namespace)


if __name__ == "__main__":
    main()
