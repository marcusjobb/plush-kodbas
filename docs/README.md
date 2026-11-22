# docs: verktygen i kursen

Korta guider till tre verktyg som kommer upp i kursen. Varje guide svarar på samma tre frågor:
**vad är det, vad används det till, och hur installerar jag det.**

| Verktyg | Vad det är | Kostnad | Guide |
|---------|------------|---------|-------|
| Claude Cowork | Agent med grafiskt gränssnitt i Claude Desktop, arbetar i mappar du väljer | Kräver betald Claude-plan | [claude_cowork.md](claude_cowork.md) |
| Rowboat | Öppen källkod-alternativ: en "AI-kollega" som bygger ett minne av din e-post, dina möten och anteckningar | Gratis, du betalar för modellen du kopplar in | [rowboat.md](rowboat.md) |
| n8n | Verktyg för att koppla ihop tjänster i flöden (automatisering), kan köras hos dig själv | Gratis att köra själv | [n8n.md](n8n.md) |

## Vilket ska jag välja?

| Jag vill... | Titta på |
|-------------|----------|
| Låta en agent läsa och ändra filer i en mapp, utan terminal | Claude Cowork (modul 07) |
| Ha en agent som minns sammanhang över tid, och som körs lokalt med öppen källkod | Rowboat |
| Få något att hända automatiskt när en annan sak händer (ett mejl kommer, en fil sparas) | n8n |
| Skriva och köra kod med en agent i terminalen eller editorn | Claude Code, OpenCode eller Copilot (se övningarna) |

## Så pratar du med en AI

Guiden [prata_med_ai.md](prata_med_ai.md) ger sju sätt att få bättre samtal med ett AI-verktyg. Den hör ihop
med samtalsstartarna i modulerna som bara har en video.

## Läs det här först: personuppgifter

Alla tre verktygen kan komma åt riktig data: filer, e-post, kalendrar, kontakter. Innan du kopplar in något:

- Fråga dig vilka personuppgifter som finns i det du ger tillgång till, och vems de är.
- Skicka inte uppgifter om andra till en molntjänst (en språkmodell räknas som det) utan att veta vad
  som gäller för dem. Vid minsta tvekan: behandla det som personuppgifter.
- Börja med påhittad data och en mapp du skapat själv. Det är så övningarna är tänkta.

## Källor

Guiderna bygger på tillverkarnas egna sidor. Verktygen uppdateras ofta, så kontrollera alltid
installationssteg mot länkarna längst ned i varje guide.
