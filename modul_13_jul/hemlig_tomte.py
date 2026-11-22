"""Hemlig tomte i konsolen. Kör med: python hemlig_tomte.py

Lägg in deltagare, lägg ev. in par som inte får dra varandra, lotta, och låt sedan var och en titta i
hemlighet vem hen ska ge till. Använd påhittade namn när du provar.
"""
import os
import random

import hemlig_tomte_logic as logic


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def add_person(names):
    name = input("Namn: ").strip()
    if not name:
        print("Namnet får inte vara tomt")
    elif name in names:
        print("Det namnet finns redan")
    else:
        names.append(name)
        print(f"Lade till {name}. Nu är ni {len(names)}.")


def add_pair(names, forbidden):
    first = input("Första personen: ").strip()
    second = input("Andra personen: ").strip()
    if first in names and second in names and first != second:
        forbidden.append((first, second))
        print(f"{first} och {second} får inte dra varandra.")
    else:
        print("Båda måste finnas i listan, och vara olika personer.")


def run_draw(names, forbidden):
    try:
        result = logic.draw(names, random.Random(), forbidden)
    except ValueError as error:
        print(f"Det gick inte: {error}")
        return None
    print("Lottat! Välj 'Titta i hemlighet' så att var och en kan se sin mottagare.")
    return result


def peek(result):
    if not result:
        print("Lotta först.")
        return
    name = input("Vem är du? ").strip()
    if name not in result:
        print("Det namnet finns inte i lottningen.")
        return
    print(f"\n{name}, du ska ge present till: {result[name]}")
    input("\nTryck Enter när du har läst. Skärmen rensas då.")
    clear_screen()


def show_the_surprise():
    print("\nHur stor andel av helt slumpade lottningar blir giltiga (ingen drar sig själv)?")
    rng = random.Random(24)
    for n in (3, 4, 5, 10, 50):
        share = logic.share_valid_random_shuffles(n, 20000, rng)
        print(f"  {n:>2} personer: {share:6.1%}")
    print("Nästan samma andel oavsett hur många ni är. Ungefär 36,8 %, alltså 1/e. Varför? Fråga ett AI-verktyg,")
    print("och kontrollera förklaringen själv med penna och papper.")


def main():
    names, forbidden, result = [], [], None
    while True:
        print(f"\n--- Hemlig tomte --- ({len(names)} deltagare)")
        print("1. Lägg till person\n2. Lägg till par som inte får dra varandra\n3. Lotta")
        print("4. Titta i hemlighet\n5. Slumpa och hoppas (matte)\n0. Avsluta")
        choice = input("Val: ").strip()
        if choice == "1":
            add_person(names)
        elif choice == "2":
            add_pair(names, forbidden)
        elif choice == "3":
            result = run_draw(names, forbidden) or result
        elif choice == "4":
            peek(result)
        elif choice == "5":
            show_the_surprise()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
