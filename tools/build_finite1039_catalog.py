"""Build the fixed 1009-job finite COUNT source catalog from archive bytes.

Only JSON, hashes and Python ASTs are read. No mathematical source is imported.
The optional original strict selector is a frozen stdlib-only metadata module.
"""
from __future__ import annotations
import ast
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from be_replay import finite1039_sources as src


def sha(raw):return hashlib.sha256(raw).hexdigest()
AST_CACHE={}
def source_ast(raw):
    pin=sha(raw)
    if pin not in AST_CACHE:AST_CACHE[pin]=ast.parse(raw)
    return AST_CACHE[pin]
def parse(raw):return json.loads(raw,object_pairs_hook=src.unique)
def dump(path,d):
    raw=(json.dumps(d,sort_keys=True,indent=2)+'\n').encode();path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw);return sha(raw)
def norm(name):
    name=name.replace('\\','/')
    if name.startswith('work/'):return name[5:]
    if name.startswith('/Users/'):
        matches=[m.start()+1 for m in re.finditer(r'/((?:continuation_)?cutoff\d+_\d{8})/',name)]
        if len(matches)!=1:raise ValueError('One explicit original archive root: '+name)
        return name[matches[0]:]
    return name


class Inputs:
    def __init__(self,old):
        base=old/'tmp/cutoff20_import_2026-10-17'
        self.paths=[old/'tmp/drive_2026-10-19/cutoff5_10_15.zip',base/'cutoff20_20261016.zip',
            base/'continuation_cutoff20_20261016_final.zip',old/'research/imports/drive_20261012/cutoff25_20261011.zip',
            base/'cutoff25_continue_20261015.zip']
        self.archives={p.name:zipfile.ZipFile(p)for p in self.paths};self.index={};self.files={};self.references={}
        for name,z in self.archives.items():
            src.zip_index(z)
            for info in z.infolist():
                if not info.is_dir()and not info.filename.startswith('__MACOSX/'):
                    self.index.setdefault(info.filename,[]).append((name,info))
    def close(self):
        for z in self.archives.values():z.close()
    def raw(self,name,pin=None,record=False):
        src.parts(name);options=self.index.get(name,[])
        src.need(options,'Exact selected archive member is available: '+name)
        for archive,info in options:
            raw=self.archives[archive].read(info)
            if pin is None or sha(raw)==pin:break
        else:raise ValueError('Selected archive member SHA: '+name)
        src.need(len(raw)<=64*src.MIB,'Explicit 64 MiB per-file source bound')
        if record:
            row=dict(archive=archive,member=info.filename,bytes=len(raw),sha256=sha(raw))
            src.need(name not in self.files or self.files[name]==row,'Unique canonical source identity');self.files[name]=row
        return raw
    def ref(self,name,pin=None):
        raw=self.raw(name,pin);self.references[name]=dict(sha256=sha(raw),bytes=len(raw));return parse(raw)


def graph_of(d,prefix=''):
    return {((prefix if prefix and not norm(k).startswith(prefix)else'')+norm(k)):v for k,v in d['files_sha256'].items()}


def lane(n):
    for name in src.LANES:
        low,high=map(int,name[1:].split('_'))
        if low<=n<=high:return name
    raise ValueError('Literal finite COUNT index')


def stdout_rule(raw,family):
    if family=='count_protocol':
        tree=source_ast(raw);functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='accept']
        src.need(len(functions)==1,'One unchanged complete COUNT acceptor')
        prints=[n for n in ast.walk(functions[0])if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='print'
                and n.args and isinstance(n.args[0],ast.Call)and isinstance(n.args[0].func,ast.Attribute)
                and isinstance(n.args[0].func.value,ast.Name)and n.args[0].func.value.id=='json'and n.args[0].func.attr=='dumps']
        src.need(len(prints)==1 and len(prints[0].args[0].args)==1 and isinstance(prints[0].args[0].args[0],ast.Name)
                 and prints[0].args[0].args[0].id=='out','Original full native JSON output, not a PASS token')
        return dict(kind='json_receipt')
    tree=source_ast(raw);functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main']
    src.need(len(functions)==1,'One unchanged strict acceptance entry')
    prints=[n for n in ast.walk(functions[0])if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='print'
            and n.args and isinstance(n.args[0],ast.Constant)and type(n.args[0].value)is str and n.args[0].value.startswith('ACCEPTED_')]
    src.need(len(prints)==1 and len(prints[0].args)==8 and isinstance(prints[0].args[1],ast.Name)
             and prints[0].args[1].id=='index','Exact original strict terminal print and index position')
    return dict(kind='text',prefix=prints[0].args[0].value,index_token=1,tokens=len(prints[0].args))


def standard(inp,directory,n,band,index,graph,selector,ordinal=0):
    prefix=directory+'/';local={k[len(prefix):]:v for k,v in graph.items()if k.startswith(prefix)and '/'not in k[len(prefix):]}
    receipt_name=f'COUNT{index}_ACCEPTED.json';forest_name=f'COUNT{index}_FOREST.json'
    if receipt_name not in local:
        candidates=[k for k in local if re.fullmatch(r'COUNT(?:\d+)?_ACCEPTED.json',k)]
        src.need(len(candidates)==1,'One exact native acceptance filename');receipt_name=candidates[0]
        forest_name=receipt_name.replace('_ACCEPTED','_FOREST')
    receipt=inp.ref(prefix+receipt_name,local[receipt_name]);manifest=inp.ref(prefix+'KERNEL_COPY_MANIFEST.json',local['KERNEL_COPY_MANIFEST.json'])
    src.need(type(receipt['n'])is int and receipt['n']==n and type(receipt['index'])is int and receipt['index']==index,'Actual source-selected sample and panel')
    pins={prefix+name:pin for name,pin in manifest['files'].items()}
    for name in ('KERNEL_COPY_MANIFEST.json','contract.json','count_protocol.py',forest_name):pins[prefix+name]=local[name]
    # Some selected p/rho restrictions add separately pinned lineage inputs
    # and a sibling helper outside the original mathematical kernel manifest.
    pending=[prefix+'count_protocol.py'];checked=set()
    while pending:
        path=pending.pop()
        if path in checked:continue
        checked.add(path);raw=inp.raw(path,pins[path]);tree=source_ast(raw)
        names=set()
        for node in ast.walk(tree):
            if isinstance(node,ast.BinOp)and isinstance(node.op,ast.Div)and isinstance(node.left,ast.Name)and node.left.id=='HERE'and isinstance(node.right,ast.Constant)and type(node.right.value)is str:names.add(node.right.value)
            if isinstance(node,ast.Import):names.update(a.name+'.py'for a in node.names if '.'not in a.name)
            if isinstance(node,ast.ImportFrom)and node.module and '.'not in node.module:names.add(node.module+'.py')
        for name in names:
            if name==receipt_name:continue
            if name in local:
                pins[prefix+name]=local[name]
                if name.endswith('.py'):pending.append(prefix+name)
    for name,pin in pins.items():src.need(graph[name]==pin,'Entire selected source map bound by frozen selector');inp.raw(name,pin,record=True)
    src.need(prefix+receipt_name not in pins,'Old own acceptance is not a runtime source')
    candidate=parse(inp.raw(prefix+forest_name,pins[prefix+forest_name]));contract=parse(inp.raw(prefix+'contract.json',pins[prefix+'contract.json']))
    src.need(receipt['contract_sha256']==pins[prefix+'contract.json']and receipt['checker_sha256']==pins[prefix+'count_protocol.py']
             and receipt['forest_sha256']==pins[prefix+forest_name]and receipt['kernel_sha256']==manifest['files'],'Exact historical input identities, never acceptance')
    row=dict(job_id=f'n{n}.{band}.p{index:02}.'+sha(directory.encode())[:12],lane=lane(n),family='count_protocol',n=n,index=index,band=band,
        directory=directory,script='count_protocol.py',arguments=['accept'],output=receipt_name,candidate=forest_name,
        candidate_sha256=pins[prefix+forest_name],contract_name='contract.json',contract_sha256=pins[prefix+'contract.json'],
        source_files_sha256=dict(sorted(pins.items())),expected_receipt=receipt,ignored_runtime_fields=['seconds'],
        expected_controls=receipt['negative_controls'],stdout_rule=stdout_rule(inp.raw(prefix+'count_protocol.py',pins[prefix+'count_protocol.py']),'count_protocol'),
        selector=selector,historical_receipt=dict(path=prefix+receipt_name,sha256=local[receipt_name]),candidate_is_untrusted=True,
        parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    row['census']=src.inspect_candidate(row,candidate)
    src.need({k:row['census'][k]for k in ('nodes','leaves','maximum_depth')}=={k:receipt['statistics'][k]for k in ('nodes','leaves','maximum_depth')},'Full candidate census matches source-selected reference')
    return row


def build(old):
    inp=Inputs(old);rows=[]
    try:
        # n10--14: literal final selection, including all twenty component
        # forests replacing five selected original probability panels.
        name='cutoff10_20261018/audit/chain10_14_join_v4/FINAL_READBACK.json';d=inp.ref(name,'1b69be3627b8a3c734ce7c244106f30f86c6850bd4add7e4cc377d63729e4110');g=graph_of(d);s=d['summary']
        overrides={(r['n'],r['band'],r['index']):norm(r['directory'])for r in s['composite_overrides']}
        for n in range(10,15):
            for band in ('B0','BN'):
                base=norm(s['selected_source_epochs'][f'{n}_{band}']['count'])+'/'+band
                for i in s[str(n)][band]['acquired_panels']:
                    dirs=[overrides[n,band,i]+f'/part{part:02}'for part in range(4)]if(n,band,i)in overrides else[base+f'/capsule{i}']
                    for directory in dirs:rows.append(standard(inp,directory,n,band,i,g,name))
        src.need(len(rows)==217,'Every selected n10--14 original/component forest');print('n10--14 source rows',len(rows),flush=True)
        # Actual15 and the sequential literal16--19 chain are different selectors.
        name15='cutoff15_20261017/audit/actual15_join_v1/FINAL_READBACK.json';d15=inp.ref(name15,'5ae420a641bb352f29799fb04fde9a641a00df13ffa1f3c8acb1cf37bd72f229')
        name16='cutoff15_20261017/audit/sequential16_19_join_v2/FINAL_READBACK.json';d16=inp.ref(name16,'3160c913aca62e36104f01405b7afa0fe36ea31ee4eb935f9bbd2d79f6906f2a')
        for n in range(15,20):
            d,name=(d15,name15)if n==15 else(d16,name16);g=graph_of(d);s=d['summary']if n==15 else d['summary'][str(n)]
            for band in ('B0','BN'):
                indices=s[band]['acquired_count_panels'if n==15 else'acquired_panels'];base=f'cutoff15_20261017/'+('analytic/count15_v1'if n==15 else f'root/count{n}_v1')+'/'+band
                for i in indices:rows.append(standard(inp,base+f'/capsule{i}',n,band,i,g,name))
        src.need(len(rows)==364,'All217+147 source-selected COUNT forests');print('n15--19 source rows',147,flush=True)
        # Actual20 final pieces, never every broad ancestry forest.
        for band,name in [('B0','continuation_cutoff20_20261016/b0/B0_CONDITIONAL_JOINED_V3.json'),('BN','continuation_cutoff20_20261016/bn/full_union_v6/BN_FULL100_CONDITIONAL.json')]:
            d=inp.ref(name);g=graph_of(d)
            selected=[]
            if band=='B0':
                for panel in d['outcomes']:
                    for forest in panel.get('forests',[]):selected.append((panel['index'],norm(forest['receipt']).rsplit('/',1)[0]))
            else:
                for panel in d['counts']:
                    selected.extend((panel['index'],norm(record['directory']))for record in panel['records'])
            src.need(len(selected)==(30 if band=='B0'else 19),'All final actual20 selected pieces')
            for i,directory in selected:rows.append(standard(inp,directory,20,band,i,g,name))
        # Actual21--24 final100-panel regional selectors, not auxiliary loosened bounds.
        for n in range(21,25):
            for band in ('B0','BN'):
                name=f'continuation_cutoff20_20261016/analytic/bridge_family_composition_v4/ACTUAL{n}_{band}_JOINED.json';d=inp.ref(name);g=graph_of(d)
                chosen=[key for key in g if re.search(r'/COUNT\d+_ACCEPTED.json$',key)]
                src.need(len(chosen)=={(21,'B0'):21,(21,'BN'):10,(22,'B0'):20,(22,'BN'):9,(23,'B0'):19,(23,'BN'):9,(24,'B0'):18,(24,'BN'):8}[n,band],'Exact actual21--24 selected census')
                for path in chosen:
                    i=int(re.search(r'COUNT(\d+)_ACCEPTED',path).group(1));rows.append(standard(inp,path.rsplit('/',1)[0],n,band,i,g,name))
        src.need(len(rows)==527,'All three lower-index lanes');print('n20--24 source rows',163,flush=True)
        # n26 actual and n27 retained prototype are bound by the same original
        # complete baseline; the other62 jobs are the explicit continued selection.
        name='cutoff25_20261011/new_audit/ACTUAL26_B0_COMPLETE_JOINED_V1.json';d=inp.ref(name);g=graph_of(d,'cutoff25_20261011/')
        for i in range(37,54):
            directory=f'cutoff25_20261011/new_audit/'+(f'actual26_b0_counts_v1/count{i}'if i<53 else'actual26_b0_p53_v1')
            rows.append(standard(inp,directory,26,'B0',i,g,name))
        selection='cutoff25_continue_20261015/root/count_join_v1/SELECTION_02.json';s=inp.ref(selection,'7f10e838673e365847951a1c59c1e600a79d4b93fb5c7aa3dc25f9e9450f948b')
        joined='cutoff25_continue_20261015/root/count_join_v1/SELECTION_02_JOIN.json';j=inp.ref(joined);g=graph_of(j)
        for selected in s['panels']:
            rows.append(standard(inp,norm(selected['directory']),selected['n'],'B0',selected['index'],g,selection))
        # The retained prototype is the unique n27 panel41 outside SELECTION02.
        # Its mandatory final edge is real, but its two count payloads are not
        # present in the supplied selected source assets. Keep this obligation;
        # do not silently call the79 available forests a complete80-job lane.
        baseline='cutoff25_20261011/new_middle/actual27_30_b0_plan_v1/actual27_count41_prototype'
        oldfinal='cutoff25_20261011/continuation_20261010/repair31/EVENTUAL_CUTOFF31_COMPOSED.json';record=inp.ref(oldfinal,'33c73b3bd4c8cb25cedb6c9c8ce3768608db18f1f65932a0fcd6bb468c2b51b9')
        old41=dict(n=27,index=41,band='B0',directory=baseline,
            final_join='cutoff25_20261013/b5/actual27_p41_join_v1/ACQUIRED_REGION.json',
            final_join_sha256='978a1b98b9cd70edd53c1af88a2df0f7ee70a34c8d7b2f72dfd86e3fc423ad16',
            candidate='COUNT41_FOREST.json',candidate_sha256='61e45510ffabb2d6a06094fae8a26b46a773d2d1c88db5236ed8b2e167c71af4',
            historical_receipt='COUNT41_ACCEPTED.json',historical_receipt_sha256='a33de9d37f36223834a9d10cdc21767dc4e8dafacf6cfe7b1a497a13d23dfb10',
            contract_sha256='f7341272d102c4660fd037b96d64acfefdda7de04df5d068d81c67fd8a323cc6',
            checker_sha256='334aaa08ea6744067f2234b5fa917f54d5432874e69d628a0dab9f6c55f7d173',
            census=dict(roots=28,nodes=6310,leaves=3169,maximum_depth=25),
            reason='Mandatory selected candidate payload absent from bounded supplied-archive path lookup; original source and constructor are present. No old acceptance substituted.',
            future_route='Original construct_alpha4.py in Colab under a new explicit bounded discovery protocol, then unchanged full native count_protocol.py accept; no original math executed locally.')
        src.need(len(rows)==606,'All606 physically available nested native count forests; one explicit missing retained p41');print('n26--30 available source rows',79,'expected80',flush=True)
        dump(ROOT/'work/finite1039-standard-source-only.json',dict(jobs=rows,source_files=inp.files,selectors=inp.references,missing=old41,arithmetic_computed=False))
        # Frozen stdlib-only selector obtains the exact402 selected strict jobs.
        vendor=ROOT/'vendor/finite1039_snapshot_v1';vendor.mkdir(parents=True,exist_ok=True)
        source=old/'publication/berry-esseen-045-certificate/moment-defects/reproduction/uniform_tail/count_catalog.py'
        raw=source.read_bytes();(vendor/'count_catalog.py').write_bytes(raw)
        license_raw=(ROOT/'vendor/n5_remaining_snapshot_v1/LICENSE').read_bytes();(vendor/'LICENSE').write_bytes(license_raw)
        snapshot=dump(vendor/'SNAPSHOT.json',dict(schema='UNCHANGED_FINITE1039_SOURCE_SELECTOR_V1',files=[dict(path='count_catalog.py',bytes=len(raw),sha256=sha(raw)),dict(path='LICENSE',bytes=len(license_raw),sha256=sha(license_raw))],mathematical_modules_imported=False))
        spec=importlib.util.spec_from_file_location('finite1039_frozen_metadata_selector',vendor/'count_catalog.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        selected,_=module.catalog(inp.archives['cutoff25_20261011.zip'])
        for oldjob in selected:
            directory='cutoff25_20261011/'+oldjob['folder'];prefix=directory+'/';pins={prefix+k:v for k,v in oldjob['sources_sha256'].items()}
            pins[prefix+oldjob['candidate']]=oldjob['candidate_sha256']
            for key,pin in pins.items():inp.raw(key,pin,record=True)
            # Runtime identity is never a mathematical expectation; omit the
            # original private executable/version context from public metadata.
            expected={k:v for k,v in oldjob['expected_mathematical_receipt'].items()if k!='child_runtime'}
            row=dict(job_id=f'n{oldjob["n"]}.strict.'+oldjob['id'],lane=lane(oldjob['n']),family='strict',n=oldjob['n'],index=oldjob['index'],
                directory=directory,script=oldjob['script'],arguments=[str(oldjob['index'])],output=oldjob['output'],candidate=oldjob['candidate'],candidate_sha256=oldjob['candidate_sha256'],
                contract_name='contract.json',contract_sha256=pins[prefix+'contract.json'],source_files_sha256=dict(sorted(pins.items())),expected_receipt=expected,
                ignored_runtime_fields=['child_runtime'],child_runtime_required='child_runtime'in oldjob['expected_mathematical_receipt'],expected_controls=oldjob['expected_mathematical_receipt']['negative_controls'],stdout_rule=stdout_rule(inp.raw(prefix+oldjob['script'],pins[prefix+oldjob['script']]),'strict'),
                selector=oldfinal,historical_receipt=dict(path='cutoff25_20261011/'+oldjob['original_receipt'],sha256=oldjob['historical_receipt_sha256'],ignored_runtime_context_omitted=True),candidate_is_untrusted=True,
                parent_acquisitions_verified=False,all_index_conclusion_verified=False)
            candidate=parse(inp.raw(prefix+oldjob['candidate'],oldjob['candidate_sha256']))
            row['candidate_contract_field']='contract_sha256'if'contract_sha256'in candidate else'targets_sha256'
            row['dimensions']=len(candidate['root'])
            row['census']=src.inspect_candidate(row,candidate)
            src.need(row['census']['leaves']==row['expected_receipt']['all_closed_leaves'],'Complete flat candidate leaf census');rows.append(row)
        rows.sort(key=lambda r:(r['n'],r['job_id']));lanes={}
        for key,count in src.LANES.items():
            chosen=[r for r in rows if r['lane']==key];src.need(len(chosen)==count-(key=='n26_30'),'Exact available lane selection and explicit missing retained job')
            lanes[key]=dict(forests=count,available_forests=len(chosen),**{name:sum(r['census'][name]for r in chosen)for name in('roots','nodes','leaves')})
        specs=[]
        urls={'cutoff5_10_15.zip':'cutoff5-sources-2026-10-20','cutoff25_20261011.zip':'cutoff20-sources-2026-10-17',
            'cutoff20_20261016.zip':'cutoff20-sources-2026-10-17','continuation_cutoff20_20261016_final.zip':'cutoff20-sources-2026-10-17',
            'cutoff25_continue_20261015.zip':'cutoff20-sources-2026-10-17'}
        for path in inp.paths:
            specs.append(dict(name=path.name,bytes=path.stat().st_size,sha256=src.digest(path),url='https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/download/'+urls[path.name]+'/'+path.name))
        d=dict(schema='FINITE1039_SELECTED_SOURCE_CATALOG_V1',assets=specs,snapshot_sha256=snapshot,jobs=rows,source_files=dict(sorted(inp.files.items())),
            selectors=dict(sorted(inp.references.items())),lanes=lanes,census=dict(forests=len(rows),**{key:sum(v[key]for v in lanes.values())for key in('roots','nodes','leaves')}),
            expected_forests=1009,lane_ready={key:key!='n26_30'for key in src.LANES},
            not_ready_lanes=dict(n26_30=dict(expected_forests=80,available_forests=79,missing_jobs=[old41])),
            source_only_file_bytes=sum(r['bytes']for r in inp.files.values()),maximum_source_file_bytes=max(r['bytes']for r in inp.files.values()),
            historical_receipts_are_fresh_proof_inputs=False,arithmetic_computed=False,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
        pin=dump(ROOT/'proof/finite1039_count_catalog.json',d);print(json.dumps(dict(catalog_sha256=pin,lanes=lanes,files=len(inp.files),bytes=d['source_only_file_bytes'],maximum_file_bytes=d['maximum_source_file_bytes']),indent=2),flush=True)
        return d,pin
    finally:inp.close()


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--old-root',type=Path,required=True);a=p.parse_args();build(a.old_root)
