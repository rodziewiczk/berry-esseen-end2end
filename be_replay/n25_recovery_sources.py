"""Pinned recovery of original n25 inputs, without importing mathematical code.

Historical receipts live only in provenance/. The capsule contains the unchanged
original design and, for ordinary targets, its UNTRUSTED original forest. Source
verification never claims leaf acceptance, acquired parents, or the n25 theorem.
"""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import zipfile

from . import n25_b5_reconstruction_sources as base

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT/'proof/n25_recovery_source_plan.json'
PLAN_SHA256 = '3952fc7bc5e4ce2a7f8434a65c641741392d02f84877d58cfdc38cadf480028b'
ARCHIVE_SHA256 = '3aac9416c286f14465037629f2aa692f1b3f5d2f216ad48821fbb581cc3c70f6'
DEFAULT_ARCHIVE = ROOT/'assets/BE_cutoff25_missing_files_20261024.zip'
SCHEMA = 'N25_ORIGINAL_RECOVERY_SOURCE_PLAN_V1'
SOURCE_SCHEMA = 'N25_RECOVERED_ORIGINAL_INPUTS_V1'
MIB = 1024**2
MAX_MEMBER = 128*MIB
MAX_TOTAL = 1024*MIB
NODE_LIMIT = 10000
DEPTH_LIMIT = 128
need, parsed, sha, encoded = base.need, base.parsed, base.sha, base.encoded


def _plan():
    raw = base._regular(PLAN, 8*MIB)
    need(sha(raw) == PLAN_SHA256, 'Pinned original-recovery source plan')
    value = parsed(raw)
    need(value['schema'] == SCHEMA and value['asset']['sha256'] == ARCHIVE_SHA256
         and value['original_mathematical_code_executed'] is False
         and value['full66_complete'] is False, 'Source-only recovery plan')
    return value


def normalize(target):
    need(type(target) is str, 'Text original target')
    plan = _plan()
    target = plan['aliases'].get(target, target)
    need(target in plan['profiles'], 'One of the thirteen pinned original capsules')
    return target


def targets(*, include_mixed=False):
    return tuple(t for t, row in _plan()['profiles'].items()
                 if include_mixed or row['kind'] != 'mixed-parent-v14')


def profile(target, *, ordinary=False):
    target = normalize(target)
    row = _plan()['profiles'][target]
    need(not ordinary or row['kind'] != 'mixed-parent-v14',
         'Mixed p24/p25 require their complete mixed verifier, not ordinary COUNT')
    return deepcopy(row)


def _safe_name(name):
    need(type(name) is str and name and '\\' not in name and ':' not in name and '\0' not in name,
         'Safe archive member name')
    path = PurePosixPath(name)
    need(not path.is_absolute() and path.as_posix() == name
         and all(p not in ('', '.', '..') and p == p.rstrip(' .') for p in name.split('/')),
         'Canonical relative archive member')
    for part in path.parts:
        base._flat(part)
    return path


def _inventory(archive):
    infos = archive.infolist()
    need(0 < len(infos) <= 2200, 'Bounded recovery ZIP inventory')
    names, folded, total = set(), set(), 0
    for info in infos:
        _safe_name(info.filename)
        mode = info.external_attr >> 16
        need(not info.is_dir() and not info.flag_bits & 1
             and stat.S_IFMT(mode) in (0, stat.S_IFREG)
             and info.filename not in names and info.filename.casefold() not in folded
             and 0 <= info.file_size <= MAX_MEMBER, 'Unique ordinary unencrypted recovery members')
        names.add(info.filename)
        folded.add(info.filename.casefold())
        total += info.file_size
    need(total <= MAX_TOTAL, 'Bounded uncompressed recovery asset')
    return names


def _stream_hash(stream):
    digest = hashlib.sha256()
    size = 0
    for chunk in iter(lambda: stream.read(MIB), b''):
        size += len(chunk)
        digest.update(chunk)
    return size, digest.hexdigest()


class RecoveryArchive:
    """One fully verified, open asset for a batch; never trusts an old report.

    Verification and extraction use the same file handle. Every staged member is
    checked again, so a changed source file cannot be laundered by an earlier check.
    """
    def __init__(self, path=DEFAULT_ARCHIVE):
        self.path = Path(path)
        self._file = None
        self._zip = None
        self.rows = None
        self.report = None

    def __enter__(self):
        base._no_link_ancestors(self.path)
        need(self.path.is_file() and self.path.stat().st_size <= 128*MIB, 'Bounded regular recovery ZIP')
        self._file = self.path.open('rb')
        try:
            size, pin = _stream_hash(self._file)
            spec = _plan()['asset']
            need(size == spec['bytes'] and pin == spec['sha256'], 'Exact external recovery ZIP SHA256 and size')
            self._file.seek(0)
            self._zip = zipfile.ZipFile(self._file)
            names = _inventory(self._zip)
            raw = self._zip.read('AUDIT_MANIFEST.json')
            need(sha(raw) == spec['manifest_sha256'], 'Externally bound original recovery manifest')
            manifest = parsed(raw)
            need(manifest['schema'] == 'N25_ORIGINAL_BYTES_RECOVERY_V1', 'Original recovery manifest schema')
            rows = manifest['files']
            self.rows = {r['member']: r for r in rows}
            need(len(self.rows) == len(rows) == spec['manifest_payload_files']
                 and names == set(self.rows) | {'AUDIT_MANIFEST.json'}, 'Exact recovery member set')
            total = 0
            for member, row in self.rows.items():
                need(type(row['bytes']) is int and row['bytes'] >= 0
                     and self._zip.getinfo(member).file_size == row['bytes'], 'Exact member size')
                with self._zip.open(member) as source:
                    observed_size, observed_sha = _stream_hash(source)
                need(observed_size == row['bytes'] and observed_sha == row['sha256'],
                     'Recovery member bytes and CRC: '+member)
                total += observed_size
            self.report = dict(schema='N25_RECOVERY_ASSET_READBACK_V1',
                               archive_sha256=pin, source_plan_sha256=PLAN_SHA256,
                               payload_files=len(rows), payload_bytes=total,
                               arithmetic_accepted=False, full66_complete=False)
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, *_):
        if self._zip is not None:
            self._zip.close()
            self._zip = None
        if self._file is not None:
            self._file.close()
            self._file = None
        self.rows = None

    def read(self, member, binding):
        need(self._zip is not None and self.rows is not None and self.report is not None,
             'Open fully verified recovery archive required')
        _safe_name(member)
        raw = self._zip.read(member)
        need(len(raw) == binding['bytes'] and sha(raw) == binding['sha256'],
             'Rechecked selected original bytes: '+member)
        return raw


def verify_archive(archive=DEFAULT_ARCHIVE):
    with RecoveryArchive(archive) as asset:
        return deepcopy(asset.report)


def _matches(path, binding):
    base._no_link_ancestors(path)
    raw = base._regular(path, MAX_MEMBER)
    need(len(raw) == binding['bytes'] and sha(raw) == binding['sha256'],
         'Exact original member: '+Path(path).name)
    return raw


def verify(target, capsule, *, outputs=False):
    spec = profile(target)
    capsule = Path(capsule)
    base._no_link_ancestors(capsule)
    need(capsule.is_dir(), 'Regular original source capsule')
    required = set(spec['files'])
    candidate = spec.get('candidate')
    if candidate:
        required.add(candidate['filename'])
    allowed = {f"COUNT{spec['index']}_ACCEPTED.json"} if outputs and candidate else set()
    actual = {p.name for p in capsule.iterdir()}
    need(required <= actual <= required | allowed, 'Exact original closure; no historical receipt in execution inputs')
    payload = {name: _matches(capsule/base._flat(name), row) for name, row in spec['files'].items()}
    frozen = parsed(payload['FROZEN_DESIGN.json'])
    need(set(frozen) == {'files'} and frozen['files'] ==
         {name: sha(raw) for name, raw in payload.items() if name != 'FROZEN_DESIGN.json'},
         'Entire unchanged original frozen design')
    kernel = parsed(payload['KERNEL_COPY_MANIFEST.json'])['files']
    need(all(name in payload and sha(payload[name]) == pin for name, pin in kernel.items()),
         'Entire unchanged original kernel closure')
    if candidate:
        _matches(capsule/candidate['filename'], candidate)
    for name in actual-required:
        base._regular(capsule/name, 4*MIB)
    return spec


def native_header(target, capsule):
    spec = verify(target, capsule, outputs=True)
    profile(target, ordinary=True)
    return deepcopy(spec['native_header'])


def geometry(target, capsule, packet=None):
    """Pure full closed-tree readback, NOT a re-evaluation of stored leaf results."""
    spec = verify(target, capsule, outputs=True)
    profile(target, ordinary=True)
    if packet is None:
        packet = parsed(_matches(Path(capsule)/spec['candidate']['filename'], spec['candidate']))
    header = spec['native_header']
    need(type(packet) is dict and set(packet) == set(header)|{'roots'}
         and all(base._same(packet[k], v) for k, v in header.items()), 'Exact unchanged original forest header')
    cfg = parsed(base._regular(Path(capsule)/'contract.json'))['rows'][0]
    roots = packet['roots']
    need(type(roots) is list and len(roots) == 26, 'All 26 closed count roots')
    box = [list(map(Fraction, cfg['p'])), [Fraction(0), Fraction(cfg['Lambda'])],
           [Fraction(0), Fraction(1)], [Fraction(-1, 2), Fraction(1, 2)],
           [Fraction(0), Fraction(cfg['d0'])]]
    nodes = leaves = splits = maximum_depth = 0
    maximum_score = Fraction(0)
    statuses = {}
    for k, root in enumerate(roots):
        need(type(root) is dict and set(root) == {'k', 'tree'}
             and type(root['k']) is int and root['k'] == k, 'Ordered literal count roots')
        stack = [(root['tree'], box, 0)]
        while stack:
            node, current, depth = stack.pop()
            nodes += 1
            maximum_depth = max(maximum_depth, depth)
            need(nodes <= NODE_LIMIT and depth <= DEPTH_LIMIT and type(node) is dict,
                 'Original 10000-node / 128-depth replay budget')
            if node.get('kind') == 'leaf':
                need(set(node) == {'kind', 'box', 'decision', 'result'}
                     and base._same(node['box'], [[str(x) for x in pair] for pair in current])
                     and type(node['decision']) is str and type(node['result']) is dict,
                     'Exact reconstructed original closed leaf, with untrusted arithmetic')
                leaves += 1
                statuses[node['decision']] = statuses.get(node['decision'], 0)+1
                if node['decision'] == 'PASS_TARGET':
                    need(type(node['result'].get('score_upper')) is str, 'Rational saved score text')
                    maximum_score = max(maximum_score, Fraction(node['result']['score_upper']))
            else:
                need(node.get('kind') == 'split' and set(node) == {'kind','axis','cut','left','right'}
                     and type(node['axis']) is int and 0 <= node['axis'] < 5
                     and type(node['cut']) is str, 'Complete literal binary split')
                axis, cut = node['axis'], Fraction(node['cut'])
                need(current[axis][0] < cut < current[axis][1], 'Strict interior rational cut')
                lo, hi = deepcopy(current), deepcopy(current)
                lo[axis][1] = hi[axis][0] = cut
                stack.extend(((node['left'], lo, depth+1), (node['right'], hi, depth+1)))
                splits += 1
    need(nodes == 2*leaves-26 and leaves == spec['leaf_count'], 'Complete original forest census')
    result = dict(roots=26, nodes=nodes, leaves=leaves, pending=0, splits=splits,
                  maximum_depth=maximum_depth, closed_statuses=statuses,
                  maximum_score=str(maximum_score), arithmetic_accepted=False)
    need(base._same({k: result[k] for k in spec['historical_statistics']}, spec['historical_statistics']),
         'Stored structural statistics agree with the pinned original candidate')
    return result


def _prepare(asset, target, destination):
    spec = profile(target)
    target = spec['target']
    destination = Path(destination).absolute()
    base._no_link_ancestors(destination)
    need(not destination.exists(), 'Exclusive new recovered-source task; never overwrite cache')
    destination.mkdir(parents=True, exist_ok=False)
    capsule = destination/'capsule'
    capsule.mkdir()
    for name, row in spec['files'].items():
        (capsule/base._flat(name)).write_bytes(asset.read(spec['member_prefix']+name, row))
    if 'candidate' in spec:
        row = spec['candidate']
        (capsule/row['filename']).write_bytes(asset.read(spec['member_prefix']+row['filename'], row))
        historical = spec['historical_receipt']
        provenance = destination/'provenance'
        provenance.mkdir()
        (provenance/historical['filename']).write_bytes(
            asset.read(spec['member_prefix']+historical['filename'], historical))
    verify(target, capsule)
    census = geometry(target, capsule) if 'candidate' in spec else None
    record = dict(schema=SOURCE_SCHEMA, target=target, source_plan_sha256=PLAN_SHA256,
                  archive_sha256=ARCHIVE_SHA256, candidate_sha256=spec.get('candidate', {}).get('sha256'),
                  census=census, discovery_required=False, source_bytes_modified=False,
                  arithmetic_accepted=False, parent_acquisitions_verified=False,
                  mixed_exclusion_verified=False, full66_complete=False)
    (destination/'RECOVERY_INPUTS.json').write_bytes(encoded(record))
    return record


def prepare(target, destination, *, archive=DEFAULT_ARCHIVE):
    with RecoveryArchive(archive) as asset:
        return _prepare(asset, target, destination)


def verify_preparation(target, task):
    spec = verify(target, Path(task)/'capsule')
    row = parsed(base._regular(Path(task)/'RECOVERY_INPUTS.json'))
    expected = dict(schema=SOURCE_SCHEMA, target=spec['target'], source_plan_sha256=PLAN_SHA256,
                    archive_sha256=ARCHIVE_SHA256, candidate_sha256=spec.get('candidate', {}).get('sha256'),
                    census=geometry(target, Path(task)/'capsule') if 'candidate' in spec else None,
                    discovery_required=False, source_bytes_modified=False, arithmetic_accepted=False,
                    parent_acquisitions_verified=False, mixed_exclusion_verified=False, full66_complete=False)
    need(base._same(row, expected), 'Complete source-only preparation readback')
    if 'historical_receipt' in spec:
        _matches(Path(task)/'provenance'/spec['historical_receipt']['filename'], spec['historical_receipt'])
    return row


def prepare_all(destination, *, archive=DEFAULT_ARCHIVE):
    """Prepare all 13 originals and pinned regional references; no mathematical run."""
    destination = Path(destination).absolute()
    base._no_link_ancestors(destination)
    need(not destination.exists(), 'New recovery workspace only')
    with RecoveryArchive(archive) as asset:
        destination.mkdir(parents=True, exist_ok=False)
        records = [_prepare(asset, t, destination/t) for t in targets(include_mixed=True)]
        for member, row in _plan()['references'].items():
            output = destination/'references'/Path(*_safe_name(member).parts)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(asset.read(member, row))
        result = dict(schema='N25_RECOVERED_ALL_INPUTS_V1', asset=asset.report,
                      targets=records, full66_complete=False, arithmetic_accepted=False)
        (destination/'RECOVERY_PREPARATION.json').write_bytes(encoded(result))
        return result
