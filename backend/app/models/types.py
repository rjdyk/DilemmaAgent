# app/models/types.py
from enum import Enum
from dataclasses import dataclass


class Move(str, Enum):
    COOPERATE = "cooperate"
    DEFECT = "defect"

@dataclass
class RoundResult:
    round_number: int
    ai_move: Move
    opponent_move: Move
    ai_reasoning: str
    ai_score: int
    opponent_score: int
