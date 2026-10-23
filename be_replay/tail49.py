"""Run the unchanged original cutoff49 selected FULL suite on Colab/Linux.

The original Docker/cgroup adapter is not portable to an undelegated Colab
runtime. BASIC mode instead observes actual arithmetic under the explicitly
weaker process-group supervisor. It never claims native or global acceptance.
All14 top-level jobs and all41 retained components remain mandatory; no quick
mode, old capture, or source patch can substitute for the full invocation.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import runpy
import shutil
import stat
import sys
import threading
import time
import traceback
import urllib.request
import uuid
import zipfile

MIB = 1024**2
DEFAULT_MEMORY_BYTES = 2048*MIB
MAX_MEMORY_BYTES = 16384*MIB
DEFAULT_CPU_SECONDS = 64800
DEFAULT_WALL_SECONDS = 64800
RESOURCE_PROFILE = 'BASIC_FULL_SUITE_EXPLICIT_BUDGETS_V4'
ARCHIVE_NAME = 'BE_cutoff49_20260930.zip'
ARCHIVE_BYTES = 16660566
ARCHIVE_SHA = 'ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e'
ARCHIVE_URL = ('https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/download/'
               'cutoff49-sources-2026-10-22/'+ARCHIVE_NAME)
PREFIX = 'BE_cutoff49_20260930/'
MANIFEST_SHA = '58a770705c6e0bc500813ed37299753a16f6245ebea6ade238ad98078d7b4e26'
VERIFY_SHA = '766e9cee5d1cb8b173fd2db264cddbd227439e4e87fbcf3daec243ec2c9a1375'
NEW_JOBS_SHA = 'edb42eef2e7e4110533173cc384ecb94167bf5c312fea8f371916fbdd6f013d6'
RETAINED_JOBS_SHA = 'd92f0017fadc5c2f9601de599f2e1f97eb9c1042b02a17a695065c040f09d7ad'
FILE_COUNT = 1401
EXPANDED_BYTES = 33252205
RUNNER = 'baseline/certificates/work/below50_20260929/release_tools/run_certificates_v2.py'
TOP_NAMES = ['composition49', 'support46', 'independent_support46', 'independent_selectors',
             'phase_product_controls', 'new_phase_controls', 'later_phase_domains',
             'independent_phase_scope', 'corrected_legacy_acquisition', 'corrected_barrier46',
             'finite_base', 'entry_schedule_mapping', 'local_formula_mapping', 'retained_components']


def need(condition, message):
    if not condition:
        raise ValueError(message)


def validate_budgets(*, wall_seconds, cpu_seconds, memory_bytes):
    """Reject invalid budgets before source access or filesystem mutation.

    BASIC CPU means per-process RLIMIT_CPU and sampled live process-group
    observations, not cumulative accounting of the complete sequential suite.
    """
    need(type(cpu_seconds) is int and 0 < cpu_seconds <= DEFAULT_CPU_SECONDS,
         'Positive integer BASIC CPU budget at most64800 seconds')
    need(type(wall_seconds) in (int, float) and 0 < wall_seconds <= DEFAULT_WALL_SECONDS
         and math.isfinite(wall_seconds),
         'Finite positive BASIC wall budget at most64800 seconds')
    need(type(memory_bytes) is int and 512*MIB <= memory_bytes <= MAX_MEMORY_BYTES,
         'Explicit BASIC full-suite memory budget between512 and16384MiB')


def sha(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(MIB), b''):
            value.update(block)
    return value.hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'Duplicate JSON field: '+key)
        result[key] = value
    return result


def load(path):
    path = Path(path)
    need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 64*MIB,
         'Bounded ordinary JSON input')
    return json.loads(path.read_text('utf-8'), object_pairs_hook=unique)


def safe(name):
    need(type(name) is str and name and not any(c in name for c in ('\\', ':', '\x00')),
         'Portable literal relative path')
    parts = name.split('/')
    need(all(p not in ('', '.', '..') for p in parts), 'No absolute or parent path')
    return parts


def manifest(raw):
    need(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA, 'Exact original BE49 manifest bytes')
    data = json.loads(raw, object_pairs_hook=unique)
    need(set(data) == {'schema', 'files'} and data['schema'] == 'BE49_ARCHIVE_V1',
         'Original complete manifest schema')
    pins = data['files']
    need(type(pins) is dict and len(pins) == FILE_COUNT-1, 'All1400 manifested original inputs')
    for name, digest in pins.items():
        safe(name)
        need(type(digest) is str and len(digest) == 64 and set(digest) <= set('0123456789abcdef'),
             'Literal SHA256 binding')
    need(pins['verify.py'] == VERIFY_SHA and pins['new_jobs.json'] == NEW_JOBS_SHA and
         pins['retained_jobs.json'] == RETAINED_JOBS_SHA, 'Original driver and complete job lists')
    return pins


def verify_sources(root):
    root = Path(root).resolve()
    need((root/'MANIFEST.json').is_file() and not (root/'MANIFEST.json').is_symlink(),
         'Ordinary original manifest file')
    pins = manifest((root/'MANIFEST.json').read_bytes())
    for name, digest in pins.items():
        path = root.joinpath(*safe(name))
        need(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(root) and
             sha(path) == digest, 'Unchanged original source: '+name)
    return pins


def obtain_archive(directory, *, download=False, progress=None):
    directory = Path(directory).absolute()
    need(not directory.is_symlink(), 'Ordinary source-cache directory')
    directory.mkdir(parents=True, exist_ok=True)
    path = directory/ARCHIVE_NAME
    if not path.exists():
        need(download, 'Missing pinned source archive; enable download')
        pending = directory/(ARCHIVE_NAME+'.download-'+uuid.uuid4().hex)
        request = urllib.request.Request(ARCHIVE_URL, headers={'User-Agent': 'berry-esseen-end2end/1'})
        used = 0
        with urllib.request.urlopen(request, timeout=60) as response, pending.open('xb') as target:
            for block in iter(lambda: response.read(MIB), b''):
                used += len(block)
                need(used <= ARCHIVE_BYTES, 'Source download within the exact pinned size')
                target.write(block)
                if progress:
                    progress('tail49_source_download', bytes=used, expected_bytes=ARCHIVE_BYTES)
        need(pending.stat().st_size == ARCHIVE_BYTES and sha(pending) == ARCHIVE_SHA,
             'Complete pinned downloaded archive')
        need(not path.exists(), 'Do not overwrite a concurrent source download')
        pending.rename(path)
    need(path.is_file() and not path.is_symlink() and path.stat().st_size == ARCHIVE_BYTES and
         sha(path) == ARCHIVE_SHA, 'Exact original archive size and SHA256')
    return path.resolve()


def prepare(archive, root):
    archive, root = Path(archive), Path(root).absolute()
    need(archive.is_file() and not archive.is_symlink() and archive.stat().st_size == ARCHIVE_BYTES and
         sha(archive) == ARCHIVE_SHA, 'Pinned archive before extraction')
    need(not root.exists() and not root.is_symlink(), 'Fresh exclusive source directory')
    with zipfile.ZipFile(archive) as capsule:
        entries = capsule.infolist()
        need(len(entries) == len({entry.filename for entry in entries}), 'Unique ZIP member names')
        files = [entry for entry in entries if not entry.is_dir()]
        need(len(files) == FILE_COUNT and sum(e.file_size for e in files) == EXPANDED_BYTES,
             'Exact1401-file complete expanded capsule')
        for entry in entries:
            need(entry.filename.startswith(PREFIX), 'One original archive root')
            relative = entry.filename[len(PREFIX):].rstrip('/')
            if relative:
                safe(relative)
            need(not stat.S_ISLNK(entry.external_attr >> 16), 'No archive symlinks')
        raw = capsule.read(PREFIX+'MANIFEST.json')
        pins = manifest(raw)
        need({e.filename[len(PREFIX):] for e in files} == set(pins)|{'MANIFEST.json'},
             'No omitted or unmanifested archive files')
        root.mkdir(parents=True)
        for entry in files:
            relative = entry.filename[len(PREFIX):]
            path = root.joinpath(*safe(relative))
            path.parent.mkdir(parents=True, exist_ok=True)
            with capsule.open(entry) as source, path.open('xb') as target:
                shutil.copyfileobj(source, target, MIB)
    verify_sources(root)
    return root.resolve()


def source_jobs(root):
    root = Path(root)
    need(sha(root/'new_jobs.json') == NEW_JOBS_SHA and sha(root/'retained_jobs.json') == RETAINED_JOBS_SHA,
         'Exact complete original job-list bytes')
    new, retained = load(root/'new_jobs.json'), load(root/'retained_jobs.json')
    need(len(new) == 10 and [j['name'] for j in new] == TOP_NAMES[:10] and
         len(retained) == 41 and len({j['name'] for j in retained}) == 41,
         'All10 new jobs and41 retained jobs; no quick reduction')
    return new, retained


def successful(row, directory, name):
    need(type(row['returncode']) is int and row['returncode'] == 0, 'Actual successful native exit: '+name)
    for kind in ('stdout', 'stderr'):
        path = Path(directory)/(name+'.'+kind+'.txt')
        need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 16*MIB and
             sha(path) == row[kind+'_sha256'], 'Actual complete captured bytes: '+name)
    need((Path(directory)/(name+'.stderr.txt')).stat().st_size == 0, 'Empty successful native stderr: '+name)


def wrapper_captures(execution):
    """Bind both outer captures before using any original-driver marker."""
    paths = {}
    for kind in ('stdout', 'stderr'):
        path = Path(execution[kind+'_path'])
        need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 16*MIB and
             sha(path) == execution[kind+'_sha256'], 'Actual bounded wrapper '+kind+' capture matches supervisor SHA')
        paths[kind] = path
    need(paths['stderr'].stat().st_size == 0, 'Empty successful wrapper stderr')
    text = paths['stdout'].read_text('utf-8')
    need(sha(paths['stdout']) == execution['stdout_sha256'], 'Wrapper stdout stable while parsing')
    return text


def validate_full_result(root, output, new, retained):
    root, output = Path(root), Path(output)
    result = load(output/'result.json')
    need(result['status'] == 'PASS_BE49_SELECTED_ARITHMETIC' and result['quick'] is False and
         result['sources_unchanged'] is True and result['manifest_sha256'] == MANIFEST_SHA and
         result['manifested_files'] == 1400 and result['executable'] == sys.executable,
         'Fresh complete original FULL output, never quick or preparation')
    rows = result['jobs']
    need([row['name'] for row in rows] == TOP_NAMES, 'All14 top-level executions in exact order')
    commands = [[sys.executable, '-B', *job['argv']] for job in new]
    commands += [[sys.executable, '-B', script] for script in
                 ('accept_finite_base.py', 'validate_schedule.py', 'check_consolidation.py')]
    commands.append([sys.executable, '-B', str(root/RUNNER), '--workspace-root',
                     str(root/'baseline/certificates'), '--job-file', str(root/'retained_jobs.json'),
                     '--output', str(output/'components')])
    for row, command in zip(rows, commands):
        need(row['command'] == command, 'Exact original top-level invocation')
        successful(row, output, row['name'])
    child = load(output/'components/metadata.json')
    need(child['schema'] == 'BE_FIXED_CERTIFICATE_SUITE_V2' and child['status'] == 'PASS' and
         child['selected_jobs'] == 41 and child['optimized'] is False and
         child['sources_unchanged'] is True and child['input_sha256'] == child['input_sha256_after'],
         'Complete retained replay and unchanged source snapshot')
    need([j['name'] for j in child['jobs']] == [j['name'] for j in retained],
         'Every one of41 retained jobs in original order')
    for row, expected in zip(child['jobs'], retained):
        need(all(row[key] == expected[key] for key in ('name', 'cwd', 'argv', 'source_run')) and
             row['command'] == [sys.executable, '-B', *expected['argv']],
             'Exact original retained invocation and provenance')
        successful(row, output/'components', row['name'])
    return {'top_level_executions': len(rows), 'retained_component_executions': len(child['jobs']),
            'quick_mode_used': False, 'result_sha256': sha(output/'result.json'),
            'retained_metadata_sha256': sha(output/'components/metadata.json')}


class Progress:
    """Observe original stage receipts without treating live snapshots as acceptance."""
    def __init__(self, directory, native_output, wrapper_stdout, interval=20):
        self.directory, self.native_output, self.stdout = map(Path, (directory, native_output, wrapper_stdout))
        self.interval, self.stop = interval, threading.Event()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.follow, daemon=True)

    def emit(self, name, **fields):
        row = {'event': name, 'utc': datetime.now(timezone.utc).isoformat(), **fields,
               'native_arithmetic_accepted': False, 'all_index_conclusion_verified': False}
        with self.lock:
            with (self.directory/'progress.jsonl').open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(row, sort_keys=True)+'\n')
                stream.flush()
                os.fsync(stream.fileno())
            print(json.dumps(row, sort_keys=True), flush=True)

    def follow(self):
        position, partial, last = 0, b'', 0.0
        started = time.monotonic()
        while True:
            try:
                with self.stdout.open('rb') as stream:
                    stream.seek(position)
                    block = stream.read(MIB)
                position += len(block)
                lines = (partial+block).split(b'\n')
                partial = lines.pop()
                for line in lines:
                    self.emit('tail49_original_stdout', line=line.decode('utf-8', errors='replace')[:4096])
            except FileNotFoundError:
                pass
            if time.monotonic()-last >= self.interval:
                counts = {}
                for label, path in (('top_level', self.native_output/'result.json'),
                                     ('retained', self.native_output/'components/metadata.json')):
                    try:
                        packet = load(path)
                        counts[label+'_recorded_executions'] = len(packet.get('jobs', []))
                    except (OSError, ValueError):
                        counts[label+'_recorded_executions'] = None
                self.emit('tail49_heartbeat', elapsed_seconds=time.monotonic()-started,
                          required_top_level=14, required_retained=41, **counts)
                last = time.monotonic()
            if self.stop.wait(.2):
                if getattr(self, 'draining', False):
                    break
                self.draining = True

    def start(self):
        self.thread.start()

    def close(self):
        self.stop.set()
        self.thread.join(timeout=5)
        need(not self.thread.is_alive(), 'Tail49 progress follower stopped')


def worker(config_path):
    config = load(config_path)
    source, output, prefix, temporary = map(Path, (config['source'], config['output'],
                                                 config['pycache_prefix'], config['tmp']))
    need(not output.exists() and not prefix.exists(), 'Fresh original output and absent bytecode prefix')
    verify_sources(source)
    sys.dont_write_bytecode = True
    sys.pycache_prefix = str(prefix)
    os.environ.update(PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1', PYTHONPYCACHEPREFIX=str(prefix),
                      TMPDIR=str(temporary), TMP=str(temporary), TEMP=str(temporary))
    script = source/'verify.py'
    sys.argv = [str(script), '--output', str(output)]
    os.chdir(source)
    runpy.run_path(str(script), run_name='__main__')


def run(output, *, archives, download=False, mode='basic', wall_seconds=DEFAULT_WALL_SECONDS,
        cpu_seconds=DEFAULT_CPU_SECONDS, heartbeat_seconds=20, memory_bytes=DEFAULT_MEMORY_BYTES):
    from . import linux_supervisor
    from .colab_batch import atomic_json
    need(mode == 'basic', 'The full subprocess suite requires its original Docker/cgroup contract for trusted acceptance; no native-mode fallback')
    validate_budgets(wall_seconds=wall_seconds, cpu_seconds=cpu_seconds, memory_bytes=memory_bytes)
    need(sys.platform == 'linux', 'Actual Linux/POSIX paths required by the original phase-scope audit')
    output = Path(output).absolute()
    need(not output.exists() and not output.is_symlink(), 'Fresh exclusive full-suite epoch')
    output.mkdir(parents=True)
    output = output.resolve()
    progress = Progress(output, output/'native-full', output/'supervision/stdout.txt', heartbeat_seconds)
    result = {'status': 'INCOMPLETE_NO_ACCEPTANCE', 'all_required_jobs_computed': False,
              'native_arithmetic_accepted': False, 'all_analytic_and_literature_inputs_verified': False,
              'all_index_conclusion_verified': False, 'scope': 'ORIGINAL_SELECTED_FULL_ARITHMETIC_BASIC_GUARD',
              'basic_memory_bytes': memory_bytes,
              'basic_cpu_seconds': cpu_seconds, 'basic_wall_seconds': wall_seconds,
              'execution_resource_profile': RESOURCE_PROFILE}
    started = time.monotonic()
    progress.start()
    try:
        archive = obtain_archive(archives, download=download, progress=progress.emit)
        source = prepare(archive, output/'original-BE49')
        new, retained = source_jobs(source)
        temporary = output/'tmp'
        temporary.mkdir()
        prefix = output/'never-created-native-pycache'
        adapter = output/'tail49_worker.py'
        shutil.copyfile(__file__, adapter)
        adapter_sha = sha(adapter)
        config = output/'worker-config.json'
        atomic_json(config, {'source': str(source), 'output': str(output/'native-full'),
                             'pycache_prefix': str(prefix), 'tmp': str(temporary)})
        result.update(source_archive_sha256=ARCHIVE_SHA, original_manifest_sha256=MANIFEST_SHA,
                      original_driver_sha256=VERIFY_SHA, complete_original_source_files=FILE_COUNT,
                      invocation_adapter_sha256=adapter_sha, python=sys.version,
                      supervisor_sha256=sha(linux_supervisor.__file__),
                      original_driver_semantic_argv=[str(source/'verify.py'), '--output', str(output/'native-full')])
        progress.emit('tail49_full_suite_started', top_level_executions=14, retained_components=41,
                      quick_mode=False, guard='BASIC_UNTRUSTED_PROCESS_GROUP',
                      memory_bytes=memory_bytes, cpu_seconds=cpu_seconds, wall_seconds=wall_seconds)
        execution = linux_supervisor.run([sys.executable, '-B', '-S', str(adapter), '--_worker', str(config)],
                    cwd=output, output_dir=output/'supervision', wall_seconds=wall_seconds,
                    cpu_seconds=cpu_seconds, memory_bytes=memory_bytes, mode='untrusted_search',
                    disk_bytes=256*MIB, log_bytes=16*MIB, heartbeat_seconds=heartbeat_seconds)
        result['execution'] = execution
        result.update(execution_status=execution.get('status'), execution_reason=execution.get('reason'))
        need(execution.get('status') == 'completed' and type(execution.get('returncode')) is int and
             execution['returncode'] == 0, 'Observed successful original FULL subprocess')
        text = wrapper_captures(execution)
        need([line[6:] for line in text.splitlines() if line.startswith('START ')] == TOP_NAMES and
             [line[5:] for line in text.splitlines() if line.startswith('PASS ')] == TOP_NAMES and
             text.splitlines().count('PASS_BE49_SELECTED_ARITHMETIC') == 1,
             'Actual full14-job stdout protocol, not a copied historical marker')
        summary = validate_full_result(source, output/'native-full', new, retained)
        verify_sources(source)
        need(sha(adapter) == adapter_sha and sha(archive) == ARCHIVE_SHA and
             not prefix.exists() and not prefix.is_symlink(), 'Unchanged sources/adapter and no old bytecode')
        result.update(summary, status='COMPUTED_ORIGINAL_BE49_FULL_SUITE_UNTRUSTED_GUARD',
                      all_required_jobs_computed=True)
    except Exception as error:
        result['error'] = type(error).__name__+': '+str(error)
        (output/'ERROR.txt').write_text(traceback.format_exc(), encoding='utf-8')
    finally:
        try:
            progress.close()
        except Exception as error:
            # A failed observer must not suppress the preserved result/error
            # files or turn a handled timeout into an unexported result.
            result.update(status='INCOMPLETE_NO_ACCEPTANCE', all_required_jobs_computed=False,
                          progress_error=type(error).__name__+': '+str(error))
            with (output/'ERROR.txt').open('a', encoding='utf-8') as stream:
                stream.write('\nProgress observer shutdown failed:\n'+traceback.format_exc())
        result['elapsed_seconds'] = time.monotonic()-started
        atomic_json(output/'TAIL49_RESULT.json', result)
        progress.emit('tail49_finished', status=result['status'],
                      all_required_jobs_computed=result['all_required_jobs_computed'],
                      memory_bytes=memory_bytes, cpu_seconds=cpu_seconds, wall_seconds=wall_seconds,
                      execution_status=result.get('execution_status'),
                      execution_reason=result.get('execution_reason'),
                      progress_error=result.get('progress_error'))
    return result


def run_colab(*, durable_root, work_root='/content/berry-esseen-runs',
              archives='/content/berry-esseen-archives', wall_seconds=DEFAULT_WALL_SECONDS,
              cpu_seconds=DEFAULT_CPU_SECONDS, backup_interval=60, mode='basic', memory_bytes=DEFAULT_MEMORY_BYTES):
    validate_budgets(wall_seconds=wall_seconds, cpu_seconds=cpu_seconds, memory_bytes=memory_bytes)
    from .colab_batch import Backups, atomic_json, bundle, event, utc
    from .environment import snapshot
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root = Path(work_root)/'tail49'/stamp
    root.mkdir(parents=True, exist_ok=False)
    durable = Path(durable_root)/'tail49'/stamp
    status = {'scope': 'COLAB_ORIGINAL_TAIL49_SELECTED_SUITE_NOT_GLOBAL_PROOF', 'state': 'started',
              'started_utc': utc(), 'required_top_level_executions': 14, 'required_retained_components': 41,
              'native_arithmetic_accepted': False, 'all_index_conclusion_verified': False,
              'basic_memory_bytes': memory_bytes, 'basic_cpu_seconds': cpu_seconds,
              'basic_wall_seconds': wall_seconds, 'execution_resource_profile': RESOURCE_PROFILE}
    atomic_json(root/'ENVIRONMENT.json', snapshot())
    atomic_json(root/'SESSION_RESULT.json', status)
    monitor = Backups(root, durable, interval=backup_interval)
    monitor.start()
    try:
        event(root, 'tail49_actual_full_replay_started', mode=mode, quick_mode=False,
              memory_bytes=memory_bytes, cpu_seconds=cpu_seconds, wall_seconds=wall_seconds,
              execution_resource_profile=RESOURCE_PROFILE)
        result = run(root/'arithmetic', archives=archives, download=True, mode=mode,
                     wall_seconds=wall_seconds, cpu_seconds=cpu_seconds, memory_bytes=memory_bytes)
        status.update(state='exact_selected_arithmetic_completed_untrusted_guard' if
                      result['all_required_jobs_computed'] else 'incomplete_full_suite', arithmetic_result=result)
    except BaseException as error:
        status.update(state='incomplete_error', error=type(error).__name__+': '+str(error))
        (root/'ERROR.txt').write_text(traceback.format_exc(), encoding='utf-8')
    finally:
        status['finished_utc'] = utc()
        atomic_json(root/'SESSION_RESULT.json', status)
        try:
            monitor.close()
        except Exception as error:
            event(root, 'final_backup_failed', error=str(error))
        archive = bundle(root, durable)
    print('TAIL49 RESULT:', status['state'], '\nZIP:', archive, flush=True)
    return {'status': status, 'bundle': str(archive.resolve()), 'work': str(root.resolve())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--archives', type=Path)
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--mode', choices=('basic', 'native'), default='basic')
    parser.add_argument('--wall-seconds', type=int, default=DEFAULT_WALL_SECONDS)
    parser.add_argument('--cpu-seconds', type=int, default=DEFAULT_CPU_SECONDS)
    parser.add_argument('--memory-mib', type=int, default=2048)
    parser.add_argument('--_worker', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args._worker:
        worker(args._worker)
        return 0
    if args.output is None or args.archives is None:
        parser.error('--output and --archives are required')
    result = run(args.output, archives=args.archives, download=args.download, mode=args.mode,
                 wall_seconds=args.wall_seconds, cpu_seconds=args.cpu_seconds,
                 memory_bytes=args.memory_mib*MIB)
    return 0 if result['all_required_jobs_computed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
