# n8n

## Vad är det?

n8n (uttalas "n-åtta-n") är ett verktyg för att **koppla ihop tjänster i automatiska flöden**. Du bygger ett
flöde (workflow) genom att dra ihop block, kallade noder, i en webbläsare: en **trigger** startar flödet
("ett mejl kommer", "klockan blir 08:00", "någon anropar en webbadress"), och därefter gör nod efter nod
sitt jobb (hämta data, filtrera, skicka vidare, spara).

Det går att köra n8n på din egen dator eller server, så att flödena och uppgifterna stannar hos dig.

> **Licens:** n8n är *source-available* under en egen licens (Sustainable Use License), inte öppen källkod
> i strikt mening. Det är gratis att köra själv för eget bruk, men det finns begränsningar för kommersiell
> vidareförsäljning. Läs licensen om du tänker använda det i ett företag.

## Vad används det till?

- Skicka ett meddelande när något händer (ny rad i en tabell, ett formulär skickas in)
- Hämta data från ett API varje natt och spara den
- Låta en språkmodell sammanfatta eller sortera inkommande material, med n8n:s AI-noder
- Koppla ihop system som saknar färdig integration, via webhooks och HTTP-anrop
- Bygga enklare agenter med en AI-nod, tydliga verktyg och begränsade rättigheter (jämför övning 3 i modul 17)

Ett flöde är en agent på lågnivå: du bestämmer exakt vilka steg som körs. Det gör det enklare att
kontrollera än en fri agent, men också mindre flexibelt.

## Så använder du det

1. Öppna n8n i webbläsaren (`http://localhost:5678` om du kör det lokalt) och skapa ett ägarkonto första gången.
2. Skapa ett nytt flöde. Lägg till en **trigger** (till exempel *Schedule* eller *Webhook*).
3. Lägg till noder efter varandra. Klicka på **Execute workflow** och titta på vad varje nod får in och skickar ut.
4. Lägg in inloggningsuppgifter för tjänster under **Credentials**, inte direkt i flödet.
5. När flödet fungerar: slå på **Active**. Då körs det av sig självt.

**Bra första flöde (utan nycklar):** *Schedule* varje morgon, sedan *HTTP Request* mot ett öppet API, sedan en
*Edit Fields*-nod som väljer ut det du vill ha. Titta på datan efter varje steg.

## Det vi gjorde i lektionen

Vi byggde två flöden:

1. **Dadjoke:** prompten "säg en dadjoke" skickades till en språkmodell via OpenRouter, och svaret
   skickades vidare med Gmail.
2. **Elpris:** flödet kollar elpriset var 15:e minut mot ett gratis API (Elpriset just nu) och aviserar när
   priset är lägre än 2 kr/kWh.

Samma elpris-uppgift löste vi också med en agent i Rowboat (se [rowboat.md](rowboat.md)). Jämför de två
sätten: i n8n bestämmer du själv varje steg, med en agent beskriver du målet och agenten väljer stegen.

Att tänka på: båda flödena använder inloggningsuppgifter (OpenRouter och Gmail). Lägg dem under
**Credentials** och inte i noderna. Skicka inte personuppgifter genom en språkmodell.

## Installation (Docker)

Det enklaste är Docker. Du behöver Docker installerat och igång.

```bash
docker volume create n8n_data

docker run -d --name n8n --restart unless-stopped \
  -p 127.0.0.1:5678:5678 \
  -e GENERIC_TIMEZONE="Europe/Stockholm" \
  -e TZ="Europe/Stockholm" \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

Öppna sedan `http://localhost:5678`.

Vad kommandot gör:

| Del | Betydelse |
|-----|-----------|
| `-v n8n_data:/home/node/.n8n` | Sparar dina flöden, uppgifter och krypteringsnyckel i en volym, så att de överlever omstart och uppdatering |
| `-p 127.0.0.1:5678:5678` | Gör n8n nåbart bara från din egen dator, inte från hela nätverket |
| `--restart unless-stopped` | Startar om n8n efter en omstart av datorn |
| `GENERIC_TIMEZONE`, `TZ` | Rätt tidszon, annars körs schemalagda flöden på fel tid |

**Vanliga kommandon**

```bash
docker logs -f n8n                     # se loggen
docker stop n8n && docker start n8n    # stoppa och starta
docker exec n8n n8n --version          # vilken version kör jag?
```

**Uppdatera:** hämta ny avbild (`docker pull docker.n8n.io/n8nio/n8n`), ta bort containern
(`docker rm -f n8n`) och kör `docker run` igen med samma volym. Flödena ligger kvar.

**Ta backup:** volymen `n8n_data` innehåller både flödena och nyckeln som krypterar dina sparade
inloggningsuppgifter. Utan nyckeln går uppgifterna inte att läsa. Spara en kopia någonstans säkert.

Tillverkaren rekommenderar Docker Compose för serverinstallationer med riktig domän och TLS. Följ då deras guide
(länk nedan). Den här versionen är för att prova lokalt.

## Säkerhet och personuppgifter

- Lägg aldrig nycklar eller lösenord direkt i en nod. Använd **Credentials**.
- Exponera inte n8n mot internet utan inloggning, TLS och en genomtänkt uppsättning. Behåll
  `127.0.0.1` i portvalet tills du vet vad du gör.
- Ett flöde som skickar personuppgifter till en språkmodell eller en annan tjänst är en behandling av
  personuppgifter. Testa med påhittad data.
- Webhooks är öppna dörrar. Den som känner adressen kan starta flödet.

## Källor

- [Installera n8n med Docker (officiell dokumentation)](https://docs.n8n.io/hosting/installation/docker)
- [Installera n8n med Docker Compose (officiell dokumentation)](https://docs.n8n.io/deploy/host-n8n/install-options/use-a-cloud-provider/use-docker-compose)
