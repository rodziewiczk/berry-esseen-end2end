# Notebooki CPU: wgraj i uruchom wszystko

Każdy notebook ma już ustawione osobne zadanie. W Colabie wybierz **Środowisko wykonawcze → Uruchom wszystko**. Nie trzeba wpisywać poleceń ani zmieniać parametrów.

Na początku Google może poprosić o zgodę na zapis kopii zapasowych na Twoim Dysku. Wyniki trafiają do `MyDrive/Berry-Esseen-end2end/`, do osobnych katalogów z nazwą zadania i czasem uruchomienia.

| Notebook | Zadanie |
|---|---|
| 01 | n25, oryginalne B3 p33 |
| 02–05 | n25, oryginalne B4 q0–q3 |
| 06–07 | n25, nowe warunkowe B3 V14 p31 i p32 |
| 08 | Pełne obliczenia n2 i n3, z osobnym statusem zgodności platformy |

W notebookach 01–07 pierwszy krótki przebieg mierzy rzeczywiste zasoby. Dalsze odcinki wykorzystują do trzech godzin przydzielonego budżetu wyszukiwania. Kompletne drzewo uruchamia osobny natywny akceptor. Niepełny wynik zachowuje checkpointy. Wznowienie tym samym notebookiem szuka najnowszej poprawnej kopii na Dysku, po czym ponownie sprawdza jej zgodność ze źródłami.

Każdy notebook pokazuje postęp: etap, czas, zasoby, liczniki dostępne w checkpointach i stan wyniku. Pełne logi zapisują się również w plikach; kopia na Dysk powstaje co minutę. Końcowy ZIP zawiera źródła danej kapsuły, checkpoint główny i zapasowy, raporty oraz logi. Notebook wyświetla link do ZIP-a i podejmuje próbę jego pobrania.

Kilka notebooków uruchamiaj w oddzielnych sesjach CPU. Każdy ma własne katalogi. Liczbę sesji wyznacza rzeczywisty przydział Colaba; kilka kart w przeglądarce nie oznacza automatycznie kilku maszyn.

**Zakres:** to konkretne zadania odtworzenia, a nie gotowy certyfikat całego dowodu. Same notebooki 01–07 nie sprawdzają wszystkich zasobów rodziców, n4, całej kontynuacji n6–48 ani ogona. Brak akceptacji albo przerwanie nigdy nie daje globalnego PASS.

Kod jest przypięty do konkretnego commita nowego publicznego repo. Źródła i wskazówki wznowienia mają osobne sumy SHA-256. Wskazówki pomagają w szukaniu; każdy liść pełnego drzewa nadal wymaga świeżej weryfikacji.
