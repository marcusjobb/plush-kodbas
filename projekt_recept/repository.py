"""Datalagret. Allt som sparas och läses går genom den här klassen.

InMemoryRepository är en låtsasdatabas: data ligger i listor och försvinner när programmet stängs.
Resten av programmet (services.py och app.py) anropar bara metoderna nedan, så den som vill ha en riktig
databas skriver en ny klass med samma metoder och byter en rad i app.py.
"""
from datetime import date, timedelta
from decimal import Decimal

from models import Category, Chef, Ingredient, PlannedMeal, Recipe

DEFAULT_CATEGORIES = ["Frukost", "Lunch", "Middag", "Efterrätt", "Bakning", "Övrigt"]


class InMemoryRepository:
    def __init__(self, seed: bool = True) -> None:
        self._chefs: list[Chef] = []
        self._recipes: list[Recipe] = []
        self._categories: list[Category] = []
        self._meals: list[PlannedMeal] = []
        self._next_chef_id = 1
        self._next_recipe_id = 1
        self._next_category_id = 1
        self._next_meal_id = 1
        for name in DEFAULT_CATEGORIES:
            self.add_category(name)
        if seed:
            self._seed()

    # --- Kockar ---

    def get_chefs(self) -> list[Chef]:
        return list(self._chefs)

    def get_chef(self, chef_id: int) -> Chef | None:
        return next((c for c in self._chefs if c.id == chef_id), None)

    def add_chef(self, chef: Chef) -> Chef:
        chef.id = self._next_chef_id
        self._next_chef_id += 1
        self._chefs.append(chef)
        return chef

    # --- Recept ---

    def get_recipes(self) -> list[Recipe]:
        return sorted(self._recipes, key=lambda r: r.name.lower())

    def get_recipe(self, recipe_id: int) -> Recipe | None:
        return next((r for r in self._recipes if r.id == recipe_id), None)

    def add_recipe(self, recipe: Recipe) -> Recipe:
        recipe.id = self._next_recipe_id
        self._next_recipe_id += 1
        self._recipes.append(recipe)
        return recipe

    def delete_recipe(self, recipe_id: int) -> None:
        self._recipes = [r for r in self._recipes if r.id != recipe_id]
        self._meals = [m for m in self._meals if m.recipe_id != recipe_id]

    def search_by_ingredient(self, text: str) -> list[Recipe]:
        needle = text.lower()
        return [r for r in self.get_recipes() if any(needle in i.name.lower() for i in r.ingredients)]

    def move_recipes(self, from_category: str, to_category: str) -> None:
        for recipe in self._recipes:
            if recipe.category == from_category:
                recipe.category = to_category

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

    def set_category_limit(self, category_id: int, weekly_limit: int) -> None:
        category = self.get_category(category_id)
        if category is not None:
            category.weekly_limit = weekly_limit

    # --- Veckoplan ---

    def add_meal(self, meal: PlannedMeal) -> PlannedMeal:
        meal.id = self._next_meal_id
        self._next_meal_id += 1
        self._meals.append(meal)
        return meal

    def get_meals_for_week(self, year: int, week: int) -> list[PlannedMeal]:
        """Måndag till söndag i ISO-vecka `week` (ISO-året kan skilja från kalenderåret kring nyår)."""
        monday = date.fromisocalendar(year, week, 1)
        sunday = monday + timedelta(days=6)
        found = [m for m in self._meals if monday <= m.date <= sunday]
        return sorted(found, key=lambda m: (m.date, m.id))

    # --- Exempeldata. Alla namn och recept är påhittade. ---

    def _seed(self) -> None:
        kim = self.add_chef(Chef(first_name="Kim", last_name="Exempelsson"))
        by_name = {c.name: c.id for c in self._categories}
        self.set_category_limit(by_name["Efterrätt"], 5)

        pancakes = self.add_recipe(Recipe(
            name="Pannkakor", servings=4, category="Efterrätt", chef_id=kim.id,
            note="Låt smeten vila en stund.",
            ingredients=[
                Ingredient("vetemjöl", Decimal("2.5"), "dl"),
                Ingredient("mjölk", Decimal("6"), "dl"),
                Ingredient("ägg", Decimal("3"), "st"),
                Ingredient("salt", Decimal("0.25"), "tsk"),
            ]))
        soup = self.add_recipe(Recipe(
            name="Tomatsoppa", servings=2, category="Lunch", chef_id=kim.id,
            ingredients=[
                Ingredient("krossade tomater", Decimal("400"), "g"),
                Ingredient("gul lök", Decimal("1"), "st"),
                Ingredient("grönsaksbuljong", Decimal("3"), "dl"),
            ]))

        # Veckoplan för vecka 48 2026 (23–29 november): måndag, torsdag och söndag.
        monday = date.fromisocalendar(2026, 48, 1)
        self.add_meal(PlannedMeal(monday, soup.id))
        self.add_meal(PlannedMeal(monday + timedelta(days=3), pancakes.id))
        self.add_meal(PlannedMeal(monday + timedelta(days=6), pancakes.id))
