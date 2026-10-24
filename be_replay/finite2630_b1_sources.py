"""59A exact original B1 inputs; only two source-location JSONs are derived."""
from __future__ import annotations
import copy,hashlib,json,re,shutil,urllib.request,zipfile
from pathlib import Path,PureWindowsPath,PurePosixPath
from . import finite1039_sources as base
ROOT,MIB=base.ROOT,base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
PLAN=ROOT/'proof/finite2630_b1_source_plan.json'
PLAN_SHA256='1a326d71a3fd63c183259d4db49460c94196eb4b7ac0b11c534b67ff1dc79031'
NATIVE='work/cutoff25_continue_20261015/root/sine_b1_cover_v1'
RECORD='work/cutoff25_continue_20261015/phase_rectangle_v1/EXACT_23STRIP_SINE_INPUTS.json'
MANIFEST=NATIVE+'/MANIFEST.json'
ACTIONS=('construct','accept')
OUTPUTS=dict(construct='COVER.json',accept='ACCEPTED.json')
SCHEMA='SEALED_FINITE2630_B1_CURRENT_LOCATION_INPUTS_V1'

def dump(d):return(json.dumps(d,sort_keys=True,indent=2)+'\n').encode('utf-8')
def loads(value):
    def invalid(value):raise ValueError('Nonfinite JSON number')
    return json.loads(value,object_pairs_hook=base.unique,parse_constant=invalid)
def same(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    return a==b
def pathclass(value):
    need(type(value)is str and '\0'not in value,'Ordinary original path string')
    cls=PureWindowsPath if re.match(r'^[A-Za-z]:',value)else PurePosixPath
    need(cls(value).is_absolute()and '..'not in cls(value).parts,'Absolute original task root');return cls
def original(request,relative):return str(pathclass(request['original_task_root'])(request['original_task_root']).joinpath(*parts(relative)))
def plan():
    need(digest(PLAN)==PLAN_SHA256,'Pinned all-B1 original source/location plan');d=read(PLAN)
    need(d['schema']=='FINITE2630_B1_CURRENT_LOCATION_SOURCE_PLAN_V1'and d['native']==NATIVE
         and d['actions']==list(ACTIONS)and len(d['source_files'])==83 and d['original_manifest_rows']==82
         and d['relocated_record']==RECORD and len(d['original_absolute_input_map'])==12
         and d['original_numerical_programs_unchanged']is True and d['only_two_json_source_location_metadata_changed']is True
         and same(d['actual_n'],[26,27,28,29,30])and d['rho_strips']==23 and d['exact_rows']==115
         and all(d[k]is False for k in('arithmetic_computed','full_notebook59_completed','parent_acquisitions_verified',
                                      'all_index_conclusion_verified')),'Complete original conditional B1 selection')
    return d
def obtain_assets(directory,*,progress=lambda *a,**k:None):
    directory=ordinary(Path(directory));directory.mkdir(parents=True,exist_ok=True);out={}
    for a in plan()['assets']:
        need(tuple(parts(a['name']))==(a['name'],),'Archive basename');p=ordinary(directory/a['name'])
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));size=0;last=0
            progress('finite2630_b1_source_download_started',archive=a['name'],total_bytes=a['bytes'])
            with urllib.request.urlopen(a['url'])as source,pending.open('wb')as target:
                while block:=source.read(MIB):
                    size+=len(block);need(size<=a['bytes'],'Bounded source transport');target.write(block)
                    if size-last>=16*MIB:progress('finite2630_b1_source_download',archive=a['name'],bytes=size);last=size
            need(size==a['bytes']and digest(pending)==a['sha256'],'Whole immutable source transport');pending.replace(p)
        need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Pinned original archive')
        out[a['name']]=p.resolve()
    return out
def prepare_cache(assets,output):
    d=plan();output=ordinary(Path(output));output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for a in d['assets']:
            p=ordinary(Path(assets[a['name']]));need(p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Whole source archive')
            opened[a['name']]=zipfile.ZipFile(p);base.zip_index(opened[a['name']])
        for name,row in d['source_files'].items():
            p=ordinary(output.joinpath(*parts(name)))
            if not p.exists():
                z=opened[row['archive']];info=z.getinfo(row['member']);need(not info.is_dir()and info.file_size==row['bytes'],'Exact original source member')
                p.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info)as source,p.open('xb')as target:shutil.copyfileobj(source,target,MIB)
            need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every unchanged original byte')
        base.verify_cache(output,d['source_files'])
    finally:
        for z in opened.values():z.close()
    return output.resolve()
def derive(task,request):
    """Typed metadata projection; no original parser, adapter or kernel runs."""
    d=plan();task=Path(task);old_record=read(task/'provenance'/RECORD);old_manifest=read(task/'provenance'/MANIFEST)
    need(digest(task/'provenance'/RECORD)==d['source_files'][RECORD]['sha256']
         and digest(task/'provenance'/MANIFEST)==d['original_manifest_sha256'],'Exact original metadata provenance')
    need(set(old_record['input_sha256'])==set(d['original_absolute_input_map'])and len(old_manifest['files_sha256'])==82,
         'Every exact frozen absolute binding and manifest row')
    record=copy.deepcopy(old_record);bindings={}
    for old,relative in d['original_absolute_input_map'].items():
        need(old_record['input_sha256'][old]==d['source_files'][relative]['sha256'],'Unchanged absolute-source commitment')
        bindings[original(request,'capsule/'+relative)]=old_record['input_sha256'][old]
    record['input_sha256']=bindings
    manifest=copy.deepcopy(old_manifest);manifest['files_sha256'][RECORD]=hashlib.sha256(dump(record)).hexdigest()
    need(same({k:v for k,v in record.items()if k!='input_sha256'},
              {k:v for k,v in old_record.items()if k!='input_sha256'}),'All numerical/profile/control record fields retained')
    need(same({k:v for k,v in manifest.items()if k!='files_sha256'},
              {k:v for k,v in old_manifest.items()if k!='files_sha256'})
         and set(manifest['files_sha256'])==set(old_manifest['files_sha256'])
         and all(pin==old_manifest['files_sha256'][name]for name,pin in manifest['files_sha256'].items()if name!=RECORD),
         'One manifest record hash changes; every other source/statement field retained')
    epoch=dict(schema='FINITE2630_B1_TWO_JSON_LOCATION_EPOCH_V1',source_plan_sha256=PLAN_SHA256,
        original_record_sha256=d['source_files'][RECORD]['sha256'],current_record_sha256=hashlib.sha256(dump(record)).hexdigest(),
        original_manifest_sha256=d['original_manifest_sha256'],current_manifest_sha256=hashlib.sha256(dump(manifest)).hexdigest(),
        bindings=[dict(original_path=old,current_path=original(request,'capsule/'+name),relative=name,
                       unchanged_sha256=d['source_files'][name]['sha256'])for old,name in d['original_absolute_input_map'].items()],
        original_python_unchanged=True,all_non_location_record_fields_unchanged=True,
        only_one_manifest_row_hash_changed=True,historical_acquisitions_promoted=False,
        full_notebook59_completed=False,all_index_conclusion_verified=False)
    return record,manifest,epoch
def prepare(cache,task):
    task=ordinary(Path(task).resolve());need(not task.exists(),'Exclusive fresh two-pass capsule');task.mkdir(parents=True);d=plan()
    for name,row in d['source_files'].items():
        p=ordinary(Path(cache).joinpath(*parts(name)));need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Exact original source cache')
        target=task/('provenance'if name in(RECORD,MANIFEST)else'capsule')/name
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
    request=dict(schema=SCHEMA,original_task_root=str(task),source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),
                 original_sources={n:r['sha256']for n,r in d['source_files'].items()},current_sources={},
                 original_python_unchanged=True,arithmetic_computed=False,full_notebook59_completed=False,
                 parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    record,manifest,epoch=derive(task,request)
    for name,value in((RECORD,record),(MANIFEST,manifest)):
        p=task/'capsule'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(dump(value))
    request['current_sources']={name:digest(task/'capsule'/name)for name in d['source_files']}
    (task/'SOURCES.json').write_bytes(dump(request));(task/'LOCATION_EPOCH.json').write_bytes(dump(epoch));verify_job(task);return request
def verify_job(task):
    task=ordinary(Path(task).resolve());d=plan();request=read(task/'SOURCES.json')
    need(request['schema']==SCHEMA and request['source_plan_sha256']==PLAN_SHA256 and request['source_adapter_sha256']==digest(__file__)
         and same(request['original_sources'],{n:r['sha256']for n,r in d['source_files'].items()})
         and request['original_python_unchanged']is True
         and all(request[k]is False for k in('arithmetic_computed','full_notebook59_completed','parent_acquisitions_verified',
                                             'all_index_conclusion_verified')),'Exact original source epoch, no acquired upstream claim')
    record,manifest,epoch=derive(task,request)
    for name,value in((RECORD,record),(MANIFEST,manifest)):
        need((task/'capsule'/name).read_bytes()==dump(value),'Byte-exact explicit two-JSON projection')
    need(same(read(task/'LOCATION_EPOCH.json'),epoch),'Exact source-location-only epoch ledger')
    expected={n:r['sha256']for n,r in d['source_files'].items()}
    expected.update({RECORD:hashlib.sha256(dump(record)).hexdigest(),MANIFEST:hashlib.sha256(dump(manifest)).hexdigest()})
    need(same(request['current_sources'],expected),'Every current source pin explicitly follows the strict projection')
    actual=set()
    for p in(task/'capsule').rglob('*'):
        ordinary(p)
        if p.is_file():actual.add(p.relative_to(task/'capsule').as_posix())
    need(set(expected)<=actual<=set(expected)|{NATIVE+'/'+n for n in OUTPUTS.values()},'Only declared source files and genuine current outputs')
    for name,pin in expected.items():need(digest(task/'capsule'/name)==pin,'Every unchanged mathematical and current metadata byte')
    for name,pin in manifest['files_sha256'].items():need(expected[name]==pin,'Complete original native manifest graph with one relocated record')
    return request
