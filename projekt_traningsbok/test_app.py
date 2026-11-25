"""Tester. Kör med: python -m unittest"""
import unittest
from datetime import date
from decimal import Decimal

from app import create_app
from models import Athlete, Exercise, Workout
from repository import InMemoryRepository
from services import (AthleteService, GoalNotifier, StatisticsService, TrainingTypeService,
                      WorkoutService, format_duration, format_weight, week_of)


class FormatTest(unittest.TestCase):
    def test_vikt_med_en_decimal(self):
        self.assertEqual(format_weight(Decimal("62.5")), "62,5 kg")
        self.assertEqual(format_weight(Decimal("65")), "65,0 kg")

    def test_tid_i_timmar_och_minuter(self):
        self.assertEqual(format_duration(65), "1 h 05 min")
        self.assertEqual(format_duration(120), "2 h 00 min")

    def test_under_en_timme_bara_minuter(self):
        self.assertEqual(format_duration(45), "45 min")


class WeekTest(unittest.TestCase):
    def test_sondag_hor_till_samma_vecka_som_veckan_fore(self):
        self.assertEqual(week_of(date(2026, 11, 15)), (2026, 46))  # söndag
        self.assertEqual(week_of(date(2026, 11, 16)), (2026, 47))  # måndag

    def test_oversikt_vecka_46_och_47(self):
        statistics = StatisticsService(InMemoryRepository())
        week46 = statistics.get_week_overview(2026, 46)
        self.assertEqual((week46.workout_count, week46.total_minutes), (2, 146))
        week47 = statistics.get_week_overview(2026, 47)
        self.assertEqual((week47.workout_count, week47.total_minutes), (2, 75))

    def test_ogiltig_vecka_ger_fel(self):
        with self.assertRaises(ValueError):
            StatisticsService(InMemoryRepository()).get_week_overview(2026, 54)


class ExerciseStatsTest(unittest.TestCase):
    def test_hogsta_vikt_och_antal_set(self):
        stats = StatisticsService(InMemoryRepository()).get_exercise_stats("knäböj")
        self.assertEqual(stats.max_weight, Decimal("65"))
        self.assertEqual(stats.total_sets, 7)

    def test_okand_ovning_ger_fel(self):
        with self.assertRaises(ValueError):
            StatisticsService(InMemoryRepository()).get_exercise_stats("Plankan")


class GoalTest(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.notifier = GoalNotifier(self.repo, StatisticsService(self.repo))
        self.workouts = WorkoutService(self.repo)

    def test_81_procent_ger_meddelande_en_gang_per_vecka(self):
        # Kondition har målet 100 min. Vecka 47 har inga konditionspass från början.
        first = self.workouts.add_workout(Workout(date(2026, 11, 17), "Kondition", 75))
        self.assertEqual(self.notifier.check(first), [])  # 75 %
        second = self.workouts.add_workout(Workout(date(2026, 11, 18), "Kondition", 6))
        self.assertEqual(self.notifier.check(second), ["Kondition är på 81 % av veckomålet."])
        third = self.workouts.add_workout(Workout(date(2026, 11, 19), "Kondition", 5))
        self.assertEqual(self.notifier.check(third), [])

    def test_nytt_meddelande_vid_100_procent(self):
        self.notifier.check(self.workouts.add_workout(Workout(date(2026, 11, 17), "Kondition", 85)))
        reached = self.workouts.add_workout(Workout(date(2026, 11, 18), "Kondition", 20))
        self.assertEqual(self.notifier.check(reached), ["Kondition har nått veckomålet."])

    def test_ingen_varning_utan_mal(self):
        workout = self.workouts.add_workout(Workout(date(2026, 11, 17), "Bollsport", 200))
        self.assertEqual(self.notifier.check(workout), [])


class TrainingTypeTest(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.types = TrainingTypeService(self.repo)

    def test_tom_traningstyp_ger_fel(self):
        with self.assertRaises(ValueError):
            self.types.add("  ")

    def test_ovrigt_kan_inte_tas_bort(self):
        ovrigt = self.repo.get_training_type_by_name("Övrigt")
        with self.assertRaises(ValueError):
            self.types.delete(ovrigt.id)

    def test_pass_flyttas_till_ovrigt(self):
        klattring = self.repo.get_training_type_by_name("Klättring")
        WorkoutService(self.repo).add_workout(Workout(date(2026, 11, 21), "Klättring", 60))
        self.types.delete(klattring.id)
        moved = [w for w in self.repo.get_workouts() if w.date == date(2026, 11, 21)]
        self.assertEqual(moved[0].training_type, "Övrigt")

    def test_veckomal_utanfor_gransen_ger_fel(self):
        with self.assertRaises(ValueError):
            self.types.set_weekly_goal(1, 0)


class AthleteTest(unittest.TestCase):
    def test_hogst_fem_utovare(self):
        service = AthleteService(InMemoryRepository())  # en finns redan
        for name in ("A", "B", "C", "D"):
            service.add(Athlete(first_name=name))
        with self.assertRaises(ValueError):
            service.add(Athlete(first_name="E"))


class PagesTest(unittest.TestCase):
    def setUp(self):
        self.client = create_app(InMemoryRepository()).test_client()

    def test_alla_sidor_svarar(self):
        for url in ("/", "/workouts", "/workouts/create", "/workouts/1", "/overview?year=2026&week=46",
                    "/exercisestats?name=Knäböj", "/trainingtypes", "/athletes"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_okand_sida_ger_404(self):
        self.assertEqual(self.client.get("/finns-inte").status_code, 404)

    def test_spara_pass_visar_meddelande_vid_malet(self):
        response = self.client.post("/workouts/create", follow_redirects=True, data={
            "date": "2026-11-17", "training_type": "Kondition", "duration": "85", "note": "", "athlete_id": ""})
        text = response.get_data(as_text=True)
        self.assertIn("är sparat", text)
        self.assertIn("Kondition är på 85 % av veckomålet.", text)

    def test_ogiltig_vikt_sparar_ingen_ovning(self):
        response = self.client.post("/workouts/1", data={"name": "Press", "sets": "3", "reps": "8",
                                                         "weight": "abc"})
        self.assertIn("ingen giltig siffra", response.get_data(as_text=True))
        self.assertNotIn("Press", self.client.get("/workouts/1").get_data(as_text=True))

    def test_avbryt_borttagning_lamnar_passet(self):
        self.client.get("/workouts/1/delete")  # bekräftelsesidan
        self.assertIn("Knäböj", self.client.get("/workouts/1").get_data(as_text=True))

    def test_ja_tar_bort_passet(self):
        self.client.post("/workouts/1/delete")
        self.assertEqual(self.client.get("/workouts/1").status_code, 302)


if __name__ == "__main__":
    unittest.main()
