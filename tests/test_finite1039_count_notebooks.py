"""Six fixed notebook routes and source-only generation; no numerical imports."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("finite1039_builder", ROOT/"tools/make_finite1039_count_notebooks.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
PIN = "a"*40
EXPECTED = {"n10_14": (50,217), "n15_19": (51,147), "n20_24": (52,163),
            "n26_30": (53,80), "n31_34": (54,282), "n35_39": (55,120)}


def cell(doc, name):
    return "".join(next(c["source"] for c in doc["cells"] if c["id"] == name))


class Finite1039Notebooks(unittest.TestCase):
    def setUp(self):
        p=patch.object(builder,"ready_lanes",return_value=set(EXPECTED));p.start();self.addCleanup(p.stop)

    def test_all_six_exact_routes_scope_and_syntax(self):
        docs = builder.build_all(PIN)
        self.assertEqual(len(docs),6)
        self.assertEqual(sum(r[1] for r in EXPECTED.values()),1009)
        for lane,(number,count) in EXPECTED.items():
            name=f"{number}_{lane}_conditional_counts"
            doc=docs[name]
            self.assertEqual(doc["metadata"]["colab"]["name"],name+".ipynb")
            prose=" ".join(cell(doc,"instructions").split())
            for text in (f"all {count} selected forests", "every 20 seconds", "every 60 seconds", "partial numerical",
                         "BASIC", "2 GiB", "43,200", "54,000", "all-index theorem remain unverified", "flags remain false",
                         "entire newly generated acceptance receipt", "after the supervised process group stops"):
                self.assertIn(text,prose)
            self.assertIn("test_finite1039*.py",cell(doc,"finite1039-count-fixtures"))
            self.assertIn("test_linux_supervisor.py",cell(doc,"actual-linux-guard-tests"))
            self.assertIn('CODE_COMMIT = "'+PIN+'"',cell(doc,"pinned-code"))
            self.assertIn(f"run_colab({lane!r}, durable_root=DURABLE, backup_interval=60)",cell(doc,"execute-task"))
            if number<54:
                self.assertIn("count_protocol.py accept",prose)
            else:
                self.assertIn("own control count",prose)
                self.assertIn("flat split/leaf paths",prose)
            for c in doc["cells"]:
                if c["cell_type"]=="code":compile("".join(c["source"]),name,"exec")

    def test_fake_routing_preserves_conditional_flags(self):
        calls=[];module=types.ModuleType("be_replay.finite1039_counts")
        def fake(lane,**kwargs):
            calls.append((lane,kwargs))
            return dict(status=dict(state="synthetic",native_arithmetic_accepted=False,
                        full_finite1039_verified=False,all_index_conclusion_verified=False),bundle="synthetic.zip",work="synthetic")
        module.run_colab=fake
        with patch.dict(sys.modules,{module.__name__:module}):
            for lane in EXPECTED:
                namespace=dict(DURABLE=Path("/synthetic/durable"))
                exec(compile(cell(builder.build(PIN,lane),"execute-task"),"fake-route","exec"),namespace)
                self.assertIs(namespace["RESULT"]["status"]["native_arithmetic_accepted"],False)
                self.assertIs(namespace["RESULT"]["status"]["full_finite1039_verified"],False)
                self.assertIs(namespace["RESULT"]["status"]["all_index_conclusion_verified"],False)
        self.assertEqual(calls,[(lane,dict(durable_root=Path("/synthetic/durable"),backup_interval=60))for lane in EXPECTED])

    def test_selftest_failure_prevents_the_numeric_cell(self):
        class Child:
            stdout=["synthetic infrastructure failure\n"]
            def wait(self):return 1
        with tempfile.TemporaryDirectory()as temporary:
            process=types.SimpleNamespace(PIPE=object(),STDOUT=object(),Popen=lambda*a,**k:Child())
            namespace=dict(SELFTEST=Path(temporary)/"fixture.log",CODE=Path(temporary),subprocess=process,sys=sys)
            with redirect_stdout(io.StringIO()),self.assertRaisesRegex(RuntimeError,"computation will not start"):
                exec(compile(cell(builder.build(PIN,"n31_34"),"finite1039-count-fixtures"),"fake-fixture","exec"),namespace)
            self.assertNotIn("RESULT",namespace)

    def test_invalid_pin_and_lane_fail_before_output(self):
        with tempfile.TemporaryDirectory()as temporary:
            output=Path(temporary)/"absent"
            for pin in (None,"main","0"*40,"A"*40,"a"*39,"a"*41):
                with self.subTest(pin=pin),self.assertRaises(ValueError):builder.write(pin,output)
                self.assertFalse(output.exists())
        for lane in (True,False,10,"n25","n10-14","all",None):
            with self.subTest(lane=lane),self.assertRaises(ValueError):builder.build(PIN,lane)

    def test_exact_six_lf_outputs(self):
        with tempfile.TemporaryDirectory()as temporary:
            output=Path(temporary)/"generated";paths=builder.write(PIN,output)
            self.assertEqual({p.name for p in paths},{f"{n}_{lane}_conditional_counts.ipynb"for lane,(n,_)in EXPECTED.items()})
            self.assertEqual(len(list(output.iterdir())),6)
            for p in paths:
                raw=p.read_bytes();self.assertNotIn(b"\r",raw);self.assertTrue(raw.endswith(b"\n"))
                self.assertEqual(json.loads(raw)["metadata"]["colab"]["name"],p.name)

    def test_blocked_lane_has_no_runnable_placeholder(self):
        with patch.object(builder,"ready_lanes",return_value=set(EXPECTED)-{"n26_30"}):
            with self.assertRaisesRegex(ValueError,"not source-complete"):
                builder.build(PIN,"n26_30")
            with tempfile.TemporaryDirectory()as temporary:
                paths=builder.write(PIN,Path(temporary)/"generated")
                self.assertEqual(len(paths),5)
                self.assertFalse(any(p.name.startswith("53_")for p in paths))


if __name__=="__main__":unittest.main()
