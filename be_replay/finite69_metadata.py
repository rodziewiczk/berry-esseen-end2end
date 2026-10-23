"""Exact finite7--9 preparation metadata, without mathematical imports.

These routines reconstruct input transport metadata only. A reconstructed
PREPARED packet is not a numerical acceptance receipt.
"""
from __future__ import annotations

import hashlib
import json
import ast
import copy
import math
import re

BASE = "work/cutoff6_20261018/analytic/initial7_9_accept_v1"
ORIGIN = "work/cutoff6_20261018/analytic/initial7_9_batch_v1"
RESOURCE = "work/cutoff6_20261020/entry/resource7_9_accept_v2"
ORIGINAL_RESOURCE_REPLAY_SHA256 = "6bcff8b60eb00c3422a0aec0d9382157669617fcfa526e466ad1618bd88b3470"
RESOURCE_REPLAY_SHA256 = "ad817754825d81d1ca7a560a6f029fc3cd8aeef4d366d869113be1ff7d6ce637"
MAX_BYTES = 64 * 1024**2
_HEX = re.compile(r"[0-9a-f]{64}")


def _need(ok, message):
    if not ok:
        raise ValueError(message)


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _unique(pairs):
    result = {}
    for name, value in pairs:
        _need(name not in result, "Unique JSON metadata keys")
        result[name] = value
    return result


def _read(raw):
    _need(type(raw) is bytes and 0 < len(raw) <= MAX_BYTES,
          "Bounded nonempty original metadata bytes")
    try:
        result = json.loads(raw, object_pairs_hook=_unique,
                            parse_constant=lambda value: _need(False, "Finite JSON metadata"))
    except (UnicodeError, RecursionError) as error:
        raise ValueError("Ordinary bounded UTF-8 JSON metadata") from error
    _need(type(result) is dict, "JSON metadata object")
    return result


def _path(value):
    _need(type(value) is str and value.startswith(("work/", "runs/")) and
          all(part and part not in (".", "..") for part in value.split("/")) and
          not any(char in value for char in "\\:\x00\r\n"),
          "Canonical relative POSIX source path")
    return value


def _pin(pins, path):
    _path(path)
    _need(type(pins) is dict and path in pins and type(pins[path]) is str and
          _HEX.fullmatch(pins[path]) is not None, "External original source SHA-256: " + path)
    return pins[path]


def reconstruct_prepared(source_prepared_bytes, candidate_bytes, *, n, band, source_pins):
    """Return exactly the externally pinned original POSIX PREPARED bytes.

    ``source_pins`` is the caller-verified original final source graph. It must
    include every referenced source, the candidate origin/INPUT aliases and the
    PREPARED output pin. This function never creates REPLAY_CHECKED or evaluates
    a candidate's mathematical claims.
    """
    _need(type(n) is int and n in (7, 8, 9) and type(band) is str and
          band in ("B0", "BN", "B2"), "Literal finite7--9 index and band")
    manifest = _read(source_prepared_bytes)
    candidate = _read(candidate_bytes)
    case = f"n{n}_{band}"
    origin = f"{ORIGIN}/INITIAL{n}_{band}.json"
    input_path = f"{BASE}/{case}/INPUT.json"
    prepared_path = f"{BASE}/{case}/PREPARED.json"
    manifest_path = BASE + "/SOURCE_PREPARED.json"
    _need(_digest(source_prepared_bytes) == _pin(source_pins, manifest_path),
          "Externally pinned SOURCE_PREPARED bytes")
    _need(set(manifest) == {"original_source_graph", "files_sha256", "execution"} and
          manifest["execution"] == "NOT_RUN", "Original source-preparation schema")
    original = manifest["original_source_graph"]
    files = manifest["files_sha256"]
    _need(type(original) is dict and len(original) == 54 and
          type(files) is dict and len(files) == 97, "Complete original preparation source inventories")
    for graph in (original, files):
        for path, pin in graph.items():
            _need(type(pin) is str and pin == _pin(source_pins, path),
                  "Every embedded source pin equals the external original graph")
    _need(type(candidate.get("n")) is int and candidate["n"] == n and
          candidate.get("band") == band and candidate.get("failure", False) is None and
          type(candidate.get("stages")) is list and len(candidate["stages"]) == 9 and
          candidate.get("cellwise_gap_gate") is True and
          candidate.get("files_sha256") == original,
          "Original complete nine-stage candidate metadata and source identity")
    candidate_pin = _digest(candidate_bytes)
    _need(candidate_pin == _pin(source_pins, origin) == _pin(source_pins, input_path),
          "Exact original candidate and INPUT byte aliases")
    graph = dict(files)
    # Preserve the original prepare.py insertion order and POSIX path spelling.
    for path, pin in (
        (origin, candidate_pin), (input_path, candidate_pin),
        (manifest_path, _digest(source_prepared_bytes)),
        (BASE + "/prepare.py", _pin(source_pins, BASE + "/prepare.py")),
        (BASE + "/replay.py", _pin(source_pins, BASE + "/replay.py")),
        (BASE + "/PROOF.txt", _pin(source_pins, BASE + "/PROOF.txt")),
    ):
        graph[path] = pin
    job = dict(n=n, band=band, input_path=origin, input_sha256=candidate_pin,
               original_source_graph=original, files_sha256=graph)
    output = (json.dumps(job, indent=2) + "\n").encode("utf-8")
    _need(_digest(output) == _pin(source_pins, prepared_path),
          "Reconstructed PREPARED bytes equal the external original output pin")
    return output


def _dump(value):
    return (json.dumps(value, indent=2) + "\n").encode("utf-8")


def _duration(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def _check_graph(graph, source_pins):
    _need(type(graph) is dict and bool(graph), "Complete source metadata graph")
    for path, pin in graph.items():
        _need(type(pin) is str and pin == _pin(source_pins, path),
              "Embedded original source graph equals external source pins")


def derive_resource_epoch(original_replay, prepared, source_result, fresh_initial, *,
                          n, band, source_pins):
    """Bind unchanged resource arithmetic to a genuinely fresh INITIAL receipt.

    The caller must first independently validate that receipt's actual full
    execution. This byte/JSON helper cannot acquire a parent fact. Original
    candidates and original scripts remain separately sealed at their paths;
    the returned PORT_REPLAY and FRESH metadata have a new execution identity.
    All other historical source dependencies still have to be supplied or
    handled by a separately reviewed, explicit conditional input boundary.
    """
    _need(type(n) is int and n in (7, 8, 9) and type(band) is str and
          band in ("B0", "BN", "B2"), "Literal finite7--9 resource case")
    case = f"n{n}_{band}"
    directory = f"{RESOURCE}/{case}"
    parent_path = f"{BASE}/{case}/REPLAY_CHECKED.json"
    _need(type(original_replay) is bytes and
          _digest(original_replay) == ORIGINAL_RESOURCE_REPLAY_SHA256 ==
          _pin(source_pins, RESOURCE + "/replay.py"), "Exact original resource replay source")
    for name, data in (("PREPARED.json", prepared), ("SOURCE_RESULT.json", source_result)):
        _need(type(data) is bytes and _digest(data) == _pin(source_pins, directory + "/" + name),
              "Exact archived resource metadata bytes: " + name)
    old_prepared = _read(prepared)
    old_source = _read(source_result)
    receipt = _read(fresh_initial)
    _need(set(old_prepared) == {"n", "band", "source_sha256", "initial_sha256", "initial_receipt",
                                "resource_cap", "initial_cap", "files_sha256"},
          "Exact original resource PREPARED schema")
    _need(set(old_source) == {"status", "n", "band", "indices", "rows", "errors", "initial_owncap",
                              "resource_owncap", "initial_receipt", "initial_receipt_sha256",
                              "files_sha256", "seconds", "cutoff_proved"},
          "Exact original resource source-result schema")
    for packet in (old_prepared, old_source):
        _need(type(packet["n"]) is int and packet["n"] == n and packet["band"] == band and
              packet["initial_receipt"] == parent_path, "Exact original resource case and parent path")
        _check_graph(packet["files_sha256"], source_pins)
        _need(packet["files_sha256"].get(parent_path) == _pin(source_pins, parent_path),
              "Original source graph binds the original parent receipt")
    _need(old_prepared["source_sha256"] == _digest(source_result) and
          old_prepared["initial_sha256"] == _pin(source_pins, directory + "/INITIAL.json") and
          old_source["initial_receipt_sha256"] == _pin(source_pins, parent_path) and
          old_source["status"] == "FULL_CONDITIONAL_RESOURCE7_9_DIAGNOSTIC_COMPLETE_NO_ACCEPTANCE" and
          old_source["cutoff_proved"] is False and old_source["errors"] == [] and
          old_source["indices"] == list(range(100)) and
          all(type(index) is int for index in old_source["indices"]) and
          type(old_source["rows"]) is list and len(old_source["rows"]) == 100 and
          old_source["initial_owncap"] == old_prepared["initial_cap"] and
          old_source["resource_owncap"] == old_prepared["resource_cap"] and
          _duration(old_source["seconds"]), "Complete original resource candidate identity and payload")
    for index, row in enumerate(old_source["rows"]):
        _need(type(row) is dict and set(row) == {"index", "status", "result", "seconds"} and
              type(row["index"]) is int and row["index"] == index and
              row["status"] in ("RESOURCE_ROW_DIAGNOSTIC", "RESOURCE_EXCLUSION_DIAGNOSTIC") and
              _duration(row["seconds"]), "All ordered original resource row metadata")
    _need(receipt.get("status") == "PASS_FRESH_CONDITIONAL_FULL_INITIAL7_9_ACQUISITION" and
          type(receipt.get("n")) is int and receipt["n"] == n and receipt.get("band") == band and
          receipt.get("input_sha256") == old_prepared["initial_sha256"] and
          receipt.get("numerical_premises", {}).get("predecessor_theorem") ==
          "sharp_CE_minimal_counterexample" and
          receipt.get("numerical_premises", {}).get("contact_error") == "0" and
          receipt.get("numerical_premises", {}).get("owncap") == old_prepared["initial_cap"],
          "Fresh INITIAL receipt for the exact same candidate, index, band and q0 premise")
    _check_graph(receipt.get("files_sha256"), source_pins)
    fresh_parent_pin = _digest(fresh_initial)
    fresh_source = copy.deepcopy(old_source)
    fresh_source["initial_receipt_sha256"] = fresh_parent_pin
    fresh_source["files_sha256"][parent_path] = fresh_parent_pin
    fresh_source_bytes = _dump(fresh_source)
    fresh_prepared = copy.deepcopy(old_prepared)
    fresh_prepared["source_sha256"] = _digest(fresh_source_bytes)
    fresh_prepared["files_sha256"][parent_path] = fresh_parent_pin
    fresh_source_path = directory + "/FRESH_SOURCE_RESULT.json"
    _need(fresh_source_path not in fresh_prepared["files_sha256"],
          "Fresh resource metadata has no historical output alias")
    fresh_prepared["files_sha256"][fresh_source_path] = _digest(fresh_source_bytes)
    fresh_prepared_bytes = _dump(fresh_prepared)
    replay = original_replay
    replacements = ((b"'PREPARED.json'", b"'FRESH_PREPARED.json'", 2),
                    (b"'SOURCE_RESULT.json'", b"'FRESH_SOURCE_RESULT.json'", 3))
    for before, after, count in replacements:
        _need(replay.count(before) == count and after not in replay,
              "Only the exact fixed resource metadata filename literals change")
        replay = replay.replace(before, after)
    _need(_digest(replay) == RESOURCE_REPLAY_SHA256, "Externally fixed resource port source identity")
    normalized = replay
    for before, after, _ in replacements:
        normalized = normalized.replace(after, before)
    _need(normalized == original_replay and
          ast.dump(ast.parse(normalized)) == ast.dump(ast.parse(original_replay)),
          "Reverse-normalized port bytes and AST equal the original replay")
    # Explicitly verify the whole JSON difference, not just selected numeric fields.
    source_check = copy.deepcopy(fresh_source)
    source_check["initial_receipt_sha256"] = old_source["initial_receipt_sha256"]
    source_check["files_sha256"][parent_path] = old_source["files_sha256"][parent_path]
    prepared_check = copy.deepcopy(fresh_prepared)
    prepared_check["source_sha256"] = old_prepared["source_sha256"]
    prepared_check["files_sha256"][parent_path] = old_prepared["files_sha256"][parent_path]
    del prepared_check["files_sha256"][fresh_source_path]
    _need(_dump(source_check) == _dump(old_source) and _dump(prepared_check) == _dump(old_prepared),
          "Only permitted parent and fresh source-file metadata changed")
    report = dict(schema="FRESH_FINITE69_RESOURCE_METADATA_EPOCH_V1", n=n, band=band,
                  original_replay_sha256=_digest(original_replay), replay_sha256=_digest(replay),
                  original_prepared_sha256=_digest(prepared),
                  fresh_prepared_sha256=_digest(fresh_prepared_bytes),
                  original_source_result_sha256=_digest(source_result),
                  fresh_source_result_sha256=_digest(fresh_source_bytes),
                  initial_receipt=parent_path,
                  original_initial_receipt_sha256=old_source["initial_receipt_sha256"],
                  fresh_initial_receipt_sha256=fresh_parent_pin,
                  initial_candidate_sha256=old_prepared["initial_sha256"],
                  original_numeric_payload_unchanged=True, rows=100,
                  fresh_initial_execution_evidence_verified=False,
                  historical_parent_ancestry_acquired=False,
                  resource_arithmetic_computed=False, all_index_conclusion_verified=False)
    return dict(replay_bytes=replay, fresh_prepared_bytes=fresh_prepared_bytes,
                fresh_source_result_bytes=fresh_source_bytes, report=report)
