"""Fakturaberäkning. Funktionen berakna_faktura fungerar för det mesta, men den är rörig,
den saknar tester, och det finns minst två fel i den. Syftet är att du ska skydda den med tester
innan du rör den, och sedan felsöka och refaktorisera med AI-hjälp.
"""
from datetime import date


def berakna_faktura(rader, kund_typ, forfallodatum, betaldatum, moms=25):
    # rader: lista med (antal, a_pris). kund_typ: "privat", "foretag" eller "foerening".
    summa = 0
    for r in rader:
        summa = summa + r[0] * r[1]
    # mängdrabatt: tio varor eller fler ger 5 %
    antal = 0
    for r in rader:
        antal = antal + r[0]
    if antal > 10:
        summa = summa * 0.95
    if kund_typ == "foretag":
        if summa > 10000:
            summa = summa * 0.9
        else:
            if summa > 5000:
                summa = summa * 0.95
    elif kund_typ == "foerening":
        summa = summa * 0.9
    else:
        if kund_typ != "privat":
            raise ValueError("Okänd kundtyp: " + kund_typ)
    # moms
    summa = summa * (1 + moms / 100)
    # dröjsmålsavgift: 2 % per påbörjad månad efter förfallodatum
    if betaldatum is not None:
        if betaldatum > forfallodatum:
            dagar = (betaldatum - forfallodatum).days
            manader = dagar // 30
            if manader > 0:
                summa = summa * (1 + 0.02 * manader)
    return round(summa, 2)


def idag() -> date:
    return date.today()
