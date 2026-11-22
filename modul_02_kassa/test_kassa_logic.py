import unittest
from decimal import Decimal

import kassa_logic as logic


class TestKassaLogic(unittest.TestCase):
    def test_two_items_with_25_percent_vat(self):
        items = [
            logic.Item("Kaffe", Decimal("100"), 25),
            logic.Item("Mugg", Decimal("100"), 25),
        ]
        self.assertEqual(logic.total_incl_vat(items), Decimal("250.00"))

    def test_empty_list_is_zero(self):
        self.assertEqual(logic.total_incl_vat([]), Decimal("0.00"))


if __name__ == "__main__":
    unittest.main()
