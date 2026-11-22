# Modul 15: Rumsbokning

Ett litet bokningssystem i Flask och SQLite. Du kan se rummen, boka och se bokningarna. Det är en
**vertikal skiva**: den går hela vägen från formulär via logik till databas, men är långt ifrån färdig.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen (`/ovningar/15`).
> Där arbetar du i ditt eget projekt. Använd det här om du vill öva mer på att bygga med AI,
> eller om du behöver en bas att lära dig på.

## Kör

```bash
cd modul_15_bokning
flask --app app run --debug
```

Öppna `http://127.0.0.1:5000`. Databasen `bokning.db` skapas automatiskt. Radera filen för att börja om.

## Vad som finns och vad som saknas

| Finns | Saknas |
|-------|--------|
| Lista rum och bokningar | Avboka |
| Boka via ett formulär | Kontroll att två inte bokar samma rum samtidigt |
| SQLite med parametriserade frågor | Validering (sluttid före starttid?) |
| | Tester |
| | Inloggning |
| | Ett API som returnerar JSON |

## Prova: ett steg i taget

Följ samma rytm som i övningarna:

1. **Läs koden först.** Be AI:n förklara `book()`, och kontrollera att förklaringen stämmer.
2. **Be om en plan** för det du vill lägga till. Godkänn den innan någon kod skrivs.
3. **Bygg minsta möjliga skiva.** Till exempel: avboka en bokning.
4. **Skriv ett test** som bevisar att det fungerar. Läs testet: testar det verkligen något?
5. **Granska diffen** och committa med ett meddelande som säger vad och varför.
6. **Logga i `AI-logg.md`** (mall finns i `modul_14_projektplan`).

## Börja här: dubbelbokningen

Boka Kajutan 9 till 11, och sedan 10 till 12 samma dag. Det går. I ett riktigt system är det en bugg.

- Be AI:n **argumentera emot** din lösning innan du skriver den: "Vilka fall missar jag?" (Be om motstånd,
  som i övning 5 på portalen.)
- Tänk på gränsfallen: 9 till 11 och 11 till 13 ska väl gå? Vad blir rätt regel?

<details markdown="1">
<summary>Lösningsförslag för överlappskontrollen</summary>

Två bokningar i samma rum samma dag överlappar om `ny.start < befintlig.slut` **och**
`ny.slut > befintlig.start`. Gör kontrollen i en SQL-fråga före `INSERT`, och svara med ett begripligt
felmeddelande om den slår till. Testa 9–11 mot 11–13 (ska gå) och 9–11 mot 10–12 (ska nekas).

</details>

## Fler idéer

- Rutnätsvy: en tabell per dag med lediga och bokade timmar
- `GET /api/bokningar` som returnerar JSON, och en sida som hämtar den med `fetch`
- Begränsa antal bokningar per person och vecka
- Mejlbekräftelse (skriv bara ut i terminalen, skicka ingenting på riktigt)
- Byt SQLite mot en annan databas
