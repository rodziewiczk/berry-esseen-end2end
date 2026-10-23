"""Read actual selected source bytes/ASTs and resource guards; never import them."""
from __future__ import annotations
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from be_replay import finite1039_sources as src
from tools.build_finite1039_catalog import stdout_rule


def audit(archives):
    d=src.catalog();opened={};asts={};reached_paths=set();issues=[];caps=Counter();depths=Counter();markers=Counter();edges=0
    stdlib=set(sys.stdlib_module_names)|set(sys.builtin_module_names)
    try:
        for asset in d['assets']:
            path=Path(archives[asset['name']]);src.need(path.stat().st_size==asset['bytes']and src.digest(path)==asset['sha256'],'Exact source archive transport')
            opened[asset['name']]=zipfile.ZipFile(path);src.zip_index(opened[asset['name']])
        def source(name):
            row=d['source_files'][name];raw=opened[row['archive']].read(row['member'])
            src.need(len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'],'Every actual source/candidate SHA');return raw
        def tree(name):
            raw=source(name);pin=d['source_files'][name]['sha256']
            if pin not in asts:asts[pin]=ast.parse(raw)
            return asts[pin],raw
        # All selected source inputs, including non-Python data and candidates.
        for ordinal,name in enumerate(d['source_files']):
            source(name)
            if ordinal%2000==0:print('Source-byte verification',ordinal,'/',len(d['source_files']),flush=True)
        for ordinal,row in enumerate(d['jobs']):
            prefix=row['directory']+'/';entry=prefix+row['script'];t,raw=tree(entry)
            src.need(stdout_rule(raw,row['family'])==row['stdout_rule'],'Exact source-specific native terminal output');markers[row['family']]+=1
            src.inspect_candidate(row,json.loads(source(prefix+row['candidate']),object_pairs_hook=src.unique))
            if row['family']=='count_protocol':
                values=[ast.literal_eval(n.value)for n in t.body if isinstance(n,ast.Assign)and any(isinstance(a,ast.Name)and a.id=='LIMIT'for a in n.targets)]
                src.need(len(values)==1 and type(values[0])is int and row['census']['nodes']<=values[0],'Candidate fits unchanged complete native node cap');caps[values[0]]+=1
            else:
                bounds=[n.comparators[0].value for n in ast.walk(t)if isinstance(n,ast.Compare)and len(n.ops)==1 and isinstance(n.ops[0],ast.LtE)and isinstance(n.left,ast.Call)and isinstance(n.left.func,ast.Name)and n.left.func.id=='len'and len(n.left.args)==1 and isinstance(n.left.args[0],ast.Name)and n.left.args[0].id=='path'and isinstance(n.comparators[0],ast.Constant)and type(n.comparators[0].value)is int]
                src.need(len(bounds)==1 and row['census']['maximum_depth']<=bounds[0],'Candidate fits original strict path-depth guard');depths[bounds[0]]+=1
            pending=[entry];seen=set()
            while pending:
                name=pending.pop()
                if name in seen:continue
                seen.add(name);reached_paths.add(name);module,_=tree(name)
                for node in ast.walk(module):
                    imports=[]
                    if isinstance(node,ast.Import):imports=[a.name for a in node.names]
                    if isinstance(node,ast.ImportFrom):
                        if node.level:issues.append(dict(job=row['job_id'],source=name,issue='relative_import',module=node.module))
                        imports=[node.module]if node.module else[]
                    if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='__import__':
                        if not node.args or not isinstance(node.args[0],ast.Constant)or type(node.args[0].value)is not str:issues.append(dict(job=row['job_id'],source=name,issue='nonliteral_dynamic_import'))
                        else:imports=[node.args[0].value]
                    for imported in imports:
                        if imported.split('.')[0]in stdlib:continue
                        sibling=prefix+imported.replace('.','/')+'.py';edges+=1
                        if sibling not in row['source_files_sha256']:issues.append(dict(job=row['job_id'],source=name,issue='unsealed_import',module=imported,path=sibling))
                        else:pending.append(sibling)
            if ordinal%200==0:print('Source-only topology/import/admission',ordinal,'/1008',flush=True)
        report=dict(schema='FINITE1039_ACTUAL_SOURCE_PREPARATION_V1',catalog_sha256=src.CATALOG_SHA256,source_files=len(d['source_files']),
            source_bytes=d['source_only_file_bytes'],maximum_source_file_bytes=d['maximum_source_file_bytes'],available_forests=1008,expected_forests=1009,
            lanes=d['lanes'],lane_ready=d['lane_ready'],reachable_python_paths=len(reached_paths),unique_reachable_source_ASTs=len(asts),
            sealed_nonstdlib_import_edges=edges,import_issues=issues,protocol_node_limits=dict(caps),strict_path_limits=dict(depths),stdout_rule_checks=dict(markers),
            all_candidate_topologies_checked=True,all_source_bytes_sha_matched=True,original_mathematical_modules_imported=False,
            arithmetic_computed=False,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
        src.need(not issues,'Complete sealed stdlib/sibling import closure');return report
    finally:
        for z in opened.values():z.close()


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archives',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=audit({asset['name']:a.archives/asset['name']for asset in src.catalog()['assets']})
    a.output.write_bytes((json.dumps(result,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(result,indent=2))
