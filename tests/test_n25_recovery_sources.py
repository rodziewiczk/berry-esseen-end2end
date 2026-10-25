"""Synthetic source fixtures with import traps; never evaluate archived math."""
from copy import deepcopy
from fractions import Fraction
import io
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from be_replay import n25_recovery_sources as sources


class RecoveryFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.target = 'synthetic-original'
        self.prefix = 'original/capsule/'
        cfg = dict(n=25, index=26, p=['13/50','27/100'], Lambda='1/10', d0='1/20')
        self.source = {
            'count_protocol.py': b"raise AssertionError('never import original code')\nLIMIT=10000\n",
            'kernel.py': b"raise AssertionError('never import kernel')\n",
            'contract.json': sources.encoded(dict(rows=[cfg]))}
        self.source['KERNEL_COPY_MANIFEST.json'] = sources.encoded(dict(files={
            'kernel.py':sources.sha(self.source['kernel.py'])}))
        self.source['FROZEN_DESIGN.json'] = sources.encoded(dict(files={
            n:sources.sha(raw) for n,raw in self.source.items()}))
        self.files = {n:dict(bytes=len(raw),sha256=sources.sha(raw)) for n,raw in self.source.items()}
        self.header = dict(schema='SYNTHETIC_ORIGINAL_FOREST', n=25, index=26, target='1/2',
                           contract_sha256=self.files['contract.json']['sha256'],
                           checker_sha256=self.files['count_protocol.py']['sha256'],
                           kernel_sha256={'kernel.py': self.files['kernel.py']['sha256']})
        box=[['13/50','27/100'],['0','1/10'],['0','1'],['-1/2','1/2'],['0','1/20']]
        self.forest = dict(**self.header, roots=[dict(k=k,tree=dict(kind='leaf',box=deepcopy(box),
                   decision='PASS_TARGET',result={'score_upper':'1/4'})) for k in range(26)])
        raw = sources.encoded(self.forest)
        self.candidate = dict(filename='COUNT26_FOREST.json',bytes=len(raw),sha256=sources.sha(raw))
        historical = sources.encoded(dict(status='HISTORICAL_ONLY_NOT_CURRENT_ACCEPTANCE'))
        self.old = dict(filename='COUNT26_ACCEPTED.json',bytes=len(historical),sha256=sources.sha(historical))
        payload = {self.prefix+n:b for n,b in self.source.items()}
        payload[self.prefix+self.candidate['filename']] = raw
        payload[self.prefix+self.old['filename']] = historical
        manifest = sources.encoded(dict(schema='N25_ORIGINAL_BYTES_RECOVERY_V1', files=[
            dict(member=n,bytes=len(b),sha256=sources.sha(b)) for n,b in payload.items()]))
        self.archive = self.root/'recovery.zip'
        with zipfile.ZipFile(self.archive,'w') as z:
            for n,b in payload.items(): z.writestr(n,b)
            z.writestr('AUDIT_MANIFEST.json',manifest)
        spec = dict(target=self.target,kind='ordinary-v14',index=26,files=self.files,
                    member_prefix=self.prefix, candidate=self.candidate,historical_receipt=self.old,
                    native_header=self.header,leaf_count=26,design_sha256=self.files['FROZEN_DESIGN.json']['sha256'],
                    historical_statistics=dict(nodes=26,leaves=26,closed_statuses={'PASS_TARGET':26},
                                               maximum_score='1/4',maximum_depth=0))
        archive_sha = sources.sha(self.archive.read_bytes())
        self.plan = dict(schema=sources.SCHEMA, original_mathematical_code_executed=False,
                         full66_complete=False, profiles={self.target:spec}, aliases={'legacy':self.target},
                         asset=dict(sha256=archive_sha,bytes=self.archive.stat().st_size,
                                    manifest_sha256=sources.sha(manifest),manifest_payload_files=len(payload)))
        plan_path=self.root/'plan.json';plan_path.write_bytes(sources.encoded(self.plan))
        for name,value in [('PLAN',plan_path),('PLAN_SHA256',sources.sha(plan_path.read_bytes())),
                           ('ARCHIVE_SHA256',archive_sha)]:
            p=patch.object(sources,name,value);p.start();self.addCleanup(p.stop)
        self.task=self.root/'task'

    def prepare(self): return sources.prepare(self.target,self.task,archive=self.archive)

    def test_prepare_unchanged_bytes_history_separate_and_no_imports(self):
        result=self.prepare()
        self.assertFalse(result['arithmetic_accepted'])
        self.assertFalse(result['full66_complete'])
        for name,raw in self.source.items(): self.assertEqual((self.task/'capsule'/name).read_bytes(),raw)
        self.assertFalse((self.task/'capsule'/self.old['filename']).exists())
        self.assertTrue((self.task/'provenance'/self.old['filename']).is_file())
        self.assertEqual(sources.verify_preparation(self.target,self.task),result)

    def test_alias_selects_original_identity_not_reconstructed_cache(self):
        self.assertEqual(sources.normalize('legacy'),self.target)
        self.assertEqual(sources.profile('legacy')['target'],self.target)
        with self.assertRaises(ValueError): sources.profile('unknown')

    def test_historical_receipt_cannot_be_staged_as_fresh(self):
        self.prepare()
        (self.task/'capsule'/self.old['filename']).write_bytes((self.task/'provenance'/self.old['filename']).read_bytes())
        with self.assertRaises(ValueError): sources.verify_preparation(self.target,self.task)

    def test_every_source_and_candidate_hash_required(self):
        self.prepare()
        for name in ('kernel.py','count_protocol.py','contract.json','FROZEN_DESIGN.json',self.candidate['filename']):
            with self.subTest(name=name):
                p=self.task/'capsule'/name;raw=p.read_bytes();p.write_bytes(raw+b' ')
                with self.assertRaises(ValueError): sources.verify(self.target,self.task/'capsule')
                p.write_bytes(raw)

    def test_current_input_flags_and_census_cannot_be_promoted(self):
        self.prepare();p=self.task/'RECOVERY_INPUTS.json';saved=p.read_bytes()
        for key in ('arithmetic_accepted','parent_acquisitions_verified','full66_complete','discovery_required'):
            row=sources.parsed(saved);row[key]=True;p.write_bytes(sources.encoded(row))
            with self.assertRaises(ValueError): sources.verify_preparation(self.target,self.task)
            p.write_bytes(saved)

    def test_original_geometry_rejects_missing_count_boolean_count_and_extra_claim(self):
        self.prepare()
        mutations=[lambda x:x['roots'].pop(),lambda x:x['roots'][0].update(k=False),
                   lambda x:x.update(accepted=True),lambda x:x['roots'].reverse(),
                   lambda x:x['roots'][0]['tree']['box'][0].__setitem__(0,'0')]
        for change in mutations:
            packet=deepcopy(self.forest);change(packet)
            with self.assertRaises(ValueError): sources.geometry(self.target,self.task/'capsule',packet)

    def test_closed_split_geometry_and_original_node_limit(self):
        self.prepare()
        packet=deepcopy(self.forest);leaf=packet['roots'][0]['tree']
        packet['roots'][0]['tree']=dict(kind='split',axis=True,cut='1/4',left=leaf,right=deepcopy(leaf))
        with self.assertRaises(ValueError): sources.geometry(self.target,self.task/'capsule',packet)
        with patch.object(sources,'NODE_LIMIT',25):
            with self.assertRaises(ValueError): sources.geometry(self.target,self.task/'capsule',self.forest)

    def test_no_overwrite_and_no_linked_destination(self):
        self.prepare()
        with self.assertRaises(ValueError): self.prepare()
        link=self.root/'link'
        try:
            link.symlink_to(self.task,target_is_directory=True)
        except OSError as error:
            if sys.platform == 'win32' and getattr(error, 'winerror', None) == 1314:
                self.skipTest('Windows account cannot create symlinks; run this fixture on Linux')
            raise
        with self.assertRaises(ValueError): sources.prepare(self.target,link/'another',archive=self.archive)

    def test_tampered_asset_fails_even_before_member_read(self):
        with self.archive.open('ab') as out:out.write(b'changed')
        with self.assertRaises(ValueError): self.prepare()
        self.assertFalse(self.task.exists())

    def test_changed_plan_is_not_trusted(self):
        sources.PLAN.write_bytes(sources.PLAN.read_bytes()+b' ')
        with self.assertRaises(ValueError): sources.targets()

    def test_duplicate_json_keys_and_nonfinite_rejected(self):
        for raw in (b'{"x":1,"x":2}',b'{"x":NaN}'):
            with self.assertRaises(ValueError): sources.parsed(raw)

    def test_read_requires_open_verified_asset(self):
        asset=sources.RecoveryArchive(self.archive)
        with self.assertRaises(ValueError):asset.read(self.prefix+'kernel.py',self.files['kernel.py'])
        with asset:
            self.assertEqual(asset.read(self.prefix+'kernel.py',self.files['kernel.py']),self.source['kernel.py'])
        with self.assertRaises(ValueError):asset.read(self.prefix+'kernel.py',self.files['kernel.py'])

    def test_mixed_parent_excluded_from_ordinary_route(self):
        p=deepcopy(self.plan);p['profiles'][self.target]['kind']='mixed-parent-v14'
        with patch.object(sources,'_plan',return_value=p):
            self.assertEqual(sources.targets(),())
            self.assertEqual(sources.targets(include_mixed=True),(self.target,))
            with self.assertRaisesRegex(ValueError,'Mixed'):sources.profile(self.target,ordinary=True)


class ArchiveSafetyTests(unittest.TestCase):
    def check_name(self,name,mode=stat.S_IFREG|0o644):
        # A real ZipFile roundtrip normalizes os.sep on Windows before the
        # application guard sees it. Supply the raw inventory object directly;
        # duplicate-entry tests below still exercise actual ZIP readback.
        row=zipfile.ZipInfo('fixture');row.filename=name
        row.external_attr=mode<<16;row.file_size=1
        class Inventory:
            def infolist(self):return [row]
        sources._inventory(Inventory())

    def test_safe_regular_name(self):self.check_name('a/kernel.py')

    def test_traversal_absolute_windows_and_noncanonical_names_rejected(self):
        for name in ('../x','/x','a/../x','a//x','a/./x','C:/x','a\\x','a/x.','a/CON'):
            with self.subTest(name=name),self.assertRaises(ValueError):self.check_name(name)

    def test_symlink_directory_and_special_file_rejected(self):
        for mode in (stat.S_IFLNK,stat.S_IFIFO,stat.S_IFDIR):
            with self.assertRaises(ValueError):self.check_name('a/x',mode|0o644)

    def test_case_aliases_and_duplicate_entries_rejected(self):
        import warnings
        for names in (('a/x','a/X'),('a/x','a/x')):
            raw=io.BytesIO()
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                with zipfile.ZipFile(raw,'w') as z:
                    for name in names:z.writestr(name,b'x')
            raw.seek(0)
            with zipfile.ZipFile(raw) as z,self.assertRaises(ValueError):sources._inventory(z)


class PinnedSelectionTests(unittest.TestCase):
    def test_real_plan_has_eleven_original_counts_and_two_mixed_sources(self):
        self.assertEqual(len(sources.targets()),11)
        self.assertEqual(len(sources.targets(include_mixed=True)),13)
        rows=[sources.profile(t) for t in sources.targets()]
        self.assertEqual(sum(r['leaf_count'] for r in rows),32093)
        self.assertTrue(all(r['historical_statistics']['nodes']<=10000 for r in rows))
        self.assertTrue(all(not r['arithmetic_accepted'] for r in rows))
        self.assertFalse(sources._plan()['full66_complete'])

if __name__=='__main__':unittest.main()
