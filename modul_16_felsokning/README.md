# Modul 16: Felsökning och refaktorisering

`fakturor.py` räknar ut en faktura med mängdrabatt, kundrabatt, moms och dröjsmålsavgift. Den fungerar
för de enklaste fallen, men den är rörig, saknar tester och har minst två fel.

> Det här är ett övningsexempel och ersätter inte övningarna på portalen (`/ovningar/16`).
> Där arbetar du i ditt eget projekt. Här får du kod som är precis så rörig som kod brukar vara.

## Kör

```bash
cd modul_16_felsokning
python fakturameny.py     # prova för hand
python -m unittest        # kör testerna (det finns ett enda)
```

## Gör så här, i den här ordningen

1. **Skydda först.** Be AI:n skriva tester som fångar hur funktionen beter sig *just nu*, även om det
   är konstigt. Läs testerna: testar de beteende, eller bara att koden körs?
2. **Sabotera.** Byt ett `>` mot `>=` i koden. Blir något test rött? Om inte saknas ett test. Ångra.
3. **Felsök med hypoteser.** Räkna ut några fakturor för hand och jämför med programmet. Hittar du en
   skillnad? Be AI:n om tre möjliga orsaker, utan fix, och testa dem själv.
4. **Refaktorisera i små steg.** Be om en lista med förslag. Välj ett, ge en avgränsad instruktion
   ("extrahera mängdrabatten till en egen funktion, ändra inte beteendet, rör inga andra filer"), kör testerna, läs diffen.
5. **När AI:n har fel.** Notera varje gång förslaget var fel eller byggde på något som inte stämde.

## Saker att fundera på

- Vad ska hända med en negativ kvantitet? Funktionen svarar, men borde den det?
- Är `float` rätt typ för pengar?
- Vad händer om `forfallodatum` är `None`?
- Vad betyder "5 % rabatt vid tio varor eller fler" i koden jämfört med kommentaren?

<details markdown="1">
<summary>Kända fel (hitta dem själv först)</summary>

1. Kommentaren säger "tio varor eller fler", men villkoret `antal > 10` ger rabatt först vid elva.
2. Dröjsmålsavgiften räknas på hela månader (`dagar // 30`), men kommentaren säger "per påbörjad månad".
   Betalar du 5 dagar sent blir avgiften noll.
3. Ordningen på rabatt och moms är en affärsregel som ingen skrivit ner. Fråga vad som gäller.
4. Pengar som `float` ger avrundningsfel. Prova `Decimal`.

Att refaktorisera *bort* ett fel utan att märka det är precis vad testerna i steg 1 ska hindra.

</details>

**Fler idéer:** se [BACKLOG.md](BACKLOG.md). Det är förslag att inspireras av, inga krav.
