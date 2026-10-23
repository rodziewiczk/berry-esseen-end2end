"""Freeze C5 supervisory sources and build a source/JSON-only replay catalog.

This maintenance command never imports an archived mathematical module. The
only imported upstream modules are the stdlib-only source selectors. No native
acceptor, evaluator, support inequality or quadrature routine is executed.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor/n5_remaining_snapshot_v1"
ARCHIVE_SHA = "8428002462d4e650613ea6e2ff673cb1e69c2079572cc40546d125349d582419"
ARCHIVE_BYTES = 141304365
PREFIX = "cutoff5_20261020/root/delivery_extract_v1/"
FINAL = "work/cutoff5_20261020/root/final_composition_v2/C5_CHECKED.json"
FINAL_SHA = "923a0d0cf3c481ae60c5e2b69d886098a7501f916a52668b37b0198f26fde4a0"
INDEX = "cutoff5_20261020/entry/delivery_review_v1/SELECTED_REPLAY_COMMANDS.json"
INDEX_SHA = "74ca2086929fd68c92416f9c0acfe8c2dce08bd31a4a5e7388a95ffc49c70341"
EXTRAS = "work/cutoff5_20261020/entry/delivery_review_v1/EXTRA_SOURCES.json"


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda: f.read(1024**2), b""): h.update(b)
    return h.hexdigest()


def dump(path, data, *, replace=False):
    raw = (json.dumps(data, sort_keys=True, indent=2) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != raw:
            if not replace: raise ValueError("Existing frozen output differs: " + str(path))
            path.write_bytes(raw)
    else: path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def freeze(old):
    declared = json.loads((old / "code/SHA256SUMS.json").read_text())["files"]
    paths = ["run_reproduction.py", "code/SHA256SUMS.json"]
    paths += ["code/" + r["path"] for r in declared]
    paths += [p.relative_to(old).as_posix() for p in (old / "reproduction/all_indices").glob("*.py")]
    # The actual snapshot is identified by every byte hash, not an unverified
    # assertion that the old checkout is a particular Git commit.
    files = []
    for name in sorted(paths):
        source, target = old / name, VENDOR / name
        raw = source.read_bytes()
        if target.exists() and target.read_bytes() != raw: raise ValueError("Frozen snapshot changed: " + name)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists(): target.write_bytes(raw)
        files.append(dict(path=name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    license_path = old.parent / "LICENSE"
    if not license_path.exists(): license_path = ROOT / "vendor/count_75a9470/LICENSE"
    raw = license_path.read_bytes()
    target = VENDOR / "LICENSE"
    if target.exists() and target.read_bytes() != raw: raise ValueError("Frozen license changed")
    if not target.exists(): target.write_bytes(raw)
    files.append(dict(path="LICENSE", bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    return dump(VENDOR / "SNAPSHOT.json", dict(schema="UNCHANGED_C5_SUPERVISORY_SOURCE_SNAPSHOT_V1",
        source="Original read-only publication snapshot; exact bytes, no Git-state claim",
        files=sorted(files, key=lambda r:r["path"]), mathematical_modules_executed=False))


def safe(name):
    parts = name.split("/")
    if not name or any(c in name for c in ("\\", ":", "\0")) or any(p in ("", ".", "..") for p in parts):
        raise ValueError("Unsafe source member")
    return parts


def extract_cache(z, graph, cache):
    for i, (name, pin) in enumerate(graph.items()):
        output = cache.joinpath(*safe(name))
        if output.exists():
            if sha(output) != pin: raise ValueError("Changed source-only cache: " + name)
            continue
        output.parent.mkdir(parents=True, exist_ok=True)
        with z.open(PREFIX + name) as source, output.open("xb") as dest:
            shutil.copyfileobj(source, dest, 1024**2)
        if sha(output) != pin: raise ValueError("Wrong source member hash: " + name)
        if i % 1000 == 0: print("Source-only catalog preparation:", i, "/", len(graph), flush=True)


def census(forest):
    if forest.get("n") != 5 or type(forest.get("n")) is not int: raise ValueError("Literal n5")
    roots = forest["roots"]
    if [r["k"] for r in roots] != list(range(6)) or any(type(r["k"]) is not int for r in roots):
        raise ValueError("Six ordered original count roots")
    nodes = leaves = depth = 0
    for root in roots:
        stack = [(root["tree"], 0)]
        while stack:
            node, level = stack.pop(); nodes += 1; depth = max(depth, level)
            if node["kind"] == "leaf": leaves += 1
            elif node["kind"] == "split": stack += [(node["left"], level+1), (node["right"], level+1)]
            else: raise ValueError("Unknown candidate node")
    return dict(roots=6, nodes=nodes, leaves=leaves, maximum_depth=depth)


def build(old, archive, cache):
    if archive.stat().st_size != ARCHIVE_BYTES or sha(archive) != ARCHIVE_SHA: raise ValueError("Exact C5 archive required")
    snapshot = freeze(old)
    # These imports select and hash sources only. All mathematical imports are
    # inside guarded native scripts and are deliberately not imported here.
    sys.path.insert(0, str(VENDOR / "reproduction/all_indices"))
    plan = importlib.import_module("c5_acquisition_plan")
    high = importlib.import_module("c5_high_one")
    initial = importlib.import_module("c5_initial_one")
    with zipfile.ZipFile(archive) as z:
        final_raw = z.read(PREFIX + FINAL)
        if hashlib.sha256(final_raw).hexdigest() != FINAL_SHA: raise ValueError("Pinned selected source graph")
        graph = dict(json.loads(final_raw)["files_sha256"])
        if len(graph) != 16576: raise ValueError("Complete selected source graph")
        extras_raw = z.read(PREFIX + EXTRAS)
        graph[FINAL], graph[EXTRAS] = FINAL_SHA, hashlib.sha256(extras_raw).hexdigest()
        for r in json.loads(extras_raw)["files"]:
            if r["path"] in graph and graph[r["path"]] != r["sha256"]: raise ValueError("Conflicting supplement")
            graph[r["path"]] = r["sha256"]
        extract_cache(z, graph, cache)
        files = {name:dict(sha256=pin, bytes=z.getinfo(PREFIX+name).file_size) for name,pin in sorted(graph.items())}
        jobs = [dict(job_id="support", kind="support", entry="c5_support_one.py", arguments=[],
                     expected_protocols=["support_v1", "support_v2", "support_A0_v1"], rows=[9,9,1]),
                dict(job_id="high", kind="high", entry="c5_high_one.py", arguments=[],
                     variants=[dict(name=r[0], rows=r[3], controls=r[4]) for r in high.VARIANTS]),
                dict(job_id="owncaps", kind="owncaps", entry="c5_owncaps_one.py", arguments=[],
                     variants=["owncaps5_v3","owncap_B3_ext_v1"], coarse_strips=87, coarse_controls=24,
                     required_supported_controls=[10,10], extended_B3_strips=4)]
        for job in plan.JOBS:
            info = plan.inspect_job(cache, graph, job, include_sources=True)
            row = dict(job_id=job.job_id, kind=job.kind, entry="c5_initial_one.py" if job.kind=="initial" else "c5_resources_one.py",
                       arguments=["--job",job.job_id], selection=plan.description(job), source_selection=info)
            if job.kind == "initial":
                row["negative_controls"] = initial.control_names((cache/job.directory/"replay.py").read_text())
            jobs.append(row)
        index_raw = z.read(INDEX)
        if hashlib.sha256(index_raw).hexdigest() != INDEX_SHA: raise ValueError("Pinned count selection")
        count_rows, counts = json.loads(index_raw)["count_acceptances"], []
        for ordinal, row in enumerate(count_rows):
            prefix = row["cwd"]+"/"
            source_files = {name[len(prefix):]:pin for name,pin in graph.items()
                            if name.startswith(prefix) and name != prefix+"COUNT_ACCEPTED.json"}
            if any("/" in name for name in source_files): raise ValueError("Flat count capsule")
            forest = json.loads(z.read(PREFIX+prefix+"COUNT_FOREST.json"))
            accepted = json.loads(z.read(PREFIX+prefix+"COUNT_ACCEPTED.json"))
            checked = census(forest); counts.append(checked)
            if checked["nodes"] != accepted["statistics"]["nodes"] or checked["leaves"] != accepted["statistics"]["leaves"]:
                raise ValueError("Candidate structural census differs from selection metadata")
            jobs.append(dict(job_id="count-%03d"%ordinal, kind="count", entry="c5_count_one.py", arguments=[],
                             index=row["index"], source_capsule=row["cwd"], source_files=source_files,
                             census=checked, expected_status=accepted["status"], negative_controls=accepted["negative_controls"]))
        if (len(counts),sum(c["nodes"]for c in counts),sum(c["leaves"]for c in counts)) != (295,148586,75178):
            raise ValueError("Full selected count census")
        jobs.append(dict(job_id="complement", kind="complement", entry="c5_complement_one.py", arguments=[],
                         strips=41, attempts=42, complete_integrations=2, native_controls=10, independent_fourier_controls=16,
                         independent_support_controls_not_claimed=3))
        own=importlib.import_module("c5_owncaps_one")
        complement=importlib.import_module("c5_complement_one")
        for row in jobs:
            if row["kind"]=="support":
                row["protocols"]=[]
                for name in row["expected_protocols"]:
                    native=json.loads((cache/(high.HIGH_ROOT+name+"/REPLAY_CHECKED.json")).read_text())
                    row["protocols"].append(dict(name=name,status=native["status"],
                        source_files_sha256=native["files_sha256"]))
            elif row["kind"]=="high":
                row["source_files_sha256"]={}
                for variant in row["variants"]:
                    row["source_files_sha256"].update(high.collect_sources(cache,graph,variant["name"]))
                    native=json.loads((cache/(high.HIGH_ROOT+variant["name"]+"/HIGH_CHECKED.json")).read_text())
                    variant.update(status=native["status"],negative_controls=native["negative_controls"],
                                   native_source_keys=sorted({n.replace("\\","/")for n in native["files_sha256"]}))
            elif row["kind"]=="owncaps":
                row["source_files_sha256"]=own.selected_sources(cache,graph)
                row["native_variants"]=[]
                for name in row["variants"]:
                    native=json.loads((cache/(own.HIGH+name+"/OWNCAPS_CHECKED.json")).read_text())
                    row["native_variants"].append(dict(name=name,status=native["status"],
                        negative_controls=native["negative_controls"],native_source_keys=sorted({n.replace("\\","/")for n in native["files_sha256"]})))
            elif row["kind"]=="complement":
                row["source_files_sha256"]=complement.selected_sources(cache,graph)
                native=json.loads((cache/(high.HIGH_ROOT+"complement5_v1/COMPLEMENT_CHECKED.json")).read_text())
                review=json.loads((cache/"work/cutoff5_20261020/audit/complement5_readback_v1/READBACK.json").read_text())
                row["native_negative_controls"]=native["negative_controls"]
                row["independent_fourier_negative_controls"]=[name for name in review["negative_controls"]
                    if name not in ("wrong q","missing support ray","false support polynomial")]
                if len(row["independent_fourier_negative_controls"])!=16:raise ValueError("Exact independent Fourier-only controls")
            elif row["kind"]in("initial","resource"):
                selection=row["selection"];case=cache/selection["directory"]/selection["case"]
                native=json.loads((case/"REPLAY_CHECKED.json").read_text())
                row["native_source_keys"]=sorted({n.replace("\\","/")for n in native["files_sha256"]})
                if row["kind"]=="resource":
                    replay=json.loads((case/"REPLAY.json").read_text())
                    row["native_negative_controls"]=native["negative_controls"]
                    row["replay_negative_controls"]=replay["negative_controls"]
    if len(jobs)!=326 or len({j["job_id"]for j in jobs})!=326: raise ValueError("326 deterministic full jobs")
    catalog = dict(schema="PINNED_N5_REMAINING_ARITHMETIC_CATALOG_V1", archive=dict(name="cutoff5_20261020.zip",
        bytes=ARCHIVE_BYTES,sha256=ARCHIVE_SHA,prefix=PREFIX), final_source_index_sha256=FINAL_SHA,
        count_selection_sha256=INDEX_SHA, supervisory_snapshot_sha256=snapshot,
        source_cache_files=files, source_cache_bytes=sum(r["bytes"]for r in files.values()), jobs=jobs,
        census=dict(jobs=326,initial=12,resources=15,resource_panels=1200,count_forests=295,count_roots=1770,
                    count_nodes=148586,count_leaves=75178),
        historical_receipts="Frozen candidate and conditional-reference/source-selection data only; never fresh acceptance",
        remaining_obligations=["Global unrestricted C4<=CE and common analytic/literature premises",
            "Fresh same-law support/HIGH/owncap-to-INITIAL and INITIAL-to-resource semantic joins",
            "Resource-to-count interfaces, full region composition and notebook13 gapfree result",
            "Three separate independent complement support-corruption controls and parent acquisition"],
        mathematical_kernels_executed=False,full_n5_verified=False,all_index_conclusion_verified=False)
    pin = dump(ROOT / "proof/n5_remaining_catalog.json", catalog, replace=True)
    print(json.dumps(dict(catalog_sha256=pin,snapshot_sha256=snapshot,census=catalog["census"],
                          source_cache_files=len(files),source_cache_bytes=catalog["source_cache_bytes"],
                          mathematical_kernels_executed=False)),flush=True)


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--old-root",type=Path,required=True);p.add_argument("--archive",type=Path,required=True)
    p.add_argument("--cache",type=Path,required=True);a=p.parse_args()
    build(a.old_root,a.archive,a.cache)
