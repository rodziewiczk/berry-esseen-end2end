"""Exact source-only independent highrho14--19 sublane of package57.

All73 original input bytes, including the original70-row manifest, are kept
unchanged. Historical numeric/capture inputs are conditional provenance, never
newly acquired results. No original mathematical module is imported here.
"""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import time
import urllib.request
import zipfile
from . import finite1039_sources as base

ROOT,MIB=base.ROOT,base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
PLAN=ROOT/'proof/finite1519_highrho_source_plan.json'
PLAN_SHA256='bf09452acdf37752a563b859c6de37f128b019a8330ef9e57b11c5e9ffc14fc1'
SCHEMA='SEALED_INDEPENDENT_HIGHRHO14_19_INPUTS_V1'
NATIVE='work/cutoff15_20261017/fourier/highrho14_19_v1'
AUDIT='work/cutoff15_20261017/fourier/highrho14_19_readback_v1'
RUNS='runs/cutoff15_20261017/fourier/highrho14_19_v1'
ACTIONS=('plan','construct','replay','readback')
LABELS=dict(plan='plan01',construct='construct01',replay='replay01')
REQUEST=AUDIT+'/FRESH_REQUEST.json'
RESULT=AUDIT+'/FRESH_RESULT.json'


def dump(packet):return(json.dumps(packet,sort_keys=True,indent=2)+'\n').encode('utf-8')


def plan():
    need(digest(PLAN)==PLAN_SHA256,'Externally pinned independent highrho source plan');d=read(PLAN)
    need(d['schema']=='FINITE1519_HIGHRHO_SOURCE_PLAN_V1'
         and d['scope']=='CONDITIONAL_HIGHRHO14_19_FOURIER_SUBLANE_ONLY'
         and len(d['source_files'])==73 and d['original_manifest_graph_rows']==70
         and d['source_programs_unchanged']is True and d['source_manifests_unchanged']is True
         and all(d[k]is False for k in('arithmetic_computed','full_notebook57_completed',
                                     'parent_acquisitions_verified','all_index_conclusion_verified')),
         'Complete original73-input selection and explicitly incomplete full57 scope')
    return d


def obtain_assets(directory, *,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);result={}
    for a in plan()['assets']:
        name=a['name'];need(tuple(parts(name))==(name,),'Pinned source archive basename');p=ordinary(directory/name)
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));count=0;last=time.monotonic();at=0
            progress('finite1519_highrho_download_started',archive=name,total_bytes=a['bytes'])
            with urllib.request.urlopen(a['url'])as source,pending.open('wb')as target:
                while block:=source.read(MIB):
                    count+=len(block);need(count<=a['bytes'],'Bounded original source download');target.write(block)
                    if count-at>=16*MIB or time.monotonic()-last>=5:
                        progress('finite1519_highrho_download',archive=name,bytes=count,total_bytes=a['bytes']);at=count;last=time.monotonic()
            need(count==a['bytes']and digest(pending)==a['sha256'],'Actual full source archive SHA');pending.replace(p)
        need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Exact immutable source transport')
        result[name]=p.resolve();progress('finite1519_highrho_archive_verified',archive=name,bytes=a['bytes'],sha256=a['sha256'])
    return result


def prepare_cache(assets,output, *,progress=lambda *a,**k:None):
    d=plan();output=ordinary(output);output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for a in d['assets']:
            p=ordinary(assets[a['name']]);need(p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Pinned source transport')
            z=zipfile.ZipFile(p);base.zip_index(z);opened[a['name']]=z
        for i,(name,row)in enumerate(d['source_files'].items()):
            p=ordinary(output.joinpath(*parts(name)))
            if not p.exists():
                z=opened[row['archive']];info=z.getinfo(row['member']);need(info.file_size==row['bytes'],'Exact selected original input size')
                p.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info)as source,p.open('xb')as target:shutil.copyfileobj(source,target,MIB)
            need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every original input byte')
            if i%20==0:progress('finite1519_highrho_source_cache',files=i,total=len(d['source_files']),arithmetic_computed=False)
        base.verify_cache(output,d['source_files'])
    finally:
        for z in opened.values():z.close()
    return output.resolve()


def output_paths(action):
    need(action in ACTIONS,'One original highrho action')
    if action=='readback':return [RESULT]
    directory=RUNS+'/'+LABELS[action]
    return [directory+'/'+n for n in('metadata.json','stdout.txt','stderr.txt',
                                     'PLAN.json'if action=='plan'else'RESULT.json')]


def prepare(cache,task):
    d=plan();task=ordinary(task);need(not task.exists(),'Fresh private independent highrho capsule');task.mkdir(parents=True)
    for name,row in d['source_files'].items():
        p=ordinary(Path(cache).joinpath(*parts(name)));need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Original sealed source input')
        dest=task/'capsule'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    m=dict(schema=SCHEMA,original_task_root=str(task.resolve()),source_plan_sha256=PLAN_SHA256,
           source_adapter_sha256=digest(__file__),sources={n:r['sha256']for n,r in d['source_files'].items()},
           original_manifest_unchanged=True,arithmetic_computed=False,full_notebook57_completed=False,
           parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    (task/'SOURCES.json').write_bytes(dump(m));verify_job(task);return m


def verify_job(task):
    task=ordinary(task);d=plan();m=read(task/'SOURCES.json')
    need(m['schema']==SCHEMA and m['source_plan_sha256']==PLAN_SHA256 and m['source_adapter_sha256']==digest(__file__)
         and m['sources']=={n:r['sha256']for n,r in d['source_files'].items()}
         and m['original_manifest_unchanged']is True and all(m[k]is False for k in('arithmetic_computed',
             'full_notebook57_completed','parent_acquisitions_verified','all_index_conclusion_verified')),
         'Truthful independent source epoch, with no historical acceptance promotion')
    found=set()
    for p in(task/'capsule').rglob('*'):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(task/'capsule').as_posix())
    allowed={REQUEST}|{n for a in ACTIONS for n in output_paths(a)}
    need(set(m['sources'])<=found<=set(m['sources'])|allowed,'Sealed source closure plus only declared genuine current outputs')
    for name,pin in m['sources'].items():need(digest(task/'capsule'/name)==pin,'Every original mathematical/source/manifest byte unchanged')
    need(digest(task/'capsule'/NATIVE/'MANIFEST.json')==d['original_manifest_sha256'],'Exact original70-row native manifest')
    return m


def fresh_request(task):
    """Only current actual outputs determine this original readback request."""
    c=Path(task)/'capsule';native=NATIVE+'/MANIFEST.json';plan_path=RUNS+'/plan01/PLAN.json'
    return dict(plan=plan_path,plan_sha256=digest(c/plan_path),manifest_sha256=digest(c/native),
                construct_capture=RUNS+'/construct01',construct_metadata_sha256=digest(c/RUNS/'construct01/metadata.json'),
                replay_capture=RUNS+'/replay01',replay_metadata_sha256=digest(c/RUNS/'replay01/metadata.json'),output=RESULT)
