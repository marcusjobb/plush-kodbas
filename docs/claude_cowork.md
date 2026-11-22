# Claude Cowork

## Vad är det?

Cowork är Anthropics agentläge i appen **Claude Desktop**. Det tar det som Claude Code kan (en agent som
läser, skriver och kör saker i flera steg) och lägger det i ett grafiskt gränssnitt, så att du slipper
terminalen.

Du ger Cowork ett mål och en mapp. Agenten planerar, gör arbetet och visar vad den gör. Den kör koden i en
**isolerad virtuell maskin** på din dator, och den kan bara läsa och skriva i de mappar du själv kopplat in.

## Vad används det till?

- Läsa en mapp med filer och sammanfatta eller sammanställa dem (som i övning 7 på portalen)
- Skapa dokument, kalkylark eller en dashboard av material du har
- Flerstegsuppgifter där du vill kunna följa arbetet och godkänna steg
- Uppgifter för dig som inte vill arbeta i terminalen

Vill du i stället arbeta i en kodbas med git, tester och diffar är Claude Code, OpenCode eller Copilot oftast
ett bättre val. Se `modul_02_kassa` och övning 2 på portalen för hur du väljer.

## Så använder du det

1. Öppna **Claude Desktop** och logga in.
2. Byt till **Cowork** och starta en ny uppgift.
3. **Välj mapp.** Det är den enda plats agenten kan arbeta i. Ge den inte mer än den behöver.
4. Skriv ett mål, helst som en specifikation: vad du vill ha, i vilket format och vad som inte får ändras.
5. **Läs varje steg innan du godkänner.** Det är din chans att stoppa ett misstag.
6. Kontrollera resultatet. Agenten kan ha fel, precis som all AI.

Prova med `modul_07_mappagent/kursutvarderingar/`: samma mapp, men nu med en riktig agent.

## Det vi gjorde i lektionen

Vi körde Cowork mot en statistikuppgift: en mapp med CSV-filer med Black Friday-priser (kläder och
datortillbehör) som agenten fick rensa och göra diagram av. Det är samma sorts uppgift som övning 7 på
portalen: en mapp, ett mål, och en agent som du följer steg för steg.

## Installation

**Krav**

- En betald Claude-plan (Pro, Max, Team eller Enterprise)
- Claude Desktop för macOS, Windows eller Linux (Linux är i beta)

**macOS och Windows:** ladda ner Claude Desktop enligt Anthropics installationssida (länk nedan) och logga in.

**Linux (Ubuntu 22.04 eller nyare, Debian 12 eller nyare, x64 eller arm64):**

1. Lägg till Anthropics apt-förråd enligt installationssidan och kör sedan:
   ```bash
   sudo apt update && sudo apt install claude-desktop
   ```
   En nedladdad `.deb`-fil fungerar också, men då kommer uppdateringarna inte automatiskt.
2. Cowork kör i en virtuell maskin, så Linux har extra krav:
   - **Hårdvaruvirtualisering** måste vara påslagen i BIOS/UEFI
   - **QEMU och KVM** måste vara installerade. Saknas de visar Cowork "Cowork requires QEMU" och kommandot som ska köras.
   - Din användare måste vara med i gruppen `kvm`, även om `/dev/kvm` redan verkar fungera:
     ```bash
     sudo usermod -aG kvm $USER     # logga ut och in igen efteråt
     ```
3. Begränsningar på Linux: "computer use" och diktering finns inte.

**Kontrollera att din dator är redo (Linux):**

```bash
id -nG | grep kvm          # ska skriva ut kvm
ls -l /dev/kvm /dev/vhost-vsock
which qemu-system-x86_64
```

## Källor

- [Installera Claude Desktop (Anthropic)](https://support.claude.com/en/articles/10065433-install-claude-desktop)
- [Claude Desktop på Linux (Claude Code-dokumentationen)](https://code.claude.com/docs/en/desktop-linux)
