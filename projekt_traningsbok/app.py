"""Träningsbok. Starta med: flask --app app run --debug

Data ligger i minnet (repository.py) och försvinner när du stoppar programmet.
"""
import os
from datetime import date, timedelta

from flask import Flask, flash, redirect, render_template, request, url_for

from inputs import parse_date, parse_decimal, parse_int
from models import Athlete, Exercise, Workout
from repository import InMemoryRepository
from services import (AthleteService, GoalNotifier, StatisticsService, TrainingTypeService,
                      WorkoutService, format_duration, format_weight, week_bounds, week_of)


def create_app(repo=None) -> Flask:
    app = Flask(__name__)
    # Påhittad utvecklingsnyckel. Den behövs för flash-meddelandena.
    app.secret_key = os.environ.get("SECRET_KEY", "bara-for-lokal-utveckling")

    repo = repo if repo is not None else InMemoryRepository()  # byt den här raden mot er egen databasklass
    training_types = TrainingTypeService(repo)
    athletes = AthleteService(repo)
    workouts = WorkoutService(repo)
    statistics = StatisticsService(repo)
    goals = GoalNotifier(repo, statistics)

    app.jinja_env.filters["weight"] = format_weight
    app.jinja_env.filters["duration"] = format_duration

    def selected_week() -> tuple[int, int]:
        """Läser ?year=&week= och faller tillbaka på innevarande vecka."""
        year, week = week_of(date.today())
        try:
            year = parse_int(request.values.get("year", str(year)), 2000, 2100, "Året")
            week = parse_int(request.values.get("week", str(week)), 1, 53, "Veckan")
            week_bounds(year, week)
        except ValueError as error:
            flash(str(error), "error")
            return week_of(date.today())
        return year, week

    def week_nav(year: int, week: int) -> dict:
        monday, _ = week_bounds(year, week)
        return {"year": year, "week": week,
                "previous": week_of(monday - timedelta(days=7)), "next": week_of(monday + timedelta(days=7))}

    def athlete_name(athlete_id):
        found = next((a for a in repo.get_athletes() if a.id == athlete_id), None)
        return found.first_name if found else ""

    app.jinja_env.globals["athlete_name"] = athlete_name

    @app.get("/")
    def index():
        return render_template("index.html")

    # --- Pass ---

    @app.get("/workouts")
    def workout_list():
        return render_template("workouts.html", workouts=repo.get_workouts())

    @app.route("/workouts/create", methods=["GET", "POST"])
    def workout_create():
        form = {"date": date.today().isoformat(), "training_type": "", "duration": "", "note": "",
                "athlete_id": ""}
        errors: list[str] = []
        if request.method == "POST":
            form = {key: request.form.get(key, "").strip() for key in form}
            try:
                workout = Workout(
                    date=parse_date(form["date"]),
                    training_type=form["training_type"],
                    duration_minutes=parse_int(form["duration"], 1, 1440, "Längden"),
                    note=form["note"],
                    athlete_id=int(form["athlete_id"]) if form["athlete_id"].isdigit() else None,
                )
                saved = workouts.add_workout(workout)
                flash(f"Passet den {saved.date.isoformat()} är sparat.", "success")
                for message in goals.check(saved):
                    flash(message, "warning")
                return redirect(url_for("workout_details", workout_id=saved.id))
            except ValueError as error:
                errors.append(str(error))
        return render_template("workout_create.html", form=form, errors=errors,
                               training_types=training_types.get_all(), athletes=repo.get_athletes())

    @app.route("/workouts/<int:workout_id>", methods=["GET", "POST"])
    def workout_details(workout_id: int):
        workout = repo.get_workout(workout_id)
        if workout is None:
            flash(f"Det finns inget pass med nummer {workout_id}.", "error")
            return redirect(url_for("workout_list"))
        form = {"name": "", "sets": "", "reps": "", "weight": ""}
        errors: list[str] = []
        if request.method == "POST":
            form = {key: request.form.get(key, "").strip() for key in form}
            if not form["name"]:
                errors.append("Övningen måste ha ett namn.")
            for key, minimum, maximum, label in (("sets", 1, 100, "Antal set"), ("reps", 1, 1000, "Antal reps")):
                try:
                    parse_int(form[key], minimum, maximum, label)
                except ValueError as error:
                    errors.append(str(error))
            weight = None
            try:
                weight = parse_decimal(form["weight"], "vikt")
                if not 0 <= weight <= 1000:
                    errors.append("Vikten måste vara mellan 0 och 1000 kg.")
            except ValueError as error:
                errors.append(str(error))
            if not errors:
                workouts.add_exercise(workout_id, Exercise(form["name"], int(form["sets"]), int(form["reps"]),
                                                           weight))
                flash(f'Övningen "{form["name"]}" är tillagd.', "success")
                return redirect(url_for("workout_details", workout_id=workout_id))
        return render_template("workout_details.html", workout=workout, form=form, errors=errors)

    @app.route("/workouts/<int:workout_id>/delete", methods=["GET", "POST"])
    def workout_delete(workout_id: int):
        workout = repo.get_workout(workout_id)
        if workout is None:
            flash("Passet finns inte.", "error")
            return redirect(url_for("workout_list"))
        if request.method == "POST":
            repo.delete_workout(workout_id)
            flash(f"Passet den {workout.date.isoformat()} är borttaget.", "success")
            return redirect(url_for("workout_list"))
        return render_template("confirm_delete.html", what="passet",
                               detail=f"{workout.date.isoformat()}, {workout.training_type}",
                               cancel_url=url_for("workout_list"))

    # --- Översikt och statistik ---

    @app.get("/overview")
    def overview_page():
        year, week = selected_week()
        return render_template("overview.html", nav=week_nav(year, week),
                               overview=statistics.get_week_overview(year, week))

    @app.get("/exercisestats")
    def exercise_stats():
        name = request.args.get("name", "")
        stats = None
        if name:
            try:
                stats = statistics.get_exercise_stats(name)
            except ValueError as error:
                flash(str(error), "error")
        names = sorted({e.name for w in repo.get_workouts() for e in w.exercises}, key=str.lower)
        return render_template("exercise_stats.html", name=name, stats=stats, names=names)

    # --- Träningstyper ---

    @app.route("/trainingtypes", methods=["GET", "POST"])
    def training_types_page():
        if request.method == "POST":
            try:
                added = training_types.add(request.form.get("name", ""))
                flash(f'Träningstypen "{added.name}" är tillagd.', "success")
            except ValueError as error:
                flash(str(error), "error")
            return redirect(url_for("training_types_page"))
        return render_template("training_types.html", training_types=training_types.get_all())

    @app.post("/trainingtypes/<int:type_id>/goal")
    def training_type_goal(type_id: int):
        try:
            minutes = parse_int(request.form.get("minutes", ""), 1, 10080, "Veckomålet")
            training_types.set_weekly_goal(type_id, minutes)
            flash("Veckomålet är sparat.", "success")
        except ValueError as error:
            flash(str(error), "error")
        return redirect(url_for("training_types_page"))

    @app.route("/trainingtypes/<int:type_id>/delete", methods=["GET", "POST"])
    def training_type_delete(type_id: int):
        training_type = repo.get_training_type(type_id)
        if training_type is None:
            flash("Träningstypen finns inte.", "error")
            return redirect(url_for("training_types_page"))
        if request.method == "POST":
            try:
                training_types.delete(type_id)
                flash(f'Träningstypen "{training_type.name}" är borttagen.', "success")
            except ValueError as error:
                flash(str(error), "error")
            return redirect(url_for("training_types_page"))
        return render_template("confirm_delete.html", what="träningstypen", detail=training_type.name,
                               note='Passen i träningstypen flyttas till "Övrigt".',
                               cancel_url=url_for("training_types_page"))

    # --- Utövare ---

    @app.route("/athletes", methods=["GET", "POST"])
    def athletes_page():
        form = {"first_name": "", "last_name": "", "birth_date": "", "hair_color": "", "height_cm": "",
                "religion": ""}
        errors: list[str] = []
        if request.method == "POST":
            form = {key: request.form.get(key, "").strip() for key in form}
            try:
                athlete = Athlete(
                    first_name=form["first_name"],
                    last_name=form["last_name"],
                    birth_date=parse_date(form["birth_date"], "Födelsedatumet") if form["birth_date"] else None,
                    hair_color=form["hair_color"],
                    height_cm=parse_int(form["height_cm"], 0, 300, "Längden") if form["height_cm"] else None,
                    religion=form["religion"],
                )
                athletes.add(athlete)
                flash(f"Utövaren {athlete.first_name} är tillagd.", "success")
                return redirect(url_for("athletes_page"))
            except ValueError as error:
                errors.append(str(error))
        return render_template("athletes.html", athletes=repo.get_athletes(), form=form, errors=errors)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("not_found.html"), 404

    return app


app = create_app()
