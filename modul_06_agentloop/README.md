# Modul 06: Agentloopen

En agent är en loop: **tänk, använd ett verktyg, observera, upprepa**. Här kan du se loopen hända,
steg för steg, och ändra den.

> **Det här är ingen AI.** Agentens "tänkande" är vanliga if-satser. Det är medvetet. Du ska se
> strukturen utan att AI:ns slumpmässighet står i vägen.
>
> Det här är ett övningsexempel och ersätter inte övningarna på portalen (`/ovningar/06`).
> Där använder du en riktig agent på din egen kod.

## Kör

```bash
cd modul_06_agentloop
python agent_loop.py
```

Välj 1 första gången. Du får godkänna varje steg och se vad agenten gör.
Välj 4 för att sätta tillbaka buggen och köra om.

## Vad du ser

| Del i koden | Motsvarar |
|-------------|-----------|
| `TOOLS` | Verktygen: köra kod, läsa och skriva filer |
| `decide()` | Hjärnan: väljer nästa steg utifrån historiken |
| `run_agent()` | Loopen: tanke, verktyg, observation |
| `MAX_STEPS` | Gränsen: en agent ska alltid kunna stoppas |
| `approved()` | Din kontroll: vilka steg får agenten göra själv? |

## Prova

1. **Ta bort ett verktyg** ur `TOOLS`, till exempel `read_file`. Vad händer? Kan agenten lösa uppgiften
   ändå? (Det här är övning 3 på portalen, fast i kod.)
2. **Lägg till en ny bugg** i `vat.py` som agenten inte har en regel för. Hur beter den sig?
3. **Skriv en egen regel** i `FIX_RULES` för den nya buggen.
4. **Lägg till ett verktyg**, till exempel `git_diff`, och låt agenten visa vad den ändrat innan den kör testerna.
5. **Sänk `MAX_STEPS`** till 3. Vad säger det om varför riktiga agenter har stoppgränser?
6. **Utmaning:** byt ut `decide()` mot ett anrop till en språkmodell. Vad måste du skicka med för att
   modellen ska veta vad som hänt hittills? (Svar: historiken.)

## Att tänka på

Agenten ändrar filer. Därför frågar den dig före varje skrivning i läge 1 och 2. Det är samma tanke som
när riktiga verktyg ber dig godkänna steg: du bestämmer hur mycket frihet den får.

**Fler idéer:** se [BACKLOG.md](BACKLOG.md). Det är förslag att inspireras av, inga krav.
