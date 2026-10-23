"""Transport adapter for byte-identical original PREFIX2 discovery helpers.

This module installs discovery-only in-memory accelerators. It never writes a
kernel, emits a prefix observation as a leaf, or invokes a native acceptor.
All completed candidates still need separate ordinary full native replay.
"""
from __future__ import annotations

from fractions import Fraction as F
import importlib
import importlib.util
from pathlib import Path
import sys

import prefix2_strategy as metadata


def load_helpers():
    """Load only sealed discovery helpers; importing them calls no kernel."""
    metadata.source_binding()
    folder = metadata.HERE/'prefix2_original'
    names = ('feasible_a0', 'split_policy', 'physical_prefix_lookahead',
             'parent_prefix_bypass', 'discovery_hoist_alpha_stoploss2',
             'integer_exponential_discovery_v1', 'geometry_memo_discovery_v12',
             'common_bound_memo_discovery_v12')
    result = {}
    for name in names:
        path = folder/(name+'.py')
        previous = sys.modules.get(name)
        if previous is not None:
            metadata.need(Path(getattr(previous, '__file__', '')).resolve() == path.resolve(),
                          'No discovery helper module collision: '+name)
            result[name] = previous
            continue
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            spec.loader.exec_module(module)
        except BaseException:
            sys.modules.pop(name, None)
            raise
        result[name] = module
    return result


def admit_capsule(c, cfg, bound, capsule, design_sha256):
    """Source/shape admission, without calling any numerical function."""
    capsule = Path(capsule).resolve()
    metadata.need(design_sha256 in metadata.ADMITTED_DESIGNS,
                  'One of the seven reviewed resource-extended PREFIX2 designs')
    metadata.need(type(cfg.get('n')) is int and cfg['n'] == 25 and c.LIMIT == 100000
                  and Path(c.HERE).resolve() == capsule, 'Literal resource-extended n25 capsule')
    metadata.need(type(bound) is dict, 'Full original kernel source map')
    for name, pin in metadata.KERNEL_PINS.items():
        metadata.need(bound.get(name) == pin and metadata.digest(capsule/name) == pin,
                      'Original accelerator-compatible kernel: '+name)


class Runtime:
    def __init__(self, helpers, geometry, common, exponential, installation):
        self.helpers = helpers
        self.geometry = geometry
        self.common = common
        self.exponential = exponential
        self.installation = installation
        self.counters = dict(parent_prefix_captures=0, physical_prefix_probes=0,
                             physical_empty_observations=0, bypass_splits=0,
                             full_evaluations=0)
        self.last_step = {}
        lookahead = helpers['physical_prefix_lookahead']
        self.original_probe = lookahead.probe
        def counted_probe(*args, **kwargs):
            self.counters['physical_prefix_probes'] += 1
            result = self.original_probe(*args, **kwargs)
            if result['physical_empty']:
                self.counters['physical_empty_observations'] += 1
            return result
        lookahead.probe = counted_probe

    def cache_statistics(self):
        groups = dict(geometry=self.geometry, common=self.common,
                      exponential={name: getattr(self.exponential, name)
                                   for name in ('exp_lower', 'exp_upper')})
        return {group: {name: dict(function.cache_info()._asdict())
                        for name, function in functions.items()}
                for group, functions in groups.items()}

    def diagnostics(self):
        return dict(discovery_strategy=metadata.STRATEGY,
                    **self.counters, cache_statistics=self.cache_statistics(),
                    **self.last_step)

    def advance(self, c, cfg, item, nodes):
        """Original bypass-first PREFIX2 step, adapted to canonical pending nodes."""
        k, path, node, box = item
        choice = None
        self.last_step = {}
        if len(path) < 128 and nodes+2 <= c.LIMIT:
            self.counters['parent_prefix_captures'] += 1
            choice = self.helpers['parent_prefix_bypass'].propose_bypass(c, cfg, k, box)
        if choice is None:
            self.counters['full_evaluations'] += 1
            decision, result = c.evaluate(cfg, k, box)
            if decision is not None:
                node.clear()
                node.update(kind='leaf', box=c.enc(box), decision=decision, result=result)
                self.last_step = dict(policy='full_native_evaluation', bypass=False)
                return 'leaf', decision
            metadata.need(len(path) < 128 and nodes+2 <= c.LIMIT,
                          'Original split depth/node budget exhausted')
            choice = self.helpers['physical_prefix_lookahead'].choose(c, cfg, k, box, result)
        else:
            self.counters['bypass_splits'] += 1
        axis, cut = choice['axis'], choice['cut']
        metadata.need(type(axis) is int and 0 <= axis < 5 and type(cut) is F,
                      'PREFIX2 strict rational split proposal')
        c.children(box, axis, cut)  # Full raw-box cover, never a contraction.
        node.clear()
        node.update(kind='split', axis=axis, cut=str(cut),
                    left={'kind': 'pending'}, right={'kind': 'pending'})
        self.last_step = dict(policy=choice['policy'],
                              lookahead=choice.get('lookahead'),
                              bypass=choice['policy'] == 'both_a0_children_physically_empty_parent_bypass',
                              split_axis=axis, split_cut=str(cut))
        return 'split', None


def install(c, cfg, bound, capsule, design_sha256):
    """Install every original V12 accelerator or fail closed; no fallback mode."""
    metadata.need(__debug__ and not sys.flags.optimize, 'Non-optimized discovery interpreter')
    admit_capsule(c, cfg, bound, capsule, design_sha256)
    helpers = load_helpers()
    for name, pin in metadata.KERNEL_PINS.items():
        module = importlib.import_module(name[:-3])
        metadata.need(Path(module.__file__).resolve() == Path(capsule).resolve()/name
                      and metadata.digest(module.__file__) == pin,
                      'Loaded original accelerator module: '+name)
    hoisted = helpers['discovery_hoist_alpha_stoploss2'].install()
    metadata.need(set(hoisted) == {'own_cdf', 'own_phase_upper'}, 'Both original hoisted functions installed')
    exponential = helpers['integer_exponential_discovery_v1']
    _, _, aliases = exponential.install()
    metadata.need(all(('exact_count_core_v5', name) in aliases for name in ('exp_lower', 'exp_upper')),
                  'Both exact integer exponential replacements installed')
    geometry = helpers['geometry_memo_discovery_v12'].install()
    metadata.need(set(geometry) == {'sharp_lower', 'box_sharp_lower'}, 'Both original geometry caches installed')
    common = helpers['common_bound_memo_discovery_v12'].install()
    metadata.need(len(common) == 6, 'All six original common-bound caches installed')
    installation = dict(discovery_strategy=metadata.STRATEGY,
                        accelerators=['loop_invariant_stoploss_hoist', 'exact_integer_exponential',
                                      'geometry_memoization', 'common_bound_memoization'],
                        exponential_aliases=len(aliases),
                        source_sha256=metadata.source_binding(),
                        arithmetic_accepted=False)
    return Runtime(helpers, geometry, common, exponential, installation)
