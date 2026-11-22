# Modul 08: AI i utvecklingsflödet, CI/CD och teamarbete

Ingen kod och inga övningar här. Videon handlar om var AI hör hemma i ett utvecklingsflöde, och var den
inte gör det. Här är frågor och promptar att ta med till ett AI-verktyg för att tänka vidare.

> Det här ersätter inga övningar. Läs först [hur du pratar med en AI](../docs/prata_med_ai.md).
> Klistra inte in kod, nycklar eller personuppgifter från ett riktigt jobb. Hitta på ett exempel.

## Börja här

- "Beskriv stegen i ett typiskt utvecklingsflöde, från idé till produktion. För varje steg: var kan ett
  AI-verktyg hjälpa, och var bör det **inte** få agera självständigt?"
- "Vad är CI/CD, och vad gör det för skillnad i ett team? Förklara för någon som bara har jobbat ensam."
- "Vad kan gå fel om ett AI-verktyg får skriva kod som sedan automatiskt byggs och släpps?"

## Teamarbete

- "Vi är ett team på fyra. Föreslå en kort uppsättning regler för hur vi använder AI-genererad kod i
  våra pull requests. Vad ska varje regel förhindra?"
- "Hur granskar man en pull request där en stor del är skriven av AI? Vad ska granskaren titta på extra?"
- "Hur ska ett team dokumentera att kod är AI-genererad, och är det en bra idé?"
- "Vem är ansvarig när AI-genererad kod orsakar en bugg i produktion?"

## Flödet i praktiken

- "Jag vill att testerna körs automatiskt vid varje push. Vilka frågor behöver jag svara på innan jag
  skriver flödet?" (Be om frågor, inte om kod först.)
- "Skriv ett förslag på ett GitHub Actions-flöde som kör mina tester. Förklara varje rad. Vad borde jag
  kontrollera innan jag litar på det?" Kontrollera sedan mot dokumentationen.
- "Vilka hemligheter får aldrig hamna i ett flöde eller en loggfil, och hur hanterar man dem?"
- "Vad skiljer kontinuerlig leverans från kontinuerlig driftsättning, och när är det ena att föredra?"

## Tips: installera `gh` och låt AI:n fixa CI/CD

`gh` är GitHubs kommandoradsverktyg. Med det kan ett AI-verktyg (Claude Code, OpenCode eller Copilot i
agentläge) själv skapa en pull request, se om flödet gick igenom och läsa felloggen, och sedan föreslå en
fix. Då slipper du klistra in loggar för hand, och det är ett bra sätt att se hur en agent arbetar med
ett riktigt flöde.

**Installera**

- macOS: `brew install gh`
- Windows: `winget install --id GitHub.cli`
- Linux: följ [GitHubs installationsguide](https://github.com/cli/cli#installation) för din distribution

Logga in med `gh auth login` och kontrollera med `gh auth status`.

**Det AI:n kan göra med `gh`**

```bash
gh run list --limit 5            # de senaste körningarna
gh run view <id> --log-failed    # loggen från det som föll
gh run watch                     # följ en pågående körning
gh pr create --fill              # skapa en pull request
gh pr checks                     # status för kontrollerna
```

**Promptar att prova**

- "Skapa ett GitHub Actions-flöde som kör mina tester vid varje push och pull request. Visa filen och
  förklara varje rad innan du sparar den."
- "Kör `gh run list --limit 5`, hitta den senaste körningen som misslyckades, läs loggen med
  `gh run view --log-failed` och förklara orsaken. Föreslå en fix, men ändra ingenting förrän jag har godkänt."
- "Flödet går igenom på min dator men faller på GitHub. Vilka skillnader i miljön kan förklara det?
  Läs loggen först."

**Ett litet flöde, så att du kan bedöma vad AI:n föreslår**

```yaml
name: tester
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m unittest
```

Versionerna (`@v4`, `@v5`) uppdateras, så kontrollera dem mot respektive åtgärds sida på GitHub. Verktyg
kan föreslå versioner som är gamla eller inte finns.

**Mini-övning (20–30 minuter)**

1. Skapa ett **privat** testrepo på GitHub med ett litet, påhittat projekt (till exempel en kopia av `modul_02_kassa`).
2. Be ditt AI-verktyg skapa flödet. Läs det innan du sparar det.
3. Pusha, och titta på körningen med `gh run watch`.
4. Ändra ett test så att det faller, och pusha igen.
5. Be AI:n läsa felloggen via `gh` och föreslå en fix. Läs diffen innan du godkänner.
6. Skriv i din AI-logg vad den hittade, och vad du själv hade missat.

**Säkerhet, viktigt**

- `gh auth login` ger verktyget åtkomst till dina repon. Använd ett konto du har för kursen, inte ett
  jobbkonto med tillgång till kundrepon, och arbeta i privata testrepon.
- Låt agenten **fråga innan den kör kommandon**. Var extra noga med sådant som `gh pr merge`,
  `gh repo delete`, `gh secret set` och `git push --force`.
- Läs flödesfilen. Vilka rättigheter ger den (`permissions:`), och vilka tredjepartsåtgärder (`uses:`) använder den?
- Hemligheter hör aldrig hemma i flödesfilen. Använd GitHub Secrets, och be inte AI:n skriva ut dem.
- Ett grönt flöde betyder bara att det flödet kontrollerar gick bra. Se modul 12.

## Be om motstånd

- "Argumentera för att ett team **inte** bör låta AI skriva kod som går direkt till produktion."
- "Vad är den största risken med att automatisera granskning med AI?"
- "Vilka delar av ett team-flöde bör alltid göras av människor?"

## Ett litet experiment (15 minuter)

Rita ditt eget team-flöde på ett papper (kod, granskning, test, bygge, release). Markera med tre färger
var AI får **göra själv**, var den får **föreslå** och var den **inte får vara med**. Fråga sedan ett
AI-verktyg om det håller med, och skriv ner var ni inte är överens.

## Skriv ner

I din AI-logg: en regel för AI-kod i team som du skulle vilja ha, och en som du tror skulle vara svår att följa.
