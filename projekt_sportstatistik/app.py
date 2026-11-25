"""Sportstatistik. Starta med: flask --app app run --debug

Data ligger i minnet (repository.py) och försvinner när du stoppar programmet.
"""
import os
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

from inputs import parse_date, parse_int
from models import Match, Player
from repository import InMemoryRepository
from services import (MatchService, PlayerService, PositionService, SquadLimitService, StandingsService,
                      TeamService, format_goal_difference, format_result)


def create_app(repo=None) -> Flask:
    app = Flask(__name__)
    # Påhittad utvecklingsnyckel. Den behövs för flash-meddelandena.
    app.secret_key = os.environ.get("SECRET_KEY", "bara-for-lokal-utveckling")

    repo = repo if repo is not None else InMemoryRepository()  # byt den här raden mot er egen databasklass
    teams = TeamService(repo)
    players = PlayerService(repo)
    positions = PositionService(repo)
    matches = MatchService(repo)
    standings = StandingsService(repo)
    limits = SquadLimitService(repo)

    app.jinja_env.filters["result"] = format_result
    app.jinja_env.filters["goal_difference"] = format_goal_difference

    def team_names() -> dict[int, str]:
        return {t.id: t.name for t in repo.get_teams()}

    def selected_season() -> int:
        """Läser ?year= och faller tillbaka på innevarande år. Säsongen är kalenderåret."""
        try:
            return parse_int(request.values.get("year", str(date.today().year)), 2000, 2100, "Säsongen")
        except ValueError as error:
            flash(str(error), "error")
            return date.today().year

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.route("/teams", methods=["GET", "POST"])
    def teams_page():
        if request.method == "POST":
            try:
                added = teams.add(request.form.get("name", ""))
                flash(f'Laget "{added.name}" är tillagt.', "success")
            except ValueError as error:
                flash(str(error), "error")
            return redirect(url_for("teams_page"))
        counts = {t.id: len(repo.get_players(t.id)) for t in repo.get_teams()}
        return render_template("teams.html", teams=repo.get_teams(), counts=counts)

    @app.route("/teams/<int:team_id>", methods=["GET", "POST"])
    def team_details(team_id: int):
        team = repo.get_team(team_id)
        if team is None:
            return render_template("not_found.html"), 404
        form = {"first_name": "", "last_name": "", "position": "", "birth_date": "", "hair_color": "",
                "height_cm": "", "religion": ""}
        errors: list[str] = []
        if request.method == "POST":
            form = {key: request.form.get(key, "").strip() for key in form}
            try:
                player = Player(
                    team_id=team_id,
                    first_name=form["first_name"],
                    last_name=form["last_name"],
                    position=form["position"],
                    birth_date=parse_date(form["birth_date"], "Födelsedatumet") if form["birth_date"] else None,
                    hair_color=form["hair_color"],
                    height_cm=parse_int(form["height_cm"], 0, 300, "Längden") if form["height_cm"] else None,
                    religion=form["religion"],
                )
                players.add(player)
                flash(f"{player.first_name} är tillagd i {team.name}.", "success")
                for warning in limits.check(team_id, date.today().year):
                    flash(warning, "warning")
                return redirect(url_for("team_details", team_id=team_id))
            except ValueError as error:
                errors.append(str(error))
        return render_template("team_details.html", team=team, players=repo.get_players(team_id),
                               positions=positions.get_all(), form=form, errors=errors)

    @app.get("/matches")
    def matches_page():
        return render_template("matches.html", matches=repo.get_matches(), names=team_names())

    @app.route("/matches/create", methods=["GET", "POST"])
    def match_create():
        form = {"home_team_id": "", "away_team_id": "", "home_goals": "", "away_goals": "",
                "date": date.today().isoformat(), "note": ""}
        errors: list[str] = []
        if request.method == "POST":
            form = {key: request.form.get(key, "").strip() for key in form}
            values: dict = {}
            for key, label, low, high in (("home_team_id", "Hemmalaget", 1, 10**9),
                                          ("away_team_id", "Bortalaget", 1, 10**9),
                                          ("home_goals", "Mål hemma", 0, 99), ("away_goals", "Mål borta", 0, 99)):
                try:
                    values[key] = parse_int(form[key], low, high, label)
                except ValueError as error:
                    errors.append("Välj både hemmalag och bortalag." if high > 99 else
                                  f'"{form[key]}" är inget giltigt värde. {error}')
            try:
                values["date"] = parse_date(form["date"])
            except ValueError as error:
                errors.append(str(error))
            if not errors:
                try:
                    saved = matches.add(Match(note=form["note"], **values))
                    names = team_names()
                    flash(f"Matchen {names[saved.home_team_id]} mot {names[saved.away_team_id]} är sparad.",
                          "success")
                    return redirect(url_for("matches_page"))
                except ValueError as error:
                    errors.append(str(error))
        return render_template("match_create.html", form=form, errors=errors, teams=repo.get_teams())

    @app.route("/matches/<int:match_id>/delete", methods=["GET", "POST"])
    def match_delete(match_id: int):
        match = repo.get_match(match_id)
        if match is None:
            flash("Matchen finns inte.", "error")
            return redirect(url_for("matches_page"))
        if request.method == "POST":
            repo.delete_match(match_id)
            flash("Matchen är borttagen.", "success")
            return redirect(url_for("matches_page"))
        names = team_names()
        detail = (f"{match.date.isoformat()}: {names.get(match.home_team_id, '?')} mot "
                  f"{names.get(match.away_team_id, '?')}, {format_result(match.home_goals, match.away_goals)}")
        return render_template("confirm_delete.html", what="matchen", detail=detail,
                               cancel_url=url_for("matches_page"))

    @app.get("/standings")
    def standings_page():
        season = selected_season()
        return render_template("standings.html", season=season, endpoint="standings_page",
                               rows=standings.get_standings(season))

    @app.route("/squadlimits", methods=["GET", "POST"])
    def squad_limits():
        season = selected_season()
        if request.method == "POST":
            try:
                team_id = parse_int(request.form.get("team_id", ""), 1, 10**9, "Laget")
                maximum = parse_int(request.form.get("max_players", ""), 1, 100, "Truppgränsen")
                limits.set_limit(team_id, season, maximum)
                flash("Truppgränsen är sparad.", "success")
            except ValueError as error:
                flash(str(error), "error")
            return redirect(url_for("squad_limits", year=season))
        counts = {t.id: len(repo.get_players(t.id)) for t in repo.get_teams()}
        return render_template("squad_limits.html", season=season, endpoint="squad_limits",
                               teams=repo.get_teams(), counts=counts, limits=limits.get_limits(season))

    @app.route("/positions", methods=["GET", "POST"])
    def positions_page():
        if request.method == "POST":
            try:
                added = positions.add(request.form.get("name", ""))
                flash(f'Positionen "{added.name}" är tillagd.', "success")
            except ValueError as error:
                flash(str(error), "error")
            return redirect(url_for("positions_page"))
        return render_template("positions.html", positions=positions.get_all())

    @app.route("/positions/<int:position_id>/delete", methods=["GET", "POST"])
    def position_delete(position_id: int):
        position = repo.get_position(position_id)
        if position is None:
            flash("Positionen finns inte.", "error")
            return redirect(url_for("positions_page"))
        if request.method == "POST":
            try:
                positions.delete(position_id)
                flash(f'Positionen "{position.name}" är borttagen.', "success")
            except ValueError as error:
                flash(str(error), "error")
            return redirect(url_for("positions_page"))
        return render_template("confirm_delete.html", what="positionen", detail=position.name,
                               note='Spelarna med positionen flyttas till "Övrigt".',
                               cancel_url=url_for("positions_page"))

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("not_found.html"), 404

    return app


app = create_app()
