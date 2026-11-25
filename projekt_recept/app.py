"""Recept. Starta med: flask --app app run --debug

Data ligger i minnet (repository.py) och försvinner när du stoppar programmet.
"""
import os
from datetime import date, timedelta

from flask import Flask, flash, redirect, render_template, request, url_for

from inputs import parse_date, parse_decimal, parse_int
from models import Chef, Ingredient, Recipe
from repository import InMemoryRepository
from services import (CategoryService, ChefService, MealPlanService, RecipeService, WarningService,
                      format_amount, format_date, monday_of, scale_ingredients, week_of)

INGREDIENT_ROWS = 5


def create_app(repo=None) -> Flask:
    app = Flask(__name__)
    # Påhittad utvecklingsnyckel. Den behövs för flash-meddelandena.
    app.secret_key = os.environ.get("SECRET_KEY", "bara-for-lokal-utveckling")

    repo = repo if repo is not None else InMemoryRepository()  # byt den här raden mot er egen databasklass
    categories = CategoryService(repo)
    chefs = ChefService(repo)
    recipes = RecipeService(repo)
    meal_plan = MealPlanService(repo)
    warnings = WarningService(repo)

    app.jinja_env.filters["amount"] = lambda ingredient: format_amount(ingredient.amount, ingredient.unit)
    app.jinja_env.filters["long_date"] = format_date

    def selected_week() -> tuple[int, int]:
        """Läser ?year=&week= och faller tillbaka på innevarande vecka."""
        year, week = week_of(date.today())
        try:
            year = parse_int(request.values.get("year", str(year)), 2000, 2100, "Året")
            week = parse_int(request.values.get("week", str(week)), 1, 53, "Veckan")
        except ValueError as error:
            flash(str(error), "error")
            return week_of(date.today())
        try:
            monday_of(year, week)
        except ValueError:
            flash(f"Vecka {week} finns inte år {year}.", "error")
            return week_of(date.today())
        return year, week

    def week_nav(year: int, week: int) -> dict:
        monday = monday_of(year, week)
        return {"year": year, "week": week,
                "previous": week_of(monday - timedelta(days=7)), "next": week_of(monday + timedelta(days=7))}

    @app.get("/")
    def index():
        return render_template("index.html")

    # --- Recept ---

    @app.get("/recipes")
    def recipe_list():
        query = request.args.get("q", "").strip()
        chef_names = {c.id: c.first_name for c in repo.get_chefs()}
        return render_template("recipes.html", recipes=recipes.search(query), query=query, chef_names=chef_names)

    @app.route("/recipes/create", methods=["GET", "POST"])
    def recipe_create():
        form = {"name": "", "servings": "4", "category": "Övrigt", "chef_id": "", "note": "",
                "rows": [{"name": "", "amount": "", "unit": ""} for _ in range(INGREDIENT_ROWS)]}
        errors: list[str] = []
        if request.method == "POST":
            names = request.form.getlist("ing_name")
            amounts = request.form.getlist("ing_amount")
            units = request.form.getlist("ing_unit")
            form = {key: request.form.get(key, "").strip() for key in ("name", "servings", "category", "chef_id", "note")}
            form["rows"] = [{"name": n, "amount": a, "unit": u} for n, a, u in zip(names, amounts, units)]
            ingredients: list[Ingredient] = []
            for number, row in enumerate(form["rows"], start=1):
                if not (row["name"].strip() or row["amount"].strip() or row["unit"].strip()):
                    continue
                try:
                    if not row["name"].strip():
                        raise ValueError(f"Rad {number}: ingrediensen saknar namn.")
                    amount = parse_decimal(row["amount"])
                    if amount <= 0:
                        raise ValueError(f"Rad {number}: mängden måste vara större än 0.")
                    if not row["unit"].strip():
                        raise ValueError(f"Rad {number}: skriv en enhet, till exempel dl.")
                    ingredients.append(Ingredient(row["name"].strip(), amount, row["unit"].strip()))
                except ValueError as error:
                    message = str(error)
                    errors.append(message if message.startswith("Rad") else f"Rad {number}: {message}")
            try:
                servings = parse_int(form["servings"], 1, 100, "Antal portioner")
                chef_id = int(form["chef_id"]) if form["chef_id"] else None
                if not errors:
                    saved = recipes.add(Recipe(form["name"], servings, ingredients, form["category"],
                                               chef_id, form["note"]))
                    flash(f'Receptet "{saved.name}" är sparat.', "success")
                    return redirect(url_for("recipe_details", recipe_id=saved.id))
            except ValueError as error:
                errors.append(str(error))
        while len(form["rows"]) < INGREDIENT_ROWS:
            form["rows"].append({"name": "", "amount": "", "unit": ""})
        return render_template("recipe_create.html", form=form, errors=errors,
                               categories=categories.get_all(), chefs=repo.get_chefs())

    @app.get("/recipes/<int:recipe_id>")
    def recipe_details(recipe_id: int):
        recipe = repo.get_recipe(recipe_id)
        if recipe is None:
            return render_template("not_found.html"), 404
        shown = recipe.servings
        if "servings" in request.args:
            try:
                shown = parse_int(request.args["servings"], 1, 100, "Antal portioner")
            except ValueError as error:
                flash(str(error), "error")
        chef = repo.get_chef(recipe.chef_id) if recipe.chef_id else None
        return render_template("recipe_details.html", recipe=recipe, shown=shown, chef=chef,
                               ingredients=scale_ingredients(recipe, shown))

    @app.route("/recipes/<int:recipe_id>/delete", methods=["GET", "POST"])
    def recipe_delete(recipe_id: int):
        recipe = repo.get_recipe(recipe_id)
        if recipe is None:
            flash("Receptet finns inte.", "error")
            return redirect(url_for("recipe_list"))
        if request.method == "POST":
            repo.delete_recipe(recipe_id)
            flash(f'"{recipe.name}" är borttaget.', "success")
            return redirect(url_for("recipe_list"))
        return render_template("confirm_delete.html", what="receptet", detail=recipe.name,
                               cancel_url=url_for("recipe_list"))

    # --- Kockar ---

    @app.route("/chefs", methods=["GET", "POST"])
    def chefs_page():
        form = {"first_name": "", "last_name": "", "birth_date": "", "hair_color": "", "height_cm": "",
                "religion": ""}
        errors: list[str] = []
        if request.method == "POST":
            form = {key: request.form.get(key, "").strip() for key in form}
            try:
                chef = Chef(
                    first_name=form["first_name"],
                    last_name=form["last_name"],
                    birth_date=parse_date(form["birth_date"], "Födelsedatumet") if form["birth_date"] else None,
                    hair_color=form["hair_color"],
                    height_cm=parse_int(form["height_cm"], 0, 300, "Längden") if form["height_cm"] else None,
                    religion=form["religion"],
                )
                chefs.add(chef)
                flash(f"Kocken {chef.first_name} är tillagd.", "success")
                return redirect(url_for("chefs_page"))
            except ValueError as error:
                errors.append(str(error))
        return render_template("chefs.html", chefs=repo.get_chefs(), form=form, errors=errors)

    # --- Kategorier ---

    @app.route("/categories", methods=["GET", "POST"])
    def categories_page():
        if request.method == "POST":
            try:
                added = categories.add(request.form.get("name", ""))
                flash(f'Kategorin "{added.name}" är tillagd.', "success")
            except ValueError as error:
                flash(str(error), "error")
            return redirect(url_for("categories_page"))
        return render_template("categories.html", categories=categories.get_all())

    @app.post("/categories/<int:category_id>/limit")
    def category_limit(category_id: int):
        try:
            limit = parse_int(request.form.get("limit", ""), 1, 21, "Gränsen")
            category = categories.set_weekly_limit(category_id, limit)
            flash(f"Gränsen för {category.name} är sparad.", "success")
        except ValueError as error:
            flash(str(error), "error")
        return redirect(url_for("categories_page"))

    @app.route("/categories/<int:category_id>/delete", methods=["GET", "POST"])
    def category_delete(category_id: int):
        category = repo.get_category(category_id)
        if category is None:
            flash("Kategorin finns inte.", "error")
            return redirect(url_for("categories_page"))
        if request.method == "POST":
            try:
                categories.delete(category_id)
                flash(f'Kategorin "{category.name}" är borttagen.', "success")
            except ValueError as error:
                flash(str(error), "error")
            return redirect(url_for("categories_page"))
        return render_template("confirm_delete.html", what="kategorin", detail=category.name,
                               note='Recepten i kategorin flyttas till "Övrigt".',
                               cancel_url=url_for("categories_page"))

    # --- Veckoplan och inköpslista ---

    @app.get("/mealplan")
    def mealplan_page():
        year, week = selected_week()
        return render_template("mealplan.html", nav=week_nav(year, week), endpoint="mealplan_page",
                               plan=meal_plan.get_week_plan(year, week), recipes=repo.get_recipes(),
                               default_date=monday_of(year, week).isoformat())

    @app.post("/mealplan")
    def mealplan_plan():
        try:
            recipe_id = parse_int(request.form.get("recipe_id", ""), 1, 10**9, "Receptet")
            day = parse_date(request.form.get("date", ""))
            meal = meal_plan.plan(recipe_id, day)
            flash("Måltiden är inplanerad.", "success")
            for warning in warnings.check(meal):
                flash(warning, "warning")
        except ValueError as error:
            flash(str(error), "error")
            return redirect(url_for("mealplan_page"))
        year, week = week_of(day)
        return redirect(url_for("mealplan_page", year=year, week=week))

    @app.get("/shoppinglist")
    def shoppinglist_page():
        year, week = selected_week()
        return render_template("shoppinglist.html", nav=week_nav(year, week), endpoint="shoppinglist_page",
                               items=meal_plan.get_shopping_list(year, week))

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("not_found.html"), 404

    return app


app = create_app()
