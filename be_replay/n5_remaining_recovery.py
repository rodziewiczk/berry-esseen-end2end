"""Recover one actual complete INITIAL from its wrapper-failed saved bundle.

No mathematical program is imported or run. Both old stage ledgers, every
source, launch, capture, result and control are revalidated by the current
pure reader before a normal completed-stage cache ZIP is created.
"""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import shutil,stat,uuid,zipfile
from . import n5_remaining as run,n5_remaining_sources as src,n5_remaining_evidence as ev
from .colab_batch import atomic_json,event

ARCHIVE_NAME='20261023T194522Z-6560588f-results.zip'
ARCHIVE_SHA256='77fdf3b9cc40070ad3350250960e0896efc91df713debda79222e227938f40c4'
ARCHIVE_BYTES=5098913
ARCHIVE_RELATIVE='n5-remaining/20261023T194522Z-6560588f/'+ARCHIVE_NAME
PREFIX='20261023T194522Z-6560588f/jobs/initial-b0-9b65f7f0/'

def extract_selected(archive,destination):
    """Contained bounded extraction of the exact selected complete task only."""
    archive=src.ordinary(Path(archive));destination=src.ordinary(Path(destination).resolve())
    src.need(archive.is_file()and archive.stat().st_size==ARCHIVE_BYTES and src.digest(archive)==ARCHIVE_SHA256,
             'Exact actual saved wrapper-failed bundle, not arbitrary recovery input')
    src.need(not destination.exists(),'Exclusive recovered task')
    with zipfile.ZipFile(archive)as z:
        rows=[r for r in z.infolist()if r.filename.startswith(PREFIX)]
        src.need(0<len(rows)<=run.CACHE_FILES,'Bounded original complete INITIAL subtree')
        seen=set();total=0
        for row in rows:
            relative=row.filename[len(PREFIX):];src.parts(relative);mode=row.external_attr>>16
            src.need(not row.is_dir()and not row.flag_bits&1 and not stat.S_ISLNK(mode)
                     and stat.S_IFMT(mode)in(0,stat.S_IFREG)and relative.casefold()not in seen
                     and 0<=row.file_size<=128*src.MIB,'Unique bounded ordinary recovered member')
            seen.add(relative.casefold());total+=row.file_size
        src.need(total<=run.CACHE_BYTES and {'job_source.json','stage_observed.json','stage_completed.json'}<=seen,
                 'Original whole completed job ledgers, not a numerical checkpoint')
        destination.mkdir(parents=True)
        for row in rows:
            target=destination.joinpath(*src.parts(row.filename[len(PREFIX):]));target.parent.mkdir(parents=True,exist_ok=True)
            with z.open(row)as source,target.open('xb')as dest:shutil.copyfileobj(source,dest,src.MIB)
    return destination

def recover_saved_initial(*,durable_root,work_root='/content/berry-esseen-runs'):
    row=src.job('initial.B0');stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root=Path(work_root).resolve()/'n5-wrapper-recovery'/stamp;root.mkdir(parents=True,exist_ok=False)
    cache=Path(durable_root).resolve()/'n5-remaining/completed'/src.CATALOG_SHA256[:16]/run.slug(row['job_id'])
    existing=run.restore_stage(cache,root/'existing',row,log_root=root)
    if existing:
        report=dict(state='existing_complete_initial_revalidated',job_id=row['job_id'],export=existing[2],mathematical_replay=False)
    else:
        archive=Path(durable_root).resolve()/ARCHIVE_RELATIVE
        if not archive.exists():
            report=dict(state='saved_bundle_unavailable_normal_initial_replay_required',job_id=row['job_id'],mathematical_replay=False)
        else:
            marker=archive.with_suffix('.zip.sha256')
            if marker.exists():
                src.ordinary(marker);src.need(marker.is_file()and marker.stat().st_size<=1024
                    and marker.read_text('ascii')==ARCHIVE_SHA256+'  '+ARCHIVE_NAME+'\n','Actual saved bundle sidecar')
            task=extract_selected(archive,root/'initial')
            checked=ev.validate_completed(task);src.need(checked['job_id']==row['job_id'],'Exact original full INITIAL.B0')
            exported=run.save_stage(task,cache)
            report=dict(state='recovered_complete_initial_B0',job_id=row['job_id'],source_bundle_sha256=ARCHIVE_SHA256,
                        summary=checked['summary'],export=exported,mathematical_replay=False)
    report.update(native_arithmetic_accepted=False,fresh_parent_fact_joins_verified=False,full_n5_verified=False,all_index_conclusion_verified=False)
    atomic_json(root/'RECOVERY.json',report)
    durable=Path(durable_root).resolve()/'n5-wrapper-recovery'/stamp;atomic_json(durable/'RECOVERY.json',report)
    event(root,'n5_completed_initial_recovery',state=report['state'],job_id=row['job_id'],mathematical_replay=False)
    return report
