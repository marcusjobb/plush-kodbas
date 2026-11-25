"""Modellerna: vad programmet handlar om. Inga beroenden, bara data."""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum


class BudgetLevel(Enum):
    OK = "ok"              # under 80 % av budgeten
    WARNING = "warning"    # 80 % eller mer
    EXCEEDED = "exceeded"  # 100 % eller mer


@dataclass
class Household:
    id: int
    name: str


@dataclass
class Member:
    first_name: str
    last_name: str = ""
    birth_date: date | None = None
    hair_color: str = ""
    height_cm: int | None = None
    religion: str = ""
    id: int = 0


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Transaction:
    """En utgift (negativt belopp) eller en inkomst (positivt belopp)."""
    amount: Decimal
    date: date
    category: str
    note: str = ""
    id: int = 0

    @property
    def is_expense(self) -> bool:
        return self.amount < 0


@dataclass
class BudgetStatus:
    category_id: int
    category_name: str
    budget_amount: Decimal
    spent: Decimal
    percent: int
    level: BudgetLevel


@dataclass
class CategoryTotal:
    category_name: str
    amount: Decimal


@dataclass
class MonthlyOverview:
    year: int
    month: int
    total_income: Decimal
    total_expenses: Decimal  # positivt tal
    balance: Decimal
    category_totals: list[CategoryTotal] = field(default_factory=list)
