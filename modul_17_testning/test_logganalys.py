import unittest

import logganalys


class TestLogganalys(unittest.TestCase):
    def test_parse_line(self):
        result = logganalys.parse_line("2026-11-02 08:01:12 INFO inloggning: användare anna_p loggade in")
        self.assertIsNotNone(result)

    def test_parse_garbage(self):
        logganalys.parse_line("skräp")

    def test_read_log(self):
        entries = logganalys.read_log("data/app.log")
        self.assertTrue(entries)

    def test_count_by_level(self):
        entries = logganalys.read_log("data/app.log")
        counts = logganalys.count_by_level(entries)
        self.assertIsNotNone(counts)

    def test_top_errors(self):
        entries = logganalys.read_log("data/app.log")
        self.assertIsNotNone(logganalys.top_errors(entries))


if __name__ == "__main__":
    unittest.main()
