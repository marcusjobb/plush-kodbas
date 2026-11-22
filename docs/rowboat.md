# Rowboat

## Vad är det?

Rowboat är en **AI-kollega med minne**, utvecklad av Rowboat Labs. Det är ett skrivbordsprogram med
öppen källkod (Apache-2.0) som av din e-post, dina möten och dina anteckningar bygger en kunskapsgraf. Den
sparas som vanliga Markdown-filer på din egen disk, och agenten kan sedan använda den som sammanhang.

Skillnaden mot en vanlig chatt: en chatt börjar om varje gång och måste få sammanhanget inklistrat.
Rowboat samlar sammanhanget över tid, så att du kan fråga "vad bestämde vi med kunden förra veckan?"
och få svar utifrån dina egna källor.

Det beskrivs ibland som ett öppet alternativ till Claude Cowork. Det är en jämförelse som kommer från
tredje part, inte från tillverkarna, och verktygen löser inte exakt samma sak: Cowork är en agent som
arbetar i dina mappar, Rowboat fokuserar på att bygga upp ett minne.

## Vad används det till?

- Hålla ordning på projekt, beslut och löften som annars försvinner i mejl och möten
- Förbereda inför ett möte: vad vet jag om personen och projektet?
- Göra utkast till svar eller sammanfattningar utifrån tidigare konversationer
- Experimentera med en agent vars minne du kan öppna och läsa själv (det är bara textfiler)

## Det vi gjorde i lektionen

Vi körde Rowboat mot en liten automatiseringsuppgift: ett skript som kollar elpriset var 15:e minut mot ett
gratis API och larmar när priset är lågt. Uppgiften är liten och går att kontrollera, vilket gör den bra
att prova en agent på. Jämför med n8n-flödet för samma sak i [n8n.md](n8n.md).

## Läs det här innan du kopplar in något

Rowboat är gjort för att läsa **just det som är känsligast**: e-post, möten och anteckningar. Det innehåller
nästan alltid personuppgifter, ofta om andra än dig.

- Koppla inte in en arbetsmejl, ett kundkonto eller något med uppgifter om studerande eller kunder utan att
  ha kontrollerat vad som gäller för uppgifterna. Vid minsta tvekan: behandla det som personuppgifter.
- Kunskapsgrafen ligger lokalt, men innehållet skickas till den språkmodell du kopplar in när agenten arbetar.
  Det är då en fråga om vilken leverantör det är, och på vilka villkor.
- Börja med ett **testkonto eller påhittad data**.

## Installation

Rowboat finns för macOS, Windows och Linux (AppImage och `.deb`).

1. Hämta rätt fil från [rowboatlabs.com/downloads](https://www.rowboatlabs.com/downloads) eller från
   [releases på GitHub](https://github.com/rowboatlabs/rowboat/releases). Se till att repot är
   `rowboatlabs/rowboat`. Det finns flera kopior med liknande namn.
2. **Debian och Ubuntu:**
   ```bash
   sudo apt install ./rowboat-linux_*.deb
   rowboat-linux            # eller starta från programmenyn
   ```
   **AppImage:** gör filen körbar (`chmod +x`) och starta den.
3. Koppla in en språkmodell i inställningarna. Vilka modeller och leverantörer som stöds står i
   programmet och i dokumentationen. Kontrollera där, eftersom det ändras.
4. Koppla in källor en i taget. Google-integrationen kräver en egen uppsättning enligt projektets
   `google-setup.md`. Röststyrning är valfri och kräver en separat nyckel.

**Kontrollera att det är installerat (Debian och Ubuntu):**

```bash
dpkg -s rowboat-linux | grep -E "Package|Version"
```

## Källor

- [Rowboat på GitHub](https://github.com/rowboatlabs/rowboat)
- [Rowboat Labs](https://www.rowboatlabs.com)
- [Launch på Y Combinator](https://www.ycombinator.com/launches/Rma-rowboat-your-ai-coworker-with-memory)
- [Jämförelse med Claude Cowork (tredje part)](https://mer.vin/2026/05/rowboat-vs-claude-cowork-local-open-source-ai-coworker-with-a-knowledge-graph/)
