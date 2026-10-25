"""Pinned original source and data closure for all22 notebook67 processes.

Only bytes, JSON and Python import syntax are read here. Historical successful
receipts remain explicitly source/provenance, never acquired theorem evidence.
"""
from __future__ import annotations
import hashlib,json,shutil,stat,urllib.request,uuid,zipfile
from functools import lru_cache
from pathlib import Path
from . import n5_remaining_sources as basic
from .colab_batch import atomic_json

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'proof/n5_full_join_source_plan.json'
PLAN_SHA256='19371f28b0ed2b5f96c21d9ebdd8acbff753d161898f6b23e52833725994f621'
MIB=1024**2
digest=basic.digest;ordinary=basic.ordinary;parts=basic.parts;read=basic.read;need=basic.need;unique=basic.unique

@lru_cache(maxsize=1)
def plan():
    need(digest(PLAN)==PLAN_SHA256,'Exact notebook67 full source plan')
    d=read(PLAN,16*MIB)
    need(d['schema']=='N5_FULL_JOIN_SOURCE_PLAN_V1'and len(d['actions'])==22 and len(d['groups'])==15
         and len({r['id']for r in d['actions']})==22 and d['numerical_calls']==22,'Complete fixed22/15 physical action partition')
    need(digest(ROOT/'proof/remaining_n5_delivery_partition.json')==d['partition_sha256'],'Original47-call scope partition')
    for name,row in d['files'].items():parts(name);parts(row['member'])
    return d

def group(group_id):
    rows=[r for r in plan()['groups']if r['id']==group_id];need(len(rows)==1,'One fixed original67 group');return rows[0]

def actions(group_id):
    p=plan();g=group(group_id);return [next(a for a in p['actions']if a['id']==i)for i in g['action_ids']]

def obtain_archive(archives,*,download=True,progress=lambda *a,**k:None):
    d=plan()['archive'];root=ordinary(archives);root.mkdir(parents=True,exist_ok=True);path=ordinary(root/d['name'])
    if not path.exists():
        need(download,'Pinned complete C5 source archive absent')
        pending=path.with_name(path.name+'.partial-'+uuid.uuid4().hex[:8]);used=0
        try:
            with urllib.request.urlopen(d['url'],timeout=60)as source,pending.open('xb')as target:
                while raw:=source.read(MIB):
                    used+=len(raw);need(used<=d['bytes'],'Bounded exact67 source download');target.write(raw)
                    if used%(16*MIB)==0:progress('n5_full_source_download',bytes=used,total=d['bytes'])
            need(used==d['bytes']and digest(pending)==d['sha256'],'Downloaded source bytes and SHA');pending.replace(path)
        finally:
            if pending.exists():pending.unlink()
    need(path.is_file()and path.stat().st_size==d['bytes']and digest(path)==d['sha256'],'Exact original67 archive')
    return path

def prepare_cache(archive,destination,*,progress=lambda *a,**k:None):
    p=plan();archive=ordinary(archive)
    need(archive.stat().st_size==p['archive']['bytes']and digest(archive)==p['archive']['sha256'],'Archive verified before preparation')
    destination=ordinary(destination);destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive)as z:
        basic.zip_members(z)
        for i,(name,row)in enumerate(p['files'].items()):
            target=destination.joinpath(*parts(name));target.parent.mkdir(parents=True,exist_ok=True)
            for parent in [target,*target.parents]:
                if parent==destination.parent:break
                ordinary(parent)
            if not target.exists():
                info=z.getinfo(row['member']);need(info.file_size==row['bytes'],'Exact original member size')
                with z.open(info)as source,target.open('xb')as output:shutil.copyfileobj(source,output,MIB)
            need(target.is_file()and target.stat().st_size==row['bytes']and digest(target)==row['sha256'],'Sealed transitive source '+name)
            if i%100==0:progress('n5_full_source_preparation',completed=i,total=len(p['files']),original_mathematics_executed=False)
    return destination

def prepare(group_id,cache,task):
    p=plan();g=group(group_id);task=ordinary(task).resolve();need(not task.exists(),'Fresh private physical67 epoch')
    capsule=task/'capsule';capsule.mkdir(parents=True,exist_ok=False)
    for name in g['inputs']:
        row=p['files'][name];source=Path(cache).joinpath(*parts(name));ordinary(source)
        need(source.is_file()and digest(source)==row['sha256'],'Actual original input '+name)
        out=capsule.joinpath(*parts(name));out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,out)
    # Store old outcomes separately. They cannot satisfy active output slots.
    for action in actions(group_id):
        for name in action['outputs']:
            target=task/'provenance'/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(Path(cache).joinpath(*parts(name)),target)
    request=dict(schema='N5_FULL_JOIN_GROUP_REQUEST_V1',group_id=group_id,plan_sha256=PLAN_SHA256,
                 original_task_root=str(task),inputs={n:p['files'][n]['sha256']for n in g['inputs']},
                 actions=g['action_ids'],old_outputs_are_current_evidence=False)
    atomic_json(task/'REQUEST.json',request);verify(task,allow_missing_outputs=True);return request

def verify(task,*,allow_missing_outputs=False):
    need(digest(PLAN)==PLAN_SHA256,'Source plan unchanged throughout execution/readback')
    task=ordinary(task).resolve();request=read(task/'REQUEST.json');g=group(request['group_id']);p=plan()
    need(request['schema']=='N5_FULL_JOIN_GROUP_REQUEST_V1'and request['plan_sha256']==PLAN_SHA256
         and request['actions']==g['action_ids']and request['old_outputs_are_current_evidence']is False
         and request['inputs']=={n:p['files'][n]['sha256']for n in g['inputs']},'Exact67 source request')
    expected=set(g['inputs']);actual=set()
    for f in(task/'capsule').rglob('*'):
        ordinary(f)
        if f.is_file():actual.add(f.relative_to(task/'capsule').as_posix())
    permitted=expected|set(g['outputs'])
    need(actual<=permitted and expected<=actual and (allow_missing_outputs or actual==permitted),'No missing/unbound runtime helper or historical active output')
    for name,pin in request['inputs'].items():need(digest(task/'capsule'/name)==pin,'Unchanged runtime source/data '+name)
    return request,g
