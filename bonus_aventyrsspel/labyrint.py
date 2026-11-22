"""Genererar en slumpad labyrint med föremål, en låst dörr och mörka rum.

Ingen in- eller utmatning här, bara ren generering, så att allt går att testa.

Lösbarhet garanteras genom konstruktion:
  1. En spanning tree (slumpad DFS) ger en labyrint där alla rum hänger ihop.
  2. Utgången läggs i det rum som ligger längst från start.
  3. Den låsta dörren väljs på den enda vägen start -> utgång. Alla rum delas då
     i sida A (före dörren) och sida B (efter dörren).
  4. Extra genvägar (loopar) läggs bara inom samma sida, så dörren går aldrig att kringgå.
  5. Röd nyckel och lampa läggs på sida A. Guldnyckeln läggs i ett mörkt rum på sida B.
"""

import math
import random
from collections import deque
from dataclasses import dataclass

BREDD = 5
HOJD = 4
ANDEL_LOOPAR = 0.4  # andel av de "extra" väggarna som blir genvägar

# riktning -> (radändring, kolumnändring)
RIKTNINGAR = {"N": (-1, 0), "S": (1, 0), "Ö": (0, 1), "V": (0, -1)}
MOTSATT = {"N": "S", "S": "N", "Ö": "V", "V": "Ö"}

ROD_NYCKEL = "röd nyckel"
GULD_NYCKEL = "guldnyckel"
LAMPA = "lampa"

RUMSNAMN = [
    ("Hallen", "Ett stort rum med ett trasigt draperi."),
    ("Köket", "Det luktar gammal soppa och något bränt."),
    ("Biblioteket", "Hyllor av dammiga böcker når upp till taket."),
    ("Källaren", "Luften är kall och väggarna är fuktiga."),
    ("Vindsrummet", "Tak i snedtak och spindelväv i alla hörn."),
    ("Matsalen", "Ett långt bord står dukat för tolv personer."),
    ("Sovrummet", "En ostädad säng och en tickande väckarklocka."),
    ("Badrummet", "Kaklet är sprucket och kranen droppar."),
    ("Arbetsrummet", "Ett skrivbord full av papper och en kall kaffekopp."),
    ("Vinkällaren", "Rad efter rad av flaskor vilar i mörkret."),
    ("Växthuset", "Fuktig värme och växter som tagit över."),
    ("Salongen", "Sammetsfåtöljer och en tyst, stor kakelugn."),
    ("Förrådet", "Burkar, lådor och en vältad stege."),
    ("Tvättstugan", "En sliten mangel och korgar med gamla lakan."),
    ("Musikrummet", "Ett piano med en ensam tangent som ligger nere."),
    ("Barnkammaren", "Gamla leksaker ligger utspridda på golvet."),
    ("Verkstaden", "Verktyg hänger prydligt på väggen, de flesta rostiga."),
    ("Kapellet", "Ljuset faller färgat genom ett litet fönster."),
    ("Rustkammaren", "Rostiga rustningar står på rad i skuggan."),
    ("Skafferiet", "Hyllor med burkar, de flesta med tveksamt innehåll."),
    ("Korridoren", "Ett smalt rum där golvet knarrar för varje steg."),
    ("Observatoriet", "Ett stort teleskop pekar mot ett sprucket tak."),
    ("Spegelrummet", "Du ser dig själv från alla håll."),
    ("Trädgårdsrummet", "Stenplattor, murgröna och ett tomt fågelbad."),
    ("Matkällaren", "Det doftar jord och gamla äpplen."),
]


@dataclass
class Labyrint:
    bredd: int
    hojd: int
    dorrar: dict  # rum -> {riktning: grannrum}
    pos: dict  # rum -> (rad, kolumn)
    start: int
    utgang: int
    last_kant: object  # frozenset({rum, rum}) eller None
    foremal: dict  # rum -> [föremål]
    morka: set  # rum utan ljus
    rumsinfo: dict  # rum -> (namn, text)


def rum_id(rad, kol, bredd):
    return rad * bredd + kol + 1


def kant(a, b):
    return frozenset((a, b))


def _grannar(rad, kol, bredd, hojd):
    for riktning, (dr, dk) in RIKTNINGAR.items():
        nr, nk = rad + dr, kol + dk
        if 0 <= nr < hojd and 0 <= nk < bredd:
            yield riktning, nr, nk


def _bygg_trad(bredd, hojd, rng):
    dorrar = {rum_id(r, k, bredd): {} for r in range(hojd) for k in range(bredd)}
    besokta = {rum_id(0, 0, bredd)}
    stack = [(0, 0)]
    while stack:
        rad, kol = stack[-1]
        val = [
            (riktning, nr, nk)
            for riktning, nr, nk in _grannar(rad, kol, bredd, hojd)
            if rum_id(nr, nk, bredd) not in besokta
        ]
        if not val:
            stack.pop()
            continue
        riktning, nr, nk = rng.choice(val)
        a, b = rum_id(rad, kol, bredd), rum_id(nr, nk, bredd)
        dorrar[a][riktning] = b
        dorrar[b][MOTSATT[riktning]] = a
        besokta.add(b)
        stack.append((nr, nk))
    return dorrar


def bfs(dorrar, start, sparrad=None):
    """Bredden-först. Returnerar (avstånd, förälder). Den spärrade kanten passeras inte."""
    avstand = {start: 0}
    foralder = {start: None}
    ko = deque([start])
    while ko:
        rum = ko.popleft()
        for granne in dorrar[rum].values():
            if granne in avstand or kant(rum, granne) == sparrad:
                continue
            avstand[granne] = avstand[rum] + 1
            foralder[granne] = rum
            ko.append(granne)
    return avstand, foralder


def vag_till(foralder, mal):
    vag = []
    while mal is not None:
        vag.append(mal)
        mal = foralder[mal]
    return vag[::-1]


def _lagg_till_loopar(dorrar, pos, bredd, hojd, rng, sida_a, sida_b):
    """Gör några väggar till passager, men aldrig över den låsta dörren."""
    kandidater = []
    for rum, (rad, kol) in pos.items():
        for riktning in ("S", "Ö"):
            dr, dk = RIKTNINGAR[riktning]
            nr, nk = rad + dr, kol + dk
            if not (0 <= nr < hojd and 0 <= nk < bredd):
                continue
            granne = rum_id(nr, nk, bredd)
            if granne in dorrar[rum]:
                continue
            if sida_a is not None and ((rum in sida_a) != (granne in sida_a)):
                continue
            kandidater.append((rum, riktning, granne))
    for rum, riktning, granne in rng.sample(kandidater, round(len(kandidater) * ANDEL_LOOPAR)):
        dorrar[rum][riktning] = granne
        dorrar[granne][MOTSATT[riktning]] = rum


def _rumsinfo(rum_lista, rng):
    pool = list(RUMSNAMN)
    rng.shuffle(pool)
    pool = pool * math.ceil(len(rum_lista) / len(pool))
    return dict(zip(sorted(rum_lista), pool))


def generera(bredd=BREDD, hojd=HOJD, rng=None):
    rng = rng or random.Random()
    dorrar = _bygg_trad(bredd, hojd, rng)
    pos = {rum_id(r, k, bredd): (r, k) for r in range(hojd) for k in range(bredd)}
    start = rum_id(0, 0, bredd)

    avstand, foralder = bfs(dorrar, start)
    utgang = max(avstand, key=lambda r: (avstand[r], -r))
    vag = vag_till(foralder, utgang)

    last_kant = None
    sida_a = sida_b = None
    if len(vag) >= 4:  # minst tre korridorer, så båda sidor får plats för saker
        i = rng.randrange(1, len(vag) - 2)
        last_kant = kant(vag[i], vag[i + 1])
        sida_a = set(bfs(dorrar, start, sparrad=last_kant)[0])
        sida_b = set(dorrar) - sida_a

    _lagg_till_loopar(dorrar, pos, bredd, hojd, rng, sida_a, sida_b)

    foremal = {rum: [] for rum in dorrar}
    morka = set()
    if last_kant:
        a_rum = sorted(sida_a - {start}) or [start]
        b_rum = sorted(sida_b - {utgang})
        foremal[rng.choice(a_rum)].append(ROD_NYCKEL)
        foremal[rng.choice(a_rum)].append(LAMPA)
        morka = set(rng.sample(b_rum, min(2, len(b_rum))))
        foremal[rng.choice(sorted(morka))].append(GULD_NYCKEL)
    else:
        kvar = sorted(set(dorrar) - {start, utgang}) or [start]
        foremal[rng.choice(kvar)].append(GULD_NYCKEL)

    return Labyrint(
        bredd=bredd,
        hojd=hojd,
        dorrar=dorrar,
        pos=pos,
        start=start,
        utgang=utgang,
        last_kant=last_kant,
        foremal=foremal,
        morka=morka,
        rumsinfo=_rumsinfo(list(dorrar), rng),
    )
