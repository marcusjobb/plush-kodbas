# Projekt: Sportstatistik

En korpserie i fotboll registrerar lag, spelare och matcher, ser tabellen för en säsong och får en varning när ett
lag närmar sig sin truppgräns. Det är ett **skal**: sidorna finns och fungerar, men all data ligger i minnet och
försvinner när du stoppar programmet. Resten bygger du, tillsammans med ditt AI-verktyg.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen. Använd det när du vill öva på att
> bygga vidare på ett större projekt än de små modulerna.

## Kör

```bash
cd projekt_sportstatistik
uv run --with "flask>=3.0" flask --app app run --debug
```

Öppna `http://127.0.0.1:5000`. Tester: `uv run --with "flask>=3.0" python -m unittest`.

## Så hänger det ihop

| Fil | Ansvar |
|-----|--------|
| `app.py` | Routes (sidorna). Kopplar ihop delarna. Här skapas repositoryt, på en enda rad. |
| `templates/`, `static/` | Gränssnittet (Jinja och CSS). Medvetet enkelt. |
| `services.py` | Reglerna: tabell, truppgränser, varningar, positioner, formatering av resultat. |
| `repository.py` | Allt som sparas och läses. `InMemoryRepository` är en låtsasdatabas. |
| `models.py` | Datan: lag, spelare, position, match, truppgräns, tabellrad. |
| `inputs.py` | Tolkar text från formulär till tal och datum. |
| `test_app.py` | Tester för reglerna och sidorna. |

Sidorna pratar bara med `services.py` och `repository.py`. Därför går det att byta ut datalagret utan att
röra gränssnittet.

## Bra att veta

- En säsong är ett kalenderår: en match den 31 december hör till det årets säsong.
- Tabellen sorteras på poäng, sedan målskillnad, sedan gjorda mål, sedan lagnamn. Vinst ger 3 poäng, oavgjort 1.
- Resultat visas som `2–1` och målskillnad alltid med tecken: `+3`, `-2` och `0`.
- Varningen kommer vid 80 % och 100 % av truppgränsen, och samma varning visas bara en gång per säsong.
  Spelarna räknas för laget, inte per säsong, och varningen gäller innevarande år.
- Exempeldatan är sex matcher i maj och juni 2026. Alla namn och resultat är påhittade.
- Allt är på svenska i gränssnittet och på engelska i koden.

## Prova

Se [BACKLOG.md](BACKLOG.md). Börja med att be ditt AI-verktyg **läsa koden och förklara den** för dig.
Kontrollera att förklaringen stämmer innan du ändrar något.
