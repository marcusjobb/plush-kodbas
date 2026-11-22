# Bonus: Äventyrsspelet

Ett textäventyr i konsolen. Du vaknar i ett låst hus med 20 rum. Hitta den röda nyckeln, lampan och
guldnyckeln, och ta dig ut genom utgångsdörren. Huset slumpas varje gång, och kartan visar bara rum du har besökt.

Spelet byggdes live i en lektion, med GitHub Copilot som agent.

> **Spelet är inte färdigt, med flit.** Det fungerar och har tester, men det finns mer att bygga.
> Se [BACKLOG.md](BACKLOG.md) för idéer. Det är en bonus och ersätter inga övningar på portalen.

## Kör

Du behöver Python 3.11 eller nyare. Spelet använder bara standardbiblioteket.

```bash
cd bonus_aventyrsspel
python aventyr.py
```

Styr med piltangenterna eller **N S Ö V**. **T** tar ett föremål, **D** öppnar utgången, **I** visar väskan
och **Q** avslutar.

## Tester

Testerna använder `pytest`:

```bash
pip install pytest
python -m pytest
```

Många av testerna körs mot 300 olika slumpade hus. De kontrollerar bland annat att varje hus går att
klara, oavsett hur det slumpas.

## Så hänger det ihop

| Fil | Ansvar |
|-----|--------|
| `labyrint.py` | Skapar huset: rum, dörrar, föremål, en låst dörr och mörka rum. Garanterar att huset går att klara |
| `motor.py` | Spelreglerna: förflyttning, föremål, utgång. Ingen in- eller utmatning, så den går att testa |
| `tangent.py` | Läser ett tangenttryck i taget, med stöd för piltangenter |
| `aventyr.py` | Skärmen: ritar kartan och skriver ut rummen |
| `test_*.py` | Tester för varje del |

Notera uppdelningen: reglerna känner inte till skärmen. Därför går de att testa utan att starta spelet.

## Prova

1. **Läs `labyrint.py`** och förklara med egna ord hur den garanterar att huset går att klara.
   Be sedan AI:n förklara samma sak och jämför.
2. **Ta ett kort från backlogen** och bygg det i en vertikal skiva: plan, kod, test, diff, commit.
3. **Bryt spelet med flit.** Ändra en regel (till exempel att den röda nyckeln läggs *efter* den låsta
   dörren) och se vilka tester som blir röda. Är det de du väntade dig?
4. **Granska AI-koden.** Spelet är skrivet med hjälp av AI. Vad skulle du ändra? Vilka namn,
   funktioner eller kommentarer är du osäker på?
