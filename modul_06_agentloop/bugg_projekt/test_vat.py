import unittest

from vat import vat_breakdown


class TestVatBreakdown(unittest.TestCase):
    def test_one_item(self):
        self.assertEqual(vat_breakdown([("Kaffe", 100, 25)]), {25: 25.0})

    def test_two_items_with_same_rate_are_summed(self):
        items = [("Kaffe", 100, 25), ("Mugg", 60, 25)]
        self.assertEqual(vat_breakdown(items), {25: 40.0})

    def test_different_rates_are_kept_apart(self):
        items = [("Kaffe", 100, 25), ("Bok", 100, 6)]
        self.assertEqual(vat_breakdown(items), {25: 25.0, 6: 6.0})


if __name__ == "__main__":
    unittest.main()
