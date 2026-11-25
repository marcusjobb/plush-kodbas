"""Datalagret. Allt som sparas och läses går genom den här klassen.

InMemoryRepository är en låtsasdatabas: data ligger i listor och försvinner när programmet stängs.
Resten av programmet (services.py och app.py) anropar bara metoderna nedan, så den som vill ha en riktig
databas skriver en ny klass med samma metoder och byter en rad i app.py.
"""
from datetime import date

from models import Match, Player, Position, Team

DEFAULT_POSITIONS = ["Målvakt", "Back", "Mittfält", "Forward", "Övrigt"]


class InMemoryRepository:
    def __init__(self, seed: bool = True) -> None:
        self._teams: list[Team] = []
        self._players: list[Player] = []
        self._positions: list[Position] = []
        self._matches: list[Match] = []
        self._limits: dict[tuple[int, int], int] = {}  # (lag-id, säsong) -> största antal spelare
        self._next_team_id = 1
        self._next_player_id = 1
        self._next_position_id = 1
        self._next_match_id = 1
        for name in DEFAULT_POSITIONS:
            self.add_position(name)
        if seed:
            self._seed()

    # --- Lag ---

    def get_teams(self) -> list[Team]:
        return list(self._teams)

    def get_team(self, team_id: int) -> Team | None:
        return next((t for t in self._teams if t.id == team_id), None)

    def add_team(self, name: str) -> Team:
        team = Team(id=self._next_team_id, name=name)
        self._next_team_id += 1
        self._teams.append(team)
        return team

    # --- Spelare ---

    def get_players(self, team_id: int) -> list[Player]:
        return [p for p in self._players if p.team_id == team_id]

    def add_player(self, player: Player) -> Player:
        player.id = self._next_player_id
        self._next_player_id += 1
        self._players.append(player)
        return player

    def move_players(self, from_position: str, to_position: str) -> None:
        for player in self._players:
            if player.position == from_position:
                player.position = to_position

    # --- Positioner ---

    def get_positions(self) -> list[Position]:
        return list(self._positions)

    def get_position(self, position_id: int) -> Position | None:
        return next((p for p in self._positions if p.id == position_id), None)

    def add_position(self, name: str) -> Position:
        position = Position(id=self._next_position_id, name=name)
        self._next_position_id += 1
        self._positions.append(position)
        return position

    def delete_position(self, position_id: int) -> None:
        self._positions = [p for p in self._positions if p.id != position_id]

    # --- Matcher ---

    def get_matches(self) -> list[Match]:
        return sorted(self._matches, key=lambda m: (m.date, m.id))

    def get_matches_for_season(self, season: int) -> list[Match]:
        """Säsongen är kalenderåret: 1 januari till och med 31 december."""
        return [m for m in self.get_matches() if m.date.year == season]

    def get_match(self, match_id: int) -> Match | None:
        return next((m for m in self._matches if m.id == match_id), None)

    def add_match(self, match: Match) -> Match:
        match.id = self._next_match_id
        self._next_match_id += 1
        self._matches.append(match)
        return match

    def delete_match(self, match_id: int) -> None:
        self._matches = [m for m in self._matches if m.id != match_id]

    # --- Truppgränser ---

    def get_limits(self, season: int) -> dict[int, int]:
        """Lag-id -> största antal spelare, för de lag som har en gräns den säsongen."""
        return {team_id: maximum for (team_id, s), maximum in self._limits.items() if s == season}

    def set_limit(self, team_id: int, season: int, max_players: int) -> None:
        self._limits[(team_id, season)] = max_players

    # --- Exempeldata. Alla namn och resultat är påhittade. ---

    def _seed(self) -> None:
        for name in ("Ummis IF", "Bryggeriet BK", "Kontoret FF", "Lagret United"):
            self.add_team(name)

        players = [
            (1, "Alex", "Exempelsson", "Målvakt"), (1, "Robin", "Påhittad", "Back"),
            (1, "Kim", "Testsson", "Mittfält"), (1, "Sam", "Demosson", "Forward"),
            (2, "Charlie", "Exempelsson", "Målvakt"), (2, "Noa", "Påhittad", "Forward"),
            (3, "Love", "Testsson", "Back"), (3, "Mika", "Demosson", "Övrigt"),
            (4, "Ellis", "Exempelsson", "Mittfält"), (4, "Juno", "Påhittad", "Back"),
            (4, "Tove", "Testsson", "Forward"), (4, "Vide", "Demosson", "Målvakt"),
        ]
        for team_id, first_name, last_name, position in players:
            self.add_player(Player(team_id, first_name, last_name, position))

        matches = [
            (1, 2, 2, 1, date(2026, 5, 3)), (3, 4, 0, 0, date(2026, 5, 10)),
            (2, 3, 3, 1, date(2026, 5, 17)), (4, 1, 1, 2, date(2026, 5, 24)),
            (1, 3, 1, 1, date(2026, 6, 7)), (4, 2, 2, 2, date(2026, 6, 14)),
        ]
        for home, away, home_goals, away_goals, day in matches:
            self.add_match(Match(home, away, home_goals, away_goals, day))

        for team_id, maximum in {1: 20, 2: 18, 3: 18, 4: 5}.items():
            self.set_limit(team_id, 2026, maximum)
