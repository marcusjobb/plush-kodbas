"""Läser ett tangenttryck i taget, med stöd för piltangenter.

las_kommando() returnerar samma text som motor.Spel.kommando förstår:
piltangenterna blir N, S, Ö och V, och övriga tangenter returneras som de är.
Är stdin inte en terminal (t.ex. pipad inmatning) faller den tillbaka på input().
"""

import sys

# Piltangenterna efter ESC [ eller ESC O (Linux/Mac) och efter 0xE0/0x00 (Windows)
PILAR_ANSI = {"A": "N", "B": "S", "C": "Ö", "D": "V"}
PILAR_WINDOWS = {"H": "N", "P": "S", "M": "Ö", "K": "V"}


def tolka_escape(rest):
    """Tolkar tecknen som följer efter ESC. Returnerar N/S/Ö/V, eller "" om det inte är en pil.

    Hanterar även pilar med modifierare, som ESC [ 1 ; 5 A (Ctrl + uppåt).
    """
    if rest[:1] in ("[", "O") and rest[-1:] in PILAR_ANSI:
        return PILAR_ANSI[rest[-1]]
    return ""


def _las_unix():
    import codecs
    import os
    import select
    import termios
    import tty

    fd = sys.stdin.fileno()
    gammal = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)  # tangent för tangent, men Ctrl-C fungerar fortfarande
        avkodare = codecs.getincrementaldecoder("utf-8")(errors="ignore")
        tecken = ""
        while not tecken:
            data = os.read(fd, 1)
            if not data:
                raise EOFError
            tecken = avkodare.decode(data)  # ö är två byte i UTF-8

        if tecken == "\x1b":
            rest = ""
            # Resten av en piltangent kommer direkt efter ESC. En ensam ESC gör det inte.
            while len(rest) < 8 and select.select([fd], [], [], 0.05)[0]:
                rest += os.read(fd, 1).decode("ascii", "ignore")
            return tolka_escape(rest)
        if tecken == "\x04":  # Ctrl-D
            raise EOFError
        return tecken
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, gammal)


def _las_windows():
    import msvcrt

    tecken = msvcrt.getwch()
    if tecken in ("\x00", "\xe0"):  # specialtangent, nästa tecken säger vilken
        return PILAR_WINDOWS.get(msvcrt.getwch(), "")
    if tecken == "\x03":
        raise KeyboardInterrupt
    return tecken


def las_tangent():
    """Väntar på ett tangenttryck och returnerar det (pilar blir N/S/Ö/V)."""
    if sys.platform == "win32":
        return _las_windows()
    return _las_unix()


def las_kommando():
    """Returnerar nästa kommando. Ignorerar Enter, mellanslag och okända specialtangenter."""
    if not sys.stdin.isatty():
        return input()
    while True:
        tecken = las_tangent()
        if tecken.strip():
            return tecken
