# Backlog

Spelet är inte färdigt. Det här är idéer att ta av, ungefär från lätt till svårt. Välj ett kort, bygg
det i en vertikal skiva och skriv ett test för det.

> Förslag. Listan är ett första utkast och kan ändras. Lägg gärna till egna kort.

## Planerat från början

- [x] **Labyrintgenerator.** Klart: huset slumpas, med låst dörr, mörka rum, lampa och två nycklar, och
      det garanteras att det går att klara.
- [x] **Kartan ryms i en konsol på 100×20.** Klart: ett rum ritas på en rad i stället för tre, och hela
      skärmen (kartan plus texten under) tar som mest 20 rader och 100 tecken. Det styr hur stort ett hus
      kan vara: **högst 14 rum i bredd och 6 i höjd** (`kartstorlek()` i `aventyr.py`). Tester mäter det.
- [ ] **Valfri storlek på spelet: minst 3×3, högst 14×6.** Se delkorten nedan. Gör dem i ordning.

### Valfri storlek: delkort

**Utgångsläget.** Motorn stödjer redan olika storlekar (`Spel(seed, bredd, hojd)`), men `aventyr.py` använder
alltid standardstorleken 5×4. Skärmen ryms i 100×20 för alla storlekar upp till 14×6, och det testas för
sex storlekar. Däremot testas det bara för standardstorleken att huset **går att klara**. Generatorn har
vi provat (40 slumpfrön per storlek) för bland annat 3×3, 4×4, 10×10 och 30×30, och alla hus gick att
klara, men den siffran skyddas inte av några tester. 14×6 har vi inte provat särskilt.

- [ ] **1. Skriv testerna först.** Gör `test_spelet_gar_att_vinna` parametriserat över storlekarna 3×3, 5×4,
      10×5, 14×3, 3×6 och 14×6. De ska vara gröna redan nu. Det är ditt skyddsnät.
- [ ] **2. Gränserna.** Bredd är ett heltal från 3 till 14, och höjd från 3 till 6. Lägg gränserna som
      konstanter (`MIN_STORLEK`, `MAX_BREDD`, `MAX_HOJD`) och låt `Spel` och `generera` neka värden
      utanför intervallet med ett tydligt `ValueError`. Skriv tester för 2, 3, 14, 15 (bredd) och 2, 3, 6, 7
      (höjd), och för ett negativt tal. Se till att `kartstorlek()` och gränserna inte säger emot varandra.
- [ ] **3. Välj storlek.** Låt spelaren välja vid start, med standardstorleken om hen bara trycker Enter.
      Valfritt: `python aventyr.py --bredd 10 --hojd 5`. Ogiltig inmatning ska ge ett felmeddelande och en
      ny fråga, inte en krasch.
- [ ] **4. Kontrollera för hand.** Spela ett 3×3-hus och ett 14×6-hus i en riktig terminal på exakt
      100×20 (och i ett mindre fönster). Notera vad du upptäcker som testerna inte fångade.
- [ ] **5. Större hus än 14×6 (valfritt, svårt).** Skärmen ryms inte för större hus, för hela kartan ritas
      alltid. Bygg en **vy som följer spelaren**: rita bara de rum som får plats, med spelaren i mitten, och
      läs terminalens storlek med `shutil.get_terminal_size()`. Då kan gränserna höjas, men tänk först på
      om ett så stort hus är roligt att spela.

**Klart när:** alla storlekar mellan 3×3 och 14×6 går att välja och klara, ogiltiga värden nekas med
ett begripligt meddelande, hela skärmen ryms i 100×20, och alla tester är gröna.

## Lätt

- [ ] **Välj slumpfrö från kommandoraden**, till exempel `python aventyr.py --seed 42`, så att du kan spela
      samma hus igen. (`spela(seed)` tar redan emot ett frö, men `main` skickar inte in något.)
- [ ] **Räkna dragen** och visa dem när du vinner
- [ ] **Kommandot `L` (titta)** som skriver ut rummet igen
- [ ] **Bättre felmeddelanden** när man skriver ett kommando spelet inte förstår

## Mellan

- [ ] **Fler föremål** med varsin användning
- [ ] **En andra låst dörr** med egen nyckel. Se kommentaren överst i `labyrint.py` för hur en dörr får
      placeras utan att huset blir omöjligt
## Spara, kartor och redigering

Fyra kort som bygger på varandra. Det sista kortet kräver det tredje. Allt sparas som JSON-filer.

- [ ] **1. Spara och ladda en session.** Avbryt ett spel och fortsätt senare. Spara allt som behövs för att
      återskapa spelet exakt: husets utseende, var spelaren är, vilka rum som är besökta, väskans innehåll,
      vilka föremål som ligger kvar och om dörren är upplåst. När hälsa och NPC:er finns ska de följa med.
      Lägg ett `version`-fält i filen, så att en gammal sparfil inte kraschar spelet efter en ändring.
      Ladda ska kontrollera filen och ge ett begripligt fel om den är trasig eller har fel version.
      Skriv tester: spara, ladda och kontrollera att spelet är identiskt, och att en trasig fil nekas.
- [ ] **2. Highscore.** Bestäm först vad poängen är: antal drag, hälsa kvar, tid, eller en kombination.
      Spara resultaten per karta och storlek, annars jämför man äpplen med päron. Visa topplistan när man
      vinner. Spelare anger ett **smeknamn**, inga riktiga namn: filen kan hamna på GitHub, och då är
      riktiga namn personuppgifter. Lägg topplistan i `.gitignore`, om du inte medvetet vill dela den.
- [ ] **3. Spara kartor i `maps/`.** Ett slumpfrö räcker inte som delbar karta: ändrar du generatorn senare
      blir samma frö ett annat hus. Spara i stället **själva huset** (rum, dörrar, föremål, den låsta dörren,
      mörka rum och utgången) som en JSON-fil i `maps/`, så att samma äventyr går att spela om och om
      igen, och kan delas på GitHub. Filen har ett `version`-fält, ett namn, en skapare (smeknamn) och
      storleken. Starta med `python aventyr.py --karta maps/hallen.json`. Vid laddning ska spelet **kontrollera**
      att kartan är giltig (storleken inom gränserna, alla rum nåbara, nycklarna går att nå, och huset går
      att klara) och neka den annars. Lägg två eller tre färdiga kartor i `maps/`, och skriv i README hur man
      delar en karta (en pull request, med en ny fil i `maps/`).
- [ ] **4. Karteditor.** Skapa och ändra kartor själv: lägg rum och dörrar, placera nycklar, lampa, låst
      dörr, mörka rum och utgång. Börja i konsolen. En webbversion med Flask kan komma sist. Editorn ska
      aldrig kunna spara en karta som inte går att klara, och ska säga **varför** när den nekar. Återanvänd
      samma kontroll som kort 3, skriv den inte två gånger. Låt editorn kunna öppna en slumpad karta
      och ändra den. Skriv tester för kontrollen, inte för menyerna.

## Svårt

- [ ] **Webbversion** med Flask, där kartan uppdateras med `fetch` (jämför `modul_03_webbutik`)
- [ ] **Skriv egna rumsbeskrivningar med en språkmodell**, och bestäm hur du kontrollerar att de passar spelet

## NPC:er: vänliga och ovänliga

En större funktion, med flera kort som bygger på varandra. Gör dem i ordning.

**Utgångsläget.** Spelet har ingen hälsa, inga fällor och inga rörliga figurer. Spelaren kan inte skadas,
och inget händer mellan två drag. Det mesta av arbetet är därför förutsättningarna i kort 1–3b.

**Idén i korthet**

| Sort | Gör | Kan man springa ifrån den? |
|------|-----|----------------------------|
| Vänlig healer | Läker dig om andra har skadat dig | Behövs inte |
| Vänlig rådgivare | Ger ett gott råd som stämmer | Behövs inte |
| Ovänlig anfallare | Jagar och skadar dig | Ja, du kan springa ifrån |
| Ovänlig bedragare | Anfaller inte, men försöker lura dig till ett rum med en fälla | Du kan välja att inte följa efter |
| Ovänlig tjuv | Stjäl ett föremål ur din väska | Ja, men du vill ha tillbaka det du förlorat |
| Vänlig givare | Ger dig en sak | Behövs inte |
| Alla | Goda och onda i samma rum anfaller varandra | Spelaren kan locka dit en ovän |

**Förutsättningar**

- [ ] **1. Hälsa.** Spelaren får ett antal hälsopoäng. Visa dem på skärmen. Vad händer vid noll? (Förslag:
      spelet förloras. Bestäm det och skriv ner det.) Skriv testerna först.
- [ ] **2. Tid.** Ett drag är en tidsenhet. Efter varje drag får figurerna agera. Lägg logiken i `motor.py`,
      inte i skärmen, så att den går att testa utan terminal.
- [ ] **3. Fällor.** Ett rum kan ha en fälla som skadar spelaren första gången hen kliver in. Fällor får
      aldrig göra huset omöjligt att klara. `labyrint.py` garanterar redan att huset går att klara, så
      bestäm hur en fälla förhåller sig till den garantin. Testa att alla hus fortfarande går att klara.
- [ ] **3b. Identitet: unikt namn och kön.** Varje NPC har ett **unikt namn** (förnamn och efternamn) och ett
      **kön**. Namnet kommer från en namngenerator, så att man slipper skriva ett namn för hand per figur.
      - **Generatorn** ligger i en egen fil (till exempel `namn.py`) och är ren logik utan utskrifter. Den
        tar emot ett slumptalsobjekt, så att samma slumpfrö ger samma namn, och därmed går att testa.
      - **Listorna** med förnamn och efternamn ligger som data (en fil eller en konstant), så att den som
        bygger kan utöka dem utan att röra logiken. Ha förnamn per kön. Namnen är **påhittade
        kombinationer**: ta inga kända personers namn, och inga namn på riktiga bekanta.
      - **Unikt:** ingen i samma hus får ha samma fullständiga namn som någon annan. Räkna ut hur många
        kombinationer listorna ger, och hur många figurer det största huset kan ha. Räcker inte
        kombinationerna ska generatorn ge ett tydligt fel, inte upprepa ett namn.
      - **Kön** är ett eget fält på figuren. Bestäm vilka värden som finns (kvinna, man, och kanske ett
        neutralt värde med eget pronomen "hen") och skriv ner det i README:n. **Pronomenet i texten
        ("hon", "han", "hen") läses ur fältet. Det gissas aldrig ur namnet**, för ett namn säger inget säkert.
      - **Namnet används i spelet:** i beskrivningen ("Du ser Elin Bergström"), i dialogen och i
        stridsmeddelanden (kort 11). Skriv hellre ut ett namn än "en vänlig figur".
      - **Följer med** när spelet sparas (kort 1 under "Spara, kartor och redigering") och när en karta
        sparas i `maps/` (kort 3). Bestäm om namnen hör till kartan, så att alla som spelar den får samma
        figurer, eller om de slumpas vid varje start.
      - **Tester:** samma slumpfrö ger samma namn, inga två figurer har samma namn i ett fullt hus (även 14×6, 84 rum),
        varje namn är ett förnamn plus ett efternamn ur listorna, och ett förnamn ur en lista för ett kön
        hamnar bara hos en figur med det könet.

**De vänliga**

- [ ] **4. Healer.** En vänlig figur i ett rum. Om spelaren är skadad och går in i rummet, läker figuren.
      Bestäm: läker den en gång eller flera, och hur mycket? Är spelaren oskadad ska den säga det.
- [ ] **5. Rådgivare.** Ger ett gott råd när spelaren pratar med den. **Rådet ska vara sant**: läs det ur
      spelets tillstånd (till exempel var den röda nyckeln ligger, eller att guldnyckeln ligger i ett
      mörkt rum), så att figuren aldrig vilseleder. Skriv ett test som kontrollerar att varje råd stämmer
      med huset. Rådgivaren kan bara veta det den "borde" veta. Bestäm vad.

**De ovänliga**

- [ ] **6. Anfallare som går att springa ifrån.** En ovänlig figur som rör sig mot spelaren och skadar
      hen när de är i samma rum. Spelaren kan fly genom att gå vidare. Bestäm hur figuren följer efter
      (`labyrint.py` och testerna har redan en bredden-först-sökning att utgå från) och hur snabb den är.
      **Springer man alltid ifrån den, blir den en chansning? Då är den för snäll. Fångas man alltid, är
      den för elak.** Justera tills det går att klara men inte slarvigt.
- [ ] **7. Fler anfallare.** Låt anfallarna vara en hel rad med olika sorter: långsam men stark, snabb men
      svag, och en som bara jagar i mörkret. Skriv en tabell med varje sorts egenskaper i README:n.
- [ ] **8. Bedragaren.** Anfaller inte, utan försöker locka spelaren till ett rum med en fälla ("Följ med,
      jag har hittat något!"). Bestäm hur figuren väljer rum, och hur en spelare som är försiktig kan
      märka att något är fel (en ledtråd, ett misstag i vad den säger, eller att rådgivaren varnar).

**Fler beteenden**

- [ ] **9. Tjuven.** En av de ovänliga är en tjuv: den anfaller inte, utan stjäl ett föremål ur väskan och
      springer. **Spelet måste gå att klara även om tjuven tar något viktigt.** Den röda nyckeln,
      lampan och guldnyckeln får inte försvinna för alltid. Bestäm hur man får tillbaka det: fångar man
      tjuven, tappar den föremålet när den skadas, eller ligger det i ett rum man kan hitta? Testa att
      spelet går att klara för alla slumpfrön när en tjuv tar varje möjligt föremål.
- [ ] **10. Givaren.** En vänlig figur ger spelaren ett föremål. Bestäm vad, och när: bara en gång, och
      kanske först när spelaren pratar med den eller har gjort något. En gåva ska aldrig kunna göra spelet
      trivialt (en nyckel rakt i handen) och aldrig fylla väskan utan gräns. Skriv ner vilka gåvor som
      finns i README:n.
- [ ] **11. Strid mellan figurer.** Hamnar en god och en ond figur i samma rum, anfaller de varandra.
      Bestäm hur en strid avgörs (styrka, hälsa, slump med ett fast frö?) och vad som händer med den som
      förlorar och med det den bär. **En föremålsbärare som slås ut ska släppa sina saker i rummet**, så
      att inget föremål kan försvinna ur spelet. Visa bara striden för spelaren om hen är i rummet, annars
      kanske ett ljud ("Du hör ett slagsmål i närheten"). Tänk på att spelaren kan utnyttja det: locka en
      ovän till en vänlig. Är det en feature eller ett fusk? Bestäm och skriv ner det. Och vad händer om
      healern slås ut?

**Klart när:** alla sorter finns (healer, rådgivare, anfallare, bedragare, tjuv och givare), strider
fungerar, varje beteende har ett test, spelet går fortfarande att klara för alla slumpfrön och storlekar
**även när tjuvar och strider har påverkat vad som finns kvar**, och man kan förlora hälsa, bli läkt,
få råd och gåvor, bli bestulen och springa ifrån.

**Tänk på**

- Figurerna ska bete sig likadant för samma slumpfrö, annars går de inte att testa.
- Skriv aldrig ut vad en NPC "tänker" på skärmen. Låt spelaren märka det av hur den beter sig.
- Valfritt, och sist: låt en språkmodell skriva repliker åt figurerna. Då ska rådgivarens råd fortfarande
  komma ur spelets tillstånd, och inte hittas på av modellen.

## Regler för alla kort

- Ett kort i taget, på en egen gren
- Skriv testet först, eller åtminstone samtidigt
- Kör alla tester innan du checkar in
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`)
