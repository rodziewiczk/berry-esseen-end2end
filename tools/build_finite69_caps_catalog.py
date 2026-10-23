"""Locate exact static inputs for a fresh owncaps/CAPS/resource epoch.

Source/ZIP/hash/JSON and the already reviewed deterministic preparation-only
reconstruction. No original mathematical source is imported or executed.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path,PurePosixPath
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from be_replay import finite69_sources as original
from be_replay import finite69_metadata as metadata
from be_replay import finite69_cap_epoch as epoch


def digest_bytes(raw):return hashlib.sha256(raw).hexdigest()
def dump(p):return(json.dumps(p,sort_keys=True,indent=2)+"\n").encode()


def build(asset_paths):
    base=original.catalog()
    public_raw=(ROOT/'proof/finite69_caps_public_assets.json').read_bytes()
    assets=json.loads(public_raw)['assets']
    resources=[r for r in base['parent_jobs']if r['kind']=='resource'
               and r['job_id'].split('.')[0]in('n7','n8','n9')]
    initials=[r for r in base['parent_jobs']if r['kind']=='initial'
              and r['job_id'].split('.')[0]in('n7','n8','n9')]
    original.need(len(resources)==len(initials)==9,'All9literal INITIAL/resource pairs')
    pins={}
    for row in initials+resources:
        for name,pin in row['source_files_sha256'].items():
            original.parts(name)
            original.need(name not in pins or pins[name]==pin,'One unambiguous original source commitment')
            pins[name]=pin
    old_initial_outputs={r['reference']['path']for r in initials}
    generated=set(epoch.DYNAMIC)|old_initial_outputs
    needed={n:p for n,p in pins.items()if n not in generated}
    rows={};contents={};opened=[]
    try:
        for asset in assets:
            path=Path(asset_paths[asset['name']]);original.ordinary(path)
            original.need(path.stat().st_size==asset['bytes']and original.digest(path)==asset['sha256'],
                          'Actual full public source transport '+asset['name'])
            archive=zipfile.ZipFile(path);opened.append(archive)
            by_basename=defaultdict(list)
            for info in archive.infolist():
                if not info.is_dir()and '__MACOSX/'not in info.filename:
                    by_basename[PurePosixPath(info.filename).name].append(info)
            for name,pin in needed.items():
                if name in rows:continue
                descriptor=base['source_files'].get(name,{})
                if 'reconstruction'in descriptor:continue
                if descriptor.get('archive')==asset['name']:
                    info=archive.getinfo(descriptor['member']);raw=archive.read(info)
                    original.need(len(raw)==descriptor['bytes']and digest_bytes(raw)==pin,
                                  'Exact previously sealed candidate/INPUT alias')
                    rows[name]=dict(archive=asset['name'],member=info.filename,bytes=len(raw),sha256=pin)
                    contents[name]=raw;continue
                candidates=by_basename[PurePosixPath(name).name]
                variants=(name,name.removeprefix('work/'))
                candidates=sorted(candidates,key=lambda r:r.filename not in variants)
                for info in candidates:
                    if not any(info.filename==v or info.filename.endswith('/'+v)for v in variants):continue
                    if not 0<=info.file_size<=256*original.MIB:continue
                    raw=archive.read(info)
                    if digest_bytes(raw)!=pin:continue
                    rows[name]=dict(archive=asset['name'],member=info.filename,bytes=len(raw),sha256=pin)
                    contents[name]=raw;break
        for name,pin in needed.items():
            descriptor=base['source_files'].get(name,{})
            if 'reconstruction'not in descriptor:continue
            original.need(descriptor['reconstruction']=='ORIGINAL_POSIX_PREPARED_V1','Only reviewed original preparation reconstruction')
            raw=metadata.reconstruct_prepared(contents[descriptor['source_prepared']],contents[descriptor['candidate']],
                n=descriptor['n'],band=descriptor['band'],source_pins=descriptor['source_pins'])
            original.need(digest_bytes(raw)==pin,'Exact externally committed original preparation bytes')
            rows[name]=dict(descriptor,bytes=len(raw),sha256=pin);contents[name]=raw
        missing=sorted(set(needed)-set(rows))
        original.need(not missing,'Unlocated required static source bytes: '+repr(missing))
        original.need(digest_bytes(contents[epoch.CAPS_PATH])==epoch.ORIGINAL_CAPS_SHA,'Old CAPS is provenance/template only')
        capsule_root='work/cutoff6_20261018/'
        entry_sources=[capsule_root+'fourier/owncaps6_9_v1/'+n for n in('planner.py','protocol.py','run.py')]
        entry_sources +=[capsule_root+'audit/supported_fourier_readback_v1/readback.py',
                        'work/cutoff6_20261020/entry/resource7_9_v2/check_caps.py',
                        'work/cutoff6_20261020/entry/resource7_9_accept_v2/replay.py']
        original.need(all(n in rows for n in entry_sources),'Complete exact numerical/metadata entry sources')
        result=dict(schema='FRESH_FINITE69_CAPS_STATIC_SOURCE_CATALOG_V1',
            base_catalog_sha256=original.CATALOG_SHA256,asset_metadata_sha256=digest_bytes(public_raw),
            metadata_adapter_sha256=original.digest(metadata.__file__),cap_epoch_adapter_sha256=original.digest(epoch.__file__),
            assets=assets,source_files={n:rows[n]for n in sorted(rows)},original_source_pins=pins,
            initial_job_ids=[r['job_id']for r in initials],resource_job_ids=[r['job_id']for r in resources],
            original_initial_outputs_as_provenance_only={n:pins[n]for n in sorted(old_initial_outputs)},
            dynamic_owncap_ancestor_paths=sorted(epoch.DYNAMIC),old_caps_template=epoch.CAPS_PATH,
            old_caps_template_sha256=epoch.ORIGINAL_CAPS_SHA,entry_sources={n:rows[n]['sha256']for n in entry_sources},
            inherited_conditional_run_inputs=[n for n in sorted(rows)if n.startswith('runs/')],
            source_only=True,arithmetic_computed=False,fresh_parent_evidence=False,
            full_finite69_verified=False,all_index_conclusion_verified=False)
        return result
    finally:
        for archive in opened:archive.close()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--asset',action='append',required=True,help='Exact public asset basename=local archive path')
    p.add_argument('--output',type=Path,default=ROOT/'proof/finite69_caps_sources.json');args=p.parse_args()
    paths={}
    for row in args.asset:
        name,path=row.split('=',1);original.need(name not in paths,'Unique transport asset');paths[name]=path
    result=build(paths);raw=dump(result);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(raw)
    print(json.dumps(dict(catalog=args.output.name,files=len(result['source_files']),
        bytes=sum(r['bytes']for r in result['source_files'].values()),sha256=digest_bytes(raw),
        original_mathematical_modules_run=False)))


if __name__=='__main__':main()
