"""Pure closed-route inventory checks; no original program is imported."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PIN='56ec7c3a140deae8723e3f6d248360e96d4b8a88305be6c1a22436ac064c3fad'

class RequiredActionPlan(unittest.TestCase):
 def setUp(self):
  self.raw=(ROOT/'proof/finite4348_source_action_plan.json').read_bytes();self.d=json.loads(self.raw)

 def test_closed_two_file_partition_retains_all_original_calls_and23h_policy(self):
  d=self.d;self.assertEqual(hashlib.sha256(self.raw).hexdigest(),PIN)
  self.assertEqual(d['proposed_notebook_files'],2);self.assertEqual(d['notebooks_currently_runnable'],0)
  self.assertEqual([v['standalone_native_calls']for v in d['sections'].values()],[25,6,2,12,9,10,5,11,1])
  self.assertEqual(d['planned_notebooks']['61']['standalone_original_calls'],33)
  self.assertEqual(d['planned_notebooks']['62']['standalone_original_calls']+d['planned_notebooks']['62']['nested_original_calls'],59)
  self.assertEqual(d['session_policy']['maximum_session_wall_seconds'],82800)
  self.assertTrue(d['session_policy']['completed_stage_cache']);self.assertFalse(d['session_policy']['partial_numerical_acceptance'])
  self.assertFalse(d['arithmetic_computed']);self.assertFalse(d['original_mathematical_modules_imported_or_evaluated']);self.assertFalse(d['all_index_conclusion_verified'])

 def test_no_raw_action_dropped_and_literal_ten_catalogue_remains_covered(self):
  d=self.d;assigned={k for row in d['sections'].values()for k in row.get('actions',[])}
  self.assertEqual(set(d['actions']),assigned|{'40.left40_accept/binding01'})
  self.assertEqual(len(d['actions']),79);self.assertEqual(len(d['ten_literal_component_actions']),10)
  self.assertTrue(set(d['ten_literal_component_actions'].values())<=assigned)
  for key,row in d['actions'].items():
   self.assertEqual(row['id'],key);self.assertIn(row['source_member'],d['source_tree']['selected_sources'])
   self.assertEqual(row['script_sha256'],d['source_tree']['selected_sources'][row['source_member']]['sha256'])
   self.assertFalse(row['historical_capture_is_fresh_evidence']);self.assertIs(type(row['arguments']),list)

 def test_full_low_constructors_replays_and_parallel_mid_are_explicit(self):
  d=self.d;rows=d['cutoff44_nested_full_LOW'];self.assertEqual([r['rows']for r in rows],[78,74])
  self.assertEqual(sum(r['strict_gates']for r in rows),23513686)
  for row in rows:self.assertEqual(d['actions'][row['action']]['arguments'],['--replay'])
  low=d['global40_nested_LOW'];self.assertEqual(low['central']['signed_rows'],70)
  self.assertEqual(d['actions'][low['central']['constructor']]['script'],'work/toward40_20261007/root/central_compare/execute_low40.py')
  self.assertNotIn('40.local/conditional_low40_execute01',d['actions'])
  self.assertEqual(low['left']['signed_rows_by_part'],[18,34,30]);self.assertEqual(low['left']['total_signed_rows'],82)
  self.assertEqual(len(low['left']['constructors']),3);self.assertEqual(low['left_MID']['whole_contexts'],5126)
  self.assertEqual(len(low['left_MID']['part_actions']),3);self.assertEqual(low['single39']['signed_rows'],90)

 def test_nine_binders_full12_epoch_and_known_remaining_boundaries_are_preserved(self):
  d=self.d;binders=d['sections']['62F']['component_bindings']
  self.assertEqual([r['id']for r in binders],['tail43','early','single39','left_acquisition','central_acquisition','central_indexed','left_comparison','central_comparison','probability'])
  self.assertEqual(d['sections']['62F']['nested_component_calls'],9);self.assertEqual(d['sections']['62F']['nested_single39_calls'],2)
  retained=d['shared_completed12'];self.assertFalse(retained['numerical_replay_required'])
  self.assertEqual((retained['top_level_executions'],retained['retained_components']),(14,41))
  self.assertEqual(retained['zip_sha256'],'51640e38549bf8ebe05e09953622e1f8526063f7a03b2f2c48756b782d17fd63')
  self.assertTrue(d['retained44_capsule']['all1825_byte_hashes_verified']);self.assertFalse(d['full_parent_graph']['all9518_byte_hashes_freshly_verified'])
  self.assertEqual(len(d['remaining_implementation_boundaries']),6);self.assertTrue(d['unacquired_mathematical_premises'])
  text=self.raw.decode();self.assertNotIn('/Users/',text);self.assertNotIn('file_uri',text);self.assertNotIn('C:\\',text)

if __name__=='__main__':unittest.main()
