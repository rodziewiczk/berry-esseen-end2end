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
import json
from pathlib import Path
import shutil
import sys
import traceback
import uuid

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


def implementation():
    return dict(**count.implementation(), count_recovery_sha256=count.digest(__file__),
                count_limit_epoch_sha256=count.digest(epoch.__file__))


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


def check_extended_checkpoint(packet, capsule, target=TARGET):
    epoch.verify(target, capsule)
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


def select_checkpoint(roots, original, capsule, target=TARGET):
    """Keep the most advanced compatible saved candidate, without accepting it."""
    chosen = None
    for root in roots:
        if not root.is_dir():
            continue
        for pattern in ('CHECKPOINT.json', 'CHECKPOINT.backup.json'):
            for path in root.rglob(pattern):
                if not path.is_file() or path.is_symlink() or path.stat().st_size > 128*MIB:
                    continue
                try:
                    packet = count.read(path)
                    old_design = packet.get('binding', {}).get('design_sha256')
                    if old_design == count.TARGETS[target][2]:
                        migrated = epoch.migrate_checkpoint(packet, original, capsule, target=target)
                    else:
                        check_extended_checkpoint(packet, capsule, target)
                        migrated = copy.deepcopy(packet)
                    statistics = check_extended_checkpoint(migrated, capsule, target)
                    candidate = (statistics['leaves'], statistics['nodes'], path.stat().st_mtime_ns,
                                 str(path), packet, migrated, statistics)
                    if chosen is None or candidate[:4] > chosen[:4]:
                        chosen = candidate
                except (ValueError, KeyError, TypeError, OSError, UnicodeError):
                    continue
    count.need(chosen is not None, 'A compatible saved '+target+' checkpoint is required; recovery never restarts fresh roots')
    return Path(chosen[3]), chosen[4], chosen[5], chosen[6]


def prepare(task, roots, target=TARGET):
    count.need(target in count.TARGETS, 'Exactly one of the seven reviewed regional targets')
    task.mkdir(parents=True, exist_ok=False)
    old = task/'original-capsule'
    provenance = _old_sources(roots, old, target)
    source_epoch = epoch.build(old, task/'capsule', target=target)
    source, before, after, statistics = select_checkpoint(roots, old, task/'capsule', target)
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


def search(task, previous, seconds, target=TARGET):
    capsule = task/'capsule'
    epoch.verify(target, capsule)
    packet = count.read(previous)
    check_extended_checkpoint(packet, capsule, target)
    run = task/('search-'+uuid.uuid4().hex[:12])
    run.mkdir()
    atomic_json(run/'resume.json', packet)
    command = [sys.executable, '-B', '-S', str(count.VENDOR/'count_discovery.py'),
               '--capsule', str(capsule), '--design-sha256', count.digest(capsule/'FROZEN_DESIGN.json'),
               '--output', str(run/'candidate'), '--seconds', str(seconds), '--resume', str(run/'resume.json'),
               '--alpha-priority', '4', '--order', 'root-first']
    observed = count.supervise(command, cwd=run, output_dir=run/'execution',
                               wall_seconds=seconds+120, cpu_seconds=seconds+120,
                               memory_bytes=NATIVE_MEMORY_BYTES, mode='untrusted_search',
                               checkpoint_paths=[run/'candidate/CHECKPOINT.json', run/'candidate/CHECKPOINT.backup.json'])
    epoch.verify(target, capsule)
    packet = count.final_packet(observed) if observed.get('status') == 'completed' and observed.get('returncode') == 0 else None
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
              memory_bytes=NATIVE_MEMORY_BYTES, total_search_seconds=total_seconds)
        prepared = prepare(root/'task', roots, target)
        status['resource_epoch'] = dict(design_sha256=prepared['design_sha256'], node_limit=100000,
                                      original_design_sha256=prepared['original_design_sha256'])
        event(root, 'untrusted_checkpoint_migrated', **prepared['migration']['statistics'],
              source_checkpoint_sha256=prepared['migration']['source_checkpoint_sha256'],
              roots_preserved=True, arithmetic_accepted=False)
        previous = root/'task/INPUT_CHECKPOINT.json'
        remaining = total_seconds
        while remaining > 0:
            seconds = min(60 if not status['slices'] else slice_seconds, remaining)
            event(root, 'recovery_search_started', seconds=seconds, remaining_allocated_seconds=remaining)
            report = search(root/'task', previous, seconds, target)
            run = Path(report['epoch'])
            status['slices'].append(dict(epoch=str(run), allotted_seconds=seconds,
                                         search_result=report['search_result'], observed_status=report['observed']['status']))
            atomic_json(root/'SESSION_RESULT.json', status)
            options = [run/'candidate/CHECKPOINT.json', run/'candidate/CHECKPOINT.backup.json']
            valid = []
            for path in options:
                if path.is_file():
                    try:
                        check_extended_checkpoint(count.read(path), root/'task/capsule', target)
                        valid.append(path)
                    except (ValueError, OSError, UnicodeError):
                        pass
            if valid:
                previous = max(valid, key=lambda path: path.stat().st_mtime_ns)
            monitor.save()
            packet = report['search_result'] or {}
            event(root, 'recovery_search_finished', status=packet.get('status', 'INCOMPLETE_NO_ACCEPTANCE'),
                  nodes=packet.get('nodes'), leaves=packet.get('leaves'), pending=packet.get('pending'))
            if packet.get('status') == 'CANDIDATE_COMPLETE_NOT_ACCEPTED':
                event(root, 'new_epoch_native_replay_started', all_26_roots=True, node_limit=100000)
                accepted = accept(root/'task', run/'candidate/CANDIDATE_FOREST.json', target=target)
                count.need(accepted['arithmetic_accepted'] is True, 'Complete independent native acceptance')
                status.update(state='regional_count_arithmetic_accepted', native_arithmetic_accepted=True,
                              native_result=accepted)
                event(root, 'regional_count_arithmetic_accepted', scope=SCOPE,
                      parent_acquisitions_verified=False, all_index_conclusion_verified=False)
                break
            if report['observed'].get('status') != 'completed' or report['observed'].get('returncode') != 0:
                status['state'] = 'incomplete_guarded_stop'
                event(root, 'guarded_child_failure', **count.execution_diagnostics(report['observed']))
                break
            remaining -= seconds
        else:
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
