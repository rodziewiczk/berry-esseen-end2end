"""Hash-only source preparation for the unchanged three-file scalar certificate."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat

ROOT=Path(__file__).resolve().parents[1]
MIB=1024**2
PLAN=ROOT/'proof/finite1014_kappa_source_plan.json'
PLAN_SHA256='3cfa73a7278e06b71c65cbb8726a500f2b6b3b6bd1524de852749f76544489bb'
SCHEMA='SEALED_ORIGINAL_KAPPA_62_625_SOURCES_V1'
FILES=('kernel.py','controls.py','PROOF.txt')
OUTPUTS=('CERTIFICATE.json','CHECKED.json')


def need(value,message):
    if not value:raise ValueError(message)


def ordinary(path):
    p=Path(path)
    for parent in (p,*p.parents):
        if parent.exists()or parent.is_symlink():
            mode=parent.lstat().st_mode
            need(not stat.S_ISLNK(mode)and (stat.S_ISREG(mode)or stat.S_ISDIR(mode)),
                 'Ordinary nonlinked source/evidence path')
            need(not getattr(parent.lstat(),'st_file_attributes',0)&1024,'No Windows reparse points')
    return p


def digest(path):
    p=ordinary(path);need(p.is_file(),'Ordinary file for SHA256')
    h=hashlib.sha256()
    with p.open('rb')as stream:
        while block:=stream.read(MIB):h.update(block)
    return h.hexdigest()


def unique(pairs):
    out={}
    for k,v in pairs:need(k not in out,'Duplicate JSON key');out[k]=v
    return out


def loads(text):
    def invalid(value):raise ValueError('Nonfinite JSON number')
    return json.loads(text,object_pairs_hook=unique,parse_constant=invalid)


def read(path,limit=4*MIB):
    p=ordinary(path);need(p.is_file()and p.stat().st_size<=limit,'Bounded ordinary JSON')
    return loads(p.read_text(encoding='utf-8'))


def dump(packet):return(json.dumps(packet,sort_keys=True,indent=2)+'\n').encode('utf-8')


def parts(name):
    need(type(name)is str and bool(name)and '\\'not in name and '\0'not in name and ':'not in name,
         'Portable relative file name')
    p=PurePosixPath(name)
    need(not p.is_absolute()and p.as_posix()==name and all(x not in('','.', '..')for x in name.split('/')),
         'Contained canonical relative path')
    return p.parts


def plan():
    need(digest(PLAN)==PLAN_SHA256,'Pinned scalar source plan');d=read(PLAN)
    need(d['schema']=='FINITE1014_KAPPA_SOURCE_PLAN_V1'and d['scope']=='UNCHANGED_GLOBAL_SCALAR_KAPPA_62_625_ONLY'
         and set(d['source_files'])==set(FILES)and d['source_programs_unchanged']is True
         and all(d[k]is False for k in('historical_outputs_supplied','arithmetic_computed',
                                      'full_notebook56_completed','all_index_conclusion_verified')),
         'Exactly three unchanged scalar sources, without historical results')
    return d


def verify_vendor():
    d=plan();vendor=ordinary(ROOT.joinpath(*parts(d['vendor_directory'])))
    expected=set(FILES)|{'LICENSE','PROVENANCE.json'}
    need(vendor.is_dir()and {p.name for p in vendor.iterdir()}==expected,'Exact small vendor closure')
    for name,row in d['source_files'].items():
        p=ordinary(vendor/name)
        need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Unchanged original '+name)
    need(digest(vendor/'PROVENANCE.json')==d['provenance_sha256']and digest(vendor/'LICENSE')==d['license_sha256'],
         'Actual source provenance and license')
    return vendor,d


def prepare(task):
    vendor,d=verify_vendor();task=ordinary(Path(task).resolve());need(not task.exists(),'Fresh scalar task')
    (task/'capsule').mkdir(parents=True)
    for name in FILES:shutil.copyfile(vendor/name,task/'capsule'/name)
    request=dict(schema=SCHEMA,source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),
        original_task_root=str(task),sources={n:dict(bytes=d['source_files'][n]['bytes'],sha256=d['source_files'][n]['sha256'])for n in FILES},
        original_sources_unchanged=True,historical_outputs_supplied=False,arithmetic_computed=False)
    (task/'SOURCES.json').write_bytes(dump(request));verify(task);return request


def verify(task):
    task=ordinary(Path(task).resolve());d=plan();request=read(task/'SOURCES.json')
    expected={n:dict(bytes=d['source_files'][n]['bytes'],sha256=d['source_files'][n]['sha256'])for n in FILES}
    need(set(request)=={'schema','source_plan_sha256','source_adapter_sha256','original_task_root','sources',
                       'original_sources_unchanged','historical_outputs_supplied','arithmetic_computed'}
         and request['schema']==SCHEMA and request['source_plan_sha256']==PLAN_SHA256
         and request['source_adapter_sha256']==digest(__file__)and request['sources']==expected
         and type(request['original_task_root'])is str and request['original_sources_unchanged']is True
         and request['historical_outputs_supplied']is False and request['arithmetic_computed']is False,
         'Exact current source preparation ledger')
    capsule=ordinary(task/'capsule');need(capsule.is_dir(),'Ordinary scalar capsule')
    need(set(FILES)<={p.name for p in capsule.iterdir()}<=set(FILES+OUTPUTS),'Only fixed sources and two fresh outputs')
    for p in capsule.iterdir():ordinary(p);need(p.is_file(),'No extra capsule directories')
    for name,row in expected.items():
        p=capsule/name;need(p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Actual scalar source bytes')
    return request
