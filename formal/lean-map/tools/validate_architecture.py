"""Check architecture schemas/fixtures only; never certify a numerical proof.

Requires jsonschema>=4 with referencing. No network schema resolution is used.
The strict codec here is a conformance aid, not the future production decoder.
"""
from __future__ import annotations

import hashlib
import base64
import importlib.metadata
import json
import re
from datetime import datetime, timezone
from fractions import Fraction
from math import gcd
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "architecture"


def fail_number(value: str):
    raise ValueError("JSON numeric tokens forbidden: " + value)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key: " + key)
        result[key] = value
    return result


def printable(value):
    if isinstance(value, str):
        if any(ord(c) < 32 or ord(c) > 126 for c in value):
            raise ValueError("non-printable/non-ASCII string")
    elif isinstance(value, dict):
        for key, child in value.items():
            printable(key)
            printable(child)
    elif isinstance(value, list):
        for child in value:
            printable(child)
    elif value is not None and not isinstance(value, bool):
        raise ValueError("unsupported RJSON value")


def encode(value) -> bytes:
    printable(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def decode(raw: bytes):
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("BOM forbidden")
    value = json.loads(raw.decode("utf-8", errors="strict"),
                       object_pairs_hook=unique_pairs, parse_int=fail_number,
                       parse_float=fail_number, parse_constant=fail_number)
    printable(value)
    return value


def raw_digest(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def domain_digest(kind: str, value) -> str:
    return raw_digest(("BEARCH/1\n" + kind + "\n").encode("ascii") + encode(value))


def semantic_primitives(value):
    if isinstance(value, list):
        for child in value:
            semantic_primitives(child)
    elif isinstance(value, dict):
        if set(value) == {"num", "den"}:
            n, d = int(value["num"]), int(value["den"])
            if d <= 0 or gcd(abs(n), d) != 1:
                raise ValueError("non-reduced rational or nonpositive denominator")
        if set(value) == {"lower", "upper"} and all(
                isinstance(value[k], dict) and set(value[k]) == {"num", "den"}
                for k in ("lower", "upper")):
            lo, hi = (Fraction(int(value[k]["num"]), int(value[k]["den"]))
                      for k in ("lower", "upper"))
            if lo > hi:
                raise ValueError("reversed interval")
        for key, child in value.items():
            if isinstance(child, str) and len(child) == 20 and child.endswith("Z") \
                    and child[4:5] == "-" and child[10:11] == "T":
                datetime.strptime(child, "%Y-%m-%dT%H:%M:%SZ")
            semantic_primitives(child)


def check_id(value):
    if not isinstance(value, dict):
        return
    for field, kind, preimage in (
        ("statement_digest", "statement", "core"),
        ("job_spec_id", "job-spec", "core"),
        ("verification_id", "verification-key", "key"),
        ("project_id", "frozen-project", "core"),
    ):
        if field in value and preimage in value:
            if value[field] != domain_digest(kind, value[preimage]):
                raise ValueError("wrong " + field)
    for field, kind in (("graph_digest", "task-graph"), ("quote_id", "cost-quote")):
        if field in value:
            core = {k: v for k, v in value.items() if k != field}
            if value[field] != domain_digest(kind, core):
                raise ValueError("wrong " + field)


def codec_controls():
    good = {"z": [True, False, None, 'a/b"\\'], "a": "0"}
    expected = b'{"a":"0","z":[true,false,null,"a/b\\\"\\\\"]}'
    if encode(good) != expected or decode(expected) != good:
        raise ValueError("codec golden vector failed")
    for bad in (b'{"a":true,"a":false}', b'1', b'1.5', b'NaN',
                b'"\\u00e9"', b'"\\n"', b'\xef\xbb\xbf{}', b'{}{}'):
        try:
            decode(bad)
        except (ValueError, UnicodeError):
            continue
        raise ValueError("codec accepted negative control: " + repr(bad))
    for bad in ({"num": "2", "den": "4"}, {"num": "0", "den": "2"},
                {"lower": {"num": "1", "den": "1"},
                 "upper": {"num": "0", "den": "1"}}):
        try:
            semantic_primitives(bad)
        except ValueError:
            continue
        raise ValueError("primitive negative control accepted")


def main():
    codec_controls()
    schemas = {}
    for path in sorted((ROOT / "schemas" / "architecture").glob("*.schema.json")):
        value = json.loads(path.read_text(encoding="utf-8-sig"))
        Draft202012Validator.check_schema(value)
        schemas[path.name] = value
    registry = Registry().with_resources(
        (value["$id"], Resource.from_contents(value)) for value in schemas.values())
    resolved_refs = 0

    def resolve_schema_refs(value, base):
        nonlocal resolved_refs
        if isinstance(value, dict):
            base = value.get("$id", base)
            if "$ref" in value:
                registry.resolver(base_uri=base).lookup(value["$ref"])
                resolved_refs += 1
            for child in value.values():
                resolve_schema_refs(child, base)
        elif isinstance(value, list):
            for child in value:
                resolve_schema_refs(child, base)

    for schema in schemas.values():
        resolve_schema_refs(schema, schema["$id"])
    index_raw = (EXAMPLES / "fixture-index.json").read_bytes()
    index = decode(index_raw)
    if encode(index) != index_raw:
        raise ValueError("fixture-index is not canonical")
    all_bytes = {}
    parsed = {}
    rows = []
    for entry in index["entries"]:
        path = (EXAMPLES / entry["path"]).resolve()
        if not path.is_relative_to(EXAMPLES.resolve()):
            raise ValueError("fixture escaped examples directory")
        raw = path.read_bytes()
        all_bytes[raw_digest(raw)] = raw
        try:
            value = decode(raw)
            is_canonical = encode(value) == raw
        except (ValueError, UnicodeError):
            value, is_canonical = None, False
        if is_canonical != entry["canonical"]:
            raise ValueError("canonical expectation failed: " + entry["path"])
        schema = entry["schema"]
        if schema is None:
            structurally_valid = value is not None
        else:
            validator = Draft202012Validator(schemas[schema], registry=registry)
            structurally_valid = value is not None and validator.is_valid(value)
        if structurally_valid != entry["structural_valid"]:
            errors = [] if value is None or schema is None else [
                e.message for e in validator.iter_errors(value)]
            raise ValueError(f"structural expectation failed: {entry['path']}: {errors[:3]}")
        primitive_error = None
        if structurally_valid and is_canonical:
            try:
                semantic_primitives(value)
            except ValueError as exc:
                primitive_error = str(exc)
            if entry["semantic_expectation"] == "reject_unreduced_rational":
                if primitive_error != "non-reduced rational or nonpositive denominator":
                    raise ValueError("negative rational control failed")
            elif primitive_error:
                raise ValueError(entry["path"] + ": " + primitive_error)
            else:
                check_id(value)
            parsed[entry["path"]] = value
        rows.append({"path": entry["path"], "schema": schema,
                     "canonical": is_canonical, "structural_valid": structurally_valid,
                     "primitive_rejection": primitive_error,
                     "semantic_expectation": entry["semantic_expectation"]})
    external = {a["artifact"]["bytes_digest"]: a["artifact"]
                for a in index.get("external_artifacts", [])}
    # Schema bytes can be named by distributed schema bundles as well as fixtures.
    for path in (ROOT / "schemas" / "architecture").glob("*.schema.json"):
        raw = path.read_bytes()
        all_bytes[raw_digest(raw)] = raw
    refs_checked, refs_external = 0, set()

    def refs(value):
        nonlocal refs_checked
        if isinstance(value, dict):
            if set(value) == {"bytes_digest", "size_bytes", "media_type", "format_id"}:
                digest = value["bytes_digest"]
                if digest in all_bytes:
                    if int(value["size_bytes"]) != len(all_bytes[digest]):
                        raise ValueError("artifact length mismatch: " + digest)
                    refs_checked += 1
                elif digest in external:
                    if value != external[digest]:
                        raise ValueError("external artifact metadata mismatch: " + digest)
                    refs_external.add(digest)
                else:
                    raise ValueError("undeclared missing artifact: " + digest)
            for child in value.values():
                refs(child)
        elif isinstance(value, list):
            for child in value:
                refs(child)

    for value in parsed.values():
        refs(value)
    scope_digests = {domain_digest("scope", parsed[e["path"]])
                     for e in index["entries"] if e["schema"] == "count-scope.schema.json"}
    claim_digests = {domain_digest("claim", value) for value in parsed.values()
                     if isinstance(value, dict) and value.get("artifact_kind") == "claim"}
    schema_bundle_digests = {domain_digest("schema-bundle", value) for value in parsed.values()
                            if isinstance(value, dict) and set(value) == {"root_schema_id", "resources"}}
    for value in parsed.values():
        if not isinstance(value, dict):
            continue
        if "scope_digest" in value and value["scope_digest"] not in scope_digests:
            raise ValueError("fixture scope domain identity mismatch")
        if "claim_digest" in value and value["claim_digest"] not in claim_digests:
            raise ValueError("fixture claim domain identity mismatch")
        if value.get("artifact_kind") == "statement":
            for field in ("parameter_schema_digest", "conclusion_schema_digest"):
                if value["core"][field] not in schema_bundle_digests:
                    raise ValueError("fixture schema-bundle domain identity mismatch")
    control_rows = []
    for control in index.get("controls", []):
        if control["kind"] != "unbound_farkas":
            raise ValueError("unsupported fixture control")
        expected = parsed[control["expected_problem"]]
        trace = parsed[control["trace"]]
        candidate = parsed[control["candidate"]]
        problem_raw = all_bytes[trace["problem"]["bytes_digest"]]
        problem = decode(problem_raw)
        if problem["statement_digest"] != expected["statement_digest"]:
            raise ValueError("control should share statement but differ in actual necessary rows")
        if problem == expected or trace["problem"]["bytes_digest"] == raw_digest(encode(expected)):
            raise ValueError("unbound Farkas control is not different")
        if candidate.get("statement_digest") != expected["statement_digest"]:
            raise ValueError("candidate control statement mismatch")
        if control["expected_outcome"] != "rejected" or control["expected_reason"] != "unbound_farkas_problem":
            raise ValueError("invalid negative fixture expectation")
        q = lambda v: Fraction(int(v["num"]), int(v["den"]))
        multipliers = [q(v) for v in trace["multipliers"]]
        inequalities = problem["inequalities"]
        if len(multipliers) != len(inequalities) or any(y < 0 for y in multipliers):
            raise ValueError("invalid toy Farkas dimensions or sign")
        for col in range(len(problem["variables"])):
            if sum((y*q(row["coefficients"][col]) for y, row in zip(multipliers, inequalities)), Fraction(0)) != 0:
                raise ValueError("toy Farkas coefficients do not cancel")
        if sum((y*q(row["rhs"]) for y, row in zip(multipliers, inequalities)), Fraction(0)) >= 0:
            raise ValueError("toy Farkas strict contradiction failed")
        control_rows.append({"kind": control["kind"], "binding_mismatch_detected": True,
                             "toy_rational_contradiction_checked": True,
                             "production_meaning_checker_executed": False})
    vectors = parsed["codec-vectors.json"]["vectors"]
    for vector in vectors:
        raw = base64.b64decode(vector["input_utf8_base64"], validate=True)
        try:
            decoded = decode(raw)
            canonical = encode(decoded) == raw
        except (ValueError, UnicodeError):
            canonical = False
        if canonical != (vector["expected"] == "canonical"):
            raise ValueError("fixture codec vector failed: " + vector["name"])
    from render_proof_map import load_checked_report
    lean = load_checked_report()
    graph = json.loads((ROOT / "assets" / "execution-map.json").read_text(encoding="utf-8"))
    ids = {n["id"] for n in graph["nodes"]}
    if len(ids) != len(graph["nodes"]):
        raise ValueError("duplicate graph node")
    for node in graph["nodes"]:
        if not (ROOT / node["doc"]).is_file():
            raise ValueError("broken architecture link")
    for edge in graph["edges"]:
        if edge["from"] not in ids or edge["to"] not in ids:
            raise ValueError("unknown graph endpoint")
    local_links = 0
    docs = sorted((ROOT / "docs" / "architecture").glob("*.md")) + [
        ROOT / "README.md", ROOT / "docs" / "plan.md"]
    for path in docs:
        for match in re.finditer(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", path.read_text(encoding="utf-8")):
            target = match.group(1).strip("<>")
            if "://" in target or target.startswith("#"):
                continue
            relative = target.split("#", 1)[0]
            if relative and not (path.parent / relative).exists():
                raise ValueError(f"broken local link in {path.relative_to(ROOT)}: {target}")
            local_links += 1
    audit = json.loads((ROOT / "docs/architecture/architecture-findings.json").read_text(encoding="utf-8-sig"))
    if audit["status"] != "specification_review_complete" or any(
            row["status"] != "contract_resolved" for row in audit["findings"]):
        raise ValueError("architecture audit has unresolved specification findings")
    for name, digest in audit["reviewed_snapshot"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError("audit snapshot changed: " + name)
    result = {
        "scope": "architecture schemas, format fixtures and preserved Lean source hashes",
        "architecture_checks_passed": True, "numerical_proof_pass": False,
        "production_runner_executed": False, "paid_cloud_resources_created": False,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "validation_environment": {p: importlib.metadata.version(p) for p in (
            "jsonschema", "referencing", "attrs", "jsonschema-specifications", "rpds-py")},
        "schema_count": len(schemas), "offline_schema_refs_resolved": resolved_refs,
        "local_document_links_checked": local_links, "codec_fixture_vectors": len(vectors),
        "scope_identities_checked": len(scope_digests),
        "claim_identities_checked": len(claim_digests),
        "schema_bundle_identities_checked": len(schema_bundle_digests),
        "resolved_specification_findings": len(audit["findings"]),
        "audit_snapshot_files_checked": len(audit["reviewed_snapshot"]),
        "fixtures": rows,
        "local_artifact_refs_checked": refs_checked,
        "declared_external_artifacts_referenced": len(refs_external),
        "controls": control_rows, "unchanged_lean_sources": len(lean["modules"]),
        "graph_nodes": len(ids), "graph_edges": len(graph["edges"]),
    }
    report_path = ROOT / "verification" / "architecture-check.json"
    report_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: result[k] for k in ("architecture_checks_passed", "numerical_proof_pass",
          "schema_count", "unchanged_lean_sources", "graph_nodes", "graph_edges")}))


if __name__ == "__main__":
    main()
