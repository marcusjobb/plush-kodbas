# Modul 12: Så granskar du AI-genererad kod kritiskt

Ingen kod och inga övningar här. Videons poäng: gröna tester betyder att koden gör det testerna kontrollerar,
inget mer. Här är frågor och promptar att ta med till ett AI-verktyg för att träna på att granska.

> Det här ersätter inga övningar. Läs först [hur du pratar med en AI](../docs/prata_med_ai.md).
> Använd kod du själv har skrivit, eller hitta på ett exempel. Klistra inte in kod från ett jobb om du
> inte vet att du får det.

## Börja här

- "Vad ska jag titta efter när jag granskar kod som en AI har skrivit? Gör en checklista, och förklara
  varför varje punkt finns."
- "Vad är skillnaden mellan att koden *fungerar*, att den är *korrekt* och att den är *bra*?"
- "Varför kan en funktion ha gröna tester och ändå vara fel? Ge tre olika sätt det kan hända på."

## Låt AI:n granska din kod, och granska granskningen

Klistra in en funktion du själv skrivit (eller en påhittad) och prova:

- "Vilka antaganden gör den här funktionen som inte står uttryckligen? Lista dem."
- "Ge mig tio gränsfall jag borde testa. Ordna dem efter hur sannolikt det är att koden brister."
- "Vad testar de här testerna **inte**?" (Klistra in testerna också.)
- "Granska den här koden som en skeptisk kollega. Hitta tre saker du skulle ifrågasätta i en pull request."
- "Förklara vad varje rad gör. Var är du osäker?"

Räkna sedan efter: hur många av svaren var rätt, hur många var fel, och hur många var irrelevanta?

## Be om fel

- "Skriv en funktion som beräknar [något enkelt] och som ser rätt ut, men som har ett subtilt fel i ett
  gränsfall. Berätta inte felet förrän jag har gissat."
- "Skriv tester som är gröna men som missar det felet. Förklara varför de missar det."
- "Vilka vanliga fel gör AI-genererad kod, till exempel med datum, avrundning, tomma listor, text i andra
  språk och flera trådar?"

## Tänk på hur du läser

- "Hur läser man en diff på ett effektivt sätt? Vilka frågor ska jag ställa till varje ändring?"
- "Hur vet jag att en AI inte har hittat på ett funktionsnamn eller ett paket? Hur kontrollerar jag det?"
- "Vad är skillnaden mellan att be en AI granska sin *egen* kod och att be en annan modell granska den?"
- "När är det bättre att skriva om koden själv än att försöka rätta AI:ns version?"

## Be om motstånd

- "Argumentera för att man aldrig bör godkänna AI-kod som man inte själv kunnat skriva. Argumentera sedan
  för att det är orimligt strängt. Var drar du gränsen?"
- "Jag har ofta godkänt AI-kod utan att läsa allt. Vad är risken, och hur ser en bättre rutin ut?"

## Ett litet experiment (20 minuter)

Ta en funktion från ditt eget projekt som en AI har skrivit. Granska den utan hjälp av AI först, med
checklistan du fick fram. Be sedan ett AI-verktyg granska samma kod, och jämför. Vad hittade bara du?
Vad hittade bara verktyget? Fortsätt sedan i `modul_17_testning` och `modul_18_kvalitet`.

## Skriv ner

I din AI-logg: din egen granskningschecklista i fem punkter, och ett fel som du själv missade men som någon
annan (eller något annat) hittade.
