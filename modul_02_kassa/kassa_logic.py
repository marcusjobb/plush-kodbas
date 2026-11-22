"""Logiken för kassan. Ingen input eller print här, så att den går att testa."""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

VALID_VAT_RATES = (25, 12, 6)


@dataclass(frozen=True)
class Item:
    name: str
    price_ex_vat: Decimal
    vat_rate: int


def money(value) -> Decimal:
    """Avrundar till två decimaler (hel öre)."""
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def vat_amount(item: Item) -> Decimal:
    return money(item.price_ex_vat * item.vat_rate / 100)


def total_ex_vat(items: list[Item]) -> Decimal:
    return money(sum((item.price_ex_vat for item in items), Decimal("0")))


def total_incl_vat(items: list[Item]) -> Decimal:
    return money(sum((item.price_ex_vat + vat_amount(item) for item in items), Decimal("0")))
