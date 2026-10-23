"""Sealed original B0--B2 sources/candidates; never import an archived kernel.

Selection is fixed by the externally pinned catalog. Historical acceptance
outputs are excluded. Every numerical conclusion requires a new Linux replay.
"""
from __future__ import annotations

import ast
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

from . import count_task as common

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "proof/n25_retained_b012_catalog.json"
CATALOG_SHA256 = "f055b5017d4e1fd14f2b48a6a95fef4a4c61a025dea6174c424cd5968de801f7"
EXPECTED_COUNTS = {"b0": 17, "b1": 35, "b2": 23}
MANIFEST = "SOURCES.json"
PREPARATION = "SOURCE_PREPARATION.json"
MIB = 1024**2
MAX_SOURCE = 16*MIB
MAX_FOREST = 128*MIB
MAX_TOTAL = 512*MIB
EXECUTION_CONTRACT = "NEW_LINUX_REPLAY_REQUIRED_NO_HISTORICAL_WINDOWS_GUARD_CLAIM"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)+"\n").encode("ascii")


def _link(path):
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def _regular(path, limit):
    path = Path(path)
    need(path.is_file() and not _link(path) and path.stat().st_size <= limit,
         "Bounded regular source/candidate file")
    return path.read_bytes()


def _json(raw):
    return json.loads(raw, object_pairs_hook=common.unique)


def _flat(name):
    need(type(name) is str and name and name not in (".", "..")
         and "/" not in name and "\\" not in name and ":" not in name and "\x00" not in name
         and name == name.rstrip(" ."), "Safe flat selected filename")
    return name


def _member(name):
    need(type(name) is str and name.startswith("cutoff25_20261011/")
         and "\\" not in name and ":" not in name and "\x00" not in name
         and not PurePosixPath(name).is_absolute()
         and all(p and p not in (".", "..") and p == p.rstrip(" .") for p in name.split("/")),
         "Literal archive-relative selected member")
    return name


def _catalog():
    raw = _regular(CATALOG, 8*MIB)
    need(sha(raw) == CATALOG_SHA256, "Externally pinned complete B0--B2 selection catalog")
    value = _json(raw)
    need(value["schema"] == "N25_RETAINED_B012_SELECTED_COUNT_CATALOG_V1"
         and len(value["jobs"]) == sum(EXPECTED_COUNTS.values()), "Complete fixed retained selection")
    ids = set()
    for row in value["jobs"]:
        identity = row["target_id"]
        need(row["branch"] in EXPECTED_COUNTS and type(identity) is str
             and re.fullmatch(r"b[012]-p[0-9]{1,2}(?:-q[0-3])?", identity) is not None
             and identity.startswith(row["branch"]+"-") and identity not in ids
             and row["archive_key"] == "old" and row["availability"] == "SELECTED_SOURCE_AND_CANDIDATE_FOUND"
             and row["historical_acceptance_is_fresh_evidence"] is False,
             "Unique safe selected job; no arbitrary source selection")
        ids.add(identity)
    need(Counter(j["branch"] for j in value["jobs"]) == EXPECTED_COUNTS,
         "Exactly17/35/23 selected B0/B1/B2 forests")
    return value


def jobs(branch):
    need(type(branch) is str and branch in EXPECTED_COUNTS, "Retained branch b0, b1 or b2 only")
    rows = deepcopy([j for j in _catalog()["jobs"] if j["branch"] == branch])
    for row in rows:
        row.update(job_id=row["target_id"], capsule_relative="capsules/"+row["target_id"])
    return rows


def _selected(job):
    need(type(job) is dict and job.get("branch") in EXPECTED_COUNTS, "One fixed selected catalog job")
    selected = [j for j in jobs(job["branch"]) if j["job_id"] == job.get("job_id")]
    need(len(selected) == 1 and encoded(job) == encoded(selected[0]), "Unchanged literal catalog job")
    return selected[0]


def _selection(job, design_raw):
    need(sha(design_raw) == job["source_epoch_manifest_sha256"], "Pinned original source design")
    design = _json(design_raw)
    need("files" in design and set(design) <= {"files", "status", "scope"} and type(design["files"]) is dict
         and len(design["files"]) == job["source_epoch_declared_file_count"], "Complete original design")
    prefix = job["capsule_member_prefix"].rstrip("/")+"/"
    expected = {}
    for row in job["source_file_rows"]:
        name = _flat(row["filename"])
        member = _member(row["member"])
        need(member == prefix+name and name not in expected, "Exact unique catalog source member")
        expected[name] = dict(filename=name, member=member, sha256=row["sha256"], bytes=row["bytes"], role="source")
    for name, pin in design["files"].items():
        _flat(name)
        need(re.search(r"(?:ACCEPTED|ACCEPTANCE|RECEIPT|EXECUTION|PROGRESS|COMPLETED)", name, re.I) is None,
             "No historical acceptance/execution output in a source closure")
        need(name != job["forest_filename"] and not re.fullmatch(r"COUNT[0-9]+_FOREST.json", name),
             "Candidate forest is separately classified")
        if name in expected:
            need(expected[name]["sha256"] == pin, "Original design equals actual runtime source pin")
        else:
            expected[name] = dict(filename=name, member=_member(prefix+name), sha256=pin, bytes=None, role="source")
    design_name = _flat(job["source_epoch_manifest_filename"])
    need(design_name == "FROZEN_DESIGN.json" and design_name not in expected, "Original design filename")
    expected[design_name] = dict(filename=design_name, member=_member(prefix+design_name),
                               sha256=job["source_epoch_manifest_sha256"], bytes=len(design_raw), role="source")
    forest = _flat(job["forest_filename"])
    need(forest == f"COUNT{job['index']}_FOREST.json" and forest not in expected,
         "Literal selected candidate forest")
    expected[forest] = dict(filename=forest, member=_member(prefix+forest), sha256=job["forest_sha256"],
                           bytes=None, role="candidate")
    need(job["acceptance_filename"] not in expected, "Archived acceptance is never selected")
    return expected


def _capsule(job, capsule):
    capsule = Path(capsule)
    need(capsule.is_dir() and not _link(capsule), "Regular sealed retained capsule")
    expected = _selection(job, _regular(capsule / "FROZEN_DESIGN.json", MAX_SOURCE))
    actual = set()
    for path in capsule.iterdir():
        need(path.is_file() and not _link(path), "Flat regular source/candidate/output inventory")
        actual.add(path.name)
    need(set(expected) <= actual <= set(expected) | {job["acceptance_filename"]},
         "Exact sealed source and candidate; only the explicit fresh native output may coexist")
    rows = []
    for name, row in sorted(expected.items()):
        raw = _regular(capsule/name, MAX_FOREST if row["role"] == "candidate" else MAX_SOURCE)
        need(sha(raw) == row["sha256"] and (row["bytes"] is None or len(raw) == row["bytes"]),
             "Exact sealed retained input: "+name)
        rows.append(dict(row, bytes=len(raw)))
    need(sha(_regular(capsule/"contract.json", MAX_SOURCE)) == job["contract_sha256"]
         and sha(_regular(capsule/"count_protocol.py", MAX_SOURCE)) == job["checker_sha256"]
         and sha(_regular(capsule/job["manifest_filename"], MAX_SOURCE)) == job["manifest_sha256"],
         "Exact checker, contract and kernel-manifest pins")
    manifest = _json(_regular(capsule/job["manifest_filename"], MAX_SOURCE))["files"]
    need(len(manifest) == job["kernel_file_count"] and all(
        name in expected and expected[name]["sha256"] == pin for name, pin in manifest.items()),
        "Complete original exact kernel binding")
    return rows, manifest


def _structure(job, capsule, kernel):
    capsule = Path(capsule)
    source = ast.parse(_regular(capsule/"count_protocol.py", MAX_SOURCE))
    limit = [n.value.value for n in source.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == "LIMIT" for t in n.targets)
             and isinstance(n.value, ast.Constant)]
    need(limit == [10000] and type(limit[0]) is int, "Original10000-node finite native profile")
    functions = [n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == "header"]
    need(len(functions) == 1 and len(functions[0].body) == 1
         and isinstance(functions[0].body[0], ast.Return), "Literal native header")
    call = functions[0].body[0].value
    need(isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == "dict",
         "Literal native dict header")
    literals = {n.arg: n.value for n in call.keywords}
    header = {k: ast.literal_eval(literals[k]) for k in ("schema", "n", "index")}
    need(header == dict(schema=job["forest_schema"], n=25, index=job["index"]), "Catalog/native header identity")
    contract = _json(_regular(capsule/"contract.json", MAX_SOURCE))
    need(len(contract["rows"]) == 1, "One fixed conditional count panel")
    cfg = contract["rows"][0]
    need(type(cfg["n"]) is int and cfg["n"] == 25 and type(cfg["index"]) is int
         and cfg["index"] == job["index"] and cfg["p"] == job["p_interval"]
         and [cfg["rho_lower"], cfg["rho_upper"]] == job["rho_interval"] and F(cfg["K"]) == 0,
         "Same actual-n25 closed probability/rho contract")
    forest = _json(_regular(capsule/job["forest_filename"], MAX_FOREST))
    need(type(forest) is dict and set(forest) == {"schema", "n", "index", "target", "contract_sha256", "kernel_sha256", "checker_sha256", "roots"}
         and type(forest["n"]) is int and type(forest["index"]) is int
         and all(forest[k] == v for k, v in header.items())
         and forest["contract_sha256"] == job["contract_sha256"]
         and forest["checker_sha256"] == job["checker_sha256"] and forest["kernel_sha256"] == kernel
         and type(forest["target"]) is str, "Complete original candidate header/source binding")
    box = [list(map(F, cfg["p"])), [F(0), F(cfg["Lambda"])], [F(0), F(1)], [F(-1, 2), F(1, 2)], [F(0), F(cfg["d0"])]]
    need(len(forest["roots"]) == 26, "All26 original closed count roots")
    nodes = leaves = splits = depth_max = 0
    maximum = F(0)
    statuses = Counter()
    for k, root in enumerate(forest["roots"]):
        need(type(root) is dict and set(root) == {"k", "tree"} and type(root["k"]) is int and root["k"] == k,
             "Complete ordered roots0 through25")
        stack = [(root["tree"], box, 0)]
        while stack:
            node, current, depth = stack.pop()
            nodes += 1
            depth_max = max(depth_max, depth)
            need(nodes <= 10000 and depth <= 128 and type(node) is dict, "Original finite tree bounds")
            if node.get("kind") == "split":
                need(set(node) == {"kind", "axis", "cut", "left", "right"} and type(node["axis"]) is int
                     and 0 <= node["axis"] < 5 and type(node["cut"]) is str, "Complete binary rational split")
                axis, cut = node["axis"], F(node["cut"])
                need(current[axis][0] < cut < current[axis][1], "Strict interior closed split")
                left, right = deepcopy(current), deepcopy(current)
                left[axis][1] = right[axis][0] = cut
                stack.extend(((node["left"], left, depth+1), (node["right"], right, depth+1)))
                splits += 1
            else:
                need(node.get("kind") == "leaf" and set(node) == {"kind", "box", "decision", "result"}
                     and node["box"] == [[str(v) for v in pair] for pair in current]
                     and type(node["decision"]) is str and node["decision"] and type(node["result"]) is dict,
                     "Complete closed leaf geometry and untrusted payload")
                leaves += 1
                statuses[node["decision"]] += 1
                if node["decision"] == "PASS_TARGET":
                    maximum = max(maximum, F(node["result"]["score_upper"]))
    need(nodes == 2*leaves-26 and (nodes, leaves, splits) == (job["node_count"], job["leaf_count"], job["split_count"])
         and leaves == job["expected_selected_leaves"], "Whole selected geometric census")
    return dict(roots=26, nodes=nodes, leaves=leaves, splits=splits, maximum_depth=depth_max,
                closed_statuses=dict(statuses), maximum_score=str(maximum))


def census(job, capsule):
    job = _selected(job)
    _, kernel = _capsule(job, capsule)
    return _structure(job, capsule, kernel)


def _manifest(branch, task):
    selected = jobs(branch)
    directory = Path(task)/"capsules"
    need(directory.is_dir() and not _link(directory), "Regular selected capsule namespace")
    need({p.name for p in directory.iterdir()} == {j["job_id"] for j in selected}, "Exactly the selected branch capsules")
    rows = []
    for job in selected:
        capsule = Path(task)/job["capsule_relative"]
        files, kernel = _capsule(job, capsule)
        _structure(job, capsule, kernel)
        rows.append(dict(job_id=job["job_id"], target_id=job["target_id"], index=job["index"],
            capsule_relative=job["capsule_relative"], forest_filename=job["forest_filename"],
            acceptance_filename=job["acceptance_filename"], source_design_sha256=job["source_epoch_manifest_sha256"],
            contract_sha256=job["contract_sha256"], checker_sha256=job["checker_sha256"],
            kernel_manifest_sha256=job["manifest_sha256"], forest_sha256=job["forest_sha256"], files=files))
    return dict(schema="RETAINED_N25_SOURCES_V1", branch=branch, catalog_sha256=CATALOG_SHA256,
                archive_asset=deepcopy(common.ASSETS["old"]), jobs=rows,
                execution_contract=EXECUTION_CONTRACT, source_algorithms_changed=False,
                historical_acceptance_used=False, fresh_arithmetic_replayed=False,
                parent_acquisitions_verified=False, full_n25_verified=False, all_index_conclusion_verified=False)


def prepare(branch, archive, output):
    """Extract every selected source/candidate byte; never copy an old receipt."""
    selected = jobs(branch)
    archive, output = Path(archive), Path(output).absolute()
    common.verify_asset(archive, common.ASSETS["old"])
    need(not output.exists() and not _link(output), "Fresh private retained source task")
    need(all(not _link(p) for p in output.parents if p.exists()), "No linked output ancestry")
    with zipfile.ZipFile(archive) as zipped:
        index = {}
        for info in zipped.infolist():
            index.setdefault(info.filename.casefold(), []).append(info)
        def member(name, limit):
            _member(name)
            matches = index.get(name.casefold(), [])
            need(len(matches) == 1 and matches[0].filename == name, "Unique exact-case selected ZIP member")
            info = matches[0]
            mode = info.external_attr >> 16
            need(not info.is_dir() and not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0, stat.S_IFREG)
                 and not info.flag_bits & 1 and 0 <= info.file_size <= limit, "Bounded regular unencrypted selected ZIP member")
            return info
        selections = []
        total = 0
        for job in selected:
            design_member = job["capsule_member_prefix"].rstrip("/")+"/FROZEN_DESIGN.json"
            design = zipped.read(member(design_member, MAX_SOURCE))
            expected = _selection(job, design)
            for row in expected.values():
                info = member(row["member"], MAX_FOREST if row["role"] == "candidate" else MAX_SOURCE)
                need(row["bytes"] is None or row["bytes"] == info.file_size, "Catalog member byte count")
                total += info.file_size
            selections.append((job, expected))
        need(total <= MAX_TOTAL, "Bounded complete branch extraction")
        output.mkdir(parents=True, exist_ok=False)
        for job, expected in selections:
            capsule = output/job["capsule_relative"]
            capsule.mkdir(parents=True, exist_ok=False)
            for name, row in sorted(expected.items()):
                raw = zipped.read(member(row["member"], MAX_FOREST if row["role"] == "candidate" else MAX_SOURCE))
                need(sha(raw) == row["sha256"], "Actual archived selected source/candidate SHA: "+row["member"])
                with (capsule/name).open("xb") as stream:
                    stream.write(raw)
    manifest = _manifest(branch, output)
    (output/MANIFEST).write_bytes(encoded(manifest))
    report = dict(schema="RETAINED_N25_SOURCE_PREPARATION_V1", branch=branch, catalog_sha256=CATALOG_SHA256,
                  source_manifest_sha256=sha(encoded(manifest)), source_helper_sha256=common.digest(__file__),
                  selected_jobs=len(selected), selected_leaves=sum(j["leaf_count"] for j in selected),
                  archive_verified=True, historical_acceptance_used=False, fresh_arithmetic_replayed=False,
                  full_n25_verified=False, all_index_conclusion_verified=False)
    (output/PREPARATION).write_bytes(encoded(report))
    return manifest


def verify(task):
    """Verify sealed inputs only; external runtime epochs belong to evidence review."""
    task = Path(task)
    need(task.is_dir() and not _link(task), "Regular retained task")
    raw = _regular(task/MANIFEST, 16*MIB)
    saved = _json(raw)
    manifest = _manifest(saved["branch"], task)
    need(raw == encoded(manifest), "Exact deterministic selected source/candidate manifest")
    report = _json(_regular(task/PREPARATION, MIB))
    need(report == dict(schema="RETAINED_N25_SOURCE_PREPARATION_V1", branch=saved["branch"], catalog_sha256=CATALOG_SHA256,
         source_manifest_sha256=sha(raw), source_helper_sha256=common.digest(__file__), selected_jobs=len(manifest["jobs"]),
         selected_leaves=sum(j["leaf_count"] for j in jobs(saved["branch"])), archive_verified=True,
         historical_acceptance_used=False, fresh_arithmetic_replayed=False, full_n25_verified=False,
         all_index_conclusion_verified=False), "Original source-only preparation evidence and current helper pin")
    return manifest
