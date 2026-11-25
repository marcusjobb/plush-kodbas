"""Tester. Kör med: python -m unittest"""
import unittest
from decimal import Decimal

from app import create_app
from repository import InMemoryRepository
from services import (BudgetService, CategoryService, HouseholdService, OverviewService,
                      WarningService, format_money)
from models import BudgetLevel, Member, Transaction
from datetime import date


class FormatMoneyTest(unittest.TestCase):
    def test_tusentalsavskiljare_och_decimalkomma(self):
        self.assertEqual(format_money(Decimal("1249.5")), "1 249,50 kr")

    def test_litet_belopp(self):
        self.assertEqual(format_money(Decimal("5")), "5,00 kr")


class OverviewTest(unittest.TestCase):
    def test_november_summor_och_sista_oktober_hamnar_i_oktober(self):
        overview = OverviewService(InMemoryRepository()).get_overview(2026, 11)
        self.assertEqual(overview.total_income, Decimal("28500"))
        self.assertEqual(overview.total_expenses, Decimal("13538.50"))
        self.assertEqual(overview.balance, Decimal("14961.50"))

    def test_oktober_har_bara_fikat(self):
        overview = OverviewService(InMemoryRepository()).get_overview(2026, 10)
        self.assertEqual(overview.total_expenses, Decimal("100"))


class BudgetTest(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.budgets = BudgetService(self.repo)

    def test_nivaer_i_november(self):
        levels = {s.category_name: (s.percent, s.level) for s in self.budgets.get_status(2026, 11)}
        self.assertEqual(levels["Boende"], (81, BudgetLevel.WARNING))
        self.assertEqual(levels["Nöje"], (79, BudgetLevel.OK))
        self.assertEqual(levels["El och internet"], (112, BudgetLevel.EXCEEDED))

    def test_budget_noll_eller_mindre_ger_fel(self):
        with self.assertRaises(ValueError):
            self.budgets.set_budget(1, 2026, 12, Decimal("0"))

    def test_varning_visas_en_gang_per_manad(self):
        warnings = WarningService(self.budgets)
        t = self.repo.add_transaction(Transaction(Decimal("-100"), date(2026, 11, 21), "Nöje"))
        self.assertEqual(warnings.check(t), ["Nöje är på 89 % av budgeten."])
        t2 = self.repo.add_transaction(Transaction(Decimal("-10"), date(2026, 11, 22), "Nöje"))
        self.assertEqual(warnings.check(t2), [])


class CategoryTest(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.categories = CategoryService(self.repo)

    def test_tom_kategori_ger_fel(self):
        with self.assertRaises(ValueError):
            self.categories.add("  ")

    def test_ovrigt_kan_inte_tas_bort(self):
        ovrigt = next(c for c in self.categories.get_all() if c.name == "Övrigt")
        with self.assertRaises(ValueError):
            self.categories.delete(ovrigt.id)

    def test_transaktioner_flyttas_till_ovrigt(self):
        nojet = next(c for c in self.categories.get_all() if c.name == "Nöje")
        self.categories.delete(nojet.id)
        moved = [t for t in self.repo.get_transactions_for_month(2026, 11) if t.note == "Konsertbiljetter"]
        self.assertEqual(moved[0].category, "Övrigt")


class HouseholdTest(unittest.TestCase):
    def test_hogst_fem_medlemmar(self):
        service = HouseholdService(InMemoryRepository())  # två finns redan
        for name in ("A", "B", "C"):
            service.add_member(Member(first_name=name))
        with self.assertRaises(ValueError):
            service.add_member(Member(first_name="D"))


class PagesTest(unittest.TestCase):
    def setUp(self):
        self.client = create_app(InMemoryRepository()).test_client()

    def test_alla_sidor_svarar(self):
        for url in ("/", "/transactions?year=2026&month=11", "/overview?year=2026&month=11",
                    "/budget?year=2026&month=11", "/categories", "/household", "/transactions/create"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_okand_sida_ger_404(self):
        self.assertEqual(self.client.get("/finns-inte").status_code, 404)

    def test_spara_transaktion_och_fa_varning(self):
        response = self.client.post("/transactions/create", follow_redirects=True, data={
            "type": "expense", "amount": "100", "date": "2026-11-21", "category": "Nöje", "note": ""})
        text = response.get_data(as_text=True)
        self.assertIn("Transaktionen är sparad", text)
        self.assertIn("Nöje är på 89 % av budgeten.", text)

    def test_ogiltigt_belopp_visar_fel_och_sparar_inte(self):
        response = self.client.post("/transactions/create", data={
            "type": "expense", "amount": "abc", "date": "2026-11-21", "category": "Mat", "note": ""})
        self.assertIn("inget giltigt belopp", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
