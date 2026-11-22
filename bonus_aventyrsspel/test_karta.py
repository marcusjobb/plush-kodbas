import math
import re

import pytest

from aventyr import (
    SKARM_BREDD,
    SKARM_HOJD,
    TEXTRADER,
    bygg_skarm,
    kartstorlek,
    rita_karta,
)
from motor import HJALP, Spel


def utan_farg(text):
    return re.sub(r"\033\[[0-9;]*m", "", text)


def karta(spel):
    return utan_farg(rita_karta(spel))


def synliga_rader(text):
    """Hur många rader texten tar i en konsol, där en för lång rad bryts till flera."""
    return sum(max(1, math.ceil(len(rad) / SKARM_BREDD)) for rad in utan_farg(text).split("\n"))


def test_spelaren_syns_med_stjarna_pa_start():
    text = karta(Spel(1))
    assert text.count("*") == 1
    assert text.count("[") == 1  # bara spelarens rum är besökt


def test_okanda_grannar_visas_som_fragetecken():
    spel = Spel(1)
    text = karta(spel)
    assert text.count("?") == len(spel.dorrar)
    assert text.count("(") == len(spel.dorrar)


def test_kartan_vaxer_nar_man_utforskar():
    spel = Spel(1)
    before = karta(spel).count("?")
    riktning = next(iter(spel.dorrar))
    spel.kommando(riktning)
    text = karta(spel)
    assert text.count("*") == 1
    assert text.count("[") == 2  # startrummet är nu besökt, och spelaren står i nästa
    assert text != karta(Spel(1)) and before > 0


def test_stjarnan_foljer_med():
    spel = Spel(1)
    first = karta(spel)
    spel.kommando(next(iter(spel.dorrar)))
    assert karta(spel) != first


def test_last_dorr_ritas_nar_den_syns():
    spel = Spel(1)
    spel.besokta = set(spel.lab.dorrar)  # låtsas att allt är utforskat
    text = karta(spel)
    assert "┤ ├" in text or "╪" in text
    spel.last_upplast = True
    text = karta(spel)
    assert "┤ ├" not in text and "╪" not in text


# --- Storlek: hela skärmen ska rymmas i 100 tecken och 20 rader ---

STORLEKAR = [(3, 3), (5, 4), (14, 3), (3, 6), (10, 5), (14, 6)]


@pytest.mark.parametrize("bredd, hojd", STORLEKAR)
def test_kartstorlek_stammer_med_ritningen(bredd, hojd):
    spel = Spel(1, bredd, hojd)
    spel.besokta = set(spel.lab.dorrar)  # allt utforskat: kartan i full storlek
    rader = karta(spel).split("\n")
    forvantat_rader, forvantad_bredd = kartstorlek(bredd, hojd)
    assert len(rader) == forvantat_rader
    assert max(len(rad) for rad in rader) <= forvantad_bredd


@pytest.mark.parametrize("bredd, hojd", STORLEKAR)
@pytest.mark.parametrize("seed", range(5))
def test_hela_skarmen_rymmer_sig_i_100_x_20(bredd, hojd, seed):
    """Prövar varje rum i huset, med de längsta meddelandena som finns."""
    spel = Spel(seed, bredd, hojd)
    spel.besokta = set(spel.lab.dorrar)
    meddelanden = [
        f"Du vaknar i ett låst hus. Hitta guldnyckeln och ta dig ut!\n{HJALP}",
        f"Förstår inte.\n{HJALP}",
        spel.kommando("xyz"),  # det riktiga felmeddelandet i spelet
    ]
    for rum in spel.lab.pos:
        spel.rum = rum
        for meddelande in meddelanden:
            skarm = utan_farg(bygg_skarm(spel, meddelande))
            rader = skarm.split("\n")
            assert len(rader) <= SKARM_HOJD
            assert max(len(rad) for rad in rader) <= SKARM_BREDD


def test_kartan_ensam_ryms_alltid_i_bredden():
    for bredd, hojd in STORLEKAR:
        _, tecken = kartstorlek(bredd, hojd)
        assert tecken <= SKARM_BREDD


def test_gransen_14_x_6_ar_den_storsta_som_garanterat_rymmer():
    """Gränsen räknas på det värsta tänkbara rummet, inte på ett enskilt rum."""
    rader_14_6, tecken_14_6 = kartstorlek(14, 6)
    assert rader_14_6 + TEXTRADER <= SKARM_HOJD and tecken_14_6 <= SKARM_BREDD
    rader_14_7, _ = kartstorlek(14, 7)
    assert rader_14_7 + TEXTRADER > SKARM_HOJD  # en rad högre och skärmen kan spricka
    _, tecken_15_3 = kartstorlek(15, 3)
    assert tecken_15_3 > SKARM_BREDD  # ett rum bredare och kartan spricker


def test_varsta_tankbara_rummet_i_det_storsta_huset_ryms():
    """Utgångsrum med tre föremål och det längsta meddelandet: alla textrader används."""
    spel = Spel(1, 14, 6)
    spel.besokta = set(spel.lab.dorrar)
    spel.rum = spel.lab.utgang
    spel.lab.morka.discard(spel.rum)
    spel.foremal[spel.rum] = ["lampa", "röd nyckel", "guldnyckel"]
    skarm = utan_farg(bygg_skarm(spel, f"Du vaknar i ett låst hus. Hitta guldnyckeln och ta dig ut!\n{HJALP}"))
    assert len(skarm.split("\n")) == SKARM_HOJD  # precis full, och inte en rad mer
