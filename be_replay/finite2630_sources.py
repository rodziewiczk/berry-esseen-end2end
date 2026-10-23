"""New, source-only n26--30 selection epoch; original numerical bytes unchanged.

The 79 archived candidates and the independently validated recovered n27/p41
pair have distinct provenance. This adapter never changes the old readiness
catalog and never presents its own copying as an old adapter execution.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import time
import urllib.request
import zipfile
from . import finite1039_sources as old

ROOT, MIB = old.ROOT, old.MIB
need, digest, read, unique = old.need, old.digest, old.read, old.unique
parts, ordinary = old.parts, old.ordinary
SELECTION = ROOT/'proof/finite2630_selection.json'
SELECTION_SHA256 = 'aa74851fd2b2030274aada84cf3177cb3c46bce44dfafd63909e0ae524e0e98c'
SCHEMA = 'FINITE2630_EXACT_ARCHIVED_JOB_INPUTS_V1'


def canonical_sha(packet):
    return hashlib.sha256(json.dumps(packet,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def selection():
    need(digest(SELECTION)==SELECTION_SHA256,'Externally pinned recovered n26--30 selection')
    d=read(SELECTION)
    need(d['schema']=='FINITE2630_RECOVERED_EXACT_SELECTION_V1'
         and d['original_catalog_sha256']==old.CATALOG_SHA256
         and d['conditional_arithmetic_completed'] is False
         and d['parent_acquisitions_verified'] is False and d['all_index_conclusion_verified'] is False,
         'Source selection is neither an acquired premise nor an arithmetic receipt')
    return d


def jobs():
    # The old blocked whole-lane API is deliberately not called or modified.
    rows=[r for r in old.jobs() if r['lane']=='n26_30'];d=selection()
    need(len(rows)==79 and [r['job_id']for r in rows]==d['original_job_ids']
         and canonical_sha(rows)==d['original_rows_sha256']
         and all(r['family']=='count_protocol' for r in rows),
         'Exactly the original79 full acceptor jobs and complete original row bindings')
    return rows


def job(job_id):
    rows=[r for r in jobs() if r['job_id']==job_id]
    need(len(rows)==1,'One literal original n26--30 COUNT job');return rows[0]


def selected_files():
    names={p for r in jobs() for p in r['source_files_sha256']};d=old.catalog()
    return {p:d['source_files'][p]for p in sorted(names)}


def obtain_assets(directory, *,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);result={}
    required={r['archive']for r in selected_files().values()}
    for a in old.catalog()['assets']:
        if a['name']not in required:continue
        name=a['name'];need(tuple(parts(name))==(name,),'Fixed immutable archive basename')
        p=ordinary(directory/name)
        if not p.exists():
            temporary=ordinary(p.with_suffix(p.suffix+'.pending'));received=0;last=time.monotonic();block_at=0
            progress('finite2630_source_download_started',archive=name,total_bytes=a['bytes'])
            with urllib.request.urlopen(a['url'])as source,temporary.open('wb')as target:
                while block:=source.read(MIB):
                    received+=len(block);need(received<=a['bytes'],'Bounded exact source download');target.write(block)
                    now=time.monotonic()
                    if received-block_at>=16*MIB or now-last>=5:
                        progress('finite2630_source_download',archive=name,bytes=received,total_bytes=a['bytes']);last=now;block_at=received
            need(received==a['bytes']and digest(temporary)==a['sha256'],'Complete original source download');temporary.replace(p)
        need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Exact pinned original source archive')
        result[name]=p.resolve();progress('finite2630_source_archive_verified',archive=name,sha256=a['sha256'],bytes=a['bytes'])
    need(set(result)==required,'Every selected original source asset');return result


def prepare_cache(assets,output, *,progress=lambda *a,**k:None):
    selected=selected_files();output=ordinary(output);output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for a in old.catalog()['assets']:
            if not any(r['archive']==a['name']for r in selected.values()):continue
            p=ordinary(assets[a['name']]);need(p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Exact source transport')
            z=zipfile.ZipFile(p);old.zip_index(z);opened[a['name']]=z
        for ordinal,(name,row)in enumerate(selected.items()):
            p=ordinary(output.joinpath(*parts(name)))
            if not p.exists():
                z=opened[row['archive']];info=z.getinfo(row['member']);need(info.file_size==row['bytes'],'Exact source member size')
                p.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info)as source,p.open('xb')as target:shutil.copyfileobj(source,target,MIB)
            need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every full original source/candidate byte')
            if ordinal%500==0:progress('finite2630_source_cache',files=ordinal,total=len(selected),arithmetic_computed=False)
        old.verify_cache(output,selected)
    finally:
        for z in opened.values():z.close()
    return output.resolve()


output_relative=old.output_relative
inspect_candidate=old.inspect_candidate


def prepare_job(job_id,cache,task):
    row=job(job_id);task=ordinary(task);need(not task.exists(),'Fresh exclusive new n26--30 source capsule');task.mkdir(parents=True)
    for name,pin in row['source_files_sha256'].items():
        p=ordinary(Path(cache).joinpath(*parts(name)));need(p.is_file()and digest(p)==pin,'Original selected input byte')
        dest=task/'capsule'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    m=dict(schema=SCHEMA,job_id=job_id,original_task_root=str(task.resolve()),selection_sha256=SELECTION_SHA256,
           original_catalog_sha256=old.CATALOG_SHA256,source_adapter_sha256=digest(__file__),
           sources=row['source_files_sha256'],arithmetic_computed=False,parent_acquisitions_verified=False,
           all_index_conclusion_verified=False)
    (task/'SOURCES.json').write_bytes((json.dumps(m,sort_keys=True,indent=2)+'\n').encode())
    verify_job(task,row);return m


def verify_job(task,row=None):
    task=ordinary(task);m=read(task/'SOURCES.json');row=job(m['job_id'])if row is None else row
    need(row==job(row['job_id'])and m['schema']==SCHEMA and m['job_id']==row['job_id']
         and m['selection_sha256']==SELECTION_SHA256 and m['original_catalog_sha256']==old.CATALOG_SHA256
         and m['source_adapter_sha256']==digest(__file__)and m['sources']==row['source_files_sha256']
         and m['arithmetic_computed']is False and m['parent_acquisitions_verified']is False
         and m['all_index_conclusion_verified']is False,'Truthful exact new source-adapter epoch')
    found=set()
    for p in(task/'capsule').rglob('*'):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(task/'capsule').as_posix())
    need(set(m['sources'])<=found<=set(m['sources'])|{output_relative(row)},'Only full sealed inputs plus one newly generated receipt')
    for name,pin in m['sources'].items():need(digest(task/'capsule'/name)==pin,'Original numerical source and candidate unchanged')
    return m
