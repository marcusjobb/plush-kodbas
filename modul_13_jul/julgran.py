"""En blinkande julgran i terminalen. Kör med: python julgran.py   (avsluta med Ctrl+C)

Flaggor:
    --hojd 12      granens höjd, 3 till 16 (så att den ryms i en konsol på 20 rader)
    --en-bild      skriv ut en enda bild och avsluta, utan animation
"""
import argparse
import random
import time

GUL = "\033[1;33m"
GRON = "\033[32m"
BRUN = "\033[33m"
NOLLA = "\033[0m"
LJUSFARGER = ["\033[91m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]  # röd, gul, blå, lila, cyan

MIN_HOJD, MAX_HOJD = 3, 16


def bygg_gran(hojd, rng):
    """Returnerar granen som en lista med rader. Varje anrop ger nya slumpade ljus."""
    rader = [" " * (hojd - 1) + f"{GUL}*{NOLLA}"]
    for i in range(1, hojd):
        grenar = []
        for _ in range(2 * i + 1):
            if rng.random() < 0.18:
                grenar.append(f"{rng.choice(LJUSFARGER)}o{NOLLA}")
            else:
                grenar.append(f"{GRON}^{NOLLA}")
        rader.append(" " * (hojd - 1 - i) + "".join(grenar))
    stam = " " * (hojd - 2) + f"{BRUN}|||{NOLLA}"
    rader += [stam, stam]
    rader.append(" " * max(0, hojd - 4) + "God Jul!")
    return rader


def main():
    parser = argparse.ArgumentParser(description="En blinkande julgran")
    parser.add_argument("--hojd", type=int, default=12)
    parser.add_argument("--en-bild", action="store_true")
    args = parser.parse_args()
    if not MIN_HOJD <= args.hojd <= MAX_HOJD:
        parser.error(f"höjden måste vara mellan {MIN_HOJD} och {MAX_HOJD}")

    rng = random.Random()
    if args.en_bild:
        print("\n".join(bygg_gran(args.hojd, rng)))
        return
    print("\033[2J", end="")  # rensa skärmen en gång
    try:
        while True:
            print("\033[H" + "\n".join(bygg_gran(args.hojd, rng)), flush=True)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"{NOLLA}\nGod Jul!")


if __name__ == "__main__":
    main()
