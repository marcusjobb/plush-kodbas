def vat_breakdown(items):
    """Returnerar momsbelopp per momssats, t.ex. {25: 25.0, 12: 6.0}."""
    breakdown = {}
    for name, price, rate in items:
        breakdown[rate] = price * rate / 100
    return breakdown
