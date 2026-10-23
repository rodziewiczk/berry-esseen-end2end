"""Exact source preparation for a new n27/p41 candidate, never old acceptance."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import urllib.request
import zipfile
from .n5_remaining_sources import MIB,need,digest,read,parts,ordinary
from .finite1039_sources import zip_index

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'proof/n27_p41_recovery_source_plan.json'
PLAN_SHA256='94d5a0048c619a86666c94fc7ba93d7cb5bfee602c3e505e663d5ee2583fc814'
ARCHIVE_URL=('https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/download/'
             'cutoff20-sources-2026-10-17/cutoff25_20261011.zip')
SOURCE_SCHEMA='N27_P41_UNCHANGED_SOURCES_NEW_CANDIDATE_V1'
OUTPUTS={'COUNT41_FOREST.json','CONSTRUCTION_RUN.json','COUNT41_ACCEPTED.json'}


def plan():
    need(digest(PLAN)==PLAN_SHA256,'Exact externally pinned n27/p41 source plan')
    d=read(PLAN)
    need(d['schema']=='N27_P41_FRESH_CANDIDATE_SOURCE_PLAN_V1'and d['source_files_count']==43
         and len(d['source_files'])==43 and d['kernel_files_count']==39
         and d['arithmetic_computed']is False and d['parent_acquisitions_verified']is False
         and d['all_index_conclusion_verified']is False and d['new_candidate_epoch_required']is True,
         'Source proposal is not an execution or acquired premise')
    need(not OUTPUTS.intersection(d['source_files']),'No historical own output is an input')
    return d


def obtain_archive(directory, *,progress=lambda *a,**k:None):
    spec=plan()['archive'];directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True)
    path=ordinary(directory/spec['name'])
    if not path.exists():
        pending=ordinary(path.with_suffix('.zip.pending'));received=0
        progress('n27_p41_source_download_started',bytes_expected=spec['bytes'])
        with urllib.request.urlopen(ARCHIVE_URL)as source,pending.open('wb')as output:
            while block:=source.read(MIB):
                received+=len(block);need(received<=spec['bytes'],'Bounded original source download');output.write(block)
                if received%(16*MIB)==0:progress('n27_p41_source_download',bytes=received,bytes_expected=spec['bytes'])
        need(received==spec['bytes']and digest(pending)==spec['sha256'],'Whole exact original source transport');pending.replace(path)
    need(path.is_file()and path.stat().st_size==spec['bytes']and digest(path)==spec['sha256'],
         'Whole source archive size and SHA')
    return path


def verify_capsule(capsule, *,outputs=()):
    capsule=ordinary(capsule);d=plan();allowed=set(outputs)
    need(allowed<=OUTPUTS,'Only explicit fresh native outputs')
    found=set()
    for p in capsule.rglob('*'):
        ordinary(p);need(p.is_file(),'No unsealed source subdirectory')
        found.add(p.relative_to(capsule).as_posix())
    need(set(d['source_files'])<=found<=set(d['source_files'])|allowed,'Exact43 sealed inputs plus explicit fresh outputs')
    for name,row in d['source_files'].items():
        need(tuple(parts(name))==(name,),'Flat original native source')
        p=capsule/name;need(p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every unchanged original source byte')
    manifest=read(capsule/'KERNEL_COPY_MANIFEST.json')['files']
    need(type(manifest)is dict and len(manifest)==39 and all(d['source_files'][n]['sha256']==pin for n,pin in manifest.items()),
         'Exact39 original kernel-manifest inputs')
    contract=read(capsule/'contract.json');row=contract['rows'][0]
    need(len(contract['rows'])==1 and type(row['n'])is int and row['n']==27 and type(row['index'])is int and row['index']==41
         and row['K']=='0'and row['p']==['41/100','21/50']and row['rho_lower']=='1'and row['rho_upper']=='11/10',
         'Unchanged literal conditional n27/p41 contract')
    return d


def prepare(archive,task):
    d=plan();spec=d['archive'];archive=ordinary(archive);task=ordinary(task)
    need(archive.is_file()and archive.stat().st_size==spec['bytes']and digest(archive)==spec['sha256'],
         'Exact original archive before any extraction')
    need(not task.exists(),'Exclusive fresh new candidate epoch')
    with zipfile.ZipFile(archive)as z:
        zip_index(z);task.mkdir(parents=True);capsule=task/'capsule';capsule.mkdir()
        for name,row in d['source_files'].items():
            need(tuple(parts(name))==(name,),'Flat original source member')
            info=z.getinfo(row['member']);need(info.file_size==row['bytes'],'Exact source member size')
            with z.open(info)as source,(capsule/name).open('xb')as output:shutil.copyfileobj(source,output,MIB)
    verify_capsule(capsule)
    m=dict(schema=SOURCE_SCHEMA,source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),
           original_task_root=str(task.resolve()),sources={n:r['sha256']for n,r in d['source_files'].items()},
           new_candidate_epoch=True,arithmetic_computed=False,native_arithmetic_accepted=False,
           semantic_replacement_join_verified=False,lane53_ready=False,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    (task/'SOURCES.json').write_bytes((json.dumps(m,sort_keys=True,indent=2)+'\n').encode())
    verify_task(task);return m


def verify_task(task):
    task=ordinary(task);m=read(task/'SOURCES.json');d=verify_capsule(task/'capsule',outputs=OUTPUTS)
    need(m['schema']==SOURCE_SCHEMA and m['source_plan_sha256']==PLAN_SHA256
         and m['source_adapter_sha256']==digest(__file__)
         and m['sources']=={n:r['sha256']for n,r in d['source_files'].items()}
         and m['new_candidate_epoch']is True and m['arithmetic_computed']is False
         and all(m[k]is False for k in('native_arithmetic_accepted','semantic_replacement_join_verified','lane53_ready',
                                      'parent_acquisitions_verified','all_index_conclusion_verified')),
         'Exact unchanged source manifest and explicit new candidate epoch')
    return m
