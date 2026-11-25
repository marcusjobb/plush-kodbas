"""Logiken. Här bor reglerna: summor, budgetar, varningar. Pratar bara med repository-objektet."""
from decimal import ROUND_HALF_UP, Decimal

from models import (BudgetLevel, BudgetStatus, Category, CategoryTotal, Member,
                    MonthlyOverview, Transaction)

OTHER = "Övrigt"
MAX_MEMBERS = 5
MONTH_NAMES = ["januari", "februari", "mars", "april", "maj", "juni", "juli",
               "augusti", "september", "oktober", "november", "december"]


def format_money(amount: Decimal) -> str:
    """1249.5 blir "1 249,50 kr". Tecknet visas bara för negativa belopp."""
    rounded = Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    text = f"{rounded:,.2f}".replace(",", " ").replace(".", ",")
    return f"{text} kr"


class CategoryService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def get_all(self) -> list[Category]:
        return self._repo.get_categories()

    def add(self, name: str) -> Category:
        name = (name or "").strip()
        if not name:
            raise ValueError("Kategorin måste ha ett namn.")
        if any(c.name.lower() == name.lower() for c in self._repo.get_categories()):
            raise ValueError(f'Kategorin "{name}" finns redan.')
        return self._repo.add_category(name)

    def delete(self, category_id: int) -> Category:
        category = self._repo.get_category(category_id)
        if category is None:
            raise ValueError("Kategorin finns inte.")
        if category.name == OTHER:
            raise ValueError(f'Kategorin "{OTHER}" kan inte tas bort.')
        self._repo.move_transactions(category.name, OTHER)
        self._repo.delete_category(category_id)
        return category


class HouseholdService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def add_member(self, member: Member) -> Member:
        if not member.first_name.strip():
            raise ValueError("Medlemmen måste ha ett förnamn.")
        if len(self._repo.get_members()) >= MAX_MEMBERS:
            raise ValueError(f"Ett hushåll kan ha högst {MAX_MEMBERS} medlemmar.")
        return self._repo.add_member(member)


class OverviewService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def get_overview(self, year: int, month: int) -> MonthlyOverview:
        transactions = self._repo.get_transactions_for_month(year, month)
        income = sum((t.amount for t in transactions if not t.is_expense), Decimal(0))
        expenses = -sum((t.amount for t in transactions if t.is_expense), Decimal(0))
        totals = spent_per_category(transactions)
        category_totals = [CategoryTotal(name, amount)
                           for name, amount in sorted(totals.items(), key=lambda item: -item[1])]
        return MonthlyOverview(year, month, income, expenses, income - expenses, category_totals)


def spent_per_category(transactions: list[Transaction]) -> dict[str, Decimal]:
    """Utgifter per kategori som positiva tal."""
    totals: dict[str, Decimal] = {}
    for t in transactions:
        if t.is_expense:
            totals[t.category] = totals.get(t.category, Decimal(0)) - t.amount
    return totals


def level_for(spent: Decimal, budget: Decimal) -> BudgetLevel:
    if spent >= budget:
        return BudgetLevel.EXCEEDED
    if spent * 100 >= budget * 80:
        return BudgetLevel.WARNING
    return BudgetLevel.OK


class BudgetService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def get_status(self, year: int, month: int) -> list[BudgetStatus]:
        budgets = self._repo.get_budgets_for_month(year, month)
        spent = spent_per_category(self._repo.get_transactions_for_month(year, month))
        statuses = []
        for category in self._repo.get_categories():
            if category.id not in budgets:
                continue
            budget = budgets[category.id]
            used = spent.get(category.name, Decimal(0))
            statuses.append(BudgetStatus(category.id, category.name, budget, used,
                                         int(used * 100 // budget), level_for(used, budget)))
        return statuses

    def set_budget(self, category_id: int, year: int, month: int, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Budgeten måste vara större än 0.")
        if self._repo.get_category(category_id) is None:
            raise ValueError("Kategorin finns inte.")
        self._repo.set_budget(category_id, year, month, amount)


class WarningService:
    """Varnar när en kategori når 80 % och 100 % av månadens budget. Samma varning visas bara en gång per månad."""

    def __init__(self, budgets: BudgetService) -> None:
        self._budgets = budgets
        self._shown: set[tuple[str, int, int, BudgetLevel]] = set()

    def check(self, transaction: Transaction) -> list[str]:
        if not transaction.is_expense:
            return []
        year, month = transaction.date.year, transaction.date.month
        for status in self._budgets.get_status(year, month):
            if status.category_name != transaction.category or status.level == BudgetLevel.OK:
                continue
            key = (status.category_name, year, month, status.level)
            if key in self._shown:
                return []
            self._shown.add(key)
            if status.level == BudgetLevel.EXCEEDED:
                return [f"{status.category_name} är över budgeten."]
            return [f"{status.category_name} är på {status.percent} % av budgeten."]
        return []
