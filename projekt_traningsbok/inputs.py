"""Tolkar text från formulär. Fel blir ValueError med ett meddelande på svenska."""
from datetime import date
from decimal import Decimal, InvalidOperation


def parse_decimal(text: str, what: str = "Värdet") -> Decimal:
    """Godkänner både 62,5 och 62.5."""
    cleaned = (text or "").strip().replace(" ", "").replace(",", ".")
    try:
        value = Decimal(cleaned)
    except InvalidOperation:
        raise ValueError(f'"{text}" är ingen giltig siffra för {what.lower()}. Skriv till exempel 62,5.') from None
    if not value.is_finite():
        raise ValueError(f'"{text}" är ingen giltig siffra för {what.lower()}. Skriv till exempel 62,5.')
    return value


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
