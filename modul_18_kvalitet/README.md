# Modul 18: Kvalitetssäkring

Ett litet kundregister med **medvetna brister**. Din uppgift är att granska det som om det vore ett
projekt du ska lämna in: hitta problemen, bedöm hur allvarliga de är och åtgärda dem.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen (`/ovningar/18`).
> Där granskar du ditt eget projekt. Här får du en bra repetition på främmande kod.
> Allt i koden, nycklar och lösenord inräknat, är påhittat.

## Kör

```bash
cd modul_18_kvalitet
python kundregister.py
```

Du behöver inte installera något. `requests` behövs bara om du kör `hamta_valutakurs`, och den pekar mot
en adress som inte finns.

## Gör så här

1. **Läs själv först** och skriv ner vad du ser, innan du ber AI:n om hjälp.
2. **Be sedan AI:n granska** och jämför. Vad hittade ni båda? Vad hittade bara du? Vad hittade bara den?
3. **Rangordna.** Vilket problem är värst, och varför? Använd skalan *kritisk, allvarlig, kosmetisk*.
4. **Åtgärda i små steg**, med ett test eller ett kommando som bevisar att varje fix fungerar.
5. **Kontrollera hemligheter och beroenden.** Sök igenom projektet efter nycklar och lösenord
   (`git grep -i "key\|pass"`). Kör `pip install pip-audit` och sedan `pip-audit -r requirements.txt`.
6. **Skriv en gapanalys:** vad skulle fattas för att det här skulle gå att lämna ifrån sig?

## Frågor att svara på

- Vad händer med en hemlighet som en gång har checkats in, även om du tar bort den i nästa commit?
- Varför är SQL byggd med f-strängar ett problem? Skriv en indata som visar det (i din egen kopia, mot din egen databas).
- Vilka personuppgifter hanteras här, och vad kräver GDPR av ett riktigt register?
- Vad borde loggas, och vad borde absolut inte loggas?

<details markdown="1">
<summary>Lösningsförslag: brister att hitta</summary>

- Hemlig nyckel och lösenord ligger i koden. Flytta till miljövariabler och lägg `.env` i `.gitignore`.
  En nyckel som checkats in måste anses röjd och bytas ut.
- SQL byggs med f-strängar och är öppen för SQL-injektion. Använd parametriserade frågor (`?`).
- Nyckeln och kundens e-post skrivs ut i en logg. Skriv aldrig ut hemligheter, och var försiktig med personuppgifter.
- `verify=False` stänger av kontrollen av servercertifikat.
- `requests==2.19.0` är gammal och har kända sårbarheter. Kör `pip-audit`.
- Lösenordet jämförs i klartext, och "radera allt" saknar bekräftelse.
- Ingen validering av indata, inga tester, och mappen har ingen egen `.gitignore` (databasfilen `kunder.db`
  skulle annars hamna i ett eget repo).
- Registret innehåller personuppgifter men saknar rutin för gallring och rätten att bli raderad.

</details>

**Fler idéer:** se [BACKLOG.md](BACKLOG.md). Det är förslag att inspireras av, inga krav.
