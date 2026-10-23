"""Build the selected high-beta3 source catalog; no mathematical imports."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SHA='17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb'
SIZE=514958998
PREFIX='cutoff25_20261011/'
C=PREFIX+'continuation_20261011/high25_beta3_exact'
L=PREFIX+'continuation_20261011/high25_beta3_cached_exact_v1'
H=PREFIX+'continuation_20261011/high25_transfers/stage_cache_v2'

def sha(raw):return hashlib.sha256(raw).hexdigest()
def digest(path):
    h=hashlib.sha256()
    with path.open('rb')as stream:
        for block in iter(lambda:stream.read(1024**2),b''):h.update(block)
    return h.hexdigest()
def need(ok,message):
    if not ok:raise ValueError(message)

def build(archive,output):
    need(archive.stat().st_size==SIZE and digest(archive)==SHA,'Exact original archive')
    with zipfile.ZipFile(archive)as z:
        def row(name,role):
            raw=z.read(name)
            return dict(member=name,bytes=len(raw),sha256=sha(raw),role=role)
        def read(name):return json.loads(z.read(name))
        selector=PREFIX+'continuation_20261011/N25_REDUCTION_AFTER_HIGH_RHO_AND_MIDDLE_BETA048.json'
        joined=L+'/HIGH25_BETA3_JOINED.json'
        union,selection=read(selector),read(joined)
        need(union['files_sha256'][joined.removeprefix(PREFIX)]==sha(z.read(joined)),'Final upper selector binds selected composition')
        originals=[17,18,19,20,21];cached=[16,22,23,24,25,26]
        need(selection['original_local_source_panels']==originals and selection['cached_local_source_panels']==cached
             and selection['global_survivors']==list(range(16,27)),'Exact final selected local partition')
        files={}
        def add(name,role,pin=None):
            value=row(name,role);need(pin is None or value['sha256']==pin,'Actual source manifest byte identity '+name)
            need(name not in files or files[name]['sha256']==value['sha256'],'Stable selected dependency')
            files[name]=value
        frozen=read(C+'/FROZEN_ALL_PROTOCOLS.json')
        for name,pin in frozen.items():
            add(C+'/'+name,'conditional_static_review'if name.endswith('.json')else'unchanged_original_source',pin)
        add(C+'/FROZEN_ALL_PROTOCOLS.json','original_source_manifest_provenance')
        for mf in ['COPY_MANIFEST.json','PANEL_COPY_MANIFEST.json','resource_exact/COPY_MANIFEST.json']:
            parent=C+'/'+mf.rsplit('/',1)[0]if'/'in mf else C
            for name,pin in read(C+'/'+mf)['files'].items():
                need(sha(z.read(parent+'/'+name))==pin,'Full transitive original source closure')
                if parent+'/'+name not in files:add(parent+'/'+name,'unchanged_original_source',pin)
        for name in ['cached_protocol.py','acquire_panel_cached.py']:add(L+'/'+name,'unchanged_original_cache_source')
        for name in ['exact_stage_cache.py','INDEPENDENT_REVIEW.json','EXACT_STAGE_CACHE_PROOF.txt']:
            add(H+'/'+name,'conditional_static_review'if name.endswith('.json')else'unchanged_original_cache_source')
        add(L+'/FROZEN_SOURCES.json','historical_cache_manifest_provenance_only')
        initial=read(C+'/INITIAL_BETA3_PROOF.json');ia=read(C+'/INITIAL_BETA3_ACCEPTED.json')
        glob=read(C+'/GLOBAL_RESOURCES_PROOF.json');ga=read(C+'/GLOBAL_RESOURCES_ACCEPTED.json')
        need(ia['status']=='PASS_FRESH_EXACT_HIGH25_BETA3_INITIAL'and len(initial['stages'])==11
             and ia['signed_rectangles']==12*9216 and len(ia['negative_controls'])==12,'Exact INITIAL reference schema')
        need(glob['initial_acceptance_sha256']==sha(z.read(C+'/INITIAL_BETA3_ACCEPTED.json'))
             and len(glob['rows'])==100 and ga['survivors']==list(range(16,27)),'Global reference complete parent chain')
        need(initial['profile']==glob['profile'],'Same original profile')
        locals_=[]
        for index in range(16,27):
            folder=L if index in cached else C
            proof=read(folder+f'/PANEL{index}_PROOF.json');receipt=read(folder+f'/PANEL{index}_ACCEPTED.json')
            need(selection['files_sha256'][folder.removeprefix(PREFIX)+f'/PANEL{index}_PROOF.json']==sha(z.read(folder+f'/PANEL{index}_PROOF.json')),'Actual final selected local candidate')
            need(proof['initial_proof_sha256']==sha(z.read(C+'/INITIAL_BETA3_PROOF.json'))
                 and proof['global_resource']==glob['rows'][index]and proof['cycle_limit']==8
                 and proof['initial_covers_per_cycle']==4 and proof['profile']==initial['profile']
                 and proof['source_sha256']==read(C+'/PANEL_COPY_MANIFEST.json')['files'],'Local candidate original interfaces')
            need(receipt['status']=='PASS_FRESH_EXACT_HIGH25_BETA3_PANEL_ACQUISITION'
                 and receipt['checker_sha256']==sha(z.read(C+'/acquire_panel.py'))and len(receipt['negative_controls'])==15,'Original full local checker and controls')
            locals_.append(dict(index=index,directory=folder,cached=index in cached,
                proof_candidate=row(folder+f'/PANEL{index}_PROOF.json','untrusted_full_object_candidate'),
                expected_status=receipt['status'],negative_controls=receipt['negative_controls'],
                cycle_limit=8,cycles=len(proof['cycles']),excluded=proof['excluded'],
                mathematical_cover_calls=sum(len(c['stages'])for c in proof['cycles'])))
        need(sum(r['mathematical_cover_calls']for r in locals_)==241,'Exact selected local cover census')
        result=dict(schema='HIGH_BETA3_ACQUISITION_SOURCE_CATALOG_V1',date='2026-10-23',
            archive=dict(name='cutoff25_20261011.zip',bytes=SIZE,sha256=SHA),branch='high-beta3',
            selector=row(selector,'final_upper_selector_provenance'),selected_composition=row(joined,'selected_regional_composition_provenance'),
            canonical_directory=C,cache_directory=L,cache_helper_directory=H,profile=initial['profile'],
            contact_allowance=initial['contact_allowance'],rho_interval=['7/4','459061/250000'],beta_interval=['14/25','640471/1000000'],
            initial=dict(proof_candidate=row(C+'/INITIAL_BETA3_PROOF.json','untrusted_full_object_candidate'),
                expected_status=ia['status'],negative_controls=ia['negative_controls']),
            global_resource=dict(expected_status=ga['status'],negative_controls=ga['negative_controls'],survivors=ga['survivors']),
            locals=locals_,source_file_rows=sorted(files.values(),key=lambda r:r['member']),
            selected_full_actions=14,global_signed_covers=12,local_signed_covers=241,
            source_epoch='EXPLICIT_SOURCE_ONLY_CACHE_PROJECTION_WITH_FRESH_PARENT_SNAPSHOTS_V1',
            mathematical_code_executed=False,historical_acceptances_imported_as_inputs=0,
            global_sharp24_required=False,resource_interfaces_verified=False,full_n25_verified=False,all_index_conclusion_verified=False)
    raw=json.dumps(result,sort_keys=True,indent=2)+'\n'
    need(not output.exists()or output.read_text()==raw,'Never overwrite a different frozen catalog')
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(raw.encode('utf-8'))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive',type=Path)
    p.add_argument('--output',type=Path,default=ROOT/'proof/high_beta3_acquisition_sources.json');a=p.parse_args()
    result=build(a.archive,a.output);print('SOURCE_ONLY',len(result['source_file_rows']),'sources',result['selected_full_actions'],'actions',digest(a.output))
