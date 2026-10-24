"""Synthetic saved-execution recovery and notebook routing, without kernels."""
import copy,hashlib,importlib.util,json,tempfile,types,unittest,zipfile
from pathlib import Path
from unittest.mock import Mock,patch
from be_replay import finite69_caps_recovery as h


class Recovery(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(dir=h.src.ROOT.parent,prefix='r46-');self.addCleanup(self.temp.cleanup)
  self.root=Path(self.temp.name);self.drive=self.root/'drive';self.work=self.root/'work'
  self.observed=h.src.dump(dict(schema=h.ev.OBSERVED,job_id=h.JOB,implementation={'exact_old_execution':'1'*64},
    conditional_arithmetic_completed=False,actions=[dict(label=n,observed={'status':'completed'})for n in('plan','construct','replay','readback','caps')]))
  self.files={'SOURCES.json':h.src.dump(dict(job_id=h.JOB,kind='owncaps')),'ACTION_PROGRESS.json':b'{"actions":[]}\n',
   'STAGE_OBSERVED.json':self.observed,'capsule/TRAP.py':b'raise AssertionError("Never import archived arithmetic")\n'}
  self.archive=self.drive/h.ARCHIVE_RELATIVE;self.archive.parent.mkdir(parents=True)
  with zipfile.ZipFile(self.archive,'x')as z:
   for name,raw in self.files.items():z.writestr(h.PREFIX+name,raw)
  self.pin=hashlib.sha256(self.archive.read_bytes()).hexdigest();self.observed_pin=hashlib.sha256(self.observed).hexdigest()
  for name,value in dict(ARCHIVE_BYTES=self.archive.stat().st_size,ARCHIVE_SHA256=self.pin,FILES=len(self.files),EXPANDED_BYTES=sum(map(len,self.files.values())),OBSERVED_SHA256=self.observed_pin).items():
   p=patch.object(h,name,value);p.start();self.addCleanup(p.stop)
  self.summary=dict(kind='owncaps',job_id=h.JOB,strips=86,whole_rows=344,caps_controls=17)

 def validators(self):
  def full(task,report):
   self.assertFalse((Path(task)/'STAGE_COMPLETED.json').exists());self.assertEqual((Path(task)/'STAGE_OBSERVED.json').read_bytes(),self.observed)
   self.assertEqual(len(report['actions']),5);return copy.deepcopy(self.summary)
  def admission(task):return dict(schema='SYNTHETIC_CURRENT_READER_ADMISSION',source_bundle_sha256=self.pin,
   original_observed_sha256=self.observed_pin,original_execution_bytes_unchanged=True,mathematical_replay=False)
  def completed(task):
   p=h.src.read(Path(task)/'STAGE_COMPLETED.json');self.assertEqual(p['implementation'],{'exact_old_execution':'1'*64})
   self.assertEqual(p['observed_sha256'],self.observed_pin);self.assertTrue(p['conditional_arithmetic_completed'])
   self.assertEqual((Path(task)/'STAGE_OBSERVED.json').read_bytes(),self.observed)
   self.assertEqual(h.src.read(Path(task)/'RECOVERY_ADMISSION.json'),admission(task))
   for f in h.ev.FLAGS:self.assertIs(p[f],False)
   return dict(job_id=h.JOB,summary=self.summary,stage_result_sha256=h.src.digest(Path(task)/'STAGE_COMPLETED.json'))
  return (patch.object(h.src,'verify_job',side_effect=lambda task:h.src.read(Path(task)/'SOURCES.json')),
   patch.object(h.ev,'validate_run',side_effect=full),patch.object(h.ev,'saved_observed_admission',side_effect=admission),
   patch.object(h.ev,'validate_completed',side_effect=completed))

 def test_exact_saved_bytes_extracted_without_completion_or_kernel_execution(self):
  task=h.extract_selected(self.archive,self.root/'extracted')
  self.assertEqual({p.relative_to(task).as_posix()for p in task.rglob('*')if p.is_file()},set(self.files))
  self.assertEqual((task/'STAGE_OBSERVED.json').read_bytes(),self.observed);self.assertFalse((task/'STAGE_COMPLETED.json').exists())

 def test_full_current_reader_precedes_truthful_new_completion_and_cache(self):
  p0,p1,p2,p3=self.validators()
  with p0,p1 as full,p2 as admitted,p3 as final,patch.object(h.run,'restore_stage',return_value=None),patch.object(h.run,'save_stage',return_value={'path':'synthetic-complete.zip'})as save,patch.object(h.run.linux_supervisor,'run')as native:
   result=h.recover_saved_owncaps(durable_root=self.drive,work_root=self.work)
  self.assertEqual(result['state'],'recovered_complete_owncaps_current_reader');self.assertTrue(result['conditional_arithmetic_completed'])
  self.assertFalse(result['mathematical_replay']);full.assert_called_once();admitted.assert_called_once();final.assert_called_once();save.assert_called_once();native.assert_not_called()
  for f in h.ev.FLAGS:self.assertIs(result[f],False)

 def test_original_ledger_or_full_control_rejection_creates_no_completion_or_cache(self):
  p0,p1,p2,p3=self.validators()
  with p0,patch.object(h.ev,'validate_run',side_effect=ValueError('Missing genuine fifth stopped capture')),p2 as admission,p3 as final,patch.object(h.run,'restore_stage',return_value=None),patch.object(h.run,'save_stage')as save:
   with self.assertRaisesRegex(ValueError,'fifth'):h.recover_saved_owncaps(durable_root=self.drive,work_root=self.work)
  save.assert_not_called();admission.assert_not_called();final.assert_not_called()
  task=next(self.work.rglob('STAGE_OBSERVED.json')).parent
  self.assertEqual((task/'STAGE_OBSERVED.json').read_bytes(),self.observed);self.assertFalse((task/'STAGE_COMPLETED.json').exists())
  report=h.src.read(next(self.work.rglob('RECOVERY.json')));self.assertFalse(report['conditional_arithmetic_completed'])

 def test_existing_full_cache_is_delegated_to_full_validator_before_skip(self):
  checked=dict(summary=self.summary);export=dict(path='already-validated.zip')
  with patch.object(h.run,'restore_stage',return_value=(Path('existing'),checked,export))as restore,patch.object(h,'extract_selected')as extract,patch.object(h.run.linux_supervisor,'run')as native:
   result=h.recover_saved_owncaps(durable_root=self.drive,work_root=self.work)
  restore.assert_called_once();extract.assert_not_called();native.assert_not_called()
  self.assertEqual(result['state'],'existing_complete_owncaps_revalidated');self.assertEqual(result['export'],export)

 def test_missing_bundle_permits_normal_execution_but_bad_sidecar_stops(self):
  self.archive.with_suffix('.zip.sha256').write_text('wrong\n',encoding='ascii')
  with patch.object(h.run,'restore_stage',return_value=None),patch.object(h,'extract_selected')as extract:
   with self.assertRaises(ValueError):h.recover_saved_owncaps(durable_root=self.drive,work_root=self.work)
   extract.assert_not_called()
  self.archive.unlink()
  with patch.object(h.run,'restore_stage',return_value=None),patch.object(h,'extract_selected')as extract:
   result=h.recover_saved_owncaps(durable_root=self.drive,work_root=self.work)
  extract.assert_not_called();self.assertIn('unavailable',result['state']);self.assertFalse(result['conditional_arithmetic_completed'])

 def test_archive_or_observed_hash_rejected_before_promotion(self):
  with patch.object(h,'ARCHIVE_SHA256','0'*64):
   with self.assertRaises(ValueError):h.extract_selected(self.archive,self.root/'bad-archive')
   self.assertFalse((self.root/'bad-archive').exists())
  task=h.extract_selected(self.archive,self.root/'bad-observed');(task/'STAGE_OBSERVED.json').write_bytes(b'{}\n')
  with patch.object(h.ev,'validate_run')as validate:
   with self.assertRaises(ValueError):h.complete_recovered(task)
  validate.assert_not_called();self.assertFalse((task/'STAGE_COMPLETED.json').exists())

 def test_metadata_preflight_rejects_traversal_duplicate_link_oversize_and_old_completion(self):
  with zipfile.ZipFile(self.archive)as z:original=z.infolist()
  for label in('traversal','backslash','duplicate','link','oversize','old_completion'):
   rows=copy.deepcopy(original)
   if label=='traversal':rows[0].filename=h.PREFIX+'../escape'
   elif label=='backslash':rows[0].filename=h.PREFIX+'a\\b'
   elif label=='duplicate':rows[0].filename=rows[1].filename
   elif label=='link':rows[0].external_attr=(0o120777<<16)
   elif label=='oversize':rows[0].file_size=256*h.src.MIB+1
   else:rows[0].filename=h.PREFIX+'STAGE_COMPLETED.json'
   fake=Mock();fake.infolist.return_value=rows
   with self.subTest(label=label),patch.object(h.zipfile,'ZipFile')as opener:
    opener.return_value.__enter__.return_value=fake
    with self.assertRaises(ValueError):h.extract_selected(self.archive,self.root/label)
   self.assertFalse((self.root/label).exists())


class NotebookRecovery(unittest.TestCase):
 def test_recovery_is_after_fixtures_before_execution_and_routes_same_drive(self):
  path=h.src.ROOT/'tools/make_finite69_caps_notebook.py';spec=importlib.util.spec_from_file_location('caps_recovery_notebook',path)
  builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder);doc=builder.build('a'*40);ids=[c['id']for c in doc['cells']]
  self.assertLess(ids.index('finite69-caps-fixtures'),ids.index('saved-owncaps-recovery'));self.assertLess(ids.index('saved-owncaps-recovery'),ids.index('execute-task'))
  code=''.join(next(c['source']for c in doc['cells']if c['id']=='saved-owncaps-recovery'))
  module=types.ModuleType('be_replay.finite69_caps_recovery');calls=[]
  module.recover_saved_owncaps=lambda **kw:(calls.append(kw)or{'state':'SYNTHETIC_REVALIDATED'})
  with patch.dict('sys.modules',{module.__name__:module}):exec(compile(code,'recovery-cell','exec'),{'DURABLE':Path('/synthetic-drive')})
  self.assertEqual(calls,[dict(durable_root=Path('/synthetic-drive'))])
  for cell in doc['cells']:
   if cell['cell_type']=='code':compile(''.join(cell['source']),'notebook46','exec')

if __name__=='__main__':unittest.main()
