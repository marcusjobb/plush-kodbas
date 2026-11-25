# Backlog: Hushållsbudget

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren. Be AI:n om en plan först och godkänn den innan någon kod skrivs.

**Det du tränar:** att byta ut en del av ett system utan att förstöra resten, att granska vad AI föreslår,
och att ha tester som skyddsnät.

## Databas

- [ ] **SQLite i stället för minnet.** Skriv en `SqliteRepository` med samma metoder som `InMemoryRepository`
      och byt en rad i `app.py`. Exempeldatan ska skapas första gången databasen är tom.
- [ ] **Tester mot båda.** Samma tester ska gå igenom oavsett vilket repository som används.
- [ ] **Belopp i databasen.** Hur sparar du pengar utan att få avrundningsfel? Jämför några alternativ.
- [ ] **Migrationer.** Hur ändrar du tabellerna när modellen ändras, utan att tappa data?

## Granska och förbättra

- [ ] **GDPR.** Gå igenom vilken data programmet samlar in och sparar. Vad behövs för att programmet ska
      fungera? Be AI:n granska, men bedöm själv om svaren håller. Ändra och motivera.
- [ ] **Beloppstecknet.** Är det en bra idé att en utgift är ett negativt tal? Vad blir enklare med ett eget
      fält för typ?
- [ ] **Felhantering.** Vad händer om någon skickar in ett formulär med konstiga värden? Försök få appen att
      krascha, och rätta det du hittar.

## Gränssnitt

- [ ] **Snygga till.** Gränssnittet är medvetet enkelt. Ge det en egen stil, utan att tappa tillgängligheten.
- [ ] **Diagram** över utgifter per kategori på månadsöversikten.
- [ ] **Mobil.** Gör sidorna användbara på en telefon.

## Funktioner

- [ ] **Redigera en transaktion** i stället för att ta bort och lägga till på nytt.
- [ ] **Sök och filtrera** transaktionerna på kategori och text.
- [ ] **Återkommande transaktioner**, till exempel hyra varje månad.
- [ ] **Export till CSV.**
- [ ] **Inloggning.** Vem får se hushållets pengar?
