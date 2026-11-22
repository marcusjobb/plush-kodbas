# Backlog: Julkoden

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren. Rytmen: planera, bygg det minsta som fungerar, testa, läs diffen.

## Hemlig tomte

- [ ] **Önskelistor.** Var och en skriver in önskemål, och mottagarens lista visas när man tittar i hemlighet
- [ ] **Grupper:** de som bor ihop ska inte lottas till varandra, utan att man behöver skriva ett par i taget
- [ ] **Spara och läsa in** deltagare och regler från en JSON-fil
- [ ] **Bytte någon plats?** Låt någon hoppa av efter lottningen, och lotta om så lite som möjligt
- [ ] **Inte samma som förra året.** Spara förra årets lottning och undvik att upprepa den. Var lagrar
      du den, och vem får se den? Det är personuppgifter om vem som gav till vem.
- [ ] **Budget och tema** som skrivs ut tillsammans med mottagaren
- [ ] **Mät algoritmen:** hur lång tid tar det för 10, 100 och 1 000 personer? Kan backtrackingen fastna?
- [ ] **Webbversion** med Flask, där var och en får en egen länk som bara visar den egna mottagaren

## Julgranen

- [ ] **Snö** som faller bakom granen
- [ ] **Klappar** under granen som blir fler ju längre den körs
- [ ] **Hastighet och färger** som flaggor
- [ ] **Egen form:** en bild eller en figur du bestämmer, till exempel en pepparkaksgubbe eller ett julgransljus
- [ ] **Anpassa efter konsolens storlek** med `shutil.get_terminal_size()`

## Nya små program

- [ ] **Adventsljusstake.** Utifrån dagens datum tänds ljusen på de fyra söndagarna före jul. Lägg in
      "dagens datum" som en parameter, så att du kan testa utan att vänta till december.
- [ ] **Julkalender** med 24 luckor, där varje lucka är en gåta eller en fråga som öppnas efter datum
- [ ] **Tomtens rutt.** Ge en lista med påhittade städer med koordinater och hitta en kort rutt (börja med
      "gå alltid till närmaste stad som inte besökts"). Hur mycket längre är den än den kortaste
      möjliga för fem städer, som du kan räkna ut för hand?
- [ ] **Pepparkaksrecept:** räkna om ett recept till ett annat antal personer, med enhetsomvandling
- [ ] **Nyårsraketer** i ASCII-konst, med slumpade färger
- [ ] **Tolv dagar, din version.** Gör om `xmas_c.md` till Python (se `jul_prompts.md`) och skriv sedan din egen
      version med egna gåvor, till exempel "en gummianka på en buggig gren". Gör sången till en funktion som tar
      dagnumret som parameter
- [ ] **Mät skillnaden:** hur många rader och tecken har C-versionen, din direkta Python-översättning och den
      rena datadrivna versionen? Vilken är lättast att ändra, och varför?
- [ ] **Nyårslöften som tester:** skriv dina löften som tydliga "klart betyder"-punkter, och en liten
      lista där du bockar av dem

## Nästa steg

- [ ] **Skriv en projektplan** för det du vill bygga härnäst, med mallen i `modul_14_projektplan`
- [ ] **Granska en kurskamrats kod** och diskutera det ni är oense om

## Regler för alla kort

- Ett kort i taget, på en egen gren
- Skriv testet först, eller åtminstone samtidigt. Kör alla tester innan du checkar in
- Läs diffen innan du committar. Du ska kunna förklara varje rad
- Använd bara påhittade namn
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`)
