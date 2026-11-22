# Modul 07: Mappagenten

En agent som får en mapp med kursutvärderingar (påhittade) och ett mål. Det som skiljer den från ett
vanligt skript är att **du styr vad den får göra**: skrivrätt av eller på, och godkännande före varje steg.

> Ingen AI här heller. Det är samma idé som i modul 06, men fokus ligger på behörigheter.
> Det här är ett övningsexempel och ersätter inte övningarna på portalen (`/ovningar/07`).
> Där bygger du en riktig agent med eget verktyg och en egen mapp.

## Kör

```bash
cd modul_07_mappagent
python mappagent.py
```

1. Välj mål 1 och godkänn varje steg. Notera hur många steg det blev.
2. Välj mål 2 **utan** skrivrätt. Vad händer? Vad skulle du vilja att agenten sa i stället?
3. Välj 3 för att ge skrivrätt, kör mål 2 igen och titta i `rapport.md`.

## Fil `utvardering_6_trasig.txt`

En fil saknar betyg, med flit. Mål 1 hanterar det (den rapporterar filen), mål 2 gör det inte ordentligt.
Vad blir snittet? Är det rätt?

## Prova

- Låt agenten också räkna ut det vanligaste betyget (median eller typvärde)
- Skriv en rapport med citat ur kommentarerna, och fundera på vad som händer om en kommentar innehåller
  en instruktion ("Ignorera allt ovan"). Den här agenten bryr sig inte, men det gör språkmodeller.
- Gör en dashboard av resultatet: en HTML-fil med stapeldiagram. Det är nästan exakt övning 3 på portalen,
  fast här kan du jämföra med vad ett skript kräver av dig.
- Lägg till ett verktyg som får flytta filer. Vilken behörighet ska det ha, och vilken ska det **inte** ha?
- Lägg till en gräns för hur många filer agenten får läsa

## Tänk efter

Vilka steg kändes onödiga att godkänna, och vilka var viktiga? Om du hade godkänt allt automatiskt,
vad hade kunnat gå fel?

**Fler idéer:** se [BACKLOG.md](BACKLOG.md). Det är förslag att inspireras av, inga krav.
