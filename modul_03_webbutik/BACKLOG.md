# Backlog: Webbutiken

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren.

**Det du tränar i den här modulen:** att låta AI skriva kod utifrån en specifikation, att felsöka med
hypoteser (momsbuggen!), och att refaktorisera i små steg med tester som skyddsnät.

## Lätt

- [ ] **`fetch` på "Lägg i varukorgen".** Antalet i menyn uppdateras utan att sidan laddas om. Det behövs en
      route som svarar med JSON.
- [ ] **Plus och minus** för antal i varukorgen, också utan omladdning
- [ ] **Töm varukorgen** med ett klick
- [ ] **Sökfält** som filtrerar produkterna medan du skriver

## Mellan

- [ ] **Lagersaldo.** Ett fel om du försöker köpa mer än det finns. Visa "Slut" på varan.
- [ ] **Rabattkod** (till exempel `JULEN10`). Vad händer med moms och avrundning när rabatten ges?
- [ ] **Orderhistorik** i SQLite, med en sida som visar dina tidigare köp
- [ ] **Sortera och filtrera** på pris och momssats
- [ ] **Fraktkostnad** som beror på summan ("fri frakt över 500 kr"). Är gränsen före eller efter moms?
- [ ] **Hitta fler buggar.** Räkna efter för hand i flera fall (stora antal, flera momssatser, rabatt). Skriv
      ett test för varje fel du hittar, innan du rättar det.
- [ ] **Flytta beräkningarna** ur `app.py` till en egen fil som går att testa utan Flask

## Svårt

- [ ] **Inloggning** och en adminsida där man lägger till produkter. Tänk på lösenord: lagra aldrig
      klartext.
- [ ] **Två köper den sista varan samtidigt.** Kan du få webbutiken att sälja en vara två gånger? Skriv
      ett test som visar problemet, och lös det.
- [ ] **Byt sessionen mot en databas** för varukorgen, så att den följer med mellan enheter
- [ ] **En enkel betalningsflöde-simulering:** en `webhook` som "betalningstjänsten" anropar när betalningen
      är klar, och som markerar ordern som betald. Vad händer om anropet kommer två gånger?
- [ ] **Flera valutor** (SEK och EUR) med en kurs i en fil. Var ska avrundningen ske?

## Utmaning: jämför verktyg

- [ ] Ge samma uppgift (till exempel lagersaldot) till två olika AI-verktyg. Läs båda diffarna. Vilken
      följde specifikationen bäst, och vilken hittade kantfall du inte tänkt på?

## Regler för alla kort

- Ett kort i taget, på en egen gren
- Skriv testet först, eller åtminstone samtidigt. Kör alla tester innan du checkar in
- Läs diffen innan du committar. Du ska kunna förklara varje rad
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`)
