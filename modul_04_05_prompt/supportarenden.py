"""Supportärenden i konsolen. Kör med: python supportarenden.py

Programmet är litet med flit. Det saknar prioritet, sparning till fil och sökning.
Det är de sakerna du ska be ditt AI-verktyg lägga till, med olika slags promptar.
"""
from datetime import date

tickets: list[dict] = []


def add_ticket() -> None:
    title = input("Rubrik: ").strip()
    if not title:
        print("Rubriken får inte vara tom")
        return
    customer = input("Kund (påhittat namn): ").strip()
    tickets.append({
        "id": len(tickets) + 1,
        "title": title,
        "customer": customer,
        "created": date.today().isoformat(),
        "status": "öppen",
    })
    print(f"Skapade ärende {tickets[-1]['id']}")


def list_tickets() -> None:
    if not tickets:
        print("Inga ärenden än")
        return
    for t in tickets:
        print(f"#{t['id']} [{t['status']}] {t['title']} ({t['customer']}, {t['created']})")


def close_ticket() -> None:
    text = input("Vilket ärendenummer? ").strip()
    for t in tickets:
        if str(t["id"]) == text:
            t["status"] = "stängd"
            print(f"Stängde #{t['id']}")
            return
    print("Hittade inget sådant ärende")


def main() -> None:
    actions = {"1": add_ticket, "2": list_tickets, "3": close_ticket}
    while True:
        print("\n1. Nytt ärende  2. Lista  3. Stäng ärende  0. Avsluta")
        choice = input("Val: ").strip()
        if choice == "0":
            break
        actions.get(choice, lambda: print("Det valet finns inte"))()


if __name__ == "__main__":
    main()
