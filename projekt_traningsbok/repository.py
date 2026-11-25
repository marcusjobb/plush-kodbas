"""Datalagret. Allt som sparas och läses går genom den här klassen.

InMemoryRepository är en låtsasdatabas: data ligger i listor och försvinner när programmet stängs.
Resten av programmet (services.py och app.py) anropar bara metoderna nedan, så den som vill ha en riktig
databas skriver en ny klass med samma metoder och byter en rad i app.py.
"""
from datetime import date
from decimal import Decimal

from models import Athlete, Exercise, TrainingType, Workout

DEFAULT_TRAINING_TYPES = ["Styrka", "Kondition", "Rörlighet", "Bollsport", "Övrigt"]


class InMemoryRepository:
    def __init__(self, seed: bool = True) -> None:
        self._athletes: list[Athlete] = []
        self._workouts: list[Workout] = []
        self._training_types: list[TrainingType] = []
        self._next_athlete_id = 1
        self._next_workout_id = 1
        self._next_exercise_id = 1
        self._next_type_id = 1
        for name in DEFAULT_TRAINING_TYPES:
            self.add_training_type(name)
        if seed:
            self._seed()

    # --- Utövare ---

    def get_athletes(self) -> list[Athlete]:
        return list(self._athletes)

    def add_athlete(self, athlete: Athlete) -> Athlete:
        athlete.id = self._next_athlete_id
        self._next_athlete_id += 1
        self._athletes.append(athlete)
        return athlete

    # --- Pass och övningar ---

    def get_workouts(self) -> list[Workout]:
        return sorted(self._workouts, key=lambda w: (w.date, w.id))

    def get_workouts_between(self, start: date, end: date) -> list[Workout]:
        """Pass från och med start till och med end."""
        return [w for w in self.get_workouts() if start <= w.date <= end]

    def get_workout(self, workout_id: int) -> Workout | None:
        return next((w for w in self._workouts if w.id == workout_id), None)

    def add_workout(self, workout: Workout) -> Workout:
        workout.id = self._next_workout_id
        self._next_workout_id += 1
        for exercise in workout.exercises:
            exercise.id = self._next_exercise_id
            self._next_exercise_id += 1
        self._workouts.append(workout)
        return workout

    def delete_workout(self, workout_id: int) -> None:
        self._workouts = [w for w in self._workouts if w.id != workout_id]

    def add_exercise(self, workout_id: int, exercise: Exercise) -> Exercise:
        workout = self.get_workout(workout_id)
        if workout is None:
            raise ValueError(f"Det finns inget pass med nummer {workout_id}.")
        exercise.id = self._next_exercise_id
        self._next_exercise_id += 1
        workout.exercises.append(exercise)
        return exercise

    def move_workouts(self, from_type: str, to_type: str) -> None:
        for workout in self._workouts:
            if workout.training_type == from_type:
                workout.training_type = to_type

    # --- Träningstyper och veckomål ---

    def get_training_types(self) -> list[TrainingType]:
        return list(self._training_types)

    def get_training_type(self, type_id: int) -> TrainingType | None:
        return next((t for t in self._training_types if t.id == type_id), None)

    def get_training_type_by_name(self, name: str) -> TrainingType | None:
        return next((t for t in self._training_types if t.name == name), None)

    def add_training_type(self, name: str) -> TrainingType:
        training_type = TrainingType(id=self._next_type_id, name=name)
        self._next_type_id += 1
        self._training_types.append(training_type)
        return training_type

    def delete_training_type(self, type_id: int) -> None:
        self._training_types = [t for t in self._training_types if t.id != type_id]

    def set_weekly_goal(self, type_id: int, minutes: int) -> None:
        training_type = self.get_training_type(type_id)
        if training_type is not None:
            training_type.weekly_goal_minutes = minutes

    # --- Exempeldata. Alla namn och värden är påhittade. ---

    def _seed(self) -> None:
        self.add_athlete(Athlete(first_name="Kim", last_name="Exempelsson"))
        klattring = self.add_training_type("Klättring")
        self.set_weekly_goal(self.get_training_type_by_name("Styrka").id, 120)
        self.set_weekly_goal(self.get_training_type_by_name("Kondition").id, 100)
        self.set_weekly_goal(klattring.id, 90)

        self.add_workout(Workout(date(2026, 11, 12), "Styrka", 65, "Ben", 1, [
            Exercise("Knäböj", 3, 8, Decimal("62.5")),
            Exercise("Marklyft", 3, 5, Decimal("80")),
        ]))
        # En söndag: passet hör till vecka 46, inte vecka 47.
        self.add_workout(Workout(date(2026, 11, 15), "Kondition", 81, "Intervaller", 1))
        self.add_workout(Workout(date(2026, 11, 18), "Styrka", 55, "", 1, [
            Exercise("Knäböj", 4, 6, Decimal("65")),
            Exercise("Bänkpress", 3, 8, Decimal("45")),
        ]))
        self.add_workout(Workout(date(2026, 11, 20), "Rörlighet", 20, "", 1))
