"""Read-only source inventory, not a kernel axiom-dependency audit.

Usage: python tools/inventory_existing_lean.py --source-root PATH
Paths in the generated manifest are relative source identities. No home
directory or credentials are recorded. Imported-axiom reachability is a
conservative file-graph warning, not a claim a theorem uses those axioms.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def without_comments(text):
    chars = list(text)
    i, depth, string = 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                depth += 1; chars[i:i+2] = '  '; i += 2
            elif text.startswith('-/', i):
                depth -= 1; chars[i:i+2] = '  '; i += 2
            else:
                if chars[i] != '\n': chars[i] = ' '
                i += 1
        elif string:
            if text[i] == '\\': i += 2
            else:
                if text[i] == '"': string = False
                i += 1
        elif text.startswith('/-', i):
            depth = 1; chars[i:i+2] = '  '; i += 2
        elif text.startswith('--', i):
            end = text.find('\n', i)
            if end < 0: end = len(text)
            chars[i:end] = ' ' * (end-i); i = end
        else:
            if text[i] == '"': string = True
            i += 1
    return ''.join(chars)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', required=True)
    args = parser.parse_args()
    source = Path(args.source_root)
    rows = {}
    for p in sorted(source.rglob('*.lean')):
        relative = p.relative_to(source).as_posix()
        module = 'EventualExactness.' + relative[:-5].replace('/', '.')
        raw = p.read_bytes()
        clean = without_comments(raw.decode('utf-8-sig'))
        imports = []
        for m in re.finditer(r'^\s*(?:(?:public|private)\s+)?import\s+([^\n]+)', clean, re.M):
            imports.extend(m.group(1).split())
        declarations = []
        for m in re.finditer(r'^\s*(?:(?:private|protected|noncomputable)\s+)*'
                             r'(def|theorem|structure|abbrev|axiom|inductive)\s+([\w.]+)', clean, re.M):
            declarations.append(dict(kind=m.group(1), name=m.group(2),
                                     line=clean[:m.start()].count('\n')+1))
        rows[module] = dict(source='EventualExactness/'+relative,
                            sha256=hashlib.sha256(raw).hexdigest(), imports=imports,
                            declaration_count=len(declarations),
                            custom_axioms=[d for d in declarations if d['kind']=='axiom'])
    for module, row in rows.items():
        seen, todo, reach = set(), [module], []
        while todo:
            node = todo.pop()
            if node in seen or node not in rows: continue
            seen.add(node)
            reach.extend(node+'.'+d['name'] for d in rows[node]['custom_axioms'])
            todo.extend(rows[node]['imports'])
        row['potential_custom_axioms_in_import_closure'] = sorted(set(reach))
    result = dict(scope='Read-only source inventory of earlier finite_cutoff_49 development',
                  interpretation='Import reachability is not theorem-level logical dependency',
                  source_files=len(rows),
                  custom_axiom_declarations=sum(len(r['custom_axioms']) for r in rows.values()),
                  modules=rows)
    output = Path(__file__).resolve().parents[1]/'docs'/'contracts'/'reuse-inventory.json'
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(f"Inventoried {result['source_files']} files and {result['custom_axiom_declarations']} custom axiom declarations.")
    print(f"Relative-source manifest: {output.name}")


if __name__ == '__main__': main()
