"""Full57H waiting/failure/export/controller fixtures, without native math."""
from copy import deepcopy
from pathlib import Path
import tempfile,unittest
from unittest.mock import patch
from be_replay import finite1519_join as run,finite1519_join_evidence as ev,finite1519_join_control_sources as src


class Controller(unittest.TestCase):
 def setUp(self):
  scratch=src.ROOT/'work/finite1519-join-fixtures';scratch.mkdir(parents=True,exist_ok=True)
  self.tmp=tempfile.TemporaryDirectory(dir=scratch);self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)

 def execute(self,name='run'):
  return run.run_colab(durable_root=self.root/'drive'/name,work_root=self.root/'work'/name,archives=self.root/'archives',backup_interval=60)

 def test_missing_complete_inputs_wait_without_download_or_native_and_export(self):
  with patch.object(run.sys,'platform','linux'),patch.object(ev,'import_completed_inputs',return_value=[dict(key='56I',requirement='full actual predecessor')]),patch.object(src,'obtain_assets',side_effect=AssertionError('WAITING must not download')),patch.object(run,'run_controls',side_effect=AssertionError('WAITING must not run original controls')):
   result=self.execute()
  self.assertEqual(result['status']['state'],'waiting_for_prerequisite_exports');self.assertFalse(result['status']['conditional_finite_chain_verified'])
  self.assertTrue(Path(result['bundle']['path']).is_file());self.assertEqual(src.digest(result['bundle']['path']),result['bundle']['sha256'])
  self.assertTrue(Path(result['bundle']['path']).with_suffix('.zip.sha256').is_file())

 def test_final_complete_claim_requires_full_readback_and_all_false_global_flags(self):
  for reject in(False,True):
   def controls(root,cache,source,status):status['conditional_controls_completed']=True
   def final(root):
    packet=ev.read(Path(root)/'SESSION_RESULT.json');self.assertIs(packet['conditional_finite_chain_verified'],True)
    if reject:raise ValueError('Synthetic hostile final rejection')
    return dict(conditional_finite_chain_verified=True)
   with patch.object(run.sys,'platform','linux'),patch.object(ev,'import_completed_inputs',return_value=[]),patch.object(src,'obtain_assets',return_value={}),patch.object(src,'prepare_cache',return_value=self.root/'source'),patch.object(run,'run_controls',side_effect=controls),patch.object(ev,'validate_batch',return_value={'synthetic_only':True}),patch.object(ev,'validate_completed',side_effect=final):
    result=self.execute('complete'+str(reject))
   self.assertEqual(result['status']['conditional_finite_chain_verified'],not reject);self.assertTrue(Path(result['bundle']['path']).is_file())
   self.assertTrue(all(result['status'][f]is False for f in run.ev.FLAGS))
   indexes=list((self.root/'drive'/('complete'+str(reject))).rglob('completed-finite/**/*.json'));self.assertEqual(len(indexes),0 if reject else 1)

 def test_original_failure_keeps_completion_false_and_emits_error_bundle(self):
  with patch.object(run.sys,'platform','linux'),patch.object(ev,'import_completed_inputs',return_value=[]),patch.object(src,'obtain_assets',side_effect=ValueError('source pin failure')):
   result=self.execute()
  self.assertEqual(result['status']['state'],'incomplete');self.assertIn('source pin failure',result['status']['error'])
  self.assertTrue((Path(result['work'])/'ERROR.txt').is_file());self.assertTrue(Path(result['bundle']['path']).is_file())

 def test_failed_drive_export_saves_local_failure_bundle(self):
  original=run.bundle;calls=[]
  def save(root,destination):
   calls.append(Path(destination))
   if len(calls)==1:raise OSError('Synthetic Drive export failure')
   return original(root,destination)
  with patch.object(run.sys,'platform','linux'),patch.object(ev,'import_completed_inputs',return_value=[{'key':'56I'}]),patch.object(run,'bundle',side_effect=save):result=self.execute()
  self.assertEqual(len(calls),2);self.assertEqual(result['status']['state'],'incomplete');self.assertIn('bundle_error',result['status']);self.assertTrue(Path(result['bundle']['path']).is_file())

 def test_whole_completed_control_cache_resume_skips_source_execution(self):
  task=self.root/'batch/controls/restored';task.mkdir(parents=True)
  (task/'CURRENT_GEOMETRY_FIXTURE.json').write_bytes(src.encoded(dict(validated_native_count={'current':'count56'})))
  d=src.plan()['fresh_geometry_fixture'];status=dict(imports=[dict(key='count:'+d['job_id'],validated={'current':'count56'})])
  loaded=(task,dict(conditional_controls_completed=True),dict(path='old',sha256='e'*64))
  with patch.object(run.controls,'restore_completed',return_value=loaded),patch.object(run.controls,'execute',side_effect=AssertionError('Complete cache must skip originals')):
   record=run.run_controls(self.root/'batch',self.root/'completed',self.root/'source',status)
  self.assertTrue(record['reused_completed_stage']);self.assertTrue(status['conditional_controls_completed'])

 def test_new_current_count_epoch_reexecutes_controls_preserving_old_cache(self):
  batch=self.root/'batch';task=batch/'controls/old';task.mkdir(parents=True);upstream=batch/'imports/count56';upstream.mkdir(parents=True)
  (task/'CURRENT_GEOMETRY_FIXTURE.json').write_bytes(src.encoded(dict(validated_native_count={'epoch':'old'})))
  d=src.plan()['fresh_geometry_fixture'];status=dict(imports=[dict(key='count:'+d['job_id'],validated={'epoch':'current'},task_relative='imports/count56')])
  loaded=(task,dict(conditional_controls_completed=True),dict(path='old-cache',sha256='e'*64))
  with patch.object(run.controls,'restore_completed',return_value=loaded),patch.object(run.controls,'execute',return_value={'six':'current'})as execute,patch.object(run.controls,'save_completed',return_value={'path':'new-cache'}):
   record=run.run_controls(batch,self.root/'completed',self.root/'source',status)
  self.assertFalse(record['reused_completed_stage']);self.assertEqual(execute.call_count,1);self.assertTrue((task/'CURRENT_GEOMETRY_FIXTURE.json').is_file())

 def test_exact_current_geometry_readback_must_match_actual_import(self):
  task=self.root/'controls';task.mkdir();put=lambda name,value:(self.root/name).write_bytes(src.encoded(value))
  put('controls/CURRENT_GEOMETRY_FIXTURE.json',dict(validated_native_count={'current':'a'}))
  status=dict(schema=ev.SCHEMA,controls=dict(task_relative='controls',validated={'six':'complete'},export={},reused_completed_stage=False),imports=[],**{f:False for f in run.ev.FLAGS})
  d=src.plan()['fresh_geometry_fixture'];inputs=({}, {}, {d['job_id']:dict(checked={'current':'b'})},dict(conditional_finite_chain_verified=True,session_result_sha256='a'*64))
  with patch.object(ev.controls,'validate_completed',return_value={'six':'complete'}),patch.object(ev,'_validated_inputs',return_value=inputs),self.assertRaisesRegex(ValueError,'actual same selected'):ev.validate_batch(self.root,status)


if __name__=='__main__':unittest.main()
