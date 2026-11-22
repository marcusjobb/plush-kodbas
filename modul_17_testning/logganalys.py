"""Analyserar en loggfil. Kör med: python logganalys.py data/app.log [--level ERROR]"""
import argparse
from collections import Counter

LEVELS = ("INFO", "WARNING", "ERROR")


def parse_line(line: str) -> dict | None:
    """Delar en rad i datum, tid, nivå, källa och meddelande. Returnerar None om raden inte är en loggrad."""
    parts = line.strip().split(" ", 4)
    if len(parts) < 5 or parts[2] not in LEVELS:
        return None
    source = parts[3].rstrip(":")
    return {"date": parts[0], "time": parts[1], "level": parts[2], "source": source, "message": parts[4]}


def read_log(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as file:
        entries = [parse_line(line) for line in file]
    return [entry for entry in entries if entry]


def count_by_level(entries: list[dict]) -> Counter:
    return Counter(entry["level"] for entry in entries)


def top_errors(entries: list[dict], limit: int = 3) -> list[tuple[str, int]]:
    errors = Counter(e["message"].split(",")[0] for e in entries if e["level"] == "ERROR")
    return errors.most_common(limit)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analysera en loggfil")
    parser.add_argument("path", help="Sökväg till loggfilen")
    parser.add_argument("--level", choices=LEVELS, help="Visa bara rader med den här nivån")
    args = parser.parse_args()

    entries = read_log(args.path)
    if args.level:
        for entry in entries:
            if entry["level"] == args.level:
                print(f"{entry['date']} {entry['time']} {entry['source']}: {entry['message']}")
        return
    print("Antal per nivå:")
    for level, count in count_by_level(entries).items():
        print(f"  {level}: {count}")
    print("Vanligaste felen:")
    for message, count in top_errors(entries):
        print(f"  {count} x {message}")


if __name__ == "__main__":
    main()
