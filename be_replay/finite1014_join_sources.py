"""Sealed original56I control sources and explicit data-only graph epochs."""
from __future__ import annotations
from pathlib import Path
import shutil,stat,zipfile
from . import finite1014_kappa_sources as base
from . import finite1014_join_epoch as epoch
ROOT,MIB=base.ROOT,base.MIB
need,digest,read,dump,ordinary,parts=base.need,base.digest,base.read,base.dump,base.ordinary,base.parts
PLAN=ROOT/'proof/finite1014_join_source_plan.json'
PLAN_SHA256='ef63834f592f8b036b30296a9f9d1f7e407f4f815082335aa43561aa6b4d1205'
SCHEMA='SEALED_FINITE1014_JOIN_CONTROL_SOURCES_V1'
META='CURRENT_CONTROL_METADATA_EPOCH.json'
DEPENDENCIES=('work/cutoff10_20261018/audit/range10_v1/CHECKED.json',
 'work/cutoff10_20261018/audit/signed_low_review_v1/CHECKED.json',
 'work/cutoff10_20261018/audit/resource_count_port_review_v2/CHECKED.json')


def plan():
 need(digest(PLAN)==PLAN_SHA256,'Pinned full56Icontrol source plan');d=read(PLAN,4*MIB)
 need(d['schema']=='FINITE1014_JOIN_CONTROLS_SOURCE_PLAN_V1'and len(d['jobs'])==10
  and len(d['source_files'])==2762 and len(d['unavailable_historical_inputs'])==30
  and d['original_python_unchanged']is True and d['mathematical_fixture_fields_unchanged']is True
  and all(d[k]is False for k in('historical_captures_fabricated','full_finite10_14_verified','arithmetic_computed','parent_acquisitions_verified','all_index_conclusion_verified')),
  'Ten full bounded calls with explicit unacquired history and no theorem promotion')
 return d


def jobs():return plan()['jobs']
def job(job_id):
 rows=[r for r in jobs()if r['job_id']==job_id];need(len(rows)==1,'Fixed selected56Icontrol');return rows[0]


def obtain_assets(directory,*,progress=lambda *a,**k:None):
 # This unchanged transport reads only the two already published source assets.
 from .finite1014_core_sources import obtain_assets as obtain
 return obtain(directory,progress=progress)


def _preflight(z):
 seen=set()
 for info in z.infolist():
  name=info.filename.rstrip('/')if info.is_dir()else info.filename;parts(name)
  folded=name.casefold();need(folded not in seen,'No duplicate/case-colliding archive member');seen.add(folded)
  kind=stat.S_IFMT(info.external_attr>>16);need(kind in(0,stat.S_IFREG,stat.S_IFDIR)and not info.flag_bits&1,'Ordinary unencrypted source archive')


def prepare_cache(assets,output,*,progress=lambda *a,**k:None):
 d=plan();output=ordinary(output);output.mkdir(parents=True,exist_ok=True);opened={}
 rows=d['source_files']|d['reference_files']
 try:
  for a in d['assets']:
   p=ordinary(assets[a['name']]);need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Actual pinned archive transport')
   opened[a['name']]=zipfile.ZipFile(p);_preflight(opened[a['name']])
  for i,(name,row)in enumerate(rows.items()):
   p=ordinary(output.joinpath(*parts(name)))
   if not p.exists():
    p.parent.mkdir(parents=True,exist_ok=True)
    if 'vendor_file'in row:shutil.copyfile(ROOT.joinpath(*parts(row['vendor_file'])),p)
    else:
     info=opened[row['archive']].getinfo(row['member']);need(not info.is_dir()and info.file_size==row['bytes']and row['bytes']<=16*MIB,'Bounded exact selected member')
     with opened[row['archive']].open(info)as source,p.open('xb')as dest:shutil.copyfileobj(source,dest,MIB)
   need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every actual original input byte')
   if i%100==0:progress('finite1014_join_source_cache',files=i,total=len(rows),arithmetic_computed=False)
 finally:
  for z in opened.values():z.close()
 return output.resolve()


def original_inputs(row):
 out=dict(plan()['source_files'])
 if not row['read_only_record']:out.pop(row['output'],None)
 for name in row['generated_sources']:out.pop(name,None)
 if row['read_only_record']:out[row['output']]=plan()['reference_files'][row['reference']]
 return out


def _metadata(task,row,original,current):
 docs={n:ordinary(Path(task)/'provenance/original-metadata'/n).read_bytes()for n in row['metadata_documents']}
 need(set(docs)<=set(original),'Only explicit source-graph metadata documents')
 return epoch.derive_metadata_epoch(docs,{n:r['sha256']for n,r in original.items()},current,
  plan()['unavailable_historical_inputs'],allowed_overrides=sorted(n for n in DEPENDENCIES if n in current and current[n]!=original[n]['sha256']))


def prepare(job_id,cache,task,*,dependencies=None):
 row=job(job_id);d=plan();cache=ordinary(Path(cache).resolve());task=ordinary(Path(task).resolve())
 need(not task.exists(),'Fresh private control task');original=original_inputs(row);dependencies={}if dependencies is None else dependencies
 need(type(dependencies)is dict and set(dependencies)<=set(DEPENDENCIES)&set(original),'Only actual prior-control output overrides')
 (task/'capsule').mkdir(parents=True);(task/'provenance').mkdir()
 for name,record in original.items():
  source=cache.joinpath(*parts(row['reference']if row['read_only_record']and name==row['output']else name));ordinary(source)
  need(source.is_file()and source.stat().st_size==record['bytes']and digest(source)==record['sha256'],'Pinned source cache input')
  dest=task/'capsule'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
 shutil.copyfile(cache/row['reference'],task/'provenance/reference.json')
 for name in row['metadata_documents']:
  dest=task/'provenance/original-metadata'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(task/'capsule'/name,dest)
 dependency_pins={}
 for name,path in dependencies.items():
  p=ordinary(path);need(p.is_file()and p.stat().st_size<=16*MIB,'Bounded actual prior-control output');shutil.copyfile(p,task/'capsule'/name);dependency_pins[name]=digest(p)
 current={n:digest(task/'capsule'/n)for n in original};derived=_metadata(task,row,original,current)
 for name,raw in derived['derived'].items():(task/'capsule'/name).write_bytes(raw)
 (task/META).write_bytes(dump(derived['ledger']))
 sources={n:dict(bytes=(task/'capsule'/n).stat().st_size,sha256=digest(task/'capsule'/n))for n in original}
 request=dict(schema=SCHEMA,job_id=job_id,source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),
  metadata_adapter_sha256=digest(epoch.__file__),original_task_root=str(task),original_sources=original,sources=sources,
  dependency_files_sha256=dependency_pins,metadata_epoch_sha256=digest(task/META),
  original_python_unchanged=True,mathematical_fixture_fields_unchanged=True,historical_capture_impersonated=False,
  arithmetic_computed=False,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
 (task/'SOURCES.json').write_bytes(dump(request));verify(task);return request,row


def verify(task):
 task=ordinary(Path(task).resolve());request=read(task/'SOURCES.json',8*MIB);row=job(request['job_id']);original=original_inputs(row)
 need(request['schema']==SCHEMA and request['source_plan_sha256']==PLAN_SHA256
  and request['source_adapter_sha256']==digest(__file__)and request['metadata_adapter_sha256']==digest(epoch.__file__)
  and epoch.same(request['original_sources'],original)and type(request['original_task_root'])is str
  and request['original_python_unchanged']is True and request['mathematical_fixture_fields_unchanged']is True
  and all(request[k]is False for k in('historical_capture_impersonated','arithmetic_computed','parent_acquisitions_verified','all_index_conclusion_verified')),
  'Exact current original source/control epoch')
 dependencies=request['dependency_files_sha256'];need(type(dependencies)is dict and set(dependencies)<=set(DEPENDENCIES)&set(original),'Declared current prior-control dependencies')
 current={n:(dependencies[n]if n in dependencies else r['sha256'])for n,r in original.items()};derived=_metadata(task,row,original,current)
 need((task/META).read_bytes()==dump(derived['ledger'])and digest(task/META)==request['metadata_epoch_sha256'],'Exact reversible source-graph metadata epoch')
 expected={n:dict(bytes=len(derived['derived'][n]),sha256=epoch.digest(derived['derived'][n]))if n in derived['derived']else
  dict(bytes=(task/'capsule'/n).stat().st_size if n in dependencies else r['bytes'],sha256=current[n])for n,r in original.items()}
 need(epoch.same(request['sources'],expected),'Exactly original inputs plus declared metadata/current-control hashes')
 for name,record in expected.items():
  p=ordinary(task/'capsule'/name);need(p.is_file()and p.stat().st_size==record['bytes']and digest(p)==record['sha256'],'Sealed actual control input: '+name)
 for name in row['metadata_documents']:
  p=ordinary(task/'provenance/original-metadata'/name);need(p.is_file()and digest(p)==original[name]['sha256'],'Exact preserved original metadata document')
 need(digest(task/'provenance/reference.json')==plan()['reference_files'][row['reference']]['sha256'],'Original mathematical/control reference bytes')
 found={p.relative_to(task/'capsule').as_posix()for p in(task/'capsule').rglob('*')if p.is_file()};allowed=set(expected)|set(row['generated_sources'])|{row['output']}
 need(set(expected)<=found<=allowed,'No unbound capsule file or historical successful-capture substitution')
 for p in(task/'capsule').rglob('*'):ordinary(p)
 for name in row['generated_sources']:
  if name in found:need(digest(task/'capsule'/name)==row['generated_sources'][name],'Generated copied helper retains original exact bytes')
 return request,row
