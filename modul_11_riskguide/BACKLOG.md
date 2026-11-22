# Backlog: Riskguiden

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren.

**Det du tränar i den här modulen:** att förstå hur EU:s AI-förordning delar in system i risknivåer, vad som
krävs av dem, och att inte lita blint på vad en AI säger om en lag. Källan är alltid förordningen själv.

## Lätt

- [ ] **Förklara varje nivå.** Efter resultatet: vad kräver nivån i praktiken? Skriv det själv, och
      kontrollera mot förordningen.
- [ ] **Fler exempelsystem** att pröva, till exempel ett spamfilter, en rekryteringsrobot och en
      ansiktsigenkänning vid en entré
- [ ] **Färg** per risknivå
- [ ] **Skriv ut en rapport** som Markdown, med frågor, dina svar och resultatet

## Mellan

- [ ] **En fråga, en sak.** Frågorna i `fragor.json` är sammanslagna. Dela upp dem, så att varje svar
      betyder en enda sak. Blir resultaten bättre?
- [ ] **Visa varför.** Låt guiden berätta vilket svar som ledde till nivån
- [ ] **Skillnad på roller:** kraven är olika för den som utvecklar och den som använder systemet.
      Visa olika kommentarer per roll.
- [ ] **Testfall:** skriv tester där varje känt exempel ska hamna på en viss nivå. Hitta ett där guiden har fel.
- [ ] **Quiz-läge:** guiden visar ett system, du gissar nivån, och får poäng. Hitta på fler fall.
- [ ] **Gren för AI-modeller för allmänna ändamål**, som har egna krav. Läs i förordningen vad som gäller,
      och skriv in källa och artikel på varje fråga du lägger till.
- [ ] **Sök bland sparade bedömningar** och filtrera på nivå

## Svårt

- [ ] **Webbversion** med Flask, eller en HTML-sida med JavaScript som läser `fragor.json`
- [ ] **Checklista per nivå:** en lista med krav som den som bygger systemet kan bocka av och spara
- [ ] **AI som granskas:** be ett AI-verktyg förklara en artikel, och kontrollera varje mening mot lagtexten.
      Spara hur ofta den hade rätt. Vad lär du dig om att använda AI för juridiska frågor?
- [ ] **Flera språk** i guiden (svenska och engelska). Lagtexten finns på båda.

## Tänk på

- Guiden är förenklad och ersätter inte juridisk rådgivning. Skriv aldrig i din egen kod att något är
  "godkänt" eller "lagligt".
- Lägg inte in uppgifter om verkliga system på riktiga företag. Hitta på exempel.

## Regler för alla kort

- Ett kort i taget, på en egen gren
- Skriv testet först, eller åtminstone samtidigt. Kör alla tester innan du checkar in
- Läs diffen innan du committar. Du ska kunna förklara varje rad
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`)
