# Backlog: Rumsbokning

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren.

**Det du tränar i den här modulen:** att bygga en **vertikal skiva** (formulär, logik, databas) med AI-stöd,
att granska diffen kritiskt och att be om motstånd. Ett kort är lagom stort när du kan visa att det
fungerar med ett test.

## Lätt

- [ ] **Avboka** en bokning
- [ ] **Validera tiden:** sluttiden måste vara efter starttiden, och inom öppettiderna
- [ ] **Meddelande efter bokning** ("Bokat!" eller varför det inte gick)
- [ ] **Sortera** bokningarna på dag och rum

## Mellan

- [ ] **Dubbelbokning.** Två bokningar får inte överlappa i samma rum. Bestäm gränsfallen först: får 9–11
      följas av 11–13? Be AI:n argumentera emot din lösning innan du skriver den.
- [ ] **Lediga tider:** visa vilka timmar som är lediga per rum och dag
- [ ] **Rutnätsvy:** en tabell per dag med rum som kolumner och timmar som rader
- [ ] **JSON-API** (`GET /api/bokningar`) och en sida som hämtar den med `fetch`
- [ ] **Begränsa** hur många timmar en person får boka per vecka
- [ ] **Återkommande bokningar** ("varje måndag kl. 10 i sex veckor"). Vad händer om en vecka redan är upptagen?
- [ ] **Exportera till kalender:** skapa en `.ics`-fil som man kan öppna i en kalenderapp
- [ ] **Tester** med Flasks testklient och en tillfällig databas, så att de inte rör `bokning.db`
- [ ] **Bekräftelsemejl** (skriv bara ut det i terminalen, skicka inget på riktigt)

## Svårt

- [ ] **Inloggning**, så att man bara kan avboka sina egna bokningar
- [ ] **Adminsida** för att lägga till och ta bort rum
- [ ] **Väntelista:** blir en tid ledig får nästa person i kön den
- [ ] **Live-uppdatering:** när någon annan bokar syns det på din sida utan omladdning
- [ ] **Två bokar samtidigt:** kan du få systemet att dubbelboka trots din kontroll? Skriv ett test som
      visar det, och lös det.
- [ ] **Byt databas**, till exempel till PostgreSQL i en Docker-container
- [ ] **Paketera** i Docker så att vem som helst kan starta det med ett kommando

## Utmaning: arbetssättet

- [ ] **Be om motstånd.** Beskriv ditt nästa kort och be AI:n hitta fem sätt det kan gå fel. Hur många
      var relevanta? Spara svaret i din AI-logg.
- [ ] **Granska diffen med frågorna:** gör koden det jag bad om, och inget mer? Finns något den hittat på?
      Vad saknas?

## Tänk på

- Använd bara påhittade namn i bokningarna. Bokningsdata är personuppgifter.

## Regler för alla kort

- Ett kort i taget, på en egen gren
- Skriv testet först, eller åtminstone samtidigt. Kör alla tester innan du checkar in
- Läs diffen innan du committar. Du ska kunna förklara varje rad
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`)
