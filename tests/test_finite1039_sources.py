"""Synthetic transport/topology fixtures; no archived mathematical module runs."""
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from be_replay import finite1039_sources as src


def raw(d):return(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
BOX=[['0','1'],['0','1'],['0','1'],['-1/2','1/2'],['0','1']]


def nested():
    return dict(n=2,index=4,contract_sha256='c'*64,roots=[dict(k=k,tree=dict(kind='leaf',box=deepcopy(BOX),decision='EMPTY_SYNTHETIC',result=dict(status='EMPTY_SYNTHETIC')))for k in range(3)])


def flat():
    return dict(index=4,contract_sha256='c'*64,root=deepcopy(BOX),splits=[dict(k=0,path=[],axis=1)],
        leaves=[dict(k=0,path=[0],status='EMPTY_SYNTHETIC',score_upper=None),dict(k=0,path=[1],status='EMPTY_SYNTHETIC',score_upper=None),
                dict(k=1,path=[],status='EMPTY_SYNTHETIC',score_upper=None),dict(k=2,path=[],status='EMPTY_SYNTHETIC',score_upper=None)],visited=5)


class SourcesTests(unittest.TestCase):
    def test_both_representations_have_all_logical_roots(self):
        row=dict(n=2,index=4,contract_sha256='c'*64,family='count_protocol')
        self.assertEqual(src.inspect_candidate(row,nested()),dict(representation='nested_binary_count_forest',roots=3,nodes=3,leaves=3,maximum_depth=0))
        row['family']='strict';self.assertEqual(src.inspect_candidate(row,flat()),dict(representation='flat_split_leaf_paths',roots=3,nodes=5,leaves=4,maximum_depth=1))

    def test_nested_pending_root_boolean_and_census_rejected(self):
        row=dict(n=2,index=4,contract_sha256='c'*64,family='count_protocol')
        for mutate in (lambda p:p['roots'].pop(),lambda p:p['roots'][0].update(k=False),lambda p:p['roots'][0]['tree'].update(kind='pending'),lambda p:p.update(index=True),lambda p:p['roots'][0]['tree']['box'][0].__setitem__(0,'00')):
            p=nested();mutate(p)
            with self.assertRaises(ValueError):src.inspect_candidate(row,p)
        row['census']=dict(roots=999)
        with self.assertRaises(ValueError):src.inspect_candidate(row,nested())

    def test_nested_split_has_no_box_and_needs_both_children(self):
        p=nested();leaf=deepcopy(p['roots'][0]['tree']);p['roots'][0]['tree']=dict(kind='split',axis=0,cut='1/2',left=leaf,right=deepcopy(leaf))
        row=dict(n=2,index=4,contract_sha256='c'*64,family='count_protocol')
        self.assertEqual(src.inspect_candidate(row,p)['leaves'],4)
        del p['roots'][0]['tree']['right']
        with self.assertRaises(KeyError):src.inspect_candidate(row,p)

    def test_flat_disconnected_duplicate_boolean_and_bad_leaf_rejected(self):
        row=dict(n=2,index=4,contract_sha256='c'*64,family='strict')
        for mutate in (lambda p:p['leaves'].pop(),lambda p:p['leaves'].append(dict(k=1,path=[0],status='EMPTY',score_upper=None)),
                       lambda p:p['leaves'].append(deepcopy(p['leaves'][0])),lambda p:p['splits'][0].update(axis=True),
                       lambda p:p['leaves'][0].update(path=[False]),lambda p:p['leaves'][0].update(status=False,score_upper='0'),lambda p:p.update(visited=True)):
            p=flat();mutate(p)
            with self.assertRaises(ValueError):src.inspect_candidate(row,p)

    def test_four_dimensional_auxiliary_targets_contract_is_preserved(self):
        row=dict(n=2,index=4,contract_sha256='c'*64,family='strict',dimensions=4,candidate_contract_field='targets_sha256')
        p=flat();p['targets_sha256']=p.pop('contract_sha256');p['root']=p['root'][:4]
        self.assertEqual(src.inspect_candidate(row,p)['roots'],3)
        p['splits'][0]['axis']=4
        with self.assertRaises(ValueError):src.inspect_candidate(row,p)

    def setup_catalog(self,root):
        directory='original/capsule4';payloads={directory+'/count_protocol.py':b'raise AssertionError("MATHEMATICAL TRAP MUST NOT IMPORT")\n',
            directory+'/contract.json':raw(dict(synthetic_only=True)),directory+'/COUNT4_FOREST.json':raw(nested())}
        row=dict(job_id='synthetic.fixed',lane='n10_14',family='count_protocol',n=2,index=4,directory=directory,
            candidate='COUNT4_FOREST.json',script='count_protocol.py',arguments=['accept'],output='COUNT4_ACCEPTED.json',
            contract_sha256='c'*64,source_files_sha256={k:sha(v)for k,v in payloads.items()})
        archive=root/'original.zip'
        with zipfile.ZipFile(archive,'w')as z:
            for k,v in payloads.items():z.writestr(k,v)
            z.writestr(directory+'/COUNT4_ACCEPTED.json',raw(dict(status='HISTORICAL_PASS_IS_NOT_INPUT')))
        asset=dict(name=archive.name,bytes=archive.stat().st_size,sha256=src.digest(archive),url='https://invalid.example/unused')
        d=dict(jobs=[row],lane_ready=dict(n10_14=True,n26_30=False),source_files={k:dict(archive=archive.name,member=k,bytes=len(v),sha256=sha(v))for k,v in payloads.items()},assets=[asset])
        return d,row,archive

    def test_exact_source_cache_and_fresh_capsule_do_not_import_math_or_copy_old_acceptance(self):
        with tempfile.TemporaryDirectory()as tmp:
            root=Path(tmp);d,row,archive=self.setup_catalog(root)
            with patch.object(src,'catalog',return_value=d):
                cache=src.prepare_cache({archive.name:archive},root/'cache','n10_14');m=src.prepare_job(row['job_id'],cache,root/'task')
                self.assertFalse(m['arithmetic_computed']);self.assertFalse((root/'task/capsule'/src.output_relative(row)).exists())
                output=root/'task/capsule'/src.output_relative(row);output.write_bytes(raw(dict(status='FAKE_NEW_OUTPUT')))
                src.verify_job(root/'task')
                (output.parent/'unbound.py').write_bytes(b'raise AssertionError()')
                with self.assertRaises(ValueError):src.verify_job(root/'task')

    def test_tampered_transport_source_and_capsule_are_rejected(self):
        with tempfile.TemporaryDirectory()as tmp:
            root=Path(tmp);d,row,archive=self.setup_catalog(root)
            with patch.object(src,'catalog',return_value=d):
                cache=src.prepare_cache({archive.name:archive},root/'cache','n10_14')
                p=cache/row['directory']/row['script'];p.write_bytes(b'changed')
                with self.assertRaises(ValueError):src.prepare_job(row['job_id'],cache,root/'bad')
                archive.write_bytes(archive.read_bytes()+b'bad')
                with self.assertRaises(ValueError):src.prepare_cache({archive.name:archive},root/'next','n10_14')

    def test_zip_preflight_rejects_traversal_duplicate_link_size_and_case(self):
        cases=[['../escape'],['/absolute'],['C:/absolute'],['same','same'],['a','A']]
        for names in cases:
            with self.subTest(names=names):
                data=io.BytesIO()
                with zipfile.ZipFile(data,'w')as z:
                    for n in names:z.writestr(n,b'fixture')
                data.seek(0)
                with zipfile.ZipFile(data)as z,self.assertRaises(ValueError):src.zip_index(z)
        for kind in ('link','size'):
            info=zipfile.ZipInfo('ordinary');info.external_attr=(stat.S_IFLNK|0o777)<<16 if kind=='link'else 0;info.file_size=257*src.MIB if kind=='size'else 0
            fake=type('Fake',(),{'infolist':lambda self:[info]})()
            with self.assertRaises(ValueError):src.zip_index(fake)

    def test_fixed_selection_rejects_arbitrary_job_or_lane(self):
        with patch.object(src,'catalog',return_value=dict(jobs=[])):
            with self.assertRaises(ValueError):src.jobs('arbitrary')
            with self.assertRaises(ValueError):src.job('../not-selected')

    def test_missing_selected_candidate_blocks_lane_before_any_filesystem_or_download(self):
        d=dict(jobs=[],lane_ready=dict(n26_30=False))
        with patch.object(src,'catalog',return_value=d),patch.object(src.urllib.request,'urlopen',side_effect=AssertionError('No download for unready lane')):
            with self.assertRaisesRegex(ValueError,'not source-complete'):src.jobs('n26_30')
            with tempfile.TemporaryDirectory()as tmp:
                with self.assertRaisesRegex(ValueError,'not source-complete'):src.prepare_cache({},Path(tmp)/'never-created','n26_30')
                self.assertFalse((Path(tmp)/'never-created').exists())

    def test_actual_frozen_catalog_keeps_all_obligations_and_no_old_own_receipt_input(self):
        d=src.catalog();self.assertEqual(d['expected_forests'],1009);self.assertEqual(len(d['jobs']),1008)
        self.assertEqual(set(d['not_ready_lanes']),{'n26_30'});self.assertFalse(d['lane_ready']['n26_30'])
        self.assertEqual(d['not_ready_lanes']['n26_30']['available_forests'],79)
        self.assertEqual(sum(r.get('child_runtime_required',False)for r in d['jobs']),218)
        for row in d['jobs']:
            prefix=row['directory']+'/'
            self.assertNotIn(src.output_relative(row),row['source_files_sha256'])
            self.assertEqual(row['source_files_sha256'][prefix+row['candidate']],row['candidate_sha256'])
            self.assertEqual(row['source_files_sha256'][prefix+row['contract_name']],row['contract_sha256'])
            self.assertNotIn('child_runtime',row['expected_receipt'])
            for name,pin in row['source_files_sha256'].items():self.assertEqual(d['source_files'][name]['sha256'],pin)


if __name__=='__main__':unittest.main()
