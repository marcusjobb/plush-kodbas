import random
import re
import unittest

import hemlig_tomte_logic as logic
from julgran import MAX_HOJD, MIN_HOJD, bygg_gran


class TestHemligTomte(unittest.TestCase):
    def test_ingen_drar_sig_sjalv_och_alla_far_en(self):
        for seed in range(200):
            for n in range(2, 13):
                names = [f"Person{i}" for i in range(n)]
                result = logic.draw(names, random.Random(seed))
                self.assertTrue(logic.is_valid(result), (seed, n))

    def test_forbjudna_par_respekteras_i_bada_riktningar(self):
        names = ["Anna", "Bo", "Cia", "Dan", "Eva", "Fia"]
        forbidden = [("Anna", "Bo"), ("Cia", "Dan")]
        for seed in range(200):
            result = logic.draw(names, random.Random(seed), forbidden)
            self.assertNotEqual(result["Anna"], "Bo")
            self.assertNotEqual(result["Bo"], "Anna")
            self.assertNotEqual(result["Cia"], "Dan")
            self.assertNotEqual(result["Dan"], "Cia")

    def test_omojligt_ger_fel(self):
        with self.assertRaises(ValueError):
            logic.draw(["Anna", "Bo"], random.Random(1), [("Anna", "Bo")])
        with self.assertRaises(ValueError):
            logic.draw(["A", "B", "C"], random.Random(1), [("A", "B"), ("B", "C"), ("A", "C")])

    def test_for_fa_eller_dubbletter_ger_fel(self):
        with self.assertRaises(ValueError):
            logic.draw(["Anna"], random.Random(1))
        with self.assertRaises(ValueError):
            logic.draw(["Anna", "Anna", "Bo"], random.Random(1))

    def test_samma_slumpfro_ger_samma_lottning(self):
        names = ["Anna", "Bo", "Cia", "Dan"]
        self.assertEqual(logic.draw(names, random.Random(7)), logic.draw(names, random.Random(7)))

    def test_andelen_giltiga_blandningar_narmar_sig_1_genom_e(self):
        share = logic.share_valid_random_shuffles(10, 20000, random.Random(1))
        self.assertAlmostEqual(share, 0.3679, delta=0.02)


class TestJulgran(unittest.TestCase):
    def test_antal_rader_och_bredd(self):
        for hojd in range(MIN_HOJD, MAX_HOJD + 1):
            rader = [re.sub(r"\033\[[0-9;]*m", "", r) for r in bygg_gran(hojd, random.Random(1))]
            self.assertEqual(len(rader), hojd + 3)
            gran, text = rader[:-1], rader[-1]  # sista raden är texten "God Jul!", som kan vara bredare än en liten gran
            self.assertLessEqual(max(len(r) for r in gran), 2 * hojd - 1)
            self.assertEqual(text.strip(), "God Jul!")
            self.assertLessEqual(max(len(r) for r in rader), 100)

    def test_hela_granen_ryms_pa_20_rader(self):
        self.assertLessEqual(len(bygg_gran(MAX_HOJD, random.Random(1))), 20)


if __name__ == "__main__":
    unittest.main()
