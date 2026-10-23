"""Sealed source-only preparation of the fixed finite10--39 COUNT selection.

The old receipt selects an untrusted candidate and the expected native schema.
No mathematical module is imported, and no old own acceptance is a runtime input.
"""
from __future__ import annotations
from fractions import Fraction
import json
from pathlib import Path
import shutil
import stat
import time
import urllib.request
import zipfile
from .n5_remaining_sources import digest,read,unique,parts,ordinary,need,MIB

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'proof/finite1039_count_catalog.json'
CATALOG_SHA256='67a647a00111fda930391bda90345ece419bbf54c44a70c0390969ad0fab3d6d'
SCHEMA='FINITE1039_EXACT_JOB_INPUTS_V1'
LANES=dict(n10_14=217,n15_19=147,n20_24=163,n26_30=80,n31_34=282,n35_39=120)
_CATALOG_CACHE=None


def catalog():
    global _CATALOG_CACHE
    need(digest(CATALOG)==CATALOG_SHA256,'Exact externally pinned finite10--39 catalog')
    if _CATALOG_CACHE is None:_CATALOG_CACHE=read(CATALOG,limit=64*MIB)
    d=_CATALOG_CACHE
    need(d['schema']=='FINITE1039_SELECTED_SOURCE_CATALOG_V1' and len(d['jobs'])==1008 and d['expected_forests']==1009
         and {k:v['forests']for k,v in d['lanes'].items()}==LANES,'Complete fixed six-lane selection')
    need(d['arithmetic_computed']is False and d['parent_acquisitions_verified']is False
         and d['all_index_conclusion_verified']is False,'Source selection is not a proof receipt')
    return d


def jobs(lane=None):
    d=catalog()
    if lane is not None:
        need(lane in LANES,'One literal selected finite COUNT lane')
        need(d['lane_ready'][lane]is True,'Selected COUNT lane is not source-complete: '+lane)
    rows=d['jobs'];need(len({r['job_id']for r in rows})==len(rows),'Unique fixed COUNT jobs')
    return [r for r in rows if lane is None or r['lane']==lane]


def job(job_id):
    rows=[r for r in jobs()if r['job_id']==job_id]
    need(len(rows)==1,'One exact source-selected COUNT job');return rows[0]


def _intervals(box,dimensions=5):
    need(type(box)is list and len(box)==dimensions and dimensions in(4,5),'Original four/five closed native coordinate intervals')
    for interval in box:
        need(type(interval)is list and len(interval)==2 and all(type(q)is str for q in interval),'Rational native coordinate interval')
        a,b=map(Fraction,interval);need(str(a)==interval[0]and str(b)==interval[1]and a<=b,'Canonical ordered rational coordinates')


def inspect_candidate(row,packet):
    """Count complete candidate topology; never evaluate a leaf or a bound."""
    n=row['n'];need(type(n)is int and type(packet['index'])is int and packet['index']==row['index'],'Literal candidate panel index')
    contract_field=row.get('candidate_contract_field','contract_sha256')
    need(contract_field in('contract_sha256','targets_sha256')and packet[contract_field]==row['contract_sha256'],'Exact original candidate contract')
    nodes=leaves=depth=0
    if row['family']=='count_protocol':
        need(type(packet['n'])is int and packet['n']==n and type(packet['roots'])is list
             and [r['k']for r in packet['roots']]==list(range(n+1)),'All original listed count roots')
        for root in packet['roots']:
            need(type(root['k'])is int,'Literal count root');todo=[(root['tree'],0)]
            while todo:
                node,level=todo.pop();nodes+=1;depth=max(depth,level)
                need(nodes<=1000000 and level<=128 and type(node)is dict,'Bounded complete native tree')
                if node.get('kind')=='leaf':
                    _intervals(node['box'])
                    leaves+=1;need(type(node.get('decision'))is str and type(node.get('result'))is dict,'Closed candidate leaf payload')
                elif node.get('kind')=='split':todo.extend(((node['left'],level+1),(node['right'],level+1)))
                else:raise ValueError('No pending or unknown native tree node')
        result=dict(representation='nested_binary_count_forest',roots=n+1,nodes=nodes,leaves=leaves,maximum_depth=depth)
    else:
        need(row['family']=='strict','Known exact candidate representation');dimensions=row.get('dimensions',5);_intervals(packet['root'],dimensions)
        split={};leaf={}
        for kind,target in (('splits',split),('leaves',leaf)):
            need(type(packet[kind])is list,'Explicit flat count topology')
            for item in packet[kind]:
                need(type(item)is dict and type(item['k'])is int and 0<=item['k']<=n and type(item['path'])is list
                     and len(item['path'])<=128 and all(type(b)is int and b in(0,1)for b in item['path']),'Literal bounded flat count path')
                key=item['k'],tuple(item['path']);need(key not in split and key not in leaf,'No duplicate/overlapping flat count node')
                if kind=='splits':need(type(item['axis'])is int and 0<=item['axis']<dimensions,'Literal native split axis')
                else:need(type(item.get('status'))is str and (item.get('score_upper')is None or type(item.get('score_upper'))is str),'Closed flat leaf payload')
                target[key]=item
        seen=set();todo=[(k,())for k in range(n+1)]
        while todo:
            key=todo.pop();need(key not in seen,'One traversal per flat node');seen.add(key);nodes+=1;depth=max(depth,len(key[1]))
            need(nodes<=1000000,'Bounded flat candidate topology')
            if key in split:todo.extend(((key[0],key[1]+(0,)),(key[0],key[1]+(1,))))
            else:need(key in leaf,'Every implicit original root is completely closed');leaves+=1
        need(seen==set(split)|set(leaf),'No unused/disconnected candidate nodes')
        need(type(packet['visited'])is int and packet['visited']==nodes,'Original flat visited census')
        result=dict(representation='flat_split_leaf_paths',roots=n+1,nodes=nodes,leaves=leaves,maximum_depth=depth)
    if 'census'in row:need(result==row['census'],'Exact full source-selected structural census')
    return result


def zip_index(z):
    result={};folded=set();total=0
    need(len(z.infolist())<=200000,'Bounded source archive directory')
    for row in z.infolist():
        name=row.filename[:-1]if row.is_dir()else row.filename;parts(name);mode=row.external_attr>>16
        need(row.filename not in result and row.filename.casefold()not in folded and not row.flag_bits&1
             and not stat.S_ISLNK(mode)and stat.S_IFMT(mode)in(0,stat.S_IFREG,stat.S_IFDIR)
             and 0<=row.file_size<=256*MIB,'Unique ordinary bounded source archive member')
        result[row.filename]=row;folded.add(row.filename.casefold());total+=row.file_size
    need(total<=8*1024*MIB,'Bounded expanded source archive');return result


def obtain_assets(directory, *,lane=None,progress=lambda *a,**k:None):
    required=None if lane is None else {r['archive']for r in selected_files(lane).values()}
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);result={}
    for asset in catalog()['assets']:
        if required is not None and asset['name']not in required:continue
        name=asset['name'];need(tuple(parts(name))==(name,),'Fixed archive basename');path=ordinary(directory/name)
        if not path.exists():
            pending=ordinary(path.with_suffix(path.suffix+'.pending'));received=0;last=time.monotonic();block_at=0
            progress('finite1039_source_download_started',archive=name,total_bytes=asset['bytes'])
            with urllib.request.urlopen(asset['url'])as source,pending.open('wb')as dest:
                while block:=source.read(MIB):
                    received+=len(block);need(received<=asset['bytes'],'Bounded exact source download');dest.write(block);now=time.monotonic()
                    if received-block_at>=16*MIB or now-last>=5:
                        progress('finite1039_source_download',archive=name,bytes=received,total_bytes=asset['bytes']);last=now;block_at=received
            need(received==asset['bytes']and digest(pending)==asset['sha256'],'Complete pinned source download');pending.replace(path)
        need(path.is_file()and path.stat().st_size==asset['bytes']and digest(path)==asset['sha256'],'Exact immutable source archive')
        result[name]=path.resolve();progress('finite1039_source_archive_verified',archive=name,bytes=asset['bytes'],sha256=asset['sha256'])
    return result


def selected_files(lane):
    names={name for row in jobs(lane)for name in row['source_files_sha256']};d=catalog()
    return {name:d['source_files'][name]for name in sorted(names)}


def verify_cache(cache,selected):
    cache=ordinary(cache);found=set()
    for p in cache.rglob('*'):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(cache).as_posix())
    need(found==set(selected),'Exact sealed source-cache inventory')
    for name,row in selected.items():
        p=cache.joinpath(*parts(name));need(p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every sealed selected input')


def prepare_cache(assets,output,lane, *,progress=lambda *a,**k:None):
    d=catalog();selected=selected_files(lane);output=ordinary(output);output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for asset in d['assets']:
            if not any(row['archive']==asset['name']for row in selected.values()):continue
            p=ordinary(assets[asset['name']]);need(p.stat().st_size==asset['bytes']and digest(p)==asset['sha256'],'Exact source transport')
            z=zipfile.ZipFile(p);zip_index(z);opened[asset['name']]=z
        for ordinal,(name,row)in enumerate(selected.items()):
            path=ordinary(output.joinpath(*parts(name)))
            if path.exists():need(path.is_file()and path.stat().st_size==row['bytes']and digest(path)==row['sha256'],'Existing exact selected input')
            else:
                z=opened[row['archive']];info=z.getinfo(row['member']);need(info.file_size==row['bytes'],'Exact archive member size')
                path.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info)as source,path.open('xb')as dest:shutil.copyfileobj(source,dest,MIB)
                need(digest(path)==row['sha256'],'Actual complete selected source byte')
            if ordinal%1000==0:progress('finite1039_source_cache',files=ordinal,total=len(selected),arithmetic_computed=False)
        verify_cache(output,selected)
    finally:
        for z in opened.values():z.close()
    return output.resolve()


def output_relative(row):return row['directory']+'/'+row['output']


def prepare_job(job_id,cache,task):
    row=job(job_id);need(catalog()['lane_ready'][row['lane']]is True,'Selected COUNT lane is not source-complete: '+row['lane'])
    task=ordinary(task);need(not task.exists(),'Fresh exclusive private COUNT capsule');task.mkdir(parents=True)
    for name,pin in row['source_files_sha256'].items():
        source=Path(cache).joinpath(*parts(name));need(digest(source)==pin,'Original selected source/candidate byte')
        dest=task/'capsule'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
    m=dict(schema=SCHEMA,job_id=job_id,original_task_root=str(task.resolve()),catalog_sha256=CATALOG_SHA256,
        source_adapter_sha256=digest(__file__),sources=row['source_files_sha256'],arithmetic_computed=False,
        parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    (task/'SOURCES.json').write_bytes((json.dumps(m,sort_keys=True,indent=2)+'\n').encode());verify_job(task,row);return m


def verify_job(task,row=None):
    task=ordinary(task);m=read(task/'SOURCES.json');row=job(m['job_id'])if row is None else row
    need(row==job(row['job_id'])and m['schema']==SCHEMA and m['job_id']==row['job_id']and m['catalog_sha256']==CATALOG_SHA256
         and m['source_adapter_sha256']==digest(__file__)and m['sources']==row['source_files_sha256']
         and m['arithmetic_computed']is False and m['parent_acquisitions_verified']is False
         and m['all_index_conclusion_verified']is False,'Exact selected source epoch and no historical acceptance')
    found=set()
    for p in(task/'capsule').rglob('*'):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(task/'capsule').as_posix())
    need(set(m['sources'])<=found<=set(m['sources'])|{output_relative(row)},'Only sealed inputs plus one fresh receipt')
    for name,pin in m['sources'].items():need(digest(task/'capsule'/name)==pin,'Unchanged complete original source closure')
    return m
