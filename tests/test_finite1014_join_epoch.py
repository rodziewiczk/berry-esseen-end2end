import json
import unittest
from be_replay import finite1014_join_epoch as e


class MetadataEpochTests(unittest.TestCase):
    def fixture(self):
        a='work/PREPARED.json';b='work/FROZEN.json';source='work/kernel.py';fresh='work/prior/CHECKED.json';missing='runs/old/metadata.json'
        original={source:e.digest(b'trap kernel, never imported'),fresh:e.digest(b'old unacquired receipt')}
        ar=e.encode(dict(status='CONDITIONAL',n=10,rows=[dict(value='3/7',flag=False)],files_sha256={source:original[source],fresh:original[fresh],missing:e.digest(b'absent')}));original[a]=e.digest(ar)
        br=e.encode(dict(status='FROZEN_SOURCE_ONLY',parts=[0,1,2,3],files_sha256={a:original[a],source:original[source]}));original[b]=e.digest(br)
        current=dict(original);current[fresh]=e.digest(b'actual current stopped output')
        return dict(documents={a:ar,b:br},original_files_sha256=original,current_files_sha256=current,unavailable={missing:e.digest(b'absent')},allowed_overrides=[fresh])

    def test_recursive_epoch_preserves_every_non_graph_field(self):
        f=self.fixture();out=e.derive_metadata_epoch(**f)
        for name,raw in f['documents'].items():
            old=e.loads(raw);new=e.loads(out['derived'][name]);self.assertTrue(e.same({k:v for k,v in old.items()if k!='files_sha256'},{k:v for k,v in new.items()if k!='files_sha256'}))
        names=list(f['documents']);self.assertEqual(e.loads(out['derived'][names[1]])['files_sha256'][names[0]],e.digest(out['derived'][names[0]]))
        self.assertEqual(len(out['ledger']['documents'][names[0]]['omitted_historical_edges']),1)
        self.assertFalse(out['ledger']['historical_capture_impersonated']);self.assertFalse(out['ledger']['arithmetic_computed'])
        self.assertEqual(out,e.derive_metadata_epoch(**f))

    def test_fresh_validated_output_may_reproduce_original_bytes(self):
        f=self.fixture();name=f['allowed_overrides'][0];f['current_files_sha256'][name]=f['original_files_sha256'][name]
        out=e.derive_metadata_epoch(**f);self.assertEqual(out['ledger']['validated_current_overrides'][name]['original_sha256'],out['ledger']['validated_current_overrides'][name]['current_sha256'])

    def test_unapproved_changed_payload_rejected(self):
        f=self.fixture();f['current_files_sha256']['work/kernel.py']=e.digest(b'mutated math')
        with self.assertRaisesRegex(ValueError,'Every changed input'):e.derive_metadata_epoch(**f)

    def test_missing_math_source_rejected(self):
        f=self.fixture();f['unavailable']['work/kernel.py']=f['original_files_sha256'].pop('work/kernel.py');f['current_files_sha256'].pop('work/kernel.py')
        with self.assertRaises(ValueError):e.derive_metadata_epoch(**f)

    def test_missing_capture_pin_and_staged_alias_rejected(self):
        for mode in('wrongpin','alias'):
            f=self.fixture();name=next(iter(f['unavailable']))
            if mode=='wrongpin':f['unavailable'][name]='0'*64
            else:f['original_files_sha256'][name]=f['current_files_sha256'][name]=f['unavailable'][name]
            with self.subTest(mode=mode),self.assertRaises(ValueError):e.derive_metadata_epoch(**f)

    def test_duplicate_and_nonfinite_json_rejected(self):
        for raw in(b'{"files_sha256":{},"n":1,"n":2}',b'{"files_sha256":{},"n":NaN}'):
            f=dict(documents={'work/FROZEN.json':raw},original_files_sha256={'work/FROZEN.json':e.digest(raw)},current_files_sha256={'work/FROZEN.json':e.digest(raw)},unavailable={})
            with self.subTest(raw=raw),self.assertRaises(ValueError):e.derive_metadata_epoch(**f)

    def test_cycle_unknown_edge_and_path_rejected(self):
        # An actual cryptographic cycle cannot be manufactured here; exercise
        # the original-edge validation and named containment independently.
        f=self.fixture();name=next(iter(f['documents']));v=e.loads(f['documents'][name]);v['files_sha256']['work/UNKNOWN.json']='0'*64;raw=e.encode(v);f['documents'][name]=raw;f['original_files_sha256'][name]=f['current_files_sha256'][name]=e.digest(raw)
        with self.assertRaisesRegex(ValueError,'Every original graph edge'):e.derive_metadata_epoch(**f)
        for name in('../x','/x','work/../x','work\\x','C:/x'):
            with self.subTest(name=name),self.assertRaises(ValueError):e.path(name)


if __name__=='__main__':unittest.main()
