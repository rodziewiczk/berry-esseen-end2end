"""Memory-counter infrastructure only. No mathematical kernel is imported."""
import ast
import json
from pathlib import Path
import subprocess
import sys
import unittest
from be_replay import n5_remaining_bridge as bridge,n5_remaining_sources as src


def original_guard(status,native=None):
    """Compile only three original infrastructure functions, never its main."""
    tree=ast.parse(bridge.derive((src.VENDOR/"run_reproduction.py").read_bytes()))
    body=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in("require","own_peak","parent_guard")]
    class Status:
        def read_text(self,encoding):
            if encoding!="ascii":raise AssertionError("ASCII proc memory format")
            return status
    namespace=dict(NATIVE=native,Path=Path if status is None else lambda p:Status(),linux_peak_from_status=bridge.linux_peak_from_status,
                   MIB=1024**2,HOST_FLOOR=1024**3,available_ram=lambda:8*1024**3)
    exec(compile(ast.Module(body=body,type_ignores=[]),"original_guard_functions_only","exec"),namespace)
    return namespace


class BridgeMemory(unittest.TestCase):
    def test_positive_unique_current_exec_counters_and_same_cap(self):
        text="Name:\tpython\nVmHWM:\t65536 kB\nVmRSS:\t12345 kB\n"
        self.assertEqual(bridge.linux_peak_from_status(text),64*1024**2)
        original_guard(text)["parent_guard"]()
        with self.assertRaisesRegex(RuntimeError,"exceeds64MiB"):
            original_guard(text.replace("65536","65537"))["parent_guard"]()
        for bad in("VmHWM: 0 kB\nVmRSS: 1 kB\n","VmHWM: 1 kB\nVmRSS: 2 kB\n",
                    "VmHWM: 3 kB\nVmHWM: 4 kB\nVmRSS: 1 kB\n","VmHWM: 3 MB\nVmRSS: 1 kB\n",
                    "VmHWM: 3 kB\n","VmHWM: -1 kB\nVmRSS: 1 kB\n","VmHWM: 3 kB\nVmRSS: True kB\n"):
            with self.subTest(bad=bad),self.assertRaises(RuntimeError):bridge.linux_peak_from_status(bad)
        for bad in(None,b"VmHWM: 3 kB\nVmRSS: 1 kB\n","x"*300000):
            with self.assertRaises(RuntimeError):bridge.linux_peak_from_status(bad)
    def test_windows_native_peak_path_is_unchanged(self):
        class Native:
            def peak(self):return 123456
        self.assertEqual(original_guard("deliberately malformed Linux status",Native())["own_peak"](),123456)
    @unittest.skipUnless(sys.platform=="linux","Actual Linux exec/proc memory-counter fixture")
    def test_linux_preexec_peak_is_separate_and_postexec_growth_rejected(self):
        child='''import json,resource,sys
from pathlib import Path
from be_replay.n5_remaining_bridge import linux_peak_from_status
sys.path.insert(0,str(Path.cwd()/'tests'))
from test_n5_remaining_bridge import original_guard
if sys.argv[1]=='post':
    blob=bytearray(96*1024**2)
    for i in range(0,len(blob),4096):blob[i]=1
peak=linux_peak_from_status(Path('/proc/self/status').read_text('ascii'))
ru=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)*1024
try:
    original_guard(None)['parent_guard']()
    rejected=False
except RuntimeError as exc:
    if 'exceeds64MiB'not in str(exc):raise
    rejected=True
print(json.dumps(dict(ru_maxrss=ru,current_exec_peak=peak,guard_rejects=rejected)))
'''
        launcher="""import os,sys
blob=bytearray(96*1024**2)
for i in range(0,len(blob),4096):blob[i]=1
os.execv(sys.executable,[sys.executable,'-B','-S','-c',sys.argv[1],'pre'])
"""
        args=[sys.executable,"-B","-S","-c",launcher,child]
        pre=subprocess.run(args,cwd=src.ROOT,capture_output=True,text=True,timeout=20,check=True)
        self.assertEqual(pre.stderr,"");a=json.loads(pre.stdout)
        self.assertGreaterEqual(a["ru_maxrss"],96*1024**2);self.assertLessEqual(a["current_exec_peak"],64*1024**2)
        self.assertFalse(a["guard_rejects"])
        post=subprocess.run([sys.executable,"-B","-S","-c",child,"post"],cwd=src.ROOT,
                            capture_output=True,text=True,timeout=20,check=True)
        self.assertEqual(post.stderr,"");b=json.loads(post.stdout)
        self.assertGreater(b["current_exec_peak"],64*1024**2);self.assertTrue(b["guard_rejects"])


if __name__=="__main__":unittest.main()
