"""Pure source metadata for the explicitly restored untrusted discovery epoch.

Importing this module never imports or calls a mathematical kernel. The outer
driver must additionally bind every returned source digest to its reviewed
vendor inventory; self-reported digests alone are not source authentication.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

STRATEGY = 'RESTORED_PREFIX2_V1'
LEGACY_STRATEGY = 'LEGACY_MIDPOINT_V1'
HERE = Path(__file__).resolve().parent
ORIGINAL_PINS = {
    'feasible_a0.py': 'bea087de1f6d18e4ddc034270b351ee81d43e76ab36a5827dc599dec16aeefbb',
    'split_policy.py': '013086ffff8d265b54a79f14a23d0aedede7e0361ed450ac0eddfcd406081fbd',
    'physical_prefix_lookahead.py': '50a4f6161eb589ecc6238804afbbd184e4bb458b9fe159f01a2ea94db07a7fa6',
    'parent_prefix_bypass.py': 'b8f71b052b6580a4863d8782f7ce1ec8186f73e0dbe36b6b5e817ebec8837e52',
    'discovery_hoist_alpha_stoploss2.py': 'cf198f062b8ac0fc98431a6e9954ef18c38f49a1a8e752af3e1504f74a71ad69',
    'integer_exponential_discovery_v1.py': '174b96fd8814402faa6ae881dfdbb3ebbc23118c7027c3f7b1148abb74f72515',
    'geometry_memo_discovery_v12.py': '380e791e558713f33f668a0d7f999923f5d7b28959ac5b581bee99d3216d4170',
    'common_bound_memo_discovery_v12.py': '2e69b968d5fa781db6c7728c1863a82b874dbc867b5e4852dcaa9187a09f128c',
}
# All seven reviewed *resource-extended* designs. The original 10,000-node
# designs remain available through the explicitly separate legacy worker mode.
ADMITTED_DESIGNS = frozenset({
    '765f7ff74e4007ba13e7aff57856d375e2c1cd0b76a6ce35b224eac67bc441d8',
    '25fd9e8675d2c6f0dc6805e0c5273d0e84c32f6d372befe0db35019d0a687197',
    '866eec6360d31f80931ddd9edfb87c4218caa23c8f06346ba8362f093b110e6a',
    'c992f1d472966409357e1a4ae3eef365462947e2400b54f5f3a9befe66cde437',
    'b1a7b8c534cd8294b56c7285d44c0facaf6465fc6bf2294881e090ab1d116b5b',
    'ba741cebd773a1b939b69729303e40a58b5fd80cbd0876310a8e5c3b5cba459d',
    '2f15572df398d0341cc174c7ab4a4e71c701890ed92718c8e40b1c4aa8447129',
})
KERNEL_PINS = {
    'exact35_core.py': 'a618867ae34841b2e3e1745e35142694142e08ca2d790b762870f50651e16d71',
    'exact_count_core_v5.py': '0ffba7a5e1a91fc3c3c770f9d3bcb073a529fade3d622bc5615567153a4255a0',
    'common_cubic_bound.py': 'f62a02b6e081b377b584a100cf704ed0966589e1de80177b4a33002af665af1c',
    'common_shifted.py': '947ef9b4b43e265fc3250d2c43b69976f11ed7229387d9e0ab51673e683e35b6',
    'general_quartic_sos_bounds.py': '716eda950209111c78960e819e20d0e86b83cb51868a9eaa583b839dbe32c4b5',
    'fixed_peak_quartic_bounds.py': '26d5ec337ef7f0cab81f7c4ced7b4c208d810e5a2670c07d25041ff797e3e88e',
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    path = Path(path)
    need(path.is_file() and not path.is_symlink(), 'Regular discovery source: '+str(path.name))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding():
    """Return path-independent pins, checking the byte-identical helper seal."""
    original = HERE/'prefix2_original'
    need(original.is_dir() and not original.is_symlink(), 'Original PREFIX2 helper directory')
    need({p.name for p in original.iterdir()} == set(ORIGINAL_PINS)|{'MANIFEST.json'},
         'No unbound original PREFIX2 helper or directory')
    manifest = json.loads((original/'MANIFEST.json').read_text(encoding='utf-8'))
    need(manifest.get('schema') == 'RESTORED_PREFIX2_ORIGINAL_HELPERS_V1'
         and manifest.get('arithmetic_accepted') is False
         and set(manifest.get('files', {})) == set(ORIGINAL_PINS), 'Original helper provenance inventory')
    for name, pin in ORIGINAL_PINS.items():
        need(digest(original/name) == pin and manifest['files'][name]['sha256'] == pin,
             'Byte-identical original PREFIX2 helper: '+name)
    names = ['prefix2_strategy.py', 'prefix2_runtime.py', 'prefix2_original/MANIFEST.json']
    names += ['prefix2_original/'+name for name in ORIGINAL_PINS]
    return {name: digest(HERE/name) for name in sorted(names)}


def strategy_binding():
    """The five fields an explicit, lossless checkpoint migration must set."""
    return dict(discovery_strategy=STRATEGY, discovery_sources_sha256=source_binding(),
                alpha_priority='16', traversal='depth',
                search_sha256=digest(HERE/'count_discovery.py'))


def validate_resume_binding(previous, current):
    """No worker-side heuristic migration; original topology is a separate input."""
    need(type(previous) is dict and type(current) is dict, 'Checkpoint binding dictionaries')
    keys = ('design_sha256', 'native_header', 'discovery_strategy',
            'discovery_sources_sha256', 'search_sha256', 'alpha_priority', 'traversal')
    need(all(key in previous and previous[key] == current[key] for key in keys),
         'Explicitly migrated unchanged PREFIX2 source/contract/strategy binding required')
