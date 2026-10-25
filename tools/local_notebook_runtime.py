"""Checksum-bound offline Colab runtime packaging; no original mathematics.

Generated notebooks are deliberately outside the source ZIP, avoiding a
notebook -> ZIP -> notebook hash cycle. No publication is required.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 'BE_NOTEBOOK_RUNTIME_V1'
MANIFEST = 'LOCAL_RUNTIME_MANIFEST.json'
SOURCE_DIRS = ('be_replay', 'proof', 'tests', 'tools', 'vendor', 'assets')
EXCLUDED = {'__pycache__', '.pytest_cache', '.ipynb_checkpoints', '.git', 'work'}


def linked(path):
    return path.is_symlink() or getattr(path, 'is_junction', lambda: False)()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()


def safe_name(name):
    if (type(name) is not str or not name or '\\' in name or ':' in name
            or '\0' in name or PurePosixPath(name).is_absolute()
            or PurePosixPath(name).as_posix() != name
            or any(v in ('', '.', '..') for v in name.split('/'))):
        raise ValueError('Canonical relative source filename required')
    return name


def source_files(root=ROOT):
    root = Path(root).resolve()
    selected = {}
    for directory in SOURCE_DIRS:
        base = root / directory
        if linked(base):
            raise ValueError('Linked source directory')
        if not base.is_dir():
            continue
        for path in sorted(base.rglob('*')):
            relative = path.relative_to(root)
            if any(p in EXCLUDED for p in relative.parts):
                continue
            if linked(path):
                raise ValueError('Linked source path: ' + str(relative))
            if path.is_file() and path.suffix not in ('.pyc', '.pyo', '.ipynb'):
                selected[safe_name(relative.as_posix())] = path
    license_path = root/'LICENSE'
    if linked(license_path):
        raise ValueError('Linked license')
    if license_path.is_file():
        selected['LICENSE'] = license_path
    if not (root / 'be_replay/__init__.py').is_file():
        raise ValueError('Execution package is missing')
    if not (root / 'tools/make_notebooks.py').is_file():
        raise ValueError('Notebook source is missing')
    return selected


def build(output, *, root=ROOT, base_commit=None):
    """Create a fresh immutable local source ZIP; never overwrite an old pin."""
    output = Path(output)
    selected = source_files(root)
    rows = {name: {'bytes': path.stat().st_size, 'sha256': digest(path)}
            for name, path in sorted(selected.items())}
    if len(rows) > 20000 or sum(r['bytes'] for r in rows.values()) > 512*1024**2:
        raise ValueError('Bounded source inventory exceeded')
    if any(row['bytes'] > 128*1024**2 for row in rows.values()):
        raise ValueError('Bounded source member exceeded')
    ledger = dict(schema=SCHEMA, base_commit=base_commit, files=rows,
                  original_mathematics_executed=False,
                  all_index_conclusion_verified=False,
                  generated_notebooks_included=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=6) as packet:
        for name, path in sorted(selected.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 25, 0, 0, 0))
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            packet.writestr(info, path.read_bytes())
        packet.writestr(MANIFEST, json.dumps(ledger, ensure_ascii=False,
                                           indent=2).encode('utf-8') + b'\n')
    # Re-read all archived source bytes, independently of the copy operation.
    with zipfile.ZipFile(output) as packet:
        if set(packet.namelist()) != set(rows) | {MANIFEST}:
            raise ValueError('Source ZIP inventory mismatch')
        for name, row in rows.items():
            raw = packet.read(name)
            if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
                raise ValueError('Source ZIP readback mismatch: ' + name)
    return dict(path=str(output), bytes=output.stat().st_size,
                sha256=digest(output), source_files=len(rows),
                original_mathematics_executed=False)


def bootstrap(source_name, source_sha256, task):
    """Return a standalone checked bootstrap cell body, with no network fallback."""
    if (safe_name(source_name) != Path(source_name).name
            or not source_name.endswith('.zip')):
        raise ValueError('A ZIP basename is required')
    if type(source_sha256) is not str or re.fullmatch('[0-9a-f]{64}', source_sha256) is None:
        raise ValueError('An actual source ZIP SHA256 is required')
    if type(task) is not str or re.fullmatch('[a-z0-9][a-z0-9-]{0,79}', task) is None:
        raise ValueError('A fixed task name is required')
    body = r'''from pathlib import Path, PurePosixPath
import hashlib, json, stat, sys, subprocess, zipfile
from google.colab import files
sys.dont_write_bytecode = True
SOURCE_NAME = __SOURCE_NAME__
SOURCE_SHA256 = __SOURCE_SHA256__
TASK = __TASK__
def _runtime_sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1024**2), b''): h.update(block)
    return h.hexdigest()
def _unique_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result: raise RuntimeError('Duplicate runtime manifest key')
        result[key] = value
    return result
source = Path('/content') / SOURCE_NAME
if source.is_symlink(): raise RuntimeError('Linked runtime ZIP')
if not source.is_file() or _runtime_sha(source) != SOURCE_SHA256:
    print('Upload the source ZIP supplied with this notebook:', SOURCE_NAME, flush=True)
    uploaded = files.upload()
    if SOURCE_NAME not in uploaded or hashlib.sha256(uploaded[SOURCE_NAME]).hexdigest() != SOURCE_SHA256:
        raise RuntimeError('The exact local source ZIP is required. No public-code fallback.')
    source.write_bytes(uploaded[SOURCE_NAME])
if _runtime_sha(source) != SOURCE_SHA256: raise RuntimeError('Local source ZIP SHA mismatch')
CODE = Path('/content') / ('berry-esseen-local-' + SOURCE_SHA256[:20])
if CODE.is_symlink(): raise RuntimeError('Linked execution directory')
with zipfile.ZipFile(source) as packet:
    infos = packet.infolist(); seen = set(); total = 0
    if not 0 < len(infos) <= 20001: raise RuntimeError('Bounded runtime inventory required')
    for info in infos:
        name = info.filename; path = PurePosixPath(name); mode = info.external_attr >> 16
        if (not name or path.is_absolute() or path.as_posix() != name
                or any(v in ('', '.', '..') for v in name.split('/'))
                or any(v in name for v in ('\\', ':', '\0')) or info.is_dir()
                or info.flag_bits & 1 or stat.S_IFMT(mode) not in (0, stat.S_IFREG)
                or name.casefold() in seen or not 0 <= info.file_size <= 128*1024**2):
            raise RuntimeError('Unsafe local runtime member')
        seen.add(name.casefold()); total += info.file_size
    if total > 512*1024**2 + 8*1024**2: raise RuntimeError('Runtime archive exceeds bound')
    raw_manifest = packet.read('LOCAL_RUNTIME_MANIFEST.json')
    if len(raw_manifest) > 8*1024**2: raise RuntimeError('Runtime manifest exceeds bound')
    ledger = json.loads(raw_manifest, object_pairs_hook=_unique_json)
    if ledger.get('schema') != 'BE_NOTEBOOK_RUNTIME_V1': raise RuntimeError('Wrong runtime schema')
    if not isinstance(ledger.get('files'), dict): raise RuntimeError('Runtime source map required')
    expected = set(ledger['files']) | {'LOCAL_RUNTIME_MANIFEST.json'}
    if {i.filename for i in infos} != expected: raise RuntimeError('Incomplete source manifest')
    for name, row in ledger['files'].items():
        raw = packet.read(name)
        if (type(row.get('bytes')) is not int or len(raw) != row['bytes']
                or hashlib.sha256(raw).hexdigest() != row.get('sha256')):
            raise RuntimeError('Runtime source manifest mismatch: ' + name)
    if not CODE.exists():
        CODE.mkdir()
        for info in infos:
            out = CODE.joinpath(*PurePosixPath(info.filename).parts)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(packet.read(info))
    if (CODE/'LOCAL_RUNTIME_MANIFEST.json').is_symlink() or (CODE/'LOCAL_RUNTIME_MANIFEST.json').read_bytes() != raw_manifest:
        raise RuntimeError('Changed local source manifest')
for name, row in ledger['files'].items():
    path = CODE.joinpath(*PurePosixPath(name).parts)
    if (path.is_symlink() or any(p.is_symlink() for p in path.parents if p != CODE.parent)
            or not path.is_file() or path.stat().st_size != row['bytes']
            or _runtime_sha(path) != row['sha256']):
        raise RuntimeError('Changed runtime source: ' + name)
for path in CODE.rglob('*'):
    relative = path.relative_to(CODE)
    if relative.parts[0] == 'work': continue
    if path.is_symlink() or (path.is_file() and relative.as_posix() not in expected):
        raise RuntimeError('Unexpected runtime helper: ' + relative.as_posix())
if (CODE/'work').is_symlink(): raise RuntimeError('Linked scratch directory')
(CODE/'work').mkdir(exist_ok=True)
for name in tuple(sys.modules):
    if name == 'be_replay' or name.startswith('be_replay.'): del sys.modules[name]
sys.path.insert(0, str(CODE))
from be_replay.environment import snapshot
if not Path(sys.modules['be_replay'].__file__).resolve().is_relative_to(CODE.resolve()):
    raise RuntimeError('Imported execution code is outside the checked source ZIP')
print(json.dumps(snapshot(), indent=2), flush=True)
print('Local source ZIP verified. Mathematical acceptance has not been established.', flush=True)
'''
    return (body.replace('__SOURCE_NAME__', repr(source_name))
            .replace('__SOURCE_SHA256__', repr(source_sha256))
            .replace('__TASK__', repr(task)))


def common(source_name, source_sha256, task):
    spec = importlib.util.spec_from_file_location('offline_notebook_base', ROOT/'tools/make_notebooks.py')
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    return [base.cell('code', bootstrap(source_name, source_sha256, task), 'local-source'),
            *base.common('1'*40, task)[1:]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--base-commit')
    args = parser.parse_args()
    print(json.dumps(build(args.output, base_commit=args.base_commit), indent=2))
