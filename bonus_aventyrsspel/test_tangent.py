import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from tangent import tolka_escape

HIT = Path(__file__).parent


@pytest.mark.parametrize(
    "rest, forvantat",
    [
        ("[A", "N"), ("[B", "S"), ("[C", "Ö"), ("[D", "V"),  # vanliga piltangenter
        ("OA", "N"), ("OD", "V"),  # applikationsläge
        ("[1;5C", "Ö"),  # Ctrl + höger
        ("", ""),  # ensam ESC
        ("[H", ""), ("[3~", ""), ("x", ""),  # Home, Delete och annat
    ],
)
def test_tolka_escape(rest, forvantat):
    assert tolka_escape(rest) == forvantat


# Riktiga tangenttryck genom en pseudoterminal (bara Linux/Mac)
pty = pytest.importorskip("pty")
termios = pytest.importorskip("termios")


def las_med_tangenter(*skickat, svar=None):
    """Startar las_kommando() i en riktig terminal, skickar tangenter och returnerar svaren.

    svar = hur många kommandon som förväntas (som standard ett per tangent).
    """
    master, slav = pty.openpty()
    kod = (
        "import tangent\n"
        f"for _ in range({len(skickat) if svar is None else svar}):\n"
        "    print(repr(tangent.las_kommando()), flush=True)\n"
    )
    barn = subprocess.Popen(
        [sys.executable, "-c", kod],
        stdin=slav, stdout=subprocess.PIPE, cwd=HIT, text=True,
    )
    os.close(slav)
    try:
        for data in skickat:
            # Vänta tills barnet har ställt om terminalen till tangent-för-tangent-läge
            for _ in range(200):
                if not termios.tcgetattr(master)[3] & termios.ICANON:
                    break
                time.sleep(0.01)
            os.write(master, data)
            time.sleep(0.15)
        barn.wait(timeout=5)
        return barn.stdout.read().split()
    finally:
        barn.kill()
        os.close(master)


def test_piltangenter_blir_riktningar():
    assert las_med_tangenter(b"\x1b[A", b"\x1b[B", b"\x1b[C", b"\x1b[D") == ["'N'", "'S'", "'Ö'", "'V'"]


def test_bokstaver_och_svenskt_o():
    assert las_med_tangenter(b"t", "ö".encode()) == ["'t'", "'ö'"]


def test_enter_och_mellanslag_ignoreras():
    assert las_med_tangenter(b"\n", b" ", b"d", svar=1) == ["'d'"]


def test_ensam_esc_ger_inget_kommando():
    assert las_med_tangenter(b"\x1b", b"q", svar=1) == ["'q'"]
