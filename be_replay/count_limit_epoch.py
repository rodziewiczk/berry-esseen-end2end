"""Source-only resource epochs for seven count jobs; no kernels are imported.

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
PROFILES = {
    "b4-q0": dict(index=29, source_scope="ORIGINAL_V12_CONDITIONAL_COUNT_ONLY",
        original_design_sha256="4d91657ddbab41e3324c00f9f28a9223526c0c1dc79bad5c5e77176240c231f7",
        original_checker_sha256="b50b337dcb99410a051b1958c247534b6287e4af16a0918b847cd9ccee9df034",
        new_design_sha256="765f7ff74e4007ba13e7aff57856d375e2c1cd0b76a6ce35b224eac67bc441d8",
        checker_sha256="582e9cf809b4b03d1e1c27ef11ba9eade1ee9083ad1054784e0b99b779136bc1",
        contract_sha256="6da0412a35fa160d9eef1e88e1ace38eb3b8425ecfd5a4fce0f3eaf3ce5b2535"),
    "b4-q1": dict(index=29, source_scope="ORIGINAL_V12_CONDITIONAL_COUNT_ONLY",
        original_design_sha256="a3cbdb1852bc51054ecc8cd3c71bd1c7121b6b201385e481b73195ad729189c4",
        original_checker_sha256="5475ebdc20b26da41364ac9d108249c29b77ead966066974113b662fbad50195",
        new_design_sha256="25fd9e8675d2c6f0dc6805e0c5273d0e84c32f6d372befe0db35019d0a687197",
        checker_sha256="4a73a17ff180f384f2159c9d552885d9082cb9a0eb3b75da66023f10253b669d",
        contract_sha256="15e13d70c655faf449825b355c8b22dffcf5efef4fb704f9d65e1425aae00c35"),
    "b4-q2": dict(index=29, source_scope="ORIGINAL_V12_CONDITIONAL_COUNT_ONLY"),
    "b4-q3": dict(index=29, source_scope="ORIGINAL_V12_CONDITIONAL_COUNT_ONLY",
        original_design_sha256="c8555b500c3e7d1ca1240b5f229f7fff5ed307571012209e022431ecd195b7ac",
        original_checker_sha256="5063e87db2a388011558a7339331bf0ddf00a13bc173ddc3386234ae4f8310da",
        new_design_sha256="c992f1d472966409357e1a4ae3eef365462947e2400b54f5f3a9befe66cde437",
        checker_sha256="6ab191f5959f971bf000ed7340b70f3878ed4728f40fdd2333d5b9681929ec60",
        contract_sha256="07cabb29930701f591d9822eac130afd1bdfc81cbb5e69b73f569b70f6151f75"),
    "b3-p33": dict(index=33, source_scope="ORIGINAL_V12_CONDITIONAL_COUNT_ONLY",
        original_design_sha256="e55bb3eeac06923f897263a65f2cde9fe77006313dd86f47bbba3f6047f30f08",
        original_checker_sha256="459027ea0126978a2686f726022a50a6a7a635aca2f347991278697c00dfd39a",
        new_design_sha256="b1a7b8c534cd8294b56c7285d44c0facaf6465fc6bf2294881e090ab1d116b5b",
        checker_sha256="dffd740e6cca3d5921b18f18f7fc295e905b545e71ba26becb778dc9a9e0047a",
        contract_sha256="fe106d1ffe295de3fa68ccf44a625323fe0e68ce1c4462730729b5b2e0e3963a"),
    "b3-p31-v14-new": dict(index=31, source_scope="NEW_CONDITIONAL_V14_NOT_HISTORICAL_IDENTITY",
        original_design_sha256="bc699a2d539b4aafc193049c8074b02e0b77a38fb01b594c1ba3e2fde6b7b3ff",
        original_checker_sha256="185aa974fc0da02f64034bb56f8099a809c67a7424d7169c9d36c4ce46bd9355",
        new_design_sha256="ba741cebd773a1b939b69729303e40a58b5fd80cbd0876310a8e5c3b5cba459d",
        checker_sha256="d7ac0a8a083124249a2866e252c4be025eb960f2a36f69af5abede5591922ae4",
        contract_sha256="9b71a135188234ba200ae145860659f4def488aec9feec278748f8e31eafd142"),
    "b3-p32-v14-new": dict(index=32, source_scope="NEW_CONDITIONAL_V14_NOT_HISTORICAL_IDENTITY",
        original_design_sha256="cfe934b1385f9a26f36b6bf94cda9e5caeb6593700a54eeac7e7b1638df61627",
        original_checker_sha256="204eb43f145db0f4422be0e69b7ec5c06bca90b0200af1fe8512419f6ca7abce",
        new_design_sha256="2f15572df398d0341cc174c7ab4a4e71c701890ed92718c8e40b1c4aa8447129",
        checker_sha256="a4fff2e8c6ab047f008def8ddc2c22d3c49b91799f5262b3c8d95603bb64cf45",
        contract_sha256="0019e13d3857849762eed1518ad63c3f6aa6133dde0fd84a9ea88674f6e34627"),
}


def profile(target=TARGET):
    need(type(target) is str and target in PROFILES, "One of the seven fixed count resource epochs")
    result = deepcopy(PROFILES[target])
    if target == TARGET:
        # These public aliases preserve the original standalone q2 API/profile.
        result.update(original_design_sha256=ORIGINAL_DESIGN_SHA256,
                      original_checker_sha256=ORIGINAL_CHECKER_SHA256,
                      new_design_sha256=NEW_DESIGN_SHA256, checker_sha256=CHECKER_SHA256,
                      contract_sha256=CONTRACT_SHA256)
    result.update(target=target, node_limit=NODE_LIMIT, original_node_limit=ORIGINAL_NODE_LIMIT)
    return result


def resource_scope(target=TARGET):
    return (SCOPE if profile(target)["source_scope"] == "ORIGINAL_V12_CONDITIONAL_COUNT_ONLY"
            else "RESOURCE_EXTENDED_PORTABLE_V14_COUNT_ONLY")


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


def _metadata(patched, target=TARGET):
    spec = profile(target)
    return dict(schema=("N25_B4_Q2_RESOURCE_LIMIT_EPOCH_V1" if target == TARGET else
                        "N25_COUNT_RESOURCE_LIMIT_EPOCH_V1"), target=target, n=25, index=spec["index"],
                scope=resource_scope(target), original_design_sha256=spec["original_design_sha256"],
                original_checker_sha256=spec["original_checker_sha256"],
                checker_sha256=sha(patched), original_node_limit=ORIGINAL_NODE_LIMIT,
                node_limit=NODE_LIMIT, maximum_depth=128,
                transformation=dict(original="LIMIT=10000", replacement="LIMIT=100000",
                                    top_level_assignments_changed=1, all_other_bytes_unchanged=True),
                resource_only_source_relation_verified=True, all_function_asts_unchanged=True,
                complete_original_roots=26, original_corruption_controls=24,
                contract_and_kernels_unchanged=True, original_profile_acceptance=False,
                arithmetic_accepted=False, parent_acquisitions_verified=False,
                all_index_conclusion_verified=False)


def metadata(target=TARGET):
    """Return exact sealed resource-policy metadata without opening a capsule."""
    spec = profile(target)
    # _metadata only uses the patched source through its digest.
    result = _metadata(b"", target)
    result["checker_sha256"] = spec["checker_sha256"]
    return result


def _derive(design_raw, checker_raw, target=TARGET):
    spec = profile(target)
    need(sha(design_raw) == spec["original_design_sha256"], "Pinned original count source design")
    need(sha(checker_raw) == spec["original_checker_sha256"], "Pinned original count checker")
    design = json.loads(design_raw, object_pairs_hook=original.unique)
    need(set(design) == {"files"} and type(design["files"]) is dict,
         "Original source design schema")
    need(design["files"].get("count_protocol.py") == spec["original_checker_sha256"],
         "Original design binds the original checker")
    patched = _patch(checker_raw)
    metadata = encoded(_metadata(patched, target))
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


def build(original_capsule, destination, target=TARGET):
    """Create a fresh private derived capsule, preserving all original evidence."""
    source, destination = Path(original_capsule), Path(destination)
    spec = profile(target)
    original.verify_capsule(target, source)
    original_files = original.read(source / "FROZEN_DESIGN.json")["files"]
    files, design, patched, metadata = _derive(_raw(source / "FROZEN_DESIGN.json"),
                                               _raw(source / "count_protocol.py"), target)
    need(sha(design) == spec["new_design_sha256"], "Externally pinned extended count source design")
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
    verify(target, destination)
    return dict(schema="N25_COUNT_LIMIT_SOURCE_BUILD_V1", target=target, scope=resource_scope(target),
                original_design_sha256=spec["original_design_sha256"], design_sha256=spec["new_design_sha256"],
                checker_sha256=sha(patched), contract_sha256=files["contract.json"],
                files=len(files), source_adapter_sha256=original.digest(__file__),
                resource_epoch=_metadata(patched, target), arithmetic_accepted=False,
                parent_acquisitions_verified=False, all_index_conclusion_verified=False)


def verify(target, capsule):
    """Recreate the exact deterministic derived design without importing kernels."""
    spec = profile(target)
    capsule = Path(capsule)
    need(capsule.is_dir() and not capsule.is_symlink(), "Regular extended source capsule")
    files, design, patched, metadata = _derive(_raw(capsule / ORIGINAL_DESIGN),
                                               _raw(capsule / ORIGINAL_CHECKER), target)
    need(sha(design) == spec["new_design_sha256"] and _raw(capsule / "FROZEN_DESIGN.json") == design,
         "Exact externally pinned deterministic extended design")
    need(_raw(capsule / "count_protocol.py") == patched and _raw(capsule / EPOCH) == metadata,
         "Exact resource-only checker and explicit sealed epoch")
    index = spec["index"]
    allowed = set(files) | {"FROZEN_DESIGN.json", f"COUNT{index}_FOREST.json", f"COUNT{index}_ACCEPTED.json"}
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


def verify_capsule(capsule, target=TARGET):
    return verify(target, capsule)


def migrate_checkpoint(packet, original_capsule, extended_capsule, target=TARGET):
    """Return a new untrusted packet; only the two explicit source pins change."""
    spec = profile(target)
    original.verify_capsule(target, original_capsule)
    original.check_checkpoint(packet, target, original_capsule)
    verify(target, extended_capsule)
    result = deepcopy(packet)
    result["binding"]["design_sha256"] = spec["new_design_sha256"]
    result["binding"]["native_header"]["checker_sha256"] = original.digest(Path(extended_capsule) / "count_protocol.py")
    expected_header = original.native_header(extended_capsule, target)
    need(all(result["binding"]["native_header"].get(k) == v for k, v in expected_header.items()),
         "Migrated header retains the original contract, roots and kernels")
    restored = deepcopy(result)
    restored["binding"]["design_sha256"] = packet["binding"]["design_sha256"]
    restored["binding"]["native_header"]["checker_sha256"] = packet["binding"]["native_header"]["checker_sha256"]
    need(canonical(restored) == canonical(packet) and canonical(result["roots"]) == canonical(packet["roots"]),
         "Only design/checker pins migrate; every candidate node/payload is preserved")
    need(result["arithmetic_accepted"] is False, "Migration never accepts arithmetic")
    return result


def checkpoint_geometry(packet, capsule, target=TARGET, *, node_limit=NODE_LIMIT):
    """Reconstruct saved closed boxes without importing a numerical evaluator.

    This validates only topology/geometry. Saved leaf decisions and result
    dictionaries remain untrusted and must be replayed by the native acceptor.
    """
    from fractions import Fraction as F
    need(type(node_limit) is int and 26 <= node_limit <= NODE_LIMIT,
         "Explicit bounded checkpoint node policy")
    contract = original.read(Path(capsule) / "contract.json")
    rows = contract.get("rows")
    need(type(rows) is list and len(rows) == 1 and type(rows[0]) is dict,
         "One sealed native target row")
    cfg = rows[0]
    need(type(cfg.get("n")) is int and cfg["n"] == 25
         and type(cfg.get("index")) is int and cfg["index"] == profile(target)["index"],
         "Checkpoint literal native target row")
    def rational(value):
        need(type(value) is str and len(value) <= 10000, "Bounded exact rational text")
        number = F(value)
        need(str(number) == value, "Canonical checkpoint rational")
        return number
    p = cfg.get("p")
    need(type(p) is list and len(p) == 2, "Complete native probability interval")
    pl, pu = map(rational, p)
    lam, d0 = rational(cfg["Lambda"]), rational(cfg["d0"])
    need(0 < pl < pu < 1 and lam > 0 and d0 > 0, "Positive sealed root domain")
    rootbox = [[pl, pu], [F(0), lam], [F(0), F(1)],
               [-F(1, 2), F(1, 2)], [F(0), d0]]
    roots = packet.get("roots")
    need(type(roots) is list and len(roots) == 26, "Exactly26 complete checkpoint roots")
    nodes = leaves = pending = depthmax = 0
    for k, root in enumerate(roots):
        need(type(root) is dict and set(root) == {"k", "tree"}
             and type(root["k"]) is int and root["k"] == k, "Ordered literal count roots")
        stack = [(root["tree"], rootbox, 0)]
        while stack:
            node, box, depth = stack.pop()
            nodes += 1
            depthmax = max(depthmax, depth)
            need(nodes <= node_limit and depth <= 128 and type(node) is dict,
                 "Bounded checkpoint topology")
            kind = node.get("kind")
            if kind == "pending":
                need(set(node) == {"kind"}, "Pending carries no success payload")
                pending += 1
            elif kind == "leaf":
                need(set(node) == {"kind", "box", "decision", "result"}
                     and type(node["decision"]) is str and type(node["result"]) is dict,
                     "Exact untrusted native leaf fields")
                need(canonical(node["box"]) == canonical([[str(x) for x in row] for row in box]),
                     "Every saved leaf has its reconstructed closed native box")
                leaves += 1
            else:
                need(kind == "split" and set(node) == {"kind", "axis", "cut", "left", "right"}
                     and type(node["axis"]) is int and 0 <= node["axis"] < 5,
                     "Complete literal native binary split")
                axis, cut = node["axis"], rational(node["cut"])
                need(box[axis][0] < cut < box[axis][1], "Strict interior saved native cut")
                left, right = deepcopy(box), deepcopy(box)
                left[axis][1], right[axis][0] = cut, cut
                stack.extend(((node["right"], right, depth + 1),
                              (node["left"], left, depth + 1)))
    need(nodes == 2 * (leaves + pending) - 26, "Full binary checkpoint census")
    return dict(nodes=nodes, leaves=leaves, pending=pending, maximum_depth=depthmax)


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
