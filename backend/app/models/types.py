# app/models/types.py
from enum import Enum
from dataclasses import dataclass

class Move(str, Enum):
    COOPERATE = "cooperate"
    DEFECT = "defect"
@dataclass
class RoundResult:
    round_number: int
    player1_move: Move
    player2_move: Move
    player1_reasoning: str
    player2_reasoning: str
    player1_score: int
    player2_score: int