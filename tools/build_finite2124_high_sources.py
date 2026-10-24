"""Freeze exact source bytes for58A; never import original mathematics."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
PREFIX='continuation_cutoff20_20261016/'
NATIVE=PREFIX+'root/bridge21_24_high_rho_v1'
REVIEW=PREFIX+'analytic/BRIDGE_HIGH_RHO_SOURCE_REVIEW.json'
ASSETS=[dict(name='cutoff20_20261016.zip',bytes=31681776,
 sha256='b1dd7e730187f62142faa1e82eff5a9fd13a879e933a2fafbd22af8a4709ef83'),
 dict(name='continuation_cutoff20_20261016_final.zip',bytes=45213423,
 sha256='1e3de8f03c28816d36258ddd84ee7f29166622b2390d5c3457eb1b193ef608b7')]

def sha(raw):return hashlib.sha256(raw).hexdigest()
def build(directory):
    opened={}
    try:
        for row in ASSETS:
            path=Path(directory)/row['name']
            assert path.stat().st_size==row['bytes']and sha(path.read_bytes())==row['sha256']
            opened[row['name']]=zipfile.ZipFile(path)
        def locate(name,pin=None):
            found=[]
            for archive,z in opened.items():
                if name in z.namelist():
                    raw=z.read(name)
                    if pin is None or sha(raw)==pin:
                        found.append((dict(archive=archive,member=name,bytes=len(raw),sha256=sha(raw)),raw))
            assert found and all(x[0]['sha256']==found[0][0]['sha256']for x in found),name
            return found[0]
        review_row,raw=locate(REVIEW);review=json.loads(raw)
        graph=dict(review['files_sha256']);graph[REVIEW]=review_row['sha256']
        rows={name:locate(name,pin)[0]for name,pin in sorted(graph.items())}
        freeze=json.loads(locate(NATIVE+'/FROZEN_SOURCES.json')[1])
        assert all(rows[n]['sha256']==h for n,h in freeze['files_sha256'].items())
        assert len(rows)==40 and rows[NATIVE+'/check.py']['sha256']=='66e161ed48acb1b51d818a94d878d7c71d4ee521c51282d43e264afb2a8adaf4'
        return dict(schema='FINITE2124_HIGHRHO_SOURCE_PLAN_V1',
            scope='ACTUAL21_24_CONDITIONAL_HIGH_RHO_SUPPORT_ONLY',
            assets=[r|dict(url='https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/download/cutoff20-sources-2026-10-17/'+r['name'])for r in ASSETS],
            source_files=rows,source_bytes=sum(r['bytes']for r in rows.values()),
            native=NATIVE,review=REVIEW,actions=['construct','accept'],actual_n=[21,22,23,24],
            excluded_rho=['9/8','infinity'],support_radius='3',support_rho_upper='6/5',
            negative_controls=10,historical_fourier_replayed=False,original_source_programs_unchanged=True,
            original_manifests_and_reviews_unchanged=True,arithmetic_computed=False,
            full_actual20_24_verified=False,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    finally:
        for z in opened.values():z.close()

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive-directory',type=Path,required=True)
    p.add_argument('--output',type=Path,default=ROOT/'proof/finite2124_high_source_plan.json');a=p.parse_args()
    raw=(json.dumps(build(a.archive_directory),sort_keys=True,indent=2)+'\n').encode()
    a.output.write_bytes(raw)
    print(json.dumps(dict(files=40,plan_sha256=sha(raw),original_math_executed=False)))
