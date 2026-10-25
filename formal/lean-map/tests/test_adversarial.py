"""Independent malformed-input and end-to-end controls for the scoped pilot."""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from be.codec import (MAX_BYTES, MAX_DEPTH, MAX_INTEGER_DIGITS, canonical_bytes,
                      loads, parse_integer, parse_rational)
from be.errors import ProtocolError


class CodecAdversarialTests(unittest.TestCase):
    def test_ambiguous_or_noncanonical_transport_is_rejected(self):
        cases = [
            b'{"x":"first","x":"second"}',
            b'{"x":1}',
            b'{"x":0.5}',
            b'{"x":NaN}',
            b'{"x":Infinity}',
            b' {"x":"same"}',
            b'{"x":"same"}\n',
            b'\xef\xbb\xbf{}',
            b'{"x":"\xc3\xa9"}',
            b'{"x":"\\u0061"}',
            b'{}{}',
        ]
        for raw in cases:
            with self.subTest(raw=raw):
                with self.assertRaises(ProtocolError):
                    loads(raw)

    def test_declared_byte_and_depth_limits_fail_closed(self):
        with self.assertRaises(ProtocolError):
            loads(b' ' * (MAX_BYTES + 1))
        with self.assertRaises(ProtocolError):
            loads(b'[' * (MAX_DEPTH + 2) + b'null' + b']' * (MAX_DEPTH + 2))

    def test_fraction_aliases_and_zero_denominator_are_rejected(self):
        for num, den in [('2','4'), ('0','2'), ('-0','1'), ('01','1'),
                         ('1','0'), ('1','-1'), ('+1','2')]:
            with self.subTest(num=num, den=den):
                with self.assertRaises(ProtocolError):
                    parse_rational({'num':num, 'den':den})
        self.assertEqual(parse_rational({'num':'0', 'den':'1'}), Fraction(0))

    def test_integer_digit_limit_counts_digits_not_sign(self):
        digits = '7' * MAX_INTEGER_DIGITS
        self.assertGreater(parse_integer(digits), 0)
        self.assertLess(parse_integer('-' + digits), 0)
        for value in [digits + '7', '-' + digits + '7']:
            with self.subTest(sign=value[0]):
                with self.assertRaises(ProtocolError):
                    parse_integer(value)

    def test_canonical_bytes_are_stable_and_do_not_allow_floats(self):
        value = {'z':None, 'a':[True, False, {'num':'1', 'den':'4'}]}
        self.assertEqual(loads(canonical_bytes(value)), value)
        self.assertEqual(canonical_bytes(value), canonical_bytes(loads(canonical_bytes(value))))
        with self.assertRaises(ProtocolError):
            canonical_bytes({'p':0.25})


class SemanticAdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from be.codec import load_json
        cls.source = load_json(ROOT / 'examples/local-pilot/source-manifest.json')
        cls.trust = load_json(ROOT / 'examples/local-pilot/trust-profile.json')
        cls.problem = load_json(ROOT / 'examples/local-pilot/problem.json')

    def request(self, *, p=None, lower=None, upper=None, bits=None):
        from be.codec import rational
        from be.semantic import freeze_request
        problem = copy.deepcopy(self.problem)
        if p is not None:
            problem['context']['p'] = rational(p)
        if lower is not None:
            problem['context']['rho']['lower'] = rational(lower)
        if upper is not None:
            problem['context']['rho']['upper'] = rational(upper)
        if bits is not None:
            problem['numeric_policy']['sqrt_bits'] = str(bits)
        return freeze_request(problem, self.source, self.trust)

    def test_both_strict_separations_produce_valid_source_bound_witnesses(self):
        from be.producer import produce_request
        from be.semantic import verify_request
        for lower, upper in [(1,1),(2,2)]:
            with self.subTest(lower=lower):
                req = self.request(lower=lower, upper=upper)
                result = verify_request(req, produce_request(req))['core']
                self.assertEqual(result['outcome'], 'infeasible')
                self.assertEqual(result['farkas_totals']['normal'],
                                 [{'num':'0','den':'1'}] * 2)
                self.assertLess(parse_rational(result['farkas_totals']['rhs']), 0)
                self.assertTrue(result['conditional'])
                self.assertFalse(result['full_proof_pass'])

    def test_equality_and_wide_rho_are_not_excluded(self):
        from be.producer import produce_request
        from be.semantic import verify_request
        cases = [dict(p=Fraction(1,2),lower=1,upper=1),
                 dict(lower=1,upper=2),
                 dict(p=Fraction(9,25),lower=Fraction(337,300),upper=Fraction(337,300))]
        for case in cases:
            with self.subTest(case=case):
                req = self.request(**case)
                receipt = verify_request(req, produce_request(req))
                self.assertEqual(receipt['core']['outcome'], 'no_contradiction')
                self.assertFalse(receipt['core']['full_proof_pass'])

    def test_coarse_enclosure_is_inconclusive_without_precision_alias(self):
        from be.producer import produce_request
        from be.semantic import verify_request
        coarse = self.request(lower=Fraction(361,250),upper=Fraction(361,250),bits=8)
        fine = self.request(lower=Fraction(361,250),upper=Fraction(361,250),bits=128)
        self.assertNotEqual(coarse['request_id'], fine['request_id'])
        self.assertEqual(verify_request(coarse,produce_request(coarse))['core']['outcome'], 'no_contradiction')
        self.assertEqual(verify_request(fine,produce_request(fine))['core']['outcome'], 'infeasible')
        self.assertEqual(verify_request(fine,produce_request(coarse))['core']['outcome'], 'rejected')

    def test_wrong_problem_binding_cannot_import_unrelated_contradiction(self):
        from be.codec import digest
        from be.producer import produce_request
        from be.semantic import derive_problem, verify_request
        req = self.request()
        wrong = derive_problem(req)
        wrong['rows'][0]['rhs'] = {'num':'-1','den':'1'}
        candidate = produce_request(req)
        candidate['problem_digest'] = digest('derived-problem', wrong)
        result = verify_request(req,candidate)['core']
        self.assertEqual(result['outcome'], 'rejected')
        self.assertEqual(result['reason_code'], 'problem_binding_mismatch')

    def test_invalid_farkas_weights_and_unknown_witness_fail_closed(self):
        from be.producer import produce_request
        from be.semantic import verify_request
        req = self.request()
        base = produce_request(req)
        variants = []
        value = copy.deepcopy(base); value['witness']['multipliers'] = [{'num':'0','den':'1'}]*6; variants.append(value)
        value = copy.deepcopy(base); value['witness']['multipliers'][0] = {'num':'-1','den':'1'}; variants.append(value)
        value = copy.deepcopy(base); value['witness']['multipliers'].pop(); variants.append(value)
        value = copy.deepcopy(base); value['witness']['multipliers'][0] = {'num':'2','den':'4'}; variants.append(value)
        value = copy.deepcopy(base); value['witness']['kind'] = 'unchecked_empty'; variants.append(value)
        for candidate in variants:
            with self.subTest(witness=candidate['witness']):
                self.assertEqual(verify_request(req,candidate)['core']['outcome'], 'rejected')

    def test_out_of_scope_inputs_are_not_interpreted_as_empty(self):
        for case in [dict(p=0),dict(p=Fraction(3,4)),dict(lower=Fraction(1,2),upper=1),
                     dict(lower=2,upper=1),dict(bits=7),dict(bits=513)]:
            with self.subTest(case=case):
                with self.assertRaises(ProtocolError):
                    self.request(**case)

    def test_changed_source_pin_is_rejected_before_numeric_acceptance(self):
        from be.codec import digest
        from be.semantic import freeze_request
        source = copy.deepcopy(self.source)
        source['source_files'][0]['bytes_digest'] = 'sha256:' + '0'*64
        trust = copy.deepcopy(self.trust)
        trust['source_manifest_digest'] = digest('source-manifest',source)
        with self.assertRaises(ProtocolError):
            freeze_request(self.problem,source,trust)

    def test_altered_receipt_boolean_is_not_trusted(self):
        from be.producer import produce_request
        from be.semantic import authorized_readback, verify_request
        req = self.request(p=Fraction(1,2))
        candidate = produce_request(req)
        forged = verify_request(req,candidate)
        forged['core']['outcome'] = 'infeasible'
        with self.assertRaises(ProtocolError):
            authorized_readback(req,candidate,forged)


class DurableStateAdversarialTests(unittest.TestCase):
    def setUp(self):
        from be.ledger import SQLiteLedger
        from be.store import LocalCAS
        temporary_root = ROOT / '.test_tmp'
        temporary_root.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix='be-adversarial-', dir=temporary_root)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.now = [1000.0]
        self.store = LocalCAS(self.root/'artifacts')
        self.ledger = SQLiteLedger(self.root/'ledger.sqlite3',clock=lambda:self.now[0])
        ref = self.store.put_json({'kind':'test-frozen-input'})
        from be.codec import digest
        self.campaign = self.ledger.campaign('adversarial',digest('frozen-test',{'scope':'runtime-only'}),
                                            ref,resume=True,wall_seconds=120)
        self.job = self.ledger.ensure_job(self.campaign['campaign_id'],digest('job-test',{'role':'producer'}),'produce')

    def test_stale_lease_cannot_complete_or_checkpoint_after_replacement(self):
        first = self.ledger.claim(self.job,'run:first',lease_seconds=1)
        self.now[0] += 2
        second = self.ledger.claim(self.job,'run:second',lease_seconds=30)
        ref = self.store.put_json({'kind':'candidate-bytes-only'})
        for operation in [lambda:self.ledger.complete(first,ref,operation_key='late-complete'),
                          lambda:self.ledger.checkpoint(first,1,ref),
                          lambda:self.ledger.renew(first)]:
            with self.assertRaises(ProtocolError):
                operation()
        response = self.ledger.complete(second,ref,operation_key='current-complete')
        self.assertEqual(response['attempt_id'],second['attempt_id'])
        self.assertEqual(self.ledger.get_job(self.job)['output_ref'],ref)

    def test_duplicate_completion_is_idempotent_but_new_bytes_conflict(self):
        fence = self.ledger.claim(self.job,'run:one')
        ref = self.store.put_json({'kind':'first'})
        one = self.ledger.complete(fence,ref,operation_key='once')
        two = self.ledger.complete(fence,ref,operation_key='once')
        self.assertEqual(one,two)
        altered = self.store.put_json({'kind':'different'})
        with self.assertRaises(ProtocolError):
            self.ledger.complete(fence,altered,operation_key='once')

    def test_simultaneous_claims_have_one_authoritative_winner(self):
        def attempt(label):
            try:
                return self.ledger.claim(self.job,label)
            except ProtocolError as exc:
                return exc.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(attempt,['run:a','run:b']))
        self.assertEqual(sum(isinstance(v,dict) for v in outcomes),1)
        self.assertIn('job_busy',outcomes)

    def test_immutable_campaign_deadline_cannot_be_reset_by_resume(self):
        ref = self.store.put_json({'kind':'test-frozen-input'})
        self.now[0] += 10
        resumed = self.ledger.campaign('adversarial',self.campaign['frozen_digest'],ref,
                                       resume=True,wall_seconds=120)
        self.assertEqual(resumed['deadline'],self.campaign['deadline'])
        self.now[0] = self.campaign['deadline']
        with self.assertRaises(ProtocolError):
            self.ledger.claim(self.job,'run:too-late')

    def test_other_project_locator_cannot_silently_create_campaign(self):
        ref = self.store.put_json({'kind':'test-frozen-input'})
        with self.assertRaises(ProtocolError):
            self.ledger.campaign('renamed-or-legacy-locator',self.campaign['frozen_digest'],ref,
                                 resume=True,wall_seconds=120)
        self.now[0] += 1
        explicit = self.ledger.campaign('renamed-or-legacy-locator',self.campaign['frozen_digest'],ref,
                                       resume=False,fresh=True,wall_seconds=120)
        self.assertNotEqual(explicit['campaign_id'],self.campaign['campaign_id'])

    def test_tampered_cas_object_is_not_verified_by_its_filename(self):
        ref = self.store.put_json({'kind':'original'})
        target = self.store.objects / ref['bytes_digest'][7:9] / ref['bytes_digest'][7:]
        target.write_bytes(b'{}')
        with self.assertRaises(ProtocolError):
            self.store.read_json(ref)


class CLIAdversarialTests(unittest.TestCase):
    def setUp(self):
        temporary_root = ROOT / '.test_tmp'
        temporary_root.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix='be-cli-adversarial-',dir=temporary_root)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def invoke(self, project, state, *, extra=(), environment=None):
        env = dict(os.environ)
        env['PYTHONPATH'] = str(ROOT/'src')
        if environment:
            env.update(environment)
        result = subprocess.run([sys.executable,'-m','be','run',str(project),'--resume',
                                 '--state-dir',str(state),*extra],
                                cwd=ROOT,env=env,capture_output=True,timeout=45)
        try:
            report = json.loads(result.stdout)
        except Exception as exc:
            self.fail('CLI did not emit one structured report: '+repr(result.stdout[:500])+repr(result.stderr[:500]))
        self.assertFalse(report['full_proof_pass'])
        self.assertFalse(report['paid_activation'])
        return result,report

    def test_real_cli_proves_only_pilot_and_resume_is_auditable(self):
        project = ROOT/'examples/local-pilot/project.toml'
        state = self.root/'state'
        one,r1 = self.invoke(project,state)
        self.assertEqual(one.returncode,0,one.stdout.decode(errors='replace'))
        self.assertEqual(r1['status'],'PILOT_PASS')
        self.assertFalse(r1['producer_cache_hit'])
        self.assertFalse(r1['verifier_cache_hit'])
        two,r2 = self.invoke(project,state)
        self.assertEqual(two.returncode,0,two.stdout.decode(errors='replace'))
        self.assertEqual(r2['status'],'PILOT_PASS')
        self.assertTrue(r2['producer_cache_hit'])
        self.assertTrue(r2['verifier_cache_hit'])
        self.assertTrue(r2['authorized_readback'])
        self.assertEqual(r1['campaign_id'],r2['campaign_id'])
        self.assertEqual(r1['frozen_digest'],r2['frozen_digest'])
        self.assertEqual(r1['attempts_total'],r2['attempts_total'])
        self.assertNotEqual(r1['run_id'],r2['run_id'])

    def test_real_cli_negative_scopes_never_print_pass(self):
        for folder in ['feasible','wide-rho']:
            with self.subTest(folder=folder):
                result,report=self.invoke(ROOT/'examples/local-pilot'/folder/'project.toml',self.root/folder)
                self.assertEqual(result.returncode,2,result.stdout.decode(errors='replace'))
                self.assertEqual(report['status'],'PILOT_NO_PASS')
                self.assertEqual(report['outcome'],'no_contradiction')

    def test_corrupt_cached_receipt_fails_closed(self):
        project = ROOT/'examples/local-pilot/project.toml'; state=self.root/'state'
        first,report=self.invoke(project,state)
        self.assertEqual(first.returncode,0,first.stdout.decode(errors='replace'))
        digest=report['receipt_ref']['bytes_digest'][7:]
        path=state/'artifacts/objects/sha256'/digest[:2]/digest
        path.write_bytes(b'{}')
        again,error=self.invoke(project,state)
        self.assertNotEqual(again.returncode,0)
        self.assertEqual(error['status'],'PILOT_NO_PASS')

    def test_actual_source_copy_drift_blocks_cached_acceptance(self):
        from be.codec import load_json
        source_root = self.root/'source-copy'
        manifest_path = ROOT/'examples/local-pilot/source-manifest.json'
        manifest = load_json(manifest_path)
        for entry in manifest['source_files']:
            destination = source_root/entry['path']
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/entry['path'],destination)
        def quoted(path):
            return json.dumps(Path(path).as_posix())
        project = self.root/'drift.toml'
        project.write_text('schema_version = "be.local-pilot/1"\n'
                           'kind = "empty-joint-cubics-zero-noise"\n'
                           'problem = '+quoted(ROOT/'examples/local-pilot/problem.json')+'\n'
                           'source_manifest = '+quoted(manifest_path)+'\n'
                           'trust_profile = '+quoted(ROOT/'examples/local-pilot/trust-profile.json')+'\n'
                           'source_root = '+quoted(source_root)+'\n',encoding='utf-8')
        first,report = self.invoke(project,self.root/'drift-state')
        self.assertEqual(first.returncode,0,first.stdout.decode(errors='replace'))
        changed = source_root/manifest['source_files'][0]['path']
        changed.write_bytes(changed.read_bytes()+b'\n')
        second,error = self.invoke(project,self.root/'drift-state')
        self.assertNotEqual(second.returncode,0)
        self.assertEqual(error['status'],'PILOT_NO_PASS')
        self.assertEqual(error['error']['code'],'source_digest_mismatch')

    def test_full_proof_kind_and_optimized_runtime_are_rejected(self):
        project=self.root/'unsupported.toml'
        project.write_text('schema_version = "be.local-pilot/1"\nkind = "full-proof"\n',encoding='utf-8')
        bad,report=self.invoke(project,self.root/'unsupported')
        self.assertEqual(bad.returncode,3)
        self.assertEqual(report['status'],'PILOT_NO_PASS')
        optimized,report=self.invoke(ROOT/'examples/local-pilot/project.toml',self.root/'optimized',
                                     environment={'PYTHONOPTIMIZE':'1'})
        self.assertEqual(optimized.returncode,3)
        self.assertEqual(report['status'],'PILOT_NO_PASS')


if __name__ == '__main__':
    unittest.main()
