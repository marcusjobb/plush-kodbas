# Backlog: Fakturaräknaren

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren.

**Det du tränar i den här modulen:** att felsöka med hypoteser före fix, att skydda kod med tester innan
du rör den, och att refaktorisera i små steg där varje steg går att verifiera. Och att upptäcka när AI:n har fel.

## Lätt

- [ ] **Skriv testerna först.** Fånga hur `berakna_faktura` beter sig *just nu*, även om det är konstigt
- [ ] **Hitta felen** med hypoteser: ge AI:n symptomen och be om tre möjliga orsaker, utan fix
- [ ] **Validera indata:** negativ kvantitet, negativt pris, okänd kundtyp, saknat förfallodatum
- [ ] **Tydliga namn.** Byt `r`, `summa` och `antal` mot något som säger vad de är, utan att ändra beteendet

## Mellan

- [ ] **Dela upp funktionen** i mindre delar (mängdrabatt, kundrabatt, moms, dröjsmålsavgift), ett steg
      i taget. Kör testerna efter varje steg, och committa efter varje steg.
- [ ] **Pengar som `Decimal`** i stället för `float`. Vilka tester gick sönder, och varför?
- [ ] **Datadrivna rabatter:** lägg rabattreglerna i en tabell eller en fil i stället för i `if`-satser
- [ ] **En faktura som objekt** (`Invoice` med rader) i stället för listor av tupler
- [ ] **Skriv en egen mutationstestare.** Ett skript som ändrar koden på ett ställe i taget (`>` till
      `>=`, `+` till `-`), kör testerna och räknar hur många ändringar som upptäcktes. Då ser du hur bra
      dina tester är. Gör det i en kopia, aldrig på originalet.
- [ ] **Fakturarader med olika momssatser** (25, 12 och 6 %), och en momsspecifikation längst ned

## Svårt

- [ ] **OCR-nummer med kontrollsiffra.** Svenska betalningsreferenser har en kontrollsiffra enligt
      Luhn-algoritmen (mod 10). Skriv en funktion som skapar och kontrollerar den. Det är matematik du kan
      räkna ut för hand först.
- [ ] **Faktura som HTML eller PDF**
- [ ] **Flera valutor** med växelkurser i en fil. Var ska avrundningen ske?
- [ ] **Påminnelseflöde:** en funktion som utifrån dagar efter förfallodatum avgör vad som ska hända
      (påminnelse, avgift, inkasso). Vad är en rimlig regel, och vem avgör det?
- [ ] **Fakturanummer** som aldrig får upprepas. Hur lagrar du senaste numret?

## Utmaning: när AI:n har fel

- [ ] **Samla fall där verktyget har fel.** Ge det gränsfall (tom lista, negativa tal, skottår, månadsskifte)
      och skriv ner varje gång svaret var fel, och hur du upptäckte det.
- [ ] **"Är du säker?"** Fråga det på ett rätt svar. Byter verktyget svar utan nya fakta?
- [ ] **Jämför två verktyg** på samma refaktorisering, med samma instruktion. Läs båda diffarna.

## Tänk på

- Att refaktorisera *bort* ett fel utan att märka det är precis vad testerna i det första kortet ska hindra.

## Regler för alla kort

- Ett kort i taget, på en egen gren
- Skriv testet först, eller åtminstone samtidigt. Kör alla tester innan du checkar in
- Läs diffen innan du committar. Du ska kunna förklara varje rad
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`)
