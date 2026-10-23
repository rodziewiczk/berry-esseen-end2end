"""Build the explicit16GiB full tail49 restart, without changing the2GiB notebook."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('tail49_phase2_builder', ROOT/'tools/make_phase2_notebooks.py')
phase2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase2)
NAME = '12_tail49_HIGHMEM_16GB_18H'

INTRO = '''# Berry–Esseen: full tail49 restart,16GiB /18hours

Choose **Runtime -> Change runtime type -> GPU**, enable high RAM if available,
then **Runtime -> Run all**. Authorize Google Drive when requested.
The calculation still uses the CPU; a GPU runtime is requested for its host
resources. Runtime availability and speed depend on the actual allocation.

This is an explicitly authorized fresh full restart. All14top-level jobs and
all41retained components are mandatory. The original verifier, mathematical
source bytes, exact targets and complete acceptance checks are unchanged.
The original driver has no numerical resume; earlier partial work is not
reused. Its logs and incomplete ZIPs remain in their existing Drive folders.

The BASIC process-group budget is16GiB, with64,800seconds (18hours) external
wall time and64,800seconds per-process CPU. These are ceilings, not an ETA.
Memory is enforced by inherited address-space limits and sampled live-group
RSS. This is not the original Docker/private-cgroup isolation contract;
native arithmetic and all-index acceptance remain false.
New evidence is stored in a fresh run directory with automatic Drive backups.
'''

EXECUTE = '''from be_replay.tail49 import run_colab
RESULT = run_colab(durable_root=DURABLE, memory_bytes=16*1024**3,
                   cpu_seconds=64800, wall_seconds=64800)
'''


def build(pin):
    if not re.fullmatch('[0-9a-f]{40}', pin):
        raise ValueError('Immutable full Git commit required')
    doc = phase2.build(pin, '12_tail49_complete_arithmetic')
    for i, cell in enumerate(doc['cells']):
        if cell['id'] == 'instructions':
            doc['cells'][i] = phase2.base.cell('markdown', INTRO, 'instructions')
        elif cell['id'] == 'execute-task':
            doc['cells'][i] = phase2.base.cell('code', EXECUTE, 'execute-task')
        elif cell['id'] == 'pinned-code':
            text = ''.join(cell['source'])
            text = text.replace('TASK = "tail49-complete-arithmetic"',
                                'TASK = "tail49-highmem16g-full-restart"')
            doc['cells'][i] = phase2.base.cell('code', text, 'pinned-code')
    doc['metadata']['colab']['name'] = NAME+'.ipynb'
    doc['metadata']['accelerator'] = 'GPU'
    for cell in doc['cells']:
        if cell['cell_type'] == 'code':
            compile(''.join(cell['source']), NAME, 'exec')
    return doc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'colab')
    args = parser.parse_args()
    document = build(args.code_commit)
    args.output.mkdir(parents=True, exist_ok=True)
    path = args.output/(NAME+'.ipynb')
    path.write_bytes((json.dumps(document, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
    print(path)


if __name__ == '__main__':
    main()
