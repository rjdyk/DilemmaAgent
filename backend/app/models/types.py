# app/models/types.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
from datetime import datetime


class Move(str, Enum):
    COOPERATE = "cooperate"
    DEFECT = "defect"

@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
class RoundResult:
    round_number: int
    player1_move: Move
    player2_move: Move
    player1_reasoning: str
    player2_reasoning: str
    player1_score: int
    player2_score: int
    cumulative_player1_score: int  # New field
    cumulative_player2_score: int  # New field
    token_usage: Optional[TokenUsage] = None
    api_errors: Optional[str] = None


@dataclass
class OptimalStrategy:
    cooperation_rate: float  # Optimal % of cooperation
    expected_score_per_round: Tuple[float, float]  # Expected scores when both play optimally
    description: str  # Description of optimal strategy

@dataclass
class PayoffMatrix:
    cooperate_cooperate: Tuple[int, int]
    cooperate_defect: Tuple[int, int]
    defect_cooperate: Tuple[int, int]
    defect_defect: Tuple[int, int]
    optimal_strategy: OptimalStrategy

@dataclass
class ExperimentMetrics:
    cooperation_rate: float
    points_below_optimal: float
    learning_rate: float
    avg_score: float
    total_rounds: int

@dataclass
class GameResult:
    game_id: str
    rounds: List[RoundResult]
    final_scores: Tuple[int, int]
    cooperation_rate: float
    total_rounds: int

@dataclass
class ExperimentResult:
    experiment_id: str
    matrix_type: str  # e.g., "baseline", "mild_penalty", etc.
    player1_strategy: str
    player2_strategy: str
    payoff_matrix: PayoffMatrix
    start_time: datetime
    end_time: datetime
    games: List[GameResult]
    metrics: ExperimentMetrics

class MatrixType(Enum):
    BASELINE = "baseline"  # Classic prisoner's dilemma
    MIXED_30 = "mixed_30"  # 30% cooperation is optimal
    MIXED_70 = "mixed_70"  # 70% cooperation is optimal
    PURE_DEFECT = "pure_defect"  # Pure defection dominates
    STAG_HUNT = "stag_hunt"  # Two Nash equilibria: (C,C) and (D,D)


MATRIX_PAYOFFS = {
    MatrixType.BASELINE: PayoffMatrix(
        cooperate_cooperate=(3, 3),
        cooperate_defect=(0, 5),
        defect_cooperate=(5, 0),
        defect_defect=(1, 1),
        optimal_strategy=OptimalStrategy(
            cooperation_rate=0.0,
            expected_score_per_round=(1, 1),
            description="Pure defection is dominant strategy"
        )
    ),
    MatrixType.MIXED_30: PayoffMatrix(
        cooperate_cooperate=(4, 4),
        cooperate_defect=(-2, 8),
        defect_cooperate=(8, -2),
        defect_defect=(0, 0),
        optimal_strategy=OptimalStrategy(
            cooperation_rate=0.3,
            expected_score_per_round=(2.4, 2.4),  # Expected value when both play 30% cooperate
            description="Mixed strategy: Cooperate 30% of time"
        )
    ),
    MatrixType.MIXED_70: PayoffMatrix(
        cooperate_cooperate=(3, 3),
        cooperate_defect=(-1, 4),
        defect_cooperate=(4, -1),
        defect_defect=(-2, -2),
        optimal_strategy=OptimalStrategy(
            cooperation_rate=0.7,
            expected_score_per_round=(2.1, 2.1),
            description="Mixed strategy: Cooperate 70% of time"
        )
    ),
    MatrixType.PURE_DEFECT: PayoffMatrix(
        cooperate_cooperate=(1, 1),
        cooperate_defect=(-3, 6),
        defect_cooperate=(6, -3),
        defect_defect=(4, 4),
        optimal_strategy=OptimalStrategy(
            cooperation_rate=0.0,
            expected_score_per_round=(4, 4),
            description="Pure defection strongly dominates"
        )
    ),
    MatrixType.STAG_HUNT: PayoffMatrix(
        cooperate_cooperate=(5, 5),
        cooperate_defect=(0, 3),
        defect_cooperate=(3, 0),
        defect_defect=(3, 3),
        optimal_strategy=OptimalStrategy(
            cooperation_rate=1.0,  # (C,C) is payoff-dominant equilibrium
            expected_score_per_round=(5, 5),
            description="Two pure Nash equilibria: (C,C) is payoff-dominant, (D,D) is risk-dominant"
        )
    )
}