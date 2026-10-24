"""Source-only exact closure for57D; never imports original mathematical modules."""
from __future__ import annotations
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NATIVE='work/cutoff15_20261017/analytic/initial15_v1'
AUDIT='work/cutoff15_20261017/analytic/support15_19_replay_v1'
CANDIDATE_SHA='e34d47801d087252f179c2ba033a7289fc3cf03213f3dd92ce69db0b42388e5d'
def sha(b):return hashlib.sha256(b).hexdigest()
def build(combined,old20):
 assets={a['name']:a for a in json.loads((ROOT/'proof/finite69_caps_sources.json').read_bytes())['assets']}
 paths={'cutoff5_10_15.zip':Path(combined),'cutoff20_20261016.zip':Path(old20)}
 for name,p in paths.items():
  assert p.stat().st_size==assets[name]['bytes']and sha(p.read_bytes())==assets[name]['sha256']
 with zipfile.ZipFile(combined)as z,zipfile.ZipFile(old20)as z20:
  candidate=z.read(NATIVE.removeprefix('work/')+'/SUPPORT15_19_BRIDGE.json');assert sha(candidate)==CANDIDATE_SHA
  graph=json.loads(candidate)['files_sha256']
  rows={};inputs=dict(graph)
  for name in(NATIVE+'/COPIED_SOURCES.json',AUDIT+'/check.py',AUDIT+'/PROOF.txt'):
   inputs[name]=sha(z.read(name.removeprefix('work/')))
  for path,pin in sorted(inputs.items()):
   member=path.removeprefix('work/');matches=[]
   for name,archive in(('cutoff5_10_15.zip',z),('cutoff20_20261016.zip',z20)):
    if member in archive.namelist():
     b=archive.read(member)
     if sha(b)==pin:matches.append(dict(archive=name,member=member,bytes=len(b),sha256=pin))
   assert matches,path
   rows[path]=matches[0]
  copied=json.loads(z.read(NATIVE.removeprefix('work/')+'/COPIED_SOURCES.json'))
  assert len(copied)==11 and len(graph)==23 and len(rows)==26
  return dict(schema='FINITE1519_FULL_RAY_SUPPORT_SOURCE_PLAN_V1',scope='UNCHANGED_CONDITIONAL_FULL_RAY_SUPPORT15_19_ONLY',
   assets=[assets[n]for n in paths if any(r['archive']==n for r in rows.values())],source_files=rows,
   original_candidate_sha256=CANDIDATE_SHA,original_candidate_source_graph=graph,
   original_constructor_sha256=inputs[NATIVE+'/support_bridge.py'],original_replay_sha256=inputs[AUDIT+'/check.py'],
   n=list(range(15,20)),rho_interval=['1','33/25'],radius='3',full_ray_rows=10,malformed_controls=14,parser_controls=2,
   original_candidate_is_not_an_execution_input=True,original_mathematical_programs_unchanged=True,
   arithmetic_computed=False,support_acquisition_verified=False,full_notebook57_completed=False,
   parent_acquisitions_verified=False,all_index_conclusion_verified=False)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--combined',type=Path,required=True);p.add_argument('--old20',type=Path,required=True)
 p.add_argument('--output',type=Path,default=ROOT/'proof/finite1519_support_source_plan.json');a=p.parse_args();d=build(a.combined,a.old20)
 a.output.write_bytes((json.dumps(d,sort_keys=True,indent=2)+'\n').encode());print(sha(a.output.read_bytes()),len(d['source_files']))
