"""Build preconfigured Colab notebooks against an immutable code commit."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ("01_n25_b3_p33", "b3-p33"),
    ("02_n25_b4_q0", "b4-q0"),
    ("03_n25_b4_q1", "b4-q1"),
    ("04_n25_b4_q2", "b4-q2"),
    ("05_n25_b4_q3", "b4-q3"),
    ("06_n25_b3_p31_v14", "b3-p31-v14-new"),
    ("07_n25_b3_p32_v14", "b3-p32-v14-new"),
]

def cell(kind, text, label):
    row = {"cell_type": kind, "id":label, "metadata":{"id":label}, "source":text.splitlines(keepends=True)}
    if kind == "code":
        row.update(execution_count=None, outputs=[])
    return row

def common(pin, task):
    code = f'''from pathlib import Path
import subprocess, sys, json, os, time
CODE_COMMIT = "{pin}"
TASK = "{task}"
REPOSITORY = "https://github.com/rodziewiczk/berry-esseen-end2end.git"
CODE = Path("/content") / ("berry-esseen-code-" + CODE_COMMIT[:12])
print("Pobieram przypięty kod:", CODE_COMMIT, flush=True)
if not CODE.exists():
    subprocess.run(["git", "clone", "--quiet", "--no-checkout", REPOSITORY, str(CODE)], check=True)
    subprocess.run(["git", "-C", str(CODE), "checkout", "--quiet", "--detach", CODE_COMMIT], check=True)
observed = subprocess.check_output(["git", "-C", str(CODE), "rev-parse", "HEAD"], text=True).strip()
if observed != CODE_COMMIT:
    raise RuntimeError("Niezgodny commit źródeł")
subprocess.run(["git", "-C", str(CODE), "diff", "--exit-code", "HEAD", "--"], check=True)
sys.path.insert(0, str(CODE))
from be_replay.environment import snapshot
print(json.dumps(snapshot(), indent=2), flush=True)
print("Kod i środowisko odczytane. To jeszcze nie akceptacja matematyczna.", flush=True)
'''
    drive = '''from google.colab import drive
drive.mount("/content/drive")
DURABLE = Path("/content/drive/MyDrive/Berry-Esseen-end2end")
DURABLE.mkdir(parents=True, exist_ok=True)
print("Logi i checkpointy:", DURABLE, flush=True)
'''
    tests = '''from datetime import datetime, timezone
SELFTEST = DURABLE / ("selftest-" + TASK + "-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".log")
print("Sprawdzam nadzorcę na rzeczywistym Linuksie. To lekkie testy, bez dowodu.", flush=True)
with SELFTEST.open("w", encoding="utf-8") as log:
    child = subprocess.Popen([sys.executable, "-B", "-S", "-m", "unittest", "discover",
                              "-s", "tests", "-p", "test_linux_supervisor.py", "-v"],
                             cwd=CODE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in child.stdout:
        print(line, end="", flush=True)
        log.write(line); log.flush()
    code = child.wait()
if code != 0:
    raise RuntimeError("Test nadzorcy nie przeszedł; obliczenia nie wystartują. Log: " + str(SELFTEST))
print("Test nadzorcy zakończony. Rozpoczynam właściwe zadanie.", flush=True)
'''
    return [
        cell("code", code, "pinned-code"),
        cell("code", drive, "durable-drive"),
        cell("code", tests, "actual-linux-guard-tests"),
    ]

def finish():
    return cell("code", '''from IPython.display import display, FileLink
from google.colab import files
print("Stan:", RESULT["status"]["state"], flush=True)
print("Globalny dowód nie jest oznaczony jako zamknięty.", flush=True)
print("ZIP na Dysku:", RESULT["bundle"], flush=True)
display(FileLink(RESULT["bundle"]))
try:
    files.download(RESULT["bundle"])
except Exception as error:
    print("Pobierz ZIP z podanej ścieżki na Dysku:", error, flush=True)
''', "download-result")

def notebook(cells, title):
    return {"nbformat":4, "nbformat_minor":5,
            "metadata":{"colab":{"name":title,"provenance":[]},
                        "kernelspec":{"name":"python3","display_name":"Python 3"},
                        "language_info":{"name":"python"}},
            "cells":cells}

def make_count(pin, stem, target):
    intro = f'''# Berry–Esseen: {target} — CPU, logi i checkpointy

Wybierz **Środowisko wykonawcze → Uruchom wszystko**. Zadanie jest już ustawione.
Google może poprosić o zgodę na Dysk, aby zachować checkpointy po utracie sesji.
Nie zmieniaj kodu i nie uruchamiaj dwóch kopii tego samego zadania równocześnie.

Najpierw krótki pomiar, potem do 3 godzin przydzielonego wyszukiwania w odcinkach.
Każdy odcinek ma zewnętrzny limit czasu. Kompletne drzewo przechodzi osobny akceptor.
Postęp jest widoczny w komórce oraz w plikach. Wynik częściowy zachowuje obie kopie checkpointu.
Ten notebook dotyczy jednego warunkowego drzewa n25, nie całego twierdzenia.
'''
    cells = [cell("markdown", intro, "instructions"), *common(pin, target)]
    cells.append(cell("code", f'''from be_replay.colab_batch import run_count
RESULT = run_count("{target}", durable_root=DURABLE,
                   total_seconds=10800, slice_seconds=1800, backup_interval=60)
''', "execute-task"))
    cells.append(finish())
    return notebook(cells, stem+".ipynb")

def make_small(pin):
    title = "08_n2_n3_cpu"
    cells = [cell("markdown", """# Berry–Esseen: n2 i n3 — pełne obliczenia CPU

Wybierz **Uruchom wszystko**. Notebook sprawdza całe dostarczone certyfikaty n2 i n3,
kompiluje jądro C++ ze źródeł i zapisuje postęp.
Zgodność oryginalnej ochrony Windows i nowego wykonania Linux jest raportowana osobno.
Sam ten wynik nie zamyka C4 ani całego twierdzenia.
""", "instructions"), *common(pin, "n2-n3")]
    cells.append(cell("code", '''import shutil
if shutil.which("g++") is None or not Path("/usr/include/boost/multiprecision/cpp_int.hpp").exists():
    print("Instaluję kompilator i nagłówki Boost z repozytorium systemowego Colaba.", flush=True)
    subprocess.run(["apt-get", "update", "-qq"], check=True)
    subprocess.run(["apt-get", "install", "-y", "-qq", "g++", "libboost-dev"], check=True)
print("Kompilator:", subprocess.check_output(["g++", "--version"], text=True).splitlines()[0], flush=True)
from be_replay.small_indices import run_colab
RESULT = run_colab(durable_root=DURABLE)
''', "execute-small"))
    cells.append(finish())
    return notebook(cells, title+".ipynb")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, default=ROOT/"colab")
    args = parser.parse_args()
    if not re.fullmatch("[0-9a-f]{40}", args.code_commit):
        raise ValueError("Immutable full Git commit required")
    args.output.mkdir(parents=True, exist_ok=True)
    docs = [(stem, make_count(args.code_commit, stem, target)) for stem,target in TARGETS]
    docs.append(("08_n2_n3_cpu", make_small(args.code_commit)))
    for stem, doc in docs:
        for item in doc["cells"]:
            if item["cell_type"] == "code":
                compile("".join(item["source"]), stem, "exec")
        path = args.output/(stem+".ipynb")
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(path)
    # The repository landing page links this preconfigured first task.
    (args.output/"count_cpu.ipynb").write_text(
        json.dumps(docs[0][1], ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
