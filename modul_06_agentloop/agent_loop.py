"""En agentloop du kan titta på. Kör med: python agent_loop.py

Det här är INGEN AI. Agentens "tänkande" är vanliga if-satser i funktionen decide().
Poängen är att se strukturen som alla agenter har: tänk, använd ett verktyg, observera, upprepa.
För att göra den på riktigt byter du ut decide() mot ett anrop till en språkmodell.
"""
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).parent / "bugg_projekt"
MAX_STEPS = 8

# Det enda agenten "kan" laga: ett byte av en rad mot en annan.
FIX_RULES = [
    ("breakdown[rate] = price * rate / 100",
     "breakdown[rate] = breakdown.get(rate, 0) + price * rate / 100"),
]


# ---- Verktygen: det här är allt agenten kan göra i världen ----

def run_tests() -> str:
    result = subprocess.run([sys.executable, "-m", "unittest", "-q"], cwd=PROJECT,
                            capture_output=True, text=True, timeout=30)
    return (result.stdout + result.stderr).strip()


def list_files() -> str:
    return "\n".join(sorted(p.name for p in PROJECT.glob("*.py")))


def read_file(name: str) -> str:
    return (PROJECT / name).read_text(encoding="utf-8")


def write_file(name: str, content: str) -> str:
    (PROJECT / name).write_text(content, encoding="utf-8")
    return f"Skrev {len(content)} tecken till {name}"


TOOLS = {"run_tests": run_tests, "list_files": list_files,
         "read_file": read_file, "write_file": write_file}


# ---- "Hjärnan": byt ut den här funktionen mot en språkmodell ----

def decide(history: list[tuple]) -> tuple | None:
    """Tittar på vad som hänt och väljer nästa steg. Returnerar (tanke, verktyg, argument) eller None."""
    if not history:
        return "Jag vet inte om något är trasigt. Jag kör testerna först.", "run_tests", {}

    tool, args, observation = history[-1]
    last_line = observation.splitlines()[-1] if observation else ""

    if tool == "run_tests" and last_line == "OK":
        return None
    if tool == "run_tests":
        return "Testerna faller. Jag tittar vilka filer som finns.", "list_files", {}
    if tool == "list_files":
        source = next(n for n in observation.splitlines() if not n.startswith("test_"))
        return f"Jag läser koden i {source}, inte testerna.", "read_file", {"name": source}
    if tool == "read_file":
        for old, new in FIX_RULES:
            if old in observation:
                return "Raden skriver över värdet i stället för att lägga till. Jag ändrar den.", \
                    "write_file", {"name": args["name"], "content": observation.replace(old, new)}
        return "Jag hittar inget jag vet hur man lagar.", "stop", {}
    if tool == "write_file":
        return "Jag har ändrat koden. Nu kontrollerar jag med testerna.", "run_tests", {}
    return None


# ---- Loopen ----

def approved(mode: str, tool: str) -> bool:
    if mode == "alla" or (mode == "skriv" and tool == "write_file"):
        return input("   Godkänn det här steget? (j/n): ").strip().lower() == "j"
    return True


def run_agent(mode: str) -> None:
    history: list[tuple] = []
    for step in range(1, MAX_STEPS + 1):
        decision = decide(history)
        if decision is None:
            print("\nAgenten är klar.")
            return
        thought, tool, args = decision
        print(f"\nSteg {step}")
        print(f"  Tanke:     {thought}")
        if tool == "stop":
            print("\nAgenten gav upp. Den hade inga fler idéer.")
            return
        print(f"  Verktyg:   {tool}({', '.join(args)})")
        if not approved(mode, tool):
            print("  Nekat. Agenten stannar.")
            return
        observation = TOOLS[tool](**args)
        shown = observation.splitlines()
        print("  Observerar:")
        for line in shown[:8]:
            print(f"    {line}")
        if len(shown) > 8:
            print(f"    ... ({len(shown) - 8} rader till)")
        history.append((tool, args, observation))
    print(f"\nStoppade efter {MAX_STEPS} steg. En agent behöver alltid en gräns.")


def reset_bug() -> None:
    shutil.copy(PROJECT / "vat.py.original", PROJECT / "vat.py")
    print("Buggen är tillbaka i vat.py")


def main() -> None:
    while True:
        print("\n--- Agentloopen ---")
        print("1. Kör agenten, godkänn varje steg")
        print("2. Kör agenten, godkänn bara när den skriver till filer")
        print("3. Kör agenten helt själv")
        print("4. Återställ buggen")
        print("0. Avsluta")
        choice = input("Val: ").strip()
        if choice == "1":
            run_agent("alla")
        elif choice == "2":
            run_agent("skriv")
        elif choice == "3":
            run_agent("auto")
        elif choice == "4":
            reset_bug()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
