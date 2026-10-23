"""Source preparation and malformed-archive fixtures; no numerical code runs."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

from be_replay import aux24_sources as sources
from be_replay import count_task as common


class Aux24SourceTests(unittest.TestCase):
    def setUp(self):
        parent = Path(sources.__file__).resolve().parents[1] / "work/aux24-source-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = self.root / "fixture.zip"
        self.prefix = sources.PREFIX + "continuation_20261010/fixture/"
        self.payloads = {
            self.prefix + "kernel.py": b"raise AssertionError('Numerical fixture must never execute')\n",
            self.prefix + "contract.json": b'{"n":22,"target":"9/10"}\n',
            self.prefix + "INITIAL_PROOF.json": b'{"schema":"untrusted-proof","value":"1/2"}\n',
            self.prefix + "candidate_31.json": b'{"roots":[],"not_accepted":true}\n',
            self.prefix + "POSITIVE23_JOINED.json": b'{"statement":"conditional predecessor"}\n',
            self.prefix + "HISTORICAL_ACCEPTED.json": b'{"status":"OLD_PASS"}\n',
        }
        with zipfile.ZipFile(self.path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in self.payloads.items():
                archive.writestr(name, data)
        self.asset = dict(name=self.path.name, tag="fixture", bytes=self.path.stat().st_size,
                          sha256=common.digest(self.path))
        self.addCleanup(patch.stopall)
        patch.object(sources, "ARCHIVE", self.asset).start()
        patch.dict(common.ASSETS, {"old": self.asset}).start()
        patch.object(common, "obtain_asset", return_value=self.path).start()
        self.members = {self.prefix + "kernel.py": "source", self.prefix + "contract.json": "source",
                        self.prefix + "INITIAL_PROOF.json": "candidate",
                        self.prefix + "candidate_31.json": "candidate",
                        self.prefix + "POSITIVE23_JOINED.json": "premise"}

    def prepare(self, name="task"):
        return sources.prepare(self.root / name, archives=self.root, members=self.members)

    def rewrite_archive(self, extra, *, mode=None):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.path, "a") as archive:
                for name, data in extra.items():
                    if mode is None:
                        archive.writestr(name, data)
                    else:
                        info = zipfile.ZipInfo(name)
                        info.create_system = 3
                        info.external_attr = mode << 16
                        archive.writestr(info, data)
        self.asset.update(bytes=self.path.stat().st_size, sha256=common.digest(self.path))

    def test_fresh_preparation_preserves_siblings_and_never_imports_trap_kernel(self):
        task = self.prepare()
        manifest = sources.verify_prepared(task)
        self.assertEqual(set(manifest["files"]), set(self.members))
        self.assertEqual(manifest["files"][self.prefix + "INITIAL_PROOF.json"]["kind"], "candidate")
        self.assertEqual(manifest["files"][self.prefix + "POSITIVE23_JOINED.json"]["kind"], "premise")
        self.assertFalse(manifest["mathematical_code_executed"])
        self.assertFalse(manifest["premises_acquired"])
        self.assertEqual(manifest["historical_acceptances_imported"], 0)
        for member in self.members:
            self.assertEqual((task / "source" / member).read_bytes(), self.payloads[member])
        self.assertFalse((sources.source_root(task) / "continuation_20261010/fixture/HISTORICAL_ACCEPTED.json").exists())

    def test_manifest_is_identical_across_local_paths_and_input_dictionary_order(self):
        first = self.prepare("first")
        second = sources.prepare(self.root / "second", archives=self.root,
                                 members=dict(reversed(list(self.members.items()))))
        self.assertEqual((first / sources.MANIFEST).read_bytes(), (second / sources.MANIFEST).read_bytes())
        pin = common.digest(first / sources.MANIFEST)
        sources.verify_prepared(second, pin)

    def test_restored_source_tree_is_path_independent_and_keeps_recorded_preparer_identity(self):
        import shutil
        first = self.prepare()
        restored = self.root / "restored"
        shutil.copytree(first, restored)
        pin = common.digest(first / sources.MANIFEST)
        record = common.read(first / sources.TASK)
        with patch.object(sources, "__file__", str(self.root / "later-preparer-code.py")):
            sources.verify_prepared(restored, pin, expected_preparer_sha=record["preparer_sha256"])
        self.assertEqual((first / sources.TASK).read_bytes(), (restored / sources.TASK).read_bytes())
        with self.assertRaisesRegex(ValueError, "recorded preparer"):
            sources.verify_prepared(restored, pin, expected_preparer_sha="0"*64)

    def test_inspection_is_exact_prefix_scoped_and_does_not_extract(self):
        inventory = sources.inspect_members(self.path, [self.prefix])
        self.assertEqual(set(inventory), set(self.payloads))
        for name, data in self.payloads.items():
            self.assertEqual(inventory[name], dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
        self.assertEqual(set(sources.inspect_members(self.path, [sources.PREFIX])), set(self.payloads))
        self.assertFalse((self.root / "source").exists())

    def test_historical_acceptance_and_optimization_receipts_cannot_be_imported_in_any_kind(self):
        for kind in sources.KINDS:
            for name in ("HISTORICAL_ACCEPTED.json", "OLD_ACCEPTANCE.json", "EXECUTION.json",
                         "OLD_RECEIPT.json", "COMPLETED.json", "OPTIMIZATION_EQUIVALENCE.json"):
                with self.subTest(kind=kind, name=name), self.assertRaisesRegex(ValueError, "Historical acceptance"):
                    sources.prepare(self.root / "bad", archives=self.root, members={self.prefix + name: kind})
        self.assertFalse((self.root / "bad").exists())

    def test_joined_statement_requires_explicit_candidate_or_conditional_premise(self):
        with self.assertRaisesRegex(ValueError, "explicit untrusted candidate"):
            sources.prepare(self.root / "bad", archives=self.root,
                            members={self.prefix + "POSITIVE23_JOINED.json": "source"})

    def test_candidate_code_and_unknown_classification_are_rejected(self):
        for kind in ("candidate", "premise", "accepted"):
            with self.assertRaises(ValueError):
                sources.prepare(self.root / "bad", archives=self.root, members={self.prefix + "kernel.py": kind})

    def test_missing_selected_member_fails_before_destination_creation(self):
        with self.assertRaisesRegex(ValueError, "Every exact selected"):
            sources.prepare(self.root / "bad", archives=self.root,
                            members={self.prefix + "missing.py": "source"})
        self.assertFalse((self.root / "bad").exists())

    def test_unsafe_names_and_case_collisions_are_rejected(self):
        unsafe = [sources.PREFIX + "../escape.py", sources.PREFIX + "x\\escape.py",
                  sources.PREFIX + "x:stream", sources.PREFIX + "x/CON.py",
                  sources.PREFIX + "x/name. ", "/absolute.py", sources.PREFIX + "x//code.py"]
        for name in unsafe:
            with self.subTest(name=name), self.assertRaises(ValueError):
                sources.prepare(self.root / "bad", archives=self.root, members={name: "source"})
        with self.assertRaisesRegex(ValueError, "case-insensitive"):
            sources.prepare(self.root / "bad", archives=self.root,
                            members={self.prefix + "Code.py": "source", self.prefix + "code.py": "source"})

    def test_duplicate_zip_member_is_rejected(self):
        self.rewrite_archive({self.prefix + "kernel.py": b"duplicate"})
        with self.assertRaisesRegex(ValueError, "duplicate selected"):
            self.prepare()

    def test_zip_symlink_and_member_size_limit_are_rejected(self):
        name = self.prefix + "link.py"
        self.rewrite_archive({name: b"outside"}, mode=stat.S_IFLNK | 0o777)
        with self.assertRaisesRegex(ValueError, "ordinary unencrypted"):
            sources.prepare(self.root / "link", archives=self.root, members={name: "source"})
        with patch.object(sources, "MAX_MEMBER", 4), self.assertRaisesRegex(ValueError, "Bounded ordinary"):
            self.prepare()

    def test_archive_pin_mismatch_is_rejected(self):
        with self.path.open("ab") as stream:
            stream.write(b"changed asset")
        with self.assertRaisesRegex(ValueError, "size/SHA mismatch"):
            self.prepare()

    def test_existing_task_is_not_overwritten(self):
        task = self.prepare()
        before = (task / sources.MANIFEST).read_bytes()
        with self.assertRaisesRegex(ValueError, "New private source task"):
            self.prepare()
        self.assertEqual((task / sources.MANIFEST).read_bytes(), before)

    def test_changed_or_missing_input_and_wrong_manifest_pin_fail_closed(self):
        task = self.prepare()
        with self.assertRaisesRegex(ValueError, "Expected exact"):
            sources.verify_prepared(task, "0"*64)
        path = task / "source" / (self.prefix + "kernel.py")
        path.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "Unchanged exact selected"):
            sources.verify_prepared(task)
        path.unlink()
        with self.assertRaisesRegex(ValueError, "Unchanged exact selected"):
            sources.verify_prepared(task)

    def test_only_named_fresh_outputs_are_allowed_and_never_accepted_by_preparation(self):
        task = self.prepare()
        relative = "continuation_20261010/fixture/FRESH_ACCEPTED.json"
        output = sources.source_root(task) / relative
        output.write_text('{"fixture":"new output; caller must validate"}')
        with self.assertRaisesRegex(ValueError, "No unknown"):
            sources.verify_prepared(task)
        manifest = sources.verify_prepared(task, outputs=[relative])
        self.assertFalse(manifest["premises_acquired"])
        self.assertNotIn(sources.PREFIX + relative, manifest["files"])
        (task / "own-ledger.json").write_text("{}")
        sources.verify_prepared(task, outputs=[relative])
        with self.assertRaises(ValueError):
            sources.verify_prepared(task, outputs=["../escape.json"])
        with self.assertRaisesRegex(ValueError, "distinct"):
            sources.verify_prepared(task, outputs=["continuation_20261010/fixture/INITIAL_PROOF.json"])

    def test_extra_empty_directory_or_old_output_is_rejected(self):
        task = self.prepare()
        extra = sources.source_root(task) / "injected"
        extra.mkdir()
        with self.assertRaisesRegex(ValueError, "unknown source tree directories"):
            sources.verify_prepared(task)
        extra.rmdir()
        (sources.source_root(task) / "OLD_ACCEPTED.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "No unknown"):
            sources.verify_prepared(task)


if __name__ == "__main__":
    unittest.main()
