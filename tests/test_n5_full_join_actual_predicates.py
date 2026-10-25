"""Optional actual-source ABI fixtures for all12+12 notebook67 regions.

Only byte-pinned original JSON and pure structural/rational evidence predicates
are used. Historical receipts here remain untrusted fixture data: these tests
do not create genuine native executions or establish a current35/67 conclusion.
No numerical producer, acceptor, integrator or search kernel is imported/run.
"""
from copy import deepcopy
from fractions import Fraction as F
import json,os,tempfile,unittest
from pathlib import Path
from be_replay import n5_full_join_semantics as sem,n5_full_join_sources as src
from be_replay import n5_remaining_sources as catalog


CACHE=Path(os.environ.get('BE_N5_ACTUAL_PREDICATE_CACHE',str(src.ROOT/'work/n5-full67-source-cache')))


def resource_fixture(region,cache=CACHE):
 """Run exact original resource readers/controls on original pinned data."""
 partition=src.read(src.ROOT/'proof/remaining_n5_delivery_partition.json',8*src.MIB)
 reference_name=next(row['outputs'][0]for row in partition['original_resource_and_count_semantic_reference_actions']
                     if row['id']=='67.semantic.resource.'+region)
 original=src.read(sem.source(cache,reference_name),32*src.MIB)
 native=src.read(sem.source(cache,original['initial_receipt']),32*src.MIB)
 job=catalog.job(sem.initial_id(region));prepared=src.read(sem.source(cache,job['selection']['prepared']),16*src.MIB)
 candidate=src.read(sem.source(cache,prepared['input_path']),32*src.MIB)
 directory,band,sector=sem.resource_spec(region)
 common=sem.pure_module(cache,sem.BASE+directory+'/common.py')
 if region.startswith('B3-'):
  helper=sem.pure_module(cache,sem.BASE+directory+'/resource_helpers.py',context={'c':common},functions_only=True)
  checker=sem.pure_module(cache,sem.BASE+directory+'/check.py',context={'c':common,'h':helper},functions_only=True)
 else:
  checker=sem.pure_module(cache,sem.BASE+directory+'/check.py',context={'c':common},functions_only=True);helper=checker
 cover=checker.initial(candidate,native,band);rows=[]
 for i in range(100):
  item=original['source_rows'][str(i)];path=sem.source(cache,item['path'])
  src.need(src.digest(path)==item['sha256'],'Actual reference resource row is independently pinned')
  row=src.read(path,16*src.MIB);src.need(type(row['index'])is int and row['index']==i,'Every original complete probability panel')
  rows.append(row)
 endpoints=[]
 if region.startswith('B2-'):
  endpoints=[i for job in catalog.jobs()if job['kind']=='resource'
             and job['selection']['initial_parent']==sem.initial_id(region)
             and job['selection']['case'].endswith('_endpoint')for i in job['selection']['indices']]
 if region.startswith('B3-'):summary=helper.resources(rows,cover,band,range(100))
 elif region.startswith('B2-'):summary=checker.resources(rows,cover,band,endpoints)
 else:summary=checker.resources(rows,cover,band)
 src.need(summary['excluded']==original['excluded']and summary['retained']==original['retained'],
          'Actual resource ABI reproduces the exact original full partition')
 namespace=dict(checker.__dict__,c=common,h=helper,z=candidate,ia=native,acq=native,b=band,band=band,sector=sector,
                rows=rows,cover=cover,summary=summary,endpoint_indices=endpoints,rl=F(original['rho_interval'][0]),F=F,json=json,deepcopy=deepcopy)
 controls=sem.resource_controls(cache,sem.BASE+directory+'/check.py',namespace,original['negative_controls'])
 beta=original.get('beta_interval',native.get('beta_interval'))
 return dict(region=region,summary=summary,rows=rows,source_rows=original['source_rows'],
             rho=original['rho_interval'],beta=beta,controls=controls,
             fixture_scope='ORIGINAL_REFERENCE_DATA_PREDICATES_ONLY_NO_FRESH_EXECUTION')


def count_frames(cache=CACHE):
 frames={}
 for job in catalog.jobs():
  if job['kind']!='count':continue
  name=job['source_capsule']+'/COUNT_ACCEPTED.json';path=sem.source(cache,name);pin=src.digest(path)
  frames[job['job_id']]=dict(task=cache,row=job,checked=dict(summary=dict(references=[dict(path=name,sha256=pin)]),
                          stage_result_sha256=pin,fixture_scope='UNTRUSTED_OLD_SOURCE_REFERENCE_NOT_CURRENT_ACCEPTANCE'))
 src.need(len(frames)==295,'All original source COUNT fixtures')
 return frames


@unittest.skipUnless(CACHE.is_dir(),'Optional actual-source predicate cache is absent; no archive/math is downloaded by this fixture')
class ActualPredicates(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.frames=count_frames();cls.resources={}
  scratch=src.ROOT/'work/n5-full67-predicate-fixtures';scratch.mkdir(parents=True,exist_ok=True)
  cls.temporary=tempfile.TemporaryDirectory(dir=scratch);cls.mirror=Path(cls.temporary.name)

 @classmethod
 def tearDownClass(cls):cls.temporary.cleanup()

 def test_all12_resource_readers_and_original_mutations(self):
  for region in sem.CASES:
   with self.subTest(region=region):
    result=resource_fixture(region);self.resources[region]=result
    self.assertEqual(sorted(result['summary']['excluded']+result['summary']['retained']),list(range(100)))
    self.assertEqual(result['fixture_scope'],'ORIGINAL_REFERENCE_DATA_PREDICATES_ONLY_NO_FRESH_EXECUTION')

 def test_all12_count_readers_295_forests_and_original_mutations(self):
  results=[]
  for region in sem.CASES:
   with self.subTest(region=region):
    resource=self.resources.get(region)or resource_fixture(region)
    result=sem.count_region(region,resource,self.frames,CACHE,self.mirror,prepare=True)
    self.assertEqual(result['retained'],resource['summary']['retained']);results.append(result)
  if len(results)==12:
   self.assertEqual(sum(len(row['retained'])for row in results),295)
   self.assertEqual(sum(row['count_roots']for row in results),1770)
   self.assertEqual(sum(row['count_totals']['leaves']for row in results),75178)
   type(self).count_results=results

 def test_final_actual_12_region_census_corner_complement_union_and_mutations(self):
  from be_replay import n5_full_join_evidence as evidence
  if getattr(type(self),'count_results',None)is None:self.test_all12_count_readers_295_forests_and_original_mutations()
  results=getattr(type(self),'count_results',[]);self.assertEqual(len(results),12)
  final=evidence.final_functions(CACHE,self.mirror)
  lower=final.constants();self.assertGreater(lower,sem.COUNT_TARGET);rows=[]
  for region,result in zip(sem.CASES,results):
   if region in('B0','BN'):
    rho=[F(1),F(11,10)]if region=='B0'else[F(11,10),F(23,20)];rows.append(final.count_case(result,region,rho))
   elif region.startswith('B2-'):
    sector=int(region[-1]);rows.append(final.count_case(result,'B2',*final.sector2(sector),sector=sector))
   else:
    case=region[3:];rows.append(final.count_case(result,'B3',*final.sector3(case),case=case))
  corner=src.read(sem.source(CACHE,sem.BASE+'audit/gapfree5_readback_v1/READBACK.json'),32*src.MIB)
  complement=src.read(sem.source(CACHE,sem.BASE+'audit/complement5_readback_v1/READBACK.json'),32*src.MIB)
  final.corner(corner);final.complement(complement)
  checks=final.union([final.sector2(i)for i in range(4)],[F(23,20),F(237,200)],[-final.B2,final.B2])
  rectangles=[final.sector3(case)for case in('S0','S2','T0','T1','T2','T3lower')]+[([F(477,400),F(6,5)],[F(17,50),final.B3])]
  checks+=final.union(rectangles,[F(237,200),F(6,5)],[-final.B3,final.B3])
  self.assertGreater(checks,0);self.assertEqual(sum(r['retained']for r in rows),295);self.assertEqual(sum(r['excluded']for r in rows),905)
  self.assertEqual(sum(r['roots']for r in rows),1770);self.assertEqual(sum(r['leaves']for r in rows),75178)
  controls=evidence.composition_mutations(CACHE,final,results,corner,complement)
  self.assertGreaterEqual(len(controls),20)

 def test_all27_initial_resource_parent_profile_edges(self):
  rules=sem.parent_rules();facts=[]
  groups=(
   (rules.support_facts,['high/support_v1/REPLAY_CHECKED.json','high/support_v2/REPLAY_CHECKED.json','high/support_A0_v1/REPLAY_CHECKED.json']),
   (rules.high_facts,['high/high5_v1/HIGH_CHECKED.json','high/high5_eta_v1/HIGH_CHECKED.json']),
   (rules.owncap_facts,['high/owncaps5_v3/OWNCAPS_CHECKED.json','high/owncap_B3_ext_v1/OWNCAPS_CHECKED.json']))
  for parser,names in groups:
   for name in names:
    path=sem.source(CACHE,sem.BASE+name);facts.extend(parser(src.read(path,32*src.MIB),src.digest(path)))
  path=sem.source(CACHE,'work/cutoff6_20261018/audit/auxiliary5_readback_v1/RESULT.json')
  global_fact=rules.GlobalOwncapFact(rules.global_coarse429(src.read(path)),src.digest(path))
  profiles={};initial_edges=[];resource_edges=[]
  for job in catalog.jobs():
   if job['kind']!='initial':continue
   selected=job['selection'];prepared=src.read(sem.source(CACHE,selected['prepared']))
   candidate=src.read(sem.source(CACHE,prepared['input_path']),32*src.MIB);profile=candidate['profile'];profiles[job['job_id']]=profile
   edge=rules.entails_profile(profile,selected['high'],selected['owncap'],facts,global_fact)
   self.assertEqual(edge['whole_child_rho'],[profile['invariants']['rho_lo'],profile['invariants']['rho']]);initial_edges.append(edge)
  for job in catalog.jobs():
   if job['kind']!='resource':continue
   selected=job['selection'];prepared=src.read(sem.source(CACHE,selected['prepared']))
   accepted=src.read(sem.source(CACHE,selected['outputs'][-1]),32*src.MIB);scoped=prepared.get('source_job',prepared)
   profile=deepcopy(profiles[selected['initial_parent']]);radius=accepted.get('radius',scoped.get('radius',profile['radius']))
   profile['radius']=radius
   for key in('radius_minus','radius_plus'):
    if key in profile:profile[key]=radius
   edge=rules.entails_profile(profile,selected['high'],selected['owncap'],facts,global_fact)
   self.assertEqual(edge['whole_child_rho'],accepted['rho_interval']);resource_edges.append(edge)
  self.assertEqual((len(initial_edges),len(resource_edges)),(12,15))


if __name__=='__main__':unittest.main()
