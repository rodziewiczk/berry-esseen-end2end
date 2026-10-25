"""Replay the eleven recovered B5 forests as one subsection of delivery66.

There is deliberately no discovery fallback. Mathematical code runs only as a
supervised original acceptor in an exclusive new capsule. Old receipts are not
inputs; cache reuse requires the full relocated evidence reader. This module
never acquires mixed theorems, parent resources, the n25 union, or full66.
"""
from __future__ import annotations
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys
import time
import traceback
import uuid
import zipfile

from . import count_task as common, n25_recovery_sources as sources
from . import n25_recovered_counts_evidence as evidence, n25_full_transport as transport
from .colab_batch import atomic_json, bundle, event, utc
from .retained_n25_extra import _cache_members, LogBackups

MIB = 1024**2
CPU = WALL = 82800
MEMORY = 2048*MIB
need = common.need


def prepare(task, target, *, archive=sources.DEFAULT_ARCHIVE):
    sources.profile(target, ordinary=True)
    return sources.prepare(target, task, archive=archive)


def check_task(task, target):
    sources.profile(target, ordinary=True)
    return sources.verify_preparation(target, task)


def accept(task, target, *, cpu_seconds=CPU, wall_seconds=WALL, on_epoch=None):
    target = sources.normalize(target)
    check_task(task, target)
    need(type(cpu_seconds) is int and 2 <= cpu_seconds <= CPU
         and type(wall_seconds) is int and 1 <= wall_seconds <= WALL,
         'Explicit at-most23-hour unchanged full native action')
    task = Path(task).resolve()
    run = task/('accept-'+uuid.uuid4().hex[:12])
    capsule = run/'capsule'
    # check_task forbids a receipt in the source. copytree never overwrites.
    shutil.copytree(task/'capsule', capsule)
    sources.verify(target, capsule)
    census = sources.geometry(target, capsule)
    spec = sources.profile(target, ordinary=True)
    receipt = capsule/f"COUNT{spec['index']}_ACCEPTED.json"
    need(not receipt.exists(), 'Fresh acceptance only: no historical receipt input')
    if on_epoch:
        on_epoch(run)
    observed = common.supervise(
        [sys.executable, '-B', '-S', str(capsule/'count_protocol.py'), 'accept'],
        cwd=capsule, output_dir=run/'execution', mode='trusted_native',
        cpu_seconds=cpu_seconds, wall_seconds=wall_seconds, memory_bytes=MEMORY,
        disk_bytes=256*MIB, log_bytes=16*MIB, checkpoint_paths=[])
    report = dict(schema=evidence.SCHEMA, target=target, epoch=str(run), scope=evidence.SCOPE,
                  observed=observed, census=census, implementation=evidence.implementation(),
                  arithmetic_accepted=False, parent_acquisitions_verified=False, full66_complete=False)
    atomic_json(run/'NATIVE_OBSERVED.json', report)
    evidence.validate_run(task, target, run, observed, census)
    report.update(arithmetic_accepted=True, native_receipt=str(receipt),
                  native_receipt_sha256=common.digest(receipt), negative_controls=24,
                  conditional_premises=evidence.premises(target))
    atomic_json(run/'NATIVE_ACCEPTED.json', report)
    return run, evidence.validate_stage(task, target, run)


def _sidecar(path):
    marker = transport.ordinary(path.with_suffix('.zip.sha256'), limit=1024)
    need(marker.read_text('ascii') == common.digest(path)+'  '+path.name+'\n',
         'Complete original-stage ZIP and SHA256 sidecar')


def save_stage(task, target, epoch, directory):
    evidence.validate_stage(task, target, epoch)
    directory = Path(directory)
    sources.base._no_link_ancestors(directory)
    directory.mkdir(parents=True, exist_ok=True)
    output = directory/(Path(epoch).name+'-native.zip')
    need(not output.exists(), 'Append-only complete original-replay export')
    temporary = output.with_name(output.name+'.pending-'+uuid.uuid4().hex[:8])
    with zipfile.ZipFile(temporary, 'x', compression=zipfile.ZIP_DEFLATED, strict_timestamps=False) as z:
        for path in sorted(Path(epoch).rglob('*')):
            sources.base._no_link_ancestors(path)
            if path.is_file():
                transport.ordinary(path, limit=128*MIB)
                z.write(path, path.relative_to(task).as_posix())
        _cache_members(z)
    need(temporary.stat().st_size <= 512*MIB, 'Bounded complete original stage')
    pin = common.digest(temporary)
    temporary.replace(output)
    marker = output.with_suffix('.zip.sha256')
    with marker.open('x', encoding='ascii') as stream:
        stream.write(pin+'  '+output.name+'\n')
    return output


def restore_stage(task, target, directory, *, log_root=None):
    task, directory = Path(task).resolve(), Path(directory)
    if not directory.exists():
        return None
    transport.ordinary(directory, directory=True)
    for path in sorted(directory.glob('accept-*-native.zip')):
        try:
            transport.ordinary(path, limit=512*MIB)
            _sidecar(path)
            with zipfile.ZipFile(path) as z:
                name, rows = _cache_members(z)
                restored = task/name
                # Repeated invocation may see its previously restored valid epoch.
                if restored.exists():
                    result = evidence.validate_stage(task, target, restored)
                    return restored, result
                restored.mkdir()
                for row in rows:
                    output = task/Path(*row.filename.split('/'))
                    output.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(row) as src, output.open('xb') as dst:
                        shutil.copyfileobj(src, dst, MIB)
            result = evidence.validate_stage(task, target, restored)
            if log_root:
                event(log_root, 'recovered_original_cache_revalidated', target=target, cache=str(path))
            return restored, result
        except Exception as error:
            if log_root:
                event(log_root, 'recovered_original_cache_rejected', target=target, cache=str(path),
                      error=type(error).__name__+': '+str(error))
    return None


def run_target(task, target, durable, *, deadline, log_root=None, on_epoch=None):
    target = sources.normalize(target)
    check_task(task, target)
    # Deliberately disjoint from PREFIX2/reconstructed epochs and notebooks01--07.
    cache = Path(durable)/'n25-recovered-original'/sources.PLAN_SHA256/target/'completed'
    completed = restore_stage(task, target, cache, log_root=log_root)
    if completed:
        return dict(state='complete_conditional_arithmetic', result=completed[1],
                    native_rerun=False, full66_complete=False)
    # A previous attempt may have accepted locally but failed while copying to Drive.
    for epoch in sorted(Path(task).glob('accept-*')):
        if not (epoch/'NATIVE_ACCEPTED.json').is_file():
            continue
        try:
            checked = evidence.validate_stage(task, target, epoch)
        except Exception as error:
            if log_root:
                event(log_root, 'local_original_stage_rejected', target=target, error=str(error))
            continue
        saved = save_stage(task, target, epoch, cache)
        return dict(state='complete_conditional_arithmetic', result=checked, native_rerun=False,
                    cache=str(saved), full66_complete=False)
    remaining = int(deadline-time.monotonic())
    if remaining < 2:
        return dict(state='incomplete_native_replay_pending', arithmetic_accepted=False, full66_complete=False)
    epoch, result = accept(task, target, cpu_seconds=min(CPU, remaining),
                           wall_seconds=min(WALL, remaining), on_epoch=on_epoch)
    saved = save_stage(task, target, epoch, cache)
    return dict(state='complete_conditional_arithmetic', result=result, native_rerun=True,
                cache=str(saved), full66_complete=False)


def run_section(*, durable_root, archive=sources.DEFAULT_ARCHIVE,
                work_root='/content/berry-esseen-runs', total_seconds=82800,
                selected_targets=None, backup_interval=60):
    """Runnable ordinary subsection, explicitly NOT a replacement for full66.

    On a handled interruption an incomplete bundle is exported. Complete stages
    are independently saved as soon as validated; they survive later failures.
    """
    need(type(total_seconds) is int and 2 <= total_seconds <= WALL, 'Bounded full section wall budget')
    need(type(backup_interval) is int and 1 <= backup_interval <= 3600, 'Positive backup interval')
    targets = tuple(sources.normalize(t) for t in (selected_targets or sources.targets()))
    need(targets and len(set(targets)) == len(targets), 'Nonempty distinct original target selection')
    for target in targets:
        sources.profile(target, ordinary=True)
    from .environment import snapshot
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root = Path(work_root).absolute()/'n25-recovered-original'/stamp
    sources.base._no_link_ancestors(root)
    root.mkdir(parents=True, exist_ok=False)
    durable = Path(durable_root)/'n25-recovered-original'/'runs'/stamp
    deadline = time.monotonic()+total_seconds
    status = dict(schema='N25_RECOVERED_ORDINARY_SUBSECTION_V1', state='started',
                  selected_targets=list(targets), completed_targets=[], stages=[],
                  discovery_run=False, native_arithmetic_accepted=False,
                  parent_acquisitions_verified=False, mixed_exclusion_verified=False,
                  full66_complete=False, all_index_conclusion_verified=False)
    atomic_json(root/'ENVIRONMENT.json', snapshot())
    atomic_json(root/'SESSION_RESULT.json', status)
    monitor = LogBackups(root, durable, backup_interval)
    monitor.start()
    try:
        with sources.RecoveryArchive(archive) as asset:
            for target in targets:
                task = root/'tasks'/target
                event(root, 'original_count_prepare', target=target, discovery=False,
                      historical_acceptance_used=False)
                sources._prepare(asset, target, task)
                result = run_target(task, target, durable_root, deadline=deadline,
                                    log_root=root, on_epoch=monitor.set_active)
                monitor.set_active(None)
                status['stages'].append(dict(target=target, **result))
                if result['state'] != 'complete_conditional_arithmetic':
                    status['state'] = 'incomplete_budget'
                    break
                status['completed_targets'].append(target)
                atomic_json(root/'SESSION_RESULT.json', status)
                monitor.save()
            else:
                status.update(state='selected_recovered_ordinary_arithmetic_accepted',
                              native_arithmetic_accepted=True)
    except BaseException as error:
        status.update(state='incomplete_error', error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(), encoding='utf-8')
        event(root, 'recovered_original_incomplete', error=status['error'])
    finally:
        status['finished_utc'] = utc()
        atomic_json(root/'SESSION_RESULT.json', status)
        try:
            monitor.close()
        except Exception as error:
            event(root, 'final_backup_failed', error=str(error))
        output = bundle(root, durable)
    return dict(status=status, bundle=str(output), work=str(root))
