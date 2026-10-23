"""Infrastructure tests with fake count APIs; no numerical kernel is imported."""
from __future__ import annotations

from collections import namedtuple
from contextlib import contextmanager
from copy import deepcopy
from fractions import Fraction as F
import io
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

VENDOR = Path(__file__).resolve().parents[1]/'vendor'/'count_75a9470'
TEMP_ROOT = Path(__file__).resolve().parents[1]/'work'
TEMP_ROOT.mkdir(exist_ok=True)


def load(name):
    # These three adapters contain only stdlib imports. The original numerical
    # capsule is never imported by this fixture suite.
    with patch.object(sys, 'path', [str(VENDOR)]+sys.path):
        spec = importlib.util.spec_from_file_location(name, VENDOR/(name+'.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


metadata = load('prefix2_strategy')
with patch.dict(sys.modules, prefix2_strategy=metadata):
    runtime = load('prefix2_runtime')
worker = load('count_discovery')


def enc(value):
    if type(value) is F:
        return str(value)
    if type(value) in (list, tuple):
        return [enc(x) for x in value]
    if type(value) is dict:
        return {k: enc(v) for k, v in value.items()}
    return value


class FakeAPI:
    LIMIT = 100000
    EMPTY = {'EMPTY_TEST'}

    def __init__(self, decision=None):
        self.decision = decision
        self.calls = 0

    def evaluate(self, cfg, k, box):
        self.calls += 1
        return self.decision, {'status': 'UNRESOLVED' if self.decision is None else self.decision}

    def enc(self, value):
        return enc(value)

    @staticmethod
    def same(a, b):
        return type(a) is type(b) and a == b

    @staticmethod
    def children(box, axis, cut):
        if type(axis) is not int or not 0 <= axis < 5 or type(cut) is not F \
                or not box[axis][0] < cut < box[axis][1]:
            raise ValueError('strict interior rational split')
        a, b = deepcopy(box), deepcopy(box)
        a[axis][1], b[axis][0] = cut, cut
        return a, b

    @staticmethod
    def rootbox(cfg):
        return deepcopy(cfg['box'])


def box():
    return [[F(1, 4), F(1, 3)], [F(1, 100), F(1, 10)], [F(0), F(1)],
            [F(-1, 2), F(1, 2)], [F(0), F(1)]]


CacheInfo = namedtuple('CacheInfo', 'hits misses maxsize currsize')


def cached_function():
    return SimpleNamespace(cache_info=lambda: CacheInfo(3, 2, 20, 2))


def fake_runtime(bypass=None, choice=None):
    helpers = {
        'parent_prefix_bypass': SimpleNamespace(propose_bypass=lambda *args: bypass),
        'physical_prefix_lookahead': SimpleNamespace(
            choose=lambda *args: choice, probe=lambda *args: {'physical_empty': False}),
    }
    exp = SimpleNamespace(exp_lower=cached_function(), exp_upper=cached_function())
    return runtime.Runtime(helpers, {'geometry': cached_function()},
                           {'common': cached_function()}, exp, {})


class MetadataTests(unittest.TestCase):
    def test_metadata_is_complete_and_calls_no_kernel(self):
        before = set(sys.modules)
        binding = metadata.strategy_binding()
        self.assertEqual(set(binding), {'discovery_strategy', 'discovery_sources_sha256',
                                       'search_sha256', 'alpha_priority', 'traversal'})
        self.assertEqual(binding['discovery_strategy'], 'RESTORED_PREFIX2_V1')
        self.assertEqual((binding['alpha_priority'], binding['traversal']), ('16', 'depth'))
        self.assertEqual(len(binding['discovery_sources_sha256']), 11)
        self.assertNotIn('exact35_core', set(sys.modules)-before)
        self.assertEqual(len(metadata.ADMITTED_DESIGNS), 7)

    def test_every_original_helper_is_byte_identical(self):
        manifest = json.loads((VENDOR/'prefix2_original'/'MANIFEST.json').read_text())
        for name, pin in metadata.ORIGINAL_PINS.items():
            self.assertEqual(metadata.digest(VENDOR/'prefix2_original'/name), pin)
            self.assertEqual(manifest['files'][name]['sha256'], pin)

    def test_extra_helper_directory_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            shutil.copytree(VENDOR/'prefix2_original', root/'prefix2_original')
            (root/'prefix2_original'/'extra').mkdir()
            with patch.object(metadata, 'HERE', root), self.assertRaises(ValueError):
                metadata.source_binding()

    def test_changed_original_helper_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            shutil.copytree(VENDOR/'prefix2_original', root/'prefix2_original')
            (root/'prefix2_original'/'feasible_a0.py').write_text('changed')
            with patch.object(metadata, 'HERE', root), self.assertRaises(ValueError):
                metadata.source_binding()

    def test_resume_requires_all_five_strategy_fields_and_native_identity(self):
        current = dict(design_sha256='a'*64, native_header={'n': 25},
                       **metadata.strategy_binding())
        original = deepcopy(current)
        metadata.validate_resume_binding(original, current)
        for field in current:
            changed = deepcopy(current)
            changed.pop(field)
            with self.subTest(field=field), self.assertRaises(ValueError):
                metadata.validate_resume_binding(changed, current)
        self.assertEqual(original, current)

    def test_legacy_checkpoint_needs_explicit_migration(self):
        current = dict(design_sha256='a'*64, native_header={'n': 25},
                       **metadata.strategy_binding())
        legacy = dict(design_sha256=current['design_sha256'], native_header=current['native_header'],
                      search_sha256='b'*64, alpha_priority='4', traversal='root-first')
        with self.assertRaises(ValueError):
            metadata.validate_resume_binding(legacy, current)


class PolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.helpers = runtime.load_helpers()  # Definitions/constants only.

    def test_original_factor16_can_choose_a_different_axis_than_legacy4(self):
        b = [[F(1, 4), F(251, 1000)], [F(1), F(1)], [F(0), F(1, 50)],
             [F(0), F(0)], [F(0), F(0)]]
        cfg = {'Lambda': '1'}
        self.assertEqual(worker.split_axis(cfg, b, F(4)), 0)
        self.assertEqual(self.helpers['split_policy'].original(cfg, b)['axis'], 2)

    def test_original_feasible_cut_is_strict_and_can_be_nonmidpoint(self):
        b = [[F(1, 4), F(1, 4)], [F(1, 100), F(1, 100)], [F(0), F(1)],
             [F(0), F(0)], [F(0), F(1)]]
        cfg = {'Lambda': '1', 'n': 25}
        choice = self.helpers['split_policy'].choose(cfg, b, {'outward0': '1', 'a0upper': '1/10'})
        self.assertEqual(choice['axis'], 4)
        self.assertEqual(choice['cut'], F(1, 20))
        self.assertNotEqual(choice['cut'], sum(b[4])/2)
        left, right = FakeAPI.children(b, choice['axis'], choice['cut'])
        self.assertEqual((left[4][0], left[4][1], right[4][0], right[4][1]),
                         (F(0), F(1, 20), F(1, 20), F(1)))

    def test_lookahead_prefers_only_strictly_more_empty_children(self):
        look = self.helpers['physical_prefix_lookahead']
        cfg = {'Lambda': '1', 'n': 25}
        b = box()
        original = {'axis': 0, 'cut': sum(b[0])/2, 'policy': 'original'}
        result = {'outward0': '1', 'a0upper': '1/10'}
        probes = []
        def probe(api, cfg, k, child):
            probes.append(deepcopy(child))
            return {'physical_empty': child[4] != b[4]}
        with patch.object(look, 'current_choose', return_value=original), patch.object(look, 'probe', probe):
            chosen = look.choose(FakeAPI(), cfg, 2, b, result)
        self.assertEqual(chosen['axis'], 4)
        self.assertEqual(len(probes), 4)
        with patch.object(look, 'current_choose', return_value=original), \
             patch.object(look, 'probe', return_value={'physical_empty': True}):
            self.assertEqual(look.choose(FakeAPI(), cfg, 2, b, result)['axis'], 0)


class AdvanceTests(unittest.TestCase):
    def test_bypass_stores_two_pending_children_and_never_emits_a_leaf(self):
        c = FakeAPI('PASS_TARGET')
        b, node = box(), {'kind': 'pending'}
        choice = dict(axis=4, cut=F(1, 20),
                      policy='both_a0_children_physically_empty_parent_bypass')
        engine = fake_runtime(bypass=choice)
        self.assertEqual(engine.advance(c, {}, (4, 'LR', node, b), 28), ('split', None))
        self.assertEqual(c.calls, 0)
        self.assertEqual(node['left'], {'kind': 'pending'})
        self.assertEqual(node['right'], {'kind': 'pending'})
        self.assertNotIn('result', node)
        self.assertEqual(engine.diagnostics()['bypass_splits'], 1)

    def test_unresolved_full_evaluation_uses_original_nonmidpoint_choice(self):
        c, node, b = FakeAPI(), {'kind': 'pending'}, box()
        engine = fake_runtime(choice=dict(axis=4, cut=F(1, 20), policy='feasible_a0'))
        self.assertEqual(engine.advance(c, {}, (1, '', node, b), 26), ('split', None))
        self.assertEqual(c.calls, 1)
        self.assertEqual(node['cut'], '1/20')
        self.assertEqual(engine.diagnostics()['policy'], 'feasible_a0')

    def test_only_full_evaluation_can_emit_leaf(self):
        c, node, b = FakeAPI('EMPTY_TEST'), {'kind': 'pending'}, box()
        engine = fake_runtime()
        self.assertEqual(engine.advance(c, {}, (0, '', node, b), 26), ('leaf', 'EMPTY_TEST'))
        self.assertEqual(node, dict(kind='leaf', box=enc(b), decision='EMPTY_TEST',
                                    result={'status': 'EMPTY_TEST'}))
        self.assertEqual(engine.diagnostics()['full_evaluations'], 1)

    def test_at_node_limit_full_evaluation_still_may_close(self):
        c, node = FakeAPI('EMPTY_TEST'), {'kind': 'pending'}
        engine = fake_runtime(bypass={'invalid': 'must not be used'})
        self.assertEqual(engine.advance(c, {}, (0, '', node, box()), c.LIMIT)[0], 'leaf')
        self.assertEqual(engine.counters['parent_prefix_captures'], 0)

    def test_unresolved_limit_keeps_pending_topology(self):
        c, node = FakeAPI(), {'kind': 'pending'}
        with self.assertRaises(ValueError):
            fake_runtime().advance(c, {}, (0, '', node, box()), c.LIMIT)
        self.assertEqual(node, {'kind': 'pending'})

    def test_old_leaf_and_split_objects_are_preserved_when_frontier_advances(self):
        c, b = FakeAPI('EMPTY_TEST'), box()
        left, right = c.children(b, 0, sum(b[0])/2)
        old_leaf = dict(kind='leaf', box=enc(left), decision='OLD_UNTRUSTED', result={'old': True})
        frozen = deepcopy(old_leaf)
        root = dict(kind='split', axis=0, cut=str(sum(b[0])/2), left=old_leaf, right={'kind': 'pending'})
        roots = [dict(k=0, tree=root)]
        cfg = {'n': 0, 'box': b}
        # The production census requires positive n; use two literal roots.
        cfg['n'] = 1
        roots.append(dict(k=1, tree={'kind': 'pending'}))
        pending, nodes, leaves = worker.census(c, cfg, roots)
        self.assertEqual((nodes, leaves, len(pending)), (4, 1, 2))
        fake_runtime().advance(c, cfg, pending[0], nodes)
        self.assertIs(root['left'], old_leaf)
        self.assertEqual(old_leaf, frozen)
        self.assertEqual((root['axis'], root['cut']), (0, str(sum(b[0])/2)))

    def test_diagnostics_include_bypass_and_all_cache_groups(self):
        data = fake_runtime().diagnostics()
        self.assertEqual(set(data['cache_statistics']), {'geometry', 'common', 'exponential'})
        self.assertEqual(data['cache_statistics']['geometry']['geometry']['hits'], 3)


class PrefixHookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.helpers = runtime.load_helpers()

    @contextmanager
    def fake_core(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            path = Path(temporary)/'exact35_core.py'
            path.write_text('# fake test API, no numerical kernel\n')
            core = SimpleNamespace(__file__=str(path), _cell35_engine=lambda *a: a[-1]())
            pin = metadata.KERNEL_PINS['exact35_core.py']
            look = self.helpers['physical_prefix_lookahead']
            bypass = self.helpers['parent_prefix_bypass']
            with patch.dict(sys.modules, exact35_core=core), \
                 patch.object(look, 'sha256', return_value=SimpleNamespace(hexdigest=lambda: pin)), \
                 patch.object(bypass, 'sha256', return_value=SimpleNamespace(hexdigest=lambda: pin)):
                yield core, look, bypass

    def test_probe_restores_engine_after_incoming_stop(self):
        with self.fake_core() as (core, look, _):
            original = core._cell35_engine
            api = SimpleNamespace(EMPTY={'EMPTY_TEST'},
                evaluate=lambda *a: core._cell35_engine(*([None]*12), lambda: ('PASS', {})))
            result = look.probe(api, {'n': 25}, 0, box())
            self.assertFalse(result['physical_empty'])
            self.assertIs(core._cell35_engine, original)
            self.assertFalse(look._active)

    def test_probe_restores_engine_after_exception_and_rejects_early_pass(self):
        with self.fake_core() as (core, look, _):
            original = core._cell35_engine
            def error(*a):
                raise RuntimeError('fake incoming failure')
            for evaluate, error_type in [(error, RuntimeError),
                                         (lambda *a: ('PASS', {'status': 'PASS'}), ValueError)]:
                api = SimpleNamespace(EMPTY={'EMPTY_TEST'}, evaluate=evaluate)
                with self.assertRaises(error_type):
                    look.probe(api, {'n': 25}, 0, box())
                self.assertIs(core._cell35_engine, original)
                self.assertFalse(look._active)

    def test_capture_uses_exact_eighteen_argument_interface_and_restores(self):
        with self.fake_core() as (core, look, bypass):
            def engine(*a):
                return a[-1](25, 3, *([F(0)]*10), F(2), F(0), F(1, 10), F(0), None, None)
            core._cell35_engine = engine
            api = SimpleNamespace(EMPTY={'EMPTY_TEST'},
                evaluate=lambda *a: core._cell35_engine(*([None]*12), lambda: None))
            result = bypass.capture(api, {'n': 25}, 3, box())
            self.assertEqual(result['exports'], {'outward0': F(2), 'a0upper': F(1, 10)})
            self.assertIs(core._cell35_engine, engine)
            self.assertFalse(look._active)


class AdmissionTests(unittest.TestCase):
    def test_cli_rejects_implicit_or_mixed_restored_parameters_before_loading_capsule(self):
        arguments = ['worker', '--capsule', 'absent', '--output', 'absent',
                     '--design-sha256', '0'*64, '--strategy', 'RESTORED_PREFIX2_V1']
        for extra in ([], ['--alpha-priority', '16'], ['--order', 'depth']):
            with self.subTest(extra=extra), patch.object(sys, 'argv', arguments+extra), \
                 self.assertRaisesRegex(ValueError, 'Explicit named discovery strategy'):
                worker.main()

    def test_unknown_design_and_wrong_kernel_pin_fail_before_import(self):
        c = SimpleNamespace(LIMIT=100000, HERE=VENDOR)
        with patch.object(runtime.importlib, 'import_module', side_effect=AssertionError('must not import')):
            with self.assertRaises(ValueError):
                runtime.admit_capsule(c, {'n': 25}, metadata.KERNEL_PINS, VENDOR, '0'*64)
            with self.assertRaises(ValueError):
                runtime.admit_capsule(c, {'n': 25}, {}, VENDOR, next(iter(metadata.ADMITTED_DESIGNS)))

    def test_all_accelerators_required_no_silent_partial_install(self):
        calls = []
        def installer(name, result):
            return SimpleNamespace(install=lambda: (calls.append(name), result)[1])
        helpers = {
            'discovery_hoist_alpha_stoploss2': installer('hoist', {'own_cdf': None, 'own_phase_upper': None}),
            'integer_exponential_discovery_v1': installer('exp', (None, None,
                [('exact_count_core_v5', 'exp_lower'), ('exact_count_core_v5', 'exp_upper')])),
            'geometry_memo_discovery_v12': installer('geometry', {'sharp_lower': None}),
        }
        with patch.object(runtime, 'admit_capsule'), patch.object(runtime, 'load_helpers', return_value=helpers), \
             patch.object(metadata, 'KERNEL_PINS', {}):
            with self.assertRaisesRegex(ValueError, 'Both original geometry caches'):
                runtime.install(None, None, None, VENDOR, None)
        self.assertEqual(calls, ['hoist', 'exp', 'geometry'])

    def test_successful_install_dispatches_all_four_original_accelerators(self):
        calls = []
        def installer(name, result):
            return SimpleNamespace(install=lambda: (calls.append(name), result)[1])
        exp = installer('exp', (None, None, [('exact_count_core_v5', 'exp_lower'),
                                             ('exact_count_core_v5', 'exp_upper')]))
        exp.exp_lower, exp.exp_upper = cached_function(), cached_function()
        helpers = {
            'discovery_hoist_alpha_stoploss2': installer('hoist', {'own_cdf': None, 'own_phase_upper': None}),
            'integer_exponential_discovery_v1': exp,
            'geometry_memo_discovery_v12': installer('geometry',
                {name: cached_function() for name in ('sharp_lower', 'box_sharp_lower')}),
            'common_bound_memo_discovery_v12': installer('common',
                {str(i): cached_function() for i in range(6)}),
            'physical_prefix_lookahead': SimpleNamespace(probe=lambda *a: {'physical_empty': False}),
        }
        with patch.object(runtime, 'admit_capsule'), patch.object(runtime, 'load_helpers', return_value=helpers), \
             patch.object(metadata, 'KERNEL_PINS', {}):
            engine = runtime.install(None, None, None, VENDOR, None)
        self.assertEqual(calls, ['hoist', 'exp', 'geometry', 'common'])
        self.assertEqual(len(engine.installation['accelerators']), 4)
        self.assertFalse(engine.installation['arithmetic_accepted'])
        self.assertEqual(len(engine.diagnostics()['cache_statistics']['common']), 6)


class WorkerTransportTests(unittest.TestCase):
    def test_restored_worker_completes_fake_api_and_resumes_without_replacing_roots(self):
        # This disposable module is a deliberately trivial fake API, not any
        # archived numerical source. The only import at worker runtime is this
        # fixture's API. Accelerator installation is mocked explicitly.
        fake_source = '''from fractions import Fraction as F
from copy import deepcopy
LIMIT=100000
def load():return {'n':25,'Lambda':'1'},{}
def header(bound):return {'schema':'FAKE_ONLY','n':25}
def rootbox(cfg):return [[F(0),F(1)] for i in range(5)]
def enc(x):
 if type(x)is F:return str(x)
 if isinstance(x,(list,tuple)):return [enc(v)for v in x]
 if isinstance(x,dict):return {k:enc(v)for k,v in x.items()}
 return x
def same(a,b):return type(a)is type(b)and a==b
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate')
  d[k]=v
 return d
def evaluate(cfg,k,box):return 'EMPTY_TEST',{'status':'EMPTY_TEST'}
def children(box,axis,cut):
 if type(axis)is not int or not 0<=axis<5 or not box[axis][0]<cut<box[axis][1]:raise ValueError('split')
 a,b=deepcopy(box),deepcopy(box);a[axis][1]=cut;b[axis][0]=cut;return a,b
'''
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            task = Path(temporary)
            capsule = task/'capsule'
            capsule.mkdir()
            checker = capsule/'count_protocol.py'
            checker.write_text(fake_source, encoding='utf-8')
            design = capsule/'FROZEN_DESIGN.json'
            design.write_text(json.dumps({'files': {'count_protocol.py': worker.digest(checker)}}))
            args = ['worker', '--capsule', str(capsule), '--design-sha256', worker.digest(design),
                    '--strategy', 'RESTORED_PREFIX2_V1', '--alpha-priority', '16', '--order', 'depth',
                    '--seconds', '1']
            output = task/'first'
            engine = fake_runtime()
            engine.installation = {'discovery_strategy': metadata.STRATEGY, 'arithmetic_accepted': False}
            fake_installer = SimpleNamespace(install=lambda *args: engine)
            with patch.object(sys, 'argv', args+['--output', str(output)]), \
                 patch.object(sys, 'path', sys.path.copy()), \
                 patch.dict(sys.modules, prefix2_strategy=metadata, prefix2_runtime=fake_installer), \
                 patch.object(sys, 'stdout', io.StringIO()) as capture:
                worker.main()
            packet = json.loads((output/'CHECKPOINT.json').read_text())
            self.assertFalse(packet['arithmetic_accepted'])
            self.assertEqual(len(packet['roots']), 26)
            self.assertTrue(all(root['tree']['kind'] == 'leaf' for root in packet['roots']))
            events = [json.loads(line) for line in capture.getvalue().splitlines()]
            self.assertEqual(events[-1]['status'], 'CANDIDATE_COMPLETE_NOT_ACCEPTED')
            self.assertEqual(events[-1]['diagnostics']['full_evaluations'], 26)
            self.assertTrue(all(event.get('arithmetic_accepted') is False for event in events))
            original_bytes = (output/'CHECKPOINT.json').read_bytes()
            resumed = task/'second'
            with patch.object(sys, 'argv', args+['--output', str(resumed), '--resume', str(output/'CHECKPOINT.json')]), \
                 patch.object(sys, 'path', sys.path.copy()), \
                 patch.dict(sys.modules, prefix2_strategy=metadata, prefix2_runtime=fake_installer), \
                 patch.object(sys, 'stdout', io.StringIO()):
                worker.main()
            self.assertEqual(json.loads((resumed/'CHECKPOINT.json').read_text())['roots'], packet['roots'])
            self.assertEqual((output/'CHECKPOINT.json').read_bytes(), original_bytes)
            self.assertTrue((resumed/'CANDIDATE_FOREST.json').is_file())


if __name__ == '__main__':
    unittest.main()
