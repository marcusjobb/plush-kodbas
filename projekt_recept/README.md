# Projekt: Recept

Ett hushåll sparar recept med ingredienser, planerar veckans måltider, får en inköpslista och en varning när
en receptkategori används för ofta under en vecka. Det är ett **skal**: sidorna finns och fungerar, men all
data ligger i minnet och försvinner när du stoppar programmet. Resten bygger du, tillsammans med ditt
AI-verktyg.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen. Använd det när du vill öva på att
> bygga vidare på ett större projekt än de små modulerna.

## Kör

```bash
cd projekt_recept
uv run --with "flask>=3.0" flask --app app run --debug
```

Öppna `http://127.0.0.1:5000`. Tester: `uv run --with "flask>=3.0" python -m unittest`.

## Så hänger det ihop

| Fil | Ansvar |
|-----|--------|
| `app.py` | Routes (sidorna). Kopplar ihop delarna. Här skapas repositoryt, på en enda rad. |
| `templates/`, `static/` | Gränssnittet (Jinja och CSS). Medvetet enkelt. |
| `services.py` | Reglerna: omräkning av portioner, kategorier, veckoplan, inköpslista, varningar. |
| `repository.py` | Allt som sparas och läses. `InMemoryRepository` är en låtsasdatabas. |
| `models.py` | Datan: recept, ingrediens, kock, kategori, inplanerad måltid. |
| `inputs.py` | Tolkar text från formulär till tal och datum. |
| `test_app.py` | Tester för reglerna och sidorna. |

Sidorna pratar bara med `services.py` och `repository.py`. Därför går det att byta ut datalagret utan att
röra gränssnittet.

## Bra att veta

- Mängder visas med högst två decimaler och utan onödiga nollor: `1,5 dl`, `2 st`, `0,25 tsk`.
- När du visar ett recept för ett annat antal portioner räknas mängderna om. Originalet ändras inte.
- Veckan börjar på måndag och slutar på söndag (ISO-veckor). En måltid på en söndag hör till den veckan.
- Inköpslistan summerar samma ingrediens med samma enhet.
- Varje kategori kan ha en gräns för hur många gånger per vecka den får förekomma. Du varnas vid 80 % och
  100 %, och samma varning visas bara en gång per vecka.
- Tar du bort en kategori flyttas recepten till "Övrigt". Den kategorin kan inte tas bort.
- Exempeldatan är vecka 48 2026. Alla namn och recept är påhittade.
- Allt är på svenska i gränssnittet och på engelska i koden.

## Prova

Se [BACKLOG.md](BACKLOG.md). Börja med att be ditt AI-verktyg **läsa koden och förklara den** för dig.
Kontrollera att förklaringen stämmer innan du ändrar något.
