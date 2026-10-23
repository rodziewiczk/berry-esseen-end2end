"""Build the lower-B5 global parent catalog from bytes/AST/JSON only.

No original mathematical source is imported or evaluated. Historical accepted
objects are read only to specify source-bound output schemas and exact edges;
they are never selected as fresh execution inputs.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_BYTES = 514958998
ARCHIVE_SHA = "17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb"
PREFIX = "cutoff25_20261011/new_root/"


def sha(raw): return hashlib.sha256(raw).hexdigest()


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024**2), b""): h.update(block)
    return h.hexdigest()


def controls(raw, variable=None):
    tree = ast.parse(raw)
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    if variable:
        values = [n.value for n in main.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == variable for t in n.targets)]
    else:
        values = [n.iter for n in main.body if isinstance(n, ast.For) and isinstance(n.iter, ast.List)]
    if len(values) != 1 or not isinstance(values[0], ast.List): raise ValueError("One original literal control inventory")
    result = [n.elts[0].value for n in values[0].elts]
    if len(result) != 12 or len(set(result)) != 12: raise ValueError("All twelve original controls")
    return result


def build(archive, output):
    if archive.stat().st_size != ARCHIVE_BYTES or digest(archive) != ARCHIVE_SHA:
        raise ValueError("Exact pinned cutoff25 source archive")
    with zipfile.ZipFile(archive) as z:
        def row(name, role):
            info = z.getinfo(name); raw = z.read(info)
            return dict(member=name, bytes=len(raw), sha256=sha(raw), role=role)
        result = dict(schema="N25_B5_GLOBAL_PARENT_SOURCE_CATALOG_V1", date="2026-10-23",
            archive=dict(name=archive.name, bytes=ARCHIVE_BYTES, sha256=ARCHIVE_SHA),
            branch="b5", n=25, rho_interval=["3/2", "33/20"], contact_allowance="5/16",
            selected_full_actions=2, mathematical_code_executed=False,
            historical_acceptances_imported_as_inputs=0, stronger24_premise_acquired=False,
            resource_interfaces_verified=False, full_n25_verified=False, all_index_conclusion_verified=False)
        for kind, folder, checker, proof, receipt in (
            ("initial", "initial25_b5_exact_v1", "initial25_b5.py", "INITIAL25_B5_PROOF.json", "INITIAL25_B5_ACCEPTED.json"),
            ("global_resource", "resource25_b5_v1", "resources_b5.py", "RESOURCE_B5_GLOBAL_PROOF.json", "RESOURCE_B5_GLOBAL_ACCEPTED.json")):
            directory = PREFIX+folder+"/"
            manifest_raw = z.read(directory+"FROZEN_SOURCES.json")
            manifest = json.loads(manifest_raw)
            sources = []
            for name, pin in manifest.items():
                r = row(directory+name, "conditional_statement_premise" if name == "STRONGER24_COMPLETE_JOINED.json" else "frozen_source")
                if r["sha256"] != pin: raise ValueError("Actual frozen member pin: "+name)
                sources.append(r)
            candidate_raw, accepted_raw = z.read(directory+proof), z.read(directory+receipt)
            candidate, accepted = json.loads(candidate_raw), json.loads(accepted_raw)
            literal_controls = controls(z.read(directory+checker), "mutations" if kind == "global_resource" else None)
            if accepted["negative_controls"] != literal_controls: raise ValueError("Original receipt/control AST agreement")
            section = dict(directory=directory.rstrip("/"),
                checker=row(directory+checker, "unchanged_full_acceptor"),
                closure=dict(manifest=row(directory+"FROZEN_SOURCES.json", "source_manifest"), source_file_rows=sources),
                proof_candidate=row(directory+proof, "untrusted_complete_proof_candidate"),
                historical_acceptance=row(directory+receipt, "output_identity_only_not_selected_input"),
                controls=literal_controls, expected_status=accepted["status"],
                candidate_schema=candidate["schema"])
            if kind == "initial":
                if len(candidate["stages"]) != 12 or len(candidate["export"]["panels"]) != 100:
                    raise ValueError("Complete archived candidate census")
                reconstructed = dict(status=accepted["status"], proof_sha256=sha(candidate_raw),
                    checker_sha256=sha(z.read(directory+checker)), source_sha256=candidate["source_sha256"],
                    profile=candidate["profile"], final_invariants=candidate["final_invariants"],
                    signed_rectangles=239616, probability_panels=100, negative_controls=literal_controls, scope=candidate["scope"])
                if (json.dumps(reconstructed, indent=2)+"\n").encode() != accepted_raw:
                    raise ValueError("Deterministic original INITIAL receipt bytes")
                result["profile"] = candidate["profile"]
                section["deterministic_receipt_serialization_verified"] = True
            else:
                if len(candidate["rows"]) != 100: raise ValueError("All100 original resource rows")
                section.update(surviving_panels=accepted["surviving_panels"], excluded_panels=accepted["excluded_panels"],
                    parent_proof_sha256=candidate["parent_proof_sha256"], parent_acceptance_sha256=candidate["parent_acceptance_sha256"])
            result[kind] = section
        if result["global_resource"]["parent_proof_sha256"] != result["initial"]["proof_candidate"]["sha256"] or result["global_resource"]["parent_acceptance_sha256"] != result["initial"]["historical_acceptance"]["sha256"]:
            raise ValueError("Exact unchanged global parent edge")
    raw = (json.dumps(result, sort_keys=True, indent=2)+"\n").encode()
    if output.exists() and output.read_bytes() != raw: raise ValueError("Existing frozen catalog differs")
    output.parent.mkdir(parents=True, exist_ok=True)
    if not output.exists(): output.write_bytes(raw)
    return sha(raw)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT/"proof/n25_b5_global_sources.json")
    args = parser.parse_args()
    print(build(args.archive, args.output))
