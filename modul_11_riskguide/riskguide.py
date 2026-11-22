"""Beslutsguide för risknivå enligt EU:s AI-förordning. Kör med: python riskguide.py

Frågorna ligger i fragor.json. Lägg till eller ändra där, utan att röra koden.
"""
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
SAVED = HERE / "bedomningar.json"


def load_rules() -> dict:
    return json.loads((HERE / "fragor.json").read_text(encoding="utf-8"))


def ask_yes_no(question: str) -> bool:
    print(f"\n{question}")
    while True:
        answer = input("(j/n): ").strip().lower()
        if answer in ("j", "n"):
            return answer == "j"


def choose_role(rules: dict) -> str:
    print("\nVad är din roll?")
    for role in rules["roles"]:
        print(f"{role['key']}. {role['text']}")
    keys = {role["key"]: role["text"] for role in rules["roles"]}
    while True:
        choice = input("Val: ").strip()
        if choice in keys:
            return keys[choice]


def classify(rules: dict) -> dict:
    """Går igenom stegen uppifrån och stannar vid första "ja"."""
    for step in rules["steps"]:
        if ask_yes_no(step["question"]):
            return {"level": step["level"], "basis": step["basis"]}
    return rules["default"]


def assess(rules: dict) -> None:
    name = input("Vad heter systemet? (påhittat namn): ").strip() or "Namnlöst"
    role = choose_role(rules)
    result = classify(rules)
    print(f"\n=== {name}: {result['level']} ===")
    print(f"Grund: {result['basis']}")
    print(f"Roll: {role}")
    print(f"({rules['disclaimer']})")
    if input("\nSpara bedömningen? (j/n): ").strip().lower() == "j":
        save({"system": name, "role": role, "date": date.today().isoformat(), **result})


def save(entry: dict) -> None:
    entries = json.loads(SAVED.read_text(encoding="utf-8")) if SAVED.exists() else []
    entries.append(entry)
    SAVED.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Sparad i bedomningar.json")


def show_saved() -> None:
    if not SAVED.exists():
        print("Inga sparade bedömningar än")
        return
    for entry in json.loads(SAVED.read_text(encoding="utf-8")):
        print(f"{entry['date']}  {entry['system']}: {entry['level']} ({entry['basis']})")


def main() -> None:
    rules = load_rules()
    while True:
        print("\n--- Riskguiden ---\n1. Bedöm ett system\n2. Visa sparade\n0. Avsluta")
        choice = input("Val: ").strip()
        if choice == "1":
            assess(rules)
        elif choice == "2":
            show_saved()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
