"""Tester. Kör med: python -m unittest"""
import unittest
from datetime import date

from app import create_app
from models import Match, Player, SquadLevel
from repository import InMemoryRepository
from services import (MatchService, PlayerService, PositionService, SquadLimitService, StandingsService,
                      TeamService, format_goal_difference, format_result, level_for)


class FormatTest(unittest.TestCase):
    def test_resultat_med_tankstreck(self):
        self.assertEqual(format_result(2, 1), "2–1")

    def test_malskillnad_alltid_med_tecken(self):
        self.assertEqual([format_goal_difference(d) for d in (3, -2, 0)], ["+3", "-2", "0"])


class StandingsTest(unittest.TestCase):
    def test_tabellen_for_2026_ar_sorterad_och_stammer(self):
        rows = StandingsService(InMemoryRepository()).get_standings(2026)
        self.assertEqual([r.team_name for r in rows],
                         ["Ummis IF", "Bryggeriet BK", "Lagret United", "Kontoret FF"])
        self.assertEqual([r.points for r in rows], [7, 4, 2, 2])
        self.assertEqual([r.goal_difference for r in rows], [2, 1, -1, -2])
        self.assertEqual((rows[0].played, rows[0].won, rows[0].drawn, rows[0].lost), (3, 2, 1, 0))
        self.assertEqual((rows[0].goals_for, rows[0].goals_against), (5, 3))

    def test_annan_sasong_ar_tom(self):
        self.assertEqual(StandingsService(InMemoryRepository()).get_standings(2025), [])

    def test_sista_december_hor_till_sin_sasong(self):
        repo = InMemoryRepository()
        MatchService(repo).add(Match(1, 2, 1, 0, date(2026, 12, 31)))
        MatchService(repo).add(Match(1, 2, 1, 0, date(2027, 1, 1)))
        standings = StandingsService(repo)
        self.assertEqual({r.team_name: r.played for r in standings.get_standings(2026)}["Ummis IF"], 4)
        self.assertEqual({r.team_name: r.played for r in standings.get_standings(2027)}, {"Ummis IF": 1,
                                                                                         "Bryggeriet BK": 1})

    def test_lika_poang_sorteras_pa_malskillnad_sedan_gjorda_mal_sedan_namn(self):
        repo = InMemoryRepository(seed=False)
        a, b, c, d = (repo.add_team(n) for n in ("Dd", "Cc", "Bb", "Aa"))
        matches = MatchService(repo)
        matches.add(Match(a.id, c.id, 1, 0, date(2026, 5, 1)))  # Dd +1, 1 gjort
        matches.add(Match(b.id, d.id, 2, 1, date(2026, 5, 1)))  # Cc +1, 2 gjorda
        rows = StandingsService(repo).get_standings(2026)
        self.assertEqual([r.team_name for r in rows], ["Cc", "Dd", "Aa", "Bb"])  # Aa före Bb: -1 men fler gjorda


class MatchTest(unittest.TestCase):
    def setUp(self):
        self.matches = MatchService(InMemoryRepository())

    def test_lag_kan_inte_mota_sig_sjalvt(self):
        with self.assertRaises(ValueError):
            self.matches.add(Match(1, 1, 0, 0, date(2026, 5, 1)))

    def test_okant_lag_ger_fel(self):
        with self.assertRaises(ValueError):
            self.matches.add(Match(1, 99, 0, 0, date(2026, 5, 1)))


class PositionTest(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.positions = PositionService(self.repo)

    def test_tom_position_ger_fel(self):
        with self.assertRaises(ValueError):
            self.positions.add(" ")

    def test_ovrigt_kan_inte_tas_bort(self):
        ovrigt = next(p for p in self.positions.get_all() if p.name == "Övrigt")
        with self.assertRaises(ValueError):
            self.positions.delete(ovrigt.id)

    def test_spelare_flyttas_till_ovrigt(self):
        libero = self.positions.add("Libero")
        PlayerService(self.repo).add(Player(1, "Lo", position="Libero"))
        PlayerService(self.repo).add(Player(1, "Li", position="Libero"))
        self.positions.delete(libero.id)
        moved = [p for p in self.repo.get_players(1) if p.first_name in ("Lo", "Li")]
        self.assertEqual([p.position for p in moved], ["Övrigt", "Övrigt"])


class PlayerAndTeamTest(unittest.TestCase):
    def test_spelare_utan_fornamn_ger_fel(self):
        with self.assertRaises(ValueError):
            PlayerService(InMemoryRepository()).add(Player(1, " "))

    def test_lag_med_samma_namn_ger_fel(self):
        with self.assertRaises(ValueError):
            TeamService(InMemoryRepository()).add("ummis if")


class SquadLimitTest(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.limits = SquadLimitService(self.repo)

    def test_nivaer(self):
        self.assertEqual([level_for(n, 20) for n in (15, 16, 20)],
                         [SquadLevel.OK, SquadLevel.WARNING, SquadLevel.FULL])

    def test_varning_vid_80_procent_visas_en_gang(self):
        self.repo.set_limit(1, 2026, 5)  # Ummis IF har 4 spelare = 80 %
        self.assertEqual(self.limits.check(1, 2026), ["Ummis IF är på 80 % av truppgränsen."])
        self.assertEqual(self.limits.check(1, 2026), [])

    def test_varning_vid_100_procent_ar_en_annan(self):
        self.repo.set_limit(1, 2026, 5)
        self.limits.check(1, 2026)
        PlayerService(self.repo).add(Player(1, "Ny"))
        self.assertEqual(self.limits.check(1, 2026), ["Ummis IF har nått truppgränsen (5 av 5)."])

    def test_ny_sasong_ger_ny_varning(self):
        self.repo.set_limit(1, 2026, 5)
        self.repo.set_limit(1, 2027, 5)
        self.limits.check(1, 2026)
        self.assertEqual(len(self.limits.check(1, 2027)), 1)

    def test_gransen_maste_vara_minst_ett(self):
        with self.assertRaises(ValueError):
            self.limits.set_limit(1, 2026, 0)


class PagesTest(unittest.TestCase):
    def setUp(self):
        self.client = create_app(InMemoryRepository()).test_client()

    def test_alla_sidor_svarar(self):
        for url in ("/", "/teams", "/teams/1", "/matches", "/matches/create", "/standings?year=2026",
                    "/squadlimits?year=2026", "/positions"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_okanda_sidor_ger_404(self):
        for url in ("/finns-inte", "/teams/99"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_tabellen_visar_resultat_och_tecken(self):
        text = self.client.get("/standings?year=2026").get_data(as_text=True)
        self.assertIn("+2", text)
        self.assertIn("-2", text)

    def test_registrera_match(self):
        response = self.client.post("/matches/create", follow_redirects=True, data={
            "home_team_id": "1", "away_team_id": "2", "home_goals": "2", "away_goals": "1",
            "date": "2026-11-12", "note": "Derby"})
        text = response.get_data(as_text=True)
        self.assertIn("är sparad", text)
        self.assertIn("2–1", text)

    def test_ogiltigt_antal_mal_sparar_inte(self):
        response = self.client.post("/matches/create", data={
            "home_team_id": "1", "away_team_id": "2", "home_goals": "abc", "away_goals": "1",
            "date": "2026-11-12", "note": ""})
        self.assertIn("inget giltigt värde", response.get_data(as_text=True))
        self.assertNotIn("Derby", self.client.get("/matches").get_data(as_text=True))

    def test_lag_mot_sig_sjalvt_ger_fel(self):
        response = self.client.post("/matches/create", data={
            "home_team_id": "1", "away_team_id": "1", "home_goals": "0", "away_goals": "0",
            "date": "2026-11-12", "note": ""})
        self.assertIn("Ett lag kan inte möta sig självt.", response.get_data(as_text=True))

    def test_ta_bort_match_kraver_bekraftelse(self):
        self.assertIn("Ta bort matchen?", self.client.get("/matches/1/delete").get_data(as_text=True))
        self.assertEqual(self.client.get("/matches").get_data(as_text=True).count("/delete"), 6)
        self.client.post("/matches/1/delete")
        self.assertEqual(self.client.get("/matches").get_data(as_text=True).count("/delete"), 5)

    def test_ny_spelare_ger_varning_vid_truppgransen(self):
        year = date.today().year
        self.client.post(f"/squadlimits?year={year}", data={"team_id": "1", "max_players": "6"})
        response = self.client.post("/teams/1", follow_redirects=True, data={
            "first_name": "Ny", "position": "Back"})  # 5 av 6 spelare
        self.assertIn("Ummis IF är på 83 % av truppgränsen.", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
