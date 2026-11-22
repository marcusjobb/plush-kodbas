# Modul 17: Testning, dokumentation och automatisering

En liten loggfilsanalys, och två saker som ser bra ut men inte är det: testerna och dokumentationen.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen (`/ovningar/17`).
> Där arbetar du i ditt eget projekt. Här får du material där det finns något att hitta.

## Kör

```bash
cd modul_17_testning
python logganalys.py data/app.log
python logganalys.py data/app.log --level ERROR
python -m unittest
```

Testerna går igenom, och de anropar alla funktioner utom `main`. Ändå är de nästan värdelösa: de
kontrollerar nästan aldrig *vad* funktionerna returnerar.

## Prova

### 1. Testa testerna

Gör ändringar i `logganalys.py` en i taget och kör testerna efter varje:

- Ändra `LEVELS` så att `"WARNING"` saknas
- Byt `most_common(limit)` mot `most_common(limit + 1)`
- Låt `parse_line` returnera `{}` i stället för `None` för skräprader
- Ta bort `.rstrip(":")`

Hur många av ändringarna upptäcktes? Be AI:n skriva det test som hade fångat varje ändring som slank förbi.
Återställ koden med `git restore logganalys.py` efteråt.

### 2. Dokumentation som stämmer

Öppna `dokumentation_att_granska.md`. Det är en README som en AI skulle kunna ha skrivit. Gå igenom varje
påstående och markera med ✔ eller ✘. Vilka kommandon fungerar? Vilka funktioner finns på riktigt?
Följ den som om du aldrig sett projektet förut.

<details markdown="1">
<summary>Lösningsförslag: vad som är fel i README:n</summary>

- `pip install logganalys` finns inte. Det är inget paket.
- `--since` och `--json` finns inte i koden.
- Nivån `DEBUG` stöds inte, bara INFO, WARNING och ERROR.
- "Valfritt format" stämmer inte. Bara raderna `DATUM TID NIVÅ källa: meddelande` fungerar.
- Export till JSON och CSV finns inte.
- Ingen prestandatest har gjorts. Filen läses in i minnet, så "flera gigabyte utan problem" är ett påstående utan stöd.
- `pytest` är inte installerat och behövs inte, testerna körs med `unittest`.
- "Full testtäckning" säger inget, se övning 1.

</details>

### 3. Automatisera en uppgift

Välj en liten återkommande uppgift och bygg en agent eller ett skript för den. Förslag med den här koden:

- Skriv en sammanfattning av nattens fel och spara den som en fil
- Hitta funktioner som saknar docstring
- Generera en loggfil med påhittad testdata

Ge agenten bara de behörigheter den behöver. Kör den på en egen gren och godkänn stegen första gången.

### 4. Testa agentens gränser

Kör din agent när det inte finns något att göra (en tom loggfil), på en trasig fil, och på en fil där
en rad innehåller en text som försöker styra den. Gör bara det på en egen gren och bara med en ofarlig
instruktion. Vad hände, och vilken behörighet hade begränsat skadan?
