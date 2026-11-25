"""Datalagret. Allt som sparas och läses går genom den här klassen.

InMemoryRepository är en låtsasdatabas: data ligger i listor och försvinner när programmet stängs.
Resten av programmet (services.py och app.py) anropar bara metoderna nedan, så den som vill ha en riktig
databas skriver en ny klass med samma metoder och byter en rad i app.py.
"""
from datetime import date
from decimal import Decimal

from models import Category, Household, Member, Transaction

DEFAULT_CATEGORIES = ["Boende", "Mat", "Transport", "El och internet", "Nöje", "Hälsa", "Övrigt"]


class InMemoryRepository:
    def __init__(self, seed: bool = True) -> None:
        self._household = Household(id=1, name="Familjen Berg")
        self._members: list[Member] = []
        self._transactions: list[Transaction] = []
        self._categories: list[Category] = []
        self._budgets: dict[tuple[int, int, int], Decimal] = {}  # (kategori-id, år, månad) -> belopp
        self._next_member_id = 1
        self._next_transaction_id = 1
        self._next_category_id = 1
        for name in DEFAULT_CATEGORIES:
            self.add_category(name)
        if seed:
            self._seed()

    # --- Hushåll och medlemmar ---

    def get_household(self) -> Household:
        return self._household

    def get_members(self) -> list[Member]:
        return list(self._members)

    def add_member(self, member: Member) -> Member:
        member.id = self._next_member_id
        self._next_member_id += 1
        self._members.append(member)
        return member

    # --- Transaktioner ---

    def get_transactions_for_month(self, year: int, month: int) -> list[Transaction]:
        found = [t for t in self._transactions if t.date.year == year and t.date.month == month]
        return sorted(found, key=lambda t: (t.date, t.id))

    def get_transaction(self, transaction_id: int) -> Transaction | None:
        return next((t for t in self._transactions if t.id == transaction_id), None)

    def add_transaction(self, transaction: Transaction) -> Transaction:
        transaction.id = self._next_transaction_id
        self._next_transaction_id += 1
        self._transactions.append(transaction)
        return transaction

    def delete_transaction(self, transaction_id: int) -> None:
        self._transactions = [t for t in self._transactions if t.id != transaction_id]

    def move_transactions(self, from_category: str, to_category: str) -> None:
        for transaction in self._transactions:
            if transaction.category == from_category:
                transaction.category = to_category

    # --- Kategorier ---

    def get_categories(self) -> list[Category]:
        return list(self._categories)

    def get_category(self, category_id: int) -> Category | None:
        return next((c for c in self._categories if c.id == category_id), None)

    def add_category(self, name: str) -> Category:
        category = Category(id=self._next_category_id, name=name)
        self._next_category_id += 1
        self._categories.append(category)
        return category

    def delete_category(self, category_id: int) -> None:
        self._categories = [c for c in self._categories if c.id != category_id]
        self._budgets = {key: amount for key, amount in self._budgets.items() if key[0] != category_id}

    # --- Budgetar ---

    def get_budgets_for_month(self, year: int, month: int) -> dict[int, Decimal]:
        """Kategori-id -> budget, för de kategorier som har en budget den månaden."""
        return {cat_id: amount for (cat_id, y, m), amount in self._budgets.items() if (y, m) == (year, month)}

    def set_budget(self, category_id: int, year: int, month: int, amount: Decimal) -> None:
        self._budgets[(category_id, year, month)] = amount

    # --- Exempeldata. Alla namn och belopp är påhittade. ---

    def _seed(self) -> None:
        self.add_member(Member(first_name="Kim", last_name="Berg"))
        self.add_member(Member(first_name="Alex", last_name="Berg"))
        self.add_category("Lön")

        rows = [
            (-100, date(2026, 10, 31), "Mat", "Fika"),  # sista oktober: hör till oktober
            (28500, date(2026, 11, 1), "Lön", "Lön november"),
            (-9800, date(2026, 11, 1), "Boende", "Hyra"),
            (-899, date(2026, 11, 5), "El och internet", "Bredband och el"),
            (-1000, date(2026, 11, 8), "Mat", "Storhandling"),
            (Decimal("-249.50"), date(2026, 11, 12), "Mat", "ICA"),
            (-790, date(2026, 11, 14), "Nöje", "Konsertbiljetter"),
            (-450, date(2026, 11, 18), "Transport", "Busskort"),
            (-350, date(2026, 11, 20), "Hälsa", ""),
        ]
        for amount, day, category, note in rows:
            self.add_transaction(Transaction(Decimal(amount), day, category, note))

        budgets = {"Boende": 12000, "Mat": 4000, "Transport": 600, "El och internet": 800, "Nöje": 1000}
        by_name = {c.name: c.id for c in self._categories}
        for name, amount in budgets.items():
            self.set_budget(by_name[name], 2026, 11, Decimal(amount))
