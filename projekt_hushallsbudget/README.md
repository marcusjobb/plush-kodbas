# Projekt: Hushållsbudget

Ett hushåll registrerar inkomster och utgifter, ser en översikt per månad och får en varning när en kategori
närmar sig sin budget. Det är ett **skal**: sidorna finns och fungerar, men all data ligger i minnet och
försvinner när du stoppar programmet. Resten bygger du, tillsammans med ditt AI-verktyg.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen. Använd det när du vill öva på att
> bygga vidare på ett större projekt än de små modulerna.

## Kör

```bash
cd projekt_hushallsbudget
uv run --with "flask>=3.0" flask --app app run --debug
```

Öppna `http://127.0.0.1:5000`. Tester: `uv run --with "flask>=3.0" python -m unittest`.

## Så hänger det ihop

| Fil | Ansvar |
|-----|--------|
| `app.py` | Routes (sidorna). Kopplar ihop delarna. Här skapas repositoryt, på en enda rad. |
| `templates/`, `static/` | Gränssnittet (Jinja och CSS). Medvetet enkelt. |
| `services.py` | Reglerna: summor, budgetstatus, varningar, kategorier. |
| `repository.py` | Allt som sparas och läses. `InMemoryRepository` är en låtsasdatabas. |
| `models.py` | Datan: hushåll, medlem, kategori, transaktion. |
| `inputs.py` | Tolkar text från formulär till tal och datum. |
| `test_app.py` | Tester för reglerna och sidorna. |

Sidorna pratar bara med `services.py` och `repository.py`. Därför går det att byta ut datalagret utan att
röra gränssnittet.

## Bra att veta

- Belopp sparas med tecken: en utgift är ett negativt tal och en inkomst ett positivt.
- Exempeldatan är november 2026. Alla namn och belopp är påhittade.
- Budgetvarningen kommer vid 80 % och 100 %, och samma varning visas bara en gång per månad.
- Allt är på svenska i gränssnittet och på engelska i koden.

## Prova

Se [BACKLOG.md](BACKLOG.md). Börja med att be ditt AI-verktyg **läsa koden och förklara den** för dig.
Kontrollera att förklaringen stämmer innan du ändrar något.
