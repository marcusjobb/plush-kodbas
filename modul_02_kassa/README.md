# Modul 02: Kassan

Ett menyprogram i konsolen som räknar ut ett kvitto med moms. Koden är medvetet uppdelad i
`kassa_logic.py` (beräkningar) och `kassa.py` (menyn), så att logiken går att testa.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen (`/ovningar/02`).
> I övningarna bygger du din egen Kvittoräknare från noll. Här får du något som redan fungerar.

## Kör

```bash
cd modul_02_kassa
python kassa.py
python -m unittest        # kör testerna
```

## Det som saknas, med flit

Det finns ingen `AGENTS.md`, ingen `.gitignore` och ingen Git-historik för mappen. Det är din lekplats.

## Prova

1. Starta ditt AI-verktyg i mappen och fråga: "Vilka regler gäller i det här projektet?" Vad svarar det
   utan en `AGENTS.md`?
2. Skriv en `AGENTS.md` (max ca 20 rader) och ställ samma fråga igen. Vad ändrades?
3. Lägg till en regel som går att kontrollera, till exempel "Belopp är alltid `Decimal`". Be verktyget
   lägga till en rabatt-funktion och se om regeln följs.
4. Be verktyget **planera** (planläge) hur kassan ska spara kvittot till en JSON-fil, innan det skriver kod.
   Läs planen. Vad skulle du ändra?
5. Ge samma uppgift ("lägg till rabatt i procent") till två olika verktyg. Jämför diffarna.

## Idéer att bygga vidare på

- Rabatt i procent eller i kronor
- Spara och läsa in ett kvitto från fil
- Skriv ut kvittot i fast bredd, med kolumner som linjerar
- Fler momssatser eller undantag (pant, gåvokort)
