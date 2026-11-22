"""En agent som får en mapp och ett mål. Kör med: python mappagent.py

Liksom i modul 06 är det ingen AI. Det här exemplet handlar om BEHÖRIGHETER: agenten kan bara göra
det du har gett den rätt att göra, och varje steg visas innan det körs.
"""
from pathlib import Path

FOLDER = Path(__file__).parent / "kursutvarderingar"
REPORT = Path(__file__).parent / "rapport.md"


class PermissionDenied(Exception):
    pass


class Tools:
    """Verktygen agenten får använda. Behörigheten avgör vilka som fungerar."""

    def __init__(self, can_write: bool):
        self.can_write = can_write

    def list_files(self) -> list[Path]:
        return sorted(FOLDER.glob("*.txt"))

    def read_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def write_report(self, text: str) -> None:
        if not self.can_write:
            raise PermissionDenied("Agenten har ingen skrivrätt")
        REPORT.write_text(text, encoding="utf-8")


def parse_rating(text: str) -> int | None:
    for line in text.splitlines():
        if line.startswith("Betyg:"):
            value = line.removeprefix("Betyg:").strip()
            return int(value) if value.isdigit() and 1 <= int(value) <= 5 else None
    return None


def step(description: str) -> None:
    print(f"  -> {description}")
    if input("     Godkänn? (j/n): ").strip().lower() != "j":
        raise PermissionDenied("Du nekade steget")


def goal_count_and_ratings(tools: Tools) -> None:
    step("Lista filerna i mappen")
    files = tools.list_files()
    ratings, skipped = [], []
    for path in files:
        step(f"Läs {path.name}")
        rating = parse_rating(tools.read_file(path))
        (ratings if rating else skipped).append(rating or path.name)
    print(f"\nFiler: {len(files)}. Med betyg: {len(ratings)}. Förekommande betyg: {sorted(set(ratings))}")
    if skipped:
        print(f"Kunde inte läsa betyg i: {', '.join(skipped)}")


def goal_write_report(tools: Tools) -> None:
    step("Lista filerna i mappen")
    ratings = []
    for path in tools.list_files():
        step(f"Läs {path.name}")
        rating = parse_rating(tools.read_file(path))
        if rating:
            ratings.append(rating)
    average = sum(ratings) / len(ratings)
    step(f"Skriv rapport.md ({len(ratings)} betyg, snitt {average:.1f})")
    tools.write_report(f"# Sammanfattning\n\nAntal betyg: {len(ratings)}\nSnittbetyg: {average:.1f}\n")
    print("\nRapporten är skriven till rapport.md")


def main() -> None:
    can_write = False
    goals = {"1": ("Hur många utvärderingar finns och vilka betyg förekommer?", goal_count_and_ratings),
             "2": ("Skriv en rapport med snittbetyg", goal_write_report)}
    while True:
        print(f"\n--- Mappagenten --- (skrivrätt: {'ja' if can_write else 'nej'})")
        for key, (text, _) in goals.items():
            print(f"{key}. Mål: {text}")
        print("3. Ändra behörighet")
        print("0. Avsluta")
        choice = input("Val: ").strip()
        if choice == "0":
            break
        if choice == "3":
            can_write = not can_write
            continue
        if choice in goals:
            try:
                goals[choice][1](Tools(can_write))
            except PermissionDenied as error:
                print(f"\nAgenten stoppades: {error}")


if __name__ == "__main__":
    main()
