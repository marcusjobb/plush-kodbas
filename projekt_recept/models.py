"""Modellerna: vad programmet handlar om. Inga beroenden, bara data."""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum


class LimitLevel(Enum):
    WARNING = 80    # 80 % av veckans gräns
    REACHED = 100   # 100 % av veckans gräns


@dataclass
class Category:
    id: int
    name: str
    weekly_limit: int | None = None  # högst så här många gånger per vecka i veckoplanen


@dataclass
class Chef:
    """Den som har skapat ett recept."""
    first_name: str
    last_name: str = ""
    birth_date: date | None = None
    hair_color: str = ""
    height_cm: int | None = None
    religion: str = ""
    id: int = 0


@dataclass
class Ingredient:
    name: str
    amount: Decimal
    unit: str


@dataclass
class Recipe:
    name: str
    servings: int
    ingredients: list[Ingredient] = field(default_factory=list)
    category: str = "Övrigt"
    chef_id: int | None = None
    note: str = ""
    id: int = 0


@dataclass
class PlannedMeal:
    """Ett recept som är inplanerat en viss dag."""
    date: date
    recipe_id: int
    id: int = 0


@dataclass
class ShoppingListItem:
    name: str
    amount: Decimal
    unit: str
