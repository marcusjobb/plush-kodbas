# logganalys (README att granska)

Ett kraftfullt verktyg för att analysera loggar snabbt och säkert.

## Installation

```bash
pip install logganalys
```

## Användning

```bash
python logganalys.py data/app.log
python logganalys.py data/app.log --level ERROR
python logganalys.py data/app.log --since 2026-11-02
python logganalys.py data/app.log --json > rapport.json
```

## Funktioner

- Läser loggar av valfritt format
- Räknar rader per nivå (INFO, WARNING, ERROR, DEBUG)
- Visar de tre vanligaste felen
- Filtrerar på nivå och datum
- Exporterar till JSON och CSV
- Hanterar loggfiler på flera gigabyte utan problem

## Tester

Alla funktioner har full testtäckning.

```bash
pytest
```
