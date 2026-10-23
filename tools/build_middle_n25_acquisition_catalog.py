"""Catalog exact selected middle-B4/B5 acquisitions using source/AST/JSON only."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE_SHA="17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb"
ARCHIVE_BYTES=514958998
PREFIX="cutoff25_20261011/"


def sha(raw):return hashlib.sha256(raw).hexdigest()


def digest(path):
    h=hashlib.sha256()
    with path.open('rb')as stream:
        for block in iter(lambda:stream.read(1024**2),b''):h.update(block)
    return h.hexdigest()


def build(archive,output):
    if archive.stat().st_size!=ARCHIVE_BYTES or digest(archive)!=ARCHIVE_SHA:raise ValueError('Exact cutoff25 source archive')
    result=dict(schema='MIDDLE_N25_ACQUISITION_SOURCE_CATALOG_V1',date='2026-10-23',
        archive=dict(name='cutoff25_20261011.zip',bytes=ARCHIVE_BYTES,sha256=ARCHIVE_SHA),branches=[],
        mathematical_code_executed=False,historical_acceptances_imported_as_inputs=0,
        global_sharp24_required=False,resource_interfaces_verified=False,full_n25_verified=False,all_index_conclusion_verified=False)
    with zipfile.ZipFile(archive)as z:
        def row(name,role):
            raw=z.read(name)
            return dict(member=name,bytes=len(raw),sha256=sha(raw),role=role)
        for band in(4,5):
            canonical=PREFIX+f'new_middle/b{band}_exact_v1'
            selection_name=PREFIX+f'new_middle/B{band}_FINAL_V4_SELECTION.json'
            selection=json.loads(z.read(selection_name))
            ip=canonical+f'/INITIAL_MIDDLE_B{band}_PROOF.json';ia=canonical+f'/INITIAL_MIDDLE_B{band}_ACCEPTED.json'
            gp=canonical+'/GLOBAL_RESOURCES_PROOF.json';ga=canonical+'/GLOBAL_RESOURCES_ACCEPTED.json'
            initial,initial_receipt,glob,global_receipt=[json.loads(z.read(n))for n in(ip,ia,gp,ga)]
            if glob['initial_proof_sha256']!=sha(z.read(ip))or glob['initial_acceptance_sha256']!=sha(z.read(ia)):
                raise ValueError('Original timed global parent edge')
            if len(initial['stages'])!=12 or len(initial['export']['panels'])!=100 or len(glob['rows'])!=100:
                raise ValueError('Every complete global cover/panel')
            branch=dict(branch=f'b{band}',band=band,canonical_directory=canonical,profile=initial['profile'],
                contact_allowance=initial['contact_allowance'],selector=row(selection_name,'final_local_and_count_selection'),
                source_file_rows=[],initial=dict(proof_candidate=row(ip,'untrusted_complete_initial_candidate'),
                    historical_acceptance=row(ia,'output_schema_reference_not_input'),expected_status=initial_receipt['status'],
                    negative_controls=initial_receipt['negative_controls']),
                global_resource=dict(historical_candidate=row(gp,'reference_only_fresh_construction_required'),
                    historical_acceptance=row(ga,'output_schema_reference_not_input'),expected_status=global_receipt['status'],
                    negative_controls=global_receipt['negative_controls'],survivors=global_receipt['survivors'],
                    original_timed_initial_receipt_sha256=glob['initial_acceptance_sha256']),locals=[])
            source_rows={}
            def add(name,role='frozen_source',pin=None):
                r=row(name,role)
                if pin is not None and r['sha256']!=pin:raise ValueError('Actual source pin '+name)
                if name in source_rows and source_rows[name]['sha256']!=r['sha256']:raise ValueError('Source collision')
                source_rows[name]=r
            folders={canonical}|{c['capsule'].removeprefix('work/')for c in selection['locals'].values()}
            for folder in sorted(folders):
                for mf in('COPY_MANIFEST.json','PANEL_COPY_MANIFEST.json','resource_exact/COPY_MANIFEST.json'):
                    add(folder+'/'+mf,'source_manifest')
                    manifest=json.loads(z.read(folder+'/'+mf))['files']
                    manifest_directory=folder+'/'+mf.rsplit('/',1)[0]if '/'in mf else folder
                    for name,pin in manifest.items():
                        role='conditional_static_review'if name.endswith('.json')and('CHECKED'in name or 'REVIEW'in name)else'frozen_source'
                        add(manifest_directory+'/'+name,role,pin)
                add(folder+'/acquire_panel_memoized.py','unchanged_empty_cache_wrapper')
                if folder!=canonical:
                    add(folder+'/TWO_CYCLE_PORT.json','historical_port_description_not_fresh_parent_evidence')
                    if z.read(folder+f'/INITIAL_MIDDLE_B{band}_PROOF.json')!=z.read(ip):raise ValueError('Identical INITIAL proof across aliases')
            for name in('exact_stage_cache.py','INDEPENDENT_REVIEW.json','EXACT_STAGE_CACHE_PROOF.txt'):
                add(PREFIX+'new_middle/stage_cache_v2/'+name,'fixed_cache_source_or_conditional_review')
            for index,choice in selection['locals'].items():
                folder=choice['capsule'].removeprefix('work/');proof_name=folder+f'/PANEL{index}_PROOF.json'
                accepted_name=folder+f'/PANEL{index}_ACCEPTED.json'
                proof,accepted=json.loads(z.read(proof_name)),json.loads(z.read(accepted_name))
                manifest=json.loads(z.read(folder+'/PANEL_COPY_MANIFEST.json'))['files']
                if proof['source_sha256']!=manifest or accepted['source_sha256']!=manifest or proof['initial_proof_sha256']!=sha(z.read(ip)):
                    raise ValueError('Complete exact selected local source/parent binding')
                if accepted['proof_sha256']!=sha(z.read(proof_name))or accepted['checker_sha256']!=sha(z.read(folder+'/acquire_panel.py')):
                    raise ValueError('Selected original local checker/candidate pair')
                branch['locals'].append(dict(index=int(index),directory=folder,cycle_limit=choice['cycle_limit'],
                    proof_candidate=row(proof_name,'untrusted_complete_selected_local_candidate'),
                    historical_acceptance=row(accepted_name,'output_schema_reference_not_input'),
                    expected_status=accepted['status'],negative_controls=accepted['negative_controls'],excluded=proof['excluded'],
                    cycles=len(proof['cycles']),mathematical_cover_calls=sum(len(c['stages'])for c in proof['cycles']),
                    initial_proof_sha256=proof['initial_proof_sha256']))
            branch['source_file_rows']=sorted(source_rows.values(),key=lambda r:r['member'])
            branch['selected_full_actions']=3+len(branch['locals'])
            branch['local_mathematical_cover_calls']=sum(r['mathematical_cover_calls']for r in branch['locals'])
            branch['alias_directories']=sorted(folders-{canonical})
            branch['initial_candidate_aliases']=[row(folder+f'/INITIAL_MIDDLE_B{band}_PROOF.json','unchanged_initial_candidate_alias')for folder in branch['alias_directories']]
            branch['global_resource']['fresh_construct_then_accept_required']=True
            result['branches'].append(branch)
    raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    if output.exists()and output.read_bytes()!=raw:raise ValueError('Existing frozen catalog differs')
    output.parent.mkdir(parents=True,exist_ok=True)
    if not output.exists():output.write_bytes(raw)
    return sha(raw)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--output',type=Path,default=ROOT/'proof/middle_n25_acquisition_sources.json');a=p.parse_args()
    print(build(a.archive,a.output))
