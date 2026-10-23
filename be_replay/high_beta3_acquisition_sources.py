"""Pinned source-only high-beta3 selection and explicit cache metadata epoch.

No original mathematical module is imported. Original source bytes and the
archived manifests remain preserved under task/source. Only the cache's broad
historical transport commitment is projected in the separate execution epoch.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
from . import aux24_sources as source, count_task as common

ROOT=Path(__file__).resolve().parents[1]
CATALOG='proof/high_beta3_acquisition_sources.json'
CATALOG_SHA='741d63a34acb1ccf141f3032316dc800f73080af21898f5bf1ecb1cf3dd07f56'
BRANCH='high-beta3'
MIB=1024**2

def need(ok,message):
    if not ok:raise ValueError(message)

def definition(branch=BRANCH):
    need(branch==BRANCH,'One exact selected high-beta3 branch')
    need(common.digest(ROOT/CATALOG)==CATALOG_SHA,'Exact independent high-beta3 selection')
    p=common.read(ROOT/CATALOG,16*MIB)
    need(p['schema']=='HIGH_BETA3_ACQUISITION_SOURCE_CATALOG_V1'and p['branch']==branch
         and p['mathematical_code_executed']is False and p['historical_acceptances_imported_as_inputs']==0
         and p['all_index_conclusion_verified']is False,'Conditional source-only selection')
    return p

def selected(branch=BRANCH):
    p=definition(branch);rows={}
    def add(r,kind):
        n=r['member'];source._kind(n,kind)
        value=dict(sha256=r['sha256'],bytes=r['bytes'],kind=kind)
        need(n not in rows or rows[n]==value,'Stable selected source identity');rows[n]=value
    for row in p['source_file_rows']:
        add(row,'premise'if row['member'].endswith('.json')and row['role']in(
            'conditional_static_review','historical_cache_manifest_provenance_only')else'source')
    add(p['initial']['proof_candidate'],'candidate')
    for local in p['locals']:add(local['proof_candidate'],'candidate')
    need(len({n.casefold()for n in rows})==len(rows),'Unique portable source paths')
    need(not any('ACCEPTED'in PurePosixPath(n).name or PurePosixPath(n).name=='GLOBAL_RESOURCES_PROOF.json'for n in rows),
         'No historical accepted/global generated output is an input')
    return rows

def selection_manifest(branch=BRANCH):
    return dict(schema=source.SCHEMA,archive=source.ARCHIVE,files=selected(branch),mathematical_code_executed=False,
        historical_acceptances_imported=0,premises_acquired=False,all_index_conclusion_verified=False)
def _raw(p):return (json.dumps(p,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode()
def selection_sha(branch=BRANCH):return hashlib.sha256(_raw(selection_manifest(branch))).hexdigest()
def prepare(task,branch=BRANCH,*,archives,download=False,progress=None):
    source.prepare(task,archives=archives,members={n:r['kind']for n,r in selected(branch).items()},download=download,progress=progress)
    verify(task,branch);return Path(task)
def verify(task,branch=BRANCH):
    source.verify_prepared(task,expected_manifest_sha=selection_sha(branch))
    p=common.read(Path(task)/source.MANIFEST,16*MIB)
    need(p==selection_manifest(branch),'All original source/candidate bytes');return p

def cache_projection(task,branch=BRANCH):
    """Explicit source-only projection, never a claim to the historical seal.

    The original flexible cached_protocol.py checks every listed byte. We retain
    every actual selected original source and cache helper, but do not import
    unrelated old executions/accepted receipts from its 1533-row snapshot.
    """
    p=definition(branch);directory=p['cache_directory'];name=directory+'/FROZEN_SOURCES.json'
    old=common.read(Path(task)/'source'/name,16*MIB)
    need(old['schema']=='NAMED_HIGH_BETA3_EXACT_STAGE_CACHE_V1','Original named cache schema')
    wanted={r['member']:r for r in p['source_file_rows']if r['member']!=name}
    mapping={n.removeprefix(source.PREFIX):r['sha256']for n,r in wanted.items()}
    need(all(old['files_sha256'].get(n)==h for n,h in mapping.items()),'Projection is a literal subset of the original source seal')
    projected=dict(old,files_sha256=mapping,scope='New source-only transport epoch. All selected original source bytes are unchanged; historical receipts and unrelated executions are not imported. Fresh parents are separately bound after full acceptance.')
    raw=_raw(projected)
    descriptor=dict(schema='HIGH_BETA3_CACHE_SOURCE_PROJECTION_V1',original_manifest_sha256=common.digest(Path(task)/'source'/name),
        original_manifest_rows=len(old['files_sha256']),projected_manifest_sha256=hashlib.sha256(raw).hexdigest(),
        projected_source_rows=len(mapping),projected_files_sha256=mapping,
        mathematical_source_changed=False,historical_manifest_acceptance_claimed=False,
        historical_acceptances_imported=0,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    return {name.removeprefix(source.PREFIX):raw,
        directory.removeprefix(source.PREFIX)+'/CACHE_SOURCE_EPOCH.json':_raw(descriptor)}

def initialize_epoch(task,branch=BRANCH):
    verify(task,branch);base=Path(task)/'epoch'/source.PREFIX.rstrip('/')
    need(not base.exists(),'New isolated source/transport execution epoch')
    shutil.copytree(source.source_root(task),base)
    for name,raw in cache_projection(task,branch).items():
        (base/name).write_bytes(raw)
    return base

def epoch_rows(task,branch=BRANCH):
    result={n.removeprefix(source.PREFIX):r for n,r in selected(branch).items()}
    for n,raw in cache_projection(task,branch).items():result[n]=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),kind='explicit_transport_metadata')
    return result

def stages(branch=BRANCH):
    p=definition(branch);folder=p['canonical_directory'].removeprefix(source.PREFIX)
    result=[dict(name='initial-accept',kind='initial',action='accept',folder=folder,script='initial_beta3.py',args=['accept'],proof='INITIAL_BETA3_PROOF.json',receipt='INITIAL_BETA3_ACCEPTED.json')]
    for action in('construct','accept'):
        result.append(dict(name='global_resource-'+action,kind='global_resource',action=action,folder=folder,
            script='global_resources.py',args=[action],proof='GLOBAL_RESOURCES_PROOF.json',receipt='GLOBAL_RESOURCES_ACCEPTED.json'if action=='accept'else None))
    for local in p['locals']:
        index=local['index'];script='acquire_panel_cached.py'if local['cached']else'acquire_panel.py'
        result.append(dict(name=f'local-{index}-accept',kind='local',action='accept',index=index,cached=local['cached'],
            folder=local['directory'].removeprefix(source.PREFIX),script=script,args=['accept',str(index)],
            proof=f'PANEL{index}_PROOF.json',receipt=f'PANEL{index}_ACCEPTED.json'))
    need(len(result)==p['selected_full_actions']==14,'All selected complete original actions');return result
