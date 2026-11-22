"""Kassan: ett menyprogram i konsolen. Kör med: python kassa.py"""
from decimal import Decimal, InvalidOperation

import kassa_logic as logic


def read_price(prompt: str) -> Decimal:
    while True:
        text = input(prompt).strip().replace(",", ".")
        try:
            price = Decimal(text)
            if not price.is_finite() or price < 0:
                raise InvalidOperation
        except InvalidOperation:
            print("Skriv ett positivt tal, till exempel 49,90")
            continue
        return price


def read_vat_rate() -> int:
    options = "/".join(str(rate) for rate in logic.VALID_VAT_RATES)
    while True:
        text = input(f"Momssats ({options}): ").strip()
        if text.isdigit() and int(text) in logic.VALID_VAT_RATES:
            return int(text)
        print(f"Välj en av {options}")


def add_item(items: list[logic.Item]) -> None:
    name = input("Varunamn: ").strip()
    if not name:
        print("Namnet får inte vara tomt")
        return
    price = read_price("Pris exklusive moms: ")
    items.append(logic.Item(name, price, read_vat_rate()))
    print(f"Lade till {name}")


def remove_item(items: list[logic.Item]) -> None:
    if not items:
        print("Kassan är tom")
        return
    show_items(items)
    text = input("Vilket nummer vill du ta bort? ").strip()
    if text.isdigit() and 1 <= int(text) <= len(items):
        removed = items.pop(int(text) - 1)
        print(f"Tog bort {removed.name}")
    else:
        print("Ogiltigt nummer")


def show_items(items: list[logic.Item]) -> None:
    for number, item in enumerate(items, start=1):
        print(f"{number}. {item.name}  {item.price_ex_vat} kr + {item.vat_rate} % moms")


def show_receipt(items: list[logic.Item]) -> None:
    if not items:
        print("Inget att visa än")
        return
    show_items(items)
    print(f"Summa exkl. moms: {logic.total_ex_vat(items)} kr")
    print(f"Att betala:       {logic.total_incl_vat(items)} kr")


def main() -> None:
    items: list[logic.Item] = []
    actions = {
        "1": ("Lägg till vara", add_item),
        "2": ("Visa kvitto", show_receipt),
        "3": ("Ta bort vara", remove_item),
    }
    while True:
        print("\n--- Kassan ---")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("0. Avsluta")
        choice = input("Val: ").strip()
        if choice == "0":
            break
        if choice in actions:
            actions[choice][1](items)
        else:
            print("Det valet finns inte")


if __name__ == "__main__":
    main()
