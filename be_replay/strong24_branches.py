"""Full conditional auxiliary-n24 arithmetic, one literal rho branch per job.

Unchanged acceptors replay archived proof/forest data as untrusted candidates.
No historical acceptance is copied. BASIC process-tree supervision is explicit;
analytic acquisition and the final C24 theorem remain separate obligations.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from fractions import Fraction
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import traceback
import uuid
import zipfile

MIB = 1024**2
PREFIX = "cutoff25_20261011/"
X10 = "continuation_20261010/local24/"
X11 = "continuation_20261011/stronger24/"
PREDECESSOR_SHA = "8871835341669078aa1a25b62e95ad7e8342dffae794c8d0cd7faf8032d4d563"
BRANCHES = {
    "b0": dict(rho=["1", "11/10"], counts=list(range(37, 49)), leaves=1929,
               contract="743dc16999e84c5473568d6c150792d2f0124c846e2eafd5a08fb8bd74412b36"),
    "b1": dict(rho=["11/10", "6/5"], counts=list(range(32, 41)), leaves=9803,
               contract="1ff58ab4a456adb38fca1646339ae11c6930a4590eca248006aad916d9073759"),
    "b2": dict(rho=["6/5", "13/10"], counts=list(range(28, 37)), leaves=26625,
               contract="deb00c596a775a4fac6504e1c46e49f07b90161e6954a073d3d49b6c7527da94"),
    "b3": dict(rho=["13/10", "7/5"], counts=list(range(25, 33)), leaves=12484,
               contract="f61e40293ec51e51614b283fd80786086856f2bdc9dfa74fcbbf7b8094987ad3",
               local=list(range(25, 36))),
    "b4": dict(rho=["7/5", "3/2"], counts=list(range(23, 31)), leaves=4168,
               contract="b3313b8cf8224903137d2ae16501cc60dc46e60d51aecde8d720533a94072b15",
               local=list(range(22, 37))),
    "b5": dict(rho=["3/2", "712569/449000"], counts=list(range(21, 28)), leaves=2444,
               contract="2454b8b052a652ba88c4b4bc2e885e5efbbb69763cdd8e3be51ec2b2bbf9f8f9",
               local=list(range(21, 35))),
}
PATCH_CONTRACT = "b0ce1a7c120de2f430bf9306d004f300a2d946d8fc5a0e0c7fd8b3bbbfb9b85a"
EFFECTIVE_Q = {"b0":"15/46", "b1":"15/46", "b2":"15/46", "b3":"15/46",
               "b4":"12351561/43750000", "b5":"746553/6250000"}
SELECTION_SHA = {
    "b0": "1539323aa87d522f4bd743ac69c24e21ddd45e95d6110e78c79a56e073c7869c",
    "b1": "15a6c47bad552cc82e19e916b16751e8d78b2bd9734eab404af3a5773f798ddc",
    "b2": "11912b7385309712b668138b0e99f6c6bdb1ada224980c9fb0907da404318d84",
    "b3": "958aa4b834dad6e0cf3c52fff2e069b4b856838a115a5c0b20e08f8b3ed57bd2",
    "b4": "7fd571fd460435729147a18bf3cbdcdc840851c87696484fea50eafcb7b2d5cf",
    "b5": "1a35c6825616cffa154918205ab8c9f4e67de083877c91a3f92dc4ed739979ec",
}
PREMISES = [
    "Conditional predecessor C23 < C_E+3/115; archived statement is not fresh acquisition",
    "Retained unrestricted attainment, same-law contact/support, INITIAL/resource/count implications",
    "The external envelopes and implementation-review inputs explicitly bound by the native source manifests",
]


def need(value, message):
    if not value:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON field")
        result[key] = value
    return result


def sha(path):
    out = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(MIB), b""):
            out.update(block)
    return out.hexdigest()


def read(path, maximum=128*MIB):
    path = Path(path)
    need(path.is_file() and not path.is_symlink() and path.stat().st_size <= maximum,
         "Bounded ordinary JSON artifact: " + path.name)
    return json.loads(path.read_text("utf-8"), object_pairs_hook=unique)


def relative(name):
    need(type(name) is str and name and not any(x in name for x in ("\\", ":", "\x00")),
         "Portable relative source name")
    need(all(x not in ("", ".", "..") for x in name.split("/")), "Contained relative source path")
    return name


def locations(branch):
    need(branch in BRANCHES, "Literal stronger24 branch b0 through b5")
    if branch in ("b0", "b1", "b2"):
        initial = X10 + ("exact_b2_common_v1" if branch == "b2" else "exact_" + branch)
        original = X10 + ("resource_b2_common_v1" if branch == "b2" else "resource_" + branch)
        resource = X10 + ("resource_b2_common_fixedpoint_v1" if branch == "b2" else "resource_" + branch + "_fixedpoint_v1")
        validation = resource.replace("_v1", "_validation")
        return dict(initial=initial, resource=resource, original=original, validation=validation,
                    count=X10+"count_"+branch)
    return dict(initial=X11+branch+"_initial_exact_v1", resource=X11+branch+"_resource_exact_v1",
                local=X11+branch+("_mixed_feedback_selected_exact_v1" if branch == "b3" else "_mixed_feedback_exact_v1"),
                composition=X11+branch+("_composition_selected_v2" if branch == "b3" else "_composition_v1"),
                count=X11+branch+("_count_wave1_conditional_v1" if branch in ("b4", "b5") else "_count_conditional_v1"))


def count_jobs(branch):
    p = locations(branch)
    return [(X10+"count_b2_meanfloor_patch_v1" if branch == "b2" and i >= 33 else p["count"], i)
            for i in BRANCHES[branch]["counts"]]


def _archive_json(archive, name):
    info = archive.getinfo(PREFIX+relative(name))
    need(not info.is_dir() and info.file_size <= 128*MIB, "Bounded selected archive JSON")
    return json.loads(archive.read(info), object_pairs_hook=unique)


def selected_members(archive_path, branch):
    """Select exact immutable source closures and candidates; never old outputs."""
    p = locations(branch)
    members = {}
    with zipfile.ZipFile(archive_path) as archive:
        available = set(archive.namelist())
        def add(name, kind="source"):
            name = relative(name)
            full = PREFIX+name
            need(full in available, "Supplied exact source member: " + name)
            need(not PurePosixPath(name).name.lower().startswith("accepted_") and
                 not PurePosixPath(name).name.upper().endswith("_ACCEPTED.JSON"),
                 "Historical acceptance is not a new source input")
            if full in members:
                need(members[full] == kind, "Consistent selected member classification")
            members[full] = kind

        def manifest(folder, filename):
            obj = _archive_json(archive, folder+"/"+filename)
            files = obj.get("files", obj)
            need(type(files) is dict and files, "Nonempty exact source manifest")
            add(folder+"/"+filename)
            for name, pin in files.items():
                need(PurePosixPath(relative(name)).name == name and type(pin) is str and len(pin) == 64,
                     "Flat pinned native manifest")
                raw = archive.read(PREFIX+folder+"/"+name)
                need(hashlib.sha256(raw).hexdigest() == pin, "Original archive manifest source binding")
                # These static JSON objects are retained source/review statements,
                # never evidence that their historical numerical run passed now.
                kind = "premise" if name.endswith(".json") and name not in (
                    "contract.json", "count_contract.json", "INPUT_DESIGN.json", "COPY_MANIFEST.json",
                    "FROZEN_SOURCES.json", "ORIGINAL_FROZEN_SOURCES.json", "contract24_"+branch+".json") else "source"
                add(folder+"/"+name, kind)

        manifest(p["initial"], "COPY_MANIFEST.json")
        manifest(p["resource"], "FROZEN_SOURCES.json")
        upper = branch.upper()
        add(p["initial"]+"/POSITIVE24_"+upper+"_INITIAL_PROOF.json", "candidate")
        add(p["resource"]+("/resources24_"+branch+"_proof.json" if branch in ("b0", "b1", "b2")
                             else "/RESOURCE_"+upper+"_GLOBAL_PROOF.json"), "candidate")
        if branch in ("b0", "b1", "b2"):
            manifest(p["original"], "FROZEN_SOURCES.json")
            add(p["validation"]+"/compare.py")
        if branch == "b2":
            manifest(X10+"b2_meanfloor_local_exact_v1", "COPY_MANIFEST.json")
            manifest(X10+"resource_b2_meanfloor_patch_v1", "FROZEN_SOURCES.json")
            add(X10+"b2_meanfloor_local_exact_v1/LOCAL_B2_MEANFLOOR_PROOF.json", "candidate")
            add(X10+"resource_b2_meanfloor_patch_v1/RESOURCE_B2_MEANFLOOR_PROOF.json", "candidate")
        if branch in ("b3", "b4", "b5"):
            manifest(p["local"], "FROZEN_SOURCES.json")
            manifest(p["composition"], "FROZEN_SOURCES.json")
            for i in BRANCHES[branch]["local"]:
                add(p["local"]+f"/PANEL_{i}_PROOF.json", "candidate")
        for folder, i in count_jobs(branch):
            historical = _archive_json(archive, folder+f"/accepted_strict_{i}.json")
            need(historical["contract_sha256"] == (PATCH_CONTRACT if branch == "b2" and i >= 33
                                                     else BRANCHES[branch]["contract"]), "Selected exact count contract")
            for name, pin in historical["source_sha256"].items():
                need(PurePosixPath(relative(name)).name == name, "Flat original count source")
                raw = archive.read(PREFIX+folder+"/"+name)
                need(hashlib.sha256(raw).hexdigest() == pin, "Archived count receipt selects exact source bytes")
                add(folder+"/"+name, "premise" if name.endswith(".json") and name != "contract.json" else "source")
            add(folder+f"/candidate_{i}.json", "candidate")
            # Isolated source inspection uses this original frozen source map.
            if branch in ("b3", "b4", "b5"):
                add(folder+"/COPY_MANIFEST.json")
    return members


def prepare(branch, archives, output, *, download=False):
    from . import aux24_sources as source
    archive = source.archive(archives, download=download)
    members = selected_members(archive, branch)
    task = source.prepare(output, archives=archives, members=members, download=download)
    need(sha(Path(task)/"SOURCES.json") == SELECTION_SHA[branch], "Independent pinned exact branch source/candidate selection")
    from .colab_batch import atomic_json
    atomic_json(Path(task)/"BRANCH.json", dict(schema="CONDITIONAL_STRONG24_BRANCH_TASK_V1", branch=branch,
                driver_sha256=sha(__file__), manifest_sha256=SELECTION_SHA[branch],
                conditional_premises=PREMISES, predecessor_acquired=False))
    return Path(task)


def _stage(name, folder, script, args=(), *, receipt=None, proof=None, kind="numeric", index=None):
    return dict(name=name, folder=folder, script=script, args=list(args), receipt=receipt,
                proof=proof, kind=kind, index=index)


def stages(branch):
    p, u = locations(branch), branch.upper()
    result = [_stage("initial-accept", p["initial"], "initial24_"+branch+".py", ["accept"],
                     receipt="POSITIVE24_"+u+"_INITIAL_ACCEPTED.json", proof="POSITIVE24_"+u+"_INITIAL_PROOF.json", kind="initial")]
    if branch in ("b0", "b1", "b2"):
        result += [_stage("resource-accept", p["resource"], "accept_resources24_"+branch+".py",
                          receipt="RESOURCES24_"+u+"_ACCEPTED.json", proof="resources24_"+branch+"_proof.json", kind="resource"),
                   _stage("fixedpoint-complete-objects", p["validation"], "compare.py",
                          receipt="FIXEDPOINT24_COMPLETE_OBJECTS_CHECKED.json", kind="equivalence")]
        if branch == "b2":
            result += [_stage("local-meanfloor-accept", X10+"b2_meanfloor_local_exact_v1", "local_initial.py", ["accept"],
                              receipt="LOCAL_B2_MEANFLOOR_ACCEPTED.json", proof="LOCAL_B2_MEANFLOOR_PROOF.json", kind="local_b2"),
                       _stage("local-resource-accept", X10+"resource_b2_meanfloor_patch_v1", "resource_patch.py", ["accept"],
                              receipt="RESOURCE_B2_MEANFLOOR_ACCEPTED.json", proof="RESOURCE_B2_MEANFLOOR_PROOF.json", kind="patch")]
    else:
        result.append(_stage("resource-accept", p["resource"], "resources_"+branch+".py", ["accept"],
                             receipt="RESOURCE_"+u+"_GLOBAL_ACCEPTED.json", proof="RESOURCE_"+u+"_GLOBAL_PROOF.json", kind="resource"))
        for i in BRANCHES[branch]["local"]:
            result.append(_stage(f"local-p{i}-accept", p["local"], "mixed_b3_selected.py" if branch == "b3" else "mixed_"+branch+".py",
                                 ["accept", str(i)], receipt=f"PANEL_{i}_ACCEPTED.json", proof=f"PANEL_{i}_PROOF.json", kind="local", index=i))
        result += [_stage("local-all-p-join", p["local"], "join_panels.py", receipt=u+"_FINITE_FEEDBACK_ACCEPTED.json",
                          proof=u+"_FINITE_FEEDBACK_PROOF.json", kind="local_join"),
                   _stage("resource-count-interfaces", p["composition"], "resource_interfaces.py", kind="interfaces")]
    result += [_stage(f"count-p{i}-accept", folder, "accept_strict.py", [str(i)],
                      receipt=f"accepted_strict_{i}.json", proof=f"candidate_{i}.json", kind="count", index=i)
               for folder, i in count_jobs(branch)]
    # The old B2 contract contains four superseded panels; never join those as
    # the selected route. The new ledger combines five old and four patch rows.
    for folder in dict.fromkeys(folder for folder, i in count_jobs(branch)):
        if branch == "b2" and folder == p["count"]:
            continue
        result.append(_stage("count-join-"+PurePosixPath(folder).name, folder, "join_counts.py", kind="count_join"))
    return result


def rebind_local_candidate(candidate, source_root, branch, *, ledger):
    """Rebind only metadata hashes; retain all archived numerical proof fields."""
    candidate = Path(candidate)
    before = read(candidate)
    need(type(before.get("parent_binding_sha256")) is dict, "Explicit local candidate parent binding map")
    old_map = dict(before["parent_binding_sha256"])
    base = Path(source_root)/("continuation_20261011/stronger24" if branch in ("b3", "b4", "b5") else "continuation_20261010")
    new_map = {}
    changed = {}
    for name, pin in old_map.items():
        path = base/relative(name)
        need(path.is_file() and not path.is_symlink(), "Fresh exact local parent exists")
        actual = sha(path)
        if actual != pin:
            need(branch in ("b3", "b4", "b5") and name == branch+"_resource_exact_v1/RESOURCE_"+branch.upper()+"_GLOBAL_ACCEPTED.json",
                 "Only the fresh timing-bearing resource receipt hash may change")
            changed[name] = dict(archived_sha256=pin, fresh_sha256=actual)
        new_map[name] = actual
    source_hash = sha(candidate)
    after = dict(before, parent_binding_sha256=new_map)
    need({k: v for k, v in before.items() if k != "parent_binding_sha256"} ==
         {k: v for k, v in after.items() if k != "parent_binding_sha256"}, "Numeric local proof is unchanged")
    if changed:
        candidate.write_text(json.dumps(after, indent=2)+"\n", encoding="utf-8")
    from .colab_batch import atomic_json
    packet = dict(schema="UNTRUSTED_LOCAL_CANDIDATE_METADATA_REBIND_V1", branch=branch,
                  original_candidate_sha256=source_hash, derived_candidate_sha256=sha(candidate),
                  modified_field="parent_binding_sha256", changed=changed,
                  numeric_fields_changed=False, arithmetic_accepted=False)
    atomic_json(ledger, packet)
    return packet


def _binding_map(root, mapping, base):
    need(type(mapping) is dict and mapping, "Nonempty actual output source/input binding")
    for name, pin in mapping.items():
        path = (Path(base)/relative(name)).resolve()
        need(path.is_relative_to(Path(root).resolve()) and path.is_file() and not path.is_symlink()
             and sha(path) == pin, "Fresh artifact is bound to current exact input: " + name)


def validate_artifact(root, branch, stage):
    """Validate output-to-input edges after an observed unchanged acceptor run."""
    root = Path(root)
    d = root/stage["folder"]
    kind = stage["kind"]
    if not stage["receipt"]:
        return dict(kind=kind, output_validation="captured_terminal_and_unchanged_sources")
    packet = read(d/stage["receipt"])
    need(type(packet.get("status")) is str and packet["status"].startswith("PASS"), "Explicit complete native output")
    if kind == "count":
        i = stage["index"]
        candidate = read(d/stage["proof"])
        need(packet["status"] == "PASS_CONDITIONAL_ON_UNACQUIRED_RESOURCES" and type(packet.get("n")) is int and
             packet["n"] == 24 and type(packet.get("index")) is int and packet["index"] == i and packet["K"] == "3/10",
             "Literal actual24 conditional count acceptance")
        need(packet["candidate_sha256"] == sha(d/stage["proof"]) and packet["contract_sha256"] == sha(d/"contract.json"),
             "Fresh complete candidate and count contract binding")
        need(packet["contract_sha256"] == (PATCH_CONTRACT if branch == "b2" and i >= 33 else BRANCHES[branch]["contract"]),
             "Selected exact branch contract")
        need(type(packet["all_closed_leaves"]) is int and packet["all_closed_leaves"] == len(candidate["leaves"]) > 0 and
             type(packet["negative_controls"]) is int and packet["negative_controls"] >= 24,
             "Complete native leaf replay and controls")
        need(Fraction(packet["maximum_score"]) < Fraction(packet["target_lower"]) and
             packet["target_lower"] == candidate["target_lower"], "Original exact strict target")
        _binding_map(root, packet["source_sha256"], d)
        return dict(kind=kind, index=i, leaves=packet["all_closed_leaves"], maximum_score=packet["maximum_score"],
                    target_lower=packet["target_lower"], controls=packet["negative_controls"], receipt_sha256=sha(d/stage["receipt"]))
    controls = packet.get("negative_controls", [])
    if kind != "equivalence":
        need(type(controls) is list and len(controls) >= 8 and len(controls) == len(set(controls)), "Complete distinct native controls")
    if stage["proof"]:
        proof = read(d/stage["proof"])
        key = "resource_sha256" if "resource_sha256" in packet else "proof_sha256"
        need(packet[key] == sha(d/stage["proof"]), "Fresh accepted complete proof binding")
        need(packet.get("checker_sha256", packet.get("acceptor_sha256")) == sha(d/stage["script"]),
             "Same fixed native checker bound by acceptance")
        if "profile" in packet:
            need(packet["profile"] == proof["profile"] and type(packet["profile"]["n"]) is int and
                 packet["profile"]["n"] == 24 and packet["profile"]["barrier"] == "3/10",
                 "Same actual-index/barrier proof and acceptance profile")
    if kind == "initial":
        need(packet.get("signed_rectangles") == 165888 and packet.get("probability_panels") == 100 and
             len(proof.get("stages", [])) == 8 and len(proof["export"]["panels"]) == 100,
             "All nine complete INITIAL covers and 100 closed probability panels")
        need(proof["predecessor_sha256"] == PREDECESSOR_SHA and proof["support"]["q"] == EFFECTIVE_Q[branch],
             "Explicit conditional predecessor and contact allowance")
        if branch in ("b4", "b5"):
            need(proof["support"]["global_predecessor_allowance"] == "15/46" and
                 Fraction(proof["support"]["q"]) == min(Fraction("15/46"),Fraction(proof["support"]["same_law_allowance"])),
                 "Preserve the stronger effective same-law allowance and global predecessor input")
        for j, row in enumerate(proof["export"]["panels"]):
            need(row["pl"] == str(Fraction(j,100)) and row["pu"] == str(Fraction(j+1,100)) and
                 [row["rho_lo"],row["rho_branch_upper"]] == BRANCHES[branch]["rho"], "Complete literal closed domain")
        for cover in [x["cover"] for x in proof["stages"]]+[proof["export"]]:
            need(type(cover["total"]) is int and cover["total"] == 18432 and
                 cover["active"]+cover["excluded"] == 18432, "Every signed INITIAL rectangle accounted")
        _binding_map(root, packet["source_sha256"], d)
        need(packet["source_sha256"] == proof["source_sha256"], "Same INITIAL proof/acceptance source closure")
    elif kind == "equivalence":
        need(packet["status"] == "PASS_FRESH_COMPLETE_N24_RESOURCE_DICTIONARY_EQUALITY" and
             packet.get("complete_objects_equal") == 3 and len(packet["indices"]) == 3, "Complete original/fixed-point object comparison")
        for folder, mapping in packet["source_sha256"].items():
            _binding_map(root, mapping, d.parent/folder)
    elif kind in ("resource", "local_join", "patch"):
        survivors, excluded = packet["surviving_panels"], packet["excluded_panels"]
        domain = list(range(33,37)) if kind == "patch" else list(range(100))
        need(all(type(i) is int for i in survivors+excluded) and sorted(survivors+excluded) == domain and
             len(set(survivors+excluded)) == len(domain), "Complete disjoint fresh probability classification")
        if kind == "resource" and branch in ("b3", "b4", "b5"):
            need(survivors == BRANCHES[branch]["local"], "All actual global survivors enter the fixed local queue")
            initial = root/locations(branch)["initial"]
            need(packet["parent_proof_sha256"] == proof["parent_proof_sha256"] ==
                 sha(initial/("POSITIVE24_"+branch.upper()+"_INITIAL_PROOF.json")) and
                 packet["parent_acceptance_sha256"] == proof["parent_acceptance_sha256"] ==
                 sha(initial/("POSITIVE24_"+branch.upper()+"_INITIAL_ACCEPTED.json")), "Resource consumes the freshly accepted INITIAL")
        elif kind == "resource":
            initial = root/locations(branch)["initial"]/("POSITIVE24_"+branch.upper()+"_INITIAL_PROOF.json")
            need(packet["input_sha256"]["initial24_"+branch+"_proof.json"] == sha(initial), "Resource alias is the same freshly accepted INITIAL")
        if kind in ("patch", "local_join"):
            need(set(survivors) <= set(BRANCHES[branch]["counts"]), "Every final survivor has a selected count forest")
        source_key = "input_sha256" if "input_sha256" in packet else "source_sha256"
        _binding_map(root, packet[source_key], d)
        if kind in ("patch", "local_join"):
            parent_base = root/("continuation_20261010" if kind == "patch" else "continuation_20261011/stronger24")
            need(packet.get("parent_binding_sha256", proof["parent_binding_sha256"]) == proof["parent_binding_sha256"], "Same fresh local parent bindings")
            _binding_map(root, proof["parent_binding_sha256"], parent_base)
        if kind == "local_join":
            need(len(proof["rows"]) == 100 and all(type(r["index"]) is int and r["index"] == i for i,r in enumerate(proof["rows"])),
                 "All 100 ordered local/global probability dispositions")
            _binding_map(root, packet["panel_binding_sha256"], d)
    elif kind == "local":
        need(type(packet.get("panel")) is int and packet["panel"] == stage["index"] and packet.get("probability_panels") == 1,
             "Same complete local panel")
        need(packet["local_signed_rectangles"] == 18432*sum(len(c["stages"]) for r in proof["rows"] for c in r["cycles"]),
             "Every complete local cycle rectangle counted")
        _binding_map(root, packet["source_sha256"], d)
        need(packet["parent_binding_sha256"] == proof["parent_binding_sha256"], "Same fresh local proof/acceptance parents")
        _binding_map(root, proof["parent_binding_sha256"], root/"continuation_20261011/stronger24")
    elif kind == "local_b2":
        need(packet["indices"] == [33,34,35,36] and packet["signed_rectangles"] ==
             18432*sum(len(r["stages"]) for r in proof["rows"]), "Complete selected B2 local mean-floor domain")
        _binding_map(root, packet["source_sha256"], d)
        _binding_map(root, proof["parent_binding_sha256"], root/"continuation_20261010")
    return dict(kind=kind, status=packet["status"], receipt_sha256=sha(d/stage["receipt"]),
                controls=len(controls) if type(controls) is list else controls,
                local_signed_rectangles=packet.get("local_signed_rectangles", packet.get("signed_rectangles")))


def validate_execution(observed, command, cwd):
    need(observed.get("status") == "completed" and type(observed.get("returncode")) is int and
         observed["returncode"] == 0, "Guarded arithmetic must finish successfully")
    need(observed.get("command", command) == command, "Same literal observed command")
    for kind in ("stdout", "stderr"):
        path = Path(observed[kind+"_path"])
        need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 16*MIB and
             sha(path) == observed.get(kind+"_sha256"), "Actual bounded capture is SHA-bound: " + kind)
    need(Path(observed["stderr_path"]).stat().st_size == 0, "Complete native action has empty stderr")
    need(Path(observed["stdout_path"]).stat().st_size > 0, "Complete action has actual nonempty output")
    scope = observed.get("guard_scope", {})
    need(observed.get("mode") == "untrusted_search" and scope.get("kind") == "UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP" and
         scope.get("proof_acceptance") is False and type(observed.get("sample_count")) is int and
         observed["sample_count"] > 0, "Actual sampled BASIC execution, without a stronger acceptance claim")


def _interface_packet(root, branch, observed):
    packet = json.loads(Path(observed["stdout_path"]).read_text("utf-8"), object_pairs_hook=unique)
    p = locations(branch)
    need(packet["status"] == "PASS_EXACT_"+branch.upper()+"_ALL_COUNT_RESOURCE_INTERFACES" and
         [x["index"]for x in packet["rows"]] == BRANCHES[branch]["counts"],
         "Every scalar/moment/signed-quadratic interface freshly evaluated")
    need(packet["mixed_proof_sha256"] == sha(Path(root)/p["local"]/(branch.upper()+"_FINITE_FEEDBACK_PROOF.json")) and
         packet["contract_sha256"] == BRANCHES[branch]["contract"] == sha(Path(root)/p["count"]/"contract.json"),
         "Actual same-law mixed proof to exact selected count contract")
    need(all(r.get("scalar_and_moment_guards") is True and type(r.get("quadratic_interfaces")) is list and
             r["quadratic_interfaces"] for r in packet["rows"]), "All acquired scalar/moment/quadratic interfaces present")
    return packet


@contextmanager
def _warnings():
    previous = os.environ.get("PYTHONWARNINGS")
    policy = "ignore:invalid escape sequence:SyntaxWarning"
    os.environ["PYTHONWARNINGS"] = (previous+"," if previous else "")+policy
    try:
        yield policy
    finally:
        if previous is None:
            os.environ.pop("PYTHONWARNINGS", None)
        else:
            os.environ["PYTHONWARNINGS"] = previous


def run(task, *, wall_seconds=7260, cpu_seconds=7200, memory_bytes=512*MIB):
    from . import aux24_sources as source, colab_batch, linux_supervisor
    from .small_indices import FollowOutput, Progress
    task = Path(task).resolve()
    info = read(task/"BRANCH.json", MIB)
    branch = info["branch"]
    need(info.get("schema") == "CONDITIONAL_STRONG24_BRANCH_TASK_V1" and info["driver_sha256"] == sha(__file__) and
         info["manifest_sha256"] == SELECTION_SHA[branch], "Same reviewed driver/task and independently pinned selection")
    source.verify_prepared(task, expected_manifest_sha=SELECTION_SHA[branch])
    sealed = source.source_root(task)
    root = task/"execution-epoch"/"cutoff25_20261011"
    need(not root.exists(), "New branch execution epoch; completed evidence is preserved")
    shutil.copytree(sealed, root)
    pins = {p.relative_to(root).as_posix():sha(p) for p in root.rglob("*") if p.is_file()}
    mutable = set()
    reports = []

    def unchanged():
        for name, pin in pins.items():
            if name not in mutable:
                path = root/name
                need(path.is_file() and not path.is_symlink() and sha(path) == pin, "Unchanged sealed numeric source/candidate: "+name)

    try:
        for stage in stages(branch):
            d = root/stage["folder"]
            if stage["name"] == "resource-accept" and branch in ("b0", "b1", "b2"):
                p = locations(branch)
                parent = root/p["initial"]/ ("POSITIVE24_"+branch.upper()+"_INITIAL_PROOF.json")
                for folder in (p["resource"],p["original"]):
                    target = root/folder/("initial24_"+branch+"_proof.json")
                    need(not target.exists(), "Only fresh accepted INITIAL supplies this resource input")
                    shutil.copyfile(parent,target)
            if stage["kind"] == "local":
                candidate = d/stage["proof"]
                rebind_local_candidate(candidate, root, branch, ledger=task/(stage["name"]+"-CANDIDATE.json"))
                mutable.add(candidate.relative_to(root).as_posix())
            if stage["receipt"]:
                need(not (d/stage["receipt"]).exists(), "No archived or previous acceptance may seed a stage")
            unchanged()
            command = [sys.executable,"-B","-u",str(d/stage["script"]),*stage["args"]]
            capture = task/"captures"/stage["name"]
            existing = {f.relative_to(root).as_posix() for f in root.rglob("*") if f.is_file()}
            colab_batch.event(task,"strong24_stage_started",branch=branch,stage=stage["name"],
                              wall_seconds=wall_seconds,cpu_seconds=cpu_seconds,source_sha256=sha(d/stage["script"]))
            progress = Progress(task/(stage["name"]+"-FOLLOW.jsonl"))
            try:
                with FollowOutput(stage["name"],capture/"stdout.txt",progress,20), _warnings() as warning_policy:
                    observed = linux_supervisor.run(command,cwd=d,output_dir=capture,wall_seconds=wall_seconds,
                               cpu_seconds=cpu_seconds,memory_bytes=memory_bytes,mode="untrusted_search",
                               disk_bytes=1024*MIB,log_bytes=16*MIB,heartbeat_seconds=20)
            finally:
                progress.close()
            report = dict(schema="OBSERVED_STRONG24_BRANCH_STAGE_V1",branch=branch,stage=stage,
                          command=command,observed=observed,warning_policy=warning_policy,
                          supervisor_sha256=sha(linux_supervisor.__file__),native_arithmetic_accepted=False,
                          all_index_conclusion_verified=False,original_task_root=str(task),
                          launch_sha256=sha(capture/"launch.json"),
                          supervisor_result_sha256=sha(capture/"supervisor-result.json"),
                          preceding_stage_sha256={r["stage"]["name"]:sha(task/(r["stage"]["name"]+"-COMPLETED.json")) for r in reports})
            colab_batch.atomic_json(task/(stage["name"]+"-ATTEMPT.json"), report)
            validate_execution(observed,command,d)
            unchanged()
            report["result"] = validate_artifact(root,branch,stage)
            if stage["kind"] == "interfaces":
                report["result"] = _interface_packet(root,branch,observed)
            artifacts = {f.relative_to(root).as_posix() for f in root.rglob("*") if f.is_file()}-existing
            for field in ("proof", "receipt"):
                if stage[field]:
                    artifacts.add(stage["folder"]+"/"+stage[field])
            report["artifact_sha256"] = {name:sha(root/name) for name in sorted(artifacts)}
            report["arithmetic_computed"] = True
            colab_batch.atomic_json(task/(stage["name"]+"-COMPLETED.json"),report)
            reports.append(report)
            colab_batch.event(task,"strong24_stage_completed",branch=branch,stage=stage["name"],
                              completed=len(reports),total=len(stages(branch)),native_arithmetic_accepted=False)
        count_results=[r["result"]for r in reports if r["stage"]["kind"]=="count"]
        need([r["index"]for r in count_results] == BRANCHES[branch]["counts"] and
             sum(r["leaves"]for r in count_results) == BRANCHES[branch]["leaves"], "Complete selected branch forest census")
        source.verify_prepared(task,expected_manifest_sha=info["manifest_sha256"])
        result=dict(schema="CONDITIONAL_STRONG24_BRANCH_ARITHMETIC_V1",state="complete_conditional_arithmetic_basic",
                    branch=branch,n=24,K="3/10",contact_allowance="15/46",effective_contact_allowance=EFFECTIVE_Q[branch],predecessor_statement_sha256=PREDECESSOR_SHA,
                    driver_sha256=sha(__file__),rho_interval=BRANCHES[branch]["rho"],probability_panels=100,arithmetic_computed=True,
                    native_arithmetic_accepted=False,branch_theorem_acquired=False,stronger24_acquisition_verified=False,
                    all_index_conclusion_verified=False,conditional_premises=PREMISES,
                    count_forests=len(count_results),count_leaves=sum(r["leaves"]for r in count_results),
                    count_indices=BRANCHES[branch]["counts"],original_task_root=str(task),
                    completed_stage_count=len(reports),stage_receipts={r["stage"]["name"]:sha(task/(r["stage"]["name"]+"-COMPLETED.json"))for r in reports},
                    source_manifest_sha256=info["manifest_sha256"],numeric_sources_changed=False,
                    resource_to_count_numeric_interfaces_computed=True,
                    interface_evidence_sha256={r["stage"]["name"]:sha(task/(r["stage"]["name"]+"-COMPLETED.json"))for r in reports
                                              if r["stage"]["kind"] in ("resource","patch","interfaces")},
                    execution_contract="BASIC sampled process-tree supervision; not trusted_native")
    except BaseException as error:
        result=dict(schema="CONDITIONAL_STRONG24_BRANCH_ARITHMETIC_V1",state="partial_not_accepted",branch=branch,
                    arithmetic_computed=False,native_arithmetic_accepted=False,branch_theorem_acquired=False,
                    stronger24_acquisition_verified=False,all_index_conclusion_verified=False,
                    completed_stage_count=len(reports),failed_stage=stage["name"] if "stage" in locals() else None,
                    error=type(error).__name__+": "+str(error),conditional_premises=PREMISES)
        (task/"ERROR.txt").write_text(traceback.format_exc(),encoding="utf-8")
    colab_batch.atomic_json(task/"RESULT.json",result)
    return result


def _relocated(path, task, original):
    """Map only one explicit recorded task prefix; original receipts stay intact."""
    value, prefix = str(path).replace("\\", "/"), str(original).replace("\\", "/").rstrip("/")
    need(value.startswith(prefix+"/"), "Captured file is under the one recorded task root")
    suffix = relative(value[len(prefix)+1:])
    result = (Path(task)/suffix).resolve()
    need(result.is_relative_to(Path(task).resolve()), "Restored capture stays inside the imported task")
    return result


def validate_completed(task, *, original_task_root=None):
    """Revalidate a finished local/restored task without rerunning numeric math.

    Returns the scoped branch evidence needed by the final auxiliary join.
    Recorded argv, receipt bytes and old capture paths are never rewritten.
    """
    from . import aux24_sources as source, linux_supervisor
    task = Path(task).resolve()
    result = read(task/"RESULT.json", 8*MIB)
    info = read(task/"BRANCH.json", MIB)
    branch = result["branch"]
    locations(branch)
    need(result.get("schema") == "CONDITIONAL_STRONG24_BRANCH_ARITHMETIC_V1" and
         result.get("state") == "complete_conditional_arithmetic_basic" and result.get("arithmetic_computed") is True,
         "Only fully computed conditional branch arithmetic may be consumed")
    need(result.get("native_arithmetic_accepted") is False and result.get("all_index_conclusion_verified") is False and
         result.get("branch_theorem_acquired") is False and result.get("stronger24_acquisition_verified") is False,
         "Preserve the conditional arithmetic and BASIC execution scope")
    need(info["driver_sha256"] == sha(__file__) and info["manifest_sha256"] == result["source_manifest_sha256"] == SELECTION_SHA[branch],
         "Same reviewed branch driver and exact externally pinned selected source epoch")
    manifest = source.verify_prepared(task, expected_manifest_sha=SELECTION_SHA[branch])
    original = original_task_root or result["original_task_root"]
    need(str(original).replace("\\","/").rstrip("/") == result["original_task_root"].replace("\\","/").rstrip("/"),
         "Explicit relocation agrees with the recorded originating task")
    root = task/"execution-epoch"/"cutoff25_20261011"
    expected = stages(branch)
    need(list(result["stage_receipts"]) == [s["name"] for s in expected] and
         result["completed_stage_count"] == len(expected), "Complete exact selected stage queue")
    preceding, counts, interfaces = {}, [], {}
    for stage in expected:
        path = task/(stage["name"]+"-COMPLETED.json")
        need(sha(path) == result["stage_receipts"][stage["name"]], "Unchanged observed stage receipt")
        report = read(path, 32*MIB)
        need(report.get("schema") == "OBSERVED_STRONG24_BRANCH_STAGE_V1" and report["branch"] == branch and
             report["stage"] == stage and report["preceding_stage_sha256"] == preceding and
             report.get("arithmetic_computed") is True and report.get("native_arithmetic_accepted") is False,
             "Exact stage identity and complete preceding observed execution chain")
        need(report["supervisor_sha256"] == sha(linux_supervisor.__file__), "Same reviewed BASIC supervisor source")
        command = report["command"]
        need(len(command) == 4+len(stage["args"]) and command[1:3] == ["-B","-u"] and command[4:] == stage["args"] and
             _relocated(command[3],task,original) == root/stage["folder"]/stage["script"], "Exact unchanged entrypoint and stage arguments")
        capture = task/"captures"/stage["name"]
        need(sha(capture/"launch.json") == report["launch_sha256"] and
             sha(capture/"supervisor-result.json") == report["supervisor_result_sha256"], "Bound original execution contract and supervisor result")
        launch = read(capture/"launch.json", 2*MIB)
        need(launch["argv"] == command and _relocated(launch["cwd"],task,original) == root/stage["folder"] and
             launch["mode"] == "untrusted_search", "Observed launch binds exact command and original cwd")
        need(read(capture/"supervisor-result.json", 4*MIB) == report["observed"], "Observed receipt equals the actual supervisor result")
        observed = dict(report["observed"])
        for field in ("stdout_path","stderr_path"):
            observed[field] = str(_relocated(observed[field],task,original))
        validate_execution(observed,command,root/stage["folder"])
        for name, pin in report["artifact_sha256"].items():
            artifact = root/relative(name)
            need(artifact.is_file() and not artifact.is_symlink() and sha(artifact) == pin, "Unchanged actual stage artifact")
        checked = validate_artifact(root,branch,stage)
        if stage["kind"] == "interfaces":
            checked = _interface_packet(root,branch,observed)
        need(checked == report["result"], "Fresh artifact/domain/control/interface evidence still agrees")
        if stage["kind"] == "count":
            counts.append(checked)
        if stage["kind"] in ("resource","patch","interfaces"):
            interfaces[stage["name"]] = sha(path)
        preceding[stage["name"]] = sha(path)
    # All numerical source bytes and all non-derived candidates remain sealed.
    local_candidates = {s["folder"]+"/"+s["proof"] for s in expected if s["kind"] == "local"}
    for name, row in manifest["files"].items():
        rel = name[len(PREFIX):]
        actual = root/rel
        if rel not in local_candidates:
            need(actual.is_file() and not actual.is_symlink() and sha(actual) == row["sha256"], "Unchanged executed numeric source/candidate")
        else:
            original_candidate = read(source.source_root(task)/rel)
            derived = read(actual)
            need({k:v for k,v in original_candidate.items() if k != "parent_binding_sha256"} ==
                 {k:v for k,v in derived.items() if k != "parent_binding_sha256"}, "Derived local candidate changes no numerical proof field")
            for parent, oldpin in original_candidate["parent_binding_sha256"].items():
                newpin = derived["parent_binding_sha256"][parent]
                need(newpin == oldpin or parent == branch+"_resource_exact_v1/RESOURCE_"+branch.upper()+"_GLOBAL_ACCEPTED.json",
                     "Only the explicitly allowed fresh resource receipt identity may differ")
    need([c["index"] for c in counts] == BRANCHES[branch]["counts"] and
         sum(c["leaves"] for c in counts) == BRANCHES[branch]["leaves"] and result["interface_evidence_sha256"] == interfaces,
         "Complete selected count census and actual numeric interface evidence")
    need(result.get("n") == 24 and type(result["n"]) is int and result.get("K") == "3/10" and
         result.get("contact_allowance") == "15/46" and result.get("predecessor_statement_sha256") == PREDECESSOR_SHA and
         result.get("effective_contact_allowance") == EFFECTIVE_Q[branch] and
         result.get("driver_sha256") == sha(__file__) and
         result.get("rho_interval") == BRANCHES[branch]["rho"] and result.get("probability_panels") == 100 and
         result.get("count_indices") == BRANCHES[branch]["counts"] and result.get("count_forests") == len(counts) and
         result.get("count_leaves") == sum(c["leaves"] for c in counts) and
         result.get("resource_to_count_numeric_interfaces_computed") is True, "Exact branch summary domain and semantic evidence")
    return dict(schema="REVALIDATED_CONDITIONAL_STRONG24_BRANCH_V1",branch=branch,n=24,K="3/10",contact_allowance="15/46",
                effective_contact_allowance=EFFECTIVE_Q[branch],
                predecessor_statement_sha256=PREDECESSOR_SHA,driver_sha256=sha(__file__),
                rho_interval=BRANCHES[branch]["rho"],probability_panels=100,count_indices=BRANCHES[branch]["counts"],
                count_forests=len(counts),count_leaves=sum(c["leaves"] for c in counts),
                numeric_resource_to_count_interfaces_verified=True,interface_evidence_sha256=interfaces,
                source_manifest_sha256=SELECTION_SHA[branch],result_sha256=sha(task/"RESULT.json"),
                arithmetic_computed=True,native_arithmetic_accepted=False,branch_theorem_acquired=False,
                stronger24_acquisition_verified=False,all_index_conclusion_verified=False,conditional_premises=PREMISES)


def run_colab(branch, *, durable_root, work_root="/content/berry-esseen-runs",
              archives="/content/berry-esseen-archives",wall_seconds=7260,cpu_seconds=7200,backup_interval=60):
    from . import colab_batch
    from .environment import snapshot
    locations(branch)
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
    root=Path(work_root)/("stronger24-"+branch)/stamp
    root.mkdir(parents=True)
    durable=Path(durable_root)/("stronger24-"+branch)/stamp
    status=dict(state="started",branch=branch,arithmetic_computed=False,native_arithmetic_accepted=False,
                branch_theorem_acquired=False,stronger24_acquisition_verified=False,all_index_conclusion_verified=False,
                conditional_premises=PREMISES)
    colab_batch.atomic_json(root/"ENVIRONMENT.json",snapshot())
    colab_batch.atomic_json(root/"SESSION_RESULT.json",status)
    monitor=colab_batch.Backups(root,durable,interval=backup_interval)
    monitor.start()
    try:
        colab_batch.event(root,"strong24_branch_started",branch=branch,native_actions=len(stages(branch)),
                          selected_forests=len(BRANCHES[branch]["counts"]),historical_leaf_census=BRANCHES[branch]["leaves"])
        task=prepare(branch,archives,root/"task",download=True)
        status.update(run(task,wall_seconds=wall_seconds,cpu_seconds=cpu_seconds))
    except BaseException as error:
        status.update(state="partial_not_accepted",error=type(error).__name__+": "+str(error))
        (root/"ERROR.txt").write_text(traceback.format_exc(),encoding="utf-8")
        colab_batch.event(root,"strong24_branch_incomplete",branch=branch,error=status["error"])
    finally:
        colab_batch.atomic_json(root/"SESSION_RESULT.json",status)
        try:
            monitor.close()
        except Exception as error:
            colab_batch.event(root,"final_backup_failed",error=str(error))
        output=colab_batch.bundle(root,durable)
        colab_batch.event(root,"strong24_branch_bundle_saved",branch=branch,path=str(output),state=status["state"])
    print("\nRESULT:",status["state"],"\nZIP:",output,flush=True)
    return dict(status=status,bundle=str(output),work=str(root))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("branch",choices=BRANCHES)
    parser.add_argument("--durable-root",required=True)
    parser.add_argument("--work-root",default="/content/berry-esseen-runs")
    parser.add_argument("--archives",default="/content/berry-esseen-archives")
    args=parser.parse_args()
    result=run_colab(args.branch,durable_root=args.durable_root,work_root=args.work_root,archives=args.archives)
    return 0 if result["status"].get("arithmetic_computed") is True else 2


if __name__=="__main__":
    raise SystemExit(main())
