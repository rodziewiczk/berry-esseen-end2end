"""Pure data-only source-graph epochs; never create historical successful captures.

The caller pins the explicit metadata documents and source selection. Only their
one top-level files_sha256 maps may change. Numerical documents/contracts must
remain outside documents and may not enter allowed_overrides. The caller must
independently validate each actual current execution supplied as an override.
"""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import PurePosixPath
import re


def need(ok,message):
    if not ok:raise ValueError(message)


def same(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    return a==b


def digest(raw):
    need(type(raw)is bytes,'Metadata input is exact bytes');return sha256(raw).hexdigest()


def path(name):
    need(type(name)is str and name and not any(x in name for x in('\\',':','\0')),'Portable source graph path')
    p=PurePosixPath(name)
    need(not p.is_absolute()and p.as_posix()==name and all(x not in('','.','..')for x in name.split('/')),'Canonical contained source graph path')
    return name


def pin(value):
    need(type(value)is str and re.fullmatch('[0-9a-f]{64}',value)is not None,'Exact source SHA256');return value


def unique(rows):
    out={}
    for key,value in rows:need(key not in out,'Duplicate metadata JSON key');out[key]=value
    return out


def loads(raw):
    def bad(_):raise ValueError('Nonfinite metadata JSON')
    need(type(raw)is bytes,'Original metadata bytes');return json.loads(raw,object_pairs_hook=unique,parse_constant=bad)


def encode(value):return(json.dumps(value,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('utf-8')


def checked_map(value):
    need(type(value)is dict,'Exact source-hash mapping')
    return{path(k):pin(v)for k,v in value.items()}


def derive_metadata_epoch(documents,original_files_sha256,current_files_sha256,unavailable,*,allowed_overrides=()):
    """Rebind only declared source maps; return derived bytes and explicit ledger.

    current_files_sha256 describes existing stopped/current inputs, not proposed
    receipts. An allowlisted override may reproduce the original bytes after a real fresh execution.
    Missing inputs are not fabricated: only exact pinned runs/* edges may be
    omitted and are recorded as UNACQUIRED_HISTORICAL_EXECUTION_PROVENANCE.
    """
    need(type(documents)is dict,'Explicit immutable metadata document selection')
    original=checked_map(original_files_sha256);current=checked_map(current_files_sha256);missing=checked_map(unavailable)
    names=list(documents);need(all(path(n)==n for n in names),'Explicit metadata paths')
    need(set(missing).isdisjoint(original)and set(missing).isdisjoint(current),'Historical unavailable inputs have no staged alias')
    need(all(n.startswith('runs/')for n in missing),'Only historical execution provenance may be unavailable')
    allowed=list(allowed_overrides);need(len(allowed)==len(set(allowed))and all(path(n)==n for n in allowed),'Unique named current execution overrides')
    need(set(current)==set(original),'Current source inventory matches original selection')
    changed={n for n in current if current[n]!=original[n]}
    need(changed<=set(allowed)and set(allowed)<=set(original)and set(allowed).isdisjoint(documents),'Every changed input is an explicit validated current override')
    parsed={}
    for name,raw in documents.items():
        need(name in original and digest(raw)==original[name],'Pinned original metadata bytes')
        value=loads(raw);need(type(value)is dict and type(value.get('files_sha256'))is dict,'One top-level source graph only')
        checked_map(value['files_sha256']);parsed[name]=value
    derived={};rows={};active=set()
    def visit(name):
        if name in derived:return derived[name]
        need(name not in active,'No metadata source-graph cycle');active.add(name)
        old=parsed[name];graph={};changes={};omitted={}
        for target,oldpin in old['files_sha256'].items():
            if target in missing:
                need(oldpin==missing[target],'Exact unavailable historical commitment');omitted[target]=oldpin;continue
            need(target in original and oldpin==original[target],'Every original graph edge has exact known source bytes')
            newpin=digest(visit(target))if target in documents else current[target]
            graph[target]=newpin
            if newpin!=oldpin:changes[target]=dict(original_sha256=oldpin,current_sha256=newpin,
                reason='DECLARED_METADATA_ANCESTOR'if target in documents else'VALIDATED_CURRENT_EXECUTION_OVERRIDE')
        new=dict(old);new['files_sha256']=graph
        need(same({k:v for k,v in old.items()if k!='files_sha256'},{k:v for k,v in new.items()if k!='files_sha256'}),'All non-graph fields remain typed-identical')
        raw=encode(new);derived[name]=raw;rows[name]=dict(original_sha256=original[name],current_sha256=digest(raw),
            non_graph_fields_unchanged=True,changed_edges=changes,omitted_historical_edges=omitted)
        active.remove(name);return raw
    for name in names:visit(name)
    ledger=dict(schema='EXPLICIT_SOURCE_GRAPH_METADATA_EPOCH_V1',document_order=names,documents={n:rows[n]for n in names},
        validated_current_overrides={n:dict(original_sha256=original[n],current_sha256=current[n])for n in allowed},
        unavailable_historical_inputs=missing,unavailable_status='UNACQUIRED_HISTORICAL_EXECUTION_PROVENANCE',
        original_mathematical_fields_unchanged=True,original_python_unchanged=True,
        historical_capture_impersonated=False,arithmetic_computed=False,parent_acquisitions_verified=False,
        all_index_conclusion_verified=False)
    return dict(derived={n:derived[n]for n in names},ledger=ledger)
