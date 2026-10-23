"""Synthetic seven-target hint ZIP tests; no preparer, kernel, or arithmetic runs.

Only the downloadable asset pin is replaced by a fixture pin.  The real ZIP
validation, literal-header reader, and checkpoint source-binding checks run.
The historical design pins below intentionally do not follow current TARGETS.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import warnings
import zipfile
from unittest.mock import patch

from be_replay import count_task as count


PUBLISHED_DESIGNS = {
    "b4-q0": "4d91657ddbab41e3324c00f9f28a9223526c0c1dc79bad5c5e77176240c231f7",
    "b4-q1": "a3cbdb1852bc51054ecc8cd3c71bd1c7121b6b201385e481b73195ad729189c4",
    "b4-q2": "2517c1b8c79949bad93eecdcaa43e389344411fd4c71d5d516dde1e40b732e2a",
    "b4-q3": "c8555b500c3e7d1ca1240b5f229f7fff5ed307571012209e022431ecd195b7ac",
    "b3-p33": "e55bb3eeac06923f897263a65f2cde9fe77006313dd86f47bbba3f6047f30f08",
    "b3-p31-v14-new": "6ca73188c5a6969c1f0ec69f41cb0fac660003cf0515fdcadeeda83afcf654f0",
    "b3-p32-v14-new": "230a6bb37696c1e79d62847d89090d4187d78d41aa6c98ccbe91c54e1f8f950b",
}
ORIGINAL_TARGETS = ("b4-q0", "b4-q1", "b4-q2", "b4-q3", "b3-p33")
V14_TARGETS = ("b3-p31-v14-new", "b3-p32-v14-new")


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


class PublishedHintsTests(unittest.TestCase):
    def setUp(self):
        # Keep temporary test artifacts in the repository's ignored work area.
        parent = count.ROOT / "work" / "published-hints-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.serial = 0
        self.targets = dict(count.TARGETS)
        for target in ORIGINAL_TARGETS:
            kind, index, _ = self.targets[target]
            self.targets[target] = (kind, index, PUBLISHED_DESIGNS[target])
        # Simulate two explicitly changed executable epochs.  The historical
        # archive still contains the old, immutable seven-target manifest.
        for target, pin in zip(V14_TARGETS, ("1" * 64, "2" * 64)):
            kind, index, _ = self.targets[target]
            self.targets[target] = (kind, index, pin)
        self.target_patch = patch.object(count, "TARGETS", self.targets)
        self.target_patch.start()
        self.addCleanup(self.target_patch.stop)
        self.capsules = {}
        self.checkpoints = {}
        for target, (_, index, _) in self.targets.items():
            capsule = self.root / target
            capsule.mkdir()
            # These files are read/hash-bound only.  Importing either fixture
            # executable would fail, which also detects accidental execution.
            (capsule / "count_protocol.py").write_text(
                "raise AssertionError('fixture protocol must never execute')\n"
                "def header(bound):\n"
                "    return dict(schema=" + repr("FIXTURE_HINT_" + target) +
                ", n=25, index=" + str(index) + ")\n", encoding="utf-8")
            (capsule / "contract.json").write_bytes(encoded(dict(fixture=target, index=index)))
            (capsule / "kernel.py").write_text(
                "raise AssertionError('fixture kernel must never execute')\n", encoding="utf-8")
            (capsule / "KERNEL_COPY_MANIFEST.json").write_bytes(encoded(
                dict(files={"kernel.py": count.digest(capsule / "kernel.py")})))
            self.capsules[target] = capsule
            self.checkpoints[target] = dict(
                schema="UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1", arithmetic_accepted=False,
                binding=dict(design_sha256=PUBLISHED_DESIGNS[target], alpha_priority="4",
                             native_header=count.native_header(capsule, target)),
                roots=[dict(k=k, tree={"kind": "pending"}) for k in range(26)])

    def destination(self):
        self.serial += 1
        return self.root / ("selected-" + str(self.serial) + ".json")

    def archive(self, *, packets=None, mutate_manifest=None, omit=(), extra=(), duplicate=None,
                manifest_bytes=None):
        packets = self.checkpoints if packets is None else packets
        payloads = {"checkpoints/" + target + "/CHECKPOINT.json": encoded(packets[target])
                    for target in self.targets}
        manifest = dict(schema="UNTRUSTED_COUNT_SEARCH_HINTS_V1", arithmetic_accepted=False,
                        targets={})
        for target in self.targets:
            member = "checkpoints/" + target + "/CHECKPOINT.json"
            raw = payloads[member]
            manifest["targets"][target] = dict(member=member, design_sha256=PUBLISHED_DESIGNS[target],
                                                bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        if mutate_manifest is not None:
            mutate_manifest(manifest)
        payloads["manifest.json"] = encoded(manifest) if manifest_bytes is None else manifest_bytes
        self.serial += 1
        path = self.root / ("hints-" + str(self.serial) + ".zip")
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
            for name, raw in payloads.items():
                if name not in omit:
                    zipped.writestr(name, raw)
            for name, raw in extra:
                zipped.writestr(name, raw)
            if duplicate is not None:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    zipped.writestr(duplicate, payloads[duplicate])
        return path

    def asset_pin(self, archive):
        return dict(name=archive.name, bytes=archive.stat().st_size, sha256=count.digest(archive))

    def extract(self, archive, target="b3-p33", *, output=None, asset=None):
        output = self.destination() if output is None else output
        assets = dict(count.ASSETS, hints=self.asset_pin(archive) if asset is None else asset)
        with patch.object(count, "ASSETS", assets):
            return count.extract_published_hint(archive, target, self.capsules[target], output)

    def reject(self, archive, message, target="b3-p33", *, asset=None):
        output = self.destination()
        with self.assertRaisesRegex(ValueError, message):
            self.extract(archive, target, output=output, asset=asset)
        self.assertFalse(output.exists(), "Rejected hints must not produce a checkpoint")

    def test_historical_manifest_pins_are_literal_and_independent_of_current_v14(self):
        self.assertEqual(count.PUBLISHED_HINT_DESIGNS, PUBLISHED_DESIGNS)
        self.assertEqual(set(count.TARGETS), set(PUBLISHED_DESIGNS))
        for target in V14_TARGETS:
            self.assertNotEqual(count.TARGETS[target][2], PUBLISHED_DESIGNS[target])

    def test_original_five_load_after_both_current_v14_pins_change(self):
        archive = self.archive()
        for target in ORIGINAL_TARGETS:
            with self.subTest(target=target):
                result = self.extract(archive, target)
                self.assertEqual(result.read_bytes(), encoded(self.checkpoints[target]))
                packet = count.read(result)
                self.assertIs(packet["arithmetic_accepted"], False)
                self.assertEqual(len(packet["roots"]), 26)
                self.assertTrue(all(root["tree"]["kind"] == "pending" for root in packet["roots"]))

    def test_old_v14_hints_cannot_cross_into_either_new_executable_epoch(self):
        archive = self.archive()
        for target in V14_TARGETS:
            with self.subTest(target=target):
                self.reject(archive, "different executable source epoch", target)

    def test_foreign_unselected_historical_design_is_rejected(self):
        # Selecting an unchanged target must still validate the whole old map.
        for target in self.targets:
            with self.subTest(foreign_row=target):
                archive = self.archive(mutate_manifest=lambda m, t=target:
                                       m["targets"][t].update(design_sha256="f" * 64))
                self.reject(archive, "exact historical source epoch")

    def test_current_v14_pins_cannot_be_substituted_into_historical_manifest(self):
        for target in V14_TARGETS:
            with self.subTest(target=target):
                archive = self.archive(mutate_manifest=lambda m, t=target:
                                       m["targets"][t].update(design_sha256=self.targets[t][2]))
                self.reject(archive, "exact historical source epoch")

    def test_foreign_unselected_member_path_is_rejected(self):
        archive = self.archive(mutate_manifest=lambda m:
                               m["targets"][V14_TARGETS[0]].update(member="checkpoints/b3-p33/CHECKPOINT.json"))
        self.reject(archive, "exact historical source epoch")

    def test_selected_header_requires_actual_contract_checker_and_kernel_binding(self):
        changes = {
            "contract": lambda h: h.update(contract_sha256="0" * 64),
            "checker": lambda h: h.update(checker_sha256="0" * 64),
            "kernel": lambda h: h.update(kernel_sha256={"kernel.py": "0" * 64}),
            "missing_kernel": lambda h: h.pop("kernel_sha256"),
            "schema": lambda h: h.update(schema="FOREIGN_HEADER"),
            "n": lambda h: h.update(n=24),
            "index": lambda h: h.update(index=32),
        }
        for name, change in changes.items():
            with self.subTest(binding=name):
                packets = deepcopy(self.checkpoints)
                change(packets["b3-p33"]["binding"]["native_header"])
                # Re-pin bytes and SHA in the fixture ZIP so a rejection must
                # come from the real native source/header comparison.
                self.reject(self.archive(packets=packets), "native contract/header/kernel binding")

    def test_changed_local_contract_or_checker_cannot_resume_published_hint(self):
        archive = self.archive()
        capsule = self.capsules["b3-p33"]
        for name in ("contract.json", "count_protocol.py"):
            with self.subTest(source=name):
                path = capsule / name
                original = path.read_bytes()
                try:
                    path.write_bytes(original + b"\n")
                    self.reject(archive, "native contract/header/kernel binding")
                finally:
                    path.write_bytes(original)

    def test_selected_checkpoint_requires_current_design_strategy_and_all_ordered_roots(self):
        changes = {
            "foreign_design": lambda p: p["binding"].update(design_sha256="0" * 64),
            "foreign_strategy": lambda p: p["binding"].update(alpha_priority="3"),
            "missing_root": lambda p: p["roots"].pop(),
            "duplicate_root": lambda p: p["roots"][1].update(k=0),
            "boolean_root": lambda p: p["roots"][0].update(k=False),
            "reordered_roots": lambda p: p["roots"].reverse(),
            "accepted_marker": lambda p: p.update(arithmetic_accepted=True),
        }
        for name, change in changes.items():
            with self.subTest(checkpoint=name):
                packets = deepcopy(self.checkpoints)
                change(packets["b3-p33"])
                self.reject(self.archive(packets=packets),
                            "source epoch and strategy|ordered original roots|explicitly untrusted")

    def test_selected_payload_requires_exact_size_and_hash(self):
        changes = {
            "wrong_sha": lambda row: row.update(sha256="0" * 64),
            "wrong_size": lambda row: row.update(bytes=row["bytes"] + 1),
            "boolean_size": lambda row: row.update(bytes=True),
        }
        for name, change in changes.items():
            with self.subTest(payload=name):
                archive = self.archive(mutate_manifest=lambda m, change=change:
                                       change(m["targets"]["b3-p33"]))
                self.reject(archive, "Exact selected hint payload")

    def test_complete_exact_member_inventory_is_required(self):
        member = "checkpoints/" + V14_TARGETS[0] + "/CHECKPOINT.json"
        archives = (
            self.archive(omit=(member,)),
            self.archive(extra=(("extra.json", b"{}"),)),
            self.archive(duplicate=member),
        )
        for archive in archives:
            with self.subTest(archive=archive.name):
                self.reject(archive, "eight unique pinned hint members")

    def test_manifest_cannot_be_acceptance_record_or_omit_any_target(self):
        changes = (
            lambda m: m.update(arithmetic_accepted=True),
            lambda m: m.update(schema="FOREIGN_HINTS"),
            lambda m: m["targets"].pop(V14_TARGETS[0]),
        )
        for change in changes:
            with self.subTest(change=change):
                self.reject(self.archive(mutate_manifest=change), "All seven hints")

    def test_duplicate_json_keys_are_rejected(self):
        archive = self.archive(manifest_bytes=b'{"schema":"x","schema":"y"}')
        self.reject(archive, "Duplicate JSON key")

    def test_full_archive_pin_is_checked_before_loading_any_hint(self):
        archive = self.archive()
        asset = self.asset_pin(archive)
        with archive.open("ab") as stream:
            stream.write(b"changed archive bytes")
        self.reject(archive, "Pinned source asset size/SHA mismatch", asset=asset)

    def test_existing_checkpoint_output_is_never_overwritten(self):
        output = self.destination()
        original = b"existing evidence must remain byte-identical\n"
        output.write_bytes(original)
        with self.assertRaises(FileExistsError):
            self.extract(self.archive(), output=output)
        self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
