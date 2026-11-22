from collections import deque

import pytest

from labyrint import GULD_NYCKEL, LAMPA, ROD_NYCKEL
from motor import Spel

SEEDS = range(300)


def hitta(spel, sak):
    return next(rum for rum, saker in spel.foremal.items() if sak in saker)


def vag_dit(spel, mal):
    """Kortaste vägen i riktningar, med hänsyn till den låsta dörren."""
    fran = {spel.rum: None}
    ko = deque([spel.rum])
    while ko:
        rum = ko.popleft()
        for riktning, granne in spel.lab.dorrar[rum].items():
            if granne in fran:
                continue
            if spel.ar_last(rum, granne) and ROD_NYCKEL not in spel.inventarie:
                continue
            fran[granne] = (rum, riktning)
            ko.append(granne)
    steg = []
    while fran[mal] is not None:
        rum, riktning = fran[mal]
        steg.append(riktning)
        mal = rum
    return steg[::-1]


def ga_till(spel, mal):
    for riktning in vag_dit(spel, mal):
        spel.kommando(riktning)
    assert spel.rum == mal


@pytest.mark.parametrize("seed", SEEDS)
def test_spelet_gar_att_vinna(seed):
    spel = Spel(seed)
    platser = {sak: hitta(spel, sak) for sak in (LAMPA, ROD_NYCKEL, GULD_NYCKEL)}
    for sak, rum in platser.items():
        if sak in spel.inventarie:  # låg i samma rum som ett tidigare föremål
            continue
        ga_till(spel, rum)
        assert sak in spel.kommando("T")
        assert sak in spel.inventarie
    ga_till(spel, spel.lab.utgang)
    assert "Grattis" in spel.kommando("D")
    assert spel.klart


def test_guldnyckeln_kraver_lampa():
    spel = Spel(1)
    ga_till(spel, hitta(spel, ROD_NYCKEL))
    spel.kommando("T")
    guld = hitta(spel, GULD_NYCKEL)
    ga_till(spel, guld)
    assert spel.ar_morkt() and spel.synliga_foremal() == []
    assert "mörkt" in spel.kommando("T")
    assert GULD_NYCKEL not in spel.inventarie


def test_lasta_dorren_stoppar_utan_nyckel():
    spel = Spel(1)
    a, b = sorted(spel.lab.last_kant)
    spel.rum = a if b in spel.lab.dorrar[a].values() else b
    andra = b if spel.rum == a else a
    riktning = next(r for r, g in spel.dorrar.items() if g == andra)
    assert "låst" in spel.kommando(riktning)
    assert spel.rum != andra
    spel.inventarie.add(ROD_NYCKEL)
    assert "låser upp" in spel.kommando(riktning)
    assert spel.rum == andra and not spel.ar_last(a, b)


def test_utgangen_kraver_guldnyckel():
    spel = Spel(1)
    assert "ingen utgångsdörr" in spel.kommando("D")
    spel.rum = spel.lab.utgang
    assert "guldnyckeln" in spel.kommando("D")
    assert not spel.klart


def test_vagg_och_okanda_kommandon():
    spel = Spel(1)
    start = spel.rum
    saknad = next(r for r in "NSÖV" if r not in spel.dorrar)
    assert "vägg" in spel.kommando(saknad)
    assert "Förstår inte" in spel.kommando("xyz")
    assert spel.rum == start


def test_o_fungerar_som_ö():
    spel = Spel(1)
    if "Ö" in spel.dorrar:
        spel.kommando("o")
        assert spel.rum != spel.lab.start


def test_vaskan_och_ta_i_tomt_rum():
    spel = Spel(1)
    assert spel.kommando("I") == "Din väska är tom."
    assert "inget att ta" in spel.kommando("T")
    spel.inventarie.update({LAMPA, ROD_NYCKEL})
    assert spel.kommando("I") == "Du bär på: lampa, röd nyckel."


def test_avsluta():
    spel = Spel(1)
    spel.kommando("q")
    assert spel.avslutat and not spel.klart
