import random

import pytest

from labyrint import GULD_NYCKEL, LAMPA, ROD_NYCKEL, bfs, generera, kant

SEEDS = range(500)


def lab_for(seed):
    return generera(rng=random.Random(seed))


@pytest.mark.parametrize("seed", SEEDS)
def test_alla_rum_hanger_ihop(seed):
    lab = lab_for(seed)
    avstand, _ = bfs(lab.dorrar, lab.start)
    assert set(avstand) == set(lab.dorrar) and len(lab.dorrar) == lab.bredd * lab.hojd


@pytest.mark.parametrize("seed", SEEDS)
def test_dorrar_ar_symmetriska(seed):
    lab = lab_for(seed)
    for rum, dorrar in lab.dorrar.items():
        for granne in dorrar.values():
            assert rum in lab.dorrar[granne].values()


@pytest.mark.parametrize("seed", SEEDS)
def test_utgang_ar_inte_start(seed):
    lab = lab_for(seed)
    assert lab.utgang != lab.start


@pytest.mark.parametrize("seed", SEEDS)
def test_last_dorr_gar_inte_att_kringga(seed):
    lab = lab_for(seed)
    assert lab.last_kant is not None
    utan_dorren, _ = bfs(lab.dorrar, lab.start, sparrad=lab.last_kant)
    assert lab.utgang not in utan_dorren
    # Dörren måste vara en riktig passage
    a, b = tuple(lab.last_kant)
    assert b in lab.dorrar[a].values()


def plats(lab, sak):
    return [rum for rum, saker in lab.foremal.items() if sak in saker]


@pytest.mark.parametrize("seed", SEEDS)
def test_foremal_ligger_pa_ratt_sida_av_dorren(seed):
    lab = lab_for(seed)
    sida_a, _ = bfs(lab.dorrar, lab.start, sparrad=lab.last_kant)

    for sak in (ROD_NYCKEL, LAMPA):
        (rum,) = plats(lab, sak)
        assert rum in sida_a  # nås utan att passera dörren

    (guld,) = plats(lab, GULD_NYCKEL)
    assert guld not in sida_a
    assert guld in lab.morka
    assert lab.utgang not in lab.morka
    assert not (lab.morka & set(sida_a))


@pytest.mark.parametrize("seed", range(50))
def test_samma_seed_ger_samma_labyrint(seed):
    a, b = lab_for(seed), lab_for(seed)
    assert a.dorrar == b.dorrar and a.foremal == b.foremal
    assert a.rumsinfo == b.rumsinfo and a.last_kant == b.last_kant


def test_olika_seeds_ger_olika_labyrinter():
    assert len({str(lab_for(s).dorrar) for s in range(20)}) > 10


def test_varje_rum_har_namn_och_text():
    lab = lab_for(1)
    assert set(lab.rumsinfo) == set(lab.dorrar)
    assert all(namn and text for namn, text in lab.rumsinfo.values())


def test_liten_labyrint_utan_lasning_gar_att_generera():
    lab = generera(3, 1, random.Random(1))  # bara tre rum i rad: för litet för en dörr
    assert lab.last_kant is None and lab.morka == set()
    assert sum(GULD_NYCKEL in s for s in lab.foremal.values()) == 1
    assert lab.utgang == 3


def test_kant_ar_oordnad():
    assert kant(1, 2) == kant(2, 1)
