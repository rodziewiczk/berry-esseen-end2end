"""English Run-all wrapper for the complete finite n6--9 implementation."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
NAME = '65_n6_9_remaining_acquisition_and_join.ipynb'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def document(common_cells, source_instructions):
    base = load('notebook65_base', ROOT / 'tools/make_notebooks.py')
    intro = '''# Berry–Esseen: 65 — complete finite n6–9 acquisition and join

Select **Runtime → Run all** and authorize the same Google Drive used for
notebooks 40–46 and 56K. ''' + source_instructions + '''
Run one active copy of this task. The calculations use the CPU in either a
CPU or GPU runtime.

This notebook performs all 19 selected original remaining calls: auxiliary5,
bridge and radius Fourier covers, complete HIGH, and all 36 support targets
with both signed rays. It reads all 345 required complete parent, resource,
COUNT and scalar inputs, including 284 whole forests and 1,200 probability
panels, then constructs the finite n6→7→8→9 implication.

Missing complete inputs produce a **WAITING** result ZIP. Independent producer
stages can finish while inputs are missing. After the inputs are available,
run all again; compatible complete checked stages are reused. Partial stages
are not accepted. Each original action has its own 23-hour CPU/wall ceiling;
this is a limit, not a predicted duration for the notebook.

The export records conditional finite conclusions and explicit analytical
premises. Notebook completion does not establish the global theorem. The final
cell saves the results ZIP, synchronizes Drive and releases the Colab runtime.
'''
    fixture = '''print("Checking full65 execution and evidence fixtures; no original mathematical kernels run.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite69-join.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest",
                              "tests.test_finite69_full_join.Infrastructure", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, bufsize=1)
    lines = []
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush(); lines.append(line)
    code = child.wait()
if code != 0 or not any(line.startswith("Ran ") for line in lines):
    raise RuntimeError("Full65 infrastructure checks failed or did not run: " + str(DRIVER_SELFTEST))
print("Full65 infrastructure checks: PASS.", flush=True)
'''
    cells = [base.cell('markdown', intro, 'instructions'), *common_cells,
             base.cell('code', fixture, 'finite69-join-fixtures'),
             base.cell('code', 'from be_replay.finite69_join import run_colab\n'
                       'RESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n', 'execute-task'),
             base.finish()]
    doc = base.notebook(cells, NAME)
    for cell in doc['cells']:
        if cell['cell_type'] == 'code':
            compile(''.join(cell['source']), NAME, 'exec')
    return doc


def build(code_commit):
    if type(code_commit) is not str or re.fullmatch('[0-9a-f]{40}', code_commit) is None:
        raise ValueError('An actual immutable full source commit is required')
    base = load('notebook65_public_base', ROOT / 'tools/make_notebooks.py')
    return document(base.common(code_commit, 'finite69-join'),
                    'The pinned published code is fetched automatically; no runtime ZIP upload is required.')


def build_local(source_name, source_sha256):
    local = load('notebook65_runtime', ROOT / 'tools/local_notebook_runtime.py')
    return document(local.common(source_name, source_sha256, 'finite69-join'),
                    'Upload the accompanying exact local source ZIP when requested.')


def write(code_commit, output):
    folder = Path(output)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / NAME
    path.write_text(json.dumps(build(code_commit), ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8', newline='\n')
    return path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--code-commit', required=True)
    parser.add_argument('--output', type=Path, default=ROOT / 'colab')
    args = parser.parse_args()
    print(write(args.code_commit, args.output))
