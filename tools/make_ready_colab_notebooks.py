"""Publish-ready Run-all wrappers against a real immutable Git code commit."""
from __future__ import annotations
import argparse,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

base=load('ready_colab_base',ROOT/'tools/make_notebooks.py')
JOBS=(
 ('66_A_40_acquisition_actions','n25-acquisitions','40 oryginalnych działań INITIAL/resources',
  'Dziesięć pełnych rodzin. Każde działanie ma własne23hCPU/wall; ukończony zweryfikowany prefiks jest zachowany.',
  'test_n25_acquisition_runtime.py','from be_replay.n25_acquisitions import run_colab\nRESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n'),
 ('66_B_10_upper_counts','n25-upper10','10 dodatkowych lasów COUNT',
  'Siedem high-beta2 i trzy middle-B3;18978liści. Gotowe oryginalne drzewa, pełna nowa akceptacja. Rozłączne ze starymi26–34.',
  'test_n25_upper_counts.py','from be_replay.n25_upper_counts import run_colab\nRESULT = run_colab("upper-retained-graph", durable_root=DURABLE, backup_interval=60)\n'),
 ('66_C_11_recovered_B5_counts','n25-recovered-original','11 odzyskanych oryginalnych lasów B5',
  '32093liście. Pełny oryginalny akceptor, bez ponownego szukania drzew i bez uruchamiania01–07. Każde działanie ma własne23h.',
  'test_n25_recovered_counts.py','from be_replay.n25_recovered_batch import run_colab\nRESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n'))

def fixtures(pattern):
    return f'''print("Checking execution/evidence fixtures; no original mathematical kernels run in these tests.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-task.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover", "-s", "tests", "-p", {pattern!r}, "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    lines = []
    for line in child.stdout:
        print(line, end="", flush=True); log.write(line); log.flush(); lines.append(line)
    rc = child.wait()
if rc != 0 or not any(line.startswith("Ran ") for line in lines):
    raise RuntimeError("Task infrastructure fixtures failed or did not run; see " + str(DRIVER_SELFTEST))
'''

def build_components(pin):
    if type(pin)is not str or re.fullmatch('[0-9a-f]{40}',pin)is None:
        raise ValueError('An actual immutable full source commit is required')
    result={}
    for name,task,title,scope,pattern,execute in JOBS:
        intro=f'''# Berry–Esseen: {title}

Wybierz **Runtime → Run all** i zezwól na podłączenie tego samego Dysku co wcześniejsze obliczenia.
Kod zostanie automatycznie pobrany z przypiętej opublikowanej wersji. Nie trzeba wgrywać runtime ZIP ani zmieniać parametrów.

{scope}

To samodzielna część obliczeń66; nie wymaga ukończenia57H/58H/67.
Nie jest całym połączeniem n25. Wyniki i zgodne cache są zachowywane.
Uruchamiaj jedną aktywną kopię każdego zadania. CPU lub GPU: arytmetyka używaCPU.
23h to limit pojedynczego działania, nie prognoza czasu całej partii.
Obsłużony błąd daje diagnostyczny ZIP. Końcowa komórka synchronizuje Dysk przed zwolnieniem środowiska.
'''
        cells=[base.cell('markdown',intro,'instructions'),*base.common(pin,task)]
        if task=='n25-acquisitions':cells.append(base.cell('code',fixtures('test_action_supervisor.py'),'action-supervisor-fixtures'))
        cells.extend([base.cell('code',fixtures(pattern),'task-fixtures'),base.cell('code',execute,'execute-task'),base.finish()])
        result[name+'.ipynb']=base.notebook(cells,name+'.ipynb')
    return result

def public_finite(pin):
    result={}
    for unit,file in [('57H','make_finite1519_join_notebook.py'),('67','make_n5_full_join_notebook.py')]:
        module=load('ready_'+unit,ROOT/'tools'/file)
        doc=module.build_local('unused-local-source.zip','1'*64)
        task='finite1519-join'if unit=='57H'else'n5-full-join'
        doc['cells']=[base.common(pin,task)[0]if c['id']=='local-source'else c for c in doc['cells']]
        text=''.join(doc['cells'][0]['source'])
        text=text.replace('Upload the accompanying exact local source ZIP when requested. CPU or GPU',
                          'The code is fetched automatically from its pinned published commit. CPU or GPU')
        text=text.replace('Dołącz podany niżej dokładny pakiet źródeł ZIP. Ten notebook korzysta z jego\nsprawdzonego manifestu, bez zależności od nieopublikowanych commitów.',
                          'Kod zostanie automatycznie pobrany z przypiętego opublikowanego commita.\nNie trzeba wgrywać lokalnego pakietu źródeł.')
        doc['cells'][0]['source']=text.splitlines(keepends=True)
        result[('57H_n15_19_finite_join'if unit=='57H'else'67_n5_full_evidence_and_proof_join')+'.ipynb']=doc
    generator=load('ready_56I',ROOT/'tools/make_finite1014_join_notebook.py')
    result['56I_n10_14_finite_join.ipynb']=generator.build(pin)
    generator=load('ready_65',ROOT/'tools/make_finite69_join_notebook.py')
    result['65_n6_9_remaining_acquisition_and_join.ipynb']=generator.build(pin)
    return result

def write(pin,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    for name,doc in (build_components(pin)|public_finite(pin)).items():
        for cell in doc['cells']:
            if cell['cell_type']=='code':
                compile(''.join(cell['source']),name,'exec')
                assert cell['execution_count']is None and cell['outputs']==[]
        (output/name).write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--code-commit',required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'colab');args=parser.parse_args();print(write(args.code_commit,args.output))
