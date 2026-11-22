# Backlog: Loganalys

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren.

**Det du tränar i den här modulen:** att kontrollera AI-genererade tester och dokumentation, och att
automatisera en liten uppgift med en agent som har begränsade rättigheter.

## Lätt

- [ ] **Gör README:n sann.** `dokumentation_att_granska.md` lovar `--since`, `--json` och nivån `DEBUG`.
      Bygg det den lovar, ett löfte i taget, med ett test för varje.
- [ ] **Starka tester.** Skriv om de svaga testerna så att de kontrollerar *värden*, inte bara att något
      returneras. Kör sedan sabotagen från README:n igen. Hur många upptäcks nu?
- [ ] **Räkna per källa** (`betalning`, `inloggning`, `lager`)
- [ ] **Trasiga rader:** visa hur många rader som inte gick att tolka, i stället för att tyst hoppa över dem

## Mellan

- [ ] **Mutationstest.** Skriv ett skript som ändrar koden ett ställe i taget, kör testerna och räknar vad
      som upptäcks. (Samma idé finns i `modul_16_felsokning`.)
- [ ] **Histogram per timme** i terminalen, med staplar av `#`
- [ ] **Larmgräns:** skriv ut en varning om felen är fler än en viss andel av raderna
- [ ] **Följ filen** (som `tail -f`): läs nya rader medan de skrivs
- [ ] **Exportera till CSV**
- [ ] **Läs filen rad för rad.** Idag läses hela filen in i minnet. Bygg om till en generator och
      **mät** med `tracemalloc` hur mycket minne det sparar. README:n påstår att flera gigabyte går bra,
      men det har aldrig mätts. Stämmer det?
- [ ] **Egen testdata:** ett skript som genererar en stor loggfil med påhittade rader, för att testa prestanda

## Svårt

- [ ] **Automatisera en uppgift med en agent.** Till exempel: sammanfatta nattens fel i en fil. Ge agenten
      bara de rättigheter den behöver (läsa loggen, skriva en sammanfattning), kör första gången på en
      egen gren och godkänn stegen. Logga uppgift, rättigheter, resultat och din bedömning.
- [ ] **Samma uppgift i n8n.** Ett flöde som kör analysen varje natt och aviserar vid många fel (se `docs/n8n.md`).
      Vad är skillnaden mot agenten?
- [ ] **Hitta avvikelser:** flagga en timme med ovanligt många fel jämfört med de andra
- [ ] **Egenskapstester:** testa att vad du än stoppar in aldrig kraschar parsern
- [ ] **Dokumentation som testas:** exemplen i README:n körs som tester. Då kan de aldrig bli osanna.

## Utmaning: agentens gränser

- [ ] Kör din agent när det inte finns något att göra (en tom fil), på en trasig fil, och på en fil där en
      rad innehåller en text som försöker styra den. Gör det på en egen gren och bara med en ofarlig
      instruktion. Följer den den? Vilken behörighet hade begränsat skadan om det varit allvar?

## Regler för alla kort

- Ett kort i taget, på en egen gren
- Skriv testet först, eller åtminstone samtidigt. Kör alla tester innan du checkar in
- Läs diffen innan du committar. Du ska kunna förklara varje rad
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`)
