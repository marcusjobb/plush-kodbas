# Modul 04 och 05: Prompt och promptbaserad interaktion

Ett litet ärendesystem i konsolen. Här finns ingen video att följa med, och kodens uppgift är att ge dig
något konkret att ställa prompter mot. Du lär dig skillnaden på en bra och en dålig prompt genom att se
vad koden blir.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen (`/ovningar/04` och `/ovningar/05`).
> Gör övningarna först. Använd det här när du vill träna mer på riktig kod.

## Kör

```bash
cd modul_04_05_prompt
python supportarenden.py
```

## Prova: samma uppgift, tre promptar

Uppgift: **lägg till prioritet på ärenden** (låg, normal, hög) och sortera listan efter den.

Spara varje försök på en egen gren och kasta det med `git restore .` när du har jämfört.

1. **Slarvig:** "Lägg till prioritet."
2. **Med kontext:** beskriv vem som använder programmet, vilka filer som finns och vilken stil koden har.
3. **Med specifikation:** syfte, indata, utdata, kantfall (vad händer om någon skriver "urgent"?) och
   begränsningar (inga nya beroenden, tester för varje kantfall).

Jämför de tre diffarna. Vad hade du själv glömt att fråga efter?

## Fler uppgifter att prompta

- Spara ärenden till en JSON-fil och läs in dem vid start
- Sökfunktion på rubrik och kund
- Statistik: hur många är öppna, hur gammalt är det äldsta?
- Låt AI:n **ställa frågor** till dig innan den skriver kod ("Ställ upp till fem frågor först")
- Be om tre olika lösningar och motivera vilken du väljer

## Att tänka på

- Använd bara påhittade kundnamn. Ett riktigt ärendesystem innehåller personuppgifter, och dem klistrar
  man inte in i ett AI-verktyg utan att ha kollat vad som gäller.

**Fler idéer:** se [BACKLOG.md](BACKLOG.md). Det är förslag att inspireras av, inga krav.
