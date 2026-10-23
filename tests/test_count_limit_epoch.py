"""Source/JSON fixtures only; trap mathematical modules are never imported."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from be_replay import count_limit_epoch as epoch, count_task as original


class LimitEpochTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "original"
        self.source.mkdir()
        protocol = b"""raise AssertionError('protocol must never be imported')
LIMIT=10000
def header(bound):return dict(schema='TRAP_SOURCE_ONLY_V1',n=25,index=29)
def construct():
 visited=1
 need(visited<=LIMIT and True,'resource guard')
def replay():
 visited=1
 need(visited<=LIMIT and True,'resource guard')
"""
        payload = {"count_protocol.py": protocol,
                   "contract.json": b'{"rows": [{"n": 25, "index": 29}]}\n',
                   "kernel.py": b"raise AssertionError('kernel must never be imported')\n"}
        manifest = {"kernel.py": epoch.sha(payload["kernel.py"])}
        payload["KERNEL_COPY_MANIFEST.json"] = epoch.encoded({"files": manifest})
        design = epoch.encoded({"files": {k: epoch.sha(v) for k, v in payload.items()}})
        payload["FROZEN_DESIGN.json"] = design
        for name, raw in payload.items():
            (self.source / name).write_bytes(raw)
        self.payload = payload
        self.old_pin, self.checker_pin = epoch.sha(design), epoch.sha(protocol)
        self.patches = [patch.object(epoch, "ORIGINAL_DESIGN_SHA256", self.old_pin),
                        patch.object(epoch, "ORIGINAL_CHECKER_SHA256", self.checker_pin),
                        patch.object(original, "TARGETS", dict(original.TARGETS,
                                     **{epoch.TARGET: ("original-v12", 29, self.old_pin)}))]
        for p in self.patches:
            p.start()
        files, derived, checker, _ = epoch._derive(design, protocol)
        for field, value in (("NEW_DESIGN_SHA256", epoch.sha(derived)),
                             ("DESIGN_SHA256", epoch.sha(derived)),
                             ("CHECKER_SHA256", epoch.sha(checker)),
                             ("CONTRACT_SHA256", files["contract.json"])):
            p = patch.object(epoch, field, value)
            p.start()
            self.patches.append(p)
        self.extended = self.root / "extended"
        self.report = epoch.build(self.source, self.extended)

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.temp.cleanup()

    def checkpoint(self):
        return dict(schema="UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1", arithmetic_accepted=False,
                    binding=dict(design_sha256=self.old_pin, alpha_priority="4",
                                 native_header=original.native_header(self.source, epoch.TARGET),
                                 search_sha256="a"*64, traversal="root-first"),
                    roots=[dict(k=k, tree={"kind": "pending"}) for k in range(26)])

    def forest(self):
        leaf = dict(kind="leaf", box=[], decision="TRAP_UNTRUSTED_ONLY", result={})
        return dict(**original.native_header(self.extended, epoch.TARGET),
                    roots=[dict(k=k, tree=deepcopy(leaf)) for k in range(26)])

    def test_build_seals_both_originals_and_every_other_byte(self):
        files = epoch.verify(epoch.TARGET, self.extended)
        self.assertEqual(len(files), 7)
        for name, raw in self.payload.items():
            self.assertEqual((self.source / name).read_bytes(), raw)
            if name not in ("FROZEN_DESIGN.json", "count_protocol.py"):
                self.assertEqual((self.extended / name).read_bytes(), raw)
        self.assertEqual((self.extended / epoch.ORIGINAL_DESIGN).read_bytes(), self.payload["FROZEN_DESIGN.json"])
        self.assertEqual((self.extended / epoch.ORIGINAL_CHECKER).read_bytes(), self.payload["count_protocol.py"])
        self.assertEqual((self.extended / "count_protocol.py").read_bytes(),
                         self.payload["count_protocol.py"].replace(b"LIMIT=10000\n", b"LIMIT=100000\n"))
        self.assertFalse(self.report["arithmetic_accepted"])
        self.assertFalse(self.report["resource_epoch"]["original_profile_acceptance"])

    def test_deterministic_path_independent_design(self):
        elsewhere = self.root / "another" / "deep" / "capsule"
        other = epoch.build(self.source, elsewhere)
        self.assertEqual(other["design_sha256"], self.report["design_sha256"])
        self.assertEqual((elsewhere / "FROZEN_DESIGN.json").read_bytes(),
                         (self.extended / "FROZEN_DESIGN.json").read_bytes())

    def test_never_overwrite_existing_capsule(self):
        with self.assertRaisesRegex(ValueError, "Fresh extended"):
            epoch.build(self.source, self.extended)

    def test_exact_migration_preserves_input_and_all_nodes(self):
        old = self.checkpoint()
        saved = deepcopy(old)
        new = epoch.migrate_checkpoint(old, self.source, self.extended)
        self.assertEqual(old, saved)
        self.assertEqual(new["roots"], old["roots"])
        self.assertNotEqual(new["binding"]["design_sha256"], old["binding"]["design_sha256"])
        self.assertNotEqual(new["binding"]["native_header"]["checker_sha256"],
                            old["binding"]["native_header"]["checker_sha256"])
        new["binding"]["design_sha256"] = old["binding"]["design_sha256"]
        new["binding"]["native_header"]["checker_sha256"] = old["binding"]["native_header"]["checker_sha256"]
        self.assertEqual(new, old)

    def test_migration_rejects_false_epoch_or_acceptance(self):
        for mutation in (lambda p: p.update(arithmetic_accepted=True),
                         lambda p: p["binding"].update(design_sha256="0"*64),
                         lambda p: p["binding"]["native_header"].update(contract_sha256="0"*64)):
            with self.subTest(mutation=mutation):
                packet = self.checkpoint()
                mutation(packet)
                with self.assertRaises(ValueError):
                    epoch.migrate_checkpoint(packet, self.source, self.extended)

    def test_wrong_target_rejected(self):
        with self.assertRaisesRegex(ValueError, "fixed B4 q2"):
            epoch.verify("b4-q1", self.extended)

    def test_tampered_sealed_files_rejected(self):
        for name in (epoch.ORIGINAL_DESIGN, epoch.ORIGINAL_CHECKER, epoch.EPOCH,
                     "count_protocol.py", "kernel.py", "contract.json", "FROZEN_DESIGN.json"):
            path = self.extended / name
            raw = path.read_bytes()
            path.write_bytes(raw+b" ")
            with self.subTest(name=name), self.assertRaises(ValueError):
                epoch.verify(epoch.TARGET, self.extended)
            path.write_bytes(raw)

    def test_missing_sealed_input_rejected(self):
        (self.extended / "kernel.py").unlink()
        with self.assertRaisesRegex(ValueError, "sealed inventory"):
            epoch.verify_capsule(self.extended)

    def test_extra_import_helper_or_directory_rejected(self):
        path = self.extended / "unbound_helper.py"
        path.write_text("raise AssertionError('unbound')\n")
        with self.assertRaisesRegex(ValueError, "sealed inventory"):
            epoch.verify_capsule(self.extended)
        path.unlink()
        path.mkdir()
        with self.assertRaisesRegex(ValueError, "flat regular"):
            epoch.verify_capsule(self.extended)

    def test_only_explicit_native_json_outputs_may_coexist(self):
        for name in ("COUNT29_FOREST.json", "COUNT29_ACCEPTED.json"):
            (self.extended / name).write_text("{}\n")
        self.assertEqual(len(epoch.verify_capsule(self.extended)), 7)

    def test_patch_rejects_multiple_assignment_or_mathematical_use(self):
        raw = self.payload["count_protocol.py"]
        for bad in (raw+b"LIMIT=10000\n", raw.replace(b"LIMIT=10000", b"LIMIT=True"),
                    raw.replace(b"LIMIT=10000", b"LIMIT = 10000"), raw+b"x=LIMIT+1\n"):
            with self.subTest(bad=bad[-50:]), self.assertRaises(ValueError):
                epoch._patch(bad)

    def test_full_census_and_source_pin(self):
        forest = self.forest()
        self.assertEqual(epoch.forest_census(forest, epoch.TARGET, self.extended),
                         dict(nodes=26, leaves=26, roots=26))
        forest["checker_sha256"] = self.checker_pin
        with self.assertRaisesRegex(ValueError, "checker_sha256"):
            epoch.forest_census(forest, epoch.TARGET, self.extended)

    def test_over_old_cap_but_below_new_cap_is_topologically_eligible(self):
        forest = self.forest()
        node = forest["roots"][0]["tree"]
        for _ in range(13):
            node = dict(kind="split", axis=0, cut="1/2", left=node, right=deepcopy(node))
        forest["roots"][0]["tree"] = node
        self.assertEqual(epoch.forest_census(forest, epoch.TARGET, self.extended),
                         dict(nodes=16408, leaves=8217, roots=26))

    def test_pending_boolean_axis_missing_root_and_depth_rejected(self):
        for kind in ("pending", "axis", "root", "depth"):
            forest = self.forest()
            if kind == "pending":
                forest["roots"][0]["tree"] = {"kind": "pending"}
            elif kind == "root":
                forest["roots"][0]["k"] = False
            elif kind == "axis":
                leaf = forest["roots"][0]["tree"]
                forest["roots"][0]["tree"] = dict(kind="split", axis=True, cut="1/2", left=leaf, right=deepcopy(leaf))
            else:
                node = forest["roots"][0]["tree"]
                for _ in range(129):
                    node = dict(kind="split", axis=0, cut="1/2", left=node,
                                right=dict(kind="leaf", box=[], decision="TRAP", result={}))
                forest["roots"][0]["tree"] = node
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                epoch.forest_census(forest, epoch.TARGET, self.extended)

    def test_new_cap_still_enforced(self):
        forest = self.forest()
        leaf = forest["roots"][0]["tree"]
        forest["roots"][0]["tree"] = dict(kind="split", axis=0, cut="1/2", left=leaf, right=deepcopy(leaf))
        with patch.object(epoch, "verify", return_value={}), patch.object(epoch, "NODE_LIMIT", 26):
            with self.assertRaisesRegex(ValueError, "finite native tree limits"):
                epoch.forest_census(forest, epoch.TARGET, self.extended)


if __name__ == "__main__":
    unittest.main()
