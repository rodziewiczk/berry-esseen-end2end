"""Resume seven regional candidates in explicit finite-tree resource epochs.

The original driver and sources remain untouched. Discovery remains untrusted;
only a fresh full native replay with the unchanged Linux guard accepts scoped
arithmetic. Numerical evaluation is performed only inside the supervised Colab
children, never by this evidence/source controller.
"""
from __future__ import annotations
from datetime import datetime, timezone
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from pathlib import PurePosixPath
import re
import shutil
import stat
import sys
import traceback
import uuid
import zipfile

from . import count_task as count
from . import count_limit_epoch as epoch
from .colab_batch import Backups, atomic_json, bundle, event

TARGET = 'b4-q2'
SCOPE = 'NEW_RESOURCE_LIMIT_EPOCH_CONDITIONAL_COUNT_ONLY'
TASK_SCHEMA = 'COUNT_LIMIT_RECOVERY_TASK_V1'
EXECUTION_SCHEMA = 'COUNT_LIMIT_RECOVERY_EXECUTION_V1'
MIB = 1024**2
NATIVE_MEMORY_BYTES = 2048*MIB
NATIVE_CPU_SECONDS = 43200
NATIVE_WALL_SECONDS = 43500
DISCOVERY_STRATEGY = 'RESTORED_PREFIX2_V1'
MIGRATION_TYPE = 'LOSSLESS_DISCOVERY_STRATEGY_MIGRATION_V1'
LEGACY_SEARCH_SHA256 = '3b239119082d0d5275446beb2d38878c9a7c7988c655da6e52fd34023e485eb4'
NATIVE_TARGET = '76824784444199314310731654405729617052063596250011448874609/187500000000000000000000000000000000000000000000000000000000'
DISCOVERY_FIELDS = {'discovery_strategy', 'discovery_sources_sha256', 'search_sha256',
                    'alpha_priority', 'traversal'}
MAX_CACHE_BYTES = 2*1024**3
MAX_CACHE_EXPANDED_BYTES = 16*1024**3


def implementation():
    return dict(**count.implementation(), count_recovery_sha256=count.digest(__file__),
                count_limit_epoch_sha256=count.digest(epoch.__file__))


def discovery_binding():
    """Read the reviewed stdlib-only discovery metadata, never a math kernel."""
    count.verify_vendor()
    source = count.VENDOR/'prefix2_strategy.py'
    spec = importlib.util.spec_from_file_location('_count_prefix2_strategy_metadata', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.strategy_binding()
    count.need(type(result) is dict and set(result) == DISCOVERY_FIELDS
               and result['discovery_strategy'] == DISCOVERY_STRATEGY
               and result['alpha_priority'] == '16' and result['traversal'] == 'depth'
               and result['search_sha256'] == count.digest(count.VENDOR/'count_discovery.py')
               and type(result['discovery_sources_sha256']) is dict
               and result['discovery_sources_sha256'], 'Complete reviewed PREFIX2 discovery binding')
    for name, pin in result['discovery_sources_sha256'].items():
        count.need(type(name) is str and name and '\\' not in name
                   and not PurePosixPath(name).is_absolute()
                   and all(p not in ('', '.', '..') for p in name.split('/'))
                   and count.VENDOR_PINS.get(name) == pin
                   and (count.VENDOR/name).resolve().is_relative_to(count.VENDOR.resolve())
                   and pin == count.digest(count.VENDOR/name), 'Actual externally pinned PREFIX2 helper bytes')
    return result


def _strategy(binding):
    """Recognize an explicit old or current strategy; unknown code never resumes."""
    count.need(type(binding) is dict, 'Explicit checkpoint binding')
    current = copy.deepcopy(discovery_binding())
    if all(binding.get(k) == current[k] for k in DISCOVERY_FIELDS):
        count.need(set(binding) == {'design_sha256', 'native_header'} | DISCOVERY_FIELDS,
                   'Exact restored discovery binding fields')
        return current
    legacy = dict(search_sha256=LEGACY_SEARCH_SHA256, alpha_priority='4', traversal='root-first')
    count.need(set(binding) == {'design_sha256', 'native_header'} | set(legacy)
               and all(binding.get(k) == v for k, v in legacy.items()),
               'Only the pinned legacy alpha4/root-first or exact restored PREFIX2 strategy')
    return dict(discovery_strategy='LEGACY_MIDPOINT_V1', **legacy)


def _check_native_binding(packet, capsule, target):
    count.need(type(packet) is dict and set(packet) == {'schema', 'binding', 'roots', 'arithmetic_accepted'}
               and packet['schema'] == 'UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1'
               and packet['arithmetic_accepted'] is False, 'Explicitly untrusted exact checkpoint packet')
    binding = packet['binding']
    count.need(type(binding) is dict, 'Complete checkpoint binding')
    expected = dict(count.native_header(capsule, target), target=NATIVE_TARGET)
    count.need(binding.get('design_sha256') == count.digest(Path(capsule)/'FROZEN_DESIGN.json')
               and epoch.canonical(binding.get('native_header')) == epoch.canonical(expected),
               'Exact native target, contract, checker and complete kernel identity')
    return _strategy(binding)


def migrate_discovery_checkpoint(packet, capsule, target=TARGET):
    """Explicit source-bound strategy transition; every tree/payload stays equal.

    Input must already have the reviewed100000-node native resource epoch.
    Resource migration, when needed, is a separate preceding operation.
    """
    epoch.verify(target, capsule)
    _check_native_binding(packet, capsule, target)
    epoch.checkpoint_geometry(packet, capsule, target)
    result = copy.deepcopy(packet)
    result['binding'].update(copy.deepcopy(discovery_binding()))
    restored = copy.deepcopy(result)
    restored['binding'] = copy.deepcopy(packet['binding'])
    count.need(epoch.canonical(restored) == epoch.canonical(packet)
               and epoch.canonical(result['roots']) == epoch.canonical(packet['roots']),
               'Discovery migration preserves every root, cut, leaf and result payload')
    check_extended_checkpoint(result, capsule, target, require_restored=True)
    return result


def extends_roots(before, after):
    """A descendant may replace pending nodes only; retained work is immutable."""
    if type(before) is not list or type(after) is not list or len(before) != len(after):
        return False
    pairs = []
    for a, b in zip(before, after):
        if type(a) is not dict or type(b) is not dict or a.get('k') != b.get('k'):
            return False
        pairs.append((a.get('tree'), b.get('tree')))
    while pairs:
        a, b = pairs.pop()
        if type(a) is not dict or type(b) is not dict:
            return False
        if a.get('kind') == 'pending':
            continue
        if a.get('kind') != b.get('kind'):
            return False
        if a.get('kind') == 'leaf':
            if epoch.canonical(a) != epoch.canonical(b):
                return False
        elif a.get('kind') == 'split':
            if a.get('axis') != b.get('axis') or a.get('cut') != b.get('cut'):
                return False
            pairs.extend(((a.get('left'), b.get('left')), (a.get('right'), b.get('right'))))
        else:
            return False
    return True


def _task_payload(parts, *, checkpoints=True):
    """Only source, resumable snapshots and native evidence are imported."""
    if 'task' not in parts:
        return False
    parts = parts[parts.index('task')+1:]
    if not parts:
        return False
    return (parts[0] in ('capsule', 'original-capsule')
            or (len(parts) == 1 and parts[0] in ('TASK.json', 'SOURCE_CHECKPOINT.json', 'INPUT_CHECKPOINT.json'))
            or re.fullmatch(r'accept-[0-9a-f]{12}', parts[0]) is not None
            or (checkpoints and parts[-1] in ('CHECKPOINT.json', 'CHECKPOINT.backup.json')))


def restore_cache_archive(archive, destination):
    """Safely restore byte-identical replay inputs; no receipt is trusted here."""
    archive, destination = Path(archive), Path(destination)
    count.need(archive.is_file() and not archive.is_symlink() and archive.stat().st_size <= MAX_CACHE_BYTES,
               'Bounded regular saved result ZIP')
    sidecar = archive.with_suffix('.zip.sha256')
    count.need(sidecar.is_file() and not sidecar.is_symlink() and sidecar.stat().st_size <= 1024,
               'Saved ZIP requires its actual SHA256 sidecar')
    words = sidecar.read_text('ascii').split()
    count.need(len(words) in (1, 2) and re.fullmatch('[0-9a-f]{64}', words[0])
               and (len(words) == 1 or words[1] == archive.name), 'Exact saved ZIP SHA256 sidecar')
    pin = count.digest(archive)
    count.need(pin == words[0], 'Actual saved ZIP matches its SHA256 sidecar')
    selected, names, expanded = [], set(), 0
    with zipfile.ZipFile(archive) as zipped:
        infos = zipped.infolist()
        count.need(len(infos) <= 100000, 'Bounded saved ZIP member count')
        for info in infos:
            name = info.orig_filename
            path = PurePosixPath(name.rstrip('/'))
            count.need(info.filename == name and name and '\\' not in name and ':' not in name and '\x00' not in name
                       and not path.is_absolute() and all(p not in ('', '.', '..') for p in name.rstrip('/').split('/'))
                       and path.as_posix() == name.rstrip('/') and path.as_posix().casefold() not in names
                       and not stat.S_ISLNK(info.external_attr >> 16), 'Unique contained regular saved ZIP member')
            names.add(path.as_posix().casefold())
            expanded += info.file_size
            count.need(info.file_size <= 128*MIB and expanded <= MAX_CACHE_EXPANDED_BYTES,
                       'Bounded saved ZIP expansion')
            if not info.is_dir() and _task_payload(path.parts):
                selected.append(info)
        count.need(selected and sum(i.file_size for i in selected) <= MAX_CACHE_BYTES,
                   'Bounded saved source/checkpoint/native-evidence selection')
        # A parent may never be a file, even if its spelling is otherwise safe.
        file_names = {i.filename.casefold() for i in infos if not i.is_dir()}
        count.need(all('/'.join(PurePosixPath(i.filename).parts[:j]).casefold() not in file_names
                       for i in infos for j in range(1, len(PurePosixPath(i.filename).parts))),
                   'No file/directory collision in saved ZIP')
        output = destination/pin
        marker = output/'CACHE_RESTORE.json'
        if output.exists():
            count.need(output.is_dir() and not output.is_symlink()
                       and not any(p.is_symlink() for p in output.rglob('*')), 'Ordinary contained restored cache tree')
            record = count.read(marker)
            count.need(record.get('archive_sha256') == pin and type(record.get('files_sha256')) is dict,
                       'Existing source-only saved ZIP import identity')
            expected = {i.filename for i in selected}
            expected_pins = {i.filename: hashlib.sha256(zipped.read(i)).hexdigest() for i in selected}
            actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
            count.need(actual == expected | {'CACHE_RESTORE.json'}
                       and record['files_sha256'] == expected_pins
                       and all((output/n).is_file() and not (output/n).is_symlink()
                               and count.digest(output/n) == h for n, h in record['files_sha256'].items()),
                       'Every existing restored input remains byte-identical')
            return output
        output.mkdir(parents=True, exist_ok=False)
        pins = {}
        for info in selected:
            path = output.joinpath(*PurePosixPath(info.filename).parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            raw = zipped.read(info)
            count.need(len(raw) == info.file_size, 'Complete saved ZIP input bytes')
            path.write_bytes(raw)
            pins[info.filename] = hashlib.sha256(raw).hexdigest()
        count.need(count.digest(archive) == pin, 'Stable saved ZIP throughout source-only extraction')
        atomic_json(marker, dict(schema='UNTRUSTED_COUNT_CACHE_RESTORE_V1', archive_sha256=pin,
                    files_sha256=pins, arithmetic_accepted=False, all_index_conclusion_verified=False))
    return output


def restore_saved_archives(roots, destination, progress_root):
    restored, seen = [], set()
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob('*.zip')):
            if path.resolve() in seen:
                continue
            seen.add(path.resolve())
            try:
                output = restore_cache_archive(path, destination)
                restored.append(output)
                event(progress_root, 'cache_archive_restored', archive=str(path),
                      archive_sha256=count.digest(path), restored=str(output), arithmetic_accepted=False)
            except (ValueError, OSError, KeyError, TypeError, UnicodeError, zipfile.BadZipFile) as error:
                event(progress_root, 'cache_archive_rejected', archive=str(path),
                      error=type(error).__name__+': '+str(error), arithmetic_accepted=False)
    return restored


def _validate_completed_task(task, target):
    record = count.read(Path(task)/'TASK.json', 4*MIB)
    count.need(record.get('target') == target, 'One exact completed-cache target')
    if record.get('schema') == TASK_SCHEMA:
        from .count_recovery_evidence import validate_completed
    else:
        count.need(record.get('schema') == 'COUNT_TASK_V1', 'Known original completed-cache task schema')
        from .n25_count_evidence import validate_completed
    result = validate_completed(task, expected_target=target)
    count.need(result.get('native_arithmetic_accepted') is True
               and result.get('parent_acquisitions_verified') is False
               and result.get('all_index_conclusion_verified') is False,
               'Fully revalidated scoped native arithmetic, never a global theorem')
    return result


def completed_cache(roots, target):
    """Reuse only complete independently revalidated native evidence."""
    accepted, seen = [], set()
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob('TASK.json'):
            if path.parent.name != 'task' or path.resolve() in seen or path.is_symlink():
                continue
            seen.add(path.resolve())
            try:
                report = _validate_completed_task(path.parent, target)
                accepted.append((path.stat().st_mtime_ns, str(path), report))
            except (ValueError, OSError, KeyError, TypeError, UnicodeError):
                continue
    if not accepted:
        return None
    _, path, report = max(accepted, key=lambda row: row[:2])
    return Path(path).parent, report


def copy_completed_cache(source, destination, target):
    count.need(not destination.exists(), 'Fresh private completed-cache copy')
    files = []
    for path in source.rglob('*'):
        count.need(not path.is_symlink(), 'No symlink in completed native evidence')
        if path.is_file() and _task_payload(('task', *path.relative_to(source).parts), checkpoints=False):
            count.need(path.stat().st_size <= 128*MIB, 'Bounded complete evidence input')
            files.append(path)
    count.need(sum(p.stat().st_size for p in files) <= MAX_CACHE_BYTES, 'Bounded complete evidence copy')
    destination.mkdir(parents=True, exist_ok=False)
    for path in files:
        copied = destination/path.relative_to(source)
        copied.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, copied)
        count.need(count.digest(path) == count.digest(copied), 'Byte-identical completed evidence copy')
    return _validate_completed_task(destination, target)


def _old_sources(roots, destination, target=TARGET):
    """Copy the actual externally pinned old closure, never its receipts."""
    for root in roots:
        if not root.is_dir():
            continue
        for design in root.rglob('FROZEN_DESIGN.json'):
            if not design.is_file() or design.is_symlink() or design.stat().st_size > MIB:
                continue
            if count.digest(design) != count.TARGETS[target][2]:
                continue
            try:
                files = count.verify_capsule(target, design.parent)
            except (ValueError, OSError):
                continue
            destination.mkdir(parents=True, exist_ok=False)
            for name in [*files, 'FROZEN_DESIGN.json']:
                shutil.copyfile(design.parent/name, destination/name)
            count.verify_capsule(target, destination)
            return dict(source_design_sha256=count.digest(design),
                        copied_source_files=len(files), historical_receipts_copied=False)
    raise ValueError('The original '+target+' live backup source closure is missing; keep the earlier result ZIP and Drive backups')


def checkpoint_statistics(packet):
    """Bound an untrusted topology; numerical decisions remain unchecked."""
    roots = packet.get('roots')
    count.need(type(roots) is list and len(roots) == 26, 'Exactly26 untrusted count roots')
    nodes = leaves = pending = depthmax = 0
    for k, root in enumerate(roots):
        count.need(type(root) is dict and set(root) == {'k', 'tree'}
                   and type(root['k']) is int and root['k'] == k, 'Ordered literal count roots')
        stack = [(root['tree'], 0)]
        while stack:
            node, depth = stack.pop()
            nodes += 1
            depthmax = max(depthmax, depth)
            count.need(nodes <= 100000 and depth <= 128 and type(node) is dict, 'Bounded recovery topology')
            kind = node.get('kind')
            if kind == 'pending':
                count.need(set(node) == {'kind'}, 'Pending carries no success payload')
                pending += 1
            elif kind == 'leaf':
                count.need(set(node) == {'kind', 'box', 'decision', 'result'}, 'Untrusted original leaf fields')
                leaves += 1
            else:
                count.need(kind == 'split' and set(node) == {'kind', 'axis', 'cut', 'left', 'right'}
                           and type(node['axis']) is int and 0 <= node['axis'] < 5
                           and type(node['cut']) is str, 'Complete exact split fields')
                from fractions import Fraction
                Fraction(node['cut'])
                stack.extend(((node['left'], depth+1), (node['right'], depth+1)))
    count.need(nodes == 2*(leaves+pending)-26, 'Full binary candidate topology')
    return dict(nodes=nodes, leaves=leaves, pending=pending, maximum_depth=depthmax)


def check_extended_checkpoint(packet, capsule, target=TARGET, *, require_restored=False):
    epoch.verify(target, capsule)
    if require_restored or packet.get('binding', {}).get('discovery_strategy') == DISCOVERY_STRATEGY:
        strategy = _check_native_binding(packet, capsule, target)
        count.need(not require_restored or strategy['discovery_strategy'] == DISCOVERY_STRATEGY,
                   'Explicit restored PREFIX2 checkpoint required')
        return epoch.checkpoint_geometry(packet, capsule, target)
    count.need(type(packet) is dict and packet.get('schema') == 'UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1'
               and packet.get('arithmetic_accepted') is False, 'Explicitly untrusted recovery checkpoint')
    binding = packet.get('binding', {})
    header = binding.get('native_header', {})
    expected = count.native_header(capsule, target)
    count.need(binding.get('design_sha256') == count.digest(Path(capsule)/'FROZEN_DESIGN.json')
               and binding.get('alpha_priority') == '4' and binding.get('traversal') == 'root-first'
               and type(header) is dict and set(header) == set(expected)|{'target'}
               and all(header.get(key) == value for key, value in expected.items())
               and type(header['target']) is str,
               'Exact extended checkpoint source/strategy identity')
    return checkpoint_statistics(packet)


def select_checkpoint(roots, original, capsule, target=TARGET, *, strategy='LEGACY_MIDPOINT_V1', diagnostics=None):
    """Choose one descendant lineage; incompatible saved work is never discarded."""
    count.need(strategy in ('LEGACY_MIDPOINT_V1', DISCOVERY_STRATEGY), 'Named reviewed discovery strategy')
    maximal, rejected, seen = [], [], set()
    for root in roots:
        if not root.is_dir():
            continue
        for pattern in ('CHECKPOINT.json', 'CHECKPOINT.backup.json'):
            for path in root.rglob(pattern):
                if path.resolve() in seen:
                    continue
                seen.add(path.resolve())
                if not path.is_file() or path.is_symlink() or path.stat().st_size > 128*MIB:
                    continue
                try:
                    packet = count.read(path)
                    count.need(type(packet) is dict, 'Checkpoint JSON is an object')
                    old_design = packet.get('binding', {}).get('design_sha256')
                    if old_design == count.TARGETS[target][2]:
                        if strategy == DISCOVERY_STRATEGY:
                            epoch.checkpoint_geometry(packet, original, target, node_limit=10000)
                        migrated = epoch.migrate_checkpoint(packet, original, capsule, target=target)
                    else:
                        check_extended_checkpoint(packet, capsule, target)
                        migrated = copy.deepcopy(packet)
                    if strategy == DISCOVERY_STRATEGY:
                        migrated = migrate_discovery_checkpoint(migrated, capsule, target)
                    statistics = check_extended_checkpoint(migrated, capsule, target,
                        **({'require_restored': True} if strategy == DISCOVERY_STRATEGY else {}))
                    candidate = dict(path=path, before=packet, after=migrated, statistics=statistics,
                                     time=path.stat().st_mtime_ns)
                    dominated = False
                    survivors = []
                    for saved in maximal:
                        forward = extends_roots(saved['after']['roots'], migrated['roots'])
                        backward = extends_roots(migrated['roots'], saved['after']['roots'])
                        if backward and (not forward or (saved['time'], str(saved['path'])) >=
                                         (candidate['time'], str(path))):
                            dominated = True
                            break
                        if not forward:
                            survivors.append(saved)
                    if not dominated:
                        maximal = survivors + [candidate]
                except (ValueError, KeyError, TypeError, OSError, UnicodeError, ZeroDivisionError) as error:
                    rejected.append(dict(path=str(path), error=type(error).__name__+': '+str(error)))
                    continue
    if diagnostics is not None:
        diagnostics.extend(rejected)
    count.need(maximal, 'A compatible saved '+target+' checkpoint is required; recovery never restarts fresh roots. '
               +json.dumps(rejected[:8], sort_keys=True))
    count.need(len(maximal) == 1, 'Ambiguous incompatible checkpoint lineages; no saved tree was selected or reset. '
               +json.dumps([dict(path=str(c['path']), **c['statistics']) for c in maximal], sort_keys=True))
    chosen = maximal[0]
    return chosen['path'], chosen['before'], chosen['after'], chosen['statistics']


def prepare(task, roots, target=TARGET, *, strategy='LEGACY_MIDPOINT_V1'):
    count.need(target in count.TARGETS, 'Exactly one of the seven reviewed regional targets')
    task.mkdir(parents=True, exist_ok=False)
    old = task/'original-capsule'
    provenance = _old_sources(roots, old, target)
    source_epoch = epoch.build(old, task/'capsule', target=target)
    diagnostics = []
    source, before, after, statistics = select_checkpoint(roots, old, task/'capsule', target,
                                                         strategy=strategy, diagnostics=diagnostics)
    # Retain original bytes as evidence, and separately serialize the migrated input.
    shutil.copyfile(source, task/'SOURCE_CHECKPOINT.json')
    count.need(count.read(task/'SOURCE_CHECKPOINT.json') == before, 'Stable source checkpoint during private copy')
    atomic_json(task/'INPUT_CHECKPOINT.json', after)
    migration = dict(source_checkpoint_sha256=count.digest(task/'SOURCE_CHECKPOINT.json'),
                     source_checkpoint_bytes=(task/'SOURCE_CHECKPOINT.json').stat().st_size,
                     source_design_sha256=before['binding']['design_sha256'],
                     execution_design_sha256=count.digest(task/'capsule/FROZEN_DESIGN.json'),
                     roots_sha256=hashlib.sha256(json.dumps(before['roots'], sort_keys=True,
                                                separators=(',', ':')).encode()).hexdigest(),
                     roots_preserved=before['roots'] == after['roots'],
                     arithmetic_accepted=False, statistics=statistics)
    if strategy == DISCOVERY_STRATEGY:
        before_capsule = old if before['binding']['design_sha256'] == count.TARGETS[target][2] else task/'capsule'
        before_statistics = epoch.checkpoint_geometry(before, before_capsule, target,
            node_limit=10000 if before_capsule == old else 100000)
        migration.update(migration_type=MIGRATION_TYPE, source_checkpoint_path=str(source),
                         source_strategy=_strategy(before['binding']), target_strategy=discovery_binding(),
                         source_binding_sha256=hashlib.sha256(epoch.canonical(before['binding'])).hexdigest(),
                         execution_binding_sha256=hashlib.sha256(epoch.canonical(after['binding'])).hexdigest(),
                         input_checkpoint_sha256=count.digest(task/'INPUT_CHECKPOINT.json'),
                         before_statistics=before_statistics, after_statistics=statistics,
                         rejected_checkpoints=diagnostics,
                         resource_epoch_migrated=before['binding']['design_sha256'] != after['binding']['design_sha256'])
        count.need(before_statistics == statistics, 'Migration changes no saved topology census')
    count.need(migration['roots_preserved'], 'Every saved tree and leaf payload retained as untrusted input')
    record = dict(schema=TASK_SCHEMA, target=target, scope=SCOPE, source_commit=count.COMMIT,
                  original_design_sha256=count.TARGETS[target][2],
                  design_sha256=count.digest(task/'capsule/FROZEN_DESIGN.json'),
                  original_node_limit=10000, node_limit=100000, source_epoch=source_epoch,
                  native_memory_bytes=NATIVE_MEMORY_BYTES,
                  prepared_source_files=len(epoch.verify(target, task/'capsule')),
                  source_archives={'old': count.ASSETS['old']},
                  source_provenance=provenance, migration=migration, implementation=implementation(),
                  arithmetic_accepted=False, parent_acquisitions_verified=False,
                  all_index_conclusion_verified=False)
    if count.TARGETS[target][0] == 'new-conditional-v14':
        record['source_archives']['base13'] = count.ASSETS['base13']
    atomic_json(task/'TASK.json', record)
    return record


def search(task, previous, seconds, target=TARGET, *, strategy='LEGACY_MIDPOINT_V1'):
    capsule = task/'capsule'
    epoch.verify(target, capsule)
    packet = count.read(previous)
    count.need(strategy in ('LEGACY_MIDPOINT_V1', DISCOVERY_STRATEGY), 'Named reviewed discovery strategy')
    check_extended_checkpoint(packet, capsule, target,
                              **({'require_restored': True} if strategy == DISCOVERY_STRATEGY else {}))
    run = task/('search-'+uuid.uuid4().hex[:12])
    run.mkdir()
    atomic_json(run/'resume.json', packet)
    command = [sys.executable, '-B', '-S', str(count.VENDOR/'count_discovery.py'),
               '--capsule', str(capsule), '--design-sha256', count.digest(capsule/'FROZEN_DESIGN.json'),
               '--output', str(run/'candidate'), '--seconds', str(seconds), '--resume', str(run/'resume.json'),
               '--alpha-priority', '16' if strategy == DISCOVERY_STRATEGY else '4',
               '--order', 'depth' if strategy == DISCOVERY_STRATEGY else 'root-first']
    if strategy == DISCOVERY_STRATEGY:
        command.extend(['--strategy', DISCOVERY_STRATEGY])
    observed = count.supervise(command, cwd=run, output_dir=run/'execution',
                               wall_seconds=seconds+120, cpu_seconds=seconds+120,
                               memory_bytes=NATIVE_MEMORY_BYTES, mode='untrusted_search',
                               checkpoint_paths=[run/'candidate/CHECKPOINT.json', run/'candidate/CHECKPOINT.backup.json'])
    epoch.verify(target, capsule)
    packet = count.final_packet(observed) if (observed.get('status') == 'completed'
        and type(observed.get('returncode')) is int and observed['returncode'] == 0) else None
    if packet is not None:
        count.need(packet.get('status') in ('SEARCH_CHECKPOINTED_INCOMPLETE', 'CANDIDATE_COMPLETE_NOT_ACCEPTED')
                   and packet.get('arithmetic_accepted') is False, 'Discovery never accepts arithmetic')
    report = dict(schema='COUNT_LIMIT_RECOVERY_SEARCH_V1', target=target, scope=SCOPE,
                  epoch=str(run), observed=observed, search_result=packet, arithmetic_accepted=False)
    atomic_json(run/'SEARCH_EXECUTION.json', report)
    return report


def accept(task, candidate, *, wall_seconds=NATIVE_WALL_SECONDS, cpu_seconds=NATIVE_CPU_SECONDS, target=TARGET):
    count.need(type(cpu_seconds) is int and 2 <= cpu_seconds <= NATIVE_CPU_SECONDS
               and type(wall_seconds) is int and 1 <= wall_seconds <= NATIVE_WALL_SECONDS,
               'Explicit bounded recovery native CPU/wall policy')
    source = task/'capsule'
    files = epoch.verify(target, source)
    forest = count.read(candidate)
    census = epoch.forest_census(forest, target, source)
    index = count.TARGETS[target][1]
    run = task/('accept-'+uuid.uuid4().hex[:12])
    capsule = run/'capsule'
    capsule.mkdir(parents=True)
    for name in [*files, 'FROZEN_DESIGN.json']:
        shutil.copyfile(source/name, capsule/name)
    epoch.verify(target, capsule)
    forest_path = capsule/('COUNT'+str(index)+'_FOREST.json')
    shutil.copyfile(candidate, forest_path)
    count.need(count.read(forest_path) == forest, 'Stable complete candidate copy')
    command = [sys.executable, '-B', '-S', str(capsule/'count_protocol.py'), 'accept']
    observed = count.supervise(command, cwd=capsule, output_dir=run/'execution',
                               wall_seconds=wall_seconds, cpu_seconds=cpu_seconds,
                               memory_bytes=NATIVE_MEMORY_BYTES, mode='trusted_native')
    report = dict(schema=EXECUTION_SCHEMA, target=target, scope=SCOPE, epoch=str(run),
                  observed=observed, census=census, implementation=implementation(),
                  arithmetic_accepted=False, parent_acquisitions_verified=False,
                  all_index_conclusion_verified=False)
    atomic_json(run/'NATIVE_OBSERVED.json', report)
    count.require_completed(observed)
    from .count_recovery_evidence import trusted_guard
    from . import n25_count_evidence as evidence
    count.need(type(observed.get('returncode')) is int and observed['returncode'] == 0
               and observed.get('mode') == 'trusted_native' and observed.get('proof_accepted') is False
               and trusted_guard(observed, script_sha=count.digest(capsule/'count_protocol.py'),
                                 supervisor_sha=report['implementation']['supervisor_sha256'],
                                 memory_bytes=NATIVE_MEMORY_BYTES, cpu_seconds=cpu_seconds),
               'Fresh original Linux native guard required for the new exact source epoch')
    execution = run/'execution'
    count.need(evidence.same(observed, count.read(execution/'supervisor-result.json')), 'Actual native supervisor receipt')
    launch = count.read(execution/'native-launch.json')
    controller_cpu = min(30, max(1, cpu_seconds//10))
    count.need(launch['argv'] == command and Path(launch['cwd']).resolve() == capsule.resolve()
               and Path(launch['output_dir']).resolve() == execution.resolve()
               and launch['mode'] == 'trusted_native' and launch['cpu_seconds'] == cpu_seconds
               and launch['wall_seconds'] == wall_seconds and launch['memory_bytes'] == NATIVE_MEMORY_BYTES
               and launch['worker_memory_bytes'] == NATIVE_MEMORY_BYTES-64*MIB and launch['supervisor_memory_bytes'] == 64*MIB
               and launch['worker_cpu_seconds'] == cpu_seconds-controller_cpu
               and launch['supervisor_cpu_seconds'] == controller_cpu and launch['checkpoint_paths'] == []
               and launch['disk_bytes'] == 256*MIB and launch['log_bytes'] == 16*MIB,
               'Actual native launch command, context and complete requested resource policy')
    outer = count.read(execution/'launch.json')
    outer_command = outer['argv']
    count.need(type(outer_command) is list and len(outer_command) == 6 and outer_command[:3] == command[:3]
               and Path(outer_command[3]).resolve() == Path(__file__).with_name('linux_supervisor.py').resolve()
               and outer_command[4] == '--_native-controller'
               and Path(outer_command[5]).resolve() == (execution/'native-launch.json').resolve()
               and evidence.same(outer, dict(launch, argv=outer_command)),
               'Actual exact native controller launch relation')
    evidence.guard_files(execution, observed, launch, count.digest(capsule/'count_protocol.py'))
    for key in ('stdout', 'stderr'):
        path = execution/(key+'.txt')
        count.need(Path(observed[key+'_path']).resolve() == path.resolve()
                   and path.is_file() and not path.is_symlink() and path.stat().st_size <= 16*MIB
                   and count.digest(path) == observed[key+'_sha256'], 'Actual complete native capture hash and context')
    count.need((execution/'stderr.txt').stat().st_size == 0, 'Fresh successful checker has empty stderr')
    receipt_path = capsule/('COUNT'+str(index)+'_ACCEPTED.json')
    receipt = count.read(receipt_path)
    epoch.verify(target, capsule)
    epoch.verify(target, source)
    count.verify_vendor()
    count.validate_native(receipt, target, capsule, census)
    count.need(receipt['negative_controls'] == evidence.control_labels(capsule/'count_protocol.py'), 'All24 original controls in order')
    statistics = dict(nodes=census['nodes'], leaves=census['leaves'], **evidence.full_statistics(forest))
    count.need(evidence.same(receipt['statistics'], statistics), 'Complete actual fresh native forest statistics')
    count.need(evidence.same(json.loads((execution/'stdout.txt').read_text('utf-8'), object_pairs_hook=count.unique), receipt),
               'Actual terminal JSON matches the saved fresh acceptance receipt')
    report.update(arithmetic_accepted=True, native_receipt=str(receipt_path),
                  native_receipt_sha256=count.digest(receipt_path), negative_controls=24,
                  conditional_premises=['Correct original whole-parent INITIAL/resource acquisitions',
                                        'Same-witness attainment/contact/Fourier/count framework'])
    if count.TARGETS[target][0] == 'new-conditional-v14':
        report['conditional_premises'].append('Global C24 auxiliary bound and attained positive-closed q25<=5/16')
    atomic_json(run/'NATIVE_ACCEPTED.json', report)
    return report


def run_colab(target=TARGET, *, durable_root, work_root='/content/berry-esseen-runs',
              total_seconds=43200, slice_seconds=1800, backup_interval=60):
    from .environment import snapshot
    count.need(type(target) is str and target in count.TARGETS, 'Exactly one of the seven reviewed regional targets')
    count.need(type(total_seconds) is int and total_seconds > 0 and type(slice_seconds) is int
               and 1 <= slice_seconds <= 7200, 'Positive total budget and bounded recovery slices')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root = Path(work_root)/target/stamp
    durable = Path(durable_root)/target/stamp
    roots = [Path(work_root)/target, Path(durable_root)/target]
    root.mkdir(parents=True, exist_ok=False)
    status = dict(scope=SCOPE, target=target, started_utc=datetime.now(timezone.utc).isoformat(),
                  state='started', native_arithmetic_accepted=False, parent_acquisitions_verified=False,
                  all_index_conclusion_verified=False, work=str(root), durable=str(durable), slices=[])
    atomic_json(root/'ENVIRONMENT.json', snapshot())
    atomic_json(root/'SESSION_RESULT.json', status)
    monitor = Backups(root, durable, interval=backup_interval)
    monitor.start()
    try:
        event(root, 'count_limit_recovery_prepare_started', target=target, old_node_limit=10000, node_limit=100000,
              memory_bytes=NATIVE_MEMORY_BYTES, total_search_seconds=total_seconds,
              discovery_strategy=DISCOVERY_STRATEGY, alpha_priority='16', traversal='depth')
        roots += restore_saved_archives(roots, Path(work_root)/target/'.restored-cache', root)
        cached = completed_cache(roots, target)
        if cached is not None:
            source, _ = cached
            accepted = copy_completed_cache(source, root/'task', target)
            status.update(state='regional_count_arithmetic_accepted', native_arithmetic_accepted=True,
                          native_result=accepted, completed_cache_reused=True, completed_cache_source=str(source))
            event(root, 'completed_native_cache_reused', source_task=str(source),
                  receipt_sha256=accepted.get('receipt_sha256'), no_search_or_native_rerun=True,
                  parent_acquisitions_verified=False, all_index_conclusion_verified=False)
            remaining = 0
        else:
            prepared = prepare(root/'task', roots, target, strategy=DISCOVERY_STRATEGY)
            status['resource_epoch'] = dict(design_sha256=prepared['design_sha256'], node_limit=100000,
                                          original_design_sha256=prepared['original_design_sha256'])
            status['checkpoint_migration'] = prepared['migration']
            event(root, 'untrusted_checkpoint_migrated', **prepared['migration']['statistics'],
                  source_checkpoint=prepared['migration'].get('source_checkpoint_path'),
                  source_checkpoint_sha256=prepared['migration']['source_checkpoint_sha256'],
                  before_statistics=prepared['migration'].get('before_statistics'),
                  after_statistics=prepared['migration'].get('after_statistics'),
                  source_strategy=prepared['migration'].get('source_strategy'),
                  target_strategy=prepared['migration'].get('target_strategy'),
                  rejected_checkpoints=prepared['migration'].get('rejected_checkpoints', []),
                  roots_preserved=True, roots_sha256=prepared['migration'].get('roots_sha256'),
                  arithmetic_accepted=False)
            previous = root/'task/INPUT_CHECKPOINT.json'
            remaining = total_seconds
        atomic_json(root/'SESSION_RESULT.json', status)
        while remaining > 0:
            seconds = min(60 if not status['slices'] else slice_seconds, remaining)
            event(root, 'recovery_search_started', seconds=seconds, remaining_allocated_seconds=remaining)
            report = search(root/'task', previous, seconds, target, strategy=DISCOVERY_STRATEGY)
            run = Path(report['epoch'])
            status['slices'].append(dict(epoch=str(run), allotted_seconds=seconds,
                                         search_result=report['search_result'], observed_status=report['observed']['status']))
            atomic_json(root/'SESSION_RESULT.json', status)
            options = [run/'candidate/CHECKPOINT.json', run/'candidate/CHECKPOINT.backup.json']
            if any(path.is_file() for path in options):
                selected, _, after, _ = select_checkpoint([run/'candidate'], root/'task/original-capsule',
                    root/'task/capsule', target, strategy=DISCOVERY_STRATEGY)
                count.need(extends_roots(count.read(previous)['roots'], after['roots']),
                           'A search slice must retain every previously saved split and leaf')
                previous = selected
            elif (report['observed'].get('status') == 'completed'
                  and type(report['observed'].get('returncode')) is int and report['observed']['returncode'] == 0):
                raise ValueError('Completed discovery returned no validated resumable checkpoint; no reset is permitted')
            monitor.save()
            packet = report['search_result'] or {}
            event(root, 'recovery_search_finished', status=packet.get('status', 'INCOMPLETE_NO_ACCEPTANCE'),
                  nodes=packet.get('nodes'), leaves=packet.get('leaves'), pending=packet.get('pending'))
            successful = (report['observed'].get('status') == 'completed'
                          and type(report['observed'].get('returncode')) is int
                          and report['observed']['returncode'] == 0)
            if packet.get('status') == 'CANDIDATE_COMPLETE_NOT_ACCEPTED' and successful:
                event(root, 'new_epoch_native_replay_started', all_26_roots=True, node_limit=100000)
                accepted = accept(root/'task', run/'candidate/CANDIDATE_FOREST.json', target=target)
                count.need(accepted['arithmetic_accepted'] is True, 'Complete independent native acceptance')
                status.update(state='regional_count_arithmetic_accepted', native_arithmetic_accepted=True,
                              native_result=accepted)
                event(root, 'regional_count_arithmetic_accepted', scope=SCOPE,
                      parent_acquisitions_verified=False, all_index_conclusion_verified=False)
                break
            if not successful:
                status['state'] = 'incomplete_guarded_stop'
                event(root, 'guarded_child_failure', **count.execution_diagnostics(report['observed']))
                break
            remaining -= seconds
        else:
            if cached is None:
                status['state'] = 'candidate_incomplete_budget_exhausted'
    except BaseException as error:
        status.update(state='incomplete_error', error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(), encoding='utf-8')
        event(root, 'incomplete_error', error=status['error'])
    finally:
        status['finished_utc'] = datetime.now(timezone.utc).isoformat()
        atomic_json(root/'SESSION_RESULT.json', status)
        try:
            monitor.close()
        except Exception as error:
            event(root, 'final_backup_failed', error=str(error))
        output = bundle(root, durable)
        event(root, 'results_bundle_saved', path=str(output), state=status['state'], all_index_conclusion_verified=False)
    print('\nRESULT:', status['state'], '\nZIP:', output, flush=True)
    return dict(status=status, bundle=str(output), work=str(root))
