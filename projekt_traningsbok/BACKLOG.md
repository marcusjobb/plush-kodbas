# Backlog: Träningsbok

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren. Be AI:n om en plan först och godkänn den innan någon kod skrivs.

**Det du tränar:** att byta ut en del av ett system utan att förstöra resten, att granska vad AI föreslår,
och att ha tester som skyddsnät.

## Databas

- [ ] **SQLite i stället för minnet.** Skriv en `SqliteRepository` med samma metoder som `InMemoryRepository`
      och byt en rad i `app.py`. Exempeldatan ska skapas första gången databasen är tom.
- [ ] **Tester mot båda.** Samma tester ska gå igenom oavsett vilket repository som används.
- [ ] **Vikt i databasen.** Hur sparar du kilo med decimaler utan att få avrundningsfel? Jämför några alternativ.
- [ ] **Relationer.** Ett pass har många övningar och tillhör en utövare. Hur ser tabellerna ut, och vad händer
      med övningarna när ett pass tas bort?

## Granska och förbättra

- [ ] **GDPR.** Gå igenom vilken data programmet samlar in och sparar. Vad behövs för att programmet ska
      fungera? Be AI:n granska, men bedöm själv om svaren håller. Ändra och motivera.
- [ ] **Träningstyp som text.** Passet sparar träningstypens namn. Vad händer om någon byter namn på en typ?
      Vad blir bättre med en koppling via id?
- [ ] **Felhantering.** Vad händer om någon skickar in ett formulär med konstiga värden? Försök få appen att
      krascha, och rätta det du hittar.

## Gränssnitt

- [ ] **Snygga till.** Gränssnittet är medvetet enkelt. Ge det en egen stil, utan att tappa tillgängligheten.
- [ ] **Diagram** över träningstid per vecka, med veckomålet som en linje.
- [ ] **Mobil.** Gör sidorna användbara på en telefon, i gymmet.

## Funktioner

- [ ] **Redigera ett pass** i stället för att ta bort och lägga till på nytt.
- [ ] **Personliga rekord.** Visa högsta vikt per övning över tid, inte bara det högsta.
- [ ] **Veckomål per utövare** i stället för ett gemensamt mål.
- [ ] **Export till CSV.**
- [ ] **Inloggning.** Vem får se vems pass?
