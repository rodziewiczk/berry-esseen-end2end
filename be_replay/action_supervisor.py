# Resource-only derivative of linux_supervisor.py for new acquisition actions.
# Counts utime+stime+cutime+cstime for every live group member. Waited children
# remain charged through their living ancestor; the unreaped leader is sampled
# before cleanup. This is a sampled cumulative limit, not a kernel cgroup.
# Existing execution/cache profiles continue to use linux_supervisor.py.
# Refuse a mismatched proc mount before launching or sampling any child.
"""Bounded Linux execution, with honestly separated resource contracts.

``untrusted_search`` is discovery only.  The wall watchdog and termination
cover an owned POSIX process group. RLIMIT_AS and RLIMIT_CPU are per process;
sampled group RSS/CPU and file quotas are observations, not cgroup limits.
An escaped session is outside that contract. No result here accepts a proof.

``trusted_native`` uses a separate limited supervisor and a Python runpy
worker. A Linux seccomp filter kills process/thread creation, exec and group
escape after interpreter startup. Hard address-space and CPU allowances are
split between those two processes. These are address-space allowances, not
cgroup charged-memory guarantees. Missing capability fails closed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import time

MIB = 1024**2


class SupervisorError(ValueError):
    pass


def _need(value, message):
    if not value:
        raise SupervisorError(message)


def _sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(MIB), b''):
            digest.update(block)
    return digest.hexdigest()


def _atomic_json(path, value):
    path = Path(path)
    pending = path.with_name(path.name + '.pending')
    with pending.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(pending, path)


def _progress(directory, value):
    """Durable append-only stage history plus an atomic current snapshot."""
    encoded = json.dumps(value, sort_keys=True)+'\n'
    with (Path(directory)/'progress.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    _atomic_json(Path(directory)/'progress.json', value)


def _last_json(path, maximum=16384):
    try:
        with Path(path).open('rb') as stream:
            stream.seek(0, os.SEEK_END)
            size = stream.tell()
            stream.seek(max(0, size-maximum))
            raw = stream.read(maximum)
        lines = raw.splitlines()
        # A partial final write is not a complete progress event.
        if raw and not raw.endswith(b'\n'):
            lines = lines[:-1]
        if size > maximum:
            lines = lines[1:]  # first line may begin outside the bounded tail
        for line in reversed(lines):
            try:
                value = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                continue
            if isinstance(value, dict):
                return value
    except FileNotFoundError:
        pass
    return None


def _settings(argv, cwd, output_dir, wall_seconds, cpu_seconds, memory_bytes,
              checkpoint_paths, mode, sample_seconds, disk_bytes, log_bytes):
    _need(mode in ('untrusted_search', 'trusted_native'), 'Explicit execution mode')
    _need(isinstance(argv, (list, tuple)) and argv and
          all(type(v) is str and v and '\x00' not in v for v in argv), 'Literal nonempty argv list')
    _need(type(wall_seconds) in (int, float) and math.isfinite(wall_seconds) and wall_seconds > 0,
          'Finite positive external wall limit')
    for name, value in (('cpu_seconds', cpu_seconds), ('memory_bytes', memory_bytes),
                        ('disk_bytes', disk_bytes), ('log_bytes', log_bytes)):
        _need(type(value) is int and value > 0, 'Positive integer ' + name)
    _need(memory_bytes >= 64*MIB, 'At least64MiB address-space allowance')
    _need(type(sample_seconds) in (int, float) and .01 <= sample_seconds <= 1,
          'Sampling interval between .01 and1 second')
    cwd = Path(cwd).absolute()
    _need(cwd.is_dir() and not cwd.is_symlink(), 'Existing ordinary working directory')
    cwd = cwd.resolve()
    output_dir = Path(output_dir).absolute()
    _need(not output_dir.is_symlink() and output_dir != cwd,
          'Dedicated ordinary output directory distinct from cwd')
    if output_dir.exists():
        _need(output_dir.is_dir() and not any(output_dir.iterdir()), 'Output directory must be empty')
    else:
        output_dir.mkdir(parents=True)
    output_dir = output_dir.resolve()
    checkpoints = []
    for path in checkpoint_paths:
        path = Path(path)
        if not path.is_absolute():
            path = cwd/path
        # Resolve parents even for a checkpoint not written yet.
        _need(not path.is_symlink(), 'No checkpoint symlink')
        resolved = path.resolve()
        _need(resolved.is_relative_to(cwd) and resolved != cwd,
              'Every checkpoint belongs to this working directory')
        _need(resolved not in checkpoints, 'No duplicate checkpoint path')
        checkpoints.append(resolved)
    return dict(argv=list(argv), cwd=str(cwd), output_dir=str(output_dir),
                wall_seconds=float(wall_seconds), cpu_seconds=cpu_seconds,
                memory_bytes=memory_bytes, checkpoint_paths=[str(p) for p in checkpoints],
                mode=mode, sample_seconds=float(sample_seconds), disk_bytes=disk_bytes,
                log_bytes=log_bytes)


def _proc_stat(pid):
    """PID, birth tick, state and group from the real Linux proc namespace."""
    raw = Path('/proc', str(pid), 'stat').read_text('ascii')
    closing = raw.rfind(')')
    opening = raw.find(' (')
    _need(opening > 0 and closing > opening and int(raw[:opening]) == pid, 'Actual proc PID')
    fields = raw[closing+1:].split()
    _need(len(fields) >= 22, 'Complete Linux process stat')
    return dict(pid=pid, state=fields[0], ppid=int(fields[1]), pgid=int(fields[2]),
                session=int(fields[3]), birth=int(fields[19]),
                cpu_ticks=int(fields[11])+int(fields[12])+int(fields[13])+int(fields[14]), vms_bytes=int(fields[20]),
                rss_pages=max(0, int(fields[21])))


def _group_sample(pgid):
    values = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            value = _proc_stat(int(entry.name))
        except (FileNotFoundError, ProcessLookupError):
            continue
        if value['pgid'] == pgid and (value['state'] not in ('Z', 'X') or
                                      (value['pid'] == pgid and value['state'] == 'Z')):
            values.append(value)
    return values


def _directory_bytes(roots, maximum):
    """Sampled ordinary-file size quota; no stable-snapshot proof is implied."""
    roots = sorted(set(Path(root).resolve() for root in roots), key=lambda p: len(p.parts))
    selected = []
    for root in roots:
        if not any(root.is_relative_to(parent) for parent in selected):
            selected.append(root)
    used, count = 0, 0
    for root in selected:
        for directory, names, files in os.walk(root, followlinks=False):
            for name in [*names, *files]:
                path = Path(directory)/name
                try:
                    value = path.lstat()
                except FileNotFoundError:
                    continue  # an atomic checkpoint publication; sample again later
                _need(not stat.S_ISLNK(value.st_mode) and
                      (stat.S_ISDIR(value.st_mode) or stat.S_ISREG(value.st_mode)),
                      'No symlink or special file in owned work/output')
                if stat.S_ISREG(value.st_mode):
                    used += value.st_size
                    count += 1
                    _need(used <= maximum and count <= 100000, 'Sampled work/output quota exceeded')
    return used


def _exited_without_reaping(process):
    # Keep the group leader as an unreaped zombie until cleanup, preventing
    # reuse of its PID/process-group identifier while we signal the group.
    return os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT) is not None


def _terminate_group(process):
    for signum, delay in ((signal.SIGTERM, .3), (signal.SIGKILL, .2)):
        try:
            os.killpg(process.pid, signum)
        except ProcessLookupError:
            pass
        if signum == signal.SIGTERM:
            time.sleep(delay)
    process.wait(timeout=3)
    return [v['pid'] for v in _group_sample(process.pid)]


def _capture_checkpoints(config):
    result = []
    output = Path(config['output_dir'])/'checkpoints'
    for original in map(Path, config['checkpoint_paths']):
        row = {'source_path': str(original), 'exists': original.exists(),
               'trusted_certificate': False}
        try:
            _need(not original.is_symlink(), 'No checkpoint symlink after execution')
            if original.exists():
                value = original.lstat()
                _need(stat.S_ISREG(value.st_mode) and value.st_size <= config['disk_bytes'],
                      'Bounded regular checkpoint only')
                destination = output/original.relative_to(Path(config['cwd']))
                destination.parent.mkdir(parents=True, exist_ok=True)
                # No search writer in the owned group remains at this point.
                total = 0
                with original.open('rb') as source, destination.open('xb') as target:
                    while block := source.read(MIB):
                        total += len(block)
                        _need(total <= config['disk_bytes'], 'Bounded checkpoint capture')
                        target.write(block)
                row.update(path=str(destination), bytes=total, sha256=_sha(destination))
        except (OSError, SupervisorError) as exc:
            row['capture_error'] = str(exc)
        result.append(row)
    return result


def _checkpoint_progress(paths):
    rows = []
    for path in paths:
        try:
            value = Path(path).lstat()
            rows.append({'path': path, 'exists': stat.S_ISREG(value.st_mode),
                         'bytes': value.st_size if stat.S_ISREG(value.st_mode) else None})
        except FileNotFoundError:
            rows.append({'path': path, 'exists': False, 'bytes': None})
    return rows


def _search(config):
    directory = Path(config['output_dir'])
    stdout_path, stderr_path = directory/'stdout.txt', directory/'stderr.txt'
    launch_path = directory/'launch.json'
    _atomic_json(launch_path, config)
    command = [sys.executable, '-B', '-S', str(Path(__file__).resolve()), '--_exec-search', str(launch_path)]
    scope = {'kind': 'UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP', 'proof_acceptance': False,
             'external_wall_seconds': config['wall_seconds'],
             'per_process_RLIMIT_AS_bytes': config['memory_bytes'],
             'per_process_RLIMIT_CPU_seconds': config['cpu_seconds'],
             'aggregate_kernel_memory_limit': False, 'aggregate_kernel_cpu_limit': False,
             'sampled_group_RSS_limit_bytes': config['memory_bytes'],
             'sampled_group_CPU_limit_seconds': config['cpu_seconds'],
             'sampled_group_CPU_includes_waited_descendants': True,
             'sampled_file_limit_bytes': config['disk_bytes'],
             'sampled_log_limit_bytes': config['log_bytes'],
             'descendants_changing_session_are_contained': False,
             'equivalent_to_Windows_Job_or_cgroup': False}
    started = time.monotonic()
    process, reason, peak_rss, peak_cpu, samples = None, None, 0, 0.0, 0
    last_progress = -float(config.get('heartbeat_seconds', 20))
    env = os.environ.copy()
    for key in ('PYTHONPATH', 'PYTHONHOME', 'PYTHONOPTIMIZE', 'PYTHONSTARTUP'):
        env.pop(key, None)
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1', PYTHONUNBUFFERED='1')
    try:
        with stdout_path.open('xb') as output, stderr_path.open('xb') as error:
            process = subprocess.Popen(command, cwd=config['cwd'], env=env,
                                       stdin=subprocess.DEVNULL, stdout=output, stderr=error,
                                       start_new_session=True, close_fds=True)
            page_size, ticks = os.sysconf('SC_PAGE_SIZE'), os.sysconf('SC_CLK_TCK')
            while True:
                elapsed = time.monotonic()-started
                if elapsed >= config['wall_seconds']:
                    reason = 'external_wall_timeout'
                    break
                members = _group_sample(process.pid)
                rss = sum(v['rss_pages'] for v in members)*page_size
                cpu = sum(v['cpu_ticks'] for v in members)/ticks
                peak_rss, peak_cpu = max(peak_rss, rss), max(peak_cpu, cpu)
                samples += 1
                if elapsed-last_progress >= config.get('heartbeat_seconds', 20):
                    progress = {'event': 'linux_supervisor_progress', 'mode': config['mode'],
                                'stage': config['mode'],
                                'elapsed_seconds': elapsed, 'wall_limit_seconds': config['wall_seconds'],
                                'sample_count': samples, 'maximum_sampled_group_RSS_bytes': peak_rss,
                                'maximum_sampled_group_CPU_seconds': peak_cpu,
                                'proof_accepted': False,
                                'checkpoints': _checkpoint_progress(config['checkpoint_paths'])}
                    native_progress = _last_json(stdout_path)
                    if native_progress is not None:
                        progress['native_progress'] = native_progress
                    _progress(directory, progress)
                    print(json.dumps(progress, sort_keys=True), flush=True)
                    last_progress = elapsed
                _need(rss <= config['memory_bytes'], 'Sampled group RSS limit exceeded')
                _need(cpu <= config['cpu_seconds'], 'Sampled group CPU limit exceeded')
                _directory_bytes((config['cwd'], directory), config['disk_bytes'])
                _need(stdout_path.stat().st_size+stderr_path.stat().st_size <= config['log_bytes'],
                      'Sampled output log limit exceeded')
                if _exited_without_reaping(process):
                    other = [v for v in members if v['pid'] != process.pid]
                    if other:
                        reason = 'live_group_descendants_after_main_exit'
                    break
                time.sleep(min(config['sample_seconds'], max(.001, config['wall_seconds']-elapsed)))
    except (OSError, SupervisorError) as exc:
        reason = str(exc)
    finally:
        if process is not None:
            try:
                remaining = _terminate_group(process)
                if remaining:
                    reason = 'owned_process_group_not_empty_after_kill:' + str(remaining)
            except (OSError, subprocess.TimeoutExpired) as exc:
                reason = 'process_group_cleanup_failed:' + str(exc)
    returncode = process.returncode if process is not None else None
    if returncode != 0 and reason is None:
        reason = 'nonzero_subprocess_exit'
    result = {'status': 'completed' if reason is None else 'incomplete', 'reason': reason,
              'mode': config['mode'], 'returncode': returncode,
              'elapsed_seconds': time.monotonic()-started,
              'stdout_path': str(stdout_path), 'stderr_path': str(stderr_path),
              'stdout_sha256': _sha(stdout_path) if stdout_path.exists() else None,
              'stderr_sha256': _sha(stderr_path) if stderr_path.exists() else None,
              'guard_scope': scope, 'sample_count': samples,
              'maximum_sampled_group_RSS_bytes': peak_rss,
              'maximum_sampled_group_CPU_seconds': peak_cpu,
              'checkpoints': _capture_checkpoints(config), 'proof_accepted': False}
    _atomic_json(directory/'supervisor-result.json', result)
    _progress(directory, {'event': 'linux_supervisor_finished', 'stage': config['mode'],
                 'status': result['status'], 'reason': result['reason'],
                 'elapsed_seconds': result['elapsed_seconds'], 'proof_accepted': False})
    return result


def run(argv, *, cwd, output_dir, wall_seconds, cpu_seconds=7200,
        memory_bytes=512*MIB, checkpoint_paths=(), mode='untrusted_search',
        sample_seconds=.2, disk_bytes=256*MIB, log_bytes=16*MIB, heartbeat_seconds=20):
    """Execute discovery or a separately guarded native Python replay.

    Returns absolute log paths and a durable supervisor receipt. A completed
    discovery is still untrusted and never constitutes native acceptance.
    """
    config = _settings(argv, cwd, output_dir, wall_seconds, cpu_seconds, memory_bytes,
                       checkpoint_paths, mode, sample_seconds, disk_bytes, log_bytes)
    _need(type(heartbeat_seconds) in (int, float) and 1 <= heartbeat_seconds <= 60,
          'Heartbeat interval between1 and60 seconds')
    config['heartbeat_seconds'] = float(heartbeat_seconds)
    if sys.platform != 'linux' or not hasattr(os, 'waitid'):
        return {'status': 'unsupported', 'returncode': None, 'elapsed_seconds': 0,
                'stdout_path': str(Path(config['output_dir'])/'stdout.txt'),
                'stderr_path': str(Path(config['output_dir'])/'stderr.txt'),
                'guard_scope': {'kind': 'UNAVAILABLE', 'proof_acceptance': False},
                'reason': 'Actual Linux proc/waitid/POSIX process groups required',
                'proof_accepted': False}
    # Some hosted test runners expose a parent PID namespace at /proc while
    # executing commands in a child namespace. A numerical PID lookup there
    # could charge an unrelated process. Fail before launch rather than use
    # that observation as a resource receipt.
    try:
        own_pid = int(Path('/proc/self/stat').read_text('ascii').split(' ', 1)[0])
        _need(own_pid == os.getpid(), 'proc_PID_namespace_mismatch')
        _need(_proc_stat(own_pid)['pgid'] == os.getpgrp(), 'proc_process_group_namespace_mismatch')
    except (OSError, ValueError) as error:
        result = {'status': 'unsupported', 'returncode': None, 'elapsed_seconds': 0,
                  'stdout_path': str(Path(config['output_dir'])/'stdout.txt'),
                  'stderr_path': str(Path(config['output_dir'])/'stderr.txt'),
                  'guard_scope': {'kind': 'UNAVAILABLE', 'proof_acceptance': False},
                  'reason': str(error), 'proof_accepted': False}
        _atomic_json(Path(config['output_dir'])/'supervisor-result.json', result)
        return result
    if mode == 'trusted_native':
        return _native(config)
    return _search(config)


def _python_target(argv, cwd):
    _need(Path(argv[0]).resolve() == Path(sys.executable).resolve(),
          'Native replay uses this actual Python interpreter')
    remaining = list(argv[1:])
    while remaining and remaining[0] in ('-B', '-S'):
        remaining.pop(0)
    _need(remaining and not remaining[0].startswith('-'),
          'Native replay requires a literal Python script, not -c/-m')
    script = Path(remaining[0])
    if not script.is_absolute():
        script = Path(cwd)/script
    _need(script.is_file() and not script.is_symlink() and script.resolve().is_relative_to(Path(cwd)),
          'Native script is a regular file in the owned capsule')
    return [str(script.resolve()), *remaining[1:]]


def _seccomp_spec(machine):
    # syscall numbers from Linux UAPI for the explicitly supported ABIs.
    # https://github.com/torvalds/linux/blob/v6.12/arch/x86/entry/syscalls/syscall_64.tbl
    # https://github.com/torvalds/linux/blob/v6.12/include/uapi/asm-generic/unistd.h
    if machine == 'x86_64':
        return (0xc000003e, {'clone': 56, 'fork': 57, 'vfork': 58, 'execve': 59,
                'setpgid': 109, 'setsid': 112, 'setrlimit': 160, 'unshare': 272,
                'setns': 308, 'execveat': 322, 'clone3': 435}, 302)
    if machine in ('aarch64', 'arm64'):
        return (0xc00000b7, {'clone': 220, 'execve': 221, 'setpgid': 154, 'setsid': 157,
                'setrlimit': 164, 'unshare': 97, 'setns': 268, 'execveat': 281,
                'clone3': 435}, 261)
    raise SupervisorError('Unsupported audited seccomp architecture: ' + machine)


def _filter_instructions(machine):
    architecture, denied, prlimit = _seccomp_spec(machine)
    load, equal, greater_equal, ret = 0x20, 0x15, 0x35, 0x06
    kill, allow = 0x80000000, 0x7fff0000  # KILL_PROCESS, ALLOW
    rows = [(load, 0, 0, 4), (equal, 1, 0, architecture), (ret, 0, 0, kill),
            (load, 0, 0, 0), (greater_equal, 0, 1, 0x40000000), (ret, 0, 0, kill)]
    for number in sorted(set(denied.values())):
        rows.extend(((equal, 0, 1, number), (ret, 0, 0, kill)))
    # prlimit64 is allowed only for querying: new_limit argument must be NULL.
    # Checking both halves also covers a nonzero pointer above4GiB.
    rows.extend(((equal, 0, 6, prlimit), (load, 0, 0, 32), (equal, 1, 0, 0),
                 (ret, 0, 0, kill), (load, 0, 0, 36), (equal, 1, 0, 0),
                 (ret, 0, 0, kill), (ret, 0, 0, allow)))
    return rows, architecture, denied, prlimit


def _install_single_process_filter():
    import ctypes
    _need(len(list(Path('/proc/self/task').iterdir())) == 1,
          'Exactly one interpreter thread before installing the filter')
    rows, architecture, denied, prlimit = _filter_instructions(os.uname().machine)
    class SockFilter(ctypes.Structure):
        _fields_ = [('code', ctypes.c_ushort), ('jt', ctypes.c_ubyte),
                    ('jf', ctypes.c_ubyte), ('k', ctypes.c_uint32)]
    class SockFprog(ctypes.Structure):
        _fields_ = [('len', ctypes.c_ushort), ('filter', ctypes.POINTER(SockFilter))]
    array = (SockFilter*len(rows))(*(SockFilter(*row) for row in rows))
    program = SockFprog(len(rows), array)
    libc = ctypes.CDLL(None, use_errno=True)
    _need(libc.prctl(38, 1, 0, 0, 0) == 0, 'Kernel PR_SET_NO_NEW_PRIVS succeeded')
    _need(libc.prctl(22, 2, ctypes.byref(program), 0, 0) == 0,
          'Kernel installed this complete seccomp BPF filter')
    _need(libc.prctl(39, 0, 0, 0, 0) == 1 and libc.prctl(21, 0, 0, 0, 0) == 2,
          'Actual no-new-privileges and seccomp filter mode')
    _need(len(list(Path('/proc/self/task').iterdir())) == 1,
          'Exactly one filtered interpreter thread before numerical entry')
    return {'seccomp_mode': 2, 'no_new_privileges': True, 'audit_architecture': architecture,
            'machine': os.uname().machine, 'denied_syscalls': denied,
            'prlimit64_query_only': prlimit, 'x32_or_unknown_syscall_ABI_killed': True,
            'filter_instructions_sha256': hashlib.sha256(json.dumps(rows).encode()).hexdigest()}


def _limits(memory_bytes, cpu_seconds):
    import resource
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
    _need(resource.getrlimit(resource.RLIMIT_AS) == (memory_bytes, memory_bytes) and
          resource.getrlimit(resource.RLIMIT_CPU) == (cpu_seconds, cpu_seconds),
          'Actual hard and soft kernel address-space/CPU limits')
    _need(_proc_stat(os.getpid())['vms_bytes'] <= memory_bytes,
          'Existing interpreter mappings already within its hard address-space allowance')


def _native_worker(path):
    import runpy
    config = json.loads(Path(path).read_text('utf-8'))
    target = _python_target(config['argv'], config['cwd'])
    os.chdir(config['cwd'])
    sys.path.insert(0, str(Path(target[0]).parent))
    sys.dont_write_bytecode = True
    sys.pycache_prefix = str(Path(config['output_dir'])/'never-created-native-pycache')
    _limits(config['worker_memory_bytes'], config['worker_cpu_seconds'])
    guard = _install_single_process_filter()
    # Interpreter startup precedes numerical entry. Never enter the unchanged
    # kernel until the dedicated parent has also lowered its own hard caps.
    deadline = time.monotonic()+min(10, config['wall_seconds'])
    ready = Path(config['output_dir'])/'native-controller-guard.json'
    while not ready.is_file():
        _need(time.monotonic() <= deadline, 'Bounded supervisor-capability handshake')
        time.sleep(.01)
    controller_guard = json.loads(ready.read_text('utf-8'))
    _need(controller_guard['address_space_bytes'] == config['supervisor_memory_bytes'] and
          controller_guard['cpu_seconds'] == config['supervisor_cpu_seconds'] and
          controller_guard['seccomp_mode'] == 2, 'Parent hard caps before native numerical entry')
    guard.update(address_space_bytes=config['worker_memory_bytes'],
                 cpu_seconds=config['worker_cpu_seconds'], script_sha256=_sha(target[0]),
                 pid=os.getpid(), birth_tick=_proc_stat(os.getpid())['birth'])
    _atomic_json(Path(config['output_dir'])/'native-worker-guard.json', guard)
    sys.argv = target
    runpy.run_path(target[0], run_name='__main__')


def _native_controller(path):
    # This is a dedicated bounded supervisor, not the notebook interpreter.
    config = json.loads(Path(path).read_text('utf-8'))
    process = subprocess.Popen([sys.executable, '-B', '-S', str(Path(__file__).resolve()),
                                '--_native-worker', str(path)], cwd=config['cwd'],
                               stdin=subprocess.DEVNULL, close_fds=True)
    try:
        # Spawn before lowering our hard limits: otherwise the child could
        # not raise inherited64MiB/30s caps to its own assigned allowance.
        _limits(config['supervisor_memory_bytes'], config['supervisor_cpu_seconds'])
        guard = _install_single_process_filter()
        guard.update(address_space_bytes=config['supervisor_memory_bytes'],
                     cpu_seconds=config['supervisor_cpu_seconds'], pid=os.getpid(),
                     birth_tick=_proc_stat(os.getpid())['birth'])
        _atomic_json(Path(config['output_dir'])/'native-controller-guard.json', guard)
        returncode = process.wait(timeout=config['wall_seconds'])
        _atomic_json(Path(config['output_dir'])/'native-controller-result.json',
                     {'returncode': returncode, 'worker_pid': process.pid,
                      'worker_source_sha256_after': _sha(_python_target(config['argv'], config['cwd'])[0])})
        return returncode
    finally:
        if process.returncode is None:
            process.kill()
            process.wait(timeout=3)


def _native(config):
    target = _python_target(config['argv'], config['cwd'])
    _need(config['memory_bytes'] >= 128*MIB and config['cpu_seconds'] >= 2,
          'Native contract requires at least128MiB and2 CPU seconds')
    config['supervisor_memory_bytes'] = 64*MIB
    config['worker_memory_bytes'] = config['memory_bytes']-64*MIB
    config['supervisor_cpu_seconds'] = min(30, max(1, config['cpu_seconds']//10))
    config['worker_cpu_seconds'] = config['cpu_seconds']-config['supervisor_cpu_seconds']
    source_sha = _sha(target[0])
    output = Path(config['output_dir'])
    path = output/'native-launch.json'
    _atomic_json(path, config)
    outer = dict(config, argv=[sys.executable, '-B', '-S', str(Path(__file__).resolve()),
                               '--_native-controller', str(path)])
    result = _search(outer)
    original_scope = result['guard_scope']
    result['guard_scope'] = {'kind': 'LINUX_SECCOMP_SINGLE_PROCESS_PYTHON_V1',
        'contract_status': 'experimental_platform_contract_requires_review',
        'proof_acceptance': False, 'native_python_execution': True,
        'hard_sum_RLIMIT_AS_bytes': config['memory_bytes'],
        'sum_caps_apply_from': 'both_interpreters_guarded_before_native_runpy_entry',
        'worker_RLIMIT_AS_bytes': config['worker_memory_bytes'],
        'supervisor_RLIMIT_AS_bytes': config['supervisor_memory_bytes'],
        'hard_sum_RLIMIT_CPU_seconds': config['cpu_seconds'],
        'worker_RLIMIT_CPU_seconds': config['worker_cpu_seconds'],
        'supervisor_RLIMIT_CPU_seconds': config['supervisor_cpu_seconds'],
        'notebook_or_orchestrator_included_in_caps': False,
        'aggregate_cgroup_charged_memory_guarantee': False,
        'equivalent_to_Windows_Job_or_cgroup': False,
        'external_group_watchdog': original_scope,
        'script_sha256': source_sha, 'supervisor_source_sha256': _sha(__file__)}
    if result['status'] == 'completed':
        try:
            supervisor_guard = json.loads((output/'native-controller-guard.json').read_text('utf-8'))
            worker_guard = json.loads((output/'native-worker-guard.json').read_text('utf-8'))
            receipt = json.loads((output/'native-controller-result.json').read_text('utf-8'))
            expected_rows, expected_arch, expected_denied, expected_prlimit = _filter_instructions(os.uname().machine)
            expected_filter_sha = hashlib.sha256(json.dumps(expected_rows).encode()).hexdigest()
            for guard, memory, cpu in ((supervisor_guard, config['supervisor_memory_bytes'],
                                        config['supervisor_cpu_seconds']),
                                       (worker_guard, config['worker_memory_bytes'], config['worker_cpu_seconds'])):
                _need(guard['seccomp_mode'] == 2 and guard['no_new_privileges'] is True and
                      guard['address_space_bytes'] == memory and guard['cpu_seconds'] == cpu and
                      guard['audit_architecture'] == expected_arch and
                      guard['denied_syscalls'] == expected_denied and
                      guard['prlimit64_query_only'] == expected_prlimit and
                      guard['filter_instructions_sha256'] == expected_filter_sha,
                      'Both bounded single-process kernel guard receipts required')
            _need(receipt['returncode'] == 0 and worker_guard['script_sha256'] == source_sha ==
                  receipt['worker_source_sha256_after'] == _sha(target[0]),
                  'Fresh native completion and unchanged script binding')
            prefix = output/'never-created-native-pycache'
            _need(not prefix.exists() and not prefix.is_symlink(), 'No native bytecode cache prefix created')
            result['guard_scope'].update(worker_guard=worker_guard, supervisor_guard=supervisor_guard,
                                         capability_established=True)
        except (OSError, ValueError, KeyError) as exc:
            result.update(status='incomplete', reason='native_platform_contract_not_established: '+str(exc))
    result['proof_accepted'] = False  # the caller must validate mathematical protocol output
    # The intermediate search-style receipt is explicitly replaced with the
    # complete native contract; an interrupted rewrite cannot count as native.
    _atomic_json(output/'supervisor-result.json', result)
    _progress(output, {'event': 'native_supervisor_finished', 'stage': 'trusted_native',
                      'status': result['status'], 'reason': result['reason'],
                      'elapsed_seconds': result['elapsed_seconds'], 'proof_accepted': False})
    return result


def _exec_search(path):
    import resource
    config = json.loads(Path(path).read_text('utf-8'))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_AS, (config['memory_bytes'], config['memory_bytes']))
    resource.setrlimit(resource.RLIMIT_CPU, (config['cpu_seconds'], config['cpu_seconds']))
    os.execvpe(config['argv'][0], config['argv'], os.environ)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--_exec-search', type=Path)
    parser.add_argument('--_native-controller', type=Path)
    parser.add_argument('--_native-worker', type=Path)
    args = parser.parse_args()
    _need(sum(v is not None for v in vars(args).values()) == 1, 'One internal launch mode required')
    if args._exec_search is not None:
        _exec_search(args._exec_search)
    elif args._native_worker is not None:
        _native_worker(args._native_worker)
    else:
        raise SystemExit(_native_controller(args._native_controller))


if __name__ == '__main__':
    main()
