"""Synthetic source/metadata fixtures; no numerical engine is imported."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch

from be_replay import finite69_metadata as metadata


def raw(value):
    return (json.dumps(value, indent=2) + "\n").encode()


def fixture(n=7, band="B0"):
    files = {f"work/synthetic/source{i}.py": hashlib.sha256(str(i).encode()).hexdigest()
             for i in range(97)}
    original = dict(list(files.items())[:54])
    manifest = dict(original_source_graph=original, files_sha256=files, execution="NOT_RUN")
    candidate = dict(n=n, band=band, failure=None, stages=[{} for _ in range(9)],
                     cellwise_gap_gate=True, files_sha256=original)
    mb, cb = raw(manifest), raw(candidate)
    origin = f"{metadata.ORIGIN}/INITIAL{n}_{band}.json"
    case = f"{metadata.BASE}/n{n}_{band}"
    pins = dict(files)
    pins[origin] = pins[case + "/INPUT.json"] = hashlib.sha256(cb).hexdigest()
    pins[metadata.BASE + "/SOURCE_PREPARED.json"] = hashlib.sha256(mb).hexdigest()
    for name in ("prepare.py", "replay.py", "PROOF.txt"):
        pins[metadata.BASE + "/" + name] = hashlib.sha256(name.encode()).hexdigest()
    graph = dict(files)
    for name in (origin, case + "/INPUT.json", metadata.BASE + "/SOURCE_PREPARED.json",
                 metadata.BASE + "/prepare.py", metadata.BASE + "/replay.py", metadata.BASE + "/PROOF.txt"):
        graph[name] = pins[name]
    expected = raw(dict(n=n, band=band, input_path=origin, input_sha256=pins[origin],
                        original_source_graph=original, files_sha256=graph))
    pins[case + "/PREPARED.json"] = hashlib.sha256(expected).hexdigest()
    return mb, cb, pins, expected


def resource_fixture():
    script = (b"job = read(dest/'PREPARED.json')\n"
              b"z = read(dest/'SOURCE_RESULT.json')\n"
              b"check(dest/'SOURCE_RESULT.json')\n"
              b"record(dest/'PREPARED.json', dest/'SOURCE_RESULT.json')\n"
              b"raise AssertionError('SYNTHETIC SCRIPT MUST NEVER EXECUTE')\n")
    parent = metadata.BASE + "/n7_B0/REPLAY_CHECKED.json"
    directory = metadata.RESOURCE + "/n7_B0"
    checker = "work/synthetic/resource_core.py"
    pins = {parent: "0" * 64, directory + "/INITIAL.json": "1" * 64,
            checker: "2" * 64, metadata.RESOURCE + "/replay.py": hashlib.sha256(script).hexdigest()}
    source = dict(status="FULL_CONDITIONAL_RESOURCE7_9_DIAGNOSTIC_COMPLETE_NO_ACCEPTANCE", n=7, band="B0",
                  indices=list(range(100)), rows=[dict(index=i, status="RESOURCE_ROW_DIAGNOSTIC",
                  result=dict(synthetic="unchanged numeric tripwire", i=i), seconds=i / 10) for i in range(100)],
                  errors=[], initial_owncap="423/1000", resource_owncap="2107/5000", initial_receipt=parent,
                  initial_receipt_sha256=pins[parent], files_sha256={parent:pins[parent], checker:pins[checker]},
                  seconds=12.5, cutoff_proved=False)
    sb = raw(source);pins[directory + "/SOURCE_RESULT.json"] = hashlib.sha256(sb).hexdigest()
    prepared = dict(n=7, band="B0", source_sha256=hashlib.sha256(sb).hexdigest(), initial_sha256="1" * 64,
                    initial_receipt=parent, resource_cap="2107/5000", initial_cap="423/1000",
                    files_sha256={parent:pins[parent], checker:pins[checker],
                                  directory + "/SOURCE_RESULT.json":hashlib.sha256(sb).hexdigest()})
    pb = raw(prepared);pins[directory + "/PREPARED.json"] = hashlib.sha256(pb).hexdigest()
    fresh = raw(dict(status="PASS_FRESH_CONDITIONAL_FULL_INITIAL7_9_ACQUISITION", n=7, band="B0",
                     input_sha256="1" * 64, numerical_premises=dict(predecessor_theorem="sharp_CE_minimal_counterexample",
                     contact_error="0", owncap="423/1000"), files_sha256={checker:pins[checker]}, seconds=123.25))
    port = script.replace(b"'PREPARED.json'", b"'FRESH_PREPARED.json'").replace(
                          b"'SOURCE_RESULT.json'", b"'FRESH_SOURCE_RESULT.json'")
    return script, pb, sb, fresh, pins, port


class Finite69Metadata(unittest.TestCase):
    def test_all_nine_literal_cases_and_original_order(self):
        for n in (7, 8, 9):
            for band in ("B0", "BN", "B2"):
                with self.subTest(n=n, band=band):
                    mb, cb, pins, expected = fixture(n, band)
                    saved = copy.deepcopy(pins)
                    self.assertEqual(metadata.reconstruct_prepared(mb, cb, n=n, band=band,
                                                                   source_pins=pins), expected)
                    self.assertEqual(pins, saved)
                    self.assertNotIn(b"REPLAY_CHECKED", expected)

    def test_external_output_and_input_pins_are_required(self):
        mb, cb, pins, _ = fixture()
        for path in (metadata.BASE + "/n7_B0/PREPARED.json", metadata.BASE + "/n7_B0/INPUT.json",
                     metadata.BASE + "/SOURCE_PREPARED.json", "work/synthetic/source42.py"):
            for replacement in (None, "0" * 64):
                changed = dict(pins)
                if replacement is None:
                    del changed[path]
                else:
                    changed[path] = replacement
                with self.subTest(path=path, replacement=replacement), self.assertRaises(ValueError):
                    metadata.reconstruct_prepared(mb, cb, n=7, band="B0", source_pins=changed)

    def test_wrong_case_boolean_and_incomplete_candidate_rejected(self):
        mb, cb, pins, _ = fixture()
        for n, band in ((True, "B0"), (6, "B0"), (7, "BC"), (8, "B0")):
            with self.subTest(n=n, band=band), self.assertRaises(ValueError):
                metadata.reconstruct_prepared(mb, cb, n=n, band=band, source_pins=pins)
        for name, value in (("n", True), ("failure", {}), ("stages", [{}]),
                            ("cellwise_gap_gate", False), ("files_sha256", {})):
            changed = json.loads(cb);changed[name] = value
            with self.subTest(name=name), self.assertRaises(ValueError):
                metadata.reconstruct_prepared(mb, raw(changed), n=7, band="B0", source_pins=pins)

    def test_duplicate_nonfinite_and_mutated_manifest_rejected(self):
        mb, cb, pins, _ = fixture()
        for changed in (mb.replace(b'"NOT_RUN"', b'"REPLAYED"'),
                        mb.replace(b'"execution": "NOT_RUN"', b'"execution": "NOT_RUN", "execution": "NOT_RUN"'),
                        mb.replace(b'"NOT_RUN"', b'NaN'), b"[]", b"\xff", b""):
            with self.subTest(length=len(changed)), self.assertRaises(ValueError):
                metadata.reconstruct_prepared(changed, cb, n=7, band="B0", source_pins=pins)

    def test_windows_or_reordered_serialization_cannot_match_posix_pin(self):
        mb, cb, pins, expected = fixture()
        d = json.loads(mb)
        d["files_sha256"] = dict(reversed(list(d["files_sha256"].items())))
        reordered = raw(d);changed = dict(pins)
        changed[metadata.BASE + "/SOURCE_PREPARED.json"] = hashlib.sha256(reordered).hexdigest()
        with self.assertRaisesRegex(ValueError, "PREPARED bytes"):
            metadata.reconstruct_prepared(reordered, cb, n=7, band="B0", source_pins=changed)
        changed = dict(pins)
        changed[metadata.BASE + "/n7_B0/PREPARED.json"] = hashlib.sha256(expected.replace(b"work/", b"work\\\\")).hexdigest()
        with self.assertRaisesRegex(ValueError, "PREPARED bytes"):
            metadata.reconstruct_prepared(mb, cb, n=7, band="B0", source_pins=changed)

    def resource_context(self, script, port):
        return patch.multiple(metadata, ORIGINAL_RESOURCE_REPLAY_SHA256=hashlib.sha256(script).hexdigest(),
                              RESOURCE_REPLAY_SHA256=hashlib.sha256(port).hexdigest())

    def test_resource_epoch_changes_only_metadata_and_filename_literals(self):
        script, pb, sb, fresh, pins, port = resource_fixture()
        before = copy.deepcopy(pins)
        with self.resource_context(script, port):
            result = metadata.derive_resource_epoch(script, pb, sb, fresh, n=7, band="B0", source_pins=pins)
        self.assertEqual(result["replay_bytes"], port)
        self.assertEqual(pins, before)
        source = json.loads(sb);new_source = json.loads(result["fresh_source_result_bytes"])
        self.assertEqual(source["rows"], new_source["rows"])
        self.assertEqual(source["seconds"], new_source["seconds"])
        parent = source["initial_receipt"]
        new_source["initial_receipt_sha256"] = source["initial_receipt_sha256"]
        new_source["files_sha256"][parent] = source["files_sha256"][parent]
        self.assertEqual(new_source, source)
        prepared = json.loads(pb);new_prepared = json.loads(result["fresh_prepared_bytes"])
        self.assertEqual(new_prepared["files_sha256"][metadata.RESOURCE + "/n7_B0/SOURCE_RESULT.json"],
                         prepared["files_sha256"][metadata.RESOURCE + "/n7_B0/SOURCE_RESULT.json"])
        self.assertEqual(result["report"]["fresh_initial_receipt_sha256"], hashlib.sha256(fresh).hexdigest())
        for name in ("fresh_initial_execution_evidence_verified", "historical_parent_ancestry_acquired",
                     "resource_arithmetic_computed", "all_index_conclusion_verified"):
            self.assertIs(result["report"][name], False)

    def test_resource_external_pin_candidate_or_script_mutation_is_rejected(self):
        script, pb, sb, fresh, pins, port = resource_fixture()
        with self.resource_context(script, port):
            for a, b, c in ((script + b"\n", pb, sb), (script, pb + b"\n", sb), (script, pb, sb + b"\n")):
                with self.subTest(lengths=(len(a),len(b),len(c))), self.assertRaises(ValueError):
                    metadata.derive_resource_epoch(a,b,c,fresh,n=7,band="B0",source_pins=pins)
        with self.assertRaises(ValueError):
            metadata.derive_resource_epoch(script,pb,sb,fresh,n=7,band="B0",source_pins=pins)

    def test_resource_wrong_fresh_parent_candidate_case_or_q_rejected(self):
        script, pb, sb, fresh, pins, port = resource_fixture()
        cases = [("n", True), ("band", "B2"), ("input_sha256", "0" * 64), ("status", "FAIL"),
                 ("files_sha256", {"work/synthetic/resource_core.py":"3" * 64})]
        with self.resource_context(script, port):
            for name, value in cases:
                changed = json.loads(fresh);changed[name] = value
                with self.subTest(name=name), self.assertRaises(ValueError):
                    metadata.derive_resource_epoch(script,pb,sb,raw(changed),n=7,band="B0",source_pins=pins)
            changed = json.loads(fresh);changed["numerical_premises"]["contact_error"] = "1/100"
            with self.assertRaises(ValueError):
                metadata.derive_resource_epoch(script,pb,sb,raw(changed),n=7,band="B0",source_pins=pins)

    def test_resource_rejects_unbound_preexisting_fresh_metadata_path(self):
        script, pb, sb, fresh, pins, port = resource_fixture()
        prepared = json.loads(pb);path = metadata.RESOURCE + "/n7_B0/FRESH_SOURCE_RESULT.json"
        prepared["files_sha256"][path] = "4" * 64
        pins[path] = "4" * 64;pb = raw(prepared)
        pins[metadata.RESOURCE + "/n7_B0/PREPARED.json"] = hashlib.sha256(pb).hexdigest()
        with self.resource_context(script, port), self.assertRaises(ValueError):
            metadata.derive_resource_epoch(script,pb,sb,fresh,n=7,band="B0",source_pins=pins)


if __name__ == "__main__":
    unittest.main()
