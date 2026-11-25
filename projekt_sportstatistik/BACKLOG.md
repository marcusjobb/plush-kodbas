# Backlog: Sportstatistik

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren. Be AI:n om en plan först och godkänn den innan någon kod skrivs.

**Det du tränar:** att byta ut en del av ett system utan att förstöra resten, att granska vad AI föreslår,
och att ha tester som skyddsnät.

## Databas

- [ ] **SQLite i stället för minnet.** Skriv en `SqliteRepository` med samma metoder som `InMemoryRepository`
      och byt en rad i `app.py`. Exempeldatan ska skapas första gången databasen är tom.
- [ ] **Tester mot båda.** Samma tester ska gå igenom oavsett vilket repository som används.
- [ ] **Tabellen i SQL.** Räkna fram tabellen med en fråga (`GROUP BY`) i stället för i Python. Vad blir
      enklare, och vad blir svårare att testa?
- [ ] **Migrationer.** Hur ändrar du tabellerna när modellen ändras, utan att tappa data?

## Granska och förbättra

- [ ] **GDPR.** Gå igenom vilken data programmet samlar in och sparar om spelarna. Vad behövs för att
      programmet ska fungera? Be AI:n granska, men bedöm själv om svaren håller. Ändra och motivera.
- [ ] **Positionen som text.** Spelaren sparar positionens namn. Vad händer om en position byter namn? Prova
      ett `position_id` i stället och se vad som måste ändras.
- [ ] **Varningens minne.** Vilka varningar som redan visats ligger i minnet i `SquadLimitService`. Vad händer
      när programmet startas om, eller körs i två processer?
- [ ] **Felhantering.** Försök få appen att krascha med konstiga formulärvärden, och rätta det du hittar.

## Gränssnitt

- [ ] **Snygga till.** Gränssnittet är medvetet enkelt. Ge det en egen stil, utan att tappa tillgängligheten.
- [ ] **Tabellen som ser ut som en tabell.** Markera täten och nedflyttningsplatserna.
- [ ] **Mobil.** Gör sidorna användbara på en telefon.

## Funktioner

- [ ] **Redigera en match** i stället för att ta bort och lägga till på nytt.
- [ ] **Lagets sida** med dess matcher och form de senaste fem matcherna.
- [ ] **Målskyttar.** Vem gjorde målen? Hur ändrar det modellen?
- [ ] **Flytta en spelare** mellan lag, och se hur truppgränserna reagerar.
- [ ] **Export till CSV.**
- [ ] **Inloggning.** Vem får registrera resultat?
