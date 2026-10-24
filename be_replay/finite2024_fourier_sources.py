"""Unchanged full sources for58D/E/F; only current readback request data is new."""
from __future__ import annotations
import json
from pathlib import Path
import shutil,time,urllib.request,zipfile
from . import finite1039_sources as base
ROOT,MIB=base.ROOT,base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
PLAN=ROOT/'proof/finite2024_fourier_source_plan.json'
PLAN_SHA256='4dc95b4cc208f96df9d579e2f43e06774162251c452198f01d4b626972ba034c'
ACTIONS=('plan','construct','replay','readback')
LABELS=dict(plan='plan01',construct='construct01',replay='replay01')
FAMILIES=('auxiliary','universal','supported')

def dump(value):return(json.dumps(value,sort_keys=True,indent=2)+'\n').encode()

def plan():
    need(digest(PLAN)==PLAN_SHA256,'Pinned exact three-family actual20 Fourier source plan');d=read(PLAN)
    need(d['schema']=='FINITE2024_FOURIER_SOURCE_PLAN_V1'and set(d['families'])==set(FAMILIES)
         and all(d[k]is False for k in('arithmetic_computed','full_notebook58_completed','predecessor_verified','all_index_conclusion_verified')),
         'Exact three conditional Fourier families without a global theorem')
    for key,count,rows in(('auxiliary',51,48),('universal',46,43),('supported',51,48)):
        c=d['families'][key]
        need(len(c['source_files'])==count and c['original_manifest_rows']==rows
             and c['original_source_programs_unchanged']is True and c['original_manifest_unchanged']is True
             and all(c[k]is False for k in('arithmetic_computed','predecessor_verified','full_notebook58_completed','all_index_conclusion_verified')),
             'Every original source/manifest retained and arithmetic unexecuted')
    return d

def family(key):
    need(type(key)is str and key in FAMILIES,'Literal auxiliary, universal or supported family');return plan()['families'][key]

def request_path(c):return c['audit']+'/FRESH_REQUEST.json'
def result_path(c):return c['audit']+'/FRESH_RESULT.json'

def output_paths(action,c):
    need(action in ACTIONS,'One complete original action')
    if action=='readback':return [result_path(c)]
    return [c['runs']+'/'+LABELS[action]+'/'+v for v in('metadata.json','stdout.txt','stderr.txt','PLAN.json'if action=='plan'else'RESULT.json')]

def obtain_assets(directory,key,*,progress=lambda *a,**k:None):
    c=family(key);used={v['archive']for v in c['source_files'].values()};directory=ordinary(Path(directory));directory.mkdir(parents=True,exist_ok=True);out={}
    for row in plan()['assets']:
        if row['name']not in used:continue
        need(tuple(parts(row['name']))==(row['name'],),'Pinned archive basename');p=ordinary(directory/row['name'])
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));count=0;last=0
            progress('finite2024_fourier_download_started',family=key,archive=row['name'],bytes=row['bytes'])
            with urllib.request.urlopen(row['url'])as source,pending.open('wb')as target:
                while block:=source.read(MIB):
                    count+=len(block);need(count<=row['bytes'],'Bounded original source archive');target.write(block)
                    if count-last>=16*MIB:progress('finite2024_fourier_download',family=key,archive=row['name'],bytes=count);last=count
            need(count==row['bytes']and digest(pending)==row['sha256'],'Actual whole original archive hash');pending.replace(p)
        need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Exact immutable source transport');out[row['name']]=p.resolve()
    return out

def prepare_cache(assets,output,key):
    c=family(key);used={v['archive']for v in c['source_files'].values()};output=ordinary(Path(output));output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for row in plan()['assets']:
            if row['name']not in used:continue
            p=ordinary(Path(assets[row['name']]));need(p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Exact original archive')
            z=zipfile.ZipFile(p);base.zip_index(z);opened[row['name']]=z
        for name,row in c['source_files'].items():
            p=ordinary(output.joinpath(*parts(name)))
            if not p.exists():
                info=opened[row['archive']].getinfo(row['member']);need(info.file_size==row['bytes'],'Selected source member size');p.parent.mkdir(parents=True,exist_ok=True)
                with opened[row['archive']].open(info)as source,p.open('xb')as target:shutil.copyfileobj(source,target,MIB)
            need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every exact original input byte')
        base.verify_cache(output,c['source_files'])
    finally:
        for z in opened.values():z.close()
    return output.resolve()

def prepare(cache,task,key):
    c=family(key);task=ordinary(Path(task).resolve());need(not task.exists(),'Fresh private full Fourier unit');task.mkdir(parents=True)
    for name,row in c['source_files'].items():
        source=ordinary(Path(cache).joinpath(*parts(name)));need(source.is_file()and source.stat().st_size==row['bytes']and digest(source)==row['sha256'],'Exact cached input')
        target=task/'capsule'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    m=dict(schema='SEALED_FINITE2024_FOURIER_SOURCES_V1',family=key,source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),
        original_task_root=str(task),sources={n:v['sha256']for n,v in c['source_files'].items()},original_manifest_unchanged=True,
        arithmetic_computed=False,full_notebook58_completed=False,predecessor_verified=False,all_index_conclusion_verified=False)
    (task/'SOURCES.json').write_bytes(dump(m));verify_job(task,key);return m

def verify_job(task,key=None):
    task=ordinary(Path(task));m=read(task/'SOURCES.json');c=family(m['family'])
    need(key is None or m['family']==key,'Requested Fourier family matches')
    need(set(m)=={'schema','family','source_plan_sha256','source_adapter_sha256','original_task_root','sources','original_manifest_unchanged',
                 'arithmetic_computed','full_notebook58_completed','predecessor_verified','all_index_conclusion_verified'}
         and m['schema']=='SEALED_FINITE2024_FOURIER_SOURCES_V1'and m['source_plan_sha256']==PLAN_SHA256 and m['source_adapter_sha256']==digest(__file__)
         and m['sources']=={n:v['sha256']for n,v in c['source_files'].items()}and m['original_manifest_unchanged']is True
         and all(m[k]is False for k in('arithmetic_computed','full_notebook58_completed','predecessor_verified','all_index_conclusion_verified')),
         'Whole unchanged source epoch and explicitly incomplete full58')
    found=set()
    for p in(task/'capsule').rglob('*'):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(task/'capsule').as_posix())
    generated={request_path(c)}|{n for a in ACTIONS for n in output_paths(a,c)}
    need(set(m['sources'])<=found<=set(m['sources'])|generated,'Only sealed sources and declared actual outputs')
    for name,pin in m['sources'].items():need(digest(task/'capsule'/name)==pin,'Every original mathematical/source byte unchanged')
    need(digest(task/'capsule'/c['native']/'MANIFEST.json')==c['original_manifest_sha256'],'Exact original manifest')
    return m

def fresh_request(task):
    m=verify_job(task);c=family(m['family']);root=Path(task)/'capsule';p=c['runs']+'/plan01/PLAN.json'
    request=dict(plan=p,plan_sha256=digest(root/p),manifest_sha256=digest(root/c['native']/'MANIFEST.json'),
        construct_capture=c['runs']+'/construct01',construct_metadata_sha256=digest(root/c['runs']/'construct01/metadata.json'),
        replay_capture=c['runs']+'/replay01',replay_metadata_sha256=digest(root/c['runs']/'replay01/metadata.json'),output=result_path(c))
    if m['family']=='universal':request['rho']=c['rho']
    return request
