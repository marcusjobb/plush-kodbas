# Projekt: Träningsbok

En utövare registrerar träningspass och övningar, ser hur träningen fördelar sig per vecka och får ett
meddelande när ett veckomål närmar sig eller är nått. Det är ett **skal**: sidorna finns och fungerar, men all
data ligger i minnet och försvinner när du stoppar programmet. Resten bygger du, tillsammans med ditt
AI-verktyg.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen. Använd det när du vill öva på att
> bygga vidare på ett större projekt än de små modulerna.

## Kör

```bash
cd projekt_traningsbok
uv run --with "flask>=3.0" flask --app app run --debug
```

Öppna `http://127.0.0.1:5000`. Tester: `uv run --with "flask>=3.0" python -m unittest`.

## Så hänger det ihop

| Fil | Ansvar |
|-----|--------|
| `app.py` | Routes (sidorna). Kopplar ihop delarna. Här skapas repositoryt, på en enda rad. |
| `templates/`, `static/` | Gränssnittet (Jinja och CSS). Medvetet enkelt. |
| `services.py` | Reglerna: veckor, summor, veckomål, meddelanden, träningstyper. |
| `repository.py` | Allt som sparas och läses. `InMemoryRepository` är en låtsasdatabas. |
| `models.py` | Datan: utövare, träningstyp, pass, övning. |
| `inputs.py` | Tolkar text från formulär till tal och datum. |
| `test_app.py` | Tester för reglerna och sidorna. |

Sidorna pratar bara med `services.py` och `repository.py`. Därför går det att byta ut datalagret utan att
röra gränssnittet.

## Bra att veta

- Veckan börjar på måndag (ISO-veckor). Ett pass på söndag hör till veckan som slutar den dagen.
- Vikt visas som `62,5 kg` och tid som `1 h 05 min`, eller `45 min` under en timme.
- Veckomålet ger meddelande vid 80 % och 100 %, och samma meddelande visas bara en gång per vecka.
- Tar du bort en träningstyp flyttas passen till "Övrigt". "Övrigt" kan inte tas bort.
- Exempeldatan är november 2026 (vecka 46 och 47). Alla namn och värden är påhittade.
- Allt är på svenska i gränssnittet och på engelska i koden.

## Prova

Se [BACKLOG.md](BACKLOG.md). Börja med att be ditt AI-verktyg **läsa koden och förklara den** för dig.
Kontrollera att förklaringen stämmer innan du ändrar något.
