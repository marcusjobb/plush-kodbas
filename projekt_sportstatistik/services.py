"""Logiken. Här bor reglerna: tabell, truppgränser, varningar. Pratar bara med repository-objektet."""
from models import Match, Player, Position, SquadLevel, StandingRow, Team

OTHER = "Övrigt"


def format_result(home_goals: int, away_goals: int) -> str:
    """2 och 1 blir "2–1" (med tankstreck)."""
    return f"{home_goals}–{away_goals}"


def format_goal_difference(difference: int) -> str:
    """Alltid med tecken: +3, -2 och 0."""
    return f"+{difference}" if difference > 0 else str(difference)


class TeamService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def add(self, name: str) -> Team:
        name = (name or "").strip()
        if not name:
            raise ValueError("Laget måste ha ett namn.")
        if any(t.name.lower() == name.lower() for t in self._repo.get_teams()):
            raise ValueError(f'Laget "{name}" finns redan.')
        return self._repo.add_team(name)


class PlayerService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def add(self, player: Player) -> Player:
        if self._repo.get_team(player.team_id) is None:
            raise ValueError("Laget finns inte.")
        if not player.first_name.strip():
            raise ValueError("Spelaren måste ha ett förnamn.")
        if player.position not in [p.name for p in self._repo.get_positions()]:
            raise ValueError("Välj en position.")
        return self._repo.add_player(player)


class PositionService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def get_all(self) -> list[Position]:
        return self._repo.get_positions()

    def add(self, name: str) -> Position:
        name = (name or "").strip()
        if not name:
            raise ValueError("Positionen måste ha ett namn.")
        if any(p.name.lower() == name.lower() for p in self._repo.get_positions()):
            raise ValueError(f'Positionen "{name}" finns redan.')
        return self._repo.add_position(name)

    def delete(self, position_id: int) -> Position:
        position = self._repo.get_position(position_id)
        if position is None:
            raise ValueError("Positionen finns inte.")
        if position.name == OTHER:
            raise ValueError(f'Positionen "{OTHER}" kan inte tas bort.')
        self._repo.move_players(position.name, OTHER)
        self._repo.delete_position(position_id)
        return position


class MatchService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def add(self, match: Match) -> Match:
        if self._repo.get_team(match.home_team_id) is None or self._repo.get_team(match.away_team_id) is None:
            raise ValueError("Välj både hemmalag och bortalag.")
        if match.home_team_id == match.away_team_id:
            raise ValueError("Ett lag kan inte möta sig självt.")
        return self._repo.add_match(match)


class StandingsService:
    def __init__(self, repo) -> None:
        self._repo = repo

    def get_standings(self, season: int) -> list[StandingRow]:
        """Tabellen för ett kalenderår. Vinst ger 3 poäng, oavgjort 1 och förlust 0."""
        names = {t.id: t.name for t in self._repo.get_teams()}
        rows: dict[int, StandingRow] = {}
        for match in self._repo.get_matches_for_season(season):
            for team_id, goals_for, goals_against in (
                    (match.home_team_id, match.home_goals, match.away_goals),
                    (match.away_team_id, match.away_goals, match.home_goals)):
                row = rows.setdefault(team_id, StandingRow(team_id, names.get(team_id, "(okänt lag)")))
                row.played += 1
                row.goals_for += goals_for
                row.goals_against += goals_against
                if goals_for > goals_against:
                    row.won += 1
                elif goals_for == goals_against:
                    row.drawn += 1
                else:
                    row.lost += 1
        return sorted(rows.values(), key=lambda r: (-r.points, -r.goal_difference, -r.goals_for, r.team_name))


def level_for(players: int, maximum: int) -> SquadLevel:
    if players >= maximum:
        return SquadLevel.FULL
    if players * 100 >= maximum * 80:
        return SquadLevel.WARNING
    return SquadLevel.OK


class SquadLimitService:
    """Truppgräns per lag och säsong. Varnar vid 80 % och 100 %, en gång per säsong och nivå."""

    def __init__(self, repo) -> None:
        self._repo = repo
        self._shown: set[tuple[int, int, SquadLevel]] = set()

    def get_limits(self, season: int) -> dict[int, int]:
        return self._repo.get_limits(season)

    def set_limit(self, team_id: int, season: int, max_players: int) -> None:
        if max_players < 1:
            raise ValueError("Truppgränsen måste vara minst 1.")
        if self._repo.get_team(team_id) is None:
            raise ValueError("Laget finns inte.")
        self._repo.set_limit(team_id, season, max_players)

    def check(self, team_id: int, season: int) -> list[str]:
        maximum = self._repo.get_limits(season).get(team_id)
        team = self._repo.get_team(team_id)
        if maximum is None or team is None:
            return []
        players = len(self._repo.get_players(team_id))
        level = level_for(players, maximum)
        key = (team_id, season, level)
        if level == SquadLevel.OK or key in self._shown:
            return []
        self._shown.add(key)
        if level == SquadLevel.FULL:
            return [f"{team.name} har nått truppgränsen ({players} av {maximum})."]
        return [f"{team.name} är på {players * 100 // maximum} % av truppgränsen."]
