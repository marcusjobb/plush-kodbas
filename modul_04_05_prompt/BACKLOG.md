# Backlog: Supportärenden

Idéer att bygga vidare på. Alla kort är förslag, och en del beslut är öppna med flit. Välj ett kort i taget,
på en egen gren.

**Det du tränar i den här modulen:** att skriva promptar som ger bra resultat. Varje kort kan lösas med en
slarvig prompt, en prompt med kontext och en prompt med specifikation. Det är **jämförelsen** som är
poängen.

## Lätt

- [ ] **Prioritet** (låg, normal, hög) och sortering efter den
- [ ] **Stäng, öppna igen och radera** ärenden. Vad ska hända med ärendenumren när ett ärende raderas?
- [ ] **Sök** på rubrik och kund
- [ ] **Färg** på prioritet i listan

## Mellan

- [ ] **Spara till JSON** och läs in vid start. Vad händer om filen är trasig?
- [ ] **Åldersvarning:** ärenden som legat öppna längre än tre dagar markeras
- [ ] **Statistik:** hur många är öppna, hur gammalt är det äldsta, vilken kund har flest?
- [ ] **Kategorier**, och ett enkelt förslag på kategori utifrån nyckelord i rubriken
- [ ] **Dubbletter:** varna när en ny rubrik liknar en befintlig
- [ ] **Exportera till CSV eller Markdown**
- [ ] **Kommentarer** på ett ärende, med tidsstämpel

## Svårt

- [ ] **Webbgränssnitt** med Flask. Låt AI:n ställa upp till fem frågor om vad du vill ha innan den skriver kod
- [ ] **Låt en språkmodell föreslå kategori och prioritet** för ett ärende. Kontrollera svaret mot reglerna
      du själv skrivit: vad gör du när modellen svarar något du inte väntade dig?
- [ ] **Svarsmallar:** ett utkast till svar utifrån ärendets typ. Hur ser du till att inget påhittat
      löfte hamnar i ett svar?

## Prompt-labbet (den viktigaste uppgiften)

- [ ] **Jämför tre promptar på samma kort.** Spara dem i en tabell: prompten, hur stor diffen blev, hur
      många tester som skrevs, vad du själv glömt att be om, och hur lång tid granskningen tog.
- [ ] **Bygg ditt eget promptbibliotek:** tre mallar (ny funktion, buggfix, refaktorisering) med fasta
      rubriker (syfte, indata, utdata, kantfall, begränsningar). Använd dem på tre kort och förbättra dem.
- [ ] **"Ställ frågor först":** be om fem frågor innan koden skrivs. Vilka frågor hade du inte tänkt på?
- [ ] **Be om tre lösningar** och motivera vilken du väljer och varför de andra föll bort

## Tänk på

- Använd bara **påhittade** kundnamn och ärenden. Riktiga ärenden innehåller personuppgifter, och dem
  klistrar du inte in i ett AI-verktyg utan att ha kontrollerat vad som gäller.

## Regler för alla kort

- Ett kort i taget, på en egen gren
- Skriv testet först, eller åtminstone samtidigt. Kör alla tester innan du checkar in
- Läs diffen innan du committar. Du ska kunna förklara varje rad
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`)
