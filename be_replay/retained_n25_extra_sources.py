"""Explicit new source seals for 115 established extra n25 count candidates.

No numerical module is imported. Stale/absent historical FROZEN_DESIGN objects
are provenance only; the native checker, actual kernel manifest, contract and
candidate remain unchanged and are separately bound by the new replay epoch.
"""
from __future__ import annotations
import ast
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
import stat
import zipfile

from . import count_task as common, retained_n25_sources as base

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PINS = {
    'n25_retained_b34_catalog.json': '38fdf0a66ea6dbdea196c146d2cf4955e75996db0a4f1e43a269756ad4201b7a',
    'n25_retained_b5_upper_catalog.json': 'd1c44334914f780ce80427915a19bb7ed1f6cf5b89579deba7aa497ae4f4d792',
}
EXPECTED_COUNTS = {'b3': 17, 'b4': 30, 'lower-b5': 39, 'middle-b4': 16,
                   'middle-b5': 7, 'upper-high-beta3': 6}
EXPECTED_LEAVES = {'b3': 37128, 'b4': 60270, 'lower-b5': 48947,
                   'middle-b4': 25257, 'middle-b5': 2446, 'upper-high-beta3': 4246}
MANIFEST, PREPARATION, EPOCH = 'SOURCES.json', 'SOURCE_PREPARATION.json', 'EXTRA_SOURCE_EPOCH.json'
MIB, MAX_SOURCE, MAX_FOREST, MAX_TOTAL = base.MIB, base.MAX_SOURCE, base.MAX_FOREST, base.MAX_TOTAL
EXECUTION_CONTRACT = 'NEW_SEALED_LINUX_EXTRA_REPLAY_NO_HISTORICAL_DESIGN_OR_GUARD_CLAIM'
need, sha, encoded = base.need, base.sha, base.encoded
_link, _regular, _json, _flat, _member = base._link, base._regular, base._json, base._flat, base._member
CATALOG_SHA256 = sha(encoded(CATALOG_PINS))


def catalogs():
    result = {}
    for name, pin in CATALOG_PINS.items():
        raw = _regular(ROOT/'proof'/name, 16*MIB)
        need(sha(raw) == pin, 'Externally pinned established extra-count selection catalog')
        result[name] = _json(raw)
    return result


def _raw_rows():
    values = catalogs()
    b34, upper = values['n25_retained_b34_catalog.json'], values['n25_retained_b5_upper_catalog.json']
    need(b34['schema'] == 'N25_RETAINED_B34_COUNT_CATALOG_V1'
         and upper['schema'] == 'N25_RETAINED_B5_UPPER_SOURCE_CATALOG_V1', 'Fixed extra catalog schemas')
    rows = [j for j in b34['jobs'] if j['selection_evidence_status'] == 'REGIONAL_OUTCOME_MATCHED']
    rows += [j for j in upper['count_jobs'] if j['branch'] in EXPECTED_COUNTS
             and j.get('availability') == 'NATIVE_RUNTIME_CLOSURE_AND_FOREST_PRESENT'
             and j['selection_status'] in ('EXACT_FINAL_OUTCOME_SELECTED',
                 'EXACT_SIX_COUNT_COLLECTION_SELECTED_FINAL_COMPOSER_READS_COLLECTION')]
    need(Counter(j['branch'] for j in rows) == EXPECTED_COUNTS, 'Exactly six established selected batches')
    need(len({j['target_id'] for j in rows}) == 115, 'Unique fixed extra count identities')
    return rows


def _normalize(row):
    b34 = 'source_file_rows' in row
    stats = row['census'] if b34 else row['structural_census']
    files = []
    for r in row['source_file_rows' if b34 else 'source_filerows']:
        if not b34 and not r['present']:
            need(not r.get('native_runtime_required'), 'No missing native runtime dependency')
            continue
        files.append(dict(filename=r['name'] if b34 else r['filename'],
            member=r['archive_member'] if b34 else r['member'], bytes=r['bytes'],
            sha256=r['sha256'] if b34 else r['actual_sha256']))
    pins = {r['filename']: r['sha256'] for r in files}
    identity = row['target_id']
    need(type(identity) is str and re.fullmatch('[a-z0-9][a-z0-9_-]{1,159}', identity)
         and row['archive_key'] == 'old' and type(row['n']) is int and row['n'] == 25,
         'Safe fixed actual-n25 extra job')
    result = dict(branch=row['branch'], target_id=identity, job_id=identity,
        capsule_relative='capsules/'+identity, archive_key='old',
        capsule_member_prefix=row['capsule_member_prefix'].rstrip('/')+'/',
        index=row['index'], n=25, forest_filename=row['forest_filename'],
        acceptance_filename=row['acceptance_filename'], manifest_filename=row['manifest_filename'],
        manifest_sha256=pins[row['manifest_filename']], contract_sha256=row['contract_sha256'],
        checker_sha256=row['checker_sha256'], forest_sha256=row['forest_sha256'],
        p_interval=row['p_interval'], rho_interval=row['rho_interval'],
        beta_interval=row.get('beta_interval'), node_count=stats['nodes'], leaf_count=stats['leaves'],
        split_count=stats['nodes']-stats['leaves'], expected_selected_leaves=stats['leaves'],
        source_file_rows=files, historical_design_issues=row.get('historical_design_provenance_issues', []),
        selection_evidence=row.get('selection_evidence', dict(member=row.get('selection_member'),
            status=row.get('selection_status'))), original_design_acceptance_claimed=False)
    need(result['forest_filename'] == f"COUNT{row['index']}_FOREST.json"
         and result['acceptance_filename'] == f"COUNT{row['index']}_ACCEPTED.json",
         'Original literal count input/output names')
    return result


def jobs(branch):
    need(type(branch) is str and branch in EXPECTED_COUNTS, 'One of six fixed extra count batches')
    rows = [_normalize(r) for r in _raw_rows() if r['branch'] == branch]
    need(len(rows) == EXPECTED_COUNTS[branch] and sum(r['leaf_count'] for r in rows) == EXPECTED_LEAVES[branch],
         'Exact selected extra forest/leaf census')
    return rows


def not_ready():
    values = catalogs()
    b34, upper = values['n25_retained_b34_catalog.json'], values['n25_retained_b5_upper_catalog.json']
    rows = [dict(target_id=j['target_id'], reason='Provisional regional selection; excluded')
            for j in b34['jobs'] if j['selection_evidence_status'] != 'REGIONAL_OUTCOME_MATCHED']
    rows += [dict(target_id=j['target_id'], reason='Exact selected source/candidate capsule missing')
             for j in upper['count_jobs'] if j.get('availability') == 'EXACT_SELECTED_CAPSULE_NOT_FOUND']
    rows += [dict(target_id=j['target_id'], reason='Upper transitive final selection unresolved; excluded')
             for j in upper['count_jobs'] if j['branch'] == 'upper-retained-graph']
    rows += [dict(target_id=j['target_id'], reason='Mixed theorem/resource registry and original V14 parent unresolved')
             for j in upper['mixed_selected_components']]
    need(len(rows) == 24, 'Exactly1provisional+11missing+10unresolved+2mixed excluded records')
    return dict(schema='RETAINED_N25_EXTRA_NOT_READY_V1', excluded=rows,
                fresh_arithmetic_replayed=False, full_n25_verified=False, all_index_conclusion_verified=False)


def _selected(job):
    selected = [j for j in jobs(job.get('branch')) if j['job_id'] == job.get('job_id')]
    need(len(selected) == 1 and encoded(job) == encoded(selected[0]), 'Exact immutable selected extra job')
    return selected[0]


def _selection(job, manifest_raw):
    need(sha(manifest_raw) == job['manifest_sha256'], 'Actual original kernel-manifest bytes')
    kernel = _json(manifest_raw)['files']
    need(type(kernel) is dict and 1 <= len(kernel) <= 256, 'Complete bounded actual native kernel map')
    supplied = {r['filename']: r for r in job['source_file_rows']}
    need(len(supplied) == len(job['source_file_rows']), 'Unique catalog source rows')
    names = set(kernel)|{'count_protocol.py', 'contract.json', job['manifest_filename']}
    if 'FROZEN_DESIGN.json' in supplied:
        names.add('FROZEN_DESIGN.json')  # Untouched provenance, not the new seal.
    expected = {}
    for name in names:
        _flat(name)
        need(name in supplied and name != job['acceptance_filename']
             and re.search(r'COUNT[0-9]+_(?:ACCEPTED|FOREST)\.json', name) is None,
             'Declared runtime source, no historical numerical acceptance/forest input')
        row = supplied[name]
        need(row['member'] == job['capsule_member_prefix']+name, 'Exact source capsule member')
        if name in kernel:
            need(kernel[name] == row['sha256'], 'Actual kernel map equals selected source bytes')
        expected[name] = dict(row, role='historical_design_provenance' if name == 'FROZEN_DESIGN.json' else 'source')
    need(expected['count_protocol.py']['sha256'] == job['checker_sha256']
         and expected['contract.json']['sha256'] == job['contract_sha256'], 'Exact selected checker/contract')
    expected[job['forest_filename']] = dict(filename=job['forest_filename'],
        member=job['capsule_member_prefix']+job['forest_filename'], sha256=job['forest_sha256'],
        bytes=None, role='candidate')
    return expected, kernel


def _epoch(job, expected):
    return dict(schema='RETAINED_N25_EXTRA_SOURCE_EPOCH_V1', job_id=job['job_id'],
        catalog_sha256=CATALOG_SHA256, catalog_pins=CATALOG_PINS,
        files_sha256={n: r['sha256'] for n, r in sorted(expected.items())},
        historical_design_issues=job['historical_design_issues'],
        original_design_acceptance_claimed=False, mathematical_source_bytes_changed=False,
        historical_acceptance_used=False, fresh_arithmetic_replayed=False,
        execution_contract=EXECUTION_CONTRACT, full_n25_verified=False, all_index_conclusion_verified=False)


def _capsule(job, capsule):
    capsule = Path(capsule)
    need(capsule.is_dir() and not _link(capsule), 'Regular extra source capsule')
    expected, kernel = _selection(job, _regular(capsule/job['manifest_filename'], MAX_SOURCE))
    wanted = set(expected)|{EPOCH}
    need(all(p.is_file() and not _link(p) for p in capsule.iterdir())
         and wanted <= {p.name for p in capsule.iterdir()} <= wanted|{job['acceptance_filename']},
         'Exact new source/candidate seal; no unbound helper, directory or receipt')
    rows = []
    for name, row in sorted(expected.items()):
        raw = _regular(capsule/name, MAX_FOREST if row['role'] == 'candidate' else MAX_SOURCE)
        need(sha(raw) == row['sha256'] and (row['bytes'] is None or len(raw) == row['bytes']),
             'Exact extra source/candidate bytes: '+name)
        rows.append(dict(row, bytes=len(raw)))
    epoch_raw = encoded(_epoch(job, expected))
    need(_regular(capsule/EPOCH, MAX_SOURCE) == epoch_raw, 'Explicit new Linux seal, never stale design acceptance')
    rows.append(dict(filename=EPOCH, member=None, bytes=len(epoch_raw), sha256=sha(epoch_raw), role='new_source_epoch'))
    return rows, kernel


def census(job, capsule):
    job = _selected(job)
    _, kernel = _capsule(job, capsule)
    # Reuse only the existing pure AST/JSON geometry checker. The schema is
    # read from the already byte-pinned original checker, never evaluated.
    tree = ast.parse(_regular(Path(capsule)/'count_protocol.py', MAX_SOURCE))
    header = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'header')
    call = header.body[0].value
    literal = next(k.value for k in call.keywords if k.arg == 'schema')
    return base._structure(dict(job, forest_schema=ast.literal_eval(literal)), capsule, kernel)


def _manifest(branch, task):
    selected = jobs(branch)
    directory = Path(task)/'capsules'
    need(directory.is_dir() and not _link(directory)
         and {p.name for p in directory.iterdir()} == {j['job_id'] for j in selected}, 'Exactly selected extra capsules')
    rows = []
    for job in selected:
        capsule = Path(task)/job['capsule_relative']
        files, _ = _capsule(job, capsule)
        census(job, capsule)
        rows.append(dict(job_id=job['job_id'], target_id=job['target_id'], index=job['index'],
            capsule_relative=job['capsule_relative'], forest_filename=job['forest_filename'],
            acceptance_filename=job['acceptance_filename'], source_design_sha256=common.digest(capsule/EPOCH),
            contract_sha256=job['contract_sha256'], checker_sha256=job['checker_sha256'],
            kernel_manifest_sha256=job['manifest_sha256'], forest_sha256=job['forest_sha256'], files=files))
    return dict(schema='RETAINED_N25_EXTRA_SOURCES_V1', branch=branch, catalog_sha256=CATALOG_SHA256,
        catalog_pins=CATALOG_PINS, archive_asset=deepcopy(common.ASSETS['old']), jobs=rows,
        geometry_helper_sha256=common.digest(base.__file__), execution_contract=EXECUTION_CONTRACT,
        original_design_acceptance_claimed=False, source_algorithms_changed=False,
        historical_acceptance_used=False, fresh_arithmetic_replayed=False,
        parent_acquisitions_verified=False, full_n25_verified=False, all_index_conclusion_verified=False)


def prepare(branch, archive, output):
    selected = jobs(branch)
    common.verify_asset(Path(archive), common.ASSETS['old'])
    output = Path(output).absolute()
    need(not output.exists() and not _link(output) and all(not _link(p) for p in output.parents if p.exists()),
         'Fresh unlinked extra source task')
    with zipfile.ZipFile(archive) as zipped:
        index = {}
        for info in zipped.infolist():
            index.setdefault(info.filename.casefold(), []).append(info)
        def read(name, limit):
            _member(name)
            entries = index.get(name.casefold(), [])
            need(len(entries) == 1 and entries[0].filename == name, 'Unique exact-case selected archive member')
            info = entries[0]
            mode = info.external_attr >> 16
            need(not info.is_dir() and not info.flag_bits & 1 and not stat.S_ISLNK(mode)
                 and stat.S_IFMT(mode) in (0, stat.S_IFREG) and 0 <= info.file_size <= limit,
                 'Bounded regular unencrypted selected member')
            return zipped.read(info)
        total = 0
        for job in selected:
            expected, _ = _selection(job, read(job['capsule_member_prefix']+job['manifest_filename'], MAX_SOURCE))
            capsule = output/job['capsule_relative']
            capsule.mkdir(parents=True, exist_ok=False)
            for name, row in sorted(expected.items()):
                raw = read(row['member'], MAX_FOREST if row['role'] == 'candidate' else MAX_SOURCE)
                total += len(raw)
                need(total <= MAX_TOTAL and sha(raw) == row['sha256']
                     and (row['bytes'] is None or len(raw) == row['bytes']), 'Exact bounded selected source bytes')
                (capsule/name).write_bytes(raw)
            (capsule/EPOCH).write_bytes(encoded(_epoch(job, expected)))
    manifest = _manifest(branch, output)
    (output/MANIFEST).write_bytes(encoded(manifest))
    report = dict(schema='RETAINED_N25_EXTRA_PREPARATION_V1', branch=branch,
        source_manifest_sha256=sha(encoded(manifest)), source_helper_sha256=common.digest(__file__),
        selected_jobs=len(selected), selected_leaves=sum(j['leaf_count'] for j in selected),
        archive_verified=True, fresh_arithmetic_replayed=False, historical_acceptance_used=False,
        original_design_acceptance_claimed=False, full_n25_verified=False, all_index_conclusion_verified=False)
    (output/PREPARATION).write_bytes(encoded(report))
    (output/'NOT_READY.json').write_bytes(encoded(not_ready()))
    return manifest


def verify(task):
    task = Path(task)
    need(task.is_dir() and not _link(task), 'Regular extra source task')
    raw = _regular(task/MANIFEST, 16*MIB)
    saved = _json(raw)
    actual = _manifest(saved['branch'], task)
    need(raw == encoded(actual), 'Exact immutable extra source manifest')
    expected = dict(schema='RETAINED_N25_EXTRA_PREPARATION_V1', branch=saved['branch'],
        source_manifest_sha256=sha(raw), source_helper_sha256=common.digest(__file__),
        selected_jobs=len(actual['jobs']), selected_leaves=EXPECTED_LEAVES[saved['branch']],
        archive_verified=True, fresh_arithmetic_replayed=False, historical_acceptance_used=False,
        original_design_acceptance_claimed=False, full_n25_verified=False, all_index_conclusion_verified=False)
    need(_regular(task/PREPARATION, MIB) == encoded(expected), 'Exact source-only extra preparation evidence')
    need(_regular(task/'NOT_READY.json', MIB) == encoded(not_ready()), 'Explicit excluded/missing selection record')
    return actual
