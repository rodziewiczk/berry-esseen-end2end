"""Generate the complete57H notebook against a real offline runtime ZIP."""
from __future__ import annotations
import argparse,importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def build_local(source_name,source_sha256):
 base=load('notebook57Hbase',ROOT/'tools/make_notebooks.py')
 local=load('notebook57Hruntime',ROOT/'tools/local_notebook_runtime.py')
 intro='''# Berry–Esseen: 57H — pełny skończony łańcuch n15–19

Uruchom **Run all** na tym samym Dysku co51,56I,56K i57A–G.
Dołącz podany niżej dokładny pakiet źródeł ZIP. Ten notebook korzysta z jego
sprawdzonego manifestu, bez zależności od nieopublikowanych commitów.
W środowisku CPU lub GPU obliczenia wykonuje CPU. Jedna aktywna kopia zadania.

Cały zakres57H obejmuje sześć oryginalnych kontroli, pełne odczyty164 wejść
(56I, sześć rodziców57A–E/56K, dziesięć INITIAL/resource oraz147 COUNT),
wszystkie1000 dyspozycji prawdopodobieństwa i147 jednoczesnych interfejsów
resource/COUNT. Skończona indukcja biegnie14→15→16→17→18→19.

Notebook sprawdza faktyczne źródła, pełne przechwycone wyniki oraz aktualne
rodzicielskie dane dla tej samej zmiennej losowej i progu. Nie zakłada wyniku
eventual20. Jawne ogólne przesłanki analityczne pozostają w eksporcie;
ukończenie notebooka nie oznacza pełnego globalnego dowodu.

Brak kompletnego wejścia daje WAITING i końcowy ZIP. Po jego dostarczeniu
ponów Run all. Ukończony sześciokontrolny etap jest weryfikowany i używany
ponownie; częściowy etap nie jest akceptowany. Oryginalne duże wywołania mają
limity CPU/wall82800s (23h) i2GiB pamięci. To limit działania, nie prognoza
całego notebooka. Postęp jest widoczny co20s, logi zachowywane co60s.
Końcowa komórka synchronizuje Dysk, a następnie zwalnia środowisko Colaba.
'''
 fixtures='''print("Checking full57H source, capture/cache, interface and finite-chain fixtures. Original mathematics is not executed.", flush=True)
DRIVER_SELFTEST = SELFTEST.with_name(SELFTEST.stem + "-finite1519-join.log")
with DRIVER_SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover", "-s", "tests", "-p", "test_finite1519_join*.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Full57H infrastructure checks failed; original control execution will not start: " + str(DRIVER_SELFTEST))
print("Full57H infrastructure checks: PASS.", flush=True)
'''
 cells=[base.cell('markdown',intro,'instructions'),*local.common(source_name,source_sha256,'finite1519-join'),
        base.cell('code',fixtures,'finite1519-join-fixtures'),
        base.cell('code','from be_replay.finite1519_join import run_colab\nRESULT = run_colab(durable_root=DURABLE, backup_interval=60)\n','execute-task'),base.finish()]
 document=base.notebook(cells,'57H_n15_19_finite_join.ipynb')
 for cell in document['cells']:
  if cell['cell_type']=='code':compile(''.join(cell['source']),'57H','exec')
 return document


def write_local(source_name,source_sha256,output):
 doc=build_local(source_name,source_sha256);directory=Path(output);directory.mkdir(parents=True,exist_ok=True)
 path=directory/'57H_n15_19_finite_join.ipynb';path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return path


if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--source-name',required=True);parser.add_argument('--source-sha256',required=True)
 parser.add_argument('--output',type=Path,default=ROOT/'colab');args=parser.parse_args();print(write_local(args.source_name,args.source_sha256,args.output))
