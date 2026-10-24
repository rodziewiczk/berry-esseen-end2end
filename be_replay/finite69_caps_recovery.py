"""Recover one fully executed five-action owncaps stage without rerunning math.

Only the exact saved bundle is admitted. Its original observed ledger and all
execution bytes are preserved; the current pure reader must validate every
source, command, stopped output, result and control before creating a complete
stage ledger and the ordinary completed-stage cache.
"""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import hashlib,shutil,stat,uuid,zipfile
from . import finite69_caps as run,finite69_caps_sources as src,finite69_caps_evidence as ev
from .colab_batch import atomic_json,event

ARCHIVE_NAME='20261023T221209Z-33953096-results.zip'
ARCHIVE_BYTES=7839135
ARCHIVE_SHA256='4f356469cf741ebeb054fbcbb8b93f4264b5064ffa872e33a2b196240265c2a7'
ARCHIVE_RELATIVE='finite69-caps/20261023T221209Z-33953096/'+ARCHIVE_NAME
PREFIX='20261023T221209Z-33953096/jobs/owncaps6_9-9884e332/'
OBSERVED_SHA256='c9ba9809de8036fbc4400428013171f724c0f7fc95eedbbcb595409ec8a38c31'
FILES=235
EXPANDED_BYTES=6486196
JOB='owncaps6_9'


def extract_selected(archive,destination):
    """Preflight and extract only the exact preserved five-action subtree."""
    archive=src.ordinary(Path(archive));destination=src.ordinary(Path(destination).resolve())
    src.need(archive.is_file()and archive.stat().st_size==ARCHIVE_BYTES and src.digest(archive)==ARCHIVE_SHA256,
             'Exact saved complete-execution bundle, not an arbitrary partial result')
    src.need(not destination.exists(),'Exclusive recovered owncaps task')
    with zipfile.ZipFile(archive)as z:
        rows=[r for r in z.infolist()if r.filename.startswith(PREFIX)]
        src.need(len(rows)==FILES,'Exact preserved owncaps subtree census')
        names=set();folded=set();total=0
        for row in rows:
            relative=row.filename[len(PREFIX):];src.parts(relative);mode=row.external_attr>>16
            src.need(not row.is_dir()and not row.flag_bits&1 and not stat.S_ISLNK(mode)
                and stat.S_IFMT(mode)in(0,stat.S_IFREG)and relative not in names and relative.casefold()not in folded
                and 0<=row.file_size<=256*src.MIB,'Unique safe ordinary bounded recovered member')
            names.add(relative);folded.add(relative.casefold());total+=row.file_size
        src.need(total==EXPANDED_BYTES and total<=run.CACHE_BYTES
            and {'SOURCES.json','ACTION_PROGRESS.json','STAGE_OBSERVED.json'}<=names
            and not({'STAGE_COMPLETED.json','RECOVERY_ADMISSION.json'}&names),
            'Original observed-only whole execution, without an invented completion ledger')
        src.need(hashlib.sha256(z.read(PREFIX+'STAGE_OBSERVED.json')).hexdigest()==OBSERVED_SHA256,
                 'Exact unchanged original false observed ledger')
        destination.mkdir(parents=True)
        for row in rows:
            target=destination.joinpath(*src.parts(row.filename[len(PREFIX):]));target.parent.mkdir(parents=True,exist_ok=True)
            with z.open(row)as source,target.open('xb')as output:shutil.copyfileobj(source,output,src.MIB)
    src.need(src.digest(destination/'STAGE_OBSERVED.json')==OBSERVED_SHA256,'Preserved observed bytes after extraction')
    return destination


def complete_recovered(task):
    """Make a completion ledger only after full current-reader validation."""
    task=src.ordinary(Path(task));observed_path=task/'STAGE_OBSERVED.json'
    src.need(not(task/'STAGE_COMPLETED.json').exists()and not(task/'RECOVERY_ADMISSION.json').exists()
             and src.digest(observed_path)==OBSERVED_SHA256,'Exact unmodified observed-only execution')
    request=src.verify_job(task);observed=src.read(observed_path)
    src.need(request['job_id']==JOB and request['kind']=='owncaps'and observed['job_id']==JOB,
             'Only the exact complete five-action owncaps transaction')
    summary=ev.validate_run(task,observed)
    src.need(src.digest(observed_path)==OBSERVED_SHA256,'Current reader does not rewrite original execution bytes')
    admission=ev.saved_observed_admission(task)
    src.need(admission['source_bundle_sha256']==ARCHIVE_SHA256
             and admission['original_observed_sha256']==OBSERVED_SHA256
             and admission['original_execution_bytes_unchanged']is True and admission['mathematical_replay']is False,
             'Explicit current-reader admission, never an impersonated execution')
    (task/'RECOVERY_ADMISSION.json').write_bytes(src.dump(admission))
    packet=dict(schema=ev.COMPLETED,scope=ev.SCOPE,job_id=JOB,
        implementation=observed['implementation'],observed_sha256=OBSERVED_SHA256,
        artifacts=ev.inventory(task),summary=summary,conditional_arithmetic_completed=True,
        **{f:False for f in ev.FLAGS})
    atomic_json(task/'STAGE_COMPLETED.json',packet)
    checked=ev.validate_completed(task)
    src.need(src.digest(observed_path)==OBSERVED_SHA256,'Original observed ledger remains byte-identical after final readback')
    return checked


def recover_saved_owncaps(*,durable_root,work_root='/content/berry-esseen-runs'):
    """Use a validated existing cache or recover the pinned saved transaction."""
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    root=Path(work_root).resolve()/'finite69-caps-recovery'/stamp;root.mkdir(parents=True,exist_ok=False)
    durable_root=Path(durable_root).resolve()
    cache=durable_root/'finite69-caps/completed'/src.CATALOG_SHA256[:16]/JOB
    report=dict(schema='FINITE69_CAPS_SAVED_EXECUTION_RECOVERY_V1',job_id=JOB,
        mathematical_replay=False,conditional_arithmetic_completed=False,**{f:False for f in ev.FLAGS})
    try:
        hit=run.restore_stage(cache,root/'existing',JOB,root=root)
        if hit:
            report.update(state='existing_complete_owncaps_revalidated',export=hit[2],summary=hit[1]['summary'],
                          conditional_arithmetic_completed=True)
        else:
            archive=src.ordinary(durable_root/ARCHIVE_RELATIVE)
            if not archive.exists():
                report.update(state='saved_bundle_unavailable_normal_full_owncaps_execution_required')
            else:
                marker=src.ordinary(archive.with_suffix('.zip.sha256'))
                if marker.exists():
                    src.need(marker.is_file()and marker.stat().st_size<=1024
                        and marker.read_text('ascii')==ARCHIVE_SHA256+'  '+ARCHIVE_NAME+'\n','Actual pinned saved bundle sidecar')
                task=extract_selected(archive,root/'owncaps')
                checked=complete_recovered(task);export=run.save_stage(task,cache)
                report.update(state='recovered_complete_owncaps_current_reader',source_bundle_sha256=ARCHIVE_SHA256,
                    original_observed_sha256=OBSERVED_SHA256,summary=checked['summary'],export=export,
                    conditional_arithmetic_completed=True)
    except BaseException as error:
        report.update(state='saved_owncaps_recovery_rejected_no_acceptance',conditional_arithmetic_completed=False,
                      error=type(error).__name__+': '+str(error))
        raise
    finally:
        atomic_json(root/'RECOVERY.json',report)
        atomic_json(durable_root/'finite69-caps-recovery'/stamp/'RECOVERY.json',report)
        event(root,'finite69_caps_saved_execution_recovery',state=report.get('state'),job_id=JOB,
              conditional_arithmetic_completed=report['conditional_arithmetic_completed'],mathematical_replay=False)
    return report
