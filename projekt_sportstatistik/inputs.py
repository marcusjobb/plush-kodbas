"""Tolkar text från formulär. Fel blir ValueError med ett meddelande på svenska."""
from datetime import date


def parse_int(text: str, minimum: int, maximum: int, what: str) -> int:
    try:
        value = int((text or "").strip())
    except ValueError:
        raise ValueError(f"{what} måste vara ett heltal mellan {minimum} och {maximum}.") from None
    if not minimum <= value <= maximum:
        raise ValueError(f"{what} måste vara ett heltal mellan {minimum} och {maximum}.")
    return value


def parse_date(text: str, what: str = "Datumet") -> date:
    try:
        return date.fromisoformat((text or "").strip())
    except ValueError:
        raise ValueError(f"{what} måste skrivas som ÅÅÅÅ-MM-DD.") from None
