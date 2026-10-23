"""Evidence-collection fixtures only; all native validators/mapper are mocked."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

from be_replay import n25_collect as join, count_task, n25_parents


P_INTERVALS = {
    'b4-q0':['29/100','117/400'], 'b4-q1':['117/400','59/200'],
    'b4-q2':['59/200','119/400'], 'b4-q3':['119/400','3/10'],
    'b3-p31-v14-new':['31/100','8/25'], 'b3-p32-v14-new':['8/25','33/100'],
    'b3-p33':['33/100','17/50'],
}


class N25CollectorTests(unittest.TestCase):
    def setUp(self):
        parent = Path(join.__file__).resolve().parents[1]/'work/n25-collect-fixtures'
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work, self.durable = self.root/'work', self.root/'durable'
        self.work.mkdir()
        self.counts = SimpleNamespace(__file__=__file__,validate_completed=self.validate_count)
        self.parents = SimpleNamespace(__file__=__file__,validate_completed=self.validate_parent)
        self.mapper = SimpleNamespace(__file__=__file__,validate=self.map_contract,target_spec=self.reference_spec)
        self.addCleanup(patch.stopall)
        patch.object(join,'validators',return_value=(self.counts,self.parents,self.mapper)).start()

    def make_zip(self,key,stamp='20261023T130000Z-fixture'):
        directory = self.durable/key/stamp
        directory.mkdir(parents=True)
        output = directory/(stamp+'-results.zip')
        with zipfile.ZipFile(output,'x') as z:
            def write(name,value):
                raw = json.dumps(value,indent=2).encode()
                z.writestr(stamp+'/task/'+name,raw)
                import hashlib
                return hashlib.sha256(raw).hexdigest()
            branch = 'b4' if key.startswith('b4-') or key.endswith('-b4') else 'b3'
            common = dict(branch=branch,n=25,native_arithmetic_accepted=True,all_index_conclusion_verified=False)
            if key in join.COUNTS:
                accepted = 'accept-fixture'
                contract_sha = write(accepted+'/capsule/contract.json',dict(target=key))
                actual_report_sha = write(accepted+'/NATIVE_ACCEPTED.json',dict(fixture_only=True,target=key))
                if key.endswith('-v14-new'):
                    write(accepted+'/capsule/ORIGINAL_V12_CONTRACT.json',dict(original_v12=True))
                packet = dict(common,schema='REVALIDATED_N25_COUNT_V1',target=key,index=count_task.TARGETS[key][1],
                    design_sha256=count_task.TARGETS[key][2],census=dict(roots=26,nodes=28,leaves=27),
                    accepted_capsule_relative=accepted+'/capsule',accepted_report_relative=accepted+'/NATIVE_ACCEPTED.json',
                    accepted_report_sha256=actual_report_sha,contract_sha256=contract_sha,parent_acquisitions_verified=False)
            else:
                names = n25_parents.names(branch)
                base='attempts/resource-accept-fixture/new_root'
                resource_sha = write(base+'/'+names['resource_dir']+'/'+names['resource_proof'],dict(branch=branch,fresh_fixture=True))
                packet = dict(common,schema='REVALIDATED_N25_PARENT_V1',contact_allowance='5/16',
                    stronger24_acquisition_verified=False,count_interface_join_verified=False,
                    resource_capsule_relative=base,resource_proof_sha256=resource_sha,resource_receipt_sha256='a'*64)
            write('FIXTURE_PACKET.json',packet)
        output.with_suffix('.zip.sha256').write_text(join.common.digest(output)+'  '+output.name+'\n')
        return output

    def validate_count(self,task,*,expected_target):
        packet = join.common.read(Path(task)/'FIXTURE_PACKET.json')
        if packet.get('target') != expected_target:
            raise ValueError('Fixture target mismatch')
        return packet

    def validate_parent(self,task,*,expected_branch):
        packet = join.common.read(Path(task)/'FIXTURE_PACKET.json')
        if packet.get('branch') != expected_branch:
            raise ValueError('Fixture branch mismatch')
        return packet

    def map_contract(self,target,*,resource_proof,contract,original_v12_contract=None):
        branch='b4' if target.startswith('b4-') else 'b3'
        if resource_proof['branch'] != branch or contract['target'] != target:
            raise ValueError('Wrong fixture resource/contract object')
        if target.endswith('-v14-new') and original_v12_contract != dict(original_v12=True):
            raise ValueError('Missing fixture original V12 reference')
        return dict(schema='N25_RESOURCE_COUNT_INTERFACE_V1',target=target,branch=branch,
                    expected_p_interval=P_INTERVALS[target],numeric_interface_verified=True,
                    analytic_attained_contact_premise_acquired=False)

    def reference_spec(self,target):
        import hashlib
        return dict(original_v12_reference_filename='ORIGINAL_V12_CONTRACT.json',
                    original_v12_reference_file_sha256=hashlib.sha256(json.dumps(dict(original_v12=True),indent=2).encode()).hexdigest())

    def complete_inputs(self):
        for key in join.JOBS:
            self.make_zip(key)

    def run_join(self):
        with redirect_stdout(io.StringIO()):
            return join.run(self.durable,self.work)

    def test_empty_drive_waits_without_calling_mapper_or_accepting(self):
        with patch.object(self.mapper,'validate',side_effect=AssertionError('No interface without inputs')):
            result=self.run_join()
        self.assertEqual(result['status'],'WAITING_FOR_N25_EVIDENCE')
        self.assertEqual(len(result['missing_jobs']),9)
        self.assertFalse(result['selected_interfaces_verified'])

    def test_all_nine_exports_verify_only_seven_selected_interfaces(self):
        self.complete_inputs()
        result=self.run_join()
        self.assertEqual(result['status'],'CONDITIONAL_SEVEN_N25_COUNT_INTERFACES_VERIFIED')
        self.assertTrue(result['selected_interfaces_verified'])
        self.assertEqual(set(result['interfaces']),set(join.COUNTS))
        self.assertTrue(all(result[field] is False for field in join.FALSE_FLAGS))
        self.assertEqual(result['selected_closed_cover']['b4_p29_closed_quarter_endpoints'][0],'29/100')
        self.assertEqual(result['selected_closed_cover']['b3_closed_panel_endpoints'][-1],'17/50')
        for row in result['imports'].values():
            self.assertEqual(row['zip_sha256'],join.common.digest(row['zip_path']))
            self.assertEqual(row['validated_report_sha256'],join.common.digest(self.work/row['validated_report_relative']))

    def test_b3_can_be_checked_while_missing_b4_evidence_still_waits(self):
        for key in ('n25-parents-b3','b3-p33','b3-p31-v14-new','b3-p32-v14-new'):
            self.make_zip(key)
        result=self.run_join()
        self.assertEqual(len(result['interfaces']),3)
        self.assertEqual(len(result['pending_interfaces']),4)
        self.assertFalse(result['selected_interfaces_verified'])

    def test_missing_or_changed_sidecar_is_not_a_complete_export(self):
        path=self.make_zip('b3-p33')
        path.with_suffix('.zip.sha256').write_text('0'*64+'  '+path.name+'\n')
        result=self.run_join()
        self.assertNotIn('b3-p33',result['imports'])
        self.assertTrue(any('sidecar' in x['reason'] for m in result['missing_jobs'] for x in m['reasons']))

    def test_boolean_n_wrong_design_or_promoted_parent_scope_rejects(self):
        self.complete_inputs()
        with redirect_stdout(io.StringIO()):
            imported,_=join.collect(self.durable,self.work,progress=lambda *a,**kw:None)
        for field,value in (('n',True),('design_sha256','0'*64),('parent_acquisitions_verified',True)):
            packet=dict(imported['b3-p33']['report'],**{field:value})
            with self.subTest(field=field),self.assertRaises(ValueError):
                join.validate_scope('b3-p33',packet)
        packet=dict(imported['n25-parents-b4']['report'],contact_allowance='0')
        with self.assertRaises(ValueError):join.validate_scope('n25-parents-b4',packet)

    def test_resource_changed_after_revalidation_cannot_supply_contract(self):
        self.complete_inputs()
        imported,_=join.collect(self.durable,self.work,progress=lambda *a,**kw:None)
        row=imported['n25-parents-b3']
        task=self.work/row['task_relative']
        path=task/row['report']['resource_capsule_relative']/n25_parents.names('b3')['resource_dir']/n25_parents.names('b3')['resource_proof']
        path.write_text('{}')
        with self.assertRaisesRegex(ValueError,'Exact imported fresh resource'):
            join.interfaces(imported,self.work,progress=lambda *a,**kw:None)

    def test_interface_failure_is_not_downgraded_to_success(self):
        self.complete_inputs()
        with patch.object(self.mapper,'validate',side_effect=ValueError('Synthetic incompatible exact contract')):
            with self.assertRaisesRegex(ValueError,'incompatible exact contract'):
                self.run_join()

    def test_b4_wrong_closed_quarter_is_rejected(self):
        packets={key:dict(interface=dict(expected_p_interval=value))for key,value in P_INTERVALS.items()}
        join.cover(packets)
        packets['b4-q1']['interface']['expected_p_interval']=['117/400','3/10']
        with self.assertRaisesRegex(ValueError,'Four literal closed'):
            join.cover(packets)

    def test_containment_rejects_traversal_absolute_and_backslash(self):
        for name in ('../outside','/outside','C:/outside','a\\b','a//b','a/./b'):
            with self.subTest(name=name),self.assertRaises(ValueError):
                join.contained(self.work,name)

    def test_waiting_and_failure_still_preserve_final_bundle(self):
        with redirect_stdout(io.StringIO()):
            result=join.run_colab(durable_root=self.durable,work_root=self.root/'sessions')
        self.assertEqual(result['status']['state'],'WAITING_FOR_N25_EVIDENCE')
        self.assertTrue(Path(result['bundle']).is_file())
        with patch.object(join,'run',side_effect=ValueError('fixture failure')),redirect_stdout(io.StringIO()):
            result=join.run_colab(durable_root=self.durable,work_root=self.root/'sessions')
        self.assertEqual(result['status']['state'],'PARTIAL_ERROR_NOT_ACCEPTED')
        self.assertFalse(result['status']['full_n25_verified'])
        with zipfile.ZipFile(result['bundle']) as z:
            self.assertTrue(any(name.endswith('/ERROR.txt')for name in z.namelist()))


if __name__=='__main__':
    unittest.main()
