"""Tester. Kör med: uv run --with "flask>=3.0" python -m unittest"""
import unittest
from datetime import date
from decimal import Decimal

from app import create_app
from models import Chef, Ingredient, Recipe
from repository import InMemoryRepository
from services import (CategoryService, ChefService, MealPlanService, RecipeService, WarningService,
                      format_amount, scale_ingredients, week_of)


class FormatAmountTest(unittest.TestCase):
    def test_inga_onodiga_nollor(self):
        self.assertEqual(format_amount(Decimal("1.50"), "dl"), "1,5 dl")
        self.assertEqual(format_amount(Decimal("2.00"), "st"), "2 st")
        self.assertEqual(format_amount(Decimal("0.25"), "tsk"), "0,25 tsk")

    def test_hogst_tva_decimaler(self):
        self.assertEqual(format_amount(Decimal("1.2345"), "dl"), "1,23 dl")


class ScaleTest(unittest.TestCase):
    def test_pannkakor_for_tva_portioner(self):
        pancakes = InMemoryRepository().get_recipes()[0]
        self.assertEqual(pancakes.name, "Pannkakor")
        flour = scale_ingredients(pancakes, 2)[0]
        self.assertEqual(format_amount(flour.amount, flour.unit), "1,25 dl")

    def test_originalet_andras_inte(self):
        pancakes = InMemoryRepository().get_recipes()[0]
        scale_ingredients(pancakes, 2)
        self.assertEqual(pancakes.ingredients[0].amount, Decimal("2.5"))


class RecipeTest(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.recipes = RecipeService(self.repo)

    def test_sok_pa_ingrediens(self):
        self.assertEqual([r.name for r in self.recipes.search("MJÖL")], ["Pannkakor"])

    def test_recept_utan_namn_ger_fel(self):
        with self.assertRaises(ValueError):
            self.recipes.add(Recipe("  ", 4))

    def test_okand_kategori_ger_fel(self):
        with self.assertRaises(ValueError):
            self.recipes.add(Recipe("Gröt", 2, category="Finns inte"))


class CategoryTest(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.categories = CategoryService(self.repo)

    def test_tom_kategori_ger_fel(self):
        with self.assertRaises(ValueError):
            self.categories.add(" ")

    def test_ovrigt_kan_inte_tas_bort(self):
        ovrigt = next(c for c in self.categories.get_all() if c.name == "Övrigt")
        with self.assertRaises(ValueError):
            self.categories.delete(ovrigt.id)

    def test_recept_flyttas_till_ovrigt(self):
        grill = self.categories.add("Grill")
        RecipeService(self.repo).add(Recipe("Burgare", 4, category="Grill"))
        RecipeService(self.repo).add(Recipe("Korv", 4, category="Grill"))
        self.categories.delete(grill.id)
        moved = [r for r in self.repo.get_recipes() if r.name in ("Burgare", "Korv")]
        self.assertEqual([r.category for r in moved], ["Övrigt", "Övrigt"])

    def test_gransen_maste_vara_mellan_1_och_21(self):
        with self.assertRaises(ValueError):
            self.categories.set_weekly_limit(1, 0)


class ChefTest(unittest.TestCase):
    def test_hogst_fem_kockar(self):
        service = ChefService(InMemoryRepository())  # en finns redan
        for name in ("A", "B", "C", "D"):
            service.add(Chef(first_name=name))
        with self.assertRaises(ValueError):
            service.add(Chef(first_name="E"))


class MealPlanTest(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.plan = MealPlanService(self.repo)
        self.pancakes = next(r for r in self.repo.get_recipes() if r.name == "Pannkakor")

    def test_sondag_hor_till_veckan_som_slutar_pa_sondagen(self):
        self.plan.plan(self.pancakes.id, date(2026, 11, 15))  # söndag
        self.assertEqual(week_of(date(2026, 11, 15)), (2026, 46))
        self.assertEqual(len(self.plan.get_week_plan(2026, 46)), 1)
        self.assertEqual(len(self.plan.get_week_plan(2026, 47)), 0)

    def test_inkopslistan_summerar_samma_ingrediens_och_enhet(self):
        items = {i.name: format_amount(i.amount, i.unit) for i in self.plan.get_shopping_list(2026, 48)}
        self.assertEqual(items["vetemjöl"], "5 dl")
        self.assertEqual(items["mjölk"], "12 dl")
        self.assertEqual(items["salt"], "0,5 tsk")
        self.assertEqual(items["gul lök"], "1 st")

    def test_okant_recept_ger_fel(self):
        with self.assertRaises(ValueError):
            self.plan.plan(999, date(2026, 11, 23))


class WarningTest(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()  # Efterrätt har gränsen 5 och två pannkaksmåltider i vecka 48
        self.plan = MealPlanService(self.repo)
        self.warnings = WarningService(self.repo)
        self.pancakes = next(r for r in self.repo.get_recipes() if r.name == "Pannkakor")

    def test_varning_vid_80_procent_och_100_procent(self):
        third = self.plan.plan(self.pancakes.id, date(2026, 11, 24))
        self.assertEqual(self.warnings.check(third), [])  # 3 av 5
        fourth = self.plan.plan(self.pancakes.id, date(2026, 11, 25))
        self.assertIn("80 %", self.warnings.check(fourth)[0])  # 4 av 5
        fifth = self.plan.plan(self.pancakes.id, date(2026, 11, 26))
        self.assertIn("100 %", self.warnings.check(fifth)[0])  # 5 av 5

    def test_samma_varning_visas_bara_en_gang_per_vecka(self):
        self.plan.plan(self.pancakes.id, date(2026, 11, 24))
        fourth = self.plan.plan(self.pancakes.id, date(2026, 11, 25))
        self.assertEqual(len(self.warnings.check(fourth)), 1)
        self.assertEqual(self.warnings.check(fourth), [])

    def test_ny_vecka_ger_ny_varning(self):
        for day in (date(2026, 12, 1), date(2026, 12, 2), date(2026, 12, 3)):
            self.plan.plan(self.pancakes.id, day)
        last = self.plan.plan(self.pancakes.id, date(2026, 12, 4))
        self.assertEqual(len(self.warnings.check(last)), 1)


class PagesTest(unittest.TestCase):
    def setUp(self):
        self.client = create_app(InMemoryRepository()).test_client()

    def test_alla_sidor_svarar(self):
        for url in ("/", "/recipes", "/recipes?q=mjölk", "/recipes/create", "/recipes/1", "/recipes/1?servings=2",
                    "/chefs", "/categories", "/mealplan?year=2026&week=48", "/shoppinglist?year=2026&week=48"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_okant_recept_ger_404(self):
        self.assertEqual(self.client.get("/recipes/999").status_code, 404)

    def test_omrakning_visas(self):
        text = self.client.get("/recipes/1?servings=2").get_data(as_text=True)
        self.assertIn("1,25 dl", text)

    def test_spara_recept(self):
        response = self.client.post("/recipes/create", follow_redirects=True, data={
            "name": "Gröt", "servings": "2", "category": "Frukost", "chef_id": "1", "note": "",
            "ing_name": ["havregryn", ""], "ing_amount": ["2,5", ""], "ing_unit": ["dl", ""]})
        text = response.get_data(as_text=True)
        self.assertIn("Gröt&#34; är sparat.", text)
        self.assertIn("2,5 dl havregryn", text)

    def test_ogiltig_mangd_visar_fel_och_sparar_inget(self):
        client = create_app(InMemoryRepository()).test_client()
        response = client.post("/recipes/create", data={
            "name": "Gröt", "servings": "2", "category": "Frukost", "chef_id": "",  "note": "",
            "ing_name": ["havregryn"], "ing_amount": ["abc"], "ing_unit": ["dl"]})
        self.assertIn("ingen giltig mängd", response.get_data(as_text=True))
        self.assertNotIn("Gröt", client.get("/recipes").get_data(as_text=True))

    def test_avbruten_borttagning_lamnar_receptet(self):
        self.assertEqual(self.client.get("/recipes/1/delete").status_code, 200)  # frågan "Är du säker?"
        self.assertIn("Pannkakor", self.client.get("/recipes").get_data(as_text=True))

    def test_bekraftad_borttagning_tar_bort_receptet(self):
        response = self.client.post("/recipes/1/delete", follow_redirects=True)
        self.assertIn("är borttaget", response.get_data(as_text=True))

    def test_planera_maltid_ger_varning_vid_gransen(self):
        for day in ("2026-11-24", "2026-11-25"):
            response = self.client.post("/mealplan", follow_redirects=True,
                                        data={"recipe_id": "1", "date": day})
        self.assertIn("80 %", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
