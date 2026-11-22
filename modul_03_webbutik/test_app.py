import unittest

from app import app


class TestWebshop(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_add_to_cart_redirects_and_counts(self):
        response = self.client.post("/lagg-till", data={"product_id": "1"})
        self.assertEqual(response.status_code, 302)
        page = self.client.get("/").get_data(as_text=True)
        self.assertIn("Varukorg (1)", page)

    def test_unknown_product_is_ignored(self):
        self.client.post("/lagg-till", data={"product_id": "999"})
        page = self.client.get("/").get_data(as_text=True)
        self.assertIn("Varukorg (0)", page)

    def test_paying_with_empty_cart_goes_back_to_shop(self):
        response = self.client.post("/betala")
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
