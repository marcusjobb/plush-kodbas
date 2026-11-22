# Modul 13: Jul (bonus)

Ingen video och ingen övning här. I stället får du lite julkod att leka med och promptar att ta med till
ett AI-verktyg. Det ersätter ingenting, och dina inlämningar går alltid först.

> Läs [hur du pratar med en AI](../docs/prata_med_ai.md) först. Använd bara påhittade namn när du provar
> hemlig tomte, särskilt om du klistrar in något i ett AI-verktyg.

## Tre steg: före, under och efter

Julmodulen ligger mitt emellan två delar av kursen, och den är byggd för att binda ihop dem.

| Steg | Hör ihop med | Vad du gör här |
|------|--------------|----------------|
| **Före** | Modul 12 (granska AI-kod kritiskt), 10 (etik och säkerhet) och 11 (AI Act) | Köra och **granska** julkoden: vad antar den, vad händer i gränsfall, vad testas inte? |
| **Under** | Modul 15 (kom igång med bygget) | Bygg **ett litet kort** ur backlogen, som en vertikal skiva: plan, kod, test, diff, commit |
| **Efter** | Modul 14 (från idé till plan) | Välj vad du vill bygga härnäst, avgränsa det och skriv en liten plan med "klart betyder" |

Börja alltså med att granska, bygg sedan lite, och avsluta med att planera. Det är samma rytm som i
projektet. Promptarna i [jul_prompts.md](jul_prompts.md) är ordnade efter de tre stegen.

## Det som finns här

| Fil | Vad |
|-----|-----|
| `julgran.py` | En blinkande julgran i terminalen |
| `hemlig_tomte.py` | Hemlig tomte med meny. Lottar så att ingen drar sig själv, och låter var och en titta i hemlighet |
| `hemlig_tomte_logic.py` | Logiken bakom lottningen, utan in- och utmatning så att den går att testa |
| `test_jul.py` | Tester |
| `xmas_c.md` | Ett klassiskt C-program att låta AI:n dissekera och göra om till Python. Promptar finns i `jul_prompts.md` |
| `jul_prompts.md` | Promptar och frågor till ett AI-verktyg |
| `BACKLOG.md` | Idéer att bygga vidare på |

## Kör

Du behöver bara Python 3.11 eller nyare.

```bash
cd modul_13_jul
python julgran.py                 # avsluta med Ctrl+C
python julgran.py --hojd 8        # mindre gran (3 till 16)
python hemlig_tomte.py
python -m unittest                # kör testerna
```

## Wow-momentet: välj "5. Slumpa och hoppas" i hemlig tomte

Om man lottar helt på måfå, hur ofta blir resultatet giltigt, alltså att ingen drar sig själv? Gissa först.
Kör sedan menyvalet. Andelen blir ungefär 37 % oavsett om ni är 5 eller 50. Varför? Det är en av de vackraste
matematiska överraskningarna som finns, och den hänger ihop med talet *e*. Be ett AI-verktyg förklara det steg
för steg, och kontrollera förklaringen själv med penna och papper för tre eller fyra personer.

## Granska först (före)

Innan du ändrar något, gör som i modul 12:

1. Läs `hemlig_tomte_logic.py` och skriv ner de antaganden den gör som inte står uttryckligen.
2. Ge dig själv fem gränsfall. Vad händer med två personer som inte får dra varandra? Med tre?
   Med två som heter likadant?
3. Titta i `test_jul.py`. Vad testas, och vad testas **inte**? Sabotera koden med flit och se vilka tester som blir röda.

## Bygg ett kort (under)

Ta ett kort ur [BACKLOG.md](BACKLOG.md), be om en plan först, godkänn den, bygg det minsta som fungerar,
skriv ett test och läs diffen innan du committar.

## Planera nästa steg (efter)

Titta på backloggen och fundera: vad av det här, eller vad du själv kommit på, skulle du vilja bygga som ett eget
projekt? Skriv fyra rader: vad det är, vad som **inte** ingår, vad "klart" betyder och vad som är den första
lilla skivan. Det är en mini-version av projektplanen i modul 14, och mallen finns i `modul_14_projektplan`.

## Regler

- All data är påhittad. Skriv aldrig in riktiga personuppgifter i ett AI-verktyg.
- Du ska kunna förklara varje rad du checkar in.
- Logga hur AI:n bidrog (mall finns i `modul_14_projektplan/ai_logg_mall.md`).
