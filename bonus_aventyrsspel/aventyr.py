"""Äventyrsspel i en slumpad labyrint.

Du vaknar i ett låst hus. Hitta guldnyckeln och ta dig ut genom utgångsdörren.
Husets planlösning slumpas varje gång, och kartan visar bara rum du har besökt.

Själva spelreglerna ligger i motor.py och labyrinten genereras i labyrint.py.
Den här filen sköter bara skärmen och inmatningen.

Hela skärmen (kartan plus texten under) ska rymmas i en konsol på 100 tecken i bredd
och 20 rader i höjd. Det styr hur stort ett hus kan vara, se kartstorlek() nedan.
"""

import os

from motor import HJALP, RIKTNINGSNAMN, Spel
from tangent import las_kommando

SKARM_BREDD = 100  # tecken
SKARM_HOJD = 20  # rader
INDRAG = 2  # blanksteg före kartan
LUCKA = 3  # tecken mellan två rum i sidled, där korridoren ritas
TEXTRADER = 9  # det mesta texten under kartan kan ta: blankrad, rum, dörrar, föremål, utgång, meddelande, prompt

GUL = "\033[1;33m"
NOLLA = "\033[0m"


def rensa_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def nummerbredd(antal_rum):
    """Hur många tecken rumsnumret behöver, till exempel 2 för hus med upp till 99 rum."""
    return len(str(antal_rum))


def kartstorlek(bredd, hojd):
    """Hur stor hela kartan blir som (rader, tecken), inklusive indrag.

    Ett rum är en rad, och mellan två rumsrader finns en rad för korridorerna uppåt och nedåt.
    """
    rumsbredd = nummerbredd(bredd * hojd) + 2
    return 2 * hojd - 1, INDRAG + bredd * rumsbredd + (bredd - 1) * LUCKA


def rita_ruta(nr, status, bredd):
    """Returnerar rummet som en lista av tecken. status: spelare/besökt/okänd."""
    if status == "spelare":
        inre = list("*".center(bredd))
        inre[inre.index("*")] = f"{GUL}*{NOLLA}"
        return ["["] + inre + ["]"]
    if status == "okänd":
        return ["("] + list("?".center(bredd)) + [")"]
    return ["["] + list(str(nr).rjust(bredd)) + ["]"]


def rita_karta(spel):
    """Ritar husets planlösning. Bara besökta rum och deras grannar (?) syns."""
    lab = spel.lab
    nr_bredd = nummerbredd(lab.bredd * lab.hojd)
    ruta = nr_bredd + 2
    steg_x = ruta + LUCKA
    duk = [
        [" "] * (lab.bredd * ruta + (lab.bredd - 1) * LUCKA)
        for _ in range(2 * lab.hojd - 1)
    ]

    def besokt(rum):
        return rum in spel.besokta

    def syns(rum):
        return besokt(rum) or any(besokt(g) for g in lab.dorrar[rum].values())

    for rum, (rad, kol) in lab.pos.items():
        if not syns(rum):
            continue
        status = "spelare" if rum == spel.rum else "besökt" if besokt(rum) else "okänd"
        for dx, tecken in enumerate(rita_ruta(rum, status, nr_bredd)):
            duk[rad * 2][kol * steg_x + dx] = tecken

    for rum, (rad, kol) in lab.pos.items():
        for riktning in ("Ö", "S"):
            granne = lab.dorrar[rum].get(riktning)
            if granne is None or not (besokt(rum) or besokt(granne)):
                continue
            last = spel.ar_last(rum, granne)
            if riktning == "Ö":
                bit = "┤ ├" if last else "─" * LUCKA
                for dx, tecken in enumerate(bit):
                    duk[rad * 2][kol * steg_x + ruta + dx] = tecken
            else:
                duk[rad * 2 + 1][kol * steg_x + ruta // 2] = "╪" if last else "│"

    return "\n".join(" " * INDRAG + "".join(rad).rstrip() for rad in duk)


def beskrivning(spel):
    """Rummets text som en lista med rader."""
    namn, text = spel.lab.rumsinfo[spel.rum]
    rader = [f"--- {namn} ---"]
    rader.append("Det är becksvart här. Du famlar längs väggarna." if spel.ar_morkt() else text)

    dorrar = ", ".join(
        f"{k} ({RIKTNINGSNAMN[k]}{', låst' if spel.ar_last(spel.rum, g) else ''})"
        for k, g in spel.dorrar.items()
    )
    rader.append(f"Dörrar: {dorrar}")

    saker = spel.synliga_foremal()
    if saker:
        rader.append(f"Du ser på golvet: {', '.join(saker)} (skriv T för att ta)")
    if spel.ar_utgang():
        rader.append("Här finns den stora utgångsdörren! (skriv D för att öppna den)")
    return rader


def bygg_skarm(spel, meddelande=""):
    """Hela skärmen som en sträng, utan avslutande radbrytning. Ren funktion, så den går att mäta."""
    rader = [rita_karta(spel), "", *beskrivning(spel)]
    if meddelande:
        rader.append(meddelande)
    rader.append("> ")
    return "\n".join(rader)


def spela(seed=None):
    spel = Spel(seed)
    meddelande = f"Du vaknar i ett låst hus. Hitta guldnyckeln och ta dig ut!\n{HJALP}"

    while True:
        rensa_terminal()
        print(bygg_skarm(spel, meddelande), end="", flush=True)
        try:
            text = las_kommando()
        except (EOFError, KeyboardInterrupt):
            print("\nSpelet avslutas.")
            return

        meddelande = spel.kommando(text)
        if spel.klart or spel.avslutat:
            rensa_terminal()
            print(rita_karta(spel))
            print(f"\n{meddelande}")
            return


if __name__ == "__main__":
    spela()
