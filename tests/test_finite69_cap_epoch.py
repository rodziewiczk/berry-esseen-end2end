"""Synthetic metadata-only epoch fixtures; no original numerical execution."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch

from be_replay import finite69_cap_epoch as caps
from be_replay import finite69_metadata as initial
from test_finite69_metadata import resource_fixture


def raw(p):return(json.dumps(p,indent=2)+"\n").encode()


class CapEpoch(unittest.TestCase):
    def setUp(self):
        script,pb,sb,parent,pins,port=resource_fixture()
        graph={p:hashlib.sha256(p.encode()).hexdigest()for p in caps.DYNAMIC}
        graph.update({f"work/synthetic/static{i}.py":hashlib.sha256(str(i).encode()).hexdigest()
                      for i in range(182-len(graph))})
        self.old=dict(status="PASS_EXACT_TIGHTER_LITERAL7_9_OWNCAPS",caps=copy.deepcopy(caps.CAPS),
            whole_accepted_rows=344,selected_n_rows=258,strips_per_band=dict(B0=30,BN=28,BC=28),
            accepted_upper={b:{str(n):"4097/10000"for n in(6,7,8,9)}for b in caps.TARGETS},
            negative_controls=[f"synthetic-control-{i}"for i in range(17)],files_sha256=graph,
            scope="SYNTHETIC metadata only; never a certificate")
        self.old_raw=raw(self.old);pins.update(graph);pins[caps.CAPS_PATH]=caps.sha(self.old_raw)
        source,prepared=json.loads(sb),json.loads(pb)
        for packet in(source,prepared):packet['files_sha256'].update(graph|{caps.CAPS_PATH:caps.sha(self.old_raw)})
        self.sb=raw(source);directory=initial.RESOURCE+"/n7_B0"
        prepared['source_sha256']=caps.sha(self.sb)
        prepared['files_sha256'][directory+"/SOURCE_RESULT.json"]=caps.sha(self.sb)
        self.pb=raw(prepared);pins[directory+"/SOURCE_RESULT.json"]=caps.sha(self.sb)
        pins[directory+"/PREPARED.json"]=caps.sha(self.pb)
        self.fresh=copy.deepcopy(self.old)
        self.fresh['files_sha256'].update({p:hashlib.sha256((p+'fresh').encode()).hexdigest()for p in caps.DYNAMIC})
        self.script,self.parent,self.pins=script,parent,pins
        for name,value in(('ORIGINAL_CAPS_SHA',caps.sha(self.old_raw)),):
            p=patch.object(caps,name,value);p.start();self.addCleanup(p.stop)
        for name,value in(('ORIGINAL_RESOURCE_REPLAY_SHA256',caps.sha(script)),('RESOURCE_REPLAY_SHA256',caps.sha(port))):
            p=patch.object(initial,name,value);p.start();self.addCleanup(p.stop)

    def invoke(self,fresh=None):
        b=raw(self.fresh if fresh is None else fresh)
        actual=dict(json.loads(b)['files_sha256'])|{caps.CAPS_PATH:caps.sha(b)}
        return caps.derive_resource_epoch(self.script,self.pb,self.sb,self.parent,self.old_raw,b,
            n=7,band='B0',source_pins=self.pins,fresh_files_sha256=actual)

    def test_complete_182_row_epoch_keeps_all_resource_numeric_fields(self):
        saved=copy.deepcopy(self.pins);result=self.invoke()
        before,after=json.loads(self.sb),json.loads(result['fresh_source_result_bytes'])
        self.assertEqual(before['rows'],after['rows'])
        self.assertEqual(before['seconds'],after['seconds'])
        self.assertNotEqual(before['initial_receipt_sha256'],after['initial_receipt_sha256'])
        self.assertEqual(result['replay_bytes'],self.script.replace(b"'PREPARED.json'",b"'FRESH_PREPARED.json'").replace(b"'SOURCE_RESULT.json'",b"'FRESH_SOURCE_RESULT.json'"))
        self.assertEqual(self.pins,saved)
        report=result['cap_epoch_report']
        self.assertEqual(report['complete_ancestor_rows'],182)
        self.assertEqual(len(report['dynamic_ancestor_paths']),11)
        self.assertEqual(result['report']['fresh_source_result_sha256'],caps.sha(result['fresh_source_result_bytes']))
        self.assertEqual(result['report']['fresh_prepared_sha256'],caps.sha(result['fresh_prepared_bytes']))
        self.assertNotEqual(result['intermediate_initial_epoch_report']['fresh_source_result_sha256'],
                            result['report']['fresh_source_result_sha256'])
        for flag in('fresh_caps_execution_evidence_verified','fresh_initial_execution_evidence_verified',
                    'mathematical_arithmetic_computed','actual_support_acquired','full_finite69_verified','all_index_conclusion_verified'):
            self.assertIs(report[flag],False)

    def test_changed_static_source_rejected_even_when_fresh_graph_recaptured(self):
        p=copy.deepcopy(self.fresh);p['files_sha256']['work/synthetic/static0.py']='0'*64
        with self.assertRaises(ValueError):self.invoke(p)

    def test_changed_cap_payload_and_scope_rejected(self):
        for field,value in(('whole_accepted_rows',True),('selected_n_rows',259),('caps',{}),('negative_controls',[]),('scope','new scope')):
            p=copy.deepcopy(self.fresh);p[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.invoke(p)

    def test_incomplete_strips_and_bad_tighter_maximum_rejected(self):
        for mutate in(lambda p:p['strips_per_band'].update(B0=29),
                      lambda p:p['strips_per_band'].update(BN=True),
                      lambda p:p['accepted_upper']['BC'].update({'9':'41/100'}),
                      lambda p:p['accepted_upper']['B0'].pop('8'),
                      lambda p:p['accepted_upper']['BN'].update({'7':'.4097'})):
            p=copy.deepcopy(self.fresh);mutate(p)
            with self.assertRaises(ValueError):self.invoke(p)

    def test_whole_actual_inventory_and_old_external_pins_required(self):
        b=raw(self.fresh);actual=dict(self.fresh['files_sha256'])|{caps.CAPS_PATH:caps.sha(b)}
        for missing in(caps.CAPS_PATH,next(iter(caps.DYNAMIC))):
            broken=dict(actual);del broken[missing]
            with self.assertRaises(ValueError):caps.cap_binding(self.old_raw,b,self.pins,broken)
        broken=dict(self.pins);broken[next(iter(caps.DYNAMIC))]='0'*64
        with self.assertRaises(ValueError):caps.cap_binding(self.old_raw,b,broken,actual)

    def test_unreviewed_graph_member_or_numeric_row_mutation_rejected(self):
        p=copy.deepcopy(self.fresh);p['files_sha256']['work/extra.py']='a'*64
        with self.assertRaises(ValueError):self.invoke(p)
        original=json.loads(self.sb);original['rows'][42]['result']['synthetic']='changed'
        original_bytes=raw(original)
        with self.assertRaises(ValueError):caps.derive_resource_epoch(self.script,self.pb,original_bytes,self.parent,
            self.old_raw,raw(self.fresh),n=7,band='B0',source_pins=self.pins,
            fresh_files_sha256=self.fresh['files_sha256']|{caps.CAPS_PATH:caps.sha(raw(self.fresh))})


if __name__=='__main__':unittest.main()
