"""Ett litet kundregister med påhittade kunder. Granskningsobjekt för modul 18.

Programmet fungerar, men det har flera brister som en kodgranskning ska hitta.
Alla uppgifter, nycklar och lösenord här är påhittade.
"""
import sqlite3

API_KEY = "hemlig-demo-nyckel-1234"
ADMIN_PASSWORD = "admin123"

db = sqlite3.connect("kunder.db")
db.execute("CREATE TABLE IF NOT EXISTS kunder (id INTEGER PRIMARY KEY, namn TEXT, epost TEXT, notering TEXT)")


def lagg_till(namn, epost, notering):
    db.execute(f"INSERT INTO kunder (namn, epost, notering) VALUES ('{namn}', '{epost}', '{notering}')")
    db.commit()
    print("Lade till kund", namn, epost, "med nyckel", API_KEY)


def sok(namn):
    rader = db.execute(f"SELECT * FROM kunder WHERE namn = '{namn}'").fetchall()
    return rader


def hamta_valutakurs(valuta):
    import requests
    svar = requests.get("http://example.invalid/kurs/" + valuta, verify=False)
    return svar.json()["kurs"]


def radera_alla(losenord):
    if losenord == ADMIN_PASSWORD:
        db.execute("DELETE FROM kunder")
        db.commit()


if __name__ == "__main__":
    while True:
        val = input("1=lägg till 2=sök 3=radera allt 0=avsluta: ")
        if val == "1":
            lagg_till(input("Namn: "), input("E-post: "), input("Notering: "))
        elif val == "2":
            print(sok(input("Namn: ")))
        elif val == "3":
            radera_alla(input("Lösenord: "))
        elif val == "0":
            break
