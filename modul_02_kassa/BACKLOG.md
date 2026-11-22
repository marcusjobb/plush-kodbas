# Backlog: Kassan

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit: det är de som du
får avgöra. Välj ett kort i taget, på en egen gren.

**Det du tränar i den här modulen:** att ge AI-verktyget en bra grund att stå på (`AGENTS.md`), att planera
före du kör, och att jämföra verktyg. Därför har flera kort en fråga till dig: *vilket verktyg gjorde det
bäst, och varför?*

## Lätt

- [ ] **Rabatt i procent** på en vara, och på hela kvittot. Vad ska hända om rabatten blir över 100 %?
- [ ] **Ångra** den senaste raden (meny 4). Lägg logiken i `kassa_logic.py`.
- [ ] **Kvitto med linjerade kolumner** i fast bredd, så att beloppen står under varandra
- [ ] **Antal per vara** ("3 st kaffe") i stället för en rad per styck

## Mellan

- [ ] **Artikelregister.** Läs varor och priser ur en JSON-fil, så att man väljer "kaffe" i stället för att
      skriva pris för hand. Vad händer med en vara som inte finns?
- [ ] **Spara och läsa in ett kvitto** från fil. Ge filen ett versionsfält.
- [ ] **Betalning och växel.** Ta emot en summa och räkna ut växeln. Gör det i mynt och sedlar. Bestäm vilka
      valörer du har, och hur du hanterar öresavrundning vid kontantbetalning (kontanta belopp avrundas
      till hela kronor i Sverige).
- [ ] **Dagskassa.** Summera dagens kvitton och visa moms per momssats. Det är vad en riktig kassa gör vid
      stängning. Tänk på att summorna ska gå ihop på öret.
- [ ] **Pant och gåvokort**, som inte beskattas som vanliga varor. Läs på först, och skriv ner vad du kommer fram till.

## Svårt

- [ ] **Webbkassa** med Flask, där varorna läggs till utan att sidan laddas om (jämför `modul_03_webbutik`)
- [ ] **Kvittot som HTML eller PDF** som går att skriva ut
- [ ] **Flera kassörer** med inloggning, och en rapport per kassör. Vilka personuppgifter hanterar du då?

## Utmaning för modulens tema: instruktionsfilen

- [ ] **Mät din `AGENTS.md`.** Skriv en regel som är lätt att kontrollera ("belopp är alltid `Decimal`, aldrig
      `float`"). Be två olika verktyg lägga till samma funktion, tio gånger vardera, och räkna hur ofta de
      bryter regeln. Ändra formuleringen av regeln och mät igen. Vad hjälpte?
- [ ] **Planläge mot direkt körning.** Ge samma uppgift (till exempel dagskassan) i planläge respektive
      direkt. Vilken diff var lättast att granska, och vilken blev bäst?

## Regler för alla kort

- Ett kort i taget, på en egen gren
- Skriv testet först, eller åtminstone samtidigt. Kör alla tester innan du checkar in
- Läs diffen innan du committar. Du ska kunna förklara varje rad
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`)
