"""Source-only B4 q2 resource epoch; no mathematical code is imported.

The only changed original source bytes are LIMIT=10000 -> LIMIT=100000.
This is a new bounded certificate profile, never original-profile acceptance.
"""
from __future__ import annotations

import ast
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from . import count_task as original

TARGET = "b4-q2"
ORIGINAL_DESIGN_SHA256 = "2517c1b8c79949bad93eecdcaa43e389344411fd4c71d5d516dde1e40b732e2a"
ORIGINAL_CHECKER_SHA256 = "5cd4f1a59ba1dbd10ae0455cde3731e03b236b0e1572dda78734dce5142e7f96"
NODE_LIMIT = 100000
ORIGINAL_NODE_LIMIT = 10000
SCOPE = "RESOURCE_EXTENDED_V12_COUNT_ONLY"
NEW_DESIGN_SHA256 = "866eec6360d31f80931ddd9edfb87c4218caa23c8f06346ba8362f093b110e6a"
DESIGN_SHA256 = NEW_DESIGN_SHA256
CHECKER_SHA256 = "f535bae9054163b57206e2bdffe2afae96b5c0bfb28b3efa4533c88d037ca376"
CONTRACT_SHA256 = "0576748a8e4deb2450fea8fc7b1b06898dd8bd3ae2d5fc3465163a123d9425c3"
EPOCH = "COUNT_LIMIT_EPOCH.json"
ORIGINAL_DESIGN = "ORIGINAL_FROZEN_DESIGN.json"
ORIGINAL_CHECKER = "ORIGINAL_COUNT_PROTOCOL.py"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True,
                       allow_nan=False) + "\n").encode("ascii")


def _patch(raw):
    """Check the full AST and replace exactly one top-level literal assignment."""
    tree = ast.parse(raw)
    assignments = [n for n in tree.body if isinstance(n, ast.Assign)
                   and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
                   and n.targets[0].id == "LIMIT"]
    need(len(assignments) == 1, "Exactly one top-level LIMIT assignment")
    node = assignments[0]
    need(isinstance(node.value, ast.Constant) and type(node.value.value) is int
         and node.value.value == ORIGINAL_NODE_LIMIT and node.lineno == node.end_lineno,
         "Original literal LIMIT=10000")
    lines = raw.splitlines(keepends=True)
    start = sum(map(len, lines[:node.lineno-1])) + node.col_offset
    end = sum(map(len, lines[:node.end_lineno-1])) + node.end_col_offset
    need(raw[start:end] == b"LIMIT=10000", "Exact checked original assignment bytes")
    # In the pinned original these are the construction and replay resource guards.
    uses = [n for n in ast.walk(tree) if isinstance(n, ast.Name)
            and n.id == "LIMIT" and isinstance(n.ctx, ast.Load)]
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    need(len(uses) == 2, "Only the two original resource-limit uses")
    for use in uses:
        compare = parents.get(use)
        need(isinstance(compare, ast.Compare) and len(compare.ops) == 1
             and isinstance(compare.ops[0], ast.LtE) and compare.comparators == [use]
             and isinstance(compare.left, ast.Name) and compare.left.id == "visited",
             "LIMIT occurs only in visited<=LIMIT resource guards")
    result = raw[:start] + b"LIMIT=100000" + raw[end:]
    changed = ast.parse(result)
    comparison = deepcopy(tree)
    next(n for n in comparison.body if isinstance(n, ast.Assign)
         and any(isinstance(t, ast.Name) and t.id == "LIMIT" for t in n.targets)).value.value = NODE_LIMIT
    need(ast.dump(changed, include_attributes=False) == ast.dump(comparison, include_attributes=False),
         "Only the resource constant differs in the entire source AST")
    need([ast.dump(n, include_attributes=False) for n in tree.body if isinstance(n, ast.FunctionDef)]
         == [ast.dump(n, include_attributes=False) for n in changed.body if isinstance(n, ast.FunctionDef)],
         "Every mathematical, parser, topology and acceptance function is unchanged")
    return result


def _metadata(patched):
    return dict(schema="N25_B4_Q2_RESOURCE_LIMIT_EPOCH_V1", target=TARGET, n=25, index=29,
                scope=SCOPE, original_design_sha256=ORIGINAL_DESIGN_SHA256,
                original_checker_sha256=ORIGINAL_CHECKER_SHA256,
                checker_sha256=sha(patched), original_node_limit=ORIGINAL_NODE_LIMIT,
                node_limit=NODE_LIMIT, maximum_depth=128,
                transformation=dict(original="LIMIT=10000", replacement="LIMIT=100000",
                                    top_level_assignments_changed=1, all_other_bytes_unchanged=True),
                resource_only_source_relation_verified=True, all_function_asts_unchanged=True,
                complete_original_roots=26, original_corruption_controls=24,
                contract_and_kernels_unchanged=True, original_profile_acceptance=False,
                arithmetic_accepted=False, parent_acquisitions_verified=False,
                all_index_conclusion_verified=False)


def _derive(design_raw, checker_raw):
    need(sha(design_raw) == ORIGINAL_DESIGN_SHA256, "Pinned original B4 q2 source design")
    need(sha(checker_raw) == ORIGINAL_CHECKER_SHA256, "Pinned original B4 q2 checker")
    design = json.loads(design_raw, object_pairs_hook=original.unique)
    need(set(design) == {"files"} and type(design["files"]) is dict,
         "Original source design schema")
    need(design["files"].get("count_protocol.py") == ORIGINAL_CHECKER_SHA256,
         "Original design binds the original checker")
    patched = _patch(checker_raw)
    metadata = encoded(_metadata(patched))
    files = dict(design["files"])
    need(not ({EPOCH, ORIGINAL_DESIGN, ORIGINAL_CHECKER} & set(files)), "New sealed epoch names")
    files.update({"count_protocol.py": sha(patched), ORIGINAL_DESIGN: sha(design_raw),
                  ORIGINAL_CHECKER: sha(checker_raw), EPOCH: sha(metadata)})
    return files, encoded({"files": files}), patched, metadata


def _raw(path, maximum=16*1024**2):
    path = Path(path)
    need(path.is_file() and not path.is_symlink() and path.stat().st_size <= maximum,
         "Bounded regular sealed source file")
    return path.read_bytes()


def build(original_capsule, destination):
    """Create a fresh private derived capsule, preserving all original evidence."""
    source, destination = Path(original_capsule), Path(destination)
    original.verify_capsule(TARGET, source)
    original_files = original.read(source / "FROZEN_DESIGN.json")["files"]
    files, design, patched, metadata = _derive(_raw(source / "FROZEN_DESIGN.json"),
                                               _raw(source / "count_protocol.py"))
    need(sha(design) == NEW_DESIGN_SHA256, "Externally pinned extended B4 q2 source design")
    need(not destination.exists(), "Fresh extended source capsule only")
    payload = {name: _raw(source / name) for name in original_files}
    need(all(sha(payload[name]) == pin for name, pin in original_files.items()),
         "Stable original frozen closure before copying")
    payload.update({"count_protocol.py": patched, ORIGINAL_DESIGN: _raw(source / "FROZEN_DESIGN.json"),
                    ORIGINAL_CHECKER: _raw(source / "count_protocol.py"), EPOCH: metadata,
                    "FROZEN_DESIGN.json": design})
    destination.mkdir(parents=True, exist_ok=False)
    for name, raw in sorted(payload.items()):
        with (destination / name).open("xb") as stream:
            stream.write(raw)
    verify(TARGET, destination)
    return dict(schema="N25_COUNT_LIMIT_SOURCE_BUILD_V1", target=TARGET, scope=SCOPE,
                original_design_sha256=ORIGINAL_DESIGN_SHA256, design_sha256=NEW_DESIGN_SHA256,
                checker_sha256=sha(patched), contract_sha256=files["contract.json"],
                files=len(files), source_adapter_sha256=original.digest(__file__),
                resource_epoch=_metadata(patched), arithmetic_accepted=False,
                parent_acquisitions_verified=False, all_index_conclusion_verified=False)


def verify(target, capsule):
    """Recreate the exact deterministic derived design without importing kernels."""
    need(target == TARGET, "Only the fixed B4 q2 resource epoch")
    capsule = Path(capsule)
    need(capsule.is_dir() and not capsule.is_symlink(), "Regular extended source capsule")
    files, design, patched, metadata = _derive(_raw(capsule / ORIGINAL_DESIGN),
                                               _raw(capsule / ORIGINAL_CHECKER))
    need(sha(design) == NEW_DESIGN_SHA256 and _raw(capsule / "FROZEN_DESIGN.json") == design,
         "Exact externally pinned deterministic extended design")
    need(_raw(capsule / "count_protocol.py") == patched and _raw(capsule / EPOCH) == metadata,
         "Exact resource-only checker and explicit sealed epoch")
    allowed = set(files) | {"FROZEN_DESIGN.json", "COUNT29_FOREST.json", "COUNT29_ACCEPTED.json"}
    actual = set()
    for path in capsule.iterdir():
        need(path.is_file() and not path.is_symlink(), "Only flat regular sealed inputs/native outputs")
        actual.add(path.name)
    need(set(files) | {"FROZEN_DESIGN.json"} <= actual <= allowed,
         "Exact sealed inventory with only explicit native JSON outputs")
    for name, pin in files.items():
        need(type(name) is str and Path(name).name == name and "/" not in name and "\\" not in name,
             "Flat sealed source filename")
        need(sha(_raw(capsule / name)) == pin, "Unchanged sealed source: " + name)
    return files


def verify_capsule(capsule):
    return verify(TARGET, capsule)


def migrate_checkpoint(packet, original_capsule, extended_capsule):
    """Return a new untrusted packet; only the two explicit source pins change."""
    original.verify_capsule(TARGET, original_capsule)
    original.check_checkpoint(packet, TARGET, original_capsule)
    verify(TARGET, extended_capsule)
    result = deepcopy(packet)
    result["binding"]["design_sha256"] = NEW_DESIGN_SHA256
    result["binding"]["native_header"]["checker_sha256"] = original.digest(Path(extended_capsule) / "count_protocol.py")
    expected_header = original.native_header(extended_capsule, TARGET)
    need(all(result["binding"]["native_header"].get(k) == v for k, v in expected_header.items()),
         "Migrated header retains the original contract, roots and kernels")
    restored = deepcopy(result)
    restored["binding"]["design_sha256"] = packet["binding"]["design_sha256"]
    restored["binding"]["native_header"]["checker_sha256"] = packet["binding"]["native_header"]["checker_sha256"]
    need(canonical(restored) == canonical(packet) and canonical(result["roots"]) == canonical(packet["roots"]),
         "Only design/checker pins migrate; every candidate node/payload is preserved")
    need(result["arithmetic_accepted"] is False, "Migration never accepts arithmetic")
    return result


def forest_census(forest, target, capsule):
    """Complete source/header/topology census under the explicit new finite cap."""
    verify(target, capsule)
    need(type(forest) is dict, "Native candidate dictionary")
    for key, value in original.native_header(capsule, target).items():
        need(forest.get(key) == value, "Exact extended native candidate header: " + key)
    roots = forest.get("roots")
    need(type(roots) is list and len(roots) == 26, "Complete26-root candidate")
    nodes = leaves = 0
    for k, root in enumerate(roots):
        need(type(root) is dict and set(root) == {"k", "tree"} and type(root["k"]) is int
             and root["k"] == k, "All original roots in exact order")
        stack = [(root["tree"], 0)]
        while stack:
            node, depth = stack.pop()
            nodes += 1
            need(nodes <= NODE_LIMIT and depth <= 128 and type(node) is dict,
                 "Explicit extended finite native tree limits")
            if node.get("kind") == "leaf":
                need(set(node) == {"kind", "box", "decision", "result"} and node["decision"] is not None,
                     "Complete untrusted leaf payload")
                leaves += 1
            else:
                need(set(node) == {"kind", "axis", "cut", "left", "right"} and node["kind"] == "split"
                     and type(node["axis"]) is int and 0 <= node["axis"] < 5 and type(node["cut"]) is str,
                     "Complete canonical binary split; no pending nodes")
                Fraction(node["cut"])
                stack.extend(((node["left"], depth+1), (node["right"], depth+1)))
    need(nodes == 2*leaves-26, "Full26-root binary forest census")
    return dict(nodes=nodes, leaves=leaves, roots=26)
