# plush-kodbas

Övningsexempel till kursen **AI verktyg för systemutvecklare** (POBASH26KD, Plushögskolan).

## Vad är det här?

Små, fungerande program du kan köra, bryta, ändra och bygga vidare på tillsammans med ditt AI-verktyg.
Det finns en mapp per modul. Varje mapp har en egen `README.md` med vad programmet gör, hur du kör det
och vad du kan prova.

## Det här ersätter inte övningarna

Övningarna på kursportalen är det du gör och det som tränar kunskapskontrollerna. Den här kodbasen är
**ett komplement**: den ger dig något att leka med.

| Övningarna | Kodbasen |
|------------|----------|
| Du bygger själv, från noll | Du får något som redan fungerar |
| Har en bestämd ordning och mål | Du bestämmer själv vad du provar |
| Tränar det som examineras | Ger dig en lekplats och idéer |

Exemplen liknar övningarna, men de är inte samma uppgifter. Hoppar du över övningarna och bara läser
koden missar du det du ska lära dig.

## Kom igång

Du behöver Python 3.12 eller nyare och Git.

```bash
git clone <adressen till repot>
cd plush-kodbas
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Bara de webbaserade modulerna (03 och 15) behöver Flask. Resten kör på Pythons standardbibliotek.

**Tips:** skapa en egen gren för dina experiment, till exempel `git switch -c mina-experiment`.
Då kan du alltid gå tillbaka till originalet.

## Modulerna

Numren följer sidorna på kursportalen (`/ovningar/NN`).

| Mapp | Portalens övningssida | Vad du får |
|------|----------------------|------------|
| `modul_02_kassa` | 02 Konfiguration och verktyg | Kassa med meny i konsolen, utan `AGENTS.md` |
| `modul_03_webbutik` | 03 Kodgenerering, felsökning, refaktorisering | Webbutik i Flask som bara använder POST. Gör den interaktiv med `fetch` |
| `modul_04_05_prompt` | 04 och 05 Prompt och promptbaserad interaktion | Supportärenden i konsolen att ändra med olika promptar |
| `modul_06_agentloop` | 06 Vad är en AI-agent? | En agentloop du kan se steg för steg, utan AI |
| `modul_07_mappagent` | 07 Bygg din första agent | En agent som läser en mapp och har behörigheter |
| `modul_11_riskguide` | 11 EU:s AI-förordning | Beslutsguide för risknivå som du kan utöka |
| `modul_14_projektplan` | 14 Från idé till plan | Mallar för projektplan och AI-logg |
| `modul_15_bokning` | 15 Kom igång med bygget | Rumsbokning i Flask och SQLite att bygga vidare på |
| `modul_16_felsokning` | 16 Felsökning och refaktorisering | Rörig fakturakod utan tester |
| `modul_17_testning` | 17 Testning, dokumentation, automatisering | Loganalys med svaga tester och dokumentation som inte stämmer |
| `modul_18_kvalitet` | 18 Kvalitetssäkring | Ett litet register med medvetna brister att granska |
| `modul_19_redovisning` | 19 Förbered redovisningen | Checklista för demon |
| `modul_20_avslut` | 20 Redovisning och avslut | Mall för reflektion |

## Regler för all kod här

- All data är påhittad. Lägg aldrig in verkliga personuppgifter, inte heller i dina experiment.
- Inga riktiga nycklar eller lösenord. Nycklar som ser ut som riktiga i exemplen är påhittade.
- Små `README.md`-filer med "Känd bugg" eller "Lösningsförslag" ligger i `<details>`. Försök själv först.
- Du får använda AI fritt här, men du ska kunna förklara varje rad du checkar in.
