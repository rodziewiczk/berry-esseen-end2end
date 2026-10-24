"""Synthetic source/capture traps only; never import archived mathematics."""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from be_replay import finite1519_join_control_sources as src


class Sources(unittest.TestCase):
    def setUp(self):
        scratch=src.ROOT/'work'/'finite1519-join-fixtures'
        scratch.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)

    def write(self,name,raw):
        p=self.root.joinpath(*name.split('/'));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        return p

    def packet(self):
        script='work/controls/check.py';meta='work/controls/MANIFEST.json'
        body=b'# synthetic source, never executed\n'
        doc=src.encoded(dict(scope='source provenance only',files_sha256={script:sha256(body).hexdigest()}))
        pins={script:sha256(body).hexdigest(),meta:sha256(doc).hexdigest()}
        d=dict(source_files={n:dict(bytes=len(raw),sha256=pins[n])for n,raw in((script,body),(meta,doc))},
               original_files_sha256=pins,metadata_documents=[meta],cases=[dict(id='finite-high',script=script,
                 original_python_sha256=pins[script],output='work/controls/CHECKED.json',dependencies=[],
                 generated_engine_copies={},input_reference_graph=pins)])
        for name,raw in((script,body),(meta,doc)):
            self.write('provenance/original/'+name,raw);self.write('capsule/'+name,raw)
        return d,meta,script

    def test_real_plan_is_full_six_call_component_without_full_join_claim(self):
        d=src.plan()
        self.assertEqual(tuple(r['id']for r in d['cases']),src.IDS)
        self.assertEqual(len(d['source_files']),161)
        self.assertEqual(len(d['metadata_documents']),5)
        self.assertTrue(d['fresh_geometry_fixture']['current_execution_required'])
        self.assertFalse(d['full_finite_join_implemented'])
        self.assertTrue(all(d[k]is False for k in src.FALSE_FLAGS))

    def test_bad_exact_plan_pin_fails_before_output(self):
        with patch.object(src,'PLAN_SHA256','0'*64):
            with self.assertRaisesRegex(ValueError,'Pinned'):src.plan()
        self.assertEqual(list(self.root.iterdir()),[])

    def test_unsafe_or_noncanonical_source_paths_fail(self):
        for name in('../escape','/absolute','a\\b','x:y','a//b','a/./b'):
            with self.subTest(name=name),self.assertRaises(ValueError):src.child(self.root,name)

    def test_empty_prior_metadata_is_exact_data_operation_without_execution(self):
        d,meta,script=self.packet()
        with patch.object(src,'plan',return_value=d):
            ledger=src.derive_current_metadata(self.root,validated_prior_actions={})
            graph=src.input_map(self.root,'finite-high',validated_prior_actions={})
        self.assertEqual(graph,d['original_files_sha256'])
        self.assertEqual(set(json.loads((self.root/'capsule'/meta).read_bytes())),{'scope','files_sha256'})
        self.assertFalse(ledger['arithmetic_computed'])
        self.assertFalse(ledger['historical_capture_impersonated'])
        self.assertEqual((self.root/'capsule'/script).read_bytes(),b'# synthetic source, never executed\n')

    def test_changed_mathematical_program_cannot_be_rehashed_into_metadata(self):
        d,meta,script=self.packet();self.write('capsule/'+script,b'changed helper\n')
        with patch.object(src,'plan',return_value=d):
            src.derive_current_metadata(self.root,validated_prior_actions={})
            with self.assertRaisesRegex(ValueError,'Exact original input'):src.input_map(self.root,'finite-high',validated_prior_actions={})

    def test_forged_metadata_payload_or_source_map_is_rejected(self):
        for change in('scope','files_sha256'):
            with self.subTest(change=change):
                d,meta,_=self.packet();doc=json.loads((self.root/'capsule'/meta).read_bytes())
                if change=='scope':doc['scope']='accepted global theorem'
                else:doc['files_sha256']={}
                self.write('capsule/'+meta,src.encoded(doc))
                with patch.object(src,'plan',return_value=d),self.assertRaisesRegex(ValueError,'Exact declared'):
                    src.input_map(self.root,'finite-high',validated_prior_actions={})

    def test_missing_predecessor_cannot_be_satisfied_by_historical_control(self):
        d,_,_=self.packet();d['cases'][0]['dependencies']=['contact-high']
        with patch.object(src,'plan',return_value=d),self.assertRaisesRegex(ValueError,'preceding native'):
            src.input_map(self.root,'finite-high',validated_prior_actions={})

    def test_generated_engine_is_required_and_byte_identical(self):
        d,_,_=self.packet();name='work/controls/engine/math.py';raw=b'# native-created synthetic copy\n'
        d['cases'][0]['generated_engine_copies']={name:dict(bytes=len(raw),sha256=sha256(raw).hexdigest())}
        d['cases'][0]['input_reference_graph'][name]=sha256(raw).hexdigest()
        inputs={k:v for k,v in d['original_files_sha256'].items()if k!=name}
        with patch.object(src,'plan',return_value=d):
            with self.assertRaises(ValueError):src.output_graph(self.root,'finite-high',inputs)
            self.write('capsule/'+name,raw)
            self.assertEqual(src.output_graph(self.root,'finite-high',inputs)[name],sha256(raw).hexdigest())
            self.write('capsule/'+name,b'changed\n')
            with self.assertRaises(ValueError):src.output_graph(self.root,'finite-high',inputs)

    def test_geometry_never_accepts_missing_or_boolean_current_acceptance_pin(self):
        d,_,_=self.packet();d['cases'][0]['id']='join-geometry';d['fresh_geometry_fixture']={}
        with patch.object(src,'plan',return_value=d):
            for value in(None,True,'f'*63):
                with self.subTest(value=value),self.assertRaises(ValueError):
                    src.input_map(self.root,'join-geometry',validated_prior_actions={},fixture_acceptance_sha256=value)

    def test_cache_rejects_added_source_even_with_a_rehashed_marker(self):
        d,_,_=self.packet();d['cases'][0]['reference']=dict(bytes=2,sha256=sha256(b'{}').hexdigest())
        rows=src.cache_inventory(d)
        for name,row in rows.items():
            if name.startswith('original/'):
                raw=(self.root/'provenance'/name).read_bytes()
            else:raw=b'{}'
            self.write('cache/'+name,raw)
        self.write('cache/SOURCE_CACHE.json',src.encoded(dict(schema='FINITE1519_JOIN_CONTROL_CACHE_V1',
            source_plan_sha256=src.PLAN_SHA256,files=rows,**src.FALSE_FLAGS)))
        with patch.object(src,'plan',return_value=d):
            self.assertEqual(src.verify_cache(self.root/'cache'),rows)
            self.write('cache/original/extra.py',b'extra')
            with self.assertRaisesRegex(ValueError,'inventory'):src.verify_cache(self.root/'cache')


if __name__=='__main__':unittest.main()
