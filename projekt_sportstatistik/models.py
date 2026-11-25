"""Modellerna: vad programmet handlar om. Inga beroenden, bara data."""
from dataclasses import dataclass
from datetime import date
from enum import Enum


class SquadLevel(Enum):
    OK = "ok"              # under 80 % av truppgränsen
    WARNING = "warning"    # 80 % eller mer
    FULL = "full"          # 100 % eller mer


@dataclass
class Team:
    id: int
    name: str


@dataclass
class Player:
    team_id: int
    first_name: str
    last_name: str = ""
    position: str = "Övrigt"
    birth_date: date | None = None
    hair_color: str = ""
    height_cm: int | None = None
    religion: str = ""
    id: int = 0


@dataclass
class Position:
    id: int
    name: str


@dataclass
class Match:
    home_team_id: int
    away_team_id: int
    home_goals: int
    away_goals: int
    date: date
    note: str = ""
    id: int = 0


@dataclass
class SquadLimit:
    team_id: int
    season: int
    max_players: int


@dataclass
class StandingRow:
    team_id: int
    team_name: str
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    @property
    def points(self) -> int:
        return self.won * 3 + self.drawn
