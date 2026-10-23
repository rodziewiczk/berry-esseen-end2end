"""Exact source-only selection for middle n25 B4/B5 parent and local actions."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
from . import aux24_sources as source,count_task as common

ROOT=Path(__file__).resolve().parents[1]
CATALOG='proof/middle_n25_acquisition_sources.json'
CATALOG_SHA='8c2c518bd044dd53ca2d5974d06bfb3ed04b3b1fa641490a1533cdfb6042d278'
MIB=1024**2


def need(ok,message):
    if not ok:raise ValueError(message)


def definition(branch):
    need(branch in('b4','b5'),'One exact selected middle branch')
    need(common.digest(ROOT/CATALOG)==CATALOG_SHA,'Independent complete middle source catalog')
    packet=common.read(ROOT/CATALOG,16*MIB)
    need(packet['schema']=='MIDDLE_N25_ACQUISITION_SOURCE_CATALOG_V1'and packet['mathematical_code_executed']is False
         and packet['historical_acceptances_imported_as_inputs']==0 and packet['all_index_conclusion_verified']is False,
         'Exact conditional source-only selection')
    rows=[r for r in packet['branches']if r['branch']==branch]
    need(len(rows)==1,'Unique selected branch')
    return rows[0]


def selected(branch):
    packet=definition(branch);rows={}
    def add(row,kind):
        name=row['member'];source._kind(name,kind)
        value=dict(sha256=row['sha256'],bytes=row['bytes'],kind=kind)
        need(name not in rows or rows[name]==value,'Consistent exact source/parent identity')
        rows[name]=value
    for row in packet['source_file_rows']:
        conditional=row['member'].endswith('.json')and row['role']in(
            'conditional_static_review','fixed_cache_source_or_conditional_review',
            'historical_port_description_not_fresh_parent_evidence')
        add(row,'premise'if conditional else'source')
    add(packet['initial']['proof_candidate'],'candidate')
    for row in packet['initial_candidate_aliases']:add(row,'candidate')
    for local in packet['locals']:add(local['proof_candidate'],'candidate')
    need(len({n.casefold()for n in rows})==len(rows),'Unique portable sealed paths')
    need(not any(PurePosixPath(n).name in('GLOBAL_RESOURCES_PROOF.json','GLOBAL_RESOURCES_ACCEPTED.json')or 'ACCEPTED'in PurePosixPath(n).name for n in rows),
         'No historical global or local accepted output selected')
    return rows


def selection_manifest(branch):
    return dict(schema=source.SCHEMA,archive=source.ARCHIVE,files=selected(branch),
        mathematical_code_executed=False,historical_acceptances_imported=0,premises_acquired=False,all_index_conclusion_verified=False)


def selection_sha(branch):
    raw=json.dumps(selection_manifest(branch),sort_keys=True,indent=2,ensure_ascii=True)+'\n'
    return hashlib.sha256(raw.encode()).hexdigest()


def prepare(task,branch,*,archives,download=False,progress=None):
    rows=selected(branch)
    source.prepare(task,archives=archives,members={n:r['kind']for n,r in rows.items()},download=download,progress=progress)
    verify(task,branch)
    return Path(task)


def verify(task,branch):
    source.verify_prepared(task,expected_manifest_sha=selection_sha(branch))
    packet=common.read(Path(task)/source.MANIFEST,16*MIB)
    need(packet==selection_manifest(branch),'Complete unchanged source/candidate epoch')
    return packet


def stages(branch):
    packet=definition(branch);folder=packet['canonical_directory'].removeprefix(source.PREFIX);band=packet['band']
    result=[dict(name='initial-accept',kind='initial',action='accept',folder=folder,script='initial_middle.py',args=['accept'],
        proof=f'INITIAL_MIDDLE_B{band}_PROOF.json',receipt=f'INITIAL_MIDDLE_B{band}_ACCEPTED.json')]
    for action in('construct','accept'):
        result.append(dict(name='global_resource-'+action,kind='global_resource',action=action,folder=folder,
            script='global_resources.py',args=[action],proof='GLOBAL_RESOURCES_PROOF.json',
            receipt='GLOBAL_RESOURCES_ACCEPTED.json'if action=='accept'else None))
    for row in packet['locals']:
        index=row['index']
        result.append(dict(name=f'local-{index}-accept',kind='local',action='accept',index=index,
            folder=row['directory'].removeprefix(source.PREFIX),script='acquire_panel_memoized.py',args=['accept',str(index)],
            proof=f'PANEL{index}_PROOF.json',receipt=f'PANEL{index}_ACCEPTED.json'))
    need(len(result)==packet['selected_full_actions'],'Every exact selected complete action')
    return result
