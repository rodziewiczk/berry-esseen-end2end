"""Lightweight resource fixtures only; no mathematical source is executed."""
from pathlib import Path
from unittest.mock import patch
import os,sys,tempfile,unittest
from be_replay import action_supervisor as new,linux_supervisor as old

class ActionSupervisor(unittest.TestCase):
 def test_only_waited_child_accounting_and_its_explicit_scope_are_changed(self):
  raw=Path(old.__file__).read_text();actual=Path(new.__file__).read_text()
  actual=actual[actual.index('"""'):]
  expected=raw.replace('cpu_ticks=int(fields[11])+int(fields[12]), vms_bytes=int(fields[20]),',
   'cpu_ticks=int(fields[11])+int(fields[12])+int(fields[13])+int(fields[14]), vms_bytes=int(fields[20]),')
  expected=expected.replace("'sampled_group_CPU_limit_seconds': config['cpu_seconds'],",
   "'sampled_group_CPU_limit_seconds': config['cpu_seconds'],\n             'sampled_group_CPU_includes_waited_descendants': True,")
  expected=expected.replace("if value['pgid'] == pgid and value['state'] not in ('Z', 'X'):",
   "if value['pgid'] == pgid and (value['state'] not in ('Z', 'X') or\n                                      (value['pid'] == pgid and value['state'] == 'Z')):")
  # The added capability precondition is checked separately. All remaining
  # machinery stays byte-identical to the original audited supervisor.
  start=actual.index('    # Some hosted test runners expose a parent PID namespace')
  end=actual.index("    if mode == 'trusted_native':",start)
  actual=actual[:start]+actual[end:]
  self.assertEqual(actual,expected)

 def test_all_four_process_cpu_fields_are_charged(self):
  fields=['S','1','2','2','0','0','0','0','0','0','0','101','202','303','404','0','0','0','0','999','1024','8']
  raw='123 (fixture child) '+' '.join(fields)
  with patch.object(new.Path,'read_text',return_value=raw):
   self.assertEqual(new._proc_stat(123)['cpu_ticks'],101+202+303+404)

 def test_bad_namespace_never_launches_a_child(self):
  with tempfile.TemporaryDirectory()as temp,patch.object(new.Path,'read_text',return_value='999999999 (fixture) S'),patch.object(new.subprocess,'Popen')as launch:
   root=Path(temp)
   report=new.run([sys.executable,'-B','-c','pass'],cwd=root,output_dir=root/'execution',mode='untrusted_search',cpu_seconds=2,wall_seconds=15)
   self.assertEqual(report['status'],'unsupported');self.assertEqual(report['reason'],'proc_PID_namespace_mismatch');launch.assert_not_called()

 @unittest.skipUnless(sys.platform=='linux','Linux resource fixture')
 def test_reaped_child_cpu_still_consumes_the_action_budget(self):
  with tempfile.TemporaryDirectory()as temp:
   root=Path(temp);source=root/'fixture.py'
   source.write_text('import subprocess,sys\n'
    'program="import time\\ns=time.process_time()\\nwhile time.process_time()-s<1.3:pass"\n'
    'for _ in range(3):subprocess.run([sys.executable,"-B","-S","-c",program],check=True)\n')
   report=new.run([sys.executable,'-B','-S',str(source)],cwd=root,output_dir=root/'execution',mode='untrusted_search',
    cpu_seconds=2,wall_seconds=15,memory_bytes=256*1024**2,disk_bytes=8*1024**2,log_bytes=1024**2,heartbeat_seconds=20)
   if int(Path('/proc/self/stat').read_text().split(' ',1)[0])!=os.getpid():
    self.assertEqual(report['status'],'unsupported');self.assertEqual(report['reason'],'proc_PID_namespace_mismatch');return
   self.assertNotEqual(report['status'],'completed');self.assertIn('CPU',report['reason'])
   self.assertTrue(report['guard_scope']['sampled_group_CPU_includes_waited_descendants']);self.assertFalse(report['proof_accepted'])

if __name__=='__main__':unittest.main()
