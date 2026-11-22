"""Ett litet menyprogram så att du kan prova fakturorna för hand. Kör med: python fakturameny.py"""
from datetime import date

from fakturor import berakna_faktura


def read_int(prompt: str) -> int:
    while True:
        text = input(prompt).strip()
        if text.isdigit():
            return int(text)
        print("Skriv ett heltal")


def read_date(prompt: str):
    while True:
        text = input(prompt).strip()
        if not text:
            return None
        try:
            return date.fromisoformat(text)
        except ValueError:
            print("Skriv datum som ÅÅÅÅ-MM-DD, eller lämna tomt")


def main() -> None:
    print("--- Fakturaräknaren ---")
    lines = []
    while True:
        quantity = read_int("Antal (0 när du är klar): ")
        if quantity == 0:
            break
        lines.append((quantity, read_int("À-pris i kronor: ")))
    customer = input("Kundtyp (privat/foretag/foerening): ").strip()
    due = read_date("Förfallodatum: ")
    paid = read_date("Betaldatum (tomt = ej betald): ")
    try:
        print(f"Att betala: {berakna_faktura(lines, customer, due, paid)} kr")
    except ValueError as error:
        print(f"Fel: {error}")


if __name__ == "__main__":
    main()
