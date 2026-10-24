"""Exact source-only conditional supported HIGH10--14 sublane of package56.

All98 original input bytes, including the original95-row manifest, are kept
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
PLAN=ROOT/'proof/finite1014_high_source_plan.json'
PLAN_SHA256='01c804d759e5f9509409bb31d78e7ae71c9922309275060f8f77458be716501b'
SCHEMA='SEALED_CONDITIONAL_SUPPORTED_HIGH10_14_INPUTS_V1'
NATIVE='work/cutoff10_20261018/root/high10_moment_v1'
AUDIT='work/cutoff10_20261018/audit/refined_high_review_v1'
RUNS='runs/cutoff10_20261018/root'
ACTIONS=('construct','replay','readback')
LABELS=dict(construct='high_moment_construct01',replay='high_moment_replay01')
OUTPUT_NAMES=dict(construct='RESULT.json',replay='REPLAY_RESULT.json')
RESULT=AUDIT+'/READBACK.json'
ENGINE_NAMES=('bound.py','kernel.py','universal.py')


def dump(packet):return(json.dumps(packet,sort_keys=True,indent=2)+'\n').encode('utf-8')


def plan():
    need(digest(PLAN)==PLAN_SHA256,'Externally pinned supported-HIGH source plan');d=read(PLAN)
    need(d['schema']=='FINITE1014_SUPPORTED_HIGH_SOURCE_PLAN_V1'
         and d['scope']=='CONDITIONAL_SUPPORTED_MOMENT_HIGH10_14_SUBLANE_ONLY'
         and len(d['source_files'])==98 and d['original_manifest_graph_rows']==95
         and d['source_programs_unchanged']is True and d['source_manifests_unchanged']is True
         and all(d[k]is False for k in('arithmetic_computed','full_notebook56_completed',
                                     'support_acquisition_verified','parent_acquisitions_verified','all_index_conclusion_verified')),
         'Complete original98-input selection and explicitly incomplete full56 scope')
    return d


def obtain_assets(directory, *,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);result={}
    for a in plan()['assets']:
        name=a['name'];need(tuple(parts(name))==(name,),'Pinned source archive basename');p=ordinary(directory/name)
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));count=0;last=time.monotonic();at=0
            progress('finite1014_high_download_started',archive=name,total_bytes=a['bytes'])
            with urllib.request.urlopen(a['url'])as source,pending.open('wb')as target:
                while block:=source.read(MIB):
                    count+=len(block);need(count<=a['bytes'],'Bounded original source download');target.write(block)
                    if count-at>=16*MIB or time.monotonic()-last>=5:
                        progress('finite1014_high_download',archive=name,bytes=count,total_bytes=a['bytes']);at=count;last=time.monotonic()
            need(count==a['bytes']and digest(pending)==a['sha256'],'Actual full source archive SHA');pending.replace(p)
        need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Exact immutable source transport')
        result[name]=p.resolve();progress('finite1014_high_archive_verified',archive=name,bytes=a['bytes'],sha256=a['sha256'])
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
            if i%20==0:progress('finite1014_high_source_cache',files=i,total=len(d['source_files']),arithmetic_computed=False)
        base.verify_cache(output,d['source_files'])
    finally:
        for z in opened.values():z.close()
    return output.resolve()


def output_paths(action):
    need(action in ACTIONS,'One complete original HIGH action')
    if action=='readback':return [RESULT]+[AUDIT+'/engine/'+n for n in ENGINE_NAMES]
    return [NATIVE+'/'+OUTPUT_NAMES[action]]


def capture_paths(action):
    need(action in ACTIONS,'One complete original HIGH action')
    if action=='readback':return []
    return [RUNS+'/'+LABELS[action]+'/'+n for n in ('metadata.json','stdout.txt','stderr.txt')]


def generated_paths(action):return output_paths(action)+capture_paths(action)


def native_input_map(request):
    from posixpath import relpath
    return {relpath(n,NATIVE):pin for n,pin in request['sources'].items()}


def prepare(cache,task):
    d=plan();task=ordinary(task);need(not task.exists(),'Fresh private supported-HIGH capsule');task.mkdir(parents=True)
    for name,row in d['source_files'].items():
        p=ordinary(Path(cache).joinpath(*parts(name)));need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Original sealed source input')
        dest=task/'capsule'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    m=dict(schema=SCHEMA,original_task_root=str(task.resolve()),source_plan_sha256=PLAN_SHA256,
           source_adapter_sha256=digest(__file__),sources={n:r['sha256']for n,r in d['source_files'].items()},
           original_manifest_unchanged=True,arithmetic_computed=False,full_notebook56_completed=False,
           support_acquisition_verified=False,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    (task/'SOURCES.json').write_bytes(dump(m));verify_job(task);return m


def verify_job(task):
    task=ordinary(task);d=plan();m=read(task/'SOURCES.json')
    need(m['schema']==SCHEMA and m['source_plan_sha256']==PLAN_SHA256 and m['source_adapter_sha256']==digest(__file__)
         and m['sources']=={n:r['sha256']for n,r in d['source_files'].items()}
         and m['original_manifest_unchanged']is True and all(m[k]is False for k in('arithmetic_computed',
             'full_notebook56_completed','support_acquisition_verified','parent_acquisitions_verified','all_index_conclusion_verified')),
         'Truthful independent source epoch, with no historical acceptance promotion')
    found=set()
    for p in(task/'capsule').rglob('*'):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(task/'capsule').as_posix())
    allowed={n for a in ACTIONS for n in generated_paths(a)}
    need(set(m['sources'])<=found<=set(m['sources'])|allowed,'Sealed source closure plus only declared genuine current outputs')
    for name,pin in m['sources'].items():need(digest(task/'capsule'/name)==pin,'Every original mathematical/source/manifest byte unchanged')
    need(digest(task/'capsule'/NATIVE/'MANIFEST.json')==d['original_manifest_sha256'],'Exact original95-row native manifest')
    return m


