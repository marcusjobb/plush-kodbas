# Backlog: Kundregistret

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren.

**Det du tränar i den här modulen:** kvalitetssäkring av ett helt projekt: hemligheter, beroenden,
regelverk och etik, kamratgranskning och en gapanalys. Brister som hittas ska också rättas, med bevis.

## Lätt

- [ ] **Flytta hemligheterna** till miljövariabler, och lägg en `.env.exempel` utan riktiga värden
- [ ] **Parametriserade SQL-frågor** i stället för f-strängar. Skriv först en indata som visar problemet,
      i din egen kopia och mot din egen databas.
- [ ] **Sluta skriva ut hemligheter** och personuppgifter i loggen
- [ ] **`.gitignore`** för databasfil, `.env` och annat som inte ska med

## Mellan

- [ ] **Uppdatera beroendet** och kör `pip-audit`. Vad hittade verktyget, och vad gjorde du åt det?
- [ ] **Rätten att se sina uppgifter:** en funktion som exporterar allt som finns om en kund
- [ ] **Rätten att bli raderad:** en funktion som tar bort en kund, och en kontroll att inget finns kvar
- [ ] **Gallring:** kunder som inte varit aktiva på ett år ska rensas bort. Vem bestämmer tiden?
- [ ] **Validera indata:** e-postadress, namnlängd, tomma fält
- [ ] **Lösenord på rätt sätt:** spara aldrig klartext. Titta på `hashlib` i standardbiblioteket och läs
      varför en vanlig snabb hash inte räcker.
- [ ] **Tester**, inklusive ett test som försöker en injektion och kontrollerar att den misslyckas
- [ ] **Bekräftelse före "radera allt"**, och bestäm om den funktionen över huvud taget ska finnas

## Svårt

- [ ] **Pre-commit-kontroll för hemligheter.** Ett skript som körs före varje commit och stoppar den om
      det hittar något som liknar en nyckel eller ett lösenord. Testa det på dina egna misstag.
- [ ] **Granskningslogg:** vem läste eller ändrade vilken kund och när? Det är personuppgifter i sig,
      så vem får läsa loggen?
- [ ] **Kryptera fält** i databasen (till exempel e-post). Var förvarar du nyckeln?
- [ ] **API med inloggning** i Flask, och en gräns för hur många anrop man får göra
- [ ] **Skriv en kort konsekvensbedömning:** vilka personuppgifter finns, varför, hur länge, vem har åtkomst,
      och vilka risker ser du?

## Utmaning: granska granskaren

- [ ] **Mät AI:ns granskning.** Gör först en egen lista över bristerna. Be sedan ett AI-verktyg granska
      koden. Räkna hur många av de verkliga bristerna det hittade, och hur många falska larm det hade.
      Upprepa med ett annat verktyg eller en annan prompt. Vad lär du dig om hur mycket man kan lita på en
      AI-granskning?
- [ ] **Kamratgranskning.** Byt med en kurskamrat: granska varandras fynd och fixar och diskutera det ni
      inte är överens om.
- [ ] **Gapanalys:** vad skulle fattas för att det här skulle gå att lämna ifrån sig till en kund?

## Tänk på

- Alla uppgifter, nycklar och lösenord i registret är påhittade. Lägg aldrig in riktiga i din egen version.

## Regler för alla kort

- Ett kort i taget, på en egen gren
- Skriv testet först, eller åtminstone samtidigt. Kör alla tester innan du checkar in
- Läs diffen innan du committar. Du ska kunna förklara varje rad
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`)
