# app/models/types.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict

class Move(str, Enum):
    COOPERATE = "cooperate"
    DEFECT = "defect"

@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
@dataclass
class RoundResult:
    round_number: int
    player1_move: Move
    player2_move: Move
    player1_reasoning: str
    player2_reasoning: str
    player1_score: int
    player2_score: int
    # New AI-specific fields
    token_usage: Optional[TokenUsage] = None
    api_errors: Optional[str] = None

@dataclass
class PayoffMatrix:
    cooperate_cooperate: tuple[int, int]
    cooperate_defect: tuple[int, int]
    defect_cooperate: tuple[int, int]
    defect_defect: tuple[int, int]