"""Pure source/transport fixtures. Every synthetic original is an import trap."""
from copy import deepcopy
import json
from pathlib import Path
import stat
import tempfile
import unittest
import warnings
import zipfile
from unittest.mock import patch

from be_replay import n25_b5_reconstruction_sources as sources


def protocol(index=26):
    controls = ",".join("('case%d',lambda x:x.update(bad=%d))" % (i, i) for i in range(24))
    p = ["13/50", "27/100"] if index == 26 else ["33/100", "17/50"]
    return ("raise AssertionError('ORIGINAL MUST NEVER BE EXECUTED')\n"
        "from rho_signed_moment_tightener import cell35\n"
        "from optimized_arithmetic import CE_LO\nLIMIT=10000\n"
        "def load():\n contract={}\n cfg=contract['rows'][0]\n return cfg\n"
        "def rootbox(cfg):return cfg['p']\n"
        "def children(box,axis,cut):return box,box\n"
        "def evaluate(cfg,k,b):\n z={}\n return F(z['score_upper'])<CE_LO\n"
        "def replay(*args):return 'tripwire'\n"
        "def first(*args):return 'tripwire'\n"
        "def construct():\n need(depth<=128,'limit')\n return 'tripwire'\n"
        "def header(bound):return dict(schema="
        +repr(f"LOW25_B5_GLOBAL_ALPHA_STOPLOSS2_V12_PANEL{index}_RIGHT_HALF_CLOSED_COUNT_FOREST_V1")
        +",n=25,index="+str(index)+")\n"
        "def accept():\n mutations=["+controls+"]\n return dict(status="
        +repr(f"PASS_FRESH_CONDITIONAL_EXACT_COUNT{index}")+")\n"
        "P="+repr(p)+"\n").encode()


class ReconstructionSourcesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.plan_path = self.root/"plan.json"
        self.output = self.root/"output"
        self.target = "b5-p26-v14-new"
        self.paths = {k:self.root/(k+".zip") for k in ("old", "base13")}
        self.contents = {k:{} for k in self.paths}
        self.inputs = {}
        self.plan = dict(schema=sources.SCHEMA, archives={}, inputs={}, bases={}, helpers={},
                         analytic_inputs={}, mixed_recipe={}, profiles={}, **sources.FALSE_FLAGS)
        self.patches = [patch.object(sources, "PLAN", self.plan_path),
                        patch.object(sources, "TARGETS", (self.target,)),
                        patch.object(sources, "PLAN_SHA256", "fixture")]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)
        kernel = {"rho_signed_moment_tightener.py":b"raise AssertionError('kernel import trap')\n",
                  "optimized_arithmetic.py":b"raise AssertionError('kernel import trap')\n"}
        kernel.update({f"PROOF{i}.txt":f"Unchanged proof {i}\r\n".encode() for i in range(69)})
        self.kernel = kernel
        files = dict(kernel, **{"count_protocol.py":protocol(),
            "contract.json":sources.encoded(dict(branch=5, index=26, rows=[dict(n=25, index=26,
                p=["13/50", "27/100"], K="0", rho_lower="3/2", rho_upper="33/20", simultaneous="unchanged")],
                source_inputs_sha256={"old-parent":"f"*64})),
            "construct_alpha4.py":b"raise AssertionError('constructor import trap')\n",
            "SOURCE_PORT.json":b'{"old_provenance":true}\n',
            "KERNEL_COPY_MANIFEST.json":sources.encoded(dict(files={n:sources.sha(b) for n,b in kernel.items()}))})
        prefix = "cutoff25_20261011/base/"
        file_rows = {n:self.add("old", prefix+n, b) for n,b in files.items()}
        design = sources.encoded(dict(files={n:sources.sha(b) for n,b in files.items()}))
        self.plan["bases"]["26"] = dict(files=file_rows, design=self.add("old", prefix+"FROZEN_DESIGN.json", design))
        helpers = {"local_contact_v14.py":b"raise AssertionError('helper import trap')\n",
                   "local_contact_support.py":b"raise AssertionError('helper import trap')\n"}
        helpers.update({f"HELPER{i}.txt":b"Original helper proof\n" for i in range(19)})
        hp = "cutoff25_20261013/helpers/"
        self.plan["helpers"] = dict(files={n:self.add("base13",hp+n,b) for n,b in helpers.items()},
            manifest=self.add("base13",hp+"LOCAL_CONTACT_V14_ADDITIONS.json",
                              sources.encoded(dict(files={n:sources.sha(b) for n,b in helpers.items()}))))
        self.plan["analytic_inputs"] = {"ANALYTIC.txt":self.add("base13",hp+"ANALYTIC.txt",b"Conditional premise\n")}
        self.plan["profiles"][self.target] = dict(target=self.target, kind="ordinary-v14",n=25,index=26,base_index=26,
            native_schema="NEW_FIXTURE_SOURCE_ONLY",native_status="NEW_FIXTURE_NATIVE_STATUS",output_files={},
            provenance_files={},**sources.FALSE_FLAGS)
        payload, provenance = sources._derive(self.plan, self.inputs, self.target)
        self.plan["profiles"][self.target].update(output_files=sources._file_rows(payload),
                                                 provenance_files=sources._file_rows(provenance))
        self.write_archives()

    def add(self, key, name, raw):
        self.contents[key][name] = raw
        row = dict(archive_key=key,member=name,bytes=len(raw),sha256=sources.sha(raw))
        ident = sources._input_key(key,name)
        self.inputs[ident] = raw
        self.plan["inputs"][ident] = row
        return row

    def write_plan(self):
        raw = sources.encoded(self.plan)
        self.plan_path.write_bytes(raw)
        sources.PLAN_SHA256 = sources.sha(raw)

    def write_archives(self, extra=(), symlink=None):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            for key,path in self.paths.items():
                with zipfile.ZipFile(path,"w") as z:
                    for name,raw in self.contents[key].items():
                        if name == symlink:
                            info = zipfile.ZipInfo(name)
                            info.create_system = 3
                            info.external_attr = (stat.S_IFLNK | 0o777)<<16
                            z.writestr(info,raw)
                        else:
                            z.writestr(name,raw)
                    if key == "old":
                        for name,raw in extra:
                            z.writestr(name,raw)
                raw = path.read_bytes()
                self.plan["archives"][key] = dict(name=path.name,bytes=len(raw),sha256=sources.sha(raw))
        self.write_plan()

    def prepare(self):
        return sources.prepare(self.output,archives=self.paths)

    def test_memory_only_reconstruction_preserves_bytes_without_importing_traps(self):
        result = self.prepare()
        cap = self.output/"capsules"/self.target
        for name,raw in self.kernel.items():
            self.assertEqual((cap/name).read_bytes(),raw)
        new = sources.parsed((cap/"contract.json").read_bytes())
        old = sources.parsed((cap/"ORIGINAL_V12_CONTRACT.json").read_bytes())
        want = deepcopy(old)
        want["rows"][0].update(local_contact_allowance="5/16",local_contact_premise=deepcopy(sources.PREMISE))
        self.assertEqual(new,want)
        code = (cap/"count_protocol.py").read_text()
        self.assertIn("exact whole original physical contract plus two contact fields",code)
        self.assertIn("ORIGINAL_V12_CONTRACT.json",code)
        self.assertEqual(sources.verify(self.output)["targets"],[self.target])
        self.assertTrue(all(result[k] is False for k in sources.FALSE_FLAGS))
        self.assertFalse(any("FOREST" in p.name or "ACCEPTED" in p.name for p in cap.iterdir()))

    def test_quarter_changes_only_domain_and_matches_closed_seams(self):
        parent = dict(status="old", rows=[dict(n=25,index=33,p=["33/100","17/50"],K="0",D="unchanged")])
        seams = ["33/100","133/400","67/200","27/80","17/50"]
        for q in range(4):
            raw,code = sources._quarter(sources.encoded(parent),protocol(33),q)
            new = sources.parsed(raw)
            self.assertEqual(new["rows"][0],dict(parent["rows"][0],p=seams[q:q+2]))
            self.assertEqual(new["quarter_partition"]["source_contract_sha256"],sources.sha(sources.encoded(parent)))
            self.assertIn(("V12_Q%d_PANEL33"%q).encode(),code)

    def test_native_projection_rejects_changed_acceptor_or_missing_control(self):
        raw = protocol()
        changed = raw.replace(b"('case23',lambda x:x.update(bad=23))",b"('case23',lambda x:x.update(bad=23)),('extra',lambda x:x)")
        with self.assertRaisesRegex(ValueError,"All24"):
            sources._v14_protocol(changed,26,"NEW","PASS","ORIGINAL_V12_CONTRACT.json")
        after = sources._v14_protocol(raw,26,"NEW","PASS","ORIGINAL_V12_CONTRACT.json")
        altered = after.decode().replace("return cfg['p']","return []")
        with self.assertRaisesRegex(ValueError,"Unchanged native function"):
            sources._projection(raw.decode(),altered,"PASS_FRESH_CONDITIONAL_EXACT_COUNT26","PASS")

    def test_static_imports_fail_closed_and_never_execute(self):
        self.assertEqual(sources._imports({"trap.py":b"raise AssertionError('never execute')\n"}),[])
        for raw in [b"import subprocess\n", b"from missing_kernel import f\n", b"eval('1')\n",
                    b"__import__('os')\n",b"from . import missing\n"]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                sources._imports({"trap.py":raw})

    def test_external_plan_pin_and_false_flags_checked_before_writes(self):
        self.plan_path.write_bytes(self.plan_path.read_bytes()+b" ")
        with self.assertRaisesRegex(ValueError,"Externally pinned"):
            self.prepare()
        self.assertFalse(self.output.exists())
        self.plan["arithmetic_accepted"] = True
        self.write_plan()
        with self.assertRaisesRegex(ValueError,"false proof flags"):
            self.prepare()
        self.assertFalse(self.output.exists())

    def test_archive_size_or_sha_tampering_never_writes(self):
        with self.paths["old"].open("ab") as stream:
            stream.write(b"tampered")
        with self.assertRaisesRegex(ValueError,"transport size"):
            self.prepare()
        self.assertFalse(self.output.exists())
        self.plan["archives"]["old"]["bytes"] += len(b"tampered")
        self.write_plan()
        with self.assertRaisesRegex(ValueError,"archive SHA256"):
            self.prepare()
        self.assertFalse(self.output.exists())

    def test_duplicate_case_and_traversal_archive_entries_reject(self):
        member = next(iter(self.contents["old"]))
        for name in [member,member.upper(),"cutoff25_20261011/../escape.py","/absolute.py"]:
            with self.subTest(name=name):
                self.write_archives(extra=[(name,b"bad")])
                with self.assertRaises(ValueError):
                    self.prepare()
                self.assertFalse(self.output.exists())

    def test_zip_symlink_rejected_before_write(self):
        member = next(iter(self.contents["old"]))
        self.write_archives(symlink=member)
        with self.assertRaisesRegex(ValueError,"symlink"):
            self.prepare()
        self.assertFalse(self.output.exists())

    def test_selected_member_corruption_rejects_even_with_new_archive_hash(self):
        member = next(iter(self.contents["old"]))
        self.contents["old"][member] += b"#changed\n"
        self.write_archives()
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertFalse(self.output.exists())

    def test_complete_derivation_precedes_any_output_mutation(self):
        with patch.object(sources,"_derive_selected",side_effect=ValueError("late derivation failure")):
            with self.assertRaisesRegex(ValueError,"late derivation"):
                self.prepare()
        self.assertFalse(self.output.exists())

    def test_unknown_duplicate_targets_and_overwrite_reject(self):
        for selected in [["unreviewed"],[self.target,self.target],[]]:
            with self.subTest(selected=selected), self.assertRaises(ValueError):
                sources.prepare(self.output,archives=self.paths,targets=selected)
        self.output.mkdir()
        marker=self.output/"keep.txt"
        marker.write_bytes(b"unchanged")
        with self.assertRaisesRegex(ValueError,"no overwrite"):
            self.prepare()
        self.assertEqual(marker.read_bytes(),b"unchanged")

    def test_new_output_pins_cannot_be_silently_rebound(self):
        self.plan["profiles"][self.target]["output_files"]["count_protocol.py"]["sha256"]="0"*64
        self.write_plan()
        with self.assertRaisesRegex(ValueError,"complete derived output"):
            self.prepare()
        self.assertFalse(self.output.exists())

    def test_prepared_source_tampering_unknown_output_and_flags_rejected(self):
        self.prepare()
        cap=self.output/"capsules"/self.target
        file=cap/"count_protocol.py"
        original=file.read_bytes()
        file.write_bytes(original+b"# changed\n")
        with self.assertRaisesRegex(ValueError,"sealed source bytes"):
            sources.verify(self.output)
        file.write_bytes(original)
        extra=cap/"COUNT26_ACCEPTED.json"
        extra.write_bytes(b'{"status":"FAKE_PASS"}')
        with self.assertRaisesRegex(ValueError,"source-only inventory"):
            sources.verify(self.output)
        extra.unlink()
        m=self.output/sources.MANIFEST
        data=sources.parsed(m.read_bytes());data["arithmetic_accepted"]=True;m.write_bytes(sources.encoded(data))
        with self.assertRaisesRegex(ValueError,"false proof flags"):
            sources.verify(self.output)

    def test_preparation_builder_and_execution_claims_are_bound(self):
        self.prepare()
        p=self.output/sources.PREPARATION
        original=p.read_bytes()
        for key,value in [("source_builder_sha256","0"*64),("original_modules_imported",True),
                          ("native_acceptance_run",True)]:
            record=sources.parsed(original);record[key]=value;p.write_bytes(sources.encoded(record))
            with self.subTest(key=key), self.assertRaisesRegex(ValueError,"source-only preparation"):
                sources.verify(self.output)
        p.write_bytes(original)
        self.assertEqual(sources.verify(self.output)["targets"],[self.target])

    def test_case_colliding_output_names_rejected(self):
        with self.assertRaisesRegex(ValueError,"Unique bounded"):
            sources._add({"original.json":b"{}"},"ORIGINAL.json",b"{}")


class PublishedPlanShapeTests(unittest.TestCase):
    def test_fixed_thirteen_profiles_and_exact_quarter_input_identities(self):
        rows=sources.profiles()
        self.assertEqual(len(rows),13)
        self.assertEqual(sum(s["kind"]=="ordinary-v14" for s in rows.values()),7)
        self.assertEqual(sum(s["kind"]=="quarter-v12" for s in rows.values()),4)
        self.assertEqual(sum(s["kind"]=="mixed-parent-v14" for s in rows.values()),2)
        for target,spec in rows.items():
            self.assertTrue(all(spec[k] is False for k in sources.FALSE_FLAGS))
            self.assertEqual(spec["requires_new_mixed_metadata_adapter"],spec["kind"]=="mixed-parent-v14")
            if spec["kind"]=="quarter-v12":
                self.assertEqual(spec["contract_sha256"],spec["historical_contract_sha256"])
                self.assertEqual(spec["checker_sha256"],spec["historical_checker_sha256"])


if __name__ == "__main__":
    unittest.main()
