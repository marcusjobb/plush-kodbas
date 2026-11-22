"""Spelets tillstånd och regler. Ingen in- eller utmatning, så allt går att testa."""

import random

from labyrint import (
    BREDD,
    GULD_NYCKEL,
    HOJD,
    LAMPA,
    RIKTNINGAR,
    ROD_NYCKEL,
    generera,
    kant,
)

RIKTNINGSNAMN = {"N": "norr", "S": "söder", "Ö": "öster", "V": "väster"}
HJALP = "Tangenter: piltangenter eller N S Ö V = gå, T = ta, D = öppna utgången, I = väskan, Q = avsluta"


class Spel:
    def __init__(self, seed=None, bredd=BREDD, hojd=HOJD):
        self.lab = generera(bredd, hojd, random.Random(seed))
        self.rum = self.lab.start
        self.besokta = {self.rum}
        self.inventarie = set()
        self.foremal = {rum: list(saker) for rum, saker in self.lab.foremal.items()}
        self.last_upplast = False
        self.klart = False
        self.avslutat = False

    # --- frågor som UI:t använder ---
    @property
    def dorrar(self):
        return self.lab.dorrar[self.rum]

    def ar_last(self, a, b):
        return self.lab.last_kant == kant(a, b) and not self.last_upplast

    def ar_morkt(self):
        return self.rum in self.lab.morka and LAMPA not in self.inventarie

    def synliga_foremal(self):
        return [] if self.ar_morkt() else self.foremal[self.rum]

    def ar_utgang(self):
        return self.rum == self.lab.utgang

    # --- kommandon ---
    def kommando(self, text):
        """Utför ett kommando och returnerar ett meddelande (kan vara tomt)."""
        kommando = text.strip().upper()
        if kommando == "O":  # tillåt O för Ö
            kommando = "Ö"

        if kommando == "Q":
            self.avslutat = True
            return "Du gav upp. Hejdå!"
        if kommando in RIKTNINGAR:
            return self._ga(kommando)
        if kommando == "T":
            return self._ta()
        if kommando == "D":
            return self._oppna_utgang()
        if kommando == "I":
            return self._vaskan()
        return f"Förstår inte.\n{HJALP}"

    def _ga(self, riktning):
        if riktning not in self.dorrar:
            return "Där är det bara vägg."
        nytt = self.dorrar[riktning]
        meddelande = ""
        if self.ar_last(self.rum, nytt):
            if ROD_NYCKEL not in self.inventarie:
                return "Dörren är låst. Du behöver en röd nyckel."
            self.last_upplast = True
            meddelande = "Du låser upp den röda dörren med din röda nyckel."
        self.rum = nytt
        self.besokta.add(nytt)
        return meddelande

    def _ta(self):
        if self.ar_morkt():
            return "Det är för mörkt för att hitta något."
        saker = self.foremal[self.rum]
        if not saker:
            return "Här finns inget att ta."
        tagna = ", ".join(saker)
        self.inventarie.update(saker)
        self.foremal[self.rum] = []
        return f"Du tog: {tagna}."

    def _oppna_utgang(self):
        if not self.ar_utgang():
            return "Det finns ingen utgångsdörr här."
        if GULD_NYCKEL not in self.inventarie:
            return "Utgångsdörren är låst. Du behöver guldnyckeln."
        self.klart = True
        return "Nyckeln passar! Du är ute. Grattis!"

    def _vaskan(self):
        if not self.inventarie:
            return "Din väska är tom."
        return "Du bär på: " + ", ".join(sorted(self.inventarie)) + "."
