"""Additional10 namespace: full existing reader fixtures, no math execution."""
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
import ast,unittest
from be_replay import n25_upper_counts_sources as sources,n25_upper_counts_evidence as evidence,n25_upper_counts as runner
from be_replay import retained_n25_extra_sources as original_sources
from tests import test_retained_n25_extra_evidence as fixtures

class Selection(unittest.TestCase):
 def test_complete_ten_unchanged_original_forests_and_disjoint_old_batches(self):
  jobs=sources.jobs('upper-retained-graph')
  self.assertEqual(len(jobs),10);self.assertEqual(sum(j['leaf_count']for j in jobs),18978)
  self.assertEqual(sum(j['node_count']for j in jobs),37696)
  old={j['target_id']for branch in original_sources.EXPECTED_COUNTS for j in original_sources.jobs(branch)}
  self.assertFalse(old&{j['target_id']for j in jobs})
  self.assertEqual(sum('/high25_beta2/' in j['capsule_member_prefix']for j in jobs),7)
  self.assertFalse(sources.not_ready()['full_physical_union_and_parent_interfaces_acquired'])

 def test_only_accept_and_native_23_hour_budgets(self):
  self.assertEqual(runner.NATIVE_CPU_SECONDS,82800);self.assertEqual(runner.NATIVE_WALL_SECONDS,82800)
  tree=ast.parse(Path(runner.__file__).read_text(encoding='utf-8'))
  function=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='accept')
  literals=[n.value for n in ast.walk(function)if isinstance(n,ast.Constant)and type(n.value)is str]
  self.assertIn('accept',literals);self.assertNotIn('construct',literals)

class WholeEvidence(fixtures.RetainedEvidenceTests):
 def setUp(self):
  p=patch.object(fixtures,'evidence',evidence);p.start();self.addCleanup(p.stop)
  super().setUp()

 def test_complete_stage_and_preledger_validation_do_not_execute_trap_source(self):
  result=self.validate();self.assertEqual(result['schema'],'REVALIDATED_N25_ADDITIONAL_UPPER_COUNT_STAGE_V1')
  self.assertTrue(result['native_arithmetic_accepted']);self.assertFalse(result['parent_acquisitions_verified'])
  self.assertEqual(result['census']['leaves'],26)
  (self.epoch/'NATIVE_ACCEPTED.json').unlink()
  self.assertEqual(evidence.validate_run(self.task,self.job,self.epoch,self.observed,self.census),self.receipt)

 def test_wrong_command_budget_controller_or_actual_guard_rejects(self):
  original=deepcopy(evidence.common.read(self.execution/'native-launch.json'))
  for change in(lambda x:x.update(memory_bytes=512*evidence.MIB),lambda x:x.update(cpu_seconds=82801),
                lambda x:x.update(wall_seconds=82801),lambda x:x['argv'].__setitem__(-1,'construct')):
   self.alter(self.execution/'native-launch.json',change);self.reject()
   self.alter(self.execution/'native-launch.json',lambda x:(x.clear(),x.update(deepcopy(original))))
  self.alter(self.execution/'launch.json',lambda x:x['argv'].__setitem__(4,'--_exec-search'));self.reject()

if __name__=='__main__':unittest.main()
