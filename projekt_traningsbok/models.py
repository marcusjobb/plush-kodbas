"""Modellerna: vad programmet handlar om. Inga beroenden, bara data."""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum


class GoalLevel(Enum):
    NONE = "none"          # inget mål satt, eller under 80 %
    WARNING = "warning"    # 80 % eller mer av veckomålet
    REACHED = "reached"    # 100 % eller mer


@dataclass
class Athlete:
    first_name: str
    last_name: str = ""
    birth_date: date | None = None
    hair_color: str = ""
    height_cm: int | None = None
    religion: str = ""
    id: int = 0


@dataclass
class TrainingType:
    id: int
    name: str
    weekly_goal_minutes: int | None = None


@dataclass
class Exercise:
    name: str
    sets: int
    reps: int
    weight: Decimal
    id: int = 0


@dataclass
class Workout:
    date: date
    training_type: str
    duration_minutes: int
    note: str = ""
    athlete_id: int | None = None
    exercises: list[Exercise] = field(default_factory=list)
    id: int = 0


@dataclass
class ExerciseStats:
    exercise_name: str
    max_weight: Decimal
    total_sets: int


@dataclass
class TrainingTypeMinutes:
    training_type_name: str
    minutes: int
    goal_minutes: int | None = None


@dataclass
class WeekOverview:
    year: int
    week: int
    start: date   # måndag
    end: date     # söndag
    workout_count: int
    total_minutes: int
    minutes_per_type: list[TrainingTypeMinutes] = field(default_factory=list)
