"""Seal notebook67's original source/data closures; never execute originals."""
from __future__ import annotations
import argparse, ast, hashlib, json, zipfile
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[1]
PARTITION=ROOT/'proof/remaining_n5_delivery_partition.json'
PREFIX='cutoff5_20261020/root/delivery_extract_v1/'
ARCHIVE_SHA='8428002462d4e650613ea6e2ff673cb1e69c2079572cc40546d125349d582419'

def sha(raw):return hashlib.sha256(raw).hexdigest()

def build(archive):
    archive=Path(archive)
    if archive.stat().st_size!=141304365 or sha(archive.read_bytes())!=ARCHIVE_SHA:raise ValueError('Exact original C5 archive')
    partition=json.loads(PARTITION.read_text('utf-8'))
    actions=partition['required_original_exact_control_programs']+partition['required_fresh_support_programs']+partition['required_fresh_complement_programs']
    with zipfile.ZipFile(archive)as z:
        members={i.filename:i for i in z.infolist()if not i.is_dir()}
        names={n[len(PREFIX):]:n for n in members if n.startswith(PREFIX)}
        for member in members:
            if member.startswith('cutoff5_20261020/') and not member.startswith(PREFIX):
                name='work/'+member
                names.setdefault(name,member)
        # This exact original check/proof is supplied outside delivery_extract.
        for tail in ('check.py','PROOF.txt'):
            alias='cutoff5_20261020/root/count_identity_controls_v1/'+tail
            if alias in members:names['work/cutoff5_20261020/root/count_identity_controls_v1/'+tail]=alias
        loaded={}
        def raw(name):
            if name not in loaded:loaded[name]=z.read(names[name])
            return loaded[name]
        def obj(name):return json.loads(raw(name))
        known={}
        def add(name,pin=None):
            if name not in names:raise ValueError('Missing transitive original member: '+name)
            b=raw(name);h=sha(b)
            if pin is not None and h!=pin:raise ValueError('Original graph mismatch: '+name)
            known[name]={'member':names[name],'bytes':len(b),'sha256':h}
        def expand(seed):
            selected=set(seed);queue=list(seed)
            while queue:
                name=queue.pop();add(name);b=raw(name)
                extra=set()
                if name.endswith('.json'):
                    try:d=json.loads(b)
                    except (ValueError,UnicodeError):d=None
                    def walk(v):
                        if isinstance(v,dict):
                            for k,x in v.items():
                                if type(k)is str and k.startswith(('work/','runs/')) and k in names and type(x)is str and len(x)==64:
                                    add(k,x);extra.add(k)
                                walk(x)
                        elif isinstance(v,list):
                            for x in v:walk(x)
                    walk(d)
                if name.endswith('.py'):
                    # Seal every possible same-directory helper, including dynamic imports.
                    directory=name.rsplit('/',1)[0]+'/'
                    extra|={n for n in names if n.startswith(directory)and '/'not in n[len(directory):]and n.endswith(('.py','.txt','.md','.diff','.json'))}
                for n in extra-selected:selected.add(n);queue.append(n)
            return selected
        rows=[]
        for action in actions:
            seed={action['entry'],*action['outputs']}
            selected=expand(seed)
            expected={o:obj(o)for o in action['outputs']}
            rows.append(dict(id=action['id'],argv=action['argv'][1:],cwd=action['cwd'],outputs=action['outputs'],
                inputs=sorted(selected-set(action['outputs'])),expected_outputs=expected,scope=action['scope']))
        # Pure independent readers are pinned as source, not historical success.
        reference_dirs=('audit/resource5_readback_v4','audit/resource5_sector_readback_v1','high/B3_resource_readback_v1',
            'audit/count5_readback_v1','audit/count5_sector_readback_v1','high/B3_count_readback_v1','root/final_composition_v2')
        references=[]
        for directory in reference_dirs:
            pre='work/cutoff5_20261020/'+directory+'/'
            for name in names:
                if name.startswith(pre)and '/'not in name[len(pre):]and name.endswith(('.py','.txt','.json','.diff')):
                    add(name);references.append(name)
        # The exact final reference graph closes all stored-data semantic inputs.
        # These are never numerical acceptance by themselves.
        expand({'work/cutoff5_20261020/root/final_composition_v2/C5_CHECKED.json'})
        groups=[dict(id=r['id'],action_ids=[r['id']],inputs=r['inputs'],outputs=r['outputs'])for r in rows[:14]]
        capture_labels=['support_tighter_construct01','support_tighter_replay01','support_A0_construct01','support_A0_replay01',
            'complement_construct01','complement_replay01','complement_accept01']
        captures=['runs/cutoff5_20261020/high/'+label+'/'+name for label in capture_labels for name in ('metadata.json','stdout.txt','stderr.txt')]
        fresh=set(o for r in rows[14:]for o in r['outputs'])|set(captures)
        groups.append(dict(id='67.support-complement-physical-epoch',action_ids=[r['id']for r in rows[14:]],
            inputs=sorted(set(n for r in rows[14:]for n in r['inputs'])-fresh),outputs=sorted(fresh)))
        for r in rows:r['capture_label']=dict(zip([v['id']for v in rows[14:21]],capture_labels)).get(r['id'])
        return dict(schema='N5_FULL_JOIN_SOURCE_PLAN_V1',archive=dict(name=archive.name,bytes=archive.stat().st_size,sha256=ARCHIVE_SHA,
            url=partition['original_asset']['url']),partition_sha256=sha(PARTITION.read_bytes()),actions=rows,groups=groups,
            files={n:known[n]for n in sorted(known)},semantic_references=sorted(set(references)),
            numerical_calls=22,semantic_regions=12,probability_panel_instances=1200,count_forests=295,count_roots=1770,count_leaves=75178,
            old_outputs_are_reference_only=True,all_index_conclusion_verified=False,original_mathematics_executed=False)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('archive',type=Path);parser.add_argument('--output',type=Path,default=ROOT/'proof/n5_full_join_source_plan.json')
    a=parser.parse_args();d=build(a.archive);a.output.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(path=str(a.output),sha256=sha(a.output.read_bytes()),files=len(d['files']),bytes=sum(v['bytes']for v in d['files'].values()),original_mathematics_executed=False)))
if __name__=='__main__':main()
