"""Pure byte/JSON/AST reconstruction of thirteen conditional B5 source capsules.

No archived module is imported, compiled, executed or numerically evaluated.
Seven ordinary V14 designs and two mixed-parent designs are new source epochs.
Four p33 contracts/checkers reproduce the selected historical bytes. Neither
kind acquires a parent premise, a forest, a mixed exclusion or an acceptance.
"""
from __future__ import annotations

import ast
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "proof/n25_b5_reconstruction_source_plan.json"
PLAN_SHA256 = "6163a6692afd34403f848100cc647cbbee846f3a51f312847393a7c40338cbc0"
SCHEMA = "N25_B5_RECONSTRUCTION_SOURCE_PLAN_V1"
MANIFEST = "SOURCE_MANIFEST.json"
PREPARATION = "SOURCE_PREPARATION.json"
EPOCH = "B5_RECONSTRUCTION_SOURCE_EPOCH.json"
MIB = 1024**2
MAX_FILE = 16*MIB
MAX_TOTAL = 256*MIB
TARGETS = tuple([f"b5-p{i}-v14-new" for i in range(26, 33)]
                + [f"b5-p33-q{q}-v12-reconstructed" for q in range(4)]
                + [f"b5-p{i}-mixed-parent-v14-new" for i in (24, 25)])
PREMISE = dict(schema="ATTAINED_POSITIVE_CLOSED_CONTACT_V1", sample_size=25,
               same_unrestricted_attained_witness=True,
               positive_closed_threshold=True, score_at_least_CE=True)
STDLIB_IMPORTS = {"collections", "copy", "fractions", "functools", "hashlib",
                  "itertools", "json", "math", "pathlib", "sys", "time", "traceback"}
FALSE_FLAGS = dict(arithmetic_accepted=False, native_acceptance_run=False,
                   parent_acquisitions_verified=False, mixed_exclusion_verified=False,
                   all_index_conclusion_verified=False)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    """Original producers used insertion order, indent2 and a terminal LF."""
    return (json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False)+"\n").encode("utf-8")


def _unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "Duplicate JSON key")
        out[key] = value
    return out


def parsed(raw):
    def invalid(_):
        raise ValueError("Non-finite JSON")
    return json.loads(raw, object_pairs_hook=_unique, parse_constant=invalid)


def _same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    return a == b


def _link(path):
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def _no_link_ancestors(path):
    path = Path(path).absolute()
    need(all(not _link(p) for p in (path, *path.parents)), "No linked source/output ancestor")


def _regular(path, limit=MAX_FILE):
    path = Path(path)
    need(path.is_file() and not _link(path) and path.stat().st_size <= limit,
         "Bounded regular input: "+str(path.name))
    return path.read_bytes()


def _flat(name):
    need(type(name) is str and name and name not in (".", "..")
         and not any(c in name for c in "/\\:\x00") and name == name.rstrip(" .")
         and not re.fullmatch(r"(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", name, re.I),
         "Safe flat capsule filename")
    return name


def _member(name, directory=False):
    need(type(name) is str and name and "\\" not in name and ":" not in name
         and "\x00" not in name and not PurePosixPath(name).is_absolute(),
         "Safe archive-relative member")
    parts = name[:-1].split("/") if directory and name.endswith("/") else name.split("/")
    need(all(p and p not in (".", "..") and p == p.rstrip(" .") for p in parts),
         "No traversal or ambiguous archive member")
    for part in parts:
        _flat(part)
    return name


def _pin(row):
    need(type(row) is dict and row.get("archive_key") in ("old", "base13")
         and type(row.get("bytes")) is int and 0 <= row["bytes"] <= MAX_FILE
         and type(row.get("sha256")) is str
         and re.fullmatch("[0-9a-f]{64}", row["sha256"]) is not None,
         "Typed exact source member pin")
    _member(row["member"])
    return row


def _plan():
    raw = _regular(PLAN, 8*MIB)
    need(sha(raw) == PLAN_SHA256, "Externally pinned B5 reconstruction plan")
    plan = parsed(raw)
    need(plan["schema"] == SCHEMA and tuple(plan["profiles"]) == TARGETS
         and all(plan[k] is False for k in FALSE_FLAGS),
         "Exactly thirteen source-only targets and false proof flags")
    need(set(plan["archives"]) == {"old", "base13"}, "Two fixed source archives")
    for row in plan["inputs"].values():
        _pin(row)
    for target, spec in plan["profiles"].items():
        need(spec["target"] == target and spec["index"] in range(24, 34)
             and type(spec["index"]) is int and spec["n"] == 25
             and all(spec[k] is False for k in FALSE_FLAGS),
             "Literal conditional source profile")
        need(type(spec["output_files"]) is dict and spec["output_files"]
             and "FROZEN_DESIGN.json" in spec["output_files"], "Sealed derived capsule")
        for name, pin in spec["output_files"].items():
            _flat(name)
            need(type(pin["bytes"]) is int and 0 <= pin["bytes"] <= MAX_FILE
                 and re.fullmatch("[0-9a-f]{64}", pin["sha256"]) is not None,
                 "Typed output pin")
    return plan


def profiles():
    return deepcopy(_plan()["profiles"])


def profile(target):
    need(type(target) is str and target in TARGETS, "Unknown B5 reconstruction target")
    return deepcopy(_plan()["profiles"][target])


def _input_key(key, member):
    return key+":"+member


def _archives(plan, paths):
    """Validate transport and every ZIP name before returning open archives."""
    need(type(paths) is dict and set(paths) == set(plan["archives"]), "Both exact archive paths required")
    opened = {}
    try:
        for key, asset in plan["archives"].items():
            path = Path(paths[key])
            need(path.is_file() and not _link(path) and path.stat().st_size == asset["bytes"],
                 "Exact bounded archive transport size")
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(MIB), b""):
                    digest.update(block)
            need(digest.hexdigest() == asset["sha256"], "Exact complete archive SHA256")
            z = zipfile.ZipFile(path)
            opened[key] = z
            seen = set()
            for info in z.infolist():
                _member(info.filename, directory=info.is_dir())
                folded = info.filename.rstrip("/").casefold()
                need(folded not in seen, "Duplicate or case-colliding ZIP member")
                seen.add(folded)
                kind = stat.S_IFMT(info.external_attr >> 16)
                need(kind not in (stat.S_IFLNK, stat.S_IFCHR, stat.S_IFBLK, stat.S_IFIFO, stat.S_IFSOCK),
                     "No ZIP symlink or special member")
        return opened
    except BaseException:
        for z in opened.values():
            z.close()
        raise


def _read_inputs(plan, paths):
    zs = _archives(plan, paths)
    result = {}
    try:
        for key, row in plan["inputs"].items():
            _pin(row)
            need(key == _input_key(row["archive_key"], row["member"]), "Literal source-key identity")
            info = zs[row["archive_key"]].getinfo(row["member"])
            need(not info.is_dir() and stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG)
                 and info.file_size == row["bytes"] and not info.flag_bits & 1,
                 "Bounded unencrypted selected regular member")
            raw = zs[row["archive_key"]].read(info)
            need(sha(raw) == row["sha256"], "Exact selected source SHA256: "+row["member"])
            result[key] = raw
    finally:
        for z in zs.values():
            z.close()
    need(sum(map(len, result.values())) <= MAX_TOTAL, "Bounded complete in-memory input set")
    return result


def _raw(inputs, row):
    raw = inputs[_input_key(row["archive_key"], row["member"])]
    need(len(raw) == row["bytes"] and sha(raw) == row["sha256"], "Exact selected in-memory source")
    return raw


def _replace(source, before, after):
    need(source.count(before) == 1, "One exact reviewed native literal transform: "+before[:60])
    return source.replace(before, after, 1)


def _functions(source):
    tree = ast.parse(source)
    result = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            need(node.name not in result, "No duplicate native function")
            result[node.name] = node
    return result


def _projection(before, after, old_status, new_status):
    old, new = _functions(before), _functions(after)
    need(set(old) == set(new), "All native function names retained")
    for name in set(old)-{"load", "header", "accept"}:
        need(ast.dump(old[name]) == ast.dump(new[name]), "Unchanged native function: "+name)
    # The full acceptance function, including every original control, differs
    # only in its honest new terminal status. No original mathematical call runs.
    for node in ast.walk(old["accept"]):
        if isinstance(node, ast.Constant) and node.value == old_status:
            node.value = new_status
    need(ast.dump(old["accept"]) == ast.dump(new["accept"]), "Native accept changes only its output identity")
    mutations = [n.value for n in ast.walk(new["accept"]) if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == "mutations" for t in n.targets)]
    need(len(mutations) == 1 and isinstance(mutations[0], ast.List) and len(mutations[0].elts) == 24,
         "All24 original native corruption controls retained")


def _v14_protocol(original, index, schema, status, reference_name, recovered=False):
    source = original.decode("utf-8")
    old_schema = (f"LOW25_B5_GLOBAL_LOCAL_CONTACT_V14_PANEL{index}_RIGHT_HALF_CLOSED_COUNT_FOREST_V1"
                  if recovered else f"LOW25_B5_GLOBAL_ALPHA_STOPLOSS2_V12_PANEL{index}_RIGHT_HALF_CLOSED_COUNT_FOREST_V1")
    after = source
    if not recovered:
        after = _replace(after, "from rho_signed_moment_tightener import cell35",
                         "from local_contact_v14 import cell35\nfrom local_contact_support import validate_premise")
    else:
        need("from local_contact_v14 import cell35,validate_premise" in after,
             "Exact recovered mixed-parent evaluator import")
    guard = "\n original=json.loads((HERE/"+repr(reference_name)+").read_text(),object_pairs_hook=unique)"
    guard += "\n expected=deepcopy(original['rows'][0])"
    guard += "\n expected.update(local_contact_allowance='5/16',local_contact_premise="+repr(PREMISE)+")"
    guard += "\n need(same(contract,dict(original,rows=[expected])),'exact whole original physical contract plus two contact fields')"
    if not recovered:
        guard += "\n validate_premise(cfg)"
    after = _replace(after, " cfg=contract['rows'][0]", " cfg=contract['rows'][0]"+guard)
    after = _replace(after, old_schema, schema)
    old_status = f"PASS_FRESH_CONDITIONAL_EXACT_COUNT{index}"
    after = _replace(after, old_status, status)
    _projection(source, after, old_status, status)
    need("LIMIT=10000" in after and "depth<=128" in after
         and "F(z['score_upper'])<CE_LO" in after, "Original finite profile and strict target")
    return after.encode("utf-8")


def _quarter(contract_raw, protocol_raw, quarter):
    parent = parsed(contract_raw)
    original = parent["rows"][0]
    need(type(quarter) is int and quarter in range(4) and original["index"] == 33,
         "Exactly a p33 closed quarter")
    lo, hi = map(Fraction, original["p"])
    cfg = deepcopy(original)
    cfg["p"] = [str(lo+(hi-lo)*quarter/4), str(lo+(hi-lo)*(quarter+1)/4)]
    contract = deepcopy(parent)
    contract["rows"] = [cfg]
    contract["quarter_partition"] = dict(parent=original["p"], quarter=quarter,
        subpanel=cfg["p"], source_contract_sha256=sha(contract_raw))
    contract["scope"] = ("One closed p quarter. Every physical/scalar/phase guard and full selected cubic kernel stays unchanged. "
        "Four ordered closed quarters cover the original panel; fresh ordinary acceptance and final same-law composition are separate.")
    source = protocol_raw.decode("utf-8")
    source = _replace(source, repr(original["p"]), repr(cfg["p"]))
    source = _replace(source, "LOW25_B5_GLOBAL_ALPHA_STOPLOSS2_V12_", f"LOW25_B5_GLOBAL_ALPHA_STOPLOSS2_V12_Q{quarter}_")
    ast.parse(source)
    return encoded(contract), source.encode("utf-8")


def _recovered_mixed(plan, inputs, index):
    recipe = plan["mixed_recipe"]
    source = _raw(inputs, recipe["template"]).decode("utf-8")
    for before, after in recipe["p25_literal_edits"]:
        source = _replace(source, before, after)
    if index == 24:
        for before, after in recipe["p24_additional_literal_edits"]:
            need(source.count(before) >= 1, "Exact recovered mixed native literal")
            source = source.replace(before, after)
    raw = source.encode("utf-8")
    need(sha(raw) == recipe["recovered_checker_sha256"][str(index)], "Recovered exact historical mixed checker")
    ast.parse(raw)
    return raw


def _imports(payload):
    """Static closure, not a general claim about arbitrary Python execution."""
    active = {n: b for n, b in payload.items() if n.endswith(".py")
              and not n.startswith(("ORIGINAL_", "HISTORICAL_"))}
    modules = {Path(n).stem for n in active}
    edges = []
    for name, raw in sorted(active.items()):
        tree = ast.parse(raw)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                need(node.level == 0, "No unresolved relative mathematical import")
                imports = [(node.module or "").split(".")[0]]
            else:
                imports = []
            for module in imports:
                need(module in modules or module in STDLIB_IMPORTS, "Complete stdlib/local AST import: "+module)
                edges.append([name, module])
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                need(node.func.id not in {"eval", "exec", "compile"}, "No dynamic mathematical source execution")
                if node.func.id == "__import__":
                    need(len(node.args) == 1 and isinstance(node.args[0], ast.Constant)
                         and node.args[0].value == "math" and not node.keywords,
                         "Only the original literal math-factorial dynamic import")
    return edges


def _add(payload, name, raw):
    _flat(name)
    need(name.casefold() not in {n.casefold() for n in payload}
         and type(raw) is bytes and len(raw) <= MAX_FILE, "Unique bounded derived filename")
    payload[name] = raw


def _derive(plan, inputs, target):
    """Deterministic memory-only transform; original code is never called."""
    spec = plan["profiles"][target]
    base = plan["bases"][str(spec["base_index"])]
    original = {n: _raw(inputs, row) for n, row in base["files"].items()}
    design = parsed(_raw(inputs, base["design"]))
    need(design["files"] == {n: sha(b) for n, b in original.items()}, "Complete unchanged original design")
    kernel = parsed(original["KERNEL_COPY_MANIFEST.json"])
    need(len(kernel["files"]) == 71 and all(sha(original[n]) == h for n, h in kernel["files"].items()),
         "All71 original kernel/proof bytes")
    payload = {}
    for name in kernel["files"]:
        _add(payload, name, original[name])
    mixed = spec["kind"] == "mixed-parent-v14"
    constructor = (_raw(inputs, plan["mixed_recipe"]["panels"][str(spec["index"])]["constructor"])
                   if mixed else original["construct_alpha4.py"])
    _add(payload, "construct_alpha4.py", constructor)
    for name in ("SOURCE_PORT.json", "count_protocol.py", "contract.json", "KERNEL_COPY_MANIFEST.json"):
        _add(payload, "ORIGINAL_V12_"+("CONTRACT.json" if name == "contract.json" else name), original[name])
    _add(payload, "ORIGINAL_V12_FROZEN_DESIGN.json", _raw(inputs, base["design"]))
    reference_name = "ORIGINAL_V12_CONTRACT.json"
    reference = original["contract.json"]
    recovered = None
    provenance = {}
    if mixed:
        physical = plan["mixed_recipe"]["panels"][str(spec["index"])]
        reference = _raw(inputs, physical["base_contract"])
        reference_name = "ORIGINAL_PHYSICAL_CONTRACT.json"
        _add(payload, reference_name, reference)
        need(_same(parsed(reference)["rows"][0], physical["base_original_cfg"]), "Exact mixed physical reference row")
        recovered = _recovered_mixed(plan, inputs, spec["index"])
        _add(payload, "HISTORICAL_NATIVE_CHECKER_REFERENCE.py", recovered)
        _add(payload, "HISTORICAL_NATIVE_HEADER_REFERENCE.json", encoded(physical["expected_native_header"]))
        provenance["HISTORICAL_MIXED_ACCEPTANCE_REFERENCE.json"] = _raw(inputs, physical["historical_acceptance"])
    contract = deepcopy(parsed(reference))
    need(len(contract["rows"]) == 1 and type(contract["rows"][0]["n"]) is int
         and contract["rows"][0]["n"] == 25 and contract["rows"][0]["index"] == spec["index"],
         "Literal complete physical contract")
    if spec["kind"] == "quarter-v12":
        contract_raw, protocol = _quarter(reference, original["count_protocol.py"], spec["quarter"])
        need(sha(contract_raw) == spec["historical_contract_sha256"]
             and sha(protocol) == spec["historical_checker_sha256"], "Exact recovered selected quarter inputs")
        manifest_raw = original["KERNEL_COPY_MANIFEST.json"]
    else:
        contract["rows"][0].update(local_contact_allowance="5/16", local_contact_premise=deepcopy(PREMISE))
        contract_raw = encoded(contract)
        if mixed:
            need(_same(contract["rows"][0], plan["mixed_recipe"]["panels"][str(spec["index"])]["mixed_original_cfg"]),
                 "Exact mixed original row plus two explicit premises")
        protocol = _v14_protocol(recovered if mixed else original["count_protocol.py"], spec["index"],
            spec["native_schema"], spec["native_status"], reference_name, recovered=mixed)
        helper_manifest = parsed(_raw(inputs, plan["helpers"]["manifest"]))
        need(len(helper_manifest["files"]) == 21, "Exactly21 unchanged combined V14 additions")
        for name, row in plan["helpers"]["files"].items():
            b = _raw(inputs, row)
            need(helper_manifest["files"][name] == sha(b), "Exact original combined addition manifest")
            _add(payload, name, b)
        _add(payload, "LOCAL_CONTACT_V14_ADDITIONS.json", _raw(inputs, plan["helpers"]["manifest"]))
        for name, row in plan["analytic_inputs"].items():
            _add(payload, name, _raw(inputs, row))
        manifest_raw = None
    _add(payload, "contract.json", contract_raw)
    _add(payload, "count_protocol.py", protocol)
    epoch = dict(schema="N25_B5_RECONSTRUCTED_SOURCE_EPOCH_V1", target=target,
        kind=spec["kind"], index=spec["index"], original_design_sha256=base["design"]["sha256"],
        physical_reference_contract_sha256=sha(reference), new_contract_sha256=sha(contract_raw),
        new_checker_sha256=sha(protocol), original71_kernel_files=kernel["files"],
        new_native_schema=spec["native_schema"], new_native_status=spec["native_status"],
        requires_new_mixed_metadata_adapter=mixed,
        old_source_inputs_sha256=parsed(reference).get("source_inputs_sha256", {}),
        scope="Source reconstruction only. Original parent identities are provenance, never fresh acquisition. "
              "An ordinary count parent capsule is not a mixed exclusion or an accepted forest.", **FALSE_FLAGS)
    _add(payload, EPOCH, encoded(epoch))
    if manifest_raw is None:
        manifest_raw = encoded(dict(files={n: sha(b) for n, b in payload.items()
            if n not in {"contract.json", "count_protocol.py"}},
            origin="NEW_CONDITIONAL_B5_RECONSTRUCTION_NOT_HISTORICAL_NATIVE_IDENTITY",
            scope="All93 original V12/combined-V14 files are unchanged; additional original references and analytic premises are source-bound, not acquired."))
    _add(payload, "KERNEL_COPY_MANIFEST.json", manifest_raw)
    _imports(payload)
    _add(payload, "FROZEN_DESIGN.json", encoded(dict(
        schema="NEW_B5_RECONSTRUCTION_SOURCE_DESIGN_V1", files={n: sha(b) for n, b in payload.items()},
        original_design_acceptance_claimed=False, **FALSE_FLAGS)))
    need(sum(map(len, payload.values())) <= MAX_TOTAL, "Bounded derived source capsule")
    return payload, provenance


def _file_rows(payload):
    return {name: dict(bytes=len(raw), sha256=sha(raw)) for name, raw in sorted(payload.items())}


def _selection(targets):
    chosen = list(TARGETS if targets is None else targets)
    need(chosen and len(set(chosen)) == len(chosen)
         and all(type(t) is str and t in TARGETS for t in chosen), "Unique known B5 source targets")
    return [t for t in TARGETS if t in chosen]


def _derive_selected(plan, inputs, chosen):
    result = {}
    for target in chosen:
        payload, provenance = _derive(plan, inputs, target)
        spec = plan["profiles"][target]
        need(_file_rows(payload) == spec["output_files"]
             and _file_rows(provenance) == spec["provenance_files"], "Externally pinned complete derived output: "+target)
        result[target] = (payload, provenance)
    return result


def prepare(output, *, archives, targets=None):
    """Verify both archives and derive every selected byte before any write."""
    output = Path(output).absolute()
    _no_link_ancestors(output)
    need(not output.exists() and not _link(output), "Exclusive new source task; no overwrite")
    parent = output.parent
    while not parent.exists():
        parent = parent.parent
    need(parent.is_dir() and not _link(parent), "Regular source task parent")
    plan = _plan()
    chosen = _selection(targets)
    inputs = _read_inputs(plan, archives)
    built = _derive_selected(plan, inputs, chosen)
    manifest = dict(schema="N25_B5_RECONSTRUCTED_SOURCES_V1", source_plan_sha256=PLAN_SHA256,
        targets=chosen, capsules={t: plan["profiles"][t]["output_files"] for t in chosen},
        provenance={t: plan["profiles"][t]["provenance_files"] for t in chosen}, **FALSE_FLAGS)
    report = dict(schema="N25_B5_RECONSTRUCTION_PREPARATION_V1", source_plan_sha256=PLAN_SHA256,
        source_builder_sha256=sha(Path(__file__).read_bytes()), selected_targets=chosen,
        source_manifest_sha256=sha(encoded(manifest)), source_archive_pins=plan["archives"],
        original_modules_imported=False, original_code_executed=False, **FALSE_FLAGS)
    output.mkdir(parents=True, exist_ok=False)
    for target, (payload, provenance) in built.items():
        folder = output/"capsules"/target
        folder.mkdir(parents=True, exist_ok=False)
        for name, raw in payload.items():
            with (folder/name).open("xb") as stream:
                stream.write(raw)
        if provenance:
            dest = output/"provenance"/target
            dest.mkdir(parents=True, exist_ok=False)
            for name, raw in provenance.items():
                with (dest/name).open("xb") as stream:
                    stream.write(raw)
    for name, value in ((MANIFEST, manifest), (PREPARATION, report)):
        with (output/name).open("xb") as stream:
            stream.write(encoded(value))
    verify(output)
    return report


def _check_folder(folder, rows):
    _no_link_ancestors(folder)
    need(folder.is_dir() and not _link(folder), "Regular sealed source folder")
    need({p.name for p in folder.iterdir()} == set(rows), "Exact source-only inventory; no forest or acceptance output")
    payload = {}
    for name, row in rows.items():
        raw = _regular(folder/_flat(name))
        need(len(raw) == row["bytes"] and sha(raw) == row["sha256"], "Exact sealed source bytes: "+name)
        payload[name] = raw
    return payload


def verify_capsule(target, capsule):
    spec = profile(target)
    payload = _check_folder(Path(capsule), spec["output_files"])
    design = parsed(payload["FROZEN_DESIGN.json"])
    need(design["files"] == {n: sha(b) for n, b in payload.items() if n != "FROZEN_DESIGN.json"}
         and all(design[k] is False for k in FALSE_FLAGS)
         and design["original_design_acceptance_claimed"] is False, "Honest complete new source design")
    epoch = parsed(payload[EPOCH])
    need(epoch["target"] == target and all(epoch[k] is False for k in FALSE_FLAGS), "Source epoch cannot promote acceptance")
    _imports(payload)
    return spec


def verify(task):
    task = Path(task)
    need(task.is_dir() and not _link(task), "Regular source task")
    plan = _plan()
    manifest = parsed(_regular(task/MANIFEST, 8*MIB))
    chosen = _selection(manifest["targets"])
    expected = dict(schema="N25_B5_RECONSTRUCTED_SOURCES_V1", source_plan_sha256=PLAN_SHA256,
        targets=chosen, capsules={t: plan["profiles"][t]["output_files"] for t in chosen},
        provenance={t: plan["profiles"][t]["provenance_files"] for t in chosen}, **FALSE_FLAGS)
    need(_same(manifest, expected), "Exact immutable source task manifest and false proof flags")
    expected_top = {"capsules", MANIFEST, PREPARATION}
    mixed = {t for t in chosen if expected["provenance"][t]}
    if mixed:
        expected_top.add("provenance")
    need({p.name for p in task.iterdir()} == expected_top
         and (task/"capsules").is_dir() and not _link(task/"capsules")
         and {p.name for p in (task/"capsules").iterdir()} == set(chosen), "Exact selected source task tree")
    for target in chosen:
        verify_capsule(target, task/"capsules"/target)
    if mixed:
        need((task/"provenance").is_dir() and not _link(task/"provenance")
             and {p.name for p in (task/"provenance").iterdir()} == mixed,
             "Separate exact historical mixed-reference inventory")
        for target in mixed:
            _check_folder(task/"provenance"/target, expected["provenance"][target])
    preparation = parsed(_regular(task/PREPARATION))
    need(preparation["schema"] == "N25_B5_RECONSTRUCTION_PREPARATION_V1"
         and preparation["source_builder_sha256"] == sha(Path(__file__).read_bytes())
         and preparation["source_plan_sha256"] == PLAN_SHA256
         and preparation["selected_targets"] == chosen
         and preparation["source_manifest_sha256"] == sha(encoded(manifest))
         and preparation["source_archive_pins"] == plan["archives"]
         and preparation["original_modules_imported"] is False
         and preparation["original_code_executed"] is False
         and all(preparation[k] is False for k in FALSE_FLAGS), "Bound source-only preparation report")
    return manifest
