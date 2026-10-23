"""Pinned selection and tiny source/ZIP/geometry fixtures; no numerical import."""
from copy import deepcopy
import json
from pathlib import Path
import stat
import tempfile
import unittest
import warnings
import zipfile
from unittest.mock import patch

from be_replay import retained_n25_extra_sources as sources, count_task as common


class ExtraSelectionTests(unittest.TestCase):
    def test_all_six_fixed_batches_and_explicit_exclusions(self):
        seen = set()
        for branch, count in sources.EXPECTED_COUNTS.items():
            jobs = sources.jobs(branch)
            self.assertEqual(len(jobs), count)
            self.assertEqual(sum(j['leaf_count'] for j in jobs), sources.EXPECTED_LEAVES[branch])
            self.assertTrue(all(j['archive_key'] == 'old' for j in jobs))
            self.assertFalse(any(j['original_design_acceptance_claimed'] for j in jobs))
            seen.update(j['target_id'] for j in jobs)
        self.assertEqual(len(seen), 115)
        self.assertNotIn('b3-p34', seen)
        excluded = sources.not_ready()['excluded']
        self.assertEqual(len(excluded), 24)
        self.assertTrue(all(j['target_id'] not in seen for j in excluded))
        self.assertEqual(sum(sources.EXPECTED_LEAVES.values()), 178294)

    def test_jobs_are_private_and_unknown_or_provisional_job_is_rejected(self):
        job = sources.jobs('b3')[0]
        job['index'] = 99
        self.assertNotEqual(sources.jobs('b3')[0]['index'], 99)
        with self.assertRaises(ValueError):
            sources._selected(job)
        with self.assertRaises(ValueError):
            sources.jobs('upper-retained-graph')


class ExtraSourceFixtures(unittest.TestCase):
    def setUp(self):
        parent = common.ROOT/'work'/'retained-extra-source-fixtures'
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.archive, self.task = self.root/'fixture.zip', self.root/'task'
        self.prefix = 'cutoff25_20261011/new_root/fake_extra/'
        checker = ("raise AssertionError('Never import numerical checker')\nLIMIT=10000\n"
                   "def header(bound):return dict(schema='FAKE_EXTRA',n=25,index=25)\n").encode()
        contract = dict(rows=[dict(n=25, index=25, K='0', p=['1/4','13/50'],
            rho_lower='13/10', rho_upper='7/5', Lambda='1', d0='1')])
        files = {'count_protocol.py': checker, 'contract.json': sources.encoded(contract),
                 'kernel.py': b"raise AssertionError('Never import numerical kernel')\n"}
        kernel = {'kernel.py': sources.sha(files['kernel.py'])}
        files['KERNEL_COPY_MANIFEST.json'] = sources.encoded(dict(files=kernel))
        # Deliberately stale provenance must remain stale, not be silently repaired.
        files['FROZEN_DESIGN.json'] = sources.encoded(dict(files={'kernel.py': '0'*64}))
        box = [['1/4','13/50'], ['0','1'], ['0','1'], ['-1/2','1/2'], ['0','1']]
        forest = dict(schema='FAKE_EXTRA', n=25, index=25, target='1/2',
            contract_sha256=sources.sha(files['contract.json']), checker_sha256=sources.sha(checker),
            kernel_sha256=kernel, roots=[dict(k=k, tree=dict(kind='leaf', box=deepcopy(box),
                decision='EMPTY_FIXTURE', result={'status':'EMPTY_FIXTURE'})) for k in range(26)])
        self.payloads = {self.prefix+n: raw for n, raw in files.items()}
        self.payloads[self.prefix+'COUNT25_FOREST.json'] = sources.encoded(forest)
        self.payloads[self.prefix+'COUNT25_ACCEPTED.json'] = b'{"status":"HISTORICAL_ONLY"}\n'
        self.job = dict(branch='b3', target_id='b3-p25', job_id='b3-p25',
            capsule_relative='capsules/b3-p25', archive_key='old', capsule_member_prefix=self.prefix,
            n=25, index=25, forest_filename='COUNT25_FOREST.json', acceptance_filename='COUNT25_ACCEPTED.json',
            manifest_filename='KERNEL_COPY_MANIFEST.json', manifest_sha256=sources.sha(files['KERNEL_COPY_MANIFEST.json']),
            checker_sha256=sources.sha(checker), contract_sha256=sources.sha(files['contract.json']),
            forest_sha256=sources.sha(sources.encoded(forest)), p_interval=contract['rows'][0]['p'],
            rho_interval=['13/10','7/5'], node_count=26, leaf_count=26, split_count=0, expected_selected_leaves=26,
            source_file_rows=[dict(filename=n, member=self.prefix+n, bytes=len(raw), sha256=sources.sha(raw))
                              for n, raw in files.items()], historical_design_issues=['Fixture stale design'],
            original_design_acceptance_claimed=False)
        self.patches = [patch.object(sources, 'jobs', side_effect=lambda branch: [deepcopy(self.job)]),
            patch.object(sources, 'EXPECTED_LEAVES', {'b3': 26}),
            patch.object(sources, 'not_ready', return_value=dict(schema='FAKE_NOT_READY', excluded=[],
                all_index_conclusion_verified=False)), patch.object(common, 'ASSETS', deepcopy(common.ASSETS))]
        for item in self.patches:
            item.start(); self.addCleanup(item.stop)
        self.write_archive()

    def write_archive(self, *, duplicate=None, symlink=None):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(self.archive, 'w') as zipped:
                for name, raw in self.payloads.items():
                    if name == symlink:
                        info = zipfile.ZipInfo(name)
                        info.create_system = 3
                        info.external_attr = (stat.S_IFLNK|0o777)<<16
                        zipped.writestr(info, raw)
                    else:
                        zipped.writestr(name, raw)
                if duplicate:
                    zipped.writestr(duplicate, b'fake duplicate')
        raw = self.archive.read_bytes()
        common.ASSETS['old'] = dict(name='fixture.zip', bytes=len(raw), sha256=sources.sha(raw))

    def prepare(self):
        return sources.prepare('b3', self.archive, self.task)

    def test_stale_design_preserved_under_explicit_new_seal_and_no_old_receipt(self):
        manifest = self.prepare()
        capsule = self.task/self.job['capsule_relative']
        self.assertEqual((capsule/'FROZEN_DESIGN.json').read_bytes(), self.payloads[self.prefix+'FROZEN_DESIGN.json'])
        epoch = common.read(capsule/sources.EPOCH)
        self.assertFalse(epoch['original_design_acceptance_claimed'])
        self.assertFalse(epoch['fresh_arithmetic_replayed'])
        self.assertFalse((capsule/self.job['acceptance_filename']).exists())
        self.assertEqual(sources.verify(self.task), manifest)
        self.assertEqual(sources.census(self.job, capsule)['leaves'], 26)

    def test_absent_historical_design_is_not_fabricated(self):
        self.job['source_file_rows'] = [r for r in self.job['source_file_rows'] if r['filename'] != 'FROZEN_DESIGN.json']
        del self.payloads[self.prefix+'FROZEN_DESIGN.json']
        self.job['historical_design_issues'] = ['Fixture absent historical design']
        self.write_archive(); self.prepare()
        capsule = self.task/self.job['capsule_relative']
        self.assertFalse((capsule/'FROZEN_DESIGN.json').exists())
        self.assertTrue((capsule/sources.EPOCH).is_file())
        sources.verify(self.task)

    def test_changed_new_seal_or_extra_file_or_missing_kernel_fails(self):
        self.prepare()
        capsule = self.task/self.job['capsule_relative']
        path = capsule/sources.EPOCH
        raw = path.read_bytes(); path.write_bytes(raw+b' ')
        with self.assertRaises(ValueError):sources.verify(self.task)
        path.write_bytes(raw)
        extra = capsule/'extra.py'; extra.write_text('raise AssertionError()')
        with self.assertRaises(ValueError):sources.verify(self.task)
        extra.unlink(); (capsule/'kernel.py').unlink()
        with self.assertRaises(ValueError):sources.verify(self.task)

    def test_duplicate_case_collision_symlink_or_bad_archive_rejects(self):
        name = self.prefix+'KERNEL_COPY_MANIFEST.json'
        for duplicate in (name, name.upper()):
            self.write_archive(duplicate=duplicate)
            with self.assertRaises(ValueError):self.prepare()
            self.assertFalse(self.task.exists())
        self.write_archive(symlink=name)
        with self.assertRaises(ValueError):self.prepare()
        self.assertFalse(self.task.exists())
        self.write_archive()
        self.archive.write_bytes(self.archive.read_bytes()+b'changed')
        with self.assertRaises(ValueError):self.prepare()
        self.assertFalse(self.task.exists())

    def test_root_order_missing_child_and_leaf_geometry_are_checked_without_execution(self):
        self.prepare()
        capsule = self.task/self.job['capsule_relative']
        forest = common.read(capsule/self.job['forest_filename'])
        # Exercise the pure geometry helper directly, after replacing only this
        # synthetic fixture's pinned candidate identity and its new source seal.
        for mutate in (lambda x:x['roots'].reverse(),
                       lambda x:x['roots'][0]['tree']['box'][0].__setitem__(0,'0'),
                       lambda x:x['roots'][0].update(tree=dict(kind='split',axis=0,cut='51/200',right={})),
                       lambda x:x.update(n=True)):
            changed = deepcopy(forest); mutate(changed)
            raw = sources.encoded(changed)
            (capsule/self.job['forest_filename']).write_bytes(raw)
            changed_job = deepcopy(self.job); changed_job['forest_sha256'] = sources.sha(raw)
            expected, _ = sources._selection(changed_job, (capsule/'KERNEL_COPY_MANIFEST.json').read_bytes())
            (capsule/sources.EPOCH).write_bytes(sources.encoded(sources._epoch(changed_job, expected)))
            with patch.object(sources, 'jobs', return_value=[changed_job]), self.assertRaises((ValueError,KeyError)):
                sources.census(changed_job, capsule)


if __name__ == '__main__':
    unittest.main()
