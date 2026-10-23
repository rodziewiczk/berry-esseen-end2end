"""Derive fixed parent replay input/metadata selection without kernel imports."""
from __future__ import annotations
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from be_replay import finite69_sources as base


def dump(path,value):
    raw=(json.dumps(value,indent=2,sort_keys=True)+"\n").encode()
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def build():
    d=base.catalog();selected=[r for r in d["parent_jobs"]if r["job_id"].startswith("n6.")or r["kind"]=="initial"]
    base.need(len(selected)==50 and len([r for r in selected if r["job_id"].startswith("n6.")])==41,
              "All fixed41 n6 and9 n7--9 INITIAL actions")
    output_jobs={r["reference"]["path"]:r["job_id"]for r in selected}
    rank={"initial":0,"local_initial":1,"resource":2,"local_resource":3}
    selected.sort(key=lambda r:(rank[r["kind"]],r["job_id"]))
    rows=[];seen=set()
    for original in selected:
        row=copy.deepcopy(original)
        base.need(not row["missing_archived_inputs"]and row["original_runtime_source_closure_complete"],"Exact full source-available parent closure")
        row["lane"]="n6"if row["job_id"].startswith("n6.")else"initial7_9"
        row["direct_fresh_dependencies"]=[dict(path=p,job_id=output_jobs[p],sha256=row["source_files_sha256"][p])
                                          for p in row["conditional_receipt_inputs"]if p in output_jobs]
        base.need(all(edge["job_id"]in seen for edge in row["direct_fresh_dependencies"]),"Every fresh metadata dependency precedes its child")
        row["reference"]["candidate_only"]=True
        rows.append(row);seen.add(row["job_id"])
    names={name for row in rows for name in row["source_files_sha256"]}
    files={name:d["source_files"][name]for name in sorted(names)}
    result=dict(schema="FIXED_FINITE69_PARENT_SOURCE_CATALOG_V1",base_catalog_sha256=base.CATALOG_SHA256,
        metadata_adapter_sha256=base.digest(ROOT/"be_replay/finite69_metadata.py"),assets=d["assets"],jobs=rows,
        source_files=files,lanes=dict(n6=dict(jobs=41,initial=4,local_initial=17,resource=3,local_resource=17),
                                    initial7_9=dict(jobs=9,initial=9)),
        remaining_obligations=["Fresh full n7--9 resources require a separately reviewed owncaps/CAPS metadata epoch.",
            "All original HIGH/owncap/support/Fourier and global predecessor statements remain conditional inputs.",
            "Full same-witness count interfaces, regional covers and final theorem composition remain separate."],
        mathematical_modules_imported=False,arithmetic_computed=False,parent_acquisitions_verified=False,
        all_index_conclusion_verified=False)
    output=ROOT/"proof/finite69_parent_sources.json"
    print(json.dumps(dict(path=output.relative_to(ROOT).as_posix(),sha256=dump(output,result),jobs=len(rows),files=len(files),
                         reconstructed_prepared_files=sum("reconstruction"in row for row in files.values()),arithmetic_computed=False)))


if __name__=="__main__":build()
