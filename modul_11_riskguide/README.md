# Modul 11: Riskguiden

En beslutsguide som ställer ja/nej-frågor om ett AI-system och placerar det i en risknivå:
förbjuden, hög risk, begränsad risk eller minimal risk. Frågorna ligger i `fragor.json`, så du kan
ändra guiden utan att programmera.

> Guiden är **förenklad** och tränar tankesättet. Den är inte juridisk rådgivning och ersätter inte
> förordningen. Det här är ett övningsexempel och ersätter inte övningarna på portalen (`/ovningar/11`).

## Kör

```bash
cd modul_11_riskguide
python riskguide.py
```

Bedöm ett par system du hittar på:

- En chattbot som svarar på frågor om öppettider
- Ett system som sorterar CV:n åt en rekryterare
- Ett spamfilter
- En kamera som försöker avgöra om elever verkar uttråkade

Stämmer resultatet med vad du lärt dig i videon? Var tycker du att guiden är för grov?

## Prova

- **Hitta fel.** Frågorna är förenklade och sammanslagna. Läs artikel 5 och bilaga III i förordningen och
  hitta något som guiden missar eller förenklar för mycket.
- **Dela upp frågorna** så att varje fråga bara handlar om en sak. Då blir svaren mer rättvisande.
- **Lägg till en förklaring** efter varje resultat: vad kräver nivån av dig i praktiken?
- **Lägg till rollen** i resultatet: kraven skiljer sig för leverantör och den som använder systemet.
  Utöka guiden så att den visar olika kommentarer per roll.
- **Gör en webbversion** med Flask. Eller en HTML-fil med JavaScript som läser `fragor.json`.
- **Skriv tester** som kontrollerar att varje exempel ovan hamnar på rätt nivå.

## Att tänka på

AI:n du frågar om förordningen kan ha fel eller vara ur tid. Kontrollera allt den påstår mot källan.
Det är en bra övning i sig: be verktyget förklara artikel 5 och läs sedan själv.
