import unittest
from datetime import date

from fakturor import berakna_faktura


class TestBeraknaFaktura(unittest.TestCase):
    """Skriv testerna här. Börja med att fånga hur funktionen beter sig just nu."""

    def test_en_vara_privatkund(self):
        # 1 st à 100 kr, 25 % moms, ingen rabatt, ej betald
        self.assertEqual(berakna_faktura([(1, 100)], "privat", date(2026, 12, 1), None), 125.0)


if __name__ == "__main__":
    unittest.main()
