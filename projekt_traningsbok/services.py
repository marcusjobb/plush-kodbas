"""Logiken. Här bor reglerna: veckor, summor, veckomål, meddelanden. Pratar bara med repository-objektet."""
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal

from models import (Athlete, Exercise, ExerciseStats, GoalLevel, TrainingType,
                    TrainingTypeMinutes, WeekOverview, Workout)

OTHER = "Övrigt"
MAX_ATHLETES = 5
MINUTES_PER_WEEK = 7 * 24 * 60


def format_weight(weight: Decimal) -> str:
    """62.5 blir "62,5 kg"."""
    rounded = Decimal(weight).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{rounded:.1f}".replace(".", ",") + " kg"


def format_duration(minutes: int) -> str:
    """65 blir "1 h 05 min". Under en timme: "45 min"."""
    if minutes < 60:
        return f"{minutes} min"
    return f"{minutes // 60} h {minutes % 60:02d} min"


def week_bounds(year: int, week: int) -> tuple[date, date]:
    """Måndag och söndag för en ISO-vecka. Ogiltig vecka ger ValueError."""
    try:
        monday = date.fromisocalendar(year, week, 1)
    except ValueError:
        raise ValueError(f"Vecka {week} finns inte {year}.") from None
    return monday, monday + timedelta(days=6)


def week_of(day: date) -> tuple[int, int]:
    """(ISO-år, veckonummer). Veckan börjar på måndag, så söndag 15 nov 2026 hör till vecka 46."""
    iso = day.isocalendar()
    return iso.year, iso.week


class TrainingTypeService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def get_all(self) -> list[TrainingType]:
        return self._repo.get_training_types()

    def add(self, name: str) -> TrainingType:
        name = (name or "").strip()
        if not name:
            raise ValueError("Träningstypen måste ha ett namn.")
        if any(t.name.lower() == name.lower() for t in self._repo.get_training_types()):
            raise ValueError(f'Träningstypen "{name}" finns redan.')
        return self._repo.add_training_type(name)

    def delete(self, type_id: int) -> TrainingType:
        training_type = self._repo.get_training_type(type_id)
        if training_type is None:
            raise ValueError("Träningstypen finns inte.")
        if training_type.name == OTHER:
            raise ValueError(f'Träningstypen "{OTHER}" kan inte tas bort.')
        self._repo.move_workouts(training_type.name, OTHER)
        self._repo.delete_training_type(type_id)
        return training_type

    def set_weekly_goal(self, type_id: int, minutes: int) -> None:
        if self._repo.get_training_type(type_id) is None:
            raise ValueError("Träningstypen finns inte.")
        if not 1 <= minutes <= MINUTES_PER_WEEK:
            raise ValueError(f"Veckomålet måste vara mellan 1 och {MINUTES_PER_WEEK} minuter.")
        self._repo.set_weekly_goal(type_id, minutes)


class AthleteService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def add(self, athlete: Athlete) -> Athlete:
        if not athlete.first_name.strip():
            raise ValueError("Utövaren måste ha ett förnamn.")
        if len(self._repo.get_athletes()) >= MAX_ATHLETES:
            raise ValueError(f"Programmet klarar högst {MAX_ATHLETES} utövare.")
        return self._repo.add_athlete(athlete)


class WorkoutService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def add_workout(self, workout: Workout) -> Workout:
        if not workout.training_type.strip():
            raise ValueError("Välj en träningstyp.")
        if self._repo.get_training_type_by_name(workout.training_type) is None:
            raise ValueError(f'Träningstypen "{workout.training_type}" finns inte.')
        if not 1 <= workout.duration_minutes <= 1440:
            raise ValueError("Längden måste vara mellan 1 och 1440 minuter.")
        return self._repo.add_workout(workout)

    def add_exercise(self, workout_id: int, exercise: Exercise) -> Exercise:
        if not exercise.name.strip():
            raise ValueError("Övningen måste ha ett namn.")
        return self._repo.add_exercise(workout_id, exercise)


class StatisticsService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def week_minutes_by_type(self, year: int, week: int) -> dict[str, int]:
        start, end = week_bounds(year, week)
        totals: dict[str, int] = {}
        for workout in self._repo.get_workouts_between(start, end):
            totals[workout.training_type] = totals.get(workout.training_type, 0) + workout.duration_minutes
        return totals

    def get_week_overview(self, year: int, week: int) -> WeekOverview:
        start, end = week_bounds(year, week)
        workouts = self._repo.get_workouts_between(start, end)
        goals = {t.name: t.weekly_goal_minutes for t in self._repo.get_training_types()}
        per_type = [TrainingTypeMinutes(name, minutes, goals.get(name))
                    for name, minutes in sorted(self.week_minutes_by_type(year, week).items(),
                                                key=lambda item: -item[1])]
        return WeekOverview(year, week, start, end, len(workouts),
                            sum(w.duration_minutes for w in workouts), per_type)

    def get_exercise_stats(self, name: str) -> ExerciseStats:
        wanted = name.strip().lower()
        if not wanted:
            raise ValueError("Skriv namnet på en övning.")
        found = [e for w in self._repo.get_workouts() for e in w.exercises if e.name.lower() == wanted]
        if not found:
            raise ValueError(f'Det finns ingen övning som heter "{name.strip()}" i något pass.')
        return ExerciseStats(found[0].name, max(e.weight for e in found), sum(e.sets for e in found))


def goal_level(minutes: int, goal: int | None) -> GoalLevel:
    if not goal:
        return GoalLevel.NONE
    if minutes >= goal:
        return GoalLevel.REACHED
    if minutes * 100 >= goal * 80:
        return GoalLevel.WARNING
    return GoalLevel.NONE


class GoalNotifier:
    """Meddelar när en träningstyp når 80 % och 100 % av veckomålet. Samma meddelande visas en gång per vecka."""

    def __init__(self, repo, statistics: StatisticsService) -> None:
        self._repo = repo
        self._statistics = statistics
        self._shown: set[tuple[str, int, int, GoalLevel]] = set()

    def check(self, workout: Workout) -> list[str]:
        training_type = self._repo.get_training_type_by_name(workout.training_type)
        if training_type is None or not training_type.weekly_goal_minutes:
            return []
        year, week = week_of(workout.date)
        minutes = self._statistics.week_minutes_by_type(year, week).get(workout.training_type, 0)
        level = goal_level(minutes, training_type.weekly_goal_minutes)
        if level == GoalLevel.NONE:
            return []
        key = (workout.training_type, year, week, level)
        if key in self._shown:
            return []
        self._shown.add(key)
        if level == GoalLevel.REACHED:
            return [f"{workout.training_type} har nått veckomålet."]
        percent = minutes * 100 // training_type.weekly_goal_minutes
        return [f"{workout.training_type} är på {percent} % av veckomålet."]
