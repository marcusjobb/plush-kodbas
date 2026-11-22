# Modul 03: Webbutiken

En liten webbutik i Flask. Den fungerar, men **allt är vanliga formulär**: varje klick skickar ett
POST-anrop och sidan laddas om helt. Det finns ingen `fetch` och ingen JavaScript alls.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen (`/ovningar/03`).
> Övningarna handlar om kvittoräknaren. Här har du en webbutik att experimentera med.

## Kör

```bash
cd modul_03_webbutik
flask --app app run --debug
```

Öppna `http://127.0.0.1:5000`. Tester: `python -m unittest`.

## Så hänger det ihop

- `app.py`: produkter, varukorg i sessionen, fem routes
- `templates/`: sidorna (Jinja)
- Priser är hela kronor exklusive moms. Momssatserna är 25, 12 och 6 %.

## Prova

**1. Gör den interaktiv med `fetch`.** Idag laddas hela sidan om när du lägger något i varukorgen.
Låt "Lägg i varukorgen" anropa servern med `fetch`, och uppdatera antalet i menyn utan omladdning.
Det behövs en route som svarar med JSON. Be ditt AI-verktyg om en plan först, och godkänn den innan
någon kod skrivs.

**2. Lägg till funktioner**, en i taget:

- Ändra antal i varukorgen (plus och minus) utan omladdning
- Sökfält som filtrerar produkterna medan du skriver
- Lagersaldo: ett fel om du försöker köpa mer än det finns
- Rabattkod
- Sida med orderhistorik

**3. Felsök.** Något stämmer inte i varukorgens summor. Hitta det själv först: köp flera av samma
vara och räkna efter med miniräknare. Be sedan AI:n om *hypoteser* innan du ber om en fix.

<details markdown="1">
<summary>Känd bugg (försök själv först)</summary>

Momsen räknas per styck och avrundas nedåt (`int(...)`) innan den multipliceras med antalet. 3 st kaffe
à 49 kr ger 15 kr moms i stället för 17,64 kr. Rätt sätt är att räkna moms på hela radens belopp, och
bestämma hur avrundningen ska göras. Skriv testet först.

</details>

**4. Refaktorisera.** Flytta beräkningarna ur `app.py` till en egen fil som går att testa utan Flask.
Be om en lista med förslag, välj ett, kör testerna.

## Realistiskt att tänka på

Varukorgen ligger i sessionen, vilket är bra för ett exempel men inte för en riktig butik. Vad händer när
två personer köper den sista varan samtidigt? Där slutar leken och arkitekturen börjar.

**Fler idéer:** se [BACKLOG.md](BACKLOG.md). Det är förslag att inspireras av, inga krav.
