"""Tiny source/ZIP/geometry fixtures; archived mathematical code is a tripwire."""
from copy import deepcopy
import json
from pathlib import Path
import stat
import tempfile
import unittest
import warnings
import zipfile
from unittest.mock import patch

from be_replay import retained_n25_sources as sources, count_task as common


class RetainedSourcesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.archive = self.root/"fixture.zip"
        self.catalog = self.root/"catalog.json"
        self.task = self.root/"task"
        self.payloads, rows = {}, []
        for branch, index, rho in (("b0", 37, ["1", "11/10"]), ("b1", 32, ["11/10", "6/5"]),
                                   ("b2", 28, ["6/5", "13/10"])):
            identity = branch+"-p"+str(index)
            prefix = "cutoff25_20261011/new_root/fixture_"+branch+"/"
            schema = "TRAP_RETAINED_"+branch.upper()+"_V1"
            protocol = ("raise AssertionError('mathematical protocol must never be imported')\n"
                        "LIMIT=10000\ndef header(bound):return dict(schema="+repr(schema)+",n=25,index="+str(index)+")\n").encode()
            contract = dict(rows=[dict(n=25, index=index, K="0", p=["0", "1"], rho_lower=rho[0],
                                      rho_upper=rho[1], Lambda="1", d0="1")])
            files = {"count_protocol.py": protocol, "contract.json": sources.encoded(contract),
                     "kernel.py": b"raise AssertionError('kernel must never be imported')\n",
                     "provenance.txt": b"Additional frozen source bytes\r\n"}
            kernel = {"kernel.py": sources.sha(files["kernel.py"])}
            files["KERNEL_COPY_MANIFEST.json"] = sources.encoded(dict(files=kernel))
            design = sources.encoded(dict(status="FROZEN_SOURCE_ONLY", scope="No acceptance", files={k: sources.sha(v) for k, v in files.items()}))
            files["FROZEN_DESIGN.json"] = design
            box = [["0", "1"], ["0", "1"], ["0", "1"], ["-1/2", "1/2"], ["0", "1"]]
            forest = dict(schema=schema, n=25, index=index, target="1/2",
                contract_sha256=sources.sha(files["contract.json"]), checker_sha256=sources.sha(protocol),
                kernel_sha256=kernel, roots=[dict(k=k, tree=dict(kind="leaf", box=deepcopy(box),
                decision="EMPTY_FIXTURE", result={"status": "EMPTY_FIXTURE"})) for k in range(26)])
            forestname, accepted = f"COUNT{index}_FOREST.json", f"COUNT{index}_ACCEPTED.json"
            forest_raw = sources.encoded(forest)
            self.payloads.update({prefix+name: raw for name, raw in files.items()})
            self.payloads[prefix+forestname] = forest_raw
            self.payloads[prefix+accepted] = b'{"status":"OLD_PASS_NOT_FRESH"}\n'
            rows.append(dict(branch=branch, target_id=identity, archive_key="old", capsule_member_prefix=prefix,
                availability="SELECTED_SOURCE_AND_CANDIDATE_FOUND", historical_acceptance_is_fresh_evidence=False,
                source_file_rows=[dict(filename=k, member=prefix+k, sha256=sources.sha(v), bytes=len(v))
                                  for k, v in files.items() if k not in ("FROZEN_DESIGN.json", "provenance.txt")],
                source_epoch_manifest_filename="FROZEN_DESIGN.json", source_epoch_manifest_sha256=sources.sha(design),
                source_epoch_declared_file_count=5, forest_filename=forestname, acceptance_filename=accepted,
                forest_sha256=sources.sha(forest_raw), contract_sha256=sources.sha(files["contract.json"]),
                checker_sha256=sources.sha(protocol), manifest_filename="KERNEL_COPY_MANIFEST.json",
                manifest_sha256=sources.sha(files["KERNEL_COPY_MANIFEST.json"]), kernel_file_count=1,
                index=index, n=25, p_interval=["0", "1"], rho_interval=rho, forest_schema=schema,
                node_count=26, leaf_count=26, split_count=0, expected_selected_leaves=26))
        self.data = dict(schema="N25_RETAINED_B012_SELECTED_COUNT_CATALOG_V1", jobs=rows)
        self.patches = [patch.object(sources, "CATALOG", self.catalog),
                        patch.object(sources, "EXPECTED_COUNTS", {"b0": 1, "b1": 1, "b2": 1}),
                        patch.object(common, "ASSETS", deepcopy(common.ASSETS))]
        for p in self.patches:
            p.start()
        self.write_catalog()
        self.write_archive()

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.temporary.cleanup()

    def write_catalog(self):
        raw = sources.encoded(self.data)
        self.catalog.write_bytes(raw)
        if hasattr(self, "catalog_pin"):
            self.catalog_pin.stop()
            self.patches.remove(self.catalog_pin)
        self.catalog_pin = patch.object(sources, "CATALOG_SHA256", sources.sha(raw))
        self.catalog_pin.start()
        self.patches.append(self.catalog_pin)

    def write_archive(self, extra=(), symlink=None):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.archive, "w") as zipped:
                for name, raw in self.payloads.items():
                    if name == symlink:
                        info = zipfile.ZipInfo(name)
                        info.create_system = 3
                        info.external_attr = (stat.S_IFLNK | 0o777) << 16
                        zipped.writestr(info, raw)
                    else:
                        zipped.writestr(name, raw)
                for name, raw in extra:
                    zipped.writestr(name, raw)
        raw = self.archive.read_bytes()
        common.ASSETS["old"] = dict(name="fixture.zip", bytes=len(raw), sha256=sources.sha(raw))

    def prepare(self):
        return sources.prepare("b0", self.archive, self.task)

    def job(self):
        return sources.jobs("b0")[0]

    def test_extracts_full_design_and_candidate_without_old_acceptance(self):
        manifest = self.prepare()
        job = self.job()
        capsule = self.task/job["capsule_relative"]
        self.assertEqual(len(manifest["jobs"]), 1)
        self.assertEqual(len(manifest["jobs"][0]["files"]), 7)
        self.assertEqual((capsule/"provenance.txt").read_bytes(), b"Additional frozen source bytes\r\n")
        self.assertFalse((capsule/job["acceptance_filename"]).exists())
        self.assertEqual(sources.verify(self.task), manifest)
        self.assertEqual(sources.census(job, capsule), dict(roots=26, nodes=26, leaves=26, splits=0,
                         maximum_depth=0, closed_statuses={"EMPTY_FIXTURE": 26}, maximum_score="0"))
        self.assertFalse(manifest["fresh_arithmetic_replayed"])

    def test_jobs_are_fixed_private_copies(self):
        job = self.job()
        job["index"] = 99
        self.assertEqual(self.job()["index"], 37)
        with self.assertRaises(ValueError):
            sources.jobs("b3")
        self.prepare()
        with self.assertRaisesRegex(ValueError, "literal catalog"):
            sources.census(job, self.task/self.job()["capsule_relative"])

    def test_catalog_pin_tampering_rejected(self):
        self.catalog.write_bytes(self.catalog.read_bytes()+b" ")
        with self.assertRaisesRegex(ValueError, "pinned complete"):
            self.prepare()
        self.assertFalse(self.task.exists())

    def test_transport_pin_checked_before_extraction(self):
        with self.archive.open("ab") as stream:
            stream.write(b"bad transport")
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertFalse(self.task.exists())

    def test_duplicate_and_case_collision_rejected_before_mutation(self):
        member = self.job()["capsule_member_prefix"]+"FROZEN_DESIGN.json"
        for name in (member, member.upper()):
            self.write_archive(extra=[(name, self.payloads[member])])
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "Unique exact-case"):
                self.prepare()
            self.assertFalse(self.task.exists())

    def test_selected_symlink_and_oversized_input_rejected(self):
        member = self.job()["capsule_member_prefix"]+"kernel.py"
        self.write_archive(symlink=member)
        with self.assertRaisesRegex(ValueError, "regular unencrypted"):
            self.prepare()
        self.assertFalse(self.task.exists())
        self.write_archive()
        with patch.object(sources, "MAX_SOURCE", 10):
            with self.assertRaisesRegex(ValueError, "regular unencrypted"):
                self.prepare()

    def test_traversal_catalog_member_rejected(self):
        self.data["jobs"][0]["capsule_member_prefix"] = "cutoff25_20261011/../../outside/"
        self.write_catalog()
        with self.assertRaisesRegex(ValueError, "archive-relative"):
            self.prepare()
        self.assertFalse(self.task.exists())

    def test_actual_source_hash_mismatch_never_writes_complete_manifest(self):
        member = self.job()["capsule_member_prefix"]+"kernel.py"
        self.payloads[member] = self.payloads[member].replace(b"kernel", b"KERNEL")
        self.write_archive()
        with self.assertRaisesRegex(ValueError, "SHA"):
            self.prepare()
        self.assertFalse((self.task/sources.MANIFEST).exists())

    def test_runtime_epochs_and_only_named_native_output_are_allowed(self):
        manifest = self.prepare()
        (self.task/"accept-0123456789ab"/"execution").mkdir(parents=True)
        (self.task/"JOB_RESULT.json").write_text("{}\n")
        (self.task/self.job()["capsule_relative"]/self.job()["acceptance_filename"]).write_text("{}\n")
        self.assertEqual(sources.verify(self.task), manifest)
        helper = self.task/self.job()["capsule_relative"]/"unbound.py"
        helper.write_text("raise AssertionError('must not import')\n")
        with self.assertRaisesRegex(ValueError, "sealed source"):
            sources.verify(self.task)

    def test_missing_source_or_extra_capsule_rejected(self):
        self.prepare()
        capsule = self.task/self.job()["capsule_relative"]
        raw = (capsule/"kernel.py").read_bytes()
        (capsule/"kernel.py").unlink()
        with self.assertRaises(ValueError):
            sources.verify(self.task)
        (capsule/"kernel.py").write_bytes(raw)
        (self.task/"capsules"/"arbitrary").mkdir()
        with self.assertRaisesRegex(ValueError, "selected branch capsules"):
            sources.verify(self.task)

    def test_source_or_manifest_tampering_rejected(self):
        self.prepare()
        capsule = self.task/self.job()["capsule_relative"]
        path = capsule/"contract.json"
        raw = path.read_bytes()
        path.write_bytes(raw+b" ")
        with self.assertRaises(ValueError):
            sources.verify(self.task)
        path.write_bytes(raw)
        (self.task/sources.MANIFEST).write_bytes((self.task/sources.MANIFEST).read_bytes()+b" ")
        with self.assertRaisesRegex(ValueError, "deterministic"):
            sources.verify(self.task)

    def test_prepare_never_overwrites_task(self):
        self.prepare()
        with self.assertRaisesRegex(ValueError, "Fresh private"):
            self.prepare()

    def test_wrong_leaf_geometry_rejected_without_oracle(self):
        self.prepare()
        job = self.job()
        path = self.task/job["capsule_relative"]/job["forest_filename"]
        forest = json.loads(path.read_bytes())
        forest["roots"][0]["tree"]["box"][0][0] = "1/2"
        raw = sources.encoded(forest)
        path.write_bytes(raw)
        self.data["jobs"][0]["forest_sha256"] = sources.sha(raw)
        self.write_catalog()
        with self.assertRaisesRegex(ValueError, "leaf geometry"):
            sources.census(self.job(), path.parent)

    def test_pending_root_rejected_without_oracle(self):
        self.prepare()
        job = self.job()
        path = self.task/job["capsule_relative"]/job["forest_filename"]
        forest = json.loads(path.read_bytes())
        forest["roots"][0]["tree"] = {"kind": "pending"}
        raw = sources.encoded(forest)
        path.write_bytes(raw)
        self.data["jobs"][0]["forest_sha256"] = sources.sha(raw)
        self.write_catalog()
        with self.assertRaisesRegex(ValueError, "leaf geometry"):
            sources.census(self.job(), path.parent)


if __name__ == "__main__":
    unittest.main()
