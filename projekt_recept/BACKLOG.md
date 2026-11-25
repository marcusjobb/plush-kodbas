# Backlog: Recept

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren. Be AI:n om en plan först och godkänn den innan någon kod skrivs.

**Det du tränar:** att byta ut en del av ett system utan att förstöra resten, att granska vad AI föreslår,
och att ha tester som skyddsnät.

## Databas

- [ ] **SQLite i stället för minnet.** Skriv en `SqliteRepository` med samma metoder som `InMemoryRepository`
      och byt en rad i `app.py`. Exempeldatan ska skapas första gången databasen är tom.
- [ ] **Tester mot båda.** Samma tester ska gå igenom oavsett vilket repository som används.
- [ ] **Ingredienser och recept.** Hur ser tabellerna ut? Vad händer med inköpslistan om en ingrediens ändras
      eller tas bort?
- [ ] **Migrationer.** Hur ändrar du tabellerna när modellen ändras, utan att tappa data?

## Granska och förbättra

- [ ] **GDPR.** Gå igenom vilken data programmet samlar in och sparar. Vad behövs för att programmet ska
      fungera? Be AI:n granska, men bedöm själv om svaren håller. Ändra och motivera.
- [ ] **Enheter.** `dl`, `st` och `tsk` är fria textfält. Vad händer med inköpslistan om någon skriver `dl` och
      någon annan `deciliter`? Hur skulle du lösa det?
- [ ] **Felhantering.** Vad händer om någon skickar in ett formulär med konstiga värden? Försök få appen att
      krascha, och rätta det du hittar.

## Gränssnitt

- [ ] **Snygga till.** Gränssnittet är medvetet enkelt. Ge det en egen stil, utan att tappa tillgängligheten.
- [ ] **Lägg till ingredienser utan omladdning.** Formuläret har fem fasta rader. Gör fler rader möjliga.
- [ ] **Mobil.** Gör sidorna användbara i ett kök, på en telefon.

## Funktioner

- [ ] **Redigera ett recept** i stället för att ta bort och lägga till på nytt.
- [ ] **Ta bort en måltid** ur veckoplanen.
- [ ] **Skala inköpslistan.** Planera en måltid för ett annat antal portioner än receptet är skrivet för.
- [ ] **Bocka av** det du har köpt på inköpslistan.
- [ ] **Skriv ut** inköpslistan.
- [ ] **Inloggning.** Vem får se och ändra hushållets recept?
