"""Logiken. Här bor reglerna: omräkning, kategorier, veckoplan, inköpslista, varningar.
Pratar bara med repository-objektet."""
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal

from models import Category, Chef, Ingredient, LimitLevel, PlannedMeal, Recipe, ShoppingListItem

OTHER = "Övrigt"
MAX_CHEFS = 5
WEEKDAYS = ["måndag", "tisdag", "onsdag", "torsdag", "fredag", "lördag", "söndag"]
MONTHS = ["januari", "februari", "mars", "april", "maj", "juni", "juli",
          "augusti", "september", "oktober", "november", "december"]


def format_amount(amount: Decimal, unit: str) -> str:
    """Högst två decimaler och inga onödiga nollor: 1,5 dl, 2 st, 0,25 tsk."""
    rounded = Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    text = f"{rounded:f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return f"{text.replace('.', ',')} {unit}"


def format_date(day: date) -> str:
    return f"{WEEKDAYS[day.weekday()]} {day.day} {MONTHS[day.month - 1]}"


def scale_ingredients(recipe: Recipe, servings: int) -> list[Ingredient]:
    """2,5 dl för 4 portioner blir 1,25 dl för 2 portioner."""
    factor = Decimal(servings) / Decimal(recipe.servings)
    return [Ingredient(i.name, i.amount * factor, i.unit) for i in recipe.ingredients]


def week_of(day: date) -> tuple[int, int]:
    """(ISO-år, ISO-vecka). Veckan börjar på måndag och slutar på söndag."""
    iso = day.isocalendar()
    return iso.year, iso.week


def monday_of(year: int, week: int) -> date:
    return date.fromisocalendar(year, week, 1)  # ValueError om veckan inte finns


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
        self._repo.move_recipes(category.name, OTHER)
        self._repo.delete_category(category_id)
        return category

    def set_weekly_limit(self, category_id: int, weekly_limit: int) -> Category:
        category = self._repo.get_category(category_id)
        if category is None:
            raise ValueError("Kategorin finns inte.")
        if not 1 <= weekly_limit <= 21:
            raise ValueError("Gränsen måste vara ett heltal mellan 1 och 21.")
        self._repo.set_category_limit(category_id, weekly_limit)
        return category


class ChefService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def add(self, chef: Chef) -> Chef:
        if not chef.first_name.strip():
            raise ValueError("Kocken måste ha ett förnamn.")
        if len(self._repo.get_chefs()) >= MAX_CHEFS:
            raise ValueError(f"Programmet klarar högst {MAX_CHEFS} kockar.")
        return self._repo.add_chef(chef)


class RecipeService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def add(self, recipe: Recipe) -> Recipe:
        recipe.name = recipe.name.strip()
        if not recipe.name:
            raise ValueError("Receptet måste ha ett namn.")
        if not 1 <= recipe.servings <= 100:
            raise ValueError("Antal portioner måste vara ett heltal mellan 1 och 100.")
        if not any(c.name == recipe.category for c in self._repo.get_categories()):
            raise ValueError("Välj en kategori som finns.")
        if recipe.chef_id is not None and self._repo.get_chef(recipe.chef_id) is None:
            raise ValueError("Kocken finns inte.")
        return self._repo.add_recipe(recipe)

    def search(self, text: str) -> list[Recipe]:
        text = (text or "").strip()
        return self._repo.search_by_ingredient(text) if text else self._repo.get_recipes()


class MealPlanService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def plan(self, recipe_id: int, day: date) -> PlannedMeal:
        if self._repo.get_recipe(recipe_id) is None:
            raise ValueError("Receptet finns inte.")
        return self._repo.add_meal(PlannedMeal(day, recipe_id))

    def get_week_plan(self, year: int, week: int) -> list[tuple[PlannedMeal, Recipe | None]]:
        return [(m, self._repo.get_recipe(m.recipe_id)) for m in self._repo.get_meals_for_week(year, week)]

    def get_shopping_list(self, year: int, week: int) -> list[ShoppingListItem]:
        """Samma ingrediens med samma enhet summeras till en rad."""
        items: dict[tuple[str, str], ShoppingListItem] = {}
        for _meal, recipe in self.get_week_plan(year, week):
            if recipe is None:
                continue
            for ingredient in recipe.ingredients:
                key = (ingredient.name.lower(), ingredient.unit.lower())
                if key in items:
                    items[key].amount += ingredient.amount
                else:
                    items[key] = ShoppingListItem(ingredient.name, ingredient.amount, ingredient.unit)
        return list(items.values())


class WarningService:
    """Varnar när en kategori når 80 % och 100 % av veckans gräns. Samma varning visas bara en gång per vecka."""

    def __init__(self, repo) -> None:
        self._repo = repo
        self._shown: set[tuple[str, int, int, LimitLevel]] = set()

    def check(self, meal: PlannedMeal) -> list[str]:
        recipe = self._repo.get_recipe(meal.recipe_id)
        category = next((c for c in self._repo.get_categories() if recipe and c.name == recipe.category), None)
        if category is None or category.weekly_limit is None:
            return []
        year, week = week_of(meal.date)
        count = 0
        for planned in self._repo.get_meals_for_week(year, week):
            planned_recipe = self._repo.get_recipe(planned.recipe_id)
            if planned_recipe is not None and planned_recipe.category == category.name:
                count += 1
        if count >= category.weekly_limit:
            level = LimitLevel.REACHED
        elif count * 100 >= category.weekly_limit * 80:
            level = LimitLevel.WARNING
        else:
            return []
        key = (category.name, year, week, level)
        if key in self._shown:
            return []
        self._shown.add(key)
        return [f"{category.name} är på {level.value} % av gränsen ({count} av {category.weekly_limit} per vecka)."]
