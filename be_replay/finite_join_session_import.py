"""Bounded full-session ZIP transport; semantic acceptance is a separate reader.

Successful filenames/flags are never accepted as evidence. The supplied pure
validator must reconstruct the entire source-bound finite session after
relocation, including all genuine upstream stopped executions.
"""
from pathlib import Path
import shutil,stat,uuid,zipfile
from .finite1519_join_control_sources import ordinary,child,digest,need,MIB
from .finite1039_sources import parts

MAX_ZIP_BYTES=2*1024**3
MAX_TOTAL_BYTES=12*1024**3
MAX_MEMBERS=250000


def members(archive,root_name):
    need(type(root_name)is str and len(parts(root_name))==1,'One literal final session root')
    rows=archive.infolist();need(0<len(rows)<=MAX_MEMBERS,'Bounded complete session inventory')
    seen=set();total=0;names=set()
    for row in rows:
        p=parts(row.filename);mode=row.external_attr>>16
        need(len(p)>=2 and p[0]==root_name and not row.is_dir()and not row.flag_bits&1
             and stat.S_IFMT(mode)in(0,stat.S_IFREG)and row.filename.casefold()not in seen
             and 0<=row.file_size<=128*MIB,'One contained ordinary unique bounded full-session member')
        seen.add(row.filename.casefold());names.add(row.filename);total+=row.file_size
    need(total<=MAX_TOTAL_BYTES and root_name+'/SESSION_RESULT.json'in names,'Entire bounded actual session result and artifacts')
    return rows


def restore_latest(directory,destination,*,validator,log=lambda *a,**k:None):
    directory=ordinary(directory);destination=ordinary(destination)
    if not directory.exists():return None
    need(directory.is_dir(),'Finite session export directory')
    candidates=sorted(directory.glob('*/*-results.zip'),reverse=True)[:16]
    for archive_path in candidates:
        try:
            ordinary(archive_path);sidecar=ordinary(archive_path.with_suffix('.zip.sha256'))
            need(archive_path.is_file()and archive_path.stat().st_size<=MAX_ZIP_BYTES and sidecar.is_file()
                 and sidecar.stat().st_size<=1024,'Bounded actual full-session archive and sidecar')
            pin=digest(archive_path)
            need(sidecar.read_text('ascii')==pin+'  '+archive_path.name+'\n','Exact actual full-session ZIP SHA')
            root_name=archive_path.name.removesuffix('-results.zip')
            outer=destination/('session-restored-'+uuid.uuid4().hex[:8])
            with zipfile.ZipFile(archive_path)as archive:
                rows=members(archive,root_name);outer.mkdir(parents=True,exist_ok=False)
                for row in rows:
                    out=child(outer,row.filename);out.parent.mkdir(parents=True,exist_ok=True)
                    with archive.open(row)as source,out.open('xb')as target:shutil.copyfileobj(source,target,MIB)
            task=outer/root_name;checked=validator(task)
            log('finite_join_full_session_revalidated',path=str(archive_path),sha256=pin,numerical_replays_skipped=True)
            return task,checked,dict(path=str(archive_path),sha256=pin)
        except Exception as error:
            log('finite_join_full_session_rejected',path=str(archive_path),error=type(error).__name__+': '+str(error))
    return None
