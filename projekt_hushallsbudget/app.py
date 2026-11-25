"""Hushållsbudget. Starta med: flask --app app run --debug

Data ligger i minnet (repository.py) och försvinner när du stoppar programmet.
"""
import os
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

from inputs import parse_date, parse_decimal, parse_int
from models import Member, Transaction
from repository import InMemoryRepository
from services import (MONTH_NAMES, BudgetService, CategoryService, HouseholdService,
                      OverviewService, WarningService, format_money)


def create_app(repo=None) -> Flask:
    app = Flask(__name__)
    # Påhittad utvecklingsnyckel. Den behövs för flash-meddelandena.
    app.secret_key = os.environ.get("SECRET_KEY", "bara-for-lokal-utveckling")

    repo = repo if repo is not None else InMemoryRepository()  # byt den här raden mot er egen databasklass
    categories = CategoryService(repo)
    household = HouseholdService(repo)
    overview = OverviewService(repo)
    budgets = BudgetService(repo)
    warnings = WarningService(budgets)

    app.jinja_env.filters["money"] = format_money
    app.jinja_env.globals["month_name"] = lambda m: MONTH_NAMES[m - 1]

    def selected_month() -> tuple[int, int]:
        """Läser ?year=&month= och faller tillbaka på innevarande månad."""
        today = date.today()
        try:
            year = parse_int(request.values.get("year", str(today.year)), 2000, 2100, "Året")
            month = parse_int(request.values.get("month", str(today.month)), 1, 12, "Månaden")
        except ValueError as error:
            flash(str(error), "error")
            return today.year, today.month
        return year, month

    def month_nav(year: int, month: int) -> dict:
        previous = (year, month - 1) if month > 1 else (year - 1, 12)
        following = (year, month + 1) if month < 12 else (year + 1, 1)
        return {"year": year, "month": month, "previous": previous, "next": following}

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/transactions")
    def transactions():
        year, month = selected_month()
        return render_template("transactions.html", nav=month_nav(year, month), endpoint="transactions",
                               transactions=repo.get_transactions_for_month(year, month))

    @app.route("/transactions/create", methods=["GET", "POST"])
    def transaction_create():
        form = {"type": "expense", "amount": "", "date": date.today().isoformat(), "category": "", "note": ""}
        errors: list[str] = []
        if request.method == "POST":
            form = {key: request.form.get(key, "") for key in form}
            amount = day = None
            try:
                amount = parse_decimal(form["amount"])
                if amount <= 0:
                    errors.append("Beloppet måste vara större än 0.")
            except ValueError as error:
                errors.append(str(error))
            try:
                day = parse_date(form["date"])
            except ValueError as error:
                errors.append(str(error))
            if not form["category"]:
                errors.append("Välj en kategori.")
            if not errors:
                signed = -amount if form["type"] == "expense" else amount
                saved = repo.add_transaction(Transaction(signed, day, form["category"], form["note"].strip()))
                flash(f"Transaktionen är sparad ({saved.category}, {saved.date.isoformat()}).", "success")
                for warning in warnings.check(saved):
                    flash(warning, "warning")
                return redirect(url_for("transaction_create"))
        return render_template("transaction_create.html", form=form, errors=errors,
                               categories=categories.get_all())

    @app.route("/transactions/<int:transaction_id>/delete", methods=["GET", "POST"])
    def transaction_delete(transaction_id: int):
        transaction = repo.get_transaction(transaction_id)
        if transaction is None:
            flash("Transaktionen finns inte.", "error")
            return redirect(url_for("transactions"))
        month_url = url_for("transactions", year=transaction.date.year, month=transaction.date.month)
        if request.method == "POST":
            repo.delete_transaction(transaction_id)
            flash("Transaktionen är borttagen.", "success")
            return redirect(month_url)
        detail = f"{transaction.date.isoformat()}, {transaction.category}, {format_money(abs(transaction.amount))}"
        return render_template("confirm_delete.html", what="transaktionen", detail=detail, cancel_url=month_url)

    @app.get("/overview")
    def overview_page():
        year, month = selected_month()
        return render_template("overview.html", nav=month_nav(year, month), endpoint="overview_page",
                               overview=overview.get_overview(year, month))

    @app.route("/budget", methods=["GET", "POST"])
    def budget():
        year, month = selected_month()
        if request.method == "POST":
            try:
                category_id = parse_int(request.form.get("category_id", ""), 1, 10**9, "Kategorin")
                amount = parse_decimal(request.form.get("amount", ""))
                budgets.set_budget(category_id, year, month, amount)
                flash("Budgeten är sparad.", "success")
            except ValueError as error:
                flash(str(error), "error")
            return redirect(url_for("budget", year=year, month=month))
        return render_template("budget.html", nav=month_nav(year, month), endpoint="budget",
                               statuses=budgets.get_status(year, month), categories=categories.get_all())

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
                               note='Transaktionerna i kategorin flyttas till "Övrigt".',
                               cancel_url=url_for("categories_page"))

    @app.route("/household", methods=["GET", "POST"])
    def household_page():
        form = {"first_name": "", "last_name": "", "birth_date": "", "hair_color": "", "height_cm": "",
                "religion": ""}
        errors: list[str] = []
        if request.method == "POST":
            form = {key: request.form.get(key, "").strip() for key in form}
            try:
                member = Member(
                    first_name=form["first_name"],
                    last_name=form["last_name"],
                    birth_date=parse_date(form["birth_date"], "Födelsedatumet") if form["birth_date"] else None,
                    hair_color=form["hair_color"],
                    height_cm=parse_int(form["height_cm"], 0, 300, "Längden") if form["height_cm"] else None,
                    religion=form["religion"],
                )
                household.add_member(member)
                flash(f"{member.first_name} är tillagd i hushållet.", "success")
                return redirect(url_for("household_page"))
            except ValueError as error:
                errors.append(str(error))
        return render_template("household.html", household=repo.get_household(), members=repo.get_members(),
                               form=form, errors=errors)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("not_found.html"), 404

    return app


app = create_app()
